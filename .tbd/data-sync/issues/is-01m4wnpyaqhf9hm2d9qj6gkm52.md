---
type: is
id: is-01m4wnpyaqhf9hm2d9qj6gkm52
title: Return the subsecond Barnett lineage test to ordinary PR coverage
kind: bug
status: closed
priority: 1
version: 3
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4w9w2vc4p0j983wvvx8pybw
hold: null
hold_until: null
created_at: 2026-10-14T07:40:58.571Z
updated_at: 2026-10-14T08:44:52.694Z
started_at: 2026-10-14T07:42:01.021Z
closed_at: 2026-10-14T08:44:52.694Z
close_reason: Fixed, independently confirmed in PR592 reviews D/E/F/G, green fast+Pages+full checkpoint38530454327 at final7a184720, and merged as f73e9de13d8ccc40b91d844b164f9c2ad9c032c1. Full mathematical proof replays remain tracked separately; no new verified n17 bound claimed.
resolution: null
duplicate_of: null
---
Main run38527537364 slow-lane failed solely because the Barnett/Ryan Xu/Ostashev lineage test was slow-marked but measured0.80s below the1s floor. Remove its marker and matching inventory entry while preserving the scientific assertions and all timing policy; fix and rerun current-head checkpoint.
