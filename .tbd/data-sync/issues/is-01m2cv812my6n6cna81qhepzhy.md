---
type: is
id: is-01m2cv812my6n6cna81qhepzhy
title: "PR #157 review MATH-03: independent witness checker counts sites, not tokens"
kind: bug
status: open
priority: 2
version: 1
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:26.772Z
updated_at: 2026-09-13T07:38:26.772Z
---
packing/src/sqpack/fractional/threshold_interval.py:365 counts one per site. Repro: sites (1,1),(3/2,1), multiplicities (2,2), threshold 4, weight 1, L=3, B=9/10, direction-zero witness (1.25,1.0): true charge 1 but the checker reports admissible charge 0. Fix: independently sum multiplicities in the exact witness routine; retain a weighted exact-witness regression.
