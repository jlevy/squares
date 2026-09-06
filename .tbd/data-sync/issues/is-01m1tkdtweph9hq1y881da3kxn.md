---
type: is
id: is-01m1tkdtweph9hq1y881da3kxn
title: "Explainer: the contradiction needs the reflection-and-pullback step, not 'one of the 181 net angles' (F2b)"
kind: bug
status: open
priority: 1
version: 1
labels:
  - review-gpt6
dependencies: []
parent_id: is-01m1tkdspk8c3n71xsc2e2t4g7
created_at: 2026-09-06T05:35:28.653Z
updated_at: 2026-09-06T05:35:28.653Z
---
Finding 2b, confirmed. explainer-article.md 'The Contradiction' (line ~436): 'Each square, whatever its angle, contains a side-B square Q_i with the same center at one of the {{N_DIRECTIONS}} net angles.' The net spans [0, pi/4]; a square at 60 degrees is 15 degrees from its nearest net angle, far beyond what B = 0.9977 tolerates. The correct construction reflects the square onto the arc (D4 invariance of the atoms), builds the inner net-oriented square there, and reflects it back, so its orientation lies in the reflected net; the detailed claim proof does this and pulls each inner square back into its own square's interior before using disjointness. Fix: one sentence in the contradiction (and in 'From a Continuum of Angles') naming the reflection and pullback. Acceptance: the condensed argument is literally true as stated.
