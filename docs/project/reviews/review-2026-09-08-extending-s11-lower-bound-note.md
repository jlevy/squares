# Contributed Research Note: Extending the Lower Bound for Eleven Squares

**Contributed research note from an external agent session, received by the owner on
2026-09-08.** It was written against repository snapshot `7ef80525`, before PRs 116, 121
and 127 landed, and is checked in here verbatim as a record so that its proposals can be
cited and dispositioned. It adjudicates nothing and changes no bound.
The integration decisions belong to the exploration the coordinator is writing, X-023 at
`packing/campaign/explorations/X-023-...`, not to this record.

**Editorial terminology note, September 10, 2026.** The contributed body below is
preserved verbatim. Its phrase “weak lower bound” is historical terminology for the
ordinary proved inequality `s(11) >= C`, where `C` is the displayed T-022 value.
Excluding every side below `C` proves that inequality by order completeness. The proof
does not assert the separate stronger inequality `s(11) > C`; “weak” does not mark a
different theorem or a lower level of proof assurance. Later T-026 proves
`s(11) >= 955000*sqrt(518400042893309449)/179696714646249 = 3.826447410572939744...`
(V4/C5). See the [current evidence account](../research/research-2026-09-09-n11-evidence-and-inference.md).

## Assessment

The best immediate route is to distinguish unfinished optimization from a genuine limitation of the weighted-point method, then remove two avoidable geometric relaxations: centers that are admissible for a small core but not for its parent unit square, and the requirement that every inner witness itself be a square. For a substantially larger improvement, the strongest direction is a hybrid proof that combines the weighted measure with compatibility between placements, conditional certificates, and exact geometric exclusion.

The public proof establishes nonexistence at side 3.81. The repository additionally records the weak lower bound

$$
s(11)\ge \frac{38100\sqrt{8100042893309449}}{899996306539}
 =3.810025723614703\ldots,
$$

obtained by sharpening containment and uniformly dilating the retained certificate. The recorded upper construction is at

$$
U=3.877083590022814177\ldots.
$$

The containment refinement is already done; it should not be proposed again as a new route to 3.817. It gains about 0.0000257, not 0.007. [1, 2]

No independently checkable external proof of $s(11)>3.817$ was located in the public sources searched through September 8, 2026. This is a retrieval limitation, not evidence that no such argument exists. A specific reference to 3.817 does occur in the repository's own Agenda 025, where it is explicitly an interpolation between two restricted covering calculations, not a theorem. The relevant external weighted-certificate posts by Burns and Massaccesi concern seventeen squares. [3, 12, 13]

This note uses repository snapshot `7ef80525b35a8e77e00b460a7e08f1489134d0cc` for its source inventory. It does not independently replay the entire 1,121-atom certificate, complete the retained LP runs, or produce a new numerical lower-bound certificate. The parent-domain reduction, rational-octagon containment lemma, and frozen-measure stability calculation below are explicit mathematical proposals with proofs; their numerical benefit for the packing problem remains to be measured. The accompanying Python program checks their stated rational constants and sufficient inequalities, not global packing infeasibility.

## 1. What the current certificate retains and loses

The certificate places a nonnegative atomic measure $\mu$ in the container. Its total mass is

$$
M=\frac{434547}{40000}=10.863675.
$$

There are 181 rational net directions and a common square-core side

$$
B=\frac{9977}{10000}=0.9977.
$$

Every allowed core placement at every net direction has measure at least

$$
m=\frac{4001}{4000}=1.00025.
$$

An arbitrary unit square contains an appropriate net-direction core strictly in its interior. Consequently, eleven nonoverlapping unit squares would contain eleven disjoint cores, requiring mass at least $11m>M$. Nonnegativity and strict interior containment are essential: they justify both enlarging witnesses and avoiding double counting along touching boundaries. [1, 4]

The scale-invariant certificate quantity is $M/m$, not raw mass alone. Here it equals

$$
\frac{434547}{40010}=10.860959760059986\ldots.
$$

For a fixed measure, the minimum covered mass can fall as far as, but not down to,

$$
M/11=\frac{434547}{440000}=0.987606818181818\ldots
$$

