"""2장 — 대표값과 흩어진 정도"""
import math
from figlib import *


def fig_three_centers():
    """평균·중앙값·최빈값이 서로 다른 곳을 가리킬 때"""
    W, H = 900, 300
    base, top = 214, 60
    px0, px1 = 70, 830
    b = [axis(px0, px1, base)]

    # 오른쪽으로 치우친 분포 (감마꼴)
    pts, ys = [], []
    n = 120
    for i in range(n + 1):
        x = 0.02 + (i / n) * 6
        y = (x ** 1.6) * math.exp(-x / 0.85)
        pts.append((x, y)); ys.append(y)
    peak = max(ys)
    sx = scale(0, 6.02, px0, px1)
    line, area = curve_paths(pts, sx, base, top, peak)
    b.append(f'<path d="{area}" fill="{TEAL_TINT}" opacity=".75"/>')
    b.append(f'<path d="{line}" fill="none" stroke="{TEAL}" stroke-width="2.6"/>')

    tot = sum(ys)
    mode_i = ys.index(peak)
    cum = 0; med_i = 0
    for i, y in enumerate(ys):
        cum += y
        if cum >= tot / 2: med_i = i; break
    mean_i = int(sum(i * y for i, y in enumerate(ys)) / tot)

    marks = [(mode_i, '최빈값', NAVY, -26), (med_i, '중앙값', TEAL, -4), (mean_i, '평균', CORAL, 18)]
    for idx, lab, color, dy in marks:
        x = sx(pts[idx][0])
        b.append(dashed(x, base, top - 6, color))
        b.append(text(x, top - 14 + dy, lab, 15, color, 700, 'middle'))

    b.append(caption(450, base + 34, '봉우리 · 한가운데 · 무게중심 — 셋이 다른 값을 가리킨다', 15))
    b.append(caption(450, base + 62,
                     '치우친 분포에서 "평균이 얼마인가"만 물으면 자료의 생김새를 놓친다', 14, SOFT))
    write('ch02-three-centers.svg', svg(W, H, '\n'.join(b)))


def fig_deviation():
    """편차 — 평균에서 각 값까지의 거리, 합하면 0"""
    W, H = 900, 320
    b = []
    data = [7, 3, 5, 4, 2, 3]
    mean = 4
    px0, px1 = 90, 830
    base = 200
    sy = lambda v: base - (v - 1) * 26   # 값 1~7을 세로로

    b.append(f'<path d="M{px0-20},{sy(mean):.0f} L{px1},{sy(mean):.0f}" stroke="{CORAL}" stroke-width="2.5"/>')
    b.append(text(px0 - 26, sy(mean) + 5, 'M = 4', 15, CORAL, 700, 'end'))

    step = (px1 - px0 - 60) / (len(data) - 1)
    for i, v in enumerate(data):
        x = px0 + 30 + i * step
        d = v - mean
        color = TEAL if d > 0 else (NAVY if d < 0 else FAINT)
        if d != 0:
            b.append(f'<path d="M{x:.0f},{sy(mean):.0f} L{x:.0f},{sy(v):.0f}" stroke="{color}" stroke-width="3"/>')
        b.append(f'<circle cx="{x:.0f}" cy="{sy(v):.0f}" r="7" fill="{color}"/>')
        b.append(text(x, sy(v) - 14 if d >= 0 else sy(v) + 22, str(v), 14, INK, 700, 'middle'))
        b.append(text(x, base + 34, f'{d:+d}' if d else '0', 15, color, 700, 'middle'))

    b.append(text(px0 - 26, base + 34, '편차', 14, SOFT, 700, 'end'))
    b.append(f'<path d="M{px0+10},{base+50} L{px1},{base+50}" stroke="{RULE}" stroke-width="1.5"/>')
    b.append(caption(450, base + 78, '편차를 모두 더하면  (+3) + (−1) + (+1) + 0 + (−2) + (−1) = 0', 16, INK))
    b.append(caption(450, base + 104,
                     '평균은 편차의 합이 0이 되는 지점이다. 그래서 편차를 그냥 더해서는 흩어진 정도를 잴 수 없다', 14, SOFT))
    write('ch02-deviation.svg', svg(W, H, '\n'.join(b)))


