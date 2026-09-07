# Tooling and Mathematical Machinery

This account is frozen at Git revision `4d305597a505ebfbe85f1851fa7148374661e622`.
Repository paths identify the source of each mechanism; the explanations and equations
below do not require that repository to be available.
This is an account of existing algorithms and proposed extensions, not a new
verification run.

The project studies the least container side $s(n)$ for $n$ freely rotating unit squares
with disjoint interiors.
Its strongest recorded lower bound for $n=11$ is $3.810025723614703\ldots$; the exactly
verified Trump construction has side $U=3.877083590022814\ldots$. The remaining gap is
approximately $0.067058$.

Three different mathematical tasks use overlapping software:

| Task | Input and successful output | Present capability |
| --- | --- | --- |
| Verify a construction | Exact square coordinates; containment and pair separation prove an upper bound | Implemented for rational and supported algebraic inputs |
| Exclude packings by a covering measure | A measure covering every possible one-square pose; total mass below $n$ proves a lower bound | Implemented for scalar shrunken-square atomic certificates |
| Classify every minimizing configuration | A complete case cover and a proof closing every case | Specialized small-$n$ results exist; global $n=11$ closure is open |

Current source and dated slice receipts determine implementation status.
Some older overview paragraphs still describe subsequently implemented components as
unbuilt. Conversely, a theorem contract or working control does not establish target
readiness.

## Exact Geometry and Algebraic Arithmetic

Represent square $i$ by center $c_i=(x_i,y_i)$ and perpendicular unit axes
$u_i=(\cos\theta_i,\sin\theta_i)$ and $v_i=(-\sin\theta_i,\cos\theta_i)$. Its corners
are $c_i+(\pm u_i\pm v_i)/2$. All four corners must belong to $[0,L]^2$. For a unit
direction $a$, its projection radius is

$$
r_i(a)=\tfrac12\bigl(|a\cdot u_i|+|a\cdot v_i|\bigr).
$$

The separating-axis theorem gives an exact finite pair test.
Squares $i,j$ have disjoint interiors precisely when, for some $a\in\{u_i,v_i,u_j,v_j\}$
and $\sigma\in\{-1,1\}$,

$$
\sigma a\cdot(c_j-c_i)-r_i(a)-r_j(a)\geq0.
$$

Equality permits an edge or corner contact.
A strictly negative best separation means overlapping interiors.
The code distinguishes an exact zero gap from absence of any separating axis; treating
both as a false Boolean would corrupt contact decisions.
Witness verification also checks the stated square geometry and its arithmetic
representation, rather than accepting arbitrary quadrilaterals as unit squares.

Rational rotations use $t=\tan(\theta/2)$:

$$
\cos\theta=\frac{1-t^2}{1+t^2},\qquad
\sin\theta=\frac{2t}{1+t^2}.
$$

Rational $t$ therefore supplies exact rational corners without approximating
trigonometry. For Trump’s witness, coordinates instead lie in $K=\mathbb Q(u)$, where
$u\in(36/100,37/100)$ is the isolated real root of

$$
5u^8-10u^7-2u^6+14u^5+12u^4-6u^3+2u^2+2u-1.
$$

The container side is $U=(6u+4)/(1+2u-u^2)$. A field element is a polynomial in $u$ with
rational coefficients, reduced modulo the defining polynomial.
Polynomial reduction decides equality.
Rational root enclosures and sign procedures decide order.
The constructor first certifies irreducibility and that the supplied interval isolates
exactly one real root.
It supports finite-field irreducibility certificates and a specified complete quartic
fallback; unsupported metadata is refused.
This is not a general algorithm for inferring a number field from decimal coordinates.

The exact Trump verifier checks all 55 pairs, including 14 pairs with zero separation,
and 20 corner coordinates on the container boundary.
Extra decimal precision does not replace the zero test: a tolerance can accept a small
overlap or reject a true contact.

Sources: `packing/src/sqpack/verify.py`, `packing/src/sqpack/field.py`,
`packing/src/sqpack/witness.py`, and `packing/cases/trump11/packing.py`.

## Fixed-Angle Cells, Linear Programs, and Quenching

