# Regularization Runs After the Adoption of Issue 967 (think-n73d)

These are the strong generators’ runs on the witness that the adoption of Doğa Özden’s
issue 967 wrote at 269, under
[the house rule](../../../campaign/result-import.md#the-house-rule), after the stage 4
review of 12 November 2026
([review-2026-11-12-ozden-967.md](../../../../docs/project/reviews/review-2026-11-12-ozden-967.md)):

| n | House | Replaces | Adopted |
| ---: | --- | --- | --- |
| 269 | T-297 | T-296 | 13 November 2026 |

The house is a new arrangement relative to T-296’s packing, the author’s own of 12
November, found by his lab’s column-band designer.
The pass is dated 13 November, the day its pull request can merge at the earliest: the
pass of 12 November had already moved 269 to T-296, and a day’s archive holds one prior
state a count. The runs were made on 12 November and are named for the pass’s day.

## How They Were Run

In the records branch `claude/bold-ritchie-xo28us-l132`, after `adopt_houses` had
written the count, and after `build_known_best_atlas --update --n 269`,
`regularize_axis_components --update-atlas --n 269` and `default_drawings --update`.
From `packing/`, at most two processes, `nice -n 19`, in run directories named for the
adoption’s day and its count, with no dot in the grid-slack names (the layer index
refuses a dot in a run id):

```sh
N=269; P=adopt-2026-11-13-n269
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg05 --near-axis-degrees 0.5
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n $N --workers 1
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 2 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
```

Then the one `layer` command the selection printed, for grid-slack’s 0.5-degree run, and
the guide’s render-and-record step.
The axis tool’s refresh replaced its index entry at 269 with its view of the new
witness, so the selection was measured against a drawing of the new witness, and no
candidate carries the note that a run measured it against another drawing than the
tree’s. The grid-slack 1-degree view of T-296’s witness, drawn there since 12 November,
lapsed with the adoption.

## What They Found

[selection-adopt-2026-11-13-n269.md](selection-adopt-2026-11-13-n269.md) is the
selection’s table, and its JSON beside it the full report.
The view is drawn at the witness’s side, admitted at row 10, and better on every goal it
changes; the figures are light, uneven and near-axis squares, angle classes and hues,
then full shared sides (house and stage), the drawing before against the view:

| n | View drawn | Goals before → after | Shared sides before → after | KKT solve below the side (row 3, held) |
| ---: | --- | --- | --- | --- |
| 269 | grid-slack’s 0.5-degree view | 18, 54, 6, 19, 19 → 0, 0, 0, 13, 13 | 729, 781 → 842, 864 | 3.36 × 10⁻¹² |

- Grid-slack’s three runs, at 0.5, 1 and 5 degrees, drew the same view, each admitted at
  row 10, and the selection drew the first of the three that tie.
- Evan Daniel’s driver refused its same-side view (`same-side-refused:
  unmatched-rotation`), so it drew no view at the witness’s side.
  Its certified KKT solve lies 3.36 × 10⁻¹² below the side, 1.04 of the certificate’s
  own contraction margin (3.236 × 10⁻¹²), and draws 4, 50, 0, 5 and 5 with 825 and 880
  shared sides. It is held at row 3 as a register candidate, not admitted, as at 156,
  172, 179, 180, 199, 268, 270, and 269 for T-290 and T-296; its registration is RV-3’s
  (think-ruu2, think-ikku).
- The record’s comparison with the base branch finds no strong view giving way to a
  worse drawing: T-296’s view drew 3 uneven squares and 836 shared sides, this one none
  and 842.
- The flip record decides the new picture’s pose again (`flip_regularization --check`):
  a mirror across the falling diagonal, by quadrants, where T-296’s view stood mirrored
  across the rising diagonal.

## Retained Here

| Directory or file | What |
| --- | --- |
| `adopt-2026-11-13-n269-grid-deg05/`, `-grid-deg1/`, `-grid-deg5/` | each run’s block, `run.json`, summed from its report, and the report, `n-269/report.json.gz` |
| `adopt-2026-11-13-n269-evand/` | the driver’s `receipt.json` and its report |
| `selection-adopt-2026-11-13-n269.json.gz`, `.md` | the selection’s report and table |

The runs cost about 31 CPU-seconds for grid-slack’s three runs, 185.5 CPU-seconds for
the driver by its receipt, and about 26 seconds of wall for the selection.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
