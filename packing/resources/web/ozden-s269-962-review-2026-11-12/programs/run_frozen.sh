#!/usr/bin/env bash
# Lane L117: rerun the frozen sequence of the stage 4 review of #962.
# Usage, from packing/ of a checkout: programs/run_frozen.sh SOURCE_DIR OUT_DIR
#   SOURCE_DIR holds n-269-candidate.yaml and n269-witness.json at the pin fdab2c0.
#   OUT_DIR receives selftest.json, check-n269.json, plan-facts-n269.json,
#   controls-plan.json and controls-n269.json.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
src="$1"
out="$2"
mkdir -p "$out"
py=(nice -n 19 uv run --frozen --all-extras --group dev python -I -B)
"${py[@]}" "$here/l117_selftest.py" "$out/selftest.json"
"${py[@]}" "$here/l117_check.py" "$src/n-269-candidate.yaml" "$src/n269-witness.json" "$out/check-n269.json"
"${py[@]}" "$here/l117_plan_facts.py" "$src/n-269-candidate.yaml" "$src/n269-witness.json" \
  "$out/check-n269.json" 16.899469075856 "$out/plan-facts-n269.json"
"${py[@]}" "$here/l117_make_plan.py" "$out/check-n269.json" "$out/plan-facts-n269.json" "$out/controls-plan.json"
"${py[@]}" "$here/l117_controls.py" "$src/n-269-candidate.yaml" "$src/n269-witness.json" \
  "$out/controls-plan.json" "$out/plan-facts-n269.json" "$out/check-n269.json" "$out/controls-n269.json"
