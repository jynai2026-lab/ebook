/**
 * 개념 애니메이션 → MP4
 *
 *   node tools/render-video.mjs video/sampling.html sampling 8
 *
 * 페이지가 window.renderFrame(t) (t는 0~1)을 내놓으면, 그것을 프레임마다
 * 불러 스크린샷을 찍고 ffmpeg로 엮는다. 그림을 그리는 코드는 책의 SVG와
 * 같은 색·글꼴을 쓰므로 영상과 책의 모양이 따로 놀지 않는다.
 */
import { mkdirSync, rmSync, existsSync } from 'fs';
import { join, dirname, resolve } from 'path';
import { fileURLToPath } from 'url';
import { execFileSync } from 'child_process';
import { launchBrowser } from './browser.mjs';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));

const page_ = process.argv[2];
const name = process.argv[3] || 'out';
const seconds = Number(process.argv[4] || 8);
// 세로(쇼츠) 영상이면 1080x1920, 아니면 1280x720
const vertical = process.argv.includes('--vertical');
const SIZE = vertical ? { width: 1080, height: 1920 } : { width: 1280, height: 720 };
const FPS = 30;
if (!page_ || !existsSync(page_)) { console.error('쓸 HTML을 지정하세요.'); process.exit(1); }

const frames = join(ROOT, '.frames', name);
rmSync(frames, { recursive: true, force: true });
mkdirSync(frames, { recursive: true });

const browser = await launchBrowser();
const page = await browser.newPage({ viewport: SIZE, deviceScaleFactor: 1 });
page.on('pageerror', e => console.error('  페이지 오류:', e.message));
await page.goto('file://' + resolve(page_));
await page.waitForFunction(() => window.__ready === true, null, { timeout: 15000 });

const total = Math.round(seconds * FPS);
for (let i = 0; i < total; i++) {
  await page.evaluate(t => window.renderFrame(t), i / (total - 1));
  await page.screenshot({ path: join(frames, `f${String(i).padStart(4, '0')}.png`) });
}
await browser.close();

const out = join(ROOT, 'dist', `${name}.mp4`);
mkdirSync(join(ROOT, 'dist'), { recursive: true });
execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS),
  '-i', join(frames, 'f%04d.png'),
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p', out]);
rmSync(frames, { recursive: true, force: true });
console.log(`${total}프레임 · ${seconds}초  ->  dist/${name}.mp4`);
