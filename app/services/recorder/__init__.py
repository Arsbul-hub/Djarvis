import time

from app.services import Service



class RecorderService(Service):

    audio_input = 0
    threshold_level = None

    def run(self):
        while not self._shared.get("recognizer_started"):

            time.sleep(0.5)
        from app.services.recorder.recorder import Recorder
        recognizer = Recorder(self._state, self._shared, self._shared_locks)
        recognizer.start()
    def on_stop(self):
        pass
