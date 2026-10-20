#!/bin/bash
# Second run: adoption and lineage again after fixing this review's own report code
# (the case record's front-matter indentation; T-135, T-182 read through the #484 and #586 packets).
set -u
W="$(cd "$(dirname "$0")/../../../../../.." && pwd)"
cd "$W" || exit 1
PY="$W/.venv/bin/python3"
P=resources/web/evand-n308-2026-10-19/review/review-2026-10-20
O=$P/outputs
run() { local name=$1; shift; echo "== $(date -u +%FT%TZ) START $name"; local t0=$(date +%s); nice -n 10 "$PY" -I "$@" > "$O/$name.log" 2>&1; local rc=$?; echo "== $(date -u +%FT%TZ) END $name rc=$rc wall=$(( $(date +%s) - t0 ))s"; }
run adoption $P/programs/adoption_1020.py --json $O/adoption.json
run lineage $P/programs/lineage_1020.py --json $O/lineage.json
