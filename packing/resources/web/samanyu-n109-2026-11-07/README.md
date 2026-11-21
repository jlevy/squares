# Samanyu-dev’s 109-Square Packing

The public Kaggle submission gives the centres and radian angles of Samanyu-dev’s
109-square pinwheel. The
[pinned CSV](https://github.com/Samanyu-dev/squares_in_squares/blob/53551d77513a9f5c180a731f291baf7eda7c3009/best_fit_101_500.csv)
is the input. The [acquisition record](acquisition/sources.json) pins it by digest and
records the source scope. The repository’s licence note distinguishes its own code
from third-party work. This packet retains the exact numerical derivation.

The importer reads the centres as binary64 values and computes a rational half-angle
tangent for each rotation by outward interval arithmetic. It translates the witness
to its exact lower-left extent and takes the larger span as its side. The asserted
upper bound is the exact certificate’s upward print at 12 places.

De Winter’s later exact certificate from [issue #1012](https://github.com/jlevy/squares/issues/1012)
gives a smaller print within the earlier packing’s contraction margin. The
[independent review](../../../../docs/project/reviews/review-2026-11-20-de-winter-1012-n109.md)
verified both its certificate and a separate rational reading of the pinned Kaggle
rows. Its earlier witness digest applies to that reading. The maintained replay
for this packet binds the portable derivation in this directory.

Both maintained routes accepted the derived certificate and refused the planned
duplicate-square and outside-container controls. The
[maintained receipt](receipts/exact-certification.json.xz) holds 35,316 pair decisions
across the three jobs and two routes.
All 11 [sharp controls](receipts/sharp-controls.json) returned their planned outcomes.

A separate guarded run of the review’s independently implemented `r1012_check.py`
accepted all 109 squares and 5,886 pairs in the exact corners copy of the portable
fact. The [binding](receipts/canonical-independent-binding.json) records the fact,
corners copy and [checker receipt](receipts/canonical-independent-check.json)
digests.

## Compressed Files

| Stored file | Origin | Git blob of decompressed source | SHA-256 of decompressed source |
| --- | --- | --- | --- |
| `facts/n-109.yaml.gz` | receipt | `6e7a027f451a0bf2107bbbee44f9968daa44511a` | `2938dddb54398f8f91afd4dce7e83a8bbd2a56db189b1e5a92c0877d85bca5d3` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
