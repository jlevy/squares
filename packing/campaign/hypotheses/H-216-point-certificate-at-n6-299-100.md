---
title: H-216 — a helper-free point certificate at n=6, side 299/100
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-216
  kind: hypothesis
  claim: >-
    A helper-free point-atom certificate exists for n=6 at container side 299/100 with
    B = 9977/10000 on the 181-direction net, on some named site set.
  lane: proof
  derived_from: [X-037]
  strategy_refs: ['proof:22']
  criterion:
    shape: determination
    metric: >-
      The covering value of a rows-complete point-atom LP on a named site set at
      (n, L, B, net) = (6, 299/100, 9977/10000, 181 directions), against the exact
      total of a depth-one ceiling family feasible for every point atom
    direction: >-
      Confirm only with a frozen point-atom covering of value strictly below 6 on a
      named site set that both routes of decide_certificate accept. Kill, and refute
      the claim at this scope, with an exact depth-one family of total at least 6 that
      independent_ceiling_reader and verify_ceiling both accept. A float LP, a stalled
      interval route, an incomplete row set, or an attic scratch number decides neither
      direction.
    threshold: 6
  instrument: >-
    devtools.run_fractional_colgen with --freeze-family writes a dual family;
    --support-cap 0 keeps every dual row. devtools.polish_ceiling_family rebuilds the
    exact vertex. devtools.independent_ceiling_reader and
    sqpack.fractional.ceiling.verify_ceiling decide a depth-one family.
    devtools.decide_certificate is the two-route gate, with --dump-stalls available
    when the interval route stalls. The n-parameterised threshold producer
    (G4 / think-qqzs) is not this instrument. This hypothesis allocates no experiment
    id; exp-161 remains Route S.
  instrument_ready: true
  regime: >-
    n=6, side 299/100, shrink 9977/10000, 181-direction net, point atoms only,
    D4-symmetric nonnegative weights, exact rational arithmetic; helper-free means no
    segment, area, or relational atom
  instance: {axis: n, point: 6}
  priority: 1
  cost_estimate: >-
    One block of two to three hours on the stock drivers now on main: freeze and polish
    a large union, then either the exact ceiling reader or both routes of the gate
  prereqs: []
  replication: true
  registered: '2026-09-18'
  notes: >-
    X-037's attic M7 lane bracketed the covering value in [83/14 exact, 6.006571 float]
    and did not decide this claim. Those numbers are scratch, not evidence. The attic
    wrote the universal negative; this artifact is the existence claim, which can still
    be wrong. Nothing here moves s(6)=3. A later certificate at this side would be
    weaker than the proved value. G1, G2, G3, and G5 landed on main in PRs 196 and 197.
    2026-09-18 session-139 froze a covering of total 76027/12500 = 6.08216 on grids
    18/24/29 (1785 sites, 132 atoms). That covering is above 6 and does not confirm.
    Polish of the merged family then both ceiling readers agreed: exact total 76/13,
    max depth 1, K3 fails. That does not kill. A second named site set on grids
    18/24/29/34 (2941 sites, 160 atoms) froze covering 151931/25000 = 6.07724, lower
    by 123/25000 and still above 6. The claim stays open. Not an n=11 result.
---
# H-216: Point Certificate at n=6, 299/100

X-037’s M7 lane asked whether a helper-free point certificate exists at a solved case.
The attic wrote the universal negative: no such certificate at side `299/100` with
`B = 9977/10000` on the 181-step net, for any site set.
That sentence is V0/C0 scratch.
This artifact is the existence claim.

A rows-complete covering below 6 on a named site set, frozen and accepted by both routes
of `devtools.decide_certificate`, confirms it.
An exact depth-one family of total at least 6 that is feasible for every point atom
kills it: that is a statement about the language, not about one site set.
An incomplete row set, a float value, a stalled interval route, or a number that lived
only under `attic/overnight/` does neither.

The tools that write and decide those two objects are on main (G1 freeze-family, G2
orbit fold, G3 ceiling-reader inequalities, G5 site-merge and stall dump).
G4, the n-parameterised threshold producer, is a different language and a different
question. `exp-161` is reserved for Route S and is not this hypothesis’s experiment.

A decided H-216 is calibration.
It does not move `s(6) = 3`, and it is not an n=11 bound.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
