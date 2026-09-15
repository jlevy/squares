---
type: is
id: is-01m2gt509a6wa4kqwbxjrq6exd
title: "Route S: admit sparse T-025 orbit compression"
kind: task
status: in_progress
priority: 0
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - research
dependencies: []
parent_id: is-01m2exznj4k1zyz1rczby8ch2k
hold: null
hold_until: null
created_at: 2026-09-14T20:36:16.810Z
updated_at: 2026-09-15T17:36:50.258Z
---
Admit a fixed-geometry support-sparse subfamily of T-025 before any target runs: select and exactly reweight complete D4 orbits from the frozen 119-orbit support, with at most 23 positive orbit representatives, unchanged geometry and threshold semantics, exact budget below 11, and later two-route coverage replay. Treat T-026 only as a support/rescaling provenance control during admission. A target may begin only after the admission PR merges.

## Notes

PR 177 merged at 5ce2839f17b2f5a337260dc3f649e05ab974bd25 after fast and deferred full gates passed. Session 134 begins BC-343 as W7 pipeline improvement on codex/n11-route-s-admission. Freeze the T-025 source digest, 119-orbit and 904-atom baseline, fixed-support family, 23-orbit ceiling, exact-rational manifest/decompressor, T-026 support/rescaling sentinels, mutation controls, and independent W2 review. No optimizer, coverage target, candidate certificate, experiment record, or scientific verdict runs in this branch. Admission success leaves BC-343 in progress for a separate discriminator PR; guard refusal parks only the frozen family.
