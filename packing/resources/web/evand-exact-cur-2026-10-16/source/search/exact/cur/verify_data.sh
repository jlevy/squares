#!/usr/bin/env bash
# Replay verify_exact.py (stdlib only) on the exact forms of current records added 2026-10-15: cur/data/n-N.minpoly.json.gz.
# Writes cur/data/verify.txt (one line per n) and prints the count of VALID.  PROCS parallel (default 8).
cd "$(dirname "$0")/.."
ls cur/data/n-*.minpoly.json.gz | sort -t- -k2 -n | xargs -P "${PROCS:-8}" -I{} sh -c \
  'timeout 3600 python3 verify_exact.py {} 2>&1 | tail -1' > cur/data/verify.txt
sort -t- -k2 -n -o cur/data/verify.txt cur/data/verify.txt
echo "VALID: $(grep -c ': VALID\.' cur/data/verify.txt) of $(ls cur/data/n-*.minpoly.json.gz | wc -l)"
