from datetime import datetime

from app.actions import say_error
from app.commands import commands_map
from config import _NAME


class Brain:
    old_time_speek = datetime.now()

    def analyse(self, text):
        text = text.lower()

        def go(words_list, commands_list):
            out_command = None

            for word in words_list:
                for command in commands_list:
                    if command == word:
                        if command.next_list and words_list[-1] != word:
                            commands_list = command.next_list
                        else:
                            return command

                    # if command == word and command.next_list:
                    #     commands_list = command.next_list
                    # if not command.next_list or words_list[-1] == word:
                    #     return command

        if self.can_analyse(text):
            text = text.replace(_NAME.lower(), "").strip()
            words_list = text.split(" ")
            command = go(words_list, commands_map)
            if command:
                command.call()
            else:
                say_error(404)

    def can_analyse(self, text):

        if _NAME.lower() in text or (datetime.now() - self.old_time_speek).seconds < 7:
            self.old_time_speek = datetime.now()
            return True
        return False
