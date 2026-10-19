---
title: X-030 — draft n11 proof obligations after the T1 local witness
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-030
  title: Draft N11 Proof Obligations After the T1 Local Witness
  date: '2026-09-13'
  author: GPT-6 Astra, reconciling the reviewed post-T1 strategy analysis
  campaign: packing.squares
  brief: >-
    Preserve the post-T1 strategy analysis as a draft exploration, state the exact
    parent-union lemma and bounded discriminators, and separate local mathematical
    decisions from complete routing and a stronger global lower bound.
  sources:
  - packing/campaign/explorations/X-028-n11-strategy-portfolio-draft.md
  - packing/campaign/explorations/X-029-bc303-t2-exact-geometry-draft.md
  - packing/campaign/hypotheses/H-159-bc303-one-corner-surplus.md
  - packing/campaign/hypotheses/H-161-bc303-literal-parent-union.md
  - packing/campaign/hypotheses/H-160-bc303-t2-charge-filters.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-159-bc303-literal-parent-union.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-158-bc303-t2-charge-filters.md
  - docs/project/reviews/review-2026-09-13-bc303-parent-union-math.md
  - docs/project/reviews/review-2026-09-13-bc303-literal-parent-union-result.md
  - docs/project/research/research-2026-09-13-bc303-literal-parent-union-result.md
  - docs/project/research/research-2026-09-12-n11-selection-routing-first-principles.md
  - docs/project/research/research-2026-09-13-bc303-t2-charge-bridge.md
  - docs/project/reviews/review-2026-09-13-bc303-t2-charge-reader-readmission.md
  - docs/project/reviews/review-2026-09-10-n11-bc329-packet-preflight.md
  - packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md
  proposes: []
---
# X-030: N11 Proof Obligations After the T1 Local Witness

**Status: draft exploration.** This analysis reconciles the T1 and T2 local branches
with the later H-161 literal-parent result.
It runs no additional scientific target.
The parent-union inequality and its integer thresholds have an
[independent mathematical review][parentreview]; the local parent mass has an
[independent result audit][parentaudit]. Broader geometric implications remain separate
questions.

T1 rejects one local BC303 surplus inequality.
It does not reject local availability restricted to actual eleven-parent packings, the
owner-selection strategy, or a stronger geometric restriction.
The retained result remains the ordinary proved exact lower bound

$$
s(11)\ge C=
\frac{955000\sqrt{518400042893309449}}{179696714646249}
=3.826447410572939744\ldots
$$

at V4/C5. The separate strict endpoint question, $s(11)>C$, is undecided by this
argument. [T-026][t026] proves exclusion below its limiting endpoint through strict
rational dilations; it does not assert a certificate at that endpoint.

## Evidence Before Priorities

The source revisions matter: T1 and T2 began as sibling worktrees above PR156. H-161 was
measured later on T1 and merged with T2 geometry for this exploration.
A review of one inspected revision does not admit later code on another branch.

