#!/bin/bash
# A241 -- the window-statement campaign: A56's parametric layer re-run on A55's exact k <= 4 kills,
# one class at a time (param241.py is one of my two python processes, its subprocess the other),
# with a commit after every class.
#
#   nohup bash attempts/A241-row-cascade/code/param241.sh > attempts/A241-row-cascade/logs/param241.log 2>&1 &
#
# RESUME BLOCK: param241.py appends one row per class to results/param241.jsonl as soon as it is known
# and skips any class already TRANSFERRED, so re-running this exact command after a kill picks up where
# it stopped.  `touch attempts/A241-row-cascade/logs/STOP` stops it cleanly between classes.
# Never touches the k5 frontier workers, the frontier loop, A238's sweep, A239, A240 or A211's certs.
cd "$(dirname "$0")/../../.." || exit 1
A=attempts/A241-row-cascade
WALL=${1:-2400}
DEPTH=${2:-48}
export PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
mkdir -p $A/logs $A/certs $A/results
PATHS="$A/certs $A/results $A/logs $A/code"

commit() {
  local msg="$1" k
  for k in 1 2 3; do
    git add -- $PATHS 2>/dev/null
    if git diff --cached --quiet -- $PATHS 2>/dev/null; then return 0; fi
    if git commit -q -m "$msg

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>" -- $PATHS 2>/dev/null; then return 0; fi
    sleep $((4 * k))
  done
  echo "$(date +%H:%M:%S) commit failed (index busy) for: $msg"
}

for CLS in k4_07 k4_10 k4_12 k4_02 k4_04 k4_00 k4_01 k4_09 k3_00; do
  [ -f $A/logs/STOP ] && { echo "$(date +%H:%M:%S) STOP present: exiting"; exit 0; }
  echo "$(date +%H:%M:%S) == $CLS"
  python $A/code/param241.py --only "$CLS" --depth "$DEPTH" --wall "$WALL"
  V=$(python - "$CLS" <<'EOF'
import json, os, sys
n = sys.argv[1]; f = "attempts/A241-row-cascade/results/param241.jsonl"; out = "?"
if os.path.exists(f):
    for ln in open(f, encoding="utf-8", errors="replace"):
        try: r = json.loads(ln)
        except Exception: continue
        if r.get("name") == n:
            out = "%s anchoring=%s param=%ss c2=%s" % (
                r.get("result"), r.get("anchoring"), r.get("param_time_s"),
                "/".join(c["result"][0] for c in (r.get("c2") or [])) or "-")
print(out)
EOF
)
  echo "$(date +%H:%M:%S) $CLS -> $V"
  commit "A241: $CLS window statement [$V]"
  python $A/code/rowcascade241.py --apply >> $A/logs/rowcascade.log 2>&1
  commit "A241: rowcascade after $CLS"
done
echo "$(date +%H:%M:%S) A241 param campaign drained"
python $A/code/rowcascade241.py --apply --report >> $A/logs/rowcascade.log 2>&1
commit "A241: param campaign drained -- cascade re-run"