def fig_why_square():
    """왜 제곱하는가 — 절댓값과 제곱의 차이"""
    W, H = 900, 290
    b = []
    for x0, title, note, color in (
        (0, '절댓값을 씌우면', '큰 편차와 작은 편차를 같은 비중으로 센다', FAINT),
        (470, '제곱을 하면', '큰 편차에 더 큰 벌점을 준다', TEAL),
    ):
        b.append(panel(x0, 0, 430, H - 44, stroke=(TEAL if color == TEAL else RULE),
                       sw=3 if color == TEAL else 2))
        b.append(text(x0 + 26, 34, title, 18, NAVY, 800))
        bx0, bx1, base = x0 + 40, x0 + 400, 190
        b.append(axis(bx0, bx1, base))
        devs = [1, 2, 3, 4]
        step = (bx1 - bx0 - 40) / len(devs)
        for i, d in enumerate(devs):
            v = d if color == FAINT else d * d
            hmax = 4 if color == FAINT else 16
            h = (v / hmax) * 112
            x = bx0 + 26 + i * step
            b.append(f'<rect x="{x:.0f}" y="{base-h:.0f}" width="{step*0.52:.0f}" height="{h:.0f}" rx="3" fill="{color}" opacity=".85"/>')
            b.append(text(x + step * 0.26, base - h - 8, str(v), 13, INK, 700, 'middle'))
            b.append(text(x + step * 0.26, base + 22, f'편차 {d}', 12, SOFT, None, 'middle'))
        b.append(text(x0 + 215, base + 54, note, 14, SOFT, None, 'middle'))

    b.append(caption(450, H - 12,
                     '제곱을 쓰면 평균에서 멀리 떨어진 값이 흩어짐에 더 크게 반영된다. 대신 단위가 제곱이 되어 표준편차로 되돌린다', 14))
    write('ch02-why-square.svg', svg(W, H, '\n'.join(b)))


def fig_ss_flow():
    """SS -> 분산 -> 표준편차 흐름"""
    W, H = 900, 250
    b = []
    boxes = [
        (20, '편차', 'X − M', '평균에서 얼마나 떨어졌나', FAINT),
        (245, '제곱합 SS', 'Σ(X − M)²', '떨어진 정도를 모두 합침', NAVY),
        (470, '분산 s²', 'SS / (n−1)', '하나당 평균 얼마나 떨어졌나', TEAL),
        (695, '표준편차 s', '√s²', '원래 단위로 되돌림', CORAL),
    ]
    for x, title, formula, note, color in boxes:
        b.append(f'<rect x="{x}" y="40" width="185" height="120" rx="10" fill="{PAPER}" stroke="{color}" stroke-width="2.5"/>')
        b.append(text(x + 92, 72, title, 17, color, 800, 'middle'))
        b.append(text(x + 92, 104, formula, 17, INK, 700, 'middle', ' font-style="italic"'))
        b.append(text(x + 92, 136, note, 12.5, SOFT, None, 'middle'))
        if x < 695:
            b.append(f'<path d="M{x+195},100 L{x+235},100" stroke="{MID}" stroke-width="2.5"/>')
            b.append(f'<path d="M{x+227},93 L{x+235},100 L{x+227},107" stroke="{MID}" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')

    b.append(caption(450, 200, '자료 7, 3, 5, 4, 2, 3 을 넣으면   SS = 16  →  s² = 16 / 5 = 3.2  →  s = 1.79', 16, INK))
    b.append(caption(450, 228, '표준편차는 "평균에서 평균적으로 이만큼 떨어져 있다"는 뜻이다', 14))
    write('ch02-ss-flow.svg', svg(W, H, '\n'.join(b)))


