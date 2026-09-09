---
title: H-146 — threshold atoms cover an owner class's residual domain where point atoms do not
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-146
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
      accepted by both routes on the residual domain. Refute with an exact depth-one
      family of residual cores of weight at least seven that is feasible for every
      rank-one threshold atom on the residual domain, decided exactly. A class whose
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
    DISPOSITIONED 2026-09-09 against agenda-033 lane X1
    (results/agenda-033/lane-x1-corner-conditioning-is-mass-neutral.md). The claim is NOT
    refuted; its premise is. Lane X1 transported the mass-eleven ceiling family to 96/25
    by PR 137's own transport and screened it with PR 137's own filter: the family
    carries weight exactly 1 at each corner mark, the four corner deletions are pairwise
    disjoint, and conditioning on m corners therefore leaves survivor weight exactly
    11 - m against a threshold of 11 - m. Four of the sixteen single-corner classes sit
    at exactly the threshold, identically at 191/50, 153/40, 383/100 and 96/25. So
    conditioning buys nothing: the gain of a conditioning is only the patch's reach
    beyond the mark, and for those classes that reach is exactly zero.
    Two things follow and both are closed. THE POINT-COVER ROUTE ON A RESIDUAL DOMAIN IS
    CLOSED - by weak duality no nonnegative point cover of those classes has mass below
    10, and a conditional certificate needs budget strictly below 10. And the rank-one
    bracket transfers verbatim to the conditional method at every m, since deleting the m
    owners of a packing at side 3.868983 leaves n - m pairwise disjoint admissible cores
    disjoint from the patches, so conditioning changes neither end of [3.82, 3.868983].
    What survives is exactly this claim, and only as a question rather than as a
    promising route. The survivor family is a fractional packing, so threshold atoms
    could still cut it and no depth-one residual family satisfying every rank-one
    threshold atom at mass seven has been exhibited; the refutation criterion is unmet.
    But lane X1 also ran the plateau reader on the 80-placement mass-10 survivor family
    of class m1:j3 and read depth exactly 1, two-of-three maximum 5/4, heaviest rank-one
    clique 11/8 at tau* = 5/3, and violated floor atoms at t = 2, 3, 4 - the same values
    the full ceiling family carries. Conditioning removed exactly one unit of mass and
    exactly none of the cut structure, so the conditional threshold problem at a class is
    the unconditional one shifted down by one, with sixteen times the work and no better
    reach. The conditional programme also has no side but 96/25 - no ownership theorem
    exists in the tree anywhere else (lane X2) - while 191/50 is already closed
    unconditionally by T-025, so its whole open window was (3.82, 3.84].
    PRIORITY LOWERED TO 3 AND DO NOT FUND IT. Retained rather than deleted because the
    claim is still falsifiable and its instrument (X-024 slice E1, the unified
    certificate format) is worth building for the unconditional lane regardless - lane A4
    found that the plateau reader separates K5 and K6 atoms that no ThresholdAtom can
    express, which is the live blocker on turning separation work into a bound.
    Superseded original note: PR 137's decisive stopping test for a class is an exact
    feasible fractional residual-core family of mass at least seven with depth at most
    one everywhere; that is the weak-duality ceiling this branch proved at 191/50 for the
    unconditional problem, where a family of mass exactly eleven stops every point cover
    and the two-of-three atoms cut it by 1/4. The one class PR 137 certified needed only
    five dots, so the conditional tree may be easy where owner patches are large; this
    claim is about the classes where it is not, and it is the measurement that decides
    whether threshold atoms make the conditional route feasible or leave the
    unconditional route as the only fractional way to 3.84.
---
# H-146 — Threshold Atoms Where Five Dots Are Not Enough

PR 137’s five-dot certificate excludes one four-owner class at `96/25` because four
guaranteed occupied patches leave a residual domain that five points pierce.
Its own analysis says the missing global step is coverage of every other class, that the
feasibility of exhausting them is unknown, and that the test which would close a class
against every point cover is a depth-one residual family of mass at least seven.
[X-024](../explorations/X-024-two-lines-at-eleven.md) reads that test as the same
integrality gap the unconditional line crossed at `191/50`, and this claim is the
discriminator: on a class whose point cover is stuck at seven or above, do threshold
atoms bring the budget below seven?

