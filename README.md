# 사회과학 통계 입문 시리즈 — 전자책

R 기반 사회과학 통계 입문서 4권 시리즈. 원고(Markdown)를 A4 PDF로 빌드합니다.

## 구성

| 권 | 주제 | 디렉터리 |
| --- | --- | --- |
| 1권 | 기초통계 | `books/01-basic-statistics/` |
| 2권 | 회귀분석 | `books/02-regression/` |
| 3권 | 요인분석 | `books/03-factor-analysis/` |
| 4권 | 구조방정식 | `books/04-sem/` |

## 내 PC에서 돌리기

macOS · Windows · Linux 모두 됩니다.

**필요한 것**

| 도구 | 용도 | 설치 |
| --- | --- | --- |
| Node.js 18 이상 | 모든 빌드 | nodejs.org |
| Google Chrome | PDF·이미지·영상 렌더 | 평소 쓰는 크롬이면 됩니다 |
| ffmpeg | 쇼츠 영상 | Mac `brew install ffmpeg` · Windows `winget install ffmpeg` |
| Python + `pip install pymupdf` | 목차 쪽번호 (없으면 쪽번호만 빈칸) | 선택 |
| R + 책에 나오는 패키지 | 원고의 R 출력 검증, 그림 자료 재생성 | 선택 (r-project.org) |

크롬은 자동으로 찾습니다. 못 찾으면 `CHROME_PATH` 환경변수로 경로를 알려 주세요.

```bash
git clone https://github.com/jynai2026-lab/ebook.git
cd ebook
npm install
```

| 하고 싶은 것 | 명령 | 결과 |
| --- | --- | --- |
| 전자책 PDF | `npm run build:1` · `npm run build:2` | `dist/*.pdf` |
| 상세페이지 이미지 | `node render-cards.mjs` | `dist/landing/` |
| 쇼츠·릴스 5편 | `node tools/make-shorts.mjs` | `dist/shorts/*.mp4` |
| 빌드 점검 | `node tools/audit.mjs 02-regression` | 오류 목록 |
| 원고의 R 출력 검증 | `node tools/run-r.mjs 02-regression` | 출력이 다르면 실패 (`--write`로 채움) |
| 2권 그림 다시 그리기 | `Rscript books/02-regression/r/figdata.R` → `python3 tools/build-figures-2.py` | `books/02-regression/figures/` |

쇼츠 음성은 Google AI Studio 키를 씁니다. 키는 저장소 밖에 둡니다.

- Mac·Linux: `~/.config/ebook/gemini.key` 파일에 키 한 줄
- Windows: `%USERPROFILE%\.config\ebook\gemini.key` 파일에 키 한 줄
- 또는 환경변수 `GEMINI_API_KEY`

키가 없으면 소리 없는 초안(`-draft.mp4`)이 나옵니다. 자세한 건 [video/README.md](video/README.md).

## 빌드

```bash
npm install
npm run build          # 전체
npm run build:1        # 1권만
```

결과물은 `dist/*.pdf`에 생성됩니다. 완성본 PDF와 쇼츠 영상(`dist/shorts/*.mp4`)은 저장소에도 올려 두므로, 원고를 고쳤다면 다시 빌드한 뒤 함께 커밋하세요.

## 원고 작성 문법

각 장은 `books/<권>/manuscript/NN-*.md` 파일 하나입니다. 파일명 순으로 정렬됩니다.

```markdown
---
part: 기초통계          # 목차의 파트 구분 (선택)
partNum: PART 1
num: 01                 # 장 번호
title: 척도가 분석을 결정한다
lead: 장 도입부 리드문
---

## 소제목

본문...
```

표준 마크다운에 더해 아래 블록을 지원합니다.

