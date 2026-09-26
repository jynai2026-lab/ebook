#!/usr/bin/env python3
"""
1권 기초통계 — 본문 그림 생성

  python3 tools/make-figures.py

books/01-basic-statistics/figures/*.svg 를 만듭니다.
개념도는 직접 그리고, 분포 그림은 R이 계산한 실제 데이터 값을 씁니다.
본문과 같은 색·폰트를 쓰므로 shared/theme/book.css 의 토큰과 맞춰 두었습니다.
"""
import json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(ROOT, 'books', '01-basic-statistics', 'figures')
os.makedirs(OUT, exist_ok=True)

INK, MID, SOFT, FAINT = '#101828', '#344054', '#667085', '#98A2B3'
TEAL, TEAL_LINE, TEAL_TINT = '#0E7490', '#A8D5DE', '#ECF7F9'
NAVY, RULE = '#16243F', '#E4E7EC'
CORAL, CORAL_TINT = '#C2452F', '#FBEAE6'

FONT = "Pretendard, sans-serif"


def svg(w, h, body):
    return (f'<svg viewBox="0 0 {w} {h}" font-family="{FONT}" '
            f'xmlns="http://www.w3.org/2000/svg">\n{body}\n</svg>\n')


def write(name, content):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  {name}')


def normal_path(mu, sd, x0, x1, px0, px1, base, height, peak_ref):
    """정규곡선을 SVG path로. peak_ref로 여러 곡선의 높이 축척을 통일한다."""
    pts = []
    n = 90
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        y = math.exp(-((x - mu) ** 2) / (2 * sd ** 2)) / (sd * math.sqrt(2 * math.pi))
        px = px0 + (px1 - px0) * (x - x0) / (x1 - x0)
        py = base - (y / peak_ref) * height
        pts.append(f'{px:.1f},{py:.1f}')
    return 'M' + ' L'.join(pts)


# ---------------------------------------------------------------- 그림 1
def fig_two_questions():
    """무엇이 궁금한가 — 집단을 통으로 보는 질문 vs 변수가 맞물리는 질문"""
    W, H = 900, 340
    b = []
    b.append(f'<rect x="0" y="0" width="430" height="{H}" rx="10" fill="#FBFCFD" stroke="{RULE}" stroke-width="2"/>')
    b.append(f'<rect x="470" y="0" width="430" height="{H}" rx="10" fill="#FBFCFD" stroke="{RULE}" stroke-width="2"/>')

    # ── 왼쪽: 집단을 통으로 본다
    b.append(f'<text x="26" y="34" font-size="19" font-weight="800" fill="{NAVY}">이 집단과 저 집단이 다른가</text>')
    b.append(f'<text x="26" y="58" font-size="15" fill="{SOFT}">개인은 사라지고 집단의 대표값만 남는다</text>')

    # 개인 점들이 두 덩어리로
    import random
    random.seed(7)
    for cx, color in ((120, FAINT), (300, FAINT)):
        for _ in range(22):
            px = cx + random.gauss(0, 26)
            py = 118 + random.gauss(0, 20)
            b.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="3.2" fill="{color}" opacity=".75"/>')

    b.append(f'<path d="M120,158 L120,186 M300,158 L300,186" stroke="{RULE}" stroke-width="2"/>')
    b.append(f'<text x="210" y="180" font-size="13" fill="{FAINT}" text-anchor="middle">뭉친다</text>')

    # 평균 두 개
    for cx, lab, val in ((120, '남성', '3.29'), (300, '여성', '3.70')):
        b.append(f'<circle cx="{cx}" cy="{212}" r="13" fill="{TEAL}"/>')
        b.append(f'<text x="{cx}" y="{247}" font-size="15" font-weight="700" fill="{INK}" text-anchor="middle">{lab}</text>')
        b.append(f'<text x="{cx}" y="{267}" font-size="15" fill="{TEAL}" text-anchor="middle">M = {val}</text>')

    b.append(f'<path d="M137,212 L283,212" stroke="{CORAL}" stroke-width="2.5" stroke-dasharray="6 5"/>')
    b.append(f'<text x="210" y="303" font-size="16" font-weight="700" fill="{CORAL}" text-anchor="middle">이 거리만 궁금하다</text>')
    b.append(f'<text x="210" y="325" font-size="14" fill="{SOFT}" text-anchor="middle">t-검정 · 분산분석</text>')

    # ── 오른쪽: 변수가 맞물려 움직이는가
    b.append(f'<text x="496" y="34" font-size="19" font-weight="800" fill="{NAVY}">한 변수가 움직이면 다른 변수도 움직이는가</text>')
    b.append(f'<text x="496" y="58" font-size="15" fill="{SOFT}">개인이 점으로 끝까지 남는다</text>')

    # 축
    b.append(f'<path d="M540,258 L860,258 M540,258 L540,88" stroke="{MID}" stroke-width="2"/>')
    b.append(f'<text x="700" y="284" font-size="14" fill="{SOFT}" text-anchor="middle">변수 X</text>')
    b.append(f'<text x="516" y="176" font-size="14" fill="{SOFT}" text-anchor="middle" transform="rotate(-90 516 176)">변수 Y</text>')

    random.seed(11)
    for _ in range(34):
        t = random.random()
        px = 552 + t * 296
        py = 246 - t * 140 + random.gauss(0, 17)
        py = max(96, min(252, py))
        b.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="3.6" fill="{TEAL}" opacity=".6"/>')
    b.append(f'<path d="M552,244 L848,104" stroke="{CORAL}" stroke-width="2.5"/>')

    b.append(f'<text x="700" y="303" font-size="16" font-weight="700" fill="{CORAL}" text-anchor="middle">이 맞물림이 궁금하다</text>')
    b.append(f'<text x="700" y="325" font-size="14" fill="{SOFT}" text-anchor="middle">상관분석 · 회귀분석</text>')

    write('two-questions.svg', svg(W, H, '\n'.join(b)))


