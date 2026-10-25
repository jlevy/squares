#!/usr/bin/env bash
# Custody of the files the 25 October 2026 review of issue 806 read. Decides nothing.
#
#   programs/custody.sh CLONE > out/custody.txt
#
# CLONE is a clone of evand/square-packing holding d99925d. The script prints the
# commit's metadata and message, the blob id, size and SHA-256 of each file the review
# read at that commit (from Git's object store; nothing in the clone is executed). The
# push time (04:16:05Z, 3c335fe..d99925d) is the stage 1 triage's reading of GitHub's
# activity log; this session had no API access to the repository to read it again.
set -euo pipefail

CLONE=$1
PIN=d99925d1298262c4ddb81c95abbb6f45adca8d3d
cd "$CLONE"
echo "== commit $PIN"
git log -1 --format='author %an <%ae>%nauthored %aI%ncommitted %cI%nparents %P' "$PIN"
echo "-- message"
git log -1 --format=%B "$PIN"
echo "== blobs at $PIN (path, blob, bytes, sha256)"
for f in search/packer/candidates/s182-1024.cert search/packer/candidates/s182-1024_regularized.cert \
  search/packer/candidates/s182-1024.exact.txt search/packer/candidates/s182-1024.input.txt \
  search/packer/candidates/s182-1024.json search/packer/candidates/s182-1024_prior.json \
  search/packer/candidates/s182-1024_vs_prior.json search/packer/candidates/s182-1024_regularized.json \
  CREDITS.md; do
  blob=$(git rev-parse "$PIN:$f")
  size=$(git cat-file -s "$blob")
  sum=$(git cat-file blob "$blob" | sha256sum | cut -d' ' -f1)
  echo "$f $blob $size $sum"
done
