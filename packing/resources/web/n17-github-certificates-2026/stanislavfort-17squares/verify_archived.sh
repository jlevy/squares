#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
DIR="$ROOT/certificates/lower_bound_4p456575"
CERT="$DIR/square17_lb_4p456575.cert"
EXPECTED_SHA=5fbee90dc6fedc1851e4b8b9866f8ffa41c38cb09ebb6a9f748096217f078550
CXX="${CXX:-g++}"

printf '%s  %s\n' "$EXPECTED_SHA" "$CERT" | sha256sum -c -
"$CXX" -O3 -std=c++17 "$DIR/verify_certificate.cpp" -o "$TMP/verify_fast"
"$CXX" -O3 -std=c++17 "$DIR/verify_certificate_bigint.cpp" -o "$TMP/verify_bigint"

"$TMP/verify_fast" "$CERT"
"$TMP/verify_bigint" "$CERT"
python3 "$DIR/verify_certificate.py" "$CERT"

echo ARCHIVED_CERTIFICATE_VERIFIED_4P456575
