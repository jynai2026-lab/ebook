# 개념 영상

책의 그림과 같은 색·글꼴·데이터를 쓰는 캔버스 애니메이션을 MP4로 뽑는다.

## 만드는 법

```bash
node tools/render-video.mjs video/sampling.html      sampling      9
node tools/render-video.mjs video/shorts-power.html  shorts-power  22 --vertical
```

`--vertical`은 1080×1920(쇼츠), 없으면 1280×720(롱폼)이다.
결과는 `dist/<이름>.mp4`.

## 페이지가 지켜야 할 것

HTML은 두 가지만 내놓으면 된다.

- `window.renderFrame(t)` — `t`는 0에서 1. 그 시점의 한 프레임을 그린다.
- `window.__ready = true` — 글꼴이 다 실린 뒤에 세운다.

렌더러가 `t`를 0부터 1까지 훑으며 프레임마다 스크린샷을 찍고 ffmpeg로 엮는다.
프레임마다 같은 그림이 나와야 하므로 **난수는 고정 시드**를 써야 한다
(`Math.random()`을 쓰면 프레임마다 그림이 달라져 화면이 떨린다).

## 숫자는 책과 같아야 한다

영상에 나오는 값은 책에 실린 값, 즉 R로 실제 실행한 결과와 같아야 한다.
예를 들어 `shorts-power.html`의 검정력 0.338 / 0.478 / 0.697 / 0.801 / 0.940은
5장의 `power.t.test(n, delta = 0.5, sd = 1, sig.level = .05)` 출력이다.

히스토그램을 그릴 때는 관측된 최댓값이 아니라 **이론 밀도로 정규화**해야
곡선과 눈금이 맞는다 (`sampling.html` 참고).
