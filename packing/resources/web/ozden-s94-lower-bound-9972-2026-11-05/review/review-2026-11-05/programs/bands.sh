#!/usr/bin/env bash
# The strips the dilation adds at shared nodes: centres within lambda*m0(t) - m(t) of a
# wall edge, where Hosono's own domain (margin m0(t) in his coordinates) stopped.
# Each strip of the quadrant [L/2, U_r]^2 (top and right) is decided with bnb.py --region;
# the region bounds are written by bands_regions.py.
set -uo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cert="$1"; out="$2"; regions="$3"
while read -r r name region; do
  timeout 1750 "$here/run.sh" bnb.py "$cert" "$r" "$out/band-r$r-$name.json" --region "$region" > "$out/band-r$r-$name.log" 2>&1
  echo "r=$r $name exit=$? $(grep -E '^(status|nodes|least_certified_bound|lowest_centre_estimate|lowest_centre_estimate_at|cpu_seconds):' "$out/band-r$r-$name.log" | tr '\n' ' ')"
done < "$regions"
