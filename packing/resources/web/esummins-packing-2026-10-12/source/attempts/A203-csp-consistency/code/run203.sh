#!/bin/bash
# A203 launcher: stage 0 + the CSP (closed form, both pads, page drawn) over the pages A202 left ALIVE at stage 0, one
# shard; the lab ceiling (12 pythons excluding "Claude Extensions" command lines) counted and WAITED on before every
# page; a git commit after every page.      bash run203.sh <shard> <nshard> [pages...]
cd "$(dirname "$0")/../../.." || exit 1
ATT=attempts/A203-csp-consistency; RES=$ATT/results/csp203.jsonl
SHARD=${1:-0}; NSHARD=${2:-1}; shift 2 2>/dev/null
export PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
if [ $# -gt 0 ]; then PAGES="$@"; else PAGES=$(python - <<'PY'
import json
last={}
for l in open('attempts/A202-fast30/results/fast30.jsonl',encoding='utf-8'):
    d=json.loads(l)
    if d.get('stage')==0 and d.get('pad')=='g1': last[d['nid']]=d['verdict']
print(' '.join(sorted(n for n,v in last.items() if v=='ALIVE')))
PY
); fi
labcount() { powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter 'Name=\"python.exe\"' | Where-Object { \$_.CommandLine -notmatch 'Claude Extensions' } | Measure-Object | Select-Object -ExpandProperty Count" | tr -d '\r '; }
k=0
for P in $PAGES; do
  k=$((k+1)); if [ $(( (k-1) % NSHARD )) -ne "$SHARD" ]; then continue; fi
  if grep -q "\"nid\": \"$P\".*\"pad\": \"zero\"" $RES 2>/dev/null || grep "\"nid\": \"$P\"" $RES 2>/dev/null | grep -q '"pad": "g1".*"verdict": "DEAD"'; then echo "skip $P (done)"; continue; fi
  while [ "$(labcount)" -ge 12 ]; do sleep 60; done
  LOG=$ATT/logs/csp203_${P}.log; SVG=docs/residue_map/csp203_${P}.svg
  T0=$(date +%s); echo "$(date +%H:%M:%S) start $P"
  timeout -s KILL 400 python $ATT/code/run203.py $P >> $LOG 2>&1
  RC=$?
  if [ $RC -eq 137 ]; then echo "{\"nid\": \"$P\", \"verdict\": \"ALIVE\", \"stage\": 0, \"pad\": \"-\", \"leaf\": \"wall 400s reached (process killed): undecided\", \"seconds\": $(( $(date +%s) - T0 )), \"killed\": true, \"when\": \"$(date '+%Y-%m-%d %H:%M:%S')\"}" >> $RES; fi
  V=$(grep "\"nid\": \"$P\"" $RES | grep -o '"verdict": "[A-Z]*"\|"pad": "[a-z0-9]*"' | tr '\n' ' ')
  for i in 1 2 3 4 5 6; do
    git add -- $RES $ATT/certs $ATT/logs $SVG 2>/dev/null
    if git commit -q -m "A203: $P [$V] $(( $(date +%s) - T0 ))s" -- $RES $ATT/certs $ATT/logs $SVG 2>/dev/null; then break; fi
    sleep $((5*i))
  done
  echo "$(date +%H:%M:%S) $P $V rc=$RC $(( $(date +%s) - T0 ))s"
done
