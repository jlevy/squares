---
type: is
id: is-01m4xjgkd0pyssg3rk8baav409
title: "#514 review B3: the landed check read origin/main through git show (OR-18) and failed only after a merge"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-10-14T16:04:19.488Z
updated_at: 2026-10-14T16:05:22.711Z
closed_at: 2026-10-14T16:05:22.711Z
close_reason: "fixed in 662da8162, a8f86a60d: results.schema.yaml requires landed; the lane generators write it with each entry; the Git-reading test and --check are removed, test_every_entry_carries_the_day_it_landed reads the tree alone; --backfill kept and a non-gating --audit added; result-import.md Stage 3, Stage 5 Before merge and the intake pass, and documentation-pass.md's New Result Publication, say so"
resolution: null
duplicate_of: null
---
Review B of #514 (review 5520287797), finding B3: the landed check read origin/main through git show (OR-18) and failed only after a merge
