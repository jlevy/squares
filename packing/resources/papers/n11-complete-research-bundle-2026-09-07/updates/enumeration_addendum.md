---
title: "From Angle Counts to a Complete Proof Cover"
subtitle: "Enumeration addendum to Beyond 3.81"
author: "Research review prepared with ChatGPT"
date: "Follow-up to the research snapshot of 6 September 2026"
lang: en-US
fontsize: 11pt
geometry:
  - margin=0.87in
  - headheight=14pt
colorlinks: true
linkcolor: NavyBlue
urlcolor: NavyBlue
toc: true
toc-depth: 1
numbersections: true
---

\newpage

# Recommendation and relation to the original review

**Integrate finite-case enumeration as the organizing structure of the proposed proof, not as a competing replacement for the resource, anchor, and kernel methods.** The user’s suggestion is mathematically sound: split competitors by rigorously defined constraints, prove that the splits cover every relevant competitor, and close the resulting cases by whatever certificate is cheapest. The difficult issue is not whether some finite description exists. It is whether one can find a description that leaves sufficiently few difficult continuous problems.

The Grok notes correctly emphasize conditional exclusions, inner approximations, and branch-and-bound. Much of that already appears in the original review and the packet’s Programs C–E. The useful additional emphasis is an explicit **case-cover architecture**: angle counts, boundary anchors, occupancy, and typed separation choices should be interchangeable descriptors in a single proof record. A complete theorem on one family should become a reusable exclusion for many later nodes. [R1, “Main proposal” and “Strengthen the main proposal”; P06, Programs C–E; P13.]

Five additions deserve explicit places in the agenda:

| Addition | What it contributes |
|---|---|
| Exact angle-multiplicity and angular-clustering descriptors | A complete, clearly quantified hierarchy of restricted problems, without assuming that all competitors have two angles |
| Quantitative transfer from exact-angle families to nearby independent angles | Converts a positive restricted-family gap into an open region of exclusion, with the geometric loss made explicit |
| A proof-carrying case-cover graph with reusable exclusions | Makes restricted results composable, and prevents an unexamined remainder from disappearing behind a list of successful cases |
| Mixed-size / mixed-shape residual problems around a rotator frame | Keeps difficult squares exact while simplifying only those whose angles are already restricted |
| Parametric LP certificates and finite stationary-side values | Exploits the existing center-elimination machinery without assuming that every optimum is rigid or unique |

These additions do not constitute a new lower bound for $s(11)$. The executable work in this addendum checks discrete catalogue completeness and elementary deductions; it does not solve the continuous cases. The original seven-row fixed-support certificate and normal-stationarity deductions remain separate results at their original scopes. Their files are preserved unchanged in the consolidated bundle. [R1; C1; C2.]

# What to retain and what to correct in the Grok notes

The following distinctions affect the mathematical agenda, not just wording.

**Inner versus outer shapes.** Replacing each square by an inscribed shape is a valid necessary relaxation. A smaller shape is weaker than the original square problem, but two different inner shapes need not be comparable to each other by inclusion. A polygonal angle-cell kernel may retain points that a shrunken square misses. Conversely, overlap of two outer envelopes is not a reason to reject the original squares. Disjoint outer envelopes can still certify that an interaction needs no further work. [P04, adaptive-core contract; P06, angle-cell kernels; Section 9 below.]

**A finite net is not an equivalent finite set of unit-square orientations at the same side.** The existing theorem supplies smaller inner witnesses. It does not allow independently rotating the full unit squares to net directions and assuming that their contacts or wall containment survive. The quantitative transfer in Section 4 is the correct replacement. [P07, proof steps 3–6; C2.]

**“At least several rotators” is not “only a few rotators.”** A lower bound on the number of intermediate tilts does not give an upper bound on the number of independent nonlinear angles. Moreover, squares near zero or near $45^\circ$ still have independent angle variables until they are handled by a uniform enclosure, a controlled inner approximation, or an actual synchronization theorem. The proposed case split must retain every count not excluded by proof. [P02, fixed-angle LP; P12, full angle domain.]

**The exact $0^\circ/45^\circ$ theorem does not, by itself, give an arbitrary positive angular radius.** It proves that a packing below its bound cannot use only those exact orientations. A quantitative neighborhood statement needs a transfer estimate or a new argument. A positive radius can indeed be deduced here; Section 4 proves one. It is smaller than the packet’s unresolved $\pm0.25^\circ$ target, so it does not silently settle H-036. [P12, “Why Uniform Core Transfer Is Insufficient.”]

**Contact counts do not prove jamming or remove all degrees of freedom.** A minimizing configuration may have rattlers or continuous equality families. One physical contact may produce several scalar rows, and those rows may be dependent. A contact graph also omits the owner axis, order, corner/edge features, wall data, and inactive feasibility constraints. The existing typed formulation and the revised physical KKT language must be retained. [P13, “Rows, contacts, and degeneracies”; R1, Propositions A–B.]