Fix all angles and select one axis and order for every pair.
Every corner offset and projection radius is then constant.
The remaining problem minimizes $L$ over the $2n+1$ variables
$(x_1,y_1,\ldots,x_n,y_n,L)$ subject to linear containment and separation inequalities.
At $n=11$, this is a 23-variable linear program.
The full problem’s difficulty remains in the free angles and the discrete separation
choices: there are $8^{55}$ raw choices before pruning or identifying duplicates.

The numerical **quench** alternates such cell solves with local angle changes.
It chooses separation branches from the current pose, solves through SciPy/HiGHS, and
uses bracketing for angle classes that rotate several squares together.
Trump’s six axis-aligned squares and five equally tilted squares reduce one particular
structured cell to a one-variable side function $\varphi(a)$. Its optimum is a kink
where the active constraints change.
Smooth coordinate descent can miss that kink; bracketing addresses this mechanism.
There is no theorem that an unknown minimizer shares Trump’s two angle classes.

An independently assembled Trump cell LP uses all ordered corner-pair projection
inequalities instead of the compact support rows.
The formulations agree numerically to approximately $4.4\times10^{-16}$ on that control.
This checks their assembly for the selected cell.
It does not cover other cells or all angle vectors.

An exact LP implementation is also present.
Given $\min c^Tz$ subject to $Az\leq b$, it can obtain a feasible basis through an
auxiliary phase-one program and then pivot with Bland’s rule over rational or accepted
algebraic coefficients.
A returned optimal vertex carries active rows $S$ and multipliers $y$, checkable by

$$
A_Sz=b_S,\quad Az\leq b,\quad A_S^Ty=-c,\quad y\geq0.
$$

These identities prove $c^Tx\geq c^Tz$ for every feasible $x$, without trusting the
pivot search. Pivot limits and singular bases yield explicit refusals.
A phase-one infeasibility determination still needs exported, independently replayable
multipliers before a new external proof can use it as a Farkas certificate.

The high-throughput quench remains numerical.
Its recorded side floor is roughly $10^{-11}$, and coordinatewise stopping does not
prove stationarity or a local minimum.
The exact LP is a useful leaf solver; it does not supply an exhaustive
configuration-space decomposition.

Sources: `packing/src/sqpack/research/quench.py`,
`packing/cases/trump11/independent_lp_cell.py`, and `packing/src/sqpack/exact_lp.py`.

## Proposal, Refinement, and Construction Certification

The retained search proposer is a Rust annealer using binary64 geometry and overlap
penalties. It proposes numerical poses; the quench refines them; a separate verifier
determines whether a retained pose is a construction.
Search-side pair evaluations are counted, but a common equal-work interface for
comparing different proposers remains unbuilt.
Billiard/inflation, continuation, neighbor transfer, and diversity-based retention
appear as proposed mechanisms, not interchangeable implemented engines.

The initial $n=11$ baseline’s best side was approximately $3.91441654$. Tested bracketed
quench starts retained a residual near $0.0629$ above Trump.
A separate near-Trump experiment obtained zero returns in 40 tested perturbation trials.
Those observations constrain the tested generator and stopping rules; they do not
establish that Trump is the only useful basin or that a better configuration is absent.

For a promising decimal construction, two certification paths exist.
Rational promotion converts centers and rotations to rational data, permits an
explicitly bounded container dilation, and exactly verifies the resulting new pose.
Contact reconstruction instead infers typed equations, proposes algebraic relations, and
uses directed interval methods such as Krawczyk inclusion to certify a root in a box.
Ambiguous contacts and singular systems must remain unresolved.
Generic components of the latter path exist, and a case-specific $n=29$ driver has
produced a verified upper bound; arbitrary witness-to-interval certification is not
exposed as a completed general route.

Endpoint keys and contact counts also do not identify connected components.
The exact $n=3$ optimal family supplies a counterexample: one connected family has
multiple geometric keys.
Consequently a saturation curve of stored endpoint keys cannot certify exhaustive
search.

