---
title: X-044 — transfer opportunities at the lowest open square-packing cases
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-044
  title: Transfer Opportunities at the Lowest Open Square-Packing Cases
  date: '2026-09-22'
  author: GPT-6 Astra at max reasoning; reviewed by the root coordinator
  campaign: packing.squares
  brief: >-
    W3 companion to X-043, following the owner's instruction to focus on the
    lowest-numbered open cases, especially n11. Check current verified and reported
    frontiers, identify where the new threshold, density, adaptive parent-core and
    compatibility machinery could move a result, and distinguish transferable
    mechanisms from numerically weaker corollaries. Propose falsifiable pilots and
    preliminary comparisons without launching a campaign or allocating H IDs.
  sources:
  - operating-rules.md
  - SYNOPSIS.md
  - packing/campaign/README.md
  - packing/campaign/explorations/X-039-n100-re-rank-after-session-140.md
  - packing/campaign/explorations/X-042-what-is-left-at-low-n.md
  - packing/campaign/explorations/X-043-new-lower-bound-proof-directions.md
  - packing/campaign/hypotheses/H-218-existing-colgen-raises-a-small-n-floor.md
  - packing/campaign/hypotheses/H-219-t028-seeded-colgen-raises-s18.md
  - packing/campaign/hypotheses/H-221-t029-seeded-colgen-raises-s18.md
  - packing/frontier/n-011.md
  - packing/frontier/n-012.md
  - packing/frontier/n-013.md
  - packing/frontier/n-014.md
  - packing/frontier/n-015.md
  - packing/frontier/n-016.md
  - packing/frontier/n-017.md
  - packing/frontier/n-018.md
  - packing/frontier/n-019.md
  - packing/frontier/n-020.md
  - packing/frontier/n-021.md
  - packing/frontier/n-022.md
  - packing/frontier/n-023.md
  - packing/frontier/n-024.md
  - packing/frontier/n-025.md
  - packing/frontier/covering-values.yaml
  - packing/cases/n12_fractional_certificate/certificate.json
  - packing/cases/n18_fractional_certificate/certificate-4679-1000.json
  - packing/cases/n20_fractional_certificate/certificate-24-5.json
  - packing/cases/n20_fractional_certificate/certificate.json
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-039/n12-793-200-t017-grid4-windows7-receipt.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-039/n18-4679-1000-t029-auto-windows5-receipt.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-039/n19-481-100-t020-grid4-windows7-receipt.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-039/n20-243-50-t021-grid4-windows7-receipt.md
  - packing/resources/papers/bentz-2010-optimal-packings-13-and-46.md
  - packing/resources/papers/bentz-2016-optimal-packings-22-and-33.md
  - docs/project/reviews/review-2026-09-14-n11-post-w5-route-selection.md
  - docs/project/reviews/review-2026-09-22-tokoharu-density-mathematics.md
  - https://github.com/jlevy/squares/blob/c183cc9abe93eedcb268a5390cdd1cdc6e7bbb39/packing/src/sqpack/fractional/parent_core.py
  - https://github.com/jlevy/squares/blob/c183cc9abe93eedcb268a5390cdd1cdc6e7bbb39/packing/src/sqpack/fractional/parent_core_interval.py
  - https://www.combinatorics.org/ojs/index.php/eljc/article/view/v17i1r126
  - https://arxiv.org/abs/1606.03746
  proposes: []
---
# X-044: Transfer Opportunities at the Lowest Open Cases

**Keep n11 first and make n12 the next mathematical target.** The next open counts are
17 through 21; 13–16 are already solved.
Among those later cases, n17 offers the best direct test of richer threshold features,
n18 has the clearest recent record of successful numerical continuation, and n21 offers
an unusually inexpensive transfer question because its current certificate was built to
exclude twenty squares.

The advances on n11 and n17 transfer more widely as **proof machinery** than as
numerical bounds. Even proving Trump’s n11 packing optimal would leave n12’s present
lower bound unchanged.
A better n17 bound near the reported Bidwell construction would still be weaker than the
existing n18 result.
Those cases need their own instances or new geometric lemmas.

This W3 report under `think-lq67` complements
[X-043](X-043-new-lower-bound-proof-directions.md), which develops the six proof
architectures in depth.
Here the question is where to apply them.
It contains a retained source-arithmetic audit and proposals, not a new packing bound,
experiment campaign or funded queue.
Formal H IDs remain unassigned.

