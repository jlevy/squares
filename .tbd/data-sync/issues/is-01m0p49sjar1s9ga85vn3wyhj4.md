---
type: is
id: is-01m0p49sjar1s9ga85vn3wyhj4
title: "canonicalize: two-level basin identity"
kind: task
status: open
priority: 1
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies:
  - type: blocks
    target: is-01m0p49sw331h8m9sjdcdyzg2d
  - type: blocks
    target: is-01m0p49t5hw127hm2yfvxynanf
parent_id: is-01m0p49s01h862tq6wp0dd085c
created_at: 2026-08-23T01:38:28.041Z
updated_at: 2026-08-23T01:40:59.455Z
---
Review R-1. Geometric key: canonicalize under the container's D4 and square relabelling, quantize at a stated resolution, hash - the fast path. Structural key: contact graph up to isomorphism after refinement - ground truth, and what makes basin statistics comparable across move sets. Report both. Measure rather than guess the quantization resolution: too coarse merges distinct basins, too fine splits one across float noise. Test by construction: generate a packing's full symmetry orbit, assert a single canonical key.
