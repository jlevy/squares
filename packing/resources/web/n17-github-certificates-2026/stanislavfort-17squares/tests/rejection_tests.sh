#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIR="$ROOT/certificates/lower_bound_4p456575"
CERT="$DIR/square17_lb_4p456575.cert"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
CXX="${CXX:-g++}"

"$CXX" -O3 -std=c++17 "$DIR/verify_certificate.cpp" -o "$TMP/verify"

expect_reject() {
    local file="$1"
    local name="$2"
    if "$TMP/verify" "$file" >/dev/null 2>&1; then
        echo "FAIL: malformed certificate accepted: $name" >&2
        exit 1
    fi
    echo "PASS_REJECT: $name"
}

# Truncation.
head -c -1 "$CERT" > "$TMP/truncated.cert"
expect_reject "$TMP/truncated.cert" truncated

# Trailing data.
cp "$CERT" "$TMP/trailing.cert"
printf '\000' >> "$TMP/trailing.cert"
expect_reject "$TMP/trailing.cert" trailing_byte

# Invalid root opcode.
cp "$CERT" "$TMP/bad_opcode.cert"
printf '\377' | dd of="$TMP/bad_opcode.cert" bs=1 seek=0 count=1 conv=notrunc status=none
expect_reject "$TMP/bad_opcode.cert" invalid_root_opcode

echo MALFORMED_CERTIFICATE_TESTS_PASSED
