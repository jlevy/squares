#!/usr/bin/env bash
# Run one command niced under a lock file, so that one heavy process of this review
# runs at a time, and log its UTC start, its output, its UTC end, wall and exit status.
#
#   run_serial.sh LOG -- COMMAND...
#
# Run from packing/. LOCK defaults to /dev/shm/rv-evand-work/serial.lock.
set -u
log="$1"; shift
[ "$1" = "--" ] && shift
lock="${LOCK:-/dev/shm/rv-evand-work/serial.lock}"
mkdir -p "$(dirname "$log")" "$(dirname "$lock")"
exec 9>"$lock"
flock 9
start=$(date -u +%Y-%m-%dT%H:%M:%SZ)
t0=$(date +%s.%N)
echo "START $start load=$(cut -d' ' -f1-3 /proc/loadavg) cmd: $*" >"$log"
nice -n 10 "$@" >>"$log" 2>&1
status=$?
t1=$(date +%s.%N)
end=$(date -u +%Y-%m-%dT%H:%M:%SZ)
wall=$(echo "$t1 - $t0" | bc)
echo "END $end exit=$status wall=${wall}s load=$(cut -d' ' -f1-3 /proc/loadavg)" >>"$log"
exit $status
