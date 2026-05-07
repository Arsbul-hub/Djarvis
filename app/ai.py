from datetime import datetime
from fuzzywuzzy import fuzz


from config import NAME_LOWER


class Brain:
    old_time_speek = None

    def __init__(self, manager):
        self.command_manager = manager


    def analyse(self, text):
        text = text.lower()

        def go(words, commands_list):
            values_list = []
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

            command = go(words_list, self.command_manager.commands_map)

            if command:
                command.call()
            else:
                self.command_manager.say_error(404)
    @staticmethod
    def remove_name(text):
        words_list = text.split(" ")
        for i, word in enumerate(words_list):
            if fuzz.partial_ratio(word, NAME_LOWER) > 80:
                print(word, NAME_LOWER, words_list, words_list[i + 1:])
                words_list = words_list[i + 1:]
                break

        return " ".join(words_list)

    def can_analyse(self, text):
        # TODO: ОЖИДАНИЕ ПОСЛЕ СКАЗАННОГО ТЕКСТА
        if fuzz.partial_ratio(text, NAME_LOWER) > 80 or self.old_time_speek and (
                datetime.now() - self.old_time_speek).seconds < 5:
            self.old_time_speek = datetime.now()
            return True
        return False
