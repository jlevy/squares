# Regularization Runs After the Adoption of 4 November 2026 (think-ybep)

These are the strong generators’ runs on the two witnesses that the adoption of 4
November 2026 wrote, under
[the house rule](../../../campaign/result-import.md#the-house-rule), after the stage 4
review of that day
([review-2026-11-04-ozden-893-894-299-204.md](../../../../docs/project/reviews/review-2026-11-04-ozden-893-894-299-204.md)):

| n | House | Certificate |
| ---: | --- | --- |
| 204 | T-264 | Doğa Özden’s further arrangement of Evan Daniel’s T-257 packing (issue 894) |
| 299 | T-263 | Doğa Özden’s further arrangement of Evan Daniel’s T-258 packing (issue 893) |

The house rule regularizes each re-housed count in the pull request that adopts it.

## How They Were Run

On 4 November 2026, from 07:28Z to 07:51Z, in the records branch
`claude/bold-ritchie-xo28us-l36` (#897), after `adopt_houses` had written the two counts
into the pass of 4 November, and after `build_known_best_atlas --update`,
`regularize_axis_components --update-atlas --n 204 299` and `default_drawings --update`,
which read both as pending.
From `packing/`, at most two processes, `nice`, on a four-core host shared with other
lanes, in run directories named as `adopt_houses` printed them but with no dot in the
grid-slack names, since a run’s id takes none (the runs were made as `grid-0.5`,
`grid-1` and `grid-5` and renamed before the selection that was layered):

```sh
N="204 299"; P=adopt-2026-11-04-n204-299
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg05
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n $N --workers 2
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 2 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
```

then the one `layer` command the selection printed (grid-slack’s 0.5-degree run at 299),
then `render_regularized_atlas --update`, `default_drawings --update`,
`flip_regularization --update`, `regularized_drawings` and `render_results --update`.
Each grid-slack run’s `run.json` here is its block as `regularize_grid_slack.run_block`
writes it from the run’s reports.

By the receipts:

- Grid-slack took 37.83, 34.14 and 33.67 seconds at 0.5, 1 and 5 degrees, the per-count
  seconds its reports record, summed, as each run’s `run.json` keeps it; the run has no
  receipt of its own.
- Evan Daniel’s driver took 1,323.90 CPU seconds over 1,186.47 s of wall at two workers,
  by its `receipt.json`: 258.39 at 204 and 1,065.41 at 299.
- The selection writes no cost; it took about 40 s of wall at two workers.

That is about 24 CPU-minutes in all, under the 40 CPU-hour item cap.

## What They Decided

| n | Outcome | Drawn now |
| ---: | --- | --- |
| 204 | Decided no better (`SETTLED`): grid-slack finds no view at any of its three thresholds, its relaxed rows overlapping at the witness’s side. Evan Daniel’s regularizer solved the witness to an exact point 4.82e-16 below its side, held at row 3 as a register candidate | the axis tool’s view |
| 299 | Grid-slack’s 0.5-degree view at the witness’s side, admitted: fewer light, uneven and near-axis squares and angle classes than the axis tool’s view, more full shared sides on both totals. The regularizer solved the witness to an exact point 1.56e-12 below its side, held at row 3 as a register candidate | grid-slack’s 0.5-degree view |

At 204 the strong view of the earlier witness, grid-slack’s 5-degree view of T-257’s
packing, lapsed with the house; the axis tool’s view of the new witness is worse than it
on every goal of the improvement rule, and the count is decided on the new witness, so
nothing is owed. Every admitted view is at its witness’s side, so no drawing proves
another bound.
The two register candidates are smaller packings than the new houses; they
are registered and reviewed as a result of their own before any adoption (think-w64i),
as the regularization guide’s
[Register Candidates](../../../../docs/project/guides/regularization-process.md#register-candidates)
asks.

## Files

- `adopt-2026-11-04-n204-299-evand/`: the driver’s `receipt.json` and each count’s
  `report.json.gz`.
- `adopt-2026-11-04-n204-299-grid-{deg05,deg1,deg5}/`: each run’s block, `run.json`, and
  each count’s `report.json.gz`.
- `selection-adopt-2026-11-04-n204-299.{json.gz,md}`: the selection’s report and table.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
