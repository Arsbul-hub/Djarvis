import json
import time

import numpy as np
from vosk import Model, KaldiRecognizer
import pyaudio
import sounddevice as sd

from config import *


class Recognizer:
    run = False
    audio_input = 0
    threshold_level = None

    def __init__(self, action):
        self.action = action
        model = Model(r"./app/stt/model-small_ru")

        self.recognizer = KaldiRecognizer(model, RATE)

        self.audio = pyaudio.PyAudio()
        for i in range(self.audio.get_host_api_info_by_index(0).get("deviceCount")):
            dev = self.audio.get_device_info_by_host_api_device_index(0, i)
            if dev["maxInputChannels"] > 0:
                print((i, dev['name'], dev['maxInputChannels']), dev['defaultSampleRate'])
        self.stream1 = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            output=True,
            frames_per_buffer=CHUNK
        )
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            input_device_index=self.audio_input,
            frames_per_buffer=CHUNK,
            stream_callback=self.loop
        )



        # self.stream.start_stream()
        self.__temp_threshold_list = []
    def start(self):
        if not self.run:
            self.run = True
            self.stream.start_stream()

            while self.stream.is_active():
                time.sleep(0.1)

            self.stream.stop_stream()
            self.stream.close()
            #self.loop()

    def stop(self):
        self.run = False

    def loop(self, in_data_bytes, frame_count, time_info, status):
        #while True:
        # if self.stream.get_read_available() >= CHUNK:
            #data = self.stream.read(CHUNK, exception_on_overflow=False)
            # if len(data) == 0:
            #     break
        in_data = np.frombuffer(in_data_bytes, dtype=np.int16)

        if self.threshold_level is None:

            self.threshold_level = np.mean(in_data)

        #in_data = in_data[in_data >= self.threshold_level]
        #print(list(in_data))
        self.stream1.write(in_data.tobytes())

        if self.recognizer.AcceptWaveform(in_data.tobytes()):
            text = json.loads(self.recognizer.Result())["text"]
            if text:
                # print(text)
                #self.__temp_threshold_list.clear()
                self.action(text)
            else:

                self.threshold_level = np.mean(in_data)
        return in_data_bytes, pyaudio.paContinue