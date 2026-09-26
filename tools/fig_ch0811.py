"""8장 종속표본 · 9장 일원분산분석 · 10장 다중비교 · 11장 이원분산분석 · 12장 부록"""
import csv, math, os
from figlib import *

DATA = os.path.join(ROOT, 'books', '01-basic-statistics', 'data')


def read(name):
    with open(os.path.join(DATA, name), encoding='utf-8') as f:
        return list(csv.DictReader(f))


def arrow(x0, y0, x1, y1, c=FAINT, w=2.2):
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    px, py = -uy, ux
    tipx, tipy = x1, y1
    return (f'<path d="M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}" stroke="{c}" stroke-width="{w}"/>'
            f'<path d="M{tipx-ux*8+px*5:.1f},{tipy-uy*8+py*5:.1f} L{tipx:.1f},{tipy:.1f} '
            f'L{tipx-ux*8-px*5:.1f},{tipy-uy*8-py*5:.1f}" fill="none" stroke="{c}" stroke-width="{w}"/>')


# ================================================================ 8장
def fig_difference():
    """두 열을 뺄셈 한 번으로 한 열로"""
    W, H = 900, 300
    b = []
    rows = [('1', '3.25', '3.89', '+0.64'), ('2', '3.70', '4.97', '+1.27'),
            ('3', '2.19', '3.04', '+0.85'), ('4', '2.17', '1.88', '−0.29'),
            ('⋮', '⋮', '⋮', '⋮')]
    # 왼쪽 표
    b.append(panel(20, 44, 340, 200))
    b.append(text(190, 32, '원자료 — 짝지어진 두 점수', 15, NAVY, 800, 'middle'))
    for j, h in enumerate(['id', '사전', '사후']):
        b.append(text(78 + j * 108, 74, h, 13.5, SOFT, 700, 'middle'))
    for i, r in enumerate(rows):
        y = 102 + i * 28
        for j in range(3):
            b.append(text(78 + j * 108, y, r[j], 14, INK, None, 'middle'))
    b.append(text(190, 262, '두 값이 서로 얽혀 있다 (r = .89)', 13, CORAL, 700, 'middle'))

    b.append(arrow(372, 144, 448, 144, TEAL, 2.6))
    b.append(text(410, 130, '뺄셈', 13.5, TEAL, 800, 'middle'))

    # 오른쪽 표
    b.append(panel(460, 44, 230, 200, stroke=TEAL, sw=2.5))
    b.append(text(575, 32, '차이점수 D', 15, TEAL, 800, 'middle'))
    b.append(text(575, 74, '사후 − 사전', 13.5, SOFT, 700, 'middle'))
    for i, r in enumerate(rows):
        b.append(text(575, 102 + i * 28, r[3], 14, INK, 600, 'middle'))
    b.append(text(575, 262, '서로 독립이다', 13, TEAL, 700, 'middle'))

    b.append(arrow(702, 144, 762, 144, NAVY, 2.6))
    b.append(f'<rect x="772" y="106" width="118" height="76" rx="9" fill="{NAVY}"/>')
    b.append(text(831, 134, '단일표본', 14, '#fff', 800, 'middle'))
    b.append(text(831, 156, 't-검정', 14, '#fff', 800, 'middle'))
    b.append(tex(831, 198, r'H_0 : \mu_D = 0', 14, NAVY, 'middle', w=200))
    b.append(caption(450, H - 12, '원점수는 더 이상 쓰이지 않는다. 검정이 묻는 것은 "이 변화량들의 평균이 0인가" 하나뿐이다', 14.5, INK))
    write('ch08-difference.svg', svg(W, H, '\n'.join(b)))


def fig_pre_post():
    """원점수의 겹침 vs 차이점수의 선명함"""
    pp = read('prepost.csv')
    pre = [float(r['pre']) for r in pp]
    post = [float(r['post']) for r in pp]
    dif = [b_ - a for a, b_ in zip(pre, post)]
    W, H = 900, 350
    b = []

    # 왼쪽: 사전/사후 개인별 선
    b.append(panel(0, 0, 430, H - 46))
    b.append(text(215, 32, '원점수 — 사람마다 출발선이 다르다', 15, NAVY, 800, 'middle'))
    top, bot = 70, 222
    lo, hi = 1.4, 5.3
    ypos = lambda v: bot - (bot - top) * (v - lo) / (hi - lo)
    x1, x2 = 130, 310
    for a, c in zip(pre, post):
        b.append(f'<path d="M{x1},{ypos(a):.1f} L{x2},{ypos(c):.1f}" stroke="{TEAL_LINE}" '
                 f'stroke-width="1.2" opacity=".75"/>')
    for a in pre:
        b.append(f'<circle cx="{x1}" cy="{ypos(a):.1f}" r="2.6" fill="{FAINT}"/>')
    for c in post:
        b.append(f'<circle cx="{x2}" cy="{ypos(c):.1f}" r="2.6" fill="{TEAL}"/>')
    for x, m, lab in ((x1, sum(pre)/len(pre), '사전'), (x2, sum(post)/len(post), '사후')):
        b.append(f'<path d="M{x-38},{ypos(m):.0f} L{x+38},{ypos(m):.0f}" stroke="{NAVY}" stroke-width="3"/>')
        b.append(text(x, bot + 24, f'{lab}  M = {m:.2f}', 13.5, INK, 700, 'middle'))
    b.append(text(215, bot + 46, '두 분포가 넓게 겹쳐 있다', 13, SOFT, None, 'middle'))

    # 오른쪽: 차이점수 분포
    b.append(panel(470, 0, 430, H - 46, stroke=TEAL, sw=2.5))
    b.append(text(685, 32, '차이점수 — 개인차가 빠진 뒤', 15, TEAL, 800, 'middle'))
    px0, px1, base = 510, 860, 216
    dlo, dhi = -0.8, 1.7
    sxd = scale(dlo, dhi, px0, px1)
    bins = 14
    counts = [0] * bins
    for v in dif:
        k = min(bins - 1, max(0, int((v - dlo) / (dhi - dlo) * bins)))
        counts[k] += 1
    mx = max(counts)
    bwid = (px1 - px0) / bins
    for i, cnt in enumerate(counts):
        if not cnt:
            continue
        h = (base - 82) * cnt / mx
        b.append(f'<rect x="{px0+i*bwid+1:.1f}" y="{base-h:.1f}" width="{bwid-2:.1f}" height="{h:.1f}" '
                 f'rx="2" fill="{TEAL}" opacity=".7"/>')
    b.append(axis(px0, px1, base))
    b.append(dashed(sxd(0), base + 6, 74, CORAL, 2.4))
    b.append(text(sxd(0), 66, '0 (변화 없음)', 13, CORAL, 800, 'middle'))
    md = sum(dif) / len(dif)
    b.append(f'<path d="M{sxd(md):.0f},{base+6} L{sxd(md):.0f},74" stroke="{NAVY}" stroke-width="2.6"/>')
    b.append(text(sxd(md) + 6, 66, f'M = {md:.3f}', 13.5, NAVY, 800))
    b.append(text(685, base + 28, 'SD가 0.65·0.89 → 0.435로 줄었다', 13.5, INK, 700, 'middle'))
    b.append(text(685, base + 48, '0에서 뚜렷이 떨어져 있다', 13, SOFT, None, 'middle'))

    b.append(caption(450, H - 14, '짝을 유지하면 개인의 원래 수준이 뺄셈으로 상쇄되고, 변화량만 남는다', 14.5, INK))
    write('ch08-pre-post.svg', svg(W, H, '\n'.join(b)))


