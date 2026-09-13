---
type: is
id: is-01m2cv8me5251f1tndg6bgwm9n
title: "PR #157 review READ-05: a successful replay leaves declared results unchecked"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:46.597Z
updated_at: 2026-09-13T08:41:09.802Z
closed_at: 2026-09-13T08:41:09.802Z
close_reason: "Fixed, and CONFIRMED real at the reviewed head rather than at the current tree -- an important distinction, because the repair makes these tests pass now and anyone re-checking the live tree would wrongly conclude the finding was wrong. Before, at the reviewed head: floor_charge=99, threshold_violation=99 and floor_violation=99, individually and all three together, each gave reproduced=True with disagreements=[]; family.placements declared as '56', null or 56.0 all reproduced; and [False] == [0] and [True, False] == [1, 0] are both True in Python so a bare list comparison cannot see a bool index. After: recomputed derives floor_charge (line 194) and both violation flags, _disagreements (line 240) compares all four rationals by name, placement indices go through _integer(at_least=0) per entry (line 277) rejecting bool and negative, and _summary_disagreements (line 289) refuses a malformed family object or placements list and now also compares family.total_weight -- a second content-level binding that was being carried and never read. The required discriminating control is synthetic on purpose: every retained receipt has the floor and binary charges EQUAL, so the retained data alone cannot prove the comparison separates anything; _synthetic_pair builds a 2-site/4-token atom at threshold 2 on a 3-placement family where placement 0 holds both sites, giving floor charge 3 against binary charge 2 on a budget of 2. One fixture was fixed mid-course: the bool control initially passed pre-fix for the wrong reason (the old reader choked on a missing size field and raised a message the match= accepted), so _synthetic_pair(spelling='archived') now makes every isolating control a record the pre-fix reader parses in full. Test file 17 -> 40 tests; 20 failed pre-fix, each for the bug."
resolution: null
duplicate_of: null
---
packing/devtools/replay_weighted_atom_source.py:132-185 ignores floor_charge, threshold_violation and floor_violation; changing any to 99 still reproduces. charged_placements=[false] also passes against [0], and malformed optional family counts can be ignored. Fix: independently recompute and compare both charges and violations; strictly validate nonnegative integer indices and declared family summaries; test a case where floor and binary charges differ.
