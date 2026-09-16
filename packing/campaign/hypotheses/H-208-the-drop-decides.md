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
  derived_from: [X-034]
  criterion:
    shape: conditions
    metric: the spread of median `closed` across a start sweep against across a schedule sweep
    direction: the start sweep's spread is the larger
    threshold: at least twice the schedule sweep's spread at the same n
  instrument: packages/workbench/tools/workbench_tools/benchmark.py --sweep inflate=... anneal=...
  instrument_ready: false
  regime: the workbench's simulation; the drop is its coarse-grid emptiest-cell rule
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [5, 10, 11, 17, 26, 29]}
  priority: 1
  cost_estimate: one grid, minutes
  registered: '2026-09-12'
---
# H-208 — the initial drop decides the answer, not the annealing

**Identity.** Derived from X-034, which was X-028 until 2026-09-13 and X-029 until
2026-09-14.

If the answer is settled at the drop, the schedule is decoration and the effort belongs
in the proposal: more candidate drops, a finer grid, best-of-k over placements rather
than over shakes.

**No valid measurement bears on it yet.** The only sweep that varied the start, through
the container inflation, ran before runs were checked to be packings, and its results
are void.

**What would refute it.** A schedule sweep whose spread matches or exceeds the start
sweep’s at the same n, over a grid wide enough that neither is being sampled more
finely.

**The confound to control.** `inflate` is not only the drop: a larger container also
changes what the contraction has to do.
A clean test needs a start that varies with the container held fixed, which the page
cannot do today — so this may end `blocked` rather than measured.

**No instrument can run the test yet.** The harness varies the start only through the
inflation. The test needs an instrument that takes the drop as a parameter, such as a
seeded choice among candidate cells at a fixed container, and records the drop each
trial used.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
