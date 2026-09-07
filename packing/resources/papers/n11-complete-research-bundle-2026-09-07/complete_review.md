# Eleven squares: complete research review

This file combines the enumeration addendum (Part I) and the original research review (Part II). See `updates/integrated_agenda.md` for the current condensed work plan. The separately preserved original report, exact certificate, and source packet keep their original evidence scopes.

# Part I — Enumeration addendum


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


---

# Part II — Original technical research review


# Executive assessment

**The research program should now make compatibility between squares its main source of additional strength.** Continue one bounded attempt to obtain an inexpensive scalar improvement, but do not make a long sequence of increasingly elaborate one-square verifiers the prerequisite for configuration-level work. The most credible substantial advance is a hybrid: coarse, rigorous pose classes; resource inequalities that retain the existing weighted-measure machinery; conditional exclusion after fixing one or two boundary squares; and a much cleaner stationary formulation for the surviving branches.

This recommendation is not based on a proved universal barrier at 3.82. The packet has not established such a barrier. It is based on the mismatch between the desired result and the information represented by the current successful relaxation. A one-square covering inequality knows that each square must consume mass, but it does not fully encode whether eleven low-cost square poses can coexist. Refining that inequality can still help, yet there is no supplied evidence that doing so alone will recover the missing geometric compatibility. [P01, “How the Eleven-Square Work Reached This Point”; P10, “The Bridge”; P06, “Configuration-level integrality.”]

Two concrete results emerged during this review, rather than merely two further suggestions.

**First, the full-size density support question can be settled for the support already in the packet.** The proposed mass-$56/5$ weighting is not almost-everywhere feasible: its depth is exactly $7/5$ throughout an explicit positive-area rational box. More importantly, seven rigorously checked necessary depth inequalities have a nonnegative rational combination proving that *every* weighting on that same 60-placement support has mass at most eleven. The known average of the eight Trump packings attains eleven. Thus the full fixed-support optimum is exactly eleven. This is a new computation from the supplied formulas, not a reinterpretation of exp-113 or exp-115. A standard-library checker and mutation tests accompany this report. It changes the next density experiment, but changes no bound on $s(11)$. [C1; P09; P11.]

**Second, abnormal Fritz–John branches are unnecessary in a suitable physical formulation.** Replace support-sign partitions by smooth corner-to-corner projection inequalities, and leave the container side variable free. Dilating centers and the container, without dilating the unit squares, strictly increases every active physical constraint. This proves a constraint qualification at every feasible point of each such branch. All stationary candidates can therefore use ordinary KKT multipliers. Their total mass is bounded by $L+1$, and a stationary multiplier certificate can be chosen with at most 34 positive scalar rows. Ties and rattlers remain, but the abnormal multiplier branch and artificial sign-stratum complications disappear. This is a proved deduction below, not an assumption of generic position.

The highest-priority directions are consequently:

| Priority | Direction | First genuinely useful outcome |
|---|---|---|
| Main program | Coarse integral resource model, strengthened by one- and two-wall-anchor conditional certificates | Exclude a substantial full-domain target such as $L=3.84$, or identify a small, explicit family of unresolved geometric cases |
| Enabling theorem | Smooth physical branches, bounded normal stresses, and fixed-angle vertex representatives | A smaller stationary search language and a complete nontrivial branch exclusion |
| High-upside parallel pilot | A two-pose positive-semidefinite kernel on the bounded placement space | A certified bound below eleven, or a precise obstruction to the chosen feature family |
| Selective one-body work | Equality-support geometry; boundary-null curved measures; below-$U$ densities | A demonstrably stronger resource representation, not another instrument without a candidate |

The side $3.84$ is an illustrative milestone, not a forecast: reaching it would close about 45% of the current bound gap. Reaching $3.85$ would close about 60%. By comparison, $61/16=3.8125$ closes about 3.69%. These are arithmetic comparisons against the packet’s endpoints, not estimates of difficulty.

The exact-value goal should be stated as **prove $s(11)=U$**, not “prove that Trump is the only optimum” unless uniqueness is independently valuable. Exact branch lower bounds or a proved family of lower bounds tending to $U$ can establish the value without classifying every equality configuration. A small numerical gap alone cannot invoke a local isolation radius.

## Scope and evidence labels

This report uses the complete supplied packet, including the full Agenda 024, the source dossiers, the embedded T-018 verifier and certificate, and the Trump diagram. The packet is frozen at revision `4d305597a505ebfbe85f1851fa7148374661e622`. Its reported construction, lower-bound, local, and experimental results are used at their stated scopes. I did not rerun the historical campaign or reconstruct its omitted tangent/modulus archives. I did parse the complete T-018 atomic data; this was inspection, not a new coverage verification. [P00; P17.]

**Packet result** means a result supplied in that snapshot. **Deduction** means an argument proved in this report from stated premises. **Review computation** means a newly executed calculation, with the exact checker distinguished from exploratory numerics. **Proposal** means an unproved research direction. No claim of external publication priority is made for the new deductions or certificate.

# What the existing work has earned

## A strong lower-bound mechanism, not yet an exact-value mechanism

The retained bracket is

$$
L_* = \frac{38100\sqrt{8100042893309449}}{899996306539}
\le s(11)\le U,
$$

with

$$
L_*=3.810025723614703\ldots,
\qquad U=3.8770835900228141773\ldots.
$$

T-018 supplies the simpler $3.81$ bound with 1,121 atoms, 181 directions, core side $B=9977/10000$, total mass $434547/40000$, and minimum core mass $4001/4000$. T-022 extracts the stronger displayed endpoint through a strict family of dilations and a limiting argument. It is not an endpoint no-fit certificate. [P01, “The Problem and the Exact Bracket”; P07, “The Theorem”; P08.]

The achievement is not just a decimal improvement. The project has an effective separation oracle for a continuum of one-square placements, exact arithmetic at the acceptance boundary, a second coverage mechanism, and a disciplined distinction between proposed and certified objects. Those are reusable mathematical assets. The limitation is equally specific: increasing the expressive power of the one-square resource does not automatically impose consistency among eleven placements.

There are three separate losses to diagnose:

**Geometric witness loss.** Shrinking and snapping to a direction net makes the admissible witness family larger than the family of cores actually selected from unit squares. The frozen scalar mechanism has a Trump-derived ceiling near $3.868983$, with the finite-net angular correction included. A new net or witness changes this ceiling; the exact core/net ceiling says nothing about all possible measures. [P10, “Thresholds to Read at Their Exact Scope.”]

**Representation and optimization loss.** Frozen atom sites, stopped column generation, conservative rationalization, and incomplete continuum verification can all prevent a valid certificate from being found. At 3.82 the exact fractional-packing lower endpoint is approximately $10.384212408$, whereas the retained $11.055616943$ covering objective is computational, not an accepted exact covering measure. These do not establish that the unrestricted covering optimum is eleven. [P01, lines 124–147; P02, “Generating Measures and Bounding Their Possible Reach.”]

**Integrality loss.** Even an exactly solved one-body relaxation may admit a weighted superposition of incompatible placements of total mass at least eleven. Eliminating this loss requires either a special geometric theorem showing that this instance has no gap, or a proof system that encodes interactions. Neither finer angular sampling nor more accurate LP arithmetic addresses that issue by itself.

The packet already recognizes these distinctions. The strategic change proposed here is to make them determine the *order of research*: do not require the first two losses to be minimized before testing whether modest interaction information is decisive.

