"""5장 가설검정의 논리 · 6장 추정과 신뢰구간"""
import math
from figlib import *


# ================================================================ 5장
def fig_why_null():
    """영가설만 분포를 그릴 수 있다"""
    W, H = 900, 300
    b = []
    # 왼쪽: 영가설
    b.append(panel(0, 0, 430, H - 52, stroke=TEAL, sw=2.5))
    b.append(text(215, 34, '영가설 — 값이 하나로 정해진다', 16, TEAL, 800, 'middle'))
    px0, px1, base, top = 40, 390, 196, 70
    sx = scale(-4, 4, px0, px1)
    pts = normal_pts(0, 1, -4, 4, 140)
    peak = max(y for _, y in pts)
    line, area = curve_paths(pts, sx, base, top, peak)
    b.append(f'<path d="{area}" fill="{TEAL_TINT}" opacity=".75"/>')
    b.append(f'<path d="{line}" fill="none" stroke="{TEAL}" stroke-width="2.6"/>')
    b.append(axis(px0, px1, base))
    b.append(dashed(sx(0), base, top + 4, TEAL, 2))
    b.append(tex(sx(0), base + 24, r'\mu_1 - \mu_2 = 0', 14, TEAL, 'middle', w=200))
    b.append(text(215, base + 48, '중심이 정해지니 확률을 계산할 수 있다', 13.5, SOFT, None, 'middle'))

    # 오른쪽: 대립가설
    b.append(panel(470, 0, 430, H - 52, stroke=RULE, sw=2.5))
    b.append(text(685, 34, '대립가설 — 값이 무수히 많다', 16, CORAL, 800, 'middle'))
    px0, px1 = 510, 860
    sx = scale(-4, 4, px0, px1)
    for mu, op in ((-2.1, .45), (-1.1, .5), (0.9, .5), (1.9, .45), (2.9, .4)):
        pts = normal_pts(mu, 1, -4, 4, 110)
        line, _ = curve_paths(pts, sx, base, top, peak)
        b.append(f'<path d="{line}" fill="none" stroke="{CORAL}" stroke-width="2" opacity="{op}"/>')
    b.append(axis(px0, px1, base))
    b.append(text(685, base + 22, '3점? 5점? 0.7점?', 14, CORAL, 700, 'middle'))
    b.append(text(685, base + 48, '어디를 중심으로 그려야 할지 정할 수 없다', 13.5, SOFT, None, 'middle'))

    b.append(caption(450, H - 14, '그래서 계산이 가능한 쪽을 영가설로 세우고, 그것을 기각하는 방식으로 검정한다', 14.5, INK))
    write('ch05-why-null.svg', svg(W, H, '\n'.join(b)))


