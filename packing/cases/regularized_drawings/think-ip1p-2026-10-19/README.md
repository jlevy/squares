# Regularization Runs for 155, 229, 236 and 271 After the 19 October Adoption (think-ip1p)

These are the strong generators’ runs on the four witnesses that the adoption of 19
October 2026 wrote: Evan Daniel’s certificates T-197 at 155, T-199 at 229, T-218 at 236
and T-219 at 271, adopted under
[the house rule](../../../campaign/result-import.md#the-house-rule) after the
[review of 19 October 2026](../../../../docs/project/reviews/review-2026-10-19-upper-bound-imports-659-664-669-674.md).
The house rule regularizes each re-housed count in the pull request that adopts it.

## How They Were Run

On 19 October 2026, from 21:30Z to 22:54Z, in the adoption’s branch
(`claude/intake-2026-10-19-evand-singles`), after `adopt_houses`,
`build_known_best_atlas --update --n 155 229 236 271`,
`regularize_axis_components --update-atlas --n 155 229 236 271` and
`default_drawings --update`, which read all four counts as pending.
From `packing/`, at most two processes, `nice -n 10`, on a four-core host shared with
other lanes at load averages of 15 to 30:

```sh
python -m devtools.regularize_evand run --run-dir $RUNS/adopt-2026-10-19-n155-271-evand --n 155 229 236 271 --workers 1
python -m devtools.regularize_grid_slack --n 155 229 236 271 --run-dir $RUNS/adopt-2026-10-19-n155-271-grid-deg05
python -m devtools.regularize_grid_slack --n 155 229 236 271 --run-dir $RUNS/adopt-2026-10-19-n155-271-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n 155 229 236 271 --run-dir $RUNS/adopt-2026-10-19-n155-271-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_select --evand-run $RUNS/adopt-2026-10-19-n155-271-evand \
  --grid-run $RUNS/adopt-2026-10-19-n155-271-grid-deg05 $RUNS/adopt-2026-10-19-n155-271-grid-deg1 \
  $RUNS/adopt-2026-10-19-n155-271-grid-deg5 --workers 2 \
  --output $RUNS/adopt-2026-10-19-n155-271-selection.json \
  --markdown $RUNS/adopt-2026-10-19-n155-271-selection.md
```

Evan Daniel’s driver took 1,199 CPU seconds (3,117 s of wall); grid-slack took 1,194,
854 and 710 CPU seconds at 0.5, 1 and 5 degrees, as their reports record; the selection
took 29 minutes of wall at two workers.
Then the `layer` commands the selection printed admitted the chosen views, and
`render_regularized_atlas --update`, `default_drawings --update`, `regularized_drawings`
and `render_results --update` recorded them.
The grid-slack runs ran in directories named `-grid-0.5`, `-grid-1` and `-grid-5`, the
names the selection report still prints.
A run’s id takes no dot, so they are kept as `-grid-deg05`, `-grid-deg1` and
`-grid-deg5`, and the 155 view was laid again from the renamed half-degree run; only its
run id changed.

## What They Decided

| n | House | Outcome | Drawn now |
| --- | --- | --- | --- |
| 155 | T-197 | grid-slack’s 0.5-degree view admitted at row 10: 1 light, 3 uneven, 0 near-axis, 20 classes, 19 hues, house sides 362, better than the axis tool’s view on uneven, near-axis, classes and house sides | grid-slack 0.5 |
| 229 | T-199 | Evan Daniel’s driver draws no view (the solve of the dilation certificate is not jammed). grid-slack’s views at 0.5, 1 and 5 degrees are better than the axis tool’s view on every goal (1 light, 4 uneven, 0 near-axis, 13 classes against 25 / 55 / 24 / 32), but two squares’ contact counts fall while no total does: row 7, for the owner’s review. Settled in `default_drawings.SETTLED` | the axis tool’s view, until a review record admits one |
| 236 | T-218 | Evan Daniel’s same-side view admitted at row 10: 1 light, 2 uneven, 0 near-axis, 6 classes, 6 hues, better on every goal | Evan Daniel’s view |
| 271 | T-219 | Evan Daniel’s same-side view admitted at row 10: 7 light, 12 uneven, 0 near-axis, 21 classes, 19 hues, better than the axis tool’s view on uneven, near-axis, classes and both totals | Evan Daniel’s view |

At 271 the strong view the earlier house drew (grid-slack’s of T-186, 10 uneven squares)
gives way to Evan Daniel’s view of the new house, with two more uneven squares; the
house moved to a packing $4.46 \times 10^{-5}$ smaller, and the owner’s rule adopts the
smaller packing and draws the best view of it.
At 229 the earlier house was the catalogue’s packing, regular as published; the new
house’s best adoptable drawing is the axis tool’s view until the owner reviews
grid-slack’s. [review-229/](review-229/) keeps grid-slack’s 0.5-degree drawing of it for
that review.

## Files

- `adopt-2026-10-19-n155-271-evand/`: the driver’s `receipt.json` and each count’s
  `report.json.gz`.
- `adopt-2026-10-19-n155-271-grid-{deg05,deg1,deg5}/`: each run’s block, `run.json`,
  built by `regularize_grid_slack.run_block` from its reports, and each count’s
  `report.json.gz`.
- `selection-adopt-2026-10-19-n155-271.json.gz` and `.md`: the selection’s report and
  table.
- `review-229/`: grid-slack’s 0.5-degree drawing at 229, for the owner’s review.

No views, solves or manifests are kept; the layer holds the admitted views.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
