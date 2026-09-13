---
type: is
id: is-01m2cv8n239svmp1sz63jmd77j
title: "PR #157 review READ-06: raw refinement and publication readers still price sites"
kind: bug
status: closed
priority: 2
version: 3
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:47.235Z
updated_at: 2026-09-13T08:19:32.495Z
closed_at: 2026-09-13T08:19:32.494Z
close_reason: "Fixed at four boundaries, two of which I had to add to the lane after re-reading the finding: measure_threshold_net_refinement.py:444-445 (rescaled_record, in __all__, also reached via fixed_core_packet.normalized_record), check_rung_figures.py:266-276 (load_certificate, outside its except-return-None block), render_explainer.py:1469 (new refuse_weighted_threshold_atoms, called at 1518-1519 for coarse and fine certificates), render_verifiable_claim.py:379 (_threshold_facts). The refinement and BC329 CLIs already refuse via their strict loaders and were left alone -- confirmed, not assumed. TWO CORRECTIONS TO THE FINDING, both for the disposition map: (1) the quoted repro no longer reproduces as written -- under the committed weighted_points serialization a weighted atom has no 'points' key, so rescaled_record raises a bare KeyError rather than emitting a wrong budget; the numbers 685457679/62500000 vs 137092261/12500000 (short by exactly 1813/31250000) are exact only for the WITHDRAWN additive spelling, which was verified. The finding still stands: a KeyError is not a refusal and persisted older records can carry the additive spelling. (2) check_rung_figures failed more quietly than 'accepts that interpretation' -- under the new spelling load_certificate returned None, so the artifact dropped out of the check entirely, certificates_checked silently decremented, and every figure anchored to it went unverified. That is worse than a wrong number and is why the refusal raises out of a function documented to return None. Also: RENDER_INPUTS needed no change (it already covers render_explainer.py and src/sqpack), so the Pages path filter and its sync test are untouched."
resolution: null
duplicate_of: null
---
packing/devtools/measure_threshold_net_refinement.py:452 preserves weighted fields while emitting an unweighted budget; check_rung_figures.py:269-275 accepts that interpretation. The explainer facts reader and verifiable-claim facts reader also lack explicit weighted refusal. Repro: a T025 atom changed to counts [2,1,1] keeps emitted budget 685457679/62500000 instead of the actual 137092261/12500000. Fix: explicitly refuse weighted input at these public raw-record boundaries until their coverage/publication contracts are admitted.

## Notes

Scope correction 2026-09-13T07:52Z: the review's READ-06 text also names 'the explainer facts reader and verifiable-claim facts reader'. I verified both genuinely handle threshold atoms and were missing from my first lane brief: packing/devtools/render_explainer.py (threshold certificate read at ~1433-1474, computes threshold_atoms and threshold_budget) and packing/devtools/render_verifiable_claim.py (~78-88, ~364). Both price sites and would understate a weighted atom the same way measure_threshold_net_refinement.py does. Added to the lane. Both are publication-facing, so refusal is the right treatment rather than teaching them to price tokens. Caution recorded: render_explainer.py's RENDER_INPUTS is test-bound to the Pages workflow path filter, and both renderers are drift-checked against generated outputs that are excluded from Markdown formatting.
