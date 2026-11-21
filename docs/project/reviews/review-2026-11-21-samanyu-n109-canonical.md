# Samanyu-dev’s s(109) Packing: Confirming Review of the Exact Import

**Date:** 2026-11-21 UTC. **Reviewer:** Codex, delegated `tbd-strong` confirming review.
This review read the source-preparation work and the earlier review before checking the
evidence. It is an AI review with disclosed prior context.

**Verdict: accepted.** The retained rational construction establishes
$s(109) \le 10.949289580946$. No blocking mathematical finding remains.
The claim concerns the separately derived exact packing and makes no claim of optimality
or exact recovery of the source’s trigonometric poses.

The reviewed [packet](../../../packing/resources/web/samanyu-n109-2026-11-07/README.md)
contains Samanyu-dev’s original numerical arrangement, derived from the public CSV at
source commit `53551d77513a9f5c180a731f291baf7eda7c3009`. Source preparation is at
`54be5b33ced1d9dd0dff905af2566d4179083bb3`, sharp controls at
`01c2f91e9284be65215e051f07d7d1b0c9cc09bf`, and the independent replay at
`8b8a6ab73ca9694033fc755150138907b7d4658c`. The compressed fact is unchanged across
those three commits.

## Geometry and Evidence Binding

The importer reads binary64 centres and radian angles, derives rational half-angle
tangents through the existing outward interval calculation at 50 decimal places, and
translates the resulting exact bounding box to the origin.
The exact rational side $S$ is the `side` literal in
[`facts/n-109.yaml.gz`](../../../packing/resources/web/samanyu-n109-2026-11-07/facts/n-109.yaml.gz).
It begins $10.949289580945379338339554460712\ldots$. Exact integer arithmetic confirms
that its 12-place ceiling is **10.949289580946**.

This review independently expanded all 109 centre-and-basis poses using
$(x+(u c-v s)/2,\ y+(u s+v c)/2)$ for $(u,v)=(-1,-1),(1,-1),(1,1),(-1,1)$. All 436
corners, or 872 coordinates, equal the retained
[corner copy](../../../packing/resources/web/samanyu-n109-2026-11-07/receipts/samanyu-canonical-corners.yaml)
exactly.
All 109 bases satisfy $c^2+s^2=1$, all ids agree, all 436 square–wall clearances
are nonnegative, and the maximum span equals $S$. The positive maintained receipt’s 109
centre-and-half-angle poses also agree exactly, using $t=s/(1+c)$.

The three SHA-256 values in the
[binding record](../../../packing/resources/web/samanyu-n109-2026-11-07/receipts/canonical-independent-binding.json)
were recomputed from the immutable evidence and match.

| Object | SHA-256 |
| --- | --- |
| Decompressed exact fact | `2938dddb54398f8f91afd4dce7e83a8bbd2a56db189b1e5a92c0877d85bca5d3` |
| Corner copy | `a8b50bb7b0480e73131c9dcab68e2723555c36c32e0156c84e82e80d7f4dec81` |
| Independent checker receipt | `bd496bbdc3cf6d81cbb6ca955492874ea44059a7c22799cdf54302dff6bd4d38` |

The corner copy’s Git blob is `0c617b07e9052d7fe68d18630356480ffb4063c5`, matching the
receipt. Its `git_blob_expected` is the placeholder `-`, so `git_blob_matches: false`
does not assert a comparison with a source blob.
The explicit digest and geometry checks above bind this derived copy to the fact.
The fact’s compressed Git blob is `007a229cea68de5c8e54fe9ccf116b67f11647a3`; its
decompressed Git blob is `6e7a027f451a0bf2107bbbee44f9968daa44511a`. The packet’s
compressed-file table describes the latter.

## Verification Scope

The
[independent receipt](../../../packing/resources/web/samanyu-n109-2026-11-07/receipts/canonical-independent-check.json)
records `ACCEPT` from the archived
[`r1012_check.py`](../../../packing/resources/web/de-winter-kodaj-n109-1012-review-2026-11-20/programs/r1012_check.py).
This review inspected that driver, its decision logic, and both geometric
implementations. Method A uses Python integer separating axes.
Method B uses GMP rational convex clipping, in both pair orders.
They share the reader, and the additional Euclidean-gap calculation is descriptive.
The receipt records 109 unit squares by both methods, area exactly 1 inside the box for
each square, all 5,886 pairs apart by both methods, and zero problems or method
disagreements. The six square–wall contacts also match this review’s direct rational
calculation.

The
[maintained replay](../../../packing/resources/web/samanyu-n109-2026-11-07/receipts/exact-certification.json.xz)
records three jobs on two routes, totalling 35,316 repeated pair decisions.
Both routes accept the positive witness, reject the duplicate-square control for
overlap, and reject the translated-square control for container penetration.
The two maintained routes share parsing, half-angle conversion, rational arithmetic and
the separating-axis method.
Their agreement alone is not the independent-method confirmation supplied by the
archived SAT-and-clipping program.
All 11
[sharp controls](../../../packing/resources/web/samanyu-n109-2026-11-07/receipts/sharp-controls.json)
have their expected outcomes on both routes, comprising four accepted cases and seven
refused cases. These are 22 consistent route outcomes.

The [earlier review](review-2026-11-20-de-winter-1012-n109.md), merged in
[PR #1049](https://github.com/jlevy/squares/pull/1049), supplies the checker’s
development and control history.
Its post-freeze Samanyu witness had SHA-256
`ab84814548fc28d18a22945b3a8bb3be6c4335a7310e93fe8ea032925842bb28` and side beginning
$10.949289580945379363234535713286\ldots$. That distinct binary64 half-angle reading
cannot by itself certify this portable fact.
The new replay and the exact pose comparison supply the required binding.
The older review’s 37 controls belong to that review’s original certificate and were not
rerun here.

This confirming review ran its digest, rational geometry, ceiling and
receipt-consistency checks with project Python 3.14.7 under the memory guard.
It inspected the archived full-check receipts without rerunning their pair decisions.
It did not reacquire the original CSV, whose pin and digest are retained in the
[acquisition record](../../../packing/resources/web/samanyu-n109-2026-11-07/acquisition/sources.json).
The accepted finite bound is credited to Samanyu-dev’s arrangement.
Registration, adoption and the later de Winter/Kodaj restatement remain separate record
operations.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
