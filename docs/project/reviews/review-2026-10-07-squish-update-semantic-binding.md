# SQUISH update: mathematical and semantic binding review

Verdict: accepted for the exact rational feasible upper bounds of the twelve newly
selected update geometries: 123, 126, 129, 154, 155, 179, 208, 237, 238, 239, 258, 263.
This review was performed by the separately tasked `followup_generator_review` AI review
lane on 7 October 2026. It does not change assurance records or establish independently
audited human oversight.

The source is `itsnaka/squish-certs` revision
`5e32bbd7028b6e3b869979278079cd37ed6770aa`, directory `squish-submission-2026-10-07`.
The reviewed retained facts are the revision-specific files under
`packing/resources/web/squish-401-update-2026-10-07/facts/`. The full replay was
inspected and reused, not rerun in this review.

## Mathematical argument and checked bindings

For rational half-angle parameter t, define c=(1−t²)/(1+t²) and s=2t/(1+t²). The
denominator is strictly positive, c²+s²=1, and the vectors (c,s), (−s,c) form an
orthonormal frame. For each retained center (x,y), the four corners are (x+(a c−b s)/2,
y+(a s+b c)/2), in the cyclic sign order (−1,−1), (1,−1), (1,1), (−1,1). Consecutive
edges have unit length and zero dot product.
This gives exact unit squares without transcendental evaluation, rounding, dilation, or
side inflation.

I independently evaluated that formula using rational arithmetic for every square and
compared each coordinate with the packet conversion.
I also parsed the pinned upstream files retained by the preceding replay and compared
their normalized facts with the current repository facts.
For every count the complete resulting checker input equals the full input in its replay
receipt: n, rational side, unit-square side, coordinate convention, representation,
scalar kind, and every ordered corner and id.

Both receipt routes accept every positive case and report exactly n(n−1)/2 pairs.
The twelve new geometries contain 2,309 squares and 237,025 unordered pairs per checker.
The inspected scratch batch additionally contains the duplicate n153: 2,462 squares and
248,653 pairs per checker across thirteen cases.
The 11,628 pairs for n153 are outside the twelve-case confirmation scope.

I inspected the independent checker’s shape, closure, containment, and separating-axis
predicates, and the native exact route’s use of exhaustive verification with bucketing
disabled by default.
The independent route enumerates all unordered pairs.
For unit squares in cyclic order, their edge-normal separating axes suffice: at least
one nonnegative projection gap excludes interior overlap.
A zero gap permits boundary contact.
Testing all four corner inequalities against the container suffices by convexity.
The routes share rational corner input and Python rational arithmetic; their agreement
is not independence from those common premises.
The separate conversion and semantic-input comparisons address this shared input
boundary.

The two retained negative controls each preserve the full 123-square roster.
I reconstructed their semantic mutations from the retained positive input: copying
square 1’s corners onto square 2, and translating square 1 left by twice the side.
Both reconstructed inputs equal the receipt inputs exactly; both routes reject both
controls while reporting all 7,503 pairs.
The earlier full replay took 108.598 seconds for positives and 7.684 seconds for
controls; these are reused measurements.

The display used for a bound is the least upward sixteen-place decimal ceiling of its
exact rational side.
Source prints remain quotations: several are below the exact side, and some exceed that
least ceiling. Every receipt’s upward display matches the current update module’s
integer-arithmetic ceiling.
The n153 facts and ordered geometry equal the previously retained original geometry; its
new source location confers no new mathematical result or assurance.

No optimality, rigidity, search completeness, discovery priority, or human oversight
follows. The author is Nate Chaoweeraprasit, using SQUISH; stated Francisco Couzo and
SQUISH seed lineages remain author-reported provenance.
No upstream solver or producer checker was executed by this review.

## Publication adapter review

The initial draft dispatcher dropped all twelve selected reports and replaced five
earlier certified SQUISH bounds with weaker historical bounds.
The repaired dispatcher selects the update provider before the original roster guard.
Its update adapter rebuilds the current report from retained update facts, reconstructs
the earlier five verified bounds from original facts, and uses the historical verified
lane for the other seven.
It preserves reviewed source history, attribution, resources, evidence, and blockers;
ordinary lower lanes are regenerated and rigidity remains owned by its separate
promotion step. Current update and earlier certified body declarations have distinct
rewrites. Ceiling disclosure follows the actual positive display gap.
The final n258 correction also retains its earlier catalogue ceiling audit under an
explicit historical heading, including the irrational-side limitation and both earlier
gaps. It does not replace that audited discussion with the current disclosure.

I accept the repaired adapter for the reported-only publication layer.
Fifteen focused regressions passed in the actual working checkout: twelve cases with
corrupted current reported, earlier verified, lower, and body declarations reconstruct
their complete committed records, including all five original S_n declarations; three
missing current or historical declarations are rejected.
The existing seven focused cases also passed with the initial adapter before generated
ceiling disclosures were added.
Confirmation will require a separately reviewed explicit branch for the new verified
lane; the current adapter intentionally restores the prior verified ceiling.

## Evidence to retain when mapping this review

The twelve complete replay inputs and both verdicts are retained in
`packing/resources/web/squish-401-update-2026-10-07/receipts/certification.json.xz`; the
two full-size mutated inputs and verdicts are in `receipts/negative-controls.json.xz`
beside it. Their accepted semantic comparison is preserved in
`receipts/reviewed-semantic-binding.json.xz`. The original run’s summary and the
twelve-case timing attribution are in `receipts/replay-summary.json`. Revision-specific
exact witnesses are under `packing/witnesses/squish-401-update-2026/`; bounded source
acquisition metadata and facts remain under this update packet.
The mathematical review is
`docs/project/reviews/review-2026-10-07-squish-update-mathematics.md`. The
reported-layer regressions remain in `packing/tests/test_generate_frontier_case.py`.

The immutable original eleven-case reviews, receipts, and evidence remain attached to
their original geometries.
This document accepts the mathematical/source binding review; it does not pre-approve a
future certification producer or evidence mapping.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
