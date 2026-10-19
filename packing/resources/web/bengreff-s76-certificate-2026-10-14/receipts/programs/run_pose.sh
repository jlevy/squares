#!/bin/sh
# Exact pose check for #594: zm_mixed.py pose (ee3e2915, with mixed_cover.py bb89de15 and
# zeromargin.py 640fe453 from the retained evand packets) at one rational pose of a cover,
# under replay_receipt.  usage: run_pose.sh NAME COVER CX CY U NOTE
PK=/home/user/squares/.claude/worktrees/agent-a1f00b5caa2265822/packing
SP=/tmp/claude-0/-home-user-squares/387dc0a2-0a91-51c6-bf71-f69e33945398/scratchpad
CK=$SP/zmcheck
O=$SP/out594/controls2
NAME=$1; C=$2; CX=$3; CY=$4; U=$5; NOTE=$6
mkdir -p "$O"
( cd "$CK" && sha256sum zm_mixed.py mixed_cover.py zeromargin.py ) | grep -c -E '^(ee3e2915349b8795128417bca6414b205d526db9f01f88cd4cd32c32e8d760ac  zm_mixed.py|bb89de15ecf5821dd7e1a36ebab8a50d792a406b7fb0f5cb38059f99ef74aae5  mixed_cover.py|640fe453c1a32f4aa580ca2b1261c6406923a4d7c131f65604a432c7fc2086ab  zeromargin.py)$' | grep -qx 3 || { echo "checker digests differ"; exit 2; }
"$PK/.venv/bin/python3" -I "$PK/devtools/replay_receipt.py" --receipt "$O/$NAME.log" \
  --cwd-label "scratch checker dir: zm_mixed.py ee3e2915, mixed_cover.py bb89de15, zeromargin.py 640fe453 (retained evand packets); cover $(sha256sum "$C" | cut -d' ' -f1), $NOTE" \
  --python-note "the project interpreter, $("$PK/.venv/bin/python3" --version 2>&1), run with -I" \
  --chdir "$CK" -- "$PK/.venv/bin/python3" -I -u "$CK/zm_mixed.py" pose "$C" --cx "$CX" --cy "$CY" --u "$U"
grep -E 'EXACT' "$O/$NAME.log"
