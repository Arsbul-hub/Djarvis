import copy
import json
import multiprocessing
import time
from threading import Thread

import sounddevice as sd
import webrtcvad
from vad import EnergyVAD

from app.services import Service

import pyaudio
import noisereduce as nr
from vosk import Model, KaldiRecognizer, EndpointerMode

from config import RATE, CHUNK
import numpy as np


class Recognizer:
    audio_input = 1
    threshold_level = None

    def __init__(self, state_buffer, shared_buffer, shared_buffer_locks):

        self.state_buffer = state_buffer
        self.shared_buffer = shared_buffer
        self.shared_buffer_locks = shared_buffer_locks
        model = Model(r"./static/stt/model-small_ru")

        self.recognizer = KaldiRecognizer(model, RATE)
        # # For short commands
        # self.recognizer.SetEndpointerMode(EndpointerMode.SHORT)
        #
        # # For longer speech
        # recognizer.SetEndpointerMode(EndpointerMode.LONG)
        #
        # # For very long continuous speech
        # recognizer.SetEndpointerMode(EndpointerMode.VERY_LONG)

        # Custom configuration
        # self.recognizer.SetEndpointerDelays(t_start_max=0.5, t_end=0.3, t_max=10.0)
        # Загрузка аудиофайла в переменную `audio`
        # self.vad = EnergyVAD(
        #     sample_rate=RATE,  # частота дискретизации
        #     frame_length=int(RATE/CHUNK),  # длина кадра в миллисекундах
        #     frame_shift=20,  # смещение кадра в миллисекундах
        #     energy_threshold=0.05,  # порог энергии (может потребовать настройки)
        #     pre_emphasis=0.95  # предварительное усиление
        # )
        self.vad = webrtcvad.Vad()
        # Режим агрессивности: 0 (least aggressive) до 3 (most aggressive)
        self.vad.set_mode(2)
        # self.require_stop = require_stop

        # self.stream.start_stream()
        self.audio = pyaudio.PyAudio()
        self.stream1 = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            output=True,
            # output_device_index=4,
            frames_per_buffer=CHUNK
        )
        self.__temp_threshold_list = []
        self.shared_buffer["text_commands"] = []
        self.noize = np.array([], dtype=np.int16)
    def g(self):
        self.stream1.write(self.noize.tobytes())
    def start(self):
        # if not self.run:
        #    self.run = True
        Thread(target=self.g).start()
        # while True:
        # if self.stream.get_read_available() >= CHUNK:
        # data = self.stream.read(CHUNK, exception_on_overflow=False)
        # if len(data) == 0:
        #     break
        # dt = time.time()

        while self.state_buffer["status"] == "running":


            # print(in_data_bytes)




                # print(self.vad.is_speech(frame_bytes, RATE))


            frames = self.shared_buffer.get("frames")

            if not frames or len(frames) == 0:
                continue
            self.shared_buffer_locks["frames"].acquire()

            try:
                frame = np.array([], dtype=np.int16)

                # print((len(frames) * CHUNK) / RATE)


                for i, f in enumerate(frames):

                    if f.size > 0:
                        #frame = np.append(frame, f)
                        #print(old_chunks, (old_chunks * CHUNK) / RATE)
                        if not self.vad.is_speech(f.tobytes(), RATE):
                            if self.noize.size > RATE * 30:
                                self.noize = self.noize[1:]
                            self.noize = np.append(self.noize, f)
                        frame = np.append(frame, f)

                # frame_bytes = frame.tobytes()



                # Для получения аудиофайла только с речью
                # print(voice_activity)

                self.shared_buffer["frames"] = []

                #
                # t1 = time.time()

                frame = nr.reduce_noise(y=frame, y_noise=self.noize, sr=RATE)

                # self.stream1.write(frame.tobytes())
                # #self.t = frame.tobytes()
                # print(time.time() - t1)
                # print(self.recognizer.PartialResult())
                if self.recognizer.AcceptWaveform(frame.tobytes()):

                    self.shared_buffer_locks["text_commands"].acquire()
                    try:
                        text = json.loads(self.recognizer.Result())["text"]

                        if text:

                            self.shared_buffer["text_commands"] = [text] + self.shared_buffer["text_commands"]
                        # else:
                        #     print(self.recognizer.PartialResult())
                    finally:
                        self.shared_buffer_locks["text_commands"].release()
                # else:
                #print(1)

            finally:
                self.shared_buffer_locks["frames"].release()
                # time.sleep(0.1)

                # self.__temp_threshold_list.clear()
                # self.action(text)

    # return in_data_bytes, pyaudio.paContinue

    # self.loop()

    # def stop(self):
    #     self.run = False
    # def stop(self):
    #     self.stream.stop_stream()
    #     self.stream.close()
