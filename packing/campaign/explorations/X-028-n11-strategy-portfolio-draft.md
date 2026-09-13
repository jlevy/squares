---
title: X-028 — draft n11 strategy portfolio after the daytime explorations
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-028
  title: Draft N11 Strategy Portfolio After the Daytime Explorations
  date: '2026-09-10'
  author: GPT-6 Astra, reconciling the retained daytime portfolio
  campaign: packing.squares
  brief: >-
    Preserve the six-route daytime strategy portfolio as a draft exploration, revise its
    scheduling and claims against Agenda 035 and the subsequent X-027 analysis, and map
    the remaining alternatives to their evidence, existing work items, prospective
    discriminators, and scoped stopping conditions. This is a documentation synthesis;
    it runs no research target and registers no new scientific claim.
  sources:
  - packing/campaign/agendas/agenda-035-n11-daytime-strategy.md
  - packing/campaign/explorations/X-026-what-conditioning-does-and-does-not-buy.md
  - packing/campaign/explorations/X-027-stromquist-fractional-and-structural-strategy.md
  - packing/campaign/hypotheses/H-156-threshold-certificate-past-3-82.md
  - packing/campaign/hypotheses/H-158-unit-parent-domain-excludes-saved-residual.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-155-h156-finer-net-threshold-dilation.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-156-unit-parent-saved-residual.md
  - docs/project/reviews/review-2026-09-10-n11-parent-domain-translation.md
  - docs/project/research/research-2026-09-09-n11-evidence-and-inference.md
  - docs/project/reviews/review-2026-09-09-n11-evidence-interpretation.md
  - docs/project/research/research-2026-09-10-x027-fractional-duality.md
  - docs/project/research/research-2026-09-10-x027-certificate-mechanisms.md
  - docs/project/research/research-2026-09-10-x027-structural-helpers.md
  - packing/campaign/hypotheses/H-131-near-axis-counts-at-q.md
  - packing/campaign/hypotheses/H-134-eleven-mark-ownership-set.md
  - packing/campaign/hypotheses/H-135-paired-full-support-pricing.md
  - packing/campaign/hypotheses/H-155-conditional-threshold-cover-on-an-owner-class.md
  - packing/campaign/hypotheses/H-018-basin-entry.md
  - packing/campaign/hypotheses/H-026-trump-first-order-rigidity.md
  proposes: []
---
# X-028: Draft N11 Strategy Portfolio After the Daytime Explorations

**Status: draft exploration.** The six routes from the retained September 10 daytime
portfolio remain useful options, but their execution order and prerequisites have
changed. The next direct-bound continuation is BC329’s frozen finer-net packet, after
runner admission. Conditional geometry, richer charges, pricing, and constructive search
retain separate questions and different standards of success.

This draft preserves and revises
`attic/n11-daytime-strategy/n11-daytime-strategy-portfolio.md`, whose source baseline
was `3a18a05a`. The later
[X-027 synthesis](X-027-stromquist-fractional-and-structural-strategy.md), read from
upstream revision `d507f5c7`, supplies the newer analytical arguments and their reviews.
Its detailed proofs remain there and in its companion reports.
[Agenda 035](../agendas/agenda-035-n11-daytime-strategy.md) owns execution state; bead
`think-dqqa` tracks preservation and reconciliation.
No target was run for this draft, and `proposes: []` records that it allocates no new
hypothesis identifiers.

## Decision Standard and Evidence

Let $s(11)$ be the least square-container side admitting eleven unit squares with
pairwise disjoint interiors.
A **strict core** is a smaller closed square lying in the interior of a physical
unit-square parent. Cores selected from distinct parents are disjoint, so a valid
counting certificate that charges every admissible core at least one with a total budget
below eleven excludes the physical packing.
A **point cover** uses nonnegative point weights; a **threshold charge** also counts
cores containing a specified number of sites.
A **fractional family** permits overlapping cores with nonnegative weights.
It obstructs a certificate language only after every capacity inequality of that
language is verified.
For a fractional family $\{(C_i,\lambda_i)\}$, its **mass** is $\sum_i\lambda_i$, and
its **point depth** at $x$ is the sum of the weights of the cores containing $x$. A
core’s **trace** on a finite site set is the subset of those sites that it contains.
An **owner** of a marked site is a selected core containing it; the core’s physical
unit-square parent contains the mark as well.
A **placement support** is the finite list of core placements used as the rows of a
finite linear program.
A result on that list need not hold after other placements are added.

The retained bound is

