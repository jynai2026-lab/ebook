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


# ---------------------------------------------------------------- 좌표 평면
def frame(x0, y0, w, h, xr, yr, xticks, yticks, xlabel=None, ylabel=None,
          xfmt=None, yfmt=None, size=12.5, grid=True):
    """자료 그림의 틀. (조각들, x변환, y변환)을 돌려준다.
    (x0, y0)은 그림 영역의 왼쪽 위, w·h는 크기. 축 이름은 x축 아래, y축 위에 가로로 쓴다."""
    xfmt = xfmt or (lambda v: f'{v:g}')
    yfmt = yfmt or (lambda v: f'{v:g}')
    sx = lambda v: x0 + (v - xr[0]) / (xr[1] - xr[0]) * w
    sy = lambda v: y0 + h - (v - yr[0]) / (yr[1] - yr[0]) * h
    b = []
    if grid:
        for t in yticks:
            b.append(f'<path d="M{x0},{sy(t):.1f} L{x0 + w},{sy(t):.1f}" stroke="{RULE}" stroke-width="1"/>')
    b.append(f'<path d="M{x0},{y0} L{x0},{y0 + h} L{x0 + w},{y0 + h}" stroke="{FAINT}" stroke-width="1.4" fill="none"/>')
    for t in xticks:
        b.append(text(sx(t), y0 + h + size + 6, xfmt(t), size, SOFT, None, 'middle'))
    for t in yticks:
        b.append(text(x0 - 8, sy(t) + size * 0.35, yfmt(t), size, SOFT, None, 'end'))
    if xlabel:
        b.append(text(x0 + w / 2, y0 + h + size * 2 + 14, xlabel, size + 1, MID, 600, 'middle'))
    if ylabel:
        b.append(text(x0 - 8, y0 - 12, ylabel, size + 1, MID, 600, 'start' if x0 < 60 else 'middle'))
    return b, sx, sy


def dots(xs, ys, sx, sy, c=None, r=4.2, op=.45, stroke=None):
    c = c or ACC
    st = f' stroke="{stroke}" stroke-width="1"' if stroke else ''
    return ''.join(f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="{r}" fill="{c}" fill-opacity="{op}"{st}/>'
                   for x, y in zip(xs, ys))


def line(x0, y0, x1, y1, c=INK, w=2.4, dash=None, op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    o = f' stroke-opacity="{op}"' if op != 1 else ''
    return f'<path d="M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}" stroke="{c}" stroke-width="{w}"{d}{o}/>'


def ols(xs, ys):
    """최소제곱 절편과 기울기."""
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    b1 = sxy / sxx
    return my - b1 * mx, b1


def corr(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    return sxy / math.sqrt(sxx * syy)


def exact_r(r, n=100, seed=1):
    """표본 상관계수가 정확히 r인 (x, y) 표준점수 쌍."""
    import random
    g = random.Random(seed)
    x = [g.gauss(0, 1) for _ in range(n)]
    e = [g.gauss(0, 1) for _ in range(n)]

    def std(v):
        m = sum(v) / len(v)
        s = math.sqrt(sum((a - m) ** 2 for a in v) / (len(v) - 1))
        return [(a - m) / s for a in v]
    x = std(x)
    # e에서 x 성분을 빼 x와 정확히 직교하게 만든다
    k = sum(a * b for a, b in zip(x, e)) / sum(a * a for a in x)
    e = std([b - k * a for a, b in zip(x, e)])
    y = [r * a + math.sqrt(1 - r * r) * b for a, b in zip(x, e)]
    return x, y
