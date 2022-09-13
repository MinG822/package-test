from mypackage.greeting_words.anyeong import say_anyeong
from mypackage.greeting_words.hello import say_hello


def test_say_hello():
    assert say_hello() == "hello"


def test_say_anyeong():
    assert say_anyeong() == "안녕"
