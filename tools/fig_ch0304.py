"""3장 분포 · 4장 표집분포와 중심극한정리"""
import json, math, os, random
from figlib import *


# ================================================================ 3장
def fig_normal_anatomy():
    """정규분포는 두 숫자로 완전히 결정된다"""
    W, H = 900, 348
    b = []
    px0, px1, base, top = 70, 830, 224, 58
    sx = scale(-6, 6, px0, px1)
    specs = [(0, 1.0, NAVY, r'M = 0,\; SD = 1'), (0, 1.8, TEAL, r'M = 0,\; SD = 1.8'),
             (2.4, 1.0, CORAL, r'M = 2.4,\; SD = 1')]
    allpts = [(mu, sd, c, lab, normal_pts(mu, sd, -6, 6, 120)) for mu, sd, c, lab in specs]
    peak = max(y for *_, pts in allpts for _, y in pts)

    for i, (mu, sd, c, lab, pts) in enumerate(allpts):
        line, _ = curve_paths(pts, sx, base, top, peak)
        b.append(f'<path d="{line}" fill="none" stroke="{c}" stroke-width="2.6"/>')
        b.append(f'<rect x="{112 + i*250}" y="{H-40}" width="14" height="14" rx="3" fill="{c}"/>')
        b.append(tex(134 + i * 250, H - 33, lab, 14.5, INK, 'start', w=210))

    b.append(axis(px0, px1, base))
    b.append(text(px0 + 6, top + 4, '평균이 위치를, 표준편차가 폭을 정한다', 15, SOFT))
    b.append(caption(450, base + 42, '두 숫자만 알면 곡선의 모든 지점이 결정된다. 그래서 M과 SD만 보고해도 분포를 복원할 수 있다', 14))
    write('ch03-normal-anatomy.svg', svg(W, H, '\n'.join(b)))


def fig_skew():
    """왜도 — 어느 쪽으로 꼬리가 길게 늘어졌나"""
    W, H = 900, 290
    b = []
    panels = [(0, '정적편포 (왜도 > 0)', 'right', '소득, 반응시간'),
              (305, '대칭 (왜도 ≈ 0)', 'sym', '키, 시험점수'),
              (610, '부적편포 (왜도 < 0)', 'left', '쉬운 시험, 만족도')]
    for x0, title, kind, ex in panels:
        w = 290
        b.append(panel(x0, 0, w, H - 46))
        b.append(text(x0 + w / 2, 32, title, 15, NAVY, 800, 'middle'))
        px0, px1, base, top = x0 + 24, x0 + w - 24, 190, 66
        ys, pts = [], []
        for i in range(101):
            t = i / 100
            x = 0.02 + t * 6
            if kind == 'sym':
                y = math.exp(-((x - 3) ** 2) / (2 * 0.95 ** 2))
            else:
                y = (x ** 1.7) * math.exp(-x / 0.85)
            pts.append((x, y)); ys.append(y)
        if kind == 'left':
            pts = [(6.02 - x, y) for x, y in pts][::-1]
        peak = max(ys)
        sx = scale(0, 6.02, px0, px1)
        line, area = curve_paths(pts, sx, base, top, peak)
        b.append(f'<path d="{area}" fill="{TEAL_TINT}" opacity=".7"/>')
        b.append(f'<path d="{line}" fill="none" stroke="{TEAL}" stroke-width="2.5"/>')
        b.append(axis(px0, px1, base))
        b.append(text(x0 + w / 2, base + 26, f'예: {ex}', 13, SOFT, None, 'middle'))
    b.append(caption(450, H - 14, '왜도의 부호는 꼬리가 길게 늘어진 쪽을 가리킨다. 절댓값이 2를 넘으면 정규성을 의심한다', 14))
    write('ch03-skew.svg', svg(W, H, '\n'.join(b)))


