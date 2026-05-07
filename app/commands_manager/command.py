class Command:
    def __init__(self, name, description, call=None, next_list=None):

        if next_list is None:
            next_list = []
        if call is not None:
            self.call = call
        self.next_list = next_list
        self.name = name
        self.description = description

    def call(self):
        pass

    def __eq__(self, text_command):
        if text_command.lower() == self.name.lower():
            return True
        return False

