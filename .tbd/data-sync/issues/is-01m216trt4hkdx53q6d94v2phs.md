---
type: is
id: is-01m216trt4hkdx53q6d94v2phs
title: Replace the isotropic pressure term with a directional wall-pressure arm
kind: feature
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m20zyy839t6mbvpqy8ay2hsn
created_at: 2026-09-08T19:10:02.051Z
updated_at: 2026-09-08T23:57:15.427Z
---
exp-132 refuted the isotropic wall-pressure surrogate (mu * mean squared offset from the bounding-box centre) and showed WHY it fails: required_side is minimised by a tight square, the surrogate by a disc, and where they disagree the search follows the term it can feel everywhere. At n = 5 every seed returned exactly 2*sqrt(2) and at n = 11 every seed returned exactly 4.0, past optima the control reaches.

That refutes the surrogate, NOT the idea of a dense objective, and the two must not be conflated in the record.

A round-2 wall-pressure arm should be directional, the way Squarl's is: push each square from the container boundary it is nearest, which has no reason to prefer a disc. Implement it in packing/sqsearch/src/geom.rs beside geom::spread, keep it behind its own flags so the control stays reachable, and score it on the same eleven cells, five seeds and pair-test budget as exp-131 and exp-132 so the three are comparable.

Do not carry mu * spread forward. exp-130 swept it from 0.02 to 50, ramped and flat, and exp-132 measured the constant version as harmful; the useful range is empty.
