# BC-260 Direct Hybrid Contracts

Independent W2 factual review for session-092, 2026-09-07. This accepts the named
mathematical implications below with their stated premises.
It does not accept an implemented BC-261 instrument, an H-118 comparison, or an H-120
exclusion. The two target hypotheses remain unresolved.

The reviewed consumers are
[H-118](../../../../hypotheses/H-118-capacity-versus-coupled-lp.md) and
[H-120](../../../../hypotheses/H-120-rank-nine-release-exclusion.md), under
[Agenda 028](../../../../agendas/agenda-028-hybrid-strength-and-angular-release.md).
[Agenda 027](../../../../agendas/agenda-027-compatibility-and-restricted-families.md)
retains the single BC-261 implementation owner.
This review consumes
[X-017](../../../../explorations/X-017-compatibility-and-complete-case-covers.md),
[X-018](../../../../explorations/X-018-hybrid-strength-and-angular-release.md), and the
[hybrid strategy review](../../../../../../docs/project/reviews/review-2026-09-07-n11-hybrid-strategy.md).
The archived reports are mathematical material being assessed; their proposed execution
instructions do not authorize runs.

## Individual Verdicts

| Implication | Verdict | Exact limit of acceptance |
| --- | --- | --- |
| Finite case composition | Accepted with X-017’s correction | A complete root, covering children, valid terminal implications, and a finite DAG or proved well-founded descent |
| Fixed-angle wall and selected SAT rows | Accepted | Closed containment and interior-disjointness, all corners and all directed alternatives accounted for |
| Uniform outer LP | Accepted | Every original row implies its relaxed row on the entire declared parameter and variable domain |
| Exact or residual Farkas contradiction | Accepted | Nonnegative multipliers and a strictly positive exact uniform gap, with independently justified bounds on every uncancelled variable |
| Interior-witness resource counting | Accepted | One nonnegative measure per budget; uniform captures by witnesses inside square interiors |
| Full-square resource counting | Accepted conditionally | The selected measure assigns zero mass to every relevant square boundary |
| Cell and subset capacity inequalities | Accepted conditionally | Complete assignment semantics and a universal capacity or incompatibility proof at the attached domain |
| Bottom-anchor residual exclusion | Accepted | Joint translation is admissible, and residual domains contain the union over every permitted anchor |
| Shared-anchor resource sum | Accepted conditionally | All captures refer to the same actual anchor and a common justified measure budget |
| H-118 strength comparison | Acceptance rule accepted; target unresolved | Uniform capacity exclusion and an exact feasible point of the frozen coupled outer relaxation on identical domains |
| H-120 direct release exclusion | Acceptance rule accepted; target unresolved | Complete variable-side domain, feature bounds and seams, with no stationarity premise |
| Separation from the retained local ball via square 3 | Accepted at the retained labels and origin | The retained top/left flush incidences and side cap imply a center-coordinate distance exceeding the named radius |
| Physical KKT, kernel, finite-motion and global few-angle conclusions | Unresolved in this review | No blanket acceptance, and no prerequisite imposed on a direct all-feasible exclusion |

## Case and Geometry Implications

Use closed unit squares in the anchored container $[0,L]^2$, with disjoint interiors and
legal boundary touching.
A pose has a center and an actual orientation in $\mathbb R/(\pi/2)\mathbb Z$. An angle
bin describes an interval of these actual orientations; it does not identify different
orientations geometrically.
Half-angle charts need explicit lifts, positive denominators, and a finite cover of
their quarter-turn seams.
Equal class angles and axis angles remain included.

For each square, let its four offsets be $v_i^{st}(\theta_i)=\tfrac12(su_i+tv_i)$, where
$s,t\in\{-1,1\}$ and $u_i=(\cos\theta_i,\sin\theta_i)$,
$v_i=(-\sin\theta_i,\cos\theta_i)$. Containment consists of the four corners satisfying
each of the four wall inequalities.
For a pair, choose a directed axis from $\{\pm u_i,\pm v_i,\pm u_j,\pm v_j\}$ and
require

$$
n\cdot(c_j+v_j^{ab}-c_i-v_i^{st})\ge0
\quad\text{for all sixteen corner pairs}.
$$

The separating-axis theorem makes the disjunction over those choices equivalent to
interior-disjointness.
Coincident axes can create duplicate alternatives; a sound deduplication supplies an
exact equivalence. Weak inequalities preserve touching.
At fixed exact angles these are linear inequalities in the centers and, when needed, the
side. They give an exact selected cell when the complete wall and selected pair rows are
retained. A subsystem uses all its own pair conditions; a full eleven-square leaf
includes all 55 pair conditions or an explicitly justified relaxation of them.

