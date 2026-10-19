#!/bin/bash
# A202: recompute STAGE 0 (both pads) with the final code over every page of one shard (stage 1 certs stay), redraw the
# pages, then the gallery; lab ceiling counted before every page.   bash refresh202.sh <shard> <nshard>
cd "$(dirname "$0")/../../.." || exit 1
ATT=attempts/A202-fast30
SHARD=${1:-0}; NSHARD=${2:-1}
export PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
PAGES=$(awk -F, 'NR>1 && $15=="ALIVE-at-LP" && ($4=="k5_16"||$4=="k5_11"){print $2}' docs/shadows/a57v4/review_a57v4.csv | sort)
labcount() { powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter 'Name=\"python.exe\"' | Where-Object { \$_.CommandLine -notmatch 'Claude Extensions' } | Measure-Object | Select-Object -ExpandProperty Count" | tr -d '\r '; }
k=0
for P in $PAGES; do
  k=$((k+1)); if [ $(( (k-1) % NSHARD )) -ne "$SHARD" ]; then continue; fi
  while [ "$(labcount)" -ge 12 ]; do sleep 60; done
  T0=$(date +%s)
  timeout -s KILL 900 python $ATT/code/run202.py $P --force-stage0 --stage0-only >> $ATT/logs/refresh_${P}.log 2>&1
  echo "$(date +%H:%M:%S) $P refreshed rc=$? $(( $(date +%s) - T0 ))s"
done
