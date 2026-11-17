# Regularization Runs After the Adoption of Issue 914 (think-lrj4)

These are the strong generators’ runs on the seven witnesses that the adoption of Evan
Daniel’s issue 914 packings wrote, under
[the house rule](../../../campaign/result-import.md#the-house-rule), after the stage 4
review of 5 November 2026
([review-2026-11-05-evand-914-seven.md](../../../../docs/project/reviews/review-2026-11-05-evand-914-seven.md)):

| n | House | Replaces | Adopted |
| ---: | --- | --- | --- |
| 175 | T-267 | T-186 | 5 November 2026 |
| 204 | T-268 | T-264 | 5 November 2026 |
| 260 | T-269 | T-265 | 6 November 2026 |
| 268 | T-270 | T-242 | 5 November 2026 |
| 293 | T-271 | T-257 | 5 November 2026 |
| 303 | T-272 | T-240 | 5 November 2026 |
| 304 | T-273 | T-242 | 5 November 2026 |

260 moved a day after the others: the pass of 5 November had already moved it to T-265,
and a day’s prior-state archive holds one record a count, so the pass of 6 November
adopted T-269 there, in the same pull request.
Its witness is the same either way.

## How They Were Run

In the records branch `claude/bold-ritchie-xo28us-l51` (#916), after `adopt_houses` had
written the seven counts, and after `build_known_best_atlas --update`,
`regularize_axis_components --update-atlas --n 175 204 260 268 293 303 304` and
`default_drawings --update`, which read all seven as pending.
From `packing/`, at most two processes, `nice -n 19`, on a four-core host shared with
other lanes, in run directories named as `adopt_houses` printed them but with no dot in
the grid-slack names, since a run’s id takes none (the runs were made as `grid-0.5`,
`grid-1` and `grid-5` and renamed before the selection):

```sh
N="175 204 260 268 293 303 304"; P=adopt-2026-11-05-n175-304
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg05
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n $N --workers 2
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 2 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
```

Grid-slack ran on 5 November 2026 from 23:29Z to 23:44Z. The driver’s first run was
stopped at 304, its last count, by a restart of the container shortly after midnight; it
wrote no receipt and is not kept.
The driver ran again on all seven counts from 00:07Z to 00:24Z on 6 November 2026, after
the pass of 6 November had adopted 260, and the selection followed it.

Then the three `layer` commands the selection printed: the driver’s run, reclassified on
a copy with `--refresh-bounds`, at 175, 204 and 268 (`--exclude 293`), grid-slack’s
0.5-degree run at 260 and its 5-degree run at 303. Then
`render_regularized_atlas --update`, `default_drawings --update`,
`flip_regularization --update`, `regularized_drawings` and `render_results --update`.
Each grid-slack run’s `run.json` here is its block: the layer’s index block for the 0.5
and 5-degree runs, and `regularize_grid_slack.run_block`’s, built from the run’s
reports, for the 1-degree run, which the index does not hold.

By the receipts:

- Grid-slack took 419.82, 451.10 and 443.11 seconds at 0.5, 1 and 5 degrees, the
  per-count seconds its reports record, summed, as each run’s `run.json` keeps it; the
  run has no receipt of its own.
- Evan Daniel’s driver took 1,756.31 CPU seconds over 1,003.92 s of wall at two workers,
  by its `receipt.json`; the stopped first run spent about as long again up to 304 and
  has no receipt.
- The selection writes no cost.
  It took 482 s of wall at two workers, so at most 16.1 CPU-minutes.

That is about 67 CPU-minutes in all (3,070 receipt seconds and at most 964 for the
selection), and about 95 with the stopped run, under the 40 CPU-hour item cap.

## What They Decided

| n | Outcome | Drawn now |
| ---: | --- | --- |
| 175 | Evan Daniel’s regularizer solves the witness to a certified KKT local minimum and draws its view at the witness’s side, admitted at row 10: 8 light, 19 uneven and no near-axis squares, 3 angle classes and 3 hues, 477 full shared sides, against the axis tool’s 22, 58, 22, 43, 19 and 292 and 422. Grid-slack’s views tie it on the first three and have more classes and hues | the regularizer’s view |
| 204 | The regularizer’s view at the witness’s side, admitted: 14 uneven and no near-axis squares, 19 classes, 517 and 535 full shared sides, against the axis tool’s 17, 2, 26 and 510 and 531. Grid-slack’s views have more classes (24) | the regularizer’s view |
| 260 | Grid-slack’s 0.5-degree view, admitted: 3 light, 9 uneven and no near-axis squares, 556 and 634 full shared sides, against the axis tool’s 26, 59, 14 and 402 and 582; its 1 and 5-degree views are the same. The regularizer’s solve failed, as the issue’s own exact solver did not converge here | grid-slack’s 0.5-degree view |
| 268 | The regularizer’s view at the witness’s side, admitted: no light, uneven or near-axis square, 12 classes and 12 hues, 697 and 727 full shared sides, against the axis tool’s 13, 47, 16, 41, 19 and 547 and 636. Grid-slack’s 1 and 5-degree views have more classes and fewer shared sides; its 0.5-degree view goes to review at row 7 | the regularizer’s view |
| 293 | Decided no better (`SETTLED`): every view, the regularizer’s certified KKT view at the witness’s side and grid-slack’s at all three thresholds, is admitted at row 10 but draws more light and uneven squares than the axis tool’s view of this witness (11 and 26 against 9 and 24), though fewer classes and hues | the axis tool’s view |
| 303 | Grid-slack’s 5-degree view, admitted: 1 light, 2 uneven and no near-axis squares, 52 classes, 756 and 798 full shared sides, against the axis tool’s 1, 4, 1, 54 and 745 and 789; its 0.5 and 1-degree views have one class more and fewer shared sides. The regularizer’s placement was infeasible and draws no view | grid-slack’s 5-degree view |
| 304 | Decided no better (`SETTLED`): the regularizer’s certified KKT view at the witness’s side is refused at row 7, its house and stage totals of shared sides falling (703 and 720 against 759 and 796); grid-slack’s views at all three thresholds go to review at row 7, 50 per-square contact counts falling while no total does, and have more uneven squares than the axis tool’s view (49 against 40) | the axis tool’s view |

Every admitted view is at its witness’s side, so no drawing proves another bound, and no
view lies below a house: there is no register candidate.
The strong views of the earlier witnesses lapsed with the houses.
`default_drawings --compare` against `main`’s record lists, at 175, 268, 293 and 303,
the earlier witness’s strong view giving way to a drawing worse on some goal; each is a
drawing of another packing, and each count is decided here on its new witness, so
nothing is owed.

Evan Daniel’s release offers his own regularized views at six of the counts (the
[views packet](../../../resources/web/evand-issue914-views-2026-11-05/README.md)).
Whether one is drawn is the generators’ to decide, as at 182 (think-2lzo); measured pose
by pose against his views (`views-against-author/`, `devtools.measure_identity`), the
regularizer’s views the layer drew reproduce his at 175 (every square within $10^{-9}$),
and at 268 but for one square moved $7.3 \times 10^{-4}$. At 204 the drawn view is his
after a half turn, with 33 squares moved beyond a hundredth and one by 0.344, another
regularization of the same packing.

## Files

- `adopt-2026-11-05-n175-304-evand/`: the driver’s `receipt.json` and each count’s
  `report.json.gz`.
- `adopt-2026-11-05-n175-304-grid-{deg05,deg1,deg5}/`: each run’s block, `run.json`, and
  each count’s `report.json.gz`.
- `selection-adopt-2026-11-05-n175-304.{json.gz,md}`: the selection’s report and table.
- `views-against-author/identity-n{175,204,268}.json`: the regularizer’s view at each
  count, as its run wrote it (`regularize.cert`), against Evan Daniel’s own view there.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
