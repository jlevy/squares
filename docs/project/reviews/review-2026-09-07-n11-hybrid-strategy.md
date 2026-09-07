# Strategic Mathematical Review: Hybrid Exclusion and Few-Angle Structure at n = 11

**Draft for discussion, 2026-09-07. New research IDs remain placeholders.**

The proposed hybrid work fits Agenda 027’s mathematical program.
Keep that agenda, add a focused exploration provisionally called **X-TBD-HYBRID**, and
develop its conditional-resource and angle-structure questions through narrower
experiments. The strongest immediate addition is an angle-first branch-and-bound method
that uses coupled translation LPs and certified small-subsystem resource inequalities.
It can cover unrestricted configurations while a separate structural investigation asks
whether some minimizing representative has only one nonaxis angle.

The few-angle idea is worth pursuing.
Trump’s exact packing supplies a precise mechanism: positive-length side contacts
connect six squares to the container’s orientation and connect the other five to one
common orientation. The missing theorem is that a suitable global minimizer must admit
such an angular simplification.
Boundary contacts, contact counts, and numerical recurrence alone do not establish it.
The direct exclusion program can proceed while that theorem remains open.

This draft contains the strategic assessment, proposed exploration, agenda additions,
and hypothesis templates.
The templates are discussion material, outside the enforced campaign registries.
They allocate no scientific identifiers or experiment budgets.

## Reviewed Sources and Branch Relationship

The review covers the scientific changes, retained outcomes, source assessments,
proposed claims, and relevant machinery on both branches, with three bounded independent
assessments. It is a strategic review, not a fresh replay of every proof receipt or a
line-by-line software audit.

