---
title: X-027 — fractional obstructions and structural proof mechanisms
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-027
  title: Fractional Obstructions and Structural Proof Mechanisms
  date: '2026-09-10'
  author: GPT-6 Astra coordinator, with independent Astra mathematical lanes
  campaign: packing.squares
  brief: >-
    The owner requested a new analytical exploration after Stromquist's September 7
    and 9 correspondence was archived in PR153. Explain the recent certified advances,
    examine the structural constraints that open other proof routes, develop
    fractional-packing and related mathematical ideas in independent spikes, and
    consolidate a strategic comparison with explicit evidence, falsifiers and next steps.
  sources:
  - SYNOPSIS.md
  - packing/campaign/ideas.md
  - packing/resources/private-correspondence/email-stromquist-2026-09-07.md
  - packing/campaign/explorations/X-023-three-losses-and-a-new-atom.md
  - packing/campaign/explorations/X-026-what-conditioning-does-and-does-not-buy.md
  - docs/project/research/research-2026-09-09-n11-evidence-and-inference.md
  - docs/project/research/research-2026-09-10-x027-fractional-duality.md
  - docs/project/research/research-2026-09-10-x027-structural-helpers.md
  - docs/project/research/research-2026-09-10-x027-certificate-mechanisms.md
  proposes: []
---
# X-027: Fractional Obstructions and Structural Proof Mechanisms

A covering proof past `L* = 38200/9977` needs a counting rule or a geometric relation
that ordinary point depth forgets.
Recent work has already made both kinds of progress: threshold charges produced T-025,
and owner restrictions produced T-023’s conditional exclusion.
Finer angular containment then carried the threshold certificate to T-026. This
exploration develops the next mechanisms and separates them from refinements that can
still give a smaller direct gain.

**Entry: W3 analytical exploration**, requested after the correspondence review, under
`think-jx95` and
[Session 126](../agent-sessions/session-126-stromquist-analytical-exploration.md).
The source baseline is `e0c2583e`, the merge of PR153. Three independent mathematical
lanes produced retained derivations and counterexamples, then cross-reviewed them.
Their new lemmas are independently reviewed arguments within this exploration; they are
not registered frontier results or claims of novelty.
No numerical target was run and no new packing bound is asserted.
The bracket remains

$$
3.826447410572939744\ldots \leq s(11)
\leq 3.877083590022814\ldots.
$$

The most consequential deductions are:

- The retained 88-core obstruction scales exactly to **full unit squares** of fractional
  mass eleven at `L* = 38200/9977`, approximately `3.8288`. It obstructs arbitrary
  unconditional point measures at that side and above, without a symmetry assumption.
  A new search for such a witness at `3.83–3.85` is unnecessary.
- An open-interior formulation gives a self-contained strong-duality argument, including
  equality with the continuous-density problem.
  Passing from dots to arbitrary density therefore does not evade that obstruction.
- At side `96/25`, a hypothetical packing must own at least **seven of eight corner
  marks**. An equivalent normalized packing has at most **three physical contact
  components**, so a contact path joins owners from different corners.
  These strengthen the inputs available to a helper argument.
- A five-site example separates a floor charge from every mixture of ordinary threshold
  charges by an exact factor `5/4` for a specified demand profile.
  Whether square geometry retains such an advantage is a well-defined next test.

## 1. What the Recent Results Actually Improved

A core is a smaller square placed strictly inside a hypothetical unit square.
A certificate charges every admitted core by at least one, using resources whose total
charge across disjoint cores is less than eleven.
It then excludes eleven unit squares.
The method has three distinct opportunities: lose less in selecting the cores, cover
them more efficiently, or use a stronger rule for sharing resources.

| Retained result | Lower bound | What changed |
| --- | --- | --- |
| T-018 | `3.81` | A complete ordinary point cover on 1,121 retained sites |
| T-022 | `3.810025723614703...` | Sharper angular containment and dilation of the same certificate |
| T-024 | `3.816609502788862...` | A finer net, larger cores, measured coverage, and common normalization of the same relative point weights |
| T-025 | `3.82` | A new integer counting rule: point atoms plus two-of-three threshold atoms |
| T-026 | `3.826447410572939...` | Re-certification of those threshold atoms on a finer net, followed by dilation |