## The local endpoint is useful, but should not dictate the whole search

The local Trump theorem provides a strict sup-norm neighborhood of radius

$$
\rho=0.004042573485
$$

in the specified labeled, anchored 33-coordinate center/radian chart. A packing of side at most $U$ in this neighborhood must be the retained pose and have side $U$. Its current quantitative assurance is retained-record-dependent; the complete per-face witnesses were not independently replayed in the supplied review. [P09, “Theorem” and “Later BC-241 Review Scope.”]

This is a valid kind of final leaf. It is not necessary that every successful global method route through it. A branchwise inequality $L\ge U$ could close a larger family directly. A different optimum at exactly $U$ would not prevent determination of the value. A proved uniform family $L_k\uparrow U$ would also suffice. Conversely, even a lower bound of $U-10^{-6}$ would not imply that a competing packing lies within $10^{-6}$, or within $\rho$, of Trump in configuration space.

The correct intermediate deliverable is therefore a **complete family of remaining cases with explicit closing mechanisms**. “Closer to Trump’s side” and “closer to Trump’s pose” must remain different metrics.

## What should not drive the next allocation

The fixed-weight shrinking negatives justify parking that mechanism. They do not justify abandoning all changed support or non-square witnesses. The failed inset/release comparison disposes its tested seed rule, not every geometric prior. The restricted-angle work has earned seven exact-angle auxiliary clauses, not the continuous $\pm0.25^\circ$ theorem. Completing that theorem could be worthwhile, but by itself it only excludes a narrow orientation family far from the known tilt. [P10; P12; P14.]

Similarly, the 23-million-cell near-tight census should not become the mandatory representation of the integral problem. Those cells are artifacts of the resource arrangement, useful for exact one-square integration but not necessarily the right atoms of a global proof. A much coarser geometric cover can carry conservative resource bounds and be refined only where compatibility requires it.

# New exact result: the Trump-orbit density support has optimum eleven

## The question settled

Let $\mathcal F$ be the 60 distinct full-size square placements obtained from the supplied Trump construction by the eight symmetries of its container. The packet’s eight orbit representatives, in order, are original square labels

$$
(0,2,4,7,10,8,6,9),
$$

and their orbit sizes are

$$
d=(4,8,8,8,8,8,8,8).
$$

Write $a_j\ge0$ for the weight of each distinct member of orbit $j$. The total weight is $d\cdot a$. Almost-everywhere feasibility means that the weighted depth is at most one except on an area-zero set. [P11, “Exact Candidate and Necessary-Row Data.”]

**Review computation, with an exact certificate.** The optimum of this full fixed-support problem is exactly eleven. This also bounds nonsymmetric weightings on $\mathcal F$: averaging such a weighting over $D_4$ preserves both total mass and almost-everywhere feasibility, and yields an orbit-constant weighting.

## A positive-area counterexample to the $56/5$ weights

The proposed weights are

$$
a^{\rm cand}=(1,0,2/5,1/10,0,1/10,3/10,0).
$$

On the entire closed box

$$
\left\|x-(97/50,71/50)\right\|_\infty\le\frac1{100000},
$$

the exact orbit-incidence vector is

$$
(0,0,0,0,0,2,4,2).
$$

Consequently the candidate depth is

$$
2\left(\frac1{10}\right)+4\left(\frac3{10}\right)=\frac75>1.
$$

The checker proves strict membership or strict exclusion for every support square throughout this box. Thus this is an area-positive violation, not a boundary artifact. Four weight-$3/10$ squares already create excess depth; none of their pairs has weight above one. This is consistent with exp-115’s successful exclusion of every overweight *pair*. [C1.]

## Seven necessary rows close the whole support

Every almost-everywhere feasible orbit weighting satisfies $Ra\le\mathbf1$, where

$$
R=\begin{pmatrix}
1&1&0&0&1&0&0&0\\
1&2&0&0&0&0&0&0\\
0&1&1&0&1&0&2&2\\
0&0&2&2&1&0&0&1\\
0&0&2&2&2&0&0&0\\
0&0&0&1&0&2&3&2\\
0&0&0&0&0&4&2&2
\end{pmatrix}.
$$

Each row is realized, with constant incidence, on a box of sup-norm radius $1/100000$ about the corresponding point:

| Row | Box center | Multiplier |
|---:|---|---:|
| 1 | $(961/1000,752/1000)$ | $1$ |
| 2 | $(922/1000,922/1000)$ | $3$ |
| 3 | $(2621/1000,3017/1000)$ | $1$ |
| 4 | $(1887/1000,2893/1000)$ | $1$ |
| 5 | $(1939/1000,3154/1000)$ | $5/2$ |
| 6 | $(2025/1000,1308/1000)$ | $1$ |
| 7 | $(1939/1000,1489/1000)$ | $3/2$ |

With

$$
\lambda=(1,3,1,1,5/2,1,3/2)^T,
$$

exact rational arithmetic gives

$$
\lambda^TR=d^T,
\qquad \lambda^T\mathbf1=11.
$$

Therefore

$$
d\cdot a=\lambda^TRa\le11.
$$

The packet’s known uniform average of the eight actual Trump packings has orbit weights

$$
(3/4,1/8,1/4,1/8,1/8,1/8,1/8,1/8)
$$

and total mass eleven. It is feasible because it is an average of feasible packings. This proves equality of the fixed-support optimum with eleven, using the supplied exact construction as the lower-bound premise. [C1; P11.]

## Why this matters strategically

There is no need to finish an exhaustive face verifier merely to decide the unchanged exp-113 candidate, or to determine this fixed support’s optimum. The seven rows are *necessary* constraints, so a finite upper certificate is sufficient. This is not the unsound shortcut of treating a finite row set as a complete depth test for a positive candidate.

The result removes one proposed obstruction to equality density, but it is not positive evidence that a global mass-eleven density exists. Placements outside $\mathcal F$ could still give a dual value above eleven. A finite-support optimum of eleven does not establish strong duality, primal attainment, or coverage of the full pose space.

I would replace the current unchanged-candidate verification task with independent review of this compact certificate. The next substantive density question should concern *new placements* or the necessary support of an equality density, rather than further reweighting of these 60 placements.

## Verification boundary

The exploratory arrangement and LP were floating-point proposal mechanisms. The delivered proof checker uses only Python’s standard library and exact rational interval arithmetic. It proves uniqueness of the defining root on $(0.36,0.37)$ by an interval derivative cover, isolates that root further by rational bisection, reconstructs the source corner formulas, and checks all 60 placements against every test box. It verifies the rational linear combination directly and does not invoke an LP solver.

A second center/projection membership assembly reproduces the seven rows. Mutation controls reject an altered incidence, an altered multiplier, an omitted row, a box crossing a square boundary, and a box extending outside the container. Normal and optimized Python runs give identical output. These checks share the root enclosure and geometry source; they are not an independent external mathematical review. The checker deliberately does not revalidate all historical construction contacts or claim a new global packing bound. [C1.]

# New structural deduction: normal, bounded stationary stresses

## Use physical branches without support-sign partitions

The packet correctly retains abnormal Fritz–John cases in its current formulation unless a constraint qualification is proved. That qualification can be proved after a modest reformulation. [P13, “Fritz–John completeness lemma.”]

