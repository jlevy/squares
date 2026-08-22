#!/usr/bin/env bash
# Run everything and check the results that matter.
set -euo pipefail
cd "$(dirname "$0")"

echo "== exact verification =="
out=$(python3 verify_trump11.py)
echo "$out"
grep -q "^VALID: 11 squares, 55 pairs tested" <<<"$out"
grep -q "14 separated with zero gap, 41 strictly" <<<"$out"
grep -q "20 corner coordinates exactly on the boundary" <<<"$out"
grep -q "P(s) == 0 for the published degree-8 polynomial: True" <<<"$out"
grep -q "s = 3.87708359002281417730789706010096" <<<"$out"

echo
echo "== negative control =="
out=$(python3 negative_control.py)
echo "$out"
# every perturbation must be rejected by the exact verifier
grep -q "delta = 1e-100  REJECT" <<<"$out"
! grep -qE "delta = 1e-[0-9]+ +accept" <<<"$out"
# and float64 with a tolerance must have a blind spot
grep -q "tol=1e-09 .*1e-12: accept" <<<"$out"

echo
echo "== derivation (needs sympy) =="
if python3 -c "import sympy" 2>/dev/null; then
  out=$(python3 derive_field.py)
  echo "$out"
  grep -q "matches sqpack.packings.trump11.U_MIN_POLY: True" <<<"$out"
else
  echo "sympy not installed, skipping"
fi

echo
echo "ALL CHECKS PASSED"
