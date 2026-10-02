"""2권 0~3장 그림"""
import random
from fig2lib import *


# ================================================================ 0장
def fig_research_model():
    W, H = 900, 310
    b = []
    X, bx = box(120, 262, 170, 60, '직무스트레스', sub='stress')
    M, bm = box(430, 112, 150, 60, '소진', sub='burnout')
    Y, by = box(660, 262, 150, 60, '이직의도', sub='turnover')
    Q, bq = box(830, 262, 110, 60, '실제 퇴사', sub='quit', fill='#fff', stroke=NAVY)
    Wm, bw = box(120, 72, 170, 60, '사회적지지', sub='support', fill=AMBER_TINT, stroke=AMBER)
    C, bc = box(735, 72, 300, 60, '통제변수', sub='성별 · 연령 · 근속연수 · 자기효능감', fill='#fff',
                stroke=RULE, color=MID, size=15, weight=700)

    a, p0, p1 = link(bx, bm, ACC, 2.6)
    bb, q0, q1 = link(bm, by, ACC, 2.6)
    cp, r0, r1 = link(bx, by, MID, 2.2)
    yq, _, _ = link(by, bq, NAVY, 2.2)
    b += [a, bb, cp, yq]
    # 조절: 지지 → (스트레스→소진 화살표의 중간)
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    b.append(to_point(bw, mx, my, AMBER, 2.2, dash='6 4'))
    b.append(f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="4" fill="{AMBER}"/>')
    b += [X, M, Y, Q, Wm, C]
    # 통제변수 → 소진 (옅은 점선)
    ctl, _, _ = link(bc, bm, FAINT, 1.8, dash='5 4')
    b.append(ctl)

    # 장 표시
    b.append(halo(322, 214, '1 · 2 · 3장', 13, ACC, 700))
    b.append(halo(578, 172, '9장 매개', 13, ACC, 700))
    b.append(halo(390, 290, '9장 직접효과', 13, MID, 700))
    b.append(halo(255, 120, '8장 조절 · 10장', 13, AMBER, 700))
    b.append(halo(752, 232, '11장', 13, NAVY, 700))
    b.append(halo(545, 74, '7장', 12, SOFT, 700))
    write('ch00-research-model.svg', svg(W, H, '\n'.join(b)))



# ================================================================ 1장
def _sb():
    return load('ch01-stress-burnout.json')


def fig_scatter():
    D = _sb()
    W, H = 900, 400
    b, sx, sy = frame(90, 40, 760, 290, (1, 5), (1, 5), [1, 2, 3, 4, 5], [1, 2, 3, 4, 5],
                      '직무스트레스', '소진')
    b.append(dots(D['x'], D['y'], sx, sy))
    b.append(rich(120, 70, [('m', 'r = .55'), ('t', '   n = 300')], 16, ACC_DEEP, 'start', 700))
    write('ch01-scatter.svg', svg(W, H, '\n'.join(b)))


def fig_quadrant():
    D = _sb()
    W, H = 900, 420
    b, sx, sy = frame(90, 40, 760, 300, (1, 5), (1, 5), [1, 2, 3, 4, 5], [1, 2, 3, 4, 5],
                      '직무스트레스', '소진')
    mx, my = D['mx'], D['my']
    b.append(f'<rect x="{sx(mx):.1f}" y="40" width="{850 - sx(mx):.1f}" height="{sy(my) - 40:.1f}" fill="{ACC_TINT}" fill-opacity=".6"/>')
    b.append(f'<rect x="90" y="{sy(my):.1f}" width="{sx(mx) - 90:.1f}" height="{340 - sy(my):.1f}" fill="{ACC_TINT}" fill-opacity=".6"/>')
    pos = [(x, y) for x, y in zip(D['x'], D['y']) if (x - mx) * (y - my) > 0]
    neg = [(x, y) for x, y in zip(D['x'], D['y']) if (x - mx) * (y - my) < 0]
    b.append(dots([p[0] for p in neg], [p[1] for p in neg], sx, sy, CORAL, 4.2, .55))
    b.append(dots([p[0] for p in pos], [p[1] for p in pos], sx, sy, ACC, 4.2, .5))
    b.append(dashed(sx(mx), 40, 340, MID, 1.6))
    b.append(f'<path d="M90,{sy(my):.1f} L850,{sy(my):.1f}" stroke="{MID}" stroke-width="1.6" stroke-dasharray="5 4"/>')
    b.append(halo(sx(mx), 32, f'스트레스 평균 {mx:.2f}', 12.5, MID, 600))
    b.append(halo(846, sy(my) - 8, f'소진 평균 {my:.2f}', 12.5, MID, 600, 'end'))
    npos, nneg = len(pos), len(neg)
    b.append(halo(830, 64, '(+) × (+) = +', 15, ACC_DEEP, 700, 'end'))
    b.append(halo(110, 326, '(−) × (−) = +', 15, ACC_DEEP, 700, 'start'))
    b.append(halo(110, 64, '(−) × (+) = −', 15, CORAL, 700, 'start'))
    b.append(halo(830, 326, '(+) × (−) = −', 15, CORAL, 700, 'end'))
    b.append(halo(300, 404, f'곱이 양수 {npos}명', 14, ACC_DEEP, 700))
    b.append(halo(600, 404, f'곱이 음수 {nneg}명', 14, CORAL, 700))
    # x축 이름과 겹치지 않도록 축 이름 대신 아래 줄에 인원을 적는다
    write('ch01-quadrant.svg', svg(W, H + 10, '\n'.join(b)))


def fig_r_gallery():
    W, H = 900, 250
    b = []
    rs = [-.8, -.4, 0, .4, .8]
    pw, gap = 152, 22
    x0 = (W - (5 * pw + 4 * gap)) / 2
    for i, r in enumerate(rs):
        px = x0 + i * (pw + gap)
        xs, ys = exact_r(r, 100, seed=11 + i)
        b.append(panel(px, 46, pw, pw, RULE, 1.4, PAPER))
        sx = lambda v, px=px: px + pw / 2 + v * pw / 7
        sy = lambda v: 46 + pw / 2 - v * pw / 7
        b.append(dots(xs, ys, sx, sy, ACC if r > 0 else (CORAL if r < 0 else SOFT), 3.0, .55))
        lab = 'r = 0' if r == 0 else f'r = {"-" if r < 0 else ""}.{abs(r) * 10:.0f}0'
        b.append(tex(px + pw / 2, 26, lab, 16, INK, 'middle', pw))
    b.append(text(W / 2, 232, '부호 = 기울어진 방향   ·   크기 = 직선 주위에 모인 정도', 14, MID, 600, 'middle'))
    write('ch01-r-gallery.svg', svg(W, H, '\n'.join(b)))


def fig_shared_variance():
    W, H = 900, 300
    r2 = .303
    R = 105
    # 겹친 면적이 원 하나의 r²가 되는 중심 거리
    def lens(d):
        return 2 * R * R * math.acos(d / (2 * R)) - d / 2 * math.sqrt(4 * R * R - d * d)
    lo, hi = 0.0, 2 * R
    for _ in range(60):
        mid = (lo + hi) / 2
        if lens(mid) / (math.pi * R * R) > r2:
            lo = mid
        else:
            hi = mid
    d = (lo + hi) / 2
    cx1, cx2, cy = 450 - d / 2, 450 + d / 2, 150
    b = []
    b.append(f'<circle cx="{cx1:.1f}" cy="{cy}" r="{R}" fill="{TEAL_TINT}" stroke="{TEAL}" stroke-width="2"/>')
    b.append(f'<circle cx="{cx2:.1f}" cy="{cy}" r="{R}" fill="{ACC_TINT}" fill-opacity=".75" stroke="{ACC}" stroke-width="2"/>')
    # 겹친 부분 강조
    b.append(f'<clipPath id="c1"><circle cx="{cx1:.1f}" cy="{cy}" r="{R}"/></clipPath>')
    b.append(f'<circle cx="{cx2:.1f}" cy="{cy}" r="{R}" fill="{ACC}" fill-opacity=".28" clip-path="url(#c1)"/>')
    b.append(text(cx1 - 52, cy - R - 14, '직무스트레스의 변동', 15, TEAL, 700, 'middle'))
    b.append(text(cx2 + 52, cy - R - 14, '소진의 변동', 15, ACC_DEEP, 700, 'middle'))
    b.append(tex(450, cy - 8, 'r^2 = .30', 17, ACC_DEEP, 'middle', 110))
    b.append(text(450, cy + 24, '함께 나눠', 13, ACC_DEEP, 600, 'middle'))
    b.append(text(450, cy + 41, '가진 몫', 13, ACC_DEEP, 600, 'middle'))
    b.append(text(cx2 + 46, cy - 6, '스트레스로', 13.5, MID, 600, 'middle'))
    b.append(text(cx2 + 46, cy + 12, '설명되지 않는', 13.5, MID, 600, 'middle'))
    b.append(text(cx2 + 46, cy + 30, '70%', 13.5, MID, 700, 'middle'))
    write('ch01-shared-variance.svg', svg(W, H, '\n'.join(b)))


def fig_anscombe():
    A = load('ch01-anscombe.json')
    W, H = 900, 300
    b = []
    titles = ['① 직선', '② 곡선', '③ 이상치가 기울기를 바꿈', '④ 이상치가 관계를 만듦']
    pw, gap = 190, 26
    x0 = (W - (4 * pw + 3 * gap)) / 2 + 10
    for i, P in enumerate(A):
        px = x0 + i * (pw + gap)
        fr, sx, sy = frame(px, 54, pw, 180, (2, 20), (2, 14), [5, 10, 15, 20], [4, 8, 12],
                           None, None, size=11.5)
        b += fr
        b.append(line(sx(3), sy(3 + .5 * 3), sx(19.5), sy(3 + .5 * 19.5), MID, 1.6, '5 4'))
        b.append(dots(P['x'], P['y'], sx, sy, ACC, 4.6, .8))
        b.append(text(px + pw / 2, 26, titles[i], 14, INK, 700, 'middle'))
        b.append(tex(px + pw / 2, 280, 'r = .816', 14, ACC_DEEP, 'middle', pw))
    write('ch01-anscombe.svg', svg(W, H, '\n'.join(b)))


def fig_range():
    D = _sb()
    W, H = 900, 430
    b, sx, sy = frame(90, 70, 760, 290, (1, 5), (1, 5), [1, 2, 3, 4, 5], [1, 2, 3, 4, 5],
                      '직무스트레스', '소진')
    lo = [(x, y) for x, y in zip(D['x'], D['y']) if x < 3.5]
    hi = [(x, y) for x, y in zip(D['x'], D['y']) if x >= 3.5]
    b.append(f'<rect x="{sx(3.5):.1f}" y="70" width="{850 - sx(3.5):.1f}" height="290" fill="{ACC_TINT}" fill-opacity=".7"/>')
    b.append(dots([p[0] for p in lo], [p[1] for p in lo], sx, sy, FAINT, 4.2, .45))
    b.append(dots([p[0] for p in hi], [p[1] for p in hi], sx, sy, ACC, 4.2, .6))
    b.append(dashed(sx(3.5), 30, 360, ACC, 1.8))
    r_hi = corr([p[0] for p in hi], [p[1] for p in hi])
    b.append(rich(sx(3.5) - 16, 40, [('t', '전체 300명  '), ('m', f'r = .{round(D["r"] * 100):02d}')], 15, MID, 'end', 700))
    b.append(rich(sx(3.5) + 16, 40, [('t', '3.5점 이상 91명  '), ('m', f'r = .{round(r_hi * 100):02d}')], 15, ACC_DEEP, 'start', 700))
    write('ch01-range.svg', svg(W, H, '\n'.join(b)))


def fig_third():
    D = load('ch01-third.json')
    W, H = 900, 420
    b, sx, sy = frame(90, 40, 600, 300, (0, 20), (1, 5), [0, 5, 10, 15, 20], [1, 2, 3, 4, 5],
                      '근속연수(년)', '직무만족')
    cols = {'사원': TEAL, '대리': AMBER, '과장이상': ACC}
    jit = random.Random(9)            # 겹친 점을 살짝 흩는다 (빌드마다 같은 그림)
    for x, y, g in zip(D['x'], D['y'], D['g']):
        b.append(f'<circle cx="{sx(x) + jit.uniform(-2.7, 2.7):.1f}" cy="{sy(y):.1f}" r="4" '
                 f'fill="{cols[g]}" fill-opacity=".45"/>')
    a0, a1 = ols(D['x'], D['y'])
    b.append(line(sx(0), sy(a0), sx(19), sy(a0 + a1 * 19), SOFT, 2.4, '7 5'))
    for g in cols:
        xs = [x for x, gg in zip(D['x'], D['g']) if gg == g]
        ys = [y for y, gg in zip(D['y'], D['g']) if gg == g]
        c0, c1 = ols(xs, ys)
        b.append(line(sx(min(xs)), sy(c0 + c1 * min(xs)), sx(max(xs)), sy(c0 + c1 * max(xs)), cols[g], 3.2))
    # 범례
    lx = 720
    b.append(line(lx, 70, lx + 34, 70, SOFT, 2.4, '7 5'))
    b.append(rich(lx + 42, 75, [('t', '전체  '), ('m', f'r = .{round(D["r"] * 100):02d}')], 14, MID, 'start', 600))
    for i, g in enumerate(cols):
        y = 110 + i * 34
        b.append(line(lx, y, lx + 34, y, cols[g], 3.2))
        w = D['within'][i]
        lab = f'r = {"-" if w < 0 else ""}.{abs(round(w * 100)):02d}'
        b.append(rich(lx + 42, y + 5, [('t', f'{g}  '), ('m', lab)], 14, cols[g], 'start', 700))
    b.append(text(lx, 236, '직급 안에서는', 13.5, MID, 600))
    b.append(text(lx, 256, '관계가 없다', 13.5, MID, 600))
    write('ch01-third.svg', svg(W, H, '\n'.join(b)))



# ================================================================ 2장
def _fit():
    return load('ch02-fit.json')


def fig_line():
    D = _fit()
    W, H = 900, 410
    b, sx, sy = frame(90, 40, 760, 300, (1, 5), (1, 5), [1, 2, 3, 4, 5], [1, 2, 3, 4, 5],
                      '직무스트레스', '소진')
    b.append(dots(D['x'], D['y'], sx, sy, ACC, 4, .28))
    b0, b1 = D['b0'], D['b1']
    b.append(line(sx(1.2), sy(b0 + b1 * 1.2), sx(4.8), sy(b0 + b1 * 4.8), ACC_DEEP, 3))
    # 기울기 삼각형: 3 → 4
    y3, y4 = b0 + b1 * 3, b0 + b1 * 4
    b.append(line(sx(3), sy(y3), sx(4), sy(y3), CORAL, 2.4))
    b.append(line(sx(4), sy(y3), sx(4), sy(y4), CORAL, 2.4))
    b.append(halo(sx(3.5), sy(y3) + 22, '1점', 14, CORAL, 700))
    b.append(halo(sx(4) + 10, (sy(y3) + sy(y4)) / 2 + 5, '0.60점', 14, CORAL, 700, 'start'))
    # 두 평균의 교점
    mx, my = sum(D['x']) / len(D['x']), sum(D['y']) / len(D['y'])
    b.append(f'<circle cx="{sx(mx):.1f}" cy="{sy(my):.1f}" r="7" fill="#fff" stroke="{NAVY}" stroke-width="2.4"/>')
    b.append(halo(sx(mx) - 16, sy(my) - 16, '두 평균이 만나는 점', 13, NAVY, 700, 'end'))
    b.append(tex(120, 72, r'\hat{Y} = 1.006 + 0.602\,X', 18, ACC_DEEP, 'start', 320))
    write('ch02-line.svg', svg(W, H, '\n'.join(b)))


def fig_residual():
    D = _fit()
    W, H = 900, 400
    b, sx, sy = frame(90, 40, 760, 290, (2.6, 4.0), (1.6, 4.2), [2.75, 3.0, 3.25, 3.5, 3.75, 4.0],
                      [2, 2.5, 3, 3.5, 4], '직무스트레스', '소진', xfmt=lambda v: f'{v:.2f}')
    b0, b1 = D['b0'], D['b1']
    pts = [(x, y) for x, y in zip(D['x'], D['y']) if 2.65 <= x <= 3.95 and 1.65 <= y <= 4.15]
    pick = pts[::7][:24]
    hl = [(3.50, 2.44), (3.17, 3.22)]
    for x, y in pick + hl:
        yh = b0 + b1 * x
        c = ACC if y > yh else CORAL
        b.append(line(sx(x), sy(y), sx(x), sy(yh), c, 1.6, None, .7))
    b.append(line(sx(2.62), sy(b0 + b1 * 2.62), sx(3.98), sy(b0 + b1 * 3.98), ACC_DEEP, 3))
    b.append(dots([p[0] for p in pick], [p[1] for p in pick], sx, sy, MID, 4.4, .55))
    for (x, y), lab, c in zip(hl, ['잔차 −0.67', '잔차 +0.31'], [CORAL, ACC]):
        b.append(f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="6.5" fill="{c}"/>')
        b.append(halo(sx(x) + 12, sy(y) + 5, lab, 14, c, 700, 'start'))
    b.append(halo(sx(3.95), sy(b0 + b1 * 3.95) - 14, '회귀선', 13.5, ACC_DEEP, 700, 'end'))
    b.append(text(850, 392, '일부 사례만 표시', 12, FAINT, None, 'end'))
    write('ch02-residual.svg', svg(W, H, '\n'.join(b)))


def fig_least_squares():
    W, H = 900, 360
    X = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
    Y = [2.4, 2.1, 4.0, 3.6, 5.6, 4.9, 6.6]
    a0, a1 = ols(X, Y)
    my = sum(Y) / len(Y)
    lines = [(a0, a1, '최소제곱선', ACC), (my - 0.25 * 4, 0.25, '다른 직선', CORAL)]
    b = []
    for k, (c0, c1, name, col) in enumerate(lines):
        px = 40 + k * 440
        fr, sx, sy = frame(px + 30, 60, 360, 240, (0, 8), (0, 8), [], [], None, None, grid=False)
        b += fr
        unit = 30                                        # 1단위 = 30px (가로세로 같게)
        sse = 0
        for x, y in zip(X, Y):
            yh = c0 + c1 * x
            e = y - yh
            sse += e * e
            side = abs(e) * unit
            top = sy(max(y, yh))
            left = sx(x) - side if x > 4 else sx(x)
            b.append(f'<rect x="{left:.1f}" y="{top:.1f}" width="{side:.1f}" height="{side:.1f}" '
                     f'fill="{col}" fill-opacity=".16" stroke="{col}" stroke-width="1.2"/>')
        b.append(line(sx(0.3), sy(c0 + c1 * 0.3), sx(7.7), sy(c0 + c1 * 7.7), col, 2.8))
        b.append(dots(X, Y, sx, sy, INK, 5, .9))
        b.append(text(px + 210, 36, name, 16, col, 800, 'middle'))
        b.append(rich(px + 210, 334, [('t', '잔차제곱합 '), ('m', f'= {sse:.2f}')], 15, col, 'middle', 700))
    write('ch02-least-squares.svg', svg(W, H, '\n'.join(b)))


def fig_ss_partition():
    W, H = 900, 380
    b, sx, sy = frame(90, 40, 600, 290, (0, 10), (0, 10), [], [], 'X', 'Y', grid=False)
    c0, c1 = 1.5, 0.7
    ybar = c0 + c1 * 5
    b.append(line(sx(0.3), sy(c0 + c1 * 0.3), sx(8.55), sy(c0 + c1 * 8.55), ACC_DEEP, 3))
    b.append(f'<path d="M{sx(0):.1f},{sy(ybar):.1f} L{sx(10):.1f},{sy(ybar):.1f}" stroke="{MID}" stroke-width="1.6" stroke-dasharray="6 5"/>')
    px_, py_ = 8.2, 9.3
    yh = c0 + c1 * px_
    X0 = sx(px_)
    b.append(f'<circle cx="{X0:.1f}" cy="{sy(py_):.1f}" r="7" fill="{INK}"/>')
    # 오른쪽 괄호 두 개 + 왼쪽 전체 괄호
    def brace(x, y0, y1, col, w=2.6):
        return (f'<path d="M{x - 8:.1f},{y0:.1f} L{x:.1f},{y0:.1f} L{x:.1f},{y1:.1f} L{x - 8:.1f},{y1:.1f}" '
                f'fill="none" stroke="{col}" stroke-width="{w}"/>')
    b.append(line(X0, sy(py_), X0, sy(ybar), FAINT, 1.4, '3 3'))
    b.append(brace(X0 + 26, sy(py_), sy(yh), CORAL))
    b.append(brace(X0 + 26, sy(yh), sy(ybar), ACC))
    b.append(f'<path d="M{X0 - 26 + 8:.1f},{sy(py_):.1f} L{X0 - 26:.1f},{sy(py_):.1f} L{X0 - 26:.1f},{sy(ybar):.1f} L{X0 - 26 + 8:.1f},{sy(ybar):.1f}" fill="none" stroke="{NAVY}" stroke-width="2.6"/>')
    b.append(rich(X0 + 40, (sy(py_) + sy(yh)) / 2 + 5, [('m', r'Y_i - \hat{Y}_i'), ('t', '  잔차')], 15, CORAL, 'start', 700))
    b.append(rich(X0 + 40, (sy(yh) + sy(ybar)) / 2 + 5, [('m', r'\hat{Y}_i - \bar{Y}'), ('t', '  회귀가 설명')], 15, ACC_DEEP, 'start', 700))
    b.append(rich(X0 - 36, sy(py_) + 18, [('t', '총 편차  '), ('m', r'Y_i - \bar{Y}')], 15, NAVY, 'end', 700))
    b.append(rich(sx(0.4), sy(ybar) + 22, [('t', '평균  '), ('m', r'\bar{Y}')], 14, MID, 'start', 600))
    b.append(halo(sx(2.2), sy(c0 + c1 * 2.2) - 14, '회귀선', 14, ACC_DEEP, 700))
    write('ch02-ss-partition.svg', svg(W, H, '\n'.join(b)))


def fig_ss_bars():
    W, H = 900, 250
    SST, SSR, SSE = 136.41, 41.34, 95.07
    x0, wmax = 150, 700
    k = wmax / SST
    b = []
    b.append(text(x0 - 14, 66, '전체', 15, NAVY, 700, 'end'))
    b.append(f'<rect x="{x0}" y="44" width="{wmax}" height="34" rx="4" fill="{NAVY_TINT}"/>')
    b.append(rich(x0 + wmax / 2, 67, [('m', 'SS_T'), ('t', ' = 136.41')], 15, NAVY, 'middle', 700))
    b.append(text(x0 - 14, 136, '쪼개면', 15, MID, 700, 'end'))
    b.append(f'<rect x="{x0}" y="114" width="{SSR * k:.1f}" height="34" rx="4" fill="{ACC}"/>')
    b.append(f'<rect x="{x0 + SSR * k + 3:.1f}" y="114" width="{SSE * k - 3:.1f}" height="34" rx="4" fill="{RULE}"/>')
    b.append(rich(x0 + SSR * k / 2, 137, [('m', 'SS_R'), ('t', ' = 41.34')], 15, '#fff', 'middle', 700))
    b.append(rich(x0 + SSR * k + SSE * k / 2, 137, [('m', 'SS_E'), ('t', ' = 95.07')], 15, MID, 'middle', 700))
    b.append(text(x0 + SSR * k / 2, 172, '스트레스로 설명', 13.5, ACC_DEEP, 700, 'middle'))
    b.append(text(x0 + SSR * k + SSE * k / 2, 172, '설명되지 않음', 13.5, SOFT, 700, 'middle'))
    b.append(tex(450, 218, r'R^2 = \frac{SS_R}{SS_T} = \frac{41.34}{136.41} = .303', 17, ACC_DEEP, 'middle', 420, 56))
    write('ch02-ss-bars.svg', svg(W, H, '\n'.join(b)))


def fig_intervals():
    D = _fit()
    W, H = 900, 410
    b, sx, sy = frame(90, 40, 760, 300, (1, 5), (1, 5), [1, 2, 3, 4, 5], [1, 2, 3, 4, 5],
                      '직무스트레스', '소진')
    g = D['grid']
    def band(lo, hi, fill, op):
        top = ' L'.join(f'{sx(x):.1f},{sy(v):.1f}' for x, v in zip(g, hi))
        bot = ' L'.join(f'{sx(x):.1f},{sy(v):.1f}' for x, v in zip(reversed(g), list(reversed(lo))))
        return f'<path d="M{top} L{bot} Z" fill="{fill}" fill-opacity="{op}"/>'
    b.append('<clipPath id="plot2"><rect x="90" y="40" width="760" height="300"/></clipPath>')
    b.append(f'<g clip-path="url(#plot2)">{band(D["pi_lo"], D["pi_hi"], ACC, .10)}</g>')
    b.append(dots(D['x'], D['y'], sx, sy, MID, 3.4, .22))
    b.append(band(D['ci_lo'], D['ci_hi'], ACC, .45))
    b0, b1 = D['b0'], D['b1']
    b.append(line(sx(g[0]), sy(b0 + b1 * g[0]), sx(g[-1]), sy(b0 + b1 * g[-1]), ACC_DEEP, 2.4))
    # 스트레스 4점에서 두 구간: 구간은 x=4에, 이름표는 자료가 없는 오른쪽 끝에
    i4 = min(range(len(g)), key=lambda i: abs(g[i] - 4))
    X4 = sx(4)
    pl, ph, cl, ch = D['pi_lo'][i4], D['pi_hi'][i4], D['ci_lo'][i4], D['ci_hi'][i4]
    b.append(line(X4, sy(pl), X4, sy(ph), ACC, 2.6))
    for yv in (pl, ph):
        b.append(line(X4 - 7, sy(yv), X4 + 7, sy(yv), ACC, 2.6))
    b.append(line(X4, sy(cl), X4, sy(ch), ACC_DEEP, 6))
    LX = sx(4.62)
    b.append(line(X4 + 9, sy(ph), LX - 6, sy(ph), ACC, 1, '3 3'))
    b.append(line(X4 + 6, sy((cl + ch) / 2), LX - 6, sy((cl + ch) / 2), ACC_DEEP, 1, '3 3'))
    b.append(text(LX, sy(ph) - 4, '예측구간', 13.5, ACC, 700))
    b.append(text(LX, sy(ph) + 14, f'[{pl:.2f}, {ph:.2f}]', 13, ACC, 600))
    b.append(text(LX, sy((cl + ch) / 2) - 4, '신뢰구간', 13.5, ACC_DEEP, 700))
    b.append(text(LX, sy((cl + ch) / 2) + 14, f'[{cl:.2f}, {ch:.2f}]', 13, ACC_DEEP, 600))
    write('ch02-intervals.svg', svg(W, H, '\n'.join(b)))



# ================================================================ 3장
def fig_simple_vs_multiple():
    W, H = 900, 300
    rows = [('직무스트레스', 0.602, 0.526), ('사회적지지', -0.406, -0.222), ('자기효능감', -0.382, -0.227)]
    x0, x1 = 230, 860
    sx = lambda v: x0 + (v + 0.6) / 1.4 * (x1 - x0)
    b = []
    for t in [-0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8]:
        b.append(f'<path d="M{sx(t):.1f},50 L{sx(t):.1f},236" stroke="{RULE if t else FAINT}" stroke-width="{1 if t else 1.6}"/>')
        b.append(text(sx(t), 258, f'{t:g}', 12.5, SOFT, None, 'middle'))
    for i, (name, s1, m1) in enumerate(rows):
        y = 84 + i * 66
        b.append(text(x0 - 20, y + 5, name, 15, INK, 700, 'end'))
        b.append(arrow(sx(s1), y, sx(m1) + (8 if s1 < 0 else -8) * 0, y, ACC, 2.4, 10))
        b.append(f'<circle cx="{sx(s1):.1f}" cy="{y}" r="7" fill="#fff" stroke="{SOFT}" stroke-width="2.4"/>')
        b.append(f'<circle cx="{sx(m1):.1f}" cy="{y}" r="7" fill="{ACC}"/>')
        b.append(halo(sx(s1), y - 14, f'{s1:.3f}'.replace('-', '−'), 13, SOFT, 700))
        b.append(halo(sx(m1), y + 25, f'{m1:.3f}'.replace('-', '−'), 13, ACC_DEEP, 700))
    b.append(f'<circle cx="300" cy="284" r="6" fill="#fff" stroke="{SOFT}" stroke-width="2.2"/>')
    b.append(text(312, 289, '단순회귀 (혼자 넣었을 때)', 13.5, MID, 600))
    b.append(f'<circle cx="560" cy="284" r="6" fill="{ACC}"/>')
    b.append(text(572, 289, '다중회귀 (함께 넣었을 때)', 13.5, ACC_DEEP, 700))
    write('ch03-simple-vs-multiple.svg', svg(W, H + 8, '\n'.join(b)))


def fig_control():
    W, H = 900, 270
    b = []
    B1, b1 = box(120, 90, 190, 64, '직무스트레스', sub='원래 점수', fill='#fff', stroke=ACC)
    B2, b2 = box(120, 210, 190, 64, '지지 · 효능감으로', sub='예측되는 부분', fill=RULE, stroke=FAINT, color=MID)
    B3, b3 = box(450, 90, 210, 64, '남은 스트레스', sub='지지 · 효능감과 무관한 부분', fill=ACC_TINT, stroke=ACC)
    B4, b4 = box(770, 90, 170, 64, '소진', fill='#fff', stroke=NAVY)
    b += [B1, B2, B3, B4]
    a, _, _ = link(b1, b3, ACC, 2.4)
    b.append(a)
    b.append(halo(282, 76, '① 걷어 낸다', 14, ACC_DEEP, 700))
    b.append(arrow(120, 124, 120, 172, FAINT, 2, dash='5 4'))
    b.append(text(134, 156, '빼기', 13, SOFT, 700))
    a2, _, _ = link(b3, b4, NAVY, 2.4)
    b.append(a2)
    b.append(halo(620, 76, '② 회귀한다', 14, NAVY, 700))
    b.append(rich(620, 128, [('t', '기울기 '), ('m', '= 0.526')], 15, NAVY, 'middle', 700))
    b.append(text(450, 196, '이 기울기가 다중회귀의 스트레스 계수와 같다', 15, INK, 700, 'middle'))
    b.append(text(450, 222, '= "지지와 효능감이 같은 사람끼리 비교한 기울기"', 14, MID, 600, 'middle'))
    write('ch03-control.svg', svg(W, H, '\n'.join(b)))


def fig_overlap():
    W, H = 900, 380
    b = []
    Y, X1, X2 = (450, 225, 112), (380, 140, 100), (520, 140, 100)
    b.append(f'<circle cx="{Y[0]}" cy="{Y[1]}" r="{Y[2]}" fill="{NAVY_TINT}" fill-opacity=".55" stroke="{NAVY}" stroke-width="2"/>')
    b.append(f'<circle cx="{X1[0]}" cy="{X1[1]}" r="{X1[2]}" fill="{ACC}" fill-opacity=".12" stroke="{ACC}" stroke-width="2"/>')
    b.append(f'<circle cx="{X2[0]}" cy="{X2[1]}" r="{X2[2]}" fill="{TEAL}" fill-opacity=".12" stroke="{TEAL}" stroke-width="2"/>')
    b.append(text(X1[0] - 60, 30, '독립변수 1', 15, ACC, 700, 'middle'))
    b.append(text(X2[0] + 60, 30, '독립변수 2', 15, TEAL, 700, 'middle'))
    b.append(text(450, 366, '종속변수 (소진)', 15, NAVY, 700, 'middle'))
    for lab, x, y, c in [('a', 362, 215, ACC_DEEP), ('b', 538, 215, TEAL), ('c', 450, 178, INK)]:
        b.append(f'<circle cx="{x}" cy="{y}" r="15" fill="#fff" stroke="{c}" stroke-width="2"/>')
        b.append(text(x, y + 6, lab, 17, c, 800, 'middle'))
    b.append(text(450, 296, '설명되지 않는 몫', 13.5, SOFT, 600, 'middle'))
    lx = 690
    for i, (k, s_) in enumerate([('a', '변수 1만의 몫'), ('b', '변수 2만의 몫'), ('c', '둘이 함께 나눠 가진 몫')]):
        b.append(text(lx, 206 + i * 26, f'{k}  {s_}', 13.5, MID, 600))
    b.append(text(40, 206, '단순회귀 1:  a + c', 13.5, ACC_DEEP, 700))
    b.append(text(40, 232, '단순회귀 2:  b + c', 13.5, TEAL, 700))
    b.append(text(40, 258, '다중회귀:  a + b + c', 13.5, INK, 700))
    write('ch03-overlap.svg', svg(W, H, '\n'.join(b)))


def fig_r2_parts():
    W, H = 900, 230
    parts = [('스트레스 고유', 21.97, ACC), ('지지 고유', 3.36, TEAL), ('효능감 고유', 3.15, AMBER),
             ('공유', 10.98, NAVY), ('설명되지 않음', 60.54, RULE)]
    x0, wmax = 60, 780
    b = []
    x = x0
    for i, (name, v, c) in enumerate(parts):
        w = wmax * v / 100
        b.append(f'<rect x="{x:.1f}" y="70" width="{w - 2:.1f}" height="44" fill="{c}" fill-opacity="{.9 if c != RULE else 1}"/>')
        cx = x + w / 2
        if v > 8:
            b.append(text(cx, 98, f'{v:.1f}%', 15, '#fff' if c != RULE else MID, 700, 'middle'))
            b.append(text(cx, 140, name, 13.5, c if c != RULE else SOFT, 700, 'middle'))
        x += w
    # 작은 두 조각은 아래로 끌어내 이름을 단다
    xs = x0 + wmax * 21.97 / 100
    for name, v, c, dy in [('지지 고유 3.4%', 3.36, TEAL, 170), ('효능감 고유 3.1%', 3.15, AMBER, 196)]:
        cx = xs + wmax * v / 200
        b.append(line(cx, 116, cx, dy - 14, c, 1.4))
        b.append(text(cx + 4, dy, name, 13, c, 700))
        xs += wmax * v / 100
    b.append(f'<path d="M{x0},52 L{x0},44 L{x0 + wmax * 39.46 / 100:.1f},44 L{x0 + wmax * 39.46 / 100:.1f},52" fill="none" stroke="{ACC_DEEP}" stroke-width="1.8"/>')
    b.append(rich(x0 + wmax * 39.46 / 200, 34, [('m', 'R^2'), ('t', ' = 39.5%  세 변수가 함께 설명')], 14, ACC_DEEP, 'middle', 700))
    write('ch03-r2-parts.svg', svg(W, H, '\n'.join(b)))


def fig_beta():
    W, H = 900, 260
    rows = [('직무스트레스', .48, .39, .57), ('사회적지지', -.20, -.29, -.10), ('자기효능감', -.19, -.28, -.09)]
    x0, x1 = 230, 840
    sx = lambda v: x0 + (v + .4) / 1.0 * (x1 - x0)
    b = []
    for t in [-.4, -.2, 0, .2, .4, .6]:
        b.append(f'<path d="M{sx(t):.1f},40 L{sx(t):.1f},206" stroke="{RULE if t else FAINT}" stroke-width="{1 if t else 1.6}"/>')
        b.append(text(sx(t), 228, f'{t:.1f}'.replace('-', '−').replace('0.', '.') if t else '0', 12.5, SOFT, None, 'middle'))
    for i, (name, bt, lo, hi) in enumerate(rows):
        y = 74 + i * 56
        c = ACC if bt > 0 else CORAL
        b.append(text(x0 - 20, y + 5, name, 15, INK, 700, 'end'))
        b.append(line(sx(lo), y, sx(hi), y, c, 3))
        for v in (lo, hi):
            b.append(line(sx(v), y - 7, sx(v), y + 7, c, 2.4))
        b.append(f'<circle cx="{sx(bt):.1f}" cy="{y}" r="7.5" fill="{c}"/>')
        lab = f'{bt:.2f}'.replace('0.', '.').replace('-', '−')
        b.append(halo(sx(hi) + 14, y + 5, lab, 14, c, 700, 'start'))
    b.append(tex(sx(0), 250, r'\beta', 15, MID, 'middle', 60))
    write('ch03-beta.svg', svg(W, H + 10, '\n'.join(b)))


ALL = [fig_research_model, fig_scatter, fig_quadrant, fig_r_gallery, fig_shared_variance,
       fig_anscombe, fig_range, fig_third,
       fig_line, fig_residual, fig_least_squares, fig_ss_partition, fig_ss_bars, fig_intervals,
       fig_simple_vs_multiple, fig_control, fig_overlap, fig_r2_parts, fig_beta]
