#!/bin/sh
# Replay zm_mixed.py (ee3e2915, with mixed_cover.py bb89de15 and zeromargin.py 640fe453, all
# from this repository's retained evand packets) on the 64 sub-roots the s(76) source lists,
# with the flags its verify.sh uses, P jobs in parallel, under replay_receipt.
set -eu
PK=/home/user/squares/.claude/worktrees/agent-a1f00b5caa2265822/packing
SP=/tmp/claude-0/-home-user-squares/387dc0a2-0a91-51c6-bf71-f69e33945398/scratchpad
WEB=$PK/resources/web
CK=$SP/zmcheck
C=$SP/data594/s76_cover_v5.txt
O=$SP/out594/zm_mixed
JOBS=$SP/src594/s76-certificate/records/zm_mixed/jobs.txt
P=${1:-3}
mkdir -p "$CK" "$O"
cp "$WEB/evand-square-packing-2026-09-28/square-packing/s12/search/zm_mixed.py" "$CK/"
cp "$WEB/evand-square-packing-2026-09-28/square-packing/s12/search/mixed_cover.py" "$CK/"
cp "$WEB/evand-square-packing-2026-09-26/square-packing/s12/search/zeromargin.py" "$CK/"
( cd "$CK" && sha256sum zm_mixed.py mixed_cover.py zeromargin.py ) > "$O/checker.sha256"
grep -q '^ee3e2915349b8795128417bca6414b205d526db9f01f88cd4cd32c32e8d760ac  zm_mixed.py$' "$O/checker.sha256"
grep -q '^bb89de15ecf5821dd7e1a36ebab8a50d792a406b7fb0f5cb38059f99ef74aae5  mixed_cover.py$' "$O/checker.sha256"
grep -q '^640fe453c1a32f4aa580ca2b1261c6406923a4d7c131f65604a432c7fc2086ab  zeromargin.py$' "$O/checker.sha256"
echo "checker digests OK"
export PK CK C O
# One job per line of jobs.txt: id cx_lo cx_hi cy_lo cy_hi u_lo u_hi
xargs -P "$P" -L 1 sh -c '
  i=$0
  cd "$CK"
  "$PK/.venv/bin/python3" -I "$PK/devtools/replay_receipt.py" --receipt "$O/j$i.log" \
    --cwd-label "scratch checker dir: zm_mixed.py ee3e2915, mixed_cover.py bb89de15, zeromargin.py 640fe453 (retained evand packets)" \
    --chdir "$CK" -- "$PK/.venv/bin/python3" -I -u "$CK/zm_mixed.py" cert "$C" \
    --d4 --cert-mode --disj --chain-from 0 --pitch 1/20 --ubins 16 --depth 24 --nproc 1 \
    --cx-lo "$1" --cx-hi "$2" --cy-lo "$3" --cy-hi "$4" --u-lo "$5" --u-hi "$6" \
    --resume "$O/j$i.jsonl" || echo "job $i exit $?" >> "$O/failures.txt"
' < "$JOBS"
echo "all jobs ended"
