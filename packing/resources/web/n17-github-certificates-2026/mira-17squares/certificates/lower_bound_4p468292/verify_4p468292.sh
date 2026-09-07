#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
CXX=${CXX:-g++}
ARCHIVE="$ROOT/square17_lb_4p468292.cert.xz"
if [[ ! -f "$ARCHIVE" ]]; then
  echo "missing certificate archive: $ARCHIVE" >&2
  exit 2
fi
RAW="$TMP/generated.cert"
ARCHIVED="$TMP/archived.cert"

"$CXX" -O3 -std=c++17 "$ROOT/generate_certificate.cpp" -o "$TMP/generate"
"$CXX" -O3 -std=c++17 "$ROOT/verify_certificate.cpp" -o "$TMP/verify_fast"
"$CXX" -O3 -std=c++17 "$ROOT/verify_certificate_bigint.cpp" -o "$TMP/verify_bigint"

"$TMP/generate" "$RAW"
printf '%s  %s\n' \
  2838f315302d67da131745925e9ec7dd2a602bb299d1335ce25e4e13a7b7b6d2 \
  "$RAW" | sha256sum -c -
xz -dc "$ARCHIVE" > "$ARCHIVED"
cmp "$RAW" "$ARCHIVED"

"$TMP/verify_fast" "$RAW"
"$TMP/verify_bigint" "$RAW"
python3 "$ROOT/verify_certificate.py" "$RAW"
bash "$ROOT/tests/rejection_tests.sh" "$TMP/verify_fast"

echo ALL_EXACT_CHECKS_PASSED_4P468292
