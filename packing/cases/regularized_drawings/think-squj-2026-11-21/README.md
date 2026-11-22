# Drawing runs for T-337 at 259

T-337’s house witness uses Sergio Fernández Rubio’s (GeiserX) 259-square construction
with Joost de Winter’s rational refinement.
Its side rounds up to 16.590016439230 at 12 places.
The witness changed when T-337 replaced T-193.

| Run | Outcome |
| --- | --- |
| Grid-slack at 0.5°, 1° and 5° | Each run refused every attempted view. Relaxed rows overlap at the requested side or the re-solved centers move beyond the admissible displacement. |
| Evan Daniel’s driver | The three exact routes accept the solved witness at a side about 1.659 × 10⁻¹⁹ above the upper bound. The same-side run refused with `unmatched-rotation`. |
| Selection | Row 4 holds the solved view. No candidate advances to the register or replaces the axis view at the house’s exact side. |

The four run reports, solver receipt, exact certificate and solved witness are retained.
The grid blocks summarize the elapsed time in each report.
They have no separate CPU measurement.
The [retention check](retention.json) verifies the solver receipt’s artifacts, all 259
pairs of pose encodings and their exact side.
The [selection](selection.json.gz) uses repository-relative paths.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
