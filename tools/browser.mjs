/**
 * 크롬 찾기 — 클라우드 컨테이너, macOS, Windows, Linux 어디서 돌려도 되게
 *
 * 순서: CHROME_PATH 환경변수 → 알려진 설치 경로 → 설치된 Google Chrome(channel)
 */
import { existsSync } from 'fs';
import { join } from 'path';
import { chromium } from 'playwright-core';

const local = process.env.LOCALAPPDATA || '';
const CANDIDATES = [
  process.env.CHROME_PATH,
  '/opt/pw-browsers/chromium/chrome-linux/chrome',                   // Claude 클라우드 컨테이너
  '/opt/pw-browsers/chromium',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',    // macOS
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',      // Windows
  'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
  local && join(local, 'Google', 'Chrome', 'Application', 'chrome.exe'),
  '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser',
];

export async function launchBrowser() {
  const path = CANDIDATES.find(p => p && existsSync(p));
  if (path) return chromium.launch({ executablePath: path });
  try {
    return await chromium.launch({ channel: 'chrome' });
  } catch {
    throw new Error('크롬을 찾지 못했습니다. Google Chrome을 설치하거나, CHROME_PATH 환경변수로 크롬 경로를 알려 주세요.');
  }
}
