import json

from vosk import Model, KaldiRecognizer
import pyaudio


from config import *


class Recognizer:
    run = False
    audio_input = 6

    def __init__(self, action):
        self.action = action
        model = Model(r"model-small")

        self.recognizer = KaldiRecognizer(model, RATE)
        print("Model Loaded")
        self.audio = pyaudio.PyAudio()
        for i in range(self.audio.get_device_count()):
            dev = self.audio.get_device_info_by_index(i)
            print((i, dev['name'], dev['maxInputChannels']), dev['defaultSampleRate'])
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            #input_device_index=self.audio_input,
            frames_per_buffer=CHUNK
        )
        self.stream.start_stream()

    def start(self):
        if not self.run:
            self.run = True

            self.loop()

    def stop(self):
        self.run = False

    def loop(self):
        while True:
            data = self.stream.read(CHUNK, exception_on_overflow=False)
            if len(data) == 0:
                break

            if self.recognizer.AcceptWaveform(data):

                text = json.loads(self.recognizer.Result())["text"]
                if text:
                    self.action(text)
