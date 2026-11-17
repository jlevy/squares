#!/usr/bin/env bash
# Lane L72 (bead think-qqyg): the self-test and both certificate checks, two at a time.
# Usage: bash run_checks.sh PYTHON SRC OUT
#   PYTHON  the project interpreter (CPython 3.14 with gmpy2 and PyYAML)
#   SRC     a directory holding s172-upper-bound and s270-upper-bound cloned at their pins
#   OUT     the receipt directory
set -euo pipefail
PY="$1"
SRC="$2"
OUT="$3"
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$OUT"
(
  nice -n 19 "$PY" -I -B "$HERE/l72_selftest.py" "$OUT/selftest.json" > "$OUT/selftest.log" 2>&1
  nice -n 19 "$PY" -I -B "$HERE/l72_check.py" "$SRC/s172-upper-bound/n-172-candidate.yaml" \
    "$SRC/s172-upper-bound/n172-witness.json" "$OUT/check-n172.json" > "$OUT/check-n172.log" 2>&1
) &
nice -n 19 "$PY" -I -B "$HERE/l72_check.py" "$SRC/s270-upper-bound/n-270-candidate.yaml" \
  "$SRC/s270-upper-bound/n270-witness.json" "$OUT/check-n270.json" > "$OUT/check-n270.log" 2>&1 || true
wait
cat "$OUT/selftest.log" "$OUT/check-n172.log" "$OUT/check-n270.log"
