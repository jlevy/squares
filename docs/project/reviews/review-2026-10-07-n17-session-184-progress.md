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
This is an interim checkpoint through exp287; subsequent results require an explicit
update.

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
endpoint family, global capture into a proved local target, and the local family
theorem.
The existing local result assumes a specified frame and45 non-slider coordinates
within `1/5000`; it does not supply global capture.
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

## Selected Next Mathematical Discriminator

The fixed single-square discriminator
[exp287](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-287-h296-pooled-relaxation-witness.md)
completed construction and fresh verification in1.11 seconds.
At the fixed rational angle parameter `53/128`, its first deterministic centre passed
every conditional owner0 strict-ownership test and all16 foreign open-interior avoidance
tests, but failed numeric-container containment.
This is a completed recipe miss; it establishes no valid one-square relaxation witness.
No alternate centre or angle was evaluated.

The next separately registered recipe will impose exact fixed-angle container walls and
all conditional owner0 body-axis strips before selecting the first centre outside the
closed foreign collision regions.
Its fixed `2^-20` ownership margin and exclusion of boundary-only foreign contact make
the search conservative: a completed miss would not prove that no admissible pose
exists. A selected candidate must still pass every original exp287 pose predicate in a
fresh reconstruction.

Such a witness would diagnose missing cross-owner constraints; it would not be a
17-square packing. If it passes, the next different information source is the partners’
complete centre and angle covers, rather than more point pooling.
That prospective proof must preserve every closed partner row and piece.
The tested finite recipes supply no proved dominance over one another, and no exp284
geometry is used. Construction and replay each have a60-second ceiling,120 seconds
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

Progress belongs in comments on the
[n17 tracker](https://github.com/jlevy/squares/issues/405); the main issue body
describes the goal and durable background.
The [draft PR](https://github.com/jlevy/squares/pull/404) carries the consolidated
branch.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
