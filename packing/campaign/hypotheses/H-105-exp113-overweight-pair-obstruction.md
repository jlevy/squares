---
title: H-105 — exp-113's fixed weights have an overweight-pair obstruction
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-105
  kind: hypothesis
  claim: >-
    Among the 60 distinct D4 placements of trump11-v1, with exactly exp-113's
    retained per-member orbit weights (1,0,2/5,1/10,0,1/10,3/10,0), two distinct
    placements have weight sum greater than one and intersecting interiors.
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:11', 'proof:17', 'proof:22']
  criterion:
    shape: determination
    metric: existence of a strict positive-area overweight-pair witness
    direction: >-
      Accept with one independently checked strict positive-area witness for an
      eligible pair. Reject only with independently checked separating axes for
      all 134 eligible pairs. Incomplete output, timeout or failed replay is
      unresolved. Neither outcome resolves H099 or certifies global a.e. depth.
    threshold: one overweight pair with intersecting interiors
  instrument: >-
    packing/devtools/run_full_size_density_pair_separator.py and the separately
    reviewed packing/devtools/check_full_size_density_pair_separator.py at cf299e6c.
    Exact separating axes or strict rational-radius boxes, with separate 30-second caps.
  instrument_ready: true
  regime: exact retained Trump side and D4 support; exp113 weights unchanged
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: one 30-second producer and one separately bounded 30-second file replay
  prereqs: [independent pair-instrument readiness, prospectively committed experiment]
  replication: false
  registered: '2026-09-06'
  notes: >-
    This predicts a candidate obstruction, not a feasible dual. A checked
    candidate-refuted packet therefore accepts H105. No-hit is not a.e.
    feasibility because three or more squares can cause excess depth without an
    overweight pair. No new row, LP, weights or geometric support is authorized.
---
# H-105 — Does a Pair Already Invalidate the Candidate?

Rejected by
[exp-115](../series/series-000-smoke-and-calibration/experiments/exp-115-h-105-fixed-candidate-pair-obstruction.md):
all 134 eligible pairs have independently checked separating axes.
This leaves the fixed candidate’s higher-order overlap depth and H-099 unresolved.

[Exp-113](../series/series-000-smoke-and-calibration/experiments/exp-113-h-099-trump-support-screen.md)
retained an exact finite-row optimum of $56/5$, not a feasible full-size density dual.
This hypothesis asks whether two squares alone invalidate those fixed weights on a
region of positive area.
It is narrower than [H-099](H-099-trump-d4-finite-support-dual.md).

The four unit-weight placements and 32 other positive-weight placements give
$\binom42+4\cdot32=134$ pairs whose weights sum to more than one.
The remaining positive weights are at most $2/5$, so no other pair is eligible.
Touching at an edge or corner does not qualify: the intersection must contain an open
box with a positive rational radius.
Nonnegative remaining weights preserve the excess throughout that box.

The
[independent instrument review](../series/series-000-smoke-and-calibration/results/agenda-026/bc-254-pair-separator-independent-review.md)
checks the strict-area argument and complete eligible-pair ordering.
Its file checker uses edge determinants for a witness and direct corner projections for
separation, while sharing the exact number field and accepted original-source
validation. It does not repeat the parent LP.

A witness accepts H-105 and retires only this candidate.
Exhausting all eligible pairs rejects H-105 but leaves possible higher-order excess
depth unchecked. H-099 remains unresolved either way.
The witness point must not become a new LP row without a separate full-support
off-boundary check: it may lie on a third square’s boundary.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
