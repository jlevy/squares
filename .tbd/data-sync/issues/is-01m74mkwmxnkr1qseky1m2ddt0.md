---
type: is
id: is-01m74mkwmxnkr1qseky1m2ddt0
title: "Stage 4 blind review of #943, #944, #945, #947 (Özden's s(156), s(180), s(268), s(269); PR #949)"
kind: task
status: in_progress
priority: 1
version: 5
delegate: bold-ritchie-l83-review
labels:
  - intake
  - review
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-11T06:27:09.085Z
updated_at: 2026-11-11T06:52:23.075Z
started_at: 2026-11-11T06:27:13.030Z
---

## Notes

L83 (bold-ritchie-l83-review) progress.

2026-11-11T06:36:12Z checker frozen: frozen/checker-frozen-digests.txt, list SHA-256 1d5b6e8d4b0c791fef77431ebbbe049daa24a75096dd2f16f1d85a9156c26c54.
Files: l83_reader.py ab7b2cf7, l83_sat.py 2236bccb, l83_clip.py c4987a55, l83_check.py 661fb2cd, l83_geom.py 6542054f, l83_selftest.py de00c72f.
Self-test PASSED, 92 cases (incl. 1,500 random centre-line closings, 600 wall closings, 37 reader refusals).
Read before the freeze: the four issues, the precedent review text, the witness schema's square-entry part, certificate and JSON layout (data). No producer code, no repo witness/verifier/promotion code, nothing of L81.

2026-11-11T06:39:19Z controls plan stated and frozen before l83_controls.py existed: frozen/controls-plan-digest.txt, list SHA-256 90bf88d377215653d17f152a4cfae368be548040d769ea5b9c1b4665bcc609c7 (controls-plan.json 68000b7c). 15 controls per count, 60 in all.
Results (scratch runs): all four certificates ACCEPT by both methods, classes equal everywhere; 60/60 controls as stated (G6 rotation-read-other-way overlaps 65/67/64/97). Sides: every claim is the 12-place ceiling; gaps 2.11277e-3, 1.37502e-3, 4.40049e-4, 5.19002e-4; vs T-260 at 156 1e-41 less. House margins: T-186 1.30e-39, T-276 3.19e-12, T-174 at 180 and 269 exactly 0 (touching pair). Lineage: not one to one with any house; issue counts reproduce with summed-distance assignment, lower-left anchoring. Final run_all in progress.
