---
title: H-245 — the least side along the six-axis plus five-common-angle family, as a function of the tilt
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-245
  kind: open_question
  claim: >-
    What is the least side f(theta) of packings of eleven unit squares with six
    axis-parallel and five at one common tilt theta, sampled at 200 tilts in
    (0 degrees, 45 degrees], and on which tilt window is f(theta) - U below 0.01?
  lane: proof
  derived_from: [X-046]
  criterion:
    shape: record
    metric: >-
      At each of 200 tilts in (0, 45] degrees, the least verified side over 100 jolted
      starts of a frozen-angle census, with the exact-witness side of the best packing,
      and the tilt window where f(theta) - U < 0.01
    direction: >-
      A pricing measurement for H-246 and BC-384; it moves no bound, since a census
      value is an upper bound on f at one tilt and never a lower one. A narrow window
      around Trump's tilt favours per-box closers such as H-246 away from it; a wide or
      scattered window favours parametric-in-tilt certificates.
    threshold: 0.01
  instrument: >-
    A frozen-angle variant of the exp-228 census (devtools.run_basin_hopping with
    sqpack.research.quench, the angle step skipped), with sqpack.verify on every
    reported packing; to be built under BC-388
  instrument_ready: false
  regime: >-
    n=11; six squares at orientation 0, five at one common frozen tilt; float quench
    with exact verification of every reported packing; 200 tilts by 100 starts
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: About two hours of Opus high build, then one night on seven workers
  prereqs: [think-91yk]
  replication: false
  registered: '2026-09-25'
  notes: >-
    The unrun half of H-239 for the one-parameter family, from the Session 159 n11
    assessment (docs/project/specs/active/plan-2026-09-25-after-r052-planning.md).
    Values already known from exp-228: f(41.56 degrees) <= 3.8867 and
    f(45 degrees) <= 3.8856, against U = 3.877084.
---
# H-245: The Side Profile Along the Rung-1 Family

Rung 1 of the settlement ladder is the family of six axis-parallel squares and five at
one common tilt. Nobody has measured how the least side in that family varies with the
tilt, and that curve decides where a certificate has to work hard.
Where $f(\theta)$ sits well above $U$ a coarse bound suffices; where it comes within
$0.01$ of $U$ the bound must be sharp.

The census is a measurement and moves no bound.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
