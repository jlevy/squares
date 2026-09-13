---
type: is
id: is-01m2cv9cfmxer0nqaefywnmkbn
title: "PR #157 review DOC-06: the threshold-mutation explanation overclaims what budget detects"
kind: bug
status: closed
priority: 3
version: 2
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:39:11.219Z
updated_at: 2026-09-13T08:17:14.568Z
closed_at: 2026-09-13T08:17:14.568Z
close_reason: "Fixed: session-127 lines 311-317 plus a correction bullet. Primary source test_replay_weighted_atom_source.py:174-181 -- the control is _mutated(threshold=3) asserting budget == 2 and 'exact budget 2'. With seven tokens floor(7/k) = 1 for k = 4, 5, 6, 7, so the budget separates none of those four; the text now names the concrete 4->3 mutation and treats threshold as an input checked through the figures it moves. A fifth overstatement was found and fixed in the same pass: the body claimed 'eleven mutation controls move each declared figure in turn', but at 8eea95b3 the parametrized control moved four declared figures only (threshold_charge, budget, size, charged_placements) while recomputed() returned six keys and _disagreements compared four -- floor_charge, threshold_violation and floor_violation were neither recomputed nor compared. The count of eleven is right (4 parametrized + 7 negative); 'each declared figure' was not."
resolution: null
duplicate_of: null
---
session-127 line 296 says a wrong threshold is caught by its budget. With seven tokens, thresholds four through seven all have budget one; the retained test checks the particular mutation 4->3, which changes the budget to two. Fix: describe that concrete mutation and retain threshold as an input checked for consistency through charges and placement lists.
