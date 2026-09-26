#!/usr/bin/env python3
"""렌더된 PDF에서 각 장이 시작하는 쪽을 찾아 JSON으로 돌려준다.

    python3 tools/toc-pages.py <pdf>

장 번호 안에 심어 둔 보이지 않는 표식(§CH07§)을 찾는다. 제목으로 찾으면
줄바꿈이 끼어들 때 검색이 실패하므로 표식을 쓴다.

표식이 자간(letter-spacing)이 넓은 글줄 안에 있어 추출하면 글자마다 줄이
나뉜다. 그래서 공백을 모두 지운 뒤에 찾는다.

출력 쪽번호는 표지를 0으로 보는 값이며, 이는 본문에 찍히는 번호와 같다.
"""
import json, re, sys
import pymupdf

doc = pymupdf.open(sys.argv[1])
found = {}
for i in range(doc.page_count):
    flat = re.sub(r'\s+', '', doc[i].get_text())
    for m in re.finditer(r'§CH(\w+)§', flat):
        found.setdefault(m.group(1), i)
print(json.dumps(found, ensure_ascii=False))
