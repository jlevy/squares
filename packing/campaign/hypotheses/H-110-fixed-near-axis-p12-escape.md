---
title: H-110 — a fixed near-axis square escapes the unchanged twelve-point set
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-110
  kind: hypothesis
  claim: >-
    At q=1939/500 and t=1/1000, the closed unit square at angle theta=2 arctan(t)
    and the fixed strip-midpoint center defined below is contained in [0,q]^2
    and strictly avoids all twelve unchanged Stromquist P12 points.
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:9', 'proof:10', 'proof:15']
  criterion:
    shape: determination
    metric: exact validity and strict twelve-point avoidance of one frozen square
    direction: >-
      Accept only an independent exact check of actual angle membership, closed
      unit-square geometry, container inclusion and strict avoidance of all twelve
      points. Reject only when an independent exact check of the correctly
      reconstructed frozen candidate establishes that it is outside the actual
      domain or contains a mark. Bad receipts, failed sufficient guards, errors,
      timeout and incomplete checks are refused or unresolved, not rejection.
    threshold: one valid frozen candidate avoiding all twelve unchanged points
  instrument: >-
    A fixed rational candidate producer and a source-distinct corner/oriented-edge
    checker with source-free positive, negative and boundary controls. No search.
  instrument_ready: true
  regime: Fixed q, rational half-angle, center formula and source-ordered P12; no alternate candidate or point movement.
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: Parallel 15–20-minute source-free author/control slices, then 10-minute independent reviews and separately frozen short producer/reader processes.
  prereqs: [source-free instrument controls, independent mathematical review, committed prospective experiment, fresh block allocation]
  replication: false
  registered: '2026-09-07'
---
# H-110 — Test the Twelve-Point Construction First

This is the selected next BC-255 discriminator under `think-qv73`, not a Session 090
target. No candidate geometry or point-membership test was evaluated at registration.
The source formulas suggest a gap between two coverage strips.
Checking one fixed square is cheaper than building a complete continuous P12 proof that
this gap might invalidate.

## Frozen Candidate

Set `q=1939/500`, `t=1/1000` and

$$
C=\frac{1-t^2}{1+t^2},\qquad S=\frac{2t}{1+t^2},\qquad
h=\frac{C+S}{2}.
$$

Here `C=cos(theta)`, `S=sin(theta)` and `theta=2 arctan(t)`. For a marked point `(a,b)`,
write its square-frame vertical coordinate as `v(a,b)=-Sa+Cb`. Define

$$
v_A=-S+C(q-3),\quad v_G=-\frac45S+C(q-2),\quad
V_0=\frac{v_A+v_G}{2},\quad x=h,\quad y=\frac{V_0+Sh}{C}.
$$

The producer must construct exactly this center and angle, with no optimizer or search.
An independent reconstruction can use `y=q-5/2+(S/C)(h-9/10)` and form corners directly
from the orthonormal vectors `(C,S)` and `(-S,C)`.

Use P12 in the order supplied by
[restricted_orientation.py](../../cases/stromquist/restricted_orientation.py):

$$
\begin{aligned}
&A_1=(1,q-3),\ A_2=(q/2,q-3),\ A_3=(3/2,13/10),\\
&B=(q-1,1),\ C_0=(q-4/5,q/2),\ D=(q-1,q-1),\\
&E=(q/2,q-4/5),\ F=(1,q-1),\ G=(4/5,q-2),\\
&H=(17/10,11/5),\ I=(11/5,11/5),\ J=(11/5,17/10).
\end{aligned}
$$

The label `C_0` distinguishes the marked point from the cosine `C`. Substitute q into
these formulas; do not scale or symmetrize the set.

## Why This Candidate Is Worth Checking

For generic `0<t<1/5`, the projected separation between A1 and G satisfies

$$
v_G-v_A-1=C+S/5-1=\frac{2t(1/5-t)}{1+t^2}>0.
$$

Thus their unit-width coverage strips leave a gap between `v_A+1/2` and `v_G-1/2`. The
chosen V coordinate is its midpoint, and `-Sx+Cy=V_0` by construction.
This generic argument establishes strict avoidance of those two marks only.
Containment and avoidance of the other ten remain untested.

The actual angle guard is distinct from the outward interval used by earlier proof
instruments. Verify `0<t<1/480`; then `2 arctan(t)<2t<1/240<pi/720`, using `pi>3`. The
candidate is therefore in the actual positive near-axis band if that guard passes.

## Next-Block Execution and Scope

Allocate this as one bounded `pipeline-improvement` slice followed by `research-loop`,
with separate producer and independent-reader authors and swapped reviews.
Controls should check `1+t^2>0`, `C>0`, `C^2+S^2=1`, the generic identities,
zero-strip-gap endpoints `t=0` and `t=1/5`, both gap signs and closed boundary
membership. A zero strip gap alone does not imply full point membership.
Scientific constructors remain forbidden in those tests.
The coordinator then commits the prospective experiment and exact process caps before
any target evaluation.

The independent reader must reconstruct the candidate and all twelve marked points,
check exact unit-square corners and containment.
For counterclockwise cyclic corners `z_i`, every marked point `p` must have
`det(z_(i+1)-z_i,p-z_i)<0` for at least one edge.
Closed membership means all four determinants are nonnegative.
A supporting-line zero alone does not establish membership when another determinant is
negative; include that case in the controls.
Require complete point inventory, exact identity and actual successful process exits.
No failure authorizes a second angle, center, point set or invocation.

Session 091 completed independent source-free readiness review on 2026-09-07 at
06:07:43 UTC. The producer's thirteen controls and the source-distinct corner reader's
twelve controls pass; swapped reviews found no soundness issue. The reader rebuilds
the center from the alternate formula and checks all sixteen wall slacks and all
forty-eight point-edge determinants. Both processes require separately frozen external
whole-process caps. No target had run at that checkpoint; readiness alone did not
establish this hypothesis.

A verified escape would invalidate the unchanged unconditional near-axis P12 auxiliary
clause. It would not refute H-036, H-102, H-104, or the accepted H-106/H-108/H-109
auxiliary results. In particular, generically `x=h<1`, outside the canonical region of
the A-forcing lemmas.
Refuting H-036 still requires the separate BC-256 task: a verified packing of eleven
squares satisfying its angle and side conditions.

## Outcome

[Exp-121](../series/series-000-smoke-and-calibration/experiments/exp-121-h-110-fixed-p12-escape.md)
accepted H-110 on 2026-09-07. The sole exact producer and source-distinct reader both
returned actual exit zero. The reader reconstructed the fixed square, verified its
actual angle and containment, and checked forty-eight exact edge determinants proving
strict avoidance of every one of the twelve marks. Combined process cost was
0.11 seconds wall. This is a counterexample to the unchanged unconditional P12
auxiliary, not a counterexample to an eleven-square packing theorem.

The next selected direction is the separately reviewed
[fixed-diamond conditional reduction](../series/series-000-smoke-and-calibration/results/agenda-026/bc-255-conditional-compatibility-assessment.md).
The present experiment did not test whether its square avoids that diamond; that is a
different claim and cannot be inferred from avoiding the marked points.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
