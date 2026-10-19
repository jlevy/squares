# Review Addendum: The Ceiling Lemma, the `+0.006` Cap and H-248 in the Post-4.640020 Plan

Reviewed 2026-09-27, read-only, by a Fable max sub-agent acting as the mathematical
reviewer, on the branch `claude/happy-hawking-br4fwg`. The object is three claims the
[post-4.640020 plan](../specs/archive/plan-2026-09-27-after-4640020-overnight.md) flags
as unsure, all resting on the
[4.640020 review](review-2026-09-27-n17-kleddamag-4640020.md) and on Kleddamag’s v1.1.0
certificate, re-read here from the clone at `13821ddfa241`. It is evidence for the
coordinator, not a verdict of record: no bound moves by writing it, and the plan itself
is not edited here.

**In one line:** the clique-weighted ceiling lemma is correct as the plan states it,
coefficient thresholds and winning-subset rules included, and the clique condition is
the exact one the atoms control, since firing cores pairwise meet but need not share a
point; the $+0.006$ side cap is not first-order in anything measured and the ledger
counts under it are misread; H-248 is posed correctly, but the anneal’s triangle count
at fixed $N = 34$ is a surrogate for its metric, not the metric.

## 1. What Was Reviewed

The plan’s section “n = 17: the certificate’s shape, its saturation, and the ceiling”,
H-248 and H-243 under `packing/campaign/hypotheses/`, ideas 248, 249, 256 and 257, §3,
§8 and F4–F5 of the 4.640020 review, the clique tools
`packing/devtools/check_weighted_clique_certificate.py` and
`packing/devtools/geometric_graph_certificate.py`, and, from the clone,
`bounds/4.640020/METHOD.md` and the publication ledger.
The plan’s probes under `attic/planning-160/` are not on this checkout, so the anneal’s
numbers are read as reported and not replayed.

Scratch instruments live at `/tmp/claude-0/review-plan/`: `elastic.py` and
`elastic2.py`, which re-run the 4.640020 review’s independent sweep (`isweep.py`) at a
perturbed parent side with the certificate’s own weights, about 4 s a row; and an inline
recount of the ledger.
About four CPU-minutes in all.

## 2. Verdicts

| Claim | Verdict |
| --- | --- |
| (1) Clique-weighted lemma for points, floor-one coefficient thresholds and pairwise-intersecting winning-subset rules; $\alpha^{\ast}(G_F) \ge 17$ refutes every such certificate at that side and below | **Correct.** The condition is $y(K) \le 1$ on every clique of the interior-overlap graph; it cannot be relaxed to sets sharing a common point (§3) |
| (2) Reweighting caps near $4.646$, $+0.006$ at first order from the $1.27\times10^{-3}$ ledger slack | **Not established.** The number is $S \times 1.27\times10^{-3}$; no derivative of charge against side is measured, the fixed-weight response is a jump, and the row counts are misread (§4) |
| (3) H-248 correctly posed; anneal readings | **Posed correctly.** The anneal minimises triangles at $N = 34$, a special case; its $\alpha^{\ast} = 16$ restates the triangle count and says nothing about families of other sizes (§5) |

## 3. The Clique-Weighted Lemma

**Setting.** A certificate at side `S` has sites in the container, rules $R$ each with a
monotone winning predicate on its site tuple and a weight $w_R \ge 0$, budget
`M = Σ_R w_R·cap(R)`, and a sweep proving $F(Q) \ge \Gamma$ for the core $Q$ of every
legal parent, where `F(Q) = Σ_R w_R·[R fires on Q]` and every core lies strictly inside
its parent. The architecture in question is the one where every rule has capacity one.

**Lemma.** Let $P_1,\ldots,P_N$ be legal unit squares in $[0,S]^2$, $G$ their
interior-overlap graph, and $y \ge 0$ with $y(K) \le 1$ on every clique $K$ of $G$. Then
$\Gamma\cdot\Sigma y_i \le M$ for every capacity-one certificate at side `S`, so
$\Sigma y_i \ge 17$ refutes them all, and all at any larger side.

