from app.actions import say


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


commands_map = [
    Command("Привет", "Приветствие", call=lambda: say("Здравствуйте"), next_list=[
        Command("Тебе", "Указание на объект", call=lambda: say("И тебе привет!"))
    ])
]
