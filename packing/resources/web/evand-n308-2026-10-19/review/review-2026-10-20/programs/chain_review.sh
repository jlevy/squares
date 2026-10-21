#!/bin/bash
# Runs this review's programs serially, niced, from packing/, logging UTC start, end,
# wall and exit status of each. CLONE is the blobless clone custody_1020.py reads.
set -u
W="$(cd "$(dirname "$0")/../../../../../.." && pwd)"
cd "$W" || exit 1
PY="$W/.venv/bin/python3"
P=resources/web/evand-n308-2026-10-19/review/review-2026-10-20
O=$P/outputs
CLONE="${CLONE:?set CLONE to the blobless clone of evand/square-packing}"
C308=resources/web/evand-n308-2026-10-19/source/search/packer/candidates
C154=resources/web/evand-n154-sweep-2026-10-20/source/search/packer/candidates
run() { local name=$1; shift; echo "== $(date -u +%FT%TZ) START $name"; local t0=$(date +%s); nice -n 10 "$PY" -I "$@" > "$O/$name.log" 2>&1; local rc=$?; echo "== $(date -u +%FT%TZ) END $name rc=$rc wall=$(( $(date +%s) - t0 ))s"; }
run third_route $P/programs/third_route_1020.py --json $O/third_route.json $C308/s308_d308.cert $C154/s154_sw.cert
run custody $P/programs/custody_1020.py --clone "$CLONE" --json $O/custody.json evand-n308-2026-10-19 evand-n154-sweep-2026-10-20
run construction $P/programs/construction_1020.py --json $O/construction.json
run receipt_totals $P/programs/receipt_totals_1020.py --json $O/receipt_totals.json
run adoption $P/programs/adoption_1020.py --json $O/adoption.json
run lineage $P/programs/lineage_1020.py --json $O/lineage.json
