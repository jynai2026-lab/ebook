#!/usr/bin/env python3
"""2권(회귀분석) 그림을 모두 다시 만든다.

    python3 tools/build-figures-2.py

자료에서 그리는 그림은 books/02-regression/figdata/*.json 을 읽는다.
그 파일은 books/02-regression/r/figdata.R 이 만든다.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

MODULES = ['fig2_ch00_03', 'fig2_ch04_07', 'fig2_ch08_12']

print('2권 그림 생성')
for name in MODULES:
    mod = __import__(name)
    for fn in getattr(mod, 'ALL', []):
        fn()
print('완료')