**Proof.** For a rule $R$, let $T_R$ be the set of $i$ such that $R$ fires on $Q_i$. Two
firing cores capture winning subsets $W_i \subseteq Q_i$ and $W_j \subseteq Q_j$;
capacity one means every two winning subsets meet (F4 of the 4.640020 review: for a
weighted threshold with $\lfloor\Sigma a_k/k\rfloor = 1$ two disjoint winning subsets
would carry coefficient at least $2k > \Sigma a_k$; for a listed family the masks
pairwise intersect by the checked predicate), so a site lies in
`Qᵢ ∩ Qⱼ ⊂ int Pᵢ ∩ int Pⱼ`, and $T_R$ is a clique of $G$. Then
$\Sigma_i y_i F(Q_i) = \Sigma_R w_R\cdot y(T_R) \le \Sigma_R w_R = M$, while
$\Sigma_i y_i F(Q_i) \ge \Gamma\cdot\Sigma y_i$. A valid certificate has
$M/\Gamma < 17$. A family in $[0,S]^2$ is a family in `[0,S']²` for `S' ≥ S` with the
same graph, which gives the monotonicity; the triangle-free family of 34 with
$y = \tfrac{1}{2}$ and the `K_{ω+1}`-free family of $17\omega$ with $y = 1/\omega$ are
the uniform cases. ∎

This is the plan’s statement, and the review’s §8 proof already carries it: the only
fact used about a rule is that its firing cores pairwise share a site.

**Which notion the atoms control.** The firing set of one rule is pairwise meeting and
not, in general, a family with a common point.
A two-of-three rule on sites $a, b, c$ fires on three cores capturing
$\lbrace a,b\rbrace$, $\lbrace b,c\rbrace$ and $\lbrace a,c\rbrace$, and three unit
squares that pairwise meet can have empty common intersection: centre three unit squares
on the side midpoints of an equilateral triangle of side $1.8$, each aligned with its
side. Any point has signed inward distances to the three sides summing to the height
$1.559$, so at most two of them are within $0.5$ of a side and no point lies in all
three squares; a $600 \times 600$ grid finds each pair meeting on a region of about
$14{,}000$ cells and the triple empty, and one site in each pairwise region makes a
two-of-three rule fire on all three (`/tmp/claude-0/review-plan/`, inline).
So the constraint must be imposed on cliques.
Weighting only the sets that share a point (the Helly-type notion) would admit
$y = \tfrac{1}{2}$ on those three cores, $y(T_R) = 3/2$, and the inequality above fails.
Imposing the constraint on the cliques of the *conservative* graph that
`geometric_graph_certificate` produces (an edge unless an exact separating axis proves
the interiors disjoint) is stronger still and therefore sufficient, which is what
H-248’s metric does.
The graph must be the interior-overlap graph: parents touching along an edge cannot
share a core point, and the tool’s “projection equality proves interior disjointness” is
the right reading.

Two small precisions for the plan’s wording.
The ceiling, the supremum of sides at which a capacity-one certificate exists, is
attained at $4.640020$ and bounded by $s(17)$, so the interval is $[4.640020, s(17)]$,
inside $[4.640020, 4.67553]$, not an open one.
And “every certificate of this architecture” means: all rules of capacity one, cores
strictly inside parents, $\Gamma$ certified over every legal parent; a rule of capacity
two or more is outside the lemma, since a firing set with matching number two need not
be a union of two cliques.

## 4. The `+0.006` Side Cap

**How the plan derives it.** From the ledger slack: the plateau $1{,}000{,}000{,}031$
against $\Gamma = 998{,}727{,}933$ is a relative $1.2721\times10^{-3}$, and
$4.640020 \times 1.2721\times10^{-3} = 0.0059$. Nothing else enters.
The previous plan converted R052’s $1.4\times10^{-3}$ slack to $+0.0014$, a factor `S`
smaller, so the two plans use different unstated conversions.

