#!/bin/sh
# #610 triage: replay zm_mixed.py (ee3e2915, with mixed_cover.py bb89de15 and zeromargin.py
# 640fe453, all from this repository's retained evand packets) on sub-roots of the s(95)
# cover with the flags the source's verify.sh uses, P jobs in parallel (default 1), each
# under devtools.replay_receipt. JOBS is a file in the format of the source's
# records/zm_mixed/jobs.txt: the whole list, or a sample written by zm_sample.py.
#   run_zm_mixed.sh JOBS [P]
set -eu
PK=${PK:-/home/user/squares/.claude/worktrees/agent-a33e48ec7ed2cb8d8/packing}
SP=${SP:-/tmp/claude-0/-home-user-squares/387dc0a2-0a91-51c6-bf71-f69e33945398/scratchpad/i610}
WEB=$PK/resources/web
CK=$SP/zmcheck
C=$SP/data/s95_cover_v2.txt
O=$SP/out/zm_mixed
JOBS=$1
P=${2:-1}
mkdir -p "$CK" "$O"
cp "$WEB/evand-square-packing-2026-09-28/square-packing/s12/search/zm_mixed.py" "$CK/"
cp "$WEB/evand-square-packing-2026-09-28/square-packing/s12/search/mixed_cover.py" "$CK/"
cp "$WEB/evand-square-packing-2026-09-26/square-packing/s12/search/zeromargin.py" "$CK/"
( cd "$CK" && sha256sum zm_mixed.py mixed_cover.py zeromargin.py ) > "$O/checker.sha256"
grep -q '^ee3e2915349b8795128417bca6414b205d526db9f01f88cd4cd32c32e8d760ac  zm_mixed.py$' "$O/checker.sha256"
grep -q '^bb89de15ecf5821dd7e1a36ebab8a50d792a406b7fb0f5cb38059f99ef74aae5  mixed_cover.py$' "$O/checker.sha256"
grep -q '^640fe453c1a32f4aa580ca2b1261c6406923a4d7c131f65604a432c7fc2086ab  zeromargin.py$' "$O/checker.sha256"
[ "$(sha256sum "$C" | cut -d' ' -f1)" = 8b2d2152867585c82920bc90c6c3ec2a2458ef2ba57311ccd7dd436d1344cb7c ]
echo "checker and cover digests OK"
export PK CK C O
# One job per line: id cx_lo cx_hi cy_lo cy_hi u_lo u_hi
xargs -P "$P" -L 1 sh -c '
  i=$0
  rm -f "$O/j$i.jsonl"
  cd "$CK"
  "$PK/.venv/bin/python3" -I "$PK/devtools/replay_receipt.py" --receipt "$O/j$i.log" \
    --cwd-label "scratch checker dir: zm_mixed.py ee3e2915, mixed_cover.py bb89de15, zeromargin.py 640fe453 (retained evand packets); cover 8b2d2152867585c82920bc90c6c3ec2a2458ef2ba57311ccd7dd436d1344cb7c" \
    --python-note "the project interpreter, $("$PK/.venv/bin/python3" --version 2>&1), run with -I" \
    --chdir "$CK" -- "$PK/.venv/bin/python3" -I -u "$CK/zm_mixed.py" cert "$C" \
    --d4 --cert-mode --disj --chain-from 0 --pitch 1/20 --ubins 16 --depth 24 --nproc 1 \
    --cx-lo "$1" --cx-hi "$2" --cy-lo "$3" --cy-hi "$4" --u-lo "$5" --u-hi "$6" \
    --resume "$O/j$i.jsonl" || echo "job $i exit $?" >> "$O/failures.txt"
' < "$JOBS"
echo "all jobs ended"
