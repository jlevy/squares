# Source-Distinct Review of the N11 Owner-Selection Report

Date: 2026-09-12. Review bead: think-gldo.
Reviewed report:
[research-2026-09-12-n11-selection-routing-first-principles.md](../research/research-2026-09-12-n11-selection-routing-first-principles.md).
Primary source revision: `9be2bf274e4c9f6dbca03c05cd6e21bb852af521`.

**Final disposition: ACCEPT after the SEL-1 correction.** The initial refusal remains
below as review history, followed by the accepting correction readback.

## Initial Verdict and Required Correction

**Initial verdict: REFUSE the report as written, solely for the concluding
rejection-scope claim below.** The mathematical reductions, exact configurations, two
new contact-path lemmas, and both surplus acceptance implications pass this
source-distinct review.
No correction to their formulas or counts is required.
Correcting the one scope claim is sufficient for acceptance as a mathematical analysis
and prospective test design; it would not admit either unrun surplus helper or a global
n11 exclusion.

### SEL-1 — P2: A failed surplus inequality does not identify a necessary next joint constraint

At lines 465–466 of the pre-correction draft, the report said either outcome determines
whether a routing lemma can use the existing measure locally or “requires additional
joint geometry.” At lines 541–543, it said a failed test would “identify exactly which
additional joint information the next proof attempt must retain.”
Neither conclusion follows from the declared rejection witness.

