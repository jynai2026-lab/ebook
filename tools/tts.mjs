/**
 * 쇼츠 내레이션 만들기
 *
 *   node tools/tts.mjs video/shorts/01-power
 *
 * 한 편의 문장을 한 번에 읽혀(호출 1번) 음성을 만들고, 문장 사이 쉼을 찾아
 * 문장별 발화 구간을 잰다. 화면은 이 구간을 따라 움직이므로 싱크가 맞는다.
 *
 * 왜 한 번에 읽히는가
 *   Gemini TTS 무료 한도는 모델마다 하루 10번이다. 문장마다 부르면 5편에
 *   31번이 들지만, 한 편씩 부르면 5번이면 끝난다. 이어서 읽으니 억양도
 *   자연스럽고, 원본 음성을 자르지 않고 그대로 쓰므로 이음매도 없다.
 *
 *   키 있음  →  Google Gemini TTS로 실제 음성을 만든다
 *   키 없음  →  문장 길이로 어림한 무음을 넣는다 (화면 초안 확인용)
 *   키 위치: GEMINI_API_KEY 환경변수, 또는 ~/.config/ebook/gemini.key
 *
 * 결과:  <dir>/build/narration.wav,  <dir>/build/timeline.json
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync, rmSync, copyFileSync } from 'fs';
import { join, dirname, resolve } from 'path';
import { fileURLToPath } from 'url';
import { execFileSync, spawnSync } from 'child_process';
import { createHash } from 'crypto';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const dir = resolve(process.argv[2] || '');
if (!existsSync(join(dir, 'script.json'))) {
  console.error('script.json이 있는 쇼츠 폴더를 지정하세요.'); process.exit(1);
}
const script = JSON.parse(readFileSync(join(dir, 'script.json'), 'utf8'));
const beats = script.beats;

// 키는 환경변수 또는 저장소 밖의 파일에서 읽는다. 저장소 안에는 절대 두지 않는다.
const KEY_FILE = join(process.env.HOME || process.env.USERPROFILE || '/root', '.config', 'ebook', 'gemini.key');
const KEY = (process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY
             || (existsSync(KEY_FILE) ? readFileSync(KEY_FILE, 'utf8') : '')).trim();
const API = 'https://generativelanguage.googleapis.com/v1beta';
const RATE = 24000;
const LEAD = 0.35, TAIL = 2.8;      // 앞 여백, 끝 안내 카드

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

/** 읽는 길이의 어림 단위: 한글 음절 1, 숫자 1, 로마자 0.4 */
const weight = s => (s.match(/[가-힣]/g) || []).length + (s.match(/[0-9]/g) || []).length
                  + (s.match(/[A-Za-z]/g) || []).length * 0.4;

/* ---------------------------------------------------------------- Gemini 호출 */

// Node의 fetch는 클라우드 환경의 프록시 설정을 따르지 않아 curl로 부른다.
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

