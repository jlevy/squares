#!/usr/bin/env bash
# Rerun the post-freeze measurements of lane L101's review of #954, then the digest audit.
#
# Usage: run_after.sh SOURCE_DIR REPO_DIR OUT_DIR
#   SOURCE_DIR  a checkout of kenaznia-doga/s179-upper-bound at bd262d8b
#   REPO_DIR    a checkout of jlevy/squares (the house and the 70 and 207 witnesses)
#   OUT_DIR     where the receipts go (the kept ones are in ../out)
# Run from packing/ of a checkout of jlevy/squares, so that `uv run` finds the project.
set -euo pipefail
SRC=$1
REPO=$2
OUT=$3
HERE=$(cd "$(dirname "$0")" && pwd)
PY="nice -n 19 uv run --frozen --all-extras --group dev python -I -B"
mkdir -p "$OUT"
KB="$REPO/packing/witnesses/known-best"
$PY "$HERE/l101_sides.py" "$SRC" "$HERE/issue-954.json" "$REPO" "$OUT/sides.json"
$PY "$HERE/l101_house.py" "$KB/n-179.yaml" "$OUT/house-n179.json"
$PY "$HERE/l101_pose.py" "$SRC" "$HERE/../out/check-n179.json" "$OUT/pose-n179.json"
$PY "$HERE/l101_identity.py" "$SRC" "$KB/n-179.yaml" "$OUT/identity-n179.json"
$PY "$HERE/l101_band.py" "$SRC" "$KB" "$OUT/band-n179.json"
$PY "$HERE/l101_custody.py" "$SRC" "$REPO" "$HERE/issue-954.json" "$OUT/custody.json"
$PY "$HERE/l101_digests.py" "$HERE/.." "$OUT/program-digests.json"