Sources: `packing/sqsearch/src/main.rs`, `packing/src/sqpack/promote/`, and the search
evidence in `SYNOPSIS.md`, sections “Experiments Conducted” and “What the 71 Rounds
Jointly Establish.”

## Trump’s Tangent Cones and the Local Endpoint

At Trump’s exact pose, the active wall and pair features have finitely many tied
separation descriptions.
Retaining all ties gives 512 raw selections, reduced by exact derivative equality to 128
branches. Each branch has a $42\times33$ matrix $A_b$ in the labeled, anchored
center-and-angle chart with side fixed at $U$.

Each retained branch has rank 33 and a strictly positive stress $\lambda_b$ satisfying
$A_b^T\lambda_b=0$. If $A_bv\geq0$, then $\lambda_b^TA_bv=0$ forces every component of
$A_bv$ to vanish; rank forces $v=0$. Thus every branch’s first-order feasible cone is
zero. A finite-branch subsequence argument upgrades this to qualitative local isolation.

The quantitative calculation uses

$$
\kappa_b=\min_{\|w\|_\infty=1}\max_j(-(A_bw)_j).
$$

The sup-norm sphere is the union of 66 cube faces.
Each face calculation is an LP. If the nonlinear row remainder satisfies
$|R_j(v)|\leq K_j\|v\|_\infty^2/2$, a positive modulus prevents sufficiently small
nonzero feasible displacements.
Inactive-feature, chart, and symmetry bounds ensure that no missing local branch
invalidates that inference.

The preferred retained radius is $\rho=808514697/200000000000=0.004042573485$ in this
mixed center/radian sup norm.
Every packing with side at most $U$ within that strict radius is the same labeled pose
and has side exactly $U$. A separate stress calculation gives
$\sigma\geq-C\|v\|_\infty^2$ for side $U+\sigma$, with $C=2574612531/200000000$.

BC-241 accepted the theorem at **retained-record-dependent local scope**. It replayed
the tangent certificates, checked aggregate arithmetic, audited selected faces, and
rejected mutations. The full 128-by-66 uniform and weighted face witnesses are absent;
the entire radius generator was not independently replayed.
The theorem’s older “awaiting review” header is historical, but this remaining replay
boundary is current.

To use this endpoint globally, another argument must show that every minimizing
configuration at side at most $U$, after a valid symmetry and relabeling, enters this
ball. Increasing confidence in the local calculation supplies no such capture.

Sources: `packing/cases/trump11/isolation-theorem.md`,
`packing/cases/trump11/tangent_cones.py`, and
`packing/campaign/series/series-000-smoke-and-calibration/results/bc-241-trump-local-theorem-review.json`.

## Atomic Covering Certificates and the All-Angle Reduction

A scalar fractional certificate consists of rational $L,B>0$, a nonnegative atomic
measure $\mu=\sum_jw_j\delta_{p_j}$ in $[0,L]^2$, and rational half-angle parameters
$0=t_0<\cdots<t_K<1$. They define exact directions $\alpha_k=2\arctan t_k$. The measure
is invariant under the container’s eight dihedral symmetries.
The final direction reaches the folded endpoint $\pi/4$, checked by $t_K^2+2t_K-1\geq0$.

For adjacent directions, the half-gap tangent is

$$
D_k=\frac{t_{k+1}-t_k}{1+t_kt_{k+1}},\qquad D=\max_kD_k.
$$

The scalar verifier requires $B(1+D)<1$, total mass $M<n$, and coverage at least one for
every contained closed $B$-square at every net direction.
Given an arbitrary unit square, reflection into the folded arc and a nearest net
direction provide a concentric core whose width in the unit square’s frame is at most
$B(1+D)<1$. Pull the core back through the same symmetry.
Measure invariance preserves coverage.
The core lies strictly inside the original square, so cores from interior-disjoint unit
squares are disjoint even as closed sets.
Therefore

$$
n\leq\sum_{i=1}^n\mu(P_i)\leq M<n,
$$

a contradiction. The resulting bound concerns $L$, not $L/B$. Reflection is a proof
reduction for one square and the common measure; independently reflecting squares in an
actual packing would change their compatibility.