def fig_paired_vs_not():
    """같은 자료, 다른 잣대"""
    W, H = 900, 320
    b = []
    for x0, title, tval, ci, col, note in (
            (0, '짝을 유지 (paired = TRUE)', 6.36, (0.298, 0.576), TEAL, 'df = 39'),
            (470, '짝을 무시 (paired = FALSE)', 2.50, (0.089, 0.785), CORAL, 'df = 78')):
        b.append(panel(x0, 0, 430, H - 56, stroke=col, sw=2.5))
        b.append(text(x0 + 215, 34, title, 15.5, col, 800, 'middle'))
        b.append(text(x0 + 215, 76, f't = {tval:.2f}', 26, col, 800, 'middle'))
        b.append(text(x0 + 215, 98, note, 13, SOFT, None, 'middle'))
        px0, px1, y = x0 + 50, x0 + 380, 156
        sx = scale(-0.1, 0.9, px0, px1)
        b.append(f'<path d="M{px0},{y} L{px1},{y}" stroke="{RULE}" stroke-width="1.6"/>')
        b.append(f'<path d="M{sx(0):.0f},{y-20} L{sx(0):.0f},{y+20}" stroke="{NAVY}" stroke-width="2"/>')
        b.append(text(sx(0), y + 38, '0', 13, NAVY, 700, 'middle'))
        b.append(f'<rect x="{sx(ci[0]):.0f}" y="{y-11}" width="{sx(ci[1])-sx(ci[0]):.0f}" height="22" '
                 f'rx="5" fill="{col}" opacity=".22" stroke="{col}" stroke-width="2"/>')
        b.append(f'<circle cx="{sx(0.437):.0f}" cy="{y}" r="5" fill="{col}"/>')
        b.append(text(x0 + 215, y + 62, f'95% CI 폭 {ci[1]-ci[0]:.3f}', 13.5, INK, 700, 'middle'))
        b.append(text(x0 + 215, y + 84, '평균 차이 0.437 (동일)', 13, SOFT, None, 'middle'))
    b.append(caption(450, H - 32, '평균 차이는 똑같은 0.437이다. 달라진 것은 그 차이를 재는 잣대, 곧 표준오차뿐이다', 14.5, INK))
    b.append(caption(450, H - 10, '두 점수의 상관 .888만큼 표준오차가 줄어 t값이 2.5배 커졌다', 13.5))
    write('ch08-paired-vs-not.svg', svg(W, H, '\n'.join(b)))


def fig_independence():
    """독립성이 깨지는 설계들"""
    W, H = 900, 250
    b = []
    cases = [('사전 · 사후', '같은 사람을 두 번', '반복측정'),
             ('남매 · 부부', '짝지어진 두 사람', '짝 자료'),
             ('중간 · 기말', '같은 학생의 두 시험', '반복측정')]
    for i, (t1, t2, tag) in enumerate(cases):
        x = 24 + i * 292
        b.append(panel(x, 52, 268, 132, stroke=TEAL_LINE, sw=2))
        b.append(text(x + 134, 86, t1, 17, NAVY, 800, 'middle'))
        b.append(f'<circle cx="{x+100}" cy="122" r="13" fill="{TEAL_TINT}" stroke="{TEAL}" stroke-width="2"/>')
        b.append(f'<circle cx="{x+168}" cy="122" r="13" fill="{TEAL_TINT}" stroke="{TEAL}" stroke-width="2"/>')
        b.append(f'<path d="M{x+113},122 L{x+155},122" stroke="{TEAL}" stroke-width="2.4"/>')
        b.append(text(x + 134, 162, t2, 13.5, MID, None, 'middle'))
        b.append(f'<rect x="{x+96}" y="{52-11}" width="76" height="22" rx="11" fill="{TEAL}"/>')
        b.append(text(x + 134, 56, tag, 12, '#fff', 700, 'middle'))
    b.append(caption(450, 32, '두 측정치가 서로 얽혀 있는 설계들', 16, INK))
    b.append(caption(450, H - 32, '관측치가 80개여도 독립적인 정보는 40개뿐이다. 자유도가 78이 아니라 39인 이유다', 14.5, INK))
    b.append(caption(450, H - 10, '종속적인 관측치는 아무리 많아도 표본크기에 1 이상 기여하지 못한다', 13.5))
    write('ch08-independence.svg', svg(W, H, '\n'.join(b)))


# ================================================================ 9장
def fig_alpha_inflation():
    """집단이 늘면 오류가 쌓인다"""
    W, H = 900, 290
    b = []
    data = [(2, 1, .0500), (3, 3, .1426), (4, 6, .2649), (5, 10, .4013), (6, 15, .5367)]
    px0, px1, base, top = 110, 790, 214, 62
    b.append(axis(px0, px1, base))
    b.append(f'<path d="M{px0},{base} L{px0},{top}" stroke="{MID}" stroke-width="2"/>')
    ypos = lambda v: base - (base - top) * v / 0.6
    b.append(f'<path d="M{px0},{ypos(.05):.0f} L{px1},{ypos(.05):.0f}" stroke="{TEAL}" '
             f'stroke-width="1.8" stroke-dasharray="6 4"/>')
    b.append(f'<path d="M{px1},{ypos(.05):.0f} L{px1+16},{ypos(.05):.0f}" stroke="{TEAL}" '
             f'stroke-width="1.8" stroke-dasharray="6 4"/>')
    b.append(tex(px1 + 20, ypos(.05) + 5, r'\alpha = .05', 13, TEAL, 'start', w=90, baseline=True))
    for v in (0, .2, .4, .6):
        b.append(text(px0 - 12, ypos(v) + 5, f'{v:.1f}', 12.5, FAINT, None, 'end'))
    bw = 74
    for i, (k, c, p) in enumerate(data):
        x = px0 + 62 + i * 134
        col = CORAL if p > .2 else (AMBER if p > .1 else TEAL)
        b.append(f'<rect x="{x-bw/2:.0f}" y="{ypos(p):.0f}" width="{bw}" height="{base-ypos(p):.0f}" '
                 f'rx="5" fill="{col}" opacity=".85"/>')
        b.append(text(x, ypos(p) - 10, f'{p:.3f}', 13.5, INK, 800, 'middle'))
        b.append(text(x, base + 22, f'집단 {k}개', 13.5, MID, 700, 'middle'))
        b.append(text(x, base + 40, f'비교 {c}회', 12.5, FAINT, None, 'middle'))
    b.append(text(px0 + 6, top - 4, '최소 한 번이라도 잘못 판단할 확률', 14, SOFT))
    b.append(caption(450, H - 12, '집단이 여섯이면 오류 확률이 53.7%다. 그래서 비교를 여러 번 하지 않고 한 번에 묻는다', 14.5, INK))
    write('ch09-alpha-inflation.svg', svg(W, H, '\n'.join(b)))


def fig_why_variance():
    """같은 평균 차이라도 산포에 따라 판단이 다르다"""
    W, H = 900, 330
    b = []
    import random
    random.seed(7)
    means = [68, 74, 77]
    for row, (sd, title, verdict, col) in enumerate((
            (1.4, '집단 안이 촘촘할 때', '6점 차이는 대단한 것이다', TEAL),
            (7.0, '집단 안이 흩어져 있을 때', '6점은 우연의 범위 안이다', CORAL))):
        y0 = 16 + row * 148
        b.append(panel(0, y0, 900, 132, stroke=col, sw=2))
        b.append(text(26, y0 + 28, title, 15, col, 800))
        b.append(text(874, y0 + 28, verdict, 14, INK, 700, 'end'))
        px0, px1 = 110, 700
        lo, hi = 50, 95
        sx = scale(lo, hi, px0, px1)
        for gi, m in enumerate(means):
            yy = y0 + 58 + gi * 24
            b.append(text(px0 - 14, yy + 5, 'ABC'[gi], 13.5, MID, 700, 'end'))
            for _ in range(22):
                v = random.gauss(m, sd)
                b.append(f'<circle cx="{sx(v):.1f}" cy="{yy + random.uniform(-5,5):.1f}" r="2.8" '
                         f'fill="{FAINT}" opacity=".7"/>')
            b.append(f'<path d="M{sx(m):.0f},{yy-10} L{sx(m):.0f},{yy+10}" stroke="{NAVY}" stroke-width="2.6"/>')
            b.append(text(720, yy + 5, f'M = {m}', 13.5, INK, 700))
    b.append(caption(450, H - 10, '집단 평균은 위아래가 똑같이 68 · 74 · 77이다. 다르게 판단해야 하는 이유는 집단 안의 산포다', 14.5, INK))
    write('ch09-why-variance.svg', svg(W, H, '\n'.join(b)))


