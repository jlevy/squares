---
title: H-155 — threshold atoms cover an owner class's residual domain where point atoms do not
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-155
  kind: hypothesis
  claim: >-
    For at least one four-owner class of PR 137's sixteen-per-corner structure at
    q = 96/25 whose residual point cover, on a declared finite site set with the rows
    complete, has value at least seven, a conditional threshold certificate exists: a
    D4-symmetric family of point and threshold atoms charging every admissible core that
    avoids the class's guaranteed occupied union at least one, with total budget below
    seven, decided from its frozen bytes by both routes of the threshold gate restricted
    to the strict residual domain.
  lane: proof
  derived_from: [X-024]
  strategy_refs: ['proof:22', 'proof:23']
  criterion:
    shape: determination
    metric: >-
      the total budget of a frozen conditional threshold certificate on one owner class
      at (96/25, 9977/10000, 361 directions), against the rows-complete value of the
      point cover on the same site set and residual domain
    direction: >-
      Confirm with a frozen conditional threshold certificate of budget below seven on a
      class whose point cover on the same sites is at least seven with rows complete,
      accepted by both routes on the residual domain. A negative for one declared
      candidate class needs an exact depth-one
      family of residual cores of weight at least seven that is feasible for every
      rank-one threshold atom on its residual domain, decided exactly. Refuting this
      existential hypothesis requires such exclusions for all qualifying classes or
      another complete argument; one class-specific obstruction is insufficient. A class whose
      point cover is already below seven decides nothing about this claim, and a
      numerical LP value decides neither direction.
    threshold: 7
  instrument: >-
    sqpack.fractional.threshold and sqpack.fractional.threshold_interval decide
    threshold certificates on the full centre domain; PR 137's devtools.owner_footprints
    and devtools.multi_owner_domains produce the strict residual domain of a class as
    polygons per direction; joining them, a forbidden region and a budget threshold in
    one certificate format with one two-route gate, is the instrument this claim needs
    and is X-024's efficiency slice E1.
  instrument_ready: false
  regime: >-
    n = 11, side 96/25, shrink 9977/10000, the 361-direction doubled net, one four-owner
    class with its guaranteed occupied union; rank-one atoms, nonnegative weights
  instance: {axis: n, point: 11}
  priority: 3
  cost_estimate: >-
    one session to join the domain restriction to the gate with controls; then one
    bounded loop of about an hour per class on three cores
  prereqs:
  - the unified certificate format and gate (X-024 slice E1)
  - a declared uncovered class from PR 137's covered/uncovered ledger, with its rows-complete point value
  replication: true
  registered: '2026-09-09'
  notes: >-
    REVIEW CORRECTION 2026-09-10 (PR139 R2-R3): the hypothesis remains live and unrun.
    The previous no-reach and sixteenfold-cost rationale is withdrawn. Lane X1's
    retained depth-one family obstructs point covers of the screened endpoint-patch
    relaxations: named neutral selections leave weight 11-m against the requirement
    below 11-m. This is a statement about that family and those patches, not a theorem
    that all owner-based point proofs fail. Global exclusion needs, for every
    hypothetical physical packing, some valid excluded owner selection; overlapping
    raw labels need not all be excluded separately. The survivor violates two-of-three
    inequalities, so it is not an obstruction to this threshold hypothesis. Matching
    two cut maxima does not identify the optimization problems or their cost.
    The unconditional B-core cap near 3.868983 has no established transfer to this
    owner-conditioned model without its own marked owners, class memberships, patches
    and routing verification. Changed wall-aware footprints, unit-parent restrictions,
    richer charges and selection routing remain open. H157 is one proposed refinement
    screen, not the only possible exception. Priority3 remains an administrative queue
    position, not evidence of comparative productivity; allocation awaits a declared
    comparison. Neither the confirmation criterion nor a complete refutation criterion
    was met. The original claim is preserved. The negative criterion is clarified before any
    target run: one-class obstruction is not a refutation over all qualifying classes.
---
# H-155 — Threshold Atoms Where Five Dots Are Not Enough

PR 137’s five-dot certificate excludes one four-owner class at `96/25` because four
guaranteed occupied patches leave a residual domain that five points pierce.
A sufficient global completion would exclude all remaining classes; more generally,
every hypothetical packing needs at least one excluded valid selection.
The feasibility of such routing is unknown.
A depth-one residual family of mass at least seven obstructs a point cover below seven
on its declared residual domain.
[X-024](../explorations/X-024-two-lines-at-eleven.md) reads that test as the same
integrality gap the unconditional line crossed at `191/50`, and this claim is the
discriminator: on a class whose point cover is stuck at seven or above, do threshold
atoms bring the budget below seven?

The instrument is a join, not a new theorem.
The threshold theorem’s counting argument is unchanged when the admissible cores are
restricted to those avoiding a fixed closed set, since the residual cores of an actual
packing avoid the occupied union by PR 137’s transfer argument, and the sweep decides
Condition 5' on whatever centre domain it is given.

## Current Disposition: Live, Unrun, and Awaiting a Scoped Comparison

**Corrected September 10, 2026, after
[PR139 review R2–R3](https://github.com/jlevy/squares/pull/139#pullrequestreview-5162420994).**
The September 9 decision against this hypothesis relied on deductions that the
measurements did not establish.
Its claims of equal reach and sixteenfold cost are withdrawn.
The original hypothesis is preserved.
Its negative criterion is clarified before any target run: refuting one class does not
refute the existential claim.

[Lane X1](../series/series-000-smoke-and-calibration/results/agenda-034/lane-x1-corner-conditioning-is-mass-neutral.md)
provides an exact point-cover obstruction on particular endpoint-patch relaxations.
The retained family leaves mass ten for the named single-owner classes; the stated
combinations with disjoint deleted sets leave mass `11-m`. This prevents a point cover
below the required budget on those domains.
It does not prove that every physical packing must use one of those selections, or that
a stronger domain has the same obstruction.

The survivor has a two-of-three violation `5/4` against budget one and a heaviest
rank-one clique of weight `11/8` with fractional piercing number `5/3`. These match
named readings of its source family.
They do not identify all cuts or establish equality of the two covering optimization
problems. In particular, the survivor is not feasible for the threshold relaxation and
does not meet this hypothesis’s refutation criterion.

The cap argument from eleven disjoint B-cores near `3.868983` concerns its unconditional
core domain. Transfer to the corner-owner domain would need separate verification of
owners, classes, occupied patches and any further restrictions at that same side.
The physical ownership theorem at `96/25` cannot supply those missing premises.

A global owner argument needs an excluded valid selection for every hypothetical
physical packing; it need not exclude every overlapping raw label independently.
Routing, joint compatibility, wall-aware footprints, unit-parent restrictions and richer
charges are therefore distinct open possibilities.
[H-157](H-157-refined-owner-sector-patch-breaks-neutrality.md) proposes one patch
refinement screen; no statement here proves that it will gain area or improve a cover.

Priority 3 is retained as the queue’s existing administrative position.
It does not measure the productivity of this route relative to unconditional work.
The next allocation should declare a target class and domain, a baseline, a stopping
criterion and an explicit cost estimate.
No target was run during this correction.
See the corrected
[inference ladder](../explorations/X-026-what-conditioning-does-and-does-not-buy.md) for
the complete premises and selection quantifiers.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
