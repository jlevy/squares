---
type: is
id: is-01m4hp5ky834m02raedees5axg
title: Place n11 three-worker completion controls in the exclusive reachable pool lane
kind: bug
status: open
priority: 2
version: 1
spec_path: development.md
labels: []
dependencies: []
parent_id: is-01m4eszf0kjvjadgn77f0hy2pc
created_at: 2026-10-10T01:17:20.692Z
updated_at: 2026-10-10T01:17:20.692Z
---
The two three-worker completion controls in packing/tests/test_n11_generic_sequential.py
carry only the slow marker.
Their explicit workers=3 reaches ProcessPoolExecutor even when the normal reachable
phase sets PACK_JOBS=1. The documented pool_heavy lane reserves inner resources and runs
serially.

Add pool_heavy to both controls while retaining slow, three workers, the 30-second
budget, source bindings and every strict assertion.
Verify both nodes occur exactly once in the reachable pool phase and never in its normal
phase. Qualify the controls in that declared shape.
Preserve the prior negative; do not accept incomplete results, skip tests or widen
deadlines.

This mismatch is byte-identical on main 1871b14dc, parent f3784895 and child 949b6f6e.
It is pre-existing lane debt, not a regression from the upstream record refresh.
The retained parent result proves only deadline exhaustion: INCOMPLETE, checked 22 of
165, 30.6056 seconds against 30, four steps and 32 rows, geometry false and no
exclusions. The underlying cause is unproved.

The full hosted slow lane uses a separate xdist path.
These annotations alone do not establish hosted isolation; any general scheduler change
needs its own coverage-conservation evidence.
Gupta’s separate broad-run failure remains unresolved without its actual traceback or
subprocess output.

Evidence:
/Volumes/spud-ext1/agent-evidence/polynomial-catalogue-01a118e4/upstream-2026-10-09/current-parent-lane-review.md
and current-parent-negative-triage.json.
The parent’s complete local push attempt hit its 900-second reachable limit; no full
pytest verdict survived.
Actual-head hosted qualification is recorded separately on the parent and publication
beads.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
