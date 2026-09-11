# Fractional Packing, Duality, and the Next N11 Discriminators

**Analytical spike for X-027, September 10, 2026.** The retained 88-core certificate
already gives a full-unit-square fractional packing of mass eleven after exact uniform
rescaling, at side

$$
L_* = \frac{191/50}{9977/10000} = \frac{38200}{9977} \approx 3.8288.
$$

It therefore supplies the proposed ordinary point-certificate obstruction throughout
`3.83–3.85`. Searching for that existence result again would duplicate retained
evidence. Stronger threshold certificates remain possible: a fractional packing must
satisfy their additional capacities before it obstructs them.

The continuous problem also admits a precise duality argument.
For legal closed unit squares, use **open interiors** in the incidence relation,
nonnegative Borel measures on pose space for packings, and nonnegative Borel measures on
the container for covers.
Compactness and finite linear-programming duality then give equality of the packing
supremum and covering infimum, with a packing optimizer.
A separate smoothing argument identifies that value with the absolutely continuous
covering value in BC-242. These are analytical arguments independently reviewed here;
they are not newly admitted frontier results or claims of novelty.

The global bracket remains `3.826447410572939744... <= s(11) <= 3.877083590022814...`.
Because its lower endpoint is below `L_*`, the fractional witness alone does **not**
prove a strict gap between fractional and physical eleven-square packing.

