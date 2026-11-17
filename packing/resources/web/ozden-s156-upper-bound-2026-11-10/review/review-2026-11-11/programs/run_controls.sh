#!/bin/bash
# Run the stated controls on the four certificates, two at a time (review L83).
# Usage: run_controls.sh SRC_DIR OUT_DIR
set -u
PY=/home/user/squares/packing/.venv/bin/python3
HERE=$(cd "$(dirname "$0")" && pwd)
SRC=$1
OUT=$2
run() { nice -n 19 "$PY" -I -B "$HERE/l83_controls.py" "$1" "$SRC/s$1/n-$1-candidate.yaml" "$HERE/controls-plan.json" "$OUT/controls-n$1.json"; }
run 156 & run 180 & wait
run 268 & run 269 & wait
