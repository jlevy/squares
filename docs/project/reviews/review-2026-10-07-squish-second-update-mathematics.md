# Issue 422 Exact Feasibility Review

The completed local replay establishes feasible upper bounds for **88, 108, 179, 180,
199, 207, 236, 263, and 302 unit squares** at the exact rational sides in Nate
Chaoweeraprasit’s SQUISH submission.
Both local exact checkers accepted all nine packings and rejected all eighteen
deliberately invalid controls.
This review accepts the scientific batch as exact feasibility evidence.
Repository integration, registration, and any future pull request require their own
review.

The source is the nine certificates under `squish-submission-2026-10-07b` at
[`itsnaka/squish-certs` revision e63e4e52b1728b6671b2f263c5e02a4aa79a39d3](https://github.com/itsnaka/squish-certs/tree/e63e4e52b1728b6671b2f263c5e02a4aa79a39d3/squish-submission-2026-10-07b),
as identified in [issue 422](https://github.com/jlevy/squares/issues/422). The
[structured review](../../../packing/resources/web/squish-422-second-update-2026-10-07/reviews/math-review.json.xz)
contains the exact side for each count, source identity, attribution, and every route
outcome. The
[complete reviewed inputs](../../../packing/resources/web/squish-422-second-update-2026-10-07/receipts/certification.json.xz)
retain all ordered corners and other values that determine each decision.

## Source Geometry and Complete Input Identity

The first stage of this review independently reconstructed all **1,762 rational source
triples and 7,048 positive corners** before the replay.
For a source centre $(x,y)$ and half-angle parameter $t$, set

$$
c=\frac{1-t^2}{1+t^2},\qquad s=\frac{2t}{1+t^2}.
$$

The denominator is positive and $c^2+s^2=1$ exactly.
The rotation matrix $R=\left(\begin{smallmatrix}c&-s\\s&c\end{smallmatrix}\right)$ is
therefore orthogonal with determinant one.
Applying it to the four ordered corners of $[-1/2,1/2]^2$ and translating by $(x,y)$
produces a counterclockwise unit square.
The independent matrix calculation matched every prepared corner exactly.
Checks of each centre, unit edge, adjacent dot product, and adjacent determinant also
passed. The conversion uses rational arithmetic throughout.

After replay, the review compared every receipt’s complete semantic input to the values
retained before replay and to the prepared witness.
All 27 inputs matched, including the exact container side, number of squares, ordered
square IDs and corners, unit size, scalar kind, representation, and coordinate frame.
Matching a count, side, or digest alone was insufficient.
The review also rechecked the full source-to-facts normalization and acquisition
custody: byte counts, SHA-256 values, and Git blob identities agreed with the pinned
upstream tree and the original acquisition.
Those hashes identify source bytes at the acquisition boundary; verdict applicability
follows from complete semantic equality.

The preparation manifest remains a record of preparation with
`feasibility_checked: false`. The completed replay summary and deciding receipts
establish feasibility.
The review checked their full nine-case and 27-job rosters, the outer exit status zero,
and all 27 child exit statuses zero.

## Exact Decisions and Invalid Controls

The two routes were `devtools.check_rational_witness_independent` and
`sqpack.witness.exact_verify`. Each checks exact unit-square shape, containment in
$[0,S]^2$, and interior disjointness for every unordered pair.
Both accepted all nine positives with empty failure lists.
The reviewer separately recomputed each square’s shape and every containment clearance
from the receipt input; the minimum clearance was exactly zero for each positive and
agreed with both routes.

For convex squares, the separating axis theorem reduces pairwise interior disjointness
to projection intervals on the four edge-normal axes supplied by the two squares.
A nonnegative separating gap permits disjoint interiors; zero permits boundary contact.
A strictly negative best gap means interior overlap.
The inspected implementations enumerate all unordered pairs, and each actual route
receipt reports exactly $n(n-1)/2$ pairs.
This receipt review did not rerun pairwise deciders or treat a parser success as a
geometry decision.

| Count | Safe Upward Display | Pairs per Positive per Route |
| --- | --- | --- |
| 88 | 9.8824510304821347 | 3,828 |
| 108 | 10.9099400734448775 | 5,778 |
| 179 | 13.8837954905121866 | 15,931 |
| 180 | 13.9176534174514757 | 16,110 |
| 199 | 14.6175721735980400 | 19,701 |
| 207 | 14.8879922583077482 | 21,321 |
| 236 | 15.8678008394255397 | 27,730 |
| 263 | 16.7404196795387766 | 34,453 |
| 302 | 17.8813062180958085 | 45,451 |

Each count also had two controls, each retaining its full square roster:

- **Overlap:** square 2’s corners were replaced by square 1’s corners, retaining
  distinct IDs. Their unit-square interiors coincide.
  Both routes reported overlap; the first-party route explicitly identified squares 0
  and 1, using its zero-based indexing.
- **Containment:** all four x coordinates of square 1 were translated by $-(\max x+1)$.
  Its largest x became exactly $-1$, so every corner lies beyond the left container
  boundary. Both routes reported containment failure and the same exact negative minimum
  clearance independently recomputed by the reviewer.

These transformations preserve unit-square shape.
The controls reached the geometry decisions and both routes tested all pairs despite the
failures. The totals are **190,303 positive pairs per route**, **570,909 pairs per route
including controls**, and **1,141,818 pair decisions across both routes**. All 54 route
outcomes met their expected verdicts and failure conditions.

## Exact Sides, Attribution, and Claim Limits

The replay used each certificate’s exact rational `s_exact`. The displayed values above
are $\lceil 10^{16}S\rceil/10^{16}$, calculated with integer arithmetic.
Each satisfies $S\leq U<S+10^{-16}$; feasibility at $S$ implies feasibility at $U$.

The source’s printed decimals are below the exact side for **179, 207, 236, 263, and
302**. They remain quotations, separate from the certified display.
For example, n263’s exact side is $9424018478849569/562949953421312$; its source print
`16.7404196795387747` is below that value, while the safe upward display is
`16.7404196795387766`.

Source lineage remains attributed to the author: Kingbird’s s(41) and s(37) for n88 and
n199; Francisco Couzo’s s(180) and s(297) for n179 and n263; SQUISH’s own s(110) and
s(182) for n108 and n180; and SQUISH’s n88 packing for n207, n236, and n302. Exact
feasibility checking does not independently establish this construction history.
The source’s `squeezed` flag is metadata, and unsuccessful perturbation searches do not
prove local minimality.

The conclusion is $s(n)\leq S_n$ for each exact side in the reviewed inputs.
It establishes neither global optimality nor local minimality, rigidity, or the
algebraic degree of an optimum.
Earlier larger feasible bounds remain valid at their own values; they are not evidence
for these smaller sides.
These nine inputs retain their separate revision and `W-squish-422-nNNN` identities.

## Shared Premises and Execution Evidence

The routes independently implement the geometry predicates but share the separating axis
theorem, Python `Fraction` arithmetic, YAML and witness serialization, and the same
exact source-to-corner inputs.
Agreement reduces implementation risk without making these premises independent.
The separate rotation-matrix reconstruction addresses conversion for every source
triple. The result is computational exact verification under those implementation and
runtime premises.

Every receipt records Python 3.14.7, the loaded adapter and checker modules, and an
explicitly selected witness schema.
The selected schema and retained copy have identical contents.
The route files inspected for the first review agree with the files at the actual
recorded execution locations.
Original receipts retain their historical runtime paths; those ephemeral locations are
provenance, not portable replay instructions or identities for future code.
This publishable review uses repository module names and complete input values instead
of machine-specific source paths.

The sum of the 27 per-job dual-route elapsed times is **222.24647779400402 seconds**.
Individual values range from **1.532619084995531** to **16.26529426900379 seconds**.
Each timer encloses both sequential deciding calls and their witness
serialization/loading, while excluding initial module imports and source admission.
The sum is neither CPU time nor elapsed time for the parallel batch.
Batch wall time was not independently recorded.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->

<!-- This document follows common-doc-guidelines.md. -->