Let $q_1,\ldots,q_4$ be the four corners of $[-1/2,1/2]^2$. Square $i$ has vertices

$$
v_{ik}=c_i+R_{\theta_i}q_k.
$$

For each pair, choose an owner edge-normal axis and an order. Absorb the order into the sign of a smooth unit axis $a_{ij}(\theta)$, so that square $i$ precedes square $j$. Instead of a support-radius expression with absolute-value sign cells, impose all sixteen smooth inequalities

$$
g_{ij,k\ell}(z)=a_{ij}(\theta)\cdot(v_{j\ell}-v_{ik})\ge0,
\qquad k,\ell\in\{1,2,3,4\}.
$$

These mean exactly that the projected interval of $i$ lies before that of $j$. Retain all corner-wall containment inequalities. Work in a local *open* angle chart at the point under consideration. The union over the eight axis/order choices for each pair covers every feasible packing, including all ties. No supporting-corner or support-sign choice is needed within a selected branch.

This is a redundant smooth description, but redundancy is harmless here. The project already has a corner-projection formulation for fixed-angle LPs; the new point is to use it as the physical stationary language. [P02, “Fixed-Angle Cells”; P16, “The cell decomposition.”]

## Proposition A: every physical branch satisfies a strict feasible-direction condition

**Statement.** At any feasible point of any branch just defined, with the container side $L$ a variable and with no artificial partition inequalities added, the direction

$$
\dot L=L,\qquad \dot c_i=c_i,\qquad \dot\theta_i=0
$$

has strictly positive directional derivative on every active inequality. Consequently every local minimum of the side on that branch satisfies ordinary KKT conditions; a nonzero abnormal nonnegative Fritz–John multiplier is impossible.

**Proof.** This direction scales the centers and container, not the unit-square shapes. Set

$$
h_i=\frac{|\cos\theta_i|+|\sin\theta_i|}{2}\ge\frac12.
$$

If a left or bottom corner-wall inequality is active, its center coordinate equals $h_i$, so its derivative along the direction is $h_i$. If a right or top inequality is active, the corresponding value $L-c_{i,x}$ or $L-c_{i,y}$ equals $h_i$, with the same derivative.

For an active pair inequality, feasibility of *all* sixteen inequalities implies that the two selected corners are extreme in the separating direction. Thus

$$
a_{ij}\cdot(c_j-c_i)=r_i(a_{ij})+r_j(a_{ij})\ge1,
$$

where $r_i(a)$ is the projection radius of square $i$. Because the angles do not change, this center separation is exactly the directional derivative of the active pair row. Every active derivative is therefore strictly positive.

Inactive rows remain feasible for a sufficiently small positive displacement, since there are finitely many rows. Equivalently, the displayed direction is a strict linearized feasible direction. If an abnormal Fritz–John relation existed,

$$
\sum_j\lambda_j\nabla g_j=0,
\qquad \lambda_j\ge0,
\qquad \lambda_jg_j=0,
$$

with some $\lambda_j>0$, taking its inner product with the direction would give a strictly positive sum equal to zero. This is impossible. The objective multiplier is therefore positive and can be normalized to one. $\square$

This proof does not assume generic contacts, independent active gradients, a rigid configuration, or absence of rattlers.

## Proposition B: explicit bounds and a load-balance identity

Write the normal KKT equation as

$$
\nabla L=\sum_j\lambda_j\nabla g_j,
\qquad \lambda_j\ge0.
$$

Let $W_\ell,W_r,W_b,W_t$ be the sums of multipliers on the four types of wall rows, counting scalar corner rows as represented. The side derivative gives $W_r+W_t=1$. Taking the inner product with a simultaneous horizontal translation of all centers gives $W_\ell=W_r$; vertical translation gives $W_b=W_t$. Therefore

$$
\sum_{j\in\mathrm{walls}}\lambda_j=2.
$$

Taking the inner product with the dilation direction yields the exact identity

$$
L=\sum_{j\in\mathrm{walls}}\lambda_jh_{i(j)}
+\sum_{j\in\mathrm{pairs}}\lambda_j
\bigl(r_{i(j)}(a_j)+r_{k(j)}(a_j)\bigr).
$$

Since $h_i\ge1/2$ and every pair-radius sum is at least one,

$$
\boxed{\sum_{j\in\mathrm{pairs}}\lambda_j\le L-1,
\qquad \sum_j\lambda_j\le L+1.}
$$

For the entire target sublevel, $L+1\le U+1<4.878$. This gives compact multiplier bounds without allowing a projective objective coefficient to approach zero.

Finally, the objective gradient is in the cone generated by the active gradients in $\mathbb R^{34}$. Conic Carathéodory reduction gives a normal certificate with at most 34 positive **scalar row** multipliers. This is not a bound of 34 physical contacts and is not a rigidity theorem. All other constraints remain part of feasibility.

## What this changes, and what it does not

The most valuable change is not a claim that stationary enumeration is suddenly small. It is that the program can search a cleaner, bounded normal system rather than carrying a potentially troublesome abnormal branch created in part by its representation.

Artificial angle-bin, coordinate-order, chart-boundary, or feature-partition constraints can invalidate the strict-direction argument. They must not be silently included in the theorem above. A safe architecture derives physical KKT conditions in an open local chart first, and subsequently restricts the candidate equations to search boxes. It does not impose stationarity of a box-constrained surrogate as a substitute for stationarity of the original packing problem.

The fixed-side Trump tangent theorem is unaffected. It does not allow $\dot L=L$, so positive fixed-side stresses there are entirely consistent with Proposition A.

Rattlers and active zero-multiplier rows remain. Independent angle variables remain. Continuous stationary components remain. The $8^{55}$ raw pair-choice count remains a warning against eager enumeration. The theorem removes a genuine obstacle; it does not provide the missing global case reduction.

## A second useful reduction: choose a fixed-angle LP vertex representative

**Deduction.** If a global minimizer exists, there is a global minimizer whose centers and side form a vertex of a fixed-angle separation LP.

Choose a minimizing packing, fix its angle vector, and select one valid separating branch per pair. The resulting LP has optimum equal to the global minimum: a better LP solution would be a better packing. At the minimum side its feasible center set is a nonempty bounded polyhedron. Choose a vertex of this optimal face; it is a vertex of the full LP and is another global minimizer. In the 23 center-and-side variables it has 23 linearly independent active rows.

This is an existence statement about a representative, not a classification of every optimum. It permits a value-only program to use active bases to eliminate centers, even when a different minimizing representative has a rattler. The chosen representative remains a global minimizer and thus also satisfies the normal KKT conditions above. There is no requirement that the 23 basis rows be the same rows as the at-most-34 positive stress rows.

The first implementation test should be a complete, nontrivial restricted branch using this representation, not an all-$n=11$ stationary atlas. Measure how often basis elimination, the multiplier bounds, and exact LP conflicts reduce a real surviving case before funding a broader enumerator.

# Main proposal: an integral resource model that does not wait for near-tightness

## Change the role of the weighted measure

The existing counting proof requires each selected witness to carry at least one unit of mass. For a configuration relaxation, a measure can instead provide a *capacity constraint*. It need not cover every square by one, need not have total mass near eleven, and need not be optimal as a standalone covering measure.

