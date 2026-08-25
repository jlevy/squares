---
type: is
id: is-01m0wqygmp0vft6a22t9wj6w6f
title: Renumber parallel campaign IDs with repren and migrate research artifacts to v2
kind: task
status: open
priority: 0
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels: []
dependencies:
  - type: blocks
    target: is-01m0wqyh11mntsvcyx7q35eph3
  - type: blocks
    target: is-01m0wqyhbewrv51618f7s0tne0
  - type: blocks
    target: is-01m0wqyhnttmv40agfac8g69jf
parent_id: is-01m0wqx97nb22qwx8v47hrpfqk
created_at: 2026-08-25T15:17:16.565Z
updated_at: 2026-08-25T15:18:12.664Z
---
Keep the earlier PR31 allocations exp-037/H-042. Use a reviewed repren simultaneous map to rename the later research lineage exp-037 to exp-038, exp-038 to exp-039, and Trump H-042 to H-043 across filenames and content without cascading. Dry-run first; check collisions and stale references; update tbd notes separately. Migrate the two exact research rounds from Experiment/v1 precision: exact to Experiment/v2 assurance verified and method exact-algebraic, add all new durable documents to DocumentMap/v1, and regenerate ledger references.
