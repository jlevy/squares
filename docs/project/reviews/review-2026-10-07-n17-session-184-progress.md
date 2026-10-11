---
title: n17 Session 184 Progress and Remaining Proof Obligations
date: 2026-10-07
status: in-progress-review
---
# n17 Session 184 Progress and Remaining Proof Obligations

This review consolidates the current evidence from the ten-hour Session184 continuation
on `codex/n17-state-review`. The [W3 review](review-2026-10-06-n17-w3-consolidation.md)
preserves the launch assessment; the
[session record](../../../packing/campaign/agent-sessions/session-184-n17-proof-contracts-and-instruments.md)
records execution and costs.
The mathematical analysis and selected proof interfaces belong to
[Astra’s research report](../research/research-2026-10-07-n17-proof-interfaces-and-lp-contract.md).
The final selected mathematical result is exp288. The
[capacity and route-selection review](../research/research-2026-10-07-n17-w3-capacity-and-route-selection.md)
uses these results to prioritize the next block; final engineering evidence is recorded
separately below.

## Current Theorem State

The optimality of the known17-square packing remains open.
The verified strict lower bound is `s(17) > 18641771/4000000 = 4.66044275` at V3/C3. The
exact feasible endpoint has the outward upper ceiling
`4.6755300936045509516342148538535054`; its identification with the degree18 catalogue
root was already settled before this session.
The [frontier case](../../../packing/frontier/n-017.md) distinguishes these claims.
The fixed lower-bound charge has only `2.5e-8` of additional runway, so another
refinement of that unchanged charge cannot bridge the remaining gap.

The composed proof still needs a complete closed-cell cover, exclusions outside the
endpoint family, global capture into a proved local target, and a valid application of
the local family theorem under checked premises.
The existing local result assumes a specified frame and45 non-slider coordinates within
`1/5000`; it does not supply global capture.
Optimality and uniqueness remain distinct goals.

The current ordinary U-cap exclusion ledger has60 admitted entries, leaving36,768 states
or4,683 D4 orbits, with the endpoint retained.
Session184 eliminated two orbits,16 states, from the58-entry launch baseline.
The95 distance-two orbits remain unresolved.
Historical low-arity milestones and sampled closure rates are not the current queue or a
completion price for it.

## Accepted Progress

| Result | Evidence and scope | Consequence |
| --- | --- | --- |
| Two ordinary exclusions | [TailA](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-266-h282-current-tail-a.md) and [TailB](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-274-h287-current-tail-replication.md): production, fresh replay and full standing verification, followed by ledger admission | Current residue decreases from4,685 to4,683 orbits. |
| Continuous local inequalities | [Widened feature forcing](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-261-h278-widened-feature-forcing.md), [apex bridge](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-264-h279-apex-replay-repair.md), [annulus patch](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-263-h280-one-annulus-patch.md), [negative cone](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-267-h283-continuous-soft-direction-cone.md), [positive cone](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-269-h284-positive-continuous-cone.md), and [coarse-slider floor](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-270-h285-coarse-slider-floor.md) | Exact scoped ingredients; their angle, coordinate, root and slider premises still need capture from the original cover. These do not form a complete angular annulus cover. |
| Rational cap join | [exp275](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-275-h288-capture-cap-root-join.md): `V=935106018721/200000000000` and a fresh dyadic root enclosure | The new cap lies above the certified endpoint side. This resolves a cap interface, not capture. |
| Numeric-cap first round | [exp276](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-276-h289-numeric-cap-first-round.md): all16 contracting-owner updates and independent zero-production replay | An accepted native parent for subsequent conditional tests; no geometric terminal predicate closes. |
| Parent intake | [exp277](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-277-h290-numeric-checkpoint-capture.md):49 exact intervals and all17 endpoint poses | All29 positions, all16 angle projections and all three slider domains fail the relevant capture boxes. Every active owner still represents the full orientation interval. |
| Centered-cap standing control | [exp280](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-280-h291-centered-endpoint-hull-capacity.md): full standing STALL with the correct48-vertex hull allowance | A checked centered-U/V interface that retains the known endpoint; no exclusion or ordinary ledger admission. |
| Conditional owned points | [exp282](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-282-h292-conditional-owned-hull-scoped-input.md): five new strictly owned points for owner0 on the closed angular guard `[13/32,27/64]`, independently reconstructed | All four support gains exceed `1/1024`. The unguarded gains fail. This is a conditional ownership lemma, not an excluded state. |

