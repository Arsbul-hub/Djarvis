import pyaudio
import numpy as np
import noisereduce as nr
# Параметры аудио
CHUNK = 1024  # Размер буфера
FORMAT = pyaudio.paInt16  # Формат данных
CHANNELS = 1  # Моно
RATE = 44100  # Частота дискретизации

p = pyaudio.PyAudio()

# Открываем входной поток (микрофон)
input_stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

# Открываем выходной поток (динамики)
output_stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    output=True,
    frames_per_buffer=CHUNK
)

print("* Запись и воспроизведение начаты. Нажмите Ctrl+C для остановки")
audio_buffer = np.array([], dtype=np.int16)
try:
    while True:
        # Читаем данные с микрофонаs
        data = input_stream.read(CHUNK, exception_on_overflow=False)
        #audio_buffer = np.append(audio_buffer, np.frombuffer(data, dtype=np.int16))
        # Сразу воспроизводим
        #reduced_noise = nr.reduce_noise(y=audio_buffer, sr=44100)

        output_stream.write(np.frombuffer(data, dtype=np.int16).tobytes())

        # Опционально: обработка аудио (например, громкость)
        # audio_data = np.frombuffer(data, dtype=np.int16)
        # audio_data = (audio_data * 1.5).astype(np.int16)  # Увеличиваем громкость
        # output_stream.write(audio_data.tobytes())

except KeyboardInterrupt:
    print("\n* Остановлено пользователем")

finally:
    # Закрываем потоки
    input_stream.stop_stream()
    input_stream.close()
    output_stream.stop_stream()
    output_stream.close()
    p.terminate()
    print("* Потоки закрыты")