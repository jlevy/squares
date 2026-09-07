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

(
  cd "$ROOT"
  sha256sum -c archive.sha256
)
xz -dc "$ARCHIVE" > "$TMP/square17_lb_4p468292.cert"
printf '%s  %s\n' \
  2838f315302d67da131745925e9ec7dd2a602bb299d1335ce25e4e13a7b7b6d2 \
  "$TMP/square17_lb_4p468292.cert" | sha256sum -c -

"$CXX" -O3 -std=c++17 "$ROOT/verify_certificate.cpp" -o "$TMP/verify_fast"
"$CXX" -O3 -std=c++17 "$ROOT/verify_certificate_bigint.cpp" -o "$TMP/verify_bigint"

"$TMP/verify_fast" "$TMP/square17_lb_4p468292.cert"
"$TMP/verify_bigint" "$TMP/square17_lb_4p468292.cert"
python3 "$ROOT/verify_certificate.py" "$TMP/square17_lb_4p468292.cert"
bash "$ROOT/tests/rejection_tests.sh" "$TMP/verify_fast"

echo ARCHIVED_CERTIFICATE_VERIFIED_4P468292
