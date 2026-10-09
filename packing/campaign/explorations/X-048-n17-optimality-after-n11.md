---
title: X-048 — Optimality Routes After n = 11
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-048
  title: Optimality Routes After n = 11
  date: '2026-10-01'
  author: Root coordinator with GPT-6 Astra max mathematical review and GPT-6 Sol research reviews
  campaign: packing.squares
  brief: >-
    Plan a fresh W3 block prioritizing n17 and other unresolved low cases after the
    imported n11 optimality proof and recent mixed-measure and parent-core results.
    Identify transferable mechanisms, endpoint obligations, structural obstacles,
    candidate falsifiers and the cheapest experiments to select next. No new bound,
    experiment verdict or proof certification is claimed.
  sources:
    - packing/frontier/results.yaml
    - packing/frontier/n-011.md
    - packing/frontier/n-012.md
    - packing/frontier/n-017.md
    - packing/frontier/n-018.md
    - packing/frontier/n-019.md
    - packing/frontier/n-020.md
    - packing/frontier/n-021.md
    - packing/frontier/n-026.md
    - packing/frontier/n-029.md
    - packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md
    - docs/project/reviews/review-2026-09-30-n11-expository-simplification.md
    - docs/project/specs/active/plan-2026-09-25-after-r052-planning.md
    - packing/campaign/explorations/X-043-new-lower-bound-proof-directions.md
    - packing/campaign/explorations/X-044-low-n-certificate-transfer.md
    - packing/campaign/explorations/X-047-low-n-angles-after-the-parent-core-advance.md
    - packing/campaign/agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md
    - docs/project/reviews/review-2026-09-27-evand-s32-s12.md
    - packing/resources/web/evand-square-packing-2026-09-28/square-packing/s12/README.md
    - docs/project/reviews/review-2026-09-27-plan-4640020-lemma-check.md
    - docs/project/reviews/review-2026-09-28-n17-guzhou-r067-r068.md
    - docs/project/reviews/review-2026-09-28-evand-s21-s45-mixed-covers.md
    - docs/project/reviews/review-2026-10-01-evand-source-coverage.md
    - docs/project/reviews/review-2026-10-01-evand-mathematical-transfer.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-242-h258-n17-core-stress.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-243-h262-n17-charge-floor-pilot.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-244-h261-n17-local-minimum.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-245-h265-n17-catalogue-polynomial.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-246-h266-n17-capacity-one-cover.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-247-h266-n17-unique-state-cover.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-248-h268-n17-local-half-composition.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-249-h267-n17-first-certified-sub-patterns.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-250-h267-n17-standing-verifier-admissions.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-251-h267-n17-overnight-flag-certification.md
    - packing/campaign/hypotheses/H-261-n17-local-minimum-modulo-sliders.md
    - packing/campaign/hypotheses/H-262-n17-conditional-charge-occupancy-census.md
    - packing/campaign/hypotheses/H-263-n17-endpoint-adapted-cover.md
    - packing/campaign/hypotheses/H-264-n17-geometric-exclusion-cost-per-leaf.md
    - packing/campaign/hypotheses/H-265-n17-catalogue-polynomial-identity.md
    - packing/campaign/hypotheses/H-266-n17-minimal-capacity-one-cover.md
    - packing/campaign/hypotheses/H-267-n17-isolated-sub-pattern-residue.md
    - packing/campaign/hypotheses/H-268-n17-local-theorem-slider-coverage.md
    - docs/project/reviews/review-2026-10-01-n17-route-after-pr265.md
    - docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
    - docs/project/reviews/review-2026-10-02-n17-charge-floor-pilot.md
    - docs/project/reviews/review-2026-10-02-n17-depth-width-wall-lemma.md
    - docs/project/reviews/review-2026-10-02-n17-capture-feasibility.md
    - docs/project/reviews/review-2026-10-02-n17-capture-after-pilot.md
    - docs/project/reviews/review-2026-10-02-n17-widened-projection-scope.md
    - docs/project/reviews/review-2026-10-02-n17-kernel-adaptation-spec.md
    - docs/project/reviews/review-2026-10-02-n17-local-theorem-recipe.md
    - docs/project/reviews/review-2026-10-02-n17-local-half-composition.md
    - docs/project/reviews/review-2026-10-02-n17-residue-process.md
    - docs/project/reviews/review-2026-10-02-n17-w7-closure.md
    - docs/project/reviews/review-2026-10-02-n17-branch-and-bound-certifier.md
    - docs/project/reviews/review-2026-10-02-n17-cost-reduction-pruning.md
    - docs/project/reviews/review-2026-10-02-n17-cost-reduction-performance.md
    - docs/project/reviews/review-2026-10-03-n17-local-radius.md
    - docs/project/reviews/review-2026-10-03-n17-verifier-rewrites.md
    - docs/project/reviews/review-2026-10-04-n17-flag2-diagnosis.md
    - docs/project/reviews/review-2026-10-05-n17-capture-r9.md
    - docs/project/n17-optimality-explainer.md
    - packing/campaign/explorations/X048-session-168-pilots/README.md
    - packing/campaign/explorations/X048-session-168-pilots/certified-sub-patterns.yaml
    - packing/hosted/n17-x048-session-168-certificates.yaml
    - packing/campaign/explorations/X048-session-168-pilots/receipts/capture-pilot2-box1024-need/receipt.json
    - packing/campaign/explorations/X048-session-168-pilots/receipts/capture-pilot2-box1024-need/score.txt
    - packing/campaign/explorations/X048-session-168-pilots/receipts/selector-recheck-90-seed1.json
    - packing/campaign/explorations/X048-session-168-pilots/receipts/residue-survey-arity8-seed1.json
    - packing/campaign/explorations/X048-session-168-pilots/receipts/residue-universe/summary-0505.json
    - packing/campaign/explorations/X048-session-168-pilots/handoff/k2/h-N1-2h.json
    - packing/campaign/explorations/X048-session-168-pilots/handoff/k2/h-N1.json
    - packing/campaign/explorations/X048-session-168-pilots/handoff/k2/h-F1.json
    - packing/campaign/explorations/X048-session-168-pilots/handoff/k2/h-sample.json
    - packing/campaign/explorations/X048-session-182-overnight/kernel-targets.txt
    - docs/project/specs/active/plan-2026-10-05-n17-overnight.md
    - https://github.com/jlevy/squares/pull/347
    - https://github.com/jlevy/squares/pull/350
    - https://github.com/jlevy/squares/pull/354
    - https://github.com/jlevy/squares/pull/355
    - https://github.com/jlevy/squares/pull/356
    - https://github.com/jlevy/squares/pull/360
  proposes: [H-253, H-254, H-255, H-256, H-257, H-258, H-259, H-260, H-261, H-262, H-263,
    H-264, H-265, H-266, H-267, H-268]
---
# X-048: Optimality Routes After n = 11

## Current Selection: 6 October 2026

The
[W3 consolidation](../../../docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md)
reconciles Sessions 182 and 183, the diagnostic packets and the current capture review.
It governs the next selection under BC-418 (`think-tmz6`). The dated sections below
retain the reasoning and frozen proposals; their snapshot figures and future-work lists
are historical where the consolidation supplies a later disposition.

The
[ten-hour continuation plan](../../../docs/project/specs/active/plan-2026-10-06-n17-ten-hour-session.md)
and agenda-043 select BC-430 / `think-ipel` as its launch coordinator.
The overnight session remains planned; no target or session clock starts with this
consolidation.

The verified bracket is now
$4.66044275 < s(17) \le 4.6755300936045509516342148538535054$. R071 is replayed, the
degree-18 side identity and first-order stress are accepted, and the capture-target
local theorem is reviewed with its stated frame and radius.
The latest certified residue is 36,784 states in 4,685 orbits under 58 admitted entries,
with the endpoint surviving.
H-275’s 26 of 29 counted closures describe its draw frame, not all 4,685 remaining
orbits.

The selected direction keeps global exclusion and family capture, with three parallel
questions: proof interfaces and portable replay, a controlled capture discriminator
alongside cheap widened-projection reconnaissance, and stratification of the actual hard
exclusion tail. Completed adaptive-row reruns are not future work.
C2 aimed splits depend on diagnosing the remaining stalls; C5 requires complete
parent-cover certificates.
The fixed R071 charge cannot deliver a material further advance.

## Original Exploration and Dated Checkpoints

