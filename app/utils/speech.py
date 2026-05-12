from datetime import datetime
import threading

import pyttsx3


class SpeechManager:
    def __init__(self):
        self.engine = pyttsx3.init()
        # Настройка параметров голоса
        voices = self.engine.getProperty('voices')
        print(voices)
        # Выбор голоса (обычно индекс 0 – мужской, 1 – женский)
        self.engine.setProperty('voice', voices[0].id)
        # Настройка скорости речи (по умолчанию 200)
        self.engine.setProperty('rate', 150)
        self.current_thread = None
        self._shared_buffer = None

    @property
    def shared_buffer(self):
        return self._shared_buffer

    @shared_buffer.setter
    def shared_buffer(self, shared_buffer):
        self._shared_buffer = shared_buffer

    def say(self, text, on_end=None):
        if self.current_thread is not None:
            self.engine.endLoop()
            self.current_thread.join()
            self.current_thread = None
        def one(name, completed):
            print(123)
            self._shared_buffer["last_speek_datetime"] = datetime.now()
            if on_end is not None:
                on_end(text)

        def say():
            self.engine.say(text)
            self.engine.startLoop()

        def d(name, completed):
            print(1)
        self.engine.connect('finished-utterance', d)
        self.current_thread = threading.Thread(target=say)
        self.current_thread.start()
