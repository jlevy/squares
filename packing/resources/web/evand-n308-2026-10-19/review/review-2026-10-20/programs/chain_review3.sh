#!/bin/bash
# Third run: the registered clipping-area route on both certificates.
set -u
W="$(cd "$(dirname "$0")/../../../../../.." && pwd)"
cd "$W" || exit 1
PY="$W/.venv/bin/python3"
P=resources/web/evand-n308-2026-10-19/review/review-2026-10-20
O=$P/outputs
run() { local name=$1; shift; echo "== $(date -u +%FT%TZ) START $name"; local t0=$(date +%s); nice -n 10 "$PY" -I "$@" > "$O/$name.log" 2>&1; local rc=$?; echo "== $(date -u +%FT%TZ) END $name rc=$rc wall=$(( $(date +%s) - t0 ))s"; }
run area_route $P/programs/area_route_1020.py --json $O/area_route.json