def fig_n_minus_1():
    """왜 n이 아니라 n-1로 나누는가"""
    W, H = 900, 300
    b = []
    b.append(text(26, 30, '표본은 모집단보다 덜 퍼져 보인다', 18, NAVY, 800))

    px0, px1, base, top = 70, 830, 210, 66
    sx = scale(-4, 4, px0, px1)
    pop = normal_pts(0, 1.0, -4, 4)
    peak = max(y for _, y in pop)
    line, area = curve_paths(pop, sx, base, top, peak)
    b.append(f'<path d="{area}" fill="{NAVY_TINT}" opacity=".45"/>')
    b.append(f'<path d="{line}" fill="none" stroke="{NAVY}" stroke-width="2.4"/>')
    b.append(text(sx(-2.9), top + 16, '모집단', 15, NAVY, 700, 'middle'))

    # 표본 몇 개는 가운데에 몰려 뽑힌다
    import random
    random.seed(3)
    xs = [random.gauss(0, 0.72) for _ in range(9)]
    for x in xs:
        b.append(f'<circle cx="{sx(x):.0f}" cy="{base-12}" r="6" fill="{TEAL}" opacity=".85"/>')
    lo, hi = min(xs), max(xs)
    b.append(f'<path d="M{sx(lo):.0f},{base+16} L{sx(hi):.0f},{base+16}" stroke="{TEAL}" stroke-width="3"/>')
    b.append(f'<path d="M{sx(lo):.0f},{base+9} L{sx(lo):.0f},{base+23} M{sx(hi):.0f},{base+9} L{sx(hi):.0f},{base+23}" stroke="{TEAL}" stroke-width="3"/>')
    b.append(text(sx((lo + hi) / 2), base + 42, '표본이 실제로 퍼진 범위', 14, TEAL, 700, 'middle'))
    b.append(f'<path d="M{sx(-3.2):.0f},{base+16} L{sx(3.2):.0f},{base+16}" stroke="{NAVY}" stroke-width="1.5" stroke-dasharray="4 4"/>')
    b.append(text(sx(-3.2), base + 42, '모집단이 퍼진 범위', 13, NAVY, None, 'start'))

    b.append(caption(450, H - 42,
                     '표본은 극단값을 놓치기 쉬워 분산을 과소추정한다. n 대신 n−1로 나누면 그만큼 값이 커진다', 15, INK))
    b.append(caption(450, H - 16, '이 보정을 자유도라고 부른다', 14))
    write('ch02-n-minus-1.svg', svg(W, H, '\n'.join(b)))