before the same counting argument ceases to be strict. The threshold 1 is only a normalization.

There are three distinct sources of weakness. A chosen finite set of atom sites may be inadequate. Replacing a unit square by a smaller witness and allowing that witness too many positions may weaken the geometric model. Finally, even the best possible one-body covering measure may fail because its fractional dual admits collections that are not genuine nonoverlapping packings. A failed run is not enough to identify which of these limitations is active.

Formally, let $\tau$ be the least total measure covering every admissible core by mass at least one. A dual feasible object is a weighted family of core placements whose weighted depth is at most one at every point. Any such family of total weight $V$ establishes $V\le\tau$. To prove a barrier to this particular certificate language, one needs $V\ge11$ with globally verified depth, not merely a solver objective of eleven on a finite collection of test sites. [5, 6]

## 2. The immediate scalar bottleneck is unresolved

The most informative retained experiment is not the initial 3.82 plateau but exp-116 at

$$
L=61/16=3.8125.
$$

The September 7 follow-up records 24,653 sites in 3,180 symmetry orbits and 11,885 placement rows. Every one of nineteen row solves stopped at a two-round limit. The terminal numerical LP objective was approximately 10.71756236. The best independently checked fractional packing family had weight

$$
\frac{20843712108}{2067791663}=10.0801799721735\ldots
$$

at depth one. Neither quantity decides whether a covering certificate below eleven exists. [7]

The extraction mechanism matters. The cutting loop retained only the 96 heaviest positive dual rows, before expanding their symmetry images. At the terminal iteration, the extracted family's mass was approximately 9.90249944, about 0.81506 below the numerical LP objective. Finding no overloaded arrangement vertex in that truncated family does not establish that the full dual is feasible everywhere. It also does not mean the primal covering constraints have all been satisfied. The loop could stop adding sites while the row solve remained unconverged. [7]

The next experiment should therefore hold the final sites fixed and complete the placement constraints. Preserve every added row, the full primal and dual vectors, the stopping reason, and the independently recomputed coverage minima. A rational measure of mass below eleven, accepted by the existing exact coverage checkers, is success. A rational dual of mass at least eleven that satisfies the finite-site constraints rejects those sites only. A globally depth-feasible dual of mass at least eleven is the substantially stronger result that rules out this unrestricted core-covering formulation at that side.

This experiment is already identified in BC-252. The recommendation is to execute that narrower scientific discriminator, not to rename it as a new idea or repeat the same two-round run with a larger time allowance. If row completion rejects the sites, use the full dual to identify missing support. A support cap may still be necessary, but its discarded weight and the effect on valid bounds should be explicit.

For improving the dual lower bound, reoptimizing weights on a retained placement family under exact arrangement-depth constraints can be more useful than uniformly scaling every weight by its maximum overload. Uniform scaling pays for the worst local conflict everywhere. Local weight reoptimization can remove weight selectively from the conflicting placements. This is an optimization proposal, not a guarantee that the dual will reach eleven.

The 3.82 records likewise do not prove a barrier. One recorded row-converged restricted cover has objective approximately 11.05561694, while an exact depth-feasible packing family gives approximately 9.90790559. The interval still straddles eleven widely. Interpolating the 3.81 certificate mass and the 3.82 restricted objective crosses eleven near 3.8171024, but the site sets differ and neither endpoint identifies the unrestricted optimal covering function. That calculation is a target-selection heuristic only. [3, 5]

## 3. Extract the remaining stability of the existing measure

There is a potentially inexpensive experiment that does not require a new LP or a new witness shape: determine the first bad event cell reached as the container expands around the existing, fixed centered atom configuration.

Move the original coordinate origin to the container center. Keep the atom positions relative to that center, their weights, $B$, and the direction net fixed. When the side increases from $L_0$ to $L$, this amounts in the original positive-coordinate convention to translating every atom by $((L-L_0)/2,(L-L_0)/2)$, not dilating the atom configuration. The measure remains symmetric about the new container center, and all atoms remain inside the larger container.

At a net direction $k$, let $r_k$ denote the horizontal and vertical half-extent of the core. For the square core in the first-quadrant chart,