| Source at the inspected revision | Established evidence | Remaining implication |
| --- | --- | --- |
| [T-026 claim][t026] and [mapped review][t026review], T1 tree `375c7bc1d49c506636a5abf71d37a8455888ff42` | Complete finite certificate decisions, strict-core counting, exact dilation, and mapped review establish $s(11)\ge C$ at V4/C5 | A new endpoint needs a new complete exclusion; strictness at $C$ is separate |
| [T1 reader review][t1] and [H-159][h159], same tree | The authenticated 377-row scan gives $\mu(C_0)=800003/800000$, surplus $g=3/800000$, and labels $\lbrace3,4,11,12\rbrace$ for parent $Q_0=[0,1]^2$ | This local parent is not known to extend to eleven parents; no continuous minimum or global routing conclusion follows |
| [H-161][h161], [exp-159][exp159], and [result audit][parentaudit], execution tree `f27c8ec7c8ebeb8a9b369c1c6f7efef4b531c359` | An exact one-run scan gives $N=4000015$ for $Q_0$ and $4N=16000060$ for four separated D4 copies; both necessary tests survive with $1048233$ integer units of slack | No extension, pose-cell exclusion, owner selection, or improved global bound follows |
| [X-029][x029], [charge bridge][bridge], and [bridge review][bridgereview], T2 tree `820e5355bdeaea122705e69f244c15725e66ec51` | Reviewed reductions of complete C geometry, its open-cell charge decision, opposite-corner separation, and a sufficient S test; exact uncharged C/S feasibility controls | C/S target charges and T2 are uncomputed in these sources; reader admission is distinct from the mathematical reduction |
| [H-160][h160], [exp-158][exp158], and [reader readmission][t2readmission], repaired reader tree `0f20fdcdd5bac7e0734b29cd0b0efef4ffea3699` | The target-free reader passed an independent exact source/replay and all-strata readmission after two documented defects were repaired | The registered C/S charge target has not run; the merged execution head still needs its own source/readiness check before that one run |
| [BC329 preflight][bc329] and [run-sheet plan][runsheet], PR156 tree `9c56e9019b97be0511d5afe590790b362b93e9e4` | An exact geometric endpoint above $C$, conditional on this packet’s coverage; instrument and control contracts | No BC329 scientific coverage outcome is assumed here |
| [X-028][x028] and [certificate analysis][mechanisms], T1 tree | Scoped fractional obstructions, the distinction between cutting a family and improving a complete program, and separate structural alternatives | Neither finite support failure nor a local counterexample exhausts a method |
| [Weighted admission record][weightedstate], PR157 tree `876c594521ba61840cf68d732b0a795f8d24e378` | Token representation and retained source replays, with implementation review corrections recorded | At this inspected revision, coverage controls and the paired-program stage remained unadmitted; no BC327 target gain follows |

The [reviewed parent-union lemma][parentreview] follows from strict-core geometry and
the imported BC303 floor.
H-161 evaluates one literal parent mass; other parent poses and the T2 source charges
remain uncomputed in the cited results.
Prioritization at the end is a judgment about readiness and logical information, with no
estimated success probability.

## What a Stronger Bound Must Prove

A universal certificate must cover a domain to which every physical parent can be
transferred by one admitted strict-core selection.
The counting theorem then excludes the whole packing.
A finite list of undercharged or covered placements cannot supply the missing universal
domain statement. [T-026][t026]

For the geometric route, let $P$ be an equipped eleven-parent packing at $q=96/25$, and
let $A_c(P)$ contain every available closed label at corner $c$. For the two currently
certified tuples,

$$
G_0=\lbrace(0,0,0,0),(15,15,15,15)\rbrace,\qquad
\Gamma(P)=\prod_c A_c(P).
$$

The missing assertion is

$$
\forall P,\qquad \Gamma(P)\cap G_0\ne\varnothing.
$$

The accepted [routing analysis][routing] splits it into local availability,
$A_c(P)\cap\lbrace0,15\rbrace\ne\varnothing$ at each corner, and consistency of forced
types: no two corners offer opposing singleton choices.
T1 was a sufficient local surplus mechanism for the first assertion.
T2 is a different sufficient mechanism for the second.
Even a complete positive T2 result leaves the first assertion open.

A normalized proof may quantify only over S1 representatives, provided cores and owners
are selected after normalization.
It must retain all physical angles and the named wall chart.
The sixteen maximal availability products avoiding $G_0$ have three physical D4 types
but ten orbits in the fixed left/bottom chart.
These are complete combinatorial remainders with continuous geometric obligations.
[Routing analysis][routing]

## Exact T2 Decisions Already Specified

Let $W=4000000$, $\varepsilon=524199/2000000$, and $w=106251/800000$. The imported BC303
floor is $W\mu(C)\ge4000015$, so every selected core has surplus at least $g=3/800000$.
A forced-0 full corner is either one co-owner C or two split owners S. In the closed
symmetric equipment domain, the minimum full-corner surplus $A$ satisfies

