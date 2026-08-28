---
title: H-046 — is Trump's record connected to its aligned predecessor by class-angle continuation?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-046
  kind: hypothesis
  claim: >-
    Starting from the aligned form of Trump's chunk arrangement and increasing the
    tilted group's shared angle, the cell-refreshed fixed-angle LP value is finite at
    every step of a declared 0.01-degree sweep of [0, 41] degrees, and its minimum over
    that sweep, refined by bracketing, reaches Trump's standing side within 1e-9 without
    any chunk fission.
  lane: search
  derived_from: [X-003]
  strategy_refs: ['search:17', 'search:19']
  criterion:
    shape: conditions
    metric: >-
      count of infeasible or fission-requiring sweep steps, and the refined minimum's
      distance to the standing best
    direction: zero infeasible steps, zero fissions, and refined minimum within 1e-9
    threshold: 1e-9
  instrument: >-
    The built cell-read LP quench driven over a declared class-angle grid on one
    imported chunk arrangement, retaining the value, canonical active-cell label, and
    chunk membership at every step, with declared tolerance hysteresis and duplicate
    event suppression around degenerate boundaries.
  instrument_ready: false
  regime: >-
    numerical f64 LP under the measured 1e-11 solver floor; one imported arrangement at
    n = 11, one tilted group, declared grid resolution
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [11]}
  priority: 1
  cost_estimate: >-
    tier S; roughly 4,100 LP solves at the measured 1.28 ms per solve, seconds of wall
    time plus the sweep driver
  prereqs: [class-angle sweep driver with retained per-step cell records]
  replication: true
  registered: '2026-08-26'
  notes: >-
    This is the cheapest test of the design discussion's third intuition, that records
    are perturbations of cleaner regular predecessors. The historical record is
    suggestive rather than decisive: Friedman's DS7 states that Trump improved Gobel's
    earlier eleven-square packing, and the catalogue annotates Bidwell's n = 17 as based
    on Hamalainen's 1980 packing. Stromquist's Theorem 3 proves no 0 or 45 degree
    packing reaches Trump's side, so a continuous path from the aligned form must leave
    the restricted class somewhere; the round records where. The retained per-step cell
    identity is the actual scientific content: the count and location of cell changes
    along the path is what says whether the aligned predecessor and the record belong to
    one arrangement family or many. A negative result is equally useful and cheap. This
    is a numerical continuation record, never a component, connectivity, or tangent
    claim; D-034 and the exp-035 through exp-042 chain own that vocabulary. Review
    amendment 2026-08-26: raw solver row sets are not stable cell identities. The sweep
    instrument must canonicalize labels and boundary events before any cell-change count
    is interpreted.
---
# H-046 — the predecessor path, recorded step by step

The intuition under test is that an optimal packing is a perturbation of a cleaner,
slightly larger, more regular arrangement.
At `n = 11` the ingredients are unusually explicit: Trump’s packing is six axis-aligned
squares plus one five-square group at `a* ~ 40.181937` degrees, and its aligned form,
with that group at zero, is an ordinary arrangement inside the `4.0` grid.

The round drives the shared angle from zero to just past `a*`, solving the
cell-refreshed fixed-angle LP at every step, and retains the value, the active cell, and
the chunk membership.
Three things can happen, and all three are results:

- **The branch runs.** The value is finite at every step, no chunk needs to break, and
  bracketing at the minimum reaches Trump’s side.
  The predecessor intuition holds for the one case that matters most.
- **The branch breaks.** Some step is infeasible or requires chunk fission.
  The location of the break prices exactly which grammar move is missing, and fission
  becomes a required move rather than an optional one.
- **The branch runs to the wrong place.** The minimum is finite but short of the
  standing best, which says the arrangement family is not the one the record lives in
  and that a chunk hypothesis alone underdetermines the target.

## Why the per-step cell record is the point

The value curve alone would only re-measure
[T-3](../../../SYNOPSIS.md#the-corner-and-the-method-it-forced), whose corner at `a*` is
already confirmed by
[exp-010](../series/series-000-smoke-and-calibration/experiments/exp-010-angle-kink-n11.md).
What is new is the sequence of active cells along the path.
A path crossing few canonical cell events says this continuation used few serialized
arrangement changes and may be a cheap proposer.
It does not by itself establish metric or topological nearness in arrangement space.
A path crossing many gives direct evidence that the “slight perturbation” framing
understates this continuation’s combinatorial work.

Because the derivative jumps at `a*`, refinement at the minimum uses bracketing rather
than any gradient method; the sweep supplies the bracket and the corner is expected, not
an anomaly.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
