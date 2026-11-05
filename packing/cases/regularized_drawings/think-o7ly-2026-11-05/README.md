# Regularization Runs After the Adoption of 5 November 2026 (think-o7ly)

These are the strong generators’ runs on the witness that the adoption of 5 November
2026 wrote, under [the house rule](../../../campaign/result-import.md#the-house-rule),
after the stage 4 review of that day
([review-2026-11-05-yim-895-260.md](../../../../docs/project/reviews/review-2026-11-05-yim-895-260.md)):

| n | House | Certificate |
| ---: | --- | --- |
| 260 | T-265 | Kaelan Yim’s further arrangement of Evan Daniel’s T-257 packing (issue 895) |

The house rule regularizes each re-housed count in the pull request that adopts it.

## How They Were Run

On 5 November 2026, from about 08:56Z to 09:07Z, in the records branch
`claude/bold-ritchie-xo28us-l48` (#911), after `adopt_houses` had written the count into
the pass of 5 November, and after `build_known_best_atlas --update`,
`regularize_axis_components --update-atlas --n 260` and `default_drawings --update`,
which read it as pending.
From `packing/`, at most two processes, `nice -n 19`, on a four-core host shared with
other lanes, in run directories named as `adopt_houses` printed them but with no dot in
the grid-slack names, since a run’s id takes none (the runs were made as `grid-0.5`,
`grid-1` and `grid-5` and renamed before the selection):

```sh
P=adopt-2026-11-05-n260
python -m devtools.regularize_grid_slack --n 260 --run-dir $RUNS/$P-grid-deg05
python -m devtools.regularize_grid_slack --n 260 --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n 260 --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n 260 --workers 2
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 2 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
```

The selection chose nothing, so no `layer` command ran.
Then `render_regularized_atlas --update`, `default_drawings --update`,
`flip_regularization --update`, `regularized_drawings` and `render_results --update`.
Each grid-slack run’s `run.json` here is its block as `regularize_grid_slack.run_block`
writes it from the run’s report.

By the receipts:

- Grid-slack took 115.13, 117.12 and 128.44 seconds at 0.5, 1 and 5 degrees, the
  per-count seconds its reports record, as each run’s `run.json` keeps it; the run has
  no receipt of its own.
- Evan Daniel’s driver took 6.90 CPU seconds over 7.26 s of wall at two workers, by its
  `receipt.json`: its solve stopped at once, finding the witness not jammed.
- The selection writes no cost; it took about 3 s of wall.

That is about 6 CPU-minutes in all, under the 40 CPU-hour item cap.

## What They Decided

| n | Outcome | Drawn now |
| ---: | --- | --- |
| 260 | Decided no better (`SETTLED`): grid-slack finds no view at any of its three thresholds, its relaxed rows overlapping at the witness’s side. Evan Daniel’s regularizer finds the witness not jammed and draws no view, which a packing with contact-free squares is (rows 78, 94, 97 and 99 touch nothing, by the review) | the axis tool’s view |

The strong view of the earlier witness, grid-slack’s 0.5-degree view of T-257’s packing,
lapsed with the house; the count is decided on the new witness, so nothing is owed.
No run drew a view, so no drawing proves another bound and no register candidate arises.
The 5 November review found that the witness’s near-upright squares, each turned by
about $-2.4 \times 10^{-12}$ radians, can be set upright with the packing still fitting
at its side (its F5); no generator here drew that variant, and the record draws the
witness as it is.

## Files

- `adopt-2026-11-05-n260-evand/`: the driver’s `receipt.json` and the count’s
  `report.json.gz`.
- `adopt-2026-11-05-n260-grid-{deg05,deg1,deg5}/`: each run’s block, `run.json`, and the
  count’s `report.json.gz`.
- `selection-adopt-2026-11-05-n260.{json.gz,md}`: the selection’s report and table.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