$$
r_k=\frac B2(\cos\theta_k+\sin\theta_k).
$$

An admissible center satisfies

$$
\|c\|_\infty\le L/2-r_k.
$$

Within an open event cell, the covered mass is constant. Call a cell bad when that mass is at most $M/11$. The infimum side at which such a cell can become reachable is

$$
L_{k,C}=2\left(r_k+\inf_{c\in C}\|c\|_\infty\right).
$$

The infimum can be calculated on the closure of the cell. Net directions, transformed event boundaries, and the small linear program defining the infinity-norm distance are rational. A finite implementation can restrict attention to the complete event arrangement inside a prespecified larger target container; cells outside that target cannot enter before it.

For every side strictly below the first bad-cell entry, every reachable cell has coverage greater than $M/11$. There are only finitely many coverage values, so their minimum has a positive gap above that threshold. Rescaling the weights by the reciprocal of this exact minimum restores the standard normalization and yields total mass below eleven. Boundary strata require care, but with nonnegative atoms a closed witness can only gain atoms at an event boundary. An endpoint claim should be made only after directly checking it; otherwise retain a strict family and its weak limit.

This is different from T-022. Uniform dilation scales the cores and is limited by strict containment. Here the core size remains unchanged and the question is when an uncovered region becomes reachable in a larger container. The test may return only a tiny improvement. Its value is that it measures the actual geometric margin remaining in the frozen certificate rather than guessing from its mass surplus. A direct exact sweep at rational candidate sides is a simpler initial implementation than a full symbolic first-entry calculation.

## 4. Use parent-feasible center domains

The current `sweep.centre_domain()` uses the set of centers where the smaller square core fits in the container. This is a safe relaxation, but it includes centers where a unit square that would select that core could not fit. The explicit code computes its boundary from `square_side * (cosine + sine) / 2`. [8]

Assign a net direction $\theta_k$ an angle cell $I_k=[\alpha_k,\beta_k]$ contained in the reflected chart $[0,\pi/4]$. For a parent unit square at angle $\theta$, define

$$
h(\theta)=\frac{\cos\theta+\sin\theta}{2}.
$$

Its center belongs to

$$
C_\theta(L)=[h(\theta),L-h(\theta)]^2.
$$

Since $h$ is increasing on that chart, the union of all possible parent-center domains is

$$
\bigcup_{\theta\in I_k}C_\theta(L)
=[h(\alpha_k),L-h(\alpha_k)]^2.
$$

It is sufficient to check the direction-$k$ witness only on this union, provided that witness is strictly inside every parent orientation assigned to the cell. Every actual parent center remains included. It would be unsound to use the intersection of the domains, or the domain at the largest angle: either would omit legitimate parents.

If $h(\alpha_k)$ is irrational, use a certified rational lower bound for the inset. That enlarges the tested domain rather than making it too small. Intersect this outward-safe domain with the original core-fit domain, which is also necessary. A cell that crosses a chart seam should first be split, and the direction assignments, endpoint coverage, and reflected images should be explicit.

The axis case illustrates the lost geometry. A unit-square center must be at least $1/2$ from every wall. The old axis-aligned core is allowed within $B/2=0.49885$, adding strips of width

$$
(1-B)/2=0.00115.
$$

Those strips are small, but a covering LP can be governed by a few difficult wall placements. Removing them may matter disproportionately to their area; whether it does is measurable.

The clean experiment changes only the center domains, keeping sites, weights during initial diagnostics, direction assignments, and core size fixed. Record which low-coverage or dual-supported placements disappear, and then compare fully separated covering solves on identical sites. This separates genuine geometric strengthening from effects of a changed search budget. It can be tested with the current common $B$, before per-cell core sizes are available.

## 5. A rational octagon that strictly dominates the square core

The repository already contemplates angle-adaptive square cores and richer common inner kernels. The adaptive containment theorem is recorded as completed, while its full verifier acceptance was still in progress in the reviewed agenda. A generic kernel implementation is not necessary to obtain the first concrete enlargement. [3]

### Containment lemma

Let the old centered square core have side $B$. Suppose it is strictly inside every parent unit-square orientation in its assigned angle cell. Choose a rational $a$ such that

