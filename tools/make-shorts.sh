#!/usr/bin/env bash
# 쇼츠·릴스 전편을 한 번에: 음성 → 영상
#   bash tools/make-shorts.sh            # 전부
#   bash tools/make-shorts.sh 01 03      # 번호로 골라서
#
# 새 컨테이너에서도 바로 돌도록, 없는 도구는 먼저 설치한다.
set -euo pipefail
cd "$(dirname "$0")/.."

[ -d node_modules ] || npm install --no-audit --no-fund
command -v ffmpeg >/dev/null || { apt-get update -qq && apt-get install -y -qq --no-install-recommends ffmpeg; }

if [ -z "${GEMINI_API_KEY:-}${GOOGLE_API_KEY:-}" ] && [ ! -f "$HOME/.config/ebook/gemini.key" ]; then
  echo "  ! GEMINI_API_KEY가 없어 무음 초안으로 만듭니다."
fi

sel=("$@")
for d in video/shorts/0*/; do
  d=${d%/}; n=$(basename "$d" | cut -d- -f1)
  if [ ${#sel[@]} -gt 0 ] && [[ ! " ${sel[*]} " =~ " $n " ]]; then continue; fi
  echo "== $(basename "$d")"
  node tools/tts.mjs "$d"
  node tools/render-short.mjs "$d"
done
