"""
그림 생성 공통 도구

색은 shared/theme/book.css 의 토큰과 맞춰 두었습니다.
본문 색을 바꾸면 여기도 함께 고쳐야 합니다.
"""
import math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'books', '01-basic-statistics', 'figures')

INK, MID, SOFT, FAINT = '#101828', '#344054', '#667085', '#98A2B3'
TEAL, TEAL_LINE, TEAL_TINT = '#0E7490', '#A8D5DE', '#ECF7F9'
NAVY, NAVY_TINT, RULE = '#16243F', '#C7D0DE', '#E4E7EC'
CORAL, CORAL_TINT = '#C2452F', '#FBEAE6'
AMBER, AMBER_TINT = '#B54708', '#FEF0C7'
PAPER = '#FBFCFD'

FONT = 'Pretendard, sans-serif'


def svg(w, h, body):
    return (f'<svg viewBox="0 0 {w} {h}" font-family="{FONT}" '
            f'xmlns="http://www.w3.org/2000/svg">\n{body}\n</svg>\n')


def write(name, content):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  {name}')


def normal_pts(mu, sd, x0, x1, n=100):
    """정규분포 (x, y) 점들. y는 확률밀도 그대로."""
    out = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        y = math.exp(-((x - mu) ** 2) / (2 * sd ** 2)) / (sd * math.sqrt(2 * math.pi))
        out.append((x, y))
    return out


def scale(x0, x1, px0, px1):
    """자료 좌표 -> 화면 x좌표 변환 함수."""
    return lambda x: px0 + (px1 - px0) * (x - x0) / (x1 - x0)


def curve_paths(pts, sx, base, top, peak):
    """(선 path, 채움 path)를 함께 돌려준다.

    여러 곡선을 겹칠 때는 채움을 모두 그린 뒤 선을 그려야 한다.
    그렇지 않으면 뒤 곡선의 반투명 채움이 앞 곡선의 선을 덮어 회색으로 보인다.
    peak은 함께 그리는 곡선 중 가장 큰 y여야 한다. 작게 잡으면 곡선이
    top 위로 넘어가 제목을 침범한다.
    """
    scr = [(sx(x), base - (y / peak) * (base - top)) for x, y in pts]
    line = 'M' + ' L'.join(f'{px:.1f},{py:.1f}' for px, py in scr)
    area = line + f' L{scr[-1][0]:.1f},{base} L{scr[0][0]:.1f},{base} Z'
    return line, area


def axis(px0, px1, base, color=MID, w=2):
    return f'<path d="M{px0},{base} L{px1},{base}" stroke="{color}" stroke-width="{w}"/>'


def panel(x0, y0, w, h, stroke=RULE, sw=2, fill=PAPER):
    return f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def text(x, y, s, size=14, color=SOFT, weight=None, anchor=None, extra=''):
    a = f' text-anchor="{anchor}"' if anchor else ''
    fw = f' font-weight="{weight}"' if weight else ''
    return f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" fill="{color}"{fw}{a}{extra}>{s}</text>'


def dashed(x, y0, y1, color, w=2, dash='5 4'):
    return f'<path d="M{x:.0f},{y0:.0f} L{x:.0f},{y1:.0f}" stroke="{color}" stroke-width="{w}" stroke-dasharray="{dash}"/>'


def caption(x, y, s, size=14, color=MID):
    return text(x, y, s, size, color, anchor='middle')


