# python setuptools 를 이용한 패키지 테스트

## 목표
- 복잡한 폴더 구조의 파이썬 프로젝트의 패키지화
- 패키지의 로컬 설치
- 로컬 설치된 패키지 테스트 실행

## 환경
- mac os
- python 3.10
- dependencies
    - pip 22.2.2
    - build 0.8.0
    - pytest 7.1.3

## 패키지 구조
```
mypackage
├── __init__.py
├── greeting
│   ├── __init__.py
│   └── greeting.py
├── main.py
└── say_hello
    ├── __init__.py
    ├── anyeong.py
    └── hello.py
```
### Intra-package References
패키지 내부의 서브 패키지들끼리 호출할 때, absolute imports 도 사용가능하며 relative imports도 사용가능
mypackage 는 절대 경로를 사용함


ex) greeting.py 에서 from say_hello.hello import say_hello

## setup.py 작성
```
├── setup.py
└── mypackage
```
```
from setuptools import setup

setup(
    name='mypackage',
    version='0.0.1',
    install_requires=[
        'importlib-metadata; python_version == "3.10"',
    ]
)
```
패키지를 위해 반드시 필요하다

패키지 이름과 버전, 디펜던시를 명시해준다.
importlib-metadata 는 mypackage에서 사용하지 않지만, 작업하던 프로젝트에서 관련한 에러가 발생했어서 기록 겸 써둔다.

## 패키징
```
python3 -m build
```
setup.py 가 위치한 곳에서 위 명령어를 실행하면 setuptools에서 setup.py 에 명시된 내용대로 현재 작업 위치의 파이썬 폴더를 찾아 패키지화한다.

구체적으로 포함할 폴더와 포함하지 않을 폴더를 명시해줄 수 있다

결과물은 mypackage.egg-info 와 dist 폴더로,
각각 패키지에 대한 메타 데이터와 whl, tar.gz 형태로 압축된 패키지를 담고있다.

## 로컬 설치
```
pip install dist/mypackage-0.0.1-py3-none-any.whl
```
만약 패키징 과정에서 문제가 있었다면,
예를 들어 패키징 위치가 잘 못 되거나한다면,
성공적으로 설치되었다고 하지만 실제로 실행했을 때
module not found 가 발생할 수 있다.

이번에 패키징하며 pip uninstall mypackage 시 
```
Found existing installation: mypackage 0.0.1
Uninstalling mypackage-0.0.1:
  Would remove:
    /Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/mypackage-0.0.1.dist-info/*
    /Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/mypackage/*
```
와 같이 패키지에 대한 정보와 패키지 소스들이 삭제되겠다는 알림이 아닌, 정보만 삭제되겠다고 메시지가 떠서 잘 못 된 걸 알게되었다.

패키지와 setup.py 의 위치, setup.py 에서 패키지 위치를 넘기는 방법들을 꼼꼼이 확인하기. 

## 테스트 코드 실행
```
pytest
```

### 추가
tests 를 실행할 때 내가 빌드한 패키지에 대해서 실행되는게 아니라
윗 뎁스의 mypackage 를 찾아서 import 해준 후 pytests 를 진행하는 듯 보였다.
```
ImportError while importing test module '/Users/ming/Test/Setuptools/tests/test_greeting.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_greeting.py:1: in <module>
    from mypackage.greeting.greeting import greeting
mypackage/greeting/greeting.py:1: in <module>
    from greeting_words.anyeong import say_anyeong
E   ModuleNotFoundError: No module named 'greeting_words'
```
확실히 하고 싶다면 venv 를 만들어서 테스트하는 게 나을 듯 하다

### 추추가
패키지라 가정하고 import를 from mypackage.~ 으로 잘 맞춰주었을 때, pytest 를 실행하면 
import_module mypackage 를 import 해주고 잘 실행해준다.
패키징 후 테스트 하는 것과 같은 효과

## 이슈
패키징 전의 마이패키지의 경우 구동시 모듈 notfound error 가 발생한다

패키징 했을 때도 동작하고, 패키징 전에도 동작하며,
호출하는 위치에서도 자유로운 import 를 하고 싶은데, 방법을 더 찾아봐야겠다.

### 시도1
mypackage 내부의 main.py 를 실행하려고 할땐, 서브 패키지 내에서 import 할 때 from mypackage. 이 아니라 from 으로 시작해도 동작.

그러나 빌드하게 되면, 서브 패키지의 모듈의 함수를 호출할 때 module not found error 발생
```
Traceback (most recent call last):
  File "/Users/ming/Test/Setuptools/tests/test_greeting.py", line 1, in <module>
    from mypackage.greeting.greeting import greeting
  File "/Users/ming/Test/Setuptools/venv/lib/python3.10/site-packages/mypackage/greeting/greeting.py", line 1, in <module>
    from greeting_words.anyeong import say_anyeong
ModuleNotFoundError: No module named 'greeting_words'
```

### 시도2
m패키징 했을 때 imoport mypackage. 가 아니라 relative import 를 할경우 main.py 를 실행할 수 없음.
```
Traceback (most recent call last):
  File "/Users/ming/Test/Setuptools/mypackage/main.py", line 1, in <module>
    from greeting.greeting import greeting
  File "/Users/ming/Test/Setuptools/mypackage/greeting/greeting.py", line 1, in <module>
    from ..greeting_words.anyeong import say_anyeong
ImportError: attempted relative import beyond top-level package
```
pytests 실행 시 매우 잘 동작

## 참고
https://setuptools.pypa.io/en/latest/userguide/quickstart.html
https://packaging.python.org/en/latest/tutorials/packaging-projects/
https://docs.python.org/3/tutorial/modules.html#intra-package-references