$$
C=\frac{955000\sqrt{518400042893309449}}{179696714646249}
=3.826447410572939744\ldots
\le s(11)\le3.877083590022814177\ldots.
$$

T-026 proves the ordinary exact lower bound at V4/C5 in the
[current evidence account](../../../docs/project/research/research-2026-09-09-n11-evidence-and-inference.md).
Its limit argument does not decide the separate strict inequality $s(11)>C$. Improving
the lower bound requires a complete exclusion for every side below some new endpoint
above $C$, proved directly or through a limiting argument.
Covering routes must establish complete coverage and physical transfer; structural
routes must cover their geometric cases and routing.
Improving the upper bound requires one independently verified packing below Trump’s
exact value; exhaustive search is unnecessary for that direction.

| Evidence | What It Establishes | What Remains Open |
| --- | --- | --- |
| T-025 and T-026; H-156 / exp-155 | Threshold charges give a certificate of budget $685457679/62500000=10.967322864$ at $191/50$; finer-net coverage and dilation prove $s(11)\ge C$ | The separate rows-complete loop at $383/100$, re-optimized weights, and changed atom families |
| A6’s exact family at $153/40$ | Mass eleven, depth one, and feasibility for all 2,566 retained ordinary atom orbits; new point sites alone cannot defeat that family with the same atom set | A changed atom language or core domain, and replacement placement supports |
| A6’s added atoms | Six ordinary atom orbits cut successive families; an admitted upper bound on the fixed 280-placement support is $2605263163/250000000$ | The larger covering LP stayed numerically at eleven; the displayed replacement family has depth above one, so neither an exact global tie nor an improved global cover follows |
| X-026 and H-157 | Neutrality obstructs point covers on named endpoint-patch residual domains; six of eight refined subclasses remain neutral and two improve | Stronger domains, conditional thresholds, compatible owner selections, and routing |
| H-158 / exp-156 | The saved residual survives its necessary parent box; all 181 B-only frames already exclude its selected TR owner | Parent-domain gain at BL, BR, or TL; the frozen protocol stopped before those owners, leaving H-158 unresolved |
| Parent-domain translation review | The translated 88-core family has individually contained exact unit parents from $3.82345$ with the retained core side and nodes | Simultaneous parents, owner conditions, changed charges, larger cores, and changed selection domains |
| X-027’s reviewed deductions | Full-unit fractional mass eleven at $L_*=38200/9977$; seven owned corner marks and at most three contact components after the stated normalization at $96/25$ | A physical integrality gap at $L_*$, useful complete geometric cells, and a new global packing bound |