$$
B/2<a<\min(B,1/2).
$$

Define

$$
K_{B,a}=\operatorname{conv}\left(
\{(\pm B/2,\pm B/2)\}
\cup\{(a,0),(-a,0),(0,a),(0,-a)\}\right),
$$

with independent signs for the four diagonal vertices. This is a convex rational octagon containing the old square core strictly.

The four diagonal vertices are the old core's corners, so they are strictly inside every allowed parent. Each of the four new axial vertices has Euclidean norm $a<1/2$. The open disk of radius $1/2$ is inside every centered unit square, regardless of orientation. Thus all eight vertices are strictly inside every allowed parent; their convex hull is too.

This proves containment for a continuum of parent orientations. It does not sample angles. Rotating the octagon to a rational net direction preserves rational coordinates. The original strict condition

$$
B(1+D)<1
$$

is already sufficient for its diagonal vertices, while $a<1/2$ handles the new ones. In particular, setting $a=1/2$ would lose the needed strictness at an aligned parent and must be refused.

### Area and interpretation

The octagon consists of the old square and four exterior triangles, so

$$
\operatorname{area}(K_{B,a})
=B^2+4\left(\frac12 B(a-B/2)\right)=2aB.
$$

For the published $B=0.9977$, take $a=499999/1000000$. Then

$$
\operatorname{area}(K_{B,a})=0.9976980046,
\qquad B^2=0.99540529.
$$

It recovers about 49.90% of the area lost by the square core. This is an area comparison, not a prediction of a 49.90% improvement in certificate mass or side bound.

The stronger statement for the covering problem is pointwise: at the same center and direction,

$$
\mu(c+R_{\theta_k}K_{B,a})
\ge\mu(c+R_{\theta_k}[-B/2,B/2]^2)
$$

for every nonnegative measure. On the same parent-feasible center domains, the new covering problem cannot be harder than the old square-core problem. Actual improvement depends on where the extra triangles capture weighted atoms. An enlarged kernel should not automatically be allowed every center where it fits: that would reintroduce the parent-domain relaxation.

For fixed orientation, an atom is covered precisely when the center lies in a rational translate of the reflected octagon. These polygon boundaries form a finite line arrangement. Coverage remains constant on its open two-dimensional cells, and nonnegative weights make boundary coverage no smaller than an adjacent cell's coverage. The rectangular prefix-sum implementation does not transfer unchanged, but exact polygon arrangements or a certified interval classifier give plausible verification routes.

A low-cost precursor is to evaluate the octagon on the retained limiting poses, then solve a finite-row LP with the same sites. This is a screen, not a certificate: favorable sampled results must be followed by a complete coverage oracle. An exact negative on the finite-row problem can reject that fixed site set even before every placement is generated; a positive cannot establish global coverage.

One should not replace the common kernel by the intersection of only the endpoint-rotated unit squares without proof. Intermediate orientations can impose additional restrictions. The octagon avoids that issue because each vertex has an independent containment argument valid throughout the cell.

## 6. Use compatibility to force extra mass consumption

A one-body certificate can stop at eleven even though eleven geometric squares cannot fit. Improving atom density cannot fix an actual fractional integrality gap. The relevant next condition is not simply that each square consumes one unit of mass, but that eleven mutually compatible squares must collectively consume more than the available mass.

The repository's X-014 already states the key slack lemma. If a measure covers every eligible core by at least one and has total mass

$$
M=11+\varepsilon,
$$

then any hypothetical eleven-square packing, with selected cores $P_i$, satisfies

$$
\sum_{i=1}^{11}(\mu(P_i)-1)\le\varepsilon,
\qquad
\mu\left(C\setminus\bigcup_iP_i\right)\le\varepsilon.
$$

In particular, no selected core can cost more than $1+\varepsilon$, and no more than $\lfloor\varepsilon/\delta\rfloor$ selected cores can each cost at least $1+\delta$. Every atom whose individual weight exceeds $\varepsilon$ must be covered by a selected core. These are consequences of the same mass accounting, not independent assumptions. [6]

