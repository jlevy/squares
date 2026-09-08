---
type: is
id: is-01m1tqpk8py2vac3kvxf76y8c5
title: "A3: state every hypothesis in the Five Conditions box"
kind: bug
status: in_progress
priority: 1
version: 2
labels:
  - review-claude
dependencies: []
parent_id: is-01m1tqpgrh5ym0r6e5apbke7p8
created_at: 2026-09-06T06:50:10.069Z
updated_at: 2026-09-06T06:50:18.722Z
---
explainer-article.md, 'The Five Conditions' preamble. Two hypotheses the proof uses are absent: the net starts at zero and increases (0 = t_0 < t_1 < ... < t_K; the claim document states it, its proof uses it by name, certificate.py enforces t_0 = 0), and the weights are nonnegative (the counting step needs it; the 2026-09-04 review's negative-weight certificate is the cautionary case). Fix per the review: 'a finite set of points in the container, each with a nonnegative rational weight (the atoms; every weight in this certificate is positive), a net of directions theta_k = 2 arctan t_k with rational half-tangents 0 = t_0 < t_1 < ... < t_K, and a shrink B, such that:'; B < 1 can go since Condition 4 implies it. In the Contradiction box, cite nonnegativity at the counting step. C5: the atom definition says 'positive' where every formal document says 'nonnegative'; use the theorem's word and note the certificate's fact.