## The Verified Frontier and the Useful Stopping Point

The audit reads immutable case records and certificate bytes from commit
`be736b0ef05ac2f256691bc3ded21873ad1f2ab1`. The table preserves the registered
inequalities: n11 and n17 are strict source theorems; the other lower bounds below are
reported with their registered non-strict symbol.
Decimal gaps are display arithmetic; the exact endpoints govern comparisons.

| Count | Current verified lower statement | Upper reference and assurance | Remaining gap and current mechanism |
| --- | --- | --- | --- |
| [11](../../frontier/n-011.md) | $s(11)>31/8=3.875$ | Trump’s exact verified $U_{11}=3.877083590022814177\ldots$ | $0.002083590022814177\ldots$; Kleddamag adaptive parent-core threshold certificate. |
| [12](../../frontier/n-012.md) | $s(12)\ge99/25=3.96$ | Verified grid upper $4$ | $0.04$; first-party point certificate T-017. Exact value open. |
| 13–16 | $s(n)=4$ | Matching verified upper and lower | Solved; exclude from numerical-improvement targets. |
| [17](../../frontier/n-017.md) | $s(17)>461300/99853=4.61979109290657\ldots$ | Bidwell’s **reported** $4.67553009360455\ldots$; registered verified upper still $5$ | $0.055739000698\ldots$ to the report, $0.380208907093\ldots$ to the verified upper; Kleddamag point-plus-triple parent-core certificate. |
| [18](../../frontier/n-018.md) | $s(18)\ge4679/1000=4.679$ | Exact verified $(7+\sqrt7)/2=4.82287565553229\ldots$ | $0.14387565553229\ldots$; first-party point certificate T-030. |
| [19](../../frontier/n-019.md) | $s(19)\ge24/5=4.8$ | Exact verified $3+4\sqrt2/3=4.88561808316412\ldots$ | $0.08561808316412\ldots$; point certificate T-020, whose filename refers to n20. |
| [20](../../frontier/n-020.md), [21](../../frontier/n-021.md) | $s(n)\ge97/20=4.85$ | Verified grid upper $5$ | $0.15$ each; the same point certificate T-021, with budget below twenty. |
| 22–25 | $s(n)=5$ | Matching verified upper and lower | Solved; a natural stopping point for this low-count screen. |

