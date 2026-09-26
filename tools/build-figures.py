#!/usr/bin/env python3
"""모든 그림을 다시 생성한다.

    python3 tools/build-figures.py

일부 그림은 R이 만든 중간 파일(tools/*.json, tools/ci_sim.csv)에 의존한다.
없으면 해당 그림만 건너뛰고 나머지는 그대로 생성된다.
"""
import os, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

MODULES = ['fig_ch02', 'fig_ch0304', 'fig_ch0506', 'fig_ch0811']

print('그림 생성')
for name in MODULES:
    mod = __import__(name)
    for fn in getattr(mod, 'ALL', []):
        fn()

# 7장 그림은 별도 스크립트가 담당한다 (R 산출물을 인자로 받는다)
subprocess.run([sys.executable, os.path.join(HERE, 'make-figures.py')], check=True)
print('완료')
