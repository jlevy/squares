#!/bin/bash
# Lineage of each certificate against its house and stated seed, two at a time (review L83).
# Usage: run_identity.sh SRC_DIR KNOWN_BEST_DIR OUT_DIR
set -u
PY=/home/user/squares/packing/.venv/bin/python3
HERE=$(cd "$(dirname "$0")" && pwd)
SRC=$1
KB=$2
OUT=$3
run() { nice -n 19 "$PY" -I -B "$HERE/l83_identity.py" "$1" "$SRC/s$1/n-$1-candidate.yaml" "$KB/n-$1.yaml" "$KB/n-$2.yaml" "$OUT/identity-n$1.json"; }
run 156 182 & run 180 154 & wait
run 268 302 & run 269 304 & wait
