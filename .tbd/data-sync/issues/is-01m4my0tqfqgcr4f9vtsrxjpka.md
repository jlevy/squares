---
type: is
id: is-01m4my0tqfqgcr4f9vtsrxjpka
title: "PR #497 A4: appendix 44.994 -> 45 is exactsolve.place_free turning axis rattlers by 0.0057 deg"
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-code@spud10
labels:
  - regularization
dependencies: []
parent_id: is-01m4my092ypz9gkxjqdy3nr3tp
hold: null
hold_until: null
created_at: 2026-10-11T07:32:15.726Z
updated_at: 2026-10-11T18:54:11.174Z
started_at: 2026-10-11T07:32:31.571Z
closed_at: 2026-10-11T18:54:11.173Z
close_reason: fixed in 5c9f4f227; turn is -1e-4 rad from exactsolve.place_free R bound; at n = 26 squares 8 (axis) and 23 (45 deg) perturbed; reply https://github.com/jlevy/squares/pull/497#issuecomment-6112491605
resolution: null
duplicate_of: null
---
Medium. docs/project/research/research-2026-10-11-evand-regularization-assessment.md:720-726 and :522-523. Squares 3 and 7 at n = 10 are axis rattlers perturbed by 2*atan(1e-4) in exactsolve place_free (R=1e-4, exactsolve.py:637); 45-degree squares are at 45 throughout. PR #497, review A: https://github.com/jlevy/squares/pull/497#pullrequestreview-5482306635
