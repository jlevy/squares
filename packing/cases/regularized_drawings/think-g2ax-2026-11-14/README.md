# Regularization Runs After the Adoption of Issue 977 (think-g2ax)

These are the strong generators’ runs on the witness that the adoption of Joost de
Winter’s issue 977 wrote at 297, under
[the house rule](../../../campaign/result-import.md#the-house-rule), after the stage 4
review of 14 November 2026
([review-2026-11-14-de-winter-977-979.md](../../../../docs/project/reviews/review-2026-11-14-de-winter-977-979.md)):

| n | House | Replaces | Adopted |
| ---: | --- | --- | --- |
| 297 | T-299 | T-174 | 14 November 2026 |

The house is a new arrangement in the layout of T-174’s packing (Francisco Couzo’s, as
Evan Daniel and PingYou Ltd improved it), with a double step in each staircase.

## How They Were Run

In the records branch `claude/bold-ritchie-xo28us-l154`, after `adopt_houses` had
written the count, and after `build_known_best_atlas --update`,
`regularize_axis_components --update-atlas --n 297` and `default_drawings --update`.
From `packing/`, at most two processes, `nice -n 19`, in run directories named for the
adoption’s day and its count.
`adopt_houses` printed the grid-slack names with a dot (`-grid-0.5`), which the layer
admitted and the index’s schema refuses (a run id is `^[a-z0-9-]+$`), so the three
directories were renamed as below, the selection run again and the view admitted again
under the new name:

```sh
N=297; P=adopt-2026-11-14-n297
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg05
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n $N --workers 1
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 2 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
```

Then the one `layer` command the selection printed, for grid-slack’s 0.5-degree run, and
the guide’s render-and-record step.
The axis tool’s refresh drew its view of the new witness first, so the selection was
measured against a drawing of the new witness.
The settlement of 297 on T-174’s witness (decided no better by the runs of 17 October,
think-3mry) lapsed with the adoption and is taken off.

## What They Found

[selection-adopt-2026-11-14-n297.md](selection-adopt-2026-11-14-n297.md) is the
selection’s table, and its JSON beside it the full report.
The view is drawn at the witness’s side, admitted at row 10, and better than the axis
tool’s view on both totals of shared sides and worse on no goal; the figures are light,
uneven and near-axis squares, angle classes and hues, then full shared sides (house and
stage):

| n | View drawn | Goals before → after | Shared sides before → after | Evan Daniel’s driver |
| ---: | --- | --- | --- | --- |
| 297 | grid-slack’s 0.5-degree view | 0, 0, 0, 17, 17 → 0, 0, 0, 17, 17 | 728, 886 → 774, 904 | solved view 1.77 × 10⁻¹⁹ above the side, held at row 4 |

- Grid-slack’s three runs, at 0.5, 1 and 5 degrees, drew the same view, one to one with
  the witness (largest move 0.0172), each admitted at row 10, and the selection drew the
  first of the three that tie.
- Evan Daniel’s driver refused its same-side view (`same-side-refused:
  literal-too-large`). Its certified KKT solve lies 1.824 × 10⁻⁵⁹ below the side, the
  certificate’s own contraction margin, and its solved view, dilated to an exact
  certificate, 1.77 × 10⁻¹⁹ above it, so the view is held at row 4 (`dilated-side`) and
  there is no register candidate; a side inside the certificate’s own padding is RV-3’s
  question (think-ruu2).
- The record’s comparison with the base branch: T-174’s witness was drawn as its house
  drawing (787 full shared sides, decided no better); the new witness draws grid-slack’s
  view (774), with no uneven or near-axis square either way.
  No strong view gives way to a worse drawing, and no runs are owed.
- The flip record decides the new picture’s pose (`flip_regularization --check`): a
  mirror across the falling diagonal, by quadrants.

## Retained Here

| Directory or file | What |
| --- | --- |
| `adopt-2026-11-14-n297-grid-deg05/`, `-grid-deg1/`, `-grid-deg5/` | each run’s block, `run.json`, summed from its report, and the report, `n-297/report.json.gz` |
| `adopt-2026-11-14-n297-evand/` | the driver’s `receipt.json` and its report |
| `selection-adopt-2026-11-14-n297.json.gz`, `.md` | the selection’s report and table |

The runs cost about 339 CPU-seconds for grid-slack’s three runs, 318 CPU-seconds for the
driver by its receipt, and about 3.6 minutes of wall for the selection, on a host shared
with another lane.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
