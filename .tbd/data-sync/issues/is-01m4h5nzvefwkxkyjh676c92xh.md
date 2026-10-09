---
type: is
id: is-01m4h5nzvefwkxkyjh676c92xh
title: Remove duplicate italic font preload after main integration
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m4h26vpd0pe8frzehv70rt4p
created_at: 2026-10-09T20:29:11.404Z
updated_at: 2026-10-09T20:29:11.404Z
---
Independent senior review found PRELOADED_FACES lists PT Serif400italic twice after merge. Inline publication deduplicates links but direct shared head still emits duplicate hint. Remove only duplicate tuple entry, retain all four distinct regular/italic/bold/front mathfaces and focused preload-order/dedup tests. Low redundant source residue; no duplicate network fetch assertion.
