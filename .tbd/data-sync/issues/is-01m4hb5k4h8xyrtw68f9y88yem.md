---
type: is
id: is-01m4hb5k4h8xyrtw68f9y88yem
title: Fold tier-wall window sampling and shard growth reports into the maintained tools (OR-1)
kind: task
status: open
priority: 3
version: 1
labels:
  - ci
dependencies: []
created_at: 2026-10-09T22:05:05.553Z
updated_at: 2026-10-09T22:05:05.553Z
---
PR #480 scripted in scratch: (1) sampling every Packing validation attempt's suite jobs over a time window with median/quantiles; (2) per-shard growth between two suite-file-costs records with top-growing files. Give devtools.read_tier_walls a --since window over all attempts, and devtools.suite_files a growth report between two partition records. Related: think-2hm6, think-be1s.
