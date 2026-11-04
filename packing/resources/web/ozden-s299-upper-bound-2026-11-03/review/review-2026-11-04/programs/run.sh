#!/usr/bin/env bash
# Rerun every program of the 4 November stage 4 review of #893 and #894, writing its receipts.
#
# Usage: programs/run.sh REPO OUT [UPSTREAM]
#   REPO      a checkout of jlevy/squares (the packets, house witnesses and Daniel's certificates are read from it)
#   OUT       the directory the receipts are written to
#   UPSTREAM  optional: a directory holding bare clones s299.git and s204.git of
#             kenaznia-doga/s299-upper-bound and kenaznia-doga/s204-upper-bound; without it the custody step is skipped
#
# Uses the project interpreter in isolated mode with no bytecode written, one process at a time, BLAS pinned to one thread.
set -euo pipefail
REPO=$(cd "$1" && pwd)
OUT=$(mkdir -p "$2" && cd "$2" && pwd)
UPSTREAM=${3:-}
HERE=$(cd "$(dirname "$0")" && pwd)
PY="${PY:-$REPO/packing/.venv/bin/python3}"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
W="$REPO/packing/resources/web"
P299="$W/ozden-s299-upper-bound-2026-11-03"
P204="$W/ozden-s204-upper-bound-2026-11-03"
S299=3560247706795812422293947620670679551/200000000000000000000000000000000000
S204=7403810497792604009019579959/500000000000000000000000000

"$PY" -I -B "$HERE/oz_selftest.py" "$OUT/selftest.json"
"$PY" -I -B "$HERE/oz_check.py" "$P299/source/n-299-candidate.yaml" "$P299/source/n299-refill2-t000173.json.gz" 299 "$S299" "$OUT/check-n299.json"
"$PY" -I -B "$HERE/oz_check.py" "$P204/source/n-204-candidate.yaml" "$P204/source/n204-witness.json" 204 "$S204" "$OUT/check-n204.json"
"$PY" -I -B "$HERE/oz_controls.py" "$P299/source/n-299-candidate.yaml" 299 "$S299" "$OUT/controls-n299.json"
"$PY" -I -B "$HERE/oz_controls.py" "$P204/source/n-204-candidate.yaml" 204 "$S204" "$OUT/controls-n204.json"
"$PY" -I -B "$HERE/oz_sides.py" "$P299/source/n-299-candidate.yaml" "$REPO/packing/witnesses/known-best/n-299.yaml" \
  "$P204/source/n-204-candidate.yaml" "$REPO/packing/witnesses/known-best/n-204.yaml" "$OUT/sides.json"
"$PY" -I -B "$HERE/oz_identity.py" "$P299/source/n-299-candidate.yaml" "$REPO/packing/witnesses/known-best/n-299.yaml" \
  "$W/evand-n299-update-2026-10-29/source/search/packer/candidates/s299_1028.cert" "$OUT/identity-n299.json"
"$PY" -I -B "$HERE/oz_identity.py" "$P204/source/n-204-candidate.yaml" "$REPO/packing/witnesses/known-best/n-204.yaml" \
  "$W/evand-issue845-2026-10-29/source/search/packer/candidates/s204_1028.cert" "$OUT/identity-n204.json"
for n in 299 204; do
  P="$W/ozden-s$n-upper-bound-2026-11-03"
  "$PY" -I -B "$HERE/oz_compare_lane.py" "$P/source/n-$n-candidate.yaml" "$P/receipts/exact-certification.json.xz" \
    "$P/receipts/sharp-controls.json" "$P/measure/identity.json" "$OUT/check-n$n.json" "$OUT/identity-n$n.json" \
    "$OUT/compare-lane-n$n.json"
done
if [ -n "$UPSTREAM" ]; then
  "$PY" -I -B "$HERE/oz_custody.py" "$UPSTREAM/s299.git" "$UPSTREAM/s204.git" "$P299" "$P204" "$OUT/custody.json"
fi
"$PY" -I -B "$HERE/oz_repair.py" "$P299/source/n-299-candidate.yaml" "$P299/source/n299-refill2-t000173.json.gz" "$OUT/repair-n299.json"
