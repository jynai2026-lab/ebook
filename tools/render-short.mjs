/**
 * 쇼츠 렌더: 타임라인대로 프레임을 찍고 내레이션과 합친다
 *
 *   node tools/tts.mjs          video/shorts/01-power     # 먼저 음성과 타임라인
 *   node tools/render-short.mjs video/shorts/01-power     # 그다음 영상
 *
 * 옵션
 *   --still 12.5   그 시점 한 장만 PNG로 (배치 확인용)
 *   --safe         플랫폼 UI가 덮는 곳을 붉게 칠해 본다
 *
 * 무음 초안이면 파일 이름 끝에 -draft를 붙인다.
 */
import { readFileSync, mkdirSync, rmSync, existsSync } from 'fs';
import { join, dirname, resolve, basename } from 'path';
import { fileURLToPath } from 'url';
import { execFileSync } from 'child_process';
import { launchBrowser } from './browser.mjs';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const FPS = 30;

const argv = process.argv.slice(2);
const dir = resolve(argv[0] || '');
const slug = basename(dir);
const tlPath = join(dir, 'build', 'timeline.json');
if (!existsSync(tlPath)) { console.error('먼저 node tools/tts.mjs ' + argv[0] + ' 를 돌리세요.'); process.exit(1); }
const TL = JSON.parse(readFileSync(tlPath, 'utf8'));
const stillAt = argv.includes('--still') ? Number(argv[argv.indexOf('--still') + 1]) : null;
const safe = argv.includes('--safe');

const outDir = join(ROOT, 'dist', 'shorts');
mkdirSync(outDir, { recursive: true });

const browser = await launchBrowser();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await page.addInitScript(tl => { window.TIMELINE = tl; }, TL);
// 페이지 쪽 오류가 조용히 묻혀 시간 초과로만 보이지 않게 한다
page.on('pageerror', e => console.error('  페이지 오류:', e.message));
await page.goto('file://' + join(dir, 'index.html') + (safe ? '?safe' : ''));
await page.waitForFunction(() => window.__ready === true, null, { timeout: 15000 });

if (stillAt !== null) {
  await page.evaluate(s => window.renderFrame(s), stillAt);
  const out = join(outDir, `${slug}@${stillAt}s${safe ? '-safe' : ''}.png`);
  await page.screenshot({ path: out });
  await browser.close();
  console.log('  ->', out.replace(ROOT + '/', ''));
  process.exit(0);
}

const frames = join(ROOT, '.frames', slug);
rmSync(frames, { recursive: true, force: true });
mkdirSync(frames, { recursive: true });

const n = Math.ceil(TL.total * FPS);
for (let i = 0; i < n; i++) {
  await page.evaluate(s => window.renderFrame(s), i / FPS);
  await page.screenshot({ path: join(frames, `f${String(i).padStart(5, '0')}.png`) });
}
await browser.close();

const out = join(outDir, `${slug}${TL.placeholder ? '-draft' : ''}.mp4`);
execFileSync('ffmpeg', ['-y', '-loglevel', 'error',
  '-framerate', String(FPS), '-i', join(frames, 'f%05d.png'),
  '-i', join(dir, 'build', 'narration.wav'),
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p',
  '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out]);
rmSync(frames, { recursive: true, force: true });

console.log(`  ${n}프레임 · ${TL.total.toFixed(1)}초${TL.placeholder ? ' (무음 초안)' : ''}  ->  ${out.replace(ROOT + '/', '')}`);