$$
\text{all adjacent and opposite T2 inequalities hold}
\iff A>\varepsilon/2.
$$

Opposite-corner copies coexist with a proved positive separation; this makes a
low-surplus full-corner witness a rejecting opposite pair.
The remaining exact queries are therefore C mass at most $4524199$ or S total mass at
most $8524199$, in integer units $W\mu$. [X-029][x029]

The smallest complete test of the registered C and S first-owner filters is their shared
all-chart sweep. Its target-free reader has been
[independently readmitted][t2readmission] at the repaired reader revision; no C or S
target charge has been measured.
C accepts only if every feasible cell has mass at least $4524200$. S accepts from its
sufficient relaxation if every first-owner strip cell has mass at least $4524185$,
because the second owner contributes at least $4000015$. A lower strip cell fails only
that sufficient relaxation; it is not a jointly realizable S witness.
C keeps all 182 source charts, 181 distinct orientations, the forbidden axis edge, and
the exact strict open-cell wall test.
Joint S boundaries cannot be discarded using C’s interior-density proof.
[Charge bridge][bridge], [independent review][bridgereview]

One disclosed candidate is a smaller *one-sided* test after integrated-head reader
admission. A low C charge, with exact physical-parent replay, rejects the C helper.
A low S first-owner charge rejects only the sufficient S filter; it does not supply a
joint S witness. A high charge leaves the corresponding complete domain unresolved.
These are disclosed-candidate checks, not target-blind discovery.
An opposite T2 rejection does not determine adjacent-only T2.

## Stronger Geometric Information Beyond T1

### Core surplus alone still admits four bad corner owners

**Deduction from the retained T1 witness.** Transport $Q_0=[0,1]^2$ and its selected
core to all four corners using $I,H,V,HV$. The four parents are separated because $q>2$,
co-own all eight marks, and each has neither certified local type.
D4 invariance gives total owner-core surplus $4g$. Even adding the necessary floor for
seven omitted cores gives only $11g<\varepsilon$.

Thus a universal four-corner inequality using only these owner-core surpluses cannot
exclude this local tuple.
This is a simultaneous four-parent counterexample to that particular resource mechanism.
It is not an eleven-parent packing or a counterexample to routing.
The [T1 review][t1] supplies the exact local mass and weighted symmetry; the
[routing analysis][routing] supplies the corner transports and their scope.

### Charge the parent union and its unavailable atoms

**Reviewed analytic lemma.** In an actual packing, let $I$ be any set of $k$ distinct
parents, and put $Q_I=\bigcup_{i\in I}Q_i$. Then

$$
\boxed{\mu(Q_I)-k+(11-k)g\le\varepsilon.} \tag{P}
$$

**Proof.** If two full-dimensional closed squares have disjoint interiors, the closed
first square cannot intersect the interior of the second.
Otherwise an open ball in the second would meet the first square’s interior.
Each outside selected core lies strictly inside its own parent, so $Q_I$ is disjoint
from every outside core.
The outside cores are also disjoint from one another.
Nonnegative additivity and the BC303 floor give

$$
\mu(Q_I)+\sum_{j\notin I}\mu(C_j)\le M,
\qquad M=11+\varepsilon,
$$

which implies (P).

Equivalently, atoms in $Q_I\setminus\bigcup_{i\in I}C_i$ must be unused by every
selected core. They can be added to the surplus account.
Count the parent **union**, not the sum of parent masses: legal parent contacts may
share weighted boundary sites.
If $Z$ is a set of marks proved globally unowned, $Q_I\cup Z$ may replace $Q_I$; the
union prevents charging the same unavailable atom twice.
This uses parent occupancy as unused mass, rather than assuming that a parent footprint
belongs to its selected core.

**Completed literal discriminator.** The source-bound H-161 scan of all 377 atoms over
the disclosed parent $Q_0$ returned $N=W\mu(Q_0)=4000015$. It decided two preregistered
necessary conditions:

