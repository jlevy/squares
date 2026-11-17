#!/usr/bin/env bash
# Rerun the L96 review: bash run_all.sh REPO_ROOT OUT MAIN_EXPORT
#   REPO_ROOT    a checkout holding the three packets (the import branch, or main after it)
#   OUT          an empty directory for the receipts, with subdirectories 941 and 942
#   MAIN_EXPORT  a directory holding `git show 591644a9e:packing/frontier/source-coverage.yaml`
#                and `.../results.yaml`
# Run from REPO_ROOT/packing so that uv selects the project interpreter (CPython 3.14.7).
# The controls plan is stated by `l96_controls.py plan` and was frozen before `run`; rerunning
# `plan` must reproduce frozen/controls-plan.json byte for byte.
set -euo pipefail
ROOT=$1
OUT=$2
MAIN=$3
HERE=$(cd "$(dirname "$0")" && pwd)
W=$ROOT/packing/resources/web
A=$W/de-winter-issue941-2026-11-10/source/above324
B=$W/de-winter-issue942-2026-11-10/source/above324_refined
C=$W/de-winter-a0c4fc8-2026-11-10/source/above324_refined
PY="nice -n 19 uv run --frozen --all-extras --group dev python -I -B"
$PY "$HERE/l96_selftest.py" "$OUT/selftest.json"
$PY "$HERE/l96_check.py" "$OUT/941" "$A"/n*.cert
$PY "$HERE/l96_check.py" "$OUT/942" "$B"/n*.cert "$C"/n*.cert
$PY "$HERE/l96_record_rows.py" "$MAIN/source-coverage.yaml" "$MAIN/results.yaml" \
  591644a9e9b41c04858e2601382e5a65485a09a9 "$OUT/record-rows.json"
$PY "$HERE/l96_claims.py" "$HERE/issues-941-942.json" "$OUT/record-rows.json" "$OUT/claims.json" \
  "$OUT/941" "$OUT/942"
$PY "$HERE/l96_controls.py" plan "$OUT/controls-plan.json" "$A"/n*.cert "$B"/n*.cert "$C"/n*.cert
$PY "$HERE/l96_controls.py" run "$HERE/../frozen/controls-plan.json" "$OUT/941" "$A"/n*.cert
$PY "$HERE/l96_controls.py" run "$HERE/../frozen/controls-plan.json" "$OUT/942" "$B"/n*.cert "$C"/n*.cert
$PY "$HERE/l96_construct.py" "$OUT/construct.json" "$A"
$PY "$HERE/l96_custody.py" "$OUT/custody.json" "$HERE/issues-941-942.json" \
  "$W/de-winter-issue941-2026-11-10/source" "$W/de-winter-issue942-2026-11-10/source" \
  "$W/de-winter-a0c4fc8-2026-11-10/source"
$PY "$HERE/l96_extent.py" "$OUT/extent.json" "$A"/n*.cert "$B"/n*.cert "$C"/n*.cert
# After the freeze, with the import lane's files exported to LANE (its ledger.json, the three
# acquisition/upstream-subtree.sha256 as manifest-941/942/a0c.sha256, and main's 227/229/260
# LICENSE as LICENSE-main-copy), the reconciliation's comparison was:
#   $PY "$HERE/l96_compare_lane.py" OUT_SHARED/compare-lane.json LANE/ledger.json OUT_SHARED \
#     LANE/manifest-941.sha256 LANE/manifest-942.sha256 LANE/manifest-a0c.sha256 LANE/LICENSE-main-copy
# where OUT_SHARED is this directory's out/, beside the other two packets' out/ directories.
