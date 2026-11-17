#!/usr/bin/env bash
# The measurements that decide nothing, one at a time (one worker).
# Usage: bash run_measures.sh PYTHON SRC REPO REVIEW_DIR
set -euo pipefail
PY="$1"; SRC="$2"; REPO="$3"; R="$4"
T272="$REPO/packing/resources/web/evand-issue914-2026-11-05/source/search/packer/candidates/s303_1105.cert"
nice -n 19 "$PY" -I -B "$R/programs/l70_identity.py" --src "$SRC" --repo "$REPO" --checks "$R/out" \
  --out "$R/out/identity.json" "--extra=t272-n303=cert=$T272" \
  "--pair=yim-n303-first:t272-n303" "--pair=house-t278-n303:t272-n303"
nice -n 19 "$PY" -I -B "$R/programs/l70_construct.py" --src "$SRC" --repo "$REPO" --checks "$R/out" --out "$R/out/construct.json"
nice -n 19 "$PY" -I -B "$R/programs/l70_contract.py" --src "$SRC" --repo "$REPO" --out "$R/out/contract.json" --no-verify \
  --only yim-n553 yim-n599 yim-n600 yim-n601 yim-n602 yim-n604 yim-n645 yim-n647 yim-n648 yim-n699 yim-n700 \
  couzo-n553 couzo-n599 couzo-n600 couzo-n601 couzo-n602 couzo-n604 couzo-n645 couzo-n647 couzo-n648 couzo-n699 couzo-n700
