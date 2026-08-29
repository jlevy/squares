---
title: H-001 — an angle-class proposer beats free-coordinate annealing
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-001
  kind: hypothesis
  claim: >-
    A proposer restricted to at most three learned angle classes, followed by the common
    LP-in-cell quench, reaches preregistered target components at n = 5, 10, 17, and 11
    in fewer pair-tests than free-coordinate annealing under the same downstream spine.
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:2', 'search:6', 'search:18']
  criterion:
    shape: record
    metric: pair-tests to the preregistered target component at each cell
    direction: lower
    threshold: baseline annealer at equal pair-test budget
  instrument: >-
    Not yet built. Needs the LP-in-cell quench (H-002) plus an angle-class proposer in
    which squares carry a class index rather than a free angle.
  instrument_ready: false
  regime: >-
    ladder cases n = 5, 10, then oblique calibration n = 17 and target n = 11;
    equal pair-test budget and the same polish, identity and verifier backend
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [5, 10, 17, 11]}
  priority: 2
  cost_estimate: tier M (1e11 pair-tests)
  prereqs: [H-002]
  replication: false
  registered: retroactive
  notes: >-
    Narrows the standing review's compound H-1 to the algorithmic comparison. The
    descriptive corpus claim that record packings use at most three angles is now H-024
    and cannot decide this experiment. Kill if the paired proposer does not improve
    target-component arrivals per pair-test on the proved/mechanism ladder.
---
# H-001 — the search space is smaller than it looks

The
[LP-in-cell result](../../../docs/project/reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md#r-2)
says the honest continuous dimension of this problem is `n` — the angles — not `3n + 1`.
Everything else is the combinatorial choice of cell, and the cell is solved exactly by a
linear program.

Empirically the displayed Trump `n = 11` construction uses one non-trivial tilt and the
`s(17)` record uses two.
H-024 tests whether that observation generalizes across the corpus; H-001 tests whether
the restriction helps search, whether or not the descriptive claim generalizes.

## Why this is registered retroactively

It originates in the standing review’s register (as H-1), which was written before this
campaign’s registry existed, so it is marked `retroactive` rather than back-dated.
It absorbed this campaign’s own two-tilt-restriction hypothesis, which claimed the same
thing for the special case of exactly two classes.

The general form is better: two classes is what `n = 11` happens to use, and a
hypothesis tuned to the answer we already have would have shown much less.
The caution recorded against the narrow version still applies — a win here shows that
*given* the right angular structure the rest is easy, which is a real finding about
where the difficulty lives, but is not evidence that an unguided method could find
`n = 11`. The sweep is what keeps that honest: it must also hold at `n = 5` and
`n = 10`, then pass the oblique `n = 17` calibration before its `n = 11` result is used
strategically.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
