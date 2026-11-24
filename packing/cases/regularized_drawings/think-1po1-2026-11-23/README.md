# Exact Local Stack at 127

The published T-341 house has a staggered seam between squares 108 and 110. The contact
census records two uneven aligned squares and house and stage totals of 259 and 293. The
house’s exact side and source witness serve as the control.

In the house’s native frame, square 108 stays fixed.
Square 110 moves to share 108’s right side.
Square 116 straightens and moves directly above 110. All other centers, bases, and
square identities stay fixed.
This gives the two new pair contacts exact full sides and holds the side to T-341. The
[receipt](receipt.json) records the rational side and both independent exact checks of
all 8,001 pairs and the walls.

| Variant | Outcome |
| --- | --- |
| Move only 110 | Overlaps 116. |
| Move only 108 to 110 | Overlaps 109. |
| Move 110 and seat 116 at the upper wall | Exactly valid. Ties the local stack on the drawing measures. |
| Move 110 and stack 116 directly above | Exactly valid. Closes the two intended seams. Selected among the tied alternatives because it makes both new pair contacts full sides exactly. |

The selected view reduces light aligned squares from one to zero and uneven aligned
squares from two to zero.
The house and stage totals rise to 266 and 300. Neither rule loses a contact count at
any individual square, including against the previously retained layer view.
The near-axis, angle-class, and hue counts hold.
The view passes row 10 and improves the displayed house under the drawing rule.

From `packing/`, reproduce the selection against the earlier default and install it with
the local stencil generator:

```bash
python -m devtools.regularize_local_stencil --n 127 --stack 108 110 116 --install \
  --receipt packing/cases/regularized_drawings/think-1po1-2026-11-23/receipt.json
```

Once the same stencil is installed, the command checks that the retained geometry
matches the recipe. The atlas verification checks the installed view again.
T-341 keeps its prior certificate and lineage credit.
This drawing is a same-side regularization by the Squares Project.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
