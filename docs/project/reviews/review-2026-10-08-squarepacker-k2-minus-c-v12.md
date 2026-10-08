# Delta Proof Review: Ryu’s k² − M(k) Bound, Version 1.2

**Reviewer:** GPT-6 Astra, independently assigned strong review.
**Date:** 8 October 2026 UTC; the host’s local work date is 7 October.
**Source:** `squarepacker/k2-minus-c`, tag `v1.2`, immutable commit
`e16a5cfa7eed489ea8d84b500e590bf6855a5f2f`. The primary `paper/paper.tex` has 127,617
bytes and SHA-256 `25db094cd7af9d707eb6eddda987e3fbb99d22813ff1672646fb0a724d1e3bb3`.
**Status:** mathematical delta, maintained constants and complete source custody
accepted in the scopes below; computational reuse retains the original independence
limits. The bounded floating-point follow-up is accepted under its explicit runtime
premises; final publication expression remains separate.
No source verifier was executed in this review, and the old full box computation was not
repeated.

## Scope and Reused Premises

Let M(k) be the maximum number of unit squares in [0, k]² that are pairwise disjoint as
closed sets, with integer k ≥ 2. This strict disjointness condition is essential: the
ordinary touching k by k grid has zero waste and is outside this model.
Version 1.2 states the coefficient 0.0353, the explicit lower bound 1.99954(log k −
13.06675)/30.418 for every k ≥ 2, and asymptotic coefficient 0.0657. The analytic
overlap bound gives the separate coefficient 0.0319. The coefficient 0.0541 additionally
assumes Daniel’s s(k² − 3) = k for every integer k ≥ 6; this review does not re-prove
that external premise or convert it into an unconditional conclusion.

The [version 1.1 review](review-2026-10-05-squarepacker-k2-minus-c.md) supplies the
previously reviewed geometric framework.
Comparison of labelled statement/proof blocks, normalizing whitespace only, found 16
unchanged blocks: the strict-packing reduction, basic geometry and closedness, the
one-unit-waste corollary, the original short-chord lemma, convex gaps, boundary
functions, both fundamental propositions, vertex sections, planarity, counting, analytic
overlap, slits, horizontal inclination cost, and cracks.
Their assumptions and original review limitations remain in force.

The new proof blocks are the short-chord/excess lemma E, the excess estimate Eline, and
the Daniel-dependent corollary.
The changed blocks are the main statements, the computer-assisted overlap explanation
Kw9, the column inclination bound Bv, quantization Q, room in a column GZ, and the
theorem’s integration argument in Section 6.

## New Geometric Steps

**Short chords against excess (Lemma E).** At a fixed height, closedness and integer k
allow at most k − 1 chords of length at least one.
Their total length is at most k − 1 + E(y). Subtracting from the covered length k − ω(y)
leaves at least 1 − ω(y) − E(y) in short chords.
A negative right side causes no difficulty: the short-chord sum is nonnegative, which
supplies the positive part used in Section 6.

**Column inclination (Lemma Bv).** The only new assumption is the enlarged upper cap 3 ×
10⁻⁶ instead of 1.5 × 10⁻⁶. The existing proof bounds each capped pair inclination using
Q* = 0.32, the inequality involving θ₁ = 10⁻⁵, and the same denominator 2 − 3 × 10⁻⁶ in
A. Thus the cap change introduces an endpoint arithmetic obligation, not an additional
geometric case. The independent constants route must check that margin at the enlarged
cap. Bottom and top segments remain separated by a strip of height two, so a unit square
cannot meet both and no pair is charged twice.

**Long-chord excess (Lemma Eline).** For inclination a < α and chord length c ≥ 1,
sec(a) − 1 ≤ 0.50001a² gives c − 1 ≤ 0.50001αac. The long chords are disjoint, so their
sum is an integral over their horizontal projections.
Columns with vertical waste at least δ have total measure at most W/δ and inclination
contribution at most αW/δ. On the remaining columns the segment from the nearer wall to
the chord meets its square and has waste below δ; Lemma Bv bounds the inclination
integral by AW. This proves E(y) ≤ 0.50001α(A + α/δ)W. Reflection handles the upper
half. The required segment length d(y) ≤ k/2 − 1 and inclination cap are explicitly
preserved in the later application.

