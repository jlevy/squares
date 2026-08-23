#!/usr/bin/env bash
# Baseline round for series 001: the stock engine at each cell of the declared
# sweep, five seeds per cell, equal move budget per chain.
#
# n=10 is the positive control (s(10) is proved), n=11 the target, n=12 the
# negative control (the 4x4 grid is almost certainly optimal, so a run that
# "beats" it has found a bug, not a packing).
set -euo pipefail
cd "$(dirname "$0")"
OUT=campaign/series/001-smoke-n11/results/exp-001-baseline.jsonl
BIN=sqsearch/target/release/sqsearch

"$BIN" --selftest || { echo "engine selftest failed; refusing to record"; exit 1; }

: > "$OUT"
for n in 10 11 12; do
  for seed in 1 2 3 4 5; do
    "$BIN" --n "$n" --seed "$seed" --chains 8 --budget-moves 100000000 \
      | grep '"kind":"summary"' >> "$OUT"
  done
done
echo "BASELINE DONE: $(grep -c . "$OUT") summaries"
