# Three Exact Grid Contacts at 259

The reference is the first-party axis-components drawing of
[Joost de Winter’s T-337 certificate](../../../frontier/n-259.md#joost-de-winters-certificate-t-337)
for Sergio Fernández Rubio’s tilted-band construction.

In that drawing’s native frame, move square 118 against 114, 99 against 101, and 104
against 108. Each move closes one full shared side exactly. All rotations and the other
256 centers stay fixed. The [admission receipt](receipt.json) identifies the original
axis-components view, the exact displacements, and both verifiers’ checks of all
33,411 pairs and the walls at the same bound.

| Drawing measure | Before | After |
| --- | ---: | ---: |
| Light aligned squares | 23 | 19 |
| Uneven aligned squares | 65 | 65 |
| House full-side total | 545 | 551 |
| Stage full-side total | 727 | 727 |

No square loses a contact against either the certified house or the previous atlas
drawing. The view passes row 10. The receipt also compares the result with the T-337
house. The rotations it lists in that comparison come from the axis-components view.
The exact side and certificate credit remain with T-337.

From `packing/`, reproduce the repair with:

```bash
python -m devtools.regularize_local_stencil --n 259 \
  --face 118 114 --face 99 101 --face 104 108 --install \
  --receipt packing/cases/regularized_drawings/think-q3yr-2026-11-23/receipt.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
