#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$ROOT/build"
python3 "$ROOT/scripts/check_certificate.py"
python3 "$ROOT/scripts/verify_filter.py"
g++ -std=c++17 -O3 -march=native -fopenmp -I"$ROOT/src" "$ROOT/src/verify_event_partition.cpp" -o "$ROOT/build/verify_event_partition"
"$ROOT/build/verify_event_partition" 8 "$ROOT/data/event_polys_filtered.tsv" "$ROOT/data/orientation_samples.tsv"
g++ -std=c++17 -O3 -march=native "$ROOT/src/verify_endpoints.cpp" -o "$ROOT/build/verify_endpoints"
"$ROOT/build/verify_endpoints" "$ROOT/data/atoms.csv"
echo 'Run scripts/run_coverage_ranges.sh for the complete 148,937-cell audit.'
