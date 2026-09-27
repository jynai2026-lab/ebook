/**
 * 사회과학 통계 입문 시리즈 — 전자책 빌드
 *
 *   node build.mjs [권슬러그]      예) node build.mjs 01-basic-statistics
 *   node build.mjs                 → books/ 아래 전체 빌드
 *
 * 원고(manuscript/*.md) → HTML 조립 → Chromium 인쇄 → 쪽번호 스탬프 → dist/*.pdf
 */
import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { execFileSync } from 'child_process';
import { launchBrowser } from './tools/browser.mjs';
import { PDFDocument, StandardFonts, rgb } from 'pdf-lib';
import MarkdownIt from 'markdown-it';
import attrs from 'markdown-it-attrs';
import katex from 'katex';

const ROOT = dirname(fileURLToPath(import.meta.url));

const md = new MarkdownIt({ html: true, breaks: false, typographer: false }).use(attrs);

/* ---------------------------------------------------------------- 유틸 */
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/** R 코드 간이 신택스 하이라이트 */
function highlightR(src) {
  const KEY = /\b(function|if|else|for|while|repeat|break|next|return|TRUE|FALSE|NULL|NA|NaN|Inf|library|require)\b/g;
  const tokens = [];
  const stash = s => `${tokens.push(s) - 1}`;

  let out = esc(src);

  // 주석 — 따옴표 안의 #은 제외
  out = out.split('\n').map(line => {
    const m = line.match(/^(.*?)(#.*)$/);
    if (!m) return line;
    const quotes = (m[1].match(/"/g) || []).length + (m[1].match(/'/g) || []).length;
    if (quotes % 2 === 1) return line;
    return m[1] + stash(`<span class="c">${m[2]}</span>`);
  }).join('\n');

  out = out.replace(/"([^"\n]*?)"/g, (_, s) => stash(`<span class="s">"${s}"</span>`));
  out = out.replace(/'([^'\n]*?)'/g, (_, s) => stash(`<span class="s">'${s}'</span>`));
  out = out.replace(/\b([A-Za-z_.][\w.]*)\s*(?=\()/g, (_, f) => stash(`<span class="f">${f}</span>`));
  out = out.replace(KEY, k => stash(`<span class="k">${k}</span>`));
  // 자리표시자(\u0001 12 \u0002) 안의 숫자를 다시 잡지 않도록 가드
  out = out.replace(/(?<![\u0001\d])\b(\d+\.?\d*)\b(?![\d\u0002])/g, n => stash(`<span class="n">${n}</span>`));
  out = out.replace(/(&lt;-|~|%&gt;%|\|&gt;|\+|=)/g, o => stash(`<span class="o">${o}</span>`));

  return out.replace(/(\d+)/g, (_, i) => tokens[+i]);
}


/** LaTeX -> KaTeX HTML. 실패해도 빌드를 멈추지 않고 원본을 보여준다. */
function tex(src, display) {
  try {
    return katex.renderToString(src.trim(), {
      displayMode: display, throwOnError: false, strict: false, output: 'html',
    });
  } catch (e) {
    console.warn(`  ! 수식 오류: ${src.trim().slice(0, 40)} — ${e.message}`);
    return `<code>${esc(src)}</code>`;
  }
}

/** 그림 SVG 안의 수식 자리표시자를 KaTeX로 조판한다 (figlib.tex 가 심어 둔다). */
function renderFigTex(svg) {
  return svg.replace(/<span data-tex="([^"]*)"\s*><\/span>/g, (_, raw) => {
    const latex = raw.replace(/&quot;/g, '"').replace(/&gt;/g, '>')
                     .replace(/&lt;/g, '<').replace(/&amp;/g, '&');
    return tex(latex, false);
  });
}

/**
 * 저자 친화 문법 → HTML
 *   :::key / :::warn / :::ok / :::paper / :::check / :::recap ... :::
 *   ```r  / ```out / ```svg
 *   $$ 수식 $$
 */
