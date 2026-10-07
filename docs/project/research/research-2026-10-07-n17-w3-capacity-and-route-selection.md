---
title: n17 W3 Capacity and Route Selection
date: 2026-10-07
status: strategic-review
---
# n17 W3 Capacity and Route Selection

The dominant limit is the missing global geometric argument.
Faster computation would help a specific verification bottleneck, but the current search
has not shown that its surviving configurations must enter the proved local region.
The next investment should test a stronger geometric representation while profiling
exact verification in parallel.
A larger unchanged search budget is not yet justified.

This judgment uses the
[Session 184 results](../reviews/review-2026-10-07-n17-session-184-progress.md) and
[proof contracts](research-2026-10-07-n17-proof-interfaces-and-lp-contract.md).
The recommendations are new selections from the existing
[W3 portfolio](../reviews/review-2026-10-06-n17-w3-consolidation.md), not new proof
claims. Work estimates below budget a decision or prototype.
They do not estimate when optimality will be proved.

## What Is Limiting Progress

| Limit | Measured evidence | Consequence for capacity |
| --- | --- | --- |
| Global capture and complete coverage | The admitted residue is 36,768 closed assignments / 4,683 D4 orbits under 60 entries, including 95 unresolved distance-two orbits. The actual numeric-cap parent fails every local, widened, apex and patch predicate. | A faster local theorem or more exclusions alone cannot close the composed proof. Every remaining state needs an exclusion or a valid route into a terminal domain. |
| Loss of geometric information | Exp-285 found no shared-point contradiction in any of four centre cases. Exp-286 left all 18 necessary pieces uncovered. Only five owners have nonempty retained point pools, leaving four foreign pools for the selected owner. | Common interior points omit much of the partners’ centre and angle information. The next test should use that information rather than merely recompress the same points. |
| Full verification throughput | Exp-284 produced 16 updates in 292.02 seconds internally; its production phase took 310.09 seconds. Fresh verification exceeded its 300-second tool ceiling, so the child is unaccepted. | Verification is a real engineering constraint. Faster replay could recover an accepted nonclosure from this candidate; it would not turn the producer’s nonclosed result into an exclusion. |
| Incomplete local-to-global joins | The feature, apex, patch and two cone certificates are conditional. The original-cell parent still has all orientations represented, and its coordinate bounds greatly exceed the required boxes. | Completing an angular annulus without first obtaining a relevant capture domain risks certifying a region the global search cannot reach. |
| Tail reuse and reproducibility | Two new full-17 exclusions removed two orbits. Conservative dependency extraction still uses all 17 owners. The older 200-object collection remains unavailable locally. | Neither a reusable smaller-arity certificate nor a reliable total-tail price has been established. Fresh-host custody is a separate completion obligation. |

The current counts and capture deficits are retained in the
[admission summary](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-274-current-tail-b-replication/admission-summary.json)
and
[numeric-parent summary](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-277-numeric-checkpoint-capture/summary.json).
The failed replay’s
[phase record](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-284-parent-guard-native-custody/phase-execution.json)
distinguishes complete production from unaccepted verification.

The size of the numerical side gap is misleading as an estimate of proof difficulty.
The unchanged lower-bound charge has only $2.5\times10^{-8}$ of further runway.
More refinement of that charge cannot reach the known endpoint.
Any lower-bound alternative needs a new geometric inequality or representation.

Compute is not uniformly scarce.
Exp-285 and exp-286 each completed their exact construction and fresh reconstruction in
about 20.74 seconds; exp-287 took 1.11 seconds.
Their negative outcomes are mathematical recipe failures, not timeouts.
The accepted numeric-cap first round took 175.86 seconds in production and 66.48 seconds
in resumed fresh replay.
Its separate full standing replay took 104.68 seconds and checked over 25 million
collision facets.
These are measured single cases, not a representative throughput model.
The finite costs are retained in the
[exp-285](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-285-pooled-parent-center-cases/phase-execution.json),
[exp-286](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-286-pooled-forbidden-cover/phase-execution.json)
and
[exp-287](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-287-pooled-relaxation-witness/phase-execution.json)
phase records.

Exp-287’s fixed one-square candidate passed every owned-point condition and failed only
container containment.
The separately registered exp-288 construction puts the exact walls and ownership strips
into the centre domain before selecting a point.
Its
[freshly checked result](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-288-pooled-feasible-center/replay.json)
is a valid one-square owned-point relaxation witness at $\tau=53/128$: containment,
strict ownership and all foreign-pool avoidance tests pass.
Construction and fresh reconstruction took about 0.39 seconds combined, with 1.12
seconds of supervised wall time.
This proves that the specific retained-point relaxation leaves a pose feasible.
It does not construct the other sixteen squares, exclude a guard, or imply that every
possible additional ownership certificate would fail.
The next route should add partner-pose information or coupled constraints.

