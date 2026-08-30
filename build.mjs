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
import { chromium } from 'playwright-core';
import { PDFDocument, StandardFonts, rgb } from 'pdf-lib';
import MarkdownIt from 'markdown-it';
import attrs from 'markdown-it-attrs';

const ROOT = dirname(fileURLToPath(import.meta.url));
const CHROME = [
  '/opt/pw-browsers/chromium/chrome-linux/chrome',
  '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell',
].find(existsSync);

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
  src = src.replace(/\*\*([^*\n]*[)\]'"’”.!?])\*\*(?=[가-힣])/g, '<strong>$1</strong>');

  const blocks = [];
  const keep = html => `\n\n<!--BLK${blocks.push(html) - 1}-->\n\n`;

  src = src.replace(/```r(?:[ \t]+([^\n]+))?\n([\s\S]*?)```/g, (_, label, code) =>
    keep(`<div class="code"><div class="code__bar">${esc(label || 'R')}</div><pre>${highlightR(code.replace(/\n$/, ''))}</pre></div>`));

  src = src.replace(/```out(?:[ \t]+([^\n]+))?\n([\s\S]*?)```/g, (_, label, code) =>
    keep(`<div class="out"><div class="out__bar">${esc(label || '실행 결과')}</div><pre>${esc(code.replace(/\n$/, ''))}</pre></div>`));

  src = src.replace(/```svg\n([\s\S]*?)```/g, (_, svg) => keep(svg));

  // !fig[캡션](파일.svg) — figures/ 의 SVG를 인라인으로 넣는다.
  // <img>로 걸면 SVG 안에서 본문 폰트를 못 써 한글이 깨지므로 반드시 인라인.
  src = src.replace(/^!fig\[([^\]]*)\]\(([^)]+)\)\s*$/gm, (m, cap, file) => {
    const path = join(figDir || '', file);
    if (!existsSync(path)) { console.warn(`  ! 그림 없음: ${file}`); return m; }
    const svg = readFileSync(path, 'utf8').replace(/<\?xml[^>]*\?>/, '');
    return keep(`<figure>${svg}${cap ? `<figcaption>${md.renderInline(cap)}</figcaption>` : ''}</figure>`);
  });

  src = src.replace(/^\$\$\n([\s\S]*?)\n\$\$(?:[ \t]*\(([^\n]+)\))?/gm, (_, f, note) =>
    keep(`<div class="formula">${esc(f.trim())}${note ? `<small>${esc(note)}</small>` : ''}</div>`));

  const KIND = {
    key:   ['callout', '핵심 정리'],
    warn:  ['callout callout--warn', '흔한 실수'],
    ok:    ['callout callout--ok', '이렇게 하세요'],
    paper: ['callout callout--paper', '논문 작성 팁'],
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
  html = html.replace(/<p>\s*<!--BLK(\d+)-->\s*<\/p>/g, (_, i) => blocks[+i])
             .replace(/<!--BLK(\d+)-->/g, (_, i) => blocks[+i]);
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

function buildToc(cfg, chapters) {
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
    html += `<li><b>${esc(ch.meta.num || '')}</b><i>${esc(ch.meta.title || '')}</i></li>`;
  }
  if (open) html += '</ul>';
  return html + '</section>';
}

function buildChapter(ch) {
  return `
<section class="chapter">
  <header class="chapter__head">
    ${ch.meta.num ? `<span class="chapter__num">${esc(ch.meta.num)}</span>` : ''}
    <h1 class="chapter__title">${esc(ch.meta.title || '')}</h1>
    ${ch.meta.lead ? `<p class="chapter__lead">${esc(ch.meta.lead)}</p>` : ''}
  </header>
  ${ch.html}
</section>`;
}

function assemble(cfg, chapters) {
  const vars = Object.entries(cfg.accent || {}).map(([k, v]) => `--${k}: ${v};`).join(' ');
  return `<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<title>${esc(cfg.title || '')}</title>
<link rel="stylesheet" href="../../shared/theme/book.css">
${vars ? `<style>:root{${vars}}</style>` : ''}
</head><body>
${buildCover(cfg)}
${buildToc(cfg, chapters)}
${chapters.map(buildChapter).join('\n')}
</body></html>`;
}

/* ---------------------------------------------------------------- 렌더 */
async function renderPdf(htmlPath, pdfPath) {
  const browser = await chromium.launch({ executablePath: CHROME });
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
  writeFileSync(htmlPath, assemble(cfg, chapters));

  mkdirSync(join(ROOT, 'dist'), { recursive: true });
  const name = cfg.filename || slug;
  const pdfPath = join(ROOT, 'dist', `${name}.pdf`);

  await renderPdf(htmlPath, pdfPath);
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
