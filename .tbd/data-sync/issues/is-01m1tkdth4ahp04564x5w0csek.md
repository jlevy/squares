---
type: is
id: is-01m1tkdth4ahp04564x5w0csek
title: "Explainer: the budget sketch counts closed squares as disjoint; introduce interior containment first (F2a)"
kind: bug
status: open
priority: 1
version: 1
labels:
  - review-gpt6
dependencies: []
parent_id: is-01m1tkdspk8c3n71xsc2e2t4g7
created_at: 2026-09-06T05:35:28.291Z
updated_at: 2026-09-06T05:35:28.291Z
---
Finding 2a, confirmed. explainer-article.md 'Atoms, Mass, and the Budget' (line ~191): 'The eleven squares are disjoint, so no atom is counted twice' -- packings allow shared boundaries, and an atom on a shared edge (e.g. (1, 1/2) between [0,1]^2 and [1,2]x[0,1]) is counted twice; atomic measures give boundaries positive mass, so no area argument helps. The detailed proof avoids this by counting the side-B square strictly inside each unit square. Fix: introduce interior containment before the first counting argument (or state the sketch's simplification and point forward to where it is repaired). Acceptance: no counting step in the explainer relies on closed squares being disjoint.
