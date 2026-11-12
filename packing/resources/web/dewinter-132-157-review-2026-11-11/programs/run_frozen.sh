#!/usr/bin/env bash
# Rerun lane L105's frozen self-test, checks and controls.
# Usage: run_frozen.sh SOURCE_DIR OUT_DIR
# SOURCE_DIR is a checkout of JoostdeWinter/square-packing at 6617869a3491, holding
# n132/ and n157/. Run from packing/ of a checkout of this repository.
set -euo pipefail
src=$1
out=$2
here=$(cd "$(dirname "$0")" && pwd)
py=(nice -n 19 uv run --frozen --all-extras --group dev python -I -B)
"${py[@]}" "$here/l105_selftest.py" "$out/selftest.json"
"${py[@]}" "$here/l105_selftest.py" "$out/selftest-mutant-A0.json" --mutant A0 || true
"${py[@]}" "$here/l105_selftest.py" "$out/selftest-mutant-Bopen.json" --mutant Bopen || true
for n in 132 157; do
  "${py[@]}" "$here/l105_check.py" "$src" "$n" "$out/check-n$n.json"
done
if [[ -f "$here/l105_controls.py" ]]; then
  for n in 132 157; do
    "${py[@]}" "$here/l105_controls.py" "$src" "$n" "$here/controls-plan.json" "$out/controls-n$n.json"
  done
fi
