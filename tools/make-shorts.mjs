/**
 * 쇼츠·릴스 전편을 한 번에: 음성 → 영상  (macOS · Windows · Linux)
 *
 *   node tools/make-shorts.mjs            # 전부
 *   node tools/make-shorts.mjs 01 03      # 번호로 골라서
 */
import { existsSync, readdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { spawnSync } from 'child_process';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const run = (cmd, args) => {
  const r = spawnSync(cmd, args, { cwd: ROOT, stdio: 'inherit', shell: process.platform === 'win32' });
  if (r.status !== 0) process.exit(r.status || 1);
};
const has = cmd => spawnSync(cmd, ['-version'], { stdio: 'ignore', shell: process.platform === 'win32' }).status === 0;

if (!existsSync(join(ROOT, 'node_modules'))) run('npm', ['install', '--no-audit', '--no-fund']);

if (!has('ffmpeg')) {
  // 클라우드 컨테이너(리눅스 root)면 직접 깔고, 내 PC면 설치 방법을 알려 준다
  if (process.platform === 'linux' && process.getuid?.() === 0) {
    run('apt-get', ['update', '-qq']);
    run('apt-get', ['install', '-y', '-qq', '--no-install-recommends', 'ffmpeg']);
  } else {
    const how = { darwin: 'brew install ffmpeg', win32: 'winget install ffmpeg' }[process.platform]
             || 'sudo apt install ffmpeg';
    console.error(`ffmpeg가 필요합니다. 터미널에서  ${how}  를 실행한 뒤 다시 돌려 주세요.`);
    process.exit(1);
  }
}

const sel = process.argv.slice(2);
const dirs = readdirSync(join(ROOT, 'video', 'shorts'))
  .filter(d => /^\d\d-/.test(d))
  .filter(d => !sel.length || sel.includes(d.slice(0, 2)))
  .sort();

for (const d of dirs) {
  console.log(`== ${d}`);
  run(process.execPath, [join('tools', 'tts.mjs'), join('video', 'shorts', d)]);
  run(process.execPath, [join('tools', 'render-short.mjs'), join('video', 'shorts', d)]);
}