**A translational remainder is not automatically a shelf packing.** For genuinely fixed orientations, centers remain continuous and pair separations remain disjunctive. Tilted obstacles produce nonrectangular free regions. A shelf or skyline routine may propose packings or cover a restricted subfamily, but it cannot exhaust arbitrary translational placements without a normalization theorem. Fixed-angle LP plus a complete separation-case cover is the safer existing foundation. [P02, “Fixed-Angle Cells”; P16, “The cell decomposition.”]

**A unique jammed optimum is unnecessary for an exact answer.** It is enough to prove that every competitor has side at least $U$, even if several rigid packings or whole families attain $U$. A lower-bound family tending to $U$ is another sufficient route. Section 8 further shows why continuous stationary families do not imply continuously many stationary side values in the revised formulation. [R1, “The local endpoint”; P02, “Determining the value and proving uniqueness.”]

# Three different ways to count angles

## Exact shared orientations: a finite hierarchy, not a finite list of poses

Let $\mathbb T_4=\mathbb R/(\pi/2)\mathbb Z$ be the orientation circle of a square. Define

$$
k(\theta)=\#\{\theta_1,\ldots,\theta_{11}\}\quad\text{in }\mathbb T_4.
$$

This counts exact equality of orientations, not a numerical clustering tolerance. After relabeling squares, list the distinct representatives in increasing order,

$$
0\le\alpha_1<\cdots<\alpha_k<\pi/2,
\qquad m_1+\cdots+m_k=11,\quad m_j\ge1.
$$

Each $m_j$ is the number of squares at $\alpha_j$. The number of possible **ordered multiplicity profiles** for fixed $k$ is

$$
\binom{10}{k-1},
$$

because one chooses $k-1$ cut positions among the ten gaps between eleven objects. Summing over $k=1,\ldots,11$ gives

$$
\boxed{\sum_{k=1}^{11}\binom{10}{k-1}=2^{10}=1024.}
$$

The counts for $k=1,2,3,4,5,6$ are respectively $1,10,45,120,210,252$; the remaining counts reverse symmetrically. C2 enumerates all 1,024 profiles by recursion and independently checks them against the cut-position construction.

There are also only 56 **unordered integer partitions** of eleven. However, a partition such as $6+5$ does not say which multiplicity belongs to the lower angle. Either use unordered angle-class labels with every assignment retained, or use the 1,024 ordered profiles. Treating 56 unordered profiles as 56 ordered-angle problems without the missing assignments is not a complete cover.

These are top-level descriptors. Each profile still carries $k$ free class angles, 22 center coordinates, and separation choices. The $k=11$ profile is the generic all-distinct-angle problem; its existence does not disappear because the other profiles were solved. Nor can one set $\alpha_1=0$ by an arbitrary rotation: the container allows only its discrete symmetries, not continuous rotational normalization.

For certification, use closed chart covers and retain collisions between neighboring class angles. The closure of an exact-$k$ family includes lower-$k$ families. An infimum on the strict distinct-angle stratum may occur at such a collision; it is unsound to assume an interior minimizer and ignore the boundary. Overlapping closed covers are acceptable if the proof records their coverage and treats the overlap consistently.

## The at-most-$k$ optimization ladder

A cleaner sequence of theorem targets is

$$
s_{\le k}(11)=\min\{L:\text{an eleven-square packing exists with }k(\theta)\le k\}.
$$

The feasible family is compact after imposing a common finite upper bound: choose $k$ angle variables on the compact orientation circle and take the finite union over assignments of eleven squares to those variables. Thus the minimum exists. These values satisfy

$$
s_{\le1}(11)\ge s_{\le2}(11)\ge\cdots\ge s_{\le11}(11)=s(11).
$$

Trump’s construction gives $s_{\le2}(11)\le U$. Therefore a proof that $s_{\le2}(11)\ge U$ would determine **the complete two-orientation optimum**. It would not determine $s(11)$: a better packing, if one existed, would then require at least three distinct orientations. Extending to $k=3$ would sharpen that structural conclusion. This is a finite and informative hierarchy even when it does not terminate quickly.

The original six-axis-plus-five-common-angle target is a smaller first member of this program. It fixes one angle to the container axes and leaves one shared free angle, with arbitrary positions and contacts. The full two-angle target has two free angles and all multiplicities. A proof on the original Trump contact cell alone settles neither target. [R1, “Solve a natural restricted optimization problem containing Trump”; P02, lines 89–110.]

## Angle bins and cluster radii are more robust global descriptors

If the orientation circle is covered or partitioned into $r$ named bins, its occupancy vector has nonnegative integer entries summing to eleven. There are

$$
\binom{11+r-1}{r-1}
$$

possible occupancy vectors before other restrictions: 78 for three bins, 364 for four, and 1,365 for five. Every square inside a bin still has its own continuous angle.

The folded value $\phi_i=\min(\theta_i,\pi/2-\theta_i)$ can conveniently describe distance from the axes and diagonals. It does **not** specify the orientation of the square. For example, $\theta$ and $\pi/2-\theta$ have the same folded value but are generally different poses. The original signs/lifts must remain in geometric constraints. C2 gives an exact touching pair that becomes strictly overlapping when only one square’s orientation is reflected. [P12, lines 49–52; C2.]

