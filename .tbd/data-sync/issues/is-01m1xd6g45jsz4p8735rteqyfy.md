---
type: is
id: is-01m1xd6g45jsz4p8735rteqyfy
title: "Phase 4: draw the 18x18 poster composite known-best-1-324 beside the 1-100 figure"
kind: feature
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-07-atlas-expansion-to-324.md
labels: []
dependencies:
  - type: blocks
    target: is-01m1xd6geb617x4k8m7wmwj57r
  - type: blocks
    target: is-01m1xd6grg7z892j713te59san
parent_id: is-01m1xd517vezdmp4hrmvs5c8bp
created_at: 2026-09-07T07:44:20.100Z
updated_at: 2026-09-07T12:24:28.515Z
closed_at: 2026-09-07T12:24:28.514Z
close_reason: "known-best-1-324 shipped: 18x18, 4224x4912, SVG 6,198,351 B under the 8 MiB budget with three measured encoding levers, PNG and PDF with receipts, schemas pinned, 1-100 family byte-identical."
resolution: null
duplicate_of: null
---
Composite specification for 1..324 at 18 columns, same card scale as the 1-100 figure, computed legend/footer baselines, recomputed legend totals; byte-budget measurement built into the builder report (target SVG <= 8 MB; drop per-square data-* attributes in the poster first, coordinate precision second, recorded against D-359); exports svg + 1x png + pdf with receipts, 2x only if under budget; hue-separation test past 20 classes; perfect-square rigidity derivation for k = 11..18; playbook section rewritten as 'the two composites'. The 1-100 family is not touched.