The useful task is to show that individually inexpensive placements cannot be selected together eleven times. Build a complete cover of relevant pose space by cells, with certified coverage-cost bounds. Connect two cells only if every pair of unit-square poses from them overlaps in its interiors. Cells must also have a certified occupancy cap; making them sufficiently small to admit at most one packed square is one possible construction. A packing then induces an independent set of eleven occupied cells satisfying the mass budget.

Pairwise conflicts support edge inequalities. Pairwise-incompatible triples or larger cliques support stronger clique inequalities even when the corresponding squares have no common intersection point. Odd-cycle inequalities can also reject fractional combinations left by edge constraints: a five-cycle permits at most two actual occupied cells, while its edge-only LP admits total weight 2.5. These are elementary finite-graph controls. Detecting them on sampled dual placements is useful for discovery, but a global packing proof needs their validity lifted to complete pose cells and a complete treatment of all remaining poses.

This route has a principled higher-order extension. De Laat and Vallentin model geometric packing, including rotations of convex bodies, through topological packing graphs and a convergent semidefinite hierarchy. Bekker and Oliveira Filho prove convergence of the related k-point bound. These theorems justify adding multi-placement information; they do not establish that a low hierarchy level is computationally manageable or sufficient for eleven squares. Start with exact local clique, cycle, and small-subset capacity cuts, and move to a semidefinite model only after a measured instance demonstrates a gap that those cuts do not close. [14, 15]

The reviewed two-threshold angle-class experiment is not a counterargument to this direction. Its target was above the exact capacity ceiling of the chosen shrunken 0°/45° class, approximately 3.876681. More weights could not make that particular control succeed. That rejects a specific class/core construction; it does not reject all angle conditioning, conditional certificates, or pairwise compatibility. [9]

## 7. Branch-specific certificates and coupled geometry

Conditioning on an anchor square is a natural way to turn the compatibility information into a finite proof. An atom heavier than the available slack provides an anchor when one exists: some selected core must contain it. Otherwise, derive a finite alternative, such as at least one square belonging to a specified collection of regions or orientation classes. Partition the anchor's possible poses into closed, completely covering boxes.

Within each box, the remaining ten squares have a smaller admissible domain. A branch-specific measure of total mass below ten that covers every possible remaining core by at least one rules out that branch. This permits different measures for geometrically different cases instead of demanding one universal witness for all cases simultaneously. X-014 and the later hybrid agendas already develop this direction. [6, 10]

A varying anchor cannot be replaced by one sampled pose. For a box of anchor poses, one conservative construction is a common inner region contained in every possible anchor. Other squares must avoid it. More accurate constraints retain the common anchor variables and couple them to every other square, rather than independently minimizing each interaction. Branch-specific measures need not retain the full D4 symmetry of the unconditional problem, so symmetry reduction must be adjusted to the actual stabilizer or explicitly expanded.

The strongest baseline for testing resource cuts is a coupled geometric relaxation, not a collection of independent pair checks. For squares $i,j$, with unit axes $u_i,v_i,u_j,v_j$, nonoverlap is equivalent to a separating-axis disjunction. For example, separation along $u_i$, with the appropriate sign, requires

$$
\pm u_i\cdot(c_j-c_i)
\ge \frac12\left(1+|\cos(\theta_j-\theta_i)|
+|\sin(\theta_j-\theta_i)|\right).
$$

At fixed angles and selected separating alternatives, containment and nonoverlap become linear constraints in the centers and container side. For angle boxes, outward coefficient bounds yield a necessary outer LP. Exact Farkas multipliers can certify infeasibility of that relaxation. All separation alternatives, interval error bounds, and seams must be represented; a branch selected from a known feasible packing does not cover all alternatives. The latest X-018 already identifies the need for arbitrary-descriptor assembly and exported exact infeasibility receipts. [10]

A resource cannot contradict an actually feasible instance of the complete fixed-angle LP. Its additional strength must come from information discarded by angle intervals, relaxed disjunctions, or fractional occupancy; alternatively, it may prove the same contradiction more cheaply. Compare the same domain under the same branching policy, and distinguish stronger bounds from lower computational cost.

