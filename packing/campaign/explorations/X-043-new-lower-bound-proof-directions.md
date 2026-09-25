---
title: X-043 — new lower-bound proof directions after the external advances
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-043
  title: New Lower-Bound Proof Directions After the External Advances
  date: '2026-09-22'
  author: GPT-6 Astra at max reasoning; reviewed by the root coordinator
  campaign: packing.squares
  brief: >-
    A W3 innovation block requested by the owner: consolidate PR221 and PR222,
    the completed independent n11 computation, and earlier negative results;
    develop new hypotheses, proof strategies, and enabling instruments for
    materially stronger lower bounds at n11 and n17. Small bounded spikes are
    permitted. Produce ideas with enough mathematical shape for subsequent
    codification and prioritization, without starting a full research campaign.
  sources:
  - operating-rules.md
  - SYNOPSIS.md
  - packing/campaign/README.md
  - packing/campaign/ideas.md
  - packing/campaign/ledger.md
  - packing/campaign/explorations/X-026-what-conditioning-does-and-does-not-buy.md
  - packing/campaign/explorations/X-027-stromquist-fractional-and-structural-strategy.md
  - packing/campaign/explorations/X-040-lower-bound-mechanisms-beyond-the-one-body-ceiling.md
  - packing/campaign/explorations/X-042-what-is-left-at-low-n.md
  - docs/project/research/research-2026-09-10-x027-certificate-mechanisms.md
  - docs/project/reviews/review-2026-09-21-n17-kleddamag-461300-99853.md
  - docs/project/reviews/review-2026-09-22-kleddamag-n11-mathematics.md
  - docs/project/reviews/review-2026-09-22-tokoharu-density-mathematics.md
  - packing/frontier/n-011.md
  - packing/frontier/n-017.md
  - packing/cases/trump11/isolation-theorem.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-041/exp-221-n17-kleddamag-unrestricted-receipt.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-041/exp-222-n17-repricing-receipt.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-041/exp-222-n17-repricing-cells.jsonl
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-040/h222-registration-review.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-040/h232-ring-centre-derivation.md
  - packing/resources/web/external-square-certificates-2026-09-22/kleddamag-11/global-certificate.json
  - packing/resources/web/external-square-certificates-2026-09-22/kleddamag-11/exact_mixed.py
  - packing/resources/web/n17-kleddamag-certified-bound-2026-09-21/kleddamag-17-squares-certified-bound/global-certificate.json
  - https://arxiv.org/abs/1311.3789v3
  - https://arxiv.org/abs/1308.4893v3
  - https://optimization-online.org/wp-content/uploads/2018/04/6556.pdf
  proposes: []
---
# X-043: New Lower-Bound Proof Directions After the External Advances

The most promising new proof architecture is to **use a strong covering certificate to
identify the placements on which it loses, then prove that too few of those placements
can coexist**. The certificate already handles most single-square geometry.
Actual parent-square compatibility can supply the missing information on the remainder.
This gives a specific way to combine the recent computational advances with structural
geometry, without beginning with an unproved normal form for an entire packing.

For an earlier numerical improvement, **n17 offers the clearer opening for joint support
and atom discovery**. Its current certificate uses ordinary points and two-of-three
features; n11 now demonstrates that an adaptive catalogue combined with two-of-five and
three-of-five features can be effective.
This is a reason to test that combination at n17, not evidence that five-site features
caused n11’s gain or that the same gain transfers.

Two more exploratory directions deserve mathematical development: **integer charges on
continuous density reservoirs**, which combine Tokoharu’s area integrals with threshold
counting; and **a localized positive-semidefinite kernel on difficult pose regions**,
which could replace an enormous global conflict graph.
The first removes the need for strict cores when all resources are absolutely
continuous. The second uses actual pair compatibility while avoiding a matrix indexed by
millions of pose cells.
Both have explicit proof obligations below; neither has a measured packing advantage.

This is a W3 exploration under `think-4kov`. It contributes deductions, candidate
hypotheses, two small exact diagnostics, and preliminary judgments of promise.
It does not promote a lower bound, decide a registered hypothesis, select a funded
queue, or claim literature novelty.
Candidate labels in this report are local labels; `proposes: []` remains empty until the
coordinator codifies them.

## The Starting Point Has Changed

Let $s(n)$ be the least side of a square container holding $n$ unit squares with
independent rotations and pairwise disjoint interiors.
Boundary contact is allowed.

| Case | Current verified lower statement | Upper reference | Meaning of a substantial next step |
| --- | --- | --- | --- |
| n11 | $s(11)>31/8=3.875$, Kleddamag | Trump’s exact verified $U_{11}=3.877083590022814177\ldots$ | The remaining gap is only $0.002083590022814177\ldots$. A target such as $3.876$ removes about half of it; an exact optimality proof needs global geometric information. |
| n17 | $s(17)>461300/99853=4.6197910929065726618\ldots$, Kleddamag | Bidwell’s **reported** $U_{17}\approx4.67553009360455$; the register’s verified upper is still $5$ | There is about $0.055739$ to the reported construction. Targets such as $4.63$ or $4.65$ are meaningful research milestones, not predictions. |

The upper-column distinction at n17 matters.
A gap to a reported construction is not the same object as the register’s fully verified
bracket. The case files remain the authority for these endpoints:
[n11](../../frontier/n-011.md), [n17](../../frontier/n-017.md).

PR221’s T-033 is valuable historical method evidence: it proves

$$
s(11)\ge
\frac{955000\sqrt{2073600042893309449}}{359341754646249}
=3.826997548829543624\ldots.
$$

