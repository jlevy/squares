#!/usr/bin/env bash
# Run the frozen controls addendum on every file, one at a time (one worker).
# Usage: bash run_addendum.sh PYTHON SRC REVIEW_DIR
set -euo pipefail
PY="$1"; SRC="$2"; R="$3"
for label in yim-n130 yim-n299 yim-n303 yim-n303-first yim-n553 yim-n599 yim-n600 yim-n601 yim-n602 yim-n604 yim-n645 yim-n647 yim-n648 yim-n699 yim-n700; do
  nice -n 19 "$PY" -I -B "$R/programs/l70_controls_addendum.py" --src "$SRC" \
    --addendum "$R/programs/controls-plan-addendum.json" --label "$label" \
    --out "$R/out/controls-addendum-$label.json" | tail -1
done
