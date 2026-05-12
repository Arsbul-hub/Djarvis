import time
from threading import Thread
import wave
import pyaudio
import numpy as np
import noisereduce as nr
import webrtcvad

# Параметры аудио
CHUNK = 4096  # Размер буфера
FORMAT = pyaudio.paInt16  # Формат данных
CHANNELS = 1  # Моно
RATE = 44100  # Частота дискретизации

# Имя входного файла
INPUT_FILE = "g.wav"  # Замените на путь к вашему файлу
OUTPUT_FILE = "output_audio.wav"  # Файл для сохранения результата

# Открываем аудиофайл для чтения
try:
    wf = wave.open(INPUT_FILE, 'rb')

    # Проверяем, соответствует ли файл нашим параметрам
    if wf.getnchannels() != CHANNELS:
        print(f"Внимание: файл имеет {wf.getnchannels()} каналов, ожидается {CHANNELS}")
    if wf.getframerate() != RATE:
        print(f"Внимание: файл имеет частоту {wf.getframerate()} Гц, ожидается {RATE} Гц")

    print(f"Файл {INPUT_FILE} успешно открыт")
    print(f"Параметры файла: {wf.getnchannels()} каналов, {wf.getframerate()} Гц, {wf.getsampwidth()} байт на сэмпл")

except FileNotFoundError:
    print(f"Ошибка: файл {INPUT_FILE} не найден!")
    exit(1)

# Инициализируем PyAudio для воспроизведения
p = pyaudio.PyAudio()

# Открываем выходной поток для воспроизведения
output_stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    output=True,
    frames_per_buffer=CHUNK
)

# Инициализируем VAD
vad = webrtcvad.Vad()
vad.set_mode(1)  # 0: Агрессивная фильтрация, 3: Менее агрессивная


def is_speech(frame):
    return vad.is_speech(frame, RATE)


print("* Начата обработка файла...")
audio_buffer = np.array([], dtype=np.int16)
n_audio_buffer = np.array([], dtype=np.int16)
f = True


def process_audio():
    global audio_buffer, n_audio_buffer, f
    while f:
        # Читаем данные из файла
        data = wf.readframes(CHUNK)

        if len(data) == 0:  # Конец файла
            print("Достигнут конец файла")
            break

        d = np.frombuffer(data, dtype=np.int16)
        n_audio_buffer = np.append(n_audio_buffer, d)

        # Применяем шумоподавление
        reduced_noise = nr.reduce_noise(y=d, sr=RATE)
        audio_buffer = np.append(audio_buffer, reduced_noise)


# Запускаем обработку в потоке
d = Thread(target=process_audio)
d.start()
d.join()  # Ждем завершения обработки

print("Обработка завершена")

# Сохраняем необработанное аудио в файл
print("Сохраняем необработанное аудио...")
with wave.open(OUTPUT_FILE.replace('.wav', '_original.wav'), 'wb') as out_wf:
    out_wf.setnchannels(CHANNELS)
    out_wf.setsampwidth(p.get_sample_size(FORMAT))
    out_wf.setframerate(RATE)
    out_wf.writeframes(n_audio_buffer.tobytes())

# Сохраняем обработанное аудио в файл
print("Сохраняем обработанное аудио...")
with wave.open(OUTPUT_FILE, 'wb') as out_wf:
    out_wf.setnchannels(CHANNELS)
    out_wf.setsampwidth(p.get_sample_size(FORMAT))
    out_wf.setframerate(RATE)
    out_wf.writeframes(audio_buffer.tobytes())

# Воспроизводим обработанное аудио
print("Воспроизводим обработанное аудио...")
output_stream.write(audio_buffer.tobytes())
time.sleep(2)

# Закрываем потоки и файлы
wf.close()
output_stream.stop_stream()
output_stream.close()
p.terminate()

print(f"* Готово!")
print(f"Сохранено:")
print(f"  - Оригинал: {OUTPUT_FILE.replace('.wav', '_original.wav')}")
print(f"  - Обработанный: {OUTPUT_FILE}")