| 문법 | 결과 |
| --- | --- |
| `:::key 제목` … `:::` | 핵심 정리 (청록 박스) |
| `:::warn 제목` … `:::` | 흔한 실수 (노랑 박스) |
| `:::ok 제목` … `:::` | 권장 사례 (초록 박스) |
| `:::paper 제목` … `:::` | 논문 작성 팁 (네이비 박스) |
| `:::check 제목` … `:::` | 체크리스트 (`-` 목록) |
| `:::recap` … `:::` | 장 끝 한 줄 요약 (네이비 스트립) |
| ` ```r 라벨 ` | R 코드 블록 (신택스 하이라이트) |
| ` ```out 라벨 ` | 콘솔 출력 블록 |
| ` ```svg ` | 도식 (SVG 원본 삽입) |
| `$$ … $$` | 수식 박스 |

표지·부제·목차 문구는 `books/<권>/book.config.json`에서 바꿉니다. 권별 강조색도 여기서 지정합니다.

## 디자인

- 판형 A4 (210×297mm), 본문 10.4pt / 행간 1.78
- 본문 Pretendard, 코드 JetBrains Mono (`shared/fonts/`)
- 공통 스타일 `shared/theme/book.css` — 4권이 공유하며 권별 차이는 `--accent` 계열 변수뿐
- 쪽번호는 빌드 시 `pdf-lib`으로 스탬프 (표지 제외)

## 상세페이지 (래피드 업로드용 이미지)

```bash
node render-cards.mjs 01-basic-statistics
```

`landing/<권>/cards.html`의 `.card` 요소를 카드별 PNG로 뽑아
`dist/landing/<권>/`에 저장합니다. 1080px 폭, 2x 레티나.

- `thumbnail.png` — 상품 목록에 뜨는 대표이미지 (1080×1080)
- `card-01.png` ~ — 상세정보 영역에 **번호 순서대로** 업로드

카드에 `data-name="이름"`을 주면 그 이름으로 저장되고, 없는 카드만 01부터
순번이 매겨집니다. 문구·구성은 `cards.html`, 스타일은 `cards.css`에서 수정하고
다시 렌더링하면 됩니다.

### 상세페이지 구성 (레퍼런스 문법)

| 카드 | 역할 |
| --- | --- |
| thumbnail | 검정 배경 + 노랑 헤드라인 + 박스 한 줄 |
| 01 | 후킹 — 상황 대비 후 인버트 하이라이트로 타격 |
| 02 | 문제 시각화 — 결과 출력에 물음표 |
| 03 | 진단 — "공식을 배웠지, 고르는 법을 안 배웠다" |
| 04 | 해결 — 분석 선택 흐름도 |
| 05 | 책 속 미리보기 — R 코드와 실행 결과 |
| 06 | 목차 |
| 07 | 이런 분께 / 이런 분은 사지 마세요 |
| 08 | 스펙 · 가격 · CTA · 환불 정책 |

> 래피드는 **첫 3페이지를 무료 미리보기**로 공개합니다. 본문 앞 3페이지가
> 사실상 상세페이지의 연장이므로 후킹 구간으로 설계해야 합니다.
> 환불 문구는 "디지털 콘텐츠 특성상 결제 후 환불 불가"로 적습니다.
> 래피드 규정의 "3일 이내 취소"는 판매자용이지 구매자 환불이 아닙니다.

## 원고 소스와 R 검증

`source/01-기초통계_원본노트.txt` — 지은이의 HWPX 노트에서 추출한 원문입니다.
본문과 수식 444개가 모두 살아 있습니다(수식은 HWP 수식 스크립트 형태의 `$...$`).
원본에 실려 있던 SPSS 화면 캡처 103장은 R 코드와 실행 결과로 교체합니다.

책에 싣는 R 출력은 **반드시 실제로 실행해 얻은 것만** 씁니다. 지어내지 않습니다.

```bash
apt-get install -y r-base-core          # R 4.3.3
LANG=C.UTF-8 Rscript 스크립트.R          # 한글 출력에는 UTF-8 로케일이 필요
```

예제 데이터는 `books/01-basic-statistics/data/sample_data.csv`에 함께 넣어,
독자가 책의 코드를 그대로 복사해 같은 숫자를 재현할 수 있게 했습니다.

## 본문 그림

```bash
LANG=C.UTF-8 Rscript tools/densities.R > tools/dens.json   # 실제 데이터 계산
python3 tools/make-figures.py                              # SVG 생성
npm run build:1
```

`tools/make-figures.py`가 `books/<권>/figures/*.svg`를 만듭니다. 원고에서는
이렇게 부릅니다.

```markdown
!fig[**그림 4-3** 캡션입니다.](equal-variance.svg)
```

빌드가 SVG를 **인라인으로** 삽입합니다. `<img>`로 걸면 SVG 안에서 본문 폰트를
쓸 수 없어 한글이 깨지기 때문입니다. 캡션에는 마크다운을 쓸 수 있습니다.

그림은 두 종류입니다.

- **개념도** — 말로 설명하기 어려운 것을 그림으로. 캡션에 `(개념도)`를 붙여
  실제 데이터가 아님을 밝힙니다.
- **데이터 그림** — R이 계산한 실제 값으로 그립니다. 숫자를 지어내지 않습니다.

색은 `shared/theme/book.css`의 토큰과 맞춰 두었으므로, 본문 색을 바꾸면
`tools/make-figures.py` 상단 상수도 함께 고칩니다.

## 수식

수식은 **KaTeX**로 조판합니다. 원고에는 LaTeX으로 씁니다.

```markdown
블록 수식:
$$
s_p^2 = \frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1+n_2-2}
$$ (닫는 $$ 와 같은 줄에 캡션을 달 수 있습니다)

인라인 수식: 자유도는 $n_1+n_2-2$ 입니다.
```

빌드 시 서버에서 HTML로 변환하므로 PDF에 그대로 박힙니다. KaTeX 폰트는
`shared/theme/fonts/`에 함께 두었습니다.

R 코드의 `df$gender` 처럼 `$`가 들어간 인라인 코드는 수식 처리 전에 먼저
빼두므로 오인되지 않습니다.

원본 노트(`source/`)의 수식은 HWP 수식 스크립트라 LaTeX이 아닙니다.
집필할 때 LaTeX으로 옮겨 적어야 합니다.

### 장별 그림 모듈

그림 생성기는 장별로 나뉘어 있습니다.

```
tools/figlib.py       공통 (색 토큰, SVG 헬퍼, 정규곡선)
tools/fig_ch02.py     2장
tools/fig_ch0304.py   3~4장
tools/make-figures.py 7장(t-검정) + 전체 실행
```

곡선을 겹쳐 그릴 때는 `curve_paths()`로 선과 채움을 따로 받아
**채움을 모두 그린 뒤 선을 그립니다.** 번갈아 그리면 뒤 곡선의 반투명 채움이
앞 곡선의 선을 덮어 회색으로 보입니다.

`peak`은 함께 그리는 곡선 중 가장 큰 y여야 합니다. 작게 잡으면 곡선이 위로
넘어가 제목을 침범합니다.

### 자리표시자 규칙 (중요)

빌드는 코드·수식·그림 같은 조각을 잠시 빼두었다가 마크다운 변환 후 되돌립니다.
이때 **블록용과 인라인용의 표시 방법이 다릅니다.**

| 용도 | 표시 | 이유 |
| --- | --- | --- |
| 블록 (코드 블록, 콜아웃, 그림) | `<!--BLK0-->` | 앞뒤 빈 줄로 감싸 독립 블록이 된다 |
| 인라인 (인라인 코드, 인라인 수식) | ` 0 ` | 아래 두 가지를 피하기 위해 |

인라인에 HTML 주석을 쓰면 두 가지가 깨집니다.

1. 콜아웃 라벨은 `esc()`를 거치므로 `<!--...-->`가 `&lt;!--...--&gt;`가 되어 복원되지 않습니다
2. 문단이 자리표시자로 시작하면 markdown-it이 그 줄을 HTML 블록으로 보고
   같은 줄의 `**강조**`를 전부 날립니다 (CommonMark HTML block type 2)

복원은 **더 바뀌지 않을 때까지 반복**합니다. 콜아웃 안에 인라인 코드가 들어가면
자리표시자가 중첩되는데, `String.replace`는 끼워 넣은 문자열을 다시 훑지 않기
때문입니다. 복원이 끝난 뒤에도 자리표시자가 남으면 **빌드가 실패합니다.**
