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
    def say(self, text):
        if self.current_thread is not None:
            self.engine.endLoop()
            self.current_thread.join()
            self.current_thread = None
        def say():

            self.engine.say(text)

            self.engine.startLoop()
        self.current_thread = threading.Thread(target=say)
        self.current_thread.start()

