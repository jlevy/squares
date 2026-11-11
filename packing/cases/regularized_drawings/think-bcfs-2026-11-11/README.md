# Regularization Runs After the Adoption of Issue 958 (think-bcfs)

These are the strong generators’ runs on the witnesses that the adoption of Joost de
Winter’s issue 958 wrote at 132 and 157, under
[the house rule](../../../campaign/result-import.md#the-house-rule), after the stage 4
review of 11 November 2026
([review-2026-11-11-dewinter-132-157.md](../../../../docs/project/reviews/review-2026-11-11-dewinter-132-157.md)):

| n | House | Replaces | Adopted |
| ---: | --- | --- | --- |
| 132 | T-292 | T-174 | 11 November 2026 |
| 157 | T-293 | the 13 × 13 grid | 11 November 2026 |

Each house is a pinwheel de Winter grew from Samanyu-dev’s 109 by cut-and-fill steps, a
new arrangement relative to the packing it replaces.

## How They Were Run

In the records branch `claude/bold-ritchie-xo28us-l104`, after `adopt_houses` had written
both counts, and after `build_known_best_atlas --update`,
`regularize_axis_components --update-atlas --n 132 157` and `default_drawings --update`.
From `packing/`, at most two processes, `nice -n 19`, in run directories named for the
adoption’s day and its counts, with no dot in the grid-slack names:

```sh
N="132 157"; P=adopt-2026-11-11-n132-157
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg05
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n $N --workers 2
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 2 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
```

Then the one `layer` command the selection printed, for grid-slack’s 0.5-degree run at
both counts, and the guide’s render-and-record step. The `SETTLED` entry at 132, decided
on T-174’s witness, is taken off; 157 had none.

## What They Found

[selection-adopt-2026-11-11-n132-157.md](selection-adopt-2026-11-11-n132-157.md) is the
selection’s table, and its JSON beside it the full report. Both views are drawn at the
witness’s side and admitted at row 10. The figures are light, uneven and near-axis
squares, angle classes and hues, then full shared sides (house and stage), the drawing
before against the view:

| n | View drawn | Goals before → after | Shared sides before → after | Better on |
| ---: | --- | --- | --- | --- |
| 132 | grid-slack, 0.5 degrees | 1, 3, 1, 15, 15 → 0, 0, 0, 14, 14 | 269, 302 → 288, 306 | every goal it changes |
| 157 | grid-slack, 0.5 degrees | 0, 0, 0, 5, 5 → 0, 0, 0, 5, 5 | 368, 376 → 376, 376 | house shared sides |

- The drawing before at 132 is the axis tool’s view of the new witness, and at 157 the
  new witness itself.
- Grid-slack’s runs at 1 and 5 degrees were admitted at row 10 as well; the selection
  prefers the 0.5-degree view at both counts.
- Evan Daniel’s driver solved each witness to a certified view about 1.2 × 10⁻¹⁹ (132)
  and 1.3 × 10⁻¹⁹ (157) above its side, held at row 4: no register candidate.
- The flip record decides each new picture’s pose again (`flip_regularization --check`):
  132 turned a half turn and flipped, by quadrants; 157 in its published pose, by the
  grid-4 test.

## Retained Here

| Directory or file | What |
| --- | --- |
| `adopt-2026-11-11-n132-157-grid-deg05/`, `-grid-deg1/`, `-grid-deg5/` | each run’s block, `run.json`, summed from its reports, and the reports, `n-NNN/report.json.gz` |
| `adopt-2026-11-11-n132-157-evand/` | the driver’s `receipt.json` and its reports |
| `selection-adopt-2026-11-11-n132-157.json.gz`, `.md` | the selection’s report and table |

The runs cost about 6 CPU-minutes for grid-slack’s three runs (about 121 seconds each by
their reports), 51.3 CPU-seconds for the driver by its receipt, and about 2 minutes of
wall for the selection.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
