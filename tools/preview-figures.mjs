/**
 * 그림 검수용 대지(contact sheet)
 *
 *   node tools/preview-figures.mjs [이름조각 ...]
 *
 * 그림을 본문과 똑같은 조건(KaTeX 조판 + 본문 폰트)으로 한 장에 늘어놓고
 * PNG로 떨군다. 이름조각을 주면 그것이 들어간 그림만 그린다.
 * 글자 겹침이나 잘림은 이 대지에서 잡는 편이 PDF를 뒤지는 것보다 빠르다.
 */
import { readFileSync, writeFileSync, readdirSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { chromium } from 'playwright-core';
import katex from 'katex';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const FIG = join(ROOT, 'books', '01-basic-statistics', 'figures');
const OUT = join(ROOT, '.figpreview');
const CHROME = process.env.CHROME_PATH || '/opt/pw-browsers/chromium';

/** build.mjs 의 renderFigTex 와 같은 일을 한다 */
const renderFigTex = svg => svg.replace(/<span data-tex="([^"]*)"\s*><\/span>/g, (_, raw) => {
  const latex = raw.replace(/&quot;/g, '"').replace(/&gt;/g, '>')
                   .replace(/&lt;/g, '<').replace(/&amp;/g, '&');
  return katex.renderToString(latex, { throwOnError: false, strict: false, output: 'html' });
});

const want = process.argv.slice(2);
const names = readdirSync(FIG).filter(f => f.endsWith('.svg'))
  .filter(f => !want.length || want.some(w => f.includes(w)))
  .sort();
if (!names.length) { console.log('해당하는 그림이 없습니다.'); process.exit(1); }

const cards = names.map(n =>
  `<div class="c"><div class="t">${n}</div>${renderFigTex(readFileSync(join(FIG, n), 'utf8'))}</div>`
).join('\n');

mkdirSync(OUT, { recursive: true });
const html = `<!doctype html><meta charset="utf-8">
<link rel="stylesheet" href="${join(ROOT, 'shared/theme/fonts.css')}">
<link rel="stylesheet" href="${join(ROOT, 'shared/theme/katex.min.css')}">
<style>
  body { margin:0; padding:16px; background:#fff; font-family:Pretendard, sans-serif; }
  .c { margin-bottom:18px; border:1px solid #E4E7EC; border-radius:8px; padding:10px; }
  .t { font-size:11px; color:#98A2B3; margin-bottom:6px; }
  svg { width:100%; height:auto; display:block; }
  .figtex { display:flex; align-items:center; width:100%; height:100%; line-height:1; }
  .figtex .katex { font-size:1em; }
</style>${cards}`;
const htmlPath = join(OUT, 'sheet.html');
writeFileSync(htmlPath, html);

const browser = await chromium.launch({ executablePath: CHROME });
const page = await browser.newPage({ viewport: { width: 1000, height: 1600 } });
await page.goto('file://' + htmlPath);
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(300);
const h = await page.evaluate(() => document.body.scrollHeight);
const parts = Math.ceil(h / 1600);
for (let i = 0; i < parts; i++) {
  await page.evaluate(y => window.scrollTo(0, y), i * 1600);
  await page.waitForTimeout(150);
  await page.screenshot({ path: join(OUT, `sheet-${i}.png`) });
}
await browser.close();
console.log(`그림 ${names.length}개 → ${parts}장  (.figpreview/sheet-*.png)`);
