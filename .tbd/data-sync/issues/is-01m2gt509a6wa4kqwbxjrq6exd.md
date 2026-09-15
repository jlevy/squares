---
type: is
id: is-01m2gt509a6wa4kqwbxjrq6exd
title: "Route S: admit sparse T-025 orbit compression"
kind: task
status: in_progress
priority: 0
version: 7
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
updated_at: 2026-09-15T20:02:42.121Z
---
Admit a fixed-geometry support-sparse subfamily of T-025 before any target runs: select and exactly reweight complete D4 orbits from the frozen 119-orbit support, with at most 23 positive orbit representatives, unchanged geometry and threshold semantics, exact budget below 11, and later two-route coverage replay. Treat T-026 only as a support/rescaling provenance control during admission. A target may begin only after the admission PR merges.

## Notes

PR 177 merged at 5ce2839f17b2f5a337260dc3f649e05ab974bd25 after fast and deferred full gates passed. Session 134 opened draft PR 182 as a no-target Route S admission checkpoint. Session 135 discharged all four source-distinct guards: checker-owned T-025 and T-026 digests, both 720-step and 1440-step T-026 sentinels, a canonical source-bound nonempty selection manifest, and the full X-032 mutation matrix. An independent re-audit returned ADMIT after a symlink-alias boundary repair. The retained receipt, 63 focused tests, schemas, records, Ruff, and BasedPyright pass locally. Exact-head hosted certification and merge now belong solely to think-so4g. H-163 is open but untested, exp-161 remains unallocated, and no optimizer, candidate, coverage target, or scientific verdict ran.
