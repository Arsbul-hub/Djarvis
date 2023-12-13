from datetime import datetime
from fuzzywuzzy import fuzz

from config import _NAME


class Brain:
    old_time_speek = None

    def __init__(self, manager):
        self.command_manager = manager

    def analyse(self, text):
        text = text.lower()

        def go(words_list, commands_list):
            out_command = None
            last_command = None
            for word in words_list:
                values_list = []

                for command in commands_list:
                    values_list.append((command, fuzz.WRatio(word, command.name)))
                command, index = max(values_list, key=lambda a: a[1])

                if index:
                    if command.next_list and words_list[-1] != word:
                        last_command = command
                        commands_list = command.next_list

                    else:
                        return command
                elif words_list[-1] == word:
                    return last_command
                    # if command == word and command.next_list:
                    #     commands_list = command.next_list
                    # if not command.next_list or words_list[-1] == word:
                    #     return command

        if self.can_analyse(text):
            # text = self.remove_name(text)

            words_list = text.split(" ")
            command = go(words_list, self.command_manager.commands_map)
            if command:
                command.call()
            else:
                self.command_manager.say_error(404)

    def remove_name(self, text):
        words_list = text.split(" ")
        for word in words_list:
            if fuzz.partial_ratio(word, _NAME) > 50:
                words_list.remove(word)

        return " ".join(words_list)

    def can_analyse(self, text):

        if fuzz.partial_ratio(text, _NAME) > 50 or self.old_time_speek and (
                datetime.now() - self.old_time_speek).seconds < 7:
            self.old_time_speek = datetime.now()
            return True

        return False