## Negative and Incomplete Results

[LP reconnaissance](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-260-h277-widened-lp-reconnaissance.md)
was numerically informative but inconclusive; it supplied no exact dual certificate.
The accepted
[saved-prefix capture test](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-272-h286-saved-prefix-capture-leaf.md)
also failed every geometric terminal predicate.
These results do not establish that a physical packing exists outside the local target.

The original conditional continuation exp283 refused at a native-custody join.
The separately repaired
[exp284](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-284-h293-parent-guard-native-custody.md)
produced all16 updates, but its fresh300-second replay stopped incomplete.
Its unique native candidate is retained for reproducing that resource failure.
No child geometry, mathematical criterion-miss or exclusion was accepted from it.

[Exp285](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-285-h294-pooled-parent-center-cases.md)
completed construction and fresh finite reconstruction in20.74 seconds.
It used only the accepted original-parent kernels and the five exp282 points.
Direct unpooled and pooled intersections were absent; the unsplit test and all four
closed centre cases remained unresolved.
Each case nevertheless constructed a nonempty seven-vertex common owned region.
This is a completed negative result for the frozen shared-point recipe.
The accepted receipt has543 raw pooled points but nonempty pools for only owners0,1,2,3
and20; therefore only four foreign point pools are available to the next recipe.

The separately registered
[exp286](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-286-h295-pooled-forbidden-cover.md)
completed construction and fresh finite verification in20.73 seconds.
Both the ordinary-final-hull and pooled-point controls left all18 necessary pieces
uncovered: six on the first singleton seam, four on the interior row, and eight on the
last singleton seam.
The common strict cores passed their exact checks.
This is a complete miss for the frozen union-cover recipe, with no excluded angular
slice or census admission.

## Reduced-Model Witness and Next Mathematical Step

The fixed single-square discriminator
[exp287](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-287-h296-pooled-relaxation-witness.md)
completed construction and fresh verification in1.11 seconds.
At the fixed rational angle parameter `53/128`, its first deterministic centre passed
every conditional owner0 strict-ownership test and all16 foreign open-interior avoidance
tests, but failed numeric-container containment.
This is a completed recipe miss; it establishes no valid one-square relaxation witness.
No alternate centre or angle was evaluated.

The separately registered
[exp288](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-288-h297-pooled-feasible-center.md)
imposed exact fixed-angle container walls and all conditional owner0 body-axis strips
before selecting the first centre outside the closed foreign collision regions.
Construction and fresh reconstruction completed in0.194 and0.200 seconds; bounded
supervision completed in1.120 seconds with cleanup.
Its first candidate on row26/piece0 passed every original pose predicate: container
containment, conditional strict ownership and avoidance of all16 foreign owned hulls.
The square touches the container’s left wall, so retaining closed boundaries matters.

This constructive witness establishes that the specific retained-point relaxation admits
this pose.
It supplies no17-square packing, global counterexample, capture, angular-slice
exclusion or census admission.
The fixed `2^-20` ownership margin and closed foreign obstacles remain conservative
restrictions; no exhaustive fixed-angle search is claimed.

The selected next source of information is the partners’ complete centre and angle
covers. A stronger coupled-cover implication must preserve every closed partner row and
piece and prove exclusion or capture of a declared closed region.
The tested finite recipes supply no proved dominance over one another, and no exp284
geometry is used.
Exp288 construction and replay each have a60-second ceiling,120 seconds
combined. The actual supervisor samples a4GiB RSS limit per live process and cleans up
the owned process group; it supplies no allocation-time hard cap or aggregate-group
enforcement. Exp286’s retained launch and manifest incorrectly named aggregate
enforcement. Its outcome record preserves that metadata deviation and the actual sampled
scope.

## Earlier Proofs, Verification and Publication

The recent n11 optimality result T-060 establishes
`s(11)=3.8770835900228141773078970601…` at V3/C3/S5. Its
[optimality review](review-2026-09-29-n11-optimality.md) and the three retained
explainer sources describe
[lower-bound development](../../../packing/devtools/templates/n11-lower-bounds-explainer-article.md),
[the threshold certificate](../../../packing/devtools/templates/n11-threshold-bound-review-article.md),
and
[the optimality proof](../../../packing/devtools/templates/n11-optimality-review-article.md).
T-112’s uniqueness result and the scoped
[Lean statement audit](review-2026-10-06-n11-lean-formalization-statement-audit.md) are
separate claims; the latter does not formalize the entire geometric proof end to end.
Session184’s n11 native readiness control exercises the retained producer/replay path;
it creates no new n11 theorem or n17 exclusion.

