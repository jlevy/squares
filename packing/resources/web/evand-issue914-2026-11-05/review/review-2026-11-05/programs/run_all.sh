#!/usr/bin/env bash
# Rerun every program of the #914 stage 4 review and bind the receipts to the programs.
#
# Usage: run_all.sh PY CANDIDATES_DIR PACKET_SOURCE_DIR REVIEW_DIR
#   PY                 the project interpreter, packing/.venv/bin/python3 (CPython 3.14)
#   CANDIDATES_DIR     packing/resources/web/evand-issue914-2026-11-05/source/search/packer/candidates
#   PACKET_SOURCE_DIR  packing/resources/web/evand-issue914-2026-11-05/source
#   REVIEW_DIR         the directory holding programs/ and out/ (out/houses/, out/issue914/
#                      and out/upstream-bb4cc78/ are inputs fetched once and kept)
# At most two processes at a time, at nice 19. About 0.11 CPU-hours.
set -euo pipefail
PY="$1"; C="$2"; SRC="$3"; R="$4"
PR="$R/programs"; O="$R/out"
cd "$PR"
sha256sum ./*.py ./run_all.sh > "$O/program-digests.txt"
run() { nice -n 19 "$PY" -I "$@"; }
FILES="s175_1105 s204_trig1 s260_ks_1105 s268_1105 s293_1105 s303_1105 s304_1105 s175_1105_regularized s204_trig1_regularized s268_1105_regularized s293_1105_regularized s303_1105_regularized s304_1105_regularized"
run "$PR/self_test.py" "$O/self-test.json"
mkdir -p "$O/feasibility" "$O/reversed-sense" "$O/controls"
for f in $FILES; do echo "$f"; done | xargs -P 2 -I{} nice -n 19 "$PY" -I "$PR/decide_feasibility.py" "$C/{}.cert" "$O/feasibility/{}.json" --label {} > "$O/feasibility/run-log.txt"
for f in $FILES; do echo "$f"; done | xargs -P 2 -I{} nice -n 19 "$PY" -I "$PR/decide_feasibility.py" "$C/{}.cert" "$O/reversed-sense/{}.json" --sense -1 --label {}-reversed > "$O/reversed-sense/run-log.txt"
for f in $FILES; do echo "$f"; done | xargs -P 2 -I{} sh -c "nice -n 19 '$PY' -I '$PR/sharp_controls.py' '$C/{}.cert' '$O/controls/{}.json' --label {} > '$O/controls/{}.log' 2>&1"
run "$PR/sides_and_kkt.py" "$C" "$O/houses" "$O/sides-and-kkt.json" > "$O/sides-and-kkt.log"
run "$PR/house_slack.py" "$C" "$O/houses" "$O/slack-and-contacts.json" > "$O/slack-and-contacts.log"
run "$PR/scale_slack.py" "$C" "$O/houses" "$O/scale-slack.json" > "$O/scale-slack.log"
run "$PR/identity.py" "$C" "$O/houses" "$O/slack-and-contacts.json" "$O/identity.json" > "$O/identity.log"
run "$PR/island_260.py" "$C/s260_ks_1105.cert" "$O/houses/T-257-s260_1028.cert" "$O/houses/W-known-best-n260.yaml" "$O/island-260.json" > "$O/island-260.log"
run "$PR/tilts.py" "$C" "$O/houses" "$O/tilts.json" > "$O/tilts.log"
run "$PR/input_260.py" "$C" "$O/input-260.json" > "$O/input-260.log"
run "$PR/custody.py" "$SRC" "$O/issue914/issue914.json" "$O/upstream-bb4cc78" "$O/custody.json" > "$O/custody.log"
echo "done"
