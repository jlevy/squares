# Regularization Runs After the Adoption of Issue 960 (think-my76)

These are the strong generators’ runs on the witness that the adoption of Doğa Özden’s
issue 960 wrote at 237, under
[the house rule](../../../campaign/result-import.md#the-house-rule), after the stage 4
review of 11 November 2026
([review-2026-11-11-ozden-960.md](../../../../docs/project/reviews/review-2026-11-11-ozden-960.md)):

| n | House | Replaces | Adopted |
| ---: | --- | --- | --- |
| 237 | T-295 | T-190 | 12 November 2026 |

The house is a new arrangement relative to T-190’s packing, found by Özden’s band-design
search from two copies of the tilted squares of the registry’s n = 70 packing.

## How They Were Run

In the records branch `claude/bold-ritchie-xo28us-l110`, after `adopt_houses` had
written the count, and after `build_known_best_atlas --update`,
`regularize_axis_components --update-atlas --n 237` and `default_drawings --update`.
From `packing/`, at most two processes, `nice -n 19`, in run directories named for the
adoption’s day and its count, with no dot in the grid-slack names (the layer index
refuses a dot in a run id):

```sh
N=237; P=adopt-2026-11-11-n237
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg05
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n $N --workers 1
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 2 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
```

Then the one `layer` command the selection printed, for Evan Daniel’s driver, and the
guide’s render-and-record step.
The axis tool’s refresh replaced its index entry at 237, its view of T-190’s witness,
with its view of the new witness, so the selection was measured against a drawing of the
new witness, and no candidate carries the note that a run measured it against another
drawing than the tree’s. The `SETTLED` entry at 237, decided on T-190’s witness, is
taken off.

## What They Found

[selection-adopt-2026-11-11-n237.md](selection-adopt-2026-11-11-n237.md) is the
selection’s table, and its JSON beside it the full report.
The view is drawn at the witness’s side, admitted at row 10, and better on every goal it
changes; the figures are light, uneven and near-axis squares, angle classes and hues,
then full shared sides (house and stage), the drawing before against the view:

| n | View drawn | Goals before → after | Shared sides before → after | KKT solve below the side (row 3, held) |
| ---: | --- | --- | --- | --- |
| 237 | Evan Daniel’s same-side view | 33, 68, 68, 75, 19 → 0, 0, 0, 2, 2 | 331, 721 → 788, 788 | 3.44 × 10⁻¹² |

- Grid-slack’s three runs were admitted at row 10 as well and are better than the
  drawing on every goal, but draw more angle classes than Evan Daniel’s view: 12 classes
  and hues and 728 and 752 shared sides at 0.5 degrees, and one view, 11 and 11 and 732
  and 756, at 1 and 5 degrees.
- Evan Daniel’s certified KKT solve lies 3.44 × 10⁻¹² below the side, 1.15 of the
  certificate’s own contraction margin (2.985 × 10⁻¹²). It is held at row 3 as a
  register candidate, not admitted, as at 156, 172, 179, 180, 199, 268, 269 and 270; its
  registration is RV-3’s (think-ruu2, think-ikku).
- The flip record decides the new picture’s pose again (`flip_regularization --check`):
  a half turn, by quadrants, where T-190’s view stood in its published pose.

## Retained Here

| Directory or file | What |
| --- | --- |
| `adopt-2026-11-11-n237-grid-deg05/`, `-grid-deg1/`, `-grid-deg5/` | each run’s block, `run.json`, summed from its report, and the report, `n-237/report.json.gz` |
| `adopt-2026-11-11-n237-evand/` | the driver’s `receipt.json` and its report |
| `selection-adopt-2026-11-11-n237.json.gz`, `.md` | the selection’s report and table |

The runs cost about 28 CPU-seconds for grid-slack’s three runs, 77.3 CPU-seconds for the
driver by its receipt, and about 21 seconds of wall for the selection.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
