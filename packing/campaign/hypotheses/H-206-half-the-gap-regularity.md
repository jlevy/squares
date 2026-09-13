---
title: H-206 — the blind physics closes a constant fraction of the record-to-grid gap
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-206
  kind: hypothesis
  claim: >-
    The workbench's blind physics closes a fraction of the gap between the best known side
    and the trivial grid ceil(sqrt(n)) that is roughly constant in n, near one half, rather
    than performing better at some n than at others. What looks like difficulty varying with
    n is the gap varying with n.
  lane: search
  derived_from: [X-028]
  criterion:
    shape: conditions
    metric: closed, the fraction of the record-to-grid gap a run closes
    direction: the median is flat in n, within a band narrower than the spread of the gaps
    threshold: the range of medians across n is under 0.4 while the gaps range over a factor of ten
  instrument: packing/devtools/bench_annealing.py
  instrument_ready: true
  regime: >-
    the workbench's own simulation at its shipped beat and force law, one headless Chromium
    on one laptop; says nothing about the campaign's Rust engine
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [5, 10, 11, 17, 26, 29]}
  priority: 2
  cost_estimate: seconds per thousand trials
  registered: '2026-09-12'
---
# H-206 — the blind physics closes a constant fraction of the record-to-grid gap

Raw excess cannot be compared across n: at n = 29 the grid is 1.1% above the record and
at n = 5 it is 10.8%, so the same excess means opposite things.
Normalised, the six n measured in X-028 fall between 0.33 and 0.70 with a median of 0.47
— a far narrower band than the tenfold range of the gaps themselves.

**What would refute it.** An n whose median `closed` sits outside that band by more than
the trial spread, with the gap accounted for.
The sweep points here are the six already measured; the claim is worth extending to n
where the gap is unusually large or small.

**Why it matters more than it looks.** If difficulty is a property of the gap rather
than of the arrangement, then the method has no structural blind spot to fix, and the
effort belongs in the tail rather than in the schedule.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
