#!/bin/bash
# Rerun every L77 program over its inputs and rewrite out/. Arguments:
#   $1  the clone of kenaznia-doga/s199-upper-bound (for custody)
#   $2  that repository's tree at d03ee0bdb223e00fe124e818ed242f6cbd714fad, extracted
#   $3  the root of a jlevy/squares checkout at main 200f2ebc1
#   $4  a scratch directory for the mutants
# Python 3.14 with gmpy2, PyYAML, mpmath, NumPy and SciPy, run isolated (-I -B).
set -euo pipefail
CLONE=$1 PIN=$2 REPO=$3 WORK=$4
PY=${PY:-python3}
HERE=$(cd "$(dirname "$0")" && pwd)
O=$HERE/out
cd "$HERE"
run() { echo "== $1"; time nice -n 19 "$PY" -I -B "$@" > /dev/null; }
run l77_selftest.py "$O/selftest.json"
run l77_mutants.py "$WORK" "$O/mutants.json"
run l77_check.py "$PIN/n-199-candidate.yaml" "$PIN/n199-witness.json" "$O/check-n199.json"
run l77_construct.py "$PIN/n-199-candidate.yaml" "$REPO/packing/resources/web/ozden-s172-upper-bound-2026-11-09/source/n-172-candidate.yaml" "$REPO/packing/witnesses/known-best/n-172.yaml" "$O/construct-n199.json"
run l77_plan_facts.py "$PIN/n-199-candidate.yaml" "$O/plan-facts-n199.json"
run l77_sides.py "$PIN/n-199-candidate.yaml" "$HERE/issue-statements.json" "$REPO/packing/witnesses/known-best/n-199.yaml" "$REPO/packing/frontier/n-199.md" "$O/sides.json"
run l77_propagate.py "$REPO/packing/frontier" "$PIN/n-199-candidate.yaml" "$O/propagate.json"
run l77_custody.py "$CLONE" "$PIN" "$REPO" "$O/custody.json"
run l77_pose.py "$PIN/n-199-decimal-pose.yaml" "$REPO/packing/resources/web/ozden-s172-upper-bound-2026-11-09/source/n-172-decimal-pose.yaml" "$PIN/n-199-candidate.yaml" "$O/pose.json"
run l77_identity.py "$PIN/n-199-candidate.yaml" "$REPO/packing/witnesses/known-best/n-199.yaml" "$O/identity-n199.json"
run l77_controls.py "$PIN/n-199-candidate.yaml" "$HERE/controls-plan.json" "$O/controls-n199.json" 2
run l77_digests.py "$O/program-digests.json"
