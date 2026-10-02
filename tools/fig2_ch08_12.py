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



# ================================================================ 9장
def _med(b, cx0, cy0, nums=None, w=900):
    """매개 삼각형. nums = (a, b, c') 문자열이면 경로에 숫자를 단다."""
    X, bx = box(cx0, cy0 + 90, 150, 54, '직무스트레스', size=14.5)
    M, bm = box(cx0 + 260, cy0, 120, 54, '소진', fill=ACC_TINT, stroke=ACC, size=15)
    Y, by = box(cx0 + 520, cy0 + 90, 130, 54, '이직의도', size=14.5)
    a, p0, p1 = link(bx, bm, ACC, 2.6)
    bb, q0, q1 = link(bm, by, ACC, 2.6)
    c, r0, r1 = link(bx, by, MID, 2.4)
    b += [a, bb, c, X, M, Y]
    ma = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
    mb = ((q0[0] + q1[0]) / 2, (q0[1] + q1[1]) / 2)
    mc = ((r0[0] + r1[0]) / 2, r0[1])
    if nums:
        b.append(rich(ma[0] - 14, ma[1] - 6, [('m', 'a'), ('t', ' = ' + nums[0])], 15, ACC_DEEP, 'end', 700))
        b.append(rich(mb[0] + 14, mb[1] - 6, [('m', 'b'), ('t', ' = ' + nums[1])], 15, ACC_DEEP, 'start', 700))
        b.append(rich(mc[0], mc[1] + 24, [('m', "c'"), ('t', ' = ' + nums[2] + '  (직접효과)')], 15, MID, 'middle', 700))
    else:
        b.append(tex(ma[0] - 14, ma[1] - 10, 'a', 18, ACC_DEEP, 'end', 40))
        b.append(tex(mb[0] + 14, mb[1] - 10, 'b', 18, ACC_DEEP, 'start', 40))
        b.append(tex(mc[0], mc[1] + 22, "c'", 18, MID, 'middle', 60))
    return ma, mb, mc


def fig_concept9():
    W, H = 900, 290
    b = []
    ma, mb, mc = _med(b, 160, 78)
    b.append(rich(430, 24, [('t', '간접경로: 소진을 거쳐 감  '), ('m', r'a \times b')], 14.5, ACC_DEEP, 'middle', 700))
    b.append(text(mc[0], mc[1] + 52, '직접경로: 소진을 거치지 않음', 13.5, MID, 700, 'middle'))
    write('ch09-concept.svg', svg(W, H, '\n'.join(b)))


def fig_decompose():
    W, H = 900, 400
    b = []
    X, bx = box(235, 50, 150, 54, '직무스트레스', size=14.5)
    Y, by = box(755, 50, 130, 54, '이직의도', size=14.5)
    a, p0, p1 = link(bx, by, NAVY, 2.8)
    b += [a, X, Y]
    b.append(rich(495, 38, [('m', 'c'), ('t', ' = 0.584  (총효과)')], 15, NAVY, 'middle', 800))
    b.append(text(40, 54, '소진을', 13.5, SOFT, 700))
    b.append(text(40, 72, '빼면', 13.5, SOFT, 700))
    b.append(line(40, 130, 860, 130, RULE, 1.4, '4 4'))
    b.append(text(40, 214, '소진을', 13.5, SOFT, 700))
    b.append(text(40, 232, '넣으면', 13.5, SOFT, 700))
    _med(b, 235, 160, ('0.602', '0.562', '0.245'))
    b.append(rich(495, 362, [('t', '간접효과  '), ('m', r'a \times b = 0.602 \times 0.562 = 0.338'), ('t', '   (총효과의 58%)')], 15, ACC_DEEP, 'middle', 800))
    write('ch09-decompose.svg', svg(W, H, '\n'.join(b)))


