#!/usr/bin/env bash
# Lineage of the five certificates against their houses and regularized views.
# Usage: run_identity.sh PYTHON SRC REPO_ROOT OUT
set -euo pipefail
PY="$1"
SRC="$2"
REPO="$3"
OUT="$4"
HERE="$(cd "$(dirname "$0")" && pwd)"
for spec in 232:s232-upper-bound 268:s268-upper-bound 299:s299-upper-bound-17801004 303:s303-upper-bound 307:s307-upper-bound; do
  n="${spec%%:*}"
  repo="${spec#*:}"
  nice -n 19 "$PY" -I -B "$HERE/l64_identity.py" "$HERE/issue-statements.json" "$n" \
    "$SRC/$repo/n-$n-candidate.yaml" \
    "$REPO/packing/witnesses/known-best/n-$n.yaml" \
    "$REPO/packing/atlas/known-best/regularized/n-$n-regularized.yaml.gz" \
    "$OUT/identity-n$n.json"
done
