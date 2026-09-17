---
type: is
id: is-01m2psbsfbsn9s7tm0nm3eggab
title: Bring the Packing pull-request wall under 180 s and re-enforce it
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels:
  - ci
  - focus-efficiency
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-17T04:17:57.226Z
updated_at: 2026-09-17T04:17:57.226Z
---
Owner decision 2026-09-17: PR #188 makes the pull-request wall check advisory because five hosted runs measured 194, 189, 178, 166 and 216 s (runs 35127260063, 35128357992, 35175474610, 35176748398 attempts 1 and 2) against OR-14's 180 s, with hosted runner speed varying about 1.6-1.8x on identical code and an occasional slow full-history fetch (45 s). Balanced two-shard suites still give about 177 s on a 1.5x runner and 185-210 s at 1.8x or with a slow fetch, and the frontend job alone runs 158-180 s end to end (setup 48-58 s: checkout 15-18, Node 6-12, Chromium apt fonts 13-19; tier: Chromium 73-82 s serialized behind liveness 12-22 s at --jobs 2). Candidate work, measured in attic/wall at 21642ed8: a third suite shard (SUITE_SHARDS=3, --suite-c, register suite_c, workflow job and packing-required need, suite_files support for re-dividing or whole-lane reports; predicted ~91 s end to end on a fast runner, ~145 s wall at 1.8x); frontend restructuring (start Chromium first or three slots, cache or drop apt fonts after checking page contracts, cache Node, split the Chromium step across jobs). Done when a declared number of consecutive exact-head hosted runs keep both walls at or below 180 s and the wall check is switched back to enforcing.
