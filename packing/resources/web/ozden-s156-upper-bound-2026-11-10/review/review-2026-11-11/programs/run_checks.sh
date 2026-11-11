#!/bin/bash
# Decide the four certificates with the frozen checker, two at a time (review L83).
# Usage: run_checks.sh SRC_DIR OUT_DIR
set -u
PY=/home/user/squares/packing/.venv/bin/python3
HERE=$(cd "$(dirname "$0")" && pwd)
SRC=$1
OUT=$2
mkdir -p "$OUT"
run() { nice -n 19 "$PY" -I -B "$HERE/l83_check.py" "$SRC/s$1/n-$1-candidate.yaml" "$SRC/s$1/n$1-witness.json" "$OUT/check-n$1.json"; }
run 156 & run 180 & wait
run 268 & run 269 & wait
