#!/usr/bin/env bash
# Decide nodes 1 to 200 with r144_bnb.py, in ranges of 25, one process at a time, and stop
# before the run's CPU passes the budget (seconds, default 7200: the coordinator's 2
# CPU-hours). Node 0 is decided by r144_axis.py. Added after the controls plan, on the
# coordinator's word (disclosed in the review as a post-plan run).
#
# Usage: r144_run_all.sh BUNDLE_DIR OUT_DIR [BUDGET_SECONDS]
# Each range writes OUT_DIR/range-AAA-BBB.json (rewritten after every node, so a stopped
# range keeps the nodes it finished), its printed lines to range-AAA-BBB.stdout.txt, and
# its process CPU (user + system, by bash's time) to range-AAA-BBB.done.
set -euo pipefail
BUNDLE=$1
OUT=$2
BUDGET=${3:-7200}
HERE=$(cd "$(dirname "$0")" && pwd)
PY=${PY:-/home/user/squares/packing/.venv/bin/python3}
mkdir -p "$OUT"
spent=0
for a in 1 26 51 76 101 126 151 176; do
  b=$((a + 24))
  name=$(printf 'range-%03d-%03d' "$a" "$b")
  if [ -s "$OUT/$name.done" ]; then
    spent=$((spent + $(cat "$OUT/$name.done")))
    continue
  fi
  left=$((BUDGET - spent))
  if [ "$left" -le 60 ]; then
    echo "budget spent before $name ($spent s)" | tee -a "$OUT/run.log"
    exit 2
  fi
  angles=$(seq -s, "$a" "$b")
  start=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  TIMEFORMAT='%U %S'
  status=0
  { time (
      ulimit -t "$left"
      OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 19 "$PY" -I -B "$HERE/r144_bnb.py" \
        --bundle "$BUNDLE" --angles "$angles" --out "$OUT/$name.json" > "$OUT/$name.stdout.txt" 2>&1
    ) ; } 2> "$OUT/$name.time" || status=$?
  cpu=$(awk '{printf "%d", $1 + $2 + 0.5}' "$OUT/$name.time")
  spent=$((spent + cpu))
  if [ "$status" -ne 0 ]; then
    echo "$name stopped: exit $status at $(date -u +%Y-%m-%dT%H:%M:%SZ), $cpu CPU-s, $spent CPU-s so far" | tee -a "$OUT/run.log"
    exit 3
  fi
  echo "$cpu" > "$OUT/$name.done"
  echo "$name done: $start to $(date -u +%Y-%m-%dT%H:%M:%SZ), $cpu CPU-s, $spent CPU-s so far" | tee -a "$OUT/run.log"
done
echo "all ranges done: $spent CPU-s" | tee -a "$OUT/run.log"
