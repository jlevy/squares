#!/bin/sh
# Run Daniel's zmx2 (6b7f0f79, built from retained bytes) over all D4 roots of the s(76) cover,
# under the repository's replay_receipt wrapper.
PK=/home/user/squares/.claude/worktrees/agent-a1f00b5caa2265822/packing
SP=/tmp/claude-0/-home-user-squares/387dc0a2-0a91-51c6-bf71-f69e33945398/scratchpad
Z=$SP/zmx2work/6b7f0f79/verify2/target/release/zmx2
C=$SP/data594/s76_cover_v5.txt
O=$SP/out594
THREADS=${1:-3}
rm -f "$O/zmx2_cert_d4.receipt"
cd "$PK" || exit 2
.venv/bin/python3 -m devtools.replay_receipt --receipt "$O/zmx2_cert_d4.log" \
  --cwd-label "scratch: zmx2 6b7f0f79 built from retained bytes (binary sha256 $(sha256sum "$Z" | cut -d' ' -f1)); cover sha256 $(sha256sum "$C" | cut -d' ' -f1)" \
  --chdir "$O" -- "$Z" cert "$C" --d4 --threads "$THREADS" --uncert-cap 200000 --log "$O/zmx2_cert_d4_roots.log"
echo "exit $?"
