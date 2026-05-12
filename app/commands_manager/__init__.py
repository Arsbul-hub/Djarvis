import json
import time

from .command import Command
from app.executor import ScriptsManager, speech_manager
import os

class CommandsTreeManager:

    scripts_manager = ScriptsManager()
    commands_map = []
    memory_data = {}

    def __init__(self, shared_buffer):
        speech_manager.shared_buffer = shared_buffer
        with open(os.path.join(os.path.dirname(__file__), "commands_map.json"), "r", encoding="utf-8") as file:
            c_map = json.load(file)["commands"]

        def walk(c_list):
            out = []
            for c in c_list:
                name = c.get("name").lower()
                description = c.get("description").lower()
                script = c.get("script").lower() if c.get("script") else None
                args = tuple(c.get("args")) if c.get("args") else ()
                script_execute = (lambda s=script, a=args: self.scripts_manager.execute(s, shared_buffer, a)) if script else None
                command_object = Command(name, description, script_execute)
                out.append(command_object)
                command_object.next_list = walk(c.get("children")) if c.get("children") else None
            return out
        t1 = time.time()
        self.commands_map = walk(c_map)
        t2 = time.time()
        print(t2 - t1)
        self.shared_buffer = shared_buffer

    def say_error(self, error_code):
        self.scripts_manager.execute_error(error_code, self.shared_buffer)

