---
type: is
id: is-01m1t71bsncn7adg02er2hyk6d
title: Run local research and documentation validation
kind: task
status: in_progress
priority: 1
version: 3
labels:
  - validation
dependencies:
  - type: blocks
    target: is-01m1t71c4hyfw28d5nc5m6jv6b
parent_id: is-01m1t5yjssbd51cnnw2zwkqah6
created_at: 2026-09-06T01:58:57.076Z
updated_at: 2026-09-06T03:07:12.836Z
---
After document, value, and upstream edits settle, run Flowmark only on maintained prose, documentation and schema checks, packing-validate --edit and --push, targeted exact replays, and an independent combined-diff review.

## Notes

At merge commit 3fecaf23: Flowmark --check passed; packing-validate --edit passed 43/64 named steps in 28.87s with ruff/basedpyright/records/exact/generated views clean. First push-tier run completed the reachable suite in 970.19s and failed only five managed-sandbox permission checks (three loopback binds, two ps process checks); the exact push tier is now being rerun outside the sandbox rather than skipped or weakened.
