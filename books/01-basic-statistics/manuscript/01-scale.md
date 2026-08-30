---
part: 기초통계
partNum: PART 1
num: 01
title: 척도가 분석을 결정한다
lead: 통계에서 가장 먼저 배워야 할 것은 t-검정도 회귀분석도 아닙니다. 내 변수가 어떤 종류인지 판별하는 것입니다. 이것만 되면 분석 방법은 자동으로 정해집니다.
---

## 왜 척도부터인가

"어떤 분석을 써야 하나요?"라는 질문에는 사실 정답이 정해져 있습니다. **변수의 척도가 결정되면 쓸 수 있는 분석이 거의 하나로 좁혀지기 때문입니다.**

바꿔 말하면, 분석 방법을 고르지 못하는 이유는 통계를 몰라서가 아니라 **내 변수가 무슨 척도인지 판별하지 못해서**입니다. 이 장 하나면 그 문제가 해결됩니다.

## 네 가지 척도

| 척도 | 뜻 | 예시 | 평균을 낼 수 있나 |
| --- | --- | --- | --- |
| **명목척도** | 이름표일 뿐, 순서 없음 | 성별, 전공, 지역 | ✗ |
| **서열척도** | 순서는 있으나 간격이 불균등 | 학력, 직급, 선호 순위 | ✗ (원칙상) |
| **등간척도** | 간격이 일정, 절대 0 없음 | 온도, 리커트 척도 | ○ |
| **비율척도** | 간격 일정 + 절대 0 있음 | 나이, 소득, 시간 | ○ |

실무에서는 이 네 가지를 그대로 외울 필요가 없습니다. **딱 두 덩어리로만 나누면 됩니다.**

:::key 실무용 2분법
- **범주형** = 명목 + 서열 → "몇 명이 어디에 속하는가"를 세는 변수
- **연속형** = 등간 + 비율 → "얼마나 높은가"를 재는 변수

분석을 고를 때 필요한 구분은 이것뿐입니다. 명목인지 서열인지는 대부분의 경우 결과를 바꾸지 않습니다.
:::

:::warn 리커트 척도는 등간인가, 서열인가
"매우 그렇다(5) ~ 전혀 아니다(1)"는 엄밀히 말하면 서열척도입니다. 4점과 5점의 간격이 1점과 2점의 간격과 같다는 보장이 없기 때문입니다.

그러나 **사회과학 논문에서는 리커트 문항 여러 개를 합산하거나 평균 낸 값을 등간척도로 취급하는 것이 표준 관행**입니다. 심사에서 지적받는 일은 거의 없습니다. 단, 문항 **하나만** 쓰면서 평균을 내는 것은 위험합니다. 최소 3문항 이상을 묶으세요.
:::

## 분석 방법 결정 흐름도

이 그림 한 장이 1권 전체의 지도입니다. 막힐 때마다 여기로 돌아오세요.

```svg
<figure>
<svg viewBox="0 0 640 292" width="100%" font-family="Pretendard, sans-serif">
  <defs>
    <style>
      .bx  { fill:#fff; stroke:#A8D5DE; stroke-width:1.2; }
      .ln  { stroke:#A8D5DE; stroke-width:1.2; fill:none; }
      .t   { fill:#344054; font-size:10px; }
      .tb  { fill:#16243F; font-size:10.5px; font-weight:700; }
      .tw  { fill:#fff; font-size:11px; font-weight:700; }
      .ts  { fill:#98A2B3; font-size:8.5px; }
      .res { fill:#0E7490; }
      .top { fill:#16243F; }
    </style>
  </defs>

  <rect class="bx top" x="220" y="6"  width="200" height="32" rx="6"/>
  <text class="tw" x="320" y="26" text-anchor="middle">종속변수(결과)의 척도는?</text>

  <path class="ln" d="M320,38 L320,56 M235,56 L560,56 M235,56 L235,72 M560,56 L560,72"/>

  <rect class="bx" x="140" y="72" width="190" height="42" rx="6"/>
  <text class="tb" x="235" y="90"  text-anchor="middle">연속형 (등간·비율)</text>
  <text class="ts" x="235" y="104" text-anchor="middle">시험점수, 소득, 만족도 평균</text>

  <rect class="bx" x="482" y="72" width="150" height="42" rx="6"/>
  <text class="tb" x="557" y="90"  text-anchor="middle">범주형 (명목·서열)</text>
  <text class="ts" x="557" y="104" text-anchor="middle">찬반, 합격 여부</text>

  <path class="ln" d="M235,114 L235,132 M80,132 L390,132 M80,132 L80,150 M235,132 L235,150 M390,132 L390,150 M557,114 L557,150"/>

  <rect class="bx" x="12"  y="150" width="136" height="44" rx="6"/>
  <text class="t" x="80"  y="169" text-anchor="middle">독립변수가</text>
  <text class="t" x="80"  y="183" text-anchor="middle">범주형 · 2개 집단</text>

  <rect class="bx" x="167" y="150" width="136" height="44" rx="6"/>
  <text class="t" x="235" y="169" text-anchor="middle">독립변수가</text>
  <text class="t" x="235" y="183" text-anchor="middle">범주형 · 3개 집단 이상</text>

  <rect class="bx" x="322" y="150" width="136" height="44" rx="6"/>
  <text class="t" x="390" y="169" text-anchor="middle">독립변수가</text>
  <text class="t" x="390" y="183" text-anchor="middle">연속형</text>

  <rect class="bx" x="489" y="150" width="136" height="44" rx="6"/>
  <text class="t" x="557" y="169" text-anchor="middle">독립변수가</text>
  <text class="t" x="557" y="183" text-anchor="middle">범주형</text>

  <path class="ln" d="M80,194 L80,212 M235,194 L235,212 M390,194 L390,212 M557,194 L557,212"/>

  <rect class="bx res" x="12"  y="212" width="136" height="36" rx="6"/>
  <text class="tw" x="80"  y="234" text-anchor="middle">독립표본 t-검정</text>
  <rect class="bx res" x="167" y="212" width="136" height="36" rx="6"/>
  <text class="tw" x="235" y="234" text-anchor="middle">일원배치 분산분석</text>
  <rect class="bx res" x="322" y="212" width="136" height="36" rx="6"/>
  <text class="tw" x="390" y="234" text-anchor="middle">상관분석</text>
  <rect class="bx res" x="489" y="212" width="136" height="36" rx="6"/>
  <text class="tw" x="557" y="234" text-anchor="middle">카이제곱 검정</text>

  <text class="ts" x="390" y="266" text-anchor="middle">→ 영향력 크기까지 보려면 회귀분석 (2권)</text>
  <text class="ts" x="557" y="266" text-anchor="middle">→ 예측까지 하려면 로지스틱 회귀 (2권)</text>
</svg>
<figcaption><b>그림 1-1</b> 척도로 분석 방법을 결정하는 흐름. 1권에서는 아래 네 가지를 다룹니다.</figcaption>
</figure>
```

