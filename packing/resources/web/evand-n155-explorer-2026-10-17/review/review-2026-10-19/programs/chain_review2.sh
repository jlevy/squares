#!/usr/bin/env bash
# The second batch, written after the first had started: the registered area route on
# the five certificates, and this review's route on the source's three regularized
# views. Run from packing/; OUT is the outputs directory.
set -u
here="$(cd "$(dirname "$0")" && pwd)"
out="${1:?usage: chain_review2.sh OUT}"
export TMPDIR="${TMPDIR:-/dev/shm}"
uvpy=(uv run --frozen --all-extras --group dev python -I)
"$here/run_serial.sh" "$out/replay/area-route.log" -- "${uvpy[@]}" "$here/area_route_1019.py" \
  --json "$out/area-route-2026-10-19.json"
"$here/run_serial.sh" "$out/replay/views.log" -- "${uvpy[@]}" "$here/views_1019.py" \
  --json "$out/views-2026-10-19.json"
