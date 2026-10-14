#!/bin/bash
# A243 -- the detached chain (LAUNCH-AND-EXIT).  Two python processes at a time (the two workers of a phase).
#   nohup bash attempts/A243-climb-17-19/code/chain243.sh > attempts/A243-climb-17-19/logs/chain243.log 2>&1 &
# Phases (n = 17 before n = 19; the climb's nodes -- the classes containing the four corners -- before the rest):
#   P1  n=17 corners4 census k = 16 -> 4  (tree walls: 90 s for k >= 8, 300 s for 4 < k < 8, 1800 s at the k = 4 root)
#   P2  n=19 corners4 census k = 16 -> 4  (90 s for k >= 11, 300 s below, 1800 s at the root)
#   P3  n=17 full census k = 16 -> 1      (the remaining classes; the k = 2 / k = 1 roots of task 3 at 1800 s)
#   P4  n=19 full census k = 16 -> 1
#   P5  climb243.py + report243.py rebuild results/climb243.md and the tree jsonl
# RESUME: re-run this script; every class with a verdict is skipped.  STOP: touch logs/STOP.
cd "$(dirname "$0")" || exit 1
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
L=../logs
phase() {
  N=$1; shift
  echo "$(date '+%F %H:%M:%S') phase n=$N $*"
  bash worker243.sh $N 0 --commit "$@" > /dev/null 2>&1 &
  P0=$!
  sleep 5
  bash worker243.sh $N 1 "$@" > /dev/null 2>&1 &
  P1=$!
  wait $P0 $P1
  [ -f $L/STOP ] && { echo "$(date '+%F %H:%M:%S') STOP"; exit 0; }
  python climb243.py all > $L/climb243_last.log 2>&1
  python report243.py > $L/report243_last.log 2>&1
  git -C ../../.. add -- attempts/A243-climb-17-19/results attempts/A243-climb-17-19/logs docs/residue_map/campaigns/A243-climb-17-19 2>/dev/null
  git -C ../../.. commit -q -m "A243: phase done (n=$N $*) -- table, climb tree, report rebuilt

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" -- attempts/A243-climb-17-19/results attempts/A243-climb-17-19/logs docs/residue_map/campaigns/A243-climb-17-19
  echo "$(date '+%F %H:%M:%S') phase n=$N done"
}
phase 17 --corners4 --kmax 16 --kstop 4
phase 19 --corners4 --kmax 16 --kstop 4
phase 17 --kmax 16 --kstop 1
phase 19 --kmax 16 --kstop 1
echo "$(date '+%F %H:%M:%S') chain243 finished"
