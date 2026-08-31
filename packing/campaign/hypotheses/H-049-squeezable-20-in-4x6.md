---
title: H-049 — do 20 unit squares pack squeezably in a 4 by 6 rectangle?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-049
  kind: hypothesis
  claim: >-
    delta((4,6), 20) > 0: twenty unit squares pack into a 4 by 6 rectangle with strictly
    positive squeeze in Arslanov's sense. If true, the m = 10 instance of Arslanov,
    Mustafin and Shangitbayev's rectangle decomposition assembles 36 + 8 + 26 + 20 = 90
    unit squares into a square of side strictly less than 10, giving s(90) < 10 and the
    first sub-grid packing at k <= m for m = 10 -- one step past Cantrell's February
    2025 n = 110 result, which bounded the s(m^2 - m) = m conjecture to m < 11.
  lane: search
  derived_from: [X-009]
  criterion:
    shape: determination
    metric: >-
      an exact or interval-certified packing of 20 unit squares in a rectangle
      4 - delta by 6 for some delta > 0, or exhaustion of the candidate structures
      with a typed refusal per structure
    direction: either determination ends the question; only delta > 0 opens n = 90
  instrument: >-
    The exact construction layer over a named field for candidate structures, the
    fixed-angle LP for squeeze measurement, and the promote or interval pipeline for
    certification; Arslanov's own delta((4,8), 26) primitive is the template and the
    calibration case.
  instrument_ready: false
  regime: >-
    exact or interval-certified only; a floating squeeze below the 1e-11 solver floor
    (D-021) is not a determination
  instance: {axis: n, point: 90}
  priority: 1
  cost_estimate: >-
    tier S to M; the primitive is a 20-square subproblem, far below the sizes the exact
    machinery already handles at n = 29
  prereqs: [a first-party read of the Arslanov decomposition constraints for m = 10]
  replication: true
  registered: '2026-08-31'
  notes: >-
    Registered by X-009 under BC-088. The negative is valuable: no squeezable
    (4,6)/20 primitive closes Arslanov's route at m = 10 by lemma, which is a measured
    reason the n = 90 grid stands, not an impression. The positive must carry the
    novelty basis of a first-party result and the standing rule applies: an unattended
    runner records it unresolved with needs_review, and a human makes the accept
    decision.
---
# H-049 — Do 20 Unit Squares Pack Squeezably in a 4 by 6 Rectangle?

Arslanov, Mustafin and Shangitbayev prove `s(m² − m) < m` for every `m ≥ 12` by
splitting the container into two integer rectangles and two squeezable ones, and their
scheme stops at `m = 12` only because their smallest retained primitive is
`δ((4,8), 26)`. At `m = 10` the same scheme needs `δ((4,6), 20) > 0` and nothing else.
The question is finite, small, and exactly the size of instrument this repository
already runs at `n = 29`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