def fig_ss_partition():
    """한 사람의 편차가 둘로 쪼개진다"""
    W, H = 900, 360
    b = []
    base, top = 228, 74
    lo, hi = 59, 84
    ypos = lambda v: base - (base - top) * (v - lo) / (hi - lo)
    grand = 73.03
    gm = [68.2, 73.6, 77.3]
    # 주석을 둘 왼쪽 여백을 비워 두고, 집단 평균선은 오른쪽에 모은다
    xs = [350, 560, 770]
    half = 76

    b.append(f'<path d="M270,{ypos(grand):.0f} L866,{ypos(grand):.0f}" stroke="{NAVY}" '
             f'stroke-width="2.4" stroke-dasharray="7 5"/>')
    b.append(text(866, ypos(grand) - 10, f'전체 평균 {grand}', 13.5, NAVY, 700, 'end'))

    for i, (x, m) in enumerate(zip(xs, gm)):
        b.append(f'<path d="M{x-half},{ypos(m):.0f} L{x+half},{ypos(m):.0f}" stroke="{TEAL}" stroke-width="3"/>')
        # B의 평균(73.6)은 전체 평균과 거의 붙어 있으므로 라벨을 아래로 내린다
        dy = 20 if i == 1 else -10
        b.append(text(x, ypos(m) + dy, f'집단 {"ABC"[i]}  {m}', 13, TEAL, 700, 'middle'))

    px, pv = xs[0], 62.0
    b.append(f'<circle cx="{px}" cy="{ypos(pv):.0f}" r="6.5" fill="{CORAL}"/>')
    b.append(tex(px + 14, ypos(pv) + 5, 'X_{i1}', 13.5, CORAL, 'start', w=50, baseline=True))
    b.append(text(px + 48, ypos(pv) + 5, '(집단 A의 한 사람)', 13, CORAL, 700))

    bars = [
        (px - 46, pv, gm[0], CORAL, '집단 내 편차', '개인차'),
        (px - 46, gm[0], grand, TEAL, '집단 간 편차', '처치효과'),
        (px - 96, pv, grand, NAVY, '총 편차', 'SS_T의 재료'),
    ]
    for bx, v0, v1, c, lab, note in bars:
        y0, y1 = ypos(v0), ypos(v1)
        b.append(f'<path d="M{bx},{y0:.0f} L{bx},{y1:.0f}" stroke="{c}" stroke-width="2.6"/>')
        for yy in (y0, y1):
            b.append(f'<path d="M{bx-5},{yy:.0f} L{bx+5},{yy:.0f}" stroke="{c}" stroke-width="2.6"/>')
    # 라벨은 겹치지 않도록 한 줄씩 아래에 모아 둔다
    b.append(axis(60, 866, base + 10))
    for i, (_, _, _, c, lab, note) in enumerate(bars):
        y = base + 44 + i * 22
        b.append(f'<rect x="{60}" y="{y-10}" width="12" height="12" rx="3" fill="{c}"/>')
        b.append(text(80, y, lab, 13, INK, 700))
        b.append(text(190, y, f'— {note}', 12.5, SOFT))
    b.append(caption(450, 36, '한 사람이 전체 평균에서 벗어난 거리는 정확히 두 조각으로 나뉜다', 16, INK))
    b.append(tex(392, base + 52, r'(X_{ij} - \bar{X}) = (\bar{X_j} - \bar{X}) + (X_{ij} - \bar{X_j})',
                 15.5, INK, 'start', w=460, baseline=True))
    b.append(text(392, base + 80, '각각을 제곱해 모두 더한 것이', 13, SOFT))
    b.append(tex(572, base + 80, r'SS_T = SS_B + SS_W', 13.5, SOFT, 'start', w=200, baseline=True))
    b.append(text(706, base + 80, '이다', 13, SOFT))
    write('ch09-ss-partition.svg', svg(W, H, '\n'.join(b)))


def fig_f_structure():
    """F값의 구조"""
    W, H = 900, 262
    b = []
    cx = 450
    b.append(tex(cx - 6, 56, 'F =', 26, NAVY, 'end', w=90))
    # 분자
    b.append(f'<rect x="{cx+16}" y="30" width="330" height="40" rx="8" fill="{TEAL_TINT}" '
             f'stroke="{TEAL}" stroke-width="2"/>')
    b.append(text(cx + 181, 56, '집단 간 분산 = 처치효과 + 개인차', 15, TEAL, 800, 'middle'))
    b.append(f'<path d="M{cx+16},82 L{cx+346},82" stroke="{NAVY}" stroke-width="2.6"/>')
    # 분모
    b.append(f'<rect x="{cx+16}" y="94" width="330" height="40" rx="8" fill="{CORAL_TINT}" '
             f'stroke="{CORAL}" stroke-width="2"/>')
    b.append(text(cx + 181, 120, '집단 내 분산 = 개인차', 15, CORAL, 800, 'middle'))

    b.append(text(cx - 260, 56, '처치효과가 0이면', 14, MID, 700))
    b.append(text(cx - 260, 80, '분자와 분모가 같아져', 14, MID, 700))
    b.append(tex(cx - 260, 108, 'F = 1', 15, NAVY, 'start', w=70, baseline=True))
    b.append(text(cx - 205, 108, '이 된다', 15, NAVY, 800))
    b.append(text(cx - 260, 134, 'F가 1보다 충분히 크면', 13.5, SOFT))
    b.append(text(cx - 260, 152, '개인차만으로는 설명되지', 13.5, SOFT))
    b.append(text(cx - 260, 172, '않는 무언가가 있다는 뜻', 13.5, SOFT))

    b.append(f'<rect x="{cx+16}" y="152" width="330" height="62" rx="8" fill="{PAPER}" '
             f'stroke="{RULE}" stroke-width="2"/>')
    b.append(text(cx + 181, 172, '교수법 자료', 13, SOFT, 700, 'middle'))
    b.append(tex(cx + 181, 194, r'F = \dfrac{209.43}{11.56} = 18.12', 16, INK, 'middle', w=300))
    b.append(caption(450, H - 12, '7장에서 t값을 "관찰된 차이 ÷ 그 차이가 변동하는 정도"로 읽었던 것과 같은 구조다', 14))
    write('ch09-f-structure.svg', svg(W, H, '\n'.join(b)))


