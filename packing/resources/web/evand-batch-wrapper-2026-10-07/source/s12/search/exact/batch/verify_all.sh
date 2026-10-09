#!/usr/bin/env bash
# Check every certificate with both independent exact verifiers (stdlib Python, exact rationals).  ~2 min, 1 core.
#   ./verify_all.sh            -> exit 0 iff all certificates pass both
set -u
cd "$(dirname "$0")"
fail=0; k=0
for c in certs/n-*.cert; do
  k=$((k + 1))
  python3 ../verify_cert.py "$c" | tail -1 | grep -q '^  VALID:' || { echo "verify_cert FAIL $c"; fail=1; }
  python3 ../verify_cert2.py "$c" > /dev/null || { echo "verify_cert2 FAIL $c"; fail=1; }
done
[ $fail = 0 ] && echo "all $k certificates VALID under both verifiers" || echo "FAILURES above"
exit $fail
