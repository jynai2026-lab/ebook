/**
 * 쇼츠·릴스 공통 틀 (1080 × 1920)
 *
 * 각 쇼츠 페이지는 Shorts.run(draw, 옵션) 한 번만 부른다.
 * 자막, 안전 영역, 마지막 안내 카드는 이 틀이 맡는다.
 *
 * 타이밍은 렌더러가 넣어 주는 window.TIMELINE(음성 길이로 잰 것)을 따른다.
 * 화면이 음성에 맞추는 구조라서 싱크가 어긋나지 않는다.
 */
(function () {
  const W = 1080, H = 1920;

  // 플랫폼 UI가 덮는 곳을 피한 안전 영역.
  // 아래는 제목·설명·계정명이, 오른쪽은 좋아요·댓글 버튼이, 위는 상단바가 덮는다.
  const SAFE = { top: 250, bottom: 1440, left: 72, right: 930 };
  const CX = (SAFE.left + SAFE.right) / 2;

  // 책(book.css, figlib.py)과 같은 색
  const C = {
    INK: '#101828', MID: '#344054', SOFT: '#667085', FAINT: '#98A2B3',
    TEAL: '#0E7490', TEAL_LINE: '#A8D5DE', TEAL_TINT: '#ECF7F9', NAVY: '#16243F',
    CORAL: '#C2452F', CORAL_TINT: '#FBEAE6', AMBER: '#B54708', RULE: '#E4E7EC',
    PAPER: '#FBFCFD', HILITE: '#7FE3F0',
  };

  const cv = document.createElement('canvas');
  cv.width = W; cv.height = H;
  // 틀은 <head>에서 불리므로 아직 <body>가 없을 수 있다
  (document.body || document.documentElement).appendChild(cv);
  const g = cv.getContext('2d');

  const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
  const ease = t => { t = clamp(t); return t * t * (3 - 2 * t); };

  function font(size, weight) { return `${weight} ${size}px Pretendard, sans-serif`; }

  function T(s, x, y, size, color, weight = 400, align = 'center') {
    g.font = font(size, weight);
    g.fillStyle = color; g.textAlign = align; g.textBaseline = 'alphabetic';
    g.fillText(s, x, y);
  }

  function box(x, y, w, h, r, fill, stroke, lw = 3) {
    g.beginPath(); g.roundRect(x, y, w, h, r);
    if (fill) { g.fillStyle = fill; g.fill(); }
    if (stroke) { g.strokeStyle = stroke; g.lineWidth = lw; g.stroke(); }
  }

  /* ---------------------------------------------------------------- 자막 */

  /** '**강조**' 표기를 글자별 강조 여부로 푼다 */
  function parseEmph(s) {
    const chars = [], emph = [];
    let on = false;
    for (let i = 0; i < s.length; i++) {
      if (s[i] === '*' && s[i + 1] === '*') { on = !on; i++; continue; }
      chars.push(s[i]); emph.push(on);
    }
    return { text: chars.join(''), emph };
  }

  /**
   * 두 줄로 나눌 때는 앞에서부터 채우지 않고 두 줄 길이가 비슷해지는 자리를 고른다.
   * 앞에서부터 채우면 '뜻' 한 글자만 둘째 줄로 떨어지는 일이 생긴다.
   */
  function balance2(text, size, weight, maxW) {
    g.font = font(size, weight);
    let best = null;
    for (let i = text.indexOf(' '); i !== -1; i = text.indexOf(' ', i + 1)) {
      const a = text.slice(0, i), b = text.slice(i + 1);
      const wa = g.measureText(a).width, wb = g.measureText(b).width;
      if (wa > maxW || wb > maxW) continue;
      const worst = Math.max(wa, wb);
      if (!best || worst < best.worst) best = { worst, lines: [{ s: a, at: 0 }, { s: b, at: i + 1 }] };
    }
    return best && best.lines;
  }

  /** 단어 단위로 줄을 나누고, 각 줄이 원문 몇 번째 글자부터인지 함께 돌려준다 */
  function wrap(text, size, weight, maxW) {
    g.font = font(size, weight);
    if (g.measureText(text).width <= maxW) return [{ s: text, at: 0 }];
    const two = balance2(text, size, weight, maxW);
    if (two) return two;
    return greedy(text, size, weight, maxW);
  }

  function greedy(text, size, weight, maxW) {
    g.font = font(size, weight);
    const lines = [];
    let start = 0, cur = '', curStart = 0;
    const words = text.split(' ');
    for (const w of words) {
      const cand = cur ? cur + ' ' + w : w;
      if (g.measureText(cand).width <= maxW || !cur) {
        if (!cur) curStart = start;
        cur = cand;
      } else {
        lines.push({ s: cur, at: curStart });
        cur = w; curStart = start;
      }
      start += w.length + 1;
    }
    if (cur) lines.push({ s: cur, at: curStart });
    return lines;
  }

  function caption(raw, alpha) {
    if (!raw) return;
    const { text, emph } = parseEmph(raw);
    const maxW = SAFE.right - SAFE.left - 64;
    // 두 줄을 넘으면 글자를 줄인다
    let size = 52, lines = wrap(text, size, 700, maxW);
    while (lines.length > 2 && size > 38) { size -= 4; lines = wrap(text, size, 700, maxW); }

    const lh = size * 1.34, pad = 24;
    const bh = lines.length * lh + pad * 2;
    const y0 = SAFE.bottom - bh;
    g.globalAlpha = alpha;
    box(SAFE.left, y0, SAFE.right - SAFE.left, bh, 22, 'rgba(22,36,63,.95)');

    g.font = font(size, 700);
    g.textBaseline = 'alphabetic'; g.textAlign = 'left';
    lines.forEach((ln, k) => {
      const y = y0 + pad + size * 1.02 + k * lh;
      let x = CX - g.measureText(ln.s).width / 2;
      // 같은 강조 상태인 글자끼리 묶어 한 번에 찍는다
      let i = 0;
      while (i < ln.s.length) {
        const on = emph[ln.at + i];
        let j = i;
        while (j < ln.s.length && emph[ln.at + j] === on) j++;
        const piece = ln.s.slice(i, j);
        g.fillStyle = on ? C.HILITE : '#fff';
        g.fillText(piece, x, y);
        x += g.measureText(piece).width;
        i = j;
      }
    });
    g.globalAlpha = 1;
  }

  /* ---------------------------------------------------------------- 틀 */

  function tagPill(s) {
    if (!s) return;
    g.font = font(30, 700);
    const w = g.measureText(s).width + 44;
    box(SAFE.left, SAFE.top + 4, w, 52, 26, C.NAVY);
    T(s, SAFE.left + w / 2, SAFE.top + 40, 30, '#fff', 700);
  }

  function endCard(q, opt) {
    const a = ease(q / 0.3);
    g.globalAlpha = a * 0.95; g.fillStyle = '#fff'; g.fillRect(0, 0, W, H);
    g.globalAlpha = a;
    T(opt.cta1 || '이런 설명이 처음부터 끝까지', CX, 700, 46, C.SOFT, 700);
    T(opt.cta2 || '전자책에 있습니다', CX, 800, 84, C.NAVY, 800);
    g.font = font(34, 700);
    const pill = opt.cta3 || '5년간 과외한 내용 그대로 · 프로필 링크';
    const pw = g.measureText(pill).width + 64;
    box(CX - pw / 2, 866, pw, 76, 38, C.TEAL);
    T(pill, CX, 916, 34, '#fff', 700);

    // 계정 이름이 뜨는 왼쪽 아래를 가리킨다 (일부러 안전 영역 밖으로)
    const k = ease((q - 0.25) / 0.3);
    if (k > 0) {
      g.globalAlpha = a * k;
      g.strokeStyle = C.TEAL; g.lineWidth = 8; g.lineCap = 'round';
      g.beginPath(); g.moveTo(CX - 60, 1010); g.quadraticCurveTo(CX - 260, 1200, 220, 1540); g.stroke();
      g.beginPath(); g.moveTo(206, 1480); g.lineTo(220, 1545); g.lineTo(282, 1520); g.stroke();
    }
    g.globalAlpha = 1;
  }

  function safeOverlay() {
    g.fillStyle = 'rgba(194,69,47,.14)';
    g.fillRect(0, 0, W, SAFE.top);
    g.fillRect(0, SAFE.bottom, W, H - SAFE.bottom);
    g.fillRect(0, SAFE.top, SAFE.left, SAFE.bottom - SAFE.top);
    g.fillRect(SAFE.right, SAFE.top, W - SAFE.right, SAFE.bottom - SAFE.top);
  }

  function run(draw, opt = {}) {
    window.renderFrame = sec => {
      const TL = window.TIMELINE;
      g.clearRect(0, 0, W, H);
      g.fillStyle = '#fff'; g.fillRect(0, 0, W, H);

      const beats = TL.beats;
      const byId = Object.fromEntries(beats.map(b => [b.id, b]));
      // 지금 장면: 가장 최근에 시작한 문장. 문장 사이 틈에는 앞 문장을 유지한다.
      let i = 0;
      beats.forEach((b, k) => { if (sec >= b.start) i = k; });
      const b = beats[i];
      const last = beats[beats.length - 1];

      const ctx = {
        sec, i, id: b.id,
        on: id => byId[id] && sec >= byId[id].start,
        /** 그 문장이 시작된 뒤 d초에 걸친 등장 진행도 (0→1) */
        at: (id, d = 0.6) => byId[id] ? ease((sec - byId[id].start) / d) : 0,
        /** 그 문장 전체 길이에 걸친 진행도 (0→1) */
        span: id => byId[id] ? ease((sec - byId[id].start) / (byId[id].end - byId[id].start)) : 0,
        beat: id => byId[id],
      };

      tagPill(opt.tag);
      draw(ctx);

      if (sec < last.end) {
        caption(b.cap, ease((sec - b.start) / 0.14));
      } else {
        endCard((sec - last.end) / Math.max(0.5, TL.total - last.end), opt);
      }
      if (location.search.includes('safe')) safeOverlay();
    };

    Promise.all([
      document.fonts.load(font(60, 800)),
      document.fonts.load(font(40, 400)),
      document.fonts.load('500 40px "JetBrains Mono"'),
    ]).then(() => {
      window.__ready = true;
      if (window.TIMELINE) window.renderFrame(0);
    });
  }

  /* ---------------------------------------------------------------- 여러 편에서 쓰는 그리기 */

  const phi = z => Math.exp(-z * z / 2);

  /**
   * 정규곡선. 가로는 [x0, x1] 화면 구간에 z ∈ [-R, R]을 펼친다.
   * sd를 1보다 작게 주면 같은 높이 기준에서 더 뾰족해진다(면적이 같도록).
   */
  function curve(x0, x1, base, h, { mu = 0, sd = 1, R = 3.6, color = C.NAVY, fill = null,
                                    lw = 5, reveal = 1, shade = null } = {}) {
    const sx = z => x0 + (x1 - x0) * (z + R) / (2 * R);
    const y = z => base - h * phi((z - mu) / sd) / sd;
    const n = 180, end = -R + 2 * R * clamp(reveal);
    const path = () => {
      g.beginPath();
      for (let i = 0; i <= n; i++) {
        const z = -R + (end + R) * i / n;
        i ? g.lineTo(sx(z), y(z)) : g.moveTo(sx(z), y(z));
      }
    };
    if (fill) {
      path(); g.lineTo(sx(end), base); g.lineTo(sx(-R), base); g.closePath();
      g.fillStyle = fill; g.fill();
    }
    // shade: [[lo, hi, 색], ...] 구간을 곡선 아래로 칠한다 (꼬리 면적 등)
    if (shade) for (const [lo, hi, c] of shade) {
      g.beginPath(); g.moveTo(sx(lo), base);
      for (let i = 0; i <= 60; i++) { const z = lo + (hi - lo) * i / 60; g.lineTo(sx(z), y(z)); }
      g.lineTo(sx(hi), base); g.closePath(); g.fillStyle = c; g.fill();
    }
    path(); g.strokeStyle = color; g.lineWidth = lw; g.stroke();
    return { sx, y };
  }

  /** 글자 위에 긋는 취소선 (t: 0→1로 그어지는 진행도) */
  function strike(x0, x1, y, t = 1, color = C.CORAL, lw = 8) {
    if (t <= 0) return;
    g.strokeStyle = color; g.lineWidth = lw; g.lineCap = 'round';
    g.beginPath(); g.moveTo(x0, y); g.lineTo(x0 + (x1 - x0) * clamp(t), y); g.stroke();
  }

  /** 가운데 정렬 알약 */
  function pill(s, cx, y, size, bg, fg = '#fff', weight = 800) {
    g.font = font(size, weight);
    const w = g.measureText(s).width + size * 1.3, h = size * 1.7;
    box(cx - w / 2, y - h / 2, w, h, h / 2, bg);
    T(s, cx, y + size * 0.36, size, fg, weight);
    return w;
  }

  function measure(s, size, weight = 400) { g.font = font(size, weight); return g.measureText(s).width; }

  /** 등장 효과: 아래에서 살짝 올라오며 나타난다 */
  function rise(a, dy = 18) { g.globalAlpha = clamp(a); return dy * (1 - clamp(a)); }

  window.Shorts = { W, H, SAFE, CX, C, g, clamp, ease, T, box, font, run,
                    curve, strike, pill, measure, rise };
})();
