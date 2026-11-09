#!/usr/bin/env bash
# Rerun every program of lane L64's review of issues 927 to 931, in order.
# Usage: run_all.sh PYTHON SRC REPO_ROOT OUT
#   PYTHON     CPython 3.14 with gmpy2, PyYAML, NumPy and SciPy (the project's packing/.venv)
#   SRC        a directory holding clones of the five kenaznia-doga repositories at their pins
#   REPO_ROOT  a checkout of jlevy/squares at 19b354a5c (the houses, views and register)
#   OUT        where the receipts go
set -euo pipefail
PY="$1"
SRC="$2"
REPO="$3"
OUT="$4"
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$OUT"
run() { nice -n 19 "$PY" -I -B "$@"; }
run "$HERE/l64_selftest.py" "$OUT/selftest.json" "$OUT/selftest-files"
bash "$HERE/run_checks.sh" "$PY" "$SRC" "$OUT"
run "$HERE/l64_sides.py" "$HERE/issue-statements.json" "$SRC" "$REPO/packing/witnesses/known-best" \
  "$REPO/packing/frontier/results.yaml" "$OUT/sides.json"
run "$HERE/l64_custody.py" "$HERE/issue-statements.json" "$SRC" "$OUT/custody.json"
bash "$HERE/run_controls.sh" "$PY" "$SRC" "$OUT"
bash "$HERE/run_controls_centre.sh" "$PY" "$SRC" "$OUT"
bash "$HERE/run_identity.sh" "$PY" "$SRC" "$REPO" "$OUT"
run "$HERE/l64_construct.py" "$HERE/issue-statements.json" "$SRC" "$OUT/construct.json"
run "$HERE/l64_houses.py" "$HERE/issue-statements.json" "$REPO/packing/witnesses/known-best" \
  "$OUT/sides.json" "$OUT/houses.json"
run "$HERE/l64_digests.py" "$HERE/../frozen/checker-frozen-digests.txt" "$OUT" \
  "$OUT/program-digests.json"
