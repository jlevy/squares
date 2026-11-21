# Regularization Runs for the Adoption of Issue 1038 (think-91fu)

The strong generators ran on Doğa Özden’s witness at 228 on 20 November 2026. Their
selected view supports the 21 November UTC adoption under
[the house rule](../../../campaign/result-import.md#the-house-rule), following the
accepted stage 4 review of 20 November 2026
([review-2026-11-20-ozden-1038.md](../../../../docs/project/reviews/review-2026-11-20-ozden-1038.md),
pull request 1044):

| n | House | Replaces | Adopted |
| ---: | --- | --- | --- |
| 228 | T-334 | T-301 | 21 November 2026 UTC |

T-334 is Özden’s exact certificate of jazivxt’s public Kaggle packing, one to one with
T-301’s packing and 1.23 times T-301’s contraction margin below it, so a new result
under the owner’s option D (think-b0w5).

## What Ran

From `packing/`, with the project interpreter, at `nice -n 15` on a four-core host
shared with other lanes, the commands `devtools.adopt_houses` printed:

- `build_known_best_atlas --update`, `regularize_axis_components --update-atlas --n 228`
  and `default_drawings --update`, which read 228 pending;
- `regularize_grid_slack --n 228` at 0.5, 1 and 5 degrees (`--near-axis-degrees`), into
  the run directories `adopt_houses` printed, `adopt-2026-11-20-n228-grid-0.5`,
  `-grid-1` and `-grid-5`;
- `regularize_evand run --n 228 --workers 1`, Evan Daniel’s driver;
- `regularize_select` over the four runs and the `regularize_evand layer` command it
  printed;
- `render_regularized_atlas --update`, `default_drawings --update`,
  `flip_regularization --update`, `regularized_drawings` and `render_results --update`.

## What They Decided

| n | View drawn | Goals before → after | Shared sides before → after | Evan Daniel’s driver |
| ---: | --- | --- | --- | --- |
| 228 | grid-slack’s 0.5-degree view, admitted at row 10 | 38, 108, 8, 36, 19 → 1, 20, 0, 28, 19 | 401, 567 → 632, 654 | KKT solve 9.66 × 10⁻¹⁴ below the side, verified exactly, held at row 3 |

The figures are light, uneven and near-axis squares, angle classes and hues, then full
shared sides (house and stage), against the axis tool’s view of the new witness.

- **228.** Grid-slack’s three runs each drew a view admitted at row 10, and the
  selection draws the 0.5-degree run’s, better on light, uneven and near-axis squares,
  classes and both totals of shared sides.
  `default_drawings --compare` against `main`: on T-301’s witness 228 was decided no
  better and drew the axis tool’s view (17 uneven, 1 near-axis, 644 full shared sides);
  the new witness is regularized and draws grid-slack’s view (20 uneven, 0 near-axis,
  632). No strong view gave way.
  228’s `default_drawings.SETTLED` entry, decided on T-301’s witness, is taken off.
- **The KKT solve.** Run on this certificate, the driver reached a local minimum of the
  side, strict modulo 123 exact flat motions, whose rational certificate validated this
  time, at 3899010779157917479945828568311/250000000000000000000000000000 =
  15.596043116631669919783314273244: exactly the side of its 15 November solve from
  T-301’s witness (think-17ex), 9.659 × 10⁻¹⁴ below this side.
  It is held at row 3 as a register candidate and not admitted.
  By the owner’s decision of 18 November 2026 at #1009’s re-solves (think-frl5), T-334
  keeps its new-result status, and the solve stays a candidate for registration
  (think-4z8z). Its solved view, measured against the certificate by
  `devtools.measure_identity`, is one to one by nearest centres with 6 squares beyond a
  tenth (largest 0.422) and turns up to 6.58 degrees; it is the driver’s regularized
  drawing at the solved side, and the minimum is strict only modulo its flat motions, so
  the measurement does not decide whether the certificate is that point.
- The flip record decides the new picture’s pose (`flip_regularization --n 228`): a half
  turn with a flip, mirrored across the rising diagonal, by quadrants.

The layer’s index refuses a run id with a dot, so after the layer wrote the 0.5-degree
run as `grid-slack-adopt-2026-11-20-n228-grid-0.5` the three runs were renamed
`-grid-deg05`, `-grid-deg1` and `-grid-deg5`, as earlier passes name theirs, in the
index, the view’s provenance line (its digest in the index moved with it), the drawings
record and the run blocks here.
The selection’s report and table keep the names the selection read.

## Retained Here

| Directory or file | What |
| --- | --- |
| `adopt-2026-11-20-n228-grid-deg05/`, `-grid-deg1/`, `-grid-deg5/` | each run’s block, `run.json`, summed from its report, and the report, `n-228/report.json.gz` |
| `adopt-2026-11-20-n228-evand/` | the driver’s `receipt.json` and its report |
| `selection-adopt-2026-11-20-n228.json.gz`, `.md` | the selection’s report and table |

The runs cost about 43 CPU-seconds for grid-slack’s three runs, 105 CPU-seconds for the
driver by its receipt, and seconds for the selection.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
