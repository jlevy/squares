#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
mkdir -p "$ROOT/build" "$ROOT/logs/reproduction_coverage"
g++ -std=c++17 -O3 -march=native -fopenmp "$ROOT/src/verify_coverage_segment.cpp" -o "$ROOT/build/verify_coverage_segment"
N=148937; CH=5000
for ((a=0;a<N;a+=CH)); do
 b=$((a+CH)); ((b>N)) && b=$N
 out="$ROOT/logs/reproduction_coverage/${a}_${b}.out"
 ok=0
 for try in 1 2 3 4 5; do
  timeout -k 2 120 "$ROOT/build/verify_coverage_segment" 1 "$ROOT/data/atoms.csv" "$ROOT/data/orientation_samples.tsv" "$a" "$b" > "$out" 2> "$out.log" || true
  if grep -q 'EXACT SEGMENT COVERAGE PASS' "$out"; then ok=1; break; fi
 done
 if [[ $ok -ne 1 ]]; then echo "range failed: $a $b" >&2; exit 1; fi
 cat "$out"
done
python3 "$ROOT/scripts/summarize_coverage.py" "$ROOT/logs/reproduction_coverage"
