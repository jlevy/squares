#!/bin/sh
# #610 negative control: zmx2 cert --d4 (6b7f0f79, built from retained bytes) on a mutated
# s(95) cover (make_mutants.py) over one root region, under devtools.replay_receipt, with
# zmx2's default --uncert-cap as the s(59), s(77) and s(76) controls ran.
#   run_control.sh KIND XLO XHI YLO YHI [THREADS]
set -eu
PK=${PK:-/home/user/squares/.claude/worktrees/agent-a33e48ec7ed2cb8d8/packing}
SP=${SP:-/tmp/claude-0/-home-user-squares/387dc0a2-0a91-51c6-bf71-f69e33945398/scratchpad/i610}
Z=$SP/zmx2work/6b7f0f79/verify2/target/release/zmx2
KIND=$1; XLO=$2; XHI=$3; YLO=$4; YHI=$5; T=${6:-1}
C=$SP/mut/s95_$KIND.txt
O=$SP/out/controls
mkdir -p "$O"
NAME="n95_control_${KIND}_zmx2_d4_x$XLO-${XHI}_y$YLO-$YHI"
rm -f "$O/$NAME.log" "$O/${NAME}_roots.log"
cd "$PK"
.venv/bin/python3 -m devtools.replay_receipt --receipt "$O/$NAME.log" \
  --cwd-label "scratch: zmx2.rs 6b7f0f79466bf25c9a85f8fe2f3866de734935f0521ea188136818c2fb5b3fed built from retained bytes (binary sha256 $(sha256sum "$Z" | cut -d' ' -f1)); cover $(sha256sum "$C" | cut -d' ' -f1), the $KIND mutation (devtools.replay_evand_zmx2.mutate) of 8b2d2152867585c82920bc90c6c3ec2a2458ef2ba57311ccd7dd436d1344cb7c" \
  --chdir "$O" -- "$Z" cert "$C" --d4 --threads "$T" \
  --xlo "$XLO" --xhi "$XHI" --ylo "$YLO" --yhi "$YHI" --bins 0-3 --log "$O/${NAME}_roots.log" || true
grep -E "^done|VERIFIED|^roots" "$O/$NAME.log"
