# Regularization Runs After the Adoption of Issue 989 (think-i8y9)

These are the strong generators’ runs on the witness that the adoption of jazivxt’s
issue 989 wrote at 90 in the pass of 15 November 2026, under
[the house rule](../../../campaign/result-import.md#the-house-rule), on the accepted
verdict of the stage 4 review of 15 November 2026
([review-2026-11-15-jazivxt-989.md](../../../../docs/project/reviews/review-2026-11-15-jazivxt-989.md)),
whose frozen findings this lane read at 03:33Z and whose final head it read at 03:58Z on
15 November, after its own replay, controls, measurements and registration were
committed:

| n | House | Replaces | Adopted |
| ---: | --- | --- | --- |
| 90 | T-303 | the case record’s own house, the 10 × 10 grid | 15 November 2026 |

The house is a new arrangement relative to the grid, the first packing of 90 squares
below it on record: a window of shifted copies of a crop of Joost de Winter’s packing of
157 squares, fitted.

## How They Were Run

In the records branch `claude/bold-ritchie-xo28us-l170`, after `adopt_houses` had
written the count at 03:42Z on 15 November, and after `build_known_best_atlas --update`,
`regularize_axis_components --update-atlas --n 90` and `default_drawings --update`. From
`packing/`, at most two processes, `nice -n 19`, in run directories named for the
adoption’s day and its count, the grid-slack directories named without a dot, since the
index’s schema refuses one:

```sh
P=adopt-2026-11-15-n90
python -m devtools.regularize_grid_slack --n 90 --run-dir $RUNS/$P-grid-deg05
python -m devtools.regularize_grid_slack --n 90 --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n 90 --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n 90 --workers 1
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 2 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
```

Then the one `layer` command the selection printed, for the driver’s run, and the
guide’s render-and-record step.
The axis tool’s refresh drew its view of the new witness first, so the selection was
measured against a drawing of the new witness.

## What They Found

[selection-adopt-2026-11-15-n90.md](selection-adopt-2026-11-15-n90.md) is the
selection’s table, and its JSON beside it the full report.
The figures are light, uneven and near-axis squares, angle classes and hues, then full
shared sides (house and stage), against the axis tool’s view of the new witness:

| n | View drawn | Goals before → after | Shared sides before → after | Evan Daniel’s driver |
| ---: | --- | --- | --- | --- |
| 90 | Evan Daniel’s same-side view, admitted at row 10 | 2, 4, 3, 15, 15 → 0, 0, 0, 9, 9 | 160, 195 → 193, 197 | certified KKT local minimum 1.108 × 10⁻¹¹ below the side, held at row 3 |

- **The views.** The driver’s same-side view, one to one with the witness (largest move
  0.145), is better than the axis tool’s view on every goal and both totals of shared
  sides, and the selection draws it.
  Grid-slack’s three runs each drew a view admitted at row 10 (0, 0, 0, 12, 12; 183,
  195), better than the axis view but not than the driver’s.
- **The KKT solve.** The driver certified a KKT local minimum of the side 1.108 × 10⁻¹¹
  below the certificate’s side, about 1.01 times the certificate’s own contraction
  margin (1.0988 × 10⁻¹¹) and just beyond it, held at row 3 as a register candidate and
  not admitted; registering it is RV-3’s question (think-ruu2, think-ikku).
  No report states that side.
- The record’s comparison with the base branch (`default_drawings --compare`): the grid
  was regular as published, its house drawing (no uneven or near-axis square, 350 full
  shared sides); the new witness draws the driver’s view (no uneven or near-axis square,
  193 full shared sides).
  No strong view gave way, and no runs are owed.
- The flip record decides the new picture’s pose (`flip_regularization --check`): a
  mirror across the falling diagonal, by quadrants.

## Retained Here

| Directory or file | What |
| --- | --- |
| `adopt-2026-11-15-n90-grid-deg05/`, `-grid-deg1/`, `-grid-deg5/` | each run’s block, `run.json`, summed from its report, and the report, `n-090/report.json.gz` |
| `adopt-2026-11-15-n90-evand/` | the driver’s `receipt.json` and its report |
| `selection-adopt-2026-11-15-n90.json.gz`, `.md` | the selection’s report and table |

The runs cost about 4.6 CPU-seconds for grid-slack’s three runs, 13.9 CPU-seconds for
the driver by its receipt, and seconds for the selection.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
