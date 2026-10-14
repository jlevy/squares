#!/bin/bash
# A211 worker (A209's worker209 adapted): drain queue files (one nid per line) through run211.py, one node at a time;
# claims by mkdir (atomic) so several workers share a queue; gated before EVERY launch on the lab ceiling (10 pythons
# excluding "Claude Extensions" command lines), on A211's own count (<= 6) and on free memory (>= 3072 MB physical);
# BLAS pinned; BelowNormal + affinity 0xFFFF set INSIDE run211.py (A210's working fix); the node re-checked against
# the closure ledgers (A57 / A149 / A209 / A211) before it runs (Lemma K1); after every node: the audit of its DEAD
# leaves (audit211, capped), fold211 (the closure ledger), progress211 (results/progress.md, the price and the STOP
# rule), the CURRENT pages refreshed, git add / commit with explicit pathspecs.  Exits when logs/STOP exists.
#   bash worker211.sh <slot name> <wall> <queue file> [<queue file> ...]
cd "$(dirname "$0")/../../.." || exit 1
ATT=attempts/A211-coarse-tree; RES=$ATT/results; PAGES=docs/residue_map/campaigns/A211-coarsetree
export PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
SLOT=${1:-w}; WALL=${2:-1800}; shift 2
labcount() { powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter 'Name=\"python.exe\"' | Where-Object { \$_.CommandLine -notmatch 'Claude Extensions' } | Measure-Object | Select-Object -ExpandProperty Count" | tr -d '\r '; }
mine() { powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter 'Name=\"python.exe\"' | Where-Object { \$_.CommandLine -match 'run211|audit211' } | Measure-Object | Select-Object -ExpandProperty Count" | tr -d '\r '; }
freemb() { powershell -NoProfile -Command "[int]((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1024)" | tr -d '\r '; }
mkdir -p $ATT/logs/claims
for Q in "$@"; do
  while read -r NID W; do
    NID=${NID//$'\r'/}; W=${W//$'\r'/}
    [ -z "$NID" ] && continue
    case "$NID" in \#*) continue;; esac
    [ -f $ATT/logs/STOP ] && { echo "$(date +%H:%M:%S) [$SLOT] STOP present: exiting"; exit 0; }
    mkdir "$ATT/logs/claims/$NID" 2>/dev/null || continue
    if python $ATT/code/fold211.py --closed "$NID" >/dev/null 2>&1; then echo "$(date +%H:%M:%S) [$SLOT] $NID already closed (ledger / ancestor): skipped"; continue; fi
    WW=${W:-$WALL}
    while [ "$(labcount)" -ge 10 ] || [ "$(mine)" -ge 6 ] || [ "$(freemb)" -lt 3072 ]; do sleep 60; done
    LOG=$ATT/logs/coarsetree211_${NID}.log
    T0=$(date +%s); echo "$(date +%H:%M:%S) [$SLOT] start $NID wall $WW (lab $(labcount), free $(freemb) MB)" | tee -a $LOG
    timeout -s KILL $(( 2 * WW + 1200 )) python $ATT/code/run211.py page $NID --wall $WW >> $LOG 2>&1
    RC=$?
    # A228: a row for EVERY non-zero exit, not just the 137 wall kill -- the pass-5 SIGSEGV (rc 139) of
    # k5_16_interior_Y0402 left no row at all in results/coarsetree211.jsonl and no mark in progress.md, so the
    # crash was invisible to every ledger.  A crashed / killed run is recorded as ALIVE + killed (undecided),
    # never as a verdict; a CRASH additionally releases its claim and is written to logs/requeue.txt so the pad is
    # offered again (the page is re-run next pass in any case).
    if [ $RC -ne 0 ]; then
      case $RC in
        137) WHY="process wall $(( 2 * WW + 1200 )) s reached (killed)";;
        139) WHY="CRASHED: SIGSEGV (rc 139) -- see A228";;
        134) WHY="CRASHED: abort (rc 134)";;
        *)   WHY="run211 exited rc=$RC";;
      esac
      echo "{\"nid\": \"$NID\", \"run\": \"process\", \"mode\": \"page\", \"pad\": \"g1\", \"verdict\": \"ALIVE\", \"leaf\": \"$WHY: undecided\", \"seconds\": $(( $(date +%s) - T0 )), \"killed\": true, \"rc\": $RC, \"when\": \"$(date '+%Y-%m-%d %H:%M:%S')\"}" >> $RES/coarsetree211.jsonl
      echo "$(date '+%Y-%m-%d %H:%M:%S') [$SLOT] $NID rc=$RC $WHY" >> $ATT/logs/requeue.txt
      echo "$NID $WW" >> $ATT/logs/requeue.txt
      if [ $RC -ne 137 ]; then rmdir "$ATT/logs/claims/$NID" 2>/dev/null; fi
    fi
    # the audit of this node's DEAD leaves (sampling; <= 6 leaves, <= 240 s each)
    python $ATT/code/audit_queue211.py --nid "$NID" 2>/dev/null | tr -d '\r' | head -6 | while read -r ANID KEY LEAF; do
      [ -z "$ANID" ] && continue
      ALOG=$ATT/logs/audit_${ANID}_${KEY}.log
      echo "$(date +%H:%M:%S) audit $ANID $KEY $LEAF" >> $ALOG
      timeout -s KILL 240 python $ATT/code/audit211.py "$ANID" "$KEY" "$LEAF" >> $ALOG 2>&1 && echo "$ANID $KEY $LEAF" >> $ATT/logs/audit_done.txt
    done
    python $ATT/code/fold211.py >> $ATT/logs/fold211.log 2>&1
    python $ATT/code/progress211.py >> $ATT/logs/progress211.log 2>&1
    python docs/residue_map/refresh_current.py > /dev/null 2>&1
    V=$(grep -o "== $NID: g1 [^|]*| pad0 [^(]*" $LOG | tail -1)
    for i in 1 2 3 4 5 6; do
      git add -- $RES $ATT/certs $ATT/logs $PAGES docs/residue_map/current 2>/dev/null
      if git commit -q -m "A211: $NID [$V] $(( $(date +%s) - T0 ))s rc=$RC" -- $RES $ATT/certs $ATT/logs $PAGES docs/residue_map/current 2>/dev/null; then break; fi
      sleep $((5*i))
    done
    echo "$(date +%H:%M:%S) [$SLOT] $NID $V rc=$RC $(( $(date +%s) - T0 ))s" | tee -a $LOG
  done < "$Q"
  echo "$(date +%H:%M:%S) [$SLOT] queue $Q done"
done
