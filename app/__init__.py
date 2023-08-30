import json

from vosk import Model, KaldiRecognizer
import pyaudio

from app.brain import Brain
from app.recognizer import Recognizer


class App:
    brain = Brain()
    recognizer = Recognizer(brain.analyse)

    def run(self):
        self.recognizer.start()
