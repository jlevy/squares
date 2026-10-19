#!/bin/bash
# Custody of the evand-exact-cur-2026-10-16 packet, as this review checked it: a blobless
# clone of evand/square-packing at the pin into DIR (an empty scratch directory outside
# the repository), the pinned tree, every manifest line's SHA-256 at the pin, and every
# retained file byte for byte against its upstream blob. Prints what it found.
# Usage, from the repository root: custody.sh DIR
set -euo pipefail
DIR=$1
PIN=7d1407a0b66c46e32cdbcbd5619586fe2bdd52a1
PACKET=$PWD/packing/resources/web/evand-exact-cur-2026-10-16
git clone -q --filter=blob:none --no-checkout https://github.com/evand/square-packing.git "$DIR/sq"
cd "$DIR/sq"
echo "commit $(git rev-parse "$PIN^{commit}") tree $(git rev-parse "$PIN^{tree}")"
grep -o '"git_tree": *"[0-9a-f]*"' "$PACKET/acquisition/sources.json"
paths=$(awk '{print substr($2, 3)}' "$PACKET/acquisition/upstream-subtree.sha256")
# shellcheck disable=SC2086
git checkout -q "$PIN" -- $paths
sha256sum -c --quiet "$PACKET/acquisition/upstream-subtree.sha256" && echo "manifest: $(wc -l < "$PACKET/acquisition/upstream-subtree.sha256") lines match at the pin"
n=0; bad=0
while IFS= read -r f; do
  n=$((n + 1))
  cmp -s "$PACKET/source/$f" "$f" || { echo "differs: $f"; bad=$((bad + 1)); }
done < <(cd "$PACKET/source" && find . -type f | sort)
echo "retained files compared: $n, differing: $bad"
cmp "search/exact/verify_exact.py" "$PACKET/../evand-exact-and-local-reports-2026-10-12/source/search/exact/verify_exact.py" && echo "verify_exact.py at the pin is the retained copy"
