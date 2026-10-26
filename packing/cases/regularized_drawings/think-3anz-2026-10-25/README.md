# Regularization Runs After the Adoption of T-242 at 268 (think-3anz)

These are the strong generators’ runs on the witness that the adoption pass of 26
October 2026 writes at 268: Evan Daniel’s certificate `s268_lightning.cert` at
`evand/square-packing@8a8879a` (T-242), adopted as the house best packing under
[the house rule](../../../campaign/result-import.md#the-house-rule) after the
[review of 24 October 2026](../../../../docs/project/reviews/review-2026-10-24-couzo-evand-n268-n304.md).
The house rule regularizes each re-housed count in the pull request that adopts it.
The new witness is Daniel’s exact descent of Vladislav Lavrentev’s public Kaggle
packing, which the certificate is to $1.41 \times 10^{-4}$: one arrangement with T-240’s
packing, the house it replaces, and another placement of it, $4.48 \times 10^{-12}$
lower.

The pass of 25 October adopted T-240 at 268 and T-242 at 304. One day’s archive holds
one prior state a count, so 268 was staged for the pass’s next pull request
(`select_houses.PENDING_ADOPTION`, think-3anz), which this is, dated 26 October.

## How They Were Run

On 25 October 2026, from 04:21Z to 04:26Z, in the records branch
`claude/intake-2026-10-26-t242-at-268`, after `adopt_houses` had written 268 into the
pass of 26 October, and after `build_known_best_atlas --update --n 268`,
`regularize_axis_components --update-atlas --n 268` and `default_drawings --update`,
which read 268 as pending.
From `packing/`, at most two processes, `nice`, on a four-core host shared with other
lanes, in run directories named as `adopt_houses` prints them but with no dot in the
grid-slack names, since a run’s id takes none:

```sh
python -m devtools.regularize_grid_slack --n 268 --run-dir $RUNS/adopt-2026-10-26-n268-grid-deg05
python -m devtools.regularize_grid_slack --n 268 --run-dir $RUNS/adopt-2026-10-26-n268-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n 268 --run-dir $RUNS/adopt-2026-10-26-n268-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/adopt-2026-10-26-n268-evand --n 268 --workers 1
python -m devtools.regularize_select --evand-run $RUNS/adopt-2026-10-26-n268-evand \
  --grid-run $RUNS/adopt-2026-10-26-n268-grid-deg05 $RUNS/adopt-2026-10-26-n268-grid-deg1 \
  $RUNS/adopt-2026-10-26-n268-grid-deg5 --workers 2 \
  --output $RUNS/adopt-2026-10-26-n268-selection.json \
  --markdown $RUNS/adopt-2026-10-26-n268-selection.md
python -m devtools.regularize_evand layer --run-dir $SCRATCH --repo-root .. \
  --grid-run $RUNS/adopt-2026-10-26-n268-grid-deg1 --grid-counts 268
```

Grid-slack took 9.05, 9.37 and 9.16 CPU seconds by its reports at 0.5, 1 and 5 degrees
(about 34 s of user CPU in all).
Evan Daniel’s driver took 132 CPU seconds over 134 s of wall at one worker: 88 s to
solve and 24 s to regularize.
The selection took 24 s of wall at two workers, and the layer 12 s. That is about 4
CPU-minutes in all, well under the 40 CPU-hour item cap.
Then `render_regularized_atlas --update`, `default_drawings --update`,
`flip_regularization --update`, `regularized_drawings` and `render_results --update`
recorded the decision.

## What They Decided

| n | Outcome | Drawn now |
| --- | --- | --- |
| 268 | Grid-slack’s view at 1 degree is admitted (row 10): at the witness’s side, one to one with it, largest move 0.384, better than the axis tool’s view of the new witness on every goal: light, uneven and near-axis squares 18, 30 and 23 to 5, 19 and 0, angle classes and hues 32 and 19 to 12 and 12, sides 611 / 721 to 751 / 759. The 0.5 and 5 degree views are admissible too, and the selection takes the 1 degree view over them: the 0.5 degree view has 6 light squares and 15 angle classes, and the 5 degree view 21 uneven squares. Evan Daniel’s regularizer solves the witness to a certified KKT local minimum; its exact solve lies about $1.7 \times 10^{-19}$ below the side, within the source’s own relative padding of $10^{-20}$, and its view is drawn at the side, one to one, largest move 0.384. That view goes to review (row 7: two squares’ contact counts fall while no total does). No view is below the house, so there is no register candidate | grid-slack’s view |

`default_drawings --compare` against `main`’s record: 268 was drawn by grid-slack’s view
of T-240 and is now drawn by grid-slack’s view of T-242, regularized, with the same 19
uneven and no near-axis squares and the same 751 full shared sides; the new drawing has
12 angle classes and hues against 9, and 759 stage sides against 753. The table names
the strong view that gives way as worse on angle classes and hues, and does not mark it,
since the count is regularized.

**The review queue.** Evan Daniel’s same-side view at 268 (row 7), with 4 angle classes
and 767 house sides against the drawn view’s 12 and 751, is listed for the owner in the
adopting pull request; it is not drawn, and the count is drawn by grid-slack’s view
meanwhile.

**think-20oj.** The regularizer’s view that #794’s runs found at 268, a certified KKT
local minimum of T-240’s witness at exactly T-242’s side, is no longer below the house
best packing: the house is now T-242, at that side.
This pull request’s run on T-242’s witness solves it to a KKT point within the source’s
padding and draws its view at the house’s side.

## Files

- `adopt-2026-10-26-n268-evand/`: the driver’s `receipt.json` and its `report.json.gz`
  for 268.
- `adopt-2026-10-26-n268-grid-{deg05,deg1,deg5}/`: each run’s block, `run.json`, built
  by `regularize_grid_slack.run_block` from its report, and its `report.json.gz` for
  268\.
- `selection-adopt-2026-10-26-n268.json.gz` and `.md`: the selection’s report and table;
  the table’s run directories are written as `$RUNS` here, and the report keeps them as
  run.

No views or solves are kept; the layer holds grid-slack’s view.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