## R에게 척도를 알려주기

사람은 성별 변수에 `1`, `2`가 들어 있으면 그게 남녀 구분이라는 걸 압니다. **R은 모릅니다.** 숫자로 저장되어 있으면 무조건 연속형으로 취급해서, 성별의 평균이 1.47이라는 무의미한 값을 계산해 버립니다.

그래서 데이터를 불러온 직후에 **범주형 변수를 `factor`로 바꿔주는 작업**이 반드시 필요합니다.

```r 데이터를 불러온 직후 항상 하는 일
df <- read.csv("data.csv")

# 범주형 변수를 factor로 변환 + 라벨 붙이기
df$gender <- factor(df$gender, levels = c(1, 2), labels = c("남성", "여성"))
df$group  <- factor(df$group,  levels = c(1, 2, 3), labels = c("통제", "처치A", "처치B"))

str(df)   # 변수별 척도가 제대로 잡혔는지 확인
```

```out str(df) 출력
'data.frame':	240 obs. of  4 variables:
 $ gender    : Factor w/ 2 levels "남성","여성": 1 2 2 1 1 2 ...
 $ group     : Factor w/ 3 levels "통제","처치A",..: 1 1 2 3 2 3 ...
 $ age       : int  23 21 25 22 24 27 ...
 $ selfesteem: num  3.42 4.10 2.85 3.97 3.20 ...
```

읽는 법은 간단합니다. `Factor w/ 2 levels`라고 나오면 **범주형으로 잘 잡힌 것**이고, `int`나 `num`이면 **연속형으로 잡힌 것**입니다. 그림 1-1의 갈림길이 여기서 결정됩니다.

:::warn 가장 흔한 사고
`gender`를 factor로 바꾸지 않은 채 t-검정을 돌리면 오류 없이 **엉뚱한 결과가 그냥 나옵니다.** 오류가 안 나기 때문에 발견하기가 더 어렵습니다. 분석 전에 `str(df)`를 습관처럼 찍어보세요.
:::

## 논문에 이렇게 씁니다

척도 구분은 논문의 '측정도구' 절에 반영됩니다.

:::paper 측정도구 절 서술 예시
> 본 연구의 종속변수인 자아존중감은 Rosenberg(1965)의 척도 10문항을 5점 리커트 척도(1=전혀 아니다, 5=매우 그렇다)로 측정하였으며, 문항 평균을 분석에 사용하였다. 독립변수인 집단은 통제집단, 처치A, 처치B의 세 수준으로 구성된 명목변수이다.

여기서 **"문항 평균을 사용하였다"**는 한 문장이 "이 변수를 연속형으로 다루겠다"는 선언입니다. 이 문장이 있어야 뒤에서 분산분석을 쓰는 것이 정당화됩니다.
:::

:::check 다음 장으로 넘어가기 전 확인
- 내 종속변수가 연속형인지 범주형인지 말할 수 있다
- 범주형 변수를 `factor()`로 변환했다
- `str(df)`로 척도가 의도대로 잡혔는지 확인했다
- 그림 1-1에서 내가 쓸 분석이 어디에 있는지 짚을 수 있다
:::

:::recap
**이 장의 한 줄** — 척도를 판별하면 분석이 정해진다. 연속형이면 평균 비교(t-검정·분산분석), 범주형이면 빈도 비교(카이제곱). <b>고민할 것은 방법이 아니라 척도다.</b>
:::