There is relevant computational precedent, but not a ready-made eleven-square solver. Montanher, Neumaier, Markót, Domes, and Schichl rigorously solved three squares in a circle by interval methods and systematic center-domain subdivision. Their lesson is the value of geometric decomposition and smaller infeasible subproblems rather than a direct high-dimensional interval attack. Their result does not predict the cost of the substantially larger square-container problem. [16]

## 8. Toward the exact Trump value

The repository already verifies Trump's exact construction and qualitative local isolation through 128 branchwise linearized cones. It does not provide a quantified global localization theorem. Repeating a local optimality calculation is therefore not the principal missing step. [2]

A credible completion strategy has two separate obligations. First, quantify a neighborhood in which no packing with smaller side is possible, with all contact branches and boundary strata handled. Second, prove that every hypothetical packing below $U$, or every minimizer in a specified side interval, belongs to a neighborhood already excluded locally. Weighted slack, anchor cases, coupled LP exclusions, and higher-order compatibility could supply the second obligation.

The logical gap is essential: a small interval in container side does not imply that all packings lie near the known construction in configuration space. There can be unrelated contact patterns at nearly identical side lengths. A proof that the six-axis/five-common-angle family is optimal is useful, but it does not classify all packings. Even an existential theorem that some global minimizer uses an axis direction and one other angle leaves the multiplicity of the tilted class to be analyzed.

X-018's proposed contact-release and angular-reduction investigations are appropriately narrower tests of that structural program. A rank count, an infinitesimal flex, or repeated numerical returns to two angles cannot replace a finite feasible deformation argument or an exhaustive representative theorem. These tests are worth pursuing in parallel, but they should not block nearer-term certificate improvements. [10]

The old fixed-net square-core language also has an artificial ceiling below Trump's value: scaling the known construction yields eleven disjoint admissible cores at approximately 3.86898 for the retained $B$ and net. That prevents an unchanged square-core certificate from proving the last part of the interval, regardless of site density. A finer net or a better witness changes the artificial ceiling; compatibility addresses a different possible obstruction, namely a fractional gap before that ceiling. [6]

## 9. Prioritized experimental sequence

| Priority | Experiment | Decisive output | Interpretation of failure |
|---|---|---|---|
| First | Complete rows on the retained 3.8125 sites | Exact covering certificate below eleven, or exact finite-site obstruction | Rejects those sites only unless global dual depth is also certified |
| First, small independent test | Expand the centered frozen measure, using its full mass margin | Exact first bad-cell threshold or certified rational side | Quantifies remaining frozen-certificate slack; not a barrier to new weights |
| Next | Restrict to parent-feasible center domains | Matched, fully separated objective and exact candidate | Rejects that particular geometric refinement/site combination, not all cores |
| Next | Test rational octagons on parent domains | Complete polygon-coverage certificate or measured lack of useful new capture | Area gain alone is not evidence of bound improvement |
| Parallel structural lane | Close one complete anchor case using coupled geometry plus compatibility cuts | Exact branch exclusion and explicitly retained sibling cases | A timeout or sampled infeasibility is not a global negative |
| Longer horizon | Quantify local Trump exclusion and prove global localization or an angular representative theorem | A complete residual case cover | Local rigidity or restricted-family optimality alone does not close the problem |

Use rational target sides 3.8125, 3.815, 3.817, and 3.82 to avoid conflating synthesis and validation. A found certificate at 3.817 would justify the desired advance; an interpolation through that value does not. For every run, preserve the distinction between a finite-row LP objective, a globally feasible covering measure, a finite-site dual obstruction, and a globally depth-feasible fractional packing.

The practical conclusion is not that the current method is exhausted. Its reviewed failures do not establish that. The strongest near-term plan combines completion of the existing scalar discriminator with precise removal of unnecessary geometric constraints. The most credible route to a considerably larger advance is to retain the successful weighted measure as one component of a compatibility-aware, branchwise exact proof.

## Sources

Repository sources below are pinned to the reviewed snapshot. References report what the repository states; they are not assertions that every recorded experiment was independently replayed for this note.