The primary statements for the nontrivial endpoints include
[Bentz’s n13 theorem](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v17i1r126)
and [his n22 theorem](https://arxiv.org/abs/1606.03746). The intervening cases follow
from their lower bounds and the matching grids; no new numerical work is warranted on
them. A bounded external search found stale indexed copies of this repository, not a new
admitted result superseding the inspected records.
This is not an exhaustive literature-completeness claim.

No conclusion here relies on the misleading idea that a small count is automatically
easy.
Excluding twelve squares below side four is stronger than excluding thirteen, which
is already proved. Conversely, n21 may permit a cheaper numerical movement than n20 at
the same side because it has one additional unit of counting allowance.

## What Can Actually Be Transferred

### Transfer a proved budget, not a filename

Let every legal selected core have charge at least $\Gamma>0$, and let all cores from a
physical packing have total charge at most $M$. Then

$$
n\Gamma>M
\quad\Longrightarrow\quad
\text{the packing is excluded}.
\tag{1}
$$

If no other premise depends on n, the first count covered is
$\lfloor M/\Gamma\rfloor+1$. That formula is conditional on complete geometry and
coverage at the declared side.
A value stored in an unfinished producer is not such a premise.
Equality $n\Gamma=M$ supplies no contradiction.

The audit computes the following from the already retained certificates.
It does not replay them or promote a new count.

| Certificate used today | Exact normalized budget $M/\Gamma$ | First count | Present consequence |
| --- | --- | ---: | --- |
| T-017, side $99/25$ | $149987/12501=11.9980001599\ldots$ | 12 | Its direct numerical target is n12; 13–16 are already solved at four. |
| T-030, side $4679/1000$ | $71573611/4000020=17.8933132834\ldots$ | 18 | Valid for larger counts, but weaker than n19’s $4.8$. |
| T-020, side $24/5$ | $946131/50007=18.9199712040\ldots$ | 19 | Still supplies n19; n20 and n21 already have $4.85$. |
| T-021, side $97/20$ | $19848723/1000005=19.8486237568\ldots$ | 20 | Supplies both n20 and n21, with more charge slack at n21. |

The direction of numerical transfer has hard limits:

* **n11 to n12:** $U_{11}<3.96$. Improving n11 alone, even to its exact verified upper,
  cannot move n12 by monotonicity.
* **n17 to n18:** the reported n17 construction is numerically below $4.679$. A
  certificate advancing toward that report cannot move n18. The tighter upper is not
  registered as verified, so it is not silently used as a proved impossibility bound.
* **n18 to n19:** a new n18 bound above $4.8$ would also improve n19. There is room
  before the verified n18 upper; $(7+\sqrt7)/2>24/5$ because $7>(13/5)^2$.
* **n18 to n20:** even the verified upper is below $4.85$, since $7<(27/10)^2$. An n18
  theorem alone cannot improve n20’s current bound.
* **n19 to n20/21:** a new n19 bound above $4.85$ would move all three.
  This is arithmetically possible before its verified upper, since $3+4\sqrt2/3>97/20$
  is equivalent to $2>(111/80)^2$.
* **n20 to n21:** every accepted n20 improvement transfers.
  An n21 improvement need not apply to n20; its budget can lie between twenty and
  twenty-one.

### Transfer geometry with all of its parameters

In the adaptive parent language, a physical container has side $L$, each parent has side
$A$, and the unit-square target is $S=L/A$. Every row has its own core geometry and
parent-orientation interval.
To increase $S$ at fixed $L$, decrease $A$: the legal centre domain expands while strict
core containment becomes harder.
The old core catalogue, its old coverage proof and its old minimum charge cannot simply
be reused.

The new native library separates those quantities explicitly.
Its core certificate type is parameterized by n; its source-specific n11 command and
frozen source receipt are not universal adapters.
A new case needs an input conversion or producer, complete row inventory, exact
premises, and its own complete coverage receipt.
Confirmation of the old n11 theorem supplies a strong control, not a new lower bound
elsewhere.

For the simpler fixed-$B$ square selector, changing only angular resolution has the
ideal ceiling

$$
S\le L/B.
\tag{2}
$$

A parent containing a $B$-square has side at least $B$. The endpoint in (2) is an upper
limit on this unchanged geometry, not a claim that all finer directions cover.
The retained artifacts all use $B=9977/10000$:

| Current source | Ideal $L/B$ with unchanged $L,B$ | Largest possible gain over the current source side under this restriction |
| --- | --- | --- |
| n12 T-017 | $39600/9977=3.96912899669\ldots$ | Less than $0.009129$ |
| n18 T-030 | $46790/9977=4.68978650897\ldots$ | Less than $0.010787$ |
| n19 T-020 | $48000/9977=4.81106545054\ldots$ | Less than $0.011066$ |
| n20/21 T-021 | $48500/9977=4.86118071565\ldots$ | Less than $0.011181$ |

Thus unchanged-$B$ refinement could be a useful bridge or control, but cannot reach
$3.97$ at n12, $4.69$ at n18, $4.82$ at n19, or $4.87$ at n20/21 from these frozen
working containers. Changed core size, support, weights, charges or conditional domains
are different hypotheses.
None of (2) is an all-source obstruction.

Two other limitations must stay separate:

1. **A fixed-shrink grid obstruction.** If the coverage domain contains every closed
   $B$-square and $L>kB$, place $k^2$ of them on a grid with small positive gaps.
   Any nonnegative additive measure charging each at least one has total mass at least
   $k^2$. For n12 this bars that language beyond $4B=3.9908$; for n20/21, beyond
   $5B=4.9885$. This elementary argument uses the strict $L>kB$ case.
   At equality, boundary conventions need separate treatment.
   An adaptive parent restriction can remove nonextendable cores, so the conclusion does
   not automatically apply there.
2. **A source-independent fractional obstruction.** At n11 the transported 88-parent
   family rules out every unconditional additive measure at and above
   $38200/9977\approx3.828806$. It applies to ordinary points and densities, even with
   better support and parent-aware geometry.
   X-043 states that proof and its scope.
   No corresponding all-source ceiling for n12, n18, n19 or n20/21 is established by the
   records inspected here.

A floating LP plateau, an incomplete high objective, a bad choice of support and a
proved all-source dual obstruction are four different observations.

## n11: The Primary Target, With a Very Small Remaining Gap

The strongest route from X-043 remains **a complete low-charge pose cover plus a bound
on which parents can coexist**. The external certificate gives most of the covering
work; compatibility can improve the total charge over eleven parents without raising the
minimum for every isolated pose.
It must use actual parents, prove cell capacities, retain unresolved boxes, and carry
global symmetry labels into joint tests.

A useful comparison is a proposed side such as $3.876$: an improvement of $0.001$
removes about 48% of the present gap.
Compare two treatments on the same target:

* repair individual losses using better core menus and new support/threshold features;
* retain the losses but certify that too few weak parents coexist to defeat the budget.

The first complete failing parent pose or surviving count relaxation distinguishes which
missing information to pursue.
Neither a sampled charge map nor a finite conflict graph decides the case.
The 208-centre n17 diagnostic in X-043 is a tool calibration, not evidence about n11’s
residual geometry.

Plain Tokoharu densities are useful integration machinery but cannot cross n11’s
additive ceiling. Combine them with integer reservoirs, threshold features, or proved
conditional packing information if using them for numerical movement here.
Likewise, T-033’s frozen old family tops out below $3.828$; another direction-net
refinement of it would not advance the current bound.

The largest payoff is a global capture theorem at Trump’s exact side followed by the
local theorem, as X-043 explains.
That is a different objective from another rational bound.
It must preserve the quantitative local packet’s outstanding dependency and allow the
known packing at equality.
This report proposes no new n11 execution beyond the X-043 candidate set.

## n12: The Next Open Case Needs a Changed Comparison

### What has actually resisted continuation

T-017 has 2,097 atoms and normalized budget only about $0.002$ below twelve.
The retained point searches at $3.965$ and $3.97$ did not produce a stronger
certificate. For example, the four-grid, window-enriched $3.965$ run stopped with
floating objective $12.066995$, 192 violated rows and no freeze.
These observations justify avoiding an identical expensive retry; they do **not** prove
a site-set or language-wide ceiling.
[H-218](../hypotheses/H-218-existing-colgen-raises-a-small-n-floor.md) explicitly
corrects the stronger negative language in some older receipts.

At $3.98$, $3.985$ and $3.99$, a different obstruction was diagnosed: site sets missed
the thin overlap windows of a nearly four-across grid of $B$-squares.
For axis position $j$, such windows have endpoints of the form

$$
[L-(4-j)B,\;jB],\qquad j=1,2,3,
$$

and width $4B-L$ when positive.
The discrete support can make geometrically overlapping cores look site-disjoint.
Adding window sites removes that particular artifact; it does not establish that a good
point certificate exists afterward.
The later searches with window sites already failed to retain a bound.

### Three useful comparisons

**1. Adaptive parent geometry on the retained charge system.** At the illustrative
target $S=793/200=3.965$, keep $L=99/25$ so $A=792/793$. The old $B$ is still smaller
than $A$, so a finer or adaptive orientation cover could fit it; complete charge
coverage at the new directions remains unknown.
This is a narrowly scoped bridge test.
It isolates discarded-parent-domain and selector loss before paying for a new support.
It cannot reach $3.97$ while that same $B$ stays fixed, by (2).

**2. Threshold features on the actual surviving placements.** Use the difficult parent
poses from that bridge as the common comparison set for ordinary points, two-of-three,
two-of-five, three-of-five and selected weighted features.
The treatment must permit the ordinary control the same new sites.
A strict rational finite primal/dual gap earns full separation; merely lowering one
floating objective does not.
Five-site atoms are a candidate because they worked within the richer n11 combination,
not because their contribution there was isolated experimentally.

**3. Rectangle densities on thin geometric regions.** Densities offer support over a
whole window or boundary strip instead of guessing a handful of point coordinates.
Compare a frozen rectangle basis against point bases on the same parent geometry, then
consider nonlinear integer reservoirs only if the additive basis meets a real
obstruction. The
[Tokoharu review](../../../docs/project/reviews/review-2026-09-22-tokoharu-density-mathematics.md)
provides the integration theorem and source provenance.
Its current fixed-net format still pays a shrink loss; density alone has not removed
that loss.

A more specific hybrid would evaluate atomic resources on a strict selected core and the
density on the actual parent:

$$
q(P)=\mu(Q(P))+\int_P g+\sum_a w_a
\mathbf1_{\{|F_a\cap Q(P)|\ge k_a\}},
\qquad
M=\mu(K)+\int_K g+\sum_a w_a\lfloor |F_a|/k_a\rfloor.
\tag{3}
$$

Each summand has its own valid disjoint-packing budget; square boundaries have zero area
for the density term.
Thus the density contribution need not lose the material between the core and parent.
This requires a new complete hybrid coverage evaluator: neither imported wrapper already
certifies (3). Without its threshold terms it remains bounded by an additive measure of
the full parent, so it cannot evade n11’s additive obstruction.
At n12 that all-source obstruction has not been established.

The strongest new architecture from X-043 also applies: partition the n12 parent domain
by charge and prove a count inequality over its low-charge remainder.
It can be more informative to bound four simultaneous losses than to insist on fixing
every one independently.
No such capacity is currently proved here.

### Exact four is a separate mathematical program

A finite list of improved rational bounds below four does not prove $s(12)=4$. One
possible route is a certificate family parameterized by $\varepsilon$ on
$0<\varepsilon\le\varepsilon_0$, at side $4-\varepsilon$, with complete pose coverage
and an exact positive budget gap throughout that interval.
Proving, for example, $12\Gamma(\varepsilon)-M(\varepsilon)\ge c\varepsilon^p>0$ would
supply the arithmetic part, but the uniform geometric coverage is the difficult premise.
Smaller sides then follow by upward embedding.
The equality packing at side four is allowed.

A finite template could rescale thin boundary regions by $\varepsilon$, keep rational
functions for point positions or reservoir masses, and certify polynomial signs on each
active regime. Its first task is one positive-width parameter interval or one complete
boundary class. A few sampled values do not establish the family.

The side-four grid witnesses have genuine flexibility.
A capture argument must include the relevant continuous components and singular boundary
cases, not assume a unique rigid grid.
The earlier Route N admission condition in the
[post-W5 review](../../../docs/project/reviews/review-2026-09-14-n11-post-w5-route-selection.md)
already demands a uniform near-four lemma.
New machinery makes a better candidate possible; it does not discharge that condition by
itself.

## A Concrete Structural Connection Between n12 and n21

These counts are $m^2-4$ for $m=4,5$. The solved neighbours $13$ and $22$ are $m^2-3$.
Their proofs offer controlled reductions, but losing one packed square weakens the
decisive counting step.

For any unavoidable set of $t$ distinct points and a hypothetical family of $n$ disjoint
open boxes, let $u$ count unused points and $r_i\ge1$ the number in box $i$. Then

$$
u+\sum_i(r_i-1)=t-n.
\tag{4}
$$

This exact identity identifies the additional occupancy patterns a neighbouring case
must handle. It is more precise than assuming that the old proof transfers with one
number changed.

If $c$ marks belong to a distinguished subset, at least $c-2(t-n)$ of them are in
single-mark boxes whenever that expression is positive: an unused mark costs one unit of
excess, and a box with $r_i\ge2$ marks accounts for at most $r_i\le2(r_i-1)$
non-singleton marks.

In the n13 proof, Bentz begins with sixteen points and obtains at least two
corner-restricted boxes.
At n12 the excess in (4) increases from three to four.
The purely combinatorial allocation of four pairs among the eight corner marks and eight
remaining singletons consumes all sixteen points in twelve boxes; it defeats that
counting inference. This is an allocation counterexample, not a geometric packing below
four. A useful new cut would exclude or control exactly such allocations using parent
footprints or threshold charges.
Any use of the old geometric transfer also needs the locally corrected Lemma 10, not its
printed coordinate transposition.
[Bentz 2010, §3](../../resources/papers/bentz-2010-optimal-packings-13-and-46.md#3-13-squares).

For n22, Bentz’s initial red and blue covers have 22 and 23 points.
At n21 their excess budgets become one and two.
The latter permits two unused marks, one unused mark plus one doubly occupied box, two
double occupancies, or one triple occupancy.
The continuous movement theorem still requires exceptional marks to remain fixed.
Its geometric applications also retain the source’s upper bound of $1.01$ on box side.
The research question is whether geometry forces those exceptions into incompatible
locations or whether an additional threshold/segment resource pays for them.
[Bentz 2016, Theorem 8 and §4](../../resources/papers/bentz-2016-optimal-packings-22-and-33.md#4-the-best-possible-packing-of-22-unit-squares).

This suggests a shared **occupancy-pattern checker with geometric proofs attached**.
First enumerate the small excess patterns exactly; then ask a local parent checker about
only the patterns that survive.
A complete list of patterns plus a proof for every branch would be transferable
machinery. Showing one pattern impossible is a local theorem, not a global n12 or n21
bound. No theorem for all $m$ is conjectured from these two cases.

## n17 and n18: Different Reasons to Continue

### n17: changed features have a concrete starting point

The external n17 certificate has parent-aware rows and ordinary points plus triples.
X-043’s main proposal is to co-design richer features and sites against its actual dual
adversaries, with core menus and compatibility as alternatives.
The exact exp-222 mass floor limits repricing only at the frozen support and $(L,A)$;
its heuristic side sensitivity is not a side ceiling.
Finer angular resolution is not the same intervention as improving the selected charge
language.

The n17 study should start from the current $461300/99853$ control, not the obsolete
first-party $4.59$ target still named in old H-218 text.
A target such as $4.63$ would be material movement, but neither the finite clique
diagnostic nor the richer n11 certificate promises it.
The best reported n17 packing is flexible, so exact closure would need a component
theorem rather than one-pose isolation.

### n18: successful seed continuation, then a possible representation boundary

T-027 through T-030 advanced n18 from $4.67$ through $4.675$ and $4.6775$ to $4.679$.
The final retained run had 957 atoms, complete coverage and both checking routes
accepted. The repeated old $4.68$ plateau is not a proved global ceiling: some records
lack exact duals, and finite supports do not settle all supports.

The closest discriminating comparison is **the same T-030 charge system with adaptive
parent geometry at $4.68$**, for which fixed $L=4679/1000$ means $A=4679/4680$. It would
distinguish geometry lost by the uniform core from missing charge resources.
It is a small numerical rung, not the full innovation target.
A persistent exact defeating pose should seed new threshold or density columns, rather
than another unmodified grid sweep.

The verified upper is much farther away than at n11. Consequently n18 is a useful
development case for a general producer if the first task can be bounded and matched.
The current $L/B$ ceiling is below $4.69$, so reaching a target such as $4.70$ already
requires a change beyond refining the frozen $B$-square family.
Success would still leave n19 unchanged until the n18 bound exceeds $4.8$.

## n19: A Useful Harder Comparison, Not an Automatic Spillover

T-020 remains at $4.8$. At $4.81$, the later four-grid/window run ended at floating
objective $19.111435$, 369 violated rows, and no freeze.
H-218’s exactness correction applies here too.
This is evidence against a blind repeat, not an all-source dual obstruction.

A parent-aware replay of the retained measure is a small control, with a frozen-family
ideal ceiling only $4.811065\ldots$. For a larger movement, such as beyond $4.82$, use
genuinely changed sites, threshold features, density regions or conditional
compatibility. Compare n19 with n18 using the same producer controls: does the new
representation defeat the named difficult placements in both cases, or merely tune one
support? This is a way to test transferability without funding a whole n19 search.

A possible high-value structural target is a certificate above $4.85$, which would
improve n19, n20 and n21 together.
The gap from $4.8$ is $0.05$, and no inspected certificate supports that jump.
Its multi-case payoff is a reason to preserve the idea, not to rank it ahead of n11 or
n12 on present evidence.

## n20 and n21: Exploit Count Slack Explicitly

The same T-021 system is much farther from its budget limit at n21. For its fixed mass
$M=19848723/10^6$ and recorded least charge $\Gamma_0=200001/200000$, a changed-geometry
coverage proof would need

$$
\Gamma>M/n.
\tag{5}
$$

| Count and source | Required new charge, strictly greater than | Relative charge loss allowed from the recorded minimum, strictly less than |
| --- | --- | --- |
| n12, T-017 | $149987/150000=0.99991333\ldots$ | $0.0166653\%$ |
| n18, T-030 | $71573611/72000000=0.99407793\ldots$ | $0.592704\%$ |
| n19, T-020 | $946131/950000=0.99592737\ldots$ | $0.421204\%$ |
| n20, T-021 | $19848723/20000000=0.99243615$ | $0.756881\%$ |
| n21, T-021 | $6616241/7000000=0.94517729\ldots$ | $5.482744\%$ |

These are charge tolerances, **not side tolerances**. No continuity estimate converts
them into an achievable side.
A small core movement can lose a large atom abruptly.

Still, n21 offers a concrete cheap question: can the unchanged T-021 weights cover
actual parents at a selected larger ratio, say $S=4.9$, with a smaller row-dependent
core and charge above $6616241/7000000$? At fixed $L=97/20$, that target requires
$A=97/98$; it is below the old $B$, so a changed core is mandatory.
Testing a few critical rows can refute this particular proposal before a full run.
Only complete coverage can accept it.
A success at n21 would not justify retagging it n20.

For n20, the old $4.855$ and $4.86$ searches stopped below twenty but still had many
violated rows. Their low floating objective was not an accepted covering.
The parent adapter, a density basis or thresholds provide a changed comparison; giving
the same unfinished setup more time is not the innovation being proposed.

For exact closure at five, n21 is the more attractive of this pair: it is one count
below the solved n22 theorem, with the explicit extra patterns in (4). n20 introduces
another deficit. Both need a uniform argument below five and must preserve the flexible
side-five boundary configurations.
No finite strict certificate can exclude the valid packing at five itself.

## Preliminary Comparison and Candidate Hypotheses

This is an information-value comparison for discussion, not an execution schedule.
Targets are illustrative and must be frozen before an experiment.

| Case | Present priority and reason | Most informative next distinction | A reason to stop the selected representation |
| --- | --- | --- | --- |
| n11 | Primary; smallest open count and strong new threshold control | Can improved per-parent selection fix the losses, or is packing compatibility necessary? | Complete exact counterexamples defeat the frozen menu/feature family, or the admitted count relaxation retains a witness. |
| n12 | Next mathematical target; only $0.04$ from exact four | Parent-domain loss versus missing threshold/density resources; separate a numerical rung from a uniform near-four lemma | Exact duals or legal poses defeat the frozen treatment; unresolved floating searches do not. |
| n17 | Strongest larger-count test of richer threshold discovery | Five-site/support columns versus the strongest matched point/triple control | Whole optimal dual face survives all proposed columns, or complete separation defeats the candidate. |
| n18 | Clearest recent numerical continuation; good producer calibration | Can parent geometry pass $4.68$, and which poses require new resources? | Same exact defeating poses survive the changed selector with all declared options. |
| n21 | Cheap companion screen with unusually large charge allowance | Does smaller-core coverage retain enough of T-021’s charge at a new ratio? | One exact admissible undercharged pose refutes those fixed bytes. |
| n19 | Secondary harder transfer test; potential later benefit to 20/21 | Does an improvement mechanism generalize beyond n18’s support? | No rational common-row gain, or a complete candidate fails; do not infer a global ceiling. |
| n20 | Companion to n21 with a stricter budget | Does the same changed representation also clear the twenty-parent threshold? | An n21-only certificate remains above twenty; that is not a failure of its n21 claim. |

The following local labels are candidates for later codification.
n11’s detailed candidates stay in X-043 rather than being duplicated here.

| Label | Falsifiable candidate | Smallest useful positive | Negative or unresolved outcome |
| --- | --- | --- | --- |
| L12-A | At a fixed side above $3.96$, the retained n12 charge system plus a specified adaptive parent/core catalogue satisfies (1). | Complete premises and complete centre coverage with the exact budget. | A legal exact undercharged pose rejects the catalogue; partial rows cannot accept. |
| L12-B | On frozen n12 adversarial poses, a new threshold or rectangle basis beats the matched ordinary-point optimum. | Rational treatment primal below rational control dual; then a separate full-separation claim. | A control optimum dual remains feasible under all proposed columns, or the geometric realizations fail. |
| L12-C | A declared finite template certifies a positive-width interval $4-\varepsilon$ uniformly, including its assigned flexible boundary classes. | A complete parameter-domain proof, not sampled rungs. | A validated packing defeats an exclusion; a surviving box or missing class leaves the template unresolved. |
| L18-A | T-030 weights with specified parent rows certify the illustrative $4.68$ target. | Full exact-premise and coverage acceptance. | Exact defeating pose; add a new resource only under a successor hypothesis. |
| L19-A | One feature/density producer gives a rational common-row advantage at both a new n18 side and a new n19 side. | Independent matched finite comparisons; no global bounds claimed yet. | A gain confined to one case rejects the two-case claim, not the successful single comparison. |
| L21-A | Smaller selected cores with T-021 weights keep complete charge above the n21 threshold at a frozen target such as $4.9$. | Full coverage with $M<21\Gamma$ and target-specific metadata. | An exact undercharged parent refutes the frozen proposal; equality in the budget is insufficient. |
| L21-B | A named exceptional-occupancy pattern from Bentz’s covers is geometrically impossible for the relevant open boxes. | Complete local proof covering all its continuous poses and boundary cases. | A validated tuple refutes that local exclusion; all other patterns remain unproved. |
| LC | A complete charge-band/count certificate improves a selected low-n bound where uniform point coverage stalled. | Verified parent-pose cover, multiplicities, geometric constraints and rational composition inequality. | A surviving relaxation vector rejects that relaxation only; absence of a packing search result proves nothing. |

L12-A/B and the n19/n20 producer comparisons overlap H-218’s ambition, but change its
fixed point/net representation.
L18-A follows the retained H-219/H-221 ladder with a different geometry test.
The uniform endpoint and occupancy-pattern candidates extend the earlier Route N and
conditional-resource questions.
They should be linked to those records, not registered as independent rediscoveries.

## What the Shared Tools Need to Preserve

One general parent-input adapter would serve the bounded bridge tests at n12, n18, n19
and n20/21. It must retain separate $L,A,B$, exact resource budgets, count-specific
charge thresholds, a contiguous orientation cover, and the source/current side
distinction. Its negative controls should reject a wrong target count and stale side.
Those are observed hazards in the imported density continuation driver, not speculative
requirements.

A complete residual-pose exporter would serve both n11 and n12 compatibility work.
It must carry unresolved leaves, actual parent domains, charge units and capacities;
independent D4 folding is valid for individual charge verification but invalid for
relative placement tests.
A small-group geometric checker and a rational count-proof checker can then share the
same interface across cases.

A density/feature producer should compare like with like: same poses, same admitted
ordinary sites, exact capacities for each threshold, and a full separation stage after
finite optimization.
An all-source no-go claim needs a valid continuous fractional packing or other global
dual. Failing to find one is not evidence that a certificate exists; a weak folded dual
is only inconclusive.

These are bounded consumers of the machinery developed in X-043. Building all tools
before selecting the first mathematical question would obscure which one earns its cost.

## Retained Audit and Limits

The retained tool
[frontier_transfer_audit.py](../../cases/w3_lower_bound_directions/frontier_transfer_audit.py)
reads frozen Git objects rather than changing working files.
Its ten-second polling budget was set before execution; it is checked between immutable
source reads rather than enforced as a hard subprocess deadline.
The first [audit](../../cases/w3_lower_bound_directions/frontier-transfer-audit.json)
took 0.376 seconds; the follow-up
[count-slack audit](../../cases/w3_lower_bound_directions/frontier-transfer-count-slack.json)
took 0.709 seconds. Both used project Python 3.14.7 and the same commit.
No geometric search, certificate replay or numerical optimization ran in this W3 screen.

From the repository root, with a fresh output filename:

```bash
packing/.venv/bin/python3 packing/cases/w3_lower_bound_directions/frontier_transfer_audit.py \
  --repo . \
  --commit be736b0ef05ac2f256691bc3ded21873ad1f2ab1 \
  --output /private/tmp/w3-frontier-transfer-count-slack-fresh.json \
  --seconds 10
```

The receipts retain original commands and all exact rational arithmetic.
Decimal gaps are derived from the displayed record fields and are not new algebraic
certificates. The report’s signed comparisons above use the exact formulas where needed.
X-043 is retained beside this report.
The native parent modules were read at
[commit c183cc9](https://github.com/jlevy/squares/tree/c183cc9abe93eedcb268a5390cdd1cdc6e7bbb39/packing/src/sqpack/fractional),
and the
[complete proof receipt and review](https://github.com/jlevy/squares/tree/e473da2fde1ca42ea3a10ef0f390a593dcbf91da/packing/campaign/agent-sessions)
are pinned to the reviewed PR223 history.
The retained audit receipts preserve their historical commands verbatim.

The useful choice is now specific: n11’s compatibility or improved-selector question,
n12’s changed representation, or a small n18/n21 transfer control that tests the shared
producer. The solved intervening cases require no numerical campaign.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
