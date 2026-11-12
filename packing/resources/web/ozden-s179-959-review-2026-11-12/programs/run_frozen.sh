#!/usr/bin/env bash
# Rerun lane L108's frozen programs: the self-test, the check, the plan facts, the plan and
# the controls. Run from packing/ of a checkout of main.
#   run_frozen.sh SOURCE_DIR OUT_DIR
# SOURCE_DIR holds n-179-candidate.yaml and n179-witness.json at the pin; OUT_DIR is new.
set -euo pipefail
src="$1"
out="$2"
here="$(cd "$(dirname "$0")" && pwd)"
py=(nice -n 19 uv run --frozen --all-extras --group dev python -I -B)
mkdir -p "$out"
"${py[@]}" "$here/l108_selftest.py" "$out/selftest.json"
"${py[@]}" "$here/l108_check.py" "$src/n-179-candidate.yaml" "$src/n179-witness.json" "$out/check-n179.json"
"${py[@]}" "$here/l108_plan_facts.py" "$src/n-179-candidate.yaml" "$src/n179-witness.json" "$out/check-n179.json" "$out/plan-facts-n179.json" >/dev/null
"${py[@]}" "$here/l108_make_plan.py" "$out/check-n179.json" "$out/plan-facts-n179.json" "$out/controls-plan.json"
"${py[@]}" "$here/l108_controls.py" "$src/n-179-candidate.yaml" "$src/n179-witness.json" "$out/controls-plan.json" "$out/plan-facts-n179.json" "$out/check-n179.json" "$out/controls-n179.json"
