from mypackage.say_hello.anyeong import say_anyeong
from mypackage.say_hello.hello import say_hello

LANGUAGE = "KOR"

def greeting():
    if LANGUAGE == "KOR":
        return say_anyeong()
    return say_hello()

if __name__ == "__main__":
    greeting()