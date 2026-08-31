---
type: is
id: is-01m0y08230ny51wne2jxtnd5nf
title: Profile and remove repeated exact row-jet construction
kind: task
status: open
priority: 0
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-research-loop-efficiency-infrastructure.md
labels:
  - packing
  - focus-efficiency
  - performance
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-26T03:01:32.382Z
updated_at: 2026-08-30T10:36:50.314Z
---
Profile the 103–181-second exact row-jet test group and remove repeated deterministic symbolic construction at the narrowest sound boundary. Acceptance: cold and repeated profiles identify the hot constructors; exact rows, gradients, Hessians, stresses, scale records, field and symmetry failures, positive controls, and relevant mutation failures are identical; every semantic input participates in cache or fixture invalidation; a no-reuse or cold path remains testable; repeated-edit median improves by at least 5x on comparable inputs.

## Notes

2026-08-30 session-045: BC-038 closed, rejected on measured arithmetic. devtools/price_row_jet_sharing counts rather than times, because the deciding quantity is whether the 35 evaluate_stress calls share a field identity and a stratum, which a profile cannot see. They largely do not: 11 distinct number fields, and RowJetInventory.active_rows refuses a foreign field by identity rather than by value. 47 active_row_jets rebuilds cover 17 distinct (field, stratum) pairs, so 17 builds are unavoidable however the sharing is arranged and the floor is about 280s against 430s -- a 1.54x ceiling against an exit wanting five-fold and a 45s warm median. The eager inventory the commitment proposes is the weaker arrangement: 11 fields times 3 strata is 33 builds where 17 pairs are requested. The trigger measurement compared unlike things -- 0.025s per call is evaluate_stress with rows handed to it, 11.95s includes building them. Evidence: campaign/series/series-000-smoke-and-calibration/results/bc-038-row-jet-sharing.json. D-384 records that the first counter keyed on id(field), a recycled address, and moved between identical runs. Next action: none for this commitment; it is complete.
