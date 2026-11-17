#!/usr/bin/env bash
# Rerun lane L109's programs written after the findings were frozen, and the two
# repository tools the review ran read-only, for issue #960.
# Usage, from packing/ of a checkout of main at c8448724e:
#   run_after.sh SOURCE_DIR OUT_DIR
# SOURCE_DIR is a clone of kenaznia-doga/s237-upper-bound at 13c4b231bb16.
set -euo pipefail
src=$1
out=$2
here=$(cd "$(dirname "$0")" && pwd)
repo=$(cd .. && pwd)
mkdir -p "$out"
py() { nice -n 19 uv run --frozen --all-extras --group dev python -I -B "$@"; }
tool() { nice -n 19 uv run --frozen --all-extras --group dev python -m "$@"; }
cert="$src/n-237-candidate.yaml"
twin="$src/n237-witness.json"
house=witnesses/known-best/n-237.yaml
t189=resources/web/couzo-certificates-2026-10-14/source/submissions/2026-10-14/certificates/n237.cert
py "$here/l109_sides.py" "$cert" "$twin" "$here/issue-960.json" "$repo" "$src" "$out/sides.json"
py "$here/l109_pose.py" "$cert" "$twin" "$src/n-237-decimal-pose.yaml" "$here/../out/check-n237.json" "$out/pose-n237.json"
py "$here/l109_identity.py" "$cert" "$twin" "$house" "$out/identity-n237.json"
py "$here/l109_band.py" "$cert" "$twin" "$house" witnesses/known-best/n-070.yaml "$out/band-n237.json"
py "$here/l109_custody.py" "$src" "$repo" "$here/issue-960.json" "$out/custody.json"
tool devtools.contraction_margin --n 237 "T-190=witness-center-basis:$house" \
  --against "issue-960=witness-corners:$cert" > "$out/contraction-margin-t190.json"
tool devtools.contraction_margin --n 237 "T-189=evand-cert:$t189" \
  --against "issue-960=witness-corners:$cert" > "$out/contraction-margin-t189.json"
tool devtools.measure_identity --n 237 "issue-960=witness-corners:$cert" \
  "T-190=witness-center-basis:$house" "T-189=evand-cert:$t189" > "$out/measure-identity-n237.json"
