---
type: is
id: is-01m0y08230ny51wne2jxtnd5nf
title: Profile and remove repeated exact row-jet construction
kind: task
status: open
priority: 0
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-research-loop-efficiency-infrastructure.md
labels:
  - packing
  - focus-efficiency
  - performance
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-26T03:01:32.382Z
updated_at: 2026-08-26T04:13:49.211Z
---
Profile the 103–181-second exact row-jet test group and remove repeated deterministic symbolic construction at the narrowest sound boundary. Acceptance: cold and repeated profiles identify the hot constructors; exact rows, gradients, Hessians, stresses, scale records, field and symmetry failures, positive controls, and relevant mutation failures are identical; every semantic input participates in cache or fixture invalidation; a no-reuse or cold path remains testable; repeated-edit median improves by at least 5x on comparable inputs.

## Notes

2026-08-26 profile: 30 exact tests take 212.53s (93.9% of pytest) versus 14.95s for 94 others. They perform 35 production active_row_jets builds plus three independent builds; stress is 122.47s and row-jets 54.00s. Spike immutable per-field/per-stratum RowJetInventory shared by owner, stress, and sheet paths. Predicted 38->6 builds and 30-45s group. Require exact values/gradients/15x15 Hessians, field isolation, mutation safety, cold path, warm median <=45s and p95 <=55s.
