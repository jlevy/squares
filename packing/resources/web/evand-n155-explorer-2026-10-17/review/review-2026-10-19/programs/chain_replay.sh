#!/usr/bin/env bash
# The maintained commands this review ran, in order, each through run_serial.sh:
# for each of the five packets, the custody check, check-claims, the structural check and
# the full replay. Run from packing/; OUT is the log directory.
set -u
here="$(cd "$(dirname "$0")" && pwd)"
out="${1:?usage: chain_replay.sh OUT}"
export TMPDIR="${TMPDIR:-/dev/shm}"
uvpy=(uv run --frozen --all-extras --group dev python)
packets=(
  evand-n155-explorer-2026-10-17
  evand-n229-dilation-2026-10-17
  evand-n229-dilation-update-2026-10-18
  evand-n236-2026-10-16
  evand-n271-2026-10-17
)
for p in "${packets[@]}"; do
  "$here/run_serial.sh" "$out/$p.acquire-check.log" -- "${uvpy[@]}" -m devtools.acquire_source "$p" --check
  "$here/run_serial.sh" "$out/$p.check-claims.log" -- "${uvpy[@]}" -m devtools.upper_bound_reports "$p" check-claims
  "$here/run_serial.sh" "$out/$p.check.log" -- "${uvpy[@]}" -m devtools.upper_bound_reports "$p" check
done
for p in "${packets[@]}"; do
  "$here/run_serial.sh" "$out/$p.replay.log" -- "${uvpy[@]}" -m devtools.upper_bound_reports "$p" check --replay
done