| Frozen local configuration | Necessary condition for an eleven-parent extension | First rejecting $N$ | Measured result |
| --- | --- | ---: | --- |
| The one literal parent $Q_0$ | $N+10(4000015)\le45048398$ | $5048249$ | $N=4000015$; survives with $1048233$ units of slack |
| Its four separated D4 corner copies | $4N+7(4000015)\le45048398$ | $4262074$ | $4N=16000060$; survives with $1048233$ units of slack |

All 19 source atoms captured by $Q_0$ already lie in its selected strict T1 core; this
parent adds no source atom on the frozen pose.
The result rejects H-161’s predicted literal nonextension.
Passing a necessary inequality does not construct the seven missing parents.
It says nothing about the mass of other parent poses, and it gives no uniform lower
bound over a pose cell.
An eventual pose-cell exclusion would need such a bound, including its boundary
behavior. [Result][parentresult], [audit][parentaudit]

### Shared residuals, contact restrictions, and different selections

The following alternatives impose different mathematical requirements:

| Restriction | Smallest exact prospective discriminator | Scope and next missing implication |
| --- | --- | --- |
| One owner compatible with two residuals | Freeze two individually compatible residual poses from one named survivor source and one owner domain; decide whether their two compatibility sets have empty intersection, using the same parent centre and angle | Empty intersection excludes that joint pair. It does not exclude every residual pair or the owner class. A surviving pair needs an actual simultaneous parent witness. The [routing analysis][routing] proves why exchanging these quantifiers fails. |
| Complete parent avoidance in one residual direction | BC337’s exact all-owner-incompatible TR region, compared with the old common patch on the same open residual-centre domain | A strict gain identifies new geometry; the new centre-space obstacle must not be Minkowski-expanded again. A full-net residual certificate and selection remain separate. Exp156’s already B-only-incompatible TR witness is not a new parent-gain test. [X-028][x028] |
| Normalized contact information | Choose one of the ten fixed-wall blocker orbits, retain an explicit contact-incidence cell and all its continuous parent variables, and prove a surplus/parent-union or residual-budget contradiction over that entire cell | This can exclude one normalized cell. S1 does not discretize angles, fix the good labels, or yield a prescribed short path. Sharing a contact chain forbids adding path-length lower bounds as if the chains were disjoint. [Routing analysis][routing] |
| A larger certified tuple family | Freeze one additional full owner class and independently certify its complete residual domain; then recompute the maximal products avoiding the enlarged $G$ | Enlarging $G$ can weaken the required selection theorem. One fixed-pose cover does not admit a full label, and all new label transports require their physical transfer proof. [Routing analysis][routing] |
| Alternative equipment selection | Freeze a new snapping/selection rule and test all permitted choices for one obstructing parent before claiming it rescues a bad label | The eventual theorem is existential in a *coherent* allowed equipment choice for each physical packing. A different choice for each constraint is invalid. The literal T1 witness does not by itself decide a changed equipment domain. [T-026][t026], [routing analysis][routing] |

For a parent-union or residual exclusion to prove global local availability, its
complete domain must cover every missing-choice owner configuration that can occur in an
actual packing, including co-ownership, split ownership, one missing mark, angle seams,
and all valid signed frames.
Strengthening a relaxation helps only when this physical transfer remains true.

## Other Routes to an Improved Bound

Each row below changes a different part of the implication chain.

