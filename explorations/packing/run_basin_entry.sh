#!/usr/bin/env bash
# H-018 basin entry: start inside Trump's packing, perturb outward, measure the return.
#
# Three arms, because "does the search return" turns out to be two different questions:
#   quench-1x / quench-10x  local quench at t_hot = eps -- does the configuration have
#                           an attracting neighbourhood, and is reaching it effort-bound?
#   hot                     the campaign's own schedule (t_hot = 0.25) -- does the
#                           annealer that exp-003 ran hold the basin when handed it?
#
# Every record is archived. The seed configuration is exported from the exact packing
# by tools/export_trump11.py and is f64 from that point on: nothing here may certify.
set -euo pipefail
cd "$(dirname "$0")"

OUT=campaign/series/series-000-smoke-and-calibration/results/exp-005-basin-entry.jsonl
SEED_CFG=${SEED_CFG:-/tmp/trump11-seed.json}
EPS=${EPS:-0,1e-5,1e-4,1e-3,1e-2,1e-1}
TRIALS=${TRIALS:-40}
BIN=./sqsearch/target/release/sqsearch

$BIN --selftest | tail -1 | grep -q "SELFTEST PASSED" || { echo "selftest failed; refusing to record" >&2; exit 1; }
python3 tools/export_trump11.py > "$SEED_CFG"

: > "$OUT"
for arm in "quench-1x --steps 400000" "quench-10x --steps 4000000" "hot --steps 400000 --t-hot 0.25"; do
  name=${arm%% *}; flags=${arm#* }
  echo "arm $name ($flags)" >&2
  $BIN --basin-entry --seed-config "$SEED_CFG" --eps "$EPS" --trials "$TRIALS" --seed 1 $flags \
    | python3 -c "
import json,sys
for line in sys.stdin:
    d=json.loads(line); d['arm']='$name'; print(json.dumps(d))
" >> "$OUT"
done
echo "wrote $OUT ($(wc -l < "$OUT") records)" >&2
