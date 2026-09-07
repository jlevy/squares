---
type: is
id: is-01m1xd6g45jsz4p8735rteqyfy
title: "Phase 4: draw the 18x18 poster composite known-best-1-324 beside the 1-100 figure"
kind: feature
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-07-atlas-expansion-to-324.md
labels: []
dependencies:
  - type: blocks
    target: is-01m1xd6geb617x4k8m7wmwj57r
  - type: blocks
    target: is-01m1xd6grg7z892j713te59san
parent_id: is-01m1xd517vezdmp4hrmvs5c8bp
created_at: 2026-09-07T07:44:20.100Z
updated_at: 2026-09-07T11:53:20.381Z
---
Composite specification for 1..324 at 18 columns, same card scale as the 1-100 figure, computed legend/footer baselines, recomputed legend totals; byte-budget measurement built into the builder report (target SVG <= 8 MB; drop per-square data-* attributes in the poster first, coordinate precision second, recorded against D-359); exports svg + 1x png + pdf with receipts, 2x only if under budget; hue-separation test past 20 classes; perfect-square rigidity derivation for k = 11..18; playbook section rewritten as 'the two composites'. The 1-100 family is not touched.
