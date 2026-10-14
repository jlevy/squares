---
type: is
id: is-01m4wb1pj89ssk3ahy34g0py3x
title: "PR592 C1: prevent component evidence from lifting whole-value rungs"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wajcx0q76t3ppdzfbjxq4d
hold: null
hold_until: null
created_at: 2026-10-14T04:34:36.741Z
updated_at: 2026-10-14T04:36:48.920Z
started_at: 2026-10-14T04:36:48.907Z
---
Published correctness C1: part evidence lifts T153/T154 to V3/C3 without proving the complete result. Require claim coverage appropriate to result kind and combine both bound sides at their weaker rung; regress actual part evidence and complete matching proofs.
