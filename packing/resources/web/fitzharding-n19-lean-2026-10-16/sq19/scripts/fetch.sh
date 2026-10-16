#!/usr/bin/env bash
# Download the generated certificate sources (release assets), check every
# archive and every extracted file against expected/generated-sources.sha256.
#   bash scripts/fetch.sh [ARCHIVE_DIR]
# With ARCHIVE_DIR containing the assets already, nothing is downloaded.
set -euo pipefail
cd "$(dirname "$0")/.."
REPO=${SQ19_REPO:-ofitzharding/sq19}
TAG=${SQ19_TAG:-v1.0.0}
DL=${1:-.downloads}; mkdir -p "$DL"
sha() { if command -v sha256sum >/dev/null; then sha256sum "$@"; else shasum -a 256 "$@"; fi; }
get() {
  [ -f "$DL/$1" ] && return
  curl -fL --retry 3 -o "$DL/$1" "https://github.com/$REPO/releases/download/$TAG/$1"
}
get SHA256SUMS
for f in $(awk '{print $2}' "$DL/SHA256SUMS"); do get "$f"; done
(cd "$DL" && sha -c SHA256SUMS)
for f in "$DL"/sq19-generated-*.tar.xz; do xz -dc "$f" | tar -xf -; done
sha -c --status expected/generated-sources.sha256 || { echo "FETCH FAILED: hash mismatch"; exit 1; }
echo "FETCH_OK $(wc -l < expected/generated-sources.sha256) generated files verified"
