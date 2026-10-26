#!/usr/bin/env bash
# Reproduces every output of the 25 October 2026 mathematical review of issue 806.
#
#   programs/run_review.sh SRC REPO
#
# SRC holds the source's files from evand/square-packing at d99925d (search/packer/
# candidates/): s182-1024.cert, s182-1024.exact.txt, s182-1024.input.txt and
# s182-1024_regularized.cert. REPO is a checkout of jlevy/squares; the comparison
# packings are read from its packing/ tree. PY defaults to the project interpreter.
# The programs only read their arguments; each runs niced, one at a time, in isolated
# mode, and writes to out/ beside this directory (about 2.5 CPU minutes in all).
set -euo pipefail

SRC=$(cd "$1" && pwd)
REPO=$(cd "$2" && pwd)
PY=${PY:-$REPO/packing/.venv/bin/python3}
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=$HERE/../out
W=$REPO/packing
mkdir -p "$OUT"

run() { nice -n 10 "$PY" -I "$@"; }

run "$HERE/exact_check.py" check "$SRC/s182-1024.cert" --json "$OUT/check-s182-1024.json" | tee "$OUT/check-s182-1024.txt"
run "$HERE/exact_check.py" controls "$SRC/s182-1024.cert" --json "$OUT/controls-s182-1024.json" | tee "$OUT/controls-s182-1024.txt"
run "$HERE/exact_check.py" check "$SRC/s182-1024_regularized.cert" --json "$OUT/check-s182-1024_regularized.json" | tee "$OUT/check-s182-1024_regularized.txt"
run "$HERE/sides.py" "$SRC/s182-1024.cert" "$W/frontier/n-182.md" \
  "$W/resources/web/evand-square-packing-2026-10-05/square-packing/s12/search/exact/batch/certs/n-182.cert" \
  "$SRC/s182-1024.exact.txt" --json "$OUT/sides.json" | tee "$OUT/sides.txt"
run "$HERE/kkt_consistency.py" "$SRC/s182-1024.cert" "$SRC/s182-1024.exact.txt" "$SRC/s182-1024.input.txt" \
  --json "$OUT/kkt-consistency.json" | tee "$OUT/kkt-consistency.txt"
run "$HERE/identity_lineage.py" --json "$OUT/identity-lineage.json" \
  --cert "$SRC/s182-1024.cert" --input "$SRC/s182-1024.input.txt" --kkt "$SRC/s182-1024.exact.txt" \
  --regularized "$SRC/s182-1024_regularized.cert" \
  --t174 "$W/resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-182.yaml.gz" \
  --house "$W/witnesses/known-best/n-182.yaml" \
  --t098 "$W/resources/web/evand-square-packing-2026-10-05/square-packing/s12/search/exact/batch/certs/n-182.cert" \
  --t056 "$W/resources/web/franciscouzo-square-packing-2026-09-27/facts/n-182.yaml" \
  --t188 "$W/resources/web/couzo-verified-bounds-2026-10-14/source/certificates/n211.cert" \
  --t175 "$W/resources/web/dostashev-merged-bands-2026-10-13/source/records/n0211.sqcert" \
  --t182 "$W/resources/web/couzo-certificates-2026-10-13/source/certificates/n211.cert" \
  --t181 "$W/resources/web/couzo-issue583-2026-10-13/source/certificates/n211.cert" | tee "$OUT/identity-lineage.txt"