Evidence labels below distinguish **retained exact evidence**, **analytic derivation**,
and **prospective experiment**. The starting evidence is the
[current handoff](../../../SYNOPSIS.md#current-handoff), the
[combined inference account, §§12–13](research-2026-09-09-n11-evidence-and-inference.md#12-the-combined-series-takeaways-and-open-comparisons),
[X-023](../../../packing/campaign/explorations/X-023-three-losses-and-a-new-atom.md),
[X-026](../../../packing/campaign/explorations/X-026-what-conditioning-does-and-does-not-buy.md),
and the
[BC-242 density contract](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-242-full-size-density-proof-contract.md).
The
[archived Stromquist correspondence](../../../packing/resources/private-correspondence/email-stromquist-2026-09-07.md)
motivates the question; the archive is unchanged.
No numerical target was run for this spike.

## 1. Exact Rescaling Already Answers the Mass-Eleven Question

The retained
[family](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/ceiling-family-191-50.json)
contains 88 closed squares `Q_i`, each of side `B = 9977/10000`, in `[0, 191/50]²`, with
weights `a_i = 1/8`. Its
[independent receipt](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/ceiling-family-191-50-independent-reader.json)
records exact containment of all 352 corners, total weight eleven, and maximum closed
depth one over all 20,376 arrangement vertices.
Its geometric statement is

$$
\sum_{i=1}^{88} a_i\mathbf 1_{Q_i}(x)\leq 1
\qquad\text{for every point }x.
$$

**Analytic derivation.** Put `U_i = B^{-1} Q_i`, scaling positions and square sides
together about the origin.
Then each `U_i` is a contained unit square in `[0,L_*]²` and

$$
\sum_i a_i\mathbf 1_{U_i}(x)
=\sum_i a_i\mathbf 1_{Q_i}(Bx)\leq1,
\qquad \sum_i a_i=11.
$$

This preserves the entire closed incidence relation, including edges and vertices.
Embedding the same family in a larger container preserves feasibility.
In particular,

$$
\frac{383}{100}-L_* = \frac{1191}{997700}>0,
$$

so the witness is already available below `3.83`.

The original reader’s `symmetric_only` label concerns its *folded finite-net covering
problem*: 44 placements have mirrored directions, so a cover of only the listed net
directions needs D4 symmetry to cover them.
In the full-unit problem every actual orientation of all 88 squares is legal.
Any cover of every legal unit square must cover each of those squares directly.
The homothety therefore obstructs **arbitrary point measures**, including asymmetric
ones, for that full pose domain.
No symmetry theorem or new angle-containment estimate is needed for this step.

Indeed, for any nonnegative point measure `mu` with `mu(U_i) >= 1`,

$$
11\leq\sum_i a_i\mu(U_i)
=\int\sum_i a_i\mathbf 1_{U_i}\,d\mu
\leq\mu([0,L_*]^2).
$$

The conclusion holds for either closed-square coverage or interior coverage, since the
closed-depth bound is the stronger capacity statement.

It also limits every ordinary point certificate obtained by selecting a strictly
interior core from each unit square.
Select the admitted core `K_i` inside each `U_i`; then `1_{K_i} <= 1_{int U_i}`, so
their weighted depth remains at most one.
A valid core-cover certificate of budget below eleven would contradict that family.
This opens the rescaled obstruction to any net and shrink with a proved core-selection
map; it does not require the new net to contain the original six folded directions.

This is a limitation of the unconditional ordinary point language at `L_*` and larger
sides. It is not a physical eleven-square construction.
Nor does it obstruct a conditionally restricted family without proving that its members
satisfy the added conditions.

## 2. The Measure Spaces and the Boundary Convention

Fix `L >= 1`, let `C_L = [0,L]²`, and put

$$
Q=[-1/2,1/2]^2,\qquad
\mathbb T_4=\mathbb R/(\pi/2)\mathbb Z.
$$

A pose is `p = (c,theta)` and represents the closed unit square `S_p = c + R_theta Q`.
The legal pose space is

$$
P_L=\{(c,\theta)\in C_L\times\mathbb T_4:S_p\subseteq C_L\}.
$$

Containment is closed under pose limits, so `P_L` is compact and metrizable.
It includes wall-touching poses.
There is no absolute continuity assumption on a packing measure; atomic and
lower-dimensional pose distributions must be allowed, including physical packings.

Write `M_+(Y)` for finite nonnegative Borel measures on the compact space `Y`. The
interior incidence kernel is

$$
A(x,p)=\mathbf 1_{\operatorname{int}S_p}(x).
$$

The set where `A = 1` is open in `C_L x P_L`: strict square membership persists under
sufficiently small changes of both the point and the pose.
Define

$$
\begin{aligned}
\nu_\circ(L)
&=\sup\left\{w(P_L):w\in M_+(P_L),
\int A(x,p)\,dw(p)\leq1\text{ for every }x\in C_L\right\},\\
\tau_\circ(L)
&=\inf\left\{\mu(C_L):\mu\in M_+(C_L),
\mu(\operatorname{int}S_p)\geq1\text{ for every }p\in P_L\right\}.
\end{aligned}
$$

Packing mass lives on **poses**; covering mass lives on **container points**. The
packing capacity is `<= 1`, whereas the covering requirement is `>= 1`. These fix the
informal continuous description in the correspondence without changing its intent.

**Weak duality.** Tonelli’s theorem, with nonnegative integrands, gives

$$
w(P_L)
\leq\int_{P_L}\mu(\operatorname{int}S_p)\,dw(p)
=\int_{C_L}\!\int_{P_L} A(x,p)\,dw(p)\,d\mu(x)
\leq\mu(C_L).
$$

A physical packing gives `w = sum_i delta_{p_i}` and satisfies interior depth at most
one even when squares touch.
Also `w(P_L) <= L²`, by integrating its depth over area; each legal unit square has area
one.

### Two boundary counterexamples

Take two touching unit squares `[0,1]²` and `[1,2] x [0,1]`. Their interiors have depth
one. A unit atom at `(1,1/2)` lies in both closed squares, so it covers this two-square
family with mass one.
Thus interior capacities cannot be paired with closed coverage of an arbitrary singular
measure. BC-242’s boundary term is a real obstruction, not a technicality.

Closed-depth feasibility also need not survive weak convergence.
In the fixed container `[0,3]²`, use the unit squares `[0,1]²` and
`[1+1/j,2+1/j] x [0,1]`, both with weight one.
For every positive integer `j` they have closed depth one.
Their pose measures converge to the touching pair, whose closed depth is two on the
common edge. Compact pose space alone consequently does not make the closed-depth
feasible set compact.
The interior-depth limit remains feasible.

## 3. A Strong-Duality Argument with Finite Covers

**Analytical theorem, independently reviewed.** In the full-unit model above,

$$
\nu_\circ(L)=\tau_\circ(L)
=\inf\{\mu(C_L):\mu\text{ is a finite atomic interior cover}\}
=\tau_{\mathrm{ac}}(L),
$$

where `tau_ac` is BC-242’s infimum over nonnegative `L¹` densities.
The packing supremum is attained by a Borel measure on `P_L`. The argument does not
assert that a covering optimizer, density optimizer, or finite packing optimizer exists.

### Finite hitting set and compact packing measures

For a point `x`, let

$$
V_x=\{p\in P_L:x\in\operatorname{int}S_p\}.
$$

These open subsets cover `P_L`: each legal square has an interior point.
Compactness gives a finite hitting set `F_0` of points with
`P_L = union_{x in F_0} V_x`. Any packing measure satisfying just the point capacities
on `F_0` has

$$
w(P_L)\leq \sum_{x\in F_0}w(V_x)\leq |F_0|.
$$

Use the weak topology on Borel measures, defined by integration against continuous
functions. For each open `V_x`, the map `w -> w(V_x)` is lower semicontinuous.
Consequently `{w:w(V_x) <= 1}` is closed.
Nonnegative measures on compact `P_L` with mass at most `|F_0|` form a compact space.
Intersecting its closed point-capacity sets gives a compact full feasible set.
Mass is a continuous functional, so a packing optimizer exists.

### Exact finite LPs and their direction

Let `F` be any finite point set containing `F_0`, and impose only its point capacities.
There are at most `2^{|F|}` realized incidence masks

$$
I(p)=\{x\in F:x\in\operatorname{int}S_p\}.
$$

Every realized mask is nonempty because `F_0` hits every pose.
Its pose class is Borel, being a finite Boolean combination of the open sets `V_x`.
Aggregate a measure’s mass by these masks.
Conversely, choose one legal representative pose for each realized mask to lift any
finite mask solution to a measure.
Thus the relaxed measure problem is exactly a finite LP, with value `v_F`. Its dual is

$$
\min\left\{\sum_{x\in F}a_x:
a_x\geq0,\quad \sum_{x\in I}a_x\geq1
\text{ for every realized mask }I\right\}.
$$

The constraints in this finite dual cover **every** legal pose, not merely a sampled
list. Its optimum is a globally feasible finite atomic interior cover of mass `v_F`.
Finding every realized mask may be expensive; the finite reduction is an existence
proof, not a promise of a small or currently implemented enumeration.

Removing point capacities gives `v_F >= nu_circle(L)`. To prove that these upper
approximations converge to the full packing value, suppose some `t > nu_circle(L)` were
feasible for every finite `F`. In the fixed compact measure space, impose the closed
condition `w(P_L) >= t` and all closed point capacities.
Every finite collection would have a common solution, so compactness would give a full
feasible measure of mass at least `t`, a contradiction.
Hence

$$
\inf_{F\supseteq F_0,\;F\text{ finite}}v_F=\nu_\circ(L).
$$

The finite dual covers give `inf_atomic tau <= nu_circle`. Weak duality gives
`nu_circle <= tau_circle <= inf_atomic tau`, proving equality.
This is the step that justifies finite upper witnesses for every *strict* target: if
`nu_circle(L) < n`, some finite atomic interior cover has mass below `n`.

### Smearing the atoms gives the BC-242 density value

Take a finite atomic interior cover `mu = sum_i a_i delta_{x_i}`. Discard zero weights
and atoms on the boundary of the container; no contained square’s interior uses such a
boundary atom. At every pose `p`, the atoms strictly inside `S_p` carry mass at least
one. Finitely many strict inequalities give a neighborhood of `p` on which those same
atoms stay inside, with a positive margin from the square boundary.
A finite subcover of `P_L` therefore gives a single `delta > 0` such that every legal
pose contains whole `delta`-balls around a subset of atoms of weight at least one.
Reduce `delta` also below the distance of every retained atom to the container boundary.

Replace each atom by its mass times a normalized nonnegative density supported in its
`delta`-ball. The resulting density is supported in `C_L`, has the same total mass, and
covers every legal square by at least one.
Thus `tau_ac <= inf_atomic tau`. Every absolutely continuous cover is itself a Borel
interior cover, since a square boundary has area zero.
The reverse inequality follows, completing the theorem.

This argument uses topology at the places the informal finite-to-continuous argument
needs it. The general infinite-hypergraph problem does not inherit finite LP duality
without hypotheses; Aharoni and Holzman give negative general cases in
[their 1992 paper](https://holzman.net.technion.ac.il/files/2012/09/gcoptimal.pdf).
Their terminology for weak and strong duality differs from the value-equality
terminology used here.

### Why BC-242’s a.e. packing value is the same value

For any finite pose measure `w`, the closed and interior depths differ by

$$
b_w(x)=\int_{P_L}\mathbf 1_{\partial S_p}(x)\,dw(p),
\qquad \int_{C_L}b_w(x)\,dx=0.
$$

Tonelli proves the second equality even for an uncountable pose support.
Thus the two depths agree for area-almost every point.
Interior depth is lower semicontinuous in `x`; if it exceeds one at an interior point of
`C_L`, it exceeds one on a neighborhood of positive area.
On the container boundary it is zero.
Therefore

$$
d_w^{\rm closed}\leq1\text{ a.e.}
\quad\Longleftrightarrow\quad
d_w^\circ\leq1\text{ everywhere}.
$$

BC-242’s `nu_ae` is consequently `nu_circle`, and the theorem supplies a route to
`nu_ae = tau_ac` and attainment of the packing measure.
It does not assert that their value is eleven at Trump’s side, or provide BC-242’s
missing equality classification.
It also does not permit closed coverage by singular point mass against a.e. depth.

As a separate check, BC-242’s continuous map `rho -> (p -> integral_{S_p} rho)` permits
a minimax formulation using probability measures on compact `P_L` and nonnegative
unit-mass `L¹` densities.
Its bilinear payoff is continuous in both variables separately, so the one-compact-side
corollary in [Sion’s minimax theorem](https://msp.org/pjm/1958/8-1/pjm-v8-n1-p14-p.pdf)
gives the same value equality after reciprocal normalization.
The finite-mask proof above also supplies the atomic-cover consequence.

## 4. What Finite Witnesses Follow, and What Does Not

The compactness proof supplies finite **covering** witnesses for a strict inequality
`nu_circle(L) < n`. It does not give a bound on their size, a separation algorithm, or a
finite packing witness attaining `nu_circle(L)` at that exact side.

For example, in the abstract compact open-incidence system `X = P = [0,1]`,
`A(x,p) = 1[x != p]`, the value is one.
An atomless probability measure covers every pose, while any finite atomic cover of
total mass `M` must obey `M - max_atom >= 1` and hence `M > 1`. Uniform weights on `r`
sites give mass `r/(r-1)`, approaching one.
This is an example about the theorem’s general topology, not a counterexample claimed
for unit squares. Value equality alone does not entail a finite optimal object on both
sides.

A useful weaker finite-packing statement does follow from the geometry.

**Lemma sketch, with side relaxation.** If a Borel fractional packing at side `L` has
mass at least an integer `n`, then for every `epsilon > 0` there is a finite fractional
packing of unit squares of mass at least `n` at side `L + epsilon`.

Choose a rational shrink `b < 1` with `L/b < L + epsilon`. Partition the compact pose
space into finitely many sufficiently small Borel pieces.
In each nonempty piece, choose a representative pose.
Its concentric closed `b`-square has a strict edge-normal margin `(1-b)/2` inside its
own unit parent. Uniformly small pose pieces preserve part of that margin inside every
unit square represented by the piece.
Give the core the piece’s measure.
A point contained in a representative core is then contained in every original square of
the piece, so the finite core family inherits depth at most one.
Its total mass is unchanged.
Uniform dilation by `1/b` makes its cores unit squares and places them in side `L/b`.

There is also room to choose rational centers and rational half-angle parameters before
dilation, by reserving part of the containment margin.
On that fixed finite rational family, all-point closed depth is a finite rational LP
over the arrangement vertices.
The real weights just constructed are feasible, so a rational optimal weight vector has
mass at least `n`. Scaling its weights down to total exactly `n` and clearing
denominators produces an integer `k` and an `n k`-member multiset with depth at most `k`
in the enlarged side.
Repeated copies of the same pose count with multiplicity.

The margin must be retained at both approximations.
This lemma does not turn a bounded search for `k = 2` or `k = 4` into a complete
decision, and it does not justify the unrestricted assertion
`nu_circle(L) >= n iff some finite k-fold packing exists at L`. Exact-side finite
attainment requires an additional argument.
The retained 88-square family does give a concrete `k = 8`, `n = 11` instance at `L_*`,
independently of that open issue.

## 5. Integrality Gaps and Threshold Capacities

Let `m(L)` be the maximum number of physical unit squares with disjoint interiors.
Then

$$
m(L)\leq\nu_\circ(L)=\tau_\circ(L).
$$

A mass-eleven fractional family establishes a strict physical integrality gap at a side
only after a separate theorem shows `m(L) <= 10`. The existing global lower bound does
not provide that theorem at `L_*`. A future global exclusion at a side at least `L_*`
would, together with the retained homothety, establish that the ordinary point
relaxation loses physical information there.

There is already a matched **core-model** gap.
T-025 uses the same `L = 191/50`, `B = 9977/10000`, and 181-direction net as the 88-core
family, with the same D4/reflected-direction convention.
Its threshold charges cover every admissible core with budget below eleven.
The counting theorem therefore excludes eleven pairwise disjoint closed cores in that
domain, although the fractional core family has mass eleven.
See the
[exact T-025 packet](../../../packing/cases/n11_threshold_certificate/t-025-threshold-certificate-proof.md).
Transporting that statement to physical unit squares with possible boundary touching
requires its own argument; the core-model gap alone is not the unresolved full-unit gap.

For a finite point set `S` and integer `k`, define the full-unit interior threshold
charge and capacity by

$$
q_{S,k}(p)=\mathbf 1[|S\cap\operatorname{int}S_p|\geq k],
\qquad c_{S,k}=\left\lfloor\frac{|S|}{k}\right\rfloor.
$$

Every integral interior-disjoint packing satisfies `sum_p q_{S,k}(p) <= c_{S,k}`,
because its point traces are disjoint.
A fractional family can violate

$$
\int q_{S,k}(p)\,dw(p)\leq c_{S,k}
$$

while satisfying all point capacities.
The closed-core version uses closed traces and pairwise disjoint closed cores.
Boundary conventions must match in either version.

An explicit unit-square example explains the extra information.
In `[0,3]²`, take axis-aligned squares centered at `(1,1)` and `(8/5,8/5)`, and a square
centered at `(19/10,7/10)` with cosine `3/5` and sine `4/5`. Give each weight `1/2`. The
first two intersect on `[11/10,3/2]²`. On that box the third square’s second slab
coordinate is at least `14/25 > 1/2`, so the triple intersection is empty.
Each pair intersects in its interior: representative pair points are

$$
(13/10,13/10),\qquad(7/5,7/10),\qquad(19/10,6/5).
$$

Consequently the family has depth at most one and mass `3/2`, but its three members
pairwise overlap, so an integral packing restricted to this support has size at most
one. Every square contains two of those three points.
The two-of-three capacity is one and the family charges it `3/2`. This is the rational
non-Helly control retained in
[the plateau-reader tests](../../../packing/tests/test_plateau_reader.py), with its
geometry spelled out here rather than inferred from an LP reading.

Stromquist’s fractional objection therefore applies to additive ordinary point covers.
For a point-and-threshold certificate, weak duality requires both the point capacities
and every threshold capacity that the certificate uses.
No assertion that all threshold or rank-one inequalities recover the integral packing
hull follows.

The A6 evidence illustrates both sides.
Its 64-placement family of weight eleven is feasible for all point capacities and the
retained 2,566 atom orbits, so that *fixed atom set* cannot produce a budget below
eleven on its declared core domain.
Later atoms cut particular families.
The exact upper value `2605263163/250000000`, approximately `10.421`, applies to the
separate 280-placement support with the stated cuts.
It bounds neither all possible supports nor the full threshold language.
The larger covering LP remained at eleven after the six added atoms, so no global
improvement follows from the support upper bound.
These are the two outcomes documented together in
[§13 of the inference account](research-2026-09-09-n11-evidence-and-inference.md#13-the-later-a6-and-h157-results-what-has-been-checked).

## 6. N6 Is a Cleaner Physical-Gap Control

The retained [n6 case](../../../packing/frontier/n-006.md) has `s(6) = 3` with a
published proof and archived earlier work.
Any exact full-unit fractional family of mass six at a side strictly below three would
therefore prove a physical integrality gap immediately.
N11 lacks that matched integral exclusion at `L_*`.

The correspondence’s failure to find a pure five-dot proof is a different statement.
It concerns five **unweighted** sites, not arbitrary positive weights or arbitrary site
counts.
As an abstract counterexample to the inference, take three disjoint copies of the
triangle set system with edges `{a,b}`, `{b,c}`, `{c,a}`. A transversal needs six
unweighted sites, while weights `1/2` on each of its nine sites give fractional cover
mass `9/2`. Thus the absence of a five-site transversal need not preclude a weighted
cover of mass below six.
This example asserts no geometric realization by the full square pose family.

A useful n6 experiment must consequently ask for one of two positive witnesses at a
declared side below three: an exact fractional mass at least six, or a globally verified
interior cover of mass below six.
A finite pose support whose maximum stays below six gives only a lower bound on the
global fractional value, and an unsuccessful five-dot search supplies neither witness.

## 7. Next Discriminators and Their Prerequisites

These are proposed mathematical comparisons, ordered by dependency and new information,
not by measured runtime.
Any numerical implementation needs a maintained tool and its own prospective experiment
contract.

| Question or mechanism | First cheap falsifier or decision | Experiment prerequisite and scope of a negative result |
| --- | --- | --- |
| Does mass eleven exist for full units at `3.83–3.85`? | The retained homothety proves existence at `38200/9977`, already below that interval | A source-bound unit-family export and independent replay would make the corollary directly consumable; no search is required |
| Does the full-unit point obstruction begin materially below `L_*`? | Freeze a smaller target and try an exact finite witness or a globally certified cover below eleven | A separate interior/a.e. arrangement reader must accept touching controls and reject positive-area excess; a fixed-support value below eleven cannot refute existence |
| Do richer atoms improve the covering problem at a fixed side? | Add an exactly violated atom, then require either changed globally verified coverage or a valid obstruction for the enlarged atom catalog | Alternate support and atom updates with full point-depth checks; a cut source that has depth above one is a proposer, not an obstruction |
| Can the retained obstruction survive conditional ownership? | Test actual residual membership and the proposed ownership/selection inequalities on the exact witness | Parent, mark, patch, joint-compatibility and routing premises must be declared; surviving one selection does not prove that every physical packing lacks an excluded selection |
| Is there a physical fractional gap for n6 below three? | An exact mass-six full-unit family settles it positively; a certified cover below six excludes a mass-six family at the chosen side | Use `L = 3` integral controls and a frozen below-three target; bounded failure to find a family is inconclusive |
| Is the new strong-duality proof admissible? | Independently challenge the finite hitting set, weak closedness, finite-mask LP and uniform smearing margin | No numerical run is needed; admission would close a theorem-contract gap, not determine the value or classify optimal packings |

For the direct n11 bound program, the useful question past `L_*` is which valid
capacities or structural restrictions remove fractional mass that point depth allows.
Threshold cuts have already demonstrated that mechanism on the matched core model.
The next comparison must measure their effect on a globally covered pose domain or on an
admitted conditional proof; eliminating one finite support is insufficient.

## 8. Review Provenance and Remaining Scope

The X-027 [structural-helper worker](research-2026-09-10-x027-structural-helpers.md)
independently reconstructed the open-incidence duality proof before reading this draft,
then checked the exact rescaling, removal of the folded-net symmetry restriction,
compactness direction, finite Borel masks, uniform atom-smearing margin and a.e.
equivalence. Its disposition was PASS. It also checked the side-relaxed rational
finite-witness argument in §4, including the bounded rational arrangement LP, and the
three rational pair-intersection points and empty triple intersection in §5; PASS.

The X-027
[certificate-mechanisms worker](research-2026-09-10-x027-certificate-mechanisms.md)
independently checked the rescaling and any-admitted-core-selection implication,
finite-mask strong duality, packing attainment, atomic-cover consequence, smearing and
the a.e. equivalence; its disposition was PASS. It then checked §§4–7, including
rationalization, the non-Helly example and A6/n6 scope, with the same disposition.
Its two wording suggestions, making the core reflection convention explicit and
narrowing the n6 negative to mass-six feasibility, are incorporated.

These are analytical results independently reviewed here, with no frontier admission or
novelty claim. The retained 88-core source and its receipts were inspected, not
numerically rerun in this spike.
No finite optimal packing at the same side, attained optimal cover, equality value at
Trump’s side, new physical n11 integrality gap, or global lower-bound improvement has
been established. The finite export, separate interior-depth instrument and prospective
geometric comparisons remain unrun.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