def fig_sd_meaning():
    """표준편차 한 칸이 얼마나 되는가"""
    W, H = 900, 310
    b = []
    px0, px1, base, top = 70, 830, 222, 56
    sx = scale(-3.6, 3.6, px0, px1)
    pts = normal_pts(0, 1, -3.6, 3.6, 140)
    peak = max(y for _, y in pts)
    line, area = curve_paths(pts, sx, base, top, peak)

    bands = [(-1, 1, TEAL, .30), (-2, -1, TEAL, .16), (1, 2, TEAL, .16),
             (-3, -2, TEAL, .07), (2, 3, TEAL, .07)]
    for lo, hi, color, op in bands:
        seg = [(x, y) for x, y in pts if lo <= x <= hi]
        if not seg: continue
        p = 'M' + ' L'.join(f'{sx(x):.1f},{base-(y/peak)*(base-top):.1f}' for x, y in seg)
        p += f' L{sx(hi):.1f},{base} L{sx(lo):.1f},{base} Z'
        b.append(f'<path d="{p}" fill="{color}" opacity="{op}"/>')

    b.append(f'<path d="{line}" fill="none" stroke="{NAVY}" stroke-width="2.6"/>')
    b.append(axis(px0, px1, base))

    for v in (-3, -2, -1, 0, 1, 2, 3):
        b.append(dashed(sx(v), base, base - 8, MID, 1.5, '2 3'))
        lab = 'M' if v == 0 else (f'M{v:+d}SD' if abs(v) == 1 else f'M{v:+d}SD')
        b.append(text(sx(v), base + 24, lab, 13, SOFT, None, 'middle'))

    for lo, hi, pct, y in ((-1, 1, '68%', top + 46), (-2, 2, '95%', top + 88), (-3, 3, '99.7%', top + 128)):
        b.append(f'<path d="M{sx(lo):.0f},{y} L{sx(hi):.0f},{y}" stroke="{CORAL}" stroke-width="2"/>')
        b.append(f'<path d="M{sx(lo):.0f},{y-6} L{sx(lo):.0f},{y+6} M{sx(hi):.0f},{y-6} L{sx(hi):.0f},{y+6}" stroke="{CORAL}" stroke-width="2"/>')
        b.append(text(sx(0), y - 8, pct, 14, CORAL, 700, 'middle'))

    b.append(caption(450, base + 56,
                     '정규분포라면 평균 ±1 표준편차 안에 약 68%, ±2 안에 약 95%가 들어온다', 15, INK))
    b.append(caption(450, base + 80, '표준편차를 알면 "이 값이 흔한가 드문가"를 바로 말할 수 있다', 14))
    write('ch02-sd-meaning.svg', svg(W, H, '\n'.join(b)))


def fig_zscore():
    """표준점수 — 단위가 다른 두 점수를 비교한다"""
    W, H = 900, 320
    b = []
    subjects = [('수학', 70, 5, 72.8, 0.56, 0), ('영어', 90, 8, 94, 0.50, 470)]
    for name, mu, sd, raw, z, x0 in subjects:
        b.append(panel(x0, 0, 430, 200))
        b.append(text(x0 + 26, 34, f'{name}  (평균 {mu}, 표준편차 {sd})', 16, NAVY, 800))
        px0, px1, base, top = x0 + 36, x0 + 394, 158, 62
        sx = scale(mu - 3.4 * sd, mu + 3.4 * sd, px0, px1)
        pts = normal_pts(mu, sd, mu - 3.4 * sd, mu + 3.4 * sd)
        peak = max(y for _, y in pts)
        line, area = curve_paths(pts, sx, base, top, peak)
        b.append(f'<path d="{area}" fill="{TEAL_TINT}" opacity=".7"/>')
        b.append(f'<path d="{line}" fill="none" stroke="{TEAL}" stroke-width="2.4"/>')
        b.append(axis(px0, px1, base))
        b.append(dashed(sx(mu), base, top + 6, FAINT, 1.8))
        b.append(dashed(sx(raw), base, top - 2, CORAL, 2.4))
        b.append(f'<circle cx="{sx(raw):.0f}" cy="{base}" r="6" fill="{CORAL}"/>')
        b.append(text(sx(raw), top - 10, f'{raw}점', 15, CORAL, 800, 'middle'))
        b.append(text(x0 + 215, base + 26, f'z = ({raw} − {mu}) / {sd} = {z}', 15, INK, 700, 'middle'))

    b.append(f'<rect x="270" y="222" width="360" height="46" rx="23" fill="{NAVY}"/>')
    b.append(text(450, 251, '수학 0.56  >  영어 0.50', 19, '#fff', 800, 'middle'))
    b.append(caption(450, 296,
                     '원점수는 영어가 훨씬 높지만, 각 과목 안에서의 위치로 바꾸면 수학을 더 잘 본 것이다', 15, INK))
    write('ch02-zscore.svg', svg(W, H, '\n'.join(b)))


ALL = [fig_three_centers, fig_deviation, fig_why_square, fig_ss_flow,
       fig_n_minus_1, fig_sd_meaning, fig_zscore]
