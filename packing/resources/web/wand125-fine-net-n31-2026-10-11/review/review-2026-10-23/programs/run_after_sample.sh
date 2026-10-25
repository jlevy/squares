#!/usr/bin/env bash
# The runs of review-2026-10-23 that follow the sample, one process at a time:
# the mutants (controls), the sharp control at the sample's least capture found, the
# source's logged poses, the cell-bound self-test and the summary.
# Usage: bash run_after_sample.sh PY PACKET_RELEASE_DIR  (from the review directory)
set -euo pipefail
PY=$1
REL=$2
C=$REL/candidate.json.gz
LOG=$REL/check2/run.jsonl.gz
CTL=$REL/check2/control-197_200.jsonl.gz
OUT=outputs
t() { { time nice -n 19 "$@"; } 2>&1; }

# 1. Every mass scaled by 99/100, at five directions: each must be REFUTED.
t "$PY" -I programs/capture.py "$C" "$OUT" 0 1 676 1036 2072 \
  --mass-scale 99/100 --tag scaled-99-100 --cpu-limit 600 | tee "$OUT/controls.stdout.txt"
# 2. The heaviest listed row (row 33, mass 1.3749) and its seven images removed.
t "$PY" -I programs/capture.py "$C" "$OUT" 1 1036 2072 \
  --drop-row 33 --tag drop-row-33 --cpu-limit 600 | tee -a "$OUT/controls.stdout.txt"
# 3. The sharp control: at the sample direction whose least capture found is least,
#    every mass scaled so that the capture at that pose is at most 1 - 1/10000.
read -r J SCALE < <("$PY" -I - "$OUT" <<'PYEOF'
import json, sys
from fractions import Fraction
from pathlib import Path
best = None
for f in Path(sys.argv[1]).glob("capture-original-*.json"):
    d = json.loads(f.read_text())
    v = d.get("least_capture_found_float")
    if v is not None and (best is None or v < best[0]):
        best = (v, d["j"])
v, j = best
# A rational at most (1 - 1/10000)/v, with v rounded up, so the mutant's capture at the
# pose is at most 1 - 1/10000 whatever the float's last digit.
up = Fraction(v).limit_denominator(10**12) + Fraction(1, 10**12)
s = Fraction(9999, 10000) / up
s = Fraction(int(s * 10**12), 10**12)
print(j, f"{s.numerator}/{s.denominator}")
PYEOF
)
echo "sharp control at direction $J, scale $SCALE" | tee -a "$OUT/controls.stdout.txt"
t "$PY" -I programs/capture.py "$C" "$OUT" "$J" \
  --mass-scale "$SCALE" --tag sharp --cpu-limit 900 | tee -a "$OUT/controls.stdout.txt"
# 4. The source's logged poses.
t "$PY" -I programs/source_log_points.py "$C" "$LOG" "$CTL" 12 \
  "$OUT/source-log-points.json" | tee "$OUT/source-log-points.stdout.txt"
# 5. The cell bound against the second method.
t "$PY" -I programs/bound_selftest.py "$C" "$OUT/bound-selftest.json" 6 \
  | tee "$OUT/bound-selftest.stdout.txt"
# 6. The summary.
"$PY" -I programs/summarize.py "$OUT" "$LOG" "$OUT/sample-plan.json" "$OUT/summary.json" \
  | tee "$OUT/summary.stdout.txt"
sha256sum programs/* > "$OUT/program-digests.sha256"
