# Regularization Runs After the Adoption of T-242 at 304 (think-hx0e)

These are the strong generators’ runs on the witness that the adoption pass of 25
October 2026 wrote at 304: Evan Daniel’s certificate `s304_pub.cert` at
`evand/square-packing@8a8879a` (T-242), adopted as the house best packing under
[the house rule](../../../campaign/result-import.md#the-house-rule) after the
[review of 24 October 2026](../../../../docs/project/reviews/review-2026-10-24-couzo-evand-n268-n304.md).
The house rule regularizes each re-housed count in the pull request that adopts it.
The new witness is Daniel’s exact descent of the packing Francisco Couzo certified at
304 (T-241), which Couzo’s index credits to Kirill Tymchishin’s Kaggle notebook, and
another arrangement than T-186’s, the house it replaces.

T-242’s certificate at 268 is not adopted here: the same pass adopts T-240 there, and
one day’s archive holds one prior state a count, so 268 is staged for the pass’s next
pull request, on or after 26 October, under the bead that adopts it
(`select_houses.PENDING_ADOPTION`, think-3anz), and its runs are owed there.

## How They Were Run

On 25 October 2026, from 01:08Z to 01:16Z, in the records branch
`claude/intake-2026-10-24-t241-t242-review`, after `adopt_houses` had written 304 into
the pass of 25 October, and after `build_known_best_atlas --update --n 304`,
`regularize_axis_components --update-atlas --n 304` and `default_drawings --update`,
which read 304 as pending.
From `packing/`, at most two processes, `nice`, on a four-core host shared with other
lanes, in run directories named as `adopt_houses` prints them but with no dot in the
grid-slack names, since a run’s id takes none:

```sh
python -m devtools.regularize_grid_slack --n 304 --run-dir $RUNS/adopt-2026-10-25-n304-grid-deg05
python -m devtools.regularize_grid_slack --n 304 --run-dir $RUNS/adopt-2026-10-25-n304-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n 304 --run-dir $RUNS/adopt-2026-10-25-n304-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/adopt-2026-10-25-n304-evand --n 304 --workers 1
python -m devtools.regularize_select --evand-run $RUNS/adopt-2026-10-25-n304-evand \
  --grid-run $RUNS/adopt-2026-10-25-n304-grid-deg05 $RUNS/adopt-2026-10-25-n304-grid-deg1 \
  $RUNS/adopt-2026-10-25-n304-grid-deg5 --workers 2 \
  --output $RUNS/adopt-2026-10-25-n304-selection.json \
  --markdown $RUNS/adopt-2026-10-25-n304-selection.md
```

Grid-slack took 35.7, 42.2 and 40.1 CPU seconds by its reports at 0.5, 1 and 5 degrees
(about 98 s of user CPU in all).
Evan Daniel’s driver took 208 CPU seconds over 297 s of wall at one worker: 186 s to
solve and 94 s to regularize.
The selection took 104 s of wall at two workers.
That is about 7 CPU-minutes in all, well under the 40 CPU-hour item cap.
No view was admitted, so no `layer` step ran; `default_drawings --update`,
`render_regularized_atlas --update`, `flip_regularization --update`,
`regularized_drawings` and `render_results --update` recorded the decision.

## What They Decided

| n | Outcome | Drawn now |
| --- | --- | --- |
| 304 | Grid-slack’s view, the same at all three thresholds, is at the witness’s side, one to one with it, largest move 0.013. Evan Daniel’s regularizer solves the witness to a certified KKT local minimum; its exact solve lies about $1.8 \times 10^{-19}$ below the side, within the source’s own relative padding of $10^{-20}$, and its view is drawn at the side, one to one, largest move 0.58. Both go to review (row 7: 14 and 36 squares’ contact counts fall while no total does), and both draw more light squares than the axis tool’s view of the witness (4 and 5 against 2), with fewer uneven and near-axis squares (14 against 18, none against 9). No view is below the house, so there is no register candidate | the axis tool’s view, decided no better |

`default_drawings --compare` against `main`’s record: 304 was drawn by the axis tool’s
view of T-186’s witness, decided no better (`SETTLED`), and is now drawn by the axis
tool’s view of T-242’s witness, decided no better, with 18 uneven and 9 near-axis
squares and 810 full shared sides against 4, 5 and 791. No strong view gives way to a
worse drawing. `SETTLED`’s entry at 304 is made again on the new witness.

**The review queue.** The row-7 views at 304, grid-slack’s and the regularizer’s, are
listed for the owner in the adopting pull request; none is drawn, and the count is
settled on the axis tool’s view meanwhile.

## Files

- `adopt-2026-10-25-n304-evand/`: the driver’s `receipt.json` and its `report.json.gz`
  for 304.
- `adopt-2026-10-25-n304-grid-{deg05,deg1,deg5}/`: each run’s block, `run.json`, built
  by `regularize_grid_slack.run_block` from its report, and its `report.json.gz` for
  304\.
- `selection-adopt-2026-10-25-n304.json.gz` and `.md`: the selection’s report and table;
  the report keeps the run directories as run.

No views or solves are kept.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
