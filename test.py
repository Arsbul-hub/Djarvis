import pyaudio
import numpy as np
import time

# Параметры записи
CHUNK = 1024  # Количество семплов за один раз
FORMAT = pyaudio.paInt16  # 16-битный формат
CHANNELS = 1  # Моно
RATE = 44100  # Частота дискретизации (Гц)
SILENCE_THRESHOLD = 500  # Порог тишины (подберите под себя)


def rms(data):
    """Вычисляет среднеквадратичное значение (RMS) звукового сигнала."""
    # Преобразуем байты в массив numpy int16
    samples = np.frombuffer(data, dtype=np.int16).astype(np.float64)

    # Вычисляем RMS
    return np.sqrt(np.mean(samples ** 2))


def main():
    # Инициализация PyAudio
    p = pyaudio.PyAudio()

    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    print(numdevices)
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'), p.get_device_info_by_host_api_device_index(0, i))

    # Открываем поток для записи
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=1)

    print("Запись началась. Говорите в микрофон...")
    print("Нажмите Ctrl+C для остановки.\n")
    time.sleep(3)
    try:
        while True:

            # Получаем данные с микрофона

            data = stream.read(CHUNK, exception_on_overflow=False)

            # Вычисляем уровень звука
            level = rms(data)

            # Простой визуальный индикатор

            bars = int(level / 200)  # Масштабирование для отображения
            if bars > 50:
                bars = 50
            visual = "|" * bars + " " * (50 - bars)

            # Вывод информации
            print(f"RMS: {level:6.0f} [{visual}]  ")

            # Проверка на тишину (опционально)
            if level < SILENCE_THRESHOLD:
                pass  # Можно добавить действия при тишине



    except KeyboardInterrupt:
        print("\n\nОстановка записи...")

    finally:
        # Закрываем поток и завершаем PyAudio
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("Запись завершена.")


if __name__ == "__main__":
    main()