from mypackage.greeting_words.anyeong import say_anyeong
from mypackage.greeting_words.hello import say_hello


def greeting(lang):
    if lang == "KOR":
        return say_anyeong()
    elif lang == "ENG":
        return say_hello()
    else:
        raise ValueError("lang")