/** 쓸 수 있는 TTS 모델을 선호 순으로: 정식판 > 미리보기, 일반 > lite, 새 버전 > 옛 버전 */
function models() {
  if (process.env.GEMINI_TTS_MODEL) return [process.env.GEMINI_TTS_MODEL];
  const out = join(build, '.models.json');
  const { code, body } = call('GET', `${API}/models?pageSize=300`, null, out);
  rmSync(out, { force: true });
  if (code !== 200) throw new Error(`모델 목록을 받지 못했습니다 (HTTP ${code}): ${body?.error?.message || ''}`);
  const names = (body.models || []).map(m => m.name.replace(/^models\//, '')).filter(n => /tts/i.test(n));
  if (!names.length) throw new Error('TTS 모델을 찾지 못했습니다. GEMINI_TTS_MODEL 환경변수로 지정하세요.');
  const ver = n => parseFloat((n.match(/(\d+\.\d+)/) || [0, 0])[1]);
  const rank = n => [/preview/.test(n) ? 1 : 0, /lite/.test(n) ? 1 : 0, -ver(n), /pro/.test(n) ? 1 : 0];
  return names.sort((a, b) => {
    const ra = rank(a), rb = rank(b);
    for (let i = 0; i < ra.length; i++) if (ra[i] !== rb[i]) return ra[i] - rb[i];
    return 0;
  });
}

class DailyQuota extends Error {}

async function synth(model, text, voice, out) {
  const req = join(build, '.req.json'), res = join(build, '.res.json'), pcm = join(build, '.clip.pcm');
  writeFileSync(req, JSON.stringify({
    contents: [{ parts: [{ text }] }],
    generationConfig: {
      responseModalities: ['AUDIO'],
      speechConfig: { voiceConfig: { prebuiltVoiceConfig: { voiceName: voice } } },
    },
  }));
  try {
    for (let attempt = 1; attempt <= 4; attempt++) {
      const { code, body } = call('POST', `${API}/models/${model}:generateContent`, req, res);
      if (code === 200) {
        const part = body.candidates?.[0]?.content?.parts?.find(p => p.inlineData);
        if (!part) throw new Error('응답에 음성이 없습니다: ' + JSON.stringify(body).slice(0, 300));
        const rate = Number(/rate=(\d+)/.exec(part.inlineData.mimeType || '')?.[1] || 24000);
        writeFileSync(pcm, Buffer.from(part.inlineData.data, 'base64'));
        ff(['-f', 's16le', '-ar', String(rate), '-ac', '1', '-i', pcm,
            '-ar', String(RATE), '-ac', '1', '-c:a', 'pcm_s16le', out]);
        return;
      }
      if (code === 429) {
        // 하루 한도면 기다려도 소용없다. 다음 모델로 넘긴다.
        const quota = (body?.error?.details || []).flatMap(d => d.violations || []).map(v => v.quotaId || '');
        if (quota.some(q => /PerDay/i.test(q))) throw new DailyQuota(model);
        const hint = body?.error?.details?.find(d => d.retryDelay)?.retryDelay;
        const wait = hint ? parseFloat(hint) * 1000 + 500 : 20000 * attempt;
        console.log(`    분당 한도에 걸렸습니다. ${(wait / 1000).toFixed(0)}초 뒤 다시 시도합니다 (${attempt}/4)`);
        await sleep(wait);
        continue;
      }
      if (code === 503) { await sleep(10000 * attempt); continue; }
      throw new Error(`TTS 호출 실패 (HTTP ${code}): ${body?.error?.message || JSON.stringify(body).slice(0, 300)}`);
    }
    throw new Error('TTS 서버가 계속 응답하지 않습니다. 잠시 뒤 다시 돌려 주세요.');
  } finally {
    [req, res, pcm].forEach(f => rmSync(f, { force: true }));
  }
}

/* ---------------------------------------------------------------- 문장 경계 찾기 */

/** 무음 구간 목록 [start, end] */
function silences(file, db = -40, min = 0.18) {
  // silencedetect는 결과를 표준오류로 낸다
  const out = spawnSync('ffmpeg', ['-i', file, '-af', `silencedetect=noise=${db}dB:d=${min}`,
    '-f', 'null', '-'], { encoding: 'utf8' }).stderr;
  const s = [...out.matchAll(/silence_start: ([\d.]+)/g)].map(m => +m[1]);
  const e = [...out.matchAll(/silence_end: ([\d.]+)/g)].map(m => +m[1]);
  return s.map((a, i) => [a, e[i] ?? duration(file)]);
}

/**
 * 통으로 읽힌 음성에서 비트별 발화 구간을 찾는다.
 *
 * 한 비트에 문장이 둘 이상이면 비트 안의 문장 사이 쉼도 비트 사이 쉼만큼 길다.
 * 그래서 비트가 아니라 **문장 경계를 모두** 한꺼번에 고른 뒤 비트로 묶는다.
 * 문장 끝 쉼(0.35~1.2초)은 쉼표에서의 쉼(0.2~0.35초)보다 길다. 문장 경계 수만큼
 * 쉼을 순서대로 고르되, 쉼이 길수록, 문장 길이 비율로 어림한 자리에 가까울수록
 * 점수를 높게 준다(동적 계획법으로 합이 가장 큰 조합).
 */
function sentences(text) {
  return text.trim().split(/(?<=[.?!])\s+/).filter(Boolean);
}

function segment(file, texts) {
  const total = duration(file);
  const sil = silences(file);
  const speechStart = sil.length && sil[0][0] < 0.05 ? sil[0][1] : 0;
  const last = sil[sil.length - 1];
  const speechEnd = last && last[1] >= total - 0.05 ? last[0] : total;
  const pauses = sil.filter(([a, b]) => a > speechStart + 0.05 && b < speechEnd - 0.05);

  // 문장 목록과 각 문장이 속한 비트
  const sents = texts.flatMap((t, k) => sentences(t).map(x => ({ beat: k, w: weight(x) })));
  const W = sents.reduce((a, x) => a + x.w, 0);
  const len = speechEnd - speechStart, avg = len / sents.length;
  const K = sents.length - 1, m = pauses.length;
  if (m < K) throw new Error(`문장 경계 ${K}곳에 비해 쉼이 ${m}곳뿐입니다. 음성을 확인해 주세요.`);

  const expect = [];
  for (let k = 0, cum = 0; k < K; k++) { cum += sents[k].w; expect.push(speechStart + len * cum / W); }
  const score = (k, j) => {
    const [a, b] = pauses[j];
    return (b - a) - 0.2 * Math.abs((a + b) / 2 - expect[k]) / avg;
  };
  // dp[k][j]: 경계 k를 쉼 j에 둘 때까지의 최고 점수
  const dp = [], from = [];
  for (let k = 0; k < K; k++) {
    dp.push(new Array(m).fill(-Infinity)); from.push(new Array(m).fill(-1));
    let best = -Infinity, arg = -1;
    for (let j = k; j <= m - (K - k); j++) {
      if (k === 0) { dp[k][j] = score(k, j); continue; }
      if (dp[k - 1][j - 1] > best) { best = dp[k - 1][j - 1]; arg = j - 1; }
      dp[k][j] = best + score(k, j); from[k][j] = arg;
    }
  }
  const cut = new Array(K);
  if (K) {
    let j = dp[K - 1].reduce((bi, v, i, arr) => (v > arr[bi] ? i : bi), 0);
    for (let k = K - 1; k >= 0; k--) { cut[k] = pauses[j]; j = from[k][j]; }
  }

  // 문장 구간 → 비트 구간
  const out = texts.map(() => ({ start: Infinity, end: -Infinity, share: 0 }));
  sents.forEach((x, i) => {
    const o = out[x.beat];
    o.start = Math.min(o.start, i === 0 ? speechStart : cut[i - 1][1]);
    o.end = Math.max(o.end, i === K ? speechEnd : cut[i][0]);
    o.share += x.w / W;
  });
  return out;
}

/* ---------------------------------------------------------------- 메인 */

const voice = script.voice || 'Charon';
const narration = join(build, 'narration.wav');
let timeline;

if (!KEY) {
  // 무음 초안: 문장 길이를 어림해 타임라인만 짠다
  console.log('  키가 없어 무음 초안으로 만듭니다 (길이는 어림값).');
  let t = LEAD;
  const out = beats.map(b => {
    const d = Math.max(1.2, weight(b.say) / 6.8 + 0.3);
    const r = { id: b.id, start: +t.toFixed(3), end: +(t + d).toFixed(3), cap: b.cap || b.say };
    t += d + 0.28;
    return r;
  });
  const total = +(out[out.length - 1].end + TAIL).toFixed(3);
  silence(total, narration);
  timeline = { total, placeholder: true, voice: null, model: null, beats: out };
} else {
  // 문장 사이를 빈 줄로 띄워 읽히면 문장 경계에서 확실히 쉰다
  const text = beats.map(b => b.say.trim()).join('\n\n');
  let model, raw;
  for (const m of models()) {
    const hash = createHash('sha1').update([m, voice, text].join('\u0000')).digest('hex').slice(0, 16);
    const file = join(cache, `${hash}.wav`);
    if (existsSync(file)) { model = m; raw = file; break; }
    try {
      console.log(`  모델 ${m} · 목소리 ${voice} — 한 편을 한 번에 읽힙니다`);
      await synth(m, text, voice, file);
      model = m; raw = file; break;
    } catch (e) {
      if (!(e instanceof DailyQuota)) throw e;
      console.log(`    ${m}: 오늘 무료 한도(하루 10번)를 다 썼습니다. 다음 모델로 넘어갑니다.`);
    }
  }
  if (!raw) throw new Error('모든 TTS 모델의 오늘 무료 한도를 다 썼습니다. 내일 다시 돌리면 만든 편은 캐시에서 이어집니다.');

  const seg = segment(raw, beats.map(b => b.say));
  // 앞뒤 무음만 잘라 쓰고, 문장 사이는 원래 쉼을 그대로 둔다
  const s0 = seg[0].start, s1 = seg[seg.length - 1].end;
  const body = join(build, '.body.wav'), lead = join(build, '.lead.wav'), tail = join(build, '.tail.wav');
  ff(['-i', raw, '-ss', s0.toFixed(3), '-to', s1.toFixed(3), '-c:a', 'pcm_s16le', body]);
  silence(LEAD, lead); silence(TAIL, tail);
  const list = join(build, '.concat.txt');
  writeFileSync(list, [lead, body, tail].map(f => `file '${f.replace(/'/g, "'\\''")}'`).join('\n'));
  ff(['-f', 'concat', '-safe', '0', '-i', list, '-c:a', 'pcm_s16le', narration]);
  [body, lead, tail, list].forEach(f => rmSync(f, { force: true }));

  const out = beats.map((b, k) => ({
    id: b.id,
    start: +(LEAD + seg[k].start - s0).toFixed(3),
    end: +(LEAD + seg[k].end - s0).toFixed(3),
    cap: b.cap || b.say,
  }));
  const total = +(LEAD + (s1 - s0) + TAIL).toFixed(3);
  timeline = { total, placeholder: false, voice, model, beats: out };

  // 경계가 제대로 잡혔는지 볼 수 있게 문장별 길이와 예상 비율을 보여 준다
  const len = s1 - s0;
  for (const [k, b] of beats.entries()) {
    const d = seg[k].end - seg[k].start, ratio = d / (len * seg[k].share);
    console.log(`    ${b.id.padEnd(9)} ${d.toFixed(2)}초  (예상 대비 ${ratio.toFixed(2)}배)${ratio < 0.55 || ratio > 1.8 ? '  ← 경계 확인 필요' : ''}`);
  }
}

writeFileSync(join(build, 'timeline.json'), JSON.stringify(timeline, null, 2));
console.log(`  ${beats.length}문장 · ${timeline.total.toFixed(1)}초  ->  ${join(dir.replace(ROOT + '/', ''), 'build')}/`);