The n = 11 proof supplies a useful architecture for another optimality proof: cover
every packing, exclude most possibilities, capture the survivors in a region where a
short exact argument forces the known side length.
For n = 17, the most promising adaptation couples global occupancy constraints with an
exact theorem about a family of Bidwell packings.
A faster version of the existing lower-bound certificate alone does not supply either
half of that argument.
The [October 5 Status Review](#october-5-status-review) records where the proof stands
after Sessions 166 to 168 and the open stack above PR 347.

This is a W3 exploration, with untested proposals below.
The
[next-session plan](../../../docs/project/specs/active/plan-2026-10-01-post-optimality-w3-session.md)
maps the proposed entry and checkpoints; W10 selects experiments after the opening W3
work. The source baseline is merged main at `f9a3409f0f03298fbeeb0a03788cd016087626b9`,
including the September 30 epistemics revision.
T-060 is machine-checked at **V3/C3** under that rubric; its historical V4/C5 label does
not imply that human proof review has occurred.
No rating or frontier field is changed here.

## What the New Results Change

| Result | Established in the retained record | Research consequence |
| --- | --- | --- |
| [T-060: n = 11](../../frontier/n-011.md) | Exact optimality at Trump’s algebraic side, using global exclusion, capture and a local endpoint theorem | A complete finite-to-continuous proof architecture is available for study and calibration |
| [T-043: n = 17](../../frontier/n-017.md) | R068 gives the strict lower bound 116511/25000 = 4.66044 | Start from the current certificate and identify structural losses; old R052 margins are historical |
| [T-052: n = 21](../../frontier/n-021.md) | Exact optimality at 5, using a mixed point-and-line measure | Retire n21 as an open target; inspect its endpoint accounting for integer-ceiling cases |
| T-061: Wang–Li n11 certificate | A strict rational improvement above 31/8, now superseded by T-060 | Certificate slack and rescaling are useful diagnostics, but do not replace an endpoint theorem |
| [Native arithmetic measurements](../../../docs/project/research/research-2026-09-30-exact-arithmetic-verifier-performance.md) | A bounded Rust verifier comparison preserves exact outputs and reduces measured CPU | Reuse measurement infrastructure when a selected proof lane is expensive; do not infer global replay speed from kernel timing |

The [n17 case](../../frontier/n-017.md) now has a verified rational outward upper
ceiling4.6755300936045509516342148538535054 from the exact chart endpoint.
Together with the established lower bound 4.66044, this leaves a gap of approximately
0.0150901. The certificate admits the known packing; global optimality remains open.

## What Transfers from the Eleven-Square Proof

The [original proof](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md) and
[simplification review](../../../docs/project/reviews/review-2026-09-30-n11-expository-simplification.md)
separate the following obligations.

| Component | General mechanism | What must be established again at n17 |
| --- | --- | --- |
| Closed centre cover | Every square has a centre in a covered region; cells with diameter below 1 hold at most one centre | A complete cover at the chosen cap, capacity proofs and closed boundary treatment |
| Occupancy masks | Reduce continuous placements to finite occupied-cell possibilities | Exhaustive occupancy enumeration; no observed contact graph or symmetry assumption may omit a packing |
| Ownership and common cores | Retain regions forced inside the square over every admitted pose | Sound cores for every angle interval and containment domain, preserving all possible owners |
| Charge and compatibility | Exclude occupancy patterns whose mandatory charges exceed available capacity | Per-atom validity, overlap accounting and global capacity; R068 features need their actual verifier semantics |
| Container symmetry | Transport configurations through exact square symmetries | Complete orbit coverage, including fixed points and seams; cells need not be permuted by the chosen symmetry |
| Capture | All survivors enter a specified terminal region | A complete certificate reaching a proved neighborhood, with no undecided leaves |
| Endpoint theorem | The terminal region cannot contain a smaller packing | A side-minimum theorem for the candidate n17 endpoint family, which may have feasible sliding motions |

For T-060, 16 closed cells give 4,368 eleven-cell masks, 2,184 half-turn classes and
2,180 exclusions; the four surviving cases reduce to a captured case through a separate
symmetry argument. Those sizes are consequences of the eleven-square geometry, not a
generic complexity bound for this method.

A crude n17 sizing calculation illustrates the obstacle.
In a container of side S, all unit-square centres lie in the square of side S − 1,
because every rotated unit square extends at least 1/2 in each coordinate direction.
At the reported S ≈ 4.67553, a 5-by-5 grid has cell diameter about 1.0396, too large for
the simple capacity-one guarantee.
A 6-by-6 grid has diameter about 0.8663, but already admits
`binomial(36,17) = 8,597,496,600` raw masks.
This rules out treating unpruned mask enumeration as a cheap first experiment.
It does not rule out better covers, occupancy constraints or implicit enumeration.

## Priority n17 Routes

### R1. Verify the Candidate and Describe Its Endpoint Family

The [Bidwell record](../../frontier/n-017.md) gives a degree-18 polynomial for the
reported side and two nonzero tilt angles.
It also reports feasible sliding squares.
A side polynomial alone is not a certified packing: coordinates, root selections,
containment and all pair separations must be checked.

First reconstruct the retained witness with a verified feasible upper enclosure.
An enclosure at a slightly larger side establishes an upper bound; equality at the
proposed algebraic endpoint requires a feasible witness at that endpoint itself.
Then separate a constrained backbone from the sliding coordinates and seek an exact
parameterization, or a certified tube containing the family.
For each contact chart, derive a side lower bound uniform over that tube.
The chart family must cover nearby changes of separating features; fixing a sliding
coordinate requires a proved side-preserving normalization.
An exact nonnegative combination of contact inequalities, an interval sign argument, or
a small reduced algebraic elimination may supply the terminal theorem.

**First discriminator:** a coordinate and contact audit identifying which variables
determine the side and which remain free, with a known valid packing as control.
Failure to certify the imported coordinates blocks promotion of that upper bound; it
does not refute Bidwell’s construction.
A feasible motion decreasing side would refute the proposed terminal theorem.
A same-side motion is expected and must be retained.

**Payoff:** a reusable endpoint target for every global route below.
The existing n11 local theorem is a design example, not an n17 checker.

### R2. Build a Small Occupancy Problem Before a Large Search

Try closed Voronoi covers adapted to the candidate geometry, mixed cell capacities, and
intersections of several covers.
Derive exclusions from centre distance, containment and cell capacity before branching
on square angles. Use exact graph or integer constraints to count surviving occupancy
patterns without listing all raw masks.

**First discriminator:** one rational cap above the candidate, a proved complete cover,
exact capacity bounds, and a census of survivors after each independently justified cut.
Report raw count, surviving count, memory and sample exclusion cost separately.
Keep known packings feasible; a cut that rejects one is invalid.
If the residual count remains too large under the declared resource cap, retain the
cover and the obstruction, then switch to a stronger constraint family.
An arbitrary threshold on mask count is not a mathematical failure criterion.

**Payoff:** a costed global capture route instead of an unrestricted 51-variable search.

### R3. Turn R068 Saturation into Constraints on Joint Placements

R068’s weighted-threshold rules and winning subsets already express more than a plain
point measure. Study which angle intervals and placements nearly attain the minimum
charge, and whether seventeen such near-minimizers can coexist.
The useful new statement would be a proved incompatibility between simultaneous
low-charge placements, not another unsupported extrapolation of row slack.
Flat row minima and a small surplus do not prove that reweighting is exhausted: that
needs an exact dual for the current dictionary and domain.

**First discriminator:** audit a fixed sample of the actual R068 binding rows, extract
their minimizing placements and identify a candidate pair or small-tuple obstruction.
Use R068 as a positive control; evaluate the proposed new cut at a declared stronger
side, such as 4.67, with rebuilt core and parent-centre envelopes.
Sampled minimizers only suggest cuts.
A global charge argument needs a complete cover of all low-charge poses, including
event-cell seams. The [X-043 interface](X-043-new-lower-bound-proof-directions.md) makes
the obligation precise: if every pose in class Cj has charge at least ℓj, and every
packing’s class-count vector belongs to a necessary relaxation R, prove
`min(z in R) sum(ℓj zj) > M`, where M is the total available charge.
Prove the selected obstruction over the full continuous domains represented by those
rows before adding it as a cut.
Retain feasible counterexamples and exact boundary contacts.
If all tested low-charge types coexist, that rejects the selected cut, not every
compatibility approach.

**Payoff:** couple a strong existing certificate to the occupancy problem and reduce the
number of expensive geometric cases.
The native reader’s missing R068 features are a separate implementation obligation;
successful replay of a simpler predecessor does not establish feature coverage.

### R4. Establish the Limit of the Present Certificate Architecture

Reuse the existing capacity-one ceiling question H-248 and BC-387 in
[agenda-042](../agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md).
The proposed route seeks weighted families of overlapping squares whose total dual
weight prevents every certificate in a specified atom class from proving the target.

The class must be stated exactly.
The general proposed witness assigns nonnegative weights of total at least 17 to
contained unit squares, with weight at most one on every clique of their
interior-overlap graph.
A triangle-free family of 34 squares, each of weight one half, is a special case.
H-248 targets 4.675 first and then 4.67; it must not be restarted below the lower bound
already certified by R068. Pointwise overlap depth alone does not establish the clique
constraint. The
[lemma review](../../../docs/project/reviews/review-2026-09-27-plan-4640020-lemma-check.md)
explains the passage to strict cores and capacity-one trigger sets.
Larger-capacity constraints and conditional geometry need separate analysis.

**First discriminator:** review the dual lemma against R068’s actual rule types before
searching for the proposed 34-square family.
An accepted dual witness limits a method, not the packing optimum.
A failed search is inconclusive.
Use the existing bead and hypothesis rather than register a duplicate.

**Payoff:** decide whether to invest in new atom types, compatibility, or capture.

### R5. Prove a Backbone Without Assuming the Catalogue Picture

Near the candidate side, area pressure and boundary occupancy may force a finite
collection of wall chains or connected blocks.
Enumerate those possibilities with disjunctive separation constraints and derive side
bounds for each. The witness suggests chains worth testing, but the global theorem must
account for chains absent from it, rotated interiors, degenerate contacts and
disconnected blocks.

**First discriminator:** select one proposed necessary wall-chain or occupancy lemma and
run an adversarial feasibility search for its negation.
Specify whether the lemma concerns all feasible packings, every minimizing packing, or
the existence of a normalized minimizing representative.
An arbitrary feasible counterexample can refute the first statement but need not refute
either of the others.
Certify any resulting packing before calling it a counterexample.
If the lemma survives, retain it as unproved until a complete exclusion certificate or
analytic derivation is available.
Do not make the witness’s three angle values a global restriction.

**Payoff:** reduce the dimension of capture, possibly bypassing a huge mask census.

### R6. A Hierarchy of Local Certificates with Global Coverage

Combine a cheap counting bound at the root with stronger pairwise or neighborhood
certificates only on unresolved cells.
Use exact Farkas witnesses for linear relaxations and interval or algebraic checks for
the nonlinear remainder.
Branch on the variable that removes the most unresolved geometry in a controlled pilot,
then freeze that choice for the measured experiment.

**First discriminator:** compare the old and strengthened relaxation on the same small
residual set, including a feasible terminal-family case.
Count eliminated cells and unresolved cells; separate producer time from independent
checker time and measure certificate size.
Any unproved strengthening invalidates the exclusion.

**Payoff:** spend exact arithmetic on a small residue while keeping the certificate
reader simple enough to audit independently.

### R7. Try a Direct Endpoint Measure

Daniel’s
[endpoint method for n21](../../../docs/project/reviews/review-2026-09-28-evand-s21-s45-mixed-covers.md)
suggests a second route to equality, separate from capture.
At a prospective exact endpoint T17, seek a nonnegative measure of total mass below 17
that assigns mass at least one to every closed unit square contained in the container.
Boundary contact can share mass in an actual endpoint packing.
For a hypothetical packing in a strictly smaller container, dilate it into the endpoint
container and take concentric unit-square cores.
These cores are disjoint closed sets, so their charges would sum to at least 17,
contradicting the total mass.
Precisely, let K = [0,T17]² and μ be the proposed finite nonnegative measure.
Dilation by T17/S makes the parent sides greater than one, so each closed unit core lies
strictly inside its parent, giving `17 ≤ sum(μ(Qi)) = μ(union(Qi)) ≤ μ(K) < 17`. Exact
feasibility at T17 separately supplies the upper bound needed for equality.

**First discriminator:** test a contact-supported measure against the endpoint packing
and its sliding family, then seek an exact finite dual obstruction or a candidate cover.
Algebraic sites, zero-margin contact seams and full continuous coverage remain
verification obligations.
This method is not a strict-parent-core certificate at T17, which would wrongly exclude
the endpoint packing itself.
An obstruction to the chosen site dictionary is not a universal obstruction.

### R8. Change the Certificate Features, Then Measure Their Value

Adaptive sites, richer threshold features and capacity-two resources could improve the
lower bound enough to simplify capture.
Compare them on identical frozen rows, preserving a rational primal/dual pair.
Then verify any candidate against the full parent domain at the proposed new side.
Changing side also changes legal parent-centre envelopes and core containment.

**First discriminator:** one proposed feature family with an exact improvement over the
fixed finite baseline, followed by a continuous counterexample check.
A finite LP gain is a search result until the universal constraints are verified.
Keep this route only if the gain changes the capture problem or yields a material bound;
do not spend the session polishing an immaterial decimal increment.

### R9. Use Settled Small Cases as Subconfiguration Cuts

T-060 gives a direct capacity fact: a square region of side strictly below T11 cannot
contain eleven complete unit squares.
Analogous facts follow from other settled small cases.
These could eliminate branches whose geometry forces too many whole squares into a
subcontainer, or yield capacity bounds for a cover of subregions.

**First discriminator:** derive one exact containment-and-assignment lemma from an n17
occupancy case and apply the known small-case bound to it.
Containment of centres alone is insufficient; whole squares and the strict side
inequality must be proved.
Overlapping subcontainers also require sound assignment or counting rules.
This is a structural use of the n11 theorem, not a numerical implication from s(11) to
s(17).

## Other Low Cases

Values below are the verified bounds in the main snapshot, except where explicitly
marked as reported. Ranking is a research judgment, not a probability of success.

| Priority | Case and verified bracket | Most useful route | First decision |
| --- | --- | --- | --- |
| Primary | [17](../../frontier/n-017.md): 4.66044 < s ≤ 5; reported upper 4.675530… | Family endpoint plus global occupancy/compatibility | Can the candidate endpoint be certified, and can the global cases be compressed? |
| Parallel secondary | [12](../../frontier/n-012.md): 3.968615 ≤ s ≤ 4 | Integer-endpoint occupancy and conditional charge/capacity | Audit the reported additive dual obstruction, then test a route outside its scope |
| First fallback | [20](../../frontier/n-020.md): 4.85 ≤ s ≤ 5 | Transfer the n21 mixed-measure mechanism with stronger occupancy or boundary constraints | Where does losing the twenty-first square break the count? |
| Structural fallback | [18](../../frontier/n-018.md): 4.679 ≤ s ≤ (7 + √7)/2 | Exact backbone/terminal-family analysis paired with stronger lower constraints | Is the construction’s side controlled by a small certifiable subsystem? |
| Structural fallback | [19](../../frontier/n-019.md): 4.8 ≤ s ≤ 3 + 4√2/3 | Same decomposition, with its own contact and boundary classification | Does a local subsystem yield a uniform side obstruction? |
| Reserve | [26](../../frontier/n-026.md): 5.508 ≤ s ≤ (7 + 3√2)/2; [29](../../frontier/n-029.md): 5.71 ≤ s ≤ 5.933834, rounded outward | Defect blocks near grid plateaus and improved exact construction analysis | Is there a substantially smaller proof problem than at n17? |

The reported lower bounds 4.695, 4.815 and 4.895 for n18–20 are intake leads; they are
not substituted for verified fields here.
For n12, the
[retained evand source](../../resources/web/evand-square-packing-2026-09-28/square-packing/s12/README.md)
reports exact fractional obstructions at 3.99 and 4, discussed in the
[mathematical review](../../../docs/project/reviews/review-2026-09-27-evand-s32-s12.md).
The
[October source audit](../../../docs/project/reviews/review-2026-10-01-evand-source-coverage.md)
recovers public support files for the side-4 and side-5 obstructions at revision
`08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5`. They have mathematical review but no fresh
local replay. The newer side-3.99 mass is $48112643084/3999999987$, approximately
12.02816; its support file remains absent from the public tree.
Check the recovered evidence before declaring the entire additive route closed.
An accepted closed-depth dual would obstruct every finite nonnegative spatial measure,
including segments and area, rather than just a fixed point dictionary.
Conditional occupancy is therefore a better initial bet than blindly transferring n21’s
endpoint measure. At side 5, the source’s exact fractional mass is
$10323890641/499999999$, approximately 20.64778, which would obstruct a plain additive
proof of n20 if its exact premises are verified.
T-052’s existing cover has exact mass 20.89474919732: a conditional adaptation must
obtain more than 0.89474919732 of valid budget saving to get strictly below 20, or prove
a correspondingly stronger minimum charge.
An exact dual obstruction could force a change of method rather than merely a better
choice of sites.
Closed cases n13–16 and n21–25 are useful positive controls for capacity
and endpoint arguments.
Additional upper-bound constructions and catalogue changes merit intake under W1/W2, but
do not displace the mathematical priority without a concrete new route.

At integer endpoints, distinguish certificates at S < 4 or S < 5 from equality.
A theorem may exclude every smaller side while allowing multiple optimal families at the
endpoint.
Do not infer n20 optimality from s(21) = 5: deleting a square provides an upper
bound, while monotonicity points the wrong way for the required lower bound.

## New Leads from the October Evand Review

The
[source audit](../../../docs/project/reviews/review-2026-10-01-evand-source-coverage.md)
and
[Astra mathematical review](../../../docs/project/reviews/review-2026-10-01-evand-mathematical-transfer.md)
separate newly reported theorems from research mechanisms.
The source reports $s(60) = s(61) = 8$ and $s(k^2 - 3) = k$ for every integer $k \ge 6$.
The latter reduces all sizes to a finite covering premise in a 7 × 7 box; the Lean
reduction assumes that premise, and the source currently supplies only one exact
implementation for checking it.
These reports neither settle n17 nor replace the obligations in R1–R9.

| Lead | Why investigate it | First discriminator and stopping condition |
| --- | --- | --- |
| Exact limiting configurations for R1/R7 | A continuum cover can fail arbitrarily close to a tight contact even when sampled angles pass. The source uses exact limiting constraints before searching for endpoint weights. | Derive necessary constraints on the proposed n17 sliding/contact family. Test exact feasibility before a global sweep; an infeasible subsystem rejects that certificate template, not optimality. |
| Continuum clique resources for n12 | The source already explores cliques defined by a point and a region, beyond ordinary spatial measures. Its finite box-clique gains nearly disappear at grazing contacts. | Start with an exact finite primal/dual comparison, then seek a uniform bound over the full continuum. Use the mathematical review’s corrected threshold argument if needed; a sampled gain without coverage of grazing contacts is inconclusive. |
| Higher-order local obstructions | The n12 source reports exact witnesses for proper subsets of a proposed obstruction; its claim that the whole leaf has no positive separation remains numerical. First-order certificates can miss a zero-margin plateau. | Identify the first nonzero exact order on a specific candidate family; retain a feasible adversary or unresolved term instead of inferring a global theorem from local derivatives. |
| A periodic family with deficit four | The reported deficit-three proof separates fixed corners, periodic walls and an area interior. A wider boundary pattern might have enough mass saving for $k^2 - 4$. | Price the source’s width-three LP first and require the exact saving condition $D > 1$ before any global checker run. The source estimates 5–10 CPU-hours for that LP and 50–80 for a subsequent check, so this is a reserve campaign, not an automatic overnight job. |

W10 may select a small discriminator from these leads without waiting for every large
external replay. It must state which unverified source premise it assumes.
The finite family premise, s60 replay, and recovered dual checks have separate beads
`think-4k80`, `think-e7xa`, and `think-q5tt`. The
[session plan](../../../docs/project/specs/active/plan-2026-10-01-post-optimality-w3-session.md)
keeps n17 first and limits secondary work to what changes the next decision.

## Approaches to Retire or Restrict

- Retire n11 and n21 as open optimality targets in the new session.
  Preserve their earlier experiments as historical evidence and use their accepted
  artifacts as controls.
- Do not rerun frozen-support weight optimization merely because Rust is faster.
  Require a new structural constraint or measured remaining headroom first.
- Do not copy the n11 exact field, terminal neighborhood, charge partition or D4 case
  numbering into n17. Reuse interfaces and proof obligations, not those constants.
- A local optimum, a rigid contact graph, or a large sample of failed searches does not
  cover all packings. Rattlers also prevent an isolated-point endpoint argument.
- An empty relaxed cell can exclude a case; a nonempty relaxed cell may be spurious.
  Preserve unresolved cases until a stronger argument decides them.
- A partial native replay or a matched bounded benchmark does not independently confirm
  the entire external certificate.

## Selection for the Next Session

Open with three parallel deliverables: n17 endpoint/family analysis, n17 global
cover-and-charge analysis, and low-n endpoint transfer.
The coordinator reconciles them into one n17 experiment and at most one secondary
experiment, each with a frozen falsifier and independent validity checks.
Keep R4 as the existing architecture-ceiling task; use it when it discriminates between
the selected alternatives.

Record source revisions, assumptions, expected information, unresolved proof obligations
and the exact next artifact for every selected route.
The
[session plan](../../../docs/project/specs/active/plan-2026-10-01-post-optimality-w3-session.md)
sets execution dependencies, review boundaries and efficiency triggers.
H-253 through H-257 now discharge rational feasibility, chart fidelity, root existence,
endpoint feasibility and the complete active-feature inventory.
The following execution checkpoint supersedes the initial readiness assessment while
preserving its selection rationale.

## October 1 Execution Checkpoint

[Session 165](../agent-sessions/session-165-post-optimality-overnight.md) has seven
accepted rounds, with immutable inputs and independent review:

| Obligation | Result | Exact Scope |
| --- | --- | --- |
| [H-253](../hypotheses/H-253-n17-retained-rational-upper.md) | Accepted | Replay of the existing rational upper witness through two local exact implementations and the source checker |
| [H-254](../hypotheses/H-254-n17-contact-chart-fidelity.md) | Accepted | All 458 chart-fidelity comparisons at the relaxed rational witness |
| [H-255](../hypotheses/H-255-n17-exact-polynomial-root.md) | Accepted | Exact existence and uniqueness in the fixed root box, with an independently implemented checker |
| [H-256](../hypotheses/H-256-n17-exact-endpoint-feasibility.md) | Accepted | Exact physical endpoint at fixed centroid sliders; all 68 walls and 136 pairs certified, all 187 interval bounds independently recalculated |
| [H-257](../hypotheses/H-257-n17-endpoint-contact-features.md) | Accepted | Complete inventory of 168 owner-axis options, 60 corner-to-active-wall gaps, and nine offsets; all 175 strict interval records independently recalculated |
| [H-259](../hypotheses/H-259-n17-mixed-capacity-cover.md) | Accepted | Complete closed 5-by-5 mixed-capacity cover; 161,100,756 occupancies; independent exact census |
| [H-260](../hypotheses/H-260-n17-closed-cell-symmetry.md) | Accepted | Complete D4 action on existential closed assignments; 20,155,518 orbits; independent eight-term audit |

The
[mathematical review](../../../docs/project/reviews/review-2026-10-01-post-optimality-w3-opening.md)
and
[projection-branch theorem](../../../docs/project/reviews/review-2026-10-01-n17-projection-branches.md)
therefore establish an attained minimum within a declared parameter and
separating-branch family.
The latter removes several orientation assumptions and proves angle rigidity at
equality, while keeping the branch premises explicit.
A rotational freedom at square 6 shows why an isolated-coordinate theorem is
inappropriate.

[H-258](../hypotheses/H-258-n17-common-core-stress.md) selected a fixed common-core
stress for both first-order branches.
Its mathematical recipe passed static review, but three bounded symbolic preparation
attempts did not finish.
The instrument is stopped, and no target stress was evaluated.
Neither stationarity nor its negation has been established.
Exact residual completion, adversarial controls and bounded interval arithmetic remain
prerequisites for a separately admitted future run.
Even a complete stationarity certificate would require further higher-order and global
arguments. H-027’s class-angle derivative threshold is not silently replaced by this
weaker question.

The separately registered
[n12 weighted-cycle review](../../../docs/project/reviews/review-2026-10-01-n12-weighted-cycle-capture.md)
proves a finite-row inequality for arbitrary nonnegative edge weights.
At side 4, canonical componentwise wall repair loses no certificate with a nonpositive
margin bound on a fixed pair support.
This removes wall variables from that conditional certificate problem.
Exact hand controls and independent algebra review passed; no source solver run or
geometric target was replayed.
Global coverage of valid row supports remains the missing premise, so this is not a new
n12 lower bound.

The two main scientific gaps remain local capture of unrestricted orientations and
separating branches, and global exclusion outside a captured neighbourhood.
The [n17 case](../../frontier/n-017.md) now admits the accepted endpoint’s rational
outward ceiling under `think-vdmf`, replacing the grid ceiling 5 while leaving the case
open. The rational H253 witness remains separate fallback evidence.
Low-n and global-cover routes retain their recorded readiness limits rather than
launching a broad search during endpoint work.

## October 5 Status Review

This review covers Sessions 166 to 168 (PR 347), the four diagnostic layers rebuilt from
Guzhou0806’s work (PRs 354 to 360) and wand125’s native branch-and-bound kernel (PR
350). It is a W3 reading of the record: it certifies nothing, runs no experiment, and
changes no bound, verdict or frontier field.
The
[overnight plan](../../../docs/project/specs/active/plan-2026-10-05-n17-overnight.md)
selects the night’s work from it.

### Where the Proof Stands

The target is $s(17) = S^\ast$, with $S^\ast$ the root of the catalogue’s degree-18
polynomial. The bracket on `main` is unchanged since October 1:
$4.66044 < s(17) \le 4.6755300936045509516342148538535054$ (T-043 and T-065, both
`V3/C3`), with Guzhou0806’s R071 at $18641771/4000000 = 4.66044275$ reported and not
replayed (T-093, `V0/C0`). The proof follows the three-part shape of $n = 11$.

| Link | Statement | Status | Where | Evidence |
| --- | --- | --- | --- | --- |
| Upper bound | 17 unit squares fit in a square of side $S^\ast$; the rational ceiling $4.67553009360455095163\ldots$ is registered | machine-certified, independently audited (exact endpoint at the H255 root, 68 wall and 136 pair obligations); the register holds the ceiling, not the exact value | `main` | exp-238, T-065 |
| Identity of the side | $S^\ast$ is the root of the catalogue’s degree-18 polynomial, irreducible over $\mathbb{Q}$ | machine-certified, independently recomputed; the frontier page and T-065 annotated by addition | stack (#347); `main`’s `n-017.md` still says unproved | exp-245, H-265 |
| Lower bound | $s(17) > 116511/25000$ | verified, `V3/C3`, one machine method | `main` | T-043 |
| Frame | every packing of side $S \le S^\ast$ embeds in the $U$-container, $U = 1169/250$, $U - S^\ast \approx 4.7\times10^{-4}$ | proved (monotone embedding) | records | kernel spec §4.1 |
| Cover | 24 closed cells, each of capacity one, cover the centre box; the family lies in one state with margin $0.002112$ | verified, with the depth–width wall lemma proved and reviewed | stack | exp-247, H-266 |
| Census | $\binom{24}{17} = 346{,}104$ states, 43,593 $D_4$ orbits | verified (Burnside and brute force agree) | stack | exp-247 |
| Exclusions | W7 (arity 7, kernel), A (arity 6, branch and bound), SW9 (arity 9, kernel, adaptive rows), N1 (a whole 17-cell state, kernel) are infeasible at cap $U$ | machine-certified and admitted; W7 and A by independent verifiers with reviews; SW9 and N1 by the standing kernel verifier’s full pass under OR-16 as amended, with no per-certificate review, and re-passed by the verifier fixed for the closed-cover defect class ([verifier-rewrites review §6.5](../../../docs/project/reviews/review-2026-10-03-n17-verifier-rewrites.md#65-re-verification-with-the-fixed-verifier)) | stack | exp-249, exp-250 |
| Certified residue | 126,168 states in 15,953 orbits survive, the family’s among them | exact consumer over admitted entries; re-run for this review at `451154f60` with the same counts. Later on October 5, exp-251 admitted lane K’s first arity-7 flag, s182-k1, leaving 102,124 states in 12,929 orbits | stack | census tool; exp-250’s `census.json`; exp-251 |
| Flags | 87 selector flags stand without certificates; if all certify, 2,197 orbits remain (17,168 states). The census tool reads the recheck receipt by default since lane H’s change in this session and projects these figures on exp-250’s four admitted entries; on the pre-recheck receipts it projected 88 and 2,189 | heuristic (float search) | stack | selector receipts, recheck; census tool |
| Per-state exclusion | N1 closed in 3,723 s wall (producer segment 1,336 s, in-process self-check 2,381 s; 2,521 s of process CPU) at 32 bins and was admitted. The two 45-minute runs, on N1 and F1, ended at the producer’s time cap of $0.5\times2{,}700$ s (producer 1,367 s and 1,355 s), not at a fixed point; F1 has never had the two-hour ceiling | one closure, one time-capped run; H-264’s falsifier needs 10 to 20 states | stack | `handoff/k2/h-N1-2h.json`, `h-N1.json`, `h-F1.json`; exp-250 |
| Near-endpoint states | states feasible at $U$ but not at $S^\ast$ must be excluded at the capture cap $U'$ | open; a float sample of 44 residue states found none feasible at $U$ (95% bound: at most about 27 of the 95 distance-2 orbits) | stack | residue process review, Q1 survey |
| Capture | every packing in the family’s state at $U'$ ($U' - S^\ast = 4.49\times10^{-13}$) lies within the local radius | open; pilot 2 met the after-pilot falsifier at round 17 (no two-sided position extent fell by 10% while every widest row was under $1/20$ of its extent); lane R9’s review finds the receipts undecided between a producer limit and the architecture | stack | pilot 2 receipt; [R9 review](../../../docs/project/reviews/review-2026-10-05-n17-capture-r9.md) |
| Local half | the capture-target theorem: a packing of side $\le S^\ast$ in the family’s state, corner at $(\sigma,\sigma)$, with its 45 non-slider coordinates within $1/5000$ of the family’s, has slides in $B_W'$, sixteen squares on the family and $S = S^\ast$ | composition of three machine-certified parts and hand lemmas 1 to 6 of the recipe review, read by one review and not machine-checked end to end | stack | exp-242, exp-244, exp-247, exp-248; composition review |
| Composed argument | census, exclusions, consumer, capture and the local theorem as one proof, with frame, caps and the $u^\ast$ enclosure charged | not written | — | explainer, item 4 |
| Registration | a theorem id, `status: proved`, rung-4 reviews and an oversight record | not started | — | — |

The 92 certificate objects (112,285,110 bytes) are listed in a manifest that passes
`hosted_data check`, but the release they name has no assets, because the cloud
environment refuses uploads; until they are uploaded no verifier can be re-run from a
fresh clone, and the census counts from committed receipts.
Every review of the stack’s mathematics is a single AI review; none has human review,
and T-060’s rungs show what further assurance costs.

The local half covers exactly what its premise says: the family’s own occupancy state,
read with the packing’s corner at $(\sigma,\sigma)$, and coordinates within $1/5000$ at
the exact root. It says nothing about other states, about packings in this state outside
the box, or about $S > S^\ast$. H-261 as worded stays unresolved, because the family
with squares 5 and 6 exchanged meets its premises outside $B_W'$ at side exactly
$S^\ast$; with the state premise that packing is the same family relabelled.
The global half still owes: the residue (15,953 orbits, or 2,197 if every flag proves),
the near-endpoint stage at $U'$, and capture from the cells, not from a $1/1024$ box.

### What Became of the October 1 Proposals

| Item | Disposition | Evidence |
| --- | --- | --- |
| H-253 to H-257 | accepted in Session 165 (exp-235 to exp-239); all on `main` | X-048 checkpoint table |
| H-258 | stopped in Session 165 after three preparation failures; rebuilt in a polynomial ring and accepted in Session 167 (exp-242, 30 s) | exp-242 |
| H-259, H-260 | accepted (exp-240, exp-241) and then set aside: the $5\times5$ mixed-capacity grid counts like a 30-cell cover (161,100,756 states), the family straddles a seam, and the two free cuts leave 7,703,312 orbits; the $D_4$ machinery was reused in the 24-cell cover’s Burnside count | bulk-exclusion design; exp-243 |
| Route R1, endpoint family | done, in capture-target form: exp-242, exp-244, exp-248, exp-245; the local theorem quotients the six slider directions and drops square 6 | composition review |
| Route R2, small occupancy problem | done by a different cover than proposed: the 24-cell capacity-one cover (H-266) replaced the grid; the per-cell charge floors of H-262 were refuted (R068’s charge collapses at the cap; any $D_4$-symmetric linear floor leaves at least 30,966 orbits); sub-pattern exclusion (H-267) is the engine | exp-243, exp-247, exp-249 |
| Route R3, R068 saturation as joint constraints | tested in its per-cell form and refuted; the asymmetric and multi-charge forms remain untested, and the bulk-exclusion review argues (empty common cores) that no charge of R068’s kind realises the floors a free search found | exp-243; bulk-exclusion design |
| Route R4, architecture ceiling (H-248) | untouched; `instrument_ready: false` | ledger |
| Route R5, backbone without the catalogue picture | not pursued as a lemma; the wall-chain structure appears instead as what the kernel closes (W7, SW9, N1) | residue process review §3 |
| Route R6, hierarchy of local certificates | realised as the two-prover pipeline with routing by structure and a per-state tail | residue process review §5 |
| Route R7, direct endpoint measure | untouched | — |
| Route R8, richer certificate features | untouched here; the lower bound moved externally (R071, reported) | n-017.md |
| Route R9, settled small cases as cuts | tested on the grid, where the $s(6)$ and $s(10)$ cuts leave 61.6 million of 161,100,756 states; on the 24-cell cover the cuts bite nothing, since every dilated cell group exceeds the thresholds | route review; bulk-exclusion design |
| Other low cases | n12 weighted-cycle review proved a finite-row inequality; no bound moved; n18–n20 and n26–n29 untouched since October 1 | X-048 checkpoint |

H-261 to H-268 also derive from this exploration (each declares
`derived_from: [X-048]`); this review adds them to its `proposes` list.

### What Sessions 166 to 168 and the Stack Changed

**The census, not the engine, was the first problem, and it is solved.** The minimal
capacity-one cover cut the occupancy census 177 times (7,703,312 orbits after cuts to
43,593), and that is the step that made the global half conceivable.
Nothing on the stack moves the census further; F1’s 23-cell idea (3.4 times fewer
states) is recorded and untested.

**Two provers, two kinds of pattern.** The ownership-induction kernel closes
wall-anchored chains: W7’s west wall pins first and side-N0 then loses every row to
collision; SW9 and the whole state N1 closed the same way (side-N0 and interior-W losing
every parent pose). The interval branch and bound closes interior crowds (A, 41,598
nodes) and did not finish W7 (0.4% of the tree in 30 minutes; 2.3% after 24 million
nodes natively). Mixed patterns of two to four wall cells and three to four interior
cells stalled under both.
The residue review’s predictor stands: the kernel’s cost is set by how many owners ever
own a point, the branch and bound’s by the margin.
F1’s addendum settled two levers against the plan: the octagon core at 32 bins does not
close W7 (the loss that needs 64 bins is the domain sweep over the row, not the core),
and the Taylor relaxation leaves the arity-8 branch and bound above $10^6$ nodes in
every form tried, because 80 to 85 per cent of the open nodes are held by the range of
each pair’s separating normal, a disjunction no relaxation of the coefficients removes.

**The cheapest census progress is the flags that were never tried with adaptive rows.**
The 87 standing flags would each remove a median of about 1,500 orbits from the
certified 15,953, and at most 3,480 (`projected_gain` in the census re-run).
The adaptive-row recipe that closed SW9 where uniform rows stalled (split floor $1/512$,
at most 1,152 rows, 24 rounds, producer share 0.6) has never run on the high-margin
mixed arity-7 flags: six classes with three wall cells and four interior cells, best
penetration $0.010$ to $0.017$, project 2,410 to 3,024 orbits each, and arity-7 closures
also count toward H-267’s own criterion.
NW7, P4 and P5 ran with uniform rows only.
This is lane K of the overnight plan.

**Why a mixed flag stalls, measured on flag 2.** K3’s diagnosis read the saved 1,152-
and 2,304-row nodes: no placement within 0.8 per cent of a side, so the flag is likely
true; side-W0 has no sampled pose that every partner supports (cut margins $0.0016$ to
$0.0042$), while interior-SE and side-S1 are over 90 per cent supported and cannot lose
a row until the west knot shrinks.
At 1,152 rows the kernel’s first-order losses (wall losses to $0.015$, the envelope
core’s $0.0076$) exceeded those margins and the run reached a true fixed point; at 2,304
rows the losses had fallen to about $0.003$ and the knot was still moving when the
producer’s time share ran out.
So this stall is loss-limited, not consistency-limited: a one-partner cut with losses
below the margins would remove side-W0 and close the pattern.
The producer cannot aim its splits at the knot today (its policy splits rows whose
domain stopped shrinking, which spent 36 per cent of the rows on the two supported
owners), so the next flag-2 run needs a producer-policy change before it needs more
time. Whether the other stalls read the same way is lane D’s question.

**The one per-state closure is a time-cap story, not a stall story.** N1 closed under
the two-hour ceiling in 3,723 s of wall, of which the producer took 1,336 s and its own
in-process self-check 2,381 s; process CPU was 2,521 s. Under the 45-minute ceiling the
same state’s producer was cut off at 1,367 s, a near miss of the 1,336 s it needed, and
F1’s producer was cut off at 1,355 s after six rounds.
Neither 45-minute run was a fixed point, and F1 has not been run under the longer
ceiling, so the record holds one closure and no priced stall.
The self-check is the larger cost and is not the admission check: the standing verifier
re-proved N1 in 482 s (0.18 s a row against the self-check’s 0.91).

**Guzhou0806’s layers are bounded negatives and diagnostics, not path progress.** On
flag B at 16 bins and two rounds, pairwise consistency over the kernel’s own atoms
deletes none of B’s 96 rows: in the binary network, where an edge means only that
universal collision was not proved, every row has a complete selection (79 selections,
1,185 pairs replayed), and stronger enhanced cores raise the supported parents from 18
to 41 to 60 of 96 while killing 71 of 79 fixed witness tuples.
Consistency-based pruning without the induction is therefore not a lever at that
resolution; whether finer rows change that was not measured.
The memo-retention measurement (producer peak down 21.0 per cent on A at 16 bins and 12
rounds, canonical bytes identical) and the shared diagnostic controls are engineering.
None of the four layers excludes a state or changes a claim, and their PR bodies say so.

**The native kernel changes search speed, not what the relaxation proves.** PR 350 ports
the branch and bound’s hot paths to Rust behind the unchanged pilot: A certifies in 42.6
CPU-seconds against 434.5 (10.2 times) with the same tree up to the LP’s choice of
optimal duals (41,958 nodes against 41,598), and every bound still passes the
outward-rounded dual check.
W7 still does not close.
wand125’s correction stands in the body: the reading that an independent prover closed
ten times more of W7’s tree per node was a search-order artefact; single-threaded to one
million nodes the two close 2.17 and 2.05 per cent, and Knuth’s estimate puts the
existing structure’s tree on A at about 40,000 nodes against 138,000. The kernel is
buildable on this container (rustup carries the pinned 1.98.0 toolchain with clippy and
rustfmt beside stable 1.97, and the crates are cached), and it changes the arity at
which an interior crowd can be *searched*: at about a thousand nodes a second, $10^6$ to
$10^7$ nodes is twenty minutes to three hours rather than a day to ten.
It does not change admission.
The native path writes no certificate, the certificate run uses the Python path (ten
times slower, same tree), and the branch-and-bound verifier costs 37.3 ms a node
(1,549.8 s for A), so a certificate of $2\times10^5$ nodes is about two hours of
verification and $10^6$ nodes ten, unless F2’s rank-2 verifier rewrite (cut-minimum
cache and gmpy2, estimated six to eight times) lands.
Knuth’s estimator is a routing signal only with its calibration failure in view: it put
A at 20,000 to 120,000 nodes against 41,598 actual, and W7 at a median of $2\times10^5$
and a mean of $7\times10^7$, and W7 did not close in 24 million native nodes.
Route on the mean, with A and W7 as controls.
Review B’s B4 also stands: `n17_bb_native.py` rebinds `Fraction` to `mpq` in every mode,
including certificate recording, where the body says the Python paths are unchanged.

**Capture is where the architecture is in question, and the stack sharpened the question
without answering it.** Pilot 1 at 24 live rows never contracted a position; the
after-pilot review modelled an idealised pairwise induction and predicted contraction
once every owner’s widest row is about a tenth of its position extent, with
$g \approx 0.9$ once calibrated by n11, and named three producer losses (the envelope
core, the owned-hull cap and the one-sided measurement) that would raise that constant
two- to four-fold. Pilot 2 lifted the row cap (256 live rows per owner, with side-N0 at
320, side-N2 at 576 and side-W2 at 416; hull cap 48; the octagon core; minimum row width
$2^{-22}$ in $t$) and drove every ratio under a twentieth for three rounds; no two-sided
position extent fell by ten per cent, and the receipt records `outcome: falsified`. Some
one-sided bounds did move (side-E0’s $y$ to 0.576 of its start, interior-N’s $x$ to
0.935), which the deviation measure cannot show.
Two readings are open.
One is lane R5’s: another producer limit, the hull cap of 48 or the partner pruning,
stands where the row cap stood.
The other is that the architecture’s constant is larger than the probe’s: the dual-norm
argument the review set aside bounds the soft coordinate by
$|\omega_{11}| \le \lVert\lambda\rVert_1\thinspace\ell$ with $\lVert\lambda\rVert_1$
between 921 and 1,439 and $\ell$ the per-row loss, which predicts an angle extent of
about 230 row widths where the probe, with one-sided and correlated losses, measured 36.
Pilot 2’s threshold of a twentieth sits at the optimistic end of the review’s own two-
to four-fold producer factor, so meeting it does not by itself separate the two
readings; a producer limit and a larger constant both predict what was seen.
No capture checkpoint resumes on this container: pilot 2’s `partial.json` is a partial
receipt, `load_checkpoint` refuses a changed hull cap, and a rebuild to round 17 cost
about 34,900 s in one process.

Lane R9 read the per-side extents and the row widths on the soft cycle’s owners (squares
9 to 14 and 16) across rounds 14 to 17 with `score_n17_capture`, and its
[review](../../../docs/project/reviews/review-2026-10-05-n17-capture-r9.md) finds pilot
2’s stall undecided between a producer limit and the architecture.
The receipts exclude all four named producer candidates: the hull cap, the octagon core,
the one-sided measurement and the partner pruning.
The review names a fifth loss that no earlier review listed, the hull-vertex compression
pull (`think-juy9`): `producer.compress` and `kernel_points` move every owned-hull
vertex $2^{-12}$ of its distance toward the hull’s vertex mean before the exact check,
about $1.22\times10^{-4}$ at unit scale.
That is 13 per cent of pilot 2’s box per hull link, too little to explain the stall, but
61 per cent of H-261’s radius $1/5000$, so no kernel capture through a hull link can
reach that radius until the constant is repaired.
Between the 128-row and the by-need runs every turn range moved by at most 6 per cent,
so the fixpoint is set by the box at every row width run; a row-driven reading survives
only with an angle constant of at least 290 row widths on squares 9, 10 and 16. The
review stages the measurement that separates the readings: a positive control on n11’s
state (2 to 4 CPU-hours), then the turn ranges of squares 9, 10 and 16 at twice and four
times the rows with the pull repaired (about 20 CPU-hours), and the position onset only
if those ranges fall (20 to 25 CPU-hours more).
The after-pilot probe that predicted contraction (`lanes/r5/pairwise_probe.py`, in a
Session 168 scratchpad) is on no ref, so its claim that pairwise induction can do no
better cannot be reproduced, and neither can its constants.

**The case for the widened projection theorem rests on curvature, not on the soft
slope.** The scope review’s LP, with the slider domain as rows, gives every one of the
32 coordinate directions a positive slope from $10^{-5}$ to $3\times10^{-2}$ radians,
the softest $0.0155$ per radian along $-\omega_{16}$ ($\beta$ increasing), within 15 per
cent of H-261’s dual bound $1/74.2$ for that coordinate.
Its $0.088$ along $-\omega_{11}$ is not evidence that the soft mode is stiff in angle
space: H-261’s $1/175.8$ bounds growth along every perturbation with the other
coordinates free, and the difference between the two numbers is the co-moving angles
(the 11/12 angle split), which a certificate over an angle box must cover.
What the review rests the theorem on is the sheet curvature, of order $0.3$ per squared
radian against the $33$ that fixes H-261’s radius, so the softest slope-to-curvature
ratio is about $5\times10^{-2}$ and an angle box of radius $10^{-2}$ is within reach,
with feature forcing (least option margin $0.0558$ at the centroid, re-verification
along the family owed) setting that radius rather than the LP. The one unpriced risk is
the patch count of the dual-sheet certificate under dual degeneracy; no instrument for
it exists on any ref.

### The Critical Path and the Overnight Plan

The links that remain open, in the order each gates the next: the capture route
(undecided after lane R9’s review), the per-state price of the residue tail (H-264), the
standing flags, the near-endpoint stage at $U'$, the composed argument and its review,
hosting, and registration.
The obstacles, ranked by how much each could change the route: the per-state stall rate
(unmeasured: one closure, no priced stall); the capture engine (undecided); admission
throughput for large certificates (37.3 ms a node for the branch and bound, 0.10 to 0.18
s a row for the kernel after F2’s rewrite); the hosting block; and the absence of a
second review on every piece.

The
[overnight plan](../../../docs/project/specs/active/plan-2026-10-05-n17-overnight.md)
(session-182) selects the night’s work from this reading and the adversarial review of
it. Its lanes, with the question each answers and what each outcome changes:

| Lane | Workflow | Question | Instrument and budget | Positive result changes | Negative result changes |
| --- | --- | --- | --- | --- | --- |
| K, flag certification | W6 under H-267 (registered, instrument ready) | Do the standing flags with the most census weight close under the adaptive-row recipe that closed SW9, or under the branch and bound where its Knuth mean is at most $1.5\times10^5$ nodes? | eight kernel targets in the plan’s count, nine frozen at registration (arity $\le 7$, at least three wall cells, penetration $\ge 5\times10^{-3}$, in projected-gain order) at 7,000 s each; Knuth estimates on 42 classes; branch-and-bound certificates under 5,400 s; every closure through a standing verifier at `kernel-closed-covers` or later, or `bb-enclosure-retry` | each closure is a permanent exclusion of thousands of orbits; three or four arity-7 closures could decide H-267 after a W2 review | stalls under adaptive rows on mixed arity-7 flags, handed to lane D |
| A, per-state price | W6 under H-264, rewritten in place first (the record named the H-263 cover or the H259 grid and was not instrument-ready; it is unlanded, so conventions §7 allows the rewrite) | Do at least half of a seeded stratified draw of 12 residue orbits (seed 182; 2 at distance 2 reported separately, 7 at 4, 3 at 6; the distance-8 strata unsampled) close under N1’s parameters within a 7,000 s ceiling, and at what producer, checker and verifier cost? | `survey_n17_residue --flag-set arity8 --sample 12 --seed 182` as the draw and float pre-screen; `check_n17_subpattern --bins 32 --max-rounds 24 --hull-limit 16 --max-seconds 7000` per state; at most 26 CPU-hours | the tail of 2,197 orbits is priced from measured CPU and flags become a cost choice | per-state exclusion needs a grammar change (a branch predicate or sub-cell seeds) before the tail is attacked |
| R, the capture route | W3 (lane R9), no CPU | Was pilot 2’s met falsifier another producer limit, and which, or is the architecture wrong? | the pilot-2 receipts and `score_n17_capture` for per-side extents; three hours in 30-minute slices | a producer limit named and pilot-3 settings written, from round 0 with checkpoints | a candidate hypothesis for the widened projection theorem and the patch-count instrument’s contract, for a later W7 build |
| D, stall diagnosis | W3 | Is each lane-K stall loss-limited or consistency-limited, and does flag 2’s reading generalise? | `diagnose_n17_flag support` and `domains` on the saved stall nodes, 1,200 s each at low priority | an aimed-split producer policy is the next build | a branch predicate in the n17 node is the next build |
| H, records and tools | W9 | — | the census reads the recheck receipt (87 flags, 2,197 orbits, 17,168 states); a `--distance` filter for the survey; this addition integrated into X-048 | counts quoted from the tool are the corrected ones | — |
| E, near-endpoint sizing (backfill) | W6 under H-273, registered only if the lane launches | Do any of the 95 distance-2 orbits place at $U$ in float? | `survey_n17_residue --flag-set arity8 --distance 2 --sample 0`, about 5.4 CPU-hours | the near-endpoint stage is non-empty and the composed argument needs exclusion at $U'$ | “no placement in $N$ searches”, recorded as unresolved |

Left out of the overnight plan, each for a stated reason there: a capture rebuild or
pilot 3 (no checkpoint resumes; about 9.7 hours in one process to round 17; lane R
chooses the producer change first); the “exact LP” half of lane R9 (the after-pilot
probe, which is on no ref, reported zero first-order extent, and the kernel spec gives
the $U'$ radius); the dual-sheet patch counter (no instrument on any ref); resuming the
residue-universe sweep (its chunks 0 to 60 were in another container and never
committed, so it would restart; 787 CPU-hours remain, and its own falsifier is met so
far at 39.3 per cent of the residue covered); the native kernel (buildable, but
admission is verifier-bound); F2’s verifier rewrite, a branch-predicate grammar and the
compiled kernel backend (multi-slice builds with reviews); the 92-object upload and the
R071 replay (egress, Boost); and the composed argument, which waits on the capture route
and the near-endpoint stage.

### Candidate Hypotheses for the Codifier

Unnumbered, as X-047 and X-049 left theirs; the registry’s highest id on every ref is
H-272, and the plan registers H-273 only when lane E launches.
None is a verdict on anything.

**C1. The distance-2 orbits are infeasible at $U$** (the plan registers this as H-273
when lane E launches).
*Claim:* each of the 95 one-square-move orbits of the 2,256-orbit frame is infeasible at
cap $U$. *Mechanism:* a one-square move loses one of the family’s contacts and must be
accommodated within the cap’s slack of $4.7\times10^{-4}$ above $S^\ast$; the float
survey found every one of 44 sampled residue states, nine of them at distance 2,
infeasible at $U$, the smallest penetration being $9.1\times10^{-3}$. *Falsifier:* an
exact placement at $U$ of any of the 95; then stage 5 of the residue pipeline is
non-empty and the consumer needs the cap ladder.
*Expected information:* the size of the near-endpoint stage.
*Limits:* float search can refute the claim but never confirm it, so a negative outcome
is “no placement in $N$ searches”, recorded as unresolved; the pricing of per-state
exclusion on these orbits is H-264’s question, not this one’s.

**C2. Kernel stalls on mixed flags are loss-limited** (needs a W7 build before it is
instrument-ready). *Claim:* for at least half of the kernel-stalled standing flags, the
stall node has an owner with support share below 10 per cent whose median cut margin
exceeds the kernel’s first-order losses at the run’s finest row, so aimed splits on that
owner and its partners, with the octagon core and a longer run, close the flag at 64
bins. *Mechanism:* K3’s reading of flag 2: the knot owner is unsupported by margins of
$0.0016$ to $0.0042$, which the losses at 1,152 rows exceeded and the losses at 2,304
rows undercut, while the two supported owners took the split budget.
*Falsifier:* a classified loss-limited flag that runs to a fixed point with the aimed
policy and leaves the knot owner live with its margins unchanged; or most stall nodes
having every owner over half supported.
*Expected information:* whether the next build is a producer policy or a grammar change;
lane D’s classification is the first half of the test.
*Limits:* the aimed-split policy does not exist and is a producer change with its own
slice; the diagnostic is float on sampled poses, a lower bound on support and an upper
bound on margins.

**C3. The kernel capture’s constant is larger than the probe’s.** *Claim:* at $U'$ on
the family’s state, two-sided position extents begin to contract only when the widest
live row on the soft cycle’s owners (squares 9 to 14 and 16) is well below a twentieth
of the position extent, at a ratio set by the dual-norm bound rather than the probe’s
measured constant. *Mechanism:* the after-pilot review’s probe found contraction near a
tenth with an angle-extent constant of 36 row widths, and set the dual-norm argument
aside, which with $\lVert\lambda\rVert_1$ between 921 and 1,439 predicts about 230; its
own producer-loss factor of two to four puts the onset between a twentieth and a
fortieth. Pilot 2 stopped at a twentieth, so it excludes the probe’s constant and the
factor-two end and is silent on the rest.
*Falsifier:* contraction of a two-sided position extent by ten per cent at a ratio
between a twentieth and about a fortieth, which would mean a producer limit explains
pilot 2 and lane R5’s constant stands.
*Expected information:* whether the kernel can deliver $1/5000$ in positions at all, and
how many bisections past pilot 2 it needs.
*Limits:* the “about 230 against 36” is the review’s own pair of numbers and the
fortieth is its own factor; a scaling from the angle constant to the position onset is a
scaling argument, not a model result; each bisection on seven owners multiplies the
per-round cost by two to four, and no pilot checkpoint resumes here.
Lane R9’s [review](../../../docs/project/reviews/review-2026-10-05-n17-capture-r9.md)
(§5) recomputes the constant for the octagon core pilot 2 used at 160 to 250, below the
290 row widths that pilot 2’s turn ranges already reach, and replaces this window: the
turn ranges of squares 9, 10 and 16 fall by at least a fifth when their rows are halved
again, and position contraction begins when every owner’s rows are under about $1/100$
of its extent.

**C4. Two-engine capture.** *Claim:* capture of the family’s state at $U'$ decomposes
into a kernel stage from the cells to angles within $5\times10^{-3}$ and centres within
$10^{-2}$ of the family, and a dual-sheet certificate of the widened projection theorem
from there to $S \ge S^\ast$ with equality on the family, with at most $10^5$ direction
patches on the seven backbone angles.
*Mechanism:* once the 135 unavailable options are forced negative (least margin $0.0558$
at the centroid), separation along each pair’s endpoint feature is linear in the centres
and the side, so the value function over the angle box is a parametric LP whose dual
sheets are nearly linear: coordinate slopes constant to three digits over three decades
of radius, curvature of order $0.3$ per squared radian against the $33$ of H-261’s
recipe, softest slope $0.0155$ along $-\omega_{16}$, so the ratio that fixes a radius is
about $5\times10^{-2}$ where H-261’s is $1.7\times10^{-4}$. *Falsifier:* a patch count
above $10^6$ under dual degeneracy; a sheet with negative slope inside the angle box, in
particular along a co-moving direction such as the 11/12 angle split where H-261’s bound
falls to $1/175.8$; the centroid margins failing along the slider family; or the kernel
failing to bring squares 9, 10 and 16’s turns under $5\times10^{-3}$ from the cell seed
(after pilot 2’s 128-row run, from a $1/1024$ box, those turns spanned $1.5$ to
$2.8\times10^{-2}$, by the local-radius review).
*Expected information:* replaces the open-ended kernel capture by two bounded
instruments and moves the terminal theorem from H-261’s radius to the feature-forcing
radius.
*Limits:* the instrument is unbuilt (one slice plus review, by the scope review),
and its patch count is uncounted; the frame and $u^\ast$-enclosure obligations are
unchanged; square 6 stays coarse; the kernel stage from the cells is where thirteen of
seventeen owners own nothing at the seed.

**C5. Branch predicates restore reach** (a grammar change: producer, checker, verifier
and a review before any certificate it writes is admissible).
*Claim:* a closed centre-halfplane split of each side cell along its long axis (two
children, n11’s existing predicate grammar) gives owners that own points from the seed,
and on the K2 states where 11 and 14 of 17 owners owned nothing, at least one child pair
closes within the two-hour ceiling where the parent stalled; separately, confining
side-W0 to one tilt direction closes flag 2 in both children at 64 bins.
*Mechanism:* a half-cell has diameter below one and a non-empty common core; K3 measured
side-W0’s ideal owned region rising from 0.73 to about 0.9 under one tilt direction.
*Falsifier:* both children stall as the parent did.
*Expected information:* whether reach, not margin, is what stalls per-state nodes, and
whether branching is the missing grammar for mixed flags.
*Limits:* the n17 node admits no constraints today; the consumer needs a rule that
admitted children cover the parent.

**C6. Asymmetric multi-charge floors are unrealisable** (open question, closes route
R3). *Question:* does any valid packing charge at cap $U$ realise per-cell floors that,
taken over the eight $D_4$ images, exclude all but $10^4$ orbits of the 24-cell census?
*Mechanism:* the bulk-exclusion review’s empty-common-core argument predicts no, and
names a one-sided LP over a point measure on a fine grid that would show it.
*Expected information:* a definite close of X-048’s route R3, which exp-243 refuted only
for symmetric linear floors.
*Limits:* a negative LP value closes the point-measure class only; majority features are
relaxed by points.

**C7. Admission is verifier-bound for large certificates** (a cost claim for W5, not a
proof claim).
*Claim:* for the branch and bound, verification costs about 37 ms a node on
the current verifier, so a flag whose Knuth mean exceeds $2\times10^5$ nodes cannot be
admitted in a night whatever the search speed, and the estimator’s median is not a safe
routing signal (W7: median $2\times10^5$, mean $7\times10^7$, unclosed at 24 million
nodes); for the kernel, the producer’s in-process self-check (0.91 s a row on N1) costs
five times the standing verifier (0.18 s a row) and is not the admission check under
OR-16 as amended. *Falsifier:* measured per-node and per-row costs after F2’s rank-2
step, or a Knuth mean within a factor of three of the actual tree on both A and W7.
*Expected information:* which of F2’s steps unlocks native-scale certificates, and
whether the self-check can leave the admission path.
*Limits:* the self-check remains the producer’s own control; dropping it from the
admission path changes no soundness argument but should be a recorded decision.

### Risks to the Claims Already Made

None of these is a soundness defect; each is a place where the wording was stronger than
the evidence, or could be read so.
Three items were corrected on #347 at `0e01d6580` while this review was written and are
marked so; #354 to #360 had not yet taken that commit.

- Corrected at `0e01d6580`: the explainer now labels the capture-target theorem “proved,
  with one review”, naming hand lemmas 1 to 6 as not machine-checked end to end; its
  global-half row says a state near the endpoint may be feasible at $U$ and must be
  excluded at a cap in $[S^\ast, U]$; and its Evidence Status table cites the
  verifier-rewrites review’s §6.5 for the SW9 and N1 re-verification.
- Corrected by lane H in this session: the census tool projected 88 flags and 2,189
  orbits from the pre-recheck receipts while the records said 87 and 2,197. It now reads
  the recheck receipt by default and projects 87 flags, 2,197 orbits and 17,168 states
  on exp-250’s four admitted entries, and 86 flags once s182-k1 is admitted; a
  projection quoted from the tool before the change should say which receipts it used.
- PR 347’s “63 per cent of the global half’s orbits are excluded” is arithmetic, not
  progress: the residue is the endpoint’s Hamming neighbourhood, where small
  certificates are rare.
- PR 350’s body still says certificate and Taylor runs “use the Python paths unchanged”;
  `n17_bb_native.py` rebinds the rational type in every mode (Review B, B4). No wrong
  output was found; the sentence is wrong.
- The flag-2 verdict “likely true” rests on float search; the explainer says so, and the
  qualifier should travel with the verdict wherever it is copied.
- The sweep summary’s top class removes 539 orbits *of the 2,264-orbit projection*, as
  the greedy cover’s first marginal; the class (the pilots README calls its $D_4$ image
  a north-wall crowd) stalled under uniform and octagon cores at 64 bins.
- Corrected here: `X-048`’s `proposes` omitted H-261 to H-268 although each declares
  `derived_from: [X-048]`.
- One frame subtlety for the composed argument, a reading rather than a finding: the
  composition review states the global half’s obligation as reading the occupancy state
  with the packing’s corner at $(\sigma,\sigma)$. Exclusions hold for any placement in
  the $U$-container, so that reading is admissible for them, but the $D_4$ transfer of a
  surviving state to the family’s representative is clean only in a placement that the
  symmetries preserve, the centred $U'$-box; embedding A is then what capture
  *concludes* (the family’s corner squares are pinned there), not what it assumes.
  The composed argument should read states in the centred box and let the capture supply
  the frame.

### Evidence Status

| Kind | Items |
| --- | --- |
| Re-run for this review | the certified census at `451154f60` (126,168 states, 15,953 orbits, 88 flagged classes, 2,189 projected; per-flag `projected_gain` median about 1,500, maximum 3,480); `hosted_data check` on the manifest |
| Read from receipts | pilot 2’s settings, per-round ratios, extents and CPU; the N1 and F1 per-state receipts (wall, process CPU, producer and checker segments, `producer_outcome: time_cap`); the sweep summary; the manifest sizes; the flag-2 diagnosis tables; `h-sample.json`’s eight chosen states |
| Read from records | every count, cost and verdict cited to an experiment, review or hypothesis above |
| Measured by the adversarial review and adopted here | the corrected projection 87 flags, 2,197 orbits, 17,168 states on a converted recheck receipt, which the census tool reproduces after lane H’s change; the rebuild cost of pilot 2 (about 34,900 s); the installed 1.98.0 toolchain |
| Derived here, needing review | the dual-norm reading of pilot 2 and the onset window in C3; the two-engine decomposition; the frame note; the verifier-bound cost claim |
| Not done | any experiment; any verification of a certificate; any change to a record |

## October 5 Evening Addition: H-267 Accepted

Added after Session 182’s exp-251 verdict and its W2 review; nothing above is changed.
[H-267](../hypotheses/H-267-n17-isolated-sub-pattern-residue.md) is accepted
([exp-251](../series/series-000-smoke-and-calibration/experiments/exp-251-h267-n17-overnight-flag-certification.md),
confirmed with corrections by
[its W2 review](../../../docs/project/reviews/review-2026-10-05-exp-251-h267.md)). The
certified sub-patterns of arity at most seven leave 9,990 orbits of the unique-state
cover at `488c72d77`, ten under $10^4$, the endpoint’s state surviving
([census-arity7-after-bc427-t4.json](X048-session-182-overnight/receipts/K/census-arity7-after-bc427-t4.json)).
That count includes A, certified by the branch and bound under exp-249’s recorded
deviation, and is 10,173 without it.
After `s182-bc427-t6` (`340e92b84`) it is 8,191 orbits
([census-arity7-after-bc427-t6.json](X048-session-182-overnight/receipts/K/census-arity7-after-bc427-t6.json)),
which no longer depends on A. Neither count includes lane K’s target 2, whose closure is
held for the owner’s ruling.
Every entry carries a standing verifier’s full pass, but the certificate objects are not
yet uploaded (`think-jhgi`), so re-verifying any of them elsewhere waits on that.
H-267 is a census statement: it moves no bound and no frontier field.

## Planning Review

Astra at max reasoning reviewed the transfer mechanisms and draft mathematics.
Sol separately audited current low-n bounds and reported obstruction sources, and
another Sol review checked workflow, document structure and execution boundaries.
The integrated corrections distinguish a flexible endpoint from isolation, exact
feasibility from an outward upper enclosure, whole-clique constraints from pointwise
depth, and sampled weak poses from complete coverage.
Upper bounds in the comparison table are exact or rounded outward.
These are reviews of proposed research, not fresh proof replays or endorsements of the
untested hypotheses.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
