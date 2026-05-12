
from app.utils.memory_manager import MemoryManager
from app.utils.speech import SpeechManager

memory_manager = MemoryManager()
speech_manager = SpeechManager()
class ScriptsManager:
    def execute(self, command_name, service_shared_buffer, args):
        script = DEFAULT_SCRIPTS_PATHS.get(command_name)
        if script:
            script(service_shared_buffer, *args)
        else:
            self.execute_error(4041, service_shared_buffer)
    def execute_error(self, error_code, service_shared_buffer):
        script = ERROR_SCRIPTS_PATHS.get(error_code)
        if script:
            script(service_shared_buffer)
        else:
            self.execute_error(404, service_shared_buffer)

from .paths import *