T-018 uses 1,121 atoms, 181 directions, $B=9977/10000$, $M=434547/40000$, and minimum
covered mass $4001/4000$. Its lower side is $381/100$. T-022 improves only the
containment/dilation step, giving the weak limit endpoint
$38100\sqrt{8100042893309449}/899996306539$. It provides no endpoint no-fit certificate.
Fixed-weight shrinking has subsequently met exact obstructions; changing sites, relative
weights, directions, or witness shapes remains a different question.

Sources: `packing/src/sqpack/fractional/certificate.py`,
`packing/cases/n11_fractional_certificate/t-018-proof-card.md`, and
`packing/cases/n11_fractional_certificate/t-022-dilation-limit-proof.md`.

## Exact Event Sweeps and Independent Interval Coverage

At a fixed net direction, rotate centers and atoms to square-frame coordinates $(u,v)$.
Atom $j$ is covered exactly when the center belongs to

$$
R_j=[u_j-B/2,u_j+B/2]\times[v_j-B/2,v_j+B/2].
$$

The rectangle boundaries partition center space into finitely many event cells.
Coverage is constant on every open cell.
A two-dimensional difference array followed by prefix sums accumulates each rectangle’s
weight across the grid.
Rational weights are scaled to exact integers; overflow guards precede integer
accumulation, with a rational route available outside the fast range.

Only cells intersecting the actual containment domain are relevant.
That domain is a rotated polygon in $(u,v)$ coordinates; its bounding box alone admits
impossible placements.
Exact clipping or contiguous-span reduction identifies reachable cells.
Because the square is closed and weights are nonnegative, a boundary includes the atoms
from its incident cells and cannot reduce their mass.
Empty or lower-dimensional domains require their own treatment or an explicit refusal;
they cannot silently disappear as successful coverage.

The retained $3.81$ decision covers 567,130,649 reachable cells.
This is a finite continuum decision, not a sample of that many independent placements.

The second verifier uses directed-rounding interval boxes, with a separate coverage
argument. For a center box $X$, sum weights only when a certified inner enclosure of
$R_j$ contains all of $X$. This gives a lower bound valid throughout $X$. Propagate the
containment half-planes, discard provably empty boxes, and bisect the remainder.
Accept coverage only when every surviving leaf has mass at least one.
A verified contained point with an upper mass bound below one refutes the candidate.
Resolution or box limits leave the answer undecided.

This route checks a doubled direction net directly instead of invoking the symmetry
reduction. Both approaches still share certificate data and some foundations, but their
continuum decisions differ.
Exactly coincident rectangle seams can prevent an interval proof even when an exact
event proof succeeds; such refusal is not a mathematical obstruction to the candidate.

Sources: `packing/src/sqpack/fractional/sweep.py`,
`packing/src/sqpack/fractional/interval.py`, and
`packing/cases/n11_fractional_certificate/minimal_verify.py`.

## Generating Measures and Bounding Their Possible Reach

For fixed sites grouped into distinct $D_4$ orbits $O$, use weight $w_O$ per site.
The covering LP is

$$
\min\sum_O|O|w_O,
\qquad \sum_O a_{rO}w_O\geq1,\quad w_O\geq0,
$$

where $a_{rO}$ counts sites of orbit $O$ covered by placement row $r$. Orbit sizes can
be less than eight; multiplying every orbit by eight changes the problem.

The row-generation loop solves a finite relaxation, finds low-coverage placements at the
net directions, adds violated rows, and repeats.
Between directions the containment theorem supplies coverage.
Floating solutions propose rationalized weights; only exact decision and independent
replay can retain a packing bound.

Column generation also changes the site set.
If $y_r$ are dual row weights, an orbit has reduced cost $|O|-\sum_ry_ra_{rO}$. Negative
reduced cost identifies useful new sites.
Searching the dual placement arrangement for excessive depth supplies such columns.
A coordinate perturbation changing no site/placement incidence cannot change the fixed
incidence LP.

A separate finite family of closed placements with nonnegative weights $y_r$ and
pointwise depth $d(x)=\sum_ry_r\mathbf1_{P_r}(x)\leq1$ gives

