---
title: H-238 — no descent-stable n11 local minimum with three orientation classes below Stromquist's value
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-238
  kind: hypothesis
  claim: >-
    Every descent-stable local minimum of the n=11 problem reached by the declared
    census, with side below Stromquist's 2 + 4 sqrt 2 / 3 = 3.885618..., lies in the
    orbit of Trump's packing.
  lane: search
  derived_from: [X-046]
  criterion:
    shape: record
    metric: >-
      A census of 1,000 jolted starts from Trump's and Stromquist's packings, each
      quenched and then passed through a descent filter that rejects any endpoint with
      a verified side-decreasing feasible direction, tabulating every surviving
      minimum's side, orientation-class count and multiplicities, each verified by
      sqpack.verify
    direction: >-
      Kill with one descent-stable minimum having at least three orientation classes
      and side below 3.885618, verified feasible. Retain the census as support, never
      as proof, if none appears. The filter must first reject the six X-046 probe-C
      stalls and accept Trump's and Stromquist's packings; a filter that fails either
      control decides nothing.
    threshold: 3.885618
  instrument: >-
    devtools/run_basin_hopping.py in a census mode with a descent-filter module beside
    sqpack.research.quench
  instrument_ready: false
  regime: >-
    n=11; float quench with exact feasibility verification of reported endpoints;
    starts are jolts of scale up to 0.3 about the two known packings
  instance: {axis: n, point: 11}
  priority: 2
  cost_estimate: Three to four hours including the filter and its controls
  prereqs: [think-nbij]
  replication: false
  registered: '2026-09-23'
  notes: >-
    X-046 candidate H-e. quench_bracket reports converged=True at class-coordinate
    stationary points that are not local minima, which its docstring permits; the
    descent filter is what makes a census readable. The kill would not touch rungs 0 to
    3 of the H-112 ladder but would make the three-orientation rung mandatory.
---
# H-238: No Third-Class Minimum Below Stromquist’s Value

The strongest threat to the settlement ladder is a genuine local minimum with three or
more orientation classes close to $U$. X-046’s first census produced six apparent ones
within $U+0.005$, and all six descended monotonically to Trump when checked: they were
stalls of the class-coordinate quench, not minima.

This claim is the repaired census.
It cannot prove anything about the global problem; its value is as a cheap falsifier,
and as the measurement that fixes how sharp any profile theorem must be.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
