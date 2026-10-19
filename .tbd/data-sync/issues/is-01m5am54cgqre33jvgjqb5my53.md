---
type: is
id: is-01m5am54cgqre33jvgjqb5my53
title: "Known-best n=1..324 atlas rebuild runs at 68–97% of its 900 s deferred deadline and timed out on #685"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-10-19T17:43:08.432Z
updated_at: 2026-10-19T17:43:08.432Z
---
Deferred checkpoint job deferred-atlas-grid, step 'known-best n=1..324 atlas rebuild' (devtools.build_known_best_atlas --check, --jobs 1 --inner-jobs 2), 900 s command deadline. Main dispatch runs 2026-10-19: 619.76 s (39233374262), 620.25 s (39244113905), 611.56 s (39250299524), 875.91 s (39256144591), 692.64 s (39262635681). PR #685 dispatch 39292263543 (merge 3c516dd7) timed out at 901 s; #685 does not touch the atlas builder or its inputs (sqpack changes: release.py edition metadata, cli/validate.py site forwarder env). Under OR-17 the deadline is not to be raised blindly: profile the rebuild (where 600-900 s goes on a 4-CPU hosted runner), reduce or partition it, or re-select its ceiling on a recorded measurement. Not a flake root cause.