def fig_f_distribution():
    """F분포"""
    W, H = 900, 300
    b = []
    px0, px1, base, top = 80, 820, 218, 62
    sx = scale(0, 22, px0, px1)

    def fpdf(x, d1, d2):
        if x <= 0:
            return 0.0
        lb = (math.lgamma((d1 + d2) / 2) - math.lgamma(d1 / 2) - math.lgamma(d2 / 2)
              + (d1 / 2) * math.log(d1 / d2) + (d1 / 2 - 1) * math.log(x)
              - ((d1 + d2) / 2) * math.log(1 + d1 * x / d2))
        return math.exp(lb)

    pts = [(i * 22 / 400, fpdf(i * 22 / 400, 2, 27)) for i in range(1, 401)]
    peak = max(y for _, y in pts)
    crit = 3.354
    seg = [(x, y) for x, y in pts if x >= crit]
    _, a = curve_paths(seg, sx, base, top, peak)
    b.append(f'<path d="{a}" fill="{CORAL}" opacity=".3"/>')
    line, area = curve_paths(pts, sx, base, top, peak)
    b.append(f'<path d="{area}" fill="{TEAL_TINT}" opacity=".5"/>')
    b.append(f'<path d="{line}" fill="none" stroke="{TEAL}" stroke-width="2.8"/>')
    b.append(axis(px0, px1, base))
    for v in (0, 5, 10, 15, 20):
        b.append(f'<path d="M{sx(v):.0f},{base} L{sx(v):.0f},{base+6}" stroke="{MID}" stroke-width="1.6"/>')
        b.append(text(sx(v), base + 22, str(v), 12.5, FAINT, None, 'middle'))
    b.append(dashed(sx(crit), base, top + 44, CORAL, 2.2))
    b.append(text(sx(crit) + 8, top + 56, '임계값 3.354', 13.5, CORAL, 800))
    b.append(tex(sx(crit) + 94, top + 56, r'(\alpha = .05)', 13.5, CORAL, 'start', w=110, baseline=True))
    b.append(f'<circle cx="{sx(18.12):.0f}" cy="{base}" r="6" fill="{NAVY}"/>')
    b.append(dashed(sx(18.12), base, top + 90, NAVY, 2.2))
    b.append(text(sx(18.12), top + 84, '우리 결과 F = 18.12', 13.5, NAVY, 800, 'middle'))
    b.append(text(px0 + 6, top - 4, 'F 분포', 14, SOFT))
    b.append(tex(px0 + 52, top - 4, r'(df_1 = 2,\; df_2 = 27)', 14, SOFT, 'start', w=190, baseline=True))
    b.append(caption(450, H - 34, '분산의 비율이므로 음수가 없고, 0에서 시작해 오른쪽으로 길게 늘어진다', 14.5, INK))
    b.append(caption(450, H - 12, '기각역이 오른쪽 꼬리에만 있는 일방검정이다', 13.5))
    write('ch09-f-distribution.svg', svg(W, H, '\n'.join(b)))


def fig_group_means():
    """세 교수법의 분포"""
    tc = read('teaching.csv')
    groups = {}
    for r in tc:
        groups.setdefault(r['method'], []).append(float(r['score']))
    W, H = 900, 300
    b = []
    px0, px1, base, top = 130, 800, 226, 66
    lo, hi = 58, 86
    ypos = lambda v: base - (base - top) * (v - lo) / (hi - lo)
    for v in range(60, 86, 5):
        b.append(f'<path d="M{px0-8},{ypos(v):.0f} L{px1},{ypos(v):.0f}" stroke="{RULE}" stroke-width="1"/>')
        b.append(text(px0 - 16, ypos(v) + 5, str(v), 12.5, FAINT, None, 'end'))
    grand = sum(sum(v) for v in groups.values()) / 30
    b.append(f'<path d="M{px0},{ypos(grand):.0f} L{px1},{ypos(grand):.0f}" stroke="{NAVY}" '
             f'stroke-width="2" stroke-dasharray="7 5"/>')
    b.append(text(px1 + 2, ypos(grand) + 5, '', 12))
    xs = [270, 465, 660]
    for (key, x) in zip(sorted(groups), xs):
        vals = groups[key]
        m = sum(vals) / len(vals)
        sd = (sum((v - m) ** 2 for v in vals) / (len(vals) - 1)) ** .5
        b.append(f'<rect x="{x-26}" y="{ypos(m+sd):.0f}" width="52" '
                 f'height="{ypos(m-sd)-ypos(m+sd):.0f}" rx="5" fill="{TEAL_TINT}" '
                 f'stroke="{TEAL_LINE}" stroke-width="1.6"/>')
        for i, v in enumerate(vals):
            off = -18 + (i % 5) * 9
            b.append(f'<circle cx="{x+off}" cy="{ypos(v):.1f}" r="3.2" fill="{TEAL}" opacity=".65"/>')
        b.append(f'<path d="M{x-40},{ypos(m):.0f} L{x+40},{ypos(m):.0f}" stroke="{NAVY}" stroke-width="3"/>')
        b.append(text(x, base + 24, f'교수법 {key}', 14.5, INK, 700, 'middle'))
        b.append(text(x, base + 44, f'M = {m:.1f}   SD = {sd:.2f}', 13, SOFT, None, 'middle'))
    b.append(axis(px0, px1, base))
    b.append(text(px0 - 16, top - 4, '점수', 13, SOFT, None, 'end'))
    b.append(text(px1 - 4, ypos(grand) - 10, f'전체 평균 {grand:.2f}', 13, NAVY, 700, 'end'))
    b.append(caption(450, H - 12, '평균은 순서대로 올라가고, 흩어진 정도(상자 = ±1SD)는 세 집단이 거의 같다', 14.5, INK))
    write('ch09-group-means.svg', svg(W, H, '\n'.join(b)))


def fig_t_vs_anova():
    """t검정 3번 vs 분산분석 1번"""
    W, H = 900, 260
    b = []
    b.append(panel(0, 0, 430, H - 52, stroke=CORAL, sw=2.5))
    b.append(text(215, 34, 't-검정을 세 번', 16, CORAL, 800, 'middle'))
    pairs = ['A vs B', 'A vs C', 'B vs C']
    for i, p in enumerate(pairs):
        y = 72 + i * 38
        b.append(f'<rect x="90" y="{y}" width="250" height="30" rx="6" fill="{CORAL_TINT}" '
                 f'stroke="{CORAL}" stroke-width="1.6"/>')
        b.append(text(160, y + 20, p, 13.5, INK, 700, 'middle'))
        b.append(tex(300, y + 20, r'\alpha = .05', 13, CORAL, 'middle', w=90))
    b.append(text(215, 198, '군집당 오류 .143 — 통제 실패', 14.5, CORAL, 800, 'middle'))

    b.append(panel(470, 0, 430, H - 52, stroke=TEAL, sw=2.5))
    b.append(text(685, 34, '분산분석 한 번', 16, TEAL, 800, 'middle'))
    b.append(f'<rect x="530" y="86" width="310" height="62" rx="8" fill="{TEAL_TINT}" '
             f'stroke="{TEAL}" stroke-width="2"/>')
    b.append(tex(685, 114, r'H_0 : \mu_A = \mu_B = \mu_C', 17, INK, 'middle', w=300))
    b.append(text(685, 134, '세 평균이 모두 같은가?', 13, MID, None, 'middle'))
    b.append(text(685, 198, '군집당 오류 .05 — 유지', 14.5, TEAL, 800, 'middle'))
    b.append(caption(450, H - 14, '대신 기각되어도 어느 집단끼리 다른지는 알려주지 않는다. 그 확인이 10장의 다중비교다', 14, INK))
    write('ch09-t-vs-anova.svg', svg(W, H, '\n'.join(b)))


# ================================================================ 10장
def fig_what_f_says():
    """F가 유의하다는 것의 의미"""
    W, H = 900, 270
    b = []
    cases = [('A만 낮다', [68.2, 76.5, 77.3]), ('C만 높다', [68.2, 69.0, 77.3]),
             ('셋 다 다르다', [68.2, 73.6, 77.3])]
    for i, (title, ms) in enumerate(cases):
        x0 = 12 + i * 296
        b.append(panel(x0, 44, 272, 154, stroke=TEAL_LINE, sw=2))
        b.append(text(x0 + 136, 74, title, 15, NAVY, 800, 'middle'))
        px0, px1 = x0 + 36, x0 + 236
        base, top = 176, 98
        lo, hi = 64, 82
        ypos = lambda v: base - (base - top) * (v - lo) / (hi - lo)
        for gi, m in enumerate(ms):
            x = px0 + 34 + gi * 66
            b.append(f'<circle cx="{x}" cy="{ypos(m):.0f}" r="7" fill="{TEAL}"/>')
            b.append(text(x, base + 18, 'ABC'[gi], 12.5, SOFT, 700, 'middle'))
        b.append(axis(px0, px1, base))
    b.append(caption(450, 30, 'F가 유의하다 = "세 평균이 한 줄에 있지는 않다"', 16.5, INK))
    b.append(caption(450, H - 32, '세 배치 모두 F는 유의하게 나올 수 있다. 어느 경우인지는 F만으로 구분되지 않는다', 14.5, INK))
    b.append(caption(450, H - 10, '그래서 사후검정이 필요하다', 13.5))
    write('ch10-what-f-says.svg', svg(W, H, '\n'.join(b)))


