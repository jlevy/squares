#!/bin/bash
# A242 POST -- after run242.sh ends (its log has "final rc="): adopt242 --dry-run, then the Lean audit
# (lean/audit.py builds Main + Statements through A78's serialised lakeb.py), then one commit.  At most 2 pythons
# (audit.py + lakeb.py), and only after the replay's two shards have exited.
#   ( "/c/Program Files/Git/bin/bash.exe" -c "cd /c/Users/esumm/code/packing && nohup bash attempts/A242-replay-31-8/code/post242.sh \
#        >> attempts/A242-replay-31-8/logs/post242.log 2>&1" & )
# RESUME: relaunch the same line (it re-waits, re-runs both steps, commits).
cd "$(dirname "$0")/../../.." || exit 1
ATT=attempts/A242-replay-31-8; LOG=$ATT/logs
export PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
echo "$(date '+%F %T') post242 waiting for run242"
until grep -q "final rc=" $LOG/replay242.log 2>/dev/null; do sleep 60; done
python $ATT/code/adopt242.py --dry-run > $LOG/adopt242.log 2>&1; echo "$(date '+%F %T') adopt242 rc=$?"
python lean/audit.py > $LOG/audit242.log 2>&1; RC=$?; echo "$(date '+%F %T') audit rc=$RC"; tail -5 $LOG/audit242.log
P="$ATT/results/adopt242_dryrun.json $ATT/results/adopt242_dryrun.txt $LOG/adopt242.log $LOG/audit242.log $LOG/post242.log lean/AUDIT.md"
Q=""; for f in $P; do [ -e "$f" ] && Q="$Q $f"; done
for i in 1 2 3 4 5; do
  git add -- $Q 2>/dev/null
  if git commit -q -m "A242: adopt242 --dry-run list + Lean audit (rc=$RC) after the replay" -- $Q 2>/dev/null; then
    git fetch -q 2>/dev/null && git merge -q --no-edit 2>/dev/null; git push -q 2>/dev/null; break
  fi
  git diff --cached --quiet -- $Q 2>/dev/null && break
  sleep $((5*i))
done
echo "$(date '+%F %T') post242 done"
