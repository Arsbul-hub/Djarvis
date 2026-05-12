import pyaudio
import webrtcvad

# --- Настройки (должны соответствовать требованиям webrtcvad) ---
RATE = 16000
CHUNK = int(RATE * 0.03)  # 20 мс при 16000 Гц (16000 * 0.02 = 320)
FORMAT = pyaudio.paInt16
CHANNELS = 1

vad = webrtcvad.Vad()
# Режим агрессивности: 0 (least aggressive) до 3 (most aggressive)
vad.set_mode(3)


def is_speech_webrtc(data, sample_rate):
    """Проверяет аудиофрагмент с помощью WebRTC VAD."""
    return vad.is_speech(data, sample_rate)


# --- Инициализация PyAudio ---
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
stream1 = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)
print("WebRTC VAD запущен. Говорите! (Ctrl+C для выхода)")

try:
    while True:
        data = stream.read(CHUNK)
        if is_speech_webrtc(data, RATE):
            print("Речь обнаружена!")
            stream1.write(data)

except KeyboardInterrupt:
    print("Остановка...")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()