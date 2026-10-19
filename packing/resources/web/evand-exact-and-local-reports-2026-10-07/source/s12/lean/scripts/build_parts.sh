#!/usr/bin/env bash
# Build the part files of a generated data set a few at a time, then the top module.
# `lake build` starts every ready module at once (one per hardware thread; it ignores `taskset`),
# and each S32Z part file peaks at ~14 GB, so a plain `lake build Sqpack.S32Lower` would start
# ~30 of them together.  This builds them JOBS at a time instead.
#   usage: lean/scripts/build_parts.sh NAME TOP [JOBS=4] [CPUS]
#   e.g.   lean/scripts/build_parts.sh S32Z Sqpack.S32Lower 4 12-15
set -euo pipefail
cd "$(dirname "$0")/.."             # the lean/ directory
name=$1; top=$2; jobs=${3:-4}; cpus=${4:-}
pin=${cpus:+taskset -c $cpus}
$pin lake build "Sqpack.$name.Pts"
ls "Sqpack/$name"/Part*.lean | sed 's#\.lean$##; s#/#.#g' | xargs -P "$jobs" -I{} $pin lake build {}
$pin lake build "$top"
