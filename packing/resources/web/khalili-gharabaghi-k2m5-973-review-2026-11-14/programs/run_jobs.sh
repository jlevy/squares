#!/bin/bash
# Run a job list "name|command" two at a time under nice -n 19, each under a wall cap.
# usage: run_jobs.sh JOBS OUTDIR CAP_SECONDS [PARALLEL]
# For each job: OUTDIR/name.out (stdout+stderr) and OUTDIR/name.time ("real user sys exit").
# A job whose .time file exists is skipped, so the list can be resumed.
set -u
jobs=$1; outd=$2; cap=$3; par=${4:-2}
mkdir -p "$outd"
export outd cap
grep -v '^\s*$' "$jobs" | xargs -d '\n' -P "$par" -n 1 bash -c '
  line=$0; name=${line%%|*}; cmd=${line#*|}
  [ -f "$outd/$name.time" ] && exit 0
  TIMEFORMAT="%R %U %S"
  { time timeout "$cap" nice -n 19 bash -c "$cmd" > "$outd/$name.out" 2>&1; echo "exit $?" > "$outd/$name.rc"; } 2> "$outd/$name.time.tmp"
  echo "$(cat "$outd/$name.time.tmp") $(cat "$outd/$name.rc")" > "$outd/$name.time"; rm -f "$outd/$name.time.tmp" "$outd/$name.rc"
  echo "$(date -u +%T) $name $(cat "$outd/$name.time")"
'
