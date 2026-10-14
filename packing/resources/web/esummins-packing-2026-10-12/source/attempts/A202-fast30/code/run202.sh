#!/bin/bash
# A202 launcher: stage 0 (closed form, both pads, page drawn) then stage 1 (A200's exact table on the surviving cells) over
# the k5_16 / k5_11 pages of one shard; each page under `timeout -s KILL`; the lab ceiling (12 pythons excluding
# "Claude Extensions" command lines) counted and WAITED on before every page; a git commit after every page.
#   bash run202.sh <shard> <nshard> [wall] [pages...]
cd "$(dirname "$0")/../../.." || exit 1
ATT=attempts/A202-fast30; RES=$ATT/results/fast30.jsonl
SHARD=${1:-0}; NSHARD=${2:-1}; WALL=${3:-600}; shift 3 2>/dev/null
export PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
if [ $# -gt 0 ]; then PAGES="$@"; else PAGES=$(awk -F, 'NR>1 && $15=="ALIVE-at-LP" && ($4=="k5_16"||$4=="k5_11"){print $2}' docs/shadows/a57v4/review_a57v4.csv | sort); fi
labcount() { powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter 'Name=\"python.exe\"' | Where-Object { \$_.CommandLine -notmatch 'Claude Extensions' } | Measure-Object | Select-Object -ExpandProperty Count" | tr -d '\r '; }
k=0
for P in $PAGES; do
  k=$((k+1)); if [ $(( (k-1) % NSHARD )) -ne "$SHARD" ]; then continue; fi
  if grep -q "\"nid\": \"$P\".*\"stage\": 1" $RES 2>/dev/null || grep "\"nid\": \"$P\"" $RES 2>/dev/null | grep -q '"pad": "g1".*"verdict": "DEAD"'; then echo "skip $P (done)"; continue; fi
  while [ "$(labcount)" -ge 12 ]; do sleep 60; done
  LOG=$ATT/logs/f30_${P}.log; SVG=docs/residue_map/fast30_${P}.svg
  T0=$(date +%s); echo "$(date +%H:%M:%S) start $P"
  timeout -s KILL $((2*WALL+120)) python $ATT/code/run202.py $P --wall $WALL >> $LOG 2>&1
  RC=$?
  if [ $RC -eq 137 ]; then echo "{\"nid\": \"$P\", \"verdict\": \"ALIVE\", \"stage\": 1, \"pad\": \"-\", \"leaf\": \"wall $((2*WALL+120))s reached (process killed): undecided\", \"seconds\": $(( $(date +%s) - T0 )), \"killed\": true, \"when\": \"$(date '+%Y-%m-%d %H:%M:%S')\"}" >> $RES; fi
  V=$(grep "\"nid\": \"$P\"" $RES | tail -1 | grep -o '"verdict": "[A-Z]*"\|"stage": [0-9]\|"pad": "[a-z0-9]*"' | tr '\n' ' ')
  for i in 1 2 3 4 5 6; do
    git add -- $RES $ATT/certs $ATT/logs $SVG 2>/dev/null
    if git commit -q -m "A202: $P [$V] $(( $(date +%s) - T0 ))s" -- $RES $ATT/certs $ATT/logs $SVG 2>/dev/null; then break; fi
    sleep $((5*i))
  done
  echo "$(date +%H:%M:%S) $P $V rc=$RC $(( $(date +%s) - T0 ))s"
done
