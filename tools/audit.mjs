/**
 * 빌드 결과 점검
 *
 *  node tools/audit.mjs [권슬러그]        기본값 01-basic-statistics
 *
 * 렌더된 HTML(dist/*.html)을 훑어 다음을 잡아낸다.
 *   1) 복원되지 않은 자리표시자
 *   2) 처리되지 않은 **강조**, $수식$
 *   3) 그림 파일 누락 / 쓰이지 않는 그림
 *   4) 그림 번호가 장 안에서 순서대로인지
 *   5) 피하기로 한 어투와 단어
 */
import { readFileSync, readdirSync, existsSync } from 'fs';
import { join, dirname, basename } from 'path';
import { fileURLToPath } from 'url';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const BOOK = join(ROOT, 'books', process.argv[2] || '01-basic-statistics');
const MAN = join(BOOK, 'manuscript');
const FIGDIR = join(BOOK, 'figures');

let fail = 0;
const bad = (label, items) => {
  if (!items.length) { console.log(`  [OK]   ${label}`); return; }
  fail += items.length;
  console.log(`  [실패] ${label} — ${items.length}건`);
  items.slice(0, 8).forEach(i => console.log(`         ${i}`));
  if (items.length > 8) console.log(`         … 외 ${items.length - 8}건`);
};

// ---------------------------------------------------------------- 렌더 결과
const htmlPath = join(BOOK, ".build.html");
const html = readFileSync(htmlPath, "utf8");

bad('자리표시자 복원', [...html.matchAll(/<!--BLK\d+-->|\uE000\d+\uE001/g)].map(m => m[0]));

// 코드블록·수식 밖에 남은 마크다운 흔적
const stripped = html
  .replace(/<pre[\s\S]*?<\/pre>/g, '')
  .replace(/<code[\s\S]*?<\/code>/g, '')
  .replace(/<span class="katex[\s\S]*?<\/span><\/span>/g, '');
bad('처리되지 않은 **강조**', [...stripped.matchAll(/\*\*[^*\n]{1,40}\*\*/g)].map(m => m[0]));
bad('처리되지 않은 $수식$', [...stripped.matchAll(/\$[^$\n]{1,40}\$/g)].map(m => m[0]));
bad('빈 캡션 / 깨진 표', [...html.matchAll(/<figcaption>\s*<\/figcaption>/g)].map(() => '빈 figcaption'));
bad('조판되지 않은 그림 수식', [...html.matchAll(/data-tex="([^"]*)"/g)].map(m => m[1]));

const onDiskEarly = () => readdirSync(FIGDIR).filter(f => f.endsWith('.svg'));

// ---------------------------------------------------------------- 원고
const files = readdirSync(MAN).filter(f => f.endsWith('.md')).sort();
const used = new Set();
const missing = [];
const numbering = [];

for (const f of files) {
  const src = readFileSync(join(MAN, f), 'utf8');
  const ch = (src.match(/^num:\s*(\d+)/m)?.[1] ?? '').replace(/^0+/, '') || '0';

  for (const m of src.matchAll(/!fig\[[^\]]*\]\(([^)]+)\)/g)) {
    used.add(m[1]);
    if (!existsSync(join(FIGDIR, m[1]))) missing.push(`${f}: ${m[1]}`);
  }
  const caps = [...src.matchAll(/\*\*그림 (\d+)-(\d+)\*\*/g)];
  caps.forEach((m, i) => {
    if (m[1] !== ch || +m[2] !== i + 1) numbering.push(`${f}: 그림 ${m[1]}-${m[2]} (${ch}-${i + 1}이어야 함)`);
  });
}

bad('그림 파일 존재', missing);

// 그림 안의 수식은 <text>가 아니라 figlib.tex()로 조판해야 한다.
// 분수를 /로 쓰거나 근호를 √ 문자로 찍으면 본문 수식과 모양이 어긋난다.
const rawMath = [];
for (const f of onDiskEarly()) {
  const svg = readFileSync(join(FIGDIR, f), 'utf8');
  for (const m of svg.matchAll(/<text[^>]*>([^<]*)<\/text>/g)) {
    const t = m[1];
    if (/√|[∑Σ]|[A-Za-z가-힣]\s*[²³]|\b[A-Za-z]+\s*\/\s*[A-Za-z(]/.test(t)) rawMath.push(`${f}: "${t}"`);
  }
}
bad('그림 안에 <text>로 찍힌 수식', rawMath);
bad('그림 번호 순서', numbering);

const onDisk = onDiskEarly();
const orphan = onDisk.filter(f => !used.has(f));
if (orphan.length) console.log(`  [참고] 원고에서 쓰이지 않는 그림 ${orphan.length}개: ${orphan.join(', ')}`);

// ---------------------------------------------------------------- 어투
const BANNED = [
  '경위', '수행하', '수행해', '수행할', '상회', '하회', '귀속', '무상으로',
  '용이하', '제고하', '기하여야', '요망', '사료', '바람직할 것으로',
  '~해요', '했어요', '이에요', '거예요', '입니다만',
];
const register = [];
for (const f of files) {
  const src = readFileSync(join(MAN, f), 'utf8');
  src.split('\n').forEach((line, i) => {
    if (line.trimStart().startsWith('```') || /^\s{4}/.test(line)) return;
    for (const w of BANNED) if (line.includes(w)) register.push(`${f}:${i + 1} "${w}" — ${line.trim().slice(0, 56)}`);
  });
}
bad('피하기로 한 어투·단어', register);

// 원고 본문의 수식도 $...$ 로 감싸 KaTeX가 조판해야 한다.
// 유니코드 첨자·근호·X̄ 를 그냥 쓰면 본문 수식과 글꼴이 어긋난다.
const RAW = /√|[∑Σ]|[A-Za-z]\s*[²³]|[₀-₉]|[ᵢⱼₖ]|X̄/;
const prose = [];
for (const f of files) {
  let src = readFileSync(join(MAN, f), 'utf8')
    .replace(/```[\s\S]*?```/g, '')
    .replace(/\$\$[\s\S]*?\$\$/g, '')
    .replace(/\$[^\n$]*\$/g, '')
    .replace(/`[^`\n]*`/g, '');
  src.split('\n').forEach((line, i) => {
    const m = line.match(RAW);
    if (m) prose.push(`${f}:${i + 1} "${m[0]}" — ${line.trim().slice(0, 56)}`);
  });
}
bad('원고에 $ 없이 쓴 수식', prose);

console.log(fail ? `\n총 ${fail}건이 걸렸습니다.` : '\n모두 통과했습니다.');
process.exit(fail ? 1 : 0);