def fig_familywise():
    """비교당 vs 군집당 유의수준"""
    W, H = 900, 270
    b = []
    b.append(panel(0, 40, 430, 172, stroke=CORAL, sw=2.5))
    b.append(text(215, 72, '보정하지 않으면', 16, CORAL, 800, 'middle'))
    for i, (lab, v) in enumerate((('비교 1', .05), ('비교 2', .05), ('비교 3', .05))):
        y = 100 + i * 28
        b.append(f'<rect x="60" y="{y}" width="{140}" height="20" rx="4" fill="{CORAL}" opacity=".35"/>')
        b.append(text(50, y + 15, lab, 12.5, MID, 700, 'end'))
        b.append(tex(212, y + 15, r'\alpha = .05', 13, CORAL, 'start', w=90, baseline=True))
    b.append(text(215, 196, '쌓이면 군집당 .143', 15, CORAL, 800, 'middle'))

    b.append(panel(470, 40, 430, 172, stroke=TEAL, sw=2.5))
    b.append(text(685, 72, '보정하면', 16, TEAL, 800, 'middle'))
    for i, lab in enumerate(('비교 1', '비교 2', '비교 3')):
        y = 100 + i * 28
        b.append(f'<rect x="530" y="{y}" width="{140}" height="20" rx="4" fill="{TEAL}" opacity=".35"/>')
        b.append(text(520, y + 15, lab, 12.5, MID, 700, 'end'))
        b.append(tex(682, y + 15, r'\alpha = .0167', 13, TEAL, 'start', w=100, baseline=True))
    b.append(text(685, 196, '전체가 .049로 묶인다', 15, TEAL, 800, 'middle'))
    b.append(caption(450, 26, '연구자가 통제해야 할 것은 개별 비교가 아니라 비교들의 묶음이다', 15.5, INK))
    b.append(caption(450, H - 14, '다중비교 방법들은 모두 "군집당 .05를 유지하면서 개별 비교를 어떻게 할 것인가"에 대한 답이다', 14))
    write('ch10-familywise.svg', svg(W, H, '\n'.join(b)))


def fig_methods():
    """네 방법의 보수성 축"""
    W, H = 900, 260
    b = []
    y = 118
    b.append(f'<path d="M80,{y} L820,{y}" stroke="{RULE}" stroke-width="5" stroke-linecap="round"/>')
    b.append(arrow(80, y, 60, y, SOFT, 2))
    b.append(arrow(820, y, 840, y, SOFT, 2))
    b.append(text(60, y - 30, '느슨함', 14, CORAL, 800))
    b.append(text(840, y - 30, '엄격함', 14, NAVY, 800, 'end'))
    b.append(text(60, y - 12, '차이를 잘 찾지만 헛발견도 는다', 12.5, SOFT))
    b.append(text(840, y - 12, '헛발견은 적지만 놓치기 쉽다', 12.5, SOFT, None, 'end'))
    items = [(150, 'Fisher LSD', '집단 3개일 때만', CORAL),
             (370, 'Tukey HSD', '기본 선택지', TEAL),
             (580, 'Bonferroni', '비교가 적을 때', AMBER),
             (790, 'Scheffé', '복합 비교 포함', NAVY)]
    for x, name, note, c in items:
        b.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{c}" stroke="#fff" stroke-width="3"/>')
        b.append(text(x, y + 40, name, 15, c, 800, 'middle'))
        b.append(text(x, y + 60, note, 12.5, SOFT, None, 'middle'))
    b.append(f'<rect x="{370-70}" y="{y+72}" width="140" height="24" rx="12" fill="{TEAL_TINT}" '
             f'stroke="{TEAL}" stroke-width="1.6"/>')
    b.append(text(370, y + 89, '특별한 사정 없으면 이것', 12, TEAL, 700, 'middle'))
    b.append(caption(450, 42, '사후검정 방법의 보수성', 17, INK))
    b.append(caption(450, H - 12, '분석을 마친 뒤에 유의하게 나오는 방법을 고르는 것은 유의성 낚시다. 미리 정해두어야 한다', 14))
    write('ch10-methods.svg', svg(W, H, '\n'.join(b)))


def fig_tukey_ci():
    """Tukey 신뢰구간 세 개"""
    W, H = 900, 290
    b = []
    rows = [('B − A', 5.4, 1.630, 9.170, .0040, True),
            ('C − A', 9.1, 5.330, 12.870, .0000064, True),
            ('C − B', 3.7, -0.070, 7.470, .0552, False)]
    px0, px1 = 250, 760
    sx = scale(-2, 14, px0, px1)
    b.append(f'<path d="M{sx(0):.0f},52 L{sx(0):.0f},214" stroke="{NAVY}" stroke-width="2.4"/>')
    b.append(text(sx(0), 42, '차이 = 0', 13.5, NAVY, 800, 'middle'))
    for i, (lab, d, lo, hi, p, sig) in enumerate(rows):
        y = 84 + i * 46
        c = TEAL if sig else CORAL
        b.append(f'<path d="M{px0-10},{y} L{px1},{y}" stroke="{RULE}" stroke-width="1"/>')
        b.append(f'<rect x="{sx(lo):.0f}" y="{y-11}" width="{sx(hi)-sx(lo):.0f}" height="22" rx="5" '
                 f'fill="{c}" opacity=".2" stroke="{c}" stroke-width="2"/>')
        b.append(f'<circle cx="{sx(d):.0f}" cy="{y}" r="5.5" fill="{c}"/>')
        b.append(text(px0 - 22, y + 5, lab, 14.5, INK, 800, 'end'))
        ptxt = 'p < .001' if p < .001 else f'p = {p:.4f}'
        b.append(text(px1 + 14, y + 5, ptxt, 13.5, c, 700))
    b.append(f'<ellipse cx="{sx(0):.0f}" cy="{84+2*46}" rx="24" ry="19" fill="none" stroke="{CORAL}" '
             f'stroke-width="2" stroke-dasharray="4 3"/>')

    b.append(axis(px0, px1, 232))
    for v in (0, 5, 10):
        b.append(text(sx(v), 250, str(v), 12.5, FAINT, None, 'middle'))
    b.append(caption(450, H - 10, '군집당 오류를 보정한 신뢰구간이다. 0을 걸치는 구간(붉은 점선)은 C−B 하나뿐이다', 14.5, INK))
    write('ch10-tukey-ci.svg', svg(W, H, '\n'.join(b)))


def fig_method_compare():
    """방법에 따라 결론이 갈리는 지점"""
    W, H = 900, 310
    b = []
    cols = ['보정 없음', 'Tukey HSD', 'Bonferroni', 'Holm']
    rows = [('B − A', [.0014, .0040, .0043, .0029]),
            ('C − A', [None, None, None, None]),
            ('C − B', [.0219, .0552, .0656, .0219])]
    x0, y0, cw, rh = 246, 92, 155, 46
    for j, c in enumerate(cols):
        b.append(text(x0 + cw * j + cw / 2, y0 - 16, c, 13.5, NAVY, 800, 'middle'))
    for i, (lab, vals) in enumerate(rows):
        y = y0 + i * rh
        b.append(text(x0 - 18, y + 28, lab, 14.5, INK, 800, 'end'))
        for j, v in enumerate(vals):
            x = x0 + cw * j
            if v is None:
                txt, sig = '< .001', True
            else:
                txt, sig = f'{v:.4f}', v < .05
            fill = TEAL_TINT if sig else CORAL_TINT
            stroke = TEAL if sig else CORAL
            b.append(f'<rect x="{x+6}" y="{y+6}" width="{cw-12}" height="{rh-12}" rx="6" '
                     f'fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>')
            b.append(text(x + cw / 2, y + 30, txt, 14, stroke, 800, 'middle'))
    yy = y0 + 2 * rh
    b.append(f'<rect x="{x0-2}" y="{yy}" width="{cw*4+4}" height="{rh}" rx="8" fill="none" '
             f'stroke="{AMBER}" stroke-width="2.6"/>')
    b.append(text(x0 + cw * 2, yy + rh + 20, '↑ 이 한 줄에서 결론이 갈린다', 13.5, AMBER, 800, 'middle'))
    b.append(caption(450, 42, '같은 자료, 같은 비교. 보정 방법만 바꾼 결과', 16.5, INK))
    b.append(caption(450, H - 32, 'C−B 한 쌍에서 보정 없음과 Holm은 유의하고, Tukey와 Bonferroni는 유의하지 않다', 14.5, INK))
    b.append(caption(450, H - 10, '그래서 방법은 분석 전에 정해두고, 결과가 어떻게 나오든 그대로 보고한다', 13.5))
    write('ch10-method-compare.svg', svg(W, H, '\n'.join(b)))


