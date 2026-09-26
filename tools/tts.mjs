/**
 * 쇼츠 내레이션 만들기
 *
 *   node tools/tts.mjs video/shorts/01-power
 *
 * script.json의 beats[].say 를 한 문장씩 음성으로 만들고, 각 길이를 재서
 * 타임라인을 짠다. 영상은 이 타임라인을 따라 움직이므로 싱크가 어긋나지 않는다.
 *
 *   키 있음  →  Google Gemini TTS로 실제 음성을 만든다
 *   키 없음  →  문장 길이로 어림한 무음을 넣는다 (화면 초안 확인용)
 *   키 위치: GEMINI_API_KEY 환경변수, 또는 ~/.config/ebook/gemini.key
 *
 * 같은 문장·목소리·모델이면 다시 부르지 않고 캐시를 쓴다. 무료 한도를 아끼려는 것.
 *
 * 결과:  <dir>/build/narration.wav,  <dir>/build/timeline.json
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync, rmSync } from 'fs';
import { join, dirname, resolve } from 'path';
import { fileURLToPath } from 'url';
import { execFileSync } from 'child_process';
import { createHash } from 'crypto';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const dir = resolve(process.argv[2] || '');
if (!existsSync(join(dir, 'script.json'))) {
  console.error('script.json이 있는 쇼츠 폴더를 지정하세요.'); process.exit(1);
}
const script = JSON.parse(readFileSync(join(dir, 'script.json'), 'utf8'));

// 키는 환경변수 또는 저장소 밖의 파일(~/.config/ebook/gemini.key)에서 읽는다.
// 저장소 안에는 절대 두지 않는다.
const KEY_FILE = join(process.env.HOME || '/root', '.config', 'ebook', 'gemini.key');
const KEY = (process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY
             || (existsSync(KEY_FILE) ? readFileSync(KEY_FILE, 'utf8') : '')).trim();
const API = 'https://generativelanguage.googleapis.com/v1beta';
const RATE = 24000;                 // 모든 조각을 이 표본율로 맞춘다
const LEAD = 0.35, GAP = 0.2, TAIL = 2.8;   // 앞 여백, 문장 사이, 끝 안내 카드

const build = join(dir, 'build');
const cache = join(ROOT, 'video', '.cache', 'tts');
mkdirSync(build, { recursive: true });
mkdirSync(cache, { recursive: true });

const ff = args => execFileSync('ffmpeg', ['-y', '-loglevel', 'error', ...args]);
const duration = f => Number(execFileSync('ffprobe',
  ['-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', f]).toString().trim());
const silence = (sec, out) =>
  ff(['-f', 'lavfi', '-i', `anullsrc=r=${RATE}:cl=mono`, '-t', sec.toFixed(3), '-c:a', 'pcm_s16le', out]);
const sleep = ms => new Promise(r => setTimeout(r, ms));

/* ---------------------------------------------------------------- Gemini 호출 */

// Node의 fetch는 이 환경의 프록시 설정을 따르지 않아 curl로 부른다.
// 키는 명령줄 인자에 드러나지 않도록 설정을 표준입력(-K -)으로 넘긴다.
function call(method, url, bodyPath, outPath) {
  const args = ['-sS', '-K', '-', '-X', method, '-o', outPath, '-w', '%{http_code}'];
  if (bodyPath) args.push('-H', 'Content-Type: application/json', '--data-binary', '@' + bodyPath);
  args.push(url);
  const code = execFileSync('curl', args, { input: `header = "x-goog-api-key: ${KEY}"\n` }).toString();
  let body = {};
  try { body = JSON.parse(readFileSync(outPath, 'utf8')); } catch { /* 본문이 JSON이 아닐 수 있다 */ }
  return { code: Number(code), body };
}

