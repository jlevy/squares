---
title: "Beyond 3.81: A Research Strategy for Eleven Squares"
subtitle: "Technical review, new structural deductions, and an exact fixed-support certificate"
author: "Research review prepared with ChatGPT"
date: "Based on the research snapshot of 6 September 2026"
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
