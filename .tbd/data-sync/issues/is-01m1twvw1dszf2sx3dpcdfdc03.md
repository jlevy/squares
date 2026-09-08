---
type: is
id: is-01m1twvw1dszf2sx3dpcdfdc03
title: "PR #93 validation V2: make deadline convergence regression deterministic"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1tve7ex9akeg5842fnbfesr
created_at: 2026-09-06T08:20:25.772Z
updated_at: 2026-09-06T08:21:20.064Z
closed_at: 2026-09-06T08:21:20.063Z
close_reason: Duplicate of closed think-say5; reuse its focused deterministic test fix from PR94 commit 9c82dc2a in PR93 instead of independent repair.
resolution: null
duplicate_of: null
---
Broad pre-push at c610d308: test_a_clock_stop_between_column_rounds_keeps_the_converged_optimum assumes nonempty rounds implies converged. A short deadline can stop first row loop before convergence. Replace timing-sensitive setup with deterministic boundary control and preserve optimum/freeze assertions.