**The counts are misread.** The independent ledger (equal to the shipped one on every
row) has $895$ rows at exactly $1{,}000{,}000{,}031$, not $1{,}983$; $1{,}683$ within
$10^{-6}$ of it, $1{,}901$ within $10^{-4}$, $2{,}014$ within $10^{-3}$; $698$ rows
above it, the highest $1{,}000{,}000{,}152$. The $65$ rows within $10^{-3}$ of $\Gamma$
are all the plan’s “65 rows that dip to $\Gamma$”; exactly one row, $1207$, is at
$\Gamma$, $18$ are within $10^{-4}$ of it, and $1{,}983$ is simply $2{,}048 - 65$.

**What the slack does bound.** METHOD.md says the integer weights are rounded upward at
scale $10^9$, and $895$ rows at exactly $1 + 31$ units is what an LP with the constraint
“charge at least one” looks like after rounding.
If that LP minimised $M$ to optimality over a subset of the cells at a side no larger
than $4.640020$, then the full LP at $4.640020$ has more constraints and a value at
least $16{,}978{,}369{,}232$, so any reweighting of this dictionary at this side has
`17Γ'/M' ≤ 17×10⁹/16,978,369,232 = 1.001274`, against the certificate’s $1.0000003$.
That is the correct form of “at most to the plateau”, and it is conditional on an
unpublished LP having been optimal.

**What it does not bound.** The side.
Turning a charge ratio into a side needs `d(17Γ/M)/dS` for the *re-optimised* LP, and
the plan measures nothing of the kind; the $+0.006$ assumes charge and side trade one
for one. The fixed-weight response, which is the only thing measurable from the
certificate, is not first-order at all: with the certificate’s own weights, cores and
envelope re-derived at side $4.640020 + \Delta S$,

| Row | $\Delta S = 0.0005$ | $0.001$ | $0.003$ | $0.006$ |
| --- | ---: | ---: | ---: | ---: |
| 1207, binding | $0$ | $-1.9\times10^{-3}$ | $-1.7\times10^{-2}$ | $-1.8\times10^{-2}$ |
| 547, next block | $-1.5\times10^{-3}$ | $-1.5\times10^{-3}$ | $-5.3\times10^{-3}$ | $-1.3\times10^{-2}$ |
| 0, plateau, near $\theta = 0$ | $-6.5\times10^{-2}$ | $-1.2\times10^{-1}$ | $-2.5\times10^{-1}$ | $-7.4\times10^{-1}$ |
| 1000, plateau | $-7\times10^{-6}$ | $-1.9\times10^{-4}$ | $-1.4\times10^{-2}$ | $-1.4\times10^{-2}$ |
| 1500, plateau | $-3.4\times10^{-4}$ | $-7.7\times10^{-4}$ | $-1.2\times10^{-2}$ | $-3.4\times10^{-2}$ |

(relative change of the row minimum; `elastic2.py` separates the core shrink from the
envelope growth and the drops come from the shrink, apart from row 1207 at $0.003$,
where either alone produces it).
The optimised sites sit on core boundaries, so the charge falls in steps, by `6.5 %` on
row 0 within $\Delta S = 0.0005$, and the fixed-weight certificate is dead at any
$\Delta S > 0$. That is why Guzhou0806’s continuation had to translate sites to move
R052 by $10^{-5}$. A reweighting can repair these steps, and how far it can repair them
is exactly the ceiling question that H-248 asks; a rigorous cap on the reweighted reach
comes only from a refuting family, never from the ledger.
The plan’s decision not to build a producer does not depend on the number, but the
number should be stated as an order of magnitude under a named assumption, and “caps
near $4.646$” should go.

## 5. H-248 and the Anneal

**Posing.** H-248’s claim, metric and direction are right: rational poses and weights,
containment exact, the conservative graph from `geometric_graph_certificate`,
`check_weighted_clique_certificate` proving every clique weight at most $1$ (its
`proved_upper_bound` branch verifies a complete branch-and-bound tree, and an
`overweight_clique` verdict is an exact refutation of the weighting), and
$\Sigma y \ge 17$ exact.
Three additions are worth making.
Say “interior-overlap graph, or any supergraph of it”, so the conservative graph is
named as sufficient.
Say that a family at $465/100$ refutes the architecture at every side from $465/100$ up,
so the $466/100$ target is implied by the $465/100$ one and the search should run at
$466/100$ first, where it is easier.
And name the architecture fully, “cores strictly inside parents” included.

