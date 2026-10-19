#!/usr/bin/env bash
# The programs this review wrote, run in order through run_serial.sh after the
# maintained replays: the third route, the dilation check and the lineage measurement.
# Run from packing/; OUT is the outputs directory, CUSTODY the directory custody.py wrote.
set -u
here="$(cd "$(dirname "$0")" && pwd)"
out="${1:?usage: chain_review.sh OUT CUSTODY}"
custody="${2:?usage: chain_review.sh OUT CUSTODY}"
export TMPDIR="${TMPDIR:-/dev/shm}"
uvpy=(uv run --frozen --all-extras --group dev python -I)
"$here/run_serial.sh" "$out/replay/third-route.log" -- "${uvpy[@]}" "$here/third_route_1019.py" \
  --json "$out/third-route-2026-10-19.json" --upstream "$custody"
"$here/run_serial.sh" "$out/replay/dilation.log" -- "${uvpy[@]}" "$here/dilation_1019.py" \
  --json "$out/dilation-2026-10-19.json"
"$here/run_serial.sh" "$out/replay/lineage.log" -- "${uvpy[@]}" "$here/lineage_1019.py" \
  --json "$out/lineage-2026-10-19.json"
