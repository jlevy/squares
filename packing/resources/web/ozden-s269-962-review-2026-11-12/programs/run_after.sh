#!/usr/bin/env bash
# Lane L117: rerun the after-freeze measurements of the stage 4 review of #962.
# Usage, from packing/ of a checkout of main at 2fe557598 or later with T-290 the house:
#   programs/run_after.sh SOURCE_DIR OUT_DIR
#   SOURCE_DIR is a clone of kenaznia-doga/s269-upper-bound-16899469076 at fdab2c0.
# None of these decides the certificate; the two devtools are this repository's own,
# run read-only and writing only to OUT_DIR.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
src="$1"
out="$2"
mkdir -p "$out"
cert="$src/n-269-candidate.yaml"
twin="$src/n269-witness.json"
house=witnesses/known-best/n-269.yaml
uvr=(nice -n 19 uv run --frozen --all-extras --group dev python)
"${uvr[@]}" -m devtools.contraction_margin --n 269 "T-290=witness-center-basis:$house" \
  --against "NEW=witness-corners:$cert" --out "$out/contraction-t290.json"
"${uvr[@]}" -m devtools.contraction_margin --n 269 "NEW=witness-corners:$cert" --out "$out/contraction-new.json"
"${uvr[@]}" -m devtools.measure_identity --n 269 "NEW=witness-corners:$cert" \
  "T-290=witness-center-basis:$house" T-174=packet:pingyou-pr574-certificates-2026-10-13 \
  --out "$out/identity-n269.json"
"${uvr[@]}" -I -B "$here/l117_sides.py" "$cert" "$twin" frontier/n-269.md "$house" \
  "$out/identity-n269.json" "$here/issue-962.json" "$out/sides.json"
"${uvr[@]}" -I -B "$here/l117_pose.py" "$cert" "$twin" "$src/n-269-decimal-pose.yaml" "$out/pose-n269.json"
"${uvr[@]}" -I -B "$here/l117_lineage.py" "$cert" "$twin" "$house" "$out/lineage-n269.json"
"${uvr[@]}" -I -B "$here/l117_custody.py" "$src" "$(git rev-parse --show-toplevel)" "$here/issue-962.json" \
  "$out/custody.json"
