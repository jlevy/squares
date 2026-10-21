# Erratum: the 21 October Review of Evan Daniel’s Import at 270

**Date:** 21 October 2026. **Correction:** the
[review of 21 October 2026](review-2026-10-21-upper-bound-import-703.md) twice says that
Evan Daniel’s regularized view `s270_sw_regularized.cert` is his certificate
`s270_sw.cert` “under a reflection”.
The symmetry is a quarter turn of the box, a rotation, whose linear part has determinant
$+1$. The correction changes no bound, rung, finding or adoption.

The review is kept as its reviewer wrote it, so the correction is here, beside it.
This erratum is the records lane’s, not the reviewer’s: an AI agent (Claude) wrote it
for the records pull request that followed PR #708, under the bead `think-xl9i`.

## Where the Review Says It

- **For the Author**, question 2 (line 60): “the view is the certificate under a
  reflection with that square set to t = 0”.
- **The Review’s Route** (line 126): “against the certificate it is one to one under a
  reflection with no square moved beyond 10^-9”.

Read “a quarter turn of the box” for “a reflection” in both places.
Everything else in both sentences stands: one to one, no square moved beyond $10^{-9}$,
and one square, square 82, turned upright.

## What Shows It

The review’s own output records a rotation.
[`out-view.json`](../../../packing/resources/web/evand-n270-sweep-2026-10-20/review/review-2026-10-21/outputs/out-view.json),
which the review cites for the second sentence, gives the matching symmetry as
`"symmetry": 1`. The review’s `lineage_708.py` counts the eight symmetries of the box as
`devtools.check_half_angle_area.symmetric` does: $k$ quarter turns about the box’s
centre, after a reflection in $x = s/2$ only when $k \ge 4$. So $k = 1$ is one quarter
turn, $(x, y) \mapsto (s - y, x)$, with no reflection.
The measurement was right; only the word for it was wrong.

## The Reply That Says So

The final reply on
[#703](https://github.com/jlevy/squares/issues/703#issuecomment-6308741545), posted at
2026-10-21T05:23:53Z, answers the review’s question 2 from the author’s retained
`s270_sw.json`, which lists `free_squares: [82]`: square 82 is the one rattler his
report counts, and the one square his view turns upright.
It says that the view is “the certificate under a quarter turn of the box with that
square set to t = 0”, and that “The review wrote ‘reflection’ for that turn; it is a
rotation.”

## What Else Carries It

Nothing in the record repeats the word.
T-224’s register entry, its two evidence entries, the case record at 270, the packet
README and the retained review programs’ README describe the view without naming the
symmetry, so none of them changes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