def fig_boot():
    D = load('ch09-boot.json')
    ab = D['ab']
    W, H = 900, 360
    lo_x, hi_x, step = 0.0, 0.56, 0.01
    nb = int((hi_x - lo_x) / step)
    counts = [0] * nb
    for v in ab:
        k = int((v - lo_x) / step)
        if 0 <= k < nb:
            counts[k] += 1
    ymax = max(counts) * 1.12
    fr, sx, sy = frame(90, 50, 760, 230, (lo_x, hi_x), (0, ymax), [0, .1, .2, .3, .4, .5], [],
                       '간접효과 a × b (2,000개)', None, grid=False, xfmt=lambda v: f'{v:.1f}')
    b = fr
    for k, n in enumerate(counts):
        x0 = lo_x + k * step
        inside = D['lo'] <= x0 + step / 2 <= D['hi']
        b.append(f'<rect x="{sx(x0) + .6:.1f}" y="{sy(n):.1f}" width="{sx(x0 + step) - sx(x0) - 1.2:.1f}" '
                 f'height="{sy(0) - sy(n):.1f}" fill="{ACC if inside else FAINT}" fill-opacity="{.75 if inside else .6}"/>')
    for v, lab, anc in ((D['lo'], f'2.5%  {D["lo"]:.3f}', 'end'), (D['hi'], f'97.5%  {D["hi"]:.3f}', 'start')):
        b.append(line(sx(v), 50, sx(v), sy(0), CORAL, 2, '6 4'))
        b.append(halo(sx(v) + (-8 if anc == 'end' else 8), 66, lab, 13.5, CORAL, 700, anc))
    b.append(line(sx(D['est']), 40, sx(D['est']), sy(0), INK, 2.4))
    b.append(halo(sx(D['est']), 32, f'추정값 {D["est"]:.3f}', 14, INK, 800))
    b.append(halo(sx(0) + 8, sy(0) - 12, '0은 한참 바깥', 13, MID, 700, 'start'))
    write('ch09-boot.svg', svg(W, H, '\n'.join(b)))



