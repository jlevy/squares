#!/usr/bin/env bash
# Decide a list of directions one after another with bnb.py; one receipt per direction.
# Usage: sample.sh CERT_GZ OUT_DIR R [R ...]
set -uo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cert="$1"; out="$2"; shift 2
for r in "$@"; do
  timeout 1750 "$here/run.sh" bnb.py "$cert" "$r" "$out/bnb-r$r.json" --log-every 60 > "$out/bnb-r$r.log" 2>&1
  echo "r=$r exit=$? $(grep -E '^(status|nodes|least_certified_bound|lowest_centre_estimate|cpu_seconds):' "$out/bnb-r$r.log" | tr '\n' ' ')"
done
