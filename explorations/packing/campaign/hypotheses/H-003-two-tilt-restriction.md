---
title: H-003 — restricting to two distinct tilt angles finds the basin
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-003
  kind: hypothesis
  claim: >-
    A search restricted to two distinct tilt angles - one fixed at 0, one free and shared
    by all tilted squares - reaches within 1e-4 of Trump's packing at n = 11 within the
    baseline budget, which the unrestricted search does not.
  lane: search
  derived_from: []
  strategy_refs: ['search:2', 'search:6']
  criterion:
    shape: record
    metric: best_side
    direction: lower
    threshold: 1e-4
  instrument: >-
    Not yet built: sqsearch needs an angle-class mode in which squares carry a class index
    rather than a free angle, and moves act on the shared class angle.
  instrument_ready: false
  regime: sqsearch, f64 screening
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [10, 11, 12]}
  priority: 2
  cost_estimate: 12e9 moves per cell, plus about a day of engine work
  prereqs: []
  replication: false
  registered: '2026-08-22'
  notes: >-
    Status will read blocked until the angle-class mode exists, which is correct: a
    hypothesis whose instrument does not exist is blocked, not measured badly.
---
# H-003 — buying the answer’s shape

Trump’s packing uses exactly two orientations: six squares at `0°` and five at
`≈40.1819°`. Restricting the search to that structure collapses eleven free angles to
one, which is a large reduction in a space where the angular degrees of freedom are what
make the problem hard.

## The honest caveat, which is the whole reason to write this down first

This bakes in a property of the known answer, so a win says less than it appears to.
It would show that *given* the right angular structure the positional search is easy — a
real and useful finding about where the difficulty lives — but it would not be evidence
that an unguided method could have found `n = 11`, and it must not be reported as if it
were.

The sweep matters more than usual here for exactly that reason.
If the restriction also finds `s(10)` — whose optimum genuinely does use two
orientations — and correctly fails to beat `n = 12`, the result is about two-tilt
structure in general.
If it only ever works at `n = 11`, it is about `n = 11`’s specific answer, which we
already had.
