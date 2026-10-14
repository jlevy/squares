---
type: is
id: is-01m4wnpyaqhf9hm2d9qj6gkm52
title: Return the subsecond Barnett lineage test to ordinary PR coverage
kind: bug
status: in_progress
priority: 1
version: 2
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4w9w2vc4p0j983wvvx8pybw
hold: null
hold_until: null
created_at: 2026-10-14T07:40:58.571Z
updated_at: 2026-10-14T07:42:01.022Z
started_at: 2026-10-14T07:42:01.021Z
---
Main run38527537364 slow-lane failed solely because the Barnett/Ryan Xu/Ostashev lineage test was slow-marked but measured0.80s below the1s floor. Remove its marker and matching inventory entry while preserving the scientific assertions and all timing policy; fix and rerun current-head checkpoint.
