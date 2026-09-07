#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
CXX=${CXX:-g++}
ARCHIVE="$ROOT/square17_lb_4p468292.cert.xz"
if [[ ! -f "$ARCHIVE" ]]; then
  echo "missing certificate archive: $ARCHIVE" >&2
  exit 2
fi

"$CXX" -O3 -std=c++17 "$ROOT/generate_certificate.cpp" -o "$TMP/generate"
"$TMP/generate" "$TMP/generated.cert"
printf '%s  %s\n' \
  2838f315302d67da131745925e9ec7dd2a602bb299d1335ce25e4e13a7b7b6d2 \
  "$TMP/generated.cert" | sha256sum -c -
xz -dc "$ARCHIVE" > "$TMP/archived.cert"
cmp "$TMP/generated.cert" "$TMP/archived.cert"
echo CERTIFICATE_REPRODUCED_BYTE_FOR_BYTE_4P468292
