import time
from datetime import datetime
from fuzzywuzzy import fuzz


from config import NAME_LOWER
from app.services import Service
from app.commands_manager import CommandsTreeManager

class Brain:
    old_time_speek = None
    def __init__(self, state_buffer, shared_buffer, shared_buffer_locks):

        self.state_buffer = state_buffer
        self.shared_buffer = shared_buffer
        self.shared_buffer_locks = shared_buffer_locks
        self.shared_buffer["last_speek_datetime"] = None
        self.command_manager = CommandsTreeManager(shared_buffer)
        self.shared_buffer["text_commands"] = []

    def run(self):
        while True:


            self.shared_buffer_locks["text_commands"].acquire()
            try:
                if self.shared_buffer["text_commands"]:


                    text_command = self.shared_buffer["text_commands"][0]
                    self.shared_buffer["text_commands"] = self.shared_buffer["text_commands"][1:]
                    self.analyse(text_command)


            finally:
                self.shared_buffer_locks["text_commands"].release()


    def analyse(self, text):
        text = text.lower()

        def go(words, commands_list):
            values_list = []
            """
            как дела у тебя

    for c in commands_list:
TypeError: 'NoneType' object is not iterable
"""
            for c in commands_list:
                values_list.append((c, fuzz.ratio(words[0], c.name)))
            c, v = max(values_list, key=lambda a: a[1])

            if v > 70:
                if len(words) == 1:
                    return c
                else:
                    return go(words[1:], c.next_list)
            else:
                return None

        if self.can_analyse(text):
            # text = self.remove_name(text)
            text = self.remove_name(text)
            words_list = text.split(" ")
            # t1 = time.time()

            command = go(words_list, self.command_manager.commands_map)

            if command:
                command.call() # TODO: РЕАЛИЗОВАТЬ ВОЗМОЖНОСТЬ ПЕРЕОПРЕДЕЛЕНИЯ РЕМЕНИ ПОСЛЕДНЕГО РАЗГОВОРА ВНУРИ CALL
            else:
                self.command_manager.say_error(404)
            # t2 = time.time()
            # print(t2 - t1)

    @staticmethod
    def remove_name(text):
        words_list = text.split(" ")
        for i, word in enumerate(words_list):
            if fuzz.partial_ratio(word, NAME_LOWER) > 90:

                words_list = words_list[i + 1:]
                break

        return " ".join(words_list)

    def can_analyse(self, text):

        if fuzz.partial_ratio(text, NAME_LOWER) > 90 or self.shared_buffer["last_speek_datetime"] and (
                datetime.now() - self.shared_buffer["last_speek_datetime"]).seconds < 5:
            self.shared_buffer["last_speek_datetime"] = datetime.now()
            return True
        return False
