#!/bin/bash
# A241 -- the DEPTH ladder for the window-statement campaign.
#
#   nohup bash attempts/A241-row-cascade/code/chain241.sh > attempts/A241-row-cascade/logs/chain241.log 2>&1 &
#
# Why: k4_07's 4D run FAILs at depth 48 with 40 witness boxes and **0 HOLES** on all three anchorings, worst
# witness at s = 191/50 with exact mass 581917/500000 = 1.1638 >= 1 -- i.e. the boxes are UNDECIDED at the cap,
# not refuted.  verify_param.py shares one depth budget across (t, x, y, s) and reached max_s_depth 11, so the
# lever is simply more depth.  This runs the ladder 48 -> 56 -> 64, each pass over the classes the previous one
# did not TRANSFER (param241.py skips a class whose row already says TRANSFERRED, so each pass is a no-op on the
# ones that landed).  No extra python process: it waits for the current pass to leave the CPU before starting the
# next, so at most the driver + its one verifier child are ever mine.
#
# RESUME BLOCK: re-running this exact command is safe at any time -- every pass is the idempotent param241.sh, the
# rows are the same file, and a TRANSFERRED class is never re-run.  `touch attempts/A241-row-cascade/logs/STOP`
# stops the inner campaign cleanly; `touch attempts/A241-row-cascade/logs/STOP_CHAIN` stops the ladder.
cd "$(dirname "$0")/../../.." || exit 1
A=attempts/A241-row-cascade
export PYTHONDONTWRITEBYTECODE=1

running() { powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter 'Name=\"python.exe\"' | Where-Object { \$_.CommandLine -match 'param241' } | Measure-Object | Select-Object -ExpandProperty Count" | tr -d '\r '; }

for D in 48 56 64; do
  [ -f $A/logs/STOP_CHAIN ] && { echo "$(date +%H:%M:%S) STOP_CHAIN present: exiting"; exit 0; }
  while [ "$(running)" -gt 0 ] 2>/dev/null; do sleep 120; done
  [ -f $A/logs/STOP ] && { echo "$(date +%H:%M:%S) STOP present: exiting"; exit 0; }
  LEFT=$(python - <<'EOF'
import json, os
f = "attempts/A241-row-cascade/results/param241.jsonl"
done = set()
if os.path.exists(f):
    for ln in open(f, encoding="utf-8", errors="replace"):
        ln = ln.strip()
        if ln:
            r = json.loads(ln)
            if r.get("result") == "TRANSFERRED":
                done.add(r["name"])
print(9 - len(done))
EOF
)
  LEFT=$(echo "$LEFT" | tr -d '\r ')
  if [ "${LEFT:-0}" -eq 0 ]; then echo "$(date +%H:%M:%S) all nine classes TRANSFERRED -- ladder done"; exit 0; fi
  echo "$(date +%H:%M:%S) == depth $D pass ($LEFT class(es) still without a window statement)"
  bash $A/code/param241.sh 5400 $D >> $A/logs/param241.log 2>&1
done
echo "$(date +%H:%M:%S) A241 depth ladder drained"
