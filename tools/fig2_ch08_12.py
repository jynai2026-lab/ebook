"""2권 8~12장 그림"""
import os, random
import figlib
from fig2lib import *


# ================================================================ 8장
def fig_concept8():
    W, H = 900, 270
    b = []
    # 왼쪽: 개념 모형
    X, bx = box(90, 170, 130, 54, '직무스트레스', size=14)
    Y, by = box(370, 170, 110, 54, '소진', size=15)
    Wb, bw = box(230, 60, 130, 54, '사회적지지', fill=AMBER_TINT, stroke=AMBER, size=14)
    a, p0, p1 = link(bx, by, ACC, 2.6)
    b += [a]
    mx = (p0[0] + p1[0]) / 2
    b.append(to_point(bw, mx, p0[1] - 2, AMBER, 2.4))
    b += [X, Y, Wb]
    b.append(text(230, 250, '개념 모형', 15, INK, 800, 'middle'))
    b.append(line(470, 30, 470, 240, RULE, 1.6))
    # 오른쪽: 통계 모형
    X2, bx2 = box(600, 60, 150, 46, '직무스트레스 X', size=13.5)
    W2, bw2 = box(600, 140, 150, 46, '사회적지지 W', fill=AMBER_TINT, stroke=AMBER, size=13.5)
    XW, bxw = box(600, 220, 150, 46, 'X × W', fill=CORAL_TINT, stroke=CORAL, size=14)
    Y2, by2 = box(820, 140, 100, 54, '소진', size=15)
    for bb, c, lab in ((bx2, ACC, 'b₁'), (bw2, AMBER, 'b₂'), (bxw, CORAL, 'b₃')):
        aa, q0, q1 = link(bb, by2, c, 2.2)
        b.append(aa)
    b += [X2, W2, XW, Y2]
    b.append(tex(712, 74, 'b_1', 15, ACC_DEEP, 'middle', 40))
    b.append(tex(712, 128, 'b_2', 15, AMBER, 'middle', 40))
    b.append(tex(712, 200, 'b_3', 15, CORAL, 'middle', 40))
    b.append(text(700, 266, '통계 모형 — 곱하기 항의 계수가 조절효과', 15, INK, 800, 'middle'))
    write('ch08-concept.svg', svg(W, H + 6, '\n'.join(b)))


def fig_simple_slopes():
    D = load('ch08.json')
    b0, be, bs, bw, bi = D['b']
    W, H = 900, 400
    fr, sx, sy = frame(90, 40, 620, 290, (1, 5), (1, 5), [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], '직무스트레스', '소진')
    b = fr
    b.append(dots(D['x'], D['y'], sx, sy, FAINT, 3.2, .35))
    levels = [(-1, '지지 낮음 (−1 SD)', CORAL), (0, '지지 평균', ACC), (1, '지지 높음 (+1 SD)', TEAL)]
    for k, lab, c in levels:
        wc = k * D['sw']
        def pred(x):
            xc = x - D['mx']
            return b0 + be * D['me'] + bs * xc + bw * wc + bi * xc * wc
        b.append(line(sx(1.3), sy(pred(1.3)), sx(4.6), sy(pred(4.6)), c, 3.4))
        slope = bs + bi * wc
        y = 120 + (k + 1) * 46
        b.append(line(730, y, 764, y, c, 3.4))
        b.append(text(772, y - 2, lab, 13.5, c, 700))
        b.append(rich(772, y + 17, [('t', '기울기 '), ('m', f'{slope:.3f}')], 13, c, 'start', 600))
    write('ch08-simple-slopes.svg', svg(W, H, '\n'.join(b)))


def fig_jn():
    D = load('ch08.json')
    W, H = 900, 420
    fr, sx, sy = frame(90, 40, 700, 250, (1.7, 5.05), (-0.4, 1.6), [2, 2.5, 3, 3.5, 4, 4.5, 5],
                       [-0.4, 0, 0.4, 0.8, 1.2, 1.6], None, '스트레스의 기울기',
                       yfmt=lambda v: f'{v:.1f}')
    b = fr
    ws, sl, lo, hi = D['jn_w'], D['jn_sl'], D['jn_lo'], D['jn_hi']
    top = ' L'.join(f'{sx(w):.1f},{sy(v):.1f}' for w, v in zip(ws, hi))
    bot = ' L'.join(f'{sx(w):.1f},{sy(v):.1f}' for w, v in zip(reversed(ws), list(reversed(lo))))
    b.append('<clipPath id="jnclip"><rect x="90" y="40" width="700" height="250"/></clipPath>')
    b.append(f'<path d="M{top} L{bot} Z" fill="{ACC}" fill-opacity=".16" clip-path="url(#jnclip)"/>')
    b.append('<path d="M' + ' L'.join(f'{sx(w):.1f},{sy(v):.1f}' for w, v in zip(ws, sl)) +
             f'" fill="none" stroke="{ACC_DEEP}" stroke-width="3"/>')
    b.append(line(90, sy(0), 790, sy(0), MID, 1.6))
    jn = next(w for w, l in zip(ws, lo) if l <= 0)
    b.append(f'<rect x="{sx(jn):.1f}" y="40" width="{790 - sx(jn):.1f}" height="250" fill="{CORAL}" fill-opacity=".07"/>')
    b.append(line(sx(jn), 40, sx(jn), 290, CORAL, 2, '6 4'))
    b.append(halo(sx(jn) - 8, 62, f'{jn:.2f}점', 14, CORAL, 800, 'end'))
    b.append(text(sx(jn) + 10, 62, '여기부터', 13, CORAL, 700))
    b.append(text(sx(jn) + 10, 80, '유의하지 않음', 13, CORAL, 700))
    for k, c in ((-1, CORAL), (0, ACC), (1, TEAL)):
        w = D['mw'] + k * D['sw']
        i = min(range(len(ws)), key=lambda j: abs(ws[j] - w))
        b.append(f'<circle cx="{sx(w):.1f}" cy="{sy(sl[i]):.1f}" r="6" fill="{c}"/>')
    b.append(halo(sx(2.0), sy(1.15), '95% 신뢰구간', 13, ACC, 700, 'start'))
    # 아래: 지지 점수의 분포
    base = 380
    bins = {}
    for w in D['w']:
        k = round(w * 4) / 4
        bins[k] = bins.get(k, 0) + 1
    mx = max(bins.values())
    for k, n in bins.items():
        h = n / mx * 46
        b.append(f'<rect x="{sx(k) - 9:.1f}" y="{base - h:.1f}" width="18" height="{h:.1f}" fill="{FAINT if k < jn else CORAL}" fill-opacity=".7"/>')
    b.append(line(90, base, 790, base, FAINT, 1.2))
    b.append(text(440, base + 30, '사회적지지 (원점수) — 아래 막대는 사람 수', 14, MID, 600, 'middle'))
    for t in [2, 3, 4, 5]:
        b.append(text(sx(t), base + 14, f'{t}', 12, SOFT, None, 'middle'))
    write('ch08-jn.svg', svg(W, H + 10, '\n'.join(b)))


ALL = [fig_concept8, fig_simple_slopes, fig_jn]
