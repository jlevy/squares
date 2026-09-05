---
type: is
id: is-01m1sbn9h3anz6vse7as2a1qrw
title: The exhaustive exact tier overran its 1800s budget on CI (1801.02s)
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T18:00:29.987Z
updated_at: 2026-09-05T21:25:13.894Z
closed_at: 2026-09-05T21:25:13.894Z
close_reason: "The exhaustive exact tier has its own workflow job, its own runner and its own verdict, selected with --only while every other job leaves it out with --skip (a new flag: --only cannot express everything-but-one). test_the_post_merge_jobs_partition_the_gate resolves both post-merge commands through the CLI's own selector and requires a disjoint cover of every declared step."
resolution: null
duplicate_of: null
---
The 'exhaustive exact behavioral tests' step measured 1801.02s against EXHAUSTIVE_SUITE_BUDGET_SECONDS = 1800.0 in packing/src/sqpack/cli/validate.py and failed the gate on main at f060b1d7, 1d541077 and 85d1c976. The constant's recorded rationale measures 892s on CI's two-core runner at 39 tests, set at twice the measurement. Needs a fresh measurement and either a justified budget or a faster tier.