It refines the direction net for the retained T-025 family.
Its fixed-family endpoint $955000/249507\approx3.82755$ is below the current external
bound. Another refinement of that same frozen family cannot be a new global lower-bound
result. The earlier identifiers and frozen bytes still matter for ancestry and controls.
[X-042](X-042-what-is-left-at-low-n.md#the-one-bound-that-moved) records the calculation
and its distinction between a limiting lower bound and exclusion at the endpoint.

### What the external certificates establish about mechanisms

Kleddamag’s n11 certificate changes several ingredients together.
It has 5,284 sites, 350 positive feature orbits, and 12,028 adaptive orientation
intervals. The positive orbits comprise 66 ordinary-point, 132 two-of-three, 10
two-of-five, and 142 three-of-five orbits.
It certifies parent side $A=764/775$ inside a container of side $L=191/50$, so the
unit-square bound is $L/A=31/8$. The exact coverage threshold and budget are

$$
\Gamma=\frac{31248829}{31250000},\qquad
M=\frac{1374934993}{125000000},\qquad
11\Gamma-M=\frac{13483}{125000000}>0.
$$

Those are a successful **combination** of supports, weights, threshold types, parent
domains and core choices.
No controlled ablation assigns the gain to one component.
The threshold principle itself was already present in this project; the new fixed
certificate and stronger result are Kleddamag’s contribution.
The pinned
[n11 source](https://github.com/Kleddamag/11-squares-certified-bound/tree/6a733f339395c3514f2ab63d8c4aa64cf63c0b5a)
and
[mathematical review](../../../docs/project/reviews/review-2026-09-22-kleddamag-n11-mathematics.md)
keep these distinctions explicit.

The completed native computation on frozen engine commit
`c183cc9abe93eedcb268a5390cdd1cdc6e7bbb39` certified all 12,028 rows by
directed-rounding boxes and direct threshold counts.
It recorded 136,081,500 boxes, no stalls or exhausted budgets, and 6,197.381 seconds
with two workers. This adds a different complete method for the same numerical theorem.
Its source digest is `57e9927da5c13f42dd8bcbf8f08c84363635fece626657ee63a810c61cd44458`.
The
[complete native proof receipt](https://github.com/jlevy/squares/blob/e473da2fde1ca42ea3a10ef0f390a593dcbf91da/packing/campaign/agent-sessions/session-153-native-full.json)
and
[mathematical review](https://github.com/jlevy/squares/blob/e473da2fde1ca42ea3a10ef0f390a593dcbf91da/docs/project/reviews/review-2026-09-22-native-n11-parent-core.md)
are pinned to their reviewed PR223 commit.
No new numerical bound follows from confirming it.

At n17, the
[pinned source](https://github.com/Kleddamag/17-squares-certified-bound/tree/a499e2c739ce7853fa04c8bcdc85caf1c2b01b37)
uses 7,853 parent-angle intervals, 6,744 positively weighted ordinary sites and 2,008
physical two-of-three features.
The source proof and its complete replay were already reviewed before PR222; the later
integration corrected the verified field to use that stronger evidence.
The
[n17 review](../../../docs/project/reviews/review-2026-09-21-n17-kleddamag-461300-99853.md)
records the source and Guzhou checker lineage.

Tokoharu’s
[rectangle-density work](https://github.com/tokoharu/square-packing-density-bounds/tree/b543990f7794b8c511cb46cf3854b7e8166c3674)
provides a different numerical representation and rigorous area-integration machinery.
Its replayed bounds at n26 and n29 are $5.508$ and $5.71$; its n11 density bound is
$3.81$. The related
[wand125 point certificates](https://github.com/wand125/square-packing-bounds/tree/1398e42f17f23fe3744bc54425a589fab1f3542c)
provide further source and search ancestry.
These results demonstrate a productive representation, not an escape from every
additive-measure obstruction.
The
[density review](../../../docs/project/reviews/review-2026-09-22-tokoharu-density-mathematics.md)
also separates the continuation driver’s import defect from the validity of the frozen
certificates.

### The negative results that still constrain a new idea

| Retained fact | What it excludes | What remains open |
| --- | --- | --- |
| The transported 88-core family obstructs unconditional additive measures at n11 from $L_*=38200/9977\approx3.82881$. | A pure point, segment or density cover cannot cross that ceiling merely by a finer discretization or a different additive representation. | Nonadditive charges, restrictions proved for physical packings, and multi-parent compatibility. |
| T-033 refines the same T-025 supports and weights. | Treating further refinement of that frozen family as the route past $3.875$. | Changed supports, features, parent domains or selection geometry. |
| At n17, deleting triples at fixed point weights gives an exact point-only counterexample; dropping the parent-centre restriction gives another. | Claims that those ingredients are decorative for that certificate. | Reoptimized point-only families, better threshold families and different domains. |
| Exp-222 gives an exact fixed-support, fixed-$(L,A)$ mass floor $33945829752/2000000005$. | More than $0.025163773\ldots$ of normalized mass improvement by changing only those weights at that same geometry. | New sites, new features, changed $A$, and joint geometry optimization. The quoted $+0.0034$ side estimate is a **heuristic**, not a theorem. |
| Corner-patch neutrality and the all-deep obstruction concern specified residual domains and point languages. | Closing those exact relaxations with more points alone. | Richer residual charges, actual parent footprints, different conditioning and valid selection rules. |
| T-031 excludes the all-free corner class at $3.84$. Fourteen mixed bin vectors form four D4 classes; the all-deep branch has a separate obstruction. | Presenting one excluded class, or the unfinished tree, as an unconditional bound. | A newly justified complete cover of cases at a stronger target. |
| Earlier global theta screens used finite families already cut by floor atoms; the global cell matrix was too large. | Repeating those screens as evidence for a useful new PSD method. | A localized continuum kernel, with a different comparison and a bounded certifier. |

The detailed scope is in [X-026](X-026-what-conditioning-does-and-does-not-buy.md),
[X-027](X-027-stromquist-fractional-and-structural-strategy.md),
[X-040](X-040-lower-bound-mechanisms-beyond-the-one-body-ceiling.md), and the
[exp-221](../series/series-000-smoke-and-calibration/results/agenda-041/exp-221-n17-kleddamag-unrestricted-receipt.md)
and
[exp-222](../series/series-000-smoke-and-calibration/results/agenda-041/exp-222-n17-repricing-receipt.md)
receipts. Their finite failures should stay finite failures.
In particular, a weak folded dual does not prove that no stronger obstruction exists.

## A Common Mathematical Interface

Fix a physical working container $K=[0,L]^2$ and parent side $A$; the target unit-square
side is $S=L/A$. Let $P$ denote a legal parent pose.
Choose a closed set $Q(P)\subset\operatorname{int}P$. It need not ultimately be a
square, although the existing certificates choose squares.
Distinct parents in a packing give disjoint selected sets.

A charge $q(Q)\ge0$ has budget $M$ if every such disjoint family satisfies

$$
\sum_i q(Q_i)\le M.
\tag{1}
$$

For a threshold feature $(F,k,w)$ with distinct sites $F$ and $w\ge0$,

$$
q_F(Q)=w\mathbf1_{\{|F\cap Q|\ge k\}},\qquad
M_F=w\lfloor |F|/k\rfloor.
$$

The existing proof establishes $q(Q(P))\ge\Gamma$ for every parent pose and uses
$n\Gamma>M$. A stronger method can improve the selectable charge, reduce the valid
budget, or improve the lower bound on the **sum over an entire packing**. The last
option does not require improving the worst individual charge.

All proposed inequalities below are stated in this working scale.
Rescaling only at the end avoids confusing $L$, $A$, the core side, and the actual lower
bound $L/A$. Increasing the target $S$ at fixed $L$ decreases $A$; it also enlarges the
legal centre domain.
Rechecking only core containment would miss the latter change.

## Direction A: Charge Deficits and Parent Compatibility

### A finite inequality with a complete geometric premise

Partition legal parent poses into classes $C_1,\ldots,C_r$. A cover is also usable if a
deterministic assignment gives each parent exactly one class.
Suppose the checker establishes

$$
P\in C_j\quad\Longrightarrow\quad q(Q(P))\ge\ell_j.
$$

Let $z_j$ be the number of parents assigned to class $j$. A physical packing induces an
integer vector $z\ge0$ with $\sum_jz_j=n$. Derive additional necessary inequalities from
actual parents: a class capacity, a clique of mutually conflicting classes, a proved
small-group exclusion, or an exact count premise.
Let $\mathcal R$ be any relaxation containing all induced count vectors.
Then

$$
\min_{z\in\mathcal R}\sum_j\ell_j z_j>M
\quad\Longrightarrow\quad
\text{no packing of }n\text{ parents exists}.
\tag{2}
$$

This follows directly from (1). Minimizing over a relaxation lowers the optimum, so a
certified lower bound above $M$ is sufficient.
A numerical optimum without a checked dual or integer proof is not sufficient.

An equivalent version is useful when most poses have a good baseline charge $g$. Put
$d_j=\max(0,g-\ell_j)$. If a proved relaxation supplies the **upper** bound

$$
\max_{z\in\mathcal R}\sum_jd_jz_j\le D,
$$

then every hypothetical packing has total charge at least $ng-D$. It is excluded when
$ng-D>M$. This form deliberately discards surplus above $g$; retaining several charge
bands in (2) can be stronger.

For example, if all parents have charge at least $g$, the good poses have at least
$g+\varepsilon$, and at most $r$ bad poses coexist, the total is at least

$$
ng+(n-r)\varepsilon.
\tag{3}
$$

Equations (2) and (3) identify a specific missing lemma: **how many low-charge parents
can coexist, with which deficits?** A small deficit occurring on a large angular
catalogue is harmless if its spatial realizations are incompatible.

### Why this changes the old structural question

Earlier corner conditioning often deleted one unit of fractional mass while reducing the
count by one. It therefore left exactly the same obstruction.
Here the partition is chosen where a successful certificate actually loses charge.
An incompatibility can remove combinations of weak placements without paying an
owner-count deduction.
The relation uses the full parents, so disjoint small cores that cannot be expanded
simultaneously do not defeat it.

This is related to the conditional demands in X-027 and the conflict methods in X-040.
The proposed change is the **certificate-guided residual domain**, together with a
checked composition inequality.
It is not a claim to have invented conflict graphs or conditional covering.

Several proof details determine whether it works:

* A region left unresolved by a box verifier stays in the bad-pose cover.
  It cannot be deleted because no sampled witness was found there.
* A single pose cell need not have capacity one.
  Prove within-cell overlap, give a valid larger capacity, or subdivide it.
  Graph vertices alone do not supply that fact.
* Parent-centre envelopes are supersets of the true orientation-dependent domains.
  They are safe for lower bounds.
  A witness in an envelope must be paired with an actually legal parent orientation
  before it can refute a geometric assertion.
* D4 invariance permits independent folding for a single-parent charge decision.
  It does **not** permit independently folding two parents before testing their relative
  positions. Expand the symmetry images or retain their group labels in joint tests.
* A low charge for one selected core is a valid conservative lower-bound issue.
  It does not prove that every core inside the same parent has low charge.
  Direction B can repair that issue before expensive compatibility work.

The cheapest sound conflict rule uses the inscribed discs of radius $A/2$. If two parent
centres are less than $A$ apart, their interiors overlap whatever their angles.
For two centre boxes, an upper bound below $A$ on all cross-distances proves a conflict;
for one box, diameter below $A$ proves capacity one.
Exact separating-axis bounds can then add orientation-dependent conflicts where the disc
test is inconclusive.

### A small diagnostic on the retained n17 witnesses

The retained exp-222 file contains one exactly clipped argmin centre per orientation
row. The following diagnostic used every row within $10^{-4}$ of the certified minimum,
including its eight container-symmetry images.
It did not sweep any new pose region.

| Diagnostic | Result |
| --- | ---: |
| Selected original rows | 26 |
| Distinct centres after D4 expansion | 208 |
| Exact inscribed-disc conflict edges | 4,180 |
| Cliques in a checked greedy partition | 13 |
| Runtime, one process | 1.818 seconds |

Every stored centre was checked against the legal centre domain at the row endpoint
having the smaller inset.
Every clique was independently checked by exact rational distance comparisons.
Thus at most 13 of these **208 particular centres** can be used simultaneously by
disjoint parents. No orientation-specific overlap test was needed.

This is a useful seed geometry: the certificate’s weakest sample placements are not 17
freely available slots.
It does **not** prove that at most 13 low-charge parents exist in a packing.
One centre per row omits almost every centre; the bad region can contain other
components; a new target changes that region; and the greedy cover is not an optimum.
The next discriminating step is a complete bad-pose cover, not a larger list of sampled
minima.

A follow-up checked how much these cliques can be enlarged.
Let $D^2$ be the largest squared centre distance within any of the 13 cliques.
At the source parent side $A=99853/100000$, the exact rational value of $A^2-D^2$ is
retained in the
[margin receipt](../../cases/w3_lower_bound_directions/weak-pose-graph-margins.json); it
is $0.0013894816999523445\ldots$ and is at least $1389481699/10^{12}$. Every centre may
therefore be enlarged to a Euclidean ball of radius

$$
\varepsilon=\frac{34788181}{200000000000}=0.000173940905.
$$

The union of the balls belonging to each clique still has capacity one, for parents of
arbitrary orientation.
Indeed, for $d\le D<A$, $A-d=(A^2-d^2)/(A+d)\ge(A^2-D^2)/(2A)$; the chosen
$\varepsilon\le(A^2-D^2)/(8A)$ makes $d+2\varepsilon<A$. Two centres in the same
individual ball also have distance below $A$. This supplies genuine neighbourhood
capacity statements, while still leaving almost all of the bad-pose cover unproved.

The same frozen clique partition **does not retain its disc proof at target $4.63$**.
With $L=4613/1000$ fixed, that target means $A'=4613/4630$, and
$A'^2-D^2=-0.0030026103001600784\ldots$. This is an informative failure of that
particular disc partition, not a counterexample to its capacity or to the target:
orientation-specific conflicts or a new partition could still work.
Both parent-side checks took 0.994 seconds together.
A target pilot must rebuild the geometry and the charge cover at its actual $A'$.

The retained code and exact receipt are
[innovation_probes.py](../../cases/w3_lower_bound_directions/innovation_probes.py) and
[weak-pose-graph.json](../../cases/w3_lower_bound_directions/weak-pose-graph.json).

### Smallest useful pilot and failure signal

Choose one prospective target, such as n11 at $3.876$ or n17 at $4.63$, and freeze a
transported charge system and a legal core selector for that target.
First emit a **complete** partition into certified charge bands and unresolved boxes.
Attempt a rational LP bound using only proved capacities and clique inequalities.
Large unresolved regions are a failed resolution attempt, not mathematical evidence
against the target.

A group of $r+1$ genuinely disjoint parents in a proposed bad-region capacity-$r$ class
refutes that capacity.
A feasible count vector surviving every admitted cut refutes the selected finite
relaxation as an exclusion proof; it need not be a packing.
A complete cover whose verified LP lower bound clears $M$ is the decisive positive.

The enabling instrument should retain the domain, symmetry labels, core selector, charge
interval, parent capacity and proof for each leaf.
A separate small checker should verify the cover and the rational count certificate.
This is a narrower instrument than a global n-parent solver, and its failed leaves
remain useful inputs to support discovery and geometric lemmas.

## Direction B: Design the Measure and the Selectable Geometry Together

### Centre-dependent core menus

The external catalogues choose a core from the parent’s orientation interval.
A parent usually contains other strict cores with slightly different centres,
orientations or shapes.
For a finite verified menu $Q_1(P),\ldots,Q_m(P)$, define

$$
G(P)=\max_{1\le a\le m}q(Q_a(P)).
$$

If $G(P)\ge\Gamma$ for every parent, select one maximizing core.
All selected cores from distinct parents are disjoint, so the original budget remains
valid. The menu can depend on a certified centre class as well as angle.
This turns a universal failure of one selector into an existential selection problem.

The crucial restriction is **one selected set per parent**. Adding the charges of
several overlapping candidate cores can count the same resource repeatedly.
Taking the charge of their union is sound if the charge is evaluated once on that union
and the union lies in the parent’s interior.
The union is then a new selected-set geometry, not several separately budgeted parents.

For an ordinary additive measure, any such charge is bounded by the measure of the
parent itself. This cannot evade the full-unit one-body ceiling.
Its promise here is to improve an already nonadditive threshold certificate and reduce
avoidable containment loss.

The smallest pilot takes an exact failed parent pose at a stronger target and searches
only a small rational menu of strict translations or alternative core directions.
An improved witness score is exploratory evidence.
A positive certificate requires a neighbourhood covered by the menu and eventually every
remaining parent pose.
If an independent upper bound on the best menu charge remains below demand at one legal
pose, that menu is refuted; merely failing to find a good core is inconclusive.

### A common inner body instead of a worst-case inscribed square

For an orientation interval $I$, let $P_u$ be the centred parent of side $A$. The
intersection

$$
K_I=\bigcap_{u\in I}P_u
$$

is the largest common inner body before imposing strictness.
The row’s inscribed square is a subset of it and can discard usable corner material.
A compact polygon contained strictly in $K_I$, or a union of verified rectangles inside
it, is another valid core.
For rational half-angle parameters, membership of a fixed rational point in every $P_u$
reduces to quadratic inequalities after clearing $1+u^2>0$. The native premise audit
already uses this algebra for square vertices.

This gives a concrete geometric extension: maximize the useful captured feature traces
over an inner polygon, rather than maximizing an orientation-independent square side.
The direct-count native verifier has a more suitable starting architecture than the
source’s signed rectangle expansion, although polygon membership bounds and a new
selector contract still have to be built.

The likely gain is limited when orientation intervals are already tiny.
That is a reason to measure the loss before building a general polygon engine.
A frozen-row comparison should separate the best selectable charge from the interval
count and from support movement.
It should retain a defeating parent when the geometry buys nothing.

### Support discovery driven by the actual dual obstruction

At n17, repricing the same 1,387 orbit variables on the same geometry has a rigorously
bounded remaining mass prize.
A more consequential producer must add new columns.
For a finite dual family of cores $Q_i$ with weights $y_i$, a proposed threshold feature
$(F,k)$ has reduced cost

$$
\lfloor|F|/k\rfloor-
\sum_i y_i\mathbf1_{\{|F\cap Q_i|\ge k\}}.
\tag{4}
$$

A negative value identifies a violated valid budget inequality.
Searching only for extra ordinary points finds only the $|F|=k=1$ cases of (4).

A new tool could synthesize features in two stages.
First enumerate the distinct site incidence patterns induced by the active dual
placements.
Then choose a small set of patterns and a threshold whose budget is violated;
generalized weighted features require their own valid capacity calculation.
Realize every token as a distinct exact rational point in its geometric cell.
Repeated incidence patterns are allowed only when that cell can supply the required
distinct sites; copying one site does not create new consumable tokens.
This separates the finite combinatorial search from coordinate realization.
Boundary patterns and all D4 images need explicit treatment; an unrealizable incidence
pattern is a rejected proposal.

The synthesis should retain several adversarial dual families and test the entire old
optimal dual face when claiming a finite improvement.
Cutting the one dual returned by the optimizer can leave another optimum untouched.
X-027 already proves that whole-face discriminator.
The new opportunity is to apply it to the richer external parent-core language and
synthesize support locations and feature types together.

At n17, an informative treatment would introduce both dispersed five-site patterns and
near-coincident patterns while allowing the control the same ordinary sites.
A three-of-five majority has capacity one; two-of-five has capacity two.
Comparing them with triples requires those actual budgets, not one unit per feature.
The full native coverage check must follow any finite LP gain.

**Candidate claim:** on a frozen common row set, newly realized five-site or weighted
features give an exact feasible covering budget below an exact control-dual lower bound.
That is a finite expressive gain.
Its stronger successor is a complete new certificate at the chosen side.
A treatment’s lower LP objective alone, before separation, is insufficient; exp-222’s
$16.776$ solution that required mass above 27 on a missed row is the relevant control
failure.

## Direction C: Stronger Resource Budgets and Continuous Integer Charges

### Geometry-aware groups of features

The sum of individual feature capacities can be loose.
For a small set of sites $V$ and a monotone trace charge $f(T)$, define

$$
\beta(V)=\max_{T_1,\ldots,T_r\text{ pairwise disjoint}}
\sum_i f(T_i).
\tag{5}
$$

This is a valid budget because traces of disjoint selected cores are disjoint.
Exact subset dynamic programming evaluates (5) for a small $V$. This general principle
and weighted/floor atoms already appear in
[X-027’s mechanism report](../../../docs/project/research/research-2026-09-10-x027-certificate-mechanisms.md#tighter-budgets-and-higher-rank-candidates).
The innovation to test is **geometric restriction of the allowed trace patterns** and
their use on the new external supports.

Let $\mathcal T$ be a checked superset of every trace realizable by a legal selected set
on $V$. In (5), allow only $T_i\in\mathcal T$. The resulting maximum is still an upper
budget, and can be smaller than the unrestricted token maximum.
Unused sites must be allowed; a convenient recurrence includes a skip-site branch as
well as the allowed nonempty traces.
A coarse safe restriction is that a captured subset cannot contain two points farther
apart than a parent diagonal $A\sqrt2$. Stronger restrictions can come from exact
common-containment decisions on a small site group.

This captures more geometry than $\lfloor m/k\rfloor$ while keeping the difficult proof
local. It does not require certifying the whole n-parent packing problem.
It also exposes the limit: proving that two traces can occur separately does not prove
that their parents can coexist.
Ignoring that latter compatibility enlarges the budget problem and remains safe, at the
possible cost of missing a saving.

There is a useful obstruction to a simpler version.
If every grouped atom is nonzero, Boolean, monotone and has capacity one, putting all
sites into one abstract block activates every atom.
Thus its token-only joint maximum equals the sum of its capacities.
Shared sites alone cannot improve that budget.
To improve it, use a capacity-above-one feature, a different charge profile, or geometry
that rules out the all-sites block and other saturating partitions.

The small n11 spike checked one representative of each of the 10 positive two-of-five
orbits, at most 32 neighbouring features per representative, and unions of at most eight
sites. It found four eligible distinct unions.
Exact subset dynamic programming gave **zero budget saving in all four**. Controls
established the five-token floor saving $(2\text{-of-}5)+(4\text{-of-}5)$, whose joint
budget is 2 against separate budget 3, and the no-saving
$(2\text{-of-}5)+(3\text{-of-}5)$ comparison, whose joint budget is 3. The run took
0.0415 seconds.

This bounded negative argues against expecting free improvement from merely regrouping
the present overlapping tokens.
It says nothing about larger groups, moved supports, new weighted features or
geometry-aware budgets.
The exact scope and partitions are retained in
[token-groups.json](../../cases/w3_lower_bound_directions/token-groups.json).

### Nonlinear charges on continuous density reservoirs

Tokoharu supplies exact total mass and rigorous lower bounds on rectangle-density
intersections. Combine that primitive with integer rounding.
Let $\nu_j$ be a finite nonnegative absolutely continuous measure, let $t_j>0$, and
define

$$
f_j(P)=\left\lfloor\frac{\nu_j(P)}{t_j}\right\rfloor,
\qquad
b_j=\left\lfloor\frac{\nu_j(K)}{t_j}\right\rfloor.
$$

For physical parents with disjoint interiors, their boundary intersections have
$\nu_j$-measure zero.
Consequently

$$
\sum_i f_j(P_i)
\le\left\lfloor\frac{\sum_i\nu_j(P_i)}{t_j}\right\rfloor
\le b_j.
\tag{6}
$$

Nonnegative weighted combinations have a valid global budget.
A binary version $\mathbf1_{\{\nu_j(P)\ge t_j\}}$ has the same budget.
These are continuous counterparts of token and floor resources, but the parents
themselves can be evaluated: there is no site mass on a shared boundary and no
strict-core shrink needed for the resource argument.

The proposed advantage has two parts.
Rectangle bases offer geometric flexibility and area-based search signals; the floor
retains indivisible global budgets that plain densities lack.
Multiple reservoirs can cover different placement profiles, with total charge above one
on some poses and zero on others.
No claim is made that merely smoothing a point certificate preserves its coverage.

One simple version cannot help: a single reservoir whose binary charge must be one on
every parent already satisfies $\nu(P)\ge t$ everywhere.
If its budget is below $n$, then $\nu(K)/t<n$, so it is an ordinary additive cover.
It inherits the one-body obstruction.
Any advantage must come from a combination of nonlinear profiles or from additional
geometric restrictions, not from calling one density a reservoir.

A controlled first test needs only a small rectangle basis and a fixed finite set of
adversarial poses. Compare ordinary density columns against floor-resource columns on
that **same** geometry.
A strict rational primal/dual separation would establish a finite profile advantage.
Failure on a few rectangles rejects that basis only.
Before any global run, the checker must validate exact reservoir masses, positive
thresholds, floor arithmetic and complete coverage.
A rigorous lower integral bound can be rounded down safely; uncertainty at a threshold
can cause refusal but must never be rounded up into a pass.

This route extends, rather than supersedes, the existing weighted and iterated-floor
ideas. It combines a newly available integration primitive with a different budget
language. No occurrence of this particular floor-density construction was found in the
bounded local search of the campaign explorations and mechanism reports; that is not a
literature novelty claim.

## Direction D: Convert a Global Certificate Into a Capture Theorem

At n11, a much more valuable outcome than another rational rung would be a proof that
every feasible packing at or below Trump’s side lies in one of the already understood
local charts. The retained local result gives a concrete endpoint for that effort.

The [quantitative Trump theorem](../../../packing/cases/trump11/isolation-theorem.md)
states a labelled, anchored sup-norm radius of at least

$$
\rho=\frac{808514697}{200000000000}\approx0.004042573485,
$$

with angles measured in radians in the specified chart.
A packing at side at most $U_{11}$ inside that ball must be exactly the retained Trump
pose and therefore has side $U_{11}$. The case file registers only the qualitative local
theorem. It records BC-241’s source-distinct acceptance of the quantitative packet at
retained-record-dependent scope, without an independent radius-generator replay; the
closure disposition remains pending.
Thus this radius is a proposed dependency for the capture route, not a newly confirmed
result of this W3 block.
Any new proof invoking it must discharge that dependency explicitly.

The missing global statement is

$$
\text{every feasible n11 packing in }[0,U_{11}]^2
\text{ lies in a relabelled D4 image of the admitted local ball.}
\tag{7}
$$

Together with the local theorem, (7) proves optimality.
It does not follow from repeatedly finding the Trump packing, from first-order rigidity,
or from a lower bound numerically close to $U_{11}$.

Direction A suggests a path to (7): exclude all charge/count regions outside a union of
candidate structural neighbourhoods, refine the surviving parent-compatibility patterns,
and prove that the only complete patterns match the Trump chart.
A small subset of forced relations may be enough: several occupied slots, ordering
constraints, or a pair of incompatible tilted centres can reduce the remaining variables
before local interval geometry is invoked.

At the exact side $U_{11}$, the known packing exists.
A global strict charge contradiction is impossible there.
The argument must allow the equality case and classify its realizations, or exclude only
the complement of the local balls.
This changes the certificate objective from uniform exclusion to **capture plus local
rigidity**.

The first pilot should not attempt 33-dimensional global subdivision.
Select one putative surviving coarse configuration pattern and ask whether the complete
pattern either enters the local chart or is excluded by exact parent geometry.
A surviving pattern far from the chart is information about missing global constraints,
not a counterexample to Trump’s optimality unless its entire packing is validated.

At n17, the retained Bidwell transcription has sliding squares.
A one-pose isolation argument is therefore the wrong endpoint.
A counterpart would need a neighbourhood of a feasible component, with rattler motions
separated from transverse directions and a proved side lower bound throughout.
That additional work makes exact closure a less immediate goal at n17 than at n11.

General-purpose rigorous optimization remains an alternative but has a demanding
calibration. Montanher, Neumaier and Markót’s
[rotating-square study](https://optimization-online.org/wp-content/uploads/2018/04/6556.pdf)
uses tiling and lower-order subproblems to overcome symmetry, and demonstrates the
method for three squares in a circle.
Its successful reduction is a reason to build local exclusion motifs; it is not evidence
that an unrestricted n11 search is cheap.

## Direction E: A Continuum Kernel on the Difficult Poses

A positive-semidefinite kernel gives another way to express incompatibility without a
large discrete adjacency matrix.
Let $V$ be a specified set of legal parent poses and let $F:V\times V\to\mathbb R$ be a
symmetric positive-semidefinite kernel.
Suppose

$$
F(p,p)\le b,
\qquad
F(p,q)\le-1
\quad\text{whenever }p,q\in V\text{ are distinct compatible parents}.
$$

For a compatible $r$-tuple,

$$
0\le\sum_{i,j}F(p_i,p_j)
\le rb-r(r-1),
$$

so $r\le b+1$. This elementary kernel certificate can bound occupancy of a bad-pose
region in Direction A. It need not exclude all n parents by itself.

The broader framework is established mathematics: de Laat and Vallentin model packing as
independence in topological packing graphs and give a convergent semidefinite hierarchy.
Their revised paper is [arXiv:1311.3789v3](https://arxiv.org/abs/1311.3789v3), which
notes a correction to an earlier proof.
The proposal here is the localized, certificate-guided application, not a new hierarchy
theorem.

A finite feature representation

$$
F(p,q)=\phi(p)^TQ\phi(q),\qquad Q\succeq0,
$$

admits an exact rational $LDL^T$ positivity check.
Features can use absolute centre coordinates, rationalized orientation and functions of
the boundary. Verifying the diagonal and compatible-pair inequalities is still a
continuum problem. With rational half-angles, denominators are positive and the
conditions can be reduced to polynomial inequalities on each separating-axis branch.
A floating SDP solver can propose $Q$; it cannot certify those inequalities by itself.

Localization is the essential experiment.
A global pose-cell theta matrix inherits the size problem found in X-040. A kernel on a
few small weak-pose components has fewer features and smaller domains for the
six-variable pair inequalities.
It should first compete against the cheap clique/count bound on exactly the same domain.
If it does not improve that bound with a rational verified certificate, it has not
earned a general solver or a global application.

A translation-invariant infinite-plane bound is poorly matched to finite square
containers: squares tile the plane with density one.
Boundary information has to enter.
The motion-group technique of de Oliveira Filho and Vallentin concerns congruent-body
packing density and combines harmonic analysis, SDP and sums of squares; its
[paper](https://arxiv.org/abs/1308.4893v3) supplies an adjacent method, not a ready
finite-container square bound.

The falsifier for one frozen kernel family is an exact compatible pair violating its
claimed sign, a failed PSD proof, or a verified optimum no stronger than the simpler
count relaxation. Failure at a fixed degree does not refute all kernel methods.

## Direction F: Learn Small Geometric Exclusions That Transfer

A reusable structural tool could search for **minimal incompatible groups of parent pose
regions**. Each group would carry a complete local proof that no parent can be chosen
from every region simultaneously.
The group becomes a no-good inequality in the count problem, such as $z_a+z_b+z_c\le2$
for three capacity-one classes.

Pairwise compatibility does not imply joint compatibility.
Three parent regions can each have a compatible pair realization while admitting no
common triple realization.
Such a local exclusion is stronger than graph edges and can matter precisely when a
clique relaxation stalls.
It is also a concrete role for a small interval, exact semialgebraic, or proof-producing
SAT/SMT kernel: verify one three- or four-parent statement, then reuse the verified
inequality.

The prototype should start from a count-relaxation solution that survives all pair
constraints, select a small group actually used by that solution, and attempt a complete
joint check. A failed numerical realization is not an exclusion.
A validated compatible tuple defeats that proposed no-good and becomes a control.
A timeout retains the tuple as unresolved.

Transfer across n should mean transfer of such a lemma or instrument under explicitly
preserved geometry. A local exclusion in a fixed rectangle or corner patch can apply
inside both n11 and n17 containers if its size, orientation and boundary hypotheses
match. An n26 density bound does not automatically give a stronger n17 bound:
monotonicity transfers a lower bound to larger counts, not smaller ones.
Deleting squares from a large packing gives upper constructions, not lower exclusions.

Classical wall or line counts can supply useful constraints only when their precise
domains are proved. Earlier work already refuted the convenient four-wall stressed
component claim, several wall-count guesses, and the proposed n32 one-spare lemma at its
stated geometry. A new local theorem should be selected because it cuts a currently
surviving pattern, then tested on the retained known-best poses and old counterexamples.

## Other Ideas Worth Preserving

These alternatives are less developed than A–F. Keeping them explicit prevents both
premature dismissal and silent promotion into an experiment queue.

| Idea | Possible use | First obstruction or discriminating question |
| --- | --- | --- |
| Equality-aware charge design near Trump | Arrange that charge/resource equality forces a small set of contact or occupancy patterns, supporting (7). | Can the known Trump pose saturate the proposed inequalities exactly while a known alternative partial packing has positive slack? An approximate equality picture is not a capture theorem. |
| Counterexample-trained structural lemma search | Mine a surviving fractional family for a small geometric relation absent from the relaxation. | A new inequality must cut more than one chosen dual and have a complete geometric proof; merely changing the displayed optimizer is insufficient. |
| Higher-rank or weighted floor resources | Use the existing integer-resource closure on features that defeat the new, stronger adversaries. | X-027 already proposed these. Demonstrate a strict common-matrix advantage and actual geometric traces before building a broad hierarchy. |
| Exact parent-interior point evaluation | Avoid square-core shrink by counting only sites strictly inside the actual parent. | Generic open cells no longer settle boundary poses automatically; the event boundaries must be checked explicitly. The additive one-body cap still applies to point-only charges. |
| Several complementary certificates | Use a vector of resource charges and an integer feasibility test on achievable charge profiles. | Any purely nonnegative linear recombination is already one larger covering LP. A gain requires count integrality or compatibility, not choosing whichever certificate looks best per square with an unjustified budget. |
| Adaptive angular/centre resolution by proof difficulty | Spend fine cells only at charge changes and ambiguous pair conflicts. | Fewer boxes or a faster proof is a tool improvement unless the saved capacity enables a stronger certificate. It must keep unresolved cells in the domain. |
| Small-region capacity bounds from inscribed discs | Import exact centre-separation constraints cheaply before square-specific geometry. | Disc bounds forget orientations and can be too weak. They are most useful for tight clusters, as in the finite n17 spike, rather than a global replacement for square geometry. |
| Two-dimensional slicing and boundary waste | Derive integer occupancy or incompatibility, possibly conditional on tilt bands. | A purely additive area or boundary measure remains subject to the one-body obstruction. Earlier counterexamples rule out convenient uniform wall counts. |
| Robust polynomial identities for selected local configurations | Replace an expensive local box proof with an exact sum-of-squares or elimination certificate. | First specify the complete disjunction of separation branches and preserve zero multipliers, ties and rattlers. A stationary subsystem alone is incomplete. |

## Preliminary Comparison of Promise

These judgments compare the next pieces of information, not forecasted bound gains or
runtime claims. The two diagnostics do not justify a full allocation by themselves.

| Direction | Preliminary promise | Why | What could change that judgment |
| --- | --- | --- | --- |
| A: certificate-guided compatibility | Strongest new proof architecture to investigate | Uses the successful charge system and adds the physical relation it forgets; the n17 witness clusters give a concrete small pilot. | A complete bad-pose cover may be diffuse or have large unavoidable multiplicities, leaving the count relaxation weak. |
| B: joint support/feature/selector discovery | Strongest candidate for a nearer numerical advance, especially n17 | Fixed-support repricing has limited mass headroom; n11 demonstrates that a richer combination can work. | Exact common-row comparisons may show no gain from five-site patterns or menus; full separation may erase finite gains. |
| C: continuous integer resources and geometric budgets | Attractive method-development branch | A new synthesis of available area integration with nonadditive budgets; can use actual parents without point-boundary ambiguity. | Few basis reservoirs may have no finite advantage, or floor seams may make complete coverage too costly. |
| D: capture plus local rigidity | Largest mathematical payoff at n11, with the largest global obligation | The local endpoint is already concrete, and A can expose which global patterns remain. | Surviving patterns may stay far from every admitted chart; the quantitative local dependency may need further confirmation. |
| E: localized continuum kernels | Speculative, worth a narrow comparison only | Adds correlations without a huge cell matrix and can feed A. | Low-degree kernels may fail even on a complete small residual domain or be harder to certify than local no-goods. |
| F: small higher-order geometric exclusions | Useful companion to A and B | Converts actual surviving pair-compatible patterns into reusable stronger constraints. | The important groups may be large, or local CSP costs may already exceed the information gained. |

For n11, I would compare A with B’s core-selection and support repairs before choosing
an exact-closure campaign.
For n17, I would compare new five-site/support columns with A’s complete weak-pose
geometry. C is the most distinct new representation to test in a deliberately small
pilot. Those are discussion priorities, not an execution order.

## Candidate Hypotheses for Codification

Each row requires the coordinator to freeze the target, input family and instrument
before execution. Targets listed below are illustrative design choices, not promised
outcomes. An instrument that does not yet exist leaves the candidate blocked.

| Local label | Testable claim and assumptions | Acceptance signal | Rejection or informative negative |
| --- | --- | --- | --- |
| A1 | At a chosen stronger side, a complete parent-pose cover with frozen charge bounds and proved capacities makes (2) exceed the exact budget. | Checked cover plus a rational count-LP dual or checked integer proof, then independent composition review. | A checked surviving count vector refutes that relaxation; unresolved cover leaves give no verdict. |
| A2 | A specified low-charge domain has occupancy at most $r<n$, using only a declared family of disc/clique inequalities. | Complete domain cover, capacity-one or explicit multiplicity proofs, and a checked clique/count certificate. | $r+1$ validated compatible parents in the domain refute the capacity; failure of a sampled graph does not decide it. |
| B1 | A finite centre-dependent core menu improves the verified worst selected charge on one frozen parent box without changing the resource budget. | A complete max-over-menu lower bound strictly above the old selector’s exact upper witness value. | An exact upper bound on every menu choice at a legal pose fails demand; a search miss is undecided. |
| B2 | A specified polygon or rectangle-union core improves a row’s complete coverage enough to preserve demand at a smaller parent side. | Strict containment for the full row, complete centre coverage and exact budget arithmetic. | A legal parent witness defeats every declared core choice, or the geometric improvement is too small at that target. |
| B3 | New geometrically realized five-site or weighted columns strictly improve a frozen n17 common-row covering problem. | A treatment primal budget below a control dual bound, both rationally checked; sites available to both controls as specified. | A surviving old optimal dual proves no finite gain from those columns. Global coverage remains a separate successor. |
| B4 | The new B3 producer plus complete row separation yields a certificate at a frozen n17 target, for example $4.63$. | Complete coverage, parent geometry and budget decision on frozen bytes. | An exact defeating pose refutes those bytes. A timeout is not a language-wide negative. |
| C1 | One specified geometry-aware trace group has exact capacity below its sum of individual capacities. | A complete allowed-trace superset, exact partition-capacity upper certificate, and a strict integer saving. | A saturating realizable disjoint tuple refutes the saving; a saturating abstract partition can refute only the selected relaxation. |
| C2 | A frozen rectangle-reservoir floor basis gives a strict finite advantage over the corresponding additive basis on the same pose set. | Exact primal/dual separation with masses and rounding checked. | A feasible old optimal dual surviving every reservoir column proves a finite tie. |
| C3 | A C2 candidate covers all legal actual parents at the target with budget below total required charge. | Complete area/floor coverage and a boundary-null budget proof. | A rigorously undercharged parent refutes the candidate; interval seam refusal is unresolved. |
| D1 | A declared coarse n11 configuration class at $U_{11}$ is either impossible or wholly captured by admitted Trump neighbourhoods. | Complete class proof, explicit relabelling/symmetry assignment and verified neighbourhood radii. | A verified feasible configuration outside those neighbourhoods refutes capture for that class. A surviving box only leaves it open. |
| E1 | A fixed low-degree kernel on a complete residual pose domain proves a smaller occupancy bound than the frozen clique/count control. | Rational PSD proof and complete diagonal/compatible-pair inequalities. | An exact violating pair or a verified family optimum no stronger than the control rejects this family. |
| F1 | A selected pair-compatible triple or quadruple of parent regions is jointly infeasible. | Complete local geometric exclusion with every separation branch accounted for. | A validated compatible tuple refutes that no-good. A solver’s unsuccessful search is not acceptance. |

The overlap with earlier H-items is substantial and should be recorded, not hidden.
B1 continues H-095/H-097’s adaptive and existential selection questions with the
external parent-core contract.
B3 continues H-094 and the weighted/floor work from X-027 on stronger contemporary
adversaries. A continues H-118/H-119/H-124 and the conditional-profile ideas, but
proposes a complete residual-charge interface.
D continues H-103’s global capture obligation.
E is a redesigned, localized successor to H-231, not a reopening of its rejected finite
screen. C2/C3 are the most distinct representation proposals in this block.
The old n11 targets below $3.875$ remain controls or method questions; they are no
longer global improvement targets.

## Instruments That Would Make the Ideas Testable

Several ideas share a small number of useful tools.
Building one general research framework before testing its first consumer would reverse
that dependency.

| Instrument | First consumer | Minimum retained output | Trust boundary |
| --- | --- | --- | --- |
| Complete residual-pose exporter | A1/A2 | Covered parent boxes, core selector, rational charge lower bounds, symmetry labels, unresolved leaves and proof provenance. | Must account for the entire legal parent domain; a list of minimizers is insufficient. |
| Parent compatibility and capacity checker | A2/F1 | Exact disc conflicts, certified separating-axis conflicts, within-cell capacities and small-group exclusions. | Uncertain pairs remain compatible; uncertain groups remain possible. |
| Count-certificate checker | A1 | Rational LP dual or explicit finite integer proof over the admitted count constraints. | A solver success string is not evidence; verify the final arithmetic and constraint provenance. |
| Joint row/feature oracle | B3/B4 | Exact site-pattern realizations, selected feature columns, dual violations, replacement duals and all newly separated rows. | Finite LP advantage and global covering acceptance remain separate verdicts. |
| Inner-set menu checker | B1/B2 | Complete parent-box-to-menu coverage and strict inclusion for every selected set. | The charge is evaluated once per parent, with one shared resource budget. |
| Small trace-capacity checker | C1 | Allowed-trace superset and exact subset recurrence or certificate. | A missing realizable trace invalidates the budget; admitting an impossible one only weakens it. |
| Area-reservoir floor checker | C2/C3 | Exact total masses and thresholds, interval integral bounds, floor counts and complete domain coverage. | The published density driver is not an admission oracle; its import defect must not be inherited. |
| Local continuum kernel checker | E1 | Rational factorization plus checked polynomial/interval inequalities on every compatibility branch. | Finite samples never establish kernel sign over a continuum. |

The completed native n11 proof provides a useful base for the first and fifth rows:
direct feature counts, memory-bounded batching and the exact adaptive parent contract
now have an executed control.
It does not automatically provide a proof-tree exporter, a new optimizer, polygon
support or a complete n17 run.
Those are separate pieces of work to scope only when a candidate needs them.

## Spike Record and Evidence Limits

Both spikes were declared before execution: one worker, standard-library Python,
30-second ceiling per spike, no coverage sweeps, no changed certificate bytes and no
production-code edits.
They used project Python 3.14.7. The retained script has an explicit interpreter guard,
refuses output overwrite and records input digests and commands.
Its exact controls test the mathematical recurrence rather than a mirrored
implementation assertion.

The commands below use the current W3 review paths.
The receipts retain the actual original invocation paths.
Reproduction needs fresh output paths because the tool refuses to overwrite evidence.
Run from the repository root:

```bash
packing/.venv/bin/python3 packing/cases/w3_lower_bound_directions/innovation_probes.py \
  token-groups \
  --source packing/resources/web/external-square-certificates-2026-09-22/kleddamag-11/global-certificate.json \
  --output /private/tmp/w3-token-groups-fresh.json \
  --seconds 30

packing/.venv/bin/python3 packing/cases/w3_lower_bound_directions/innovation_probes.py \
  weak-pose-graph \
  --source packing/resources/web/n17-kleddamag-certified-bound-2026-09-21/kleddamag-17-squares-certified-bound/global-certificate.json \
  --cells packing/campaign/series/series-000-smoke-and-calibration/results/agenda-041/exp-222-n17-repricing-cells.jsonl \
  --output /private/tmp/w3-weak-pose-graph-fresh.json \
  --seconds 30
```

The follow-up repeated the second command with output `weak-pose-graph-margins.json` and
`--target-side 463/100`. It added the exact within-clique distance margin and the
neighbourhood calculation, without changing the selected centres or rebuilding the graph
at the proposed target.

Their digests bind the diagnostic inputs, not a claim of independent global replay.
The n11 certificate digest is the one given above.
The n17 certificate digest is
`0288aaac680131aa675adb63ea6a67e3d363fcca6061d4c788301da7c5d69cec`; the argmin file
digest is `fa7e40e66844f11250518c4c3b22e4ea2acb8b622951066668f30248bb9cbef3`. The
commands and output paths must be moved together into a durable result directory when
the coordinator integrates this report; the temporary links identify the current review
artifacts.

The paper lookups were bounded primary-source checks for the proposed kernel and local
optimization architectures.
They do not establish that nobody has used the proposed combinations before.
The algebra in (2), (3), (5), (6) and the elementary kernel bound is derived here or
explicitly attributed to the earlier mechanism report.
The existence of a useful certificate in any of those languages is conjectural.

The next decision is which uncertainty to resolve: whether the weak-pose remainder is
geometrically small, whether new support/feature columns outperform the current n17
family, or whether continuous integer resources add useful expressive power.
Each has a different, bounded pilot and a result that would justify or reject further
work.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
