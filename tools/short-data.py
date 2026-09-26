#!/usr/bin/env python3
"""쇼츠가 그리는 실제 데이터를 JS 파일로 뽑는다.

    python3 tools/short-data.py

쇼츠 페이지는 file:// 로 열리므로 CSV를 fetch로 읽을 수 없다.
그래서 책과 같은 원자료에서 data.js 를 만들어 페이지가 <script>로 싣게 한다.
"""
import csv, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'books', '01-basic-statistics', 'data')
SHORTS = os.path.join(ROOT, 'video', 'shorts')


def write(slug, name, obj, source):
    p = os.path.join(SHORTS, slug, 'data.js')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(f'// 자동 생성: tools/short-data.py — 원자료 {source}\n')
        f.write(f'window.{name} = {json.dumps(obj, ensure_ascii=False)};\n')
    print('  ', os.path.relpath(p, ROOT))


with open(os.path.join(DATA, 'prepost.csv'), encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
write('04-paired', 'PREPOST',
      {'pre': [float(r['pre']) for r in rows], 'post': [float(r['post']) for r in rows]},
      'books/01-basic-statistics/data/prepost.csv (8장)')

with open(os.path.join(ROOT, 'tools', 'ci_sim.csv'), encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
write('05-ci', 'CISIM',
      [{'m': float(r['m']), 'lo': float(r['lo']), 'hi': float(r['hi'])} for r in rows],
      'tools/ci_sim.csv (6장 신뢰구간 모의실험, 100개 중 97개 포함)')
