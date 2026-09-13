---
type: is
id: is-01m2cv81pbrvq05vbrwnq9jwc4
title: "PR #157 review MATH-04: module comments keep distinct-site formulas; one test comment self-contradicts"
kind: bug
status: open
priority: 3
version: 1
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:27.403Z
updated_at: 2026-09-13T07:38:27.403Z
---
threshold.py:3 and threshold_interval.py:20 still state distinct-site formulas. packing/tests/test_weighted_threshold_atoms.py:96 says two sites cannot reach threshold four immediately before asserting the two heavy sites do. Fix: state the token formulas; correct the contradictory comment.
