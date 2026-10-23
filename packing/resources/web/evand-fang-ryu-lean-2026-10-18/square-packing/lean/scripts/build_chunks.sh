#!/usr/bin/env bash
# Build a `lean_cert.py --split` module JOBS chunks at a time: Data, then C*.lean (+ Sorted.lean), then the top.
# A plain `lake build` starts every chunk at once (one per hardware thread); chunks of large certificates peak at
# several GB each (n = 651 with --cut: <= 8 GB), so that can exhaust memory.
#   usage: lean/scripts/build_chunks.sh MODULE [JOBS=8]      e.g. lean/scripts/build_chunks.sh Sqpack.Exact.Fang.N651 8
set -euo pipefail
cd "$(dirname "$0")/.."             # the lean/ directory
mod=$1; jobs=${2:-8}
dir=$(echo "$mod" | tr . /)
lake build "$mod.Data"
ls "$dir"/C*.lean "$dir"/Sorted.lean 2>/dev/null | sed 's#\.lean$##; s#/#.#g' | xargs -P "$jobs" -I{} lake build {}
lake build "$mod"
