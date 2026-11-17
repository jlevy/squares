#!/usr/bin/env bash
# Rerun lane L109's frozen self-test, check, census and controls for issue #960.
# Usage, from packing/ of a checkout of main: run_frozen.sh SOURCE_DIR OUT_DIR
# SOURCE_DIR is a clone of kenaznia-doga/s237-upper-bound at 13c4b231bb16.
# The receipts differ from the kept ones only in their CPU seconds.
set -euo pipefail
src=$1
out=$2
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$out"
py() { nice -n 19 uv run --frozen --all-extras --group dev python -I -B "$@"; }
py "$here/l109_selftest.py" "$out/selftest.json"
py "$here/l109_check.py" "$src/n-237-candidate.yaml" "$src/n237-witness.json" "$out/check-n237.json"
py "$here/l109_census.py" "$src/n-237-candidate.yaml" "$src/n237-witness.json" "$out/census-n237.json"
py "$here/l109_controls.py" "$src/n-237-candidate.yaml" "$src/n237-witness.json" \
  "$here/controls-plan.json" "$here/../out/plan-facts-n237.json" "$out/controls-n237.json"
