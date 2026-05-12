from pocketsphinx import LiveSpeech

for phrase in LiveSpeech(sampling_rate=8000, kws_threshold=1e-10):
    print(phrase)
# speech = LiveSpeech(keyphrase='ohio', kws_threshold=1e-20)
# for phrase in speech:
#     print(phrase.segments(detailed=True))
