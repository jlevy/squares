#!/usr/bin/env bash
# Run every program of the 5 November 2026 review of jlevy/squares#895, from the
# repository root, writing receipts into OUT_DIR.
#
# Usage: bash run_all.sh PYTHON PROGRAMS_DIR OUT_DIR [part1|part2|all|custody CLONE]
#   PYTHON is the project interpreter (Python 3.14), e.g. packing/.venv/bin/python3;
#   every program runs under it with -I. Inputs are read by repository-relative paths.
#   `custody CLONE` runs custody.py on a bare clone of vitamoon/vitamoon at CLONE.
set -euo pipefail
PY="$1"
D="$2"
O="$3"
PART="${4:-all}"
W=packing/resources/web
Y=$W/yim-s260-upper-bound-2026-11-05/source/n260.cert
T=$W/evand-issue845-2026-10-29/source/search/packer/candidates/s260_1028.cert
H=packing/witnesses/known-best/n-260.yaml
FRACTION='1045817814143413714427921537528704162855767253933 / 62872364692131569638734867237718772414897487626'
mkdir -p "$O"
run() { echo "+ $*" >&2; nice -n 19 "$PY" -I "$@"; }

if [[ "$PART" == all || "$PART" == part1 ]]; then
  run "$D/selftest.py" --out "$O/selftest.json" --random 400 --seed 895
  run "$D/certcheck.py" "$Y" --out "$O/check-yim-n260-ccw.json" --label yim-n260-ccw
  run "$D/certcheck.py" "$Y" --sense cw --out "$O/check-yim-n260-cw.json" --label yim-n260-cw-reversed-sense
  run "$D/certcheck.py" "$T" --out "$O/check-t257-s260-ccw.json" --label t257-s260-ccw
  run "$D/certcheck.py" "$T" --sense cw --out "$O/check-t257-s260-cw.json" --label t257-s260-cw-reversed-sense
  run "$D/side.py" --yim "$Y" --t257 "$T" --issue-fraction "$FRACTION" --out "$O/side.json"
  run "$D/identity.py" --yim "$Y" --t257 "$T" --house "$H" --out "$O/identity.json"
  run "$D/upright.py" --yim "$Y" --t257 "$T" --out "$O/upright.json"
  run "$D/movers.py" --yim "$Y" --t257 "$T" --out "$O/movers.json" --tau 0.1 0.01 0.001
fi
if [[ "$PART" == all || "$PART" == part2 ]]; then
  run "$D/controls.py" "$Y" --out "$O/controls.json"
  run "$D/slides.py" --yim "$Y" --t257 "$T" --out "$O/slides.json" --tau 0.1
  run "$D/rowsback.py" --yim "$Y" --t257 "$T" --out "$O/rowsback.json"
fi
if [[ "$PART" == custody ]]; then
  run "$D/custody.py" --clone "$5" --packet "$W/yim-s260-upper-bound-2026-11-05" --repo . --out "$O/custody.json"
fi