**Quantization and room (Lemmas Q and GZ).** The geometric arguments are unchanged; the
endpoint scale is now 236,000. With α(s) = 1/(2s), the drift bound 0.50001(1 + α/s)/(4s)
decreases as s increases.
The ramp endpoints therefore reduce to checking the stated 5.3 × 10⁻⁷ drift, 2.119 ×
10⁻⁶ inclination, and 1.2649 × 10⁻⁵ ramp bound below w₀ = 1.265 × 10⁻⁵. For GZ, α and
cos α + sin α decrease with s in the relevant small-angle interval, while cos α − sin α
increases. Each positive factor in the displayed upper bound for
|B_Z| consequently decreases. Its worst endpoint is s = 236,000. The new bounds
|B_Z| < 0.500023 and middle-band length > 1 − 2.12 × 10⁻⁶ leave more than
0.49997488, hence more than g₀ = 0.49997. The arithmetic route must certify the endpoint
inequalities; a finite sample of scales would not establish monotonicity.

## Section 6: Constant Cutoff and Integration

The integer cutoff makes the period sum explicit.
For j₀ = 236,000 and j₁ = floor((1 − ε)(k/2 − 3)), each interval [m + w₀, m + 1 − w₀]
lies in the lower height set.
Its integral with weight 1/y is at least h₀/(m + 1), which is at least h₀ times the
integral over [m + 1, m + 2]. Summing and reflecting gives the stated lower bound
2h₀(log k − 13.06675), conditional on the fresh endpoint logarithm checks.
The reflection preserves the fractional-height exclusion because k is an integer.

The height partition into high waste, high inclination, and small inclination is
exhaustive and disjoint.
On the third part, Eline applies because d(y) is below k/2 − 1 and its line threshold is
below 1.5 × 10⁻⁶. Extending the positive excess integral on each half to infinity gives

Γ ≤ 1.00002[A/(C′y_min) + 1/(2C′²δy_min²)].

This is the direct integral of the 1/y² and 1/y³ terms, not a quadrature estimate.
The factor two accounts for both halves of the container exactly once.

At a scale s, integration of the short chords gives the lower bound on the number of
squares with ramps meeting the height window.
Quantization forces each associated good column to be non-rigid: otherwise its ramp
would lie within w₀ of an integer, contrary to the height set.
A vertical line meets at most εs + 2.01 of these good-column sets, since their disjoint
chords have length at least one and occupy an interval shorter than εs + 2.01. This
gives the stated bound on the measure of non-rigid columns.

The first non-rigid scale exists on the relevant closed interval: vertical waste is
continuous in segment length, and each of the finitely many square-inclination events is
closed. The resulting functions are measurable; the defining finite polygonal conditions
also make the joint sets measurable.
All integrands used in the two Tonelli steps are nonnegative.
For a lower-half height y, its scale interval [y, y/(1 − ε)] is fully inside
[y_min, k/2 − 3], by the definition of H. Direct integration of 1/(εs²) on this interval
gives 1/y; the remaining denominator factor is bounded at y_min. The upper half follows
by the same reflection.

Finally, 1 − ω₀ ≤ (1 − ω₀ − E)₊ + E and E ≤ γW put Γ in the bracket as an additive cost.
Together with the other two height classes, this gives exactly the three displayed
bracket terms plus Γ. Its sign and the direction of each inequality are appropriate for
deriving a lower bound on W. For k ≥ 10¹², log k − 13.06675 is positive, so lowering the
numerator and raising the bracket are conservative.
The smaller k use W ≥ 1 separately.
The all-k coefficient can equivalently be checked at the crossing of 1 and the
affine-in-log bound: max(1, F(k))/log k decreases up to that crossing and increases
afterward.

The conditional coefficient uses the analogous crossing of 4 and F(k) for k ≥ 6, with k
= 2 through 5 checked from W ≥ 1. The reduction from Daniel’s assumption to W ≥ 4 uses
the unchanged strict-packing equivalence and integrality of k² − M(k). No new universal
packing assertion follows if that external assumption is removed.

## Computational Reuse and Remaining Limits

The reviewer compared the old replay’s `receipts/verify-leaves2/inputs.sha256` against
the new immutable checkout.
All 13 uncompressed deciding leaf lists extracted in memory from `data/kw9_data.zip`
match. So do `bnb.py`, `bnb_wall.py`, `verify_leaves.py`, `verify_leaves2.py`, their
`run_v2.py`/`run_seq.py` drivers, `coverage_check.py`, and both independent coverage
deciders. This comparison read source and data only.