| Route and missing implication | Smallest high-information exact discriminator | What the outcome can establish |
| --- | --- | --- |
| BC329: complete coverage of one fixed finer-net packet | At its frozen sites and relative weights, determine exact raw minimum $m$ and compare with $M_0/11$, where $M_0=685457679/62500000$ | $m>M_0/11$ permits normalization; both complete coverage routes and dilation replay must then agree on the same bytes. A valid core with charge at most the threshold rejects this packet’s common scaling. Timeout is unresolved. The conditional endpoint is $3.826721480476156460\ldots$. [Preflight][bc329] |
| Reoptimized weights or different core/net geometry: extend beyond that packet | If a BC329 refuter is obtained, freeze its exact membership/admissibility breakpoints over the improving core-size interval; alternatively freeze one exact common program with old and changed weights | A persistent refuter excludes only the traced parameter interval. A finite improved primal/dual pair establishes that finite program’s gain; complete geometric coverage remains necessary. An inserted direction or direction-dependent core needs its own full angular transfer. [Strategy audit][audit] |
| Weighted threshold language: geometric expressiveness and replacement supports | Freeze one seven-token, threshold-four five-site motif; compare its realized traces with all 80 ordinary atom types on those five sites | An exact dual bound above one on traces with realizing cores proves a local advantage. A cost-at-most-one ordinary mixture must dominate on the *complete* realizable trace universe to show no advantage. The abstract $4/3$ ratio and source-family charge $3/2$ do not decide the global program. [Weighted review][weighted], [certificate analysis][mechanisms] |
| Added atoms improve a finite optimum: remove the whole old optimal face | On one authenticated common row/column manifest, test whether an exact old optimal dual survives every new capacity | A surviving optimum proves a finite tie; incompatible new capacities across the entire old optimal face force a strict finite improvement under the stated finite LP assumptions. Cutting only the solver’s returned family is insufficient. Afterwards update supports and verify complete coverage. [Certificate analysis][mechanisms] |
| Angle-count demands: exploit a proved nonuniform composition | Freeze one exact cell partition and a necessary count set $\mathcal N$ containing every physical profile; compare one same-language certificate against $\min_{n\in\mathcal N}\sum_jn_jd_j$ | Budget below that minimum, with complete per-class charge $d_j$ and physical classification, excludes the packing. A proof that $n_0\le9$ does not assert $(n_0,n_1)=(9,2)$; that vector minimizes demand only when $d_0\le d_1$. [H-131][h131], [certificate analysis][mechanisms] |
| Conditional thresholds: beat a point obstruction on one residual class | After restricted-gate admission, freeze one four-owner class, its full 361-direction source, and a complete point baseline at least seven; seek one threshold certificate below seven | A complete accepted threshold certificate excludes that class. The retained neutral family already violates a two-of-three capacity, so it does not obstruct this language. A single escaped core rejects that candidate only. Global selection remains required. [X-028][x028] |
| Geometrically tighter atom budgets: use joint realizability in the capacity proof | Freeze one atom with ordinary budget at least two and one admitted domain; decide whether two simultaneously realizable residual parents can both trigger it | A complete exclusion reduces that atom’s permitted simultaneous count on that domain. Independently feasible positive traces are insufficient. A surviving pair refutes only the proposed budget-one reduction; it does not invalidate the atom’s ordinary resource bound. The disjoint-trace theorem in [T-026][t026] supplies the baseline; this stronger-budget test is proposed here. |
| Full-support pricing: detect information lost by truncating a dual family | BC331/H-135’s one-candidate exact comparison $d_{32}\le1<d_{\mathrm{full}}$, including same-point geometry and absent orbit | A hit proposes a new point orbit; it does not prove a cover improvement. The full-unit mass-eleven family at $L_{\ast}=38200/9977$ blocks unconditional point certificates there and above, so a useful continuation needs a smaller side, richer charges, or a justified restricted domain. [X-028][x028], [strategy audit][audit] |
| Improve the upper bound constructively | Select a different contact signature and one prospectively bounded proposal search; reconstruct the best candidate and independently verify all walls and parent pairs | One valid packing below the retained upper bound improves it. Trump-local rigidity and a failed finite search do not settle other signatures or global optimality. [X-028][x028] |

The weighted and finite-program rows are sequential questions rather than
interchangeable success criteria.
PR157’s representation progress permits later admission work; it does not replace either
scientific comparison.
Every exact reader needs the complete source atoms/rows, direction and boundary policy,
and executing implementation identity bound to its receipt.
A second implementation of rational arithmetic is source independence; it is not
automatically distinct-method confirmation.
[T1 review][t1]

