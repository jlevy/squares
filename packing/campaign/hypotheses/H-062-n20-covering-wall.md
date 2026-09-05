---
title: H-062 — the m = 5 covering wall sits strictly below the ceiling, and four rungs bracket it
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-062
  kind: hypothesis
  claim: >-
    On the retained 181-direction net at B = 9977/10000, the side at which a converged
    restricted covering optimum at n = 20 first reaches twenty -- the covering wall of
    the ladder that T-020 left at 24/5 -- lies strictly below the method's structural
    limit 5B = 9977/2000 = 4.9885, and four rungs of a bisection schedule fixed before
    any command runs bracket that side to within 0.02.
  lane: proof
  derived_from: [X-014, X-013]
  strategy_refs: ['proof:21', 'proof:22']
  criterion:
    shape: determination
    metric: >-
      the interval between the greatest pre-registered side carrying a retained
      certificate of total mass strictly below twenty and the least pre-registered side
      at which the row loop converges to a restricted optimum at or above twenty on two
      independent site sets
    direction: >-
      accepted only if the four decided rungs leave an interval of width at most 0.02
      whose lower end carries a certificate retained through devtools.decide_certificate
      with both routes agreeing on the value, whose upper end carries a converged
      restricted optimum at or above twenty on two independently constructed site sets,
      and whose upper end is strictly below 9977/2000; rejected only by a retained
      certificate at a side of 4.98 or above -- within 0.02 of five, so within 0.0085 of
      the structural limit -- or by four decided rungs finding no converged optimum at or
      above twenty anywhere below 9977/2000, either of which says the covering value
      never binds before the ceiling does at m = 5; a rung that is time-limited, or whose
      converged optimum is an exactly round 20.000000, decides nothing and the round
      reports the bracket the remaining rungs support
    threshold: bracket width at most 0.02, upper end strictly below 9977/2000
  instrument: >-
    sqpack.fractional.colgen's column generation at each pre-registered side, with site
    sets built independently two ways -- site_set_from_grids at a density set by
    agenda-019's BC-191 rule, and a set seeded from the retained n = 20 certificate's
    2260 atoms -- and devtools.decide_certificate as the retention gate on frozen bytes,
    both routes accepting and agreeing on the value before any rung is retained.
    sqpack.fractional.certificate.ceiling_side supplies 5B. The sides are the successive
    midpoints of the live bracket over [24/5, 9977/2000], rounded to the nearest 1/200
    with ties taken away from 24/5: rung 1 at 979/200, then 247/50 or 97/20, then
    993/200, 123/25, 39/8 or 193/40, then the live midpoint by the same rule. Every leaf
    of that tree leaves a bracket of at most 0.015.
    The asymmetry the schedule exploits is a property of the program and not a
    convenience: adding rows can only raise a restricted optimum, so a rung is refuted as
    soon as its optimum crosses twenty with violated placements still outstanding, while
    a rung is confirmed only by the row loop stopping for want of a violated placement.
  instrument_ready: true
  regime: >-
    The retained net and shrink, read from the certificate files rather than recalled:
    angle_limit 207107/500000 and direction_steps 180, so 181 directions over an arc of 0
    to 45.000043 degrees with spacing 0.263696 degrees at the axis-parallel end;
    B = 9977/10000, D = 207107/90000000, B(1 + D) = 0.999996. D4-symmetric atom sets,
    exact rational arithmetic throughout, no numerical tolerance in any decision.
    The wall this claim is about is the instrument's, measured on the two declared
    site-construction rules. It is not tau*(L). Adding sites can only lower a restricted
    optimum, so a converged optimum at or above twenty is a statement about the site sets
    that produced it, and no run in this register has ever measured the unrestricted
    covering value.
  instance: {axis: n, point: 20}
  sweep:
    axis: container side
    points: ['193/40', '39/8', '97/20', '979/200', '123/25', '247/50', '993/200']
  priority: 1
  cost_estimate: >-
    180 elapsed minutes inside agenda-021's BC-197: four rungs at about 20 minutes on the
    refutation side and about 60 on the confirmation side, plus one retention gate per
    passing rung at roughly 40 s now that the exact sweep decides in integers
  prereqs:
  - the bisection schedule fixed and recorded before any target command runs
  - two independently constructed site sets per rung, since one site set cannot carry a
    wall claim
  replication: true
  registered: '2026-09-05'
  notes: >-
    Why m = 5 and not the case anyone cares about. At n = 20 and n = 21 the best known
    packing is the axis-parallel grid at 5, so every tilt offset from a net direction is
    zero, the reach table's packing cap collapses onto the ceiling, and both structural
    limits are the single number 4.9885. Nothing but the covering value can bind below
    it. Everywhere else in the register a packing record sits in the way and a failed
    rung has two explanations; here it has one.
    The estimate, written down before the run so the run can contradict it. From X-013's
    finite differences over the six reported restricted optima -- about 7.1 mass per unit
    side from 3.82 to 3.96, 8.0 to 4.58, at most 8.9 to 4.80 -- the 1.077 of mass between
    T-020's retained 946131/50000 = 18.922620 and twenty is 0.12 to 0.135 of side, so the
    wall is expected at 4.92 to 4.94. That is an extrapolation from six clustered points,
    two of them unconverged, and no rung in this register has ever been claimed from one.
    Two readings are refused in advance and both have cost this project time before. A
    converged optimum on one site set says only that no certificate exists on that site
    set. And an exactly round value is the known artefact signature in this pipeline --
    18.000000 on three site sets at 117/25, and 18.0 among n = 17's grid-31 optima -- so
    20.000000 is inconclusive rather than a wall, and the round reports it as such.
    One soundness alarm rides along at every rung above 4.885618, where Wainwright's
    n = 19 packing sits. A converged optimum below nineteen at a higher side would
    contradict a retained packing; it is a bug to chase and not a rung to bank, and every
    rung above that side must land in [19, 20).
    The same rungs read the n = 21 criterion as well: a rung's restricted optimum M
    certifies every n > M, so a rung whose M lies in [20, 21) is a certificate for
    n = 21 alone, and BC-197 runs one pre-registered rung at 997/200 = 4.985 on that
    reading first, because the same finite differences put the covering value at
    the ceiling near 20.4 to 20.7 -- an extrapolation, labelled as one -- so the
    n = 21 wall is expected above the ceiling rather than below it.
---
# H-062 — The `m = 5` Covering Wall Sits Below the Ceiling

Nobody has ever measured a covering wall.
The record holds seven reported restricted optima at seven sides, and
`CERTIFICATE-REACH.md` says of them that no covering-search run log or solver checkpoint
was retained for any, that two of the seven are explicitly unconverged, and that seven
heterogeneous reports across a side band `0.98` wide support no growth trend at all.
The closest thing to a wall in the register is two independent site sets stopping at
exactly `11.000000` at side `3.82`, and `T-018` says plainly that reading that as `τ*`
would be reading an artefact.

This claim is the first attempt to measure one deliberately, and it is made at `m = 5`
because that is where the measurement is clean.
At `n = 20` and `n = 21` the upper bound is the trivial grid, so the packing cap and the
ceiling are the same number and no packing record stands between the ladder and the
method’s structural limit.
A rung that fails there fails for one reason.

What the claim is not is a statement about the covering value of the container.
The quantity measured is the restricted optimum on two declared site-construction rules,
and adding sites can only lower it.
That distinction is the whole of why `T-018`’s `3.82` result is recorded as a
measurement rather than as a bound, and it is inherited here unchanged.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
