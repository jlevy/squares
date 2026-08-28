---
title: H-032 — what are the exact small-n optimal configuration spaces?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-032
  kind: open_question
  claim: >-
    What are the connected components, dimensions, active strata, and symmetry
    stabilizers of the optimal configuration spaces F_n(s(n)) modulo D4 and square
    relabelling for n = 3, 4, 5, and 6?
  lane: proof
  derived_from: [X-002]
  strategy_refs: ['proof:10', 'proof:11', 'proof:15', 'proof:27']
  instrument: >-
    Begin with an exhaustive analytic classification of the physical n = 3 side-2
    space, including arbitrary orientations modulo each square's quarter-turn
    redundancy, then compute the labelled and D4 x S_n quotients. Continue one n at a
    time with active-cell enumeration, certified continuation, interval exclusion, and
    semialgebraic decomposition.
  instrument_ready: false
  regime: >-
    proved optimal side for each n; physical square orientations modulo pi/2; labelled
    space, S_n quotient, and D4 x S_n quotient declared separately
  instance: {axis: n, point: 3}
  sweep: {axis: n, points: [3, 4, 5, 6]}
  priority: 1
  cost_estimate: tier S analytic n = 3 control; agent-days for the first complete higher-n case
  prereqs: []
  replication: true
  registered: '2026-08-24'
  notes: >-
    A sampled endpoint census cannot determine this. Exhaustiveness, including the
    exclusion of additional rotated configurations, is part of every classification.
    The n = 3 solution is also the acceptance test for every family, stratum, quotient,
    and merge visualization. An experiment fills only its declared n cell and cannot
    answer the four-cell open question by itself.
    Literature routing: [Alpert et al. 2023] and [Alvarado-Garduño–González 2025] are
    archived as topology and unlabelled-space context; [Plakhta 2021] is tracked as
    publisher-access-blocked. None answers this exact optimal-moduli question.
    Filled cells: exp-014 proves that F_3(2) is two labelled circles, with S3 quotient
    a circle and D4 x S3 quotient an interval; exp-015 proves that F_4(2) is 24 labelled
    points and both symmetry quotients are one point. Instrument readiness remains false
    for the unfilled n = 5 and n = 6 cells.
---
# H-032 — topology begins on a case whose answer is known

The question deliberately asks for the optimal set, not every local optimum.
Exp-014 and exp-015 solve the first two sweep cells exactly.
The next step is the full labelled component relation at `n = 5`, not a denser endpoint
sample.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