$$
\sum_ry_r\leq\sum_ry_r\mu(P_r)=\int d\,d\mu\leq M.
$$

Thus exact total weight at least eleven proves a ceiling for that covering method.
It does not prove that eleven unit squares fit.
For finite closed polygons, maximum pointwise depth occurs at an arrangement vertex: a
polygon containing an open face contains its closure.
The exact depth checker can therefore enumerate vertices, including all relevant
equality cases.

At side $3.82$, the retained exact fractional lower endpoint is
$21342289572/2055263195\approx10.384212408$. The retained row-converged computational
upper endpoint is $11.0556169429\ldots$. That upper number is not an exact accepted
covering measure. Later unconverged objectives cannot improve it by declaration.
The finite interval has not established a method ceiling at eleven.

An external strategy must also account for the scalar shrink cap: the existing
$(B,\text{net})$ fits disjoint cores inside a scaled Trump construction near side
$3.868983$, preventing that fixed mechanism from reaching $U$. A finer net, richer
witnesses, a proved limiting family, or configuration-level argument is necessary to
close the final gap.

Determining the value and proving uniqueness are separate goals.
An analytically proved family of global lower bounds $L_k\uparrow U$ would already
establish $s(11)=U$, using the known construction; it would need neither an endpoint
certificate nor a local uniqueness theorem.
A finite numerical ladder does not establish that family.
When only a fixed lower bound below $U$ is available, local isolation cannot remove the
remaining global gap without a capture argument.

Sources: `packing/src/sqpack/fractional/generate.py`,
`packing/src/sqpack/fractional/colgen.py`, `packing/src/sqpack/fractional/cutting.py`,
`packing/src/sqpack/fractional/ceiling.py`, and
`packing/campaign/explorations/X-014-closing-from-both-ends.md`.

## Adaptive Cores and Richer Witnesses

BC-230 assigns a rational core side $B_k$ to each direction’s exact ownership cell.
Adjacent angular seams have rational tangent $q_k=(t_{k-1}+t_k)/(1-t_{k-1}t_k)$. The
cells partition $[0,\pi/4]$, with explicit ownership of zero, the fold, and every seam.
For direction tangent $a_k=2t_k/(1-t_k^2)$, the largest endpoint mismatch is the maximum
of $|a_k-q|/(1+a_kq)$. The accepted contract requires $B_k(1+D_k)<1$ cell by cell.
The same disjoint-core counting proof applies.

Two control slices have implemented geometry adapters, two project coverage routes, and
a bounded exact JSON loader.
A nonuniform five-atom control at side $6/5$ has core sides $7/10,3/4,4/5$ and checked
minima $6/5,13/10,7/5$. The loader validates structure and declarations; loading is not
a coverage verdict. An independent standalone checker, three-route receipts, full
retained-source replays, and remaining boundary controls are incomplete.
The current estimate is 180–320 active worker minutes plus unpriced replays; no adaptive
target result exists.

Angle-cell polygons could retain more useful mass than square cores.
Their required property is strict containment throughout a complete angle cell, followed
by a coverage decision for every allowed center.
More polygon area alone does not help if it captures no additional positive mass.
Existential menus instead require $\forall$ pose $\exists$ a strictly interior heavy
witness, including every pose-box boundary.
Nested concentric choices add no advantage over their largest uniformly admissible
member. Segment measures require exact intersection-length integrals; binary segment-hit
tests do not decide their coverage.
These are conditional designs, not completed alternatives to the scalar verifier.

Sources:
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-230-adaptive-core-contract.md`,
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-231-next-phases-slice-02.md`,
and `docs/project/specs/active/plan-2026-09-06-post-381-research-sequence.md`.

## Full-Size Area Densities and Complete Depth Verification

BC-242 proposes a different boundary convention.
Let $P_L$ be all contained full-size unit-square placements.
The primal seeks $\rho\in L^1_+([0,L]^2)$ satisfying $F_\rho(p)=\int_{S_p}\rho\geq1$ for
every $p\in P_L$, minimizing $\int\rho$. Square boundaries have zero area, so a mass
below eleven excludes eleven interior-disjoint unit squares without shrinking them.

