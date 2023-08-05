from vosk import Model, KaldiRecognizer
import os
import pyaudio
CHUNK = 44100
model = Model(r"model") # полный путь к модели
rec = KaldiRecognizer(model, CHUNK)
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=CHUNK,
    input=True,
    frames_per_buffer=CHUNK
)
stream.start_stream()

while True:
    data = stream.read(4000)
    if len(data) == 0:
        break

    print(rec.Result() if rec.AcceptWaveform(data) else rec.PartialResult())

print(rec.FinalResult())