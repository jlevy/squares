#!/usr/bin/env bash
# Lane L72 (bead think-qqyg): the stated controls at both counts, two at a time.
# Usage: bash run_controls.sh PYTHON SRC OUT
#   OUT must already hold check-n172.json and check-n270.json from run_checks.sh.
set -euo pipefail
PY="$1"
SRC="$2"
OUT="$3"
HERE="$(cd "$(dirname "$0")" && pwd)"
nice -n 19 "$PY" -I -B "$HERE/l72_controls.py" "$HERE/controls-plan.json" 172 \
  "$SRC/s172-upper-bound/n-172-candidate.yaml" "$OUT/check-n172.json" "$OUT/controls-n172.json" \
  > "$OUT/controls-n172.log" 2>&1 &
nice -n 19 "$PY" -I -B "$HERE/l72_controls.py" "$HERE/controls-plan.json" 270 \
  "$SRC/s270-upper-bound/n-270-candidate.yaml" "$OUT/check-n270.json" "$OUT/controls-n270.json" \
  > "$OUT/controls-n270.log" 2>&1 || true
wait || true
cat "$OUT/controls-n172.log" "$OUT/controls-n270.log"
