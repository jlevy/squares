---
type: is
id: is-01m5am54cgqre33jvgjqb5my53
title: Deferred atlas rebuild (900 s) and slow lane (1800 s) run at their command deadlines on hosted runners
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-10-19T17:43:08.432Z
updated_at: 2026-10-19T18:36:34.106Z
---
Deferred checkpoint job deferred-atlas-grid, step 'known-best n=1..324 atlas rebuild' (devtools.build_known_best_atlas --check, --jobs 1 --inner-jobs 2), 900 s command deadline. Main dispatch runs 2026-10-19: 619.76 s (39233374262), 620.25 s (39244113905), 611.56 s (39250299524), 875.91 s (39256144591), 692.64 s (39262635681). PR #685 dispatch 39292263543 (merge 3c516dd7) timed out at 901 s; #685 does not touch the atlas builder or its inputs (sqpack changes: release.py edition metadata, cli/validate.py site forwarder env). Under OR-17 the deadline is not to be raised blindly: profile the rebuild (where 600-900 s goes on a 4-CPU hosted runner), reduce or partition it, or re-select its ceiling on a recorded measurement. Not a flake root cause.

## Notes

2026-10-19 #685 second dispatch 39297968153 (head f3495bc0e): atlas rebuild again 901 s timeout; slow behavioral tests timed out at 1801 s with 233/234 started tests finished — gw1 still in tests/test_n11_corner_class_certificate.py::test_the_gate_decides_the_case_certificate_under_the_corner_clip (a 27 s test in the passing attempt), reached at +29.8 min vs +22.5 min in passing run 39292263543; other workers finished at ~16 min vs ~12 min. Not a hang: ~1.3x slower runner and an imbalanced xdist tail. Main 39262635681 (#665 premerge) slow-lane job 1819 s total, passed just under its deadline. Exhaustive-3 1347 s vs 920 s in the same comparison. Concurrent main-only control dispatched 2026-10-19T18:36Z to separate runner variance from source.
