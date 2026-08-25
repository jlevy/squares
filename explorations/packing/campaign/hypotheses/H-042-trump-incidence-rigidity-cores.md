---
title: H-042 — every Trump derivative branch has a proper incidence rigidity core
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-042
  kind: hypothesis
  claim: >-
    Every one of the 128 derivative-distinct fixed-side branches at Trump's exact
    n = 11 pose has a proper inclusion-minimal subset of its 25 geometric incidences
    whose grouped derivative rows still force the branch cone to be {0}.
  lane: proof
  derived_from: [X-001]
  strategy_refs: ['proof:20', 'proof:21']
  criterion:
    shape: determination
    metric: >-
      exact grouped-incidence zero-cone certificates and exact one-group-deletion
      directions for all 128 derivative-distinct branches
    direction: >-
      every branch has an incidence-minimal zero-cone core that removes at least one
      oriented derivative-row class from the complete branch system
  instrument: >-
    A successor to cases.trump11.tangent_cones will rederive the complete exp-013
    branch universe, keep the rows of each wall incidence or selected contact feature
    atomic, normalize oriented half-space row classes exactly over Q(u), and greedily
    minimize groups with an exact terminal zero-or-direction oracle.
  instrument_ready: false
  regime: >-
    Trump's labeled exact pose over Q(u), fixed container side, the existing anchored
    33-variable chart, 11 wall-incidence groups and 14 branch-selected contact groups;
    tied support rows remain conjunctive and incidental zero-projection noncontacts
    remain excluded
  instance: {axis: n, point: 11}
  sweep: {axis: derivative_branch, points: [all-128-exp-013-matrices]}
  priority: 1
  cost_estimate: >-
    meter one branch and eight representative branches first; a complete pass needs at
    most 3,200 greedy group decisions before caching, followed by exact replay
  prereqs: [exp-013 complete exact branch inventory and replay]
  replication: true
  registered: '2026-08-25'
  notes: >-
    The quantifiers are for every branch there exists a branch-specific core, not one
    common physical core. The claim is about grouped first-order inequalities only.
    It asserts neither uniqueness nor minimum cardinality and implies no isolation
    radius, side stability, nonlinear prestress stability, distant-contact restriction,
    or global optimality. An out-of-scope unretained float scout examined primitive-row
    deletion on branch 0 before registration; it did not test grouped incidences, and
    its suggested 34-row threshold is excluded from this criterion.
---
# H-042 — test whether Trump rigidity is incidence-redundant in every branch

For one derivative branch `b`, let `G_b` contain the eleven active wall incidences and
the fourteen active pair contacts with that branch’s selected separating feature.
Each group is atomic: a tied wall support or selected contact may contribute two
simultaneous scalar rows, and the experiment may not split them.

For `S ⊆ G_b`, let `A_b(S)` contain the union of those grouped rows after exact
normalization of positive-proportional rows as the same oriented half-space.
The tested cone is

```text
C_b(S) = {v in R^33 : A_b(S) v >= 0}.
```

The claim is `∀b ∃S_b`, where `S_b` is a proper subset, `C_b(S_b) = {0}`, and deleting
any one retained group makes the cone nonzero.
“Proper” requires the selected groups to omit at least one derivative-row class, so a
duplicate provenance label cannot accept the hypothesis by itself.

## Exact decision contract

A branch accepts only with both kinds of replayable certificate:

- exact rank 33 and an exact stress strictly positive on every retained row, with
  `A_b(S_b)^T λ = 0`, prove the selected cone is zero;
- for every retained group `g`, an exact normalized nonzero vector satisfying all rows
  of `A_b(S_b − {g})` proves group-level inclusion minimality.

A deterministic greedy deletion order may return **an** inclusion-minimal core.
It is not “the” core, a unique core, a minimum-cardinality core, or a census of all
cores. Monotonicity makes one pass sufficient: once deleting a group produces a nonzero
cone, later deletions cannot restore rigidity without that group.

H-042 is accepted only if all 128 exp-013 matrix keys terminate with proper exact cores.
It is rejected if any branch’s complete normalized group system is exactly
inclusion-minimal.
A numerical proposal failure, timeout, branch drift, missing alias, or
missing exact witness leaves the result unresolved.

The first run is a one-branch instrument check, followed by eight representative matrix
keys before a complete pass.
Partial branch coverage may validate the instrument but cannot decide the universal
claim.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
