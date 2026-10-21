---
type: is
id: is-01m5am54cgqre33jvgjqb5my53
title: Deferred atlas rebuild (900 s) and slow lane (1800 s) run at their command deadlines on hosted runners
kind: bug
status: closed
priority: 2
version: 5
delegate: claude-deadline-fix-20261019
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-19T17:43:08.432Z
updated_at: 2026-10-20T00:08:40.753Z
started_at: 2026-10-19T20:59:02.402Z
closed_at: 2026-10-20T00:08:40.746Z
close_reason: "Fixed by PR #691 (merged b16ddeb0a): _margin_summary computes axes/projections once with a value-preserving early exit (Review A correctness proof + 10,379-case differential), atlas builder memoizes cases and the composite test builds only its poster. Hosted deferred at the merged code: atlas rebuild 269.6/420.2 s of 900 s, slow lane 915.2/570.4 s of 1800 s, full deferred checkpoint 39341838826 green. Regularized-views deadline risk moved to think-uomm."
resolution: null
duplicate_of: null
---
Deferred checkpoint job deferred-atlas-grid, step 'known-best n=1..324 atlas rebuild' (devtools.build_known_best_atlas --check, --jobs 1 --inner-jobs 2), 900 s command deadline. Main dispatch runs 2026-10-19: 619.76 s (39233374262), 620.25 s (39244113905), 611.56 s (39250299524), 875.91 s (39256144591), 692.64 s (39262635681). PR #685 dispatch 39292263543 (merge 3c516dd7) timed out at 901 s; #685 does not touch the atlas builder or its inputs (sqpack changes: release.py edition metadata, cli/validate.py site forwarder env). Under OR-17 the deadline is not to be raised blindly: profile the rebuild (where 600-900 s goes on a 4-CPU hosted runner), reduce or partition it, or re-select its ceiling on a recorded measurement. Not a flake root cause.

## Notes

2026-10-19 PR #691: fix (99c7fff6c margin summary, b5e20d90b memo) reviewed A (Fable correctness, accept) and B (senior, approve). Hosted: atlas rebuild 269.6/420.2 s of 900; slow lane 915.2/570.4 s of 1800; deferred 39340213681 fully green. Regularized-views deadline risk recorded on think-uomm.