The prior complete 78,673-box replay and its 52 output records may therefore be cited as
existing evidence for that unchanged computational subclaim, with its original runtime,
controls and limitations.
This is not a new execution.
Reuse needs an explicit packet record linking those complete retained inputs and results
to this version’s same overlap premise.
The old receipt manifest does not transfer wholesale: `kw13_check.py` and the coverage
summary changed, and the old constants programs were replaced.
New arithmetic is a separate obligation.

Kw9 now explains the last angular arc and the floating-point greedy count.
The angular arc argument matches the version 1.1 review: at most the last angle in the
side case can lie beyond the floating endpoint; the corresponding accepted interval
extends to exact 2π and covers it.
The repaired k ≥ 4 assumption also matches its use here.
The new floating-point paragraph claims a finite comparison gap and accumulated error
bound. The initial delta reading left that claim open; the bounded follow-up below
records its subsequent arithmetic check and remaining historical-runtime premise.
Matching unchanged checker bytes alone does not close the old RF-2 limitation.
The old RF-1 limit also remains: per-box labelling has one implementation, although
coverage has independent routes.
No C3/C4 computational-independence or human-review upgrade is implied by this delta
review.

## Maintained Constants and Source Admission

**Accepted:** the separately maintained v1.2 arithmetic route in
[`ryu_k2_minus_c_constants.py`](../../../packing/cases/asymptotic/ryu_k2_minus_c_constants.py)
implements the new proof’s numerical obligations, conditional on the geometric premises
reviewed above.
It evaluates rational expressions exactly and transcendental inequalities
with 60-digit intervals.
All 34 rows for overlap nine and all 30 rows for overlap thirteen hold.
The nine-overlap route alone includes the stated Daniel-dependent coefficient and
fixed-c threshold; the analytic route does not inherit those rows.
The old v1.1 route remains the default, including its existing JSON payload.

The bracket bounds are 30.4179798014… and 36.4925322146…, and the integrated-excess
bounds are 1.60025141068… × 10⁻⁵ and 1.92098767864… × 10⁻⁵. The exact all-k lower
envelope minima are 0.0353616181402… and 0.0319310823424…; these support the respective
rounded statements. Meaningful controls refuse tightened gamma, bracket, numerator,
shift, room and coefficient claims, an inadequate cutoff or Q*, a tenth rectangle under
the nine-overlap constant, and transfer of the computer-assisted coefficient to the
analytic route.

**V12-C1, Medium, closed:** the first parameterized implementation accepted a negative
room denominator, `room_bound="-1"`, with all 34 rows holding.
Dividing by that value would reverse the proof inequality, so the override was outside
the valid proof domain.
The default paper constants were unaffected.
The repaired entry point requires positive physical/arithmetic bounds and an integer
cutoff before evaluation.
Six controls reject zero or negative room, negative bracket or shift, zero numerator and
a fractional cutoff.
The reviewer independently reran both versioned test modules after the correction: **26
tests passed in 0.16 seconds**, recorded in `k2-v12-constants-domain-fix-review.log` in
the external review directory.
The pre-fix reproduction remains in `k2-v12-domain-review.log`.

The reviewer also ran the complete source-packet acquisition check with the project
interpreter. It exited zero with `PACKET_MATCHES_ITS_CONTRACT`, recorded in
`k2-v12-source-admission-review.log`. All 78 immutable source files are accounted for:
ten changed files, totaling 822,918 bytes, are retained in the new packet, and 68
byte-identical files, totaling 950,262 bytes, have explicit links to the retained v1.1
copies.
This includes the original licence texts: MIT for code/data and CC BY 4.0 for the
paper. The check admits source custody and attribution; it is not a theorem verifier.

## Bounded Floating-Point Follow-up

The coordinator subsequently assigned this reviewer implementation of the new
[`ryu_k2_minus_c_float_gap.py`](../../../packing/cases/asymptotic/ryu_k2_minus_c_float_gap.py)
and its [tests](../../../packing/tests/test_ryu_k2_minus_c_float_gap.py).
This section records implementation evidence and the coordinator’s separate source
review. The coordinator inspected the frozen module and pinned operation model, then
independently ran all thirteen tests with exit zero in 0.616 seconds of command wall
time, recorded in `float-gap-independent-tests.log`. That review accepted the
finite-domain reduction, ninth-step bootstrap and conservative endpoint/rounding
envelope under the explicit current-constant and binary64 premises.
No upstream module is imported or executed by the new route.

