#!/bin/bash
# A242 RUN -- replay of Kleddamag's certificate (s(11) > 31/8, T-037) at the pinned release, offline.
#   ( "/c/Program Files/Git/bin/bash.exe" -c "cd /c/Users/esumm/code/packing && nohup bash attempts/A242-replay-31-8/code/run242.sh \
#        >> attempts/A242-replay-31-8/logs/replay242.log 2>&1" & )
# Steps: integrity -> threshold algebra -> integrity again -> 2 row shards in parallel (the only 2 pythons) -> commit
#        -> independent_controls (their stdlib control) -> rows242 finish (row-by-row vs their evidence) -> final242
#        (verdict block in results/replay242.md; on PASS the adoption lines) -> commit.
# STOP:   touch attempts/A242-replay-31-8/logs/STOP242 (shards stop between rows only if killed; nothing else is killed)
# RESUME: rm -f logs/STOP242 and relaunch the SAME line: shards skip rows already in results/replay242_shard*.jsonl;
#         finished steps are skipped by their output files.
cd "$(dirname "$0")/../../.." || exit 1
ATT=attempts/A242-replay-31-8; CODE=$ATT/code; RES=$(pwd)/$ATT/results; LOG=$ATT/logs
export PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
mkdir -p $LOG $ATT/results
commit() {  # $1 message, rest: paths
  local m="$1"; shift; local P=""
  for f in "$@"; do [ -e "$f" ] && P="$P $f"; done
  for i in 1 2 3 4 5; do
    git add -- $P 2>/dev/null
    if git commit -q -m "$m" -- $P 2>/dev/null; then git fetch -q 2>/dev/null && git merge -q --no-edit 2>/dev/null; git push -q 2>/dev/null; return 0; fi
    git diff --cached --quiet -- $P 2>/dev/null && return 0
    sleep $((5*i))
  done
}
T0=$(date +%s); echo "$(date '+%F %T') A242 run start"
[ -f $LOG/STOP242 ] && { echo "STOP242 present"; exit 0; }
if [ ! -f $RES/integrity242.txt ]; then
  python $CODE/prio242.py check_integrity.py > $RES/integrity242.txt 2>&1
  python $CODE/prio242.py verify_threshold_algebra.py > $LOG/algebra242.log 2>&1; echo "algebra rc=$?"
  python $CODE/prio242.py check_integrity.py >> $RES/integrity242.txt 2>&1
  (cd $ATT/ext/repo && sha256sum global-certificate.json exact_mixed.py integer_sweep.py replay_parallel.py \
     independent_controls.py verify.py verify_threshold_algebra.py prepare_secondary.py replay_secondary_parallel.py \
     secondary-adaptation.json check_integrity.py MANIFEST.json) >> $RES/integrity242.txt
  cat $RES/integrity242.txt
fi
python $CODE/rows242.py shard 0 2 >> $LOG/shard0.log 2>&1 &
P0=$!
python $CODE/rows242.py shard 1 2 >> $LOG/shard1.log 2>&1 &
P1=$!
wait $P0; R0=$?; echo "$(date '+%F %T') shard 0 rc=$R0"
commit "A242: replay shard 0 of 2 (rc=$R0)" $ATT/results/replay242_shard0of2.jsonl $LOG/shard0.log $LOG/replay242.log $RES/integrity242.txt
wait $P1; R1=$?; echo "$(date '+%F %T') shard 1 rc=$R1"
commit "A242: replay shard 1 of 2 (rc=$R1)" $ATT/results/replay242_shard1of2.jsonl $LOG/shard1.log $LOG/replay242.log
if [ ! -f $RES/controls242.json ]; then
  python $CODE/prio242.py independent_controls.py global-certificate.json --output $RES/controls242.json > $LOG/controls242.log 2>&1
  echo "$(date '+%F %T') controls rc=$?"
fi
python $CODE/rows242.py finish 2 > $LOG/finish242.log 2>&1; echo "$(date '+%F %T') finish rc=$?"
cat $LOG/finish242.log | head -c 1500; echo
python $CODE/final242.py >> $LOG/replay242.log 2>&1; echo "$(date '+%F %T') final rc=$? wall $(( $(date +%s) - T0 ))s"
commit "A242: replay verdict -- full Python row replay + controls (see results/replay242.md)" \
  $ATT/results/replay242.json $ATT/results/controls242.json $ATT/results/replay242.md $LOG/controls242.log \
  $LOG/finish242.log $LOG/algebra242.log $LOG/replay242.log $ATT/results/adopt242_dryrun.txt \
  docs/residue_ledger.md attempts/REGISTRY.md LOG.md
