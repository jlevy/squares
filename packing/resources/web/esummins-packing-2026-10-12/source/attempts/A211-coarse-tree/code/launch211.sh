#!/bin/bash
# A211 -- THE ONE DETACHED LAUNCHER: N worker slots (each a worker211.sh over the gallery queue then the frontier
# queue, gated per launch at 10 lab pythons / 6 of A211's / 3072 MB free) plus the hourly progress.md commit.
#   nohup bash attempts/A211-coarse-tree/code/launch211.sh [N=4] [WALL=1800] > attempts/A211-coarse-tree/logs/launch211.out 2>&1 &
# Resume: the same command (claims in logs/claims/ skip the nodes already taken; remove a claim dir to re-run a node;
# touch logs/STOP to stop the workers after their current node, logs/HOURLY_STOP to stop the hourly loop).
cd "$(dirname "$0")/../../.." || exit 1
ATT=attempts/A211-coarse-tree
N=${1:-4}; WALL=${2:-1800}
export PYTHONDONTWRITEBYTECODE=1
mkdir -p $ATT/logs
echo "$(date '+%Y-%m-%d %H:%M:%S') A211 launcher: $N worker slots, wall $WALL s per pad; queues code/queue_gallery.txt then code/queue_frontier.txt; pid $$" | tee -a $ATT/logs/launch211.log
for i in $(seq 1 $N); do
  SLOT=w$i
  nohup bash $ATT/code/worker211.sh $SLOT $WALL $ATT/code/queue_gallery.txt $ATT/code/queue_frontier.txt > $ATT/logs/worker_$SLOT.out 2>&1 &
  echo "$(date +%H:%M:%S) worker $SLOT pid $!" | tee -a $ATT/logs/launch211.log
  sleep 90                                   # stagger: the gate reads the lab count between launches
done
while true; do
  sleep 3600
  python $ATT/code/fold211.py >> $ATT/logs/fold211.log 2>&1
  python $ATT/code/progress211.py >> $ATT/logs/progress211.log 2>&1
  git add -- $ATT/results/progress.md $ATT/results/superseded_by_coarsetree_A211.jsonl 2>/dev/null
  git commit -q -m "A211: hourly progress.md $(date '+%Y-%m-%d %H:%M')" -- $ATT/results/progress.md $ATT/results/superseded_by_coarsetree_A211.jsonl 2>/dev/null
  [ -f $ATT/logs/HOURLY_STOP ] && { echo "$(date +%H:%M:%S) HOURLY_STOP: launcher exiting" | tee -a $ATT/logs/launch211.log; exit 0; }
  if ! pgrep -f "worker211.sh" > /dev/null 2>&1; then echo "$(date +%H:%M:%S) no worker left: launcher exiting" | tee -a $ATT/logs/launch211.log; exit 0; fi
done
