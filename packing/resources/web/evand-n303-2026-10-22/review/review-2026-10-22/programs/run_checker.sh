#!/bin/sh
# Run both routes of review_728_check.py on the certificate, as two processes.
# Usage: run_checker.sh CERT OUTDIR [PYTHON]
# Each route writes OUTDIR/route-R.json (full receipt), route-R.summary.json and route-R.time.
set -u
CERT=$1; OUT=$2; PY=${3:-python3}
HERE=$(dirname "$0")
SIDE=447744305431858194305431410441/25000000000000000000000000000
for R in Z C; do
  ( T0=$(date +%s.%N)
    nice -n 10 "$PY" -I "$HERE/review_728_check.py" "$CERT" --route $R \
      --expect-side $SIDE --out "$OUT/route-$R.json" > "$OUT/route-$R.summary.json" 2> "$OUT/route-$R.time"
    RC=$?
    T1=$(date +%s.%N)
    echo "route $R: exit $RC, wall $(echo "$T1 - $T0" | bc) s" >> "$OUT/route-$R.time" ) &
done
wait
