#!/bin/bash
# One final run of every L83 program over the kept bytes, at most two processes at nice 19.
# Usage: run_all.sh SRC_DIR REPO_ROOT OUT_DIR
# SRC_DIR holds the clones s156, s180, s268, s269; REPO_ROOT is a jlevy/squares checkout at
# main f54ad1048; OUT_DIR must already hold the four plan-facts receipts kept from the plan.
set -eu
PY=/home/user/squares/packing/.venv/bin/python3
HERE=$(cd "$(dirname "$0")" && pwd)
SRC=$1
REPO=$2
OUT=$3
KB=$REPO/packing/witnesses/known-best
p() { nice -n 19 "$PY" -I -B "$HERE/$@"; }
p l83_selftest.py "$OUT/selftest.json"
bash "$HERE/run_checks.sh" "$SRC" "$OUT"
bash "$HERE/run_controls.sh" "$SRC" "$OUT"
p l83_sides.py "$SRC" "$KB" "$HERE/issue-statements.json" "$OUT/sides.json"
p l83_houses.py 156 "$KB" "$OUT/houses-n156.json" & p l83_houses.py 268 "$KB" "$OUT/houses-n268.json" & wait
p l83_houses.py 180 "$KB" "$OUT/houses-n180.json" & p l83_houses.py 269 "$KB" "$OUT/houses-n269.json" & wait
p l83_shares.py "$OUT" "$OUT/shares.json"
bash "$HERE/run_identity.sh" "$SRC" "$KB" "$OUT"
bash "$HERE/run_construct.sh" "$SRC" "$OUT"
p l83_custody.py "$SRC" "$REPO" "$HERE/issue-statements.json" "$OUT/custody.json"
