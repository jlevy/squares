# BC-255: Restricted-Angle Instrument Design

Status: design and pricing only, under BC-255 / H-036 / `think-6s8x`, Session 089 phase
5, W7 pipeline-improvement/correctness.
The commission is `20:15:48–20:35:48 UTC` on 2026-09-06. No target-side or
perturbed-angle geometry, target search, LP, or experiment was run.
The [source-control report](bc-255-theorem3-source-control-slice-01.md) and
[source code](../../../../../cases/stromquist/restricted_orientation.py) are inputs to
an independent review, not conclusions of this design.
Every implementation recommendation below is conditional on the coordinator accepting
that review’s usable source-control guarantees.

The smallest next discriminator is the proposed point-set mechanism at **side 3.878 and
the two exact source angles**, before building its continuous-angle extension.
If that necessary screen passes, use a one-parameter event sweep with exact boundary
leaves. Direct interval boxes can discard easy regions; any unresolved boundary leaf
still needs an exact argument.

## Fixed Claim and What the Instrument Would Prove

Keep [H-036](../../../../hypotheses/H-036-robust-restricted-orientation.md) unchanged:

$$
q=1939/500,
\qquad \delta=\pi/720,
\qquad \Theta=[-\delta,\delta]\cup[\pi/4-\delta,\pi/4+\delta].
$$