def fig_subsets():
    """동질적 부분집합"""
    W, H = 900, 290
    b = []
    px0, px1, base = 150, 790, 148
    lo, hi = 64, 82
    sx = scale(lo, hi, px0, px1)
    b.append(f'<path d="M{px0},{base} L{px1},{base}" stroke="{MID}" stroke-width="2"/>')
    for v in range(66, 81, 2):
        b.append(f'<path d="M{sx(v):.0f},{base} L{sx(v):.0f},{base+6}" stroke="{MID}" stroke-width="1.4"/>')
        b.append(text(sx(v), base + 22, str(v), 12, FAINT, None, 'middle'))
    pts = [('A', 68.2, NAVY), ('B', 73.6, TEAL), ('C', 77.3, TEAL)]
    for lab, m, c in pts:
        b.append(f'<circle cx="{sx(m):.0f}" cy="{base}" r="8" fill="{c}" stroke="#fff" stroke-width="2.5"/>')
        b.append(text(sx(m), base - 20, f'{lab}  {m}', 14, c, 800, 'middle'))
    # 부분집합 밴드
    b.append(f'<rect x="{sx(68.2)-26:.0f}" y="{base+40}" width="52" height="26" rx="13" '
             f'fill="{NAVY}" opacity=".16" stroke="{NAVY}" stroke-width="2"/>')
    b.append(text(sx(68.2), base + 58, '집합 1', 12.5, NAVY, 700, 'middle'))
    b.append(f'<rect x="{sx(73.6)-30:.0f}" y="{base+40}" width="{sx(77.3)-sx(73.6)+60:.0f}" height="26" '
             f'rx="13" fill="{TEAL}" opacity=".16" stroke="{TEAL}" stroke-width="2"/>')
    b.append(text((sx(73.6) + sx(77.3)) / 2, base + 58, '집합 2 — 서로 구분되지 않음', 12.5, TEAL, 700, 'middle'))
    b.append(caption(450, 42, 'A는 나머지 둘과 다르고, B와 C는 구분되지 않는다', 16.5, INK))
    b.append(caption(450, H - 32, '"구분되지 않는다"와 "같다"는 다르다. p = .055는 다르다고 판단할 근거가 부족하다는 뜻이다', 14.5, INK))
    b.append(caption(450, H - 10, '집단당 10명은 사후검정에 넉넉한 수가 아니다', 13.5))
    write('ch10-subsets.svg', svg(W, H, '\n'.join(b)))


# ================================================================ 11장
def fig_design():
    """2 × 3 설계의 구조"""
    W, H = 900, 350
    b = []
    x0, y0, cw, ch = 230, 92, 178, 62
    schools = ['분반', '합반', '단성학교']
    cells = [[66.57, 74.38, 83.58], [67.12, 76.73, 75.94]]
    rowm = [74.84, 73.26]
    colm = [66.84, 75.56, 79.76]
    for j, s in enumerate(schools):
        b.append(text(x0 + cw * j + cw / 2, y0 - 16, s, 14, NAVY, 800, 'middle'))
    b.append(text(x0 + cw * 3 + 62, y0 - 16, '주변평균', 14, CORAL, 800, 'middle'))
    for i, g in enumerate(['남', '여']):
        b.append(text(x0 - 20, y0 + ch * i + 38, g, 15, NAVY, 800, 'end'))
        for j in range(3):
            x, y = x0 + cw * j, y0 + ch * i
            b.append(f'<rect x="{x+4}" y="{y+4}" width="{cw-8}" height="{ch-8}" rx="7" '
                     f'fill="{TEAL_TINT}" stroke="{TEAL_LINE}" stroke-width="1.8"/>')
            b.append(text(x + cw / 2, y + 30, f'{cells[i][j]:.2f}', 16, INK, 700, 'middle'))
            b.append(text(x + cw / 2, y + 48, 'n = 18', 11.5, FAINT, None, 'middle'))
        x = x0 + cw * 3
        b.append(f'<rect x="{x+10}" y="{y0+ch*i+4}" width="104" height="{ch-8}" rx="7" '
                 f'fill="{CORAL_TINT}" stroke="{CORAL}" stroke-width="1.8"/>')
        b.append(text(x + 62, y0 + ch * i + 36, f'{rowm[i]:.2f}', 16, CORAL, 800, 'middle'))
    y = y0 + ch * 2
    b.append(text(x0 - 20, y + 32, '주변평균', 14, CORAL, 800, 'end'))
    for j in range(3):
        x = x0 + cw * j
        b.append(f'<rect x="{x+4}" y="{y+4}" width="{cw-8}" height="44" rx="7" '
                 f'fill="{CORAL_TINT}" stroke="{CORAL}" stroke-width="1.8"/>')
        b.append(text(x + cw / 2, y + 32, f'{colm[j]:.2f}', 16, CORAL, 800, 'middle'))
    x = x0 + cw * 3
    b.append(f'<rect x="{x+10}" y="{y+4}" width="104" height="44" rx="7" fill="{NAVY}"/>')
    b.append(text(x + 62, y + 32, '74.05', 16, '#fff', 800, 'middle'))

    def wide(t, size=13):
        # 한글은 한 글자가 대략 글자크기만큼, 로마자·숫자는 그 절반쯤 차지한다
        return sum(size if ord(c) > 0x2000 else size * .55 for c in t)

    legend = [(TEAL_TINT, TEAL_LINE, '셀 평균 — 상호작용이 본다'),
              (CORAL_TINT, CORAL, '주변평균 — 주효과가 본다'),
              (NAVY, NAVY, '전체 평균')]
    total = sum(34 + wide(l) for _, _, l in legend) - 34
    lx = (W - total) / 2
    for fill, stroke, lab in legend:
        b.append(f'<rect x="{lx}" y="{H-56}" width="14" height="14" rx="3" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="1.6"/>')
        b.append(text(lx + 20, H - 44, lab, 13, INK, 700))
        lx += 34 + wide(lab)
    b.append(caption(450, 42, '2 × 3 설계 — 셀 여섯 개, 주변평균 다섯 개, 전체 평균 하나', 16.5, INK))
    b.append(caption(450, H - 16, '주효과는 바깥쪽 붉은 칸만 본다. 그래서 셀 안에서 벌어지는 일을 놓칠 수 있다', 14))
    write('ch11-design.svg', svg(W, H, '\n'.join(b)))


