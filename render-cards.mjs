/**
 * 상세페이지 카드 렌더러 — landing/<권>/cards.html 의 .card 요소를 카드별 PNG로 뽑습니다.
 *
 *   node render-cards.mjs 01-basic-statistics
 *
 * 결과: dist/landing/<권>/card-01.png ...  (래피드 상세페이지에 순서대로 업로드)
 */
import { existsSync, mkdirSync, readdirSync, rmSync, statSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { launchBrowser } from './tools/browser.mjs';

const ROOT = dirname(fileURLToPath(import.meta.url));

const slug = process.argv[2] || '01-basic-statistics';
const htmlPath = join(ROOT, 'landing', slug, 'cards.html');
if (!existsSync(htmlPath)) {
  console.error(`cards.html 없음: ${htmlPath}`);
  process.exit(1);
}

const outDir = join(ROOT, 'dist', 'landing', slug);
if (existsSync(outDir)) {
  for (const f of readdirSync(outDir)) if (f.endsWith('.png')) rmSync(join(outDir, f));
}
mkdirSync(outDir, { recursive: true });

const browser = await launchBrowser();
const page = await browser.newPage({
  viewport: { width: 1080, height: 1350 },
  deviceScaleFactor: 2,          // 2x 레티나 — 래피드에서 선명하게 보이도록
});

await page.goto('file://' + htmlPath, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);

const cards = await page.$$('.card');
console.log(`카드 ${cards.length}장 렌더링\n`);

let total = 0;
let seq = 0;                       // data-name 없는 카드만 01부터 순번
for (let i = 0; i < cards.length; i++) {
  const custom = await cards[i].getAttribute('data-name');
  const name = custom || `card-${String(++seq).padStart(2, '0')}`;
  const file = join(outDir, `${name}.png`);
  await cards[i].screenshot({ path: file });
  const box = await cards[i].boundingBox();
  const kb = (statSync(file).size / 1024).toFixed(0);
  console.log(`  ${(name + '.png').padEnd(16)} ${box.width}x${Math.round(box.height)}  (@2x)  ${kb}KB`);
  total += Number(kb);
}

await browser.close();
console.log(`\n합계 ${(total / 1024).toFixed(1)}MB  ->  dist/landing/${slug}/`);