# ---------------------------------------------------------------- 그림 2
def fig_distributions(dens):
    """실제 데이터의 두 집단 분포"""
    W, H = 900, 330
    L, R, BASE, TOP = 70, 860, 258, 52
    b = []
    peak = max(max(dens['male']['y']), max(dens['female']['y']))

    # 축
    b.append(f'<path d="M{L},{BASE} L{R},{BASE}" stroke="{MID}" stroke-width="2"/>')
    for v in (1, 2, 3, 4, 5):
        px = L + (R - L) * (v - 1) / 4.2
        b.append(f'<path d="M{px:.0f},{BASE} L{px:.0f},{BASE+6}" stroke="{MID}" stroke-width="2"/>')
        b.append(f'<text x="{px:.0f}" y="{BASE+26}" font-size="14" fill="{SOFT}" text-anchor="middle">{v}</text>')
    b.append(f'<text x="{(L+R)/2:.0f}" y="{BASE+52}" font-size="14" fill="{SOFT}" text-anchor="middle">자아존중감 (5점 리커트 문항 평균)</text>')

    def build(key, color, fill):
        d = dens[key]
        pts = [f'{L + (R-L)*(x-1)/4.2:.1f},{BASE - (y/peak)*(BASE-TOP):.1f}'
               for x, y in zip(d['x'], d['y'])]
        line = 'M' + ' L'.join(pts)
        area = line + f' L{L + (R-L)*(d["x"][-1]-1)/4.2:.1f},{BASE} L{L + (R-L)*(d["x"][0]-1)/4.2:.1f},{BASE} Z'
        return line, area, L + (R - L) * (d['mean'] - 1) / 4.2, color, fill

    layers = [build('male', NAVY, '#C7D0DE'), build('female', TEAL, TEAL_TINT)]
    # 채움 -> 평균선 -> 곡선 순. 뒤 곡선의 채움이 앞 곡선의 선을 덮지 않게 한다.
    for _, area, _, _, fill in layers:
        b.append(f'<path d="{area}" fill="{fill}" opacity=".55"/>')
    for _, _, mx, color, _ in layers:
        b.append(f'<path d="M{mx:.0f},{BASE} L{mx:.0f},{TOP-4}" stroke="{color}" stroke-width="2" stroke-dasharray="5 4"/>')
    for line, _, _, color, _ in layers:
        b.append(f'<path d="{line}" fill="none" stroke="{color}" stroke-width="2.6"/>')

    mx_m, mx_f = layers[0][2], layers[1][2]

    # 두 평균이 0.41점 차이라 라벨이 겹친다. 위아래로 어긋나게 두고 각각 바깥쪽으로 정렬.
    b.append(f'<text x="{mx_m-6:.0f}" y="{TOP-8}" font-size="14" font-weight="700" fill="{NAVY}" text-anchor="end">남성 3.29</text>')
    b.append(f'<text x="{mx_f+6:.0f}" y="{TOP+14}" font-size="14" font-weight="700" fill="{TEAL}" text-anchor="start">여성 3.70</text>')

    # 평균 차이 표시
    b.append(f'<path d="M{mx_m:.0f},{BASE-8} L{mx_f:.0f},{BASE-8}" stroke="{CORAL}" stroke-width="2.5"/>')
    b.append(f'<text x="{(mx_m+mx_f)/2:.0f}" y="{BASE-16}" font-size="14" font-weight="700" fill="{CORAL}" text-anchor="middle">0.41</text>')

    b.append(f'<text x="{R}" y="{TOP+2}" font-size="13" fill="{FAINT}" text-anchor="end">n = 118 / 122</text>')
    write('distributions.svg', svg(W, H, '\n'.join(b)))


