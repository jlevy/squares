# Regularization Runs After the Adoption of Issues 943, 944, 945 and 947 (think-xq4o)

These are the strong generators’ runs on the witnesses that the adoption of Doğa Özden’s
issues 943, 944, 945 and 947 wrote at 156, 180, 268 and 269, under
[the house rule](../../../campaign/result-import.md#the-house-rule), after the stage 4
review of 11 November 2026
([review-2026-11-11-ozden-943-947.md](../../../../docs/project/reviews/review-2026-11-11-ozden-943-947.md)):

| n | House | Replaces | Adopted |
| ---: | --- | --- | --- |
| 156 | T-287 | T-186 | 11 November 2026 |
| 180 | T-288 | T-174 | 11 November 2026 |
| 268 | T-289 | T-276 | 11 November 2026 |
| 269 | T-290 | T-174 | 11 November 2026 |

Each house is a new arrangement relative to the one it replaces, found by Özden’s
transplant search from another count’s registry packing.

## How They Were Run

In the records branch `claude/bold-ritchie-xo28us-l81`, after `adopt_houses` had written
the four counts, and after `build_known_best_atlas --update`,
`regularize_axis_components --update-atlas --n 156 180 268 269` and
`default_drawings --update`. From `packing/`, at most two processes, `nice -n 19`, in
run directories named for the adoption’s day and its lowest and highest count, with no
dot in the grid-slack names (the layer index refuses a dot in a run id):

```sh
N="156 180 268 269"; P=adopt-2026-11-11-n156-269
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg05
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n $N --workers 2
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 2 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
```

Then the two `layer` commands the selection printed, for Evan Daniel’s driver at 156 and
180 and for grid-slack’s 0.5-degree run at 268 and 269, and the guide’s
render-and-record step.
The axis tool’s refresh had recorded the earlier witnesses’ views at 156 and 268 as
lapsed, so each selection was measured against the drawing of the new witness, and no
candidate carries the note that a run measured it against another drawing than the
tree’s (think-xs9t’s stale-view failure does not recur).
The `SETTLED` entries at 180 and 269, decided on T-174’s witnesses, are taken off.

## What They Found

[selection-adopt-2026-11-11-n156-269.md](selection-adopt-2026-11-11-n156-269.md) is the
selection’s table, and its JSON beside it the full report.
Each view is drawn at the witness’s side, admitted at row 10, and better on every goal
it changes; the figures are light, uneven and near-axis squares, angle classes and hues,
then full shared sides (house and stage), the drawing before against the view:

| n | View drawn | Goals before → after | Shared sides before → after | KKT solve below the side (row 3, held) |
| ---: | --- | --- | --- | --- |
| 156 | Evan Daniel’s same-side view | 5, 9, 1, 19, 19 → 2, 4, 0, 18, 18 | 337, 364 → 356, 368 | 2.59 × 10⁻¹² |
| 180 | Evan Daniel’s same-side view | 20, 43, 9, 25, 19 → 4, 9, 0, 8, 8 | 405, 477 → 513, 515 | 2.71 × 10⁻¹² |
| 268 | grid-slack’s 0.5-degree view | 24, 103, 18, 49, 19 → 1, 22, 0, 32, 19 | 611, 813 → 822, 828 | 3.27 × 10⁻¹² |
| 269 | grid-slack’s 0.5-degree view | 9, 28, 12, 44, 19 → 1, 0, 0, 32, 19 | 565, 709 → 646, 718 | 3.40 × 10⁻¹² |

- Grid-slack’s 1- and 5-degree runs drew the same views as its 0.5-degree run at all
  four counts.
- Evan Daniel’s certified KKT solves lie 2.59 to 3.40 × 10⁻¹² below the sides, about
  each certificate’s own contraction margin (2.42, 2.58, 3.20 and 3.24 × 10⁻¹²). They
  are held at row 3 as register candidates, not admitted, as at 172, 199 and 270; their
  registration is RV-3’s (think-ruu2, think-ikku).
- The flip record decides each new picture’s pose again (`flip_regularization --check`).

## Retained Here

| Directory or file | What |
| --- | --- |
| `adopt-2026-11-11-n156-269-grid-deg05/`, `-grid-deg1/`, `-grid-deg5/` | each run’s block, `run.json` (the 0.5-degree one the layer index’s own block), and its reports, `n-NNN/report.json.gz` |
| `adopt-2026-11-11-n156-269-evand/` | the driver’s `receipt.json` and its reports |
| `selection-adopt-2026-11-11-n156-269.json.gz`, `.md` | the selection’s report and table |

The runs cost about 2.8 CPU-minutes for grid-slack’s three runs, 8.0 CPU-minutes for the
driver (479.9 CPU seconds by its receipt) and about 1.5 minutes of wall for the
selection.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