def fig_pvalue():
    """p값은 점이 아니라 꼬리 면적"""
    W, H = 900, 320
    b = []
    px0, px1, base, top = 70, 830, 222, 62
    sx = scale(-4.2, 4.2, px0, px1)
    pts = normal_pts(0, 1, -4.2, 4.2, 200)
    peak = max(y for _, y in pts)
    line, area = curve_paths(pts, sx, base, top, peak)
    b.append(f'<path d="{area}" fill="{TEAL_TINT}" opacity=".45"/>')

    # 꼬리 면적 — 얇아서 옅게 칠하면 보이지 않는다
    obs = 2.3
    for lo, hi in ((obs, 4.2), (-4.2, -obs)):
        seg = [(x, y) for x, y in pts if lo <= x <= hi]
        if seg:
            sl, sa = curve_paths(seg, sx, base, top, peak)
            b.append(f'<path d="{sa}" fill="{CORAL}" opacity=".75"/>')
            b.append(f'<path d="{sl}" fill="none" stroke="{CORAL}" stroke-width="2"/>')
    b.append(f'<path d="{line}" fill="none" stroke="{TEAL}" stroke-width="2.6"/>')
    b.append(axis(px0, px1, base))

    b.append(dashed(sx(0), base, top, TEAL_LINE, 2))
    b.append(text(sx(0), top - 8, '영가설이 참이라면 여기가 중심', 13.5, SOFT, None, 'middle'))

    b.append(f'<circle cx="{sx(obs):.0f}" cy="{base}" r="6" fill="{CORAL}"/>')
    b.append(dashed(sx(obs), base, top + 30, CORAL, 2))
    b.append(text(sx(obs) + 10, top + 42, '내가 얻은 값', 14, CORAL, 800))

    for sign in (1, -1):
        xx = sx(sign * 2.85)
        b.append(f'<path d="M{xx:.0f},{base-10} L{xx:.0f},{base-46}" stroke="{CORAL}" stroke-width="1.6"/>')
        b.append(text(xx, base - 54, 'p값 = 이 면적', 13.5, CORAL, 800, 'middle'))

    b.append(caption(450, H - 36, 'p값은 내 결과보다 바깥쪽에 있는 면적이다. 한 점의 확률이 아니라 꼬리 전체의 넓이다', 15, INK))
    b.append(caption(450, H - 12, '양방검정에서는 반대쪽 꼬리까지 더한다', 13.5))
    write('ch05-pvalue.svg', svg(W, H, '\n'.join(b)))


