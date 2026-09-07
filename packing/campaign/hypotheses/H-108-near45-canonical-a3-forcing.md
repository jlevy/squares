---
title: H-108 — a canonical near-45 avoider contains A3
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-108
  kind: hypothesis
  claim: >-
    At q=1939/500, every contained closed unit square whose angle lies in
    [pi/4-pi/720,pi/4+pi/720], whose center lies in R=[1,q/2]x[0,1], and which
    avoids the unchanged P10 source-formula points contains A3=(3/2,13/10).
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:9', 'proof:10', 'proof:15']
  criterion:
    shape: determination
    metric: exact A3 forcing throughout the closed near-45 angle neighborhood
    direction: >-
      Accept a complete sufficient implication verified by a source-distinct
      exact reader, including the whole center domain and both angle signs.
      Reject only an independently verified square in the actual declared domain
      avoiding P10 and A3. A failed sufficient triangle assignment is unresolved.
    threshold: every declared canonical avoider contains A3
  instrument: >-
    An exact moving-triangle reduction over Q(sqrt2), an unsplit Bernstein
    producer and a source-distinct reader with independently derived quartics.
  instrument_ready: true
  regime: Unchanged q, P10, A3 and canonical region; no point movement or angle narrowing.
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: Parallel 20-minute author slices, independent 10-minute review, then separately frozen 10-second producer and 10-second reader.
  prereqs: [complete source-free controls and independent mathematical review, committed prospective experiment]
  replication: false
  registered: '2026-09-07'
---
# H-108 — Near-45 A3 Forcing

This is one clause of the restricted argument under
[H-036](H-036-robust-restricted-orientation.md) and
[H-102](H-102-complete-restricted-angle-support-families.md).
It follows the separately accepted near-axis cover in
[H-106](H-106-continuous-near-axis-ten-point-cover.md), but does not use that lemma as a
premise.
Localization into the canonical region, A1 and A2 forcing, and both twelve-point
clauses remain separate.

Here `q=1939/500`, `A3=(3/2,13/10)` and the canonical center region is
`R=[1,q/2]x[0,1]`. The angle neighborhood is `[pi/4-pi/720,pi/4+pi/720]`, and
containment means containment in `[0,q]^2`.

The unchanged point set comes from
[the source-formula implementation](../../cases/stromquist/restricted_orientation.py).
It contains the horizontal and vertical reflections of the four seeds `(1,1)`,
`(q/2,1)`, `(3/2-q/4,q/2)`, and `(1/2+q/4,q/2)`. The sufficient implication uses only
`L=(1,1)` and `M=(q/2,1)`. Avoiding these two points is a weaker antecedent than
avoiding P10, so proving that it forces A3 establishes a stronger theorem.
Avoidance of a closed square is strict; a boundary hit is not avoidance.

## Reduction to Three Moving Vertices

Write `C=cos(theta)`, `S=sin(theta)` and `h=(C+S)/2`. For this angle chart, `0<C,S<1`
and `h>1/2`. Containment puts the center `(x,y)` in `[h,q-h]^2`. Together with the
canonical region, this gives `X=x-1 in [0,W]`, `W=q/2-1 in (0,1)` and
`Y=1-y in [0,1-h]`.

Avoidance of L reduces to `CX-SY>1/2` or `SX+CY>1/2`. Avoidance of M reduces to
`C(W-X)+SY>1/2` or `S(W-X)-CY>1/2`. The other signed failures are impossible because
`X,W-X,Y` are nonnegative and `Y<1/2`. Three of the four combinations would force
respectively `CW>1`, `SW>1`, or `CX+S(W-X)-(C+S)Y>1`; each contradicts `W<1` and
`C,S<1`.

Thus, in square-frame coordinates `U=Cx+Sy`, `V=-Sx+Cy`, every square avoiding L and M
under these hypotheses has its center in the closed enlargement

$$
K_\theta=\{U\le u_*,\ V\le v_*,\ SU+CV\ge h\},\qquad
u_*=Cq/2+S-1/2,\quad v_*=C-S-1/2.
$$

For positive C and S this set is empty, a singleton, or the triangle with formal
vertices

$$
E=(u_*,v_*),\qquad
F=((h-Cv_*)/S,v_*),\qquad
G=(u_*,(h-Su_*)/C).
$$

Indeed, let `Delta=Su*+Cv*-h`. For positive Delta the barycentric coefficients at F, G
and E are respectively `S(u*-U)/Delta`, `C(v*-V)/Delta` and `(SU+CV-h)/Delta`. They are
nonnegative and sum to one.
At zero Delta the vertices coincide; at negative Delta the set is empty.
Checking all three formal vertices even in that last case is a stronger sufficient test,
not an assertion that those vertices are admissible centers.

Containment of the marked point `A=(a,b)` requires nonnegativity of the four affine
margins `1/2 +/- (Ca+Sb-U)` and `1/2 +/- (-Sa+Cb-V)`. Nonnegativity at all three
vertices therefore covers the whole closed triangle, including its boundary.

## Exact Angle Certificate and Its Limits

Put `t=tan((theta-pi/4)/2)` and use both closed slabs `[-T,0]` and `[0,T]`, with
`T=110880/50803079`. The
[angle design](../series/series-000-smoke-and-calibration/results/agenda-026/bc-255-angle-instrument-design.md)
proves that T exceeds `tan(pi/1440)`. Let `D=1+t*t`, `c=(sqrt(2)/2)(1-2t-t*t)` and
`s=(sqrt(2)/2)(1+2t-t*t)`, so `C=c/D` and `S=s/D`. Since `T<1/3`, both quadratic factors
exceed `2/9`; D, cD and sD are positive.
Clearing these denominators turns each margin into a polynomial of degree at most four
over `Q(sqrt(2))`.

The first profile has 24 obligations: three vertices, four margins and two closed slabs,
including duplicates.
It uses unsplit Bernstein coefficients.
A separate reader must reconstruct its own chart, vertex margins, polynomial arithmetic
and sign test. Shared exact field arithmetic remains an explicit common dependency.
Source-free controls check identities, denominator signs, the empty/singleton/full
triangle cases, genuine negative margins and complete packet admission.
The earlier full-P10 source result is not a known-positive control for this stronger
implication, whose two-point antecedent is weaker.

No target had run at registration.
A failed formal vertex or Bernstein test leaves the claim unresolved; it is not
necessarily an avoider in the declared geometric domain.
No subdivision increase, altered point or narrower interval is authorized by failure.
Even success proves only A3 forcing, not H-036 or a global packing bound.

## Outcome

[Exp-119](../series/series-000-smoke-and-calibration/experiments/exp-119-h-108-near45-a3-forcing.md)
accepted this clause on 2026-09-07. Both the producer and source-distinct reader proved
all 24 closed-slab obligations with actual exit zero and no unresolved entries.
The generic triangle implication supplies complete center coverage.
Localization, A1/A2 forcing and twelve-point coverage are not inferred from this result.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