def fig_ss_split():
    """제곱합이 넷으로"""
    W, H = 900, 260
    b = []
    total_w, x0 = 800, 50
    # 위: 일원
    b.append(text(x0, 42, '일원분산분석', 15, SOFT, 800))
    parts1 = [('설명되는 변동', 'SS_B', .38, TEAL), ('오차', 'SS_W', .62, FAINT)]
    xx = x0
    for lab, sym, frac, c in parts1:
        w = total_w * frac
        b.append(f'<rect x="{xx:.0f}" y="56" width="{w-4:.0f}" height="44" rx="6" fill="{c}" opacity=".35" '
                 f'stroke="{c}" stroke-width="2"/>')
        b.append(text(xx + w / 2 - 34, 84, lab, 13.5, INK, 700, 'middle'))
        b.append(tex(xx + w / 2 + 12, 84, sym, 13.5, INK, 'start', w=70, baseline=True))
        xx += w
    # 아래: 이원
    b.append(text(x0, 142, '이원분산분석', 15, NAVY, 800))
    parts2 = [('성별', 'SS_A', .012, NAVY), ('학교 유형', 'SS_B', .40, TEAL),
              ('상호작용', 'SS_{AB}', .066, AMBER), ('오차', 'SS_{S/AB}', .522, FAINT)]
    xx = x0
    for lab, sym, frac, c in parts2:
        w = total_w * frac
        b.append(f'<rect x="{xx:.0f}" y="156" width="{max(w-4,6):.0f}" height="44" rx="6" fill="{c}" '
                 f'opacity=".35" stroke="{c}" stroke-width="2"/>')
        if w > 110:
            b.append(text(xx + w / 2 - 30, 184, lab, 13, INK, 700, 'middle'))
            b.append(tex(xx + w / 2 + 6, 184, sym, 13.5, INK, 'start', w=90, baseline=True))
        else:
            # 칸이 좁으면 막대 아래에 기호만 적는다
            b.append(tex(xx + w / 2, 222, sym, 12.5, INK, 'middle', w=90))
        xx += w
    b.append(caption(450, 26, '전체 변동을 어떻게 나누는가', 16.5, INK))
    b.append(caption(450, H - 14, '요인을 하나 더 넣으면 그만큼 오차에서 빠져나간다. 분모가 작아지니 F가 커진다', 14, INK))
    write('ch11-ss-split.svg', svg(W, H, '\n'.join(b)))


def fig_interaction_types():
    """상호작용의 네 전형"""
    W, H = 900, 280
    b = []
    cases = [('상호작용 없음', [[3, 6], [5, 8]], '선이 평행하다'),
             ('서열적 상호작용', [[3, 7], [4, 5]], '기울기가 다르다'),
             ('비서열적 (교차)', [[3, 7], [7, 3]], '방향이 뒤집힌다'),
             ('한쪽만 효과', [[4, 4], [3, 8]], '한 선만 움직인다')]
    pw = 216
    for i, (title, lines, note) in enumerate(cases):
        x0 = 8 + i * (pw + 8)
        b.append(panel(x0, 44, pw, 176, stroke=RULE, sw=2))
        b.append(text(x0 + pw / 2, 72, title, 14, NAVY, 800, 'middle'))
        px0, px1, base, top = x0 + 46, x0 + pw - 34, 186, 92
        ypos = lambda v: base - (base - top) * (v - 2) / 7
        for li, (pts, c) in enumerate(zip(lines, (TEAL, CORAL))):
            xs = [px0, px1]
            b.append(f'<path d="M{xs[0]},{ypos(pts[0]):.0f} L{xs[1]},{ypos(pts[1]):.0f}" '
                     f'stroke="{c}" stroke-width="2.8"/>')
            for xx, vv in zip(xs, pts):
                b.append(f'<circle cx="{xx}" cy="{ypos(vv):.0f}" r="4.5" fill="{c}"/>')
        b.append(axis(px0 - 8, px1 + 8, base))
        b.append(text(px0, base + 18, '수준 1', 11.5, FAINT, None, 'middle'))
        b.append(text(px1, base + 18, '수준 2', 11.5, FAINT, None, 'middle'))
        b.append(text(x0 + pw / 2, base + 40, note, 12.5, SOFT, None, 'middle'))
    b.append(caption(450, 30, '가로축에 한 요인, 선으로 다른 요인. 셀 평균을 이어 그린다', 15.5, INK))
    b.append(caption(450, H - 12, '선이 평행하면 상호작용이 없다. 기울기가 다르거나 교차하면 있다', 14, INK))
    write('ch11-interaction-types.svg', svg(W, H, '\n'.join(b)))


def fig_interaction_plot():
    """실제 자료의 상호작용"""
    W, H = 900, 320
    b = []
    schools = ['남녀공학/분반', '남녀공학/합반', '단성학교']
    male = [66.57, 74.38, 83.58]
    female = [67.12, 76.73, 75.94]
    px0, px1, base, top = 180, 760, 236, 74
    lo, hi = 62, 88
    ypos = lambda v: base - (base - top) * (v - lo) / (hi - lo)
    for v in range(65, 86, 5):
        b.append(f'<path d="M{px0-14},{ypos(v):.0f} L{px1+20},{ypos(v):.0f}" stroke="{RULE}" stroke-width="1"/>')
        b.append(text(px0 - 22, ypos(v) + 5, str(v), 12.5, FAINT, None, 'end'))
    xs = [px0 + 40, (px0 + px1) / 2, px1 - 40]
    for series, c, lab in ((male, TEAL, '남'), (female, CORAL, '여')):
        d = 'M' + ' L'.join(f'{x:.0f},{ypos(v):.0f}' for x, v in zip(xs, series))
        b.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="3.2"/>')
        for x, v in zip(xs, series):
            b.append(f'<circle cx="{x:.0f}" cy="{ypos(v):.0f}" r="6" fill="{c}" stroke="#fff" stroke-width="2"/>')
        b.append(text(px1 + 28, ypos(series[-1]) + 5, lab, 15, c, 800))
    for x, s in zip(xs, schools):
        b.append(text(x, base + 24, s, 13, MID, 700, 'middle'))
    b.append(axis(px0 - 14, px1 + 20, base))
    # 벌어지는 구간 강조
    b.append(f'<rect x="{xs[2]-40:.0f}" y="{ypos(84):.0f}" width="80" height="{ypos(74)-ypos(84):.0f}" '
             f'rx="8" fill="none" stroke="{AMBER}" stroke-width="2.4" stroke-dasharray="5 4"/>')
    b.append(text(xs[2], ypos(84) - 12, '7.6점 차이', 13.5, AMBER, 800, 'middle'))
    b.append(text(280, 44, '성별 × 학교 유형', 16, INK, 700))
    b.append(tex(400, 44, r'F(2,\,102) = 6.27,\; p = .003', 16, INK, 'start', w=260, baseline=True))
    b.append(caption(450, H - 34, '분반과 합반에서는 남녀가 거의 겹치는데 단성학교에서만 벌어진다', 14.5, INK))
    b.append(caption(450, H - 12, '방향이 반대인 차이들이 주변평균에서는 상쇄되어 사라진다', 13.5))
    write('ch11-interaction-plot.svg', svg(W, H, '\n'.join(b)))


def fig_marginal_masking():
    """주변평균이 상호작용을 가린다"""
    W, H = 900, 270
    b = []
    b.append(panel(0, 44, 430, 172, stroke=RULE, sw=2))
    b.append(text(215, 74, '주변평균만 보면', 15.5, SOFT, 800, 'middle'))
    px0, px1, base = 100, 330, 168
    ypos = lambda v: base - (base - 100) * (v - 70) / 10
    for x, v, lab, c in ((160, 74.84, '남 74.84', NAVY), (270, 73.26, '여 73.26', NAVY)):
        b.append(f'<rect x="{x-30}" y="{ypos(v):.0f}" width="60" height="{base-ypos(v):.0f}" rx="5" '
                 f'fill="{FAINT}" opacity=".4"/>')
        b.append(text(x, ypos(v) - 10, lab, 13, MID, 700, 'middle'))
    b.append(axis(px0, px1, base))
    b.append(text(215, 196, '거의 같다 → p = .201', 14.5, SOFT, 700, 'middle'))

    b.append(panel(470, 44, 430, 172, stroke=AMBER, sw=2.5))
    b.append(text(685, 72, '셀 평균을 보면', 15.5, AMBER, 800, 'middle'))
    rows = [('분반', 66.57, 67.12), ('합반', 74.38, 76.73), ('단성', 83.58, 75.94)]
    for i, (lab, m, f) in enumerate(rows):
        y = 118 + i * 28
        b.append(text(540, y, lab, 13, MID, 700, 'end'))
        b.append(text(600, y, f'{m:.2f}', 13.5, TEAL, 700, 'middle'))
        b.append(text(680, y, f'{f:.2f}', 13.5, CORAL, 700, 'middle'))
        diff = m - f
        c = AMBER if abs(diff) > 3 else FAINT
        b.append(text(770, y, f'{diff:+.2f}', 13.5, c, 800, 'middle'))
    b.append(text(600, 96, '남', 12.5, TEAL, 800, 'middle'))
    b.append(text(680, 96, '여', 12.5, CORAL, 800, 'middle'))
    b.append(text(770, 96, '차이', 12.5, MID, 800, 'middle'))
    b.append(f'<path d="M540,104 L800,104" stroke="{RULE}" stroke-width="1.4"/>')
    b.append(text(685, 204, '단성학교에서만 7.64점 벌어진다', 14, AMBER, 800, 'middle'))
    b.append(caption(450, 30, '성별 주효과가 유의하지 않다 ≠ 성별이 성적과 무관하다', 16.5, INK))
    b.append(caption(450, H - 12, '방향이 반대인 차이들이 평균을 내는 과정에서 서로 상쇄된 것이다', 14, INK))
    write('ch11-marginal-masking.svg', svg(W, H, '\n'.join(b)))


