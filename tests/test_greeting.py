from mypackage.greeting.greeting import greeting
import pytest


def test_greeting():
    assert greeting("KOR") == "안녕"
    assert greeting("ENG") == "hello"

    with pytest.raises(ValueError) as e:
        greeting("JPN")
    assert e.value.args[0] == "lang"
