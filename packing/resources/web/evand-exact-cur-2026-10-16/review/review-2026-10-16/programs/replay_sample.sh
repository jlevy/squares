#!/bin/bash
# Re-run the source's verify_exact.py, unchanged from its retained copy, on three of #639's
# exact forms, one python -I process at a time under nice -n 10, and log each run's UTC
# start and end, wall and CPU seconds, exit status and last line. Run from packing/.
# $1: directory holding the fetched pinned-only forms; $2: log file.
CHECKER=resources/web/evand-exact-and-local-reports-2026-10-12/source/search/exact/verify_exact.py
DATA=resources/web/evand-exact-cur-2026-10-16/source/search/exact/cur/data
TIMEFORMAT='wall %R s, user %U s, sys %S s'
sha256sum "$CHECKER" >> "$2"
for f in "$DATA/n-126.minpoly.json.gz" "$DATA/n-266.minpoly.json.gz" "$1/n-267.minpoly.json.gz"; do
  sha256sum "$f" >> "$2"
  start=$(date -u +%H:%M:%SZ)
  { time nice -n 10 .venv/bin/python3 -I "$CHECKER" "$f" > "$2.out" 2>&1; status=$?; } 2> "$2.time"
  echo "$start to $(date -u +%H:%M:%SZ): $(cat "$2.time"), exit $status" >> "$2"
  tail -1 "$2.out" | sed 's|^.*/||' >> "$2"
done