function preprocess(src, figDir) {
  // CommonMark의 right-flanking 규칙상, 닫는 **이 구두점 바로 뒤이면서 한글 바로 앞에
  // 오면 강조로 인식되지 않는다. 한국어 원고에서 흔한 형태라 먼저 태그로 바꿔 둔다.
  // (콜아웃 본문도 여기서 함께 처리되도록 블록을 잘라내기 전에 실행한다)
  src = src.replace(/\*\*([^*\n]*[)\]'"’”.,!?%:;·…\-~])\*\*(?=[가-힣])/g, '<strong>$1</strong>');

  const blocks = [];
  const keep = html => `\n\n<!--BLK${blocks.push(html) - 1}-->\n\n`;

  // 문단 중간에 들어가는 조각에는 HTML 주석을 쓸 수 없다. 두 가지가 깨진다.
  //  1) 콜아웃 라벨은 esc()를 거치므로 <!--...-->가 &lt;!--...--&gt;로 변해 복원되지 않는다.
  //  2) 문단이 자리표시자로 시작하면 markdown-it이 그 줄을 HTML 블록으로 보고
  //     같은 줄의 **강조**를 전부 날린다 (CommonMark HTML block type 2).
  // 그래서 마크다운도 esc()도 건드리지 않는 사설영역 문자를 쓴다.
  const IN0 = '\uE000', IN1 = '\uE001';
  const keepInline = html => `${IN0}${blocks.push(html) - 1}${IN1}`;

  src = src.replace(/```r(?:[ \t]+([^\n]+))?\n([\s\S]*?)```/g, (_, label, code) =>
    keep(`<div class="code"><div class="code__bar">${esc(label || 'R')}</div><pre>${highlightR(code.replace(/\n$/, ''))}</pre></div>`));

  src = src.replace(/```out(?:[ \t]+([^\n]+))?\n([\s\S]*?)```/g, (_, label, code) =>
    keep(`<div class="out"><div class="out__bar">${esc(label || '실행 결과')}</div><pre>${esc(code.replace(/\n$/, ''))}</pre></div>`));

  src = src.replace(/```svg\n([\s\S]*?)```/g, (_, svg) => keep(renderFigTex(svg)));

  // 인라인 코드(`df$gender` 등)를 먼저 빼둬야 R의 $가 수식으로 오인되지 않는다
  src = src.replace(/`([^`\n]+)`/g, (_, code) => keepInline(`<code>${esc(code)}</code>`));

  // $...$ 인라인 수식
  src = src.replace(/\$([^\s$][^$\n]*?)\$/g, (_, f) => keepInline(tex(f, false)));

  // !fig[캡션](파일.svg) — figures/ 의 SVG를 인라인으로 넣는다.
  // <img>로 걸면 SVG 안에서 본문 폰트를 못 써 한글이 깨지므로 반드시 인라인.
  src = src.replace(/^!fig\[([^\]]*)\]\(([^)]+)\)\s*$/gm, (m, cap, file) => {
    const path = join(figDir || '', file);
    if (!existsSync(path)) { console.warn(`  ! 그림 없음: ${file}`); return m; }
    const svg = renderFigTex(readFileSync(path, 'utf8').replace(/<\?xml[^>]*\?>/, ''));
    return keep(`<figure>${svg}${cap ? `<figcaption>${md.renderInline(cap)}</figcaption>` : ''}</figure>`);
  });

  // 캡션은 인라인 수식·코드가 이미 자리표시자로 바뀐 뒤라 esc하면 안 된다. 본문과 같은 인라인 렌더를 태운다.
  src = src.replace(/^\$\$\n([\s\S]*?)\n\$\$(?:[ \t]*\(([^\n]+)\))?/gm, (_, f, note) =>
    keep(`<div class="formula">${tex(f, true)}${note ? `<small>${md.renderInline(note)}</small>` : ''}</div>`));

  const KIND = {
    key:   ['callout', '개념 정리'],
    warn:  ['callout callout--warn', '유의 사항'],
    ok:    ['callout callout--ok', '권장 절차'],
    paper: ['callout callout--paper', '논문 보고'],
  };
  src = src.replace(/^:::(key|warn|ok|paper)(?:[ \t]+([^\n]+))?\n([\s\S]*?)\n:::[ \t]*$/gm, (_, kind, label, body) => {
    const [cls, def] = KIND[kind];
    return keep(`<div class="${cls}"><span class="callout__label">${esc(label || def)}</span>\n${md.render(body)}</div>`);
  });

  src = src.replace(/^:::check(?:[ \t]+([^\n]+))?\n([\s\S]*?)\n:::[ \t]*$/gm, (_, label, body) => {
    const items = body.split('\n').filter(l => l.trim().startsWith('-'))
      .map(l => `<li>${md.renderInline(l.replace(/^\s*-\s*/, ''))}</li>`).join('');
    return keep(`<div class="check"><p class="check__title">${esc(label || '체크리스트')}</p><ul>${items}</ul></div>`);
  });

  src = src.replace(/^:::recap\n([\s\S]*?)\n:::[ \t]*$/gm, (_, body) =>
    keep(`<div class="recap">${md.render(body)}</div>`));

  let html = md.render(src);

  // 콜아웃·체크리스트 같은 블록은 그 자체가 자리표시자로 보관되는데,
  // 안에 인라인 코드나 수식의 자리표시자가 또 들어 있다. String.replace는
  // 끼워 넣은 문자열을 다시 훑지 않으므로 한 번만 돌리면 중첩된 것이 남는다.
  // 더 바뀌지 않을 때까지 반복한다.
  const restore = h => h
    .replace(/<p>\s*<!--BLK(\d+)-->\s*<\/p>/g, (_, i) => blocks[+i])
    .replace(/<!--BLK(\d+)-->/g, (_, i) => blocks[+i])
    .replace(/\uE000(\d+)\uE001/g, (_, i) => blocks[+i]);

  for (let pass = 0; pass < 10; pass++) {
    const next = restore(html);
    if (next === html) break;
    html = next;
  }

  const left = html.match(/<!--BLK\d+-->|\uE000\d+\uE001/g);
  if (left) throw new Error(`자리표시자가 복원되지 않았습니다 (${left.length}개): ${left.slice(0, 3).join(', ')}`);

  return html;
}

/** manuscript/*.md 한 장(章) 파싱 */
function parseChapter(raw, figDir) {
  const m = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  const meta = {};
  let body = raw;
  if (m) {
    body = m[2];
    for (const line of m[1].split('\n')) {
      const kv = line.match(/^(\w+):\s*(.*)$/);
      if (kv) meta[kv[1]] = kv[2].trim();
    }
  }
  return { meta, html: preprocess(body, figDir) };
}

/* ---------------------------------------------------------------- 조립 */
function buildCover(cfg) {
  const pts = (cfg.coverPoints || []).map(p => `<li>${esc(p)}</li>`).join('');
  // 표지 제목: *강조* -> <em>, 줄바꿈 -> <br>
  const title = esc(cfg.title || '')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>');
  return `
<section class="cover">
  <div class="cover__grid"></div>
  <svg class="cover__deco" viewBox="0 0 400 160" preserveAspectRatio="none">
    <path d="M0,160 C60,160 70,20 130,20 C150,20 155,8 200,8 C245,8 250,20 270,20 C330,20 340,160 400,160 Z" fill="#fff"/>
  </svg>
  <div class="cover__series">${esc(cfg.series || '')}</div>
  <div class="cover__vol">${esc(cfg.volumeLabel || '')}</div>
  <h1 class="cover__title">${title}</h1>
  <div class="cover__rule"></div>
  <p class="cover__sub">${esc(cfg.subtitle || '')}</p>
  <ul class="cover__points">${pts}</ul>
  <div class="cover__foot">
    <span class="cover__author">${esc(cfg.author || '')}</span>
    <span>${esc(cfg.tool || '')}</span>
  </div>
</section>`;
}

function buildToc(cfg, chapters, pageOf = {}) {
  let html = `<section class="toc"><h1 class="toc__title">목차</h1>`;
  if (cfg.tocLead) html += `<p class="toc__lead">${esc(cfg.tocLead)}</p>`;
  let part = null, open = false;
  for (const ch of chapters) {
    if (ch.meta.part && ch.meta.part !== part) {
      part = ch.meta.part;
      if (open) html += '</ul>';
      html += `<div class="toc__part"><span>${esc(ch.meta.partNum || '')}</span>${esc(part)}</div><ul>`;
      open = true;
    }
    if (!open) { html += '<ul>'; open = true; }
    const pg = pageOf[ch.meta.num];
    html += `<li><b>${esc(ch.meta.num || '')}</b><i>${esc(ch.meta.title || '')}</i>`
          + `<em>${pg == null ? '' : pg}</em></li>`;
  }
  if (open) html += '</ul>';
  return html + '</section>';
}

function buildChapter(ch) {
  // 목차 쪽번호를 매기려면 이 장이 PDF 몇 쪽에서 시작하는지 알아야 한다.
  // 새 줄을 만들지 않도록 이미 있는 장 번호 안에 흰 글씨로 끼워 넣는다.
  const mark = ch.meta.num ? `<span class="pagemark">§CH${esc(ch.meta.num)}§</span>` : '';
  return `
<section class="chapter">
  <header class="chapter__head">
    ${ch.meta.num ? `<span class="chapter__num">${esc(ch.meta.num)}${mark}</span>` : ''}
    <h1 class="chapter__title">${esc(ch.meta.title || '')}</h1>
    ${ch.meta.lead ? `<p class="chapter__lead">${esc(ch.meta.lead)}</p>` : ''}
  </header>
  ${ch.html}
</section>`;
}

function assemble(cfg, chapters, pageOf = {}) {
  const vars = Object.entries(cfg.accent || {}).map(([k, v]) => `--${k}: ${v};`).join(' ');
  return `<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<title>${esc(cfg.title || '')}</title>
<link rel="stylesheet" href="../../shared/theme/katex.min.css">
<link rel="stylesheet" href="../../shared/theme/book.css">
${vars ? `<style>:root{${vars}}</style>` : ''}
</head><body>
${buildCover(cfg)}
${buildToc(cfg, chapters, pageOf)}
${chapters.map(buildChapter).join('\n')}
</body></html>`;
}

/* ---------------------------------------------------------------- 렌더 */
async function renderPdf(htmlPath, pdfPath) {
  const browser = await launchBrowser();
  const page = await browser.newPage();
  await page.goto('file://' + htmlPath, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: pdfPath, preferCSSPageSize: true, printBackground: true });
  await browser.close();
}

const hexToRgb = h => {
  const v = parseInt(String(h || '#0E7490').slice(1), 16);
  return { r: ((v >> 16) & 255) / 255, g: ((v >> 8) & 255) / 255, b: (v & 255) / 255 };
};

/** 표지 다음 페이지부터 하단 중앙에 쪽번호 + 악센트 점 */
async function stampPageNumbers(pdfPath, accentHex) {
  const doc = await PDFDocument.load(readFileSync(pdfPath));
  const font = await doc.embedFont(StandardFonts.Helvetica);
  const pages = doc.getPages();
  const c = hexToRgb(accentHex);

  pages.forEach((p, i) => {
    if (i === 0) return;                       // 표지는 번호 없음
    const n = String(i);
    const { width } = p.getSize();
    const size = 8.5;
    const w = font.widthOfTextAtSize(n, size);
    p.drawText(n, { x: width / 2 - w / 2, y: 30, size, font, color: rgb(0.40, 0.45, 0.53) });
    p.drawCircle({ x: width / 2, y: 45, size: 1.15, color: rgb(c.r, c.g, c.b) });
  });

  writeFileSync(pdfPath, await doc.save());
  return pages.length;
}

/** 1차 렌더 결과에서 장별 시작 쪽을 읽는다. 실패하면 목차 쪽번호만 비운다. */
function readChapterPages(pdfPath) {
  try {
    // Windows에는 python3가 없고 python 또는 py로 부른다
    for (const py of ['python3', 'python', 'py']) {
      try {
        const out = execFileSync(py, [join(ROOT, 'tools', 'toc-pages.py'), pdfPath],
                                 { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
        return JSON.parse(out);
      } catch (e) { if (e.code !== 'ENOENT') throw e; }
    }
    throw new Error('파이썬을 찾지 못했습니다');
  } catch (e) {
    console.log('  - 목차 쪽번호를 읽지 못했습니다:', e.message.split('\n')[0]);
    return {};
  }
}

/* ---------------------------------------------------------------- 메인 */
async function buildBook(slug) {
  const dir = join(ROOT, 'books', slug);
  const cfg = JSON.parse(readFileSync(join(dir, 'book.config.json'), 'utf8'));
  const mdir = join(dir, 'manuscript');

  const files = existsSync(mdir) ? readdirSync(mdir).filter(f => f.endsWith('.md')).sort() : [];
  if (!files.length) { console.log(`  - ${slug}: 원고 없음, 건너뜀`); return; }

  const figDir = join(dir, 'figures');
  const chapters = files.map(f => parseChapter(readFileSync(join(mdir, f), 'utf8'), figDir));
  const htmlPath = join(dir, '.build.html');

  mkdirSync(join(ROOT, 'dist'), { recursive: true });
  const name = cfg.filename || slug;
  const pdfPath = join(ROOT, 'dist', `${name}.pdf`);

  // 1차: 쪽번호 없이 한 번 찍어서 각 장이 몇 쪽에서 시작하는지 알아낸다.
  writeFileSync(htmlPath, assemble(cfg, chapters));
  await renderPdf(htmlPath, pdfPath);
  const pageOf = readChapterPages(pdfPath);

  // 2차: 목차에 그 쪽번호를 넣어 다시 찍는다.
  if (Object.keys(pageOf).length) {
    writeFileSync(htmlPath, assemble(cfg, chapters, pageOf));
    await renderPdf(htmlPath, pdfPath);
  }
  const n = await stampPageNumbers(pdfPath, (cfg.accent || {}).accent);
  const kb = (readFileSync(pdfPath).length / 1024).toFixed(0);

  console.log(`  [OK] ${cfg.title} — ${n}쪽, ${kb}KB -> dist/${name}.pdf`);
}

const target = process.argv[2];
const slugs = target ? [target]
  : readdirSync(join(ROOT, 'books')).filter(d => existsSync(join(ROOT, 'books', d, 'book.config.json')));

console.log('전자책 빌드 시작\n');
for (const s of slugs) {
  try { await buildBook(s); }
  catch (e) { console.error(`  [FAIL] ${s}: ${e.message}`); }
}
console.log('\n완료.');
