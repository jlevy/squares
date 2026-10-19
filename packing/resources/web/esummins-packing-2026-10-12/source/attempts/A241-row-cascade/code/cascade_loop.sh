#!/bin/bash
# A241 -- the 10-minute cascade loop, as a BRIDGE until the status loop picks up its new body.
#
#   nohup bash attempts/A241-row-cascade/code/cascade_loop.sh 36 > attempts/A241-row-cascade/logs/cascade_loop.log 2>&1 &
#
# `docs/shadows/status_loop.sh` was edited by RENAME (it is running), so the running bash still executes the OLD
# inode -- kept as `status_loop.sh.pre_a241` -- and the new `rowcascade241.py --apply --report` line only takes
# effect when that loop is relaunched (it was started 2026-09-15 23:59 with a 48 h horizon).  This loop supplies
# the same cadence in the meantime and is a NO-OP once the status loop carries the line: rowcascade241.py is
# idempotent, so whichever runs first simply finds nothing to add.  It also commits the A56 scoreboard, which
# param241.sh's own pathspecs do not cover.
#
# RESUME BLOCK: re-running this command is always safe.  `touch attempts/A241-row-cascade/logs/STOP_CASCADE` stops it.
# No python process of its own beyond the short cascade run; never touches the frontier workers or their loops.
cd "$(dirname "$0")/../../.." || exit 1
A=attempts/A241-row-cascade
HOURS=${1:-36}; END=$(( $(date +%s) + HOURS * 3600 ))
export PYTHONDONTWRITEBYTECODE=1
PATHS="$A/results $A/logs attempts/A56-sparametric/results/scoreboard.json attempts/A56-sparametric/results/scoreboard.json.bak_pre_a241"
while [ "$(date +%s)" -lt "$END" ]; do
  [ -f $A/logs/STOP_CASCADE ] && { echo "$(date +%H:%M:%S) STOP_CASCADE present: exiting"; exit 0; }
  python $A/code/rowcascade241.py --apply --report >> $A/logs/rowcascade.log 2>&1
  git add -- $PATHS 2>/dev/null
  if ! git diff --cached --quiet -- $PATHS 2>/dev/null; then
    git commit -q -m "A241: row cascade $(date +%H:%M) -- scoreboard rows and results/rows241.md refreshed

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>" -- $PATHS 2>/dev/null && echo "$(date +%H:%M:%S) committed"
  fi
  sleep 600
done
echo "$(date +%H:%M:%S) horizon reached: exiting"
