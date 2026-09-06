---
type: is
id: is-01m1tkdw9gt7rkyzsrs5j8wtkq
title: "Explainer: the LP paragraph overstates what tau* depends on, when a certificate exists, and what a round optimum means (F6)"
kind: task
status: open
priority: 2
version: 1
labels:
  - review-gpt6
dependencies: []
parent_id: is-01m1tkdspk8c3n71xsc2e2t4g7
created_at: 2026-09-06T05:35:30.095Z
updated_at: 2026-09-06T05:35:30.095Z
---
Finding 6, confirmed at explainer-article.md:462-474. Three corrections: (1) the finite LP depends on the site set A and the net Theta as well as L and B -- write tau*(A, Theta; L, B) or say so in words; (2) 'a certificate exists exactly when tau* < n' needs Conditions 1, 3 and 4 kept alongside (reviewer's example: L = B = 2, net {0, 1/2}, one unit atom at the centre has LP optimum 1 < 2 yet Condition 4 fails); (3) 'an optimum that lands on a round number is a sign of a bug' is unjustified -- incidence constraints produce simple optima routinely -- restate the intended point (the target n never enters the objective) without the categorical claim. Also describe the output as a verified feasible rational certificate rather than an exact optimum: scaling all weights by 4000/4001 keeps coverage and lowers total mass to 434547/40010, so the submitted vector is not an exact minimiser. Acceptance: the paragraph makes only claims the verifier supports.