This is a strengthening of the packet’s configuration-level proposals, not a claim that conflict graphs or conditional measures are new ideas. The difference is that the proposed model starts from a coarse cover of the *whole* pose space and uses arbitrary certified resource bounds. It is not blocked on finding a near-eleven covering measure or reducing the 23-million-cell census. [P06, Programs C–E; P05, “Coverage of the Earlier Reviews.”]

## Proposition C: a resource-and-conflict certificate

Fix $L$ and let $P_L$ be all contained full-size unit-square poses, with orientation modulo quarter turns. Let $B_1,\ldots,B_m$ be a finite cover of $P_L$. Overlap between cover sets is allowed; assign each actual pose to one covering set by a fixed rule.

Assume each $B_a$ can contain at most one member of any packing. Let $W(p)\subset\operatorname{int}S_p$ be a specified interior witness for each pose, using complete angle ownership and boundary conventions. For each nonnegative finite measure $\mu_j$, suppose exact numbers satisfy

$$
\mu_j(C_L)\le M_j,
\qquad
\mu_j(W(p))\ge m_{ja}\ge0
\quad\text{for every }p\in B_a.
$$

Then every eleven-square packing determines binary variables $z_a$ satisfying

$$
\sum_a z_a=11,
\qquad
\sum_a m_{ja}z_a\le M_j\quad\text{for every }j.
$$

If every pose in $B_a$ overlaps every pose in $B_b$ in their interiors, add

$$
z_a+z_b\le1.
$$

If a specified collection of cells has no jointly compatible representatives, add its corresponding no-good inequality. If several angle cells belong to one one-occupancy spatial tile, also impose a single capacity-one inequality across those angle cells.

**Proof.** Assign the eleven actual poses to their cover sets. One-occupancy gives binary selections. For each measure separately, the selected witnesses are disjoint sets, so

$$
\sum_a m_{ja}z_a
\le\sum_{i=1}^{11}\mu_j(W(p_i))
\le\mu_j(C_L)\le M_j.
$$

The conflict and no-good inequalities follow from their universal incompatibility certificates. Thus infeasibility of the finite system implies infeasibility of the original packing problem. $\square$

There is an equally clean full-size version: use $W(p)=S_p$ and require each $\mu_j$ to charge no square boundary. Absolutely continuous densities, and the curved measures introduced later, satisfy that condition.

Every measure retains its own budget. This does not repeat the invalid idea of combining independent angle-specific measures under one cheap shared budget. Likewise, the selection inequalities do not replace the individual covering rows in the T-018 theorem; they belong to a different proof object.

## A very small starting spatial cover exists

Every square center lies in

$$
[1/2,L-1/2]^2,
$$

since the projection half-width is at least $1/2$. Every unit square contains the open disk of radius $1/2$ about its center. Therefore two centers less than one unit apart necessarily give overlapping square interiors, regardless of their angles.

At $L\le U$, split this center square into a $4\times5$ rectangular grid. A tile has diameter at most

$$
\frac{U-1}{20}\sqrt{41}<1.
$$

Thus **twenty spatial tiles suffice for a rigorous capacity-one cover**. There are only $\binom{20}{11}=167{,}960$ raw eleven-tile subsets before any resource or geometric pruning. A $5\times5$ cover is a slightly larger alternative that respects the full container symmetry more naturally.

These are not 167,960 solved packing cases: every tile subset still carries continuous centers and angles. The value of the observation is representational. One can begin an integral outer model without importing hundreds of millions of atomic event cells. Refine angle or center variables only when a surviving selection demands it.

## How existing machinery enters

The scalar net already supplies a valid strict interior witness map. Use the current atom sites and weights as an initial resource, but recompute lower captured masses on the chosen cells at the *new* side. The measure need not remain a valid global unit-threshold cover. Additional measures can target different boundary corridors, spatial regions, or angular interactions, with a separate certified budget for each.

A cell lower bound must hold throughout its center and angle domain. Existing exact event sweeps, interval containment, and adaptive ownership formulas can help produce those bounds. A representative sample does not suffice. Unresolved bounds may be weakened to zero; unresolved conflicts are simply omitted. Both weaken the outer model safely.

Use a discrete solver only as a proposer unless it exports a checkable infeasibility proof. A practical proof record can be a finite branch tree with exact rational LP certificates, elementary integer cuts, and referenced geometric incompatibility certificates. Exact fixed-angle leaves can reuse the LP machinery, but its currently incomplete Farkas export is a specific missing interface worth finishing. [P02, “Fixed-Angle Cells” and “Proof Orchestration”; P13, “Leaf-closing obligations.”]

For exact fixed placements, pairwise compatibility already implies joint compatibility. Higher-order no-goods add genuinely new geometry only for cells whose pairwise feasible representatives may be inconsistent. This distinction from the packet should remain explicit in the implementation.

## The model is complete in principle at a strictly infeasible side

A useful convergence fact can be proved without any covering measure. Let $G(p,q)$ be the maximum of the eight continuous separating gaps; compatibility is $G(p,q)\ge0$. If no eleven-square packing exists at $L$, compactness gives

$$
\max_{(p_1,\ldots,p_{11})\in P_L^{11}}
\min_{i<j}G(p_i,p_j)=-\eta<0.
$$

Uniform continuity then implies that, for sufficiently fine pose cells, every eleven-cell selection contains a pair that overlaps for *all* representatives of those two cells. The robust conflict graph therefore eventually has no independent set of size eleven.

This proves that refinement is not missing a logical ingredient. It says nothing useful yet about the required mesh size or computation. Resource constraints, anchoring, and small-subsystem no-goods are intended to make that eventual finite proof achievable at a coarse scale.

## Decisive pilot and stop conditions

At one substantial target, preferably $3.84$ as an initial planning choice, build the coarse complete domain and a small collection of rigorously bounded resource measures. Compare the resource-and-conflict model with the same geometric model without resource rows. Record the number of surviving spatial/angle patterns, the worst unresolved subsystem, the number of universal incompatibility certificates, and the cost of closing complete branches.

A success is not “many cells removed.” A success is a complete exclusion at the target, or a sharply smaller and explicitly described residual family that can be handled by anchor conditioning or the normal stationary formulation. A useful negative is evidence that low-order conflicts and the selected resources leave essentially the same large residual problem after a few meaningful refinements. That outcome calls for a stronger interaction model, not automatic global grid refinement.

# Strengthen the main proposal by anchoring boundary squares

## An unconditional two-dimensional entry point

Any packing can be translated downward until some square touches the bottom wall, without losing containment. It can also be translated leftward until some square touches the left wall. These are joint translations, not independent motions of squares. The two touching squares need not be the same.

A bottom-wall anchor is described by

$$
p=(x,h(\theta),\theta),
\qquad h(\theta)=\frac{|\cos\theta|+|\sin\theta|}{2},
\qquad h(\theta)\le x\le L-h(\theta).
$$

This is a two-dimensional pose domain. It is available for *every* packing, not just stationary configurations, and does not require an unsupported claim that a minimizer touches all four walls. It is a better initial structural split than demanding a six-plus-five angle pattern before that pattern has been proved.

## Proposition D: residual-ten conditional certificates

Let $b$ be a compact set of admissible bottom-anchor poses. Define the residual pose family

$$
\mathcal R_b=
\{q\in P_L:\text{ there exists }p\in b
\text{ with }\operatorname{int}S_q\cap\operatorname{int}S_p=\varnothing\}.
$$

Suppose a nonnegative boundary-null measure $\mu_b$ satisfies