def fig_error_table():
    """제1종 · 제2종 오류 2×2"""
    W, H = 900, 348
    b = []
    x0, y0, cw, ch = 250, 74, 300, 96
    b.append(text(x0 + cw, 34, '실   제', 15, NAVY, 800, 'middle'))
    for i, (h, note) in enumerate((('H_0', '이 참 (효과 없음)'), ('H_1', '이 참 (효과 있음)'))):
        mid = x0 + cw * (0.5 + i)
        b.append(tex(mid - 62, 62, h, 14, MID, 'start', w=40, baseline=True))
        b.append(text(mid - 42, 62, note, 14, MID, 700, 'start'))
    for k, chr_ in enumerate('판단'):
        b.append(text(74, y0 + ch - 10 + k * 22, chr_, 15, NAVY, 800, 'middle'))
    b.append(text(238, y0 + 50, '기각 실패', 14, MID, 700, 'end'))
    b.append(tex(238 - 34, y0 + ch + 50, 'H_0', 14, MID, 'end', w=60, baseline=True))
    b.append(text(238, y0 + ch + 50, '기각', 14, MID, 700, 'end'))

    # (칸 이름, 수식, 풀이말) — 수식은 KaTeX로 조판한다
    cells = [
        (0, 0, TEAL_TINT, TEAL, '옳은 판단', r'1 - \alpha', None),
        (1, 0, CORAL_TINT, CORAL, '제2종 오류', r'\beta', '있는 것을 놓침'),
        (0, 1, CORAL_TINT, CORAL, '제1종 오류', r'\alpha', '없는 것을 발견했다고 주장'),
        (1, 1, TEAL_TINT, TEAL, '검정력', r'1 - \beta', '있는 것을 찾아냄'),
    ]
    for cx, cy, fill, stroke, t1, formula, t2 in cells:
        x, y = x0 + cx * cw, y0 + cy * ch
        cx0 = x + cw / 2 - 3
        b.append(f'<rect x="{x}" y="{y}" width="{cw-6}" height="{ch-6}" rx="8" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        b.append(text(cx0, y + 32, t1, 15.5, stroke, 800, 'middle'))
        b.append(tex(cx0, y + 52, formula, 15, stroke, 'middle', w=180))
        if t2:
            b.append(text(cx0, y + 78, t2, 12.5, MID, None, 'middle'))

    b.append(caption(450, H - 38, '대각선 둘은 옳은 판단이고, 나머지 둘이 오류다. 통계학은 제1종 오류를 더 엄격하게 막는다', 15, INK))
    b.append(caption(450, H - 14, '없는 효과를 발표하면 그 위에 후속 연구가 쌓이기 때문이다', 13.5))
    write('ch05-error-table.svg', svg(W, H, '\n'.join(b)))


def fig_power_n():
    """표본크기와 검정력"""
    W, H = 900, 300
    b = []
    data = [(20, .338), (30, .478), (50, .697), (64, .801), (100, .940)]
    px0, px1, base, top = 100, 820, 218, 58
    b.append(axis(px0, px1, base))
    b.append(f'<path d="M{px0},{base} L{px0},{top}" stroke="{MID}" stroke-width="2"/>')
    ypos = lambda v: base - (base - top) * v
    # .80 기준선
    b.append(f'<path d="M{px0},{ypos(.8):.0f} L{px1},{ypos(.8):.0f}" stroke="{CORAL}" '
             f'stroke-width="1.8" stroke-dasharray="6 4"/>')
    b.append(text(px1 - 4, ypos(.8) - 10, '목표 .80', 13.5, CORAL, 700, 'end'))
    for v in (0, .2, .4, .6, .8, 1.0):
        b.append(text(px0 - 12, ypos(v) + 5, f'{v:.1f}', 12.5, FAINT, None, 'end'))

    bw = 78
    for i, (n, p) in enumerate(data):
        x = px0 + 56 + i * 140
        col = TEAL if p >= .8 else TEAL_LINE
        b.append(f'<rect x="{x-bw/2:.0f}" y="{ypos(p):.0f}" width="{bw}" height="{base-ypos(p):.0f}" '
                 f'rx="5" fill="{col}"/>')
        # 막대 안에 넣어야 .80 기준선과 겹치지 않는다
        b.append(text(x, ypos(p) + 22, f'{p:.3f}', 14, '#fff' if p >= .8 else INK, 800, 'middle'))
        b.append(text(x, base + 22, f'n = {n}', 13.5, MID, 700, 'middle'))
    b.append(text(px0 + 6, top - 4, '검정력 (효과크기 d = 0.50, α = .05 고정)', 14, SOFT))
    b.append(caption(450, H - 12, '각 집단 30명으로는 실재하는 중간 크기 효과의 절반 이상을 놓친다. 64명이 되어야 .80을 넘는다', 14.5, INK))
    write('ch05-power-n.svg', svg(W, H, '\n'.join(b)))


def fig_alpha_beta():
    """두 분포가 겹치는 구간에서 α와 β가 갈린다"""
    W, H = 900, 320
    b = []
    px0, px1, base, top = 70, 830, 222, 74
    sx = scale(-4, 7.2, px0, px1)
    p0 = normal_pts(0, 1, -4, 7.2, 220)
    p1 = normal_pts(3, 1, -4, 7.2, 220)
    peak = max(y for _, y in p0)
    crit = 1.96

    # β 영역 (대립분포에서 기각선 왼쪽)
    seg = [(x, y) for x, y in p1 if x <= crit]
    _, a = curve_paths(seg, sx, base, top, peak)
    b.append(f'<path d="{a}" fill="{AMBER}" opacity=".30"/>')
    # α 영역 (영분포에서 기각선 오른쪽) — 얇으므로 진하게 칠하고 윤곽선을 준다
    seg = [(x, y) for x, y in p0 if x >= crit]
    sl, a = curve_paths(seg, sx, base, top, peak)
    b.append(f'<path d="{a}" fill="{CORAL}" opacity=".8"/>')
    b.append(f'<path d="{sl}" fill="none" stroke="{CORAL}" stroke-width="2"/>')

    for pts, c, lab, note, lx in ((p0, NAVY, 'H_0', '분포 (효과 없음)', 0),
                                  (p1, TEAL, 'H_1', '분포 (효과 있음)', 3)):
        line, _ = curve_paths(pts, sx, base, top, peak)
        b.append(f'<path d="{line}" fill="none" stroke="{c}" stroke-width="2.6"/>')
        b.append(tex(sx(lx) - 62, top - 10, lab, 14, c, 'start', w=40, baseline=True))
        b.append(text(sx(lx) - 40, top - 10, note, 14, c, 800, 'start'))
    b.append(axis(px0, px1, base))
    b.append(dashed(sx(crit), base + 6, top - 26, INK, 2.2, '6 4'))
    b.append(text(sx(crit), top - 34, '기각선', 13.5, INK, 800, 'middle'))

    b.append(f'<rect x="{px0}" y="{H-58}" width="13" height="13" rx="3" fill="{CORAL}" opacity=".85"/>')
    b.append(text(px0 + 22, H - 47, 'α — 효과가 없는데 있다고 판단', 13.5, INK, 700))
    b.append(f'<rect x="{px0+330}" y="{H-58}" width="13" height="13" rx="3" fill="{AMBER}" opacity=".5"/>')
    b.append(text(px0 + 352, H - 47, 'β — 효과가 있는데 놓침', 13.5, INK, 700))
    b.append(caption(450, H - 14, '기각선을 오른쪽으로 옮기면 α는 줄지만 β는 늘어난다. 둘을 함께 줄이려면 표본을 키워야 한다', 14))
    write('ch05-alpha-beta.svg', svg(W, H, '\n'.join(b)))


def fig_logic_steps():
    """가설검정 5단계 소거법"""
    W, H = 900, 250
    b = []
    steps = [
        ('1', '영가설이 참이라고\n가정한다', NAVY),
        ('2', '그 가정 위에서\n분포를 그린다', NAVY),
        ('3', '내 결과가\n어디에 있는지 본다', TEAL),
        ('4', '너무 바깥이면\n가정을 의심한다', CORAL),
        ('5', '영가설을\n기각한다', CORAL),
    ]
    bw, gap = 148, 27
    left = (W - (bw * 5 + gap * 4)) / 2
    for i, (num, txt, c) in enumerate(steps):
        x = left + i * (bw + gap)
        b.append(f'<rect x="{x}" y="60" width="{bw}" height="106" rx="10" fill="{PAPER}" '
                 f'stroke="{c}" stroke-width="2.2"/>')
        b.append(f'<circle cx="{x+bw/2}" cy="86" r="15" fill="{c}"/>')
        b.append(text(x + bw / 2, 91, num, 14, '#fff', 800, 'middle'))
        for j, ln in enumerate(txt.split('\n')):
            b.append(text(x + bw / 2, 124 + j * 19, ln, 13.5, INK, 600, 'middle'))
        if i < 4:
            ax = x + bw + 6
            b.append(f'<path d="M{ax},113 L{ax+18},113" stroke="{FAINT}" stroke-width="2.2"/>')
            b.append(f'<path d="M{ax+13},108 L{ax+19},113 L{ax+13},118" fill="none" '
                     f'stroke="{FAINT}" stroke-width="2.2"/>')
    b.append(caption(450, 32, '가설검정은 대립가설을 증명하는 절차가 아니라, 영가설을 소거하는 절차다', 16, INK))
    b.append(caption(450, H - 16, '그래서 "기각에 실패했다"고 말하지 "영가설이 맞다"고 말하지 않는다', 14))
    write('ch05-logic-steps.svg', svg(W, H, '\n'.join(b)))


def fig_effect_vs_p():
    """같은 차이, 표본만 다를 때"""
    W, H = 900, 320
    b = []
    rows = [(50, 0.6374, 0.067), (100, 0.5050, 0.067), (400, 0.1824, 0.067), (1000, 0.0350, 0.067)]
    x0, y0, rh = 90, 86, 40
    cols = [(0, '표본크기'), (200, '평균 차이'), (390, '유의확률 p'), (600, "효과크기 d")]
    for cx, lab in cols:
        b.append(text(x0 + cx + 70, y0 - 14, lab, 14, NAVY, 800, 'middle'))
    for i, (n, p, d) in enumerate(rows):
        y = y0 + i * rh
        b.append(f'<rect x="{x0-10}" y="{y}" width="740" height="{rh-6}" rx="7" '
                 f'fill="{"#fff" if i%2 else PAPER}" stroke="{RULE}" stroke-width="1"/>')
        sig = p < .05
        b.append(text(x0 + 70, y + 23, f'n = {n:,}', 14, INK, 700, 'middle'))
        b.append(text(x0 + 270, y + 23, '1점', 14, MID, None, 'middle'))
        b.append(text(x0 + 460, y + 23, f'{p:.4f}' + ('  ✔ 유의' if sig else ''),
                      14, CORAL if sig else SOFT, 800 if sig else None, 'middle'))
        b.append(text(x0 + 670, y + 23, f'{d:.3f}', 14, TEAL, 800, 'middle'))
    b.append(caption(450, 40, '100점 만점에서 1점 차이. 표본크기만 바꿨다', 16, INK))
    b.append(caption(450, H - 32, '평균 차이도 효과크기도 그대로인데 p값만 작아져 결론이 뒤집힌다', 14.5, INK))
    b.append(caption(450, H - 10, '효과크기 공식에는 표본크기가 들어가지 않기 때문이다', 13.5))
    write('ch05-effect-vs-p.svg', svg(W, H, '\n'.join(b)))


# ================================================================ 6장
def fig_point_interval():
    """점추정 vs 구간추정"""
    W, H = 900, 260
    b = []
    for x0, title, color in ((0, '점추정', NAVY), (470, '구간추정', TEAL)):
        b.append(panel(x0, 0, 430, H - 56, stroke=color, sw=2.5))
        b.append(text(x0 + 215, 36, title, 18, color, 800, 'middle'))
    ln = 152
    # 왼쪽
    b.append(f'<path d="M50,{ln} L380,{ln}" stroke="{MID}" stroke-width="2"/>')
    b.append(f'<circle cx="215" cy="{ln}" r="7" fill="{NAVY}"/>')
    b.append(text(215, ln - 18, 'M = 3.50', 15, NAVY, 800, 'middle'))
    b.append(text(215, 84, '값 하나를 찍는다', 14, MID, None, 'middle'))
    b.append(text(215, ln + 30, '얼마나 믿을 만한지는 말해주지 않는다', 13, SOFT, None, 'middle'))
    # 오른쪽
    b.append(f'<path d="M520,{ln} L850,{ln}" stroke="{MID}" stroke-width="2"/>')
    b.append(f'<rect x="628" y="{ln-13}" width="114" height="26" rx="5" fill="{TEAL_TINT}" '
             f'stroke="{TEAL}" stroke-width="2"/>')
    b.append(f'<circle cx="685" cy="{ln}" r="6" fill="{TEAL}"/>')
    for x in (628, 742):
        b.append(f'<path d="M{x},{ln-13} L{x},{ln+13}" stroke="{TEAL}" stroke-width="2.6"/>')
    b.append(text(628, ln - 22, '3.39', 13.5, TEAL, 700, 'middle'))
    b.append(text(742, ln - 22, '3.60', 13.5, TEAL, 700, 'middle'))
    b.append(text(685, 84, '값 + 흔들릴 수 있는 범위', 14, MID, None, 'middle'))
    b.append(text(685, ln + 30, '구간이 좁을수록 정밀한 추정이다', 13, SOFT, None, 'middle'))
    b.append(caption(450, H - 16, '구간 = 추정치 ± (임계값 × 표준오차). 이 형태는 이후 모든 신뢰구간에서 똑같이 반복된다', 14.5, INK))
    write('ch06-point-interval.svg', svg(W, H, '\n'.join(b)))


def load_ci():
    """tools/ci_sim.csv — R에서 실제로 돌린 100개 신뢰구간"""
    import csv, os
    p = os.path.join(ROOT, 'tools', 'ci_sim.csv')
    with open(p, encoding='utf-8') as f:
        return [(float(r['m']), float(r['lo']), float(r['hi'])) for r in csv.DictReader(f)]


def fig_ci_coverage(rows=None):
    """100개 신뢰구간 중 몇 개가 모평균을 담는가"""
    W, H = 900, 330
    b = []
    mu = 3.5
    px0, px1, top, bot = 60, 840, 72, 250
    lo_v, hi_v = 2.48, 4.52
    sx = scale(lo_v, hi_v, px0, px1)
    if rows is None:
        rows = load_ci()
    n = len(rows)
    for i, (m, lo, hi) in enumerate(rows):
        y = top + (bot - top) * i / (n - 1)
        ok = lo <= mu <= hi
        c = TEAL_LINE if ok else CORAL
        b.append(f'<path d="M{sx(lo):.1f},{y:.1f} L{sx(hi):.1f},{y:.1f}" stroke="{c}" '
                 f'stroke-width="{1.6 if ok else 2.4}"/>')
        b.append(f'<circle cx="{sx(m):.1f}" cy="{y:.1f}" r="1.7" fill="{TEAL if ok else CORAL}"/>')
    b.append(f'<path d="M{sx(mu):.0f},{top-16} L{sx(mu):.0f},{bot+14}" stroke="{NAVY}" stroke-width="2.4"/>')
    b.append(tex(sx(mu) - 26, top - 19, r'\mu = 3.50', 14.5, NAVY, 'end', w=120, baseline=True))
    b.append(text(sx(mu) - 22, top - 19, '(모평균)', 14, NAVY, 800, 'start'))
    miss = sum(1 for m, lo, hi in rows if not (lo <= mu <= hi))
    b.append(f'<rect x="{px0}" y="{H-62}" width="13" height="13" rx="3" fill="{TEAL_LINE}"/>')
    b.append(text(px0 + 22, H - 51, f'모평균을 포함한 구간 {n-miss}개', 13.5, INK, 700))
    b.append(f'<rect x="{px0+280}" y="{H-62}" width="13" height="13" rx="3" fill="{CORAL}"/>')
    b.append(text(px0 + 302, H - 51, f'놓친 구간 {miss}개', 13.5, CORAL, 700))
    b.append(caption(450, H - 26, '95%가 말하는 것은 구간 하나에 대한 확률이 아니라, 이 절차를 반복했을 때의 성공률이다', 14.5, INK))
    b.append(caption(450, H - 6, '놓친 구간들은 오류가 아니라 설계상 예정된 5%다', 13.5))
    write('ch06-ci-coverage.svg', svg(W, H, '\n'.join(b)))


def fig_t_vs_z():
    """t분포와 정규분포"""
    W, H = 900, 370
    b = []
    px0, px1, base, top = 80, 820, 216, 62
    sx = scale(-4.2, 4.2, px0, px1)

    def tpdf(x, v):
        return (math.gamma((v + 1) / 2) / (math.sqrt(v * math.pi) * math.gamma(v / 2))
                * (1 + x * x / v) ** (-(v + 1) / 2))

    specs = [(3, CORAL, 'df = 3'), (10, AMBER, 'df = 10'), (30, TEAL, 'df = 30')]
    zpts = normal_pts(0, 1, -4.2, 4.2, 200)
    peak = max(y for _, y in zpts)
    line, _ = curve_paths(zpts, sx, base, top, peak)
    b.append(f'<path d="{line}" fill="none" stroke="{NAVY}" stroke-width="3"/>')
    for v, c, lab in specs:
        pts = [(x, tpdf(x, v)) for x, _ in zpts]
        line, _ = curve_paths(pts, sx, base, top, peak)
        b.append(f'<path d="{line}" fill="none" stroke="{c}" stroke-width="2.2"/>')
    b.append(axis(px0, px1, base))
    # 꼬리 강조
    b.append(f'<ellipse cx="{sx(3.1):.0f}" cy="{base-14}" rx="52" ry="24" fill="none" '
             f'stroke="{CORAL}" stroke-width="1.6" stroke-dasharray="4 3"/>')
    b.append(text(sx(3.1), base - 44, '꼬리가 두껍다', 13, CORAL, 700, 'middle'))

    items = [(NAVY, '정규분포 (z)', '임계값 1.960')] + \
            [(c, lab, f'임계값 {v}') for (v, c, lab), v in
             zip(specs, ('3.182', '2.228', '2.042'))]
    for i, (c, lab, note) in enumerate(items):
        y = base + 34 + i * 21
        b.append(f'<rect x="{px0+120}" y="{y-10}" width="12" height="12" rx="3" fill="{c}"/>')
        b.append(text(px0 + 140, y, lab, 13.5, INK, 700))
        b.append(text(px0 + 270, y, note, 13.5, SOFT))
    b.append(caption(450, H - 10, '자유도가 작을수록 꼬리가 두꺼워 같은 결론에 더 큰 값을 요구한다. 커지면 정규분포와 겹친다', 14, INK))
    write('ch06-t-vs-z.svg', svg(W, H, '\n'.join(b)))


def fig_ci_test():
    """신뢰구간과 유의성 판단은 같은 이야기"""
    W, H = 900, 340
    b = []
    px0, px1 = 130, 810
    sx = scale(2.8, 3.8, px0, px1)
    lo, hi, m = 3.391, 3.603, 3.497
    for i, (ref, lab, verdict, c) in enumerate(
            ((3.0, '기준값 3.0', '구간 밖 → p < .001, 기각', CORAL),
             (3.4, '기준값 3.4', '구간 안 → p = .072, 기각 실패', TEAL))):
        y = 104 + i * 112
        b.append(f'<path d="M{px0},{y} L{px1},{y}" stroke="{RULE}" stroke-width="1.6"/>')
        b.append(f'<rect x="{sx(lo):.0f}" y="{y-13}" width="{sx(hi)-sx(lo):.0f}" height="26" rx="5" '
                 f'fill="{TEAL_TINT}" stroke="{TEAL}" stroke-width="2"/>')
        b.append(f'<circle cx="{sx(m):.0f}" cy="{y}" r="5" fill="{TEAL}"/>')
        b.append(f'<path d="M{sx(ref):.0f},{y-22} L{sx(ref):.0f},{y+22}" stroke="{c}" stroke-width="2.6"/>')
        b.append(f'<circle cx="{sx(ref):.0f}" cy="{y}" r="6" fill="{c}"/>')
        b.append(text(sx(ref), y - 30, lab, 13.5, c, 800, 'middle'))
        b.append(text(px1 + 4, y + 5, '', 13))
        b.append(text(px0 - 14, y + 5, verdict.split(' → ')[0], 13, MID, 700, 'end'))
        b.append(text(sx((lo + hi) / 2), y + 40, verdict.split(' → ')[1], 13.5, c, 700, 'middle'))
    b.append(text(sx(lo), 62, '3.391', 13, TEAL, 700, 'middle'))
    b.append(text(sx(hi), 62, '3.603', 13, TEAL, 700, 'middle'))
    b.append(text(sx((lo + hi) / 2), 40, '95% 신뢰구간', 15, TEAL, 800, 'middle'))
    b.append(caption(450, H - 12, '기준값이 구간 안에 들어오면 기각되지 않는다. 신뢰구간과 유의확률은 언제나 같은 답을 준다', 14.5, INK))
    write('ch06-ci-test.svg', svg(W, H, '\n'.join(b)))


def fig_ci_width():
    """표본크기와 신뢰구간 폭"""
    W, H = 900, 290
    b = []
    rows = [(25, 0.3442), (100, 0.1654), (240, 0.1060), (400, 0.0820)]
    px0, px1 = 190, 800
    sx = scale(-0.42, 0.42, px0, px1)
    mid = sx(0)
    for i, (n, half) in enumerate(rows):
        y = 78 + i * 46
        b.append(f'<path d="M{px0},{y} L{px1},{y}" stroke="{RULE}" stroke-width="1.2"/>')
        b.append(f'<rect x="{sx(-half):.0f}" y="{y-12}" width="{sx(half)-sx(-half):.0f}" height="24" '
                 f'rx="5" fill="{TEAL_TINT}" stroke="{TEAL}" stroke-width="2"/>')
        b.append(f'<circle cx="{mid:.0f}" cy="{y}" r="4.5" fill="{TEAL}"/>')
        b.append(text(px0 - 16, y + 5, f'n = {n}', 14, INK, 700, 'end'))
        b.append(text(px1 + 4, y + 5, f'폭 {half*2:.3f}', 13.5, SOFT, None, None))
    b.append(f'<path d="M{mid:.0f},56 L{mid:.0f},{78+3*46+22}" stroke="{NAVY}" stroke-width="1.8" '
             f'stroke-dasharray="5 4"/>')
    b.append(text(mid, 46, '표본평균', 13.5, NAVY, 700, 'middle'))
    b.append(caption(450, H - 36, '25명에서 100명으로 75명을 더 모으면 폭이 0.357 줄지만,', 14, INK))
    b.append(caption(450, H - 14, '240명에서 400명으로 160명을 더 모아도 0.048밖에 줄지 않는다 — 수확체감', 14, INK))
    write('ch06-ci-width.svg', svg(W, H, '\n'.join(b)))


def fig_ci_meaning():
    """신뢰구간 해석 — 틀린 것과 옳은 것"""
    W, H = 900, 250
    b = []
    b.append(panel(0, 0, 430, H - 46, stroke=CORAL, sw=2.5, fill=CORAL_TINT))
    b.append(text(215, 40, '✕  틀린 해석', 17, CORAL, 800, 'middle'))
    for i, ln in enumerate(['"모평균이 이 구간에 있을', '확률이 95%다"']):
        b.append(text(215, 84 + i * 24, ln, 15.5, INK, 700, 'middle'))
    for i, ln in enumerate(['모평균은 고정된 상수이고', '구간도 이미 확정된 숫자다.',
                            '들어 있거나 아니거나 둘 중 하나다.']):
        b.append(text(215, 140 + i * 20, ln, 13, MID, None, 'middle'))

    b.append(panel(470, 0, 430, H - 46, stroke=TEAL, sw=2.5, fill=TEAL_TINT))
    b.append(text(685, 40, '✔  옳은 해석', 17, TEAL, 800, 'middle'))
    for i, ln in enumerate(['"같은 방식으로 구간을 만들면', '그중 95%가 모평균을 담는다"']):
        b.append(text(685, 84 + i * 24, ln, 15.5, INK, 700, 'middle'))
    for i, ln in enumerate(['95%가 수식하는 것은 구간이 아니라', '구간을 만드는 절차다.',
                            '지금 이 구간이 맞는지는 알 수 없다.']):
        b.append(text(685, 140 + i * 20, ln, 13, MID, None, 'middle'))
    b.append(caption(450, H - 14, '심사에서 가장 자주 지적되는 대목이므로 표현을 정확히 써야 한다', 14, INK))
    write('ch06-ci-meaning.svg', svg(W, H, '\n'.join(b)))


def run():
    fig_why_null(); fig_pvalue(); fig_error_table(); fig_power_n()
    fig_alpha_beta(); fig_logic_steps(); fig_effect_vs_p()
    fig_point_interval(); fig_ci_coverage(); fig_t_vs_z()
    fig_ci_test(); fig_ci_width(); fig_ci_meaning()


ALL = [run]
