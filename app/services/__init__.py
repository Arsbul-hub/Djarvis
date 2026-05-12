import multiprocessing
import threading
import time
from abc import ABC, abstractmethod
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class Service(ABC):
    """Базовый класс сервиса, запускаемого в отдельном процессе"""

    def __init__(self, name: str):
        self.name = name
        self._shared = None
        self._shared_locks = None
        self._stop_event: Optional[multiprocessing.Event] = None
        self._state: Optional[multiprocessing.managers.DictProxy] = None

    @abstractmethod
    def run(self) -> None:
        """Основной цикл сервиса"""
        pass
    @abstractmethod
    def on_stop(self):
        pass

    def start(self, stop_event: multiprocessing.Event, state, shared, shared_locks) -> None:
        """Точка входа для процесса"""
        self._stop_event = stop_event
        self._state = state
        self._shared = shared
        self._shared_locks = shared_locks
        self._state['status'] = 'running'
        #try:
        self.run()
        # except Exception as e:
        #     logger.error(f"Service {self.name} error: {e}")
        #     self._state['status'] = f'error: {e}'
        # finally:
        #     self._state['status'] = 'stopped'

    @property
    def state(self):
        return dict(self._state) if self._state else {}

    def should_stop(self) -> bool:
        return self._stop_event.is_set() if self._stop_event else True


class ServiceManager:
    """Менеджер для управления сервисами"""

    def __init__(self, locks: tuple = (),):
        self._manager = multiprocessing.Manager()
        self.shared_dict = self._manager.dict()
        self.shared_dict_locks = {l: multiprocessing.Lock() for l in locks}
        self._services: Dict[str, Dict] = {}


    @property
    def manager(self):
        return self._manager

    def add_service(self, service_class: type, name: str, is_process: bool = True, *args, **kwargs) -> None:
        """Регистрирует сервис для управления"""
        self._services[name] = {
            'class': service_class,
            'args': args,
            'kwargs': kwargs,
            'process': None,
            'stop_event': self._manager.Event(),
            'state': self._manager.dict({'status': 'init'}),
            "is_process": is_process,

            "service": None,
            'restart_policy': True
        }

    def start(self, name: str = None) -> None:
        """Запускает сервис(ы)"""
        names = [name] if name else self._services.keys()

        for n in names:
            if n not in self._services:
                logger.warning(f"Service {n} not registered")
                continue

            svc = self._services[n]
            if svc['process'] and svc['process'].is_alive():
                logger.info(f"Service {n} already running")
                continue

            svc['stop_event'].clear()
            svc['state']['status'] = 'starting'

            # Создаём сервис БЕЗ передачи manager
            service = svc['class'](
                name=n,
                *svc['args'],
                **svc['kwargs']
            )

            if svc["is_process"]:
                svc['process'] = multiprocessing.Process(
                    target=service.start,
                    args=(svc['stop_event'], svc['state'], self.shared_dict, self.shared_dict_locks),
                    name=n
                )
            else:
                svc['process'] = threading.Thread(
                    target=service.start,
                    args=(svc['stop_event'], svc['state'], self.shared_dict, self.shared_dict_locks),
                    name=n
                )
            svc["service"] = service
            svc['process'].start()
            logger.info(f"Service {n} started")

    def start_all(self):
        """Запускает все зарегистрированные сервисы"""
        self.start()

    def stop(self, name: str = None, graceful: bool = True) -> None:
        """Останавливает сервис(ы)"""
        names = [name] if name else self._services.keys()

        for n in names:
            svc = self._services.get(n)
            if not svc or not svc['process']:
                continue

            svc['restart_policy'] = False

            if graceful:
                svc['stop_event'].set()
                svc['process'].join(timeout=5)

            if svc['process'].is_alive():
                svc['process'].terminate()
                svc['process'].join(timeout=2)

            if svc['process'].is_alive() and svc["is_process"]:
                svc['process'].kill()

            svc["service"].on_stop()
            logger.info(f"Service {n} stopped")

    def restart(self, name: str) -> None:
        """Перезапускает сервис"""
        self.stop(name)
        self._services[name]['restart_policy'] = True
        time.sleep(0.5)  # Небольшая задержка для очистки ресурсов
        self.start(name)

    def monitor(self, check_interval: float = 1.0) -> None:
        """Мониторинг и авто-рестарт упавших сервисов"""
        try:
            while True:
                for name, svc in self._services.items():
                    if (svc['process'] and
                            not svc['process'].is_alive() and
                            svc['restart_policy']):
                        logger.warning(f"Service {name} died, restarting...")
                        self.start(name)
                time.sleep(check_interval)
        except KeyboardInterrupt:
            self.stop_all()

    def stop_all(self) -> None:
        """Останавливает все сервисы"""
        logger.info("Stopping all services...")
        self.stop()
        self._manager.shutdown()

    def get_state(self, name: str) -> dict:
        """Получить состояние сервиса"""
        svc = self._services.get(name)
        if svc and 'state' in svc:
            return dict(svc['state'])
        return {}

    def get_all_states(self) -> dict:
        """Получить состояния всех сервисов"""
        return {name: dict(svc['state']) for name, svc in self._services.items() if 'state' in svc}