Every square chooses its angle independently, modulo quarter turns.
The proof must cover both signs and all endpoints, not one shared perturbation angle.
At fixed side $q$, its one-square domain is
$\{(c,\theta):\theta\in\Theta,\ c\in[h(\theta),q-h(\theta)]^2\}$, where
$h=(|\cos\theta|+|\sin\theta|)/2$. Use exactly the candidate ten-set, twelve-set,
A-triple, and canonical rectangle $R=[1,q/2]\times[0,1]$ defined in the
[assessment](bc-255-restricted-angle-assessment.md#candidate-conditional-cover), with
the source coordinate formulas evaluated at $q$. Do not optimize or move those points
inside the first discriminator.

The complete auxiliary obligations are near-axis ten-set coverage, localization of every
near-45° ten-set avoider into a coordinate-reflection image of $R$, containment of each
A-point separately by every canonical avoider, and twelve-set coverage on both angle
neighborhoods. A checked failure of any one obligation rejects this proposed sufficient
mechanism. It is not an eleven-square counterexample to H-036.

If all obligations hold, the assessment’s strict-sublevel argument applies to every
composition of near-axis and near-45° squares at once.
Scale a putative packing with $L<q$ to side $q$; each enlarged open square contains its
concentric closed unit square strictly inside it.
At least one of the eleven enlarged squares avoids the ten-set.
After reflecting the **whole configuration**, localization and forcing place three
distinct twelve-set points inside that square.
The other ten squares each require a different remaining twelve-set point, but only nine
remain. Closed-unit boundary hits are legitimate because the containing enlarged square
is open and strictly larger.
Reflecting individual squares independently is not a reduction.

This would prove the declared restricted-family lower bound, not global optimality,
equality at $q$, or exclusion of intermediate orientations.
BC-256’s independent packing falsifier can proceed separately when commissioned.
Only a rigorously checked eleven-square packing below $q$, with every angle in the
actual $\Theta$, refutes H-036.

## Why the Uniform Core Does Not Close the Gap

For $s_0=2+(4/3)\sqrt2$, the uniform core argument transfers only

$$
L\geq\frac{s_0}{\cos\delta+\sin\delta}<q.
$$

The strict comparison is already proved with rational inequalities in the
[assessment](bc-255-restricted-angle-assessment.md#why-uniform-core-transfer-is-insufficient).
Increasing arithmetic precision cannot recover the geometric loss from shrinking every
square by the same worst-angle factor.
The conditional cover must exploit its own angle-dependent inequalities.
Shrinking the angle radius would change the prospective claim and is not a fallback.

## One Parameter and Two Center Coordinates

Write $\theta=\alpha+\varepsilon$, with $\alpha=0$ or $\pi/4$, and put

$$
t=\tan(\varepsilon/2),\quad d=1+t^2,\quad
C_0=(1-t^2)/d,\quad S_0=2t/d.
$$

Use $(C,S)=(C_0,S_0)$ in the first chart and $((C_0-S_0)/\sqrt2,(C_0+S_0)/\sqrt2)$ in
the second. All geometry is rational in $t$ over $K=\mathbb Q(\sqrt2)$. Split at $t=0$
before removing absolute values from $h$. Prove the signs used on each chart; do not
infer them from a midpoint.
The exact denominator $d$ is positive throughout.

For proof coverage, a fixed rational outer endpoint avoids constructing the algebraic
number $\tan(\pi/1440)$ as a new number field.
For example, with $x_+=11/5040$, use

$$
T=\frac{x_+}{1-x_+^2/2}.
$$

The inequalities $\pi<22/7$, $\sin x\leq x$, and $\cos x\geq1-x^2/2>0$ show
$\tan(\pi/1440)<T$. A proof on the two closed charts $t\in[-T,T]$ therefore covers the
unchanged claim. This is an outward enlargement, never a hidden narrowing.
An escape in the added sliver does not refute even the actual-angle auxiliary lemma.
Any proposed counterexample needs a separate check that $|t|\leq\tan(\pi/1440)$, using
certified endpoint enclosures or exact inequalities; an undecided endpoint comparison is
a refusal.

In square-frame center coordinates $U=Cx+Sy$, $V=-Sx+Cy$, each marked point $p$ is
contained exactly when

$$
U\in[p_U(t)-1/2,p_U(t)+1/2],\qquad
V\in[p_V(t)-1/2,p_V(t)+1/2].
$$

The coarse square $[-2q,2q]^2$ contains every projected admissible center, since
$|C|,|S|\leq1$ and $0\leq x,y\leq q$. Its constant bounds avoid introducing moving
bounding-box extrema into the event list.
Containment and the localization/canonical regions remain linear inequalities in $(U,V)$
with rational-function coefficients in $t$. Clear only the positive denominator $d$; the
resulting boundary-line coefficients have degree at most two over $K$ on each sign
chart.

## Complete Event Sweep, Including Feasibility Changes

Projected-point ordering alone is insufficient.
A point-cell can enter or leave the moving containment polygon, or the localization
failure region, while every projected marked-point order remains unchanged.
The complete instrument must include both kinds of event.

1. Form each axis’s marked-point entry/exit functions and coarse bounds.
   Isolate all nonidentically-zero pairwise differences on the parameter chart.
   Identical functions keep their point labels but share a geometric event.
   Between roots, exact order and closed-point membership masks are constant.
2. At a rational sample in each open parameter interval, enumerate singleton events and
   intervening open intervals on both center axes.
   Classify every product stratum by its masks.
   A correctly covered stratum needs no reachability calculation.
   Every mask failing the relevant auxiliary obligation remains to be checked against
   containment and its required region, even if currently unreachable at the sample.
3. For each such potentially bad stratum, collect its four closed cell bounds,
   containment bounds, and the relevant region bounds.
   Include zeros of all nonidentically-zero pair determinants and triple augmented
   determinants of these boundary lines.
   They detect parallelism, coincident support lines, vertex-edge contacts, and changes
   in the feasible intersection’s dimension or strict-boundary status.
   These polynomials have degree at most four and six respectively over $K$.
4. Subdivide at those roots and decide reachability on every resulting open parameter
   interval and every singleton parameter root.
   Constant determinant signs justify transferring the labelled feasibility decision
   from a sample across an open interval.
   Recompute the event inventory and masks at singleton roots; neither neighboring
   interval owns a collision automatically.

The economical implementation generates feasibility determinants only for potentially
bad cells, not every triple of every line in the combined arrangement.
Rigorous interval signs may discard a polynomial with no zero on a slab or certify an
unreachable cell uniformly; a failed interval test simply leaves the exact obligation.
Checking a midpoint or two endpoints without those uniform certificates is insufficient.

There are at most $(4m+3)^2$ center product strata for $m$ labelled marked points,
including all dimensions and the two coarse bounds per axis.
For the combined 22 labels this bound is 8,281; separate twelve-set coverage has bound
2,601. These are combinatorial bounds, not measured target counts or throughput.
Use separate obligation inventories where that is cheaper, while sharing exact event
polynomials and refusing missing point labels.

### Exact boundary leaves without a general algebraic-field framework

For $p(t)=a(t)+\sqrt2b(t)$, zeros are among those of $a(t)^2-2b(t)^2\in\mathbb Q[t]$.
Using this norm may introduce conjugate roots; retaining extra split points is safe.
Square-free rational Sturm isolation gives a finite complete root cover; multiplicities
must not be interpreted as sign changes, and identities must not be sent to a root
finder. Root brackets from different polynomials must be ordered and disjoint, or proved
by a gcd check to describe the same root.
Overlapping numerical brackets must not be conflated or leave a gap in the angle cover.

The existing [field implementation](../../../../../src/sqpack/field.py) has rational
Sturm primitives, but its `NumberField` precondition checks are not a general engine for
every compositum arising at an event root.
Do not assume that every such field can be instantiated.
A smaller boundary oracle represents one real root by a square-free rational polynomial
and a rational isolating interval.
To decide a rational polynomial at that root, first test equality by a gcd and root
count, then refine its interval until a nonzero sign is separated.
For $a+\sqrt2b$, combine the signs of $a$, $b$, and $a^2-2b^2$; this also distinguishes
an actual zero from an extraneous conjugate zero.
The norm degree is at most twelve for the general determinant list above.
This oracle is an implementation obligation, not an available public API or a completed
proof checker.

No algebraic vertex coordinates need be divided or numerically rounded for the
reachability decision.
The closed intersection is bounded; enumerate intersections of nonparallel boundary
pairs and test all inequalities through determinant signs.
For each strict constraint, require at least one feasible closure vertex where it is
strict. The average of all feasible vertices then satisfies every strict constraint
simultaneously.
If a strict constraint is tight at every vertex, the open intersection is
empty. This retains line segments, points, wall contacts, and coincident events.
The argument needs all feasible closure vertices, not one selected clipping vertex.

## Controls and Refusals Before Any Target Run

Preserve the reviewed source replay and its fixed source-only command.
Its exact boundary-hit, open-segment, endpoint, and independently checked escape
controls are necessary starting controls, conditional on source review.
Add only controls that exercise the new parameter logic:

| Constructive control | Required outcome |
| --- | --- |
| A constant parameter family equal to an accepted fixed-angle source control | Same complete decision and boundary ownership for every parameter; no vacuous empty-domain success |
| Two event functions $e_1(t)=t$, $e_2(t)=0$ on $[-1,1]$ | Two open order intervals and the singleton collision at zero |
| Coincident events and a tangency $e_1-e_2=t^2$ | Identity labels retained; zero isolated without assuming a sign flip |
| The cell $U=V=0$ and moving half-plane $U+V\leq t$ | Reachability changes at zero although point-axis orders do not; the singleton is feasible |
| A closed square clipped first to a segment, then to an endpoint, with one endpoint required open | Preserve the closed segment and point; reject the excluded open endpoint |
| Isolated root $\rho=\sqrt2$ tested on $\rho-\sqrt2$ and $\rho+\sqrt2$ | First value exactly zero, second positive despite both norms vanishing |
| $p(t)=t^2-2t+2$ on $[0,2]$, whose ordinary Horner interval straddles zero although $p=(t-1)^2+1>0$ | Refine or retain an unresolved leaf; never report exact zero from enclosure overlap |
| An omitted root/angle endpoint, changed strict flag, narrowed chart, or dropped point label | Independent coverage/semantics replay refuses the incomplete certificate |

Use the existing
[directed interval arithmetic](../../../../../src/sqpack/promote/interval.py) for
optional uniform enclosures, not rounded center samples.
Its refusal-on-zero-overlap contract is appropriate.
The existing
[fractional interval checker](../../../../../src/sqpack/fractional/interval.py)
explicitly documents why exact cover seams can stall pure boxes; importing its
mass-cover verdict would not prove this different conditional point-cover statement.
`PoseBox` supplies an input shape, not complete angle/center coverage.

## Next Frozen Discriminator and Price

After source review, commission **one 20–30 active-minute implementation slice** for an
exact fixed-frame adapter and the controls above that do not yet require algebraic
parameter roots. Keep the original source command unchanged; the candidate uses a
separate explicit entry point.
A later coordinator-frozen run tests all seven auxiliary obligations at $q$ and exactly
0°/45°, with the assessment’s unchanged point coordinates.
Use one process, a proposed ten-second wall cap, and no point movement or second
candidate. Source timings of 1.70–2.01 seconds motivate an unmeasured planning range of
1–10 seconds; they do not certify that cap for the candidate.

The discriminator is precise: either every listed exact-angle auxiliary obligation is
completely checked, or retain its first directly verified escaping unit square and the
unchecked obligations.
A timeout, empty-domain mistake, missing boundary, or unreplayable witness is
unresolved.
A checked escape rejects the present sufficient mechanism and parks its angle
extension.
Passing is only permission to price the continuous-angle instrument, not H-036
acceptance.

If that screen survives, estimate **60–120 additional active author minutes**, in slices
of at most 30 minutes, for parameter events, lazy feasibility determinants, and the
algebraic boundary sign oracle; allow a separate 10–20-minute source-distinct review.
These are design estimates, not a renewed commission or measured implementation cost.
Do not spend an hour enumerating all line triples before a control has exercised the
needed event list.

Before its first continuous target run, freeze the two charts, point formulas,
obligation order, arithmetic, and command in the ordinary experiment record.
A proposed initial limit is one process and 60 wall seconds, with at most 10,000
generated nonzero critical polynomials, 10,000 parameter leaves, and 256 root-isolation
bisections per root bracket.
Controls must price these guards before the coordinator adopts them.
Any guard leaves the unprocessed intervals, roots, and center obligations explicitly
unresolved; none authorizes finer grids, another point set, or an automatic longer run.

For a first continuous discriminator, select near-axis ten-set coverage on its entire
closed chart, not a few angle samples.
Only after that completes should the coordinator fund the remaining localization, three
separate forcing, and both twelve-cover obligations.
Partial completion is a restricted auxiliary result; all clauses remain necessary for
this route to H-036.

The principal risks are an actual failure of the fixed point-set mechanism, an omitted
feasibility event, an unhandled algebraic singleton, excessive root/event growth, or
misuse of a closed boundary hit in the packing count.
Direct three-dimensional interval boxes are a cheaper exploratory implementation, but
are economical as the primary proof route only if a complete run certifies every leaf
without unresolved seams.
Otherwise they duplicate work that the exact event boundary instrument still has to do.
No global eleven-square atlas, density instrument, new registry claim, or certificate
manifest is needed for this first decision.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