For a proposed “few angle clusters” theorem, a useful alternative to exact equality is the continuous descriptor

$$
D_k(\theta)=\min_{\alpha_1,\ldots,\alpha_k\in\mathbb T_4}
\max_i\min_j d_4(\theta_i,\alpha_j),
$$

where $d_4$ is circular distance modulo $\pi/2$. The quantity $D_k$ is the smallest radius of $k$ orientation clusters. It is continuous, indeed 1-Lipschitz in the maximum labeled angular distance. The latter follows by applying the triangle inequality for any fixed cluster centers and then minimizing, in both directions.

The split $D_2\le\delta$ versus $D_2>\delta$ is exhaustive. The near-cluster branch can use controlled transfer or mixed-size cores; the dispersed branch can use resource and incompatibility cuts that specifically penalize angular diversity. There is currently no proof that the dispersed branch is empty below $U$. This is a better stated research question than assuming every competitor has exactly two angles.

## Seek angle synchronization through proved edge contacts

A particularly useful structural precursor is **angle-equality propagation**.
Two squares sharing a positive-length straight edge segment have parallel edge
lines, so their orientations agree modulo a quarter turn. A square sharing an
edge segment with a container wall is axis-aligned. These implications follow
directly from the geometry; a corner-edge or corner-corner contact does not give
them.

On a branch where these contact types are proved, form a graph of the forced
angle equalities, adding an axis-class node for proved edge-wall contacts.
Each connected component has one shared orientation. Count only components
containing squares; components may coincidentally have equal angles, so this
bounds the number of distinct orientations from above rather than forcing them
to be different.

This suggests a sharper missing lemma: **every relevant minimizing representative
has a forced-equality graph with at most k components**. Such a lemma, combined
with the at-most-k optimality theorem, could bypass the all-distinct-angle
remainder. It is not currently proved, and ordinary contact counts or KKT stress
support do not imply it. Only derive an equality after its geometric hypotheses
are certified; retain corner-only and zero-length-contact alternatives in the
case cover. The useful first experiment is whether typed surviving cases force
substantial equality propagation, not an assumption that their contacts do so.

# Quantitative bridges from angle families to neighborhoods

## Proposition F: the angular transfer inequality

For an arbitrary labeled orientation vector $\theta$, let $f(\theta)$ be the least container side when centers are free and all pair-separation possibilities are retained. This is not the value of one fixed contact cell or one quench run.

Suppose $d_4(\theta_i,\alpha_i)\le\delta\le\pi/4$ for every $i$, and write

$$
\gamma(\delta)=\cos\delta+\sin\delta.
$$

Then

$$
\boxed{\frac{f(\alpha)}{\gamma(\delta)}\le f(\theta)
\le\gamma(\delta)f(\alpha).}
$$

**Proof.** A unit square at $\theta_i$ contains the concentric square of side $1/\gamma(\delta)$ at $\alpha_i$: its support in either normal direction of the original square is at most $1/2$. Given a packing at side $L$, replace all its squares by these cores and scale the entire configuration by $\gamma(\delta)$. This gives unit squares at the angles $\alpha_i$ in side $\gamma(\delta)L$. Therefore $f(\alpha)\le\gamma(\delta)f(\theta)$. Interchanging the two vectors gives the other inequality. Boundary touching is legal, so non-strict containment is sufficient for this geometric transfer. A separate atomic-mass argument would still require its own strict-interior rule. $\square$

The useful corollary is not merely that a dense angle net converges. If a **complete** exact-angle family $\mathcal A$ has certified lower bound $V$, then every orientation vector within distance $\delta$ of some member of $\mathcal A$ satisfies

$$
L\ge V/\gamma(\delta).
$$

In particular, if $V>U\gamma(\delta)$, the entire neighborhood is excluded at sides at most $U$. This converts a restricted theorem with spare margin into a reusable global case exclusion. If $V=U$, any fixed positive shrink loss prevents this corollary alone from closing the final interval below $U$; use sharper branch geometry, a local theorem, or a proved limiting argument there.

## A quantitative obliquity statement already follows

Use the supplied restricted-orientation theorem

$$
s_0=2+\frac43\sqrt2
$$

for exact $0^\circ/45^\circ$ packings. If every square is within $\delta$ of one of these two orientations, Proposition F gives

$$
L\ge\frac{s_0}{\cos\delta+\sin\delta}.
$$

Thus for every $\delta$ with $U(\cos\delta+\sin\delta)<s_0$, any packing at side at most $U$ must contain a square farther than $\delta$ from **both** classes. The limiting radius of this particular transfer is

$$
\delta_*(U)=\frac\pi4-\arccos\!\left(\frac{s_0}{\sqrt2\,U}\right)
\approx0.12626249^\circ.
$$

The corresponding indicative radii at target sides 3.82, 3.84, and 3.85 are about $0.99285^\circ$, $0.68477^\circ$, and $0.53255^\circ$. These rounded values are explanatory only. Any actual exclusion uses a radius strictly below the limit or a separately checked endpoint statement.