$$
\mu_b(S_q)\ge1\quad\text{for every }q\in\mathcal R_b,
\qquad \mu_b(C_L)<10.
$$

Then no eleven-square packing has an anchor in $b$.

**Proof.** The remaining ten squares of such a packing would all lie in $\mathcal R_b$. Summing their ten lower coverage bounds contradicts their disjoint-interior mass budget. The anchor itself requires no mass constraint. $\square$

Strict interior witnesses give an atomic version of the same statement. A finite cover of the entire bottom-anchor domain by boxes having these certificates proves global exclusion at $L$.

The quantifier is important: $\mathcal R_b$ is a union over possible anchors. Replacing it by compatibility with the midpoint anchor is unsound. One can use a rigorously proved *superset* of $\mathcal R_b$ safely. The packet’s common-occupied-region idea supplies one such relaxation; actual separating-axis compatibility can be stronger. [P10, “Conditional Certificates.”]

## Why this is more ambitious than another angle-class threshold

An angle composition tells the resource how many squares belong to each class, but leaves their locations unrelated. An anchor rules out an actual occupied region and constrains where ten mutually disjoint full squares can sit around it. Two anchors can define a corner corridor, a narrow passage, or an opposing-wall geometry. That is the kind of information that may force a block structure.

The residual-ten formulation also avoids spending one unit of a common covering budget on the anchor. If a broad anchor box is too weak, a fractional residual family of mass ten can demonstrate that this particular relaxation cannot close it. One can then split the anchor or fix a second square, rather than blindly refine the angle net everywhere.

At $U$, boxes containing the known Trump anchors cannot have strict residual-ten certificates, because the other ten Trump squares are an actual residual packing. This is a positive control and indicates where the method should stop excluding and begin classifying.

## From anchors to the exact endpoint

A complete branch tree can mix three kinds of leaf: a residual packing exclusion; a normal-stationary or direct geometric inequality giving $L\ge U$; or capture of the entire remaining labeled pose box inside the strict Trump radius after a justified symmetry and label map.

The first unresolved implication is **whether one or two anchor conditions reduce the residual fractional or integral problem enough at a substantial side**. The smallest decisive calculation is one whole anchor box that an unconditional resource cannot close but a conditional resource can, followed by a complete cover of a meaningful anchor interval. A successful midpoint calculation is not that result.

The first useful global target need not be $U$. A complete $3.84$ proof from these leaves would already justify a more aggressive endpoint program. Conversely, a clear failure of one-anchor residual certificates across broad boxes would indicate that pair kernels, multi-square no-goods, or three-square anchor configurations are needed.

# A high-upside alternative: two-pose semidefinite certificates

## Use the bounded placement graph, not an unreduced 34-variable SOS problem

Let vertices be all poses in $P_L$ and join two distinct vertices when the corresponding square interiors overlap. The problem is to bound the independence number of this compact packing graph. The de Laat–Vallentin hierarchy is an established framework for such infinite geometric graphs: it has duality and finite-level convergence results for compact topological packing graphs. Our pose graph has the required local overlap property. This provides a relevant theoretical framework, not a prediction that a low level will be sharp or cheap here. [W1.]

The elementary two-pose certificate below should be tested before building a general hierarchy. Its universal geometric check is over two poses—six real coordinates before exploiting structure—not over all 34 variables of an eleven-square packing.

## Proposition E: a kernel certificate

Suppose a real symmetric kernel $K$ on $P_L\times P_L$ satisfies:

$$
K-1\text{ is a positive-semidefinite kernel},
$$

$$
K(p,p)\le b\quad\text{for every }p\in P_L,
$$

and

$$
K(p,q)\le0\quad\text{for every distinct compatible pair }p,q\in P_L.
$$

The last condition includes legal touching pairs. Then every packing has at most $b$ squares.

**Proof.** For a packing $p_1,\ldots,p_N$, positive semidefiniteness applied to the all-ones vector gives

$$
N^2\le\sum_{i,j}K(p_i,p_j).
$$

Compatibility and the diagonal bound give

$$
\sum_{i,j}K(p_i,p_j)\le\sum_iK(p_i,p_i)\le Nb.
$$

Hence $N\le b$. In particular, $b<11$ excludes eleven squares. $\square$

An implementable ansatz is

$$
K(p,q)=1+\phi(p)^TQ\phi(q),\qquad Q\succeq0,
$$

where $\phi$ is a finite feature vector. Features can combine center coordinates, distances to walls, and quarter-turn-invariant angular functions such as $\cos4\theta$ and $\sin4\theta$. Symmetrize the kernel under the *joint* action $(p,q)\mapsto(gp,gq)$ of $D_4$. Do not independently fold the two poses, which would change their compatibility.

The negative pair condition can be verified on the eight closed separating-axis branches, using the smooth corner formulation and rational angle charts. A finite pose sample only proposes $Q$ and $b$; the diagonal and pair inequalities must subsequently hold over their complete continuous domains.

## The one-body method embeds into this kernel language

There is a direct mathematical bridge to what has already worked. Let $\mu$ be a nonnegative finite boundary-null measure with total mass $M$, and let

$$
m(p)=\mu(S_p)\ge1.
$$

Define

$$
K_\mu(p,q)=
\frac{M\,\mu(S_p\cap S_q)}{m(p)m(q)}.
$$

Set $f_p=\mathbf1_{S_p}/m(p)$, so $\int f_p\,d\mu=1$. Then

$$
K_\mu(p,q)-1
=M\left\langle f_p-\frac1M,
                    f_q-\frac1M\right\rangle_{L^2(\mu)},
$$

which is a Gram kernel and is positive semidefinite. Compatible squares have zero intersection mass, and

$$
K_\mu(p,p)=\frac{M}{m(p)}\le M.
$$

Thus the one-body bound is a special case of the kernel certificate at the ideal functional level. A general kernel is not required to arise from physical intersection mass; it may exploit negative correlations between compatible poses. This is a concrete reason to expect additional expressive power, though it does not prove that the extra power is sufficient for $n=11$. Nor does the embedding promise that a small polynomial feature basis reproduces every useful measure kernel exactly.

## What would establish the exact value

At $U$, a kernel with $b=11$ only proves that twelve squares do not fit. It does **not** prove that eleven require side $U$. That distinction is essential.

There are two legitimate continuations. One is a parameterized family with $b(L)<11$ for every $L<U$ in the remaining range. The other is an equality analysis at $U$: an eleven-packing must satisfy $K(p_i,p_i)=11$, $K(p_i,p_j)=0$ for $i\ne j$, and equality in the Gram bound. For the finite-feature ansatz, the latter implies

$$
Q\sum_{i=1}^{11}\phi(p_i)=0.
$$

It would suffice to prove that every compatible eleven-tuple satisfying these conditions spans a container of side $U$. Full uniqueness is stronger than necessary.

## A disciplined first experiment

Use exact Trump poses as a positive control: no sound $U$-side certificate can have $b<11$. Fit a small symmetry-adapted feature family at a chosen lower side, then add adversarially found compatible-pair violations. A rigorously certified finite-sample lower bound $b\ge11$ would reject that *feature family*, since it already fails on necessary constraints. A sample solution with $b<11$ earns continuum verification, not acceptance.

The expensive new component is the six-dimensional pair separator and its boundary treatment. Stop increasing feature degree if violation search repeatedly discovers qualitatively new troublesome regions without producing useful margin. In that case test a restricted anchor-conditioned kernel, or return the pair violations as cells and cuts to the main integral model.