Put h = π/720 and γ = arccos(1 − 1/[2(√2 + 10⁻⁴)²]). The maintained route encloses γ as
2 atan2(1, √(4(√2 + 10⁻⁴)² − 1)) in a private 60-digit interval context.
It checks all 25,929 pairs (j, m), with 1 ≤ j ≤ 9 and 0 ≤ m ≤ 2880. The smallest
interval for |jγ − mh| lies at (8, 1325), with value 0.000043249683487061138… > 4 ×
10⁻⁵. Negative m are farther from the positive jγ; m beyond 2880 are farther than 4π −
9γ, which is separately bounded above the required gap.
Thus the finite roster covers every integer multiple that could reduce the minimum.

For any allowed-cell mask, a greedy point is a cell start plus j separations.
The target/end, target/start and circular-closing decisions involve j = 1 through 9. The
separately checked 8γ < 2π < 9γ supplies the full-circle count and refuses a ninth
point; this closes the induction that bounds the number of accumulated additions.
An empty mask has no points.
The source’s off loop only uses 0 through 1439, so its one-revolution cutoff stays at
least one full cell away; it is covered separately, rather than by an inapplicable
nonzero-j comparison.

For binary64 round-to-nearest, a basic operation whose result has magnitude below 16 has
absolute rounding error at most u = 2⁻⁵⁰. Let e be the exact binary DPHI error against
h. The unwrapped endpoint expression has at most 2879 cell widths and four roundings;
2880e + 4u bounds it conservatively.
The certified closed-cell end, formed by the maximum of the adjacent binary endpoints
and extended at the final end to exact 2π, satisfies the same larger bound.
Two such endpoint bounds, the binary 2π error and sixteen further rounding units cover
the position additions and target/closing operations.
All intermediate magnitudes are separately bounded below 14.

The actual endpoint/basic-operation envelope is below 2.199 × 10⁻¹⁴. The checker uses
its conservative cap 10⁻¹², then adds up to nine separation deficits, their exact
binary-lift discrepancies, the cell comparison slack and closing slack.
The resulting error is below 1.101 × 10⁻¹¹, well below the certified 4 × 10⁻⁵ gap.
This supplies a conservative sufficient bound; it does not certify the paper’s tighter
wording that every accumulated rounding error is below 10⁻¹⁴.

The recorded current-host binary constants are:

| Constant | Exact binary64 hexadecimal value |
| --- | --- |
| π | `0x1.921fb54442d18p+1` |
| DPHI | `0x1.1df46a2529d39p-8` |
| G0_SAFE | `0x1.720337bf92a51p-1` |
| Cell slack | `0x1.203af9ee75616p-50` |
| Closing slack | `0x1.19799812dea11p-40` |

All thirteen tests passed.
They refuse an excessive claimed gap, excessive or insufficient error budgets, increased
separation deficit, increased closing slack, an incorrect binary separation, and invalid
arithmetic domains. They also check independence from ambient mpmath precision.
The complete-grid test call took 0.26 seconds; the test run’s 240.44-second aggregate
included separately observed external-volume kernel I/O wait before execution.
The documented standalone command then exited zero in 0.243 seconds.
Ruff reported no findings, and BasedPyright with the project interpreter reported zero
errors, warnings or notes.
The complete receipts are `k2-v12-float-gap-tests.log` and
`k2-v12-float-gap-receipt.json` in the external review directory.

**RF-2 disposition:** the finite gap and conservative comparison error argument are now
implemented and tested for the reviewed operation model and explicit current-host
constants. The old verifier defines `G0_SAFE = B.G0 - 1e-12`, with `B.G0` obtained from
`math.acos`; it does not contain a recoverable literal for the historical value.
The old replay receipt did not print that libm output.
This new check therefore does not retroactively certify an unobserved historical
transcendental result or execute the old box labels again.
Any use of the old replay must retain that runtime premise and the original RF-1
single-implementation limit.
This work supplies neither independent per-box labelling nor C3/C4 computational
assurance.

## Final Disposition

**Accepted within the stated premises:** no gap was found in the new geometric
reductions or Section 6 integration.
The analytic 0.0319 route avoids the box-labelling premise; the stronger nine-overlap
statements retain it.
The 0.0541 conclusion remains conditional on the stated Daniel assumption.
The maintained constants and full 78-file source admission are now accepted.
Final integration still requires an explicit record of the unchanged computational
subclaim reuse and reader-facing claims that preserve the strict-packing and conditional
scopes. The original per-box implementation limit remains C1; no new independent
labelling implementation or human oversight is supplied here.
The older v1.1 evidence and assurance must remain independently addressable and
unchanged.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
