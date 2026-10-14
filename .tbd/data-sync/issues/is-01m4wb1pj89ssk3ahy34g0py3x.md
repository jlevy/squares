---
type: is
id: is-01m4wb1pj89ssk3ahy34g0py3x
title: "PR592 C1: prevent component evidence from lifting whole-value rungs"
kind: bug
status: closed
priority: 1
version: 3
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wajcx0q76t3ppdzfbjxq4d
hold: null
hold_until: null
created_at: 2026-10-14T04:34:36.741Z
updated_at: 2026-10-14T08:44:52.594Z
started_at: 2026-10-14T04:36:48.907Z
closed_at: 2026-10-14T08:44:52.593Z
close_reason: Fixed, independently confirmed in PR592 reviews D/E/F/G, green fast+Pages+full checkpoint38530454327 at final7a184720, and merged as f73e9de13d8ccc40b91d844b164f9c2ad9c032c1. Full mathematical proof replays remain tracked separately; no new verified n17 bound claimed.
resolution: null
duplicate_of: null
---
Published correctness C1: part evidence lifts T153/T154 to V3/C3 without proving the complete result. Require claim coverage appropriate to result kind and combine both bound sides at their weaker rung; regress actual part evidence and complete matching proofs.
