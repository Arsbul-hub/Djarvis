import json
import multiprocessing
import time

import sounddevice as sd
from vad import EnergyVAD
from app.services import Service

import pyaudio

from vosk import Model, KaldiRecognizer
from config import RATE, CHUNK
import numpy as np
import logging


class Recorder:
    audio_input = 1
    threshold_level = None

    def __init__(self, state_buffer, shared_buffer, shared_buffer_locks):

        self.state_buffer = state_buffer
        self.shared_buffer = shared_buffer
        self.shared_buffer_locks = shared_buffer_locks
        # model = Model(r"./static/stt/model-small_ru")
        self.shared_buffer["frames"] = []

        # self.recognizer = KaldiRecognizer(model, RATE)

        self.audio = pyaudio.PyAudio()
        for i in range(self.audio.get_host_api_info_by_index(0).get("deviceCount")):
            dev = self.audio.get_device_info_by_host_api_device_index(0, i)
            if dev["maxInputChannels"] > 0:
                print((i, dev['name'], dev['maxInputChannels']), dev['defaultSampleRate'])
        # self.stream1 = self.audio.open(
        #     format=pyaudio.paInt16,
        #     channels=1,
        #     rate=RATE,
        #     output=True,
        #     # output_device_index=4,
        #     frames_per_buffer=CHUNK
        # )
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            input_device_index=self.audio_input,
            frames_per_buffer=CHUNK,
            stream_callback=self.on_frame
        )

        # self.stream.start_stream()

        self._local_buffer = bytearray()  # Локальный, быстрый буфер
        self._last_sync = time.time()
        self.__temp_threshold_list = []
        self.lost_frames = []


        # self.vad = EnergyVAD(
        #     sample_rate=RATE,  # частота дискретизации
        #     frame_length=int(RATE/CHUNK),  # длина кадра в миллисекундах
        #     frame_shift=20,  # смещение кадра в миллисекундах
        #     energy_threshold=0.05,  # порог энергии (может потребовать настройки)
        #     pre_emphasis=0.95  # предварительное усиление
        # )


    def start(self):
        # if not self.run:
        #    self.run = True
        self.stream.start_stream()

        # self.loop()

    # def stop(self):
    #     self.run = False
    def stop(self):
        self.stream.stop_stream()
        self.stream.close()

    def on_frame(self, in_data_bytes, frame_count, time_info, status):

        #
        # # Копим локально (быстро)
        # self._local_buffer.extend(in_data_bytes)
        #
        # # Синхронизируем с DictProxy раз в 0.5 секунды
        # if time.time() - self._last_sync > 0.5:
        #     try:
        #         self.shared_buffer["frames"] = bytes(self._local_buffer[-16000:])  # Последние 0.5 сек
        #         self._last_sync = time.time()
        #     except Exception as e:
        #         logging.error(f"Sync error: {e}")
        # return in_data_bytes, pyaudio.paContinue
        # while True:
        # if self.stream.get_read_available() >= CHUNK:
        # data = self.stream.read(CHUNK, exception_on_overflow=False)
        # if len(data) == 0:
        #     break

        in_data = np.frombuffer(in_data_bytes, dtype=np.int16)
        #
        # in_data1 = self.vad.apply_vad(np.array([in_data, ]))  # numpy-массив той же формы, что и `audio`
        #
        # self.stream1.write(in_data1.tobytes())
        # if self.threshold_level is None:
        #
        #     self.threshold_level = np.mean(in_data)

        # in_data = in_data[in_data >= self.threshold_level]
        # print(list(in_data))
        # for i in self.shared_buffer["frames"]:
        #     self.stream1.write(i.tobytes())

        if (len(self.lost_frames) * CHUNK) / RATE > 0.03 and self.shared_buffer_locks["frames"].acquire(block=False):

            try:
                # print(f"Выгружено: {len(self.lost_frames)}")
                new_buffer = self.shared_buffer["frames"] + self.lost_frames + [in_data]
                self.shared_buffer["frames"] = new_buffer
                self.lost_frames = []
            finally:

                self.shared_buffer_locks["frames"].release()
        else:
            self.lost_frames = self.lost_frames + [in_data]
        # frame = np.array([], dtype=np.int16)

        # print((len(frames) * CHUNK) / RATE)
        # d =  self.shared_buffer.get("frames")
        # for i, f in enumerate(d):
        #
        #     if f.size > 0:
        #         frame = np.append(frame, f)
        # self.stream1.write(frame.tobytes())
        # if self.recognizer.AcceptWaveform(in_data.tobytes()):
        #     text = json.loads(self.recognizer.Result())["text"]
        #     if text:
        #         # print(text)
        #         # self.__temp_threshold_list.clear()
        #         self.action(text)
        #     else:
        #
        #         self.threshold_level = np.mean(in_data)
        return in_data_bytes, pyaudio.paContinue
