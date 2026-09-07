---
title: H-109 — one near-45 A1 proof forces both remaining A-points
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-109
  kind: hypothesis
  claim: >-
    At q=1939/500, every contained closed unit square with angle in
    [pi/4-pi/720,pi/4+pi/720], center in R=[1,q/2]x[0,1], and avoiding
    L=(1,1) and M=(q/2,1), contains both A1=(1,q-3) and A2=(q/2,q-3).
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:9', 'proof:10', 'proof:15']
  criterion:
    shape: determination
    metric: exact A1 forcing plus the complete local-reflection implication for A2
    direction: >-
      Accept a complete independently checked A1 certificate over both closed
      angle signs and the generic reflection proof that transfers it to A2.
      Reject only an independently verified square satisfying this actual domain
      and avoiding either A-point. Failed sufficient triangle margins are unresolved.
    threshold: both A-points in every declared canonical two-point avoider
  instrument: >-
    A closed A1/A3 selector on the independently implemented near-45 triangle
    producer and reader; the same 24-obligation unsplit-quartic scheme for A1,
    plus analytic reflection.
  instrument_ready: true
  regime: Fixed q, L, M, A1, A2, canonical region and angle neighborhood; no point movement or angle narrowing.
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: Parallel 15-minute selector adaptations, independent 10-minute reviews, then separately frozen 10-second producer and 10-second reader.
  prereqs: [source-free cross-clause and reflection controls, independent review, committed prospective experiment]
  replication: false
  registered: '2026-09-07'
---
# H-109 — A1 and A2 by One Certificate

This strengthens the A1/A2 clauses needed under
[H-036](H-036-robust-restricted-orientation.md): every P10 avoider avoids L and M. The
converse is not assumed.
It reuses the generic triangle reduction from
[H-108](H-108-near45-canonical-a3-forcing.md), not the truth of A3 forcing.
At the fixed side `q=1939/500`, the points are `A1=(1,439/500)` and
`A2=(1939/1000,439/500)`. Avoiding only L and M is the weaker antecedent; proving the
implication from that antecedent gives the stronger theorem.

## Why One A1 Proof Suffices

Set `k=1+q/2` and reflect by `Phi(x,y)=(k-x,y)`. Use the same canonical region
`R=[1,q/2]x[0,1]` and angle neighborhood `[pi/4-pi/720,pi/4+pi/720]` as H-108. Write
`C=cos(theta)`, `S=sin(theta)`, `h=(C+S)/2` and `t=tan((theta-pi/4)/2)`. The reflected
square can be represented with angle `theta'=pi/2-theta`. Thus `C'=S`, `S'=C`, `h'=h`
and the half-angle offset satisfies `t'=-t`. This reflection preserves the canonical
region and exchanges L with M and A1 with A2. It also preserves containment for
canonical centers: `h<1` and `q>2` imply `[1,q/2]` is contained in `[h,q-h]`; vertical
containment is unchanged.
Closed membership and strict avoidance are preserved by reflection.

Suppose the stronger implication from avoiding L and M to containing A1 has been proved
throughout both angle signs.
Apply it to the reflected square.
Reflecting its A1 hit back gives A2 in the original square, while the original
implication already gives A1 there.
Phi is not a global symmetry of the container, and P10 invariance is not assumed.
Transferring a statement with only a P10-avoidance antecedent would require a different
proof.

The formal triangle itself transforms exactly.
In the square-frame coordinates defined in H-108, `(U',V')=(Sk+V,U-Ck)`, the upper
bounds transform as `u*'=Sk+v*` and `v*'=u*-Ck`, and `S'U'+C'V'=SU+CV`. Hence Phi maps
the complete closed set K onto the reflected K, maps E to the corresponding E vertex,
and exchanges F and G. The U/V margin pairs and the two closed slabs exchange as well.
Checking one A1 certificate therefore suffices; no second A2 target or certificate is
needed.

## Instrument and Scope

The instrument preserves the existing A3 command and packet identity.
The new closed A1 selector has a distinct packet kind and exact point, with the same
side, slabs, E/F/G inventory and 24 unsplit obligations.
Neither implementation accepts arbitrary target coordinates from its CLI. The producer
and reader retain their separate polynomial and Bernstein calculations.
Source-free tests reject cross-clause packets and check the toy reflection and
polynomial covariance without evaluating either scientific target.

Independent review cleared the instrument at 03:47:14 UTC on 2026-09-07, with 19
producer controls and 22 reader controls.
Both exact kernels remain unchanged; the reviewed source is
`57ad0deaa0fb9f57ccec7b606171de0507422c82`. That review established instrument
readiness, not the A1/A2 claim; no target had run at that point.

No A1 target had run at registration.
A failed formal-vertex proof, an exhausted cap or an incomplete receipt leaves the claim
unresolved; the sufficient triangle may be larger than the actual center domain.
The initial profile permits no subdivision increase, changed point, narrower angle or
retry. Even success leaves localization and both twelve-point clauses open, so it does
not prove H-036 or a global packing bound.

## Outcome

[Exp-120](../series/series-000-smoke-and-calibration/experiments/exp-120-h-109-near45-a1-a2-forcing.md)
accepted H-109 on 2026-09-07. The sole producer and independent reader proved all 24 A1
inequalities on the two closed angle signs with actual exit zero.
The reflection argument above transfers that complete implication to A2 without another
target run. Combined process cost was 0.26 seconds wall and 0.21 CPU. Localization,
twelve-point coverage, H-036 and the global packing bound remain unproved by this
result.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