# ================================================================ 10장
def fig_concept10():
    W, H = 900, 300
    b = []
    X, bx = box(160, 200, 150, 54, '직무스트레스', size=14.5)
    M, bm = box(430, 110, 120, 54, '소진', fill=ACC_TINT, stroke=ACC, size=15)
    Y, by = box(700, 200, 130, 54, '이직의도', size=14.5)
    Wb, bw = box(160, 50, 150, 54, '사회적지지', fill=AMBER_TINT, stroke=AMBER, size=14.5)
    a, p0, p1 = link(bx, bm, ACC, 2.8)
    bb, _, _ = link(bm, by, ACC, 2.8)
    c, r0, r1 = link(bx, by, MID, 2.2)
    b += [a, bb, c]
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    b.append(to_point(bw, mx, my, AMBER, 2.4, dash='6 4'))
    b.append(f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="4.5" fill="{AMBER}"/>')
    b += [X, M, Y, Wb]
    b.append(tex(mx + 22, my + 22, r'a_1 + a_3 W', 15, ACC_DEEP, 'start', 120))
    b.append(tex(585, 142, 'b', 16, ACC_DEEP, 'start', 30))
    b.append(tex(430, 218, "c'", 16, MID, 'middle', 40))
    b.append(rich(560, 274, [('t', '간접효과 '), ('m', r'= (a_1 + a_3 W) \times b'), ('t', '   →  지지(W)에 따라 달라진다')], 14.5, INK, 'middle', 700))
    write('ch10-concept.svg', svg(W, H, '\n'.join(b)))


def fig_conditional():
    D = load('ch10.json')
    W, H = 900, 340
    fr, sx, sy = frame(140, 40, 560, 230, (0, 3), (0, 0.6), [], [0, .1, .2, .3, .4, .5, .6], None, '간접효과',
                       yfmt=lambda v: f'{v:.1f}')
    b = fr
    pts = [('low', '지지 낮음', '−1 SD', CORAL), ('mid', '지지 평균', '', ACC), ('high', '지지 높음', '+1 SD', TEAL)]
    xy = []
    for i, (k, lab, sub, c) in enumerate(pts):
        est, lo, hi = D[k]
        x = sx(i + 0.5)
        xy.append((x, sy(est)))
        b.append(line(x, sy(lo), x, sy(hi), c, 3))
        for v in (lo, hi):
            b.append(line(x - 8, sy(v), x + 8, sy(v), c, 2.4))
        b.append(f'<circle cx="{x:.1f}" cy="{sy(est):.1f}" r="8" fill="{c}"/>')
        b.append(halo(x + 16, sy(est) + 5, f'{est:.3f}', 14, c, 800, 'start'))
        b.append(text(x, 292, lab, 14.5, INK, 700, 'middle'))
        if sub:
            b.append(text(x, 310, sub, 12.5, SOFT, 600, 'middle'))
    b.append('<path d="M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in xy) + f'" fill="none" stroke="{MID}" stroke-width="1.6" stroke-dasharray="5 4"/>')
    est, lo, hi = D['index']
    b.append(text(730, 110, '조절된 매개지수', 14.5, INK, 800))
    b.append(rich(730, 136, [('m', r'a_3 \times b = ' + f'{est:.3f}'.replace('-', '-'))], 15, CORAL, 'start', 700))
    b.append(text(730, 162, f'95% CI [{lo:.3f}, {hi:.3f}]'.replace('-', '−'), 13.5, MID, 600))
    b.append(text(730, 186, '0을 포함하지 않음', 13.5, MID, 600))
    write('ch10-conditional.svg', svg(W, H, '\n'.join(b)))



# ================================================================ 11장
def _logistic(z):
    return 1 / (1 + math.exp(-z))


def fig_linear_vs_logit():
    D = load('ch11.json')
    g = random.Random(5)
    W, H = 900, 380
    fr, sx, sy = frame(110, 40, 640, 270, (1, 5), (-0.25, 1.15), [1, 2, 3, 4, 5], [0, 0.5, 1],
                       '이직의도', '퇴사 (확률)', yfmt=lambda v: f'{v:g}')
    b = fr
    b.append(f'<rect x="110" y="{sy(0):.1f}" width="640" height="{sy(-0.25) - sy(0):.1f}" fill="{CORAL}" fill-opacity=".07"/>')
    b.append(line(110, sy(0), 750, sy(0), FAINT, 1.2))
    b.append(line(110, sy(1), 750, sy(1), FAINT, 1.2))
    xs = [x + g.uniform(-.05, .05) for x in D['x']]
    ys = [y + g.uniform(-.05, .05) for y in D['y']]
    b.append(dots(xs, ys, sx, sy, MID, 3.4, .35))
    l0, l1 = D['lin']
    b.append(line(sx(1), sy(l0 + l1), sx(5), sy(l0 + l1 * 5), CORAL, 2.6, '8 5'))
    u0, u1 = D['uni']
    pts = [1 + 4 * i / 100 for i in range(101)]
    b.append('<path d="M' + ' L'.join(f'{sx(x):.1f},{sy(_logistic(u0 + u1 * x)):.1f}' for x in pts) +
             f'" fill="none" stroke="{ACC_DEEP}" stroke-width="3.2"/>')
    b.append(halo(sx(1.55), sy(-0.18), '직선은 확률 0 아래로 내려간다', 13.5, CORAL, 700, 'start'))
    b.append(text(770, 120, '실선', 14, ACC_DEEP, 800))
    b.append(text(770, 140, '로지스틱 곡선', 13.5, ACC_DEEP, 700))
    b.append(text(770, 160, '0과 1 사이에 머문다', 13, MID, 600))
    b.append(text(770, 210, '점선', 14, CORAL, 800))
    b.append(text(770, 230, '직선 회귀', 13.5, CORAL, 700))
    write('ch11-linear-vs-logit.svg', svg(W, H, '\n'.join(b)))


def fig_logit_map():
    W, H = 900, 360
    fr, sx, sy = frame(110, 40, 620, 250, (-5, 5), (0, 1), [-4, -2, 0, 2, 4], [0, .21, .5, .79, 1],
                       '로짓 (로그오즈)', '확률', yfmt=lambda v: f'{v:g}'.replace('0.', '.'),
                       xfmt=lambda v: f'{v:g}'.replace('-', '−'))
    b = fr
    pts = [-5 + 10 * i / 200 for i in range(201)]
    b.append('<path d="M' + ' L'.join(f'{sx(z):.1f},{sy(_logistic(z)):.1f}' for z in pts) +
             f'" fill="none" stroke="{ACC_DEEP}" stroke-width="3.2"/>')
    for p, c in ((.21, CORAL), (.5, INK), (.79, TEAL)):
        z = math.log(p / (1 - p))
        b.append(line(sx(-5), sy(p), sx(z), sy(p), c, 1.4, '4 4'))
        b.append(line(sx(z), sy(p), sx(z), sy(0), c, 1.4, '4 4'))
        b.append(f'<circle cx="{sx(z):.1f}" cy="{sy(p):.1f}" r="6" fill="{c}"/>')
        lab = '로짓 0' if abs(z) < 1e-9 else f'로짓 {z:+.2f}'.replace('-', '−')
        b.append(halo(sx(z) + 10, sy(p) + 18, lab, 13, c, 700, 'start'))
    b.append(tex(750, 100, r'p = \dfrac{1}{1 + e^{-\text{로짓}}}', 19, ACC_DEEP, 'start', 150, 70))
    b.append(text(750, 160, '로짓은 어떤 값이든', 13.5, MID, 600))
    b.append(text(750, 180, '확률은 0과 1 사이', 13.5, MID, 600))
    write('ch11-logit-map.svg', svg(W, H, '\n'.join(b)))


def fig_prob():
    D = load('ch11.json')
    c0, c1, c2 = D['multi']
    ms = D['ms']
    W, H = 900, 360
    fr, sx, sy = frame(110, 40, 580, 250, (1, 5), (0, 1), [1, 2, 3, 4, 5], [0, .2, .4, .6, .8, 1],
                       '이직의도', '퇴사 예측 확률', yfmt=lambda v: f'{v:.1f}')
    b = fr
    pts = [1 + 4 * i / 100 for i in range(101)]
    pr = lambda x: _logistic(c0 + c1 * x + c2 * ms)
    b.append('<path d="M' + ' L'.join(f'{sx(x):.1f},{sy(pr(x)):.1f}' for x in pts) +
             f'" fill="none" stroke="{ACC_DEEP}" stroke-width="3.2"/>')
    for x in (2, 3, 4):
        p = pr(x)
        b.append(line(sx(x), sy(0), sx(x), sy(p), FAINT, 1.4, '4 4'))
        b.append(f'<circle cx="{sx(x):.1f}" cy="{sy(p):.1f}" r="7" fill="{ACC}"/>')
        b.append(halo(sx(x) - 10, sy(p) - 8, f'{p * 100:.1f}%', 14, ACC_DEEP, 800, 'end'))
    b.append(text(714, 110, '오즈비는 어디서나 3.43', 13.5, INK, 700))
    b.append(text(714, 132, '확률의 배수는', 13.5, MID, 600))
    b.append(text(714, 152, '2→3점 2.9배', 13.5, MID, 600))
    b.append(text(714, 172, '3→4점 2.3배', 13.5, MID, 600))
    b.append(text(714, 214, '직무만족은 평균에 고정', 12.5, SOFT, 600))
    write('ch11-prob.svg', svg(W, H, '\n'.join(b)))


def fig_classification():
    D = load('ch11.json')['tab']
    W, H = 900, 300
    b = []
    x0, y0, cw, ch = 300, 70, 170, 80
    b.append(text(x0 + cw, 30, '예측', 15, INK, 800, 'middle'))
    b.append(text(x0 + cw / 2, 58, '재직 (0)', 14, MID, 700, 'middle'))
    b.append(text(x0 + cw * 1.5, 58, '퇴사 (1)', 14, MID, 700, 'middle'))
    b.append(text(x0 - 120, y0 + ch + 6, '실제', 15, INK, 800, 'middle'))
    b.append(text(x0 - 14, y0 + ch / 2 + 5, '재직 (0)', 14, MID, 700, 'end'))
    b.append(text(x0 - 14, y0 + ch * 1.5 + 5, '퇴사 (1)', 14, MID, 700, 'end'))
    cells = [(0, 0, D['tn'], '맞음', ACC_TINT, ACC_DEEP), (1, 0, D['fp'], '틀림', CORAL_TINT, CORAL),
             (0, 1, D['fn'], '틀림 — 놓친 퇴사자', CORAL_TINT, CORAL), (1, 1, D['tp'], '맞음', ACC_TINT, ACC_DEEP)]
    for i, j, n, lab, fill, c in cells:
        x, y = x0 + i * cw, y0 + j * ch
        b.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="{fill}" stroke="#fff" stroke-width="3"/>')
        b.append(text(x + cw / 2, y + 40, f'{n}', 26, c, 800, 'middle'))
        b.append(text(x + cw / 2, y + 62, lab, 12.5, c, 700, 'middle'))
    tot = D['tn'] + D['fp'] + D['fn'] + D['tp']
    acc = (D['tn'] + D['tp']) / tot
    sens = D['tp'] / (D['tp'] + D['fn'])
    spec = D['tn'] / (D['tn'] + D['fp'])
    base = (D['tn'] + D['fp']) / tot
    lx = 680
    for k, (name, v, c) in enumerate([('정확도', acc, INK), ('모두 재직으로 찍으면', base, SOFT),
                                       ('민감도 (퇴사자 적중)', sens, CORAL), ('특이도 (재직자 적중)', spec, ACC_DEEP)]):
        b.append(text(lx, 92 + k * 42, name, 13.5, MID, 600))
        b.append(text(lx, 112 + k * 42, f'{v * 100:.1f}%', 17, c, 800))
    write('ch11-classification.svg', svg(W, H, '\n'.join(b)))


ALL = [fig_concept8, fig_simple_slopes, fig_jn, fig_concept9, fig_decompose, fig_boot,
       fig_concept10, fig_conditional, fig_linear_vs_logit, fig_logit_map, fig_prob, fig_classification]
