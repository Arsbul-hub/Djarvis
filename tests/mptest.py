import time
from threading import Thread

import pyttsx3
def d(name, completed):
    print(1)
engine = pyttsx3.init()

engine.connect('finished-utterance', d)
def d():
    engine.say("Hello sir, how may I help you, sir.")
    engine.startLoop()

Thread(target=d).start()
time.sleep(5)
Thread(target=d).start()
time.sleep(5)

# import pyttsx3
#
# def onEnd(name, completed):
#     print(f'Завершение высказывания: {name}, завершено: {completed}')
#
# engine = pyttsx3.init()
# engine.connect('finished-utterance', onEnd)
#
# engine.say('The quick brown fox jumped over the lazy dog.')
# engine.runAndWait()