#!/usr/bin/env bash
# Rerun lane L108's after-freeze programs. Run from packing/ of a checkout of main at
# c8448724e (T-174 is the house there).
#   run_after.sh SOURCE_DIR SOURCE954_DIR T291_HOUSE REPO_DIR OUT_DIR
# SOURCE_DIR: the clone of kenaznia-doga/s179-upper-bound-13880960371 at 6ab3cfe.
# SOURCE954_DIR: #954's n-179-candidate.yaml, n179-witness.json (SHA-256 75813e7c...) and pose,
#   as retained in packing/resources/web/ozden-s179-upper-bound-2026-11-11/source/.
# T291_HOUSE: packing/witnesses/known-best/n-179.yaml from main at b5b12c206.
# REPO_DIR: the checkout of main at c8448724e. OUT_DIR: where the receipts go.
set -euo pipefail
src="$1"
s954="$2"
t291="$3"
repo="$4"
out="$5"
here="$(cd "$(dirname "$0")" && pwd)"
py=(nice -n 19 uv run --frozen --all-extras --group dev python -I -B)
mkdir -p "$out"
"${py[@]}" "$here/l108_sides.py" "$src/n-179-candidate.yaml" "$s954/n-179-candidate.yaml" "$repo" "$here/issue-959.json" "$src" "$out/sides.json" >/dev/null
"${py[@]}" "$here/l108_house.py" house_t174 "$repo/packing/witnesses/known-best/n-179.yaml" "$s954/n-179-candidate.yaml" "$s954/n179-witness.json" "$out/house-n179.json"
"${py[@]}" "$here/l108_house.py" house_t291_main_b5b12c2 "$t291" "$s954/n-179-candidate.yaml" "$s954/n179-witness.json" "$out/house-t291-main.json"
"${py[@]}" "$here/l108_pose.py" "$src/n-179-candidate.yaml" "$src/n-179-decimal-pose.yaml" "$repo" "$out/pose-n179.json" >/dev/null
"${py[@]}" "$here/l108_pose.py" "$s954/n-179-candidate.yaml" "$s954/n-179-decimal-pose.yaml" "$repo" "$out/pose-n954.json" >/dev/null
"${py[@]}" "$here/l108_s70.py" "$src/n-179-candidate.yaml" "$repo" "$out/s70-n179.json" >/dev/null
"${py[@]}" "$here/l108_identity.py" "$src/n-179-candidate.yaml" house-t174 "$repo/packing/witnesses/known-best/n-179.yaml" n954 "$s954/n-179-candidate.yaml" house-t291-main "$t291" "$out/identity-n179.json" >/dev/null
"${py[@]}" "$here/l108_contract.py" "$src/n-179-candidate.yaml" "$src/n179-witness.json" "$repo" "$out/contract-n179.json" 1e-13 19e-14 199e-15 2e-13
"${py[@]}" "$here/l108_custody.py" "$src" "$repo" "$here/issue-959.json" "$out/custody.json" >/dev/null
