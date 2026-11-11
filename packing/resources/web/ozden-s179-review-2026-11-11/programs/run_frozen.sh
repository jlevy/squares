#!/usr/bin/env bash
# Rerun the frozen part of lane L101's review of #954: the self-test, the check and the
# controls. The plan facts and the plan are kept as written before the controls existed
# and are not rewritten here; pass KEEP=0 to rewrite them into a scratch directory.
#
# Usage: run_frozen.sh SOURCE_DIR OUT_DIR
#   SOURCE_DIR  a checkout of kenaznia-doga/s179-upper-bound at bd262d8b
#   OUT_DIR     where the receipts go (the kept ones are in ../out)
# Run from packing/ of a checkout of jlevy/squares, so that `uv run` finds the project.
set -euo pipefail
SRC=$1
OUT=$2
HERE=$(cd "$(dirname "$0")" && pwd)
PY="nice -n 19 uv run --frozen --all-extras --group dev python -I -B"
mkdir -p "$OUT"
$PY "$HERE/l101_selftest.py" "$OUT/selftest.json"
$PY "$HERE/l101_check.py" "$SRC/n-179-candidate.yaml" "$SRC/n179-witness.json" 179 "$OUT/check-n179.json"
if [ "${KEEP:-1}" = 0 ]; then
  $PY "$HERE/l101_plan_facts.py" "$SRC/n-179-candidate.yaml" "$SRC/n179-witness.json" 179 \
    "$OUT/check-n179.json" "$OUT/plan-facts-n179.json"
  $PY "$HERE/l101_make_plan.py" "$OUT/check-n179.json" "$OUT/plan-facts-n179.json" "$OUT/controls-plan.json"
  PLAN="$OUT/controls-plan.json"; FACTS="$OUT/plan-facts-n179.json"
else
  PLAN="$HERE/controls-plan.json"; FACTS="$HERE/../out/plan-facts-n179.json"
fi
$PY "$HERE/l101_controls.py" "$SRC/n-179-candidate.yaml" "$SRC/n179-witness.json" 179 \
  "$PLAN" "$FACTS" "$OUT/controls-n179.json"
