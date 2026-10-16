#!/usr/bin/env bash
# Run every review program on PR #622's certificate and compare with the kept outputs.
#
# Usage: run_review.sh WORK ASSETS
#   WORK    a directory outside the checkout; outputs go to WORK/outputs
#   ASSETS  a directory holding pingyou-n29-certificate-2026-10-15.zip, the release asset
#           (n29_exact_review.py refuses any other bytes)
#
# The interpreter is the project's, through uv, run isolated (-I); set PYTHON to a
# Python 3.14 to use another. Nothing is fetched, extracted or written outside WORK.
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "usage: $0 WORK ASSETS" >&2
  exit 2
fi
work=$(cd "$1" && pwd)
assets=$(cd "$2" && pwd)
here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
review=$(dirname "$here")
packet=$(dirname "$review")
repo=$(cd "$packet/../../../.." && pwd)
asset="$assets/pingyou-n29-certificate-2026-10-15.zip"
prog="$here/n29_exact_review.py"

if [[ -n "${PYTHON:-}" ]]; then
  run=("$PYTHON" -I)
else
  run=(uv run --frozen --all-extras --group dev --project "$repo/packing" python -I)
fi

mkdir -p "$work/outputs"
out="$work/outputs"
nice -n 10 "${run[@]}" "$prog" certificate "$asset" >"$out/certificate.json"
nice -n 10 "${run[@]}" "$prog" controls "$asset" >"$out/controls.json"
nice -n 10 "${run[@]}" "$prog" fact "$asset" "$packet/facts/n-029.yaml.gz" >"$out/fact.json"
nice -n 10 "${run[@]}" "$prog" native "$asset" >"$out/native.json"
nice -n 10 "${run[@]}" "$prog" sides "$asset" "$repo" >"$out/sides.json"
for b in pr574-v2 pr549 evan; do
  nice -n 10 "${run[@]}" "$prog" certificate "$asset" \
    --member "n29-certificate/baselines/$b-n029.cert.json" >"$out/baseline-$b.json"
done

# Each output against the kept one, field for field, apart from CPU times.
"${run[@]}" - "$review/outputs" "$out" <<'PY'
import json
import sys
from pathlib import Path

kept, fresh = Path(sys.argv[1]), Path(sys.argv[2])


def strip(value):
    if isinstance(value, dict):
        return {k: strip(v) for k, v in value.items() if k != "cpu_s"}
    if isinstance(value, list):
        return [strip(v) for v in value]
    return value


names = sorted(p.name for p in kept.glob("*.json"))
bad = [n for n in names if strip(json.loads((kept / n).read_text()))
       != strip(json.loads((fresh / n).read_text()))]
for n in names:
    print(("DIFFERS " if n in bad else "same    ") + n)
sys.exit(1 if bad else 0)
PY
