from app.services import Service



class RecognizerService(Service):

    audio_input = 0
    threshold_level = None

    def run(self):
        from app.services.recognizer.recognizer import Recognizer
        recognizer = Recognizer(self._state, self._shared, self._shared_locks)
        self._shared["recognizer_started"] = True
        recognizer.start()

    def on_stop(self):
        pass