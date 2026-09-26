---
part: 기초통계
partNum: PART 1
num: 01
title: 척도가 분석을 결정한다
lead: 통계 학습에서 가장 먼저 다루어야 할 것은 개별 분석 기법이 아니라 변수의 척도를 판별하는 절차입니다. 척도가 확정되면 쓸 수 있는 분석이 사실상 하나로 좁혀집니다.
---

## 척도를 먼저 다루는 이유

어떤 분석을 적용해야 하는가라는 질문에는 대체로 정해진 답이 있습니다. **변수의 척도가 확정되면 쓸 수 있는 분석이 거의 하나로 좁혀지기 때문입니다.**

분석 방법을 선택하지 못하는 원인은 통계 지식의 부족이 아니라 **변수의 척도를 판별하지 못하는 데** 있습니다. 이 장은 그 판별 절차를 다룹니다.

## 네 가지 척도

| 척도 | 정의 | 예시 | 평균 산출 |
| --- | --- | --- | --- |
| **명목척도** | 범주를 구분할 뿐 순서가 없음 | 성별, 전공, 지역 | 불가 |
| **서열척도** | 순서는 있으나 간격이 균등하지 않음 | 학력, 직급, 선호 순위 | 원칙상 불가 |
| **등간척도** | 간격이 균등하나 절대영점이 없음 | 온도, 리커트 척도 | 가능 |
| **비율척도** | 간격이 균등하고 절대영점이 있음 | 연령, 소득, 시간 | 가능 |

분석 방법을 선택하는 데에는 네 가지 구분을 모두 적용할 필요가 없으며, **두 범주로 축약하면 충분합니다.**

:::key 분석 선택을 위한 이분법
- **범주형** = 명목 + 서열 — 각 범주에 몇 사례가 속하는지를 세는 변수
- **연속형** = 등간 + 비율 — 값의 크기를 측정하는 변수

분석 선택에 필요한 구분은 이것으로 충분합니다. 명목과 서열의 구분은 대부분의 경우 분석 결과에 영향을 주지 않습니다.
:::

:::warn 리커트 척도의 처리
"매우 그렇다(5)~전혀 아니다(1)" 형식은 엄밀하게는 서열척도입니다. 4점과 5점의 간격이 1점과 2점의 간격과 동일하다는 보장이 없기 때문입니다.

그러나 **복수의 리커트 문항을 합산하거나 평균한 값을 등간척도로 취급하는 것이 사회과학의 표준 관행**이며, 이 처리가 심사에서 문제가 되는 경우는 드뭅니다.

다만 단일 문항의 값을 등간척도로 취급하는 것은 정당화하기 어렵습니다. 최소 3문항 이상을 합산하여 사용합니다.
:::

## 분석 선택 흐름도

이 도식은 1권 전체의 구조를 요약한 것입니다. 분석 선택에 확신이 서지 않을 때 참조합니다.

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

## R에 척도를 지정하는 절차

성별 변수에 `1`과 `2`가 입력되어 있으면 사람은 이를 범주 구분으로 인식하지만, **R은 그렇지 않습니다.** 숫자로 저장된 변수는 모두 연속형으로 처리하므로, 성별의 평균이 1.47이라는 무의미한 값이 산출됩니다.

따라서 자료를 불러온 직후 **범주형 변수를 `factor`로 변환하는 절차**가 반드시 선행되어야 합니다.

```r 자료를 불러온 직후 수행합니다
df <- read.csv("data.csv")

# 범주형 변수를 factor로 변환 + 라벨 붙이기
df$gender <- factor(df$gender, levels = c(1, 2), labels = c("남성", "여성"))
df$group  <- factor(df$group,  levels = c(1, 2, 3), labels = c("통제", "처치A", "처치B"))

str(df)   # 변수별 척도가 의도대로 지정되었는지 확인
```

```out str(df) 출력
'data.frame':	240 obs. of  4 variables:
 $ gender    : Factor w/ 2 levels "남성","여성": 1 2 2 1 1 2 ...
 $ group     : Factor w/ 3 levels "통제","처치A",..: 1 1 2 3 2 3 ...
 $ age       : int  23 21 25 22 24 27 ...
 $ selfesteem: num  3.42 4.10 2.85 3.97 3.20 ...
```

출력에서 `Factor w/ 2 levels`로 표시되면 **범주형으로 지정된 것**이고, `int` 또는 `num`이면 **연속형으로 지정된 것**입니다. 그림 1-1의 분기가 이 단계에서 결정됩니다.

:::warn 탐지되지 않는 오류
`gender`를 factor로 변환하지 않은 상태에서 t-검정을 수행하면 **오류 메시지 없이 잘못된 결과가 나옵니다.** 오류가 발생하지 않으므로 발견이 더 어렵습니다. 분석 전에 `str(df)`로 척도 지정을 확인하는 습관을 들여야 합니다.
:::

## 보고 방법

척도의 구분은 논문의 측정도구 절에 반영됩니다.

:::paper 측정도구 절 기술 예시
> 본 연구의 종속변수인 자아존중감은 Rosenberg(1965)의 척도 10문항을 5점 리커트 척도(1=전혀 아니다, 5=매우 그렇다)로 측정하였으며, 문항 평균을 분석에 사용하였다. 독립변수인 집단은 통제집단, 처치A, 처치B의 세 수준으로 구성된 명목변수이다.

여기서 **문항 평균을 사용하였다**는 기술이 해당 변수를 연속형으로 처리하겠다는 선언에 해당합니다. 이 진술이 있어야 이후 분산분산분석을 쓰는 것이 정당해집니다.
:::

:::check 점검 항목
- 종속변수가 연속형인지 범주형인지 판별할 수 있다
- 범주형 변수를 `factor()`로 변환했다
- `str(df)`로 척도 지정을 확인했다
- 그림 1-1에서 내가 쓸 분석이 어디인지 짚을 수 있다
:::

:::recap
**요약** — 척도가 확정되면 분석이 특정됩니다. 종속변수가 연속형이면 평균 비교(t-검정·분산분석), 범주형이면 빈도 비교(카이제곱 검정)로 진행합니다. 검토해야 할 것은 분석 기법이 아니라 변수의 척도입니다.
:::