Exact SDP rounding has been developed for packing problems over the rationals and quadratic extensions. That is relevant implementation guidance, not a ready-made degree-eight certificate pipeline for this project. Exact factorization/PSD checking and all geometric inequalities still need explicit proof objects. [W2.]

Motion-group methods also treat rotated congruent convex bodies, but their infinite-space density bounds must not be transferred naively. Squares tile the plane, so a translation-invariant bulk-density argument misses the finite-container obstruction. The bounded pose domain and its walls must remain in the model. [W3; the last inference is specific to this proposal.]

# Reconsider the one-body frontier without assuming it is exhausted

## Equality density has a much smaller necessary support

**Deduction.** Let $A$ be the union of the eleven exact Trump squares. If a nonnegative absolutely continuous measure $\mu$ of total mass eleven covers every unit-square pose at $U$ by at least one, then

$$
\mu(C_U\setminus\Omega)=0,
\qquad
\Omega=\bigcap_{g\in D_4}gA.
$$

**Proof.** For each $g$, the eleven members of the packing $gA$ require at least eleven units of mass and have disjoint interiors. The total available mass is exactly eleven. Hence the mass outside $gA$ is zero. There are only eight such sets, so the mass outside their intersection is zero. $\square$

The same proof applies to any finite measure charging no square boundary. This strengthens the observation that an equality density must be supported on the union of *one* Trump packing. It must lie in the region covered by *every* symmetry image.

This gives a cheaper inverse-design gate. Construct $\Omega$ from the exact polygon data and first ask whether some admissible unit square misses it up to area zero. Such a square would immediately rule out an absolutely continuous mass-eleven equality density. If no such easy obstruction appears, restrict the density basis to $\Omega$ and impose the exact Trump coverage equalities there, together with valid wall-normal conditions wherever differentiability is proved.

The seven boxes in the new support certificate already give an explicit finite-support calibration. Spread each row multiplier uniformly over its box and average the resulting measure over $D_4$. The total mass is eleven. Every support square in orbit $j$ receives

$$
\frac{1}{d_j}\sum_{r=1}^7\lambda_rR_{rj}=1.
$$

Thus an absolutely continuous measure of mass eleven covering those **sixty specified poses** exists explicitly. It is not a global covering density. Testing it against other poses is a useful way to propose new placement orbits for the full-size dual, without first building a general density optimizer.

A larger dual value on an expanded support would still need a complete almost-everywhere depth certificate. If it is eventually found at $U$, also test whether the placements have enough containment margin to persist at a smaller side. Only an actual transport proof would turn an endpoint obstruction into a barrier on an interval below $U$; continuity must not be assumed across wall contacts.

The below-$U$ primal question remains independent. Failure of equality at $U$ would not rule out useful density certificates at $3.84$, $3.85$, or other smaller sides. [P11, weak duality and equality contract; P15, H-099 through H-101.]

## Curved singular measures remove the boundary tax too

The packet contrasts atoms and straight segments, which need special boundary handling, with full-size area densities. There is an intermediate class worth testing: **measures on curved arcs that charge no line**.

**Proposition F.** Let

$$
\gamma_r(t)=p_r+v_rt+w_rt^2,
\qquad t\in I_r,
\qquad \det(v_r,w_r)\ne0,
$$

be finitely many nondegenerate quadratic arcs contained in $C_L$. Put

$$
\mu=\sum_r(\gamma_r)_\#\bigl(f_r(t)\,dt\bigr),
\qquad f_r\ge0,\quad f_r\in L^1(I_r).
$$

Then $\mu(\partial S)=0$ for every square $S$, at every location and orientation. Consequently $\mu(C_L)<11$ and $\mu(S)\ge1$ for every contained full-size unit square imply no eleven-square packing.

**Proof.** The preimage of any line under $\gamma_r$ is the zero set of a nonzero polynomial of degree at most two. It is nonzero because a nonzero line normal cannot annihilate both linearly independent vectors $v_r,w_r$. Thus the preimage is finite and has zero $f_r(t)\,dt$ mass. A square boundary is contained in four lines. Summing the eleven full-square masses is therefore legitimate despite legal boundary touching. $\square$

This is not an extension of the area-density contract by assertion; it supplies the missing boundary-null theorem. It requires neither a shrunken core nor a two-dimensional density mesh.

For rational arcs and polynomial parameter densities, intersection with a square is decided by four quadratic inequalities in $t$. The captured mass is an integral over a finite union of parameter intervals. Its endpoints are algebraic roots. This suggests a one-dimensional algebraic integration primitive coupled to a three-dimensional pose verifier.

The difficult part remains continuum coverage. Tangencies create root collisions and can spoil naive derivative or Lipschitz bounds. Use complete event treatment or conservative interval integration; do not assume smooth dependence of captured mass. The measure is singular, but captured mass is continuous in pose because each limiting square boundary has measure zero and dominated convergence applies.

A useful calibration comes directly from T-018. Its strict containment inequality gives a uniform positive distance between the selected cores and the boundaries of their unit squares. Replacing each atom by a sufficiently small curved arc of the same mass preserves full-unit coverage at the old side. This transfers the successful resource into the new language without claiming a new bound. The substantive experiment is then whether varying arc extent, shape, and weights improves coverage at a larger side.

This route remains one-body. In particular, a finite full-size dual whose depth is bounded off its finite collection of edge lines also bounds such curved measures: the exceptional lines have zero curve mass. Curved support does not evade a genuine finite one-body obstruction. It only removes the avoidable shrink/boundary loss with a different representation.

## What not to rebuild first

Do not require completion of adaptive square cores before trying a few exact curved or polygonal witnesses at the actual limiting poses. Conversely, do not fund a general curve-integral verifier merely because the boundary lemma is attractive. Require a proposed measure, a measurable gain on difficult pose families, and an explicit route to the missing universal check.

The same principle applies to polygonal kernels and existential witness menus already in H-096 and H-097. A larger shape is useful only if it captures additional positive mass where the current witness fails. A shifted witness is useful only through mass placement, not because translation increases its largest possible inscribed size. [P06; P15.]

# Structural theorems worth more than another tiny bound increment

## Solve a natural restricted optimization problem containing Trump

The packet already proposes six-plus-five and two-orientation searches. I would promote one of these from a search suggestion to a principal restricted theorem target. [P06, final search proposals.]

A particularly clean statement is:

> Every packing of six axis-aligned unit squares and five unit squares sharing one arbitrary orientation, with otherwise arbitrary positions and contacts, requires side at least $U$.

Together with the known construction, this would determine that entire restricted optimum exactly. It is much stronger than minimizing the already selected Trump contact cell, and more directly relevant to the conjectured mechanism than extending a tiny neighborhood of the 0°/45° family.

The complete domain has one shared nonlinear angle, all possible center arrangements, all wall contacts, and all separating branches. The fixed-angle center problem remains disjunctive, but conditional certificates, a spatial integer model, and exact LP branch bounds can be used while subdividing a single angle parameter. The exact-value theorem must account for every contact pattern, not merely reproduce the retained cell’s kink.

A broader successor allows arbitrary counts in two orientation classes. It generally has **two** angle parameters: rotating the entire packing by an arbitrary angle does not preserve an axis-aligned square container, so one cannot set the first class to zero without a theorem. A theorem for this full two-class family would determine whether any better packing must use at least three orientations. That would materially redirect both proof and search.

