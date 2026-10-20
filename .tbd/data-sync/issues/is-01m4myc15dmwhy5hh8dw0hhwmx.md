---
type: is
id: is-01m4myc15dmwhy5hh8dw0hhwmx
title: "PR #406 A1: aggregate ceiling charges edit churn per historical version; refuses 12 of 37 routine merges"
kind: bug
status: closed
priority: 0
version: 3
delegate: claude-code@spud10
labels: []
dependencies: []
parent_id: is-01m4mybh5kcffr8zqzm2ajg86e
hold: null
hold_until: null
created_at: 2026-10-11T07:38:22.725Z
updated_at: 2026-10-11T18:58:26.858Z
started_at: 2026-10-11T07:39:06.143Z
closed_at: 2026-10-11T18:58:26.857Z
close_reason: "fixed in 0a4a69d5e: per-path largest-version total, merge-base tip diff, --census; total 48 MiB from the census (12 of 38 merges rejected before, 1 after: #461). Disposition: https://github.com/jlevy/squares/pull/406#issuecomment-6112530517"
resolution: null
duplicate_of: null
---
Blocker. packing/devtools/check_added_blobs.py:149-173,216-231 sums every historical blob version in base..head against MAX_TOTAL_BYTES. Fix: aggregate once per path at its largest version, per-blob ceiling over all history, census mode in the tool, measured refusal rate in the PR body; #435 and the 9 aggregate-only refusals must pass. Review A: https://github.com/jlevy/squares/pull/406#pullrequestreview-5482287656 (PR #406).