# ---------------------------------------------------------------- 그림 3
def fig_equal_variance():
    """등분산 가정의 의미 — 출발선이 같았는가"""
    W, H = 900, 330
    b = []
    SDS = (0.55, 0.55, 0.42, 1.05)               # 네 곡선의 표준편차
    # 축척 기준은 실제로 그리는 곡선 중 가장 뾰족한 것이어야 한다.
    # 그렇지 않으면 더 좁은 곡선이 상한을 넘어 제목을 침범한다.
    peak = 1 / (min(SDS) * math.sqrt(2 * math.pi))

    def panel(x0, title, sd1, sd2, verdict, vcolor, note):
        x1 = x0 + 410
        b.append(f'<rect x="{x0}" y="0" width="410" height="{H}" rx="10" fill="#FBFCFD" stroke="{RULE}" stroke-width="2"/>')
        b.append(f'<text x="{x0+24}" y="34" font-size="18" font-weight="800" fill="{NAVY}">{title}</text>')
        # 제목 아래로 곡선이 올라오지 않도록 top을 충분히 내린다
        base, top = 228, 78
        px0, px1 = x0 + 30, x1 - 30
        b.append(f'<path d="M{px0},{base} L{px1},{base}" stroke="{MID}" stroke-width="2"/>')

        curves = []
        for mu, sd, color, fill in ((2.4, sd1, NAVY, '#C7D0DE'), (3.8, sd2, TEAL, TEAL_TINT)):
            d = normal_path(mu, sd, 0.6, 5.6, px0, px1, base, base - top, peak)
            curves.append((d, mu, color, fill))
        # 반투명 채움이 다른 곡선의 선을 덮지 않도록 채움을 모두 먼저 그린다
        for d, _, _, fill in curves:
            b.append(f'<path d="{d} L{px1},{base} L{px0},{base} Z" fill="{fill}" opacity=".5"/>')
        for d, mu, color, _ in curves:
            mx = px0 + (px1 - px0) * (mu - 0.6) / 5.0
            b.append(f'<path d="M{mx:.0f},{base} L{mx:.0f},{top+4}" stroke="{color}" stroke-width="1.8" stroke-dasharray="4 4"/>')
            b.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.6"/>')

        b.append(f'<text x="{x0+205}" y="270" font-size="17" font-weight="800" fill="{vcolor}" text-anchor="middle">{verdict}</text>')
        b.append(f'<text x="{x0+205}" y="296" font-size="14" fill="{SOFT}" text-anchor="middle">{note}</text>')

    panel(0, '퍼진 정도가 같다', 0.55, 0.55,
          '출발선이 같았다', TEAL, '평균 차이를 처치의 결과로 볼 수 있다')
    panel(490, '퍼진 정도가 다르다', 0.42, 1.05,
          '출발선이 달랐을 수 있다', CORAL, '평균이 달라도 처치 때문인지 알 수 없다')

    write('equal-variance.svg', svg(W, H, '\n'.join(b)))


