---
title: H-208 — the initial drop decides the answer, not the annealing
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-208
  kind: hypothesis
  claim: >-
    Where a blind run ends is decided by where the new square is dropped and how much the
    container is inflated, not by the annealing that follows. Varying the start produces a
    wider spread of `closed` than varying the schedule does.
  lane: search
  derived_from: [X-028]
  criterion:
    shape: conditions
    metric: the spread of median `closed` across a start sweep against across a schedule sweep
    direction: the start sweep's spread is the larger
    threshold: at least twice the schedule sweep's spread at the same n
  instrument: packing/devtools/bench_annealing.py --sweep inflate=... anneal=...
  instrument_ready: true
  regime: the workbench's simulation; the drop is its coarse-grid emptiest-cell rule
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [5, 10, 11, 17, 26, 29]}
  priority: 1
  cost_estimate: one grid, minutes
  registered: '2026-09-12'
---
# H-208 — the initial drop decides the answer, not the annealing

If the answer is settled at the drop, the schedule is decoration and the effort belongs
in the proposal: more candidate drops, a finer grid, best-of-k over placements rather
than over shakes.

The first evidence is suggestive rather than decisive.
Varying `inflate` between 1.12 and 1.4 moved n = 11’s median `closed` from 0.712 to
0.544 — a swing of 0.17 — while the whole shake dial from 0 to 10 moved it from 0.712 to
0.539, a swing of 0.17 in the same direction.
Equal, on that one cell, which is not what the claim predicts.

**What would refute it.** A schedule sweep whose spread matches or exceeds the start
sweep’s at the same n, over a grid wide enough that neither is being sampled more
finely.

**The confound to control.** `inflate` is not only the drop: a larger container also
changes what the contraction has to do.
A clean test needs a start that varies with the container held fixed, which the page
cannot do today — so this may end `blocked` rather than measured.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
