#!/bin/sh
# Rebuild the two large certificates of Theorem A's construction (not shipped: 12 MB and 49 MB)
# and check them against LARGE.sha256. Then check them with both exact checkers (a few minutes).
#   sh regenerate.sh [OUTDIR]          (default: ./large)
set -e
cd "$(dirname "$0")"
OUT=${1:-large}
mkdir -p "$OUT"
for k in 300 600; do python3 -I lband.py $k --out "$OUT/k$k.cert"; done
(cd "$OUT" && shasum -a 256 -c ../LARGE.sha256)
python3 -I windowed_check.py "$OUT/k300.cert" "$OUT/k600.cert"
