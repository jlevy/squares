# Review Programs for Khalili and Gharabaghi’s `s(44) = 7`

These are the programs written for the stage 4 review
[review-2026-10-31-khalili-gharabaghi-s44-mixed-cover.md](../../../../../docs/project/reviews/review-2026-10-31-khalili-gharabaghi-s44-mixed-cover.md)
of the closed mixed cover for $s(44) = 7$, with everything they printed.
The reviewer is Claude, strong sub-agent tier, in a distinct pass of the intake lane that
retained the source.

**They decide nothing.** Every number they report is exact (Python integers and
`fractions.Fraction`); floating point only chooses where to look, and no output is a
certificate. A sample of poses can find a violation and cannot show that none exists,
so no evidence entry cites these programs, and none is registered in
[`verifiers.yaml`](../../../../frontier/verifiers.yaml).

Both programs import nothing from the source, from Daniel’s checkers or from this
repository. `s44_review.py` was written from the mixed format v1 specification
(`certificate/FORMAT_mixed_v1.md`), the statement and the record formats as read in the
source’s files; `zmx2_fn_diff.py` only locates what a reader of two `zmx2.rs` versions
has to read.

## What Each Program Does

| Program | Reads | Does | Output |
| --- | --- | --- | --- |
| `programs/s44_review.py cover COVER` | the cover | its own parser of the mixed format: well-formedness, the exact total and slack below 44, the point and segment census, wall segments, points on loaded lines, and $D_4$ invariance as a measure under all eight symmetries (points by position, each line’s density as a canonical step function) | `outputs/cover-n44.json` |
| `programs/s44_review.py compare-s45 COVER S45` | this cover and Daniel’s $s(45) = 7$ cover, retained in the evand 28 September packet | denominators, segment supports and shared point positions, for the warm-start credit | `outputs/compare-s45.json` |
| `programs/s44_review.py zm-records DIR` | the source’s `verification/logs/zm_mixed/` | the `zm_mixed.py` records: digests and settings in every header, every root of the $D_4$ grid at the header’s pitch and bins once, the census, and whether every root uncertified at depth 24 is certified whole by a deeper run | `outputs/zm-records-n44.json` |
| `programs/s44_review.py poses COVER` | the cover | exact $\mu(Q)$ at sampled admissible poses (uniform in the $D_4$ region, near the grid tiles, flush against a wall at tilts of 0.01° to 3°, near 45°), then float descents from the lowest, each end re-evaluated exactly at a rational pose | `outputs/poses-n44.json` |
| `programs/s44_review.py mutants COVER` | the cover | its own removal of the heaviest point orbit and of the heaviest segment orbit, the mutants’ SHA-256 (to compare with the control receipts), and for each a rational pose where the mutant captures less than 1 exactly, with the published cover’s mass there | `outputs/mutants-n44.json` |
| `programs/zmx2_fn_diff.py A.rs B.rs [--show NAME ...]` | two `zmx2.rs` files | every top-level function, same, changed, or only in one; `--show` prints a function’s diff | `outputs/zmx2-fn-diff.txt` |

## How They Were Run

On 31 October 2026, on the shared four-core container of the intake lane, under the
project interpreter with `-I`, from a scratch copy of the programs; the cover was read
from the packet’s `s44-equals-7/certificate/s44_cover_7.txt.gz`. From `packing/`:

```shell
P=resources/web/moh63-dev-s44-equals-7-2026-10-29
COVER=$P/s44-equals-7/certificate/s44_cover_7.txt.gz
.venv/bin/python3 -I $P/review/programs/s44_review.py cover "$COVER"
.venv/bin/python3 -I $P/review/programs/s44_review.py compare-s45 "$COVER" \
    resources/web/evand-square-packing-2026-09-28/square-packing/s12/certificates/s45/s45_mixed_cover_7.txt.gz
.venv/bin/python3 -I $P/review/programs/s44_review.py zm-records $P/s44-equals-7/verification/logs/zm_mixed
.venv/bin/python3 -I $P/review/programs/s44_review.py poses "$COVER"
.venv/bin/python3 -I $P/review/programs/s44_review.py mutants "$COVER"
.venv/bin/python3 -I $P/review/programs/zmx2_fn_diff.py \
    resources/web/evand-square-packing-2026-09-28/square-packing/s12/verify2/src/bin/zmx2.rs \
    resources/web/evand-square-packing-2026-10-04/square-packing/s12/verify2/src/bin/zmx2.rs
```

`poses` and `mutants` take a fixed seed (842), so a rerun repeats the same poses.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
