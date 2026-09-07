# Restricted Orientations and the Continuous-Angle Gap

The seven exact-angle auxiliary clauses are completed results. A theorem for the closed near-axis angle neighborhoods is still open. The dated final section of the instrument design supersedes its earlier fixed-angle recommendation. Full quantifiers for H-036 and H-102-104 are in file 15; the original source lemmas are in file 16.

<a id="source-1"></a>

## Source 1: `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-restricted-angle-assessment.md`

Snapshot `4d305597a505`, source lines 1-222.

<a id="source-1-bc-255-restricted-angle-assessment"></a>

### BC-255 Restricted-Angle Assessment

Status: W3 assessment for BC-255 / `think-dene`; no target search, new experiment, or
theorem acceptance. The coordinator owns registration and disposition.

A bounded proof/falsification pair is worth preparing for
[H-036](15-registered-mathematical-questions.md#source-1).
The first proof instrument should test Stromquist’s conditional point-cover argument
over one square’s center and angle.
Its obligations are finite-dimensional and explicit; their truth and running cost over
the angle neighborhoods remain untested.
This assessment does not justify building an eleven-square atlas.

The first readiness gap is a checked replay of Stromquist’s **Theorem 3** at exact
0°/45°. The existing
[repaired-cover certificate (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/cases/stromquist/repaired_cover.py) replays
Theorem 2, whose printed Figure 14 needed a source-distinct repair.
It is useful machinery and a caution about source transcription, but does not discharge
H-036’s restricted-orientation control.
Theorem 3’s source remains
[the archived paper, “45-degree packings”](16-mathematical-background-and-literature.md#source-5-45-degree-packings).

<a id="source-1-fixed-domain-and-complete-cases"></a>

#### Fixed Domain and Complete Cases

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
[BC-245 packet](13-typed-global-structure.md#source-1-smooth-support-branches), but
the point-cover proposal below needs no stationary-record producer or local-rigidity
claim.

The nine-point near-axis argument in
[X-014](10-fractional-barriers-and-negatives.md#source-1) supplies a small
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

<a id="source-1-why-uniform-core-transfer-is-insufficient"></a>

#### Why Uniform Core Transfer Is Insufficient

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

<a id="source-1-candidate-conditional-cover"></a>

#### Candidate Conditional Cover

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
[Figure 13 partition (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/cases/stromquist/repaired_cover.py): four corner
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

<a id="source-1-one-lp-obligation-and-its-interval-extension"></a>

#### One LP Obligation and Its Interval Extension

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

The [exact LP implementation (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/src/sqpack/exact_lp.py) supplies exact
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

<a id="source-2"></a>

## Source 2: `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-114-h-104-fixed-side-auxiliaries.md`

Snapshot `4d305597a505`, source lines 67-end.

<a id="source-2-exp-114--a-ten-second-point-cover-discriminator"></a>

### exp-114 — A Ten-Second Point-Cover Discriminator

H-104 is accepted at its narrow auxiliary scope.
The producer completed all seven clauses, and its single independent file replay
accepted the exact inputs and receipt.
There were no unchecked clauses or returned obstructions.
H-036 remains unresolved; this does not improve the already known exact-0/45 packing
bound or cover nearby angles.

The prospective claim and protocol were committed before target access; `2153cb02`
retains the independently reviewed reader and final operational lease.
All 31 record checks passed before the single producer run from clean `e45c8a63`. The
reader ran once from clean `2153cb02`, at 21:35:35 UTC, and returned exit 0. The
[independent output review (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/campaign/series/series-000-smoke-and-calibration/results/exp-114-h-104-fixed-side-auxiliaries/target-output-independent-review.md)
accepts computational verification through the reviewed exhaustive algorithm plus
independent exact input/receipt checks, not a standalone exhaustive certificate.

Producer process cost was 2.41 seconds wall and 2.37 seconds CPU; the worker reported
2.280254 seconds wall and 2.249838 seconds CPU. The independent reader used 0.05 seconds
wall and 0.05 seconds CPU. Summed process wall was 2.46 seconds and CPU 2.42 seconds;
these do not measure operator attention.
Both process exits were 0, within their separate ten-second caps, and neither was
repeated.

Event-product stratum counts were `[280,526,247]` at 0 degrees and `[668,1397,728]` at
45 degrees. Six 45-degree strata avoid the ten-set, one in the canonical region.
These are diagnostic counts, not the independent proof of exhaustive coverage.
The next decision is whether to fund the separately priced continuous-angle instrument.
No such extension is automatically authorized by this result.

<a id="source-2-retained-readiness-and-prospective-protocol"></a>

#### Retained Readiness and Prospective Protocol

The target remained unopened during reader development.
The independent reader’s author stopped at 21:13:28 UTC with nine passing source/toy
tests, but explicitly withheld reader readiness pending cold review and two targeted
regressions. The original 21:14 operational lease expired without a target invocation.
`think-slox` then returned cold-review GO, with twelve source/toy tests passing and
writer stop at 21:26:39 UTC. Root accepts reader readiness and prospectively opens the
unused target/replay allowances through 21:40 UTC. No process budget has been consumed,
shortened or reset.

The independent command, run from the committed reader checkout, is:

```bash
PYTHONPATH=src /Users/levy/wrk/github/squares/packing/.venv/bin/python3 -m devtools.check_restricted_orientation_discriminator PACKET --target-fixed-side --producer-exit-code STATUS
```

`PACKET` is the absolute retained producer path and `STATUS` its actual exit code.
The reader installs its own fixed ten-second alarm.
Retain its stdout as `replay.json`, stderr and process costs as `replay.log`, and the
independent scope review beside them.
There is no second producer or source-distinct exhaustive positive certificate.

This one run tests
[H-104](15-registered-mathematical-questions.md#source-13), not the full
H-036 packing statement.
The root commits this protocol before accessing target geometry and runs it from a clean
immutable checkout of `e45c8a63`. The
[adapter review (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-fixed-side-discriminator-independent-review.md)
has accepted the source-preserving algorithm and its controls.

Accept H-104 only if all seven clauses are completely checked, the exact input and
receipt agree with this protocol, and independent output review accepts that scope.
The positive result relies on the reviewed exhaustive event-stratum algorithm; counts
alone are not a standalone geometric certificate.
Reject H-104 if an independent exact replay verifies one returned counterexample to a
clause, even if the remaining clauses are unchecked.
With neither a complete positive check nor a verified counterexample, leave it
unresolved.

Retain producer stdout as `packet.json` and stderr/process costs as `run.log` in the
declared directory. The independent reviewer owns a separate ten-second receipt/witness
replay and retains its result and cost.
It must not rerun the target producer or infer positive exhaustive coverage from counts.
A failed run with no checked negative witness is not a mathematical negative.
No unchanged retry is authorized.

A checked failure parks the continuous-angle extension of these point formulas.
A complete positive result permits pricing that extension, but no continuous-angle work
starts automatically.
Neither outcome proves or refutes H-036; its original3.878 and ±0.25-degree criterion
remains fixed.

<a id="source-3"></a>

## Source 3: `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-angle-instrument-design.md`

Snapshot `4d305597a505`, source lines 19-203.

<a id="source-3-fixed-claim-and-what-the-instrument-would-prove"></a>

#### Fixed Claim and What the Instrument Would Prove

Keep [H-036](15-registered-mathematical-questions.md#source-1) unchanged:

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
[assessment](12-restricted-orientations.md#source-1-candidate-conditional-cover), with
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

<a id="source-3-why-the-uniform-core-does-not-close-the-gap"></a>

#### Why the Uniform Core Does Not Close the Gap

For $s_0=2+(4/3)\sqrt2$, the uniform core argument transfers only

$$
L\geq\frac{s_0}{\cos\delta+\sin\delta}<q.
$$

The strict comparison is already proved with rational inequalities in the
[assessment](12-restricted-orientations.md#source-1-why-uniform-core-transfer-is-insufficient).
Increasing arithmetic precision cannot recover the geometric loss from shrinking every
square by the same worst-angle factor.
The conditional cover must exploit its own angle-dependent inequalities.
Shrinking the angle radius would change the prospective claim and is not a fallback.

<a id="source-3-one-parameter-and-two-center-coordinates"></a>

#### One Parameter and Two Center Coordinates

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

<a id="source-3-complete-event-sweep-including-feasibility-changes"></a>

#### Complete Event Sweep, Including Feasibility Changes

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

<a id="source-3-exact-boundary-leaves-without-a-general-algebraic-field-framework"></a>

##### Exact boundary leaves without a general algebraic-field framework

For $p(t)=a(t)+\sqrt2b(t)$, zeros are among those of $a(t)^2-2b(t)^2\in\mathbb Q[t]$.
Using this norm may introduce conjugate roots; retaining extra split points is safe.
Square-free rational Sturm isolation gives a finite complete root cover; multiplicities
must not be interpreted as sign changes, and identities must not be sent to a root
finder. Root brackets from different polynomials must be ordered and disjoint, or proved
by a gcd check to describe the same root.
Overlapping numerical brackets must not be conflated or leave a gap in the angle cover.

The existing [field implementation (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/src/sqpack/field.py) has rational
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

<a id="source-4"></a>

## Source 4: `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-angle-instrument-design.md`

Snapshot `4d305597a505`, source lines 287-end.

<a id="source-4-2026-09-06-next-allocation-after-h-104"></a>

#### 2026-09-06: Next Allocation After H-104

This source-only update is `think-p0nx`, commissioned at 22:09:48 UTC and handed back
under the shortened 22:19:32 deadline.
The preceding assessment remains historical.
[Exp-114](12-restricted-orientations.md#source-2) now accepts H-104:
the seven fixed-formula clauses hold at exactly 0° and 45°, through the reviewed
exhaustive producer and independent input/receipt checks.
It supplies no nearby-angle result, positive margin, or H-036 decision.
The frozen side 3.878 and both closed ±0.25° neighborhoods remain unchanged.

<a id="source-4-first-complete-obligation"></a>

##### First complete obligation

Keep the first continuous discriminator as **every contained near-axis closed unit
square hits the frozen ten-set**. Its domain includes every center and both signs of the
angle perturbation, including zero and the angle endpoints.
Proving it would complete one auxiliary clause; it would not settle localization, the
three separate A-point implications, either twelve-cover clause, or H-036. The earlier
nine-point argument already excludes the compositions with at most one near-45° square.
This ten-set check supports the particular conditional-cover proof, not a new claim to
that composition exclusion.

<a id="source-4-try-a-fixed-tiling-before-a-general-event-root-engine"></a>

##### Try a fixed tiling before a general event-root engine

A cheaper sufficient certificate may avoid moving event arrangements altogether.
Keep the actual angle-dependent containment domain by mapping a fixed unit square of
parameters $z=(z_1,z_2)$ to the center:

$$
F_t(z)=\bigl(h(t)+(q-2h(t))z_1,\ h(t)+(q-2h(t))z_2\bigr).
$$

The width must be proved positive throughout each chart.
Cover $[0,1]^2$ by a finite closed rational triangulation, and assign one frozen ten-set
point to each triangle on each one-sided angle chart.
For every triangle vertex $z$, assigned point $p$, and
$a(t)\in\{u(t),-u(t),v(t),-v(t)\}$, certify

$$
d(t)^2\bigl(1/2-a(t)\mathbin{\cdot}(p-F_t(z))\bigr)\geq0
\quad\hbox{throughout the chart},\qquad d(t)=1+t^2>0.
$$

Membership is affine in $z$, so vertex inequalities cover the whole closed triangle.
A checked triangulation covers every center, including seams and vertices.
After splitting the absolute-value signs in $h$, these are polynomials of degree at most
four over $\mathbb Q(\sqrt2)$; the near-axis rational target uses rational coefficients.
No moving vertex or algebraic parameter root is required by a successful certificate of
this form.

One small sign checker can map an angle slab to $w\in[0,1]$ and verify nonnegative
Bernstein coefficients by exact arithmetic.
That condition proves nonnegativity on the entire closed slab, including boundary zeros.
Exact factoring at rational endpoints and bounded rational subdivision may help, but a
mixed-sign coefficient list is inconclusive, not a negative value of the polynomial.
In particular, $(w-1/2)^2$ is nonnegative despite its negative middle degree-two
Bernstein coefficient.
An unresolved leaf must remain in the output.
This limitation can persist under subdivision: a nonzero polynomial with an interior
zero cannot have all nonnegative Bernstein coefficients there, because every Bernstein
basis function is positive in the interval’s interior.
An irrational tangency cannot become an endpoint of a finite rational subdivision.
Such a case needs another exact sign argument or the separately priced root-boundary
oracle; the proposed cheap checker is not a complete sign-decision procedure.

This is a sufficient, potentially stronger certificate shape: one assigned point must
work over a whole triangle and angle slab, although the true cover may switch points
inside it. No tiling, coefficient inventory, or target feasibility has been computed
here. H-104’s true Boolean verdict does not supply this certificate.
Unlike the unsuccessful uniform-core transfer above, this construction retains the
moving wall constraints; it does not shrink every square by one worst-angle factor.
Uniform shrinking, or a center shift without a complete containment-and-membership
argument, is not an alternative proof.

Endpoint samples and a denser angle grid are insufficient.
A fixed-axis core cover remains a useful sufficient test for an individual clause only
if its complete domain transfer is proved; the known loss rules it out as the sole route
to H-036. A hand-derived monotonicity argument or an exact uniform LP dual could replace
the Bernstein check where available, but neither may omit zero-slack faces or an
unproved coefficient sign.
If fixed tiles cannot close the obligation, retain the obstruction to that certificate
shape and reconsider the earlier event/feasibility-root design; do not automatically
build both instruments.

<a id="source-4-controls-independent-review-and-disposition"></a>

##### Controls, independent review, and disposition

Before target access, controls must establish:

- A constant-angle accepted source control retains its complete result; the moving
  center map preserves wall contacts and both orientation signs.
- Closed tile seams and corners survive; an omitted triangle or boundary is refused.
  A positive-area picture alone does not establish a closed cover.
- The nonnegative polynomial $w(1-w)$ keeps both zero endpoints, while $w^2-w+3/16$
  cannot pass from its positive endpoint values: its midpoint is negative.
  Mixed Bernstein signs, a dropped sign chart, a narrowed angle range, and a changed
  point label cannot produce acceptance.
- A source-distinct reviewer reconstructs the center map and four membership
  inequalities from the original coordinates, checks the tile union, and verifies the
  polynomial identities and sign certificates.
  The existing H-104 receipt reader does not establish continuous coverage.

The rational outer angle bound above remains safe for a positive result.
An escape in its added sliver is not a counterexample in the declared neighborhood.
A negative witness needs independent corner containment, strict point avoidance, and
certified membership in the actual angle interval.
One such witness rejects this continuous auxiliary clause even if other leaves remain
unchecked; it does not undo H-104 or refute H-036. Only an independently verified
eleven-square packing with $L<q$ and all eleven angles in the actual allowed family
refutes H-036. BC-256’s proof/falsifier counterpart therefore remains a separate bounded
allocation; failure to find a packing supplies no positive proof evidence.

<a id="source-4-conditional-price-and-stop"></a>

##### Conditional price and stop

Prefer a proposed **20–30 active-minute source/toy implementation slice** for the
fixed-domain tile and polynomial-sign checker, followed by **10–20 independent review
minutes**, before authorizing the earlier 60–120-minute general event build.
These are unmeasured effort estimates, not commissions or target-runtime estimates.
The exact partition machinery already used by the
[repaired source cover (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/cases/stromquist/repaired_cover.py) is a reuse
candidate; its contract must be checked for the new tile format.

At that boundary, require either a reviewed complete certificate interface with working
controls, or a named missing boundary/identity check and revised price.
Only then should the coordinator freeze a bounded target attempt and its independent
replay. Actual target runtime and the number of necessary tiles or angle slabs remain
unknown. No new target limit is adopted here.
Refusal by the cheaper certificate shape is not a mathematical negative, and does not
fund an automatic retry, changed points, smaller angle radius, or full event-root build.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
