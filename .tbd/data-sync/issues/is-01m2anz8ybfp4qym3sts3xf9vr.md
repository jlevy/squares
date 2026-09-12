---
type: is
id: is-01m2anz8ybfp4qym3sts3xf9vr
title: Make BC329 raw and exact schedulers bounded and completion-aware
kind: bug
status: in_progress
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: root implementation
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m2anzgc2aqn6vzx29ps3rpn2
  - type: blocks
    target: is-01m2aj2d1mccqf56hnxqqcwt1b
  - type: blocks
    target: is-01m2aj2e56r62h83avk7kexvhb
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T11:27:48.158Z
updated_at: 2026-09-12T14:13:24.519Z
---
The raw and normalized-exact routes still use ProcessPoolExecutor.map over the whole direction net. Eager submission weakens the memory bound, and ordered consumption can hide an already completed dense/slab disagreement behind a slower earlier direction until the deadline. Replace both routes with a bounded completion-order scheduler, cap outstanding tasks at a declared multiple of the worker count, atomically retain every landed result, preserve deterministic minima and final net ordering, promote any completed exact disagreement before timeout classification, and terminate workers on incomplete exits. Add adversarial controls for slow-prefix/fast-disagreement, deadline, bounded submission, deterministic ties, and partial readback before admission.

## Notes

First implementation bounded raw/exact work at 2W and promoted completed disagreements, with 137 integrated tests passing. Root plus independent Sol audit found a blocking partial-readback race: rows from a landed batch are written before its one receipt, so a kill can leave extra sparse rows and the reader cannot recover which indices the last count/minimum summarized. Follow-up now adds canonical completed_directions to partial raw/exact receipts and reconstructs exactly that set while treating later valid rows as unpublished. Do not close until adversarial race controls and integrated validation pass.
