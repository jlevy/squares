---
title: H-136 — fixed corner geometry improves a matched finite covering margin
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-136
  kind: hypothesis
  claim: On the declared 19-by-19 site grid and nine retained directions at side 96/25,
    the converged numerical covering objective for cores avoiding four fixed flush corner
    unit squares is more than 4.001 below the matched unrestricted objective.
  lane: proof
  derived_from: []
  criterion:
    shape: determination
    metric: numerical M_global minus M_residual minus 4, with both arms converged
    direction: greater than 0.001
    threshold: 0.001
  instrument: packing/devtools/run_residual_cover_pilot.py; exact geometry controls and
    publication precede the numerical target in exp-135.
  instrument_ready: true
  regime: Container 96/25, core side 9977/10000; a 19-by-19 grid spanning coordinates
    1/2 to 167/50, 361 sites in 55 D4 orbits; retained 181-direction net indices
    0,23,45,68,90,113,135,158,180. One numerical row-generation run per arm on identical
    support, with 120-second cooperative deadlines, sixty rounds and four rows per direction.
  instance:
    axis: n
    point: 11
  priority: 1
  cost_estimate: Two sequential 120-second arms in one process, with a five-minute external
    timeout and two-second TERM grace. No tuning or second site grid in this round.
  prereqs:
  - independent six-piece domain review and focused instrument controls
  - prospective exp-135 and frozen instrument source before either target arm
  replication: false
  registered: '2026-09-09'
  notes: This is a finite-direction, finite-support numerical mechanism screen. Acceptance
    is not an exact optimum-gap theorem or a conditional packing certificate. A converged
    score at most 0.001 rejects only this stated numerical claim. Failure to converge,
    a guard refusal, timeout or execution error remains unresolved. Four fixed poses
    are not a universal normalization of eleven-square packings.
---
# H-136 — Fixed-Corner Residual Cover

The owner’s first pilot asks whether geometry can do more than account for four already
placed squares.
Both the covering objective and the contradiction threshold decrease when
four physical squares are fixed.
The relevant paired score is therefore `M_global − M_residual − 4`, not the raw decrease
in covering mass.

The sites and directions are deliberately small and fixed before the numerical run.
No score from a different site set, core size or direction family is the control.
Numerical discovery precedes any rational covering verification; a rationalized output
by itself is not a certificate.

The separate generalization uses proved corner-mark owners and exhaustive pose classes.
Its guaranteed occupied triangles are smaller than the fixed unit obstacles, so this
pilot cannot predict its gain or exclude its untested branches.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
