#!/usr/bin/env bash
# Regenerate the Lean certificate data that is too big to commit (gitignored).
# Run from anywhere; then build the opt-in module, e.g. `lake build Sqpack.S11Lower`.
# S32Z (96 part files, ~14 GB each): `lean/scripts/build_parts.sh S32Z Sqpack.S32Lower 4`, not a
# plain `lake build` (which would start ~30 of them at once).  Likewise S12H (320 part files, up to
# ~31 GB each): `lean/scripts/build_parts.sh S12H Sqpack.S12HLower 1` (6.5 h on 2 cores).
# The generator is deterministic and untrusted: the kernel checks whatever it writes.
#   usage: lean/scripts/gen_data.sh [S11 S13 S32Z S12H ...]     (default: all)
set -euo pipefail
cd "$(dirname "$0")/../.."          # the s12/ directory
G="python3 lean/scripts/gen_boxtree.py"

gen() {
  case "$1" in
    S11) $G certificates/s11_lower_3.8143.txt --n 11 --look 0 --parts 24 --name S11 --outdir lean/Sqpack/S11 ;;  # ~4 min
    S13) python3 lean/scripts/gen_zmtree.py certificates/rung2/s13_closed_cover_4.txt --n 13 --name S13 --outdir lean/Sqpack/S13 --nproc 4 ;;  # ~2.5 min on 4 cores
    S32Z) python3 lean/scripts/gen_zmtree.py certificates/s32/s32_closed_cover_6.txt --n 32 --name S32Z --outdir lean/Sqpack/S32Z --nproc 4 --parts 96 ;;  # ~75 min on 4 cores
    S12H) $G certificates/s12_lower_3.9686.txt --n 12 --look 0 --parts 320 --balance digits --name S12H --outdir lean/Sqpack/S12H ;;  # ~40 min, one core
    *) echo "unknown data set: $1" >&2; exit 2 ;;
  esac
}

for d in ${@:-S11 S13 S32Z S12H}; do gen "$d"; done