For a very simple exact version, take

$$
q=\frac{38771}{10000}=3.8771>U,\qquad \delta=\frac1{500}\text{ radians}.
$$

C2 checks $U<q$ directly from the supplied defining polynomial and isolating root. Since $\sqrt2>1414213/10^6$ and $\cos\delta+\sin\delta\le1+\delta$,

$$
2+\frac43\frac{1414213}{10^6}
-q\left(1+\frac1{500}\right)
=\frac{11447}{15000000}>0.
$$

Consequently every eleven-square packing with side at most $q$, if one exists, has a square more than $1/500$ radians, approximately $0.11459^\circ$, from both the axes and diagonals. This is a deduction from the supplied restricted theorem, not a fresh proof of that theorem or a claim of publication novelty.

It does **not** prove that two or more squares are this far from both classes. It does **not** prove H-036, whose radius is $0.25^\circ$ at side 3.878. The existing uniform transfer loses too much for that stronger target. [P12, “Why Uniform Core Transfer Is Insufficient”; C2.]

## Combine distinct count restrictions without confusing them

The packet’s nine-point argument provides a different restriction: at most nine squares can be sufficiently near the **axis** class. The tilted exceptions may be near $45^\circ$; they need not be in the intermediate class. [P10, lines 317–326.]

For the same $q$ and $\delta=1/500$, a near-axis unit square contains a strictly interior axis-aligned core of side $b=1/(1+\delta)$. The strictness follows because the true maximum $\cos\delta+\sin\delta$ is less than $1+\delta$. Moreover,

$$
4-q(1+\delta)=\frac{575729}{5000000}>0,
$$

so $b>q/4$. Each such core contains a point of $\{q/4,q/2,3q/4\}^2$, and disjoint cores cannot share a point. Hence at most nine squares are near-axis.

Partition folded angles into near-axis, strict-middle, and near-$45^\circ$ bins, assigning both cutoff boundaries to the near bins. If their counts are $(a,m,d)$, every candidate at side at most $q$ satisfies

$$
a+m+d=11,\qquad a\le9,\qquad m\ge1.
$$

There are 65 integer profiles left from the original 78. C2 checks this enumeration. This modest reduction is a control and a reusable lemma, not evidence that the final enumeration is small. The packet’s sharper near-axis threshold can be used separately; there is no reason to weaken it in production just to use a common radius.

# Make the enumeration a proof-carrying case cover

## The object to build

A case should identify a domain of configurations, not merely a graph, an angle count, or a list of approximate coordinates. It may specify a side interval, orientation charts, exact class equalities or interval memberships, center tiles, boundary anchors, selected separation alternatives, and existing certified exclusions.

The root domain can represent either all competitors below a target $T$ or all globally side-minimizing representatives in the relevant sublevel. The latter is sufficient for a value-only proof once compactness supplies a minimizer whenever a better packing exists. State this choice explicitly: a certificate valid only at physical stationary points cannot prune an all-feasible-configuration node without that reduction. [P13, compactness; R1, Propositions A–B.]

A small generic record would carry:

```text
case_id; parent_ids; target_side; configuration_domain
scope: all_feasible | original_stationary | restricted_family
split_cover_proof; symmetry_or_relabeling_map
certificate_kind; certificate_inputs; status
remaining_open_domain
```

This is a proposed interface, not a finished solver schema. The indispensable fields are the complete domain, the parent-to-child cover argument, and the leaf’s actual proof. Merely accepting this record format establishes nothing geometrically.

## Proposition G: finite-cover composition

Let $\mathcal F$ be a set of competitor representatives such that a packing below $T$ would imply $\mathcal F\ne\varnothing$. Let a finite rooted case graph satisfy:

1. Its root covers $\mathcal F$.
2. Every split covers its parent’s relevant configurations by its children; a symmetry reduction supplies a valid map of the entire configuration and its constraints.
3. Each terminal node is proved empty, or proved to have side at least $T$.

Then no packing below $T$ exists. If $T=U$, the known construction gives $s(11)=U$.

**Proof.** A better packing supplies a root representative. Follow the coverage maps and splits to a terminal node. That node cannot contain the representative by its terminal certificate. The graph is finite and acyclic, so a terminal node is reached. $\square$

Children may overlap. Boundary strata must be covered somewhere. An unresolved terminal node keeps the global conclusion unresolved. A lower-dimensional contact family cannot be discarded because it has zero volume in the original pose coordinates.

## Reuse exclusions rather than multiply every descriptor

Do not eagerly form the Cartesian product of all angle profiles, all center-tile selections, all wall signatures, and $8^{55}$ pair choices. An adaptive case graph should choose a descriptor only when it improves the current bound. An exact exclusion of a three-square subsystem becomes a no-good for every eleven-square case containing it. A conditional resource inequality remains reusable on every domain where its hypotheses hold. Two nodes can share a proved subcase or lemma instead of duplicating its computation.

