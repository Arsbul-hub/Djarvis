import json

from vosk import Model, KaldiRecognizer
import pyaudio

from app.ai import Brain
from app.commands_manager import CommandManager
from app.executor import ScriptsManager
from app.recognizer import Recognizer


class App:

    command_manager = CommandManager()
    brain = Brain(command_manager)
    recognizer = Recognizer(brain.analyse)

    def run(self):
        self.recognizer.start()
