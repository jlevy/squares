#!/bin/bash
# Runs the maintained acquisition and replay checks serially, niced, logging UTC start/end/exit.
W=/tmp/claude-0/-home-user-squares/4d60ed7e-c8f7-58a7-a1b1-aeee5c887ef3/scratchpad/wt-699/packing
cd "$W" || exit 1
PY="$W/.venv/bin/python3"
run() { echo "== $(date -u +%FT%TZ) START $*"; local t0=$(date +%s); nice -n 10 "$PY" -m "$@"; local rc=$?; echo "== $(date -u +%FT%TZ) END rc=$rc wall=$(( $(date +%s) - t0 ))s $*"; }
for P in evand-n308-2026-10-19 evand-n154-sweep-2026-10-20; do
  run devtools.acquire_source "$P" --check
  run devtools.upper_bound_reports "$P" check-claims
  run devtools.upper_bound_reports "$P" check
  run devtools.upper_bound_reports "$P" check --replay
done