This is the proper role for lazy SAT/LP/interval reasoning and subsumption. Every learned clause must carry the exact geometric or algebraic implication that makes it valid. Uncertainty about a pair produces no conflict edge; it does not certify compatibility. The original resource model and two-pose kernel are possible node-level bounding methods, not rival definitions of the cases. [R1, Propositions C–E; P06, “Cell hyperedges.”]

A relevant primary precedent is Montanher and coauthors’ rigorous three-square-in-a-circle proof. They use capacity-one center tiles and solve smaller subproblems before extending combinations. That supports the partial-assignment architecture, but their three-square experiment supplies no runtime forecast or completeness shortcut for eleven squares in a square. [W5, Sections 4–5.]

# Rotator frames and mixed-size residual packing

## Keep the frame exact; simplify only the proven remainder

The strongest part of the frame idea is conditional, heterogeneous simplification. Suppose a branch specifies $r$ frame squares in pose boxes and restricts each of the other $11-r$ squares to within $\delta_i$ of a reference orientation $\alpha_i$. Replace only these latter squares by concentric reference-oriented squares of side

$$
b_i=\frac1{\cos\delta_i+\sin\delta_i},
$$

or a rigorously smaller rational side. Keep every frame square full size and keep its pose variable within its entire box. If this mixed-size necessary problem is impossible, so is the original branch. No common rescaling is needed.

This retains more geometry than uniformly shrinking all eleven squares. It can exploit a large frame square’s exact forbidden region while treating tightly bounded nuisance angles as translations of slightly smaller squares. It is especially natural near an axis-aligned remainder, but near-$45^\circ$ squares form a different translational family and must not be merged into the axis class.

A relaxation with different core sizes still needs the ordinary mixed-size containment and separation formulas. A pair of core squares of sides $b_i,b_j$ has the corresponding scaled projection radii. A full frame square uses side one. An infeasible sample frame does not close its box: the exclusion must hold uniformly throughout the frame domain.

For a box $b$ of possible frame poses, guaranteed occupied regions such as the intersection of all squares in $b$ supply safe, cheap forbidden regions for the remainder. They may be much weaker than keeping the frame variables. Use them as an outer relaxation of the residual feasible set, not as an assertion that every compatible remainder can be completed by one common frame.

## Master/subproblem decomposition

A practical master problem chooses frame locations or boxes, angular bins, and coarse residual occupancy. Its subproblem tests the entire residual domain by resource bounds, mixed-size geometry, exact fixed-angle LPs, or interval-certified angle boxes. A certified residual contradiction returns a reusable condition on the master variables.

The logical point is crucial: if each residual square is individually compatible with *some* frame in a box, the independently selected frames may differ. Allowing this only enlarges the residual problem, so proving it impossible is safe. Calling it feasible would not certify a common completion. Stronger subproblems retain the common frame variables or add jointly verified no-goods.

The frame itself must be forced by a theorem or included in a complete outer case cover. Named pictures such as a diagonal belt, a $40^\circ$ block, or a rational-slope pattern are useful proposal families. They are not exhaustive until a covering argument proves that every remaining competitor belongs to one of them.

## The first useful frame result

Choose one broad bottom-wall anchor family, as in R1, and then a small number of additional frame hypotheses. Try to prove a complete residual-capacity inequality on that family, not merely solve one numerical completion. If one anchor leaves too much freedom, test a second anchor or one angle-count condition before adding a large catalogue of contact graphs.

Record the quantitative loss caused by the chosen $b_i$, the domain closed, and the cases left open. A feasible mixed-core configuration may diagnose that the relaxation is too weak; it is not a packing of full unit squares. A failed shelf search says still less.

# Parametric LPs are the most natural continuous leaf engine

## Cover parameter regions, not sampled angles

For a fixed separation branch and a fixed angle-class assignment, write the center-and-side constraints as

$$
A(t)z\le b(t),\qquad z=(x_1,y_1,\ldots,x_{11},y_{11},L),
$$

where $t$ comprises rational half-angle chart variables. For an exact-angle profile there are $k$ such variables; in the six-axis-plus-five-common-angle problem there is only one. The functions are rational with explicitly positive chart denominators. At each fixed $t$, the problem is a 23-variable LP. [P02; P16.]

The promising extension is to turn a useful numerical LP dual into a theorem valid throughout a whole $t$-box. A large angle grid with one floating LP per point is not a substitute. Nor is it enough to track the basis selected by one local solver: an unvisited basis may support a better configuration.

## Proposition H: robust Farkas certificates with residual cancellation

Suppose all relevant center-and-side variables lie in a known box $\ell\le z\le u$, and choose rational $y\ge0$. Define

$$
r(t)=A(t)^Ty.
$$

Every feasible point must satisfy

$$
\sum_j\min\{r_j(t)\ell_j,r_j(t)u_j\}
\le r(t)^Tz\le y^Tb(t).
$$

Therefore a uniform proof of

$$
\boxed{\inf_{t\in I}\left[
\sum_j\min\{r_j(t)\ell_j,r_j(t)u_j\}-y^Tb(t)
\right]>0}
$$

