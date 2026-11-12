#!/usr/bin/env bash
# Rerun lane L105's programs written after the findings were frozen. None decides a packing.
# Usage: run_after.sh SOURCE_DIR SEED_DIR REPO_DIR OUT_DIR
# SOURCE_DIR: a clone of JoostdeWinter/square-packing at 6617869a3491.
# SEED_DIR: a clone of Samanyu-dev/squares_in_squares at 53551d77513a.
# REPO_DIR: a checkout of this repository at main c8448724e.
# Run from packing/ of a checkout of this repository.
set -euo pipefail
src=$1
seed=$2
repo=$3
out=$4
here=$(cd "$(dirname "$0")" && pwd)
py=(nice -n 19 uv run --frozen --all-extras --group dev python -I -B)
"${py[@]}" "$here/l105_sides.py" "$src" "$repo" "$here/issue-958.json" "$out/sides.json"
"${py[@]}" "$here/l105_construct.py" "$src" "$out/construct.json"
"${py[@]}" "$here/l105_lineage.py" "$seed/best_fit_101_500.csv" "$src" "$out/lineage.json"
"${py[@]}" "$here/l105_identity.py" "$src" "$repo/packing/witnesses/known-best/n-132.yaml" "$out/identity-n132.json"
"${py[@]}" "$here/l105_custody.py" "$src" "$seed" "$repo" "$out/custody.json"
"${py[@]}" "$here/l105_digests.py" "$here/.." "$out/program-digests.json"
