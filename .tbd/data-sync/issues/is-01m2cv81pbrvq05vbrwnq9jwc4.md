---
type: is
id: is-01m2cv81pbrvq05vbrwnq9jwc4
title: "PR #157 review MATH-04: module comments keep distinct-site formulas; one test comment self-contradicts"
kind: bug
status: closed
priority: 3
version: 2
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:27.403Z
updated_at: 2026-09-13T08:11:10.560Z
closed_at: 2026-09-13T08:11:10.560Z
close_reason: "Fixed both parts. (a) threshold.py:3-61 and threshold_interval.py:11-64 restated in token terms: (S,a,k,w), A = sum a_x, budget w floor(A/k), the k|A redundant case, the dual sum_{P: a(P and S) >= k} y_P <= floor(A/k), point atoms as |S|=A=k=1, D4 images carrying counts with their sites, and the inclusion-exclusion over j-subsets of TOKENS; also records why _headroom bounds the expansion and not the tokens. (b) test_weighted_threshold_atoms.py:96-97 comment corrected -- the two heavy sites reach the threshold of four on their own while the three light sites stop one token short. The assertions (4 and 3) were already right and were not touched."
resolution: null
duplicate_of: null
---
threshold.py:3 and threshold_interval.py:20 still state distinct-site formulas. packing/tests/test_weighted_threshold_atoms.py:96 says two sites cannot reach threshold four immediately before asserting the two heavy sites do. Fix: state the token formulas; correct the contradictory comment.
