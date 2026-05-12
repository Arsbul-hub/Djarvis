from datetime import datetime
from fuzzywuzzy import fuzz

from app.services.ai.ai import Brain
from config import NAME_LOWER

from app.services import Service
from app.commands_manager import CommandsTreeManager

class AiService(Service):

    def run(self) -> None:
        ai = Brain(self._state, self._shared, self._shared_locks)
        ai.run()
    def on_stop(self):
        pass