An admissible local or pair witness with surplus at or below the named threshold refutes
that specific universal inequality on that declared domain.
It need not extend to eleven parents, and it does not establish which omitted constraint
would eliminate it, whether a different local resource would suffice, or whether joint
geometry is necessary.
The report already states the correct narrower rejection scopes in
[Test 1](../research/research-2026-09-12-n11-selection-routing-first-principles.md#test-1-can-one-missing-choice-corner-overspend-the-common-allowance)
and
[Test 2](../research/research-2026-09-12-n11-selection-routing-first-principles.md#test-2-can-a-forced-0forced-15-pair-overspend-the-allowance).
The closing sentences must preserve those scopes.

This distinction is concrete for the fixed measure: its retained BC303 replay gives the
stronger universal core charge `800003/800000`, rather than just one.
Consequently even a generic contribution from the omitted cores can strengthen a surplus
threshold without adding a contact or shared-owner geometry theorem.
This is an available additional resource fact, not a claim that it resolves either
proposed test; see the
[BC303 replay, lines 191–193](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/bc-303-first-wave-selection.md).

**Exact replacements:**

- Replace the sentence at lines 465–466 with: “These tests decide whether the stated
  one-corner or two-corner BC303 surplus inequality holds on its declared domain.
  A rejection leaves stronger domain restrictions and different resources or arguments
  open.”
- Replace the final sentence at lines 541–543 with: “A successful complete inequality
  would discharge the stated part of the routing theorem.
  A failed one would refute only that surplus mechanism; it would not identify which
  additional information a future proof needs.”

## Quantifiers and Physical Transfer

The equipped-packing definition at report lines 31–50 correctly separates a physical
unit parent from its selected strict core.
Physical parent angles remain continuous, while selected core angles belong to the
admitted net. Strict containment makes different closed cores disjoint, including at
their boundaries; hence a mark has at most one selected-core owner.
The ownership arguments apply to the selected cores, not to arbitrary parent-only mark
containment. These are the premises in the
[structural-helper definitions, lines 28–130](../research/research-2026-09-10-x027-structural-helpers.md)
and the [shrink derivation, lines 232–248](../../../TUTORIAL.md).

For a fixed equipped packing, all available labels are realized by cores that already
coexist. Different corners have distinct owners, so independently choosing a label at
each corner indeed gives a valid four-owner selection.
Thus `Gamma(P) = product A_c(P)` has the stated meaning.
It is not the product of four existential pose domains.
The proof in report lines 52–82 preserves the source quantifier in the
[helper report, lines 422–465](../research/research-2026-09-10-x027-structural-helpers.md)
and
[X-028, lines 244–259](../../../packing/campaign/explorations/X-028-n11-strategy-portfolio-draft.md).

The universal statement over the declared equipped domain is sufficient for the global
conditional route. It should continue to be understood with that domain: if a future
argument changes the allowed choice of cores, it must restate that quantifier and its
symmetry transfer. A physical existence proof would in general need only one successful
admitted equipment and selection per hypothetical packing.
There is no current error from proving the stronger equipped-domain statement.

S1 supplies a representative in every feasible fixed-angle translation component with
the named left/bottom contacts and a genuine contact basis.
Selecting cores and owners *after* normalization is valid; transporting the original
availability sets along the motion is not asserted or needed.
The report’s implication from a nonempty physical feasible set to a nonempty normalized
family, followed by universal routing on that family, is sound.
I checked the compactness, lexicographic vertex, and strict separating-axis steps
against [S1, lines 121–207](review-2026-09-10-n11-structural-normal-forms.md) and its
[independent review, lines 58–143](review-2026-09-10-n11-structural-normal-forms-independent.md).
Neither proof supplies finite physical angles or preservation of the original contact
components.

For a valid T-023 tuple, four distinct owners leave seven actual residual cores.
The admitted cover of the corresponding complete residual domain forces each to contain
a dot, and closed-core disjointness makes the dots distinct.
The resulting `7 <= 5` contradiction is valid.
Additional mark owners remain among those seven when only four owners are selected.
The physical transfer and residual-domain qualifications in report lines 79–115 and
338–362 match the [T-023 account, lines 396–451](../../../TUTORIAL.md).

## Finite Reductions and Symmetries

The source contract defines exactly two transported occupied geometries, with tuples
`(0,0,0,0)` and `(15,15,15,15)`, and two accompanying dot patterns for each.
Those four paired certificates do not create mixed occupied tuples.
This matches the
[wall-containment contract, lines 55–113](../../../packing/cases/n11_five_dot_cover/wall-containment-contract.md).
The report explicitly limits its remainder to this `G0`.

For any nonempty availability factors, the product hits `G0` exactly when every factor
contains 0 or every factor contains 15. Its failure therefore has witnesses `c,d` with
`0 not in A_c` and `15 not in A_d`. Fill every other label into every factor: this gives
`E^(c,d)`. Each such product avoids both uniform tuples, and restoring either deleted
label admits the corresponding tuple.
Every avoiding product is contained in one of them.
The two deleted positions determine the ordered pair uniquely, so there are exactly 16
maximal products, including the four cases `c=d`. This proves the maximality claim
without interpreting a combinatorial product as a physically realizable packing.

I also checked all `4^4 = 256` profiles of membership in `{0,15}`. Exactly 31 route and
225 fail; all 225 are covered by those 16 maximal products.
The two proposed missing lemmas are equivalent to routing: four nonempty subsets of a
two-element set have a common element exactly when opposite singleton subsets do not
both occur. Labels outside `{0,15}` do not affect this equivalence.

In the declared reflected corner charts, `H` and `V` permute the corners without
exchanging the two relevant local labels.
Diagonal reflection `S` exchanges those labels by `tau(m_a:j) = m_(3-a):(7-j)`. It
therefore sends the ordered blocker pair to `(S d, S c)`. Direct finite enumeration
gives full-D4 orbit sizes **4, 8, 4**: same corner, adjacent corners, opposite corners.

For the family with the fixed pair of named walls `{left,bottom}`, the invariant global
subgroup is `{I,S}`. Its four fixed ordered pairs are `(BL,BL)`, `(BR,TL)`, `(TL,BR)`,
`(TR,TR)`. The other twelve pairs form six two-element orbits, giving **ten** orbits.
Using only three representatives while imposing that fixed wall chart would lose cases.
The report correctly refuses to repair that loss by an unproved second normalization
that preserves labels.

The incidence count is independently reproduced as `sum binom(4,sigma) = 16` with no
missing mark and `8 sum binom(3,sigma) = 64` with one missing mark.
There are `4+sigma` distinct mark owners in either case.
Intersecting these 80 incidence conditions with the 16 blocker conditions is a complete
overlapping cover, with continuous geometry still required.

## Exact Geometry and the Two New Path Lemmas

I used exact rational arithmetic, independently constructing each signed-axis frame from
the signs of `z-m`. For an axis core, the first signed ray at angle `r*pi/2` lies in the
two closed bins `2r-1,2r` modulo eight.
This gives all the labels claimed in report lines 377–420:

| Centre | First-ray directions for `m1`, `m2` | Complete local label set |
| --- | --- | --- |
| `(17/20,17/20)` | north, south | `{1,2,13,14}` |
| `(6/5,9/10)` | east, south | `{0,7,13,14}` |
| `(9/10,6/5)` | north, east | `{1,2,8,15}` |
| `(1/2,1/2)` | west, west | `{3,4,11,12}` |

For the first three centres, the largest coordinate displacement to either mark is
`1474/3175`. Its strict core-containment margin is

`9977/20000 - 1474/3175 = 87879/2540000 > 0`.

The parent containment margins are positive.
Transporting any of the three choices independently to the four corners gives 81
configurations; all pass exact joint parent separation.
Some coordinate separates each pair of different-corner centres by at least `36/25`, so
unit parents have a separation margin of at least `11/25` on that axis.
The literal-corner core bounds are exactly `23/20000` and `19977/20000`, and both marks
lie strictly between them.
The report’s small-angle persistence assertion follows by continuity while retaining the
axis core and using a sufficiently small admitted parent-angle interval.

These configurations establish the stated four-parent controls, not an eleven-parent
extension or either missing global lemma.
The signed-ray definition and boundary convention agree with the
[sector proof, lines 26–71](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/corner-owner-sector-footprints.md).

**The `9-sigma` path lemma is correct.** After S1, four distinct corner roles occupy at
most three physical contact components, so at least one eligible pair is connected.
Take a shortest path among all connected pairs of mark owners from different corners.
If an interior vertex were a mark owner, its corner would differ from at least one
endpoint’s corner, producing a shorter eligible subpath.
Every interior vertex is therefore among the `11-k` parents owning none of the eight
marks. Counting both endpoints gives at most `11-k+2 = 13-k = 9-sigma` parents.
This uses all mark owners, not merely the selected four.
The report correctly restricts the conclusion to some corner pair, rather than a
prescribed pair or a wall-to-wall path.

**The distant-wall three-parent lemma is correct.** Every right-corner mark has
`x >= q-a = 1808/635`, and

`(1808/635)^2 - 8 = 43064/403225 > 0`.

A unit parent touching the left wall lies entirely in `x <= sqrt(2)`. Any parent meeting
it has a common point there and horizontal width at most `sqrt(2)`, so it lies entirely
in `x <= 2 sqrt(2)`. Neither can own the right-corner mark.
S1 gives a path to a left-wall parent, and that path must contain at least three
parents. The top/bottom claim is its coordinate transpose.
This is a statement about genuine contact and actual parent containment, as the report
says; strict cores need not touch along the path.
The source inputs are the
[mark coordinates and distance bound](../research/research-2026-09-10-x027-structural-helpers.md)
and the
[wall-width/component argument](../research/research-2026-09-10-x027-structural-helpers.md).

The other controls also retain their scopes:

- The tilted single parent has the four stated vertices and minimum `x+y=3/5`.
- The side-two two-square example is optimal by the cited container-centre argument,
  while occupying no container corner.
- The six-square rotational rattler has half-width at most `sqrt(2)/2` inside its vacant
  side-two box; optimality is the retained `s(6)=3` premise, not newly proved here.
- The pair at `74/35` has relative frame coordinates `(1/7,-1)` and contact length
  `6/7`. The fixed-angle centre box forces equality at one of its four extreme relative
  vectors, leaving four isolated labelled configurations.
  This verifies the same-component snug-only limitation, without refuting a full-space
  existential snug theorem.
- In the continuous shared-owner control, compatibility with `R0` gives
  `t in [3/5,7/10]` and compatibility with `R1` gives `t in [1,11/10]`. These nonempty
  intervals are disjoint.
  The artificial mark is at most `1/4 < B/2` from every candidate core centre in the
  horizontal coordinate.
  It is correctly identified as a control outside the BC303 mark domain.

The imported neutral-core and four-diamond assertions match their cited retained
reviews. This review did not rerun those scientific checks; the report does not promote
them to an eleven-square packing or unavoidable-selection result.

## Sufficiency and Limits of the Surplus Tests

The exact arithmetic is correct:

`epsilon = 524199/2000000`, `2w-epsilon = 441/125000 > 0`, and
`epsilon-w = 517143/4000000`.

For a packing with disjoint selected closed cores, `U_mu + sum_i (mu(C_i)-1) = epsilon`
and `U_mu >= u*w`. Every omitted core has nonnegative surplus; different-corner owner
sets are disjoint. The report neither banks a co-owner twice nor combines separately
chosen measures. These are precisely the premises of the
[common surplus argument, lines 345–387](../research/research-2026-09-10-x027-structural-helpers.md).

**Test 1 acceptance is sufficient.** Its four roles exhaust the possible ownership at a
corner because at most one of all eight marks is unowned.
For a full pair, its owner surplus cannot exceed `epsilon` in a physical packing.
For a one-mark role, the missing mark forces the stronger upper bound `epsilon-w`. A
strict lower bound above the respective allowance on every complete role therefore
excludes an empty relevant availability set.
D4 symmetry of the fixed measure and admitted equipped domains transfers this
unconditioned result to every corner.
Both split-parent compatibility and absence of *every* available good label are
necessary and explicitly retained.

The use of an infimum adds no hidden compactness assumption here.
With a fixed finite atomic measure and at most two owner cores, the surplus takes only
finitely many possible exact values, even on a continuous or nonclosed pose domain.
On a nonempty domain its infimum is consequently an attained minimum.
The domains themselves need not be compact for this assertion.
No sampled or partial computation of that minimum would suffice.

**Test 2 acceptance is sufficient.** Put `J = I_c union I_d`. For a full packing
extending a local pair,

`sum_(i in J) xi_i <= epsilon - U_mu <= epsilon - u_total*w <= epsilon - u_local*w`.

The proposed strict reverse inequality on every simultaneous local realization therefore
excludes the pair, regardless of the omitted corners and residuals.
A missing mark elsewhere only strengthens the contradiction.
After local availability is established, every remaining routing failure has opposing
singleton types at two distinct corners; the adjacent and opposite physical orbit types
cover those pairs.
A fixed contact-wall chart requires the additional subdivision already
stated in the report.

A rejecting exact witness for either test disproves only its respective inequality on
the declared local domain.
It establishes no global extension and supplies no choice of a necessary next
constraint. This is the sole correction required by SEL-1.

## Checks and Residual Limits

The retained independent check is
[check_n11_selection_routing.py](../../../packing/devtools/check_n11_selection_routing.py).
Reproduce it from `packing/` with the project’s Python 3.14 interpreter:

```bash
uv run --frozen --all-extras --group dev python \
  -m devtools.check_n11_selection_routing
```

It uses only standard-library exact rational arithmetic and finite enumeration.
It checked the 256 relevant availability profiles, all 16 maximal products, both orbit
counts, the 80 incidence counts, all 81 four-parent configurations, signed label sets,
strict containment and separation margins, the distant-wall comparison, and the listed
rational controls. The geometric path proofs and continuous-domain surplus implications
were reviewed analytically.

The review began while
`docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md` had a
concurrent change.
That plan-only change was later committed as `f1e397cd`; it is outside
the cited source set and was not used as a premise.
The checked source files still match the declared revision.
No BC329 target, BC303 surplus target, positive full-shape profile, or new scientific
experiment was run. No target was registered.
No core charges for the new local configurations were measured.

Acceptance after SEL-1 would admit these deductions and the scoped prospective tests,
not their unrun outcomes.
The local-availability and forced-consistency lemmas remain open, T-023 remains
conditional, and the global n11 bound is unchanged.

## Correction Readback — 2026-09-12

**ACCEPT the corrected draft.
SEL-1 is closed.** This verdict supersedes the original refusal above for the exact
draft identified here; the original finding remains as the review history.

The inspected corrected source draft, now retained as
[research-2026-09-12-n11-selection-routing-first-principles.md](../research/research-2026-09-12-n11-selection-routing-first-principles.md),
had byte length `30517` and SHA-256
`82bfce3a790734175facfe6b24f5c0d55cff4f96a680a7db9f3814fa23b5887a`. The digest was
checked before and after the readback.
The retained report intentionally has different bytes because its paths and review
status now refer to durable repository artifacts; its accepted mathematical content is
unchanged. The primary source remains revision
`9be2bf274e4c9f6dbca03c05cd6e21bb852af521`. Later commit `f1e397cd` changes only the
active plan already excluded from this review; the cited primary source files are
unchanged.

The two required replacements are present in the retained report’s
[test-scope introduction](../research/research-2026-09-12-n11-selection-routing-first-principles.md#two-falsifiable-mathematical-tests)
and the same section’s closing paragraph.
They restrict rejection to the stated one-corner or two-corner BC303 inequality and
explicitly leave stronger domains and different resources or arguments open.
They no longer infer which additional information a future proof needs.

The related correction in
[the four-parent controls](../research/research-2026-09-12-n11-selection-routing-first-principles.md#eight-marks-and-joint-owners-do-not-force-either-missing-lemma)
now says only that their extension to eleven parents remains open.
It no longer prescribes the seven-parent extension as the particular geometry every
valid helper must use.
The correction in
[Test 1](../research/research-2026-09-12-n11-selection-routing-first-principles.md#test-1-can-one-missing-choice-corner-overspend-the-common-allowance)
correctly leaves another local resource or a stronger domain undecided after rejection.
These changes preserve the exact controls and their previously accepted scope.

I reread the full corrected draft and searched all occurrences of failure, rejection,
requirements, necessity, additional information, and future arguments.
No remaining passage claims that rejection of either proposed surplus test determines
which information or argument is necessary.
The remaining requirements concern explicit mathematical premises, complete verification
of a named inequality, or the two-part routing reduction; they do not recreate SEL-1.
The status wording at lines 20–27 and 219 accurately describes the mathematical checks
already completed by this review.

No new mathematical blocker was introduced.
The proposed BC303 surplus tests remain **unrun**, and this readback measured no core
charges and ran no scientific target.
Neither local availability nor forced-type consistency is proved, no global selection
theorem is established, T-023 remains conditional, and the global n11 bound is
unchanged. Only this review artifact was updated; no repository file or draft byte was
edited during the readback itself.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
