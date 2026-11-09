#!/usr/bin/env bash
# Decide the five certificates with the frozen checker, two processes at a time.
# Usage: run_checks.sh PYTHON SRC OUT
set -euo pipefail
PY="$1"
SRC="$2"
OUT="$3"
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$OUT"
check() {
  local n="$1" repo="$2"
  nice -n 19 "$PY" -I -B "$HERE/l64_check.py" \
    "$SRC/$repo/n-$n-candidate.yaml" "$SRC/$repo/n$n-witness.json" "$n" \
    "$OUT/check-n$n.json" || true
}
( check 232 s232-upper-bound; check 299 s299-upper-bound-17801004; check 307 s307-upper-bound ) &
( check 268 s268-upper-bound; check 303 s303-upper-bound ) &
wait
