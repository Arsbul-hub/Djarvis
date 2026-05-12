import time

from app.services import ServiceManager
from app.services.ai import AiService

from app.services.recognizer import RecognizerService

from app.services.recorder import RecorderService
class App:
    servicemanager = None

    def run(self):
        self.servicemanager = ServiceManager((
            "frames",
            "text_commands"
        ))
        self.servicemanager.add_service(RecognizerService, "recognizer")
        self.servicemanager.add_service(AiService, "ai")
        self.servicemanager.add_service(RecorderService, "recorder", False)


        self.servicemanager.start_all()
        print("Сервисы запущены")
        try:
            # Просто бесконечно спим, пока не нажмут Ctrl+C
            while True:
                time.sleep(1)

                # Можно выводить состояние
                # states = self.servicemanager.get_all_states()
                # print(f"Статус: {states}")

        except KeyboardInterrupt:
            print("\nЗавершаем всё...")
        finally:
            self.servicemanager.stop_all()