## Extract a geometric inequality from the successful branch

The known kink suggests looking for two competing support constraints whose lower bounds cross at the exact Trump angle. The desirable result has a form such as

$$
L\ge\max\{F(\alpha),G(\alpha)\},
\qquad
\min_\alpha\max\{F(\alpha),G(\alpha)\}=U,
$$

but only after a proved structural reduction supplies its hypotheses. A dual LP certificate can reveal wall-to-wall chains or weighted projections that suggest $F$ and $G$. The hard step is showing that every packing in the declared family contains a relevant chain, or falls into an explicitly excluded alternative.

This should be treated as mathematical discovery, not just output formatting. Minimize the support of an exact dual explanation, identify its geometric inequalities, then test that explanation on neighboring contact patterns. A compact inequality valid across many branches may have more value than thousands of separate leaf certificates.

The new normal stress identities offer a guide: every positively loaded component balances its horizontal and vertical wall loads. A component with positive pair stress cannot be completely unsupported by walls; dilating that component alone would contradict its positive pair contribution. With noncontact pairs assigned a strictly separating branch, positive pair rows correspond to actual contacts. These facts suggest enumerating wall-spanning loaded structures rather than arbitrary contact graphs. They do not prove that the entire packing has one connected backbone or that every wall has positive load.

## Use other-$n$ results only through explicit geometric reductions

The project’s $n=12$ bound and solved smaller cases are valuable controls and can become pruning lemmas. They do not automatically improve $s(11)$. A smaller-$n$ bound applies only when a subset of squares is proved to lie in the required container. An $n=12$ obstruction applies only after an explicit augmentation lemma shows that the hypothesized eleven-packing could be extended within a forbidden twelve-square side. [P01, “What the Larger Project Has Established.”]

Useful new intermediate results could therefore be restricted residual packing numbers in a corner corridor, an L-shaped complement of one anchor, or the complement of two anchored squares. These are not distractions from $n=11$: they are the subproblem the proposed conditional proof actually needs. A complete ten-square residual theorem in one such family may eliminate a large collection of eleven-square branches at once.

# Search should test the reductions, not merely repeat the same proposer

The existing search evidence is more diagnostic of the tested algorithms than of the true landscape. The supplied quench and annealer have difficulty reaching the known oblique configuration, and related oblique controls are also problematic. It would be risky to treat failure of those engines as strong evidence for a proposed global structural theorem. [P02, “Proposal, Refinement, and Construction Certification”; P14.]

The useful search targets are the negations of the intended reductions: a packing below $U$ with three or more distinct angle classes; a six-plus-five packing with a different wall-support pattern; or a low-side configuration in an anchor cell the current certificate cannot exclude. Search and proof then produce information about the same cases.

Use continuation from inflated containers and coordinated contact-release moves as candidate mechanisms. In particular, permit the five tilted squares to split their shared angle, and release several contacts together rather than only varying one angle at a time. These are proposals, not claims that a particular annealing schedule will work. Maintain several structural families instead of retaining only the lowest side returned by one refinement rule.

Calibration should include recovery of Trump from a declared distribution of perturbed or inflated starts, not only convergence on $n=5$ and $n=10$. Failure to rediscover the known oblique witness is evidence that a negative search on an unfamiliar oblique branch has little exclusion value. Numerical endpoints remain proposals until exact or interval construction verification succeeds.

A smaller verified packing would invalidate the present optimality conjecture and be a major advance, but would not by itself determine the new optimum. The global proof machinery should therefore be parameterized by the current verified upper witness rather than hard-coded around Trump’s contact pattern.

# Recommended research sequence and decision criteria

## First: integrate the two deductions that already have concrete content

Independently review the seven-row support certificate and replace the unresolved $[11,56/5]$ fixed-support interval with its exact value eleven once that review is accepted. Do not rewrite exp-113’s finite-row result or exp-115’s pair result; append the stronger determination with its new evidence. The full-face verifier may still be useful for future supports, but the unchanged candidate no longer justifies it.

Review Proposition A and the multiplier identities as a replacement physical stationarity contract. The critical checks are that all corner projection rows are retained, the side is free, angle charts are locally open, and no artificial partition row is smuggled into the constraint qualification. Then make a small complete control implementation before attempting a nontrivial restricted branch.

These are relatively compact mathematical deliverables. Their acceptance is more valuable than another broad strategy document because they change what subsequent solvers are required to represent.

Keep the acceptance boundary strict, but allow exploratory discovery to be aggressive. The new support certificate was found with an untrusted floating-point arrangement and then reduced to a tiny exact check. That is a useful pattern: search for a counterexample or a short necessary-row certificate before building two complete general-purpose verifiers. Preserve historical experimental contracts, but do not turn the implementation sequence of one experiment into a mathematical dependency of every new direction.

## Next: compare two concrete global-reduction pilots

Run the coarse resource/anchor approach at one substantial side and the six-plus-five restricted-family approach as complementary pilots. The first tests whether a modest amount of position-dependent compatibility can beat the one-body plateau. The second tests whether the entire candidate mechanism can be proved optimal without assuming its contact graph.

Neither needs a global stationary atlas. Both can reuse exact one-square geometry, the fixed-angle LP, and the existing interval routines. Both should export complete branch exclusions and unresolved regions in the same form so that useful cases can be transferred between them.

The comparison should use **closed mathematical cases and strength of the resulting reduction**, not percentage of raw cells removed. A branch count is meaningful only together with its continuous domains and its closure certificates.

## Keep one high-upside interaction pilot and one selective resource pilot

Test the two-pose kernel with a small explicit feature family and an adversarial compatible-pair separator. In parallel, choose *one* of equality-support geometry, an expanded full-size dual support, or curved measures based on an actual candidate. Do not open all of them as large infrastructure projects.

The scalar $61/16$ probe remains reasonable because its instrument exists. A result should be certified and retained. It should not automatically outrank a promising substantial exclusion or force the whole program into an incremental ladder. The packet’s adaptive implementation can remain available without being a mandatory scientific dependency of unrelated methods.

## Success and stop conditions

| Direction | Continue when | Change course when |
|---|---|---|
| Coarse resource model | Exact resource rows and low-order incompatibilities close whole cases or sharply restrict anchor/angle patterns | Repeated meaningful refinement leaves essentially the same large family, or resource bounds remain nearly all zero |
| Anchor conditioning | A complete anchor interval closes, or the residual problem drops to a few verifiable configurations | Broad and refined anchors retain a certified residual fractional capacity of ten with no useful geometric reduction |
| Normal stationary formulation | Complete restricted branches close with bounded stress and active-basis elimination | Symbolic support enumeration grows before actual branch exclusions are obtained |
| Two-pose kernel | A fixed feature family produces a candidate with margin that survives increasingly adversarial pair separation | Exact finite necessary constraints already rule out $b<11$ for that family, or separation complexity overwhelms the gain |
| Curves or density | A specified resource gains coverage on the limiting poses and has a viable full-domain certificate | Improvements occur only on samples, or tangency/boundary verification costs dominate without additional mass margin |
| Six-plus-five theorem | All contact cases over nontrivial angle intervals are excluded or reduced to a small algebraic family | The argument relies on retaining the original contact graph or silently synchronizing independent variables outside the declared family |

