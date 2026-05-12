import os
from pocketsphinx import Decoder

# Настройки
MODEL_DIR = r'./static/stt/zero_ru_cont_8k_v3'  # <-- измените на ваш полный путь
AUDIO_FILE = r'./t.wav'          # <-- путь к вашему тестовому WAV

config = Decoder.default_config()
config.set_string('-hmm', os.path.join(MODEL_DIR, 'zero_ru.cd_ptm_4000'))
config.set_string('-lm', os.path.join(MODEL_DIR, 'ru.lm'))
config.set_string('-dict', os.path.join(MODEL_DIR, 'ru.dic'))
config.set_string('-logfn', 'nul')  # отключить логи в файл

decoder = Decoder(config)

# Открываем WAV и проверяем его свойства (он должен быть 16 кГц, 16 бит, моно)
import wave
with wave.open(AUDIO_FILE, 'rb') as wf:
    print(f"Каналы: {wf.getnchannels()}, Частота: {wf.getframerate()}, Битность: {wf.getsampwidth()*8}")
    assert wf.getnchannels() == 1, "Только моно"
    assert wf.getframerate() == 8000, "Только 16000 Гц"
    assert wf.getsampwidth() == 2, "Только 16 бит"

# Распознаём потоком
decoder.start_utt()
with open(AUDIO_FILE, 'rb') as f:
    # Пропускаем заголовок WAV (44 байта)
    f.seek(44)
    while True:
        buf = f.read(4096)
        if buf:
            decoder.process_raw(buf, False, False)
        else:
            break
decoder.end_utt()

hypothesis = decoder.hyp()
if hypothesis:
    print('Распознано:', hypothesis.hypstr)
else:
    print('Ничего не распознано')