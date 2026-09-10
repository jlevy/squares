# N11 Research: Definitions, Findings, and the Inference Chain

**Scientific evidence cutoff:** the results published in
[PR145](https://github.com/jlevy/squares/pull/145) at
`2acf4b859d39e01cc9fcb1156d8573f65e08efbd`, through exp153 on September 9, 2026. The
subsequent two-attainer verifier and unit-parent constraints are preparation or analytic
proposals, not new measured outcomes.

**Interpretation and preparation updated September 10, 2026.** Exp153 remains the latest
scientific experiment.
The global bounds and T-023 are unchanged.

| Work | Current status | What that status establishes |
| --- | --- | --- |
| Exp145–153 | Recorded scientific results; PR145’s matching full checkpoint passed | The scoped findings in §7, with the retained analytic premises |
| This account | Narrative review passed; subsequent currentness and structure pass applied | The exposition preserves the reviewed distinctions; it is not a fresh proof of every premise |
| Fixed two-attainer instrument | Source admitted; twelve synthetic controls passed; target unrun | Reviewed preparation for one fixed construction, with no target separation result |
| Unit-parent centre bound | Derived and checked again by its originating lane | Conditional analytic reasoning; independent review, implementation admission and measured effects remain outstanding |

The [narrative review](../reviews/review-2026-09-09-n11-evidence-interpretation.md),
[pair source admission](../../../packing/cases/n11_five_dot_cover/two-attainer-source-admission.md),
and
[parent-bound author check](../reviews/review-2026-09-10-n11-parent-centre-author-check.md)
record these different assurance scopes.

This account follows an explicit order: define the problem and objects; identify the
selected evidence; state observations; expose the assumptions needed to interpret those
observations; derive only the conclusions they support; then describe unresolved
questions and possible actions.
A decision to test one hypothesis is recorded as a decision, not as evidence that
alternatives are less productive.

Read [§§1–6](#1-the-physical-problem-and-the-existing-bounds) for the definitions and
physical-to-relaxed model, [§7](#7-the-recorded-observations-in-order) for the
observations, [§§8–9](#8-why-exp153-decides-more-than-a-few-candidate-dots) for their
interpretation and pricing terminology, and [§§10–11](#10-what-is-not-yet-established)
for the gaps and possible next tests.

### Evidence Labels Used Here

- **Analytic implication:** a mathematical argument from stated premises.
  Derivation, independent review and mechanized verification are separate assurance
  facts.
- **Exactly computed:** the specified finite computation used exact arithmetic and
  satisfied its completion conditions.
  Its interpretation still depends on the domain reduction and source assumptions.
- **Numerical proposal:** floating-point evidence used to suggest a candidate; it is not
  yet an exact covering or packing certificate.
- **Partial:** the declared work did not finish.
  Retained sub-results keep their own scope; an incomplete search is not a universal
  negative.
- **Unrun:** no target result exists.
  Source code, controls, or an expired scheduling window do not supply a positive or
  negative scientific result.
- **Source admission:** a review of whether a proposed instrument implements its stated
  test. It is not the target outcome and is not a new physical theorem.
- **Strategic judgment:** a choice based on goals, assumptions and available evidence.
  It is revisable and should not be presented as measured comparative productivity.

## 1. The Physical Problem and the Existing Bounds

A **unit square** has side one.
It may translate and rotate inside a larger square container.
A **packing** permits boundary contact but forbids overlap of the interiors of any two
unit squares. A **pose** specifies one square’s centre and orientation; a
**configuration** specifies the poses of all the squares.

Write `s(11)` for the infimum of container sides that permit eleven such squares.
An **upper bound** comes from a valid construction.
A **lower bound** proves that containers below a specified side cannot contain eleven
squares. These are different proof tasks.

The retained project record gives

$$
3.810025723614703\ldots \leq s(11)
\leq 3.877083590022814\ldots.
$$

The lower endpoint is T-022; the upper endpoint is the exactly verified Trump
construction, T-011. The simpler introductory lower bound is T-018’s `3.81`. These are
the project’s retained verified claims, not a claim that this report has performed a
fresh exhaustive literature search.
See the [claim register](../../../packing/frontier/RESULTS.md) and
[tutorial](../../../TUTORIAL.md).

The recent conditional experiments use **q = 96/25 = 3.84** as a test container side.
A successful argument covering every hypothetical eleven-square packing at this side
would improve the lower bound.
A result about only one conditional branch, or about one proposed certificate, does not
do that by itself.

## 2. Why Smaller Squares and Finite Directions Appear

A **parent square** is one of the physical unit squares.
A **core** is a smaller square placed at the same centre, with side

$$B=9977/10000=0.9977.$$

The core’s orientation is selected from a finite set of exact rational directions,
called a **direction net**. A rational direction means that the components of its unit
axis vectors are rational; it does not mean that its angle in radians is rational.
**Snapping** selects a nearby net orientation while preserving the centre.

This is not justified by assuming a dense sample approximates every angle.
The retained argument bounds the angular mismatch and proves that the chosen closed core
lies strictly inside its unit parent.
Consequently cores selected from a physical packing are pairwise disjoint, including
their boundaries. This strict containment is also why an atom on a core boundary cannot
be counted by two packed parents.
The [tutorial’s finite-direction argument](../../../TUTORIAL.md) gives the shrink
inequality.

The unconditional symmetric certificate uses 181 folded directions.
The selected owner-patch work uses the complete 361-direction manifest appropriate to
that construction. These counts refer to different retained symmetry reductions.
At each direction, centres still vary continuously.

An exact check over all centres at a net direction requires a geometric reduction;
checking a few sampled centres would be a different, weaker test.

## 3. Dots, Weights, and the Counting Argument

A **site** or **dot** is a point.
An **atom** is a site carrying a specified nonnegative weight.
For sites `p_j` and weights `w_j`, the atomic measure

$$\mu=\sum_j w_j\delta_{p_j}$$

assigns a region the sum of the weights of all sites it contains.
Its **total mass** is `W = sum_j w_j`. A square **covers mass** when it contains those
sites, with the stated boundary convention.
A **weighted cover** requires every square in a declared family to cover at least some
positive mass `m`.

For pairwise disjoint cores `P_1,...,P_k`, nonnegativity gives

$$k m\leq \sum_i\mu(P_i)\leq W.$$

Thus a cover with `W/m < k` rules out `k` such disjoint cores.
Unit-weight dots are the special case `w_j=1`. Five unavoidable dots allow at most five
disjoint cores; six unavoidable dots allow at most six.
Equality `W/m = k` gives no contradiction.

The measure is defined on the whole container, but its mass may sit at finitely many
sites. There is no requirement to spread weight across every location.
Once occupied geometry is forced, a conditional argument can require coverage only of
the remaining admissible square family.
The reduction must follow from a proved condition, or every uncovered condition must
remain in an exhaustive case split.

A floating-point optimization can propose sites or weights.
Rationalizing those numbers does not establish validity.
The rational candidate must then satisfy the complete required coverage constraints
under the declared geometry.
Exact arithmetic removes rounding ambiguity in that check; it does not remove the need
to prove that the checked family is the right one.

## 4. What Is Actually Forced Near the Corners

A **mark** is a specified point used in the ownership argument.
Here the marks are near the corners, not at the four corners themselves.
For example, the bottom-left pair is

$$
(3152/3175,2336/3175),\quad(2336/3175,3152/3175).
$$

An **owner** is a selected core that contains a mark.
A parent containing a nearby mark is not automatically an owner in this precise sense:
the retained argument concerns mark containment in the selected core.

There is a general ownership premise in the retained work.
At `q=3.84`, an auxiliary weighted measure has total mass `11.2620995` and verified mass
at least one in every required core.
In a hypothetical eleven-square packing, at most `0.2620995` mass can remain outside the
eleven selected cores.
Each corner pair has mass `0.2656275`, larger than that allowance.
At least one mark from each pair must therefore lie in a selected core.
Cross-corner mark distances exceed a core’s diameter, so these four owners are distinct.
The source gives exact fractions and the positive margin `0.003528`:
[corner-pair replay](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/bc-303-first-wave-selection.md#3-replay-of-the-corner-pair-theorem-lane-c)
and
[sector derivation](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/corner-owner-sector-footprints.md).

This forces four owners.
It does **not** force four squares into the container corners, force their edges to
touch the walls, or prove that an arbitrary optimum can be moved into such a
configuration. Those would be additional geometric statements.

An **owner class** records a choice of owned mark and a closed sector for signed core
axes directed toward the centre from that mark.
Two mark choices and eight sectors give sixteen classes per corner.
It does not specify one square pose.
Closed classes can overlap on boundaries, and a core can own both marks without becoming
two owners.

An **owner tuple** selects one class at each corner, in the declared order bottom-left,
bottom-right, top-left, top-right.
There are `16^4 = 65,536` raw labels.
This is neither a count of feasible packings nor a probability distribution.
The labels cover possible choices under the ownership premise, but some labels may be
impossible and some physical configurations may receive more than one label.

## 5. Guaranteed Footprints and the Relaxed Residual Family

A **common footprint** of an owner class is a region contained in every allowed core
pose of that class. It is guaranteed occupied if that class is selected.
A small common footprint is not a representative full square and need not capture all of
its owner’s restrictions.

A **wall-aware footprint** first restricts possible owner centres using B-core
containment in the container.
The intersection of all remaining core poses can then grow.
A larger footprint is a stronger guaranteed obstacle, but whether that helps a dot cover
is a separate question.
Exp146 measured footprint growth; exp147 tested one particular way of transferring an
existing cover from that growth.

A **residual core** represents one of the squares remaining after the four owners have
been selected. Four distinct owners leave seven physical parents to exclude.
For a fixed tuple, the current model allows every strictly contained net-oriented B-core
that strictly avoids the tuple’s four selected closed footprints.

This is a **relaxation**: it includes every relevant physical residual core, but may
also include cores that have no feasible unit parent, no compatible full owners, or no
place in a simultaneous eleven-square packing.
Avoiding a patch is weaker than avoiding the full owner that contains the patch.

The logic is one-way.
Covering the whole relaxation can prove coverage for its physical subset.
Finding an escape in the relaxation does not prove a physical packing exists.
Similarly, proving that the relaxation needs more weight does not prove that the
physical subset needs that much weight.

**Routing** is the passage from general ownership to a sufficient certified owner
selection. For this architecture, the needed statement is: every hypothetical physical
packing admits **at least one** valid owner selection whose tuple has been excluded.
Proving every raw tuple excluded would suffice, but is stronger than necessary because
mark and sector choices can overlap.
The four-owner existence premise is already available; this sufficient routing result is
not. T-023 proves a specified conditional branch exclusion at `q=3.84`; it is not a
global lower bound at that side.

**Banking occupied mass** is a further conditional counting option.
If A is the union of guaranteed occupied patches, residual cores avoid A, so their
available mass is `W_available = mu(K) - mu(A)`. A residual cover can therefore suffice
when `W_available/m < 7`, even if its nominal total W is larger.
Subtract the mass of the union, not overlapping pieces repeatedly.
Four selected owners reduce the number of remaining squares by four; their small
guaranteed patches do not automatically bank four units of mass.

## 6. The Exact Geometry Used in the Recent Tests

A **collision region** is a set of possible centres, not an occupied square.
For fixed core shape `S` and obstacle `A`, it consists of centres `c` for which `c+S`
meets `A`. A dot also gives such a collision region: all centres whose core contains
that dot. The implementation constructs these regions exactly as polygons.

The five original unit-weight sites are denoted **D**. With four selected footprints,
there are nine collision obstacles at each direction: four from the footprints and five
from D. **U**, the strict missed-centre domain at that direction, consists of centres
strictly inside the core’s container-centre rectangle and outside all nine closed
collision obstacles.
A core centred in U escapes both D and the selected patches.

A **deficit** is the exact area of this container-centre domain not covered by the
collision regions. Positive deficit supplies an open missed region.
A retained **escape witness** is an exact centre and direction independently checked
against the strict containment and avoidance conditions.
It refutes a proposed cover on the stated relaxation.
It is not a full packing witness.

The strict missed domain is open.
Within this model, a nonempty missed domain therefore has positive area.
This topological premise matters when exact zero area is used to establish that no
strict missed centre remains.

For a unit axis u, the **projection** of a centre c is the scalar `u·c`. A **geometric
support value** is an extremal projection, such as `sup_{c in U} u·c`. It describes how
far a set extends in a direction.
This is the meaning of “support” in exp153; §9 distinguishes it from a measure’s
positive-weight sites and an LP dual’s positive-weight square rows.

**Vertical decomposition** splits the missed domain into finitely many free strips
between geometric event coordinates and records their polygonal closures.
An **attainer** is a vertex where a projection reaches an extremum.
A closure vertex may be tangent to a forbidden obstacle, so it must not be called a
strict escape without additional work.

## 7. The Recorded Observations, in Order

The source of each finding is its frozen experiment record and receipt.
The following statements preserve the tested object; they do not attach broader
productivity judgments to a positive or negative verdict.

| Experiment | Observation | Supported conclusion | What remains outside it |
| --- | --- | --- | --- |
| [exp145](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-145-independent-five-dot-union.md) | Independent union computation returned zero deficit on all 361 directions for the retained five-dot instance | Independent computational confirmation of that conditional cover | A new owner tuple, a global bound, or independent re-proof of every analytic transfer premise |
| [exp146](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-146-wall-owner-footprints.md) | Twelve of sixteen wall-aware class footprints strictly grew; four were equal; none was impossible | Container restrictions strengthened those twelve common footprints | That the growth yields another packing exclusion |
| [exp147](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-147-wall-owner-containment.md) | The tested component-containment transfer found no new tuple; only the two retained baseline tuples survived that test | This specific sufficient transfer test added no case | That no other cover, union-level argument, or refined owner model can help |
| [exp148](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-148-fixed-five-dot-wall-expansion.md) | The bounded fixed-pattern screening run ended partially, retaining two validated escapes but no completed seed | Its saved escapes refute fixed-D coverage for the labels they reach | An exhaustive search, a packing census, or a universal negative for other dot patterns |
| [exp149](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-149-selected-wall-tuple-cover.md) | The selected tuple (0,0,0,7) had a positive deficit and strict escape at direction 0 | D does not cover this tuple’s patch relaxation | Impossibility or feasibility of the physical tuple |
| [exp150](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-150-wall-owner-escape-compatibility.md) | For that saved escape, each selected class supplied an independently replayed compatible B-core at frame 0: four evaluated frames in total | No single class universally excludes this one escape in the existing centre model | Simultaneous compatibility of four owners, unit-parent feasibility, or compatibility with every residual escape |
| [exp151](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-151-selected-six-dot-cover.md) | Adding the exp149 escape centre as a sixth site gave six initial zero deficits, then a strict escape at direction 6 | This fixed six-site pattern fails | Every other sixth-site location, relocated base sites, or fractional weights |
| [exp152](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-152-sixth-site-two-core-screen.md) | The two retained escaping cores had a nonempty two-dimensional intersection with four vertices | A common site can hit those two witnesses | That the site hits every core in the relaxation |
| [exp153](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-153-direct-sixth-site-feasibility.md) | The exact common-site region became empty after 188 complete direction constraints | No single added site can cover the selected patch relaxation while D stays fixed | Arbitrary added fractional mass, altered original weights or sites, stronger owner geometry, or a physical packing conclusion |

See the [experiment ledger](../../../packing/campaign/ledger.md) and the
[exp153 record](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-153-direct-sixth-site-feasibility.md).
Exp150, exp151, exp152 and exp153 took 9.01, 13.45, 9.84 and 22.36 seconds respectively
as complete external target processes.
Those timings exclude implementation, review, publication and model usage; they do not
by themselves measure research productivity.
Exp150’s checker can traverse up to 181 frames per class, but this existential result
stopped at the first witness in each class.
It did not exhaust all 724 possible frames.

The partial exp148 record and later symmetry reasoning must also be distinguished.
Statements that a witness rejects thousands of labels mean it rejects D as a cover for
those labels. They do not mean thousands of physical packing cases have been proved
impossible. The mask counts and their exact scope remain in the
[exp148 interpretation](../../../packing/cases/n11_five_dot_cover/after-exp148-strategy.md).

## 8. Why Exp153 Decides More Than a Few Candidate Dots

Let `I*` be the set of sites belonging to every core in the fixed-D missed family.
A single new dot completes D exactly when it belongs to I*. Exp152 intersected only two
necessary witness cores; exp153 addressed the entire continuous-centre family at the
retained directions.

For a direction with orthonormal axes u and v and `h=B/2`, a site p belongs to the core
centred at c exactly when

$$|u\cdot(p-c)|\leq h,\qquad |v\cdot(p-c)|\leq h.$$

To belong to every such core with centre in U, it must satisfy

$$
\sup_{c\in U}u\cdot c-h\leq u\cdot p
\leq\inf_{c\in U}u\cdot c+h,
$$

and the analogous pair for v. If U is empty, that direction contributes no site
constraint. The lower bound uses the maximum centre projection; the upper bound uses the
minimum.

The reviewed decomposition argument identifies its component closures with the closure
of U. Continuity therefore permits exact extrema over all their vertices, including
boundary attainers. A mere overapproximation of the closure would not justify a negative
result: it might add impossible constraints.

Exp153 intersected these necessary and sufficient site inequalities, starting from the
two-core intersection.
After direction 187, no site remained.
Additional constraints cannot restore a site, so this is a complete negative result
after 188 directions, not an unfinished 361-direction traversal.
Had a site survived every direction, acceptance would additionally have required the
independent full-net union check.

The rational computation and source review are substantial evidence for this exact
statement. They are not a machine-checked proof of every analytic premise, and passing
software tests is not a substitute for those premises.
The
[source admission](../../../packing/cases/n11_five_dot_cover/direct-sixth-site-source-admission.md)
separates the closure argument, implementation checks and outcome semantics.

### The Explicit Inference Ledger for Exp153

1. **Available data:** the bound input receipts, exact computed half-planes and regions,
   source review, tests, launch metadata and completed outcome.
2. **Selected data:** one q, one B and net, one owner tuple, one relaxed obstacle model,
   and one fixed five-site set D. Other tuples, weights and geometries were not varied.
3. **Meaning assigned to the data:** these rows constrain a point common to every
   D-missed core in that precise model.
4. **Necessary premises:** the source bindings and arithmetic are correct, the
   decomposition gives the exact closure, and the projection and clipping rules have the
   stated semantics. The source admission explains the evidence for these premises.
5. **Supported conclusion:** no one added site completes D on that relaxation.
6. **Judgments not supplied by the data:** whether reweighting, parent constraints,
   another tuple, or a different architecture offers greater research value.
7. **Possible actions:** independently replay a compact obstruction, test a stronger
   necessary domain, or examine another certificate family.
   Selecting one would be a prospective decision with explicit assumptions, not an
   additional experimental fact.

## 9. Three Different Meanings of “Support”

**Atomic support** is the set of sites with positive weights in a measure.
A fixed allowed site list may be larger than the positive-weight support if some
optimized weights are zero.
Fixing the allowed sites means allowing weights to change only at those locations;
allowing new sites is a different optimization problem.

**Dual support** is the set of square constraints assigned positive multipliers by a
linear-programming dual solution.
It is a set of weighted square rows, not a set of candidate atom locations.

**Geometric support** is a directional projection extremum, such as `sup_{c in U} u·c`.
Exp153 uses this meaning.
Its “support directions” are the directions for which these geometric inequalities were
completed.

In a finite covering LP, rows are square constraints, columns are candidate sites, and
an incidence entry records whether a square contains a site.
The primal minimizes total site weight subject to giving each retained square row at
least unit mass. Its dual assigns nonnegative row weights so the combined weight through
every retained site is at most one.
**Pricing** searches for a new site where that dual weight exceeds one, which identifies
a violation of the current dual pointwise constraint outside the retained site list.
Such a violation does not guarantee a strictly better optimized objective, particularly
when the row weights were rationalized from a numerical proposal.
It does not itself certify coverage of all physical squares.

A **fractional packing of core poses** is the corresponding dual geometric object:
assign nonnegative weights to cores so the weighted depth at every site is at most one.
If that pointwise condition is verified everywhere, summing the core coverage
requirements shows that any point cover must have mass at least the total core weight.
The cores may overlap and need not have jointly feasible unit parents.
Thus this is a bound on a covering problem, not automatically a physical packing.

The reserve **full-support pricing experiment H135/exp134** has a narrower, precise
question. It would solve one transported BC232 state, rationalize one retained sequence
of positive dual rows, and compare the first 32 entries with the full positive sequence.
It asks whether the same new site orbit has exact weighted depth at most one in the
32-row version but greater than one in the full version.
**Depth** here means the sum of dual row weights of squares containing that site.
An **orbit** is the set of its images under the stated container symmetries.

H135 remains unrun. “Full” means all positive rows of that one rationalized LP solution,
not all possible square poses, all weights everywhere in the container, or the full
owner-conditioned research program.
Its administrative unrun outcome is not a negative result about pricing.
See the
[H135 definition](../../../packing/campaign/hypotheses/H-135-paired-full-support-pricing.md).

## 10. What Is Not Yet Established

An empty I* rules out one added site, even if that site’s weight were increased.
It does not rule out splitting added weight across several sites.

If two independently replayed strict D-missed closed cores in the relaxation are
disjoint, each needs unit added mass, and no added atom can contribute to both.
That would force added mass at least two and nominal total mass at least seven while the
five original unit atoms remain fixed.
A further inference about mass available after banking also needs the original five
atoms to lie outside the selected occupied union, or must explicitly account for those
that do not. That relation has not been newly checked in this interpretation block.
The prepared two-attainer construction seeks such a pair, but no target has run.
Its boundary vertices are not already verified strict escaping cores.
Its
[source admission](../../../packing/cases/n11_five_dot_cover/two-attainer-source-admission.md)
and synthetic controls are complete; they do not supply the missing target replay.
No exp154 has been registered or run in this block.

If three cores have empty common intersection but every pair intersects, their three
constraints alone can be covered with mass 3/2: put weight 1/2 at a point in each pair
intersection. This does not cover the rest of the family, but it demonstrates why a
three-core obstruction alone cannot establish the disjoint-pair mass conclusion.

The proposed **unit-parent centre restriction** is different.
Every contained unit square has its centre in `[1/2,q-1/2]^2`. The centre-preserving
snapping construction allows this necessary condition to be intersected with existing
owner-centre domains.
An additional rational frame-aware bound is derived in the
[retained contract](../../../packing/cases/n11_five_dot_cover/unit-parent-centre-contract.md)
from the angular mismatch allowance.
The
[originating lane’s proof check](../reviews/review-2026-09-10-n11-parent-centre-author-check.md)
found no analytic error under the stated hypotheses, but it is not an independent audit.
It identified two implementation obligations: record empty restricted frames explicitly,
and reconstruct the added parent restriction during replay.
The existing exp150 replay checks the older B-core centre domain and cannot certify the
new domain unchanged.
Independent proof review, implementation admission and target measurement remain
outstanding. No footprint gain, removed escape or new case exclusion has been measured.

Nothing in exp145–153 proves that an optimum can be pushed into four occupied corners,
that all sixteen owner classes at each corner are physically realizable, that all
relaxed escaped cores can be extended to unit parents, or that the chosen tuple is the
most consequential remaining case.

## 11. Alternatives and the Evidence Needed to Compare Them

The following are questions, not a ranking of research productivity.
Several can be pursued together.
Their costs and chances of resolving the physical problem have not been compared under a
common protocol.

| Possible approach | Question it would answer | Evidence still needed |
| --- | --- | --- |
| Fixed two-attainer obstruction | Can a compact strict disjoint pair certify that added mass below two cannot rescue the five unit atoms in this relaxation? | Source is admitted; the exact target gap, perturbation and independent replay remain unrun. Failure would concern only the frozen construction |
| Fractional weights with D retained | Can multiple added atoms of total mass below two cover the missed family? | A complete weighted cover, or a sound obstruction such as a verified disjoint pair; empty I* alone is insufficient, and banking needs its own available-mass accounting |
| Reweight the original sites as well | Can redistributing existing mass and adding sites bring total mass below seven? | A specified support or pricing procedure, rational candidate, complete domain verification; no fixed-five-unit-weights obstruction answers this |
| Move several or all sites | Does the chosen geometry of D cause the failure? | A defined search family and complete verification; exp153 varies only the sixth site |
| Necessary unit-parent centre bounds | Are some problematic relaxed poses artifacts of using only B-core containment? | Audited physical transfer and measured change in domains, footprints or fixed-witness compatibility |
| Individual or joint owner compatibility | Do full possible owners rule out residual poses that avoid their common patches? | Explicit quantifiers; all required frames for a universal conclusion; joint reasoning where separate witnesses can choose different owners |
| Refine selected owner classes | Does splitting angle or position uncertainty produce a sufficient stronger footprint? | Complete subdivision coverage and a tested gain; a failure of coarse containment does not decide this |
| Broader tuple routing or structural lemmas | Can every hypothetical packing be routed to at least one excluded valid owner selection? | A theorem with the correct existential selection and physical coverage quantifiers; exhausting all raw labels is sufficient but not necessary |
| Other counting or geometric constraints | Can angle counts, contact restrictions, face conditions or a mixed measure improve the argument? | A clearly stated necessary physical fact and its independent proof before combining it with weights |
| H135 paired full-support pricing | Does the truncated dual omit a useful site for its retained LP state? | Its own prospective paired pointwise test; this is distinct from conditional owner-patch pricing |
| Change q, B, the net, marks or the source measure | Is the present parameterization hiding a useful route? | Re-established ownership, snapping and coverage premises for the changed regime; current failures do not transfer automatically |

A sound action decision can consider expected information, implementation cost and the
importance of the unanswered question.
Those are judgments with stated assumptions.
They should be revised when new evidence arrives.
The existing record supports several precise negative results and one retained
conditional packing exclusion; it does not yet support a global verdict about which
broad approach is productive.

## 12. Corrections and Continuing Review

The completed independent inference audit identifies stale experiment statuses, missing
quantifiers and ambiguous uses of “exclude” in earlier summaries.
Corrections retain the historical experiment and its frozen criterion while revising
current explanatory prose.
A negative cover witness should be described as rejecting a named cover family; a
physical case exclusion should be named separately.

The final independent narrative review is **PASS for the stated interpretation and
evidence scope**. It confirmed the ownership numbers and main inference chain.
Its reviewer was separate from the account’s author but participated in underlying
mathematical work; this is not independent re-derivation of every retained premise.
The reviewed corrections to B-core containment, strict domains, empty-direction
semantics, pricing and support terminology are incorporated.
The [inference audit](research-2026-09-09-n11-inference-audit.md) records the concrete
backfills; the
[narrative review](../reviews/review-2026-09-09-n11-evidence-interpretation.md) records
its assurance scope.
No new scientific target is part of this interpretation block.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