These are research decisions, not mathematical refutations of every member of a method class. A failed feature basis is not a failed kernel theorem. A failed anchor relaxation is not a packing counterexample. A failed sufficient Bernstein certificate is not a negative geometric inequality.

## The eventual global theorem

A realistic exact-value theorem could read:

> Every side-minimizing eleven-square packing with $L_*\le L\le U$ has a representative in a finite, explicitly covered collection of physical branches. Each branch is either impossible, has a certified lower bound $L\ge U$, or lies wholly inside a verified local neighborhood where the same bound holds.

Compactness supplies a minimizing representative if a better packing exists. The branch cover supplies global completeness. The branch certificates supply exclusion or a sharp lower bound. The known construction supplies the matching upper bound.

Nothing in this statement requires proving that all near-tight one-square poses resemble Trump, that every minimizer is generic, or that every feasible configuration belongs to a discovered numerical basin. Those are unnecessary burdens. The central challenge is to find a coarse reduction whose surviving branches are few enough—and geometrically organized enough—to close.

# Bottom line

The most valuable next move is not simply to make the weighted sets more elaborate. It is to let those weighted sets participate in an integral proof, where their mass bounds are combined with actual geometric compatibility and boundary conditioning.

The review supplies one exact research outcome—the fixed Trump-orbit full-size dual optimum is eleven—and a structural simplification that removes abnormal stationary branches in a revised physical formulation. Neither settles $s(11)$, but both remove avoidable work from the present agenda.

My strongest recommendation is to develop the resource-and-anchor proof architecture, using normal bounded stresses and active-basis elimination for difficult residual branches, while testing a genuinely richer two-pose kernel in parallel. The natural restricted six-plus-five optimum is an especially useful intermediate theorem. Curved boundary-null measures and the common-support region $\Omega$ are selective one-body opportunities, not reasons to postpone interaction-based work.

The remaining gap is large enough that success will likely require a new geometric reduction or a stronger relaxation, but the existing machinery is well suited to discovering and certifying either. The appropriate ambition is a proof that closes complete families of competitors—not merely a succession of smaller decimal increments.

# Appendix A: certificate files and reproduction

The accompanying certificate directory contains:

- `check_support_ceiling.py`: standalone exact rational-interval checker for the seven necessary rows and the depth-$7/5$ counterexample.
- `test_support_ceiling.py`: known-answer, second-assembly, and mutation checks.
- `support_exact_result.json` and `support_tests.json`: the outputs obtained during this review.
- `README.md`: the mathematical scope and execution instructions.

Run with Python 3.10 or later:

```sh
python check_support_ceiling.py
python test_support_ceiling.py
python -O check_support_ceiling.py
```

The checker’s root polynomial is

$$
5u^8-10u^7-2u^6+14u^5+12u^4-6u^3+2u^2+2u-1.
$$

The root is the one in $(36/100,37/100)$ and the side is

$$
U=\frac{6u+4}{1+2u-u^2}.
$$

The source corner formulas are transcribed from P09. Orbit order comes from P11. The proof of the upper bound needs only those exact polygons, the positive-area row boxes, and the rational multiplier combination. Equality of the optimum with eleven additionally uses the packet’s independently established feasibility of the original Trump packing.

The delivered checker does not depend on `sqpack`, SciPy, Shapely, an LP solver, or an external number-field library. Its interval operations use `fractions.Fraction`. A failed sign enclosure produces refusal, not an inferred sign. The exploratory floating-point producer is not part of the proof boundary and is not needed to reproduce the certificate.

# Appendix B: packet coverage and references

References P00–P18 identify the uploaded files by their filename prefixes. They refer to the frozen packet, not a later state of the online repository. The complete selected mathematical text was reviewed; the long T-018 JSON was parsed in full rather than reproduced as prose.

| Ref. | Supplied file | Principal use in this report |
|---|---|---|
| P00 | 00 — READ ME FIRST | Target, requested ambition, reading and evidence boundaries |
| P01 | 01 — research progress | Current bracket, scoped outcomes, latest interpretation |
| P02 | 02 — tooling and machinery | Reusable exact geometry, LP, sweep, interval, and proof interfaces |
| P03 | 03 — agenda 024 | Complete current allocation and its historical amendments |
| P04 | 04 — child agendas | Adaptive, density, and stationary commitments and controls |
| P05 | 05 — current assessment and review | Existing prioritization, corrections, and implementation gates |
| P06 | 06 — alternative strategies | Prior conditional, integral, kernel, and geometric proposals |
| P07 | 07 — standalone 381 proof | Full counting theorem, verifier mechanism, and 1,121-atom data |
| P08 | 08 — dilation limit | Exact lower endpoint and strict-family/weak-limit distinction |
| P09 | 09 — trump construction and local proof | Exact construction formulas and local endpoint |
| P10 | 10 — fractional barriers and negatives | Scoped barriers, tightness, and conditional certificate lemmas |
| P11 | 11 — density contract candidate and results | Weak duality, exact support, exp-113/115, and new certificate input |
| P12 | 12 — restricted orientations | Exact-angle clauses and continuous-angle obligations |
| P13 | 13 — typed global structure | Existing FJ language and completeness/degeneracy obligations |
| P14 | 14 — search and near tight evidence | Search calibration, near-tight census, and failed seed comparison |
| P15 | 15 — registered mathematical questions | H-036 and H-093–105 quantifiers and acceptance scopes |
| P16 | 16 — mathematical background and literature | Geometry, source lemmas, literature qualifications |
| P17 | 17 — source catalogue | Source-selection provenance and omitted material |
| P18 | 18 — trump packing | Visual inspection of the supplied exact construction |

Historical scheduling instructions in these sources were treated as source material, not as instructions to execute repository work. The incomplete H-092 transport was not promoted to independently inspected evidence. The generic-radius contact bound noted in P16 was not applied to equal unit squares. The finite-net caveat in P10 was preserved.

**C1. Review computation.** `check_support_ceiling.py`, `test_support_ceiling.py`, `support_exact_result.json`, and `support_tests.json`, distributed with this report. These contain the new fixed-support certificate and its stated assurance boundary.

## External primary sources

**W1.** David de Laat and Frank Vallentin, *A semidefinite programming hierarchy for packing problems in discrete geometry*. arXiv:1311.3789v3. Theorems 1.1 and 1.2 concern duality and convergence for compact topological packing graphs; Section 5 discusses two- and three-point bounds. [Primary text](https://arxiv.org/html/1311.3789v3).

**W2.** Maria Dostert, David de Laat, and Philippe Moustrou, *Exact semidefinite programming bounds for packing problems*. Author-posted paper, 2020. The stated arithmetic scope is rational or quadratic-extension rounding; no ready-made degree-eight implementation is inferred here. [Primary repository entry](https://optimization-online.org/2020/01/7553/).

**W3.** Fernando Mário de Oliveira Filho and Frank Vallentin, *Computing upper bounds for the packing density of congruent copies of a convex body*. arXiv:1308.4893v3; DOI 10.1007/978-3-662-57413-3_7. Relevant as a rotated-body kernel/SOS framework, not a finite-container theorem for this problem. [Primary record](https://arxiv.org/abs/1308.4893).

External sources were consulted to identify relevant proof frameworks. This was not an exhaustive priority audit or a fresh validation of the public lower-bound record. The new propositions in the body are supported by their displayed proofs, and the new support determination by C1.
