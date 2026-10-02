"""2권 4~7장 그림"""
import os, random
import figlib
from fig2lib import *


# ================================================================ 4장
def fig_model_picture():
    W, H = 900, 380
    b, sx, sy = frame(90, 30, 640, 300, (0, 10), (0, 10), [], [], 'X', 'Y', grid=False)
    c0, c1, sd = 1.6, 0.72, 0.85
    g = random.Random(4)
    pts = []
    for _ in range(90):
        x = g.uniform(0.6, 9.4)
        pts.append((x, c0 + c1 * x + g.gauss(0, sd)))
    b.append(dots([p[0] for p in pts], [p[1] for p in pts], sx, sy, FAINT, 3.4, .55))
    b.append(line(sx(0.3), sy(c0 + c1 * 0.3), sx(9.7), sy(c0 + c1 * 9.7), ACC_DEEP, 3))
    for xc in (2, 4.5, 7):
        mu = c0 + c1 * xc
        path = []
        for i in range(61):
            t = -3 + 6 * i / 60
            dens = math.exp(-t * t / 2)
            path.append(f'{sx(xc) + dens * 56:.1f},{sy(mu + t * sd):.1f}')
        b.append(f'<path d="M{sx(xc):.1f},{sy(mu - 3 * sd):.1f} L' + ' L'.join(path) +
                 f' L{sx(xc):.1f},{sy(mu + 3 * sd):.1f} Z" fill="{ACC}" fill-opacity=".14" stroke="{ACC}" stroke-width="1.8"/>')
        b.append(line(sx(xc), sy(mu - 3 * sd), sx(xc), sy(mu + 3 * sd), ACC, 1.2, '3 3'))
    ye = sy(c0 + c1 * 9.7)
    b.append(text(sx(9.7) + 12, ye - 4, '회귀선', 14, ACC_DEEP, 800))
    b.append(text(sx(9.7) + 12, ye + 16, '각 X에서 Y의 평균', 13, ACC_DEEP, 600))
    b.append(text(760, 210, '어느 X에서나', 14, MID, 700))
    b.append(text(760, 230, '같은 폭의 정규분포', 14, MID, 700))
    b.append(tex(760, 266, r'\varepsilon \sim N(0, \sigma^2)', 16, ACC, 'start', 130))
    write('ch04-model-picture.svg', svg(W, H, '\n'.join(b)))