The sources for the finite-family statements and their independent replay are the
[A6 evidence section](../../../docs/project/research/research-2026-09-09-n11-evidence-and-inference.md#13-the-later-a6-and-h157-results-what-has-been-checked).
The
[interpretation review](../../../docs/project/reviews/review-2026-09-09-n11-evidence-interpretation.md)
and [X-026](X-026-what-conditioning-does-and-does-not-buy.md) keep those findings
separate from broader strategic judgments.
X-027’s new deductions have reviewed analytical arguments; this draft does not promote
them to registered frontier claims.

## Portfolio and Existing Work Map

The ordering below is a readiness and information judgment.
It is not a measured comparison of expected gains or runtime, and it does not authorize
a new target. The six original routes remain visible; the successful finer-net mechanism
now has its own direct continuation.

| Order | Route | Existing Work | Disposition at This Reconciliation |
| --- | --- | --- | --- |
| 1 | Finer core/net packet with frozen relative weights | BC329, think-17qa; runner admission think-qw9w | Selected direct-bound continuation; coverage unmeasured |
| 2 | Changed certificate language with support updates | Original route 1; BC327, think-yc80 | Blocked on multiplicity and paired-program admission; X-027 supplies a smaller geometric trace comparison |
| 3 | Conditional owner geometry | Original route 2; completed BC326 / exp156; BC337, think-0cdq | Retire the old TR comparison; BC337 is the distinct unary-domain successor |
| 4 | Joint compatibility and selection routing | Original route 3; completed BC328’s normal form; X-027 structural proposals | Use the new premises to select one complete comparison before broad enumeration |
| 5 | Threshold charges on one residual owner domain | Original route 4; H-155 / BC330, think-vx0p | Blocked on the restricted gate and matched complete point baseline |
| 6 | Exact full-support pricing | Original route 5; H-135 / BC331, think-lkvd | Prepared reserve requiring a fresh forward protocol |
| 7 | Constructive challenge outside Trump’s local class | Original route 6 | Retained alternative requiring its own selected contact signature and search allocation |

### 1. Finer-Net Coverage Before Another Language Expansion

[H-156](../hypotheses/H-156-threshold-certificate-past-3-82.md) succeeded through its
finer-net disjunct in
[exp-155](../series/series-000-smoke-and-calibration/experiments/exp-155-h156-finer-net-threshold-dilation.md).
BC329 is a prospective successor with the same T-025 sites and relative weights, a
2880-step net, core side $B=9981/10000$, and angular mismatch bound
$D=207107/1440000000$. Here $D$ is the worst mismatch tangent, not an angle.
Its geometric limit is approximately $3.826721480476156460$, conditional on complete
coverage of that packet.
The
[preflight](../../../docs/project/reviews/review-2026-09-10-n11-bc329-packet-preflight.md)
states the frozen source and normalization.

**Discriminator.** Admit the bounded fixed-core runner, then register its single target
before execution. With raw budget $M=685457679/62500000$ and exact least charge $m$,
success requires $m>M/11=685457679/687500000$. Normalize once by $1/m$, then obtain both
complete coverage decisions and the dilation replay on the same normalized certificate.
A numerical minimum or a promising geometric limit cannot replace those checks.

**Stop and scope.** Preserve BC329’s admitted process limits and one-packet contract.
One verified core of raw charge at most $M/11$ rejects this packet’s normalization;
timeout or incomplete coverage is unresolved.
Neither closes re-optimization, other packets, or richer charges.
This route remains selected because it tests a specific continuation of a mechanism that
has produced a stronger bound.
Direction-dependent core sizes remain another geometric option, requiring complete
coverage and physical transfer on every assigned angle cell.

### 2. Change Atoms and Check the Replacement Supports

A6 shows why adding arbitrary point sites while retaining its 2,566 atom orbits and core
domain cannot defeat that family.
It also shows why cutting a particular fractional family is insufficient: another
support can retain the finite program’s value.
New atoms and new placement rows must be compared on an explicitly matched program, with
complete geometric coverage still required for a theorem.

BC327 retains the seven-token, threshold-four five-site motif.
Its multiplicities need admission throughout the producer, loader, capacity reader,
symmetry handling, and both coverage routes.
The paired adapter and reconstructable row manifest are also prerequisites.
X-027’s
[certificate analysis](../../../docs/project/research/research-2026-09-10-x027-certificate-mechanisms.md)
provides a useful preliminary question: does this motif retain an expressive advantage
over all 80 ordinary threshold types on the same five sites once only geometrically
realizable traces are considered?

**Discriminator.** Freeze one motif, its coordinates, and the admissible core domain.
An exact dual lower bound above one on traces with exact realizing cores proves a local
advantage. A certified ordinary mixture costing at most one on the complete realizable
trace universe removes that advantage on this domain.
Ordinary replacement columns may still improve the current catalog.
Neither outcome alone decides the full covering LP.

For the later paired program, use X-027’s exact test on the whole old optimal dual face:
new atoms improve a finite optimum only if no old optimum satisfies every new capacity.
Removing the solver’s single returned dual vector is weaker.
A complete point-depth check remains necessary for any replacement family claimed as a
point obstruction.

**Stop and scope.** One declared motif or one admitted support/atom comparison per
registered block. An exact finite tie closes that comparison; a globally admissible
mass-eleven obstruction closes its declared language and domain.
Numerical ties, row-incomplete covers, and replay timeouts decide neither.
Higher-rank or floor charges remain alternatives after an explicit globally valid cut
demonstrates useful separation; the abstract five-site floor-profile advantage alone
does not justify a global claim.

### 3. Conditional Parent Geometry After Exp156

The
[translation proof](../../../docs/project/reviews/review-2026-09-10-n11-parent-domain-translation.md)
removes a redundant global test: tightening isolated-parent containment with the
retained $B=9977/10000$ and nodes cannot defeat its translated point obstruction at
$3.827$. Each core has a possible parent; the parents are not proved mutually
compatible. X-027 additionally transports the family to full unit squares at $L_*$,
obstructing unconditional point measures there and above.
Continuous density does not bypass that point-capacity obstruction under the report’s
stated formulation.

The conditional fixed-residual test has now run.
[Exp156](../series/series-000-smoke-and-calibration/experiments/exp-156-unit-parent-saved-residual.md)
returns `b-only-incompatible` for TR: the residual survives its parent box, but the old
B-core owner model already excludes it.
The narrower parent-restricted TR set cannot show added gain.
The sole registered invocation stopped there, and H-158 is neither accepted nor
rejected. A later comparison of BL, BR, and TL needs a new prospective protocol with
matched B-only controls; exp150’s different residual cannot supply them.

**Discriminator.** BC337 instead proposes the complete TR all-owner-incompatible region
for exp151’s fixed direction and tuple.
Compare it with the old common-patch obstacle while retaining the same other obstacles
and the open residual-centre domain.
Admit the source-bound constructor, exact clipping, bounded runner, and independent
reader first. The new centre-space obstacle must be used directly, without a second
Minkowski expansion.
This is a unary compatibility test, separate from shared-owner pair tests.

**Stop and scope.** Follow BC337’s one-invocation contract after admission.
Complete coverage excludes this direction of this residual domain; a strict surviving
escape with its compatible TR witness limits this comparison.
Neither is a full-net class cover, parent-realizable eleven-square packing, or global
routing theorem.
Preserve exact partial results as partial if construction or coverage is
incomplete.

### 4. Joint Owners and Selection Routing

A global conditional proof needs the following statement.
For every hypothetical physical packing $P$, let $\Gamma(P)$ be its valid owner
selections, and let $G$ be the selections whose residual families have been excluded.
Then prove

$$
\forall P,\qquad \Gamma(P)\cap G\ne\varnothing.
$$

A surviving label may coexist with an excluded selection of the same packing.
Conversely, an individually feasible owner or an abstract compatible tuple need not
extend to a physical packing.
These quantifiers are why X-026’s named neutral classes do not refute conditioning as a
strategy.

The
[structural-helper report](../../../docs/project/research/research-2026-09-10-x027-structural-helpers.md)
adds seven-of-eight mark ownership, shared surplus accounting, and at most three
physical contact components after fixed-angle normalization at $96/25$. Owners selected
after that normalization give a contact path between different corners.
These are useful analytical premises, but they imply no short path, finite angle set, or
rigidity. The 80 abstract mark-incidence patterns still contain continuous geometric
obligations.

**Discriminator.** Select one of X-027’s two nearer comparisons: a source-bound co-owner
geometry with its full parents and common surplus, or two disjoint residuals with
positive unary controls followed by a complete common-owner test.
Exp149 and exp151 cannot stand in for the latter: their cores intersect, and exp151
already fails the TR unary control.
Co-ownership alone also has a retained neutral counterexample.

A routing graph or hypergraph remains a useful proposal instrument once its labels,
coverage, and geometric implications are justified.
Begin with the seven-mark availability patterns and the already excluded selections,
then choose one surviving geometric obligation.
Broad contact enumeration has not earned priority over that smaller comparison.

**Stop and scope.** One frozen comparison with complete domain decisions.
A fixed-pose exclusion can justify a positive-width owner cell; it is not that cell’s
proof. A common owner stops that pair, without closing other pairs.
A combinatorial cover supplies a physical theorem only with complete transfer from every
physical packing and independently verified geometry.
Segment/angle helpers remain a subsequent route when a specific incidence cell supplies
the missing resource inequality.
Other retained structural inputs include the snug-parent/contact-path alternative and
[H-134’s ten-segment unavoidable set](../hypotheses/H-134-eleven-mark-ownership-set.md).
Neither supplies an exclusion without its own complete geometric argument.

### 5. Threshold Charges on a Residual Domain

[H-155](../hypotheses/H-155-conditional-threshold-cover-on-an-owner-class.md) remains
open. T-025 supplies the unconditional counting rule, and T-023 supplies one admitted
conditional residual construction.
The neutral endpoint-patch survivor family blocks point covers below the residual
requirement, but it violates a two-of-three capacity at charge $5/4$ against budget one.
It therefore does not obstruct the richer conditional threshold language.

**Discriminator.** After restricted-domain gate admission, freeze one qualifying
four-owner class, occupied region, site bundle, full 361-direction source, and a
complete point baseline at least seven.
A threshold certificate below seven with both decision routes and the physical transfer
excludes that class.
Selecting the class using the new mark or parent premises requires admitting the
resulting domain first.

X-027’s mixed angle-count comparison is a related alternate use of existing atoms: hold
the language fixed while comparing uniform and class-specific demands, then hold the
proved profile fixed while comparing points and thresholds.
Do not conflate a demand improvement with a language improvement, or use rounded angle
labels in place of the proved physical-to-core classification.
This is a separately registered eleven-core profile comparison under
[H-131’s exact angle-count premises](../hypotheses/H-131-near-axis-counts-at-q.md); it
does not inherit BC330’s four-owner residual domain or seven-unit budget.

**Stop and scope.** One class and one frozen candidate after admission, within BC330’s
registered allowance.
An escaped core rejects the candidate packet only.
A mass-seven family feasible for the whole declared language obstructs that fixed
residual problem.
Neither rejects H-155’s existential claim or settles selection routing.
Matching two cut maxima on one survivor family is not a matched optimization or runtime
comparison.

### 6. Exact Full-Support Pricing as a Prepared Reserve

[H-135](../hypotheses/H-135-paired-full-support-pricing.md) compares the first 32
positive rationalized dual rows with the full positive support from one LP solve on the
exact unit-square transport of BC232. That state is distinct from A6’s shrunken-core
program. The accept rule is an absent complete symmetry orbit with same-point exact
depths satisfying $d_{32}\le1<d_{\mathrm{full}}$.

**Discriminator.** Publish BC331’s fresh forward protocol, retaining the original
source, one solve, rationalization, selected-candidate rule, and 30-minute process
allowance. Replay the exact membership and orbit absence.
A hit identifies information lost by truncation and proposes a column.
At H-135’s frozen $q=96/25$, X-027’s transported mass-eleven family rules out an
unconditional point certificate below eleven.
Turning a pricing hit into a stronger bound therefore requires a side below $L_*$,
richer charges, or a justified restricted domain, followed by the corresponding
re-optimization, complete coverage, and physical transfer.

**Stop and scope.** Keep the one-candidate contract and its external grace.
Timeout, line-pair refusal, missing output, an existing orbit, or failure of the paired
inequality leaves H-135 unresolved.
A no-hit does not establish that truncated pricing suffices or that another state
contains no useful missing site.

### 7. A Constructive Challenge Outside Trump’s Local Class

The [exact local result](../hypotheses/H-026-trump-first-order-rigidity.md) verifies the
128 derivative-distinct one-sided cones and supports Trump’s local isolation and strict
local side optimality.
It does not exclude distant contact classes.
[H-018](../hypotheses/H-018-basin-entry.md) measured finite-refiner behavior, so its
return rate must not be reused as a basin-width estimate.

**Discriminator.** Select a different contact signature with a stated reason to try it,
freeze a source-bound proposal budget, and search that signature.
A numerical improvement is a candidate.
Reconstruct exact or interval-certified coordinates and independently verify all walls
and pairwise non-overlap before changing the upper bound.
Retain the best valid packing and tested signature even when it does not improve Trump.

**Stop and scope.** One signature, one fixed proposal budget, and one reconstruction
attempt in its own allocation.
Collapse into a retained Trump branch ends this proposal; a rejected verifier premise
invalidates it. Failure within a search budget leaves other signatures and unsearched
parameters open.
It supplies no evidence of global optimality or a quantified probability
of finding a better packing.

## Preserved Questions and Reopening Conditions

The compact two-attainer proposal remains a diagnostic, conditional on a strict replay
showing two disjoint cores missing the fixed five-site set.
Such a pair forces at least two units of added nonnegative point mass if each must
collect one; the available-mass premise needed for a cover contradiction is separate.
Stronger owner domains require fresh membership and common-owner checks.
The intersecting retained escapes are not already that pair.

The following disposition avoids repeating decided tests while retaining alternatives:

- Keep BC329 as the selected direct-bound continuation after admission.
- Keep BC337 as the separate unary-domain continuation; do not rerun exp156 at TR to
  measure parent gain.
- Preserve weighted traces, support updates, joint-owner geometry, mixed angle profiles,
  conditional thresholds, full-support pricing, and construction as separately
  selectable questions with their own controls.
- Reopen the full-unit fractional-existence question at a smaller frozen side or with a
  changed capacity family.
  Existence of fractional mass eleven on $[3.83,3.85]$ is already settled by the
  [exact transport](../../../docs/project/research/research-2026-09-10-x027-fractional-duality.md).
- Reopen a named neutral residual case when an additional parent, mark, joint, contact,
  or charge premise changes its domain.
  Relabeling or refining the same obstructed patch alone does not discharge the global
  routing obligation.

The old instruction to run the original rank 1 or rank 2 next is superseded by this
mapping and the active agenda.
Future execution must select and prospectively register one ready discriminator.
Preserving an option here records its scientific question; it does not spend an
experiment allowance or convert a draft preference into evidence.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
