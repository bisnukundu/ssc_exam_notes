#!/bin/bash
# Generic infographic renderer: HTML -> PNG via Chrome Headless Shell.
# Usage: tools/render-infographic.sh <html-file> <output-png> [width] [height]
# Defaults: landscape 1920x1080. Screenshots, then trims trailing whitespace.
set -e
HTML="$(readlink -f "$1")"
OUT="$2"
W="${3:-1920}"
H="${4:-1080}"
CH=~/workspace/.chrome-headless-shell/chrome-headless-shell-linux64/chrome-headless-shell
TMP=/tmp/infographic-raw.png
"$CH" --headless --disable-gpu --no-sandbox --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=${W},${H} \
  --screenshot="$TMP" "file://$HTML" 2>/dev/null
python3 - "$TMP" "$OUT" <<'EOF'
import sys
import numpy as np
from PIL import Image
im = Image.open(sys.argv[1]).convert("RGB")
w, h = im.size
a = np.asarray(im)
nonwhite = (a < 245).any(axis=2)
rows = np.where(nonwhite.any(axis=1))[0]
bottom = rows[-1] + 1 if len(rows) else h
bottom = min(bottom + 16, h)
im.crop((0, 0, w, bottom)).save(sys.argv[2], quality=92)
print("saved", sys.argv[2], (w, bottom))
EOF