Every branch split must cover all alternatives not already ruled out, including ties.
A finite DAG proves a root empty by reverse induction from its certified leaves.
Children may overlap.
Unresolved children remain in the result, and no volume-zero argument removes a contact
or angle seam. A lemma reuse supplies domain inclusion into all the lemma’s hypotheses,
including labels, actual angle lifts and side range.
Circular references are insufficient even if the graph is finite.
These are the additional hypotheses required by the proof of
[archived Proposition G](../../../../../resources/papers/n11-complete-research-bundle-2026-09-07/updates/enumeration_addendum.md#proposition-g-finite-cover-composition).

A joint container symmetry acts on centers, angles, wall identities, selected axes and
any resources or lemma charts being reused.
Consistent relabeling is allowed.
Reflecting one square independently, folding every angle independently to an acute
interval, or rotating an arbitrary angle class to zero does not preserve the problem.

Deleting a necessary LP row only weakens an outer relaxation; a valid infeasibility
certificate for that weaker system remains sound.
Consequently a missing-row control must test the claimed complete descriptor-to-row
assembly or a stale dual’s row binding.
It should not assert that every row deletion makes an exclusion false.
Omitting an SAT alternative is different: it can remove feasible configurations from the
cover.

## Uniform LP and Farkas Acceptance

Write an original necessary inequality as $g_r(t,z)=a_r(t)^Tz-b_r(t)\ge0$ on a closed
parameter box $I$ and a justified variable box $B=[\ell,u]$. Choose a reference
expression $\bar g_r$ and prove $|g_r-\bar g_r|\le E_r$ throughout $I\times B$. Then
$\bar g_r+E_r\ge0$ is necessary.
For example, coefficient errors $|a_{rj}-\bar a_{rj}|\le\epsilon_{rj}$ and
$|b_r-\bar b_r|\le\epsilon_{rb}$ give the valid bound

$$
E_r=\epsilon_{rb}+\sum_j\epsilon_{rj}\max(|\ell_j|,|u_j|).
$$

The error sign is positive in the relaxed $g$ inequality.
A contraction used to shrink $B$ must already follow from the current node; a midpoint
solution supplies no such bound.
Correlations between angles may be discarded conservatively, at a possible loss of
exclusion strength. Algebraic identities and denominator signs cannot be assumed from
floating approximations.

For reconstructed outer rows $Az\ge b$, an exact certificate consists of

$$
\lambda\ge0,\qquad \lambda^TA=0,\qquad \lambda^Tb>0.
$$

Feasibility would give $0=\lambda^TAz\ge\lambda^Tb>0$. The certificate includes
variable-bound rows or binds to independently proved variable bounds.
A rational certificate can use exact rational arithmetic throughout; an algebraic
certificate additionally needs exact field and sign evidence.

For a uniform combination of the original rows, put $r(t)=A(t)^T\lambda$ and
$h_B(r)=\sum_j\max\{r_j\ell_j,r_ju_j\}$. Feasibility implies
$\lambda^Tb(t)\le r(t)^Tz\le h_B(r(t))$. Thus it suffices to prove

$$
\inf_{t\in I}\left[\lambda^Tb(t)-h_B(r(t))\right]>0.
$$

This is
[archived Proposition H](../../../../../resources/papers/n11-complete-research-bundle-2026-09-07/updates/enumeration_addendum.md#proposition-h-robust-farkas-certificates-with-residual-cancellation)
with its $\le$ row convention reversed.
An interval reader may lower-bound the first term and upper-bound each product over the
endpoint rectangle for $r_j$ and $z_j$. That loses correlations safely.
Every variable with a nonzero possible residual needs a valid bound; an unbounded
residual coordinate cannot be silently assigned zero.
Midpoint cancellation and a nonpositive or unresolved gap do not prove exclusion.

The coordinator’s proposed rational midpoint construction is also sound with explicit
product-error propagation.
For $t\in[a,b]$, $t_m=(a+b)/2$ and $\delta=(b-a)/2$, the functions
$c(t)=(1-t^2)/(1+t^2)$ and $s(t)=2t/(1+t^2)$ satisfy $|c'(t)|\le2$ and $|s'(t)|\le2$ for
every real $t$. Indeed $c'=-4t/(1+t^2)^2$ and $s'=2(1-t^2)/(1+t^2)^2$. Each sine/cosine
deviation is therefore at most $2\delta$. This is a chart-coordinate radius, not a
radian radius. For square $i$ with radius $\delta_i$, either corner-offset coordinate
changes by at most $2\delta_i$, so a wall row needs error at most $2\delta_i$. For a
pair normal owned by square $k\in\{i,j\}$, let $D_x,D_y$ bound the absolute
center-coordinate differences over the node.
Since normal coordinates have absolute value at most one and corner-offset coordinates
at most one, a conservative complete pair-row error is

$$
E_{ij}=2\delta_k(D_x+D_y)+8\delta_k+4\delta_i+4\delta_j.
$$

The first term bounds the center contribution; the rest bounds both products of a normal
coordinate and a corner-offset difference.
Reusing a bare $2\delta$ as the error of a whole pair row is unjustified.
This construction gives a rational outer LP without a new general interval package.
A tiny nonzero angle-box leaf is an admissible first control; BC-261 readiness still
owes its complete small case cover.

At a genuinely infeasible fixed side, compact pose domains, continuous rows, complete
SAT choices and convergent enclosures justify the review’s finite-cover existence
argument. For each complete choice, the minimum over the compact domain of the largest
row violation is strictly positive.
Sufficiently small angle boxes therefore have infeasible outer LPs.
This proves neither an effective depth nor a practical runtime, and it supplies no
uniform endpoint margin at the feasible Trump side.

The current [LP assembly](../../../../../src/sqpack/exact_lp.py) selects alternatives
from a supplied feasible pose.
Its positive phase-I path raises `ExactLPError` without returning an independently
replayable infeasibility object.
The retained implementation therefore does not satisfy this interface merely because its
internal arithmetic is exact.
A solver’s `infeasible` status is not an exported proof.

## Resource, Capacity and Anchor Premises

For a finite nonnegative measure $\mu$ and witnesses
$W_i(p)\subset\operatorname{int}S_i(p)$, a legal packing makes the selected witnesses
pairwise disjoint. If $a_i\le\mu(W_i(p))$ for every admitted pose and
$\mu([0,L]^2)\le M$, then $\sum_i a_i\le M$. A strictly larger sum excludes the whole
domain. Different measures carry separate inequalities and separate budgets; they cannot
share a smaller invented mass budget.
These are the premises of
[archived Proposition C](../../../../../resources/papers/n11-complete-research-bundle-2026-09-07/original_review/n11_research_review.md#proposition-c-a-resource-and-conflict-certificate).

Atoms on square boundaries cannot be counted using closed-square membership: the atom
$(1,1/2)$ belongs to both touching squares $[0,1]^2$ and $[1,2]\times[0,1]$. For full
closed-square capture, require $\mu(\partial S)=0$ for every admitted square.
Then intersections have zero measure and the same budget argument holds.
Area-null boundaries do not suffice for an arbitrary atomic measure.

For a reference-aligned concentric core of side $b$ and mismatch at most
$\delta\le\pi/4$, $b(\cos\delta+\sin\delta)<1$ certifies strict containment.
The weak version is enough for an inner-shape geometric relaxation but cannot license
atomic mass on a touching core boundary.
Membership in the intersection of all full anchor squares is not membership in the
intersection of their selected cores.
Each proposed atom capture requires its actual strict-core predicate.

Assign each pose to one cell of a finite complete pose cover, with an explicit rule at
overlaps and boundaries.
A binary occupancy variable requires capacity one for that entire assigned cell.
Several angle bins of one capacity-one spatial tile share that tile’s occupancy budget.
Incircle reasoning establishes capacity one when tile diameter is strictly less than
one; equality is insufficient because touching can occur.
A certified upper bound $\kappa(S)$ on compatible representatives in a cell collection
licenses $\sum_{c\in S}z_c\le\kappa(S)$. All capacities concern simultaneous compatible
representatives, not independent pairwise witnesses chosen at different poses.

For atomic captures from slots $S$, a local budget may use a set of atoms containing
every atom any selected witness from those slots can reach.
Uniform exclusion remains valid with that shared restricted budget.
An unproved capture can be weakened to zero; an unproved conflict can be omitted.
Integer occupancy cuts need an exact finite proof, such as exhaustive checked branching
or verified integer rounding from valid rows.
A discrete solver status alone does not supply that proof.

A joint downward translation of an unrestricted packing reaches a bottom contact and
preserves pair geometry and containment.
Its anchor has center $(x,h(\theta))$, with $h=(|\cos\theta|+|\sin\theta|)/2$ and
$h\le x\le L-h$. It need not be axis aligned or flush along an edge.
The reduction requires covering anchor labels and features.
It cannot be applied to a restricted family when translation would destroy prescribed
top-wall incidences.

For an anchor box $A$, a static residual domain must contain the union over all $a\in A$
of compatible residual poses.
Requiring compatibility only with a midpoint anchor can omit real packings.
Independent existential anchors for different residual slots give a sound outer
relaxation for exclusion but not a common feasible completion.
This validates
[archived Proposition D](../../../../../resources/papers/n11-complete-research-bundle-2026-09-07/original_review/n11_research_review.md#proposition-d-residual-ten-conditional-certificates).

If retaining anchor dependence, use the same actual $a$ in every residual domain and
capture function. For a fixed measure with budget $M$,
$\inf_{a\in A}[\alpha(a)+\sum_iw_i(a)-M]>0$ excludes the whole anchor box.
Loose independent minima failing to exclude establish no strict comparison advantage.

H-118 requires the two exact witnesses on identical declared domains, actual angle
relations, selected alternatives and branch policy.
Its geometric comparator includes the specified applicable ordering and projection
deductions. At exact fixed angles with complete choices, a feasible exact LP point is a
packing, so a valid resource cannot exclude it.
Strict additional strength concerns the specified outer relaxation; cheaper proof of the
same exclusion is a separate cost result.
The side-3.9 four-slot band is a control, and horizontal ordering already excludes it.

## Direct Release and Local-Scope Binding

The retained six segments are $(3,4),(3,5),(6,7),(6,8),(7,9),(8,9)$. The nine flush
incidences are square 0 at left/bottom; 1 at bottom/right; 2 at top; 3 at left/top; 4 at
top; and 5 at left. Positive-length segments force equal actual orientations modulo
quarter turns, and flush edges force the axis orientation.
The retained graph has wall component $\{0,\ldots,5,*\}$ and unanchored components
$\{6,7,8,9\}$ and $\{10\}$, hence rank nine by a spanning forest.
This is the retained equality graph’s rank.
Recontacts or new contacts can raise the full contact graph’s rank, and distinct
components can have coincident actual angles.
Neither rank nor nullity proves a feasible motion.

The direct pilot keeps $381/100\le L\le96/25$, all eleven-square containment and all 55
pair conditions. A positive rational minimum segment length gives a closed feature
restriction when the contact equations and endpoint overlap bounds are non-strict.
Shorter and zero-length siblings remain open when claiming a larger cover.
Dropping segment $(9,10)$ permits its original equality seam, point contacts and strict
separation; do not turn that removal into an implicit positive-gap requirement.
Axis and coincident component angles remain in the direct domain.
Eliminating them by a restricted-family lemma requires that lemma’s separately accepted
full scope.

The proposed side range is outside the retained local ball without subtraction.
In [the source construction](../../../../../cases/trump11/packing.py), zero-based square
3 is `axis_aligned(0, side - 1)`, so its exact center is $(1/2,U-1/2)$. Its retained top
and left flush incidences similarly force center $(1/2,L-1/2)$ throughout the release
family. The
[local chart](../../../../../cases/trump11/isolation-theorem.md#exact-witness-and-chart)
uses the same labels and origin and the sup norm on 33 center/radian coordinates; side
is not one of those coordinates.

The source gives $u\in(36/100,37/100)$ and $U=(6u+4)/(1+2u-u^2)$. The denominator is
positive and

$$
\frac{dU}{du}=\frac{6u^2+8u-2}{(1+2u-u^2)^2}>0
\quad\text{on }[36/100,37/100].
$$

Consequently

$$
\|z-z_*\|_\infty\ge U-L
\ge\frac{1925}{497}-\frac{96}{25}
=\frac{413}{12425}>\frac3{100}
>\frac{808514697}{200000000000}=\rho_{\rm row}.
$$

This separates even the closed named local ball.
It uses no tangent or radius-generator replay and no local exclusion theorem: it is a
coordinate-distance calculation from the supplied exact source and named radius.
It applies at the fixed labels and origin; other symmetry or relabeling charts need
their own mapping and comparison.
It proves no infeasibility of the release family.
Trump at $U$ remains a feasible parent/recontact control outside the target side
interval.

## Minimal Safe BC-261 Interface and Controls

BC-261 needs one actual uniform leaf and one complete small control cover before either
consumer claims instrument readiness.
The minimal shared interface is:

1. **Geometry descriptor:** declared claim scope, square labels and sizes, container
   origin and side interval or fixed side, variable order, exact center bounds, actual
   angle charts and class relations, selected directed pair alternatives, inherited
   feature equalities/bounds, and any proved contractions.
   An independent reader reconstructs physical rows from these definitions rather than
   trusting an exported matrix or choosing alternatives from a feasible source pose.
2. **Uniform leaf:** stable row identities, reference coefficients and rigorously
   justified error bounds, plus either exact outer-LP multipliers or a residual-bound
   witness. The reader recomputes the row implications, nonnegativity, cancellation or
   support bound, and strict contradiction.
   Failure returns unresolved or refused.
3. **Case cover:** parent/child domains, exact covering split and seam conventions,
   complete SAT alternatives, valid joint symmetries, terminal proofs and explicit open
   leaves, with a checked DAG. A restricted lemma carries an inclusion proof into every
   premise. A generic descriptor catalog does not fill these fields with evidence.
4. **Consumer attachment:** H-118 adds fixed measures, exact witness containment and
   capture bounds, cell assignment/capacity proofs, and its exact surviving comparator
   point. H-120 adds the variable-side wall/segment descriptor and all feature siblings
   needed by its claimed parent scope.
   Segment lengths can be enclosed or relaxed outward if the resulting leaf still
   excludes the full declared target.

| Control | Required observation |
| --- | --- |
| Feasible touching case | Its weak wall/SAT geometry is accepted; no strict gap or positive-area convention rejects it |
| Known infeasible complete small cover | Every alternative and seam closes with independently reconstructed certificates |
| Quarter-turn endpoint and equal-angle tie | The endpoint remains covered, including changed corner/axis labels |
| Omitted SAT alternative or boundary child | Complete-cover acceptance fails |
| Missing or changed physical row in a claimed complete export | Descriptor/row identity fails; a sparse dual may legitimately omit zero multipliers |
| Sign-flipped or negative multiplier; forged right-hand side | Exact Farkas replay fails |
| Widened angle or variable box | The old enclosures/domain binding are refused or recomputed; widening need not destroy every valid certificate |
| Midpoint-only cancellation and an unbounded residual | Uniform replay refuses without a proved support bound |
| Independent reflection | The claimed whole-configuration map is refused |
| Circular lemma reuse or widened lemma domain | DAG or domain-inclusion validation fails |
| Boundary atom and independent-measure budget mixing | Resource acceptance fails; strict-interior and separate-budget controls pass |
| Overlapping pose cells and shared spatial tile | Assignment represents all boundaries, and angle bins cannot duplicate capacity |
| Anchor midpoint substitution | A residual pose compatible with another anchor is still covered or the claimed union fails |
| Release recontact and rank change | The equality seam remains present even when the full graph has higher rank |
| Fixed-side substitution for the release interval | Refused unless a separate attachment-preserving reduction proves it sound |
| Local-chart label, origin or norm mutation | The square-3 distance shortcut is refused outside its bound chart |

These are prospective controls, not tests claimed to have run in this review.
Physical KKT and pair-kernel acceptance remain separate reviews.
A stationary-only leaf cannot close an all-feasible node without a representative
reduction, and neither such a reduction nor a kernel theorem is needed by the direct
leaf described here.

## Evidence, Cost and Next Action

Read-only inspection covered the named agendas, X-017/X-018, H-118/H-120, the hybrid
review, archived Propositions C, D, G and H, the retained Trump construction/local
chart, and the current exact LP assembly and phase-I error path.
The radius separation and sign conventions were checked algebraically from the displayed
formulas. No target solver run, source-control replay, new dependency, registry edit or
Git mutation was performed.
The review writes only this assigned report; the coordinator owns tracking and
integration under BC-260. `tbd prime` was used for read-only project orientation.
Failed exploratory filename globs were corrected to the actual source paths and supplied
no mathematical evidence.

The installed formatter reports Flowmark 0.4.0. The document receives a common-doc
structure/footer and AI-prose pass, targeted formatting, whitespace checking and local
link checking. There is no claim that BC-261’s prospective controls passed.

The selected next action is BC-261’s bounded export and independent reconstruction of
one uniform infeasible leaf on a complete small control domain.
The resource comparison and variable-side release designers should supply the concrete
descriptor needs above.
If the first shared leaf cannot represent a required premise, retain that named
implementation obligation and price it before a target.
No new global bound or H-118/H-120 target verdict follows from this contract acceptance.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
