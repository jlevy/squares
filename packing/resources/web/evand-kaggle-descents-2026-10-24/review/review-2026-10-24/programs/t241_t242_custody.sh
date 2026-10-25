#!/usr/bin/env bash
# Custody check of the stage 4 review of T-241 and T-242 (think-vm3m). Decides nothing
# about any bound: it compares the Git blob id of each file the review reads from a
# packet with the blob the source's tree holds at the pinned commits. It reads trees
# and commits only, which a blobless clone holds, so it fetches nothing.
#
# Usage, from packing/:  bash PATH/TO/t241_t242_custody.sh EVAND_CLONE COUZO_CLONE
set -euo pipefail
evand=$1
couzo=$2
web=resources/web
row() {  # clone commit path retained-file
  local tree blob
  tree=$(git -C "$1" ls-tree "$2" -- "$3" | awk '{print $3}')
  blob=$(git hash-object "$4")
  printf '%s %-9s %-60s source=%s retained=%s %s\n' "$(basename "$1")" "${2:0:9}" "$3" "${tree:-absent}" "$blob" \
    "$([ "$tree" = "$blob" ] && echo SAME || echo DIFFERENT)"
}
cand=search/packer/candidates
for f in s268_lightning.cert s304_pub.cert s268_lightning.input.txt s268_lightning.predescent.txt s304_pub.input.txt s268_lightning_regularized.cert; do
  row "$evand" 8a8879a2972c32cbd2d906049228cc9f0762b02a "$cand/$f" "$web/evand-kaggle-descents-2026-10-24/source/$cand/$f"
done
row "$evand" 8a8879a2972c32cbd2d906049228cc9f0762b02a CREDITS.md "$web/evand-kaggle-descents-2026-10-24/source/CREDITS.md"
for commit in fa6237e288cf3fc53b53fc43438c91f3f59c40e9 964ee2b 1c17153; do
  row "$couzo" "$commit" certificates/best/n304.cert "$web/couzo-issue763-2026-10-23/source/certificates/best/n304.cert"
done
row "$couzo" 964ee2b certificates/best/n268.cert "$web/couzo-issue763-2026-10-23/source/certificates/best/n268.cert"
for p in 85dbd707746197d31f62dd52b4e580dfb90097498a4970c577f776ce7de2df46 22f07a7c318328d257d1a7efd9c5acb05e3286650a94da751592b21014424244; do
  row "$couzo" 964ee2b "certificates/parents/$p.cert" "$web/couzo-issue763-2026-10-23/source/certificates/parents/$p.cert"
done
# The first commit on the source's history that holds the retained n304.cert bytes.
want=$(git hash-object "$web/couzo-issue763-2026-10-23/source/certificates/best/n304.cert")
for c in $(git -C "$couzo" rev-list --reverse 964ee2b -- certificates/best/n304.cert); do
  b=$(git -C "$couzo" ls-tree "$c" -- certificates/best/n304.cert | awk '{print $3}')
  printf 'n304.cert history: %s %s %s\n' "${c:0:9}" "${b:-absent}" "$([ "$b" = "$want" ] && echo RETAINED-BYTES || echo other)"
done
# Manifest blob at the two commits the credit chain reads.
for commit in fa6237e288cf3fc53b53fc43438c91f3f59c40e9 964ee2b; do
  printf 'manifest %s %s\n' "${commit:0:9}" "$(git -C "$couzo" ls-tree "$commit" -- certificates/best/manifest.json | awk '{print $3}')"
done