The instrument is a join, not a new theorem.
The threshold theorem’s counting argument is unchanged when the admissible cores are
restricted to those avoiding a fixed closed set, since the residual cores of an actual
packing avoid the occupied union by PR 137’s transfer argument, and the sweep decides
Condition 5' on whatever centre domain it is given.

## Dispositioned 2026-09-09: the premise is refuted, the claim is not

**Do not fund this.** The reading above — that conditioning lowers the bar and that the
question is whether threshold atoms clear the lowered bar — rests on a premise that has
since been measured and is false.
[Lane X1](../series/series-000-smoke-and-calibration/results/agenda-033/lane-x1-corner-conditioning-is-mass-neutral.md)
transported the mass-eleven ceiling family at `191/50` to `96/25` by PR 137’s own
transport and screened it with PR 137’s own filter.
The family carries weight **exactly 1** at each corner mark, and the four corner
deletions are pairwise **disjoint**, because the cross-corner distance `1.8545` exceeds
the core diameter `B sqrt 2 = 1.4109`. Conditioning on `m` corners therefore leaves
survivor weight exactly `11 - m` against a threshold of `11 - m` — one corner 10 against
10, four corners 7 against 7 — and four of the sixteen single-corner classes sit at
exactly the threshold at every side tested.
**Conditioning does not buy mass.
It gives up one unit of threshold and takes back one unit of ceiling.**

Two things are closed by that, and they are what this entry now records.
**The point-cover route on a residual domain is closed**: by weak duality no nonnegative
point cover of classes `m1:j3`, `m1:j4`, `m2:j3` or `m2:j4` has mass below 10, while a
conditional certificate needs budget strictly below 10, so no point cover can ever close
them. And the rank-one bracket transfers verbatim: at any side where eleven
pairwise-disjoint admissible cores exist, deleting the `m` owners leaves `n - m`
disjoint admissible cores that avoid the patches, so the conditional rank-one method is
capped at the same `3.868983` for every `m`, and conditioning changes neither end of
`[3.82, 3.868983]`.

**What this claim still asks is open, and that is why it is retained rather than
deleted.** The survivor family is a fractional packing, not a threshold-feasible one, so
threshold atoms could still cut it; no depth-one residual family of mass seven feasible
for every rank-one threshold atom has been exhibited, so the refutation criterion above
is unmet and the claim stands as stated.
What has changed is that it is no longer promising.
Lane X1 ran the plateau reader on the 80-placement mass-10 survivor family of class
`m1:j3` and read depth exactly 1, two-of-three maximum `5/4`, heaviest rank-one clique
`11/8` at `tau* = 5/3`, and violated floor atoms at `t = 2, 3, 4` — the *same* values
the full ceiling family carries.
Conditioning removed exactly one unit of mass and exactly none of the cut structure, so
the conditional threshold problem at a class is the unconditional one shifted down by
one, at sixteen times the work and with no better reach.
The conditional line also has no side but `96/25`, since no ownership theorem exists
anywhere else in the tree
([lane X2](../series/series-000-smoke-and-calibration/results/agenda-033/lane-x2-owner-instrument-survey.md)
§3), while `191/50` is already closed unconditionally by `T-025`.

The instrument is still worth building, for the other lane.
[Lane A4](../series/series-000-smoke-and-calibration/results/agenda-033/lane-a4-separating-the-plateau-dual-at-153-40.md)
found that the plateau reader separates `K5` clique atoms with multiplicities and `K6`
floor atoms charging more than one per core, neither of which a `ThresholdAtom` can
express — so nothing the reader separates beyond two-of-three can be frozen or gated
today. That is X-024 slice E1’s real motivation now, and it is unconditional.

## The instrument, as originally scoped

What has to be built is the domain: PR 137’s polygons per direction, handed to this
branch’s sweep and interval route, with controls that refuse a domain that is not the
strict residual one.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