| Source | Reviewed identity | Scope |
| --- | --- | --- |
| [PR #105](https://github.com/jlevy/squares/pull/105) | Scientific checkpoint `f5684f51fea68fd02ce60fe875e50c4383034e83`; closeout `54d1ca98bf53a02d337e9d90b8dea7cca5af0169`; priority amendment `6d8b2b38cf696a82ed7cc5b9ad6744ba7e439312` | 109 changed files from `4d305597` through the amendment: scalar production and completion, density algorithms and controls, continuous restricted-angle results, Session 090, and source handoffs |
| [PR #107](https://github.com/jlevy/squares/pull/107) | Reviewed base `54ad6bc1f6dfe30b7294a7e804358e5f92265a4c` | Its 70-file change from shared checkpoint `6d8b2b38`: contributed research archive and replay, X-017, Agenda 027, H-111–117, and campaign identity safeguards |
| Earlier hybrid spikes | Local stash `8f6592818f17f1cea83a617bb11ed6ffd6e112a6`, based on `4d305597` | Unpublished instruments and receipts; the mathematical arguments needed for this strategy are included below. The raw interval counts and tests cannot be replayed from this PR alone. |

The publication branch stacks on PR107’s `54ad6bc1`, which incorporates PR105’s
`54d1ca98` closeout and `6d8b2b38` priority amendment and uses X-017 as the final
exploration identity.
The
[revised Session 090 handoff](https://github.com/jlevy/squares/blob/6d8b2b38cf696a82ed7cc5b9ad6744ba7e439312/packing/campaign/agent-sessions/session-090-four-hour-research.md)
keeps H-110 selected, defers H-107 from the next two-hour block, and selects a short
conditional-compatibility assessment alongside H-110. Neither source update changes a
scientific verdict. The publication diff adds this single review and its two navigation
entries; the source allocations retain their coordinator.

The inherited strategy was reviewed through
[X-014](../../../packing/campaign/explorations/X-014-closing-from-both-ends.md),
[X-015](../../../packing/campaign/explorations/X-015-the-map-and-the-three-programs.md),
[X-016](../../../packing/campaign/explorations/X-016-after-381-two-managers-one-proof-boundary.md),
the
[Agenda 024 portfolio](../../../packing/campaign/agendas/agenda-024-post-381-24h-portfolio.md)
and its two children, and
[Session 090](../../../packing/campaign/agent-sessions/session-090-four-hour-research.md).
PR107’s
[X-017 exploration](../../../packing/campaign/explorations/X-017-compatibility-and-complete-case-covers.md)
accounts for both contributed mathematical reports, their combined agenda, supplied
checkers and controls, the frozen source packet, and directions not selected for the
opening allocation.
Its latest archive cleanup retains the research text, delivered PDFs,
mathematical code and replay evidence in Git; the complete upload and publishing assets
remain in the source coordinator’s attic.
The research text and mathematical evidence are unchanged.

## The Mathematical Position After Both Branches

Let $s(11)$ be the least side of a square containing eleven closed unit squares with
pairwise disjoint interiors.
Touching is legal, and every square may rotate independently.
The retained bracket is

$$
\frac{38100\sqrt{8100042893309449}}{899996306539}
\le s(11)\le U,
\qquad
3.810025723614703\ldots\le s(11)\le3.877083590022814\ldots.
$$

The lower endpoint is T-022’s weak limit consequence of T-018’s exact $3.81$
certificate. It is not a separate no-fit certificate at the limiting endpoint.
The upper endpoint is Trump’s verified construction.
Its exact representation is

$$
U=\frac{6u+4}{1+2u-u^2},\qquad
5u^8-10u^7-2u^6+14u^5+12u^4-6u^3+2u^2+2u-1=0,
\quad \frac{36}{100}<u<\frac{37}{100}.
$$

The [result register](../../../packing/frontier/RESULTS.md),
[dilation proof](../../../packing/cases/n11_fractional_certificate/t-022-dilation-limit-proof.md),
and [exact Trump construction](../../../packing/cases/trump11/packing.py) own these
claims. Neither branch closes the gap.

| Work | Current evidence | Strategic consequence |
| --- | --- | --- |
| Global fractional certificate | T-018 proves $s(11)\ge3.81$; T-022 sharpens containment slightly | A working proof mechanism exists. Improvements can target approximation, optimization, or configuration compatibility separately. |
| Fractional frontier at $3.82$ | The later exact packing-family floor is $21342289572/2055263195\approx10.384212408$; the separate computational covering objective is about $11.055616943$ | This remains an unresolved bracket. Neither number proves a universal barrier at $3.82$. |
| Scalar attempt at $61/16$ | Exp-116’s 19 row solves were unconverged. Its independently checked depth-one family has mass $20843712108/2067791663\approx10.080180$, below eleven | H-093 remains unresolved. The unchanged attempt is closed to retries; H-107 is a changed fixed-site completion protocol. |
| Fixed-site completion | H-107’s adapter, input identity checks, controls, and protocol are reviewed; exp-118 never launched. The latest source priority amendment defers the test under paused `think-7fec`. | It can produce a checked certificate but has no exact finite-site dual rejection path. Failed convergence, a high numerical objective or failed certification leaves even the frozen-site claim unresolved. Readiness does not allocate a run. |
| Full-size density | Complete facet and slab mechanisms exist; the original source passes, but three distinct algorithms exhaust the uniform-source cap | The candidate target remains unopened. This is an instrument cost problem, without a mathematical impossibility verdict. |
| Restricted orientations | H-106 proves continuous near-axis P10 coverage throughout the closed $\pm0.25^\circ$ interval at $1939/500$. H-108 proves canonical near-45 A3 forcing; H-109 proves A1 and transfers A2 by reflection | The auxiliary continuous mathematics has advanced. Near-45 localization, the remaining P12 obligations, and H-036’s full theorem remain open. |
| Current source handoff | H-110 specifies an unevaluated fixed P12 escape candidate. The latest amendment adds a 30-minute BC-255/H-102 conditional-compatibility derivation and review using accepted A-point forcing; H-107 is deferred. | Preserve the source allocation. An H-110 escape would reject the unchanged P12 formulas, not H-036. The compatibility assessment proposes necessary structure; conditional coverage and strict interior incidence remain unproved. |
| Trump local theorem | A labelled, anchored 33-coordinate neighborhood has preferred retained radius $808514697/200000000000$; the reviewed implication depends on retained BC-199 data | It is a possible terminal lemma for a global cover. The review did not independently replay every radius face witness, and global capture remains unproved. |

The fractional continuation is recorded in
[exp-070](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-070-h-064-n11-fractional-resume.md);
the recent results are recorded in Session 090 and
[Agenda 026](../../../packing/campaign/agendas/agenda-026-density-stationarity-and-trump-capture.md).
The latest source allocation is in
[Agenda 024 at `6d8b2b38`](https://github.com/jlevy/squares/blob/6d8b2b38cf696a82ed7cc5b9ad6744ba7e439312/packing/campaign/agendas/agenda-024-post-381-24h-portfolio.md#selected-continuation-after-session-090).
Its conditional-compatibility assessment gives a concrete connection to the hybrid
proposal: accepted forcing can restrict a configuration before a local resource is
applied. The source assessment must still establish the required localization, coverage,
and interior-incidence premises; it is separately owned and scheduled.
The [local theorem packet](../../../packing/cases/trump11/isolation-theorem.md) must be
read with BC-241’s retained-record qualification, rather than its older status line.

The earlier hybrid drafts need these updates before incorporation.
Their statements that scalar $61/16$ was unopened, only exact-angle auxiliary proofs
existed, or complete density mechanisms were unimplemented describe their older
snapshot.

## What PR107 Adds Mathematically

The most consequential contributed calculation is a proposed seven-row ceiling of eleven
for H-099’s fixed sixty-placement Trump-D4 support.
Seven positive-area incidence regions give necessary depth inequalities whose rational
combination bounds the support’s total weight.
The average of the eight feasible Trump images supplies the matching value eleven.
A further region gives depth $7/5$ for the older $56/5$ candidate, consistent with the
earlier failure to find an overweight overlapping pair: higher-order overlap can violate
depth without such a pair.

The supplied checker replays, but independent binding of all 88 images to the 60
placements, orbit order, weights, and exact geometry remains BC-259’s acceptance work.
If accepted, this can resolve the unchanged support question without the expensive
candidate computation.
It would leave expanded supports, other measures, and transport to smaller containers
open. A support optimum of eleven at $U$ is not a global equality-density theorem.
See the
[contributed proof and its scope](../../../packing/resources/papers/n11-complete-research-bundle-2026-09-07/original_review/n11_research_review.md).

The contributed physical stationarity argument is also useful.
It uses variable side, open angle charts, all physical wall inequalities, and sixteen
smooth corner-projection inequalities for each selected pair separation.
Dilating centers and container while keeping unit squares fixed provides a strict
feasible direction for active physical rows.
The proposed consequences include normal KKT, bounded multipliers, and a stress
certificate supported on at most 34 scalar rows.
BC-267 should review these claims in that formulation.
The argument does not remove abnormal-case obligations from an unchanged fixed-side or
artificially constrained formulation.

Fixed-angle LP vertices and finitely many semialgebraic stationary side values are
existence reductions.
They do not give finitely many configurations, a practical count of contact patterns, or
an angle bound. Stress support, translation-basis rank, and orientation-contact rank
count different objects.

The remaining contributions have distinct roles:

| Direction | Existing home | Assessment |
| --- | --- | --- |
| Complete resource/anchor exclusions at $96/25$ | H-111; BC-260–262 | Closest fit for aggressive hybrid pruning |
| Six axis squares and five sharing one free angle, with all contacts free | H-112; BC-263 | A useful theorem target even before a global normal form is known |
| At most two arbitrary absolute orientations, all multiplicities | H-113; BC-266 | Broader than the axis-plus-one-angle family |
| Two-pose positive-semidefinite interaction kernels | H-114; BC-264 | A distinct compatibility mechanism, with a costly continuum pair-domain obligation |
| Curved boundary-null resources and expanded full-size support | H-115/116; BC-265 | Preserve as candidate-led alternatives; the fixed support result does not settle them |
| Forced angular complexity in minimizing representatives | H-117; BC-267 | The natural home for the flush-square intuition and contact-release argument |

The prepared
[Agenda 027](../../../packing/campaign/agendas/agenda-027-compatibility-and-restricted-families.md)
already separates these programs.
Consolidation should retain that separation of mathematical claims within one
coordinated agenda.

## What the Earlier Spikes Establish

The four earlier instruments are useful evidence for implementation choices.
Their claims must retain their exact domains and their separate draft provenance.

| Spike | Established at its tested scope | Remaining step |
| --- | --- | --- |
| Conditional weights | At side $3.9$, four selected near-axis slots in one horizontal band each capture weight at least one from three common atoms; all six independent pair screens remain unresolved, but total demand four exceeds mass three | Compare against coupled LP geometry. The target is a restricted four-slot conjunction, not a global $n=11$ exclusion. |
| Angle counts | Exact inner-core arguments at side at most $3.88$ force at least two squares away from the axes and at least one away from both axes and diagonals. An abstract resource example also distinguishes integer counts from fractional counts | Actual geometric multi-resource rows are needed to improve the composition pruning. The example supplies no upper bound on rotators. |
| Interval separation | With center-coordinate radius $1/1000$ and angular displacement at most $2\arctan(1/1000)$ around Trump, 41 of 55 pairs are uniformly separated; the 14 unresolved pairs have 512 raw combined label choices before joint consistency | Export interval endpoints and selected constraints into replayable LP leaves. This box differs from the local theorem’s center/radian sup-norm ball; every tested Trump box contains a feasible packing. |
| Orientation graph | Exact contact classification gives Trump six wall-anchored squares and one unanchored five-square component; angular forest rank ten. Göbel and rational fixtures distinguish points from segments and show that graph nullity need not imply motion | Prove a structural implication beyond the known source packing. The graph does not determine rattlers; Göbel’s unanchored angle is constrained by other contacts. |

For the weight control, the four center domains are $[1/2,17/5]\times[19/10,2]$, with
$|\tan(\theta/2)|\le1/1000$. Strict axis cores of side $9977/10000$ meet at least one of
the three atoms $(99/100,39/20)$, $(39/20,39/20)$, $(291/100,39/20)$, each of weight
one. The exact sweep has 33 event strata.
Three axis unit squares centered at $(1/2,39/20)$, $(39/20,39/20)$, and $(17/5,39/20)$
give a feasible equality control.
The seven other squares can have zero guaranteed capture.
This proves the four-slot branch impossible at $3.9$, where Trump itself fits elsewhere.

The capacity proof can be checked analytically without the unpublished sweep.
For an orientation mismatch bounded by $2\arctan t\le\pi/4$, write

$$
R(t)=\frac{1+2t-t^2}{1+t^2}.
$$

A concentric core aligned to the reference orientation, of side $b$, lies strictly
inside its unit square when $bR(t)<1$. For this control,

$$
1-\frac{9977}{10000}R(1/1000)
=\frac{3065977}{10000010000}>0.
$$

Every atom is at vertical distance at most $1/20<b/2$ from any allowed center.
Adjacent horizontal atoms are $24/25<b$ apart; their open radius-$b/2$ intervals overlap
and cover the full center interval $[1/2,17/5]$. At least one atom is therefore strictly
inside every selected core.
Disjoint unit-square interiors cannot share such an atom, giving capacity three for the
band.

These results support a mechanism: localizing several poses can turn a weak global
resource into a useful joint exclusion.
The following analytical deduction strengthens the relaxation comparison without a new
numerical run.

### The capacity control survives pair and triple convexification

Consider a relaxation of the four-slot band in which, for each subset of at most three
labels, its pose vector must belong to the convex hull of that subsystem’s feasible
placements. Set all four centers to $(39/20,39/20)$ and all angles to zero.
This is not a packing.
Nevertheless, each triple is the average of the six label permutations of the feasible
three-square control above.
The three horizontal center coordinates average to $(1/2+39/20+17/5)/3=39/20$; all other
coordinates agree. Every pair also has a feasible swapped-pair average with that center.

Thus the collapsed vector satisfies all these exact subsystem convex-hull conditions
simultaneously, while the common three-atom certificate excludes four actual squares in
the full band. A capacity-three inequality contains information lost by this particular
pair/triple convexification.
The argument concerns labelled pose coordinates and the declared subsystem relaxation,
not the convex hull of all four-square packings or a fully branched geometric system.

The fixture has another cheap solution.
At angle zero the identical slots can be ordered horizontally by symmetry.
Their vertical differences are below one, so successive horizontal gaps must be at least
one; three gaps cannot fit in a center span of $29/10$. A fair target baseline should
include applicable ordering and projection deductions.
The new comparison therefore establishes a real relaxation separation, without a general
claim that weights outperform coupled geometry.

## A Direct Hybrid Method Without an Angle Conjecture

Start with the full feasible problem at a rational trial side $q$, initially $q=96/25$.
Each square has a center and an actual angle modulo $\pi/2$. A node records closed angle
domains, optional center bounds, selected separation alternatives, and every inherited
restriction. Whole-container symmetries and consistent relabelings may reduce cases.
Independently reflecting individual square angles changes relative geometry and is
invalid.

A common downward translation produces at least one bottom-wall contact in every
packing. This justifies a bottom anchor after covering the anchor’s label and feature.
It fixes the vertical center through its angle-dependent support height; it does not
force the anchor to be flush or axis-aligned.
The remaining anchor parameters include horizontal position and angle, and every
permitted value must remain covered.

For a square pair, the separating-axis theorem gives up to eight directed alternatives:
two edge-normal directions from either square and either order.
Once actual angles and one alternative per pair are fixed, containment and separation
are linear in the centers and side.
A corner formulation includes all sixteen corner-pair inequalities for a chosen directed
axis. Thus a fixed-side cell has 22 translation variables; a variable-side cell has 23
variables.

With $0\le L\le4$, each fixed-angle cell is a bounded polytope.
A nonempty cell has an optimal vertex, even when an optimal face contains rattlers.
Starting with any global minimizer, freezing its angles, and selecting valid pair
alternatives therefore yields another global minimizer supported by a full translation
basis. This proves an LP representative exists; it does not determine the angles or
create segment contacts.
This vertex argument applies to the closed physical/SAT polytope.
A requirement to preserve positive-length segments defines an open feature stratum; its
limit can lose segment length.
Choosing a vertex need not preserve those strict features.

For an angle box, use coefficient enclosures and center bounds to build an **outer LP**:
every genuine packing in the node satisfies its rows.
One simple construction writes a geometric inequality as $g(\theta,z)\ge0$, chooses a
reference linear expression $\bar g(z)$, and proves

$$
|g(\theta,z)-\bar g(z)|\le E
\quad\text{throughout the node}.
$$

Then $\bar g(z)+E\ge0$ is a necessary linear inequality.
LP contractions can tighten the center bounds used to calculate $E$, provided each
contraction is independently justified.
Feasible points of this relaxation are not automatically packing witnesses.

For rows $Az\ge b$, an exact Farkas leaf can use $\lambda\ge0$, $\lambda^T A=0$, and
$\lambda^T b>0$. Bounds on variables belong in the row system.
Alternatively, a uniform weighted combination of the original rows can tolerate
imperfect cancellation if a rigorous bound on the residual still gives a strict
contradiction over the whole parameter box.
Midpoint cancellation alone is insufficient.

The node loop should use cheap interval and projection tests, coupled LP contraction,
local resource cuts, and then selective branching on the remaining uncertainty.
Branch on angles when coefficient variation dominates; branch on separation labels when
their disjunction dominates; split positions when resources need localization.
An aggressive scheduler can prioritize useful conflicts and reuse exclusions while the
mathematical root still contains every feasible configuration.

There is a precise limit on a resource comparison.
At exact fixed angles, with every separation choice fixed and every wall row included,
the translation LP is already exact.
A sound resource cannot turn one of its feasible packings into an infeasible one.
The prospective advantages are tighter outer relaxations over angle boxes, exclusion
before all separation alternatives are selected, and cheaper or smaller proofs.
The four-slot control currently establishes an advantage only over independent pair
screens by a measured run, and over the specified pair/triple convexification by the
analytical argument above.
A target-domain comparison against the implemented coupled LP remains to be run.

### Completeness at a fixed infeasible side

The angle-first method has a useful completeness argument in principle.
Fix a side $q$ that is strictly infeasible and one complete selection $\sigma$ of pair
SAT alternatives. Write its corner and wall rows as $g_{\sigma r}(\theta,z)\ge0$, with
centers in a fixed compact box and a compact angular cover including all seams.
Continuity and infeasibility imply

$$
\min_{\theta,z}\max_r\{-g_{\sigma r}(\theta,z)\}>0.
$$

Convergent coefficient enclosures eventually make the outer LP error smaller than this
uniform violation. Every sufficiently small angular box is then excluded.
Compactness gives a finite cover, and there are finitely many complete SAT selections.
Center subdivision is therefore not needed for this existence argument, though it can be
valuable computationally.
A relaxation that never resolves its remaining separation disjunctions does not inherit
the argument.

This supplies no usable subdivision depth or runtime.
It also does not close the exact endpoint: $U$ has a feasible packing, so there is no
positive global violation margin there.
Even if every fixed $q<U$ is infeasible, the required cover can grow without a uniform
bound as $q$ approaches $U$. A finite exact-value proof still needs uniform control near
the endpoint, such as complete local capture or a structural and algebraic argument.

## Bottom-Up Resources, Capacities, and Anchor Correlations

Let $D_i$ be a domain for square $i$, and let $W_i(p)$ be a specified witness strictly
inside that square at pose $p$. For one nonnegative measure $\mu$ with total mass $M$,
prove

$$
a_i\le\inf_{p\in D_i}\mu(W_i(p)).
$$

In any simultaneous packing, the selected witnesses are disjoint, so $\sum_i a_i\le M$.
A strict reverse inequality excludes the whole domain.
Atomic measures require the strict-interior convention; full-square integration requires
a measure that assigns zero mass to square boundaries.
Different measures retain different budgets.

The guaranteed occupied region and the guaranteed captured core are different sets.
For a pose domain, $G=\bigcap_Q Q$ can exclude residual squares that overlap its
interior, while $J=\bigcap_Q W(Q)$ guarantees membership in the chosen cores.
Membership in $G$ alone does not guarantee core capture.
For example, $(1/10000,1/2)$ lies inside the unit square $[0,1]^2$ but outside its
concentric $9977/10000$ core.
X-014’s conditional counting lemma remains sound; its suggested placement of atoms in a
common occupied region needs this additional capture premise.

The bottom-up version learns inequalities on small subsets before expanding the
eleven-square tree. Suppose a finite pose cover has cells $C$, and a proved capacity
bound $\kappa(S)$ says that at most $\kappa(S)$ pairwise compatible squares can have
assigned poses in a cell set $S$. Then the integer occupancy model can use

$$
\sum_{c\in S}z_c\le\kappa(S).
$$

Every actual pose must be assigned to a covering cell.
Overlapping closed cells need an explicit assignment convention or a proof that at least
one consistent assignment is represented.
A binary variable requires a proved capacity-one cell.
Several angle bins over the same capacity-one spatial tile share one occupancy budget.

Integer counts also retain information lost by fractional occupancy.
The abstract constraints $c_A,c_B\le11/2$ and $c_A+c_B=11$ admit $(11/2,11/2)$ over the
reals, but no integer solution because each count is at most five.
A geometric application must supply actual certified resource rows; this example is only
the rounding mechanism.
For atomic resources, let $A(S)$ contain every atom that a selected witness from slots
$S$ can reach. Guaranteed captures then satisfy the more localized bound
$\sum_{i\in S}a_i\le\sum_{p\in A(S)}\mu(\{p\})$. This is another way to derive subset
inequalities with a shared, explicitly restricted budget.

Weighted captures can prove some capacities; exact two-, three-, or four-square
subproblems can prove others.
An infeasible combination becomes a reusable exclusion only with its full geometric
domain attached. Reuse on a narrower node is justified by domain inclusion; reuse after
widening requires a new proof.
Incircle distances, interval SAT, and existing small-$n$ theorems are cheap inputs when
their containing region and shape assumptions match.
A disk relaxation’s feasible placement proves nothing about the original squares.

This gives a concrete connection between the two search directions: top-down branching
produces localized pose domains; bottom-up certificates exclude combinations of those
domains and are reused across many larger nodes.
It is already within H-111’s resource/conflict program, but the proposed subset
certificate library makes its implementation more specific.

### Preserve the common anchor parameter

Let $a$ denote an actual anchor pose in a closed box $A$. For each residual slot use a
safe domain $D_i(a)$ containing every pose compatible with that same anchor.
A static outer domain may take the union over $a\in A$. Taking only the midpoint’s
residual region would omit real configurations.

A stronger proposed representation retains the common parameter.
For one fixed measure, certify anchor capture $\alpha(a)$ and residual guarantees
$w_i(a)$. The uniform inequality

$$
\inf_{a\in A}\left[\alpha(a)+\sum_i w_i(a)-M\right]>0
$$

excludes the whole anchor box.
Independent minima can fail because their worst cases occur at different anchors:

$$
\inf_A\alpha+\sum_i\inf_A w_i\le M.
$$

If these are merely conservative guarantees, that inequality shows only that the chosen
bounds fail. Establishing a real gain requires a frozen static comparator with sharp
independently certified minima, a feasible relaxation witness, or an exact obstruction
for its declared finite candidate family.

For an abstract illustration, take $a\in[0,1]$, $M=1$, $\alpha(a)=(1+a)/2$, and
$w(a)=1-a/2$. Each capture lies between $1/2$ and the whole budget, but their sum is
always $3/2$. Separate minima sum to exactly one, where pruning is invalid.
These functions are a logical example, not captures realized by square geometry.
A coupled LP retaining $a$ already detects this linear example; the comparison is
specifically with independent minimization.

The geometric spike must produce actual strict-interior captures, joint parameter
enclosures, and an independently verified positive margin.
The comparison concerns a specified unsplit anchor box and resource representation.
Arbitrarily refined anchor boxes may recover the same correlation; the prospective gain
is avoiding that refinement or reducing proof size.

## What Few Angles Would Require

For a feasible packing $P$, form a graph with eleven square vertices and one fixed wall
vertex. A square-square edge requires a shared segment of positive length; a wall edge
requires a square edge flush with a container wall.
Point contacts do not enter this graph.

A segment forces equal orientations modulo $\pi/2$; a wall edge forces orientation zero.
If $k(P)$ is the number of components not connected to the wall, the angular incidence
matrix has rank

$$
r(P)=11-k(P).
$$

A spanning forest proves this identity.
At most $k(P)$ independent orientation variables remain after these equalities, together
with the fixed axis orientation if its component contains a square.
Other constraints may determine those variables; they are not necessarily feasible
motions. Rank at least ten is sufficient for an axis-plus-one-angle description.
It is not necessary: disconnected components can share an angle without a contact
forcing that coincidence.

Trump’s seven square-square segments, using the source’s zero-based labels, are

$$
(3,4),(3,5),(6,7),(6,8),(7,9),(8,9),(9,10).
$$

Nine flush wall incidences anchor squares $0,1,2,3,4,5$. The other component is
$\{6,7,8,9,10\}$, giving rank ten.
The incidences are square 0 at left and bottom; square 1 at bottom and right; square 2
at top; square 3 at left and top; square 4 at top; and square 5 at left.
Squares 7 and 10 also touch walls at points, which do not fix their orientation.
The [typed contact extractor](../../../packing/src/sqpack/promote/contacts.py),
[exact contact loci](../../../packing/src/sqpack/render/contacts.py), and source
construction support the draft graph control.

There are two reasons to avoid inferring this structure from apparent crowding.
First, a rotated square can touch an axis square at a vertex-edge contact while
remaining at another angle.
A contact force then lies in a vertex normal cone; neither that fact nor torque balance
equates the orientations.
Second, even optimal packings can contain angular rattlers.
At $n=6$, five axis squares at lower-left corners $(2,0),(2,1),(2,2),(0,2),(1,2)$ leave
a sixth unit square centered at $(1,1)$ free to rotate in the vacant $2\times2$ region.
The theorem $s(6)=3$ makes this an optimal family; see the
[archived six-square source](../../../packing/resources/papers/stromquist-1984-packing-unit-squares-inside-squares-i-six-unit-squares.raw.md).

An unconditional boundary statement is available: a minimizing packing has an ordinary
contact component spanning opposite walls.
Otherwise each component has both bounding-box widths strictly below the side.
Small separate translations fit every component in a smaller square, while the positive
distances between distinct compact components preserve separation.
This contradicts minimality.
The contacts at the two walls can be points; the argument supplies no count of flush
squares.

### The useful normal-form statement is existential

The proposed statement is: **some global minimizer has all orientations in
$\{0,\theta\}$ modulo $\pi/2$**. A complete lower bound of $U$ for that family would
then prove $s(11)=U$. H-117 already contains the broader question of a bound on exact
orientation classes.
Requiring every optimum to have Trump’s graph is substantially stronger than needed.

One possible proof selects, among global minimizers, one with the fewest distinct
nonaxis angles.
Such a selection exists because a minimizer exists by compactness and the
possible counts are integers.
An angle-elimination lemma would show that whenever two nonaxis angles remain, a finite
feasible motion at nonincreasing side either improves the side or reaches a
configuration with fewer nonaxis angles.
Either outcome contradicts the chosen representative.

The difficult obligation is the finite motion through contact changes.
An infinitesimal flex, a small stress support, or a count of variables does not prove
that such a path exists.
Contact release, newly formed contacts, and point-segment transitions must all remain in
the argument. A local minimum with several angles would challenge a proposed motion
lemma. Even proving that it is a global minimum would not refute the existential normal
form: another global minimizer could have fewer angles.
Refutation requires excluding every low-angle minimizing representative, for example by
proving uniqueness of a high-angle global minimizer.

### A concrete structural test

Release the segment identity $(9,10)$ from Trump’s graph, keeping the other six
specified pair segments, all nine specified flush wall incidences, and all 55 pair
nonoverlap and wall conditions.
The retained equality graph has wall component $\{0,\ldots,5,*\}$ and two unanchored
components, $\{6,7,8,9\}$ and $\{10\}$. Its rank is nine, allowing an axis class and two
oblique parameters.

This is a precise family in which to test an LP/capacity exclusion or a conditional
angle-merging argument.
A direct exclusion must specify $L\le q<U$; a motion claim must specify its
variable-side minimizing-representative sublevel and premises.
The parent family, which contains Trump, cannot itself be declared infeasible.
Require at least two distinct nonaxis actual angles before demanding an angle-reducing
motion. Configurations whose component angles coincide, or whose extra component is
axis-aligned, instead enter the axis-plus-one-angle family.
Graph rank nine alone does not distinguish these cases.
Retained positive segments are strict feature conditions; their zero-length boundaries
need explicit sibling cases when making a closed cover.
The released contact may open or become a point, and its equality seam must remain
covered. Trump is a feasible control in the parent family and on the equality seam, not
in a child that requires strict release.

The family is narrower than all configurations of six axis squares, four squares at one
angle, and one at another.
It also retains source wall attachments.
A successful pilot must be followed by alternative feature/wall domains if it is to
contribute to global structure.
It should begin outside any region already closed by the retained local theorem, so
success contributes new geometry.

## Restricted Families and the Remaining Exact-Value Gap

Three families need separate names and complete domains:

| Family | Angular parameters | Required cases |
| --- | --- | --- |
| H-112: six axis squares and five at one common angle | One | Every common angle, every center placement, every contact and wall pattern |
| Axis plus one angle, arbitrary multiplicity | One | All multiplicities, including an empty axis class; useful intermediate target |
| H-113: at most two arbitrary absolute orientations | Two | Both angles, all multiplicities, coincident classes, and quarter-turn seams |

An arbitrary rotation cannot normalize one of H-113’s classes to zero while keeping the
square container fixed.
H-112 is one multiplicity within the intermediate family, rather than a replacement for
it.

The draft strict-core lemmas at side at most $97/25$ give $\alpha=2\arctan(3/200)$ and
$\gamma=2\arctan(1/1500)$: at least two squares are farther than $\alpha$ from the axes,
and at least one is farther than $\gamma$ from both axes and diagonals.
Both bounds follow from the core support function $R(t)$ above.
For the near-axis claim, take $q=97/25$, $b=971/1000$, and $t=3/200$. Then

$$
bR(t)=\frac{39996461}{40009000}<1,
\qquad b-q/4=1/1000>0.
$$

The nine marks $\{q/4,q/2,3q/4\}^2$ meet the interior of every contained axis core: the
gaps between consecutive marks and either wall are smaller than its side.
At most nine of eleven packed squares can belong to this closed angular neighborhood, so
at least two lie outside it.

For the union of endpoint neighborhoods, take $b_e=749/750$ and $t_e=1/1500$. We have

$$
R(t_e)=\frac{2252999}{2250001},\qquad
1-b_eR(t_e)=\frac{4499}{1687500750}>0.
$$

If all eleven squares belonged to these neighborhoods, choose strict concentric cores
oriented exactly at the corresponding axis or diagonal.
After scaling by $1/b_e$, they would be unit squares with orientations $0^\circ$ or
$45^\circ$ in side $2910/749$. But this side is below $L_0=2+4\sqrt2/3$, since

$$
3(2910/749-2)=4236/749>0,
\qquad 32\cdot749^2-4236^2=8336>0.
$$

This contradicts Stromquist’s
[Theorem 3](../../../packing/resources/papers/stromquist-2003-packing-10-or-11-unit-squares.md),
whose source and boundary conventions are assessed in the
[BC-255 review](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-theorem3-source-control-independent-review.md).
For the boundary bridge, a closed-unit packing strictly below $L_0$ dilates to pairwise
disjoint open squares of side greater than one in side $L_0$, which the source theorem
forbids. At least one original square must therefore lie outside both endpoint
neighborhoods. The witnesses for the two angle conclusions need not be the same squares.

Conditional on the axis-plus-one-angle family, one common reflection folds the angle
into $[0,\pi/4]$, and these lemmas give

$$
m\in\{2,\ldots,11\},\qquad \alpha<\theta<\pi/4-\gamma.
$$

These ten multiplicities are useful pruning within that family.
Equivalently, the shared half-angle satisfies

$$
\frac3{200}<t<
\frac{(\sqrt2-1)-1/1500}{1+(\sqrt2-1)/1500}.
$$

They are not a classification of unrestricted packings.
For a common-angle class containing at least ten squares, rotating the whole class and
container into its axes gives the additional necessary inequality
$L(\cos\theta+\sin\theta)\ge4$. Indeed, if the enclosing axis square had side below
four, a $3\times3$ grid of marks would hit the interior of every axis unit square,
contradicting ten disjoint interiors.
At $L\le97/25$, the half-angle parameter $t=\tan(\theta/2)$ must satisfy
$197t^2-194t+3\le0$.

For one shared angle, all corner coefficients are rational in $t$ through
$\cos\theta=(1-t^2)/(1+t^2)$ and $\sin\theta=2t/(1+t^2)$. A selected translation basis
therefore gives rational center and side functions.
Exact root isolation can partition parameter intervals by determinant roots, slack
roots, and objective comparisons with $U$. Singular values require another basis or an
exact slice decision; identically zero polynomials remain identities.
A minimum-value argument also needs derivative critical points and endpoint limits.
Samples of angles or generic nonsingular bases do not constitute this analysis.

For multiplicity $m$, even after merging identical owner axes within each class, the raw
separation-label count can be $4^{55-m(11-m)}8^{m(11-m)}$. Most labels may be
impossible, but that must be shown.
The one-angle reduction removes nonlinear variables without establishing a practical
global case count.

Angular transfer can expand a restricted theorem only when its margin pays for the
approximation. If $f(\alpha)$ is the optimum over **all centers and separation
alternatives** at exact angles $\alpha$, a mismatch of every actual orientation at most
$0\le\delta\le\pi/4$ modulo quarter turns gives
$f(\theta)\ge f(\alpha)/(\cos\delta+\sin\delta)$. Thus a theorem with endpoint
$f(\alpha)=U$ supplies no positive-radius exclusion at the same endpoint through this
inequality alone. The
[contributed addendum](../../../packing/resources/papers/n11-complete-research-bundle-2026-09-07/updates/enumeration_addendum.md)
makes the same distinction.

There are consequently two complete routes to the exact value.
Direct exclusion can cover all feasible configurations below $U$, perhaps sending an
entire residual into an accepted local chart.
Alternatively, a global minimizing-representative theorem can reduce the root, followed
by a complete restricted-family bound.
Proving only H-112, finding many two-angle numerical optima, or excluding one
released-contact family completes neither route.
Uniqueness would require additional equality classification even after the value is
proved.

## Available Machinery and the Missing Connections

The project has substantial exact geometry and certificate infrastructure.
The implementation task is to connect existing parts around one real uniform exclusion.

| Machinery | Available capability | Hybrid use and missing connection |
| --- | --- | --- |
| [Number fields](../../../packing/src/sqpack/field.py), exact construction and contact verification | Rational/algebraic arithmetic, exact corner geometry, SAT, feature classification, and the degree-eight Trump witness | Bind source controls and algebraic endpoints; preserve interval and field identities in exported certificates |
| [Exact LP](../../../packing/src/sqpack/exact_lp.py) | Rational and field-valued LPs, exact pivots, phase I, certified vertices and multipliers; tilted fixed-cell construction | Accept arbitrary selected SAT descriptors and export an infeasible phase-I certificate. The current fixed-cell helper chooses a valid axis from a supplied feasible pose. |
| [Trump cell LP](../../../packing/cases/trump11/independent_lp_cell.py) | Independent corner-row formulation and numerical scans of the retained cell | A geometry control for uniform certificates; no full-family or all-angle conclusion from scans |
| [Fractional package](../../../packing/src/sqpack/fractional/) | Covering row generation, site pricing, event-cell sweeps, interval decisions, retained states and exact certificate paths | Propose and verify local resources; no automatic transfer from a global witness sweep to arbitrary obstacle-conditioned domains |
| [Class certificates](../../../packing/src/sqpack/fractional/classcert.py) and [adaptive cores](../../../packing/src/sqpack/fractional/adaptive.py) | Exact fixed-composition decisions with unchanged center domain; direction-cell/core geometry and independent control machinery | Existing class decisions are reusable. Adaptive controls are not a completed target acceptance route, and neither component supplies general conditional minima. |
| [Standalone verifier](../../../packing/cases/n11_fractional_certificate/verify_claim.py) and [retention adapter](../../../packing/devtools/decide_certificate.py) | Independent export/replay precedent for the supported uniform-net one-square certificate | The retention adapter accepts unconditional certificates and refuses conditional/class variants. The hybrid proof needs its own reviewed adapter. |
| [Point covers](../../../packing/src/sqpack/cover.py) | Exact marked-point predicates and mesh/partition checks | Reuse geometric primitives. Mark resources are different from capacity-one pose tiles and grouped occupancy. |
| [Scalar completion](../../../packing/devtools/run_fixed_site_completion.py) | Changed fixed-site adapter, identity guards, retained outcomes, and reviewed controls | Preserve its separate question and deferred status. Reopening requires a named downstream use and a fresh source allocation. |
| [Density facet verifier](../../../packing/devtools/density_face_verifier.py) and [slab verifier](../../../packing/devtools/density_slab_verifier.py) | Complete depth methods with independently structured reader, sign and incidence reuse | Potential resource/support verification; uniform-source cost still blocks the current target |
| [Density source binding](../../../packing/src/sqpack/full_size_density/support_screen.py) and [necessary support rows](../../../packing/src/sqpack/full_size_density/support_ceiling.py) | D4 image/preimage reconstruction, positive-area incidence regions and exact support ceilings | Reuse during independent seven-row adoption. Closed-point fractional depth and almost-everywhere density depth have different boundary semantics. |
| [Near-axis reader](../../../packing/devtools/check_angle_near_axis_control.py) and [near-45 reader](../../../packing/devtools/check_angle_near45_triangle_control.py) | Independent exact rectangle and Bernstein triangle reasoning for stated continuous clauses | Models for whole-domain proof receipts and possible necessary angle cuts, with the original clause premises retained |
| [Local Trump theorem](../../../packing/cases/trump11/isolation-theorem.md) and [radius machinery](../../../packing/cases/trump11/isolation_radius.py) | Quantified local closure from exact tangent branches, stress, rank, curvature, and retained modulus data | Terminal lemma only after full chart, label, angle-lift and radius inclusion; retain the independent replay qualification |
| [Numerical quench](../../../packing/src/sqpack/research/quench.py), [Rust search](../../../packing/sqsearch/src/search.rs), and [promotion](../../../packing/src/sqpack/promote/refine.py) | Fixed-angle numerical LPs and angle moves, reproducible annealing, Newton refinement and interval/exact promotion routes | Propose alternative frames, bases and adversarial witnesses. A contact-equation root still needs independent packing verification; failed searches prove no exclusion. |
| [Structural labels](../../../packing/src/sqpack/contact_full_cell.py) | Small axis-aligned scaffold canonicalization and execution descriptors | Its current $n\le5$ scope is separate from the general exact LP. Descriptor validity does not establish matrix assembly or complete target coverage. |
| Draft hybrid instruments | Rectangular strict-core minima, interval contact screens, angle-count controls, and exact orientation graphs | Adapt selected parts after review; no generic obstacle-aware resource engine, uniform LP exporter, or complete proof-DAG reader is supplied by those spikes |
| Campaign and validation tools | Hypothesis/experiment records, outcome and provenance checks, generated maps, and tiered validation | Add one shared certificate contract after a consumer exists; PR107’s cross-agenda BC uniqueness check should accompany integration |

The missing core is a small interface carrying a closed domain, its geometry rows and
coefficient bounds, a leaf certificate, and an independently checkable implication.
A complete proof also records a finite directed acyclic graph of case splits, or a
proved well-founded descent.
Every split covers its parent, every boundary remains present, and every reused lemma
receives a domain-inclusion check.
Unresolved leaves remain explicit.
A catalog of labels or generic arithmetic helpers is not this interface.
The campaign’s existing dependency graph validates research records; it does not check
mathematical child coverage or lemma implications.

Implementation and validation follow [development.md](../../../development.md).
Python 3.14 is required for project code.
Producers can use numerical optimization to find candidates; independent readers check
the exact or directed-interval object actually claimed.
New fast regressions belong on the normal CI surface.
Shared resource counts, LP rows, and proof composition need separate negative controls
for omitted constraints, widened domains, boundary loss, invalid symmetries, and
circular dependencies.

## Proposed Exploration and Agenda Additions

**X-TBD-HYBRID: Conditional Resources and Angular Structure for Eleven Squares.** Its
contribution would be the four scoped spike results, the exact orientation-graph
derivation, the distinction between exact and outer LPs, the subset-capacity mechanism,
the shared-anchor correlation proposal, and the contact-release test.
It should cite PR107’s survey rather than duplicate the full source archive.

**AGENDA-TBD-HYBRID** denotes this proposed addition to Agenda 027, pending the
integration decision.
The recommendation is to retain Agenda 027’s existing identity.
The following placeholder block labels describe work to fold into its commitments; they
do not reserve another BC range.

| Placeholder block | Existing home | Concrete output |
| --- | --- | --- |
| BC-TBD-CONTRACT | BC-260/261 | One actual uniform LP exclusion, exact certificate export, independent replay, and a minimal complete case control |
| BC-TBD-CAPACITY | BC-262 / H-111 | A matched comparison of interval screens, coupled outer LPs, and the same geometry with local resources or subset capacities |
| BC-TBD-ANCHOR | BC-262 / H-111 | A joint-anchor certificate on one unsplit domain if loss of anchor correlation explains the current residual |
| BC-TBD-RELEASE | BC-267 / H-117 | An independently scoped release-family exclusion or precise angle-elimination obligation, retaining feature boundaries |
| BC-TBD-FAMILY | BC-263/266 / H-112/113 | A complete common-angle interval pilot with all contact alternatives, plus an independent attempt to find a sub-$U$ witness |
| BC-TBD-INTEGRATE | BC-268 | Compare closed domains, residual structure and proof cost; select the next representation from evidence |

BC-259’s support review remains independently useful.
BC-264’s pair kernel and BC-265’s candidate-led resource selection retain their own
identities and entry conditions.
The new design need not wait for physical stationarity to prove direct all-feasible
exclusions, nor for BC-248’s separate near-tight global-residue tree to meet its measure
and census guards.

### First execution checkpoint

This is Agenda 027’s separate opening allocation.
Session 090’s H-110 continuation and the newly selected 30-minute BC-255/H-102
conditional-compatibility assessment keep their source allocation.
H-107 is deferred from that next two-hour block under paused `think-7fec`; any later
reopening must meet the source agenda’s named-use conditions and fund its retained
35-minute producer, 20-minute shared verification allowance, and coordination margin.
The hybrid plan changes none of those allocations.

Use Agenda 027’s proposed first checkpoint of about four active hours as a planning
estimate, retaining its short slices and integration reserve.
No global solver runtime has been measured.
The first useful sequence is:

1. Review the direct proof implications and export one real uniform leaf on a complete
   small control domain.
   Confirm refusals for a missing row, widened angle box, omitted boundary, and invalid
   certificate reuse. Reuse the accepted source controls at their provenance.
2. Freeze $q=96/25$, a nontrivial closed bottom-anchor domain, a complete outer cover of
   its ten-square residual, resource choices, and the coupled geometric comparator.
   Price that exact task before freezing its scientific cap.
   A smaller complete pilot is preferable if the proposed domain cannot be priced.
3. Run the matched resource comparison with identical domains and branch policy.
   Record exact exclusions, the whole unresolved remainder, certificate bytes and replay
   cost, branch work, and actual compute.
   Distinguish additional exclusion strength from a cheaper route to the same
   conclusion.
4. In parallel, examine one explicit rank-nine release domain, outside already closed
   local scope, and its seam controls.
   Choose either a direct exclusion or a conditional minimizing-motion claim; do not mix
   their premises.
5. At the checkpoint, expand only a representation that closes a meaningful continuous
   domain or leaves a simpler actionable remainder.
   If one prescribed refinement gives no additional exclusions, near-universal zero
   captures, or the same large residual, retain that negative and price a specific
   change such as a second anchor, a small-subsystem inequality, or a different
   resource.

This reprices a selected representation rather than retiring the idea of weighted
branch-and-bound. It also leaves the six-plus-five theorem as another consumer of the
shared interface. A failure of a sufficient certificate test is unresolved geometry, not
proof that the represented configurations exist.

## Draft Hypothesis Templates

Each placeholder below is a narrower possible claim under an existing parent.
Before any target run, replace the domain and instrument placeholders by concrete frozen
objects, specify the finite candidate family when a negative search is meant to be
decisive, and include independent replay in the budget.
A new hypothesis record is needed only if the claim deserves a separate durable
identity.

| Placeholder | Proposed claim and existing parent | Acceptance and limits |
| --- | --- | --- |
| H-TBD-CAPACITY | Under H-111, a frozen continuous domain $D_{\rm TBD}$ at $96/25$ is excluded by a specified common-measure or subset-capacity certificate while the specified coupled outer LP has an exact feasible relaxation witness | Accept only both exact witnesses on identical domains. Exhausting a declared finite resource family can reject that family comparison. A timeout or lack of a found resource leaves it unresolved. |
| H-TBD-ANCHOR | Under H-111, one fixed measure and unsplit anchor box have a strictly positive uniform joint capture gap, while the specified independent-minimum comparator fails | Require complete parameter coverage, exact margin, and a certified obstruction or surviving solution for the static comparator. This does not compare against arbitrary anchor subdivision or other measures. |
| H-TBD-RELEASE | Under H-117, every candidate in one fully specified release domain satisfying the declared minimizing premises and having at least two distinct nonaxis actual angles is excluded or admits a finite nonincreasing-side motion reducing that count | Require a uniform argument through releases, new contacts and seams; route coincident or axis component angles to the restricted family. A proved counterexample refutes the conditional lemma; failure to find a motion does not. A successful local domain leaves the global remainder open. |
| H-TBD-NORMAL-FORM | As a precise specialization of H-117, some global minimizer has orientations in $\{0,\theta\}$ modulo quarter turns | Requires a global representative argument, for example complete angle elimination or a sufficient segment-rank theorem. A high-angle feasible packing alone does not refute it. No numerical prevalence threshold can accept it. |

H-112 and H-113 already state the corresponding restricted-family lower-bound claims, so
another broad “few-angle optimum” hypothesis would duplicate them.
An axis-plus-one-angle theorem over all ten trimmed multiplicities may warrant a
separate intermediate claim when that complete domain is selected for execution.
Tool readiness and the elementary graph-rank identity belong in evidence or mathematical
contracts rather than becoming speculative scientific hypotheses.

## Alternatives That Remain Open

| Direction | Present reason to retain it | Evidence that would change allocation |
| --- | --- | --- |
| Changed weights/sites and adaptive cores, H-094/095 | The fixed-weight shrink negatives and incomplete scalar solves do not settle the unrestricted certificate problem | A completed certificate or exact obstruction at the declared representation |
| Geometric angle-cell kernels, witness menus and segment measures, H-096–098 | These change how one-square capture is represented | A candidate with proved containment, boundary semantics and a tractable universal reader |
| Full-size density and equality analysis, H-100/101 | The sixty-placement support is only one finite dual test | A useful changed support or equality structure with a complete geometric check |
| Pair PSD kernels, H-114 | They directly encode interactions beyond a one-body resource | A small exact feature obstruction or a candidate with priced continuum pair verification |
| Curved resources and expanded support, H-115/116 | They are distinct from the unchanged support and present atomic cores | A concrete candidate or obstruction that identifies the next verifier |
| Several rotator frames, few-large-tilt cases, and dispersed angle classes | Unrestricted competitors may have more than two orientations | Complete domains whose capacities or LP structure are simpler than the original root |
| Contact and stationary algebra | Exact residual leaves may be easier than broad pose subdivision | A reviewed physical formulation and a measured finite family of remaining cases |
| Numerical adversarial search | A different sub-$U$ witness would immediately redirect the program | Exact verification of an improvement; repeated failures alone do not restrict the feasible set |

The strategic preference is to combine a direct proof method with a structural
investigation whose conclusion would reduce its cost.
The evidence currently favors testing useful uniform leaves and correlations before
building a global atlas.
It gives no basis for discarding the general-angle remainder.

## Integration and Identifier Finalization

The working branch is `codex/n11-hybrid-research-plan`, created directly from PR105’s
`f5684f51` head and now stacked on PR107’s `54ad6bc1` base, including PR105’s `54d1ca98`
closeout and `6d8b2b38` scheduling amendment.
The earlier spike drafts remain local, unpublished provenance in the stash identified
above; their untracked files are in its third parent.
The strategic arguments needed for incorporation are collected in this review.
Adopting an instrument or measured receipt later requires bringing that particular
artifact into the repository and reviewing it, with a fresh identifier check.

After the mathematical scope is settled, fold this review into PR107’s research program,
adopt selected spike evidence and adapters, and update one scientific agenda and its
hypotheses through one coordinator for this program.
Session 090’s H-110 continuation and conditional-compatibility assessment retain their
source coordinator and allocations; H-107 retains its deferred status unless that
coordinator reopens it under the stated conditions.
A separate implementation branch can preserve ownership without creating a separate
research agenda.
Another agenda would be justified by an independently managed scientific
objective, rather than by the Git branch alone.

The reviewed PR107 publishes X-017, Agenda 027, H-111–117, and BC-258–268. Its latest
coordination update restores X-017 and supersedes the temporary X-020 name and earlier
speculative reservation.
All new labels in this review remain placeholders.
They consume no part of either branch’s namespace.
Finalization should recheck both live branches, reuse existing claims wherever possible,
allocate only the records actually being created, and update affected references
together. Preserve PR107’s campaign-wide uniqueness validation and every prior
experiment’s frozen identity.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