excludes the entire parameter box $I$. This remains sound when a rounded dual does not cancel the center coefficients exactly. Ordinary Farkas cancellation is the special case $r\equiv0$ and $y^Tb<0$.

C2 implements a conservative rational interval version of this inequality and tests coefficient-widening and missing-row traps. It does not assemble the packing coefficients or prove that a proposed enclosure covers all angles. Those remain the geometry engine’s obligations.

For a promising restricted branch, search for duals at informative parameter values, then enlarge the region on which each dual is certified. Split only where the certificate fails. This targets **certified parameter coverage per useful dual**, rather than number of numerical LP calls.

## Basis elimination is complementary, not a completeness shortcut

R1 proves that some global minimizing representative is a vertex of a fixed-angle center LP. For a nonsingular 23-row basis $B$,

$$
z(t)=A_B(t)^{-1}b_B(t)
$$

is a rational function of the angle parameters. Feasibility and a side comparison reduce to signs of polynomials after denominator signs are certified. In a one- or two-angle family, this may expose short wall-to-wall inequalities or an algebraic endpoint relation.

The determinant-zero loci, alternate bases, support ties, and angle-collision boundaries must remain covered. “One numerical root for each observed graph” is not a proof that all bases or all roots have been found. Use basis elimination to simplify surviving cases after a coverage framework exists, and use uniform dual certificates whenever they can close a domain without enumerating its vertices.

# Finite stationary side values do not require rigid optima

## A useful consequence of the revised normal-KKT formulation

The original review proves a strict feasible-direction condition for the physical branch formed by all corner-wall constraints and all sixteen corner-projection inequalities for each chosen pair separation. The side is variable and the local angle chart is open. Hence every minimizing representative has normal KKT multipliers, with $\sum_j\lambda_j\le L+1$. No generic-position or rigidity assumption is used. [R1, Propositions A–B.]

After rational angle substitution and clearing positive denominators, the normal stationary systems are semialgebraic. They have finitely many connected components, each with piecewise continuously differentiable semialgebraic connecting paths. These are standard real-algebraic facts; they do not make component computation inexpensive. [W4, Sections 2–3.]

## Proposition I: the side is constant on each stationary component

Consider one such physical branch, with inequalities $g_j(z)\ge0$, and its normal stationary pairs $(z,\lambda)$ satisfying

$$
\nabla L=\sum_j\lambda_j\nabla g_j,
\qquad \lambda_j\ge0,\qquad \lambda_jg_j=0.
$$

Along a continuously differentiable segment of a path in this set,

$$
\frac{dL}{ds}=\sum_j\lambda_j\frac{d}{ds}g_j(z(s))=0.
$$

Indeed, if $\lambda_j>0$, complementarity gives $g_j=0$ at that parameter value. Since $g_j(z(s))\ge0$ along the path, its derivative there is zero. If $\lambda_j=0$, its contribution is zero anyway. Thus $L$ is constant on each smooth segment, and continuity makes it constant on the entire connecting path.

It follows that each connected component carries a single side value. Since there are finitely many components and finitely many physical branch/chart choices,

$$
\boxed{\text{Only finitely many normal stationary side values occur in a bounded sublevel.}}
$$

With the algebraic input conventions used here, those finitely many side values are algebraic as well: their set is a finite semialgebraic projection over real algebraic coefficients.

This is a **deduction**, not an enumeration of the values or a claim of novelty for the general stationary-component principle. It is relevant because the preceding constraint qualification ensures that a global minimum is not lost by using normal stationary systems. It gives a theoretically finite target even when equality configurations form curves or rattler families.

## What this does and does not buy

A value-only program could eventually enumerate or bound stationary **components or values**, rather than insist on finitely many rigid poses. Several distinct components may have the same minimal side. Showing that every component’s side is at least $U$ would be sufficient; uniqueness is unnecessary.

But isolating all components may still be vastly harder than proving an inequality that excludes an entire branch. No useful bound on the number of components, their algebraic degrees, or the n=11 computational cost is obtained here. A small numerical gap to $U$ cannot be closed by invoking unspecified algebraic separation bounds.

The stationarity model must also match the theorem target. In a deliberately restricted shared-angle optimization, there is one torque equation per class. For an original freely rotating minimizer, there is one torque equation per square. Replacing the latter by class-summed equations creates a weaker necessary system; it is safe as an outer relaxation, but does not certify original stationarity or justify an assumed synchronization. A restricted optimum need not be an unrestricted stationary point.

Artificial angle-bin or chart-boundary constraints must not invalidate the physical constraint-qualification argument. Derive physical stationarity first, then intersect its solution set with search boxes. The old sign-partitioned formulation retains its own abnormal-case obligations unless the revised formulation has actually replaced it. [R1, “What this changes, and what it does not.”]

# Other shapes: retain the useful roles, reject the wrong ones

## The disk relaxation has an explicit low ceiling

There is no need to rely on a current disk-packing record to see that replacing every square by its diameter-one incircle is too weak for a standalone improvement beyond 3.81. The twelve disk centers

