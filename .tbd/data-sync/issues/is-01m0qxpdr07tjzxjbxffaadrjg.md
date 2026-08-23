---
type: is
id: is-01m0qxpdr07tjzxjbxffaadrjg
title: Prototype active-set and contact-graph branch-and-bound search
kind: feature
status: open
priority: 1
version: 3
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - pr-14
  - creative-alternative
dependencies:
  - type: blocks
    target: is-01m0qxpfkjybnxbyx67zy0vyta
  - type: blocks
    target: is-01m0qxpg0nryz3nwhedeqgwm1g
parent_id: is-01m0qxka8ebkztq7erex50vvr2
created_at: 2026-08-23T18:21:30.751Z
updated_at: 2026-08-23T18:21:57.607Z
---
Category: creative alternatives. Search the actual decomposition: angle variables plus a discrete separating-cell or contact topology, with LP solves for each fixed cell. Enumerate or mutate active sets with symmetry and rigidity pruning, traverse adjacent LP bases, and use interval branch-and-bound or SAT disjunctions on remaining angle boxes.

Acceptance: one executable prototype emits proof-carrying cell records, exact pair-test or node budgets, and lower bounds for pruned boxes. It reproduces n = 5 and n = 10, reconstructs the known n = 11 cell when seeded, and is compared with free-coordinate annealing under a declared budget. A failed scale-up still leaves topology counts, pruning ratios and counterexamples.
