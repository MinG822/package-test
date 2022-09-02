from mypackage import say_hello
from mypackage.say_hello.anyeong import say_anyeong
from mypackage.say_hello.hello import say_hello


def test_say_hello():
    assert say_hello() == "hello"

def test_say_anyeong():
    assert say_anyeong() == "안녕"