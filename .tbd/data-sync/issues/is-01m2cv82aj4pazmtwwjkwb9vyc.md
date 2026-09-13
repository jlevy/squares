---
type: is
id: is-01m2cv82aj4pazmtwwjkwb9vyc
title: "PR #157 review READ-01 (High): orbit admission can accept a violated weighted row"
kind: bug
status: open
priority: 1
version: 1
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:28.050Z
updated_at: 2026-09-13T07:38:28.050Z
---
packing/devtools/admit_threshold_atom_orbits.py:216 sums cached memberships once per site while its budget counts tokens. Repro: unit square centered (1,1) in side-two container, family weight 3/2, four-image orbit of sites (1,1),(1,17/10) with counts (2,1), threshold 2 -> returns admitted=True, charge 0, budget 4; exact weighted charge is 6. Fix: sum multiplicity times cached membership; retain a heavy-site-only negative control plus a valid positive control. This is false ROW admission; K0-K3 remains unchecked so it is not a demonstrated false global bound.
