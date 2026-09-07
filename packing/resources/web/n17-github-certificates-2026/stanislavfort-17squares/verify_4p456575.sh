#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

DIR="$ROOT/certificates/lower_bound_4p456575"
CERT="$DIR/square17_lb_4p456575.cert"
GENERATED="$TMP/generated.cert"
EXPECTED_SHA=5fbee90dc6fedc1851e4b8b9866f8ffa41c38cb09ebb6a9f748096217f078550
CXX="${CXX:-g++}"

"$CXX" -O3 -std=c++17 "$DIR/generate_certificate.cpp" -o "$TMP/generate"
"$CXX" -O3 -std=c++17 "$DIR/verify_certificate.cpp" -o "$TMP/verify_fast"
"$CXX" -O3 -std=c++17 "$DIR/verify_certificate_bigint.cpp" -o "$TMP/verify_bigint"

"$TMP/generate" "$GENERATED"
printf '%s  %s\n' "$EXPECTED_SHA" "$GENERATED" | sha256sum -c -
printf '%s  %s\n' "$EXPECTED_SHA" "$CERT" | sha256sum -c -
cmp "$GENERATED" "$CERT"
"$TMP/verify_fast" "$GENERATED"
"$TMP/verify_bigint" "$GENERATED"
python3 "$DIR/verify_certificate.py" "$GENERATED"

echo ALL_EXACT_CHECKS_PASSED_4P456575
