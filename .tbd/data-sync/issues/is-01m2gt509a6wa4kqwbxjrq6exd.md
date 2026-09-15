---
type: is
id: is-01m2gt509a6wa4kqwbxjrq6exd
title: "Route S: admit sparse T-025 orbit compression"
kind: task
status: in_progress
priority: 0
version: 5
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - research
dependencies: []
parent_id: is-01m2exznj4k1zyz1rczby8ch2k
child_order_hints:
  - is-01m2k79x7hsjbtddk51nhehcpf
hold: null
hold_until: null
created_at: 2026-09-14T20:36:16.810Z
updated_at: 2026-09-15T19:04:37.872Z
---
Admit a fixed-geometry support-sparse subfamily of T-025 before any target runs: select and exactly reweight complete D4 orbits from the frozen 119-orbit support, with at most 23 positive orbit representatives, unchanged geometry and threshold semantics, exact budget below 11, and later two-route coverage replay. Treat T-026 only as a support/rescaling provenance control during admission. A target may begin only after the admission PR merges.

## Notes

PR 177 merged at 5ce2839f17b2f5a337260dc3f649e05ab974bd25 after fast and deferred full gates passed. Session 134 opened draft PR 182 as a no-target Route S admission checkpoint. Exact primitives now inventory T-025 as 79 point plus 40 threshold D4 orbits, 904 atoms, and budget 685457679/62500000; verify T-026 common scale 500000000/498684619; measure the 119-to-at-most-23 policy; and round-trip decompressed certificates through the existing loader. The retained checkpoint has all target, optimizer, coverage, candidate, and experiment flags false. Independent review refused admission pending four obligations: pin all T-025/T-026 digests outside the mutable contract; bind both 720-step and 1440-step T-026 sentinels; admit a canonical selection-manifest parser and serializer; and exercise every X-032 mutation refusal. H-163 remains blocked, exp-161 is unallocated, and no scientific target or verdict ran. Continue only from these re-entry obligations on draft PR 182.
