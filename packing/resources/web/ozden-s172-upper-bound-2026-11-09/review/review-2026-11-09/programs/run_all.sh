#!/usr/bin/env bash
# Lane L72 (bead think-qqyg): every program of the review, in order, two at a time.
# Usage: bash run_all.sh PYTHON SRC REPO_ROOT OUT172 OUT270
#   PYTHON    the project interpreter (CPython 3.14 with gmpy2, PyYAML, NumPy, SciPy, mpmath)
#   SRC       a directory holding s172-upper-bound and s270-upper-bound cloned at their pins
#   REPO_ROOT a checkout of this repository at main ef1af4933 (the houses, views and retained licences)
#   OUT172    the 172 packet's review/review-2026-11-09/out
#   OUT270    the 270 packet's review/review-2026-11-09/out
# The plan facts (plan-facts-nNNN.json) are kept as written before the controls plan was
# stated and are not rewritten here; l72_digests.py runs last, apart.
set -euo pipefail
PY="$1"
SRC="$2"
REPO="$3"
O1="$4"
O2="$5"
HERE="$(cd "$(dirname "$0")" && pwd)"
run() { nice -n 19 "$PY" -I -B "$@"; }
mkdir -p "$O1" "$O2"
(
  run "$HERE/l72_selftest.py" "$O1/selftest.json" > "$O1/selftest.log" 2>&1
  run "$HERE/l72_check.py" "$SRC/s172-upper-bound/n-172-candidate.yaml" \
    "$SRC/s172-upper-bound/n172-witness.json" "$O1/check-n172.json" > "$O1/check-n172.log" 2>&1
  run "$HERE/l72_controls.py" "$HERE/controls-plan.json" 172 "$SRC/s172-upper-bound/n-172-candidate.yaml" \
    "$O1/check-n172.json" "$O1/controls-n172.json" > "$O1/controls-n172.log" 2>&1
  run "$HERE/l72_identity.py" "$HERE/issue-statements.json" 172 "$SRC" "$REPO" "$O1/identity-n172.json" \
    > "$O1/identity-n172.log" 2>&1
  run "$HERE/l72_construct.py" "$HERE/issue-statements.json" 172 "$SRC" "$O1/check-n172.json" \
    "$O1/construct-n172.json" > "$O1/construct-n172.log" 2>&1
  run "$HERE/l72_custody.py" "$HERE/issue-statements.json" "$SRC" "$REPO" "$O1/custody.json" > "$O1/custody.log" 2>&1
) &
(
  run "$HERE/l72_check.py" "$SRC/s270-upper-bound/n-270-candidate.yaml" \
    "$SRC/s270-upper-bound/n270-witness.json" "$O2/check-n270.json" > "$O2/check-n270.log" 2>&1
  run "$HERE/l72_controls.py" "$HERE/controls-plan.json" 270 "$SRC/s270-upper-bound/n-270-candidate.yaml" \
    "$O2/check-n270.json" "$O2/controls-n270.json" > "$O2/controls-n270.log" 2>&1
  run "$HERE/l72_identity.py" "$HERE/issue-statements.json" 270 "$SRC" "$REPO" "$O2/identity-n270.json" \
    > "$O2/identity-n270.log" 2>&1
  run "$HERE/l72_construct.py" "$HERE/issue-statements.json" 270 "$SRC" "$O2/check-n270.json" \
    "$O2/construct-n270.json" > "$O2/construct-n270.log" 2>&1
) &
wait
run "$HERE/l72_sides.py" "$HERE/issue-statements.json" "$SRC" "$REPO" "$O1/sides.json" > "$O1/sides.log" 2>&1
run "$HERE/l72_houses.py" "$HERE/issue-statements.json" "$O1/sides.json" "$REPO" "$O1/houses.json" > "$O1/houses.log" 2>&1
tail -n 1 "$O1/selftest.log" "$O1/check-n172.log" "$O2/check-n270.log" "$O1/controls-n172.log" "$O2/controls-n270.log" \
  "$O1/custody.log" "$O1/sides.log"
