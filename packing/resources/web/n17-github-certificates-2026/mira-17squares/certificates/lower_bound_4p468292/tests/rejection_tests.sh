#!/usr/bin/env bash
set -euo pipefail

CHECKER=${1:?usage: rejection_tests.sh /path/to/fast-checker}
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

expect_reject() {
  local file=$1
  if "$CHECKER" "$file" >/dev/null 2>&1; then
    echo "unexpected acceptance: $file" >&2
    exit 1
  fi
}

: > "$TMP/empty.cert"
printf '\377' > "$TMP/unknown-opcode.cert"
printf '\001' > "$TMP/false-root-witness.cert"
printf '\021' > "$TMP/early-eof-after-split.cert"

expect_reject "$TMP/empty.cert"
expect_reject "$TMP/unknown-opcode.cert"
expect_reject "$TMP/false-root-witness.cert"
expect_reject "$TMP/early-eof-after-split.cert"

echo REJECTION_TESTS_PASSED_4P468292