## Ranked Mathematical Routes

One block below means roughly 30 minutes of focused work by the named lane, with a
retained artifact and a stop decision.
The ranges are planning allowances for the first discriminator, not forecasts of a
theorem or measured implementation costs.

| Priority | Route and first checkable result | Initial allowance | Continue or stop |
| --- | --- | --- | --- |
| 1 | Use complete partner pose covers to test a surviving owned-point witness, then certify a closed centre/angle region that those stronger constraints exclude. | 2–4 blocks for the mathematical contract, bounded instrument and first controlled result | Continue when exact coupling excludes a declared region that the matched point-only control leaves unresolved. If the fixed test gains nothing, change the guard or representation only under a new criterion; do not extend unchanged propagation automatically. |
| 2 | Profile and optimize full exact replay on retained accepted controls, then attempt the same exp-284 object under a separately registered verification budget. | 2–4 engineering blocks, parallel with route 1 | Continue only with a measured hotspot and exact equivalence. A proposed useful threshold is at least a twofold end-to-end improvement on a frozen control without increased proof obligations or unacceptable RSS. This is an acceptance target, not an expected speedup. |
| 3 | Amortize exclusions across a proved family of cell assignments instead of closing one full-17 mask at a time. | 2–4 blocks for one family-lifting contract; implementation cost remains unmeasured | Require one exact certificate whose checked cell-containment or parameter inequalities cover multiple named current assignments. A shared-looking proof trace or a deleted tuple is insufficient. Park the attempt if its relaxed family includes the known endpoint or cannot retain complete assignment coverage. |
| 4 | Derive a structural normal form that forces a small set of contact or orientation alternatives from the actual cell domains and cap. | 4–8 mathematical blocks for one substantive lemma or counterexample | Require a necessary statement about every packing in the declared domain, with degenerate and boundary cases. Numerical contact patterns, local stationarity and a guessed contact graph do not meet this criterion. |
| 5 | Build an exact dual envelope or combine local cone inequalities on a capture domain actually delivered by a stronger global argument. | 2–4 blocks after that domain exists | Require uniform bounds on every allowed branch over a complete closed region. Stop if progress is only another isolated direction or patch with no identified contribution to a finite cover. |

Routes 1 and 2 are ready for a bounded next block.
Routes 3 and 4 address the possibility that the current architecture needs a larger
change; they should receive a deliberate mathematical slice if the first coupling
discriminator fails.
Route 5 retains the useful local work without making an unpriced sixteen-dimensional
covering problem the default next job.

### What Stronger Coupling Must Prove

For an owner-0 angle interval $J$, let $C_J$ be a strict core of its square.
A partner’s complete closed row $k$ supplies a centre domain $P_k$ and a strict core
$D_k$. For every facet $n\cdot z\le h$ of $D_k-C_J$, impose

$$
n\cdot x\le h+\min_{y\in P_k}n\cdot y.
$$

Intersect these inequalities over **all** live rows of that partner.
Any centre in the resulting region must collide with the partner regardless of its
remaining pose.
Then take the union of the regions proved for different partners and test
coverage of the owner-0 domain.
The order of these quantifiers matters: a union over partner rows would discard
alternatives instead of covering them.

The independent standing checker already verifies this type of implication in
`admit_cover`, `check_partners` and `check_collisions`. A finite probe can reuse those
exact primitives.
It must preserve all closed rows, residual pieces, typed references and
strict-core checks. A row may be skipped only with accepted emptiness or a fresh proof
that every piece has empty necessary-wall intersection.

This is a plausible source of stronger information, not a prediction of success.
Even pairwise pose covers can lose correlations among several squares.
If they do, the next mathematical choice is a small complete closed partition coupling
two owners’ centres or angles, with every child verified and their union checked.
One successful child is never a parent exclusion.

### Alternatives That Could Change the Cost Structure

**Certificate families.** The two new tail closures are evidence that the producer can
close some remaining masks, not a rate estimate for 4,683 orbits.
A useful experiment would replace a small set of alternative named owner cells by a
checked common outer region, prove exclusion there, and transfer it back by exact cell
containment and label maps.
Another possibility is to verify uniform inequality margins across a finite family of
cell choices. Both require a new admission interface; the all-17 dependency inventory
neither supplies such a certificate nor proves that no smaller proof exists.

**Structural reduction.** A complete normal-form lemma could remove many angle and
centre variables before search.
A bounded first attempt should ask whether the tight cap and selected occupied cells
force one specified separating-feature or contact alternative.
Any use of local stress must state why the global domain satisfies its premises.
Compactness or optimality stationarity alone does not justify a particular contact
graph, especially with sliders and inactive contacts.

