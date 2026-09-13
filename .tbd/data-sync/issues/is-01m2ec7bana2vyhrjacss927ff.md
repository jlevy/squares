---
type: is
id: is-01m2ec7bana2vyhrjacss927ff
title: Repair reflected BC303 T2 parent transport and independent source-cell replay
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - bc303
dependencies:
  - type: blocks
    target: is-01m2e9etf82fvg7xz4xg6dn4zc
parent_id: is-01m2e6e4j1ee5nre22gp7fyyrc
created_at: 2026-09-13T21:54:24.724Z
updated_at: 2026-09-13T22:17:06.637Z
closed_at: 2026-09-13T22:17:06.635Z
close_reason: Repairs committed at 0f20fdcdd5bac7e0734b29cd0b0efef4ffea3699 with 20 target-free focused controls passing and edit tier 45/74 selected steps passing; fresh independent admission think-ncn8 remains open before exp-158
resolution: null
duplicate_of: null
---
Admission review think-ncn8 refuses cdf854e240aa0068b0a4554f6c20d09385aa02d8. In packing/cases/n11_five_dot_cover/bc303_t2_charge_sweep.py lines 409-410 and 431, reflected source index 180 receives an unreflected folded parent; lines 446-448 check the physical slope directly rather than pulling back reflection and the source quarter turn. The existing synthetic fixture produces an accepted C parent (13575/19193,13568/19193), whose inverse-reflected source slope is 13575/13568 > U180=1. Its S first-owner receipt has inverse-reflected slope 207107000000/207106690551 > 1. Fix construction and independent replay for both roles, preserve closed axis aliases and source endpoint policy, reject wrong-reflection parent forgeries, and promote the target-free failing regression /private/tmp/test_bc303_t2_charge_reader_admission_2026_09_13.py into maintained tests. Use a rational angle inside the source cell for S, because the selected index-180 core overshoots the folded endpoint. Complete a fresh independent reader admission before exp-158; do not run target while this repair and admission are open. No target source charges have been evaluated by the review.

## Notes

Construction reflects the folded rational parent; C and S both use a source-admitted physical parent. Replay independently undoes reflection and quarter turns, checks exact inclusive source endpoints and unit length, and rejects prior wrong-reflection C/S forgeries. The reflected index-180 and both axis aliases replay in maintained synthetic tests. Clean local repair commit 0f20fdcdd5bac7e0734b29cd0b0efef4ffea3699 on codex/bc303-t2-charge-reader-repair (base cdf854e240aa0068b0a4554f6c20d09385aa02d8). Focused geometry, charge, and original target-free admission controls: 20 passed. Ruff and BasedPyright: zero findings. Documentation check passes. packing-validate --edit: 45/74 selected steps passed. Historical REFUSE and original failing log retained in repo. No BC293 target charge, H-160/exp-158 edit, target invocation, push, or PR. Fresh independent admission of this exact clean head remains pending.
