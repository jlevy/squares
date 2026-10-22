#!/bin/sh
# Run the maintained routes on the certificate: the positive job with the kernel's own
# sharp controls in one process, and the two gross controls in a second.
# Usage: run_maintained.sh CERT OUTDIR PACKING PYTHON
set -u
CERT=$1; OUT=$2; PACKING=$3; PY=$4
HERE=$(cd "$(dirname "$0")" && pwd)
cd "$PACKING" || exit 2
( nice -n 10 "$PY" -I "$HERE/maintained_routes_728.py" "$CERT" --packing "$PACKING" --n 303 \
    --control positive --sharp --out "$OUT/maintained-positive.json" > "$OUT/maintained-positive.txt" 2>&1
  echo "exit $?" >> "$OUT/maintained-positive.txt" ) &
( for c in duplicate-square-overlap square-translated-outside-container; do
    nice -n 10 "$PY" -I "$HERE/maintained_routes_728.py" "$CERT" --packing "$PACKING" --n 303 \
      --control $c --out "$OUT/maintained-$c.json" > "$OUT/maintained-$c.txt" 2>&1
    echo "exit $?" >> "$OUT/maintained-$c.txt"
  done ) &
wait
