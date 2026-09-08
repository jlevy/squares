---
title: H-129 — the shrink-free fractional packing value stays below eleven up to 3.87
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-129
  kind: hypothesis
  claim: >-
    The shrink-free covering value at side 3.87, with coverage required for every
    contained unit placement and every orientation, is strictly below eleven. A finite
    direction net supplies candidate dual families; a covering result on that net alone
    does not decide the continuum claim. The 2026-09-08 correction below preserves the
    original finite-net/nonexistence wording and repairs its claimed equivalence.
  lane: proof
  derived_from: [X-021]
  strategy_refs: ['proof:9', 'proof:15']
  criterion:
    shape: determination
    metric: exact primal upper bound and independently verified finite-family dual lower bound, with the covered direction domain stated
    direction: >-
      Confirm only with an exact measure of mass below eleven covering every contained
      unit placement at every orientation at 3.87. Refute with an exactly verified finite
      closed-unit family of weight at least eleven at a side at most 3.87. A finite-net
      covering upper bound, a family below eleven, or a numerical LP optimum leaves the
      continuum claim inconclusive. Outside-neighbourhood weight at least one additionally
      defeats only the stated strict capture design, after that membership is verified.
    threshold: 11
  instrument: >-
    sqpack.fractional.ceiling for exact finite-family replay; devtools.transport_ceiling_family
    scales exp-070's retained family by 10000/9977 into a valid unit control below 96/25.
    The depth polisher, net-bound resume, and full-direction positive verifier must be
    completed before a two-sided target determination; readings are at 3.84, 3.86 and 3.87.
  instrument_ready: false
  regime: >-
    n = 11; the claim concerns all orientations. Closed unit squares at finitely many
    directions suffice for a dual lower bound, since Condition 4 is not needed for that
    geometric family; a finite-net covering upper bound has narrower scope. Sides 3.84,
    3.86 and 3.87.
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: one session of three to four hours on one core
  prereqs: [exp-070 retained family replay and exact unit transport, guarded depth polisher, full-direction positive verification]
  replication: true
  registered: '2026-09-08'
  notes: >-
    Correction 2026-09-08: the historical reading below overstates both the duality scope
    and what a low family value can decide; the corrected criterion and dated body section
    govern continuation. Exact geometric scaling of exp-070 gives a retained unit-family
    floor of 21342289572/2055263195 at 96/25. Session-100's scratch family/state is absent
    from this checkout and its embedded resume driver remaps its own net twice.
    A verified dual family obstructs its specified one-body program, while a valid
    covering measure below eleven establishes the positive direction on the domain it
    covers. Ownership and compatibility arguments remain open. Session-100's historical
    unit-family reading was 8.918 on 203 directions with diffuse angular weight and 5.93
    outside Trump's neighbourhood; it did not decide the optimum. The stronger retained
    exp-070 control replaces that missing scratch state for the depth-polisher handoff.

---
# H-129 — The Unit-Square Covering Value

The unit-square covering value measures the reach of the corresponding one-body
certificate. A verified fractional family supplies a lower bound on that value; an exact
covering measure supplies an upper bound on its declared domain.
[X-021](../explorations/X-021-what-can-be-proved-about-eleven-squares.md) records the
corrected weak-duality scope.
The particular retained-shrink obstruction below `U` disappears at `B = 1`, which
motivates measuring this value without deciding the fate of ownership or multi-square
arguments.

[Agenda 030](../agendas/agenda-030-parallel-structural-lanes-at-n11.md) measures it in
BC-294, and BC-301 waits on its first reading.

## Correction of 2026-09-08: The Criterion and the Continuation

The original claim said that no finite-net depth-one family of value at least eleven
exists, then called that equivalent to a covering value strictly below eleven.
The original criterion measured the best family found and accepted a value below eleven.
Neither implication is valid: a search supplies a lower bound, and a supremum of eleven
need not be attained by a finite family.
The corrected frontmatter states the intended continuum covering question and the
distinct evidence needed in each direction.
Session-100 remains inconclusive; its eight-point-nine reading is a historical result,
not evidence that the relaxation stays below eleven.

The
[dated lane-D correction](../series/series-000-smoke-and-calibration/results/agenda-030/lane-d-contacts-and-closing-route.md#correction-of-2026-09-08-duality-scope-cap-and-retained-continuation)
gives the corrected strict retained-net cap, the exact transport of exp-070’s stronger
family to unit squares, and the failed resume’s replacement.
A value-eleven family can defeat strict one-body and specified capture certificates; it
does not defeat ownership, geometric case splits, or strengthened programs with
compatibility and capacity cuts.
The old claim that the retained 3.82 bracket says nothing about the unit value at q is
also withdrawn: scaling by the reciprocal shrink gives the exact lower bound
`21342289572/2055263195 > 10` there.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