New native objects are preserved locally with narrow hosted-data manifests.
Publication and clean-fetch recovery remain unverified.
The older200-object collection, approximately2.136GB, remains unavailable on this Mac;
the new local objects do not repair that collection’s custody gap.

Source controls, mathematical review and independent mechanical review precede each
target run. The session’s push gates have retained failures, followed by scoped repairs
or unchanged focused controls; no full checkpoint pass is claimed here.
Exp284’s incomplete mathematical replay is not repaired by engineering tests.
The final checkpoint must record source identity, complete selection, failures and
skips. Finite receipts are exact computational checks; their geometric composition and
coverage implications have sole-Astra hand review, without independent mathematical
review or a machine-checked end-to-end proof.

## Final Verification and Handoff

The
[final checkpoint record](../../../packing/campaign/agent-sessions/session-184-final-checkpoint.json)
preserves the source identities, complete selections, counts and remaining obligations.
The ordinary full checkpoint at `969588d09` completed all 101 selected steps in 3,493.53
seconds: 90 passed, eight failed and three skipped.
The exact proof, Rust, slow symbolic rebuild and exhaustive lanes passed.
The full checkpoint nevertheless failed, and the three missing `sqsearch` steps remain
unverified.

The later push checkpoint at `800bba638` completed all 61 selected steps in 357.24
seconds: 59 passed and two failed.
Both failures arose from the missing W3 entry and report count in README. Its reachable
normal phase recorded 3,617 passes, 19 skips and one failed README worker baseline; the
complementary pool phase did not run after that failure.
The README correction subsequently passed the direct check and the exact failed worker
baseline. These additive results do not relabel either complete checkpoint as passed.

Further scoped checks reconciled all 37 original failed mutation controls after
restoring isolated project discovery, verified the primary browser floor and 56 liveness
controls, and retained a genuine green hosted cohort for test ownership.
The expensive exact positive-cone rebuild passed in the full checkpoint; its measured
slow declaration keeps that cost explicit rather than weakening the check.
Two historical byte pins still fail even though both newly produced toy certificates
pass complete independent exact verification.
Their byte-drift provenance remains open under `think-8xdr`. Atlas rendering drift,
existing timing findings and the missing engine checks also remain distinct obligations.

The finalization contract now permits successive reserved slices while rejecting any
resumption of research after the first such slice.
All 21 affected clock, phase and session controls passed in 1.18 seconds, with zero Ruff
or type findings; the two new boundary controls also passed independent review.
The session stops with certification pending under `think-7hy3`. No full pass on the
actual final source or end-to-end optimality proof is claimed.

The
[official cost receipt](../../../packing/campaign/resource-usage/codex-task-tree-session184-through-20261007T165726Z.yaml)
covers 07:08:33–16:57:26Z: 9.81 hours of elapsed envelope and 39.20 overlapping
agent-hours.
Three live sessions make it a lower bound; subsequent publication is outside
this cutoff. Earlier overlapping partial receipts are retained but not summed.
The limited finalization-repair bead is closed locally; a conflicting remote tracker
sync remains pending, with its closure preserved in the local outbox.

The
[strategic W3 assessment](../research/research-2026-10-07-n17-w3-capacity-and-route-selection.md)
selects complete partner-pose coupling as the next mathematical discriminator
(`think-hkqz`), with a matched exact-replay profile in parallel (`think-svkl`). Each
first decision receives a one-to-two-hour allowance.
A deeper two-to-four-hour optimization block requires a measured hotspot and exact
equivalence; a twofold speedup is a proposed acceptance target, not a forecast.
Certificate-family lifting and a necessary structural normal form are the next
alternatives if coupling loses the correlations needed for complete coverage.

Progress belongs in comments on the
[n17 tracker](https://github.com/jlevy/squares/issues/405); the main issue body
describes the goal and durable background.
The [draft PR](https://github.com/jlevy/squares/pull/404) carries the consolidated
branch.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
