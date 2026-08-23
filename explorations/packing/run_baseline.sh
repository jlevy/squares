#!/usr/bin/env bash
# Baseline round: the stock engine at each cell of the declared sweep, five seeds
# per cell, equal move budget per chain. Takes the archive path as its argument so
# a re-run under a changed engine lands in its own round rather than overwriting an
# earlier one -- the record is corrected by addition, never in place.
#
# n=10 is the positive control (s(10) is proved), n=11 the target, n=12 the
# negative control (the 4x4 grid is almost certainly optimal, so a run that
# "beats" it has found a bug, not a packing).
set -euo pipefail
cd "$(dirname "$0")"
OUT="${1:?usage: run_baseline.sh <output.jsonl>}"
BIN=sqsearch/target/release/sqsearch

"$BIN" --selftest || { echo "engine selftest failed; refusing to record"; exit 1; }

: > "$OUT"
for n in 10 11 12; do
  for seed in 1 2 3 4 5; do
    # Archive EVERY line, not just the summaries. The per-chain records carry the
    # actual configurations (x, y, t) and the recomputed overlap -- without them a
    # round's packings cannot be regenerated from its own archive, and they are also
    # exactly the raw material the basin atlas is built from.
    "$BIN" --n "$n" --seed "$seed" --chains 8 --budget-moves 100000000 >> "$OUT"
  done
done
echo "BASELINE DONE: $(grep -c . "$OUT") summaries"
