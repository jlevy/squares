#!/bin/bash
# Re-check the s(44) = 7 certificate from scratch.
#   1. exact bookkeeping and D4 invariance (sanity.py, this repository, no shared code with the checkers)
#   2. zmx2 (Evan Daniel's Rust exact checker), D4-reduced sweep and full (unreduced) sweep
#   3. zm_mixed.py (Evan Daniel's separately written Python exact checker), D4 mode, complete two-stage run
#      (depth 24 everywhere, then depth 30 in every root left with uncertified boxes); see zm_mixed_check.py
# Requirements: git, python3 with numpy, Rust (cargo).  Checkers are pinned to evand/square-packing@659ee62.
# Usage:  bash verification/verify.sh [--fast]
#   --fast: sanity + zmx2 D4 + an audit of our recorded zm_mixed logs (~5 min)
#   default: also zmx2 full (~30 min) and the complete zm_mixed run (~140 CPU-hours, parallel, resumable)
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT=$(pwd); CERT=$ROOT/certificate/s44_cover_7.txt
PIN=659ee62e4a9d39542a1146e8b011cc3ab6407ede

echo "== certificate hash"; (cd certificate && sha256sum -c SHA256SUMS 2>/dev/null || shasum -a 256 -c SHA256SUMS)

echo "== 1. exact bookkeeping (total < 44, D4 invariance)"
python3 verification/sanity.py "$CERT" 44

mkdir -p build
if [ ! -d build/square-packing ]; then
  git clone -q https://github.com/evand/square-packing build/square-packing
fi
git -C build/square-packing checkout -q $PIN
echo "checkers pinned to evand/square-packing@$PIN"

echo "== 2a. zmx2, D4-reduced sweep"
(cd build/square-packing/verify2 && cargo build -q --release)
Z=build/square-packing/verify2/target/release/zmx2
$Z cert "$CERT" --d4 --log build/zmx2_d4.log | grep -E "^(VERIFIED|NOT VERIFIED|INCOMPLETE)|total"
echo "== audit of the recorded zm_mixed logs (verification/logs/zm_mixed)"
python3 verification/zm_mixed_check.py audit verification/logs/zm_mixed
[ "${1:-}" = "--fast" ] && exit 0

echo "== 2b. zmx2, full (unreduced) sweep  (~30 min single thread)"
$Z cert "$CERT" --full --log build/zmx2_full.log | grep -E "^(VERIFIED|NOT VERIFIED|INCOMPLETE)|total"

echo "== 3. zm_mixed.py, complete two-stage run  (~140 CPU-hours; resumable: re-run this script to continue)"
python3 verification/zm_mixed_check.py run
