---
type: is
id: is-01m0p49sjar1s9ga85vn3wyhj4
title: "canonicalize: two-level basin identity"
kind: task
status: closed
priority: 1
version: 5
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies:
  - type: blocks
    target: is-01m0p49sw331h8m9sjdcdyzg2d
  - type: blocks
    target: is-01m0p49t5hw127hm2yfvxynanf
parent_id: is-01m0p49s01h862tq6wp0dd085c
created_at: 2026-08-23T01:38:28.041Z
updated_at: 2026-08-23T16:20:34.128Z
closed_at: 2026-08-23T16:20:34.121Z
close_reason: "Built as sqpack/canonical.py on claude/packing-overnight-strategy-queue (PR #14): two-level identity — a D4- and relabel-invariant quantized geometric key, plus a contact-graph certificate canonical up to isomorphism by individualization-refinement, with angle class and wall-contact node attributes. Six checks in tools/canonical_check.py, wired into test.sh, and four negative controls watching them fail. One control caught the check reusing d4_images to test itself; the symmetry transforms are now written independently."
resolution: null
duplicate_of: null
---
Review R-1. Geometric key: canonicalize under the container's D4 and square relabelling, quantize at a stated resolution, hash - the fast path. Structural key: contact graph up to isomorphism after refinement - ground truth, and what makes basin statistics comparable across move sets. Report both. Measure rather than guess the quantization resolution: too coarse merges distinct basins, too fine splits one across float noise. Test by construction: generate a packing's full symmetry orbit, assert a single canonical key.
