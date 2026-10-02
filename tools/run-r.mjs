/**
 * 원고의 R 코드를 실제로 돌려 실행 결과 블록을 검증·갱신한다.
 *
 *   node tools/run-r.mjs 02-regression              모든 장 검사 (다르면 실패)
 *   node tools/run-r.mjs 02-regression 03 05        3장, 5장만
 *   node tools/run-r.mjs 02-regression 03 --write   결과 블록을 실제 출력으로 채움
 *
 * 규칙
 *   - 장마다 R 세션 하나. ```r 블록을 위에서부터 순서대로 실행한다.
 *     작업 폴더는 books/<권>/ 이므로 원고 속 "data/survey.csv"가 그대로 읽힌다.
 *   - ```r 블록 바로 뒤의 ```out 블록이 그 블록의 출력이다.
 *     출력은 콘솔에 찍히는 표준출력만 모은다(패키지 시작 메시지·경고는 제외).
 *   - install.packages()가 든 블록과, 바로 앞 줄이 <!-- norun --> 인 블록은 건너뛴다.
 *
 * R이 출력한 그대로를 책에 싣기 위한 도구다. 원고의 숫자는 이 출력과 맞춰 쓴다.
 */
import { readFileSync, writeFileSync, readdirSync, mkdtempSync, rmSync } from 'fs';
import { join, dirname } from 'path';
import { tmpdir } from 'os';
import { spawnSync } from 'child_process';
import { fileURLToPath } from 'url';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const args = process.argv.slice(2);
const WRITE = args.includes('--write');
const pos = args.filter(a => !a.startsWith('--'));
const slug = pos[0];
if (!slug) { console.error('사용법: node tools/run-r.mjs <권슬러그> [장번호...] [--write]'); process.exit(1); }
const BOOK = join(ROOT, 'books', slug);
const MAN = join(BOOK, 'manuscript');
const only = pos.slice(1);

const FENCE = /```r(?:[ \t]+[^\n]*)?\n([\s\S]*?)```\n?(?:[ \t]*\n)*(```out(?:[ \t]+[^\n]*)?\n)?/g;

function blocks(src) {
  const out = [];
  for (const m of src.matchAll(FENCE)) {
    const code = m[1];
    const before = src.slice(0, m.index).replace(/\s+$/, '');
    const norun = /<!--\s*norun\s*-->$/.test(before) || /install\.packages\(/.test(code);
    let outRange = null;
    if (m[2]) {
      const start = m.index + m[0].length;            // 결과 블록 본문 시작
      const end = src.indexOf('```', start);          // 결과 블록 닫는 울타리
      outRange = [start, end];
    }
    out.push({ code, norun, outRange });
  }
  return out;
}

function rLiteral(s) {
  // R의 raw string: r"---( ... )---"
  if (s.includes(')---"')) throw new Error('코드에 )---" 가 들어 있어 감쌀 수 없습니다.');
  return `r"---(${s})---"`;
}

function run(list) {
  const lines = [
    'options(width = 80, warn = 1)',
    'pdf(NULL)                       # plot()은 그리되 파일은 남기지 않는다',
    `setwd(${rLiteral(BOOK)})`,
    '.blk <- function(i, code) {',
    '  cat(sprintf("\\n@@BLOCK %d@@\\n", i))',
    '  ex <- tryCatch(parse(text = code, keep.source = FALSE),',
    '                 error = function(e) { cat("@@ERROR", conditionMessage(e), "\\n"); NULL })',
    '  for (e in ex) {',
    '    r <- tryCatch(withVisible(eval(e, globalenv())),',
    '                  error = function(err) { cat("@@ERROR", conditionMessage(err), "\\n"); NULL })',
    '    if (!is.null(r) && r$visible) print(r$value)',
    '  }',
    '}',
  ];
  list.forEach((b, i) => { if (!b.norun) lines.push(`.blk(${i}, ${rLiteral(b.code)})`); });
  lines.push('cat("\\n@@END@@\\n")');

  const dir = mkdtempSync(join(tmpdir(), 'run-r-'));
  const file = join(dir, 'chapter.R');
  writeFileSync(file, lines.join('\n'));
  const r = spawnSync('Rscript', ['--vanilla', file], {
    encoding: 'utf8', env: { ...process.env, LC_ALL: 'C.UTF-8', LANG: 'C.UTF-8' }, maxBuffer: 64 << 20,
  });
  rmSync(dir, { recursive: true, force: true });
  if (r.error) throw r.error;

  const res = {};
  const parts = r.stdout.split(/\n@@BLOCK (\d+)@@\n/);
  for (let k = 1; k < parts.length; k += 2) {
    res[+parts[k]] = parts[k + 1].replace(/\n@@END@@\n?$/, '').replace(/^\n+/, '').replace(/\s+$/, '');
  }
  // 한글 축 이름을 그림 장치(pdf)가 못 그려 나는 경고는 책 내용과 무관하므로 뺀다
  const warn = (r.stderr || '').split('\n')
    .filter(l => /^Warning|^경고|Error/.test(l) && !/in (title|text|axis|mtext)\(|conversion failure/.test(l));
  return { res, warn };
}

const files = readdirSync(MAN).filter(f => f.endsWith('.md')).sort()
  .filter(f => !only.length || only.some(n => f.startsWith(n.padStart(2, '0'))));

let bad = 0;
for (const f of files) {
  const path = join(MAN, f);
  let src = readFileSync(path, 'utf8');
  const list = blocks(src);
  if (!list.some(b => !b.norun)) continue;
  const { res, warn } = run(list);

  const problems = [];
  // 뒤에서부터 바꿔야 앞쪽 위치가 어긋나지 않는다
  for (let i = list.length - 1; i >= 0; i--) {
    const b = list[i];
    if (b.norun) continue;
    const got = res[i] ?? '';
    if (/@@ERROR/.test(got)) problems.push(`블록 ${i + 1}: 오류\n${got}`);
    if (!b.outRange) {
      if (got) problems.push(`블록 ${i + 1}: 출력이 있는데 결과 블록이 없음\n${got.split('\n').slice(0, 4).join('\n')}`);
      continue;
    }
    const [s, e] = b.outRange;
    const cur = src.slice(s, e).replace(/\s+$/, '');
    if (cur !== got) {
      if (WRITE) src = src.slice(0, s) + got + '\n' + src.slice(e);
      else problems.push(`블록 ${i + 1}: 결과가 다름`);
    }
  }
  if (WRITE) writeFileSync(path, src);
  const label = problems.length ? `[확인] ${f}` : `[OK]   ${f}`;
  console.log(`  ${label}  (코드 ${list.filter(b => !b.norun).length}개)`);
  problems.reverse().forEach(p => console.log('         ' + p.replace(/\n/g, '\n         ')));
  warn.slice(0, 6).forEach(w => console.log('         R: ' + w));
  bad += problems.length;
}
if (bad && !WRITE) { console.log(`\n${bad}건. --write 로 채우거나 원고를 고치세요.`); process.exit(1); }