The
[certificate analysis](../../../docs/project/research/research-2026-09-10-x027-certificate-mechanisms.md#what-produced-the-retained-gains)
links each exact proof and distinguishes direct rational-side exclusions from limiting
dilation statements.
T-022, T-024, and T-026 establish the displayed lower limits without deciding their
equality cases.

For frozen relative weights, let `M` be their original total resource budget and `m` the
least charge on a proposed core domain.
Common normalization succeeds exactly when `m > M/11`: multiply every weight by `1/m`.
The remaining geometric gain depends on core side and angular gaps.
A finer net’s geometric headroom is not a coverage result.

That is why **BC329 remains the next direct-bound target**. Its frozen `B = 0.9981`,
2880-step packet has a geometric limit `3.826721480476156460...`, but coverage is
unmeasured. It first needs the admitted bounded runner and the exact comparison of raw
least charge with `M/11 = 685457679/687500000`. The existing adaptive refinement CLI
performs a different experiment.
See the
[packet preflight](../../../docs/project/reviews/review-2026-09-10-n11-bc329-packet-preflight.md).
This remains worthwhile as a bounded continuation of a mechanism that has worked.

The structural line has a different achievement: **T-023 excludes one specified
four-owner branch at `3.84`**. Its exact full-net cover and geometric transfer are
retained. A global theorem still needs to show that every physical packing admits a
selection belonging to an excluded branch.
Later wall footprints enlarged twelve of sixteen classes, but exp147’s containment test
added no selection. Those outcomes do not measure the productivity of the two lines
against each other.

The
[combined evidence account](../../../docs/project/research/research-2026-09-09-n11-evidence-and-inference.md#12-the-combined-series-takeaways-and-open-comparisons)
is the historical authority.
X-027 adds deductions and prospective discriminators to that corrected account.

## 2. What Stromquist’s Fractional Suggestion Settles

### The full-unit obstruction is already retained by exact transport

The archived
[September 7 and 9 correspondence](../../resources/private-correspondence/email-stromquist-2026-09-07.md)
suggests weighted families of squares with depth at most one.
Such a family can obey every point capacity even though its squares cannot all occur in
one physical packing.
Integrating any point cover against the family bounds the cover’s total weight below.

The existing exact family has 88 closed squares of side `B = 9977/10000` in container
side `191/50`, each of weight `1/8`, with closed depth at most one everywhere.
Scaling all positions and sides by `1/B` gives unit squares in

$$
L_* = \frac{191/50}{9977/10000} = \frac{38200}{9977}
< \frac{383}{100}.
$$

The scaled family still has total weight eleven and closed depth at most one.
Any nonnegative point measure covering every legal unit square must therefore have mass
at least eleven. This includes asymmetric measures: in the full-unit problem, all the
family’s actual orientations are legal, so the old folded-net symmetry qualification is
unnecessary.
The same obstruction applies to any sound unconditional point-core selection
rule, since selecting a core inside each unit square only decreases depth.

The
[fractional derivation, §1](../../../docs/project/research/research-2026-09-10-x027-fractional-duality.md#1-exact-rescaling-already-answers-the-mass-eleven-question)
retains the source and independent certificate receipt.
A directly consumable full-unit export would be useful engineering; another existence
search at `3.83–3.85` would not.

**A strict physical integrality gap remains unproved.** The current physical lower bound
lies below `L*`. To prove that the fractional relaxation actually permits more squares
than physical packing at `L*`, we still need a physical exclusion there.
A global lower bound strictly above `L*`, for example `3.83`, would establish both a
stronger bound and this gap.
T-025 already demonstrates a matched gap in its declared closed-core model; the
unit-square statement is separate.

### Continuous density has the same optimum under a precise convention

Let `P_L` be the compact space of contained unit-square poses and use incidence
`x in interior(S_p)`. Packing measures live on `P_L`; covering measures live on the
container.
Define `nu_circle(L)` by maximizing packing mass subject to pointwise interior
depth at most one, and `tau_circle(L)` by minimizing covering mass subject to mass at
least one inside every legal square.

The independently reviewed argument gives

$$
\nu_\circ(L)=\tau_\circ(L)
=\inf(\text{finite atomic interior-cover masses})
=\tau_{\rm ac}(L).
$$

Here `tau_ac` is the absolutely continuous density optimum in the existing BC242
contract. The packing supremum is attained; no covering optimizer or finite optimal
packing is asserted.

The proof has four substantive steps.
Compactness gives a finite set of points hitting every pose interior, which uniformly
bounds packing mass.
Interior point capacities are closed conditions on weakly converging measures.
Finite sets of these constraints give exact finite LPs over all realized incidence
masks; compactness and finite duality identify their limiting value with the full
problem. Finally, any finite atomic cover has a uniform interior margin over the compact
pose space, so its atoms can be smeared into densities at unchanged cost.
Tonelli’s theorem and lower semicontinuity also show that closed depth at most one
almost everywhere is equivalent to interior depth at most one everywhere.
Full proofs and boundary counterexamples are in
[§§2–4 of the fractional analysis](../../../docs/project/research/research-2026-09-10-x027-fractional-duality.md#2-the-measure-spaces-and-the-boundary-convention).

This answers the value-equality part of the continuous question under explicit
hypotheses.
It does not classify equality at Trump’s side, compute the optimum at any new
side, or pair singular closed-square covers with almost-everywhere capacities.
Touching edges make that last combination unsound.

A second lemma supplies finite rational `k`-fold witnesses after **arbitrarily small
side enlargement**: shrink a compact pose partition to strictly interior representative
cores, rationalize with margin, and dilate.
Exact-side finite attainment is not proved.
The retained family already supplies a concrete `k = 8` witness at `L*`.

## 3. Stronger Charges: Test Expressiveness Before a Large Covering Run

An ordinary point atom counts one site.
An ordinary threshold atom counts whether a square contains at least `k` of a fixed set
of `r` sites, with budget `floor(r/k)` across disjoint squares.
It uses indivisibility of site consumption, which fractional point depth alone forgets.
The retained non-Helly three-square example shows this with exact rational unit-square
coordinates: pairwise overlaps allow fractional mass `3/2`, while a two-of-three site
capacity is only one.

The A6 plateau shows why merely finding one violated atom is insufficient.
A 64-placement family of mass eleven satisfies all point capacities and all 2,566
retained atom orbits on its declared domain.
Additional point sites cannot defeat that catalog.
Later cuts reduced a different, fixed 280-placement program to an exact upper value near
`10.421`, but the larger covering LP stayed numerically at eleven.
Its displayed lower candidate also violates full point depth, so it is not a new
fractional packing. The
[A6 admission](../../cases/n11_fractional_certificate/a6_dual_upper/README.md) preserves
these scopes.

### Weighted binary atoms and floor atoms ask different questions

Give site `s` a positive integer token count `a_s` and put `h(P) = sum_{s in P} a_s`,
`A = sum_s a_s`. The two globally valid charges are

$$
f_{\rm bin}(P)=\mathbf 1[h(P)\ge t],\qquad
f_{\rm floor}(P)=\left\lfloor\frac{h(P)}{t}\right\rfloor,
\qquad c=\left\lfloor\frac A t\right\rfloor.
$$

Disjoint core traces consume disjoint site tokens, proving both budgets.
The existing weighted motif `(2,2,1,1,1)` at threshold four has only seven tokens, so
binary and floor charges coincide there.
Its abstract `4/3` gain tests multiplicities, not genuinely multilevel floor values.

The new five-site example uses `f(T)=floor(|T|/2)` on all Boolean traces `T`. One floor
atom has budget two.
Every nonnegative mixture of ordinary threshold atoms on those same five sites
dominating this profile costs at least `5/2`, and point weights `1/2` at each site
attain it. An explicit fifteen-trace dual witness proves the lower bound.
This is an exact **profile-domination** separation of `5/4`; rows of demand two are
essential. It is not a measured improvement of a unit-demand square-cover LP. The
[certificate analysis](../../../docs/project/research/research-2026-09-10-x027-certificate-mechanisms.md)
gives the complete capacity table and proof.

The cheapest geometric test starts with one retained weighted five-site motif.
Admit the realizable site traces on its frozen core domain, then compare its charge with
the 80 ordinary threshold atoms supported on those sites.
Exact domination cost at most one over **all realizable traces** rules out its
multiplicity advantage over all ordinary atoms on those sites.
Its ordinary replacement could still add useful columns missing from the current
catalog. A witnessed realizable trace subset with cost above one proves that some local
advantage survives geometry.
Neither result settles the full covering budget.
A genuine floor test should likewise retain traces requiring multiple charge levels.

### Alternate atom and support changes; test the whole optimal dual face

The existing `think-yc80` continuation should alternate proposing atoms and updating the
fractional support, with full depth checks before calling a support an obstruction.
A finite LP dual vector can propose useful cuts even when it fails those checks, but it
supplies no packing impossibility claim.

One exact discriminator improves the interpretation of a stalled finite LP. Freeze its
old optimal value `v` and add proposed atom columns.
The new columns strictly lower the finite covering optimum **if and only if** no old
optimal dual solution satisfies all their new capacity inequalities.
Violating the particular dual returned by a solver does not establish this.
An exact feasibility problem on the old optimal dual face decides whether the new
columns matter to that finite control; omitted geometric poses remain a separate
obligation.

Higher-rank floor compositions are globally sound when built from already globally valid
integer charges: if `f_j` have budgets `b_j` and `lambda_j >= 0`, then
`floor(sum_j lambda_j f_j)` has budget `floor(sum_j lambda_j b_j)`. This creates a
precise future language.
It earns an implementation block after an explicit composition separates a retained
obstruction and has a complete geometric evaluation rule.
An arbitrary finite-support cut is insufficient.

## 4. Structural Helpers Now Have Stronger Premises

Stromquist’s helper arguments use more than a collection of dots: ownership and
incidence restrict what another square can occupy.
The current structural results make that approach concrete at eleven, but the relevant
owner choices must coexist in one physical packing.

### Seven marks, common surplus, and co-owned segments

At `q = 96/25`, the admitted BC303 measure has mass `M = 22524199/2000000`. Its eight
corner marks each have weight `w = 106251/800000`. Eleven disjoint selected cores
collect at least eleven units of this measure, leaving unused mass at most
`epsilon = M - 11`. Since

$$
2w-\epsilon=\frac{441}{125000}>0,
$$

at most one corner mark can be unowned.
Exact cross-corner distances prevent a core from owning marks at different corners.
Thus at least three corner pairs are fully owned; a full pair is either co-owned by one
core, which contains their joining segment, or split between two cores.
If `s` pairs are split, there are `4+s` corner-owner cores and `7-s` remaining cores.

The abstract zero-or-one-missing-mark patterns number `2^4 + 8*2^3 = 80`. These are
labels with continuous geometry still to decide, not eighty feasible packing classes or
a reason to launch eighty LPs.
With unused mass `U`, the exact shared accounting is

$$
U+\sum_{i=1}^{11}(\mu(C_i)-1)=\epsilon.
$$

If a geometry lemma forces a charge surplus for several distinct owners, their surpluses
and any missing mark must fit this **one** allowance.
Charging the same owner’s surplus twice would invalidate the argument.
The
[structural proof, §2](../../../docs/project/research/research-2026-09-10-x027-structural-helpers.md#2-seven-of-eight-marks-are-owned)
also retains counterexamples: co-ownership alone leaves a known neutral core, and split
ownership is locally realizable.
A useful next lemma needs the actual parent geometry, additional avoided marks, or a
strict common-surplus bound.

### Wall contact gives a finite component restriction

For two unit squares touching the left wall, their centre x coordinates differ by at
most `(sqrt(2)-1)/2`. Their open radius-`1/2` incircles are disjoint, so their vertical
separation is at least

$$
\eta=\frac{\sqrt{1+2\sqrt2}}{2}.
$$

Four such centres would span at least `3 eta > q-1`; therefore at most three squares
touch any wall, including vertex contact.
The admitted fixed-angle normal form S1 gives an equivalent packing whose every physical
contact component touches both left and bottom walls.
It consequently has at most three components, one containing at least four squares.

Select the corner owners **after** normalization.
Four distinct corner owners in at most three components force a parent-contact path
joining owners at two different corners.
The six unordered corner pairs provide endpoint types.
Neither a short path, positive-length contacts, common angles, rigidity, nor touching
strict cores follows.
The
[full proof and limits](../../../docs/project/research/research-2026-09-10-x027-structural-helpers.md#5-a-wall-has-at-most-three-touching-squares)
keep the normalization and the original packing distinct.

### Joint owner consistency is stronger than independent compatibility

Individual unit parents for an obstruction’s cores do not make those parents coexist.
Likewise, an owner compatible with residual square `R1` and an owner compatible with
`R2` need not be the **same** owner.
A pair test can expose this loss: each unary owner domain must be nonempty, but their
intersection can be empty.
It first needs a disjoint residual pair with positive unary controls.
Exp149 and exp151 are unsuitable: their cores intersect, and exp151 already fails the
complete TR unary test.

BC337 already proposes a stronger **unary** forbidden region derived from all allowed
owners. It remains blocked on its constructor, clipping, bounded runner, and independent
reader. It is not a new joint-consistency experiment.
Exp156 established old-model TR incompatibility for the saved exp151 pose, so repeating
a narrower parent-restricted TR test cannot show added gain.
Its frozen run leaves BL, BR, and TL untested.

Selection routing is another independent question.
Let `A_c(P)` be a physical packing’s available owner labels at corner `c`, and `G` the
set of excluded selections.
The global obligation is

$$
\text{for every physical }P,\qquad
\left(\prod_c A_c(P)\right)\cap G\ne\varnothing.
$$

Showing that one allowed selection survives says nothing about whether another available
selection is excluded.
The seven-mark constraints can reduce the abstract availability patterns that avoid `G`;
each remaining pattern still needs geometry.
This is an appropriate small combinatorial precursor to further conditional covers.

### Segment and angle profiles connect the two proof routes

For strict cores, segment lengths are additive resources.
For an owner of a mark on a segment, another disjoint owner restricts it to the
connected free portion accessible from that mark.
A uniform lower length demand exceeding this accessible capacity excludes the joint
incidence-and-angle cell.
Co-owned mark segments and split-pair incidence now supply a reason to select such
cells. The constants in Stromquist’s n6 helper cannot be carried to n11 unchanged.

The first test should derive exact formulas on one positive-width angle cell, including
facet changes and endpoints.
A midpoint violation is proposal evidence only.
If independently minimizing each owner’s demand loses the gap, a joint angle profile may
retain it on a proved compatibility relation.

Mixed angle counts offer a parallel certificate route.
Use one universal charge budget `M`, but class-specific lower demands `d_j`. A proved
count profile excludes the packing when `M < sum_j n_j d_j`; for a `(9,2)` branch this
is `M < 9 d0 + 2 d1`. The existing angle theorems use exact rational cell boundaries,
not rounded degree labels, and every physical unit-to-core assignment must respect those
boundaries. Two separate controls isolate the mechanisms: hold the charge language fixed
while comparing uniform and class-specific demands, then hold the profile fixed while
comparing point-only and ordinary-threshold charges.
A four-arm comparison would measure both effects and their interaction.
Existing charge types suffice before multiplicity machinery is built.

## 5. Ranked Continuations and Explicit Stop Conditions

This ordering is a judgment about readiness and information, not a measured runtime or
productivity ranking.
The numerical targets require prospective registration and maintained instruments.
`proposes: []` records that this analytical block promotes no new hypothesis or theorem
identifier.

| Order | Bounded next slice | What would change the decision | Stop or limit |
| --- | --- | --- | --- |
| 1, direct bound | Admit and run the already frozen BC329 packet | Exact least charge exceeds `M/11`, with the frozen normalization and independent covering evidence | An exact failing pose rejects this packet; timeout or incomplete coverage is unresolved. Neither closes re-optimization or finer nets generally |
| 2, language | Test one weighted five-site motif on admitted realizable traces against all ordinary atoms on those sites | A strict exact domination gap survives geometry; then compare a covering LP on a common control | No gap rejects its multiplicity advantage on that domain; ordinary replacement columns may still help the current catalog. A gap alone is not a global cover |
| 3, obstruction loop | Continue `think-yc80` with atom/support updates and an exact optimal-dual-face test | Added columns remove the whole old optimal face, or an admitted replacement depth-one obstruction survives | A cut of one support or one dual vector supplies no general closure |
| 4, structural | Apply the seven-mark premises to one source-bound co-owner geometry, or a disjoint pair with positive unary controls | Parent geometry, shared surplus, or common-owner consistency removes a witness that the matched weaker model admits | Fixed poses need positive-width continuation; co-ownership alone has a retained neutral counterexample |
| 5, profile | Test a proved mixed angle-count branch, holding language fixed for the demand comparison and profile fixed for the charge comparison | Class demands improve on uniform demands, or ordinary-threshold charges improve on points under the same profile | These are distinct effects; unproved angle assignments, exact-angle substitutes, or ignored profiles invalidate either comparison |
| 6, theoretical admission | Retain independent review of the interior-duality and finite-witness arguments; export the transported unit family if a consumer needs it | A maintained reader can consume the already proved transport; BC242 can use a precise value-equality theorem | This does not calculate the fractional optimum or classify equality |
| 7, next structural depth | One anchored component or segment/angle cell joining corner roles | Exact joint geometry yields a strict resource inequality on the whole cell | Graph counts, sampled contacts, and isolated orientations are insufficient |
| 8, richer closure | A genuine multilevel floor or higher-rank charge | A globally valid new charge separates an obstruction and has a complete pose evaluator | Abstract profile separation or finite-support cuts alone do not justify a full format expansion |

BC337 and its existing prerequisites remain the separate unary-domain continuation.
The new structural work should share its geometry tools when appropriate, while testing
a newly declared premise.
A new agenda can select two or three of these slices after instrument readiness is
known; X-027 is not an instruction to run every row at once.

## 6. Parked Questions, with Reasons to Reopen Them

- **Find fractional mass eleven at `3.83–3.85`.** Already answered by exact transport.
  Reopen for a smaller frozen side or a new capacity family, not existence in that
  range.
- **Replace point sites by unrestricted continuous density to cross `L*`.** The retained
  family and the duality argument block this unconditional method.
  Reopen with a richer charge or conditional domain whose witness membership is checked.
- **Split the same neutral endpoint patches again.** H-157’s six neutral subclasses are
  a result for that finite patch universe.
  Additional marks, parent consistency, segment demand, or selection routing could
  change the domain; relabelling it cannot.
- **Treat removal of one fractional support as a global breakthrough.** A5 and A6 show
  the replacement-support problem.
  Reopen only with full covering evidence or a theorem controlling every support on the
  declared domain.
- **Broad contact-graph enumeration.** The new component cap is useful, but it gives no
  rigidity or short-path theorem.
  Start with one complete component cell that changes a resource inequality.
- **Use n6 as evidence that five-dot failure implies weighted failure.** The letter
  concerns unweighted sites.
  A simple set-system counterexample separates those statements.
  N6 is still a clean physical-gap control: its proved `s(6)=3` means an exact
  fractional mass-six family below three would establish a gap immediately.
  A failed finite-support search would be inconclusive.
- **Conflate the author’s Figure14 repair with the repository’s verified repair.** The
  archived suggested `G=(0.8,s/2-0.05)` or `(0.8,1.845)` differs from the independently
  verified `G=(0.79,1.85)`. A paired exact replay would settle that historical detail;
  it is a lower-priority source-control question, not evidence for an n11 bound.
  The n18 priority and n26 relevance withdrawals likewise change attribution and scope,
  not the validity of the archived constructions.

## 7. Review Record and Research Disposition

| Independent lane | Retained report | Mathematical review |
| --- | --- | --- |
| Fractional packing and duality, Astra max | [Full-unit transport, continuous duality, finite witnesses, and controls](../../../docs/project/research/research-2026-09-10-x027-fractional-duality.md) | Structural and certificate lanes passed transport and duality; structural lane also checked the rational finite-witness lemma and explicit three-square control |
| Structural helpers, Astra max | [Seven marks, joint owners, contact components, and segments](../../../docs/project/research/research-2026-09-10-x027-structural-helpers.md) | Fractional and certificate lanes independently checked the BC303 arithmetic, ownership counting, wall bound, and normalized contact consequence |
| Certificate mechanisms, Astra extra high | [Recent gains, multiplicities, floor profiles, and optimal faces](../../../docs/project/research/research-2026-09-10-x027-certificate-mechanisms.md) | Structural lane and coordinator checked the five-site dual witness, global floor budget, and finite optimal-face criterion |

The coordinator checked the source scopes and consequential deductions, and assembled
the comparison. A separate integrated review found no mathematical blocker and prompted
four scope corrections: limit the introductory cap claim to sides past `L*`, distinguish
timeouts from exact packet rejection, preserve the possible usefulness of ordinary
replacement columns, and separate the angle-demand and charge-language controls.
Its broken structural-section link was also corrected.
The session record carries validation, resource usage, and the final review disposition.
The source reports preserve the full proofs and counterexamples so later numerical work
can cite an exact premise rather than a strategic summary.

The [idea board](../ideas.md#stromquist-fractional-and-structural-strategy--x-027)
retains the new shaped directions.
Existing direct-bound and unary-domain work keeps its existing identity.
The next implemented block should declare one mathematical question, the matched control
that isolates it, and the exact evidence that would justify expansion.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