**What the anneal results mean.** The probe minimises the triangle count over exactly
$34$ squares, which is the $y = \tfrac{1}{2}$ special case.
At $N = 34$ with $t$ vertex-disjoint triangles and the rest covered by edges, the
fractional clique cover gives $\alpha^{\ast} \le 17 - t/2$, so “2 triangles,
$\alpha^{\ast} = 16$” restates the triangle count; “3 triangles, $\alpha^{\ast} = 16$”
at $4.66$ says the triangles share a vertex.
That a family at $4.65$ is also a family at $4.66$ and the $4.66$ run ends worse (three
triangles against two) measures the anneal, not the geometry.
Neither run says anything about the families H-248 actually admits and the plan’s search
never visits: $51$ squares with no four pairwise overlapping (`y = ⅓`, pointwise depth
at most three against an available density of $2.36$), $68$ with no five
($y = \tfrac{1}{4}$, but the clique tool stops at $64$ vertices), and mixed weightings
of any $N \le 64$ with $\alpha^{\ast}$ computed by the clique LP. The BC-387 build
should take $\alpha^{\ast}(G_F)$ itself, or its dual, the fractional clique cover, as
the objective, with the triangle anneal as a warm start only.
The plan’s reading, “the anneal does not find the family, and it does not show one is
far away either”, stands.

## 6. Edits the Plan Needs

| Where | Now | Replace with |
| --- | --- | --- |
| Saturation bullet | “1,983 rows sit at exactly $1{,}000{,}000{,}031$ units and 65 rows dip to the binding $\Gamma = 998{,}727{,}933$, a relative $1.27\times10^{-3}$ below the plateau; 18 rows are within $10^{-4}$ of $\Gamma$.” | “895 rows sit at exactly $1{,}000{,}000{,}031$ units and 1,901 within $10^{-4}$ of it; one row is at the binding $\Gamma = 998{,}727{,}933$, a relative $1.27\times10^{-3}$ below the plateau, 18 rows are within $10^{-4}$ of $\Gamma$ and 65 within $10^{-3}$.” |
| Saturation bullet | "Reweighting the same dictionary can lift the 65 binding rows at most to the plateau, about $+0.006$ in side at first order, so a first-party reweighting caps near $4.646$; a larger gain needs new sites, which is Kleddamag’s unpublished “4.65 research”." | "If the source’s LP was optimal, reweighting the same dictionary raises the ratio $17\Gamma/M$ from $1.0000003$ to at most $1.00127$; what that buys in side is not measured here (the fixed-weight charge falls in steps, by `6.5 %` on row 0 within $\Delta S = 0.0005$), and $S \times 1.27\times10^{-3} \approx 0.006$ is an order of magnitude under the assumption that charge and side trade one for one. A larger gain needs new sites, which is Kleddamag’s unpublished “4.65 research”." |
| Ceiling bullet | “with $y(K) \le 1$ on every clique $K$ of $F$’s overlap graph” | “with $y(K) \le 1$ on every clique $K$ of $F$’s interior-overlap graph, or of any supergraph of it such as the conservative graph the checker builds” |
| Ceiling bullet | “the open interval for the architecture’s ceiling is $(4.640020, 4.67553)$.” | “the architecture’s ceiling lies in $[4.640020, s(17)]$, so below $4.67553$.” |
| Family-search bullet | “with $\alpha^{\ast} = 16.00$ on the resulting graph against the 17 needed.” | “with $\alpha^{\ast} = 16$ on the resulting graph against the 17 needed, which at $N = 34$ is what two disjoint triangles cost; the anneal’s objective is the $y = \tfrac{1}{2}$ special case, and the BC-387 search should optimise $\alpha^{\ast}$ over families of any size up to 64, $K_4$-free 51-families included.” |
| Not selected | “the same dictionary caps near $4.646$” | “the same dictionary’s reweighting is worth of order $10^{-3}$ in charge, an unmeasured amount of side” |

The same first two corrections apply to H-248’s `notes` field ("the ceiling lies in
$(4.640020, 4.67553)$") and to idea 257; the lemma text in H-248 and idea 256 needs no
change.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
