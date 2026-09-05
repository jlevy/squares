---
title: H-063 — a {0°, 45°} class certificate at n = 11 certifies above Trump's side, and n₁ ≤ 1 is closed
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-063
  kind: hypothesis
  claim: >-
    Two statements, one instrument. First, the class certificate of X-014's Lemma 3 --
    per-direction-class thresholds as linear-program variables, classes as unions of the
    net's half-gap cells -- with the class taken as the two end cells of the retained
    181-direction net, around 0 and 45 degrees, refutes the composition
    (n0, n1) = (11, 0) at a rational side at or above Trump's 3.877084. Second, for every
    near-axis class contained in the tilts below theta0(s), the compositions with n1 at
    most 1 are closed at every side below Trump's, so at least two of any eleven squares
    are tilted beyond that class.
  lane: proof
  derived_from: [X-014]
  strategy_refs: ['proof:2', 'proof:9', 'proof:22']
  criterion:
    shape: conditions
    metric: >-
      the largest rational side at which the two-threshold covering program refutes
      (n0, n1) = (11, 0) for the class of the net's two end half-gap cells; and the
      optimum the same program returns for a near-axis class contained in the tilts below
      theta0(s), against nine
    direction: >-
      accepted only if both clauses hold on frozen bytes decided exactly: the two-end-cell
      class program refutes (11, 0) at a side at or above 3877084/1000000, and the
      near-axis class program at that side returns an optimum of at most nine, which
      closes n1 at most 1 by the count alone; rejected only if the two-end-cell class
      program, with its row loop converged, fails to refute (11, 0) at every rational
      side at or above 3877084/1000000 -- X-014's own kill condition, that conditioning
      on direction buys too little; a near-axis optimum above nine is an instrument
      defect, since the nine-point measure is feasible there by construction, and it
      suspends the round rather than deciding it
    threshold: 3.877084 for the class side, 9 for the near-axis optimum
  instrument: >-
    The two-threshold form of Condition 5, built in agenda-021's BC-198 on top of
    sqpack.fractional.colgen: weights w0 and w1 enter as linear-program variables
    alongside the atom weights, one normalisation row fixes the homogeneous scale, class
    membership is decided by which half-gap cell holds a direction, and the composition
    is refuted by the sign of M - n0 w0 - n1 w1. Nothing geometric changes: the admissible
    centre domain is unmoved, so sweep.centre_domain, the float mirror in generate.py and
    the four half-planes interval.DirectionSearch propagates are untouched, which is what
    separates this from Lemma 2's conditional certificate and is why it is the cheap half
    to test first. Floats propose and exact arithmetic confirms.
    Two controls, both fixed before the target run. The nine-point control: nine atoms of
    unit weight on the pitch-s/4 grid pierce every axis-parallel square of side at least
    s/4 in the container, and a B-square at tilt theta contains an axis-parallel square of
    side B / (cos theta + sin theta), so the measure is feasible for any near-axis class
    inside theta0 and the program's optimum must be at most nine. The Stromquist control:
    Theorem 3 reaches 2 + (4/3)sqrt(2) = 3.885618 for the exact two-direction class by a
    further box step -- twelve points, one more than eleven, closed by forcing a box to
    swallow three at once -- which this program does not have, so 3.877084 is the
    threshold this claim registers and 3.885618 is not.
    Retention needs the gate extended: a two-threshold object is not what
    devtools.decide_certificate reads today, and nothing is registered until w0 and w1 are
    in the frozen bytes and both routes decide on them.
  instrument_ready: false
  regime: >-
    The retained net, read from cases/n11_fractional_certificate/certificate.json:
    angle_limit 207107/500000, direction_steps 180, so 181 directions over an arc of 0 to
    45.000043 degrees, spacing 0.263696 degrees at the axis-parallel end, B = 9977/10000.
    Classes are unions of half-gap cells -- the arcs between consecutive midpoints -- and
    never unions of geometric angle ranges: a square at 4.9 degrees on this net lies in
    the cell of the direction at 5.007 degrees and contains no B-square at the direction
    below it, so a class cut at a geometric angle would count it wrongly. The two-end-cell
    class has half-width 0.131848 degrees at the axis end. At side 3877/1000 the largest
    near-axis class inside theta0 -- cos theta + sin theta = 4B/s, giving 1.706162 degrees
    -- is the first six cells, upper boundary 1.450253 degrees. Exact rational arithmetic;
    no numerical tolerance enters either decision.
  instance: {axis: n, point: 11}
  sweep:
    axis: composition n1
    points: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
  priority: 1
  cost_estimate: >-
    one 110-minute build-and-control cell (agenda-021's BC-198) and one 150-minute theorem
    cell (agenda-022's BC-208); twelve class linear programs per side at n = 11, each a
    covering program with two extra variables and one extra row
  prereqs:
  - BC-198's frozen class program with both controls passing
  - the retention gate extended to read and decide two thresholds from frozen bytes
  replication: true
  registered: '2026-09-05'
  notes: >-
    What a success is and what it is not. Stromquist's Theorem 3 already settles Gardner's
    conjecture at 2 + (4/3)sqrt(2) for the {0, 45} class; reproducing 3.877084 with a
    first-party class certificate is a mechanisation of a published restricted-orientation
    result and claims S3 at most, one method family. What it adds beyond the published
    statement is the widening: the class here is two half-gap cells rather than two exact
    angles, so it covers strictly more packings than Stromquist's does, and the widening
    rather than the number is the result worth having.
    The value is not the bound. No class certificate moves s(11) on its own, because the
    compositions the ladder needs closed are the ones near Trump's own -- five squares at
    40.181937 degrees, 0.012100 degrees from net index 159 -- and those are exactly the
    compositions a class cut cannot close. Lemma 3 prices what everyone in this subject
    knows informally, that a tilted square costs more room than an aligned one, as a dual
    variable instead of a lemma; the class ladder's use is as the coarse tier of a tree,
    and the tree is X-014's proposal and not this claim.
    The second clause is a mechanisation of a classical count and its arithmetic is worth
    keeping straight, because the shrink shifts it. For unit squares X-014's theta0
    satisfies cos theta + sin theta = 4/s, giving 1.85 degrees at Trump's side and 2.77 at
    3.82; for the B-squares this program actually constrains the condition is 4B/s, giving
    1.706162 and 2.622745. The class must be a union of cells inside the smaller of the
    two, which at 3877/1000 is the first six cells.
---
# H-063 — A Class Certificate at `n = 11`, and the Composition Count

X-014’s Lemma 3 is the cheapest of the three lemmas by a wide margin, and it is the one
that can be tested against a published answer.
Partition the net directions into `D4`-closed classes, each a union of half-gap cells;
give each class its own threshold as a linear-program variable; fix a composition
`n₀ + n₁ = 11`; and refute the composition when the total mass falls below
`n₀w₀ + n₁w₁`. The constraints are linear in `(μ, w₀, w₁)` and the objective is
homogeneous, so it is one linear program per composition, decided by the sign of its
optimum under a normalisation.

Stromquist’s Theorem 3 is that shape with one more step.
His class is `{0°, 45°}`, his strengthened Lemmas 7 and 8 are the covering condition
restricted to that class, and his twelve points — one more than eleven, so the count
alone proves nothing — are closed by forcing a box to swallow three of them at once.
His bound, `2 + (4/3)√2 ≈ 3.885618`, sits above Trump’s value, which is what settles
Gardner’s conjecture and also what shows the shape is the right one: the class that does
not contain Trump’s packing is closed above `U` by a certificate conditioned on the
class.

So the threshold registered here is Trump’s `3.877084` and not Stromquist’s `3.885618`.
The program has the covering condition and not the box step, and asking it for the
higher number would be asking it for someone else’s lemma.

The second clause needs no computer at all and is registered here because it calibrates
the composition step.
Nine points on a grid of pitch `s/4` pierce every axis-parallel square of side at least
`s/4` inside the container, because an interval of that length inside `[0, s]` contains
a multiple of `s/4` other than `0` and `s`; a `B`-square at tilt `θ` contains an
axis-parallel square of side `B / (cos θ + sin θ)`; so at most nine squares of any
packing sit inside the near-axis class, and at least two lie outside it.
Trump’s packing has five such squares, so the fact is consistent rather than sharp.
Its value is as the template: a class certificate is a covering condition restricted to
a class, and the classical unavoidable-point lemmas are the special case where the
covering is by points of weight one.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
