"""
2권(회귀분석) 그림 공통 도구

figlib의 그리기 함수를 그대로 쓰고, 저장 위치와 주색만 2권에 맞춘다.
주색은 books/02-regression/book.config.json 의 accent와 같다.
"""
import os
import figlib
from figlib import *          # noqa: F401,F403  (text, tex, rich, panel, ...)

figlib.OUT = os.path.join(figlib.ROOT, 'books', '02-regression', 'figures')
DATA = os.path.join(figlib.ROOT, 'books', '02-regression', 'figdata')

ACC, ACC_DEEP, ACC_TINT, ACC_LINE = '#4338CA', '#312E81', '#EEF0FB', '#C3C7F2'


def load(name):
    """R이 만든 그림용 자료(figdata/*.json)."""
    import json
    with open(os.path.join(DATA, name), encoding='utf-8') as f:
        return json.load(f)


def write(name, content):
    figlib.write(name, content)


# ---------------------------------------------------------------- 경로도 도구
import math


def halo(x, y, s, size=13, color=SOFT, weight=None, anchor='middle'):
    """선 위에 얹어도 읽히도록 흰 테두리를 두른 글자."""
    return text(x, y, s, size, color, weight, anchor,
                ' paint-order="stroke" stroke="#fff" stroke-width="5" stroke-linejoin="round"')


def box(cx, cy, w, h, label, fill=None, stroke=None, color=INK, size=16, weight=700,
        sub=None, rx=10, sw=2):
    """가운데 (cx, cy)에 이름표 상자. 경로도의 변수 상자로 쓴다. 상자 정보도 돌려준다."""
    fill = fill or ACC_TINT
    stroke = stroke or ACC
    out = [f'<rect x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w:.0f}" height="{h:.0f}" '
           f'rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>']
    if sub:
        out.append(text(cx, cy - 2, label, size, color, weight, 'middle'))
        out.append(text(cx, cy + size * 0.95, sub, size * 0.72, SOFT, None, 'middle'))
    else:
        out.append(text(cx, cy + size * 0.36, label, size, color, weight, 'middle'))
    return ''.join(out), (cx, cy, w, h)


def arrow(x0, y0, x1, y1, c=MID, w=2.2, head=11, dash=None):
    """끝에 채운 삼각형 머리가 달린 화살표."""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    px, py = -uy, ux
    bx, by = x1 - ux * head, y1 - uy * head
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<path d="M{x0:.1f},{y0:.1f} L{bx:.1f},{by:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'
            f'<path d="M{x1:.1f},{y1:.1f} L{bx + px * head * .48:.1f},{by + py * head * .48:.1f} '
            f'L{bx - px * head * .48:.1f},{by - py * head * .48:.1f} Z" fill="{c}"/>')


def _edge_point(b, tx, ty, gap):
    """상자 b의 가운데에서 (tx, ty) 쪽으로 나간 직선이 상자 테두리와 만나는 점."""
    cx, cy, w, h = b
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return cx, cy
    sx = (w / 2 + gap) / abs(dx) if dx else float('inf')
    sy = (h / 2 + gap) / abs(dy) if dy else float('inf')
    s = min(sx, sy)
    return cx + dx * s, cy + dy * s


def link(b1, b2, c=MID, w=2.2, gap=5, dash=None):
    """상자 b1에서 b2로 가는 화살표. 상자 테두리에서 시작해 테두리에서 끝난다.
    (화살표, 시작점, 끝점)을 돌려준다."""
    x0, y0 = _edge_point(b1, b2[0], b2[1], gap)
    x1, y1 = _edge_point(b2, b1[0], b1[1], gap)
    return arrow(x0, y0, x1, y1, c, w, dash=dash), (x0, y0), (x1, y1)


def to_point(b, x, y, c=MID, w=2.2, gap=5, dash=None):
    """상자 b에서 임의의 점(다른 화살표의 중간 등)으로 가는 화살표."""
    x0, y0 = _edge_point(b, x, y, gap)
    return arrow(x0, y0, x, y, c, w, dash=dash)