$$
\left(\frac12+c+\frac{r\bmod2}{2},\;
\frac12+\frac{13r}{15}\right),
\qquad r=0,1,2,3,\quad c=0,1,2,
$$

fit in a square of side $18/5=3.6$. Same-row neighboring centers are one apart. Nearest adjacent-row centers have squared distance

$$
\frac14+\frac{169}{225}=\frac{901}{900}>1.
$$

More distant rows are farther apart, and every center stays at least $1/2$ from the container walls. C2 checks all 66 pairs and all wall distances exactly. Therefore eleven such disks already fit by 3.6. The unconditioned disk non-fit problem cannot prove a side lower bound above 3.6 for the squares.

This does not make disks useless. Their center-distance implication supplies the original review’s coarse capacity-one tiles and fast local conflicts. A globally weak relaxation may be effective inside a heavily conditioned branch. [R1, “A very small starting spatial cover exists”; W5, Lemma 3.]

## Selective surrogate refinement is better than a single substitute shape

Inside each branch, start with cheap inner shapes or guaranteed occupied regions. When a spurious relaxed packing survives, strengthen only the poses or pairs responsible for it: disk to polygon, coarse common core to an angle-dependent kernel, then the full square if necessary. A proof may use different inner shapes for different squares, provided the containment implication is uniform on the stated branch.

The comparison is about preserved constraints, not merely area. Adding a corner or a support direction that resolves the active conflict can matter more than adding area elsewhere. Conversely, adding an inner shape that is contained in the current witness supplies no stronger exclusion unless it enables a different, cheaper certificate.

There is also a legitimate convergence statement. If a centrally placed shape $K$ satisfies

$$
\beta Q\subseteq K\subseteq Q,
\qquad Q=[-1/2,1/2]^2,
$$

and rotations are allowed consistently, then their optimal container sides satisfy

$$
\beta s_Q(11)\le s_K(11)\le s_Q(11).
$$

The right inequality follows by replacement; the left follows by extracting $\beta Q$ from a $K$-packing and rescaling. Hence a nested sequence of suitable inner shapes with $\beta\uparrow1$ converges to the square optimum. This is a proof of convergence, not a claim that those surrogate problems are easier. A finite list of numerical surrogate solutions supplies neither their exact optima nor the limiting lower-bound theorem.

The original fixed strictly shrunken-square mechanism retains its known ceiling. That ceiling does not apply automatically to every larger polygonal kernel, mixed-size branch, or convergent hierarchy. Outer envelopes remain useful for proving that certain interactions can be skipped, never for rejecting originals solely because the envelopes overlap. [P10, “Thresholds to Read at Their Exact Scope.”]

# Revised agenda: add structure without starting another oversized solver

## First deliverable: a common case language and one honest catalogue

Adopt the distinction between exact angle profiles, interval occupancy, and cluster radius. The supplied C2 catalogue already verifies the discrete counts and simple cuts. The next implementation should attach these descriptors to the existing pose domains and export a checked parent-to-child covering relation. Include zero/quarter-turn seams, equal-angle collisions, independent orientation lifts, and valid whole-configuration symmetry maps as controls.

A complete list of descriptors is a useful interface control, but not a research success by itself. Require a nontrivial continuous family to close before expanding the schema or multiplying descriptor combinations.

## Main mathematical pilot: a complete restricted family, with reusable neighborhood bounds

Keep the six-axis-plus-five-common-angle theorem as the most focused contact-independent target. Use uniform parametric LP exclusions and selected basis elimination, not the retained Trump contact graph as an assumption. Record all surviving parameter intervals and every unresolved separation branch.

Then price the complete at-most-two-angle problem, with all ten ordered two-class multiplicities and both absolute class angles. Its success would determine $s_{\le2}(11)=U$. Apply Proposition F to any subfamilies excluded with margin, turning them into neighborhood exclusions for the general problem. At endpoint families with no margin, keep direct geometry or local closure.

The three-or-more-angle remainder stays explicitly open. Test it through the angular-cluster split and resource/anchor machinery. Do not infer that it is empty from repeated numerical returns to a two-angle construction.

## Main substantial-bound pilot: integrate counts into the resource/anchor model

At a substantial target such as 3.84, combine the original coarse center tiles and boundary anchors with one small angular occupancy partition. Each nonnegative measure retains its own capacity inequality. Add mixed-size residual relaxations only on the branches where angular localization is already proved. Return exact low-order incompatibilities and uniform dual inequalities to the common case graph.

This keeps the original review’s central recommendation intact. Enumeration organizes the proof; measures, geometric conflicts, LP duals, kernels, and local theorems close its leaves.

## Preserve the high-upside kernel pilot

The two-pose kernel is still a credible alternative source of stronger bounds, supported by the compact packing-graph hierarchy framework. It may close many cases without explicit contact enumeration, or supply stronger bounds inside an anchor/angle branch. The framework’s convergence does not guarantee that a low-degree feature family will work efficiently here. [R1, Proposition E; W6.]

