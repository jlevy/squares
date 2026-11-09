#!/usr/bin/env bash
# The addendum's centre-line controls on the five certificates, two processes at a time.
# Usage: run_controls_centre.sh PYTHON SRC OUT
set -euo pipefail
PY="$1"
SRC="$2"
OUT="$3"
HERE="$(cd "$(dirname "$0")" && pwd)"
ctl() {
  local n="$1" repo="$2"
  nice -n 19 "$PY" -I -B "$HERE/l64_controls_centre.py" "$HERE/controls-plan-addendum.json" \
    "$SRC/$repo/n-$n-candidate.yaml" "$n" "$OUT/check-n$n.json" \
    "$OUT/controls-centre-n$n.json" || true
}
( ctl 232 s232-upper-bound; ctl 299 s299-upper-bound-17801004; ctl 307 s307-upper-bound ) &
( ctl 268 s268-upper-bound; ctl 303 s303-upper-bound ) &
wait
