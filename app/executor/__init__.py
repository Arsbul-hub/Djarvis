
from ..memory_manager import MemoryManager
from ..speech import SpeechManager

memory_manager = MemoryManager()
speech_manager = SpeechManager()
class ScriptsManager:

    def execute(self, command_name, args):
        script = DEFAULT_SCRIPTS_PATHS.get(command_name)
        if script:
            script(*args)
        else:
            self.execute_error(4041)

    def execute_error(self, error_code):
        script = ERROR_SCRIPTS_PATHS.get(error_code)
        if script:
            script()
        else:
            self.execute_error(404)

from .paths import *