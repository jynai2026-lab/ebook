"""2권 0~3장 그림"""
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


ALL = [fig_research_model]