def fig_simple_effects():
    """단순주효과 — 수준별로 나눠 보기"""
    W, H = 900, 250
    b = []
    for x0, who, F, p, ss, c in ((0, '남학생', 28.17, '< .001', 2612, TEAL),
                                  (470, '여학생', 14.56, '< .001', 1024, CORAL)):
        b.append(panel(x0, 34, 430, 160, stroke=c, sw=2.5))
        b.append(text(x0 + 215, 68, who, 18, c, 800, 'middle'))
        b.append(text(x0 + 215, 106, f'F(2, 51) = {F}', 20, INK, 800, 'middle'))
        b.append(text(x0 + 215, 132, f'p {p}', 14, SOFT, None, 'middle'))
        w = 300 * ss / 2612
        b.append(f'<rect x="{x0+65}" y="152" width="300" height="22" rx="5" fill="{RULE}"/>')
        b.append(f'<rect x="{x0+65}" y="152" width="{w:.0f}" height="22" rx="5" fill="{c}" opacity=".7"/>')
        b.append(text(x0 + 215, 168, f'SS = {ss:,}', 12.5, INK, 700, 'middle'))
    b.append(caption(450, 22, '상호작용이 유의하면 다른 요인의 수준별로 나누어 확인한다', 16, INK))
    b.append(caption(450, H - 32, '두 집단 모두 학교 유형의 효과는 유의하지만 크기가 두 배 이상 다르다', 14.5, INK))
    b.append(caption(450, H - 10, '학교 유형이 남학생의 성적에 더 크게 작용한다 — 상호작용이 유의했던 이유', 13.5))
    write('ch11-simple-effects.svg', svg(W, H, '\n'.join(b)))


# ================================================================ 12장
def fig_flowchart():
    """1권 전체 분석 선택 흐름도"""
    W, H = 900, 480
    b = []

    def box(x, y, w, h, fill='#fff', stroke=TEAL_LINE, sw=1.6, rx=7):
        return (f'<rect x="{x - w / 2:.0f}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def line(d):
        return f'<path d="{d}" stroke="{TEAL_LINE}" stroke-width="1.6" fill="none"/>'

    def fork(parent_x, y0, y1, kids):
        """부모에서 내려와 좌우로 뻗은 뒤 자식들로 갈라진다"""
        mid = (y0 + y1) / 2
        d = [f'M{parent_x},{y0} L{parent_x},{mid:.0f}',
             f'M{min(kids):.0f},{mid:.0f} L{max(kids):.0f},{mid:.0f}']
        d += [f'M{k:.0f},{mid:.0f} L{k:.0f},{y1}' for k in kids]
        return line(' '.join(d))

    # 잎(결과) 자리부터 정하고 위로 거슬러 올라간다
    LEAF = [(70, '독립표본 t', '7장', '평균 차이'),
            (196, '종속표본 t', '8장', '변화량'),
            (330, '일원분산분석', '9 · 10장', '어느 집단?'),
            (466, '이원분산분석', '11장', '상호작용'),
            (620, '상관분석', '2권', '관계 방향 · 강도'),
            (800, '카이제곱 검정', '2권', '빈도 차이')]

    b.append(box(450, 10, 300, 40, NAVY, NAVY, 0, 8))
    b.append(text(450, 35, '종속변수(결과)의 척도는?', 15, '#fff', 800, 'middle'))

    x_cont, x_cat = 300, 800
    b.append(fork(450, 50, 88, [x_cont, x_cat]))

    b.append(box(x_cont, 88, 258, 48))
    b.append(text(x_cont, 108, '연속형 (등간 · 비율)', 14, NAVY, 800, 'middle'))
    b.append(text(x_cont, 126, '점수, 소득, 리커트 평균', 12, FAINT, None, 'middle'))
    b.append(box(x_cat, 88, 200, 48))
    b.append(text(x_cat, 108, '범주형 (명목 · 서열)', 14, NAVY, 800, 'middle'))
    b.append(text(x_cat, 126, '찬반, 합격 여부', 12, FAINT, None, 'middle'))

    iv = [(133, 116, '독립변수', '범주형 · 2집단'),
          (398, 148, '독립변수', '범주형 · 3집단 이상'),
          (620, 120, '독립변수', '연속형')]
    b.append(fork(x_cont, 136, 178, [x for x, *_ in iv]))
    for x, w, t1, t2 in iv:
        b.append(box(x, 178, w, 46))
        b.append(text(x, 197, t1, 12.5, MID, None, 'middle'))
        b.append(text(x, 214, t2, 12.5, INK, 700, 'middle'))

    sub = [(133, [(70, '독립', '서로 다른 사람'), (196, '대응', '같은 사람 2회')]),
           (398, [(330, '요인 1개', '독립변수 하나'), (466, '요인 2개', '독립변수 둘')])]
    for parent, kids in sub:
        b.append(fork(parent, 224, 262, [k for k, *_ in kids]))
        for x, t1, t2 in kids:
            b.append(box(x, 262, 116, 42))
            b.append(text(x, 280, t1, 12.5, INK, 700, 'middle'))
            b.append(text(x, 296, t2, 11, FAINT, None, 'middle'))

    b.append(line(f'M620,224 L620,330  M{x_cat},136 L{x_cat},330'))
    b.append(line(' '.join(f'M{x},304 L{x},330' for x, *_ in
                          [(70,), (196,), (330,), (466,)])))

    for x, name, ch, note in LEAF:
        b.append(box(x, 330, 128, 44, TEAL, TEAL, 0, 8))
        b.append(text(x, 350, name, 13, '#fff', 800, 'middle'))
        b.append(text(x, 366, ch, 11, '#CFEAF0', None, 'middle'))
        b.append(line(f'M{x},374 L{x},394'))
        b.append(text(x, 408, note, 11.5, SOFT, None, 'middle'))

    b.append(f'<rect x="60" y="432" width="780" height="34" rx="8" fill="{TEAL_TINT}" '
             f'stroke="{TEAL_LINE}" stroke-width="1.6"/>')
    b.append(text(450, 454, '영향력의 크기까지 알고 싶다면 → 회귀분석 (2권)  ·  측정도구를 검증하려면 → 요인분석 (3권)',
                  13, TEAL, 700, 'middle'))
    write('ch12-flowchart.svg', svg(W, H, '\n'.join(b)))


def run():
    fig_difference(); fig_pre_post(); fig_paired_vs_not(); fig_independence()
    fig_alpha_inflation(); fig_why_variance(); fig_ss_partition()
    fig_f_structure(); fig_f_distribution(); fig_group_means(); fig_t_vs_anova()
    fig_what_f_says(); fig_familywise(); fig_methods(); fig_tukey_ci()
    fig_method_compare(); fig_subsets()
    fig_design(); fig_ss_split(); fig_interaction_types(); fig_interaction_plot()
    fig_marginal_masking(); fig_simple_effects()
    fig_flowchart()


ALL = [run]
