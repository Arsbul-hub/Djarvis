from config import ERROR_CODES


def say(text):
    print(text)


def say_error(code):
    print(ERROR_CODES[code])
