#!/usr/bin/env bash
# Push times of the two publications, from GitHub's repository activity API (read only).
# Decides nothing; it checks the report order the ledger and the register state.
set -euo pipefail
for repo in franciscouzo/square-packing evand/square-packing; do
  echo "== $repo"
  gh api "repos/$repo/activity?per_page=40" \
    --jq '.[] | select(.timestamp >= "2026-10-23") | [.timestamp, .activity_type, .ref, .before, .after] | @tsv'
done
