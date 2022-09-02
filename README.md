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


ex) greeting.py 에서 from mypackage.say_hello.hello import say_hello

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

## 이슈
패키징 전의 마이패키지의 경우 구동시 모듈 notfound error 가 발생한다

패키징 했을 때도 동작하고, 패키징 전에도 동작하며,
호출하는 위치에서도 자유로운 import 를 하고 싶은데, 방법을 더 찾아봐야겠다.


## 참고
https://setuptools.pypa.io/en/latest/userguide/quickstart.html
https://packaging.python.org/en/latest/tutorials/packaging-projects/
https://docs.python.org/3/tutorial/modules.html#intra-package-references