def fig_resid_fitted():
    D = load('ch04-diag.json')
    W, H = 900, 380
    b, sx, sy = frame(90, 30, 760, 280, (1.7, 4.0), (-2, 2), [2, 2.5, 3, 3.5, 4], [-2, -1, 0, 1, 2],
                      '예측값', '잔차')
    b.append(line(90, sy(0), 850, sy(0), MID, 1.6, '6 4'))
    b.append(dots(D['fitted'], D['resid'], sx, sy, ACC, 3.8, .35))
    # 예측값을 8구간으로 나눠 잔차 평균을 잇는다
    pairs = sorted(zip(D['fitted'], D['resid']))
    k = 8
    pts = []
    for i in range(k):
        seg = pairs[i * len(pairs) // k:(i + 1) * len(pairs) // k]
        pts.append((sum(p[0] for p in seg) / len(seg), sum(p[1] for p in seg) / len(seg)))
    b.append('<path d="M' + ' L'.join(f'{sx(x):.1f},{sy(y):.1f}' for x, y in pts) +
             f'" fill="none" stroke="{ACC_DEEP}" stroke-width="3"/>')
    for x, y in pts:
        b.append(f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="4.5" fill="{ACC_DEEP}"/>')
    b.append(halo(840, sy(0) - 10, '잔차 = 0', 13, MID, 600, 'end'))
    b.append(halo(sx(pts[-1][0]) - 6, sy(pts[-1][1]) - 14, '구간별 잔차 평균', 13, ACC_DEEP, 700, 'end'))
    write('ch04-resid-fitted.svg', svg(W, H, '\n'.join(b)))


def fig_patterns():
    W, H = 900, 280
    g = random.Random(7)
    titles = ['가정이 맞는 경우', '곡선을 직선으로 적합', '이분산 (깔때기)']
    cols = [ACC, CORAL, AMBER]
    b = []
    pw, gap = 250, 40
    x0 = (W - (3 * pw + 2 * gap)) / 2
    for k in range(3):
        px = x0 + k * (pw + gap)
        fr, sx, sy = frame(px, 50, pw, 170, (0, 10), (-4, 4), [], [0], '예측값', None, grid=False, size=12)
        b += fr
        b.append(line(px, sy(0), px + pw, sy(0), MID, 1.4, '5 4'))
        xs, ys = [], []
        for _ in range(110):
            x = g.uniform(0.4, 9.6)
            if k == 0:
                y = g.gauss(0, 1)
            elif k == 1:
                y = 0.16 * (x - 5) ** 2 - 1.3 + g.gauss(0, .55)
            else:
                y = g.gauss(0, 0.12 + 0.3 * x)
            xs.append(x); ys.append(max(-3.9, min(3.9, y)))
        b.append(dots(xs, ys, sx, sy, cols[k], 3.4, .6))
        b.append(text(px + pw / 2, 30, titles[k], 15, cols[k] if k else ACC_DEEP, 700, 'middle'))
        b.append(text(px - 6, 56, '잔차', 12, MID, 600, 'start'))
    write('ch04-patterns.svg', svg(W, H, '\n'.join(b)))


def fig_curve():
    D = load('ch04-curve.json')
    W, H = 900, 390
    b, sx, sy = frame(90, 40, 760, 280, (1, 5), (2, 7), [1, 2, 3, 4, 5], [2, 3, 4, 5, 6, 7],
                      '각성 수준', '수행')
    b.append(dots(D['x'], D['y'], sx, sy, ACC, 3.8, .35))
    l0, l1 = D['line']
    b.append(line(sx(1), sy(l0 + l1), sx(5), sy(l0 + l1 * 5), SOFT, 2.6, '8 6'))
    q0, q1, q2 = D['curve']
    pts = [(1 + 4 * i / 80) for i in range(81)]
    b.append('<path d="M' + ' L'.join(f'{sx(x):.1f},{sy(q0 + q1 * x + q2 * x * x):.1f}' for x in pts) +
             f'" fill="none" stroke="{ACC_DEEP}" stroke-width="3.2"/>')
    b.append(rich(sx(4.95), sy(2.3), [('t', '직선(점선)  '), ('m', 'R^2 = .005')], 14, SOFT, 'end', 700))
    b.append(rich(sx(3), 30, [('t', '이차항을 넣은 곡선  '), ('m', 'R^2 = .512')], 14, ACC_DEEP, 'middle', 700))
    write('ch04-curve.svg', svg(W, H, '\n'.join(b)))


def fig_qq():
    D = load('ch04-diag.json')
    W, H = 900, 400
    b, sx, sy = frame(250, 30, 400, 300, (-3.2, 3.2), (-3.6, 3.2), [-3, -2, -1, 0, 1, 2, 3], [-3, -2, -1, 0, 1, 2, 3],
                      '정규분포라면 와야 할 값', '표준화 잔차')
    b.append(line(sx(-3.2), sy(-3.2), sx(3.2), sy(3.2), CORAL, 2, '7 5'))
    b.append(dots(D['qx'], D['qy'], sx, sy, ACC, 3.6, .5))
    b.append(halo(sx(3.1), sy(-2.2), '대각선 = 완전한 정규분포', 13, CORAL, 700, 'end'))
    write('ch04-qq.svg', svg(W, H, '\n'.join(b)))


def fig_influence():
    W, H = 900, 300
    base = [(1, 2.2), (2, 2.4), (2.6, 3.4), (3.2, 3.1), (4, 4.2), (4.6, 4.0), (5.2, 5.1), (6, 5.0)]
    extra = [(3.5, 7.6), (11, 9.5), (11, 3.2)]
    titles = ['이상치', '지렛값이 큰 점', '영향점']
    subs = ['Y만 튐 → 선이 조금 뜸', 'X만 튐 → 선 위에 있으면 무해', '둘 다 튐 → 선이 끌려감']
    b = []
    pw, gap = 260, 30
    x0 = (W - (3 * pw + 2 * gap)) / 2
    for k in range(3):
        px = x0 + k * (pw + gap)
        fr, sx, sy = frame(px, 50, pw, 180, (0, 12), (0, 10), [], [], None, None, grid=False)
        b += fr
        a0, a1 = ols([p[0] for p in base], [p[1] for p in base])
        b.append(line(sx(0.3), sy(a0 + a1 * 0.3), sx(11.7), sy(a0 + a1 * 11.7), FAINT, 2.2, '6 5'))
        pts = base + [extra[k]]
        c0, c1 = ols([p[0] for p in pts], [p[1] for p in pts])
        col = [AMBER, TEAL, CORAL][k]
        b.append(line(sx(0.3), sy(c0 + c1 * 0.3), sx(11.7), sy(c0 + c1 * 11.7), col, 2.6))
        b.append(dots([p[0] for p in base], [p[1] for p in base], sx, sy, MID, 4.6, .8))
        ex, ey = extra[k]
        b.append(f'<circle cx="{sx(ex):.1f}" cy="{sy(ey):.1f}" r="7.5" fill="{col}"/>')
        b.append(text(px + pw / 2, 32, titles[k], 16, col, 800, 'middle'))
        b.append(text(px + pw / 2, 258, subs[k], 13.5, MID, 600, 'middle'))
    b.append(line(300, 288, 330, 288, FAINT, 2.2, '6 5'))
    b.append(text(338, 293, '그 점이 없을 때의 회귀선', 12.5, SOFT, 600))
    b.append(line(540, 288, 570, 288, MID, 2.6))
    b.append(text(578, 293, '그 점이 있을 때', 12.5, SOFT, 600))
    write('ch04-influence.svg', svg(W, H + 6, '\n'.join(b)))


def fig_cook():
    D = load('ch04-diag.json')
    W, H = 900, 330
    cook = D['cook']
    b, sx, sy = frame(90, 30, 760, 240, (0, 301), (0, 0.07), [1, 50, 100, 150, 200, 250, 300],
                      [0, 0.02, 0.04, 0.06], '사례 번호', "Cook의 거리", yfmt=lambda v: f'{v:.2f}')
    thr = 4 / 300
    for i, c in enumerate(cook):
        col = ACC if c > thr else FAINT
        b.append(f'<path d="M{sx(i + 1):.1f},{sy(0):.1f} L{sx(i + 1):.1f},{sy(c):.1f}" stroke="{col}" stroke-width="1.6"/>')
    b.append(line(90, sy(thr), 850, sy(thr), CORAL, 1.6, '6 4'))
    b.append(halo(846, sy(thr) - 8, '4/n = .013', 13, CORAL, 700, 'end'))
    i = max(range(len(cook)), key=lambda j: cook[j])
    b.append(halo(sx(i + 1) - 8, sy(cook[i]) + 4, f'{i + 1}번  {cook[i]:.3f}', 13, ACC_DEEP, 700, 'end'))
    b.append(text(450, 22, '기준 1까지 올라가는 사례는 없다', 13.5, MID, 600, 'middle'))
    write('ch04-cook.svg', svg(W, H, '\n'.join(b)))



# ================================================================ 5장
def _axis_rows(b, x0, x1, lo, hi, ticks, y0, y1, fmt=None):
    sx = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    fmt = fmt or (lambda t: f'{t:g}'.replace('-', '−'))
    for t in ticks:
        b.append(f'<path d="M{sx(t):.1f},{y0} L{sx(t):.1f},{y1}" stroke="{FAINT if t == 0 else RULE}" stroke-width="{1.6 if t == 0 else 1}"/>')
        b.append(text(sx(t), y1 + 20, fmt(t), 12.5, SOFT, None, 'middle'))
    return sx


def fig_coef_ci():
    D = load('ch05.json')
    W, H = 900, 330
    b = []
    sx = _axis_rows(b, 290, 860, -0.4, 1.0, [-0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0], 30, 270)
    rows = [('스트레스', '업무과부하 없이', D['stress_alone'], ACC),
            ('', '업무과부하와 함께', D['stress_both'], CORAL),
            ('업무과부하', '스트레스 없이', D['load_alone'], ACC),
            ('', '스트레스와 함께', D['load_both'], CORAL)]
    for i, (name, sub, (est, lo, hi), c) in enumerate(rows):
        y = 60 + i * 55 + (14 if i >= 2 else 0)
        if name:
            b.append(text(20, y + 5, name, 15, INK, 800))
        b.append(text(270, y + 5, sub, 13.5, c, 700, 'end'))
        b.append(line(sx(lo), y, sx(hi), y, c, 3))
        for v in (lo, hi):
            b.append(line(sx(v), y - 7, sx(v), y + 7, c, 2.4))
        b.append(f'<circle cx="{sx(est):.1f}" cy="{y}" r="7" fill="{c}"/>')
        b.append(halo(sx(est), y - 13, f'{est:.3f}'.replace('-', '−'), 13, c, 700))
    b.append(text(575, 316, '회귀계수와 95% 신뢰구간', 13, MID, 600, 'middle'))
    write('ch05-coef-ci.svg', svg(W, H, '\n'.join(b)))


def fig_overlap5():
    W, H = 900, 336
    b = ['<defs><pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         f'<line x1="0" y1="0" x2="0" y2="7" stroke="{CORAL}" stroke-width="2.4"/></pattern></defs>']
    Y = (450, 215, 105)
    S = (425, 120, 92)
    L = (475, 120, 92)
    b.append(f'<circle cx="{Y[0]}" cy="{Y[1]}" r="{Y[2]}" fill="{NAVY_TINT}" fill-opacity=".5" stroke="{NAVY}" stroke-width="2"/>')
    # 고유한 가장자리: 한 원에서 다른 원을 뺀 부분을 빗금으로
    b.append(f'<clipPath id="notL"><path d="M0,0 H900 V320 H0 Z M{L[0] + L[2]},{L[1]} a{L[2]},{L[2]} 0 1,0 -{2 * L[2]},0 a{L[2]},{L[2]} 0 1,0 {2 * L[2]},0 Z" clip-rule="evenodd"/></clipPath>')
    b.append(f'<clipPath id="notS"><path d="M0,0 H900 V320 H0 Z M{S[0] + S[2]},{S[1]} a{S[2]},{S[2]} 0 1,0 -{2 * S[2]},0 a{S[2]},{S[2]} 0 1,0 {2 * S[2]},0 Z" clip-rule="evenodd"/></clipPath>')
    b.append(f'<circle cx="{S[0]}" cy="{S[1]}" r="{S[2]}" fill="url(#hatch)" clip-path="url(#notL)"/>')
    b.append(f'<circle cx="{L[0]}" cy="{L[1]}" r="{L[2]}" fill="url(#hatch)" clip-path="url(#notS)"/>')
    b.append(f'<circle cx="{S[0]}" cy="{S[1]}" r="{S[2]}" fill="{ACC}" fill-opacity=".10" stroke="{ACC}" stroke-width="2"/>')
    b.append(f'<circle cx="{L[0]}" cy="{L[1]}" r="{L[2]}" fill="{TEAL}" fill-opacity=".10" stroke="{TEAL}" stroke-width="2"/>')
    b.append(text(S[0] - 130, 70, '직무스트레스', 15, ACC, 700, 'end'))
    b.append(line(S[0] - 124, 66, S[0] - 70, 80, ACC, 1.4))
    b.append(text(L[0] + 130, 70, '업무과부하', 15, TEAL, 700, 'start'))
    b.append(line(L[0] + 124, 66, L[0] + 70, 80, TEAL, 1.4))
    b.append(text(450, 74, '겹치는 부분', 14, INK, 700, 'middle'))
    b.append(tex(450, 94, r'r = .89', 14, INK, 'middle', 90))
    b.append(text(450, 290, '소진', 15, NAVY, 700, 'middle'))
    b.append(f'<rect x="640" y="200" width="22" height="16" fill="url(#hatch)" stroke="{CORAL}" stroke-width="1"/>')
    b.append(text(672, 213, '고유한 부분', 13.5, CORAL, 700))
    b.append(text(672, 233, '계수는 여기서만 계산된다', 13, MID, 600))
    write('ch05-overlap.svg', svg(W, H, '\n'.join(b)))


def fig_vif_curve():
    W, H = 900, 380
    b, sx, sy = frame(90, 40, 720, 270, (0, 1), (0, 12), [0, .2, .4, .6, .8, 1.0], [0, 2, 4, 6, 8, 10, 12],
                      '두 독립변수의 상관 r', None, xfmt=lambda v: f'{v:.1f}')
    rs = [i / 200 for i in range(0, 193)]
    vif = [1 / (1 - r * r) for r in rs]
    b.append('<path d="M' + ' L'.join(f'{sx(r):.1f},{sy(min(v, 12)):.1f}' for r, v in zip(rs, vif)) +
             f'" fill="none" stroke="{ACC}" stroke-width="3"/>')
    b.append('<path d="M' + ' L'.join(f'{sx(r):.1f},{sy(math.sqrt(v)):.1f}' for r, v in zip(rs, vif)) +
             f'" fill="none" stroke="{CORAL}" stroke-width="3"/>')
    for v, lab in ((5, 'VIF 5'), (10, 'VIF 10')):
        b.append(line(90, sy(v), 810, sy(v), FAINT, 1.4, '5 4'))
        b.append(halo(96, sy(v) - 7, lab, 12.5, SOFT, 700, 'start'))
    r0 = .889
    v0 = 1 / (1 - r0 * r0)
    b.append(line(sx(r0), sy(0), sx(r0), sy(v0), MID, 1.4, '3 3'))
    b.append(f'<circle cx="{sx(r0):.1f}" cy="{sy(v0):.1f}" r="6" fill="{ACC}"/>')
    b.append(f'<circle cx="{sx(r0):.1f}" cy="{sy(math.sqrt(v0)):.1f}" r="6" fill="{CORAL}"/>')
    b.append(halo(sx(r0) - 10, sy(v0) + 5, f'VIF {v0:.1f}', 13.5, ACC_DEEP, 700, 'end'))
    b.append(halo(sx(r0) + 10, sy(1.25), f'표준오차 {math.sqrt(v0):.1f}배', 13.5, CORAL, 700, 'start'))
    b.append(halo(sx(r0) - 6, sy(0) - 8, '이 자료 .89', 12.5, MID, 700, 'end'))
    b.append(line(600, 74, 630, 74, ACC, 3))
    b.append(text(638, 79, 'VIF', 13.5, ACC_DEEP, 700))
    b.append(line(600, 98, 630, 98, CORAL, 3))
    b.append(rich(638, 103, [('t', '표준오차 배율 '), ('m', r'\sqrt{\text{VIF}}')], 13.5, CORAL, 'start', 700))
    write('ch05-vif-curve.svg', svg(W, H, '\n'.join(b)))


def fig_split():
    D = load('ch05.json')
    W, H = 900, 290
    b = []
    sx = _axis_rows(b, 300, 860, -0.4, 1.0, [-0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0], 30, 236)
    rows = [('업무과부하와 함께', '스트레스 계수', D['split_both']['A'][0], D['split_both']['B'][0], CORAL),
            ('', '업무과부하 계수', D['split_both']['A'][1], D['split_both']['B'][1], CORAL),
            ('업무과부하 뺌', '스트레스 계수', D['split_one']['A'], D['split_one']['B'], ACC)]
    for i, (grp, name, a, bb, c) in enumerate(rows):
        y = 64 + i * 62 + (12 if i == 2 else 0)
        if grp:
            b.append(text(20, y - 22, grp, 13, c, 800))
        b.append(text(280, y + 5, name, 14, INK, 700, 'end'))
        b.append(line(sx(a), y, sx(bb), y, c, 2, None, .5))
        for v, lab in ((a, 'A'), (bb, 'B')):
            b.append(f'<circle cx="{sx(v):.1f}" cy="{y}" r="11" fill="#fff" stroke="{c}" stroke-width="2.4"/>')
            b.append(text(sx(v), y + 5, lab, 13, c, 800, 'middle'))
            b.append(halo(sx(v), y - 17 if lab == 'A' else y + 28, f'{v:.3f}'.replace('-', '−'), 12.5, c, 700))
    b.append(text(580, 280, 'A, B = 무작위로 나눈 150명씩의 두 절반', 13, MID, 600, 'middle'))
    write('ch05-split.svg', svg(W, H, '\n'.join(b)))



# ================================================================ 6장
def _csv(name):
    import csv
    with open(os.path.join(figlib.ROOT, 'books', '02-regression', 'data', name), encoding='utf-8') as f:
        return list(csv.DictReader(f))


def fig_means6():
    rows = _csv('survey.csv')
    order = ['사원', '대리', '과장이상']
    m = {g: sum(float(r['satisfaction']) for r in rows if r['position'] == g) /
         sum(1 for r in rows if r['position'] == g) for g in order}
    W, H = 900, 360
    b, sx, sy = frame(120, 40, 600, 260, (0, 3), (2.9, 3.7), [], [3.0, 3.2, 3.4, 3.6], None, '직무만족 평균',
                      yfmt=lambda v: f'{v:.1f}')
    base = m['사원']
    xs = {g: sx(i + 0.5) for i, g in enumerate(order)}
    b.append(line(120, sy(base), 720, sy(base), ACC, 1.8, '7 5'))
    for i, g in enumerate(order):
        b.append(text(xs[g], 324, g, 15, INK, 700, 'middle'))
        if i:
            b.append(arrow(xs[g], sy(base), xs[g], sy(m[g]) + 10, CORAL, 2.6, 10))
            b.append(halo(xs[g] + 12, (sy(base) + sy(m[g])) / 2 + 5, f'+{m[g] - base:.3f}', 15, CORAL, 800, 'start'))
        b.append(f'<circle cx="{xs[g]:.1f}" cy="{sy(m[g]):.1f}" r="9" fill="{ACC}"/>')
        b.append(halo(xs[g], sy(m[g]) - 16, f'{m[g]:.3f}', 14, ACC_DEEP, 700))
    b.append(text(740, sy(base) + 5, '절편 = 사원 평균', 14, ACC_DEEP, 700))
    b.append(text(740, 120, '빨간 화살표', 13.5, CORAL, 700))
    b.append(text(740, 140, '= 더미의 계수', 13.5, CORAL, 700))
    b.append(text(740, 160, '(사원과의 차이)', 13, MID, 600))
    write('ch06-means.svg', svg(W, H, '\n'.join(b)))


def fig_ttest_line():
    rows = _csv('sample_data.csv')
    g = random.Random(3)
    W, H = 900, 380
    b, sx, sy = frame(170, 40, 520, 270, (-0.5, 1.5), (1, 5), [], [1, 2, 3, 4, 5], None, '자아존중감')
    pts = {0: [], 1: []}
    for r in rows:
        k = 0 if r['gender'] == '1' else 1
        pts[k].append(float(r['selfesteem']))
    for k in (0, 1):
        xs = [k + g.uniform(-0.18, 0.18) for _ in pts[k]]
        b.append(dots(xs, pts[k], sx, sy, [ACC, TEAL][k], 3.4, .3))
    m0 = sum(pts[0]) / len(pts[0]); m1 = sum(pts[1]) / len(pts[1])
    b.append(line(sx(-0.3), sy(m0 - 0.3 * (m1 - m0)), sx(1.3), sy(m1 + 0.3 * (m1 - m0)), INK, 3))
    for k, mm in ((0, m0), (1, m1)):
        b.append(f'<circle cx="{sx(k):.1f}" cy="{sy(mm):.1f}" r="9" fill="#fff" stroke="{INK}" stroke-width="3"/>')
    b.append(text(sx(0), 334, '남성 (0)', 15, ACC_DEEP, 700, 'middle'))
    b.append(text(sx(1), 334, '여성 (1)', 15, TEAL, 700, 'middle'))
    b.append(halo(sx(0) - 26, sy(m0) + 5, f'{m0:.3f}', 14, INK, 700, 'end'))
    b.append(halo(sx(1) + 26, sy(m1) + 5, f'{m1:.3f}', 14, INK, 700, 'start'))
    b.append(text(720, 140, '평균끼리 이은 선의 기울기', 14, INK, 700))
    b.append(rich(720, 166, [('m', f'= {m1:.3f} - {m0:.3f}')], 14, MID, 'start', 600))
    b.append(rich(720, 192, [('m', f'= {m1 - m0:.3f}')], 15, CORAL, 'start', 800))
    b.append(text(720, 222, '= 회귀계수 = 평균 차이', 14, CORAL, 700))
    write('ch06-ttest-line.svg', svg(W, H, '\n'.join(b)))



# ================================================================ 7장
def fig_blocks():
    W, H = 900, 300
    b, sx, sy = frame(110, 40, 520, 210, (0, 2), (0, .5), [], [0, .1, .2, .3, .4, .5], None, None,
                      yfmt=lambda v: f'{v:.1f}'.replace('0.', '.') if v else '0')
    r1, r2 = .0130, .4056
    bw = 120
    for i, (lab, top, parts) in enumerate([('모형 1', r1, [(0, r1, NAVY)]),
                                           ('모형 2', r2, [(0, r1, NAVY), (r1, r2, ACC)])]):
        cx = sx(i + 0.5)
        for lo, hi, c in parts:
            b.append(f'<rect x="{cx - bw / 2:.1f}" y="{sy(hi):.1f}" width="{bw}" height="{max(sy(lo) - sy(hi), 1.5):.1f}" fill="{c}"/>')
        b.append(text(cx, 274, lab, 15, INK, 700, 'middle'))
        b.append(rich(cx, sy(top) - 10, [('m', f'R^2 = .{round(top * 1000):03d}')], 14, INK, 'middle', 700))
    cx2 = sx(1.5)
    b.append(f'<path d="M{cx2 + bw / 2 + 12:.1f},{sy(r1):.1f} L{cx2 + bw / 2 + 20:.1f},{sy(r1):.1f} L{cx2 + bw / 2 + 20:.1f},{sy(r2):.1f} L{cx2 + bw / 2 + 12:.1f},{sy(r2):.1f}" fill="none" stroke="{ACC_DEEP}" stroke-width="2"/>')
    b.append(rich(cx2 + bw / 2 + 30, (sy(r1) + sy(r2)) / 2 - 6, [('m', r'\Delta R^2 = .393')], 16, ACC_DEEP, 'start', 800))
    b.append(text(cx2 + bw / 2 + 30, (sy(r1) + sy(r2)) / 2 + 18, '직무 변수가 더한 몫', 13.5, ACC_DEEP, 700))
    b.append(f'<rect x="700" y="196" width="16" height="16" fill="{NAVY}"/>')
    b.append(text(724, 209, '통제변수 (성별·연령·근속)', 13, MID, 600))
    b.append(f'<rect x="700" y="222" width="16" height="16" fill="{ACC}"/>')
    b.append(text(724, 235, '직무스트레스·지지·효능감', 13, MID, 600))
    write('ch07-blocks.svg', svg(W, H, '\n'.join(b)))


ALL = [fig_model_picture, fig_resid_fitted, fig_patterns, fig_curve, fig_qq, fig_influence, fig_cook,
       fig_coef_ci, fig_overlap5, fig_vif_curve, fig_split,
       fig_means6, fig_ttest_line, fig_blocks]