# ---------------------------------------------------------------- 그림 4
def fig_normality():
    """정규성 — 평균이 집단을 대표하는가"""
    W, H = 900, 300
    b = []
    base, top = 208, 52

    def panel(x0, title, skew, verdict, vcolor):
        x1 = x0 + 410
        px0, px1 = x0 + 30, x1 - 30
        b.append(f'<rect x="{x0}" y="0" width="410" height="{H}" rx="10" fill="#FBFCFD" stroke="{RULE}" stroke-width="2"/>')
        b.append(f'<text x="{x0+24}" y="32" font-size="18" font-weight="800" fill="{NAVY}">{title}</text>')
        b.append(f'<path d="M{px0},{base} L{px1},{base}" stroke="{MID}" stroke-width="2"/>')

        # 감마꼴로 치우침 표현
        pts, ys = [], []
        n = 100
        for i in range(n + 1):
            t = i / n
            x = 0.02 + t * 6
            if skew:
                k, th = 2.0, 0.9
                y = (x ** (k - 1)) * math.exp(-x / th)
            else:
                y = math.exp(-((x - 3) ** 2) / (2 * 0.9 ** 2))
            ys.append(y)
        mx = max(ys)
        for i, y in enumerate(ys):
            px = px0 + (px1 - px0) * i / n
            py = base - (y / mx) * (base - top)
            pts.append(f'{px:.1f},{py:.1f}')
        line = 'M' + ' L'.join(pts)
        b.append(f'<path d="{line} L{px1},{base} L{px0},{base} Z" fill="{TEAL_TINT}" opacity=".7"/>')
        b.append(f'<path d="{line}" fill="none" stroke="{TEAL}" stroke-width="2.6"/>')

        # 평균/중앙값 위치
        tot = sum(ys); cum = 0; med_i = 0
        for i, y in enumerate(ys):
            cum += y
            if cum >= tot / 2: med_i = i; break
        mean_i = int(sum(i * y for i, y in enumerate(ys)) / tot)
        # 두 선이 거의 붙는 경우가 있어 라벨을 좌우로 갈라 놓는다
        for idx, lab, color, side in ((med_i, '중앙값', NAVY, -1), (mean_i, '평균', CORAL, 1)):
            px = px0 + (px1 - px0) * idx / n
            b.append(f'<path d="M{px:.0f},{base} L{px:.0f},{top}" stroke="{color}" stroke-width="2" stroke-dasharray="5 4"/>')
            anchor = 'end' if side < 0 else 'start'
            b.append(f'<text x="{px + side * 6:.0f}" y="{top-6}" font-size="14" font-weight="700" '
                     f'fill="{color}" text-anchor="{anchor}">{lab}</text>')

        b.append(f'<text x="{x0+205}" y="248" font-size="16" font-weight="800" fill="{vcolor}" text-anchor="middle">{verdict}</text>')

    panel(0, '좌우 대칭이면', False, '평균이 집단을 대표한다', TEAL)
    panel(490, '한쪽으로 치우치면', True, '평균이 대다수를 벗어난다', CORAL)
    b.append(f'<text x="450" y="284" font-size="14" fill="{SOFT}" text-anchor="middle">'
             f't-검정은 각 집단을 평균 하나로 요약해 비교하므로, 평균의 대표성이 곧 비교의 근거가 된다</text>')
    write('normality-mean.svg', svg(W, H, '\n'.join(b)))


# ---------------------------------------------------------------- 그림 5
def fig_ci():
    """신뢰구간이 0을 걸치는가"""
    W, H = 900, 250
    b = []
    L, R = 120, 830
    zero = L + (R - L) * 0.62

    b.append(f'<path d="M{zero},34 L{zero},206" stroke="{MID}" stroke-width="2.5"/>')
    b.append(f'<text x="{zero}" y="228" font-size="15" font-weight="700" fill="{MID}" text-anchor="middle">차이 = 0</text>')

    def band(y, x_lo, x_hi, est, color, label, verdict):
        b.append(f'<path d="M{x_lo},{y} L{x_hi},{y}" stroke="{color}" stroke-width="4" stroke-linecap="round"/>')
        b.append(f'<path d="M{x_lo},{y-11} L{x_lo},{y+11} M{x_hi},{y-11} L{x_hi},{y+11}" stroke="{color}" stroke-width="3"/>')
        b.append(f'<circle cx="{est}" cy="{y}" r="7" fill="{color}"/>')
        b.append(f'<text x="{L-16}" y="{y+6}" font-size="15" font-weight="700" fill="{INK}" text-anchor="end">{label}</text>')
        b.append(f'<text x="{R+8}" y="{y+6}" font-size="15" font-weight="700" fill="{color}">{verdict}</text>')

    band(80, 195, 470, 330, TEAL, '사례 A', 'p < .05')
    band(160, 400, 760, 580, FAINT, '사례 B', 'p > .05')

    b.append(f'<text x="332" y="112" font-size="13.5" fill="{SOFT}" text-anchor="middle">구간이 0을 걸치지 않는다 · 차이가 있다고 판단</text>')
    b.append(f'<text x="580" y="192" font-size="13.5" fill="{SOFT}" text-anchor="middle">구간이 0을 포함한다 · 차이를 확인하지 못함</text>')
    write('ci-zero.svg', svg(W, H, '\n'.join(b)))


