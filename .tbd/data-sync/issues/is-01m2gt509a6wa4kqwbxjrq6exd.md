---
type: is
id: is-01m2gt509a6wa4kqwbxjrq6exd
title: "Route S: admit sparse T-025 orbit compression"
kind: task
status: closed
priority: 0
version: 9
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - research
dependencies: []
parent_id: is-01m2exznj4k1zyz1rczby8ch2k
child_order_hints:
  - is-01m2k79x7hsjbtddk51nhehcpf
  - is-01m2k9tx5ydxdk8ty7vj0mk728
hold: null
hold_until: null
created_at: 2026-09-14T20:36:16.810Z
updated_at: 2026-09-16T07:25:59.204Z
closed_at: 2026-09-16T07:25:17.875Z
close_reason: "PR #182 merged at 1d9c49c4 after independent exact-head review, 59 focused Route S tests, complete records validation, and green hosted fast/Pages checks. The target-blind instrument is admitted; H-163 remains open and untested, exp-161 remains unallocated, and no scientific target ran."
resolution: null
duplicate_of: null
---
Admit a fixed-geometry support-sparse subfamily of T-025 before any target runs: select and exactly reweight complete D4 orbits from the frozen 119-orbit support, with at most 23 positive orbit representatives, unchanged geometry and threshold semantics, exact budget below 11, and later two-route coverage replay. Treat T-026 only as a support/rescaling provenance control during admission. A target may begin only after the admission PR merges.

## Notes

Completed by PR #182, merged as 1d9c49c4 with reviewed head 609d7d62. The target-blind Route S instrument is admitted with the at-most-23 orbit policy, canonical selection manifest, two T-026 provenance sentinels, complete-content Git revision/path bindings, and snapshot-safe parsing. Exact-head validation passed: 59 focused tests, records and 167 controls, Ruff, BasedPyright, hosted fast checks, and Pages. H-163 remains open and untested; exp-161 is unallocated; no scientific target ran.