The dual permits finite nonnegative measures $w$ on placement space with
$d_w(x)=\int\mathbf1_{S_p}(x)\,dw(p)\leq1$ almost everywhere in area.
Tonelli’s theorem gives $w(P_L)\leq\int\rho$. An exact dual value greater than eleven at
$U$ would therefore rule out a mass-eleven equality density in this class.
It would leave Trump’s optimality and useful densities at smaller sides unresolved.
Strong duality, attainment, and complete primal continuum verification remain open.
Singular measures cannot inherit this almost-everywhere boundary argument.

The current finite support is the deduplicated dihedral closure of Trump’s eleven
squares: 88 labeled images, 60 distinct placements, eight orbits.
Averaging the eight valid packings gives mass eleven.
Exp-113 optimized arbitrary nonnegative orbit weights subject to 20 exact necessary
depth rows. Its independently replayed optimum is $56/5$, giving the *fixed-support*
interval $[11,56/5]$. The maximizing weight vector, per distinct member of each orbit,
is

$$
(1,0,2/5,1/10,0,1/10,3/10,0),
$$

with orbit sizes $(4,8,8,8,8,8,8,8)$. Each sampled row is proved constant on a
positive-area neighborhood off all boundaries; this makes it necessary for a.e.
feasibility. The finite-row upper certificate is valid, while the candidate’s global
depth remains unverified.

Exp-115 checked all 134 pairs whose weights sum above one and retained independent
separating axes for each.
This rules out an overweight-pair obstruction.
Three or more lower-weight overlapping squares can still exceed unit depth, so
higher-order depth remains unresolved.

The next proposed complete verifier uses the 36 positive-weight placements.
Their supporting lines and the container walls number at most 148 before deduplication.
Depth is constant on each positive-area arrangement face.
Boundary lines themselves are null and must not be scored as violations.

The proposed **facet procedure** deduplicates lines exactly, clips them to the
container, splits at every intersection, and probes both sides of every nondegenerate
open segment.
Choose a rational displacement small enough to cross only the segment’s own
line. Every positive-area face has an open boundary segment, so these probes cover all
faces. A violating probe yields an exact point and positive-area box whose depth exceeds
one.

The proposed independent **slab procedure** reconstructs the geometry separately, sorts
all vertical lines and intersection x-coordinates, and chooses one vertical line inside
each resulting open slab.
Each square cuts that line in an open interval.
Sweep weighted interval endpoints, grouping equal endpoints, and score each nonempty
open band. Their ordering cannot change inside a slab without a recorded event.
Exceptional x-lines have area zero.
This gives a separate completeness argument; checking only the producer’s supplied
probes would not.

Neither complete route is implemented at this snapshot.
Required controls include touching packings, triple overlaps without overweight pairs,
coincident and parallel lines, concurrent intersections, omitted segment sides/slabs,
zero-weight boundaries, and malformed witness margins.
Both routes will share the exact field kernel and original source, which limits their
independence. An external reviewer can improve the completeness argument, propose a
smaller exact certificate, or reject the current candidate with one positive-area depth
witness without accessing the full codebase.

Sources:
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-242-full-size-density-proof-contract.md`,
`packing/src/sqpack/full_size_density/support_ceiling.py`,
`packing/src/sqpack/full_size_density/pair_separator.py`, and
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-254-post-screen-next-discriminator.md`.

## Restricted Structure and a Global Proof Cover

BC-245 supplies a finite typed language for minimizing configurations.
Compactness of the feasible sublevel $L\leq U$ gives existence of a minimizer.
On each angle chart, select one pair separation per pair and resolve support absolute
values by closed sign cases.
Retain all wall, inactive, tied, and zero-multiplier constraints.
Fritz–John necessity gives

$$
\alpha\nabla L-\sum_j\lambda_j\nabla g_j=0,\qquad
\lambda_jg_j=0,\qquad \alpha,\lambda_j\geq0,
$$

with multipliers not all zero.
Both $\alpha>0$ and abnormal $\alpha=0$ branches remain necessary unless a constraint
qualification is proved.
Movable rattlers also remain configuration variables.
Contact incidence alone neither determines these equations nor justifies deleting
noncontact inequalities.

