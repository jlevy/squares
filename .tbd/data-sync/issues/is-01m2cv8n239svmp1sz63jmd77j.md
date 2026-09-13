---
type: is
id: is-01m2cv8n239svmp1sz63jmd77j
title: "PR #157 review READ-06: raw refinement and publication readers still price sites"
kind: bug
status: open
priority: 2
version: 2
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:47.235Z
updated_at: 2026-09-13T07:49:44.083Z
---
packing/devtools/measure_threshold_net_refinement.py:452 preserves weighted fields while emitting an unweighted budget; check_rung_figures.py:269-275 accepts that interpretation. The explainer facts reader and verifiable-claim facts reader also lack explicit weighted refusal. Repro: a T025 atom changed to counts [2,1,1] keeps emitted budget 685457679/62500000 instead of the actual 137092261/12500000. Fix: explicitly refuse weighted input at these public raw-record boundaries until their coverage/publication contracts are admitted.

## Notes

Scope correction 2026-09-13T07:52Z: the review's READ-06 text also names 'the explainer facts reader and verifiable-claim facts reader'. I verified both genuinely handle threshold atoms and were missing from my first lane brief: packing/devtools/render_explainer.py (threshold certificate read at ~1433-1474, computes threshold_atoms and threshold_budget) and packing/devtools/render_verifiable_claim.py (~78-88, ~364). Both price sites and would understate a weighted atom the same way measure_threshold_net_refinement.py does. Added to the lane. Both are publication-facing, so refusal is the right treatment rather than teaching them to price tokens. Caution recorded: render_explainer.py's RENDER_INPUTS is test-bound to the Pages workflow path filter, and both renderers are drift-checked against generated outputs that are excluded from Markdown formatting.
