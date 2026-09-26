#!/usr/bin/env bash
# 쇼츠·릴스 전편을 한 번에: 음성 → 영상
#   bash tools/make-shorts.sh            # 전부
#   bash tools/make-shorts.sh 01 03      # 번호로 골라서
set -euo pipefail
cd "$(dirname "$0")/.."
sel=("$@")
for d in video/shorts/0*/; do
  d=${d%/}; n=$(basename "$d" | cut -d- -f1)
  if [ ${#sel[@]} -gt 0 ] && [[ ! " ${sel[*]} " =~ " $n " ]]; then continue; fi
  echo "== $(basename "$d")"
  node tools/tts.mjs "$d"
  node tools/render-short.mjs "$d"
done
