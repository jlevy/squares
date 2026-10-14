#!/bin/bash
# A241 -- the TRACTION check: A238's benchmark re-run on k3_02's 20 A100 head-to-head cover cells
# WITH the new forced cells, against A238's blind run (0 DEAD / 20 ALIVE, 4.3 s, 0 kills, depth 0).
#
#   nohup bash attempts/A241-row-cascade/code/traction241.sh 300 > attempts/A241-row-cascade/logs/traction241.log 2>&1 &
#
# ISOLATED: --cert-dir / --results point at A241's own dirs, so A238's sweep, its certs and its
# bench238.jsonl are never touched; the k5 frontier workers, the frontier loop, A239, A240 and A211's
# certs are never touched either.  A238's code is imported unchanged (frozen verifiers untouched).
#
# RESUME BLOCK: one row per node is appended to results/traction241.jsonl as soon as the node is
# decided and a node that already has a row is skipped, so re-running this exact command after a kill
# picks up where it stopped.  `touch attempts/A241-row-cascade/logs/STOP_TRACTION` stops it cleanly.
# It first waits (5 min per poll, detached -- no turn of mine waits on it) until the row cascade has
# actually given k3_02 a usable forced cell: a run before that would just re-measure A238's blind run.
cd "$(dirname "$0")/../../.." || exit 1
A=attempts/A241-row-cascade
WALL=${1:-300}; NODES=${2:-600}; DEPTH=${3:-6}
Q=$A/code/queue_k3_02.txt
export PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
export A220_NOROOM_INHERIT=1 A221_LANE=1 A224_SNAP=1 A230_EPS=1 A238_SNAP_AT_GATE=1
mkdir -p $A/logs $A/certs_traction $A/results
PATHS="$A/certs_traction $A/results $A/logs $A/code"

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

usable() { python - <<'EOF'
import os, sys
sys.path.insert(0, "attempts/A241-row-cascade/code")
import load_cl241 as L
CL = L.classes(); CL._SB = None
print(sum(1 for r in CL.forced_cells("k3_02") if r["usable"]))
EOF
}

N=$(usable | tr -d '\r ')
while [ "${N:-0}" -lt 1 ]; do
  [ -f $A/logs/STOP_TRACTION ] && { echo "$(date +%H:%M:%S) STOP_TRACTION present: exiting"; exit 0; }
  echo "$(date +%H:%M:%S) k3_02 usable forced cells = $N -- waiting for the row cascade"
  sleep 300
  N=$(usable | tr -d '\r ')
done
echo "$(date +%H:%M:%S) k3_02 usable forced cells = $N -- running the 20 head-to-head cells, wall ${WALL}s"

while read -r NID REST; do
  NID=${NID//$'\r'/}
  [ -z "$NID" ] && continue
  case "$NID" in \#*) continue;; esac
  [ -f $A/logs/STOP_TRACTION ] && { echo "$(date +%H:%M:%S) STOP_TRACTION present: exiting"; exit 0; }
  if grep -q "\"$NID\"" $A/results/traction241.jsonl 2>/dev/null; then
    echo "$(date +%H:%M:%S) $NID: already decided -- skipped"; continue
  fi
  # my own python processes only (A241's campaign + its verifier child + this node): cap 2, so wait
  while [ "$(powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter 'Name=\"python.exe\"' | Where-Object { \$_.CommandLine -match 'param241|verify_param|verify_case|A241' } | Measure-Object | Select-Object -ExpandProperty Count" | tr -d '\r ')" -gt 1 ] 2>/dev/null; do sleep 60; done
  echo "$(date +%H:%M:%S) == $NID"
  python attempts/A238-k4-benchmark/code/run238.py page "$NID" --wall $WALL --nodes $NODES --depth $DEPTH \
      --no-fig --cert-dir $A/certs_traction --results $A/results/traction241.jsonl >> $A/logs/node_k3_02.log 2>&1
  RC=$?
  V=$(python - "$NID" <<'EOF'
import json, os, sys
nid = sys.argv[1]; f = "attempts/A241-row-cascade/results/traction241.jsonl"; out = "?"
if os.path.exists(f):
    for ln in open(f, encoding="utf-8", errors="replace"):
        try: r = json.loads(ln)
        except Exception: continue
        if r.get("nid") == nid:
            out = "%s nodes=%s s=%s gate=%s rules=%s" % (r.get("verdict"), r.get("n_nodes"),
                                                         r.get("seconds"), r.get("gate_hits"),
                                                         r.get("kills_by_rule"))
print(out)
EOF
)
  echo "$(date +%H:%M:%S) $NID -> $V (rc=$RC)"
  commit "A241 traction: $NID [$V] rc=$RC"
done < "$Q"
echo "$(date +%H:%M:%S) A241 traction queue drained"
python $A/code/traction241.py >> $A/logs/traction241_report.log 2>&1
commit "A241: traction queue drained -- results/traction241.md refreshed"
