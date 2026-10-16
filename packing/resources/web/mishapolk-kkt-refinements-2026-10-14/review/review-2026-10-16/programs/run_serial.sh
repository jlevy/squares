#!/bin/bash
# Run one heavy command at a time under the lane's CPU lock, niced, logging UTC times,
# wall seconds and the exit status. Usage: run_serial.sh LABEL -- command args...
set -u
SCR=/tmp/claude-0/-home-user/497b954f-f1d7-5565-9258-beec4cbe400c/scratchpad/laneC
LABEL=$1; shift; [ "$1" = "--" ] && shift
LOG=$SCR/replay/$LABEL.log
cd /home/user/squares/.claude/worktrees/review-185/packing
exec 9>$SCR/cpu.lock
flock 9
START=$(date -u +%Y-%m-%dT%H:%M:%SZ); S=$(date +%s.%N)
echo "start $START: $*" > $LOG
nice -n 10 "$@" >> $LOG 2>&1
RC=$?
E=$(date +%s.%N); END=$(date -u +%Y-%m-%dT%H:%M:%SZ)
printf 'end %s exit %d wall %.1f s\n' "$END" "$RC" "$(echo "$E - $S" | bc)" >> $LOG
echo "$LABEL start $START end $END exit $RC wall $(echo "$E - $S" | bc)" >> $SCR/replay/SUMMARY.txt
flock -u 9
exit $RC
