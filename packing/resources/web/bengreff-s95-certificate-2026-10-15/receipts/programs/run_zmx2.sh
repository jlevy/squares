#!/bin/sh
# #610 triage: Daniel's zmx2 (zmx2.rs 6b7f0f79, built from retained bytes by
# devtools.replay_evand_zmx2 build) on the s(95) cover, under devtools.replay_receipt.
#   run_zmx2.sh d4           exact D4 invariance (zmx2 d4)
#   run_zmx2.sh cert [T]     cert --d4 over all 10,000 D4 roots, T threads (default 1)
#   run_zmx2.sh nowall [T]   the same sweep on the cover without its wall segments
# PK is the repository's packing/, SP the scratch directory the triage ran in.
set -eu
PK=${PK:-/home/user/squares/.claude/worktrees/agent-a33e48ec7ed2cb8d8/packing}
SP=${SP:-/tmp/claude-0/-home-user-squares/387dc0a2-0a91-51c6-bf71-f69e33945398/scratchpad/i610}
Z=$SP/zmx2work/6b7f0f79/verify2/target/release/zmx2
O=$SP/out
MODE=$1; T=${2:-1}
mkdir -p "$O"
ZSHA=$(sha256sum "$Z" | cut -d' ' -f1)
LABEL="scratch: zmx2.rs 6b7f0f79466bf25c9a85f8fe2f3866de734935f0521ea188136818c2fb5b3fed built from retained bytes (binary sha256 $ZSHA)"
cd "$PK"
case $MODE in
  d4)
    C=$SP/data/s95_cover_v2.txt
    .venv/bin/python3 -m devtools.replay_receipt --receipt "$O/n95_zmx2_d4_invariance.log" \
      --cwd-label "$LABEL; cover $(sha256sum "$C" | cut -d' ' -f1)" \
      --chdir "$O" -- "$Z" d4 "$C" ;;
  cert)
    C=$SP/data/s95_cover_v2.txt
    rm -f "$O/n95_zmx2_d4.log" "$O/n95_zmx2_d4_roots.log"
    .venv/bin/python3 -m devtools.replay_receipt --receipt "$O/n95_zmx2_d4.log" \
      --cwd-label "$LABEL; cover $(sha256sum "$C" | cut -d' ' -f1)" \
      --chdir "$O" -- "$Z" cert "$C" --d4 --threads "$T" --uncert-cap 200000 \
      --log "$O/n95_zmx2_d4_roots.log" ;;
  nowall)
    C=$SP/mut/s95_nowall.txt
    mkdir -p "$O/controls"
    rm -f "$O/controls/n95_control_nowall_zmx2_d4.log" "$O/controls/n95_control_nowall_zmx2_d4_roots.log"
    .venv/bin/python3 -m devtools.replay_receipt --receipt "$O/controls/n95_control_nowall_zmx2_d4.log" \
      --cwd-label "$LABEL; cover $(sha256sum "$C" | cut -d' ' -f1), 8b2d2152867585c82920bc90c6c3ec2a2458ef2ba57311ccd7dd436d1344cb7c with its wall segments removed" \
      --chdir "$O/controls" -- "$Z" cert "$C" --d4 --threads "$T" --uncert-cap 200000 \
      --log "$O/controls/n95_control_nowall_zmx2_d4_roots.log" ;;
  *) echo "usage: run_zmx2.sh d4|cert|nowall [threads]" >&2; exit 2 ;;
esac
