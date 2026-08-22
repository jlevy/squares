---
type: is
id: is-01m0n6qw9bg0rbmjk383mvfp5s
title: "Catalogue: interval arithmetic and branch-and-bound rigorous proofs"
kind: task
status: closed
priority: 0
version: 3
assignee: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m0n6pa4vsng8hxap83wb279e
created_at: 2026-08-22T17:01:52.299Z
updated_at: 2026-08-22T17:07:23.045Z
closed_at: 2026-08-22T17:07:23.045Z
close_reason: "Found the actual frontier: Montanher, Neumaier, Markot, Domes, Schichl (J. Global Optim. 2018) apply interval branch-and-bound with a sentinels non-overlap formulation to unit squares with free rotation, rigorously settling n=3. Markot reaches n=33 for circles. This OVERTURNS the doc's earlier claim that the approach was untried; corrected in place."
---
The most promising untried line. Study the circle-packing precedent (Markot and successors) in detail, then assess concretely what breaks for squares: the disjunctive separating-axis condition and the rotational degree of freedom. Estimate whether the case explosion is merely large or prohibitive.
