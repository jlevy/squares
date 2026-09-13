---
type: is
id: is-01m2e9etf82fvg7xz4xg6dn4zc
title: Independently admit the BC303 T2 charge reader before exp-158
kind: task
status: in_progress
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Astra Max mathematics plus Sol source replay
labels:
  - n11
  - math-review
dependencies:
  - type: blocks
    target: is-01m2e6e4j1ee5nre22gp7fyyrc
  - type: blocks
    target: is-01m2eddtqbpv11d9g5yk0s8cv0
parent_id: is-01m2e6e4j1ee5nre22gp7fyyrc
created_at: 2026-09-13T21:06:03.879Z
updated_at: 2026-09-13T22:16:55.624Z
---
Review exact clean cdf854e2 charge-reader branch source-bound identity, 377 atoms and 182 charts, C clipped/coincident event sweep, closed witness replay, S strict first-owner strip, adversarial reference controls, and H-160/exp-158 frozen thresholds against accepted X-029/charge bridge. Retain ACCEPT/REFUSE with exact source blobs and conditions. Do not run target until reader admission; no global T2 or s11 claim.

## Notes

2026-09-13 independent admission REFUSE at clean cdf854e240aa0068b0a4554f6c20d09385aa02d8. Full review with exact source and implementation blobs: /private/tmp/bc303-t2-charge-reader-review-2026-09-13.md. R1 Blocker think-sv4b: reflected index-180 C and S parent receipts pass replay while their inverse-reflected source slopes exceed U180=1. R2 High think-3lcm: capped reference search skips a feasible zero-charge synthetic cell and returns 1 instead of 0; add actual interior end/start control. Retained target-free controls: /private/tmp/test_bc303_t2_charge_reader_admission_2026_09_13.py; log /private/tmp/bc303-t2-charge-reader-admission-2026-09-13.log; 3 failing regressions and 2 passing independent controls in 1.10 s. Existing geometry/charge suite 7 passed in 1.31 s; pinned source-check passes 377 atoms and 182 charts; independent frozen manifest/seam comparison passes. Exact clipping/event/C-prefix math, C boundary reduction, S strict first-owner implication, nonnegative atom authentication, and H-160/exp-158 thresholds survive. No actual source charge or target was evaluated; no source edits or PR change. Admission remains open and depends on both repairs; instrument_ready must remain false until fresh independent admission.

2026-09-13 repair checkpoint: clean local branch codex/bc303-t2-charge-reader-repair at 0f20fdcdd5bac7e0734b29cd0b0efef4ffea3699 (base cdf854e240aa0068b0a4554f6c20d09385aa02d8). R1/R2 implementation and durable target-free controls are committed; historical source-distinct REFUSE is docs/project/reviews/review-2026-09-13-bc303-t2-charge-reader-refusal.md, with its original failing log retained under packing/cases/n11_five_dot_cover/evidence/. Focused geometry, charge, and original admission controls: 20 passed. Ruff, BasedPyright, documentation check, and packing-validate --edit: passed (45/74 selected steps). No BC293 target charge, H-160/exp-158 edit, target invocation, push, or PR. Fresh independent admission of this exact clean head remains required before setting instrument_ready or invoking exp-158.