async function pickModel() {
  if (process.env.GEMINI_TTS_MODEL) return process.env.GEMINI_TTS_MODEL;
  const out = join(build, '.models.json');
  const { code, body } = call('GET', `${API}/models?pageSize=200`, null, out);
  rmSync(out, { force: true });
  if (code !== 200) throw new Error(`모델 목록을 받지 못했습니다 (HTTP ${code}): ${body?.error?.message || ''}`);
  const names = (body.models || []).map(m => m.name.replace(/^models\//, '')).filter(n => /tts/i.test(n));
  if (!names.length) throw new Error('TTS 모델을 찾지 못했습니다. GEMINI_TTS_MODEL 환경변수로 지정하세요.');
  // 정식판 flash > 미리보기 flash > 그 밖의 순서로 고른다
  return names.find(n => /flash/.test(n) && !/preview/.test(n))
      || names.find(n => /flash/.test(n))
      || names.sort()[0];
}

async function synth(model, text, voice, out) {
  const req = join(build, '.req.json'), res = join(build, '.res.json'), pcm = join(build, '.clip.pcm');
  writeFileSync(req, JSON.stringify({
    contents: [{ parts: [{ text }] }],
    generationConfig: {
      responseModalities: ['AUDIO'],
      speechConfig: { voiceConfig: { prebuiltVoiceConfig: { voiceName: voice } } },
    },
  }));

  for (let attempt = 1; attempt <= 5; attempt++) {
    const { code, body } = call('POST', `${API}/models/${model}:generateContent`, req, res);
    if (code === 200) {
      const part = body.candidates?.[0]?.content?.parts?.find(p => p.inlineData);
      if (!part) throw new Error('응답에 음성이 없습니다: ' + JSON.stringify(body).slice(0, 300));
      const rate = Number(/rate=(\d+)/.exec(part.inlineData.mimeType || '')?.[1] || 24000);
      writeFileSync(pcm, Buffer.from(part.inlineData.data, 'base64'));
      ff(['-f', 's16le', '-ar', String(rate), '-ac', '1', '-i', pcm,
          '-ar', String(RATE), '-ac', '1', '-c:a', 'pcm_s16le', out]);
      [req, res, pcm].forEach(f => rmSync(f, { force: true }));
      return;
    }
    // 무료 한도에 걸리면 서버가 알려 준 만큼 기다렸다 다시 부른다
    if (code === 429 || code === 503) {
      const hint = body?.error?.details?.find(d => d.retryDelay)?.retryDelay;
      const wait = hint ? parseFloat(hint) * 1000 + 500 : 15000 * attempt;
      console.log(`    한도에 걸렸습니다 (HTTP ${code}). ${(wait / 1000).toFixed(0)}초 뒤 다시 시도합니다 (${attempt}/5)`);
      await sleep(wait);
      continue;
    }
    throw new Error(`TTS 호출 실패 (HTTP ${code}): ${body?.error?.message || JSON.stringify(body).slice(0, 300)}`);
  }
  throw new Error('TTS 한도에 계속 걸립니다. 잠시 뒤 다시 돌리면 이미 만든 문장은 캐시에서 이어집니다.');
}

/* ---------------------------------------------------------------- 무음 초안 */

/** 한국어 낭독 속도(초당 약 6.8음절)로 문장 길이를 어림한다 */
function estimate(say) {
  const syl = (say.match(/[가-힣]/g) || []).length
            + (say.match(/[0-9]/g) || []).length
            + (say.match(/[A-Za-z]/g) || []).length * 0.4;
  return Math.max(1.2, syl / 6.8 + 0.3);
}

/* ---------------------------------------------------------------- 메인 */

const voice = script.voice || 'Charon';
const style = script.style || '';
const placeholder = !KEY;
const model = placeholder ? null : await pickModel();

console.log(placeholder
  ? '  GEMINI_API_KEY가 없어 무음 초안으로 만듭니다 (길이는 어림값).'
  : `  모델 ${model} · 목소리 ${voice}`);

const clips = [];
for (const [k, b] of script.beats.entries()) {
  let clip;
  if (placeholder) {
    clip = join(build, `.ph-${k}.wav`);
    silence(estimate(b.say), clip);
  } else {
    const text = style ? `${style} ${b.say}` : b.say;
    const hash = createHash('sha1').update([model, voice, text].join('\u0000')).digest('hex').slice(0, 16);
    clip = join(cache, `${hash}.wav`);
    if (!existsSync(clip)) {
      console.log(`    [${k + 1}/${script.beats.length}] ${b.id}`);
      await synth(model, text, voice, clip);
    }
  }
  clips.push({ ...b, file: clip, dur: duration(clip) });
}

// 타임라인: 앞 여백 → 문장 → 틈 → 문장 … → 끝 안내 카드
const parts = [];
const lead = join(build, '.lead.wav'), gap = join(build, '.gap.wav'), tail = join(build, '.tail.wav');
silence(LEAD, lead); silence(GAP, gap); silence(TAIL, tail);

let t = LEAD;
const beats = clips.map((c, k) => {
  parts.push(c.file);
  parts.push(k < clips.length - 1 ? gap : tail);
  const out = { id: c.id, start: +t.toFixed(3), end: +(t + c.dur).toFixed(3), cap: c.cap || c.say };
  t += c.dur + (k < clips.length - 1 ? GAP : 0);
  return out;
});
const total = +(t + TAIL).toFixed(3);

const list = join(build, '.concat.txt');
writeFileSync(list, [lead, ...parts].map(f => `file '${f.replace(/'/g, "'\\''")}'`).join('\n'));
ff(['-f', 'concat', '-safe', '0', '-i', list, '-c:a', 'pcm_s16le', join(build, 'narration.wav')]);

writeFileSync(join(build, 'timeline.json'),
  JSON.stringify({ total, placeholder, voice: placeholder ? null : voice, model, beats }, null, 2));

// 초안용 무음 조각은 지운다 (캐시와 달리 다시 쓸 일이 없다)
for (const f of [list, lead, gap, tail, ...clips.filter(c => placeholder).map(c => c.file)]) rmSync(f, { force: true });

console.log(`  ${beats.length}문장 · ${total.toFixed(1)}초  ->  ${join(dir.replace(ROOT + '/', ''), 'build')}/`);