# ---------------------------------------------------------------- 그림 6
def fig_t_distribution(td):
    """t분포에서 p값이 무엇인지 — 관측된 t가 어디에 떨어졌는가"""
    W, H = 900, 340
    L, R, BASE, TOP = 60, 860, 250, 46
    b = []
    xs, ys = td['x'], td['y']
    peak = max(ys)
    crit, obs = td['crit'], td['obs']

    def px(x): return L + (R - L) * (x + 4.5) / 9.0
    def py(y): return BASE - (y / peak) * (BASE - TOP)

    # 기각역 채우기
    for lo, hi in ((-4.5, -crit), (crit, 4.5)):
        pts = [f'{px(lo):.1f},{BASE:.1f}']
        for x, y in zip(xs, ys):
            if lo <= x <= hi: pts.append(f'{px(x):.1f},{py(y):.1f}')
        pts.append(f'{px(hi):.1f},{BASE:.1f}')
        b.append(f'<path d="M{" L".join(pts)} Z" fill="{CORAL}" opacity=".22"/>')

    line = 'M' + ' L'.join(f'{px(x):.1f},{py(y):.1f}' for x, y in zip(xs, ys))
    b.append(f'<path d="{line}" fill="none" stroke="{NAVY}" stroke-width="2.6"/>')
    b.append(f'<path d="M{L},{BASE} L{R},{BASE}" stroke="{MID}" stroke-width="2"/>')

    # 임계값
    for c, lab in ((-crit, '−1.97'), (crit, '+1.97')):
        b.append(f'<path d="M{px(c):.0f},{BASE} L{px(c):.0f},{TOP+34}" stroke="{CORAL}" stroke-width="2" stroke-dasharray="5 4"/>')
        b.append(f'<text x="{px(c):.0f}" y="{TOP+26}" font-size="13" font-weight="700" fill="{CORAL}" text-anchor="middle">{lab}</text>')

    # 관측값
    b.append(f'<path d="M{px(obs):.0f},{BASE} L{px(obs):.0f},{TOP}" stroke="{TEAL}" stroke-width="3"/>')
    b.append(f'<circle cx="{px(obs):.0f}" cy="{BASE}" r="6" fill="{TEAL}"/>')
    b.append(f'<text x="{px(obs):.0f}" y="{TOP-8}" font-size="15" font-weight="800" fill="{TEAL}" text-anchor="middle">우리 결과 t = −3.93</text>')

    b.append(f'<text x="{px(0):.0f}" y="{BASE+26}" font-size="14" fill="{SOFT}" text-anchor="middle">0</text>')
    b.append(f'<text x="{(L+R)/2:.0f}" y="{BASE+52}" font-size="14" fill="{SOFT}" text-anchor="middle">t 값 (자유도 238)</text>')

    b.append(f'<text x="{px(-3.2):.0f}" y="{BASE-14}" font-size="13" fill="{CORAL}" text-anchor="middle">기각역 2.5%</text>')
    b.append(f'<text x="{px(3.2):.0f}" y="{BASE-14}" font-size="13" fill="{CORAL}" text-anchor="middle">기각역 2.5%</text>')

    b.append(f'<text x="{(L+R)/2:.0f}" y="{H-8}" font-size="14" fill="{MID}" text-anchor="middle">'
             f'영가설이 참이라면 t는 대부분 가운데에 떨어진다. 우리 결과는 꼬리 밖에 있다.</text>')
    write('t-distribution.svg', svg(W, H, '\n'.join(b)))