## Priority From This Evidence

1. Complete the already selected BC329 admission and frozen packet chain.
   It has a direct specified chain from complete coverage to an ordinary improved lower
   bound, because the counting and dilation theorem already exist.
   No terminal BC329 result is assumed.
2. Check source identity and readiness on the integrated C/S reader head, then run the
   one preregistered H-160/exp-158 target.
   Independent readmission accepted the target-free repaired reader, not a charge
   result. A complete C answer and either a sufficient S proof or a precisely delimited
   joint S remainder would inform forced-type consistency; the availability theorem
   would remain separate.
3. Reframe the parent-union route after H-161. The literal $Q_0$ scan is complete and
   did not reject. A changed parent pose, a set of proved unavailable marks, or a larger
   joint parent union could charge different source atoms; each proposal needs a frozen
   exact comparison and a separate argument connecting its domain to every physical
   packing branch it claims to cover.
4. Keep the weighted geometric trace test as an independent route after its required
   admission, and select broader joint-owner, contact, or residual-class work only with
   one complete frozen domain and a stated route to the selection theorem.
   These choices have more open proof implications than BC329; that is not evidence of a
   lower chance of eventual success.

Beyond the recorded H-161 result, this note supplies no scientific target, new lower
bound, probability estimate, or method-wide exhaustion claim.

[t026]: ../../cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md
[t026review]: ../../../docs/project/reviews/review-2026-09-10-t025-t026-verifiable-claims.md
[t1]: ../../../docs/project/reviews/review-2026-09-13-n11-bc303-t1-reader-final-math.md
[h159]: ../hypotheses/H-159-bc303-one-corner-surplus.md
[x029]: X-029-bc303-t2-exact-geometry-draft.md
[bridge]: ../../../docs/project/research/research-2026-09-13-bc303-t2-charge-bridge.md
[bridgereview]: ../../../docs/project/reviews/review-2026-09-13-bc303-t2-charge-bridge.md
[bc329]: ../../../docs/project/reviews/review-2026-09-10-n11-bc329-packet-preflight.md
[runsheet]: ../../../docs/project/specs/archive/plan-2026-09-13-n11-bc329-three-profile-run-sheet.md
[x028]: X-028-n11-strategy-portfolio-draft.md
[routing]: ../../../docs/project/research/research-2026-09-12-n11-selection-routing-first-principles.md
[mechanisms]: ../../../docs/project/research/research-2026-09-10-x027-certificate-mechanisms.md
[weighted]: ../../../docs/project/reviews/review-2026-09-10-n11-weighted-five-site-atoms.md
[weightedstate]: https://github.com/jlevy/squares/blob/876c594521ba61840cf68d732b0a795f8d24e378/packing/campaign/agent-sessions/session-127-weighted-five-site-atom-admission.md
[h131]: ../hypotheses/H-131-near-axis-counts-at-q.md
[audit]: ../../../docs/project/reviews/review-2026-09-12-n11-post-bc329-strategy-audit.md
[parentreview]: ../../../docs/project/reviews/review-2026-09-13-bc303-parent-union-math.md
[parentresult]: ../../../docs/project/research/research-2026-09-13-bc303-literal-parent-union-result.md
[parentaudit]: ../../../docs/project/reviews/review-2026-09-13-bc303-literal-parent-union-result.md
[h161]: ../hypotheses/H-161-bc303-literal-parent-union.md
[exp159]: ../series/series-000-smoke-and-calibration/experiments/exp-159-bc303-literal-parent-union.md
[h160]: ../hypotheses/H-160-bc303-t2-charge-filters.md
[exp158]: ../series/series-000-smoke-and-calibration/experiments/exp-158-bc303-t2-charge-filters.md
[t2readmission]: ../../../docs/project/reviews/review-2026-09-13-bc303-t2-charge-reader-readmission.md

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
