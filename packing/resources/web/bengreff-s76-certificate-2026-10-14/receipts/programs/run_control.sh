#!/bin/sh
# Negative control for #594: zmx2 cert --d4 (6b7f0f79, built from retained bytes) on a mutated
# s(76) cover over one root region, under the repository's replay_receipt wrapper, with zmx2's
# default --uncert-cap as the s(59) and s(77) controls ran.
# usage: run_control.sh KIND XLO XHI YLO YHI [THREADS]
PK=/home/user/squares/.claude/worktrees/agent-a1f00b5caa2265822/packing
SP=/tmp/claude-0/-home-user-squares/387dc0a2-0a91-51c6-bf71-f69e33945398/scratchpad
Z=$SP/zmx2work/6b7f0f79/verify2/target/release/zmx2
KIND=$1; XLO=$2; XHI=$3; YLO=$4; YHI=$5; T=${6:-1}
C=$SP/mut594/s76_$KIND.txt
O=$SP/out594/controls2
mkdir -p "$O"
NAME="n76_control_${KIND}_zmx2_d4_x$XLO-${XHI}_y$YLO-$YHI"
rm -f "$O/$NAME.log" "$O/${NAME}_roots.log"
cd "$PK" || exit 2
.venv/bin/python3 -m devtools.replay_receipt --receipt "$O/$NAME.log" \
  --cwd-label "scratch: zmx2.rs 6b7f0f79466bf25c9a85f8fe2f3866de734935f0521ea188136818c2fb5b3fed built from retained bytes (binary sha256 $(sha256sum "$Z" | cut -d' ' -f1)); cover $(sha256sum "$C" | cut -d' ' -f1), the $KIND mutation (devtools.replay_evand_zmx2.mutate) of b6a1214b99f00e5dd136d74c8d87bccd178df38a1063b2c7be90517eb2b862b2" \
  --chdir "$O" -- "$Z" cert "$C" --d4 --threads "$T" \
  --xlo "$XLO" --xhi "$XHI" --ylo "$YLO" --yhi "$YHI" --bins 0-3 --log "$O/${NAME}_roots.log"
echo "exit $?"
grep -E "^done|VERIFIED|^roots" "$O/$NAME.log"
