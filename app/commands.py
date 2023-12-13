from datetime import datetime

from config import ERROR_CODES


class Command:
    def __init__(self, name, description, call, next_list=None):

        if next_list is None:
            next_list = []
        self.call = call
        self.next_list = next_list
        self.name = name
        self.description = description

    def __eq__(self, text_command):
        if text_command.lower() == self.name.lower():
            return True
        return False


class CommandManager:
    commands_map = []
    memory_data = {}

    def __init__(self):
        self.commands_map = [
            Command("Привет", "Приветствие", call=self.greeting, next_list=[
                Command("Тебе", "Указание на объект", call=lambda: self.say("И тебе привет!"))
            ]),
            Command("Джарвис", "Вызов бота", call=lambda: self.say("Да сэр")),
            Command("Как", "Базовый вопрос", call=lambda: self.say("Что как?"), next_list=[
                Command("Дела", "Вопрос о дне", call=lambda: self.say("Нормально, а как у вас?"))
            ])

        ]

    def greeting(self):
        if "last_greeting" in self.memory_data:
            if (datetime.now() - self.memory_data["last_greeting"]).seconds / 60 < 20:
                if self.memory_data.get("greetings_count", 0) > 2:
                    # Ничего не говорим
                    self.memory_data["last_greeting"] = datetime.now()
                    self.memory_data["greetings_count"] = self.memory_data.get("greetings_count", 0) + 1
                else:
                    self.say("Мы уже здоровались недавно")
                    self.memory_data["greetings_count"] = self.memory_data.get("greetings_count", 0) + 1

            else:
                self.say("Привет")
                self.memory_data["greetings_count"] = 0
                self.memory_data["last_greeting"] = datetime.now()

        else:
            self.say("Привет")
            self.memory_data["greetings_count"] = 0
            self.memory_data["last_greeting"] = datetime.now()

    def say(self, text):
        print(text)

    def say_error(self, code):
        print(ERROR_CODES[code])