def fig_kurtosis():
    """첨도 — 가운데가 얼마나 뾰족한가"""
    W, H = 900, 300
    b = []
    px0, px1, base, top = 90, 810, 218, 56
    sx = scale(-4.2, 4.2, px0, px1)
    specs = [(0.62, CORAL, '뾰족 (첨도 > 0)', '가운데에 몰리고 꼬리가 두껍다'),
             (1.00, NAVY, '정규분포 (첨도 = 0)', '기준'),
             (1.55, TEAL, '평평 (첨도 < 0)', '고르게 퍼져 있다')]
    allp = [(sd, c, t, n, normal_pts(0, sd, -4.2, 4.2, 130)) for sd, c, t, n in specs]
    peak = max(y for *_, pts in allp for _, y in pts)
    for sd, c, t, n, pts in allp:
        line, _ = curve_paths(pts, sx, base, top, peak)
        b.append(f'<path d="{line}" fill="none" stroke="{c}" stroke-width="2.6"/>')
    b.append(axis(px0, px1, base))
    for i, (sd, c, t, n, _) in enumerate(allp):
        y = base + 32 + i * 24
        b.append(f'<rect x="{px0}" y="{y-11}" width="13" height="13" rx="3" fill="{c}"/>')
        b.append(text(px0 + 22, y, t, 14, INK, 700))
        b.append(text(px0 + 190, y, n, 13.5, SOFT))
    b.append(caption(450, H - 10, '첨도가 크면 평균 근처와 극단값이 동시에 늘어난다. 절댓값 7을 넘으면 문제로 본다', 14))
    write('ch03-kurtosis.svg', svg(W, H, '\n'.join(b)))


# ================================================================ 4장
def fig_clt(clt):
    """중심극한정리 — 원자료가 치우쳐도 표본평균은 정규분포로"""
    W, H = 900, 320
    b = []
    panels = [('pop', 0, '원자료 하나하나', '지수분포 · 심하게 치우침', 0, 5),
              ('n5', 305, '5명씩 뽑은 평균', '벌써 대칭에 가까워진다', 0, 3),
              ('n30', 610, '30명씩 뽑은 평균', '정규분포에 근사한다', 0, 3)]
    for key, x0, title, note, lo, hi in panels:
        w = 290
        d = clt[key]
        ours = key == 'n30'
        b.append(panel(x0, 0, w, H - 62, stroke=(TEAL if ours else RULE), sw=3 if ours else 2))
        b.append(text(x0 + w / 2, 32, title, 15, NAVY, 800, 'middle'))
        px0, px1, base, top = x0 + 24, x0 + w - 24, 196, 62
        pts = list(zip(d['x'], d['y']))
        peak = max(d['y'])
        sx = scale(lo, hi, px0, px1)
        line, area = curve_paths(pts, sx, base, top, peak)
        b.append(f'<path d="{area}" fill="{TEAL_TINT}" opacity=".7"/>')
        b.append(f'<path d="{line}" fill="none" stroke="{TEAL}" stroke-width="2.5"/>')
        b.append(axis(px0, px1, base))
        b.append(text(x0 + w / 2, base + 26, note, 13, SOFT, None, 'middle'))
        b.append(text(x0 + w / 2, base + 48, f"왜도 {d['skew']:.2f}  ·  표준편차 {d['sd']:.2f}",
                      13.5, INK, 700, 'middle'))
    b.append(caption(450, H - 30, '모집단이 아무리 치우쳐 있어도, 표본크기가 커지면 표본평균의 분포는 정규분포로 간다', 15, INK))
    b.append(caption(450, H - 8, '표본을 많이 뽑는 것이 아니라, 표본 하나의 크기 n이 커져야 한다', 14))
    write('ch04-clt.svg', svg(W, H, '\n'.join(b)))


def fig_sampling_concept():
    """표집분포는 점수의 분포가 아니라 통계치의 분포"""
    W, H = 900, 330
    b = []
    b.append(panel(0, 0, 250, 250))
    b.append(text(125, 32, '모집단', 17, NAVY, 800, 'middle'))
    random.seed(5)
    for _ in range(60):
        b.append(f'<circle cx="{random.uniform(30,220):.0f}" cy="{random.uniform(60,220):.0f}" r="4" fill="{FAINT}" opacity=".7"/>')
    b.append(text(125, 238, '우리는 여기를 알고 싶다', 13, SOFT, None, 'middle'))

    for i in range(3):
        y = 62 + i * 62
        b.append(f'<path d="M258,{y+16} L316,{y+16}" stroke="{RULE}" stroke-width="2"/>')
        b.append(f'<rect x="320" y="{y}" width="128" height="34" rx="7" fill="{PAPER}" stroke="{TEAL}" stroke-width="2"/>')
        b.append(text(384, y + 22, f'표본 {i+1} → M', 13.5, TEAL, 700, 'middle'))
    b.append(text(384, 258, '표본을 무한히 반복해서 뽑는다면', 13, SOFT, None, 'middle'))
    b.append(text(384, 278, '(실제로는 상상만 한다)', 13, FAINT, None, 'middle'))

    px0, px1, base, top = 490, 880, 214, 62
    sx = scale(-3.4, 3.4, px0, px1)
    pts = normal_pts(0, 1, -3.4, 3.4, 120)
    peak = max(y for _, y in pts)
    line, area = curve_paths(pts, sx, base, top, peak)
    b.append(f'<path d="{area}" fill="{TEAL_TINT}" opacity=".7"/>')
    b.append(f'<path d="{line}" fill="none" stroke="{TEAL}" stroke-width="2.6"/>')
    b.append(axis(px0, px1, base))
    b.append(text((px0 + px1) / 2, 34, '표집분포', 17, NAVY, 800, 'middle'))
    b.append(text((px0 + px1) / 2, base + 26, '표본평균 M들이 이루는 분포', 13.5, SOFT, None, 'middle'))
    b.append(caption(450, H - 34, '표집분포는 사람들의 점수가 모인 분포가 아니라, 표본평균이라는 통계치가 모인 분포다', 15, INK))
    b.append(caption(450, H - 10, '실제로 그려본 적은 없지만, 그 모양을 알기 때문에 추론이 가능해진다', 14))
    write('ch04-sampling-concept.svg', svg(W, H, '\n'.join(b)))


