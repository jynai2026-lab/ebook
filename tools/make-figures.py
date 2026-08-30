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

    def curve(key, color, fill):
        d = dens[key]
        pts = []
        for x, y in zip(d['x'], d['y']):
            px = L + (R - L) * (x - 1) / 4.2
            py = BASE - (y / peak) * (BASE - TOP)
            pts.append(f'{px:.1f},{py:.1f}')
        line = 'M' + ' L'.join(pts)
        area = line + f' L{L + (R-L)*(d["x"][-1]-1)/4.2:.1f},{BASE} L{L + (R-L)*(d["x"][0]-1)/4.2:.1f},{BASE} Z'
        b.append(f'<path d="{area}" fill="{fill}" opacity=".55"/>')
        b.append(f'<path d="{line}" fill="none" stroke="{color}" stroke-width="2.6"/>')
        mx = L + (R - L) * (d['mean'] - 1) / 4.2
        b.append(f'<path d="M{mx:.0f},{BASE} L{mx:.0f},{TOP-4}" stroke="{color}" stroke-width="2" stroke-dasharray="5 4"/>')
        return mx

    mx_m = curve('male', NAVY, '#C7D0DE')
    mx_f = curve('female', TEAL, TEAL_TINT)

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
    peak = 1 / (0.55 * math.sqrt(2 * math.pi))   # 가장 뾰족한 곡선 기준

    def panel(x0, title, sd1, sd2, verdict, vcolor, note):
        x1 = x0 + 410
        b.append(f'<rect x="{x0}" y="0" width="410" height="{H}" rx="10" fill="#FBFCFD" stroke="{RULE}" stroke-width="2"/>')
        b.append(f'<text x="{x0+24}" y="34" font-size="18" font-weight="800" fill="{NAVY}">{title}</text>')
        base, top = 224, 62
        px0, px1 = x0 + 30, x1 - 30
        b.append(f'<path d="M{px0},{base} L{px1},{base}" stroke="{MID}" stroke-width="2"/>')
        for mu, sd, color, fill in ((2.4, sd1, NAVY, '#C7D0DE'), (3.8, sd2, TEAL, TEAL_TINT)):
            d = normal_path(mu, sd, 0.6, 5.6, px0, px1, base, base - top, peak)
            b.append(f'<path d="{d} L{px1},{base} L{px0},{base} Z" fill="{fill}" opacity=".5"/>')
            b.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.6"/>')
            mx = px0 + (px1 - px0) * (mu - 0.6) / 5.0
            b.append(f'<path d="M{mx:.0f},{base} L{mx:.0f},{top+4}" stroke="{color}" stroke-width="1.8" stroke-dasharray="4 4"/>')
        b.append(f'<text x="{x0+205}" y="266" font-size="17" font-weight="800" fill="{vcolor}" text-anchor="middle">{verdict}</text>')
        b.append(f'<text x="{x0+205}" y="294" font-size="14" fill="{SOFT}" text-anchor="middle">{note}</text>')

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
        for idx, lab, color in ((mean_i, '평균', CORAL), (med_i, '중앙값', NAVY)):
            px = px0 + (px1 - px0) * idx / n
            b.append(f'<path d="M{px:.0f},{base} L{px:.0f},{top}" stroke="{color}" stroke-width="2" stroke-dasharray="5 4"/>')
            dy = 0 if lab == '평균' else 20
            b.append(f'<text x="{px:.0f}" y="{top-6+dy if lab=="평균" else top+14}" font-size="14" font-weight="700" fill="{color}" text-anchor="middle">{lab}</text>')

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


if __name__ == '__main__':
    dens_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'tools', 'dens.json')
    print('그림 생성')
    fig_two_questions()
    fig_equal_variance()
    fig_normality()
    fig_ci()
    if os.path.exists(dens_path):
        fig_distributions(json.load(open(dens_path, encoding='utf-8')))
    else:
        print(f'  ! {dens_path} 없음 — 분포 그림은 건너뜀 (tools/densities.R 실행 필요)')
    print('완료')