**Dual envelopes.** The exact all-branch patch and signed cones suggest combining
several certified inequalities over a delivered capture footprint.
Candidate duals may come from numerical LPs, but acceptance still needs exact signs,
residual bounds and complete feature/angle coverage.
Piecewise support functions and degenerate directions prevent treating a sampled
positive Hessian as a global convexity proof.
A useful milestone is one closed region joining existing terminal pieces, rather than a
larger collection of unjoined samples.

**A different cover.** If centre or angle correlations are repeatedly lost, a cover
aligned with the forced geometry may be more effective than finer uniform rows.
This is an existing guarded-coupling idea with a stricter current test: compare one
closed refinement against its matched parent and require exact exclusion or terminal
capture of all its children.
The 95 distance-two D4 orbits are a possible declared test population.
Numerical failure to find placements does not exclude any of them.

## A Deeper Optimization Block

The Mac has ten logical CPUs and 32 GiB RAM. That does not make a sequential producer or
a fresh proof replay ten times faster.
The selected production runs are CPU intensive: exp-276 records 174.55 seconds of
process CPU time against 175.86 seconds elapsed; exp-284 records 288.36 against 292.02.
Those observations establish neither parallel scaling nor an I/O bottleneck.
Independent states can run concurrently, but their useful throughput must include full
verification, memory, evidence storage and ordinary admission.
Reserve a quiet worker for matched timing before attributing wall-time changes to an
optimization.

A two-to-four-hour engineering block is justified for verification, with these
deliverables:

1. Add retained phase timers and counters for decoding, accepted-parent intake, facet
   construction, support minima, exact intersections and coverage sweeps.
   Measure a frozen accepted full control.
   The current record does not separate intake cost from finite geometry, so that split
   must not be guessed.
2. Select the measured dominant repeated operation.
   Existing caches already store core-pair facets, domain/direction minima and
   owned-hull forbidden regions.
   Measure hit rates and eviction before proposing another cache.
   The conditional checker also repeats accepted-parent extraction during preparation;
   eliminate it only through immutable validated inputs that retain complete EOF and
   byte identity checks.
3. Compare the candidate and reference on identical proof objects, including degenerate
   and boundary controls.
   Preserve full row, facet and final-state verification.
   Require a material end-to-end gain under a frozen wall and RSS criterion, then run
   one full scientific replay with its own registration.

The exp-284 replay timeout is the reason to fund this block.
The cheap finite misses are not.
Native-code acceleration of an exact arithmetic hotspot is a possible later
implementation choice; GPU search, blanket parallelism and a new cache are not supported
speedup claims without that profile.
Likewise, weakening coverage, using sampled verifier rows or increasing a timeout is not
an algorithmic improvement.

The supervisor samples current RSS per live process, with owned-group cleanup.
Its 4 GiB guard is neither an aggregate-group limit nor an allocation-time hard cap.
Fast child processes can finish between samples.
Resource conclusions must retain those limits.

## Next Two Hours and Conditional Two-Day Program

For the next one-to-two-hour block, keep one Astra on mathematical selection and two Sol
workers on implementation and independent review.
Use exp-288’s exact reduced-model witness as a fixed control for the complete
partner-pose implication above.
The witness touches the centered container’s left wall, so retain boundary cases.
Eliminating this one point is a discriminator; useful coverage requires a nonzero closed
excluded region or a complete guard argument.
Freeze that mathematical criterion before implementing its target instrument.

In parallel, one Sol can prepare the replay profile and controls while the other
implements the selected finite geometry.
The mathematical milestone is a newly proved closed exclusion/capture region, or an
exact discriminator that rejects the proposed representation.
The engineering milestone is a retained hotspot measurement and a candidate with
unchanged verification semantics.
End the block with an explicit continue, revise or park decision for each lane.

A further one-to-two-day program is justified only after that checkpoint supplies new
geometric information or a repeatable verification improvement.
Allocate the first half-day to one coupled-cover prototype and the verifier
optimization; use the next half-day for a preregistered small residue stratum and one
certificate-family or normal-form discriminator.
Fund a second day only if complete checked coverage grows, a uniform implication
replaces multiple cases, or end-to-end certificate cost materially falls.
Repeated partial contractions, more isolated local patches, or faster unverified output
fail that renewal test.

There is no defensible proof-completion date yet.
It depends on whether a global capture or structural lemma succeeds and on the cost
distribution of the actual remaining residue.
Extrapolating two chosen tail closures, multiplying by core count, or pricing 4,683
orbits as independent identical jobs would conceal those unknowns.
The proposed program buys evidence about that cost and the right proof representation;
it does not promise optimality within two days.

All new geometric implications here are the session’s sole Astra agent’s hand arguments.
Existing exact receipts retain their scopes.
Independent mathematical review, complete proof composition and the missing global
coverage remain open.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