A proposed global solver would generate branches lazily, eliminate centers with exact
LP/Farkas arguments, exclude angle boxes by intervals, and isolate algebraic roots only
in surviving leaves.
It must prove that every minimizer belongs to an enumerated branch and that every
surviving box is either excluded or captured by the local Trump theorem.
No such global solver or credible complete $n=11$ runtime is available.
The existing 11,013 abstract size-five scaffolds are geometry-free orbits, not
stationary packings.
Exact $n=3,4$ optimal classifications provide completeness controls; the $n=5$ local
result does not classify all its optima.

The archived contact literature supplies hypotheses to check, not a shortcut around
these cases. Dewar’s $2n-2$ bound for face-to-face contacts assumes a weak generic
condition on the square radii.
Eleven equal radii violate that condition.
It therefore does not supply a contact-count cap for the target problem.
Smooth-particle jamming theorems likewise require justification at square feature ties.

The current restricted route H-036 concerns only angles within $0.25^\circ$ of $0^\circ$
or $45^\circ$, modulo quarter turns, and seeks $L\geq3.878$. It extends Stromquist’s
conditional point-cover argument: a ten-point cover localizes an exceptional square,
that square captures three designated points, and a twelve-point cover leaves too few
points for the other ten squares.
Scaling a putative smaller packing before applying closed unit witnesses ensures
interior ownership of points.

Exp-114 proved seven auxiliary clauses at exactly $0^\circ,45^\circ$. Continuous angle
coverage remains open.
The next design maps each angle-dependent center domain from a fixed unit square,
triangulates it, assigns a marked point to each tile, and certifies vertex membership
inequalities throughout each closed angle interval.
Half-angle substitution makes these low-degree polynomial inequalities.
Nonnegative Bernstein coefficients give a sufficient sign certificate; mixed
coefficients are inconclusive, including at interior tangencies.
A complete event/root engine is a separately priced alternative.

Even full H-036 acceptance would exclude only that restricted family.
Trump’s approximately $40.18^\circ$ tilt lies outside it.
The reviewer should identify how this case result would reduce a complete global cover,
or propose a stronger conditional statement with a demonstrable route to capture.

Sources:
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-245-typed-backbone-theorem-packet.md`,
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-restricted-angle-assessment.md`,
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-angle-instrument-design.md`,
and `packing/resources/papers/dewar-2024-contacts-oriented-squares.raw.md`, Theorem 1.1
and Corollary 5.2.

## Research Records and What a Reviewer Can Change

The record distinguishes hypotheses, prospective experiments, execution receipts,
theorem claims, and workflow completion.
An experiment freezes its candidate family, controls, acceptance rule, and budget before
measurement. Results distinguish exact obstruction, failed numerical search, verifier
refusal, and incomplete execution.
A control can establish correct implementation while leaving its research hypothesis
open.
Independent replay may share arithmetic or source data; that dependence is reported
rather than counted as full independence.

The retained Lean spike has nine source proofs for counting, symmetry, and scalar
inequalities. This host has not replayed their pinned build and axiom audit.
Oriented square geometry, continuum coverage, and the headline packing theorem are not
formalized. The existing lower bounds are computer-assisted results with explicit
mathematical arguments and exact/interval decisions.

For a new proposal, specify the quantified configuration or measure class, the
certificate it would produce, why that certificate implies a stronger bound or global
capture, and a small discriminator against the known obstructions.
Configuration selection cuts, Hall constraints, and compatible-cell hyperedges require
variables for a whole packing; inserting them into the one-body covering LP changes the
proof without justification.
A useful alternative may be a hand-derived wall-to-wall inequality, a conditional cover,
or another global invariant.
It need not preserve the current software architecture, but its completeness and
boundary obligations must be stated.

Sources: `packing/campaign/README.md`, `epistemics.md`,
`packing/cases/n11_fractional_certificate/lean-spike/README.md`, and
`docs/project/reviews/review-2026-09-05-strategy-gpt-56-pro-gemini-grok.md`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
