---
type: is
id: is-01m2cv8me5251f1tndg6bgwm9n
title: "PR #157 review READ-05: a successful replay leaves declared results unchecked"
kind: bug
status: open
priority: 2
version: 1
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:46.597Z
updated_at: 2026-09-13T07:38:46.597Z
---
packing/devtools/replay_weighted_atom_source.py:132-185 ignores floor_charge, threshold_violation and floor_violation; changing any to 99 still reproduces. charged_placements=[false] also passes against [0], and malformed optional family counts can be ignored. Fix: independently recompute and compare both charges and violations; strictly validate nonnegative integer indices and declared family summaries; test a case where floor and binary charges differ.
