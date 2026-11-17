#!/bin/bash
# Measure the construction statements for each certificate, two at a time (review L83).
# Usage: run_construct.sh SRC_DIR OUT_DIR
set -u
PY=/home/user/squares/packing/.venv/bin/python3
HERE=$(cd "$(dirname "$0")" && pwd)
SRC=$1
OUT=$2
run() { nice -n 19 "$PY" -I -B "$HERE/l83_construct.py" "$1" "$SRC/s$1/n-$1-candidate.yaml" "$SRC/s$1/n-$1-decimal-pose.yaml" "$OUT/check-n$1.json" "$OUT/construct-n$1.json"; }
run 156 & run 180 & wait
run 268 & run 269 & wait