# ---------------------------------------------------------------- 그림 7
def fig_sample_size():
    """같은 차이인데 표본만 커지면 유의해진다"""
    W, H = 900, 300
    b = []
    rows = [(20, 0.59, .5567), (50, 0.94, .3508), (100, 1.33, .1864),
            (300, 2.30, .0220), (1000, 4.19, .0001)]
    x0, bw = 190, 480
    xc = x0 + bw * 1.97 / 4.5          # .05 기준선 자리 (라벨 배치에도 쓴다)
    b.append(f'<text x="26" y="30" font-size="17" font-weight="800" fill="{NAVY}">평균 차이 0.15점, 표준편차 0.8로 고정 — 표본크기만 바꿨을 때</text>')

    for i, (n, t, p) in enumerate(rows):
        y = 68 + i * 44
        sig = p < .05
        color = TEAL if sig else FAINT
        b.append(f'<text x="150" y="{y+5}" font-size="15" font-weight="700" fill="{INK}" text-anchor="end">n = {n}</text>')
        w = min(bw, bw * t / 4.5)
        b.append(f'<rect x="{x0}" y="{y-11}" width="{w:.0f}" height="22" rx="4" fill="{color}" opacity=".85"/>')
        # 막대가 기준선에 못 미치면 라벨이 선을 가로지르므로 선 오른쪽으로 민다
        lx = max(x0 + w + 12, xc + 14)
        b.append(f'<text x="{lx:.0f}" y="{y+5}" font-size="14" font-weight="700" fill="{color}">'
                 f'p = {p:.4f}{" ✓ 유의" if sig else ""}</text>')

    # .05 기준선
    b.append(f'<path d="M{xc:.0f},52 L{xc:.0f},{68+len(rows)*44-18}" stroke="{CORAL}" stroke-width="2" stroke-dasharray="5 4"/>')
    b.append(f'<text x="{xc:.0f}" y="44" font-size="13" font-weight="700" fill="{CORAL}" text-anchor="middle">유의성 경계</text>')

    b.append(f'<text x="450" y="{H-12}" font-size="14" fill="{MID}" text-anchor="middle">'
             f'차이의 크기는 그대로다. p값만 작아진다. 그래서 효과크기를 따로 본다.</text>')
    write('sample-size-p.svg', svg(W, H, '\n'.join(b)))


# ---------------------------------------------------------------- 그림 8
def fig_effect_size():
    """Cohen's d가 얼마나 겹치는지"""
    W, H = 900, 300
    b = []
    peak = 1 / math.sqrt(2 * math.pi)
    panels = [(0, 0.2, '작은 효과', False), (305, 0.5, '중간 효과', True), (610, 0.8, '큰 효과', False)]
    for x0, d, lab, ours in panels:
        w = 290
        stroke = TEAL if ours else RULE
        sw = 3 if ours else 2
        b.append(f'<rect x="{x0}" y="0" width="{w}" height="{H-40}" rx="10" fill="#FBFCFD" stroke="{stroke}" stroke-width="{sw}"/>')
        base, top = 190, 62
        px0, px1 = x0 + 22, x0 + w - 22
        b.append(f'<path d="M{px0},{base} L{px1},{base}" stroke="{MID}" stroke-width="2"/>')
        for mu, color, fill in ((-d/2, NAVY, '#C7D0DE'), (d/2, TEAL, TEAL_TINT)):
            pth = normal_path(mu, 1.0, -3.4, 3.4, px0, px1, base, base - top, peak)
            b.append(f'<path d="{pth} L{px1},{base} L{px0},{base} Z" fill="{fill}" opacity=".5"/>')
            b.append(f'<path d="{pth}" fill="none" stroke="{color}" stroke-width="2.4"/>')
        b.append(f'<text x="{x0+w/2:.0f}" y="{base+34}" font-size="17" font-weight="800" fill="{INK}" text-anchor="middle">d = {d}</text>')
        b.append(f'<text x="{x0+w/2:.0f}" y="{base+56}" font-size="14" fill="{SOFT}" text-anchor="middle">{lab}</text>')
        if ours:
            b.append(f'<rect x="{x0+w/2-58:.0f}" y="22" width="116" height="26" rx="13" fill="{TEAL}"/>')
            b.append(f'<text x="{x0+w/2:.0f}" y="40" font-size="13" font-weight="800" fill="#fff" text-anchor="middle">우리 결과 0.51</text>')

    b.append(f'<text x="450" y="{H-10}" font-size="14" fill="{MID}" text-anchor="middle">'
             f'd가 커질수록 두 분포가 덜 겹친다. 겹침이 적을수록 두 집단이 실질적으로 다르다는 뜻이다.</text>')
    write('effect-size.svg', svg(W, H, '\n'.join(b)))


if __name__ == '__main__':
    dens_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'tools', 'dens.json')
    print('그림 생성')
    fig_two_questions()
    fig_equal_variance()
    fig_normality()
    fig_ci()
    fig_sample_size()
    fig_effect_size()
    td_path = os.path.join(ROOT, 'tools', 'tdist.json')
    if os.path.exists(td_path):
        fig_t_distribution(json.load(open(td_path, encoding='utf-8')))
    else:
        print('  ! tools/tdist.json 없음 — t분포 그림은 건너뜀 (tools/tdist.R 실행 필요)')
    if os.path.exists(dens_path):
        fig_distributions(json.load(open(dens_path, encoding='utf-8')))
    else:
        print(f'  ! {dens_path} 없음 — 분포 그림은 건너뜀 (tools/densities.R 실행 필요)')
    print('완료')
