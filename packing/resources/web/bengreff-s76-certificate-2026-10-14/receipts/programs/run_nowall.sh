#!/bin/sh
# Wall-segment control for #594: zmx2 cert --d4 (6b7f0f79, built from retained bytes) over all
# 8,100 D4 roots of the s(76) cover with its 16 container-wall segments removed (mass 1/25000000),
# under replay_receipt. A sound checker certifies the stripped cover wherever it certifies the
# original, since no unit square needs mass on the container's walls.
PK=/home/user/squares/.claude/worktrees/agent-a1f00b5caa2265822/packing
SP=/tmp/claude-0/-home-user-squares/387dc0a2-0a91-51c6-bf71-f69e33945398/scratchpad
Z=$SP/zmx2work/6b7f0f79/verify2/target/release/zmx2
C=$SP/mut594/s76_nowall.txt
O=$SP/out594/controls2
T=${1:-2}
mkdir -p "$O"
NAME="n76_control_nowall_zmx2_d4"
rm -f "$O/$NAME.log" "$O/${NAME}_roots.log"
cd "$PK" || exit 2
.venv/bin/python3 -m devtools.replay_receipt --receipt "$O/$NAME.log" \
  --cwd-label "scratch: zmx2.rs 6b7f0f79466bf25c9a85f8fe2f3866de734935f0521ea188136818c2fb5b3fed built from retained bytes (binary sha256 $(sha256sum "$Z" | cut -d' ' -f1)); cover $(sha256sum "$C" | cut -d' ' -f1), b6a1214b99f00e5dd136d74c8d87bccd178df38a1063b2c7be90517eb2b862b2 with its 16 wall segments removed" \
  --chdir "$O" -- "$Z" cert "$C" --d4 --threads "$T" --uncert-cap 200000 --log "$O/${NAME}_roots.log"
echo "exit $?"
grep -E "^done|VERIFIED|^roots|^cover" "$O/$NAME.log"
