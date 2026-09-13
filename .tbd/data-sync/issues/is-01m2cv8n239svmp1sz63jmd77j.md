---
type: is
id: is-01m2cv8n239svmp1sz63jmd77j
title: "PR #157 review READ-06: raw refinement and publication readers still price sites"
kind: bug
status: open
priority: 2
version: 1
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:47.235Z
updated_at: 2026-09-13T07:38:47.235Z
---
packing/devtools/measure_threshold_net_refinement.py:452 preserves weighted fields while emitting an unweighted budget; check_rung_figures.py:269-275 accepts that interpretation. The explainer facts reader and verifiable-claim facts reader also lack explicit weighted refusal. Repro: a T025 atom changed to counts [2,1,1] keeps emitted budget 685457679/62500000 instead of the actual 137092261/12500000. Fix: explicitly refuse weighted input at these public raw-record boundaries until their coverage/publication contracts are admitted.
