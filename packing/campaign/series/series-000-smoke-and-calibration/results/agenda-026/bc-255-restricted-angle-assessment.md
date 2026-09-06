# BC-255 Restricted-Angle Assessment

Status: W3 assessment for BC-255 / `think-dene`; no target search, new experiment, or
theorem acceptance. The coordinator owns registration and disposition.

A bounded proof/falsification pair is worth preparing for
[H-036](../../../../hypotheses/H-036-robust-restricted-orientation.md).
The first proof instrument should test Stromquist’s conditional point-cover argument
over one square’s center and angle.
Its obligations are finite-dimensional and explicit; their truth and running cost over
the angle neighborhoods remain untested.
This assessment does not justify building an eleven-square atlas.

The first readiness gap is a checked replay of Stromquist’s **Theorem 3** at exact
0°/45°. The existing
[repaired-cover certificate](../../../../../cases/stromquist/repaired_cover.py) replays
Theorem 2, whose printed Figure 14 needed a source-distinct repair.
It is useful machinery and a caution about source transcription, but does not discharge
H-036’s restricted-orientation control.
Theorem 3’s source remains
[the archived paper, “45-degree packings”](../../../../../resources/papers/stromquist-2003-packing-10-or-11-unit-squares.md#45-degree-packings).

## Fixed Domain and Complete Cases

Keep H-036’s existing claim: eleven unit squares, each oriented within 0.25° of 0° or
45° modulo quarter turns, require a containing side of at least 3.878. Write

$$
q=\frac{1939}{500}=3.878,\qquad
\delta=\frac{\pi}{720},\qquad
\Theta=[-\delta,\delta]\;\cup\;
[\pi/4-\delta,\pi/4+\delta].
$$

Every allowed angle has a representative in these two closed intervals.
Both signs of each square’s perturbation are retained independently.
A quarter turn preserves the square; reflecting one square independently does not
preserve its relations to the other squares and is not a valid configuration reduction.

For centers $c_i=(x_i,y_i)$ and $\theta_i\in\Theta$, let

$$
u_i=(\cos\theta_i,\sin\theta_i),\quad
v_i=(-\sin\theta_i,\cos\theta_i),\quad
r_i(a)=\tfrac12(|a\cdot u_i|+|a\cdot v_i|).
$$

The complete configuration domain consists of:

- Every composition $k=0,\ldots,11$, where $k$ squares use the near-45° interval.
  Relabeling makes the first $k$ squares that class without restricting their geometry.
- Containment of all four corners of every square in $[0,L]^2$, with $0\leq L<q$.
  Equivalently, each center coordinate lies in $[h_i,L-h_i]$, where
  $h_i=(|\cos\theta_i|+|\sin\theta_i|)/2$.
- For each of the 55 unordered pairs, all eight owner-axis-order possibilities: choose
  $a\in\{u_i,v_i,u_j,v_j\}$ and $\sigma\in\{-1,1\}$, and impose
  $\sigma a\cdot(c_j-c_i)\geq r_i(a)+r_j(a)$ for at least one choice.
- All zero gaps, wall contacts, coincident support expressions, and angle endpoints.
  If absolute values are split into sign cases, retain both closed cases at zero.
  A single fixed-angle separation branch cannot stand in for this union.

This is a completeness specification, not a proposal to enumerate $8^{55}$ branches.
The support formulation agrees with the
[BC-245 packet](bc-245-typed-backbone-theorem-packet.md#smooth-support-branches), but
the point-cover proposal below needs no stationary-record producer or local-rigidity
claim.

The nine-point near-axis argument in
[X-014](../../../../explorations/X-014-closing-from-both-ends.md) supplies a small
composition control.
For $|\theta|\leq\delta$, a concentric axis-aligned square of side $b=199/200$ lies
strictly inside the unit square because

$$
b(\cos\theta+|\sin\theta|)
\leq b(1+\delta)
<\frac{199}{200}\frac{2531}{2520}
=\frac{503669}{504000}<1,
$$

using $\pi<22/7$. Also $b>q/4=1939/2000$. Each such core contains an interior point of
$\{q/4,q/2,3q/4\}^2$, so ten near-axis squares with disjoint interiors cannot fit in
$[0,q]^2$. This explicitly checks the existing mechanism for compositions $k=0,1$; it is
not a fresh accepted campaign result.
The remaining compositions still require their declared coverage.

## Why Uniform Core Transfer Is Insufficient

Stromquist’s exact 0°/45° optimum is $s_0=2+(4/3)\sqrt2$. Replacing every perturbed unit
square by its concentric 0°/45° core of side $b_0=1/(\cos\delta+\sin\delta)$ and
rescaling gives only

$$
L\geq \frac{s_0}{\cos\delta+\sin\delta}.
$$

That guaranteed lower bound is strictly below $q$. This comparison needs no numerical
run: $\sqrt2<99/70$ gives

$$
s_0<\frac{136}{35}<q\frac{501}{500},
$$

while $\delta>1/240$ and monotonicity of $\cos t+\sin t$ on $[0,\pi/4]$ give

$$
\cos\delta+\sin\delta
>1+\frac1{240}-\frac1{2\cdot240^2}-\frac1{6\cdot240^3}
>\frac{501}{500}.
$$

Thus this transfer alone cannot prove H-036. It does not refute H-036 or rule out an
angle-dependent conditional cover.
Reducing the angle radius would require a different prospective claim.

## Candidate Conditional Cover

At side $q$, define the ten-point set $P_{10}$ by the coordinate-reflection orbit of

$$
(1,1),\quad(q/2,1),\quad(3/2-q/4,q/2),\quad(1/2+q/4,q/2).
$$

The group is $K_4=\{1,(x,y)\mapsto(q-x,y),(x,y)\mapsto(x,q-y),
(x,y)\mapsto(q-x,q-y)\}$. It is not the full dihedral group: quarter-turning $(q/2,1)$
gives $(q-1,q/2)$, absent from $P_{10}$.

Use the paper’s twelve-point coordinates with $s$ replaced by $q$:

$$
\begin{aligned}
A_1&=(1,q-3),& A_2&=(q/2,q-3),& A_3&=(3/2,13/10),\\
B&=(q-1,1),& C&=(q-4/5,q/2),& D&=(q-1,q-1),\\
E&=(q/2,q-4/5),& F&=(1,q-1),& G&=(4/5,q-2),\\
H&=(17/10,11/5),& I&=(11/5,11/5),& J&=(11/5,17/10).
\end{aligned}
$$

Call this set $P_{12}$ and its first three points $A$. Substitution of $q$ and extension
to $\Theta$ are proposed mechanisms, not claims already supplied by the paper.
The complete one-square domain is

$$
\mathcal D=\{(c,\theta):\theta\in\Theta,
\quad c\in[h(\theta),q-h(\theta)]^2\}.
$$

Three obligations would suffice:

1. **Localization.** Every closed unit square in $\mathcal D$ avoiding all of $P_{10}$
   has a near-45° angle and its center in one of the four $K_4$ images of
   $R=[1,q/2]\times[0,1]$.
2. **Triple forcing.** After the corresponding reflection of the entire container and
   configuration, every such square with center in $R$ contains all three points of $A$.
   Test failure of each of the three containments, not just simultaneous failure.
3. **Twelve-point cover.** Every closed unit square in $\mathcal D$ contains at least
   one point of $P_{12}$.

For localization, reuse only the topology of the
[Figure 13 partition](../../../../../cases/stromquist/repaired_cover.py): four corner
cells, four side cells, ten triangles, and four exceptional rectangles.
Recompute their coordinates at $q$ and verify the tiling and every relevant covering
inequality. All cell edges and vertices must be covered, including shared boundaries.
Split each angle neighborhood at its central angle when needed for signs; both endpoints
remain. The existing Theorem 2 numerical or algebraic inequalities are not reusable as
Theorem 3 proofs merely because the topology matches.

If all three obligations hold, a putative unit packing with $L<q$ can be scaled to side
$q$, producing eleven interior-disjoint squares of side strictly greater than one.
Each contains its concentric closed unit square in its interior.
At least one enlarged square avoids $P_{10}$ because a point can lie in at most one of
their interiors. Localization and triple forcing put three points of the appropriately
reflected $P_{12}$ in that same square’s interior.
The other ten squares each contain a point of $P_{12}$ in their interiors, but only nine
points remain. This is the contradiction.
Using the enlarged squares prevents a shared boundary point from being counted twice.
The argument requires the strict sublevel $L<q$, exactly as H-036 does.

## One LP Obligation and Its Interval Extension

For fixed $\theta$, let $u=(\cos\theta,\sin\theta)$ and $v=(-\sin\theta,\cos\theta)$.
For each $p\in P_{12}$, choose one of four signed directions $d_p\in\{u,-u,v,-v\}$ and
impose

$$
d_p\cdot(p-c)\geq\tfrac12+\eta,
\qquad c\in[h(\theta),q-h(\theta)]^2.
$$

Maximize the common slack $\eta$. A point-avoiding closed unit square exists exactly
when some branch has a feasible $\eta>0$. Proving every branch has maximum at most zero
establishes the twelve-point cover; a zero optimum is a boundary case, not an escape.
With rows $Az\leq b$, $z=(c_x,c_y,\eta)$, an exact upper-bound certificate has $y\geq0$,
$A^Ty=(0,0,1)^T$, and $y^Tb\leq0$. Empty branches may instead have exact Farkas
certificates.
The same slack construction handles point-avoidance clauses in localization
and each failed triple containment.

The [exact LP implementation](../../../../../src/sqpack/exact_lp.py) supplies exact
coefficient arithmetic and optimality checking.
Its phase-one infeasibility exception does not itself retain an independent certificate,
so the new instrument must retain and replay the actual multipliers or an equivalent
exact infeasibility witness.

A full $4^{12}$ branch enumeration is unnecessary at a fixed angle.
In square coordinates, each point covers an axis-aligned unit square of possible
centers. The $2m$ boundary coordinates on each axis partition the plane into at most
$(2m+1)^2$ open rectangles: 625 for $m=12$. All line segments, intersection points, and
coincident boundaries must also be retained.
Intersect each cell with the rotated containment domain and test its point-cover status.
This count is a combinatorial bound, not measured throughput.

For an angle interval, projected point orders can change and the LP coefficients vary.
The certifier must either subdivide at certified order changes or retain a complete
overlapping cover with interval bounds valid throughout each leaf.
A midpoint LP or an exact LP at the two endpoints does not certify the intervening
angles. A rational outer LP with proved coefficient-error bounds and an exact dual
certificate is one possible leaf check.
Exact-angle boundary leaves may need symbolic inequalities when their best slack is
zero. No global interval-cover implementation or running-time claim is supplied by this
assessment.

## Controls, Falsifiers, and Bounded Exit

The required controls have different purposes:

| Control | Required behavior |
| --- | --- |
| Eleven axis-aligned unit squares centered on $\{1/2,3/2,5/2,7/2\}\times\{1/2,3/2,5/2\}$, omitting $(7/2,5/2)$, in side 4 | Independent exact packing verification accepts this rational, in-regime feasible instance. Side 4 is a control, not the target threshold. |
| Side 1, angle 0, center $(1/2,1/2)$, marked point $(1,1)$ | The point-cover checker retains the zero-slack boundary hit and does not report a strict escape. |
| Side 4, angle 0, center $(1/2,1/2)$, sole marked point $(2,2)$ | The checker accepts a point-avoiding feasible square; its signed avoidance slack is exactly 1 by substitution. |
| Theorem 3 at exact 0°/45° and side $s_0$ | Replay the source’s conditional argument with its original coordinates before extending the instrument. The grid controls do not substitute for this preregistered requirement. |
| Existing exact Trump witness and its local LP/cone controls | Retain their original verdicts. The witness’s tilted angle is outside H-036; accepting it as an in-regime counterexample is a rejection-control failure. Local rigidity supplies no global capture premise. |

The feasible-grid coordinates and the two elementary point-cover examples above are
transparent constructions, not newly executed measurements.
The Trump witness is in [its exact case](../../../../../cases/trump11/packing.py), and
the distinction between local and global conclusions is recorded in
[the frontier](../../../../../frontier/n-011.md).

Pair a later frozen proof attempt with BC-256’s independent eleven-square search over
the unchanged $\Theta^{11}$ domain.
A rigorously feasible candidate with $L<q$ refutes H-036 after independent angle,
containment, and nonoverlap checks; it need not beat Trump.
Failure to find one is not proof.
A single square escaping $P_{12}$, escaping localization, or defeating the forced triple
only rejects the corresponding proposed auxiliary lemma.
It does not refute H-036.

The next proof-side decision is whether a bounded Theorem 3 control replay and a
complete one-square cover instrument are justified after pricing their implementation.
Stop that assessment at the first missing boundary case, unreplayable control, or
unpriced interval leaf.
Record the precise obstruction under
[H-102](../../../../hypotheses/H-102-complete-restricted-angle-support-families.md),
with H-036 unresolved.
No density measure, global atlas, or revision of the restricted claim is required to
expose that obstruction.

If authorized, keep implementation in
`packing/cases/stromquist/restricted_orientation.py` and controls in
`packing/tests/test_stromquist_restricted_orientation.py`, leaving the frozen source and
existing Theorem 2 certificates unchanged.
Retained target outputs belong under this Agenda 026 results directory after the
coordinator assigns and freezes their experiment record.
This assessment is the only artifact written by this slice.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