def fig_se_shrink():
    """표본이 커지면 표집분포가 좁아진다"""
    W, H = 900, 340
    b = []
    px0, px1, base, top = 80, 820, 216, 54
    sx = scale(-1.2, 1.2, px0, px1)
    specs = [(25, 0.1668, FAINT), (100, 0.0834, TEAL_LINE), (400, 0.0417, TEAL)]
    allp = [(n, se, c, normal_pts(0, se, -1.2, 1.2, 200)) for n, se, c in specs]
    peak = max(y for *_, pts in allp for _, y in pts)
    for n, se, c, pts in allp:
        line, _ = curve_paths(pts, sx, base, top, peak)
        b.append(f'<path d="{line}" fill="none" stroke="{c}" stroke-width="2.8"/>')
    b.append(axis(px0, px1, base))
    for i, (n, se, c, _) in enumerate(allp):
        y = base + 34 + i * 24
        b.append(f'<rect x="{px0+130}" y="{y-11}" width="13" height="13" rx="3" fill="{c}"/>')
        b.append(text(px0 + 152, y, f'n = {n}', 14, INK, 700))
        b.append(text(px0 + 236, y, f'표준오차 {se:.4f}', 14, SOFT))
    b.append(text(px0, top + 4, 'SD는 그대로 0.83인데, 표본평균의 흔들림만 줄어든다', 14.5, SOFT))
    b.append(caption(450, H - 12, '표본이 4배가 되면 표준오차는 절반이 된다. 제곱근이 붙어 있기 때문이다', 14))
    write('ch04-se-shrink.svg', svg(W, H, '\n'.join(b)))


def fig_sd_vs_se():
    """표준편차와 표준오차는 다른 것을 잰다"""
    W, H = 900, 270
    b = []
    for x0, title, subject, note, color in (
        (0, '표준편차 (SD)', '사람들이 서로 얼마나 다른가', '자료 자체의 성질 · 표본이 커져도 줄지 않는다', NAVY),
        (470, '표준오차 (SE)', '내 평균이 얼마나 못 미더운가', '추정의 정밀도 · 표본이 커지면 줄어든다', TEAL),
    ):
        b.append(panel(x0, 0, 430, H - 46, stroke=color, sw=2.5))
        b.append(text(x0 + 215, 40, title, 19, color, 800, 'middle'))
        b.append(text(x0 + 215, 78, subject, 16, INK, 700, 'middle'))
        b.append(text(x0 + 215, 114, note, 13.5, SOFT, None, 'middle'))
        b.append(tex(x0 + 215, 168, 'SD' if color == NAVY else r'SE = \dfrac{SD}{\sqrt{n}}',
                     19, color, 'middle', w=260))
    b.append(caption(450, H - 12, '논문 표에 SD를 쓸지 SE를 쓸지는 무엇을 말하려는지에 달렸다', 14))
    write('ch04-sd-vs-se.svg', svg(W, H, '\n'.join(b)))


def load(name):
    p = os.path.join(ROOT, 'tools', name)
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None


def run():
    fig_normal_anatomy(); fig_skew(); fig_kurtosis()
    fig_sampling_concept(); fig_se_shrink(); fig_sd_vs_se()
    clt = load('clt.json')
    if clt: fig_clt(clt)
    else: print('  ! tools/clt.json 없음 — 중심극한정리 그림 건너뜀')


ALL = [run]
