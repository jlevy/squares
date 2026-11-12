# Regularization Runs After the Adoption of Issue 962 (think-s418)

These are the strong generators’ runs on the witness that the adoption of Doğa Özden’s
issue 962 wrote at 269, under
[the house rule](../../../campaign/result-import.md#the-house-rule), after the stage 4
review of 12 November 2026
([review-2026-11-12-ozden-962.md](../../../../docs/project/reviews/review-2026-11-12-ozden-962.md)):

| n | House | Replaces | Adopted |
| ---: | --- | --- | --- |
| 269 | T-296 | T-290 | 12 November 2026 |

The house is a new arrangement relative to T-290’s packing, the author’s own of the day
before, found by his band-design search from tilted squares of the registry’s n = 207
and n = 70 packings and his own n = 179 packing of issue 954.

## How They Were Run

In the records branch `claude/bold-ritchie-xo28us-l120`, after `adopt_houses` had
written the count, and after `build_known_best_atlas --update`,
`regularize_axis_components --update-atlas --n 269` and `default_drawings --update`.
From `packing/`, at most two processes, `nice -n 19`, in run directories named for the
adoption’s day and its count, with no dot in the grid-slack names (the layer index
refuses a dot in a run id):

```sh
N=269; P=adopt-2026-11-12-n269
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg05 --near-axis-degrees 0.5
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n $N --workers 1
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 2 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
```

Then the one `layer` command the selection printed, for grid-slack’s 1-degree run, and
the guide’s render-and-record step.
The axis tool’s refresh replaced its index entry at 269 with its view of the new
witness, so the selection was measured against a drawing of the new witness, and no
candidate carries the note that a run measured it against another drawing than the
tree’s. The grid-slack 0.5-degree view of T-290’s witness, drawn there since 11
November, lapsed with the adoption.

## What They Found

[selection-adopt-2026-11-12-n269.md](selection-adopt-2026-11-12-n269.md) is the
selection’s table, and its JSON beside it the full report.
The view is drawn at the witness’s side, admitted at row 10, and better on every goal it
changes; the figures are light, uneven and near-axis squares, angle classes and hues,
then full shared sides (house and stage), the drawing before against the view:

| n | View drawn | Goals before → after | Shared sides before → after | KKT solve below the side (row 3, held) |
| ---: | --- | --- | --- | --- |
| 269 | grid-slack’s 1-degree view | 17, 52, 29, 54, 19 → 1, 3, 0, 24, 19 | 651, 826 → 836, 854 | 3.39 × 10⁻¹² |

- Grid-slack’s 5-degree run drew the same view as its 1-degree run, and its 0.5-degree
  run one with 25 classes and 828 and 846 shared sides; all three were admitted at row
  10, and the selection drew the first of the two that tie.
- Evan Daniel’s driver refused its same-side view (`same-side-refused:
  unmatched-rotation`), so it drew no view at the witness’s side.
  Its certified KKT solve lies 3.39 × 10⁻¹² below the side, 1.05 of the certificate’s
  own contraction margin (3.234 × 10⁻¹²), and draws 1, 3, 0, 10 and 10 with 860 and 864
  shared sides. It is held at row 3 as a register candidate, not admitted, as at 156,
  172, 179, 180, 199, 268, 269 for T-290 and 270; its registration is RV-3’s
  (think-ruu2, think-ikku).
- The record’s comparison with the base branch notes that the strong view gives way to a
  drawing worse on uneven squares: T-290’s view drew no uneven square and 646 shared
  sides, this one 3 and 836. It is a view of a different witness, regularized, and owes
  no run.
- The flip record decides the new picture’s pose again (`flip_regularization --check`):
  a mirror across the rising diagonal, by quadrants, where T-290’s view stood turned a
  quarter turn clockwise.

## Retained Here

| Directory or file | What |
| --- | --- |
| `adopt-2026-11-12-n269-grid-deg05/`, `-grid-deg1/`, `-grid-deg5/` | each run’s block, `run.json`, summed from its report, and the report, `n-269/report.json.gz` |
| `adopt-2026-11-12-n269-evand/` | the driver’s `receipt.json` and its report |
| `selection-adopt-2026-11-12-n269.json.gz`, `.md` | the selection’s report and table |

The runs cost about 34 CPU-seconds for grid-slack’s three runs, 114.8 CPU-seconds for
the driver by its receipt, and about 35 seconds of wall for the selection.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