def tex(x, y, latex, size=15, color=INK, anchor='middle', w=380, h=None, baseline=False):
    """수식을 KaTeX로 조판해 넣는다.

    SVG의 <text>로는 분수를 가로선으로, 근호를 제대로 된 기호로 그릴 수 없다.
    그래서 자리표시자만 남기고, 빌드(build.mjs)가 SVG를 본문에 끼워 넣을 때
    KaTeX HTML로 바꾼다.

    (x, y)는 수식이 놓일 자리다. anchor가 'middle'이면 가운데, 'start'면
    왼쪽 끝, 'end'면 오른쪽 끝이 그 x에 온다. w는 글상자의 폭일 뿐이고
    배경이 없으므로 넉넉히 잡아도 다른 요소를 가리지 않는다.

    baseline=True면 y를 text()와 같은 글줄 기준선으로 본다. 한 줄 안에서
    text()와 나란히 놓을 때 쓴다. 기본값(False)은 y를 수식의 세로 가운데로
    보므로, 분수처럼 위아래로 뻗는 수식을 홀로 놓을 때 알맞다.
    """
    if baseline:
        y -= size * 0.36
    h = h or size * 2.8
    just = {'middle': 'center', 'start': 'flex-start', 'end': 'flex-end'}[anchor]
    fx = {'middle': x - w / 2, 'start': x, 'end': x - w}[anchor]
    safe = (latex.replace('&', '&amp;').replace('<', '&lt;')
                 .replace('>', '&gt;').replace('"', '&quot;'))
    return (f'<foreignObject x="{fx:.0f}" y="{y - h / 2:.0f}" '
            f'width="{w:.0f}" height="{h:.0f}">'
            f'<div xmlns="http://www.w3.org/1999/xhtml" class="figtex" '
            f'style="justify-content:{just};font-size:{size}px;color:{color}">'
            f'<span data-tex="{safe}"></span></div></foreignObject>')


CANVAS_W = 900          # 그림 SVG의 표준 폭


def rich(x, y, parts, size=15, color=INK, anchor='middle', weight=None, w=None, h=None):
    """한글과 수식이 섞인 한 줄을 배치한다.

    파이썬에서 글자 폭을 어림해 좌표를 계산하면 어림이 틀린 만큼 간격이
    벌어진다. 그래서 조각을 그대로 넘기고 정렬은 브라우저(flex)에 맡긴다.

    parts: ('t', '글자') 또는 ('m', 'LaTeX') 의 나열.
           간격은 글자 조각 안의 공백으로 준다 (white-space: pre).
    y는 text()와 같은 글줄 기준선이다.
    """
    h = h or size * 2.8
    y -= size * 0.36
    just = {'middle': 'center', 'start': 'flex-start', 'end': 'flex-end'}[anchor]
    if w is None:
        # 글상자가 그림 밖으로 나가면 잘리므로, 놓일 자리에 맞춰 폭을 잡는다
        room = {'middle': 2 * min(x, CANVAS_W - x), 'start': CANVAS_W - x, 'end': x}[anchor]
        w = max(60, min(760, room))
    fx = {'middle': x - w / 2, 'start': x, 'end': x - w}[anchor]

    inner = []
    for kind, val in parts:
        if not val:
            continue
        if kind == 't':
            esc = val.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            fw = f'font-weight:{weight};' if weight else ''
            inner.append(f'<span style="white-space:pre;{fw}">{esc}</span>')
        else:
            safe = (val.replace('&', '&amp;').replace('<', '&lt;')
                       .replace('>', '&gt;').replace('"', '&quot;'))
            inner.append(f'<span data-tex="{safe}"></span>')
    return (f'<foreignObject x="{fx:.0f}" y="{y - h / 2:.0f}" '
            f'width="{w:.0f}" height="{h:.0f}">'
            f'<div xmlns="http://www.w3.org/1999/xhtml" class="figtex" '
            f'style="justify-content:{just};font-size:{size}px;color:{color}">'
            f'{"".join(inner)}</div></foreignObject>')


def label_tex(cx, y, korean, latex, size=15, color=INK, weight=700, gap=None):
    """'분산 s²'처럼 한글과 기호가 섞인 이름표를 가운데 정렬로 놓는다."""
    return rich(cx, y, [('t', korean + ' ' if korean else ''), ('m', latex)],
                size, color, 'middle', weight)