Do not redirect the entire program to a contact atlas merely because its language is finite. The meaningful comparison is which method closes broad complete domains with reviewable certificates.

## Success and stop criteria

| Work item | Evidence that warrants expansion | Evidence that calls for a change |
|---|---|---|
| Angle-family enumeration | A complete nontrivial angle interval or whole multiplicity family is closed | Only sampled angles or one selected contact graph are solved |
| Parametric LP certificate reuse | A small collection of exact duals covers substantial parameter domains | Each microscopic box requires unrelated branching and no reuse emerges |
| Rotator-frame residuals | Uniform residual-capacity bounds eliminate broad frame boxes | Only exact sample frames fail, or shrunken residuals admit many unrelated completions |
| Cluster-radius split | The dispersed branch receives a genuine bound, or the near-cluster branch contracts sharply | An upper bound on cluster count is assumed instead of proved |
| Case-cover system | Leaf certificates compose with no missing boundaries or unexplained remainder | Percentage of sampled cases closed is used as a substitute for coverage |

None of these failure modes disproves the general method class. They identify the current representation or relaxation that needs changing.

# What was actually checked and what is still open

The consolidated bundle preserves the original report, its PDF build assets, its exact fixed-support checker, its tests, and its retained outputs. The original checker and tests were run again during this follow-up; normal and optimized Python outputs agree. This is a fresh replay of the same implementation, not a new independent mathematical review. The historical 3.81 coverage computation and the omitted full Trump-radius archive were not rerun.

The new C2 work comprises complete discrete angle-profile enumeration, the 78-to-65 elementary histogram calculation, a rational proof of the needed side enclosure and obliquity arithmetic, the twelve-disk control, exact counterexamples to unsafe angle simplifications, and a generic robust-Farkas arithmetic helper with known-answer and mutation tests. It does not solve a new full-domain n=11 branch, prove the six-plus-five conjecture, establish an upper bound on the number of rotators, or improve the global lower bound.

Propositions F–I are mathematical deductions with proofs in this addendum. Their general ingredients are standard; no publication-priority claim is made. Their application to the research architecture is the point. They remain available for independent review before integration into a final proof.

**Bottom line.** The best version of the enumeration idea is not “list a few plausible frames and solve them.” It is “maintain a finite, explicit cover of all competitors, learn broad certified exclusions, and progressively replace the open remainder by simpler cases.” Exact angle counts are useful labels; angular neighborhoods and residual capacity are more likely to make those labels computationally productive. A single optimal value can be established even when the equality configurations are not unique or rigid.

# References and bundle guide

**R1.** Original report, *Beyond 3.81: A Research Strategy for Eleven Squares*, preserved in `original_review/` with its exact certificate and build assets.

**P00–P18.** The supplied research packet, frozen at revision `4d305597a505ebfbe85f1851fa7148374661e622`, preserved in `source_packet/`. These labels use the same file-prefix map as R1. In particular, P02 is tooling; P06 is prior alternative strategies; P07 is the standalone 3.81 proof; P09 is the construction/local theorem; P10 is scoped barriers; P12 is restricted orientations; P13 is typed stationarity; and P16 is mathematical background/source lemmas.

**G.** User-provided Grok notes in the follow-up request. They are reviewed proposals, not independent evidence for a packing theorem. The point-by-point assessment in Section 2 identifies the retained ideas and corrections explicitly.

**C1.** `original_review/certificate/`: the seven-row fixed-support certificate, checker, tests, and original outputs. Fresh same-code replays are in `evidence/`.

**C2.** `enumeration/`: `enumeration_checks.py`, `test_enumeration.py`, `profile_catalogue.json`, `elementary_results.json`, and `test_results.json`. The directory README gives execution instructions and its restricted scope.

**W4.** Saugata Basu, *Algorithms in Real Algebraic Geometry: A Survey*, arXiv:1409.1534. Sections 2–3 provide the real-algebraic framework for quantifier elimination, finite sign decompositions, connected components, and roadmaps. [Primary text](https://arxiv.org/html/1409.1534). The new application to normal stationary side values is proved in Section 8 here, rather than attributed as a square-packing theorem of that survey.

**W5.** Tiago Montanher, Arnold Neumaier, Mihály Csaba Markót, Ferenc Domes, and Hermann Schichl, *Rigorous packing of unit squares into a circle*, Journal of Global Optimization 73, 547–565, issue 2019; published online 3 October 2018. DOI: 10.1007/s10898-018-0711-5. Sections 4–5 supply the tiling and incremental-subproblem precedent. [Primary article](https://link.springer.com/article/10.1007/s10898-018-0711-5).

**W6.** David de Laat and Frank Vallentin, *A semidefinite programming hierarchy for packing problems in discrete geometry*, arXiv:1311.3789v3. Relevant to the retained interaction-kernel program, not a ready-made finite enumeration of n=11 squares. [Primary text](https://arxiv.org/html/1311.3789v3).

No exhaustive public-record or novelty search was undertaken for this follow-up. The frozen user packet remains the basis for the research status, and the external sources supply method context only.