1. Joshua Levy and project collaborators, *s(11) ≥ 381/100: A New Lower Bound on the Square Packing Problem*, public explainer, accessed September 8, 2026. https://jlevy.github.io/squares/
2. `packing/frontier/n-011.md`, case status, exact upper construction, local rigidity, and T-022 refinement. https://github.com/jlevy/squares/blob/7ef80525b35a8e77e00b460a7e08f1489134d0cc/packing/frontier/n-011.md
3. `packing/campaign/agendas/agenda-025-adaptive-fractional-frontier.md`, interpolation near 3.817, adaptive witnesses, and scalar run status. https://github.com/jlevy/squares/blob/7ef80525b35a8e77e00b460a7e08f1489134d0cc/packing/campaign/agendas/agenda-025-adaptive-fractional-frontier.md
4. `packing/cases/n11_fractional_certificate/certificate.json`, exact certificate constants. https://github.com/jlevy/squares/blob/7ef80525b35a8e77e00b460a7e08f1489134d0cc/packing/cases/n11_fractional_certificate/certificate.json
5. `packing/frontier/CERTIFICATE-REACH.md`, restricted covering values and method ceilings. https://github.com/jlevy/squares/blob/7ef80525b35a8e77e00b460a7e08f1489134d0cc/packing/frontier/CERTIFICATE-REACH.md
6. `packing/campaign/explorations/X-014-closing-from-both-ends.md`, fractional duality, slack lemmas, conditional certificates, and core ceiling. https://github.com/jlevy/squares/blob/7ef80525b35a8e77e00b460a7e08f1489134d0cc/packing/campaign/explorations/X-014-closing-from-both-ends.md
7. `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-252-exp116-next-discriminator.md`, September 7 assessment of incomplete row solves and truncated dual extraction. https://github.com/jlevy/squares/blob/7ef80525b35a8e77e00b460a7e08f1489134d0cc/packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-252-exp116-next-discriminator.md
8. `packing/src/sqpack/fractional/sweep.py`, particularly `centre_domain`, event-cell geometry, and boundary semantics. https://github.com/jlevy/squares/blob/7ef80525b35a8e77e00b460a7e08f1489134d0cc/packing/src/sqpack/fractional/sweep.py
9. `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-064-h-063-two-threshold-class-program.md`, the exact ceiling of the tested two-class construction. https://github.com/jlevy/squares/blob/7ef80525b35a8e77e00b460a7e08f1489134d0cc/packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-064-h-063-two-threshold-class-program.md
10. `packing/campaign/explorations/X-018-hybrid-strength-and-angular-release.md`, September 7 hybrid strategy, coupled LPs, capacities, and contact-release programs. https://github.com/jlevy/squares/blob/7ef80525b35a8e77e00b460a7e08f1489134d0cc/packing/campaign/explorations/X-018-hybrid-strength-and-angular-release.md
11. Walter Stromquist, *Packing 10 or 11 unit squares in a square*, Electronic Journal of Combinatorics 10 (2003), R8. Historical geometric arguments; see the project's separate discussion of its repaired Figure 14 step. https://www.combinatorics.org/ojs/index.php/eljc/article/download/v10i1r8/pdf
12. Sam Burns, *Proposing a Better Lower Bound for n=17 Square Packing*, August 2026. https://sam-burns.com/posts/proposing-better-lower-bound-for-n17-square-packing/
13. Gustavo Massaccesi, *Another Better Lower Bound for n=17 Square Packing*, August 2026. https://gus-massa.blogspot.com/2026/08/another-better-lower-bound-for-n17.html
14. David de Laat and Frank Vallentin, *A semidefinite programming hierarchy for packing problems in discrete geometry*, Mathematical Programming, Series B 151 (2015), 529–553; arXiv v3, 2021. https://arxiv.org/abs/1311.3789v3
15. Bram Bekker and Fernando Mário de Oliveira Filho, *On the convergence of the k-point bound for topological packing graphs*, 2023. https://arxiv.org/abs/2306.02725
16. Tiago Montanher, Arnold Neumaier, Mihály Csaba Markót, Ferenc Domes, and Hermann Schichl, *Rigorous packing of unit squares into a circle*, Journal of Global Optimization 73 (2019), 547–565; online October 3, 2018. https://link.springer.com/article/10.1007/s10898-018-0711-5

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
