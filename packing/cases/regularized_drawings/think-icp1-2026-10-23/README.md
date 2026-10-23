# Regularization Runs After the 23 October Adoption of T-230 (think-icp1)

These are the strong generators’ runs on the witness that the adoption pass of 23
October 2026 wrote at 303: Evan Daniel’s dilation certificate of issue #728 (T-230),
adopted as the house best packing under
[the house rule](../../../campaign/result-import.md#the-house-rule) after the
[review of 22 October 2026](../../../../docs/project/reviews/review-2026-10-22-daniel-728.md).
The house rule regularizes each re-housed count in the pull request that adopts it.
The new witness is another arrangement of Daniil Ostashev’s two-band design, with one
tilted band’s tilt reversed, found from his packing, which T-186 certified before.

## How They Were Run

On 23 October 2026, from 00:45Z to 00:49Z, in the #728 records branch
(`claude/intake-728-daniel-s303`), after `adopt_houses` had joined 303 to the pass of 23
October, and after `build_known_best_atlas --update`, `regularize_axis_components
--update-atlas --n 303` and `default_drawings --update`, which read 303 as pending.
From `packing/`, at most two processes, `nice`, on a four-core host shared with other
lanes, in run directories named as `adopt_houses` prints them but with no dot in the
grid-slack names, since a run’s id takes none:

```sh
python -m devtools.regularize_grid_slack --n 303 --run-dir $RUNS/adopt-2026-10-23-n303-grid-deg05
python -m devtools.regularize_grid_slack --n 303 --run-dir $RUNS/adopt-2026-10-23-n303-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n 303 --run-dir $RUNS/adopt-2026-10-23-n303-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/adopt-2026-10-23-n303-evand --n 303 --workers 2
python -m devtools.regularize_select --evand-run $RUNS/adopt-2026-10-23-n303-evand \
  --grid-run $RUNS/adopt-2026-10-23-n303-grid-deg05 $RUNS/adopt-2026-10-23-n303-grid-deg1 \
  $RUNS/adopt-2026-10-23-n303-grid-deg5 --workers 2 \
  --output $RUNS/adopt-2026-10-23-n303-selection.json \
  --markdown $RUNS/adopt-2026-10-23-n303-selection.md
```

Grid-slack took 18.5, 15.7 and 15.9 CPU seconds at 0.5, 1 and 5 degrees, as their
reports record. Evan Daniel’s driver took 50.3 CPU seconds over 92.8 s of wall at two
workers. The selection took 53 s of wall.
That is about 2 CPU-minutes in all, well under the 40 CPU-hour item cap.
The same commands had run on 22 October, before the adoption, on a copy of this witness
built by `upper_bound_houses`’ own house builder and serialized as the atlas serializes
it: the witness the adoption wrote is byte-identical to it, and those runs found the
same.
They were run again on the adopted witness so that each record reads the case’s new
upper bound and drawing; the earlier runs are not retained.
No `layer` command followed, since the selection chose no view.
Then `render_regularized_atlas --update`, `regularized_drawings` and `default_drawings
--update` recorded the decision.

## What They Decided

| n | Outcome | Drawn now |
| --- | --- | --- |
| 303 | No view is drawn. Evan Daniel’s regularizer finds the witness not first-order jammed and yields no view (row 1). Grid-slack’s views at 0.5, 1 and 5 degrees are one view at the witness’s side that straightens the witness’s 15 near-upright squares: 0 near-axis squares against 2, 40 angle classes against 42, and house and stage sides 766 / 782 against 758 / 776 for the axis tool’s view of the new witness, but 13 light squares against 12. A square’s contact count falls while no total does, so each goes to review at row 7 (think-ykgh, the owner’s). Settled in `default_drawings.SETTLED` | the axis tool’s view |

`default_drawings --compare` against `main`’s record (`fcf2f96a5`):

- 303: the axis tool’s view of T-186 (15 uneven, 0 near-axis, 808 full shared sides),
  decided no better, gives way to the axis tool’s view of T-230 (45 uneven, 2 near-axis,
  758), decided no better.
  No strong view gives way: the count was drawn by the axis tool before and after, and
  the house rule keeps the smaller packing.

`SETTLED`’s entry at 303, decided on T-186’s witness by the runs of 16 October, is made
again on T-230’s witness, owing the owner’s row-7 review (think-ykgh).
Until a review record admits grid-slack’s view, the axis tool’s view stays drawn, as at
229 on 20 October. No view lies below the witness’s side, so there is no register
candidate.

## Files

- `adopt-2026-10-23-n303-evand/`: the driver’s `receipt.json` and its `report.json.gz`
  for 303.
- `adopt-2026-10-23-n303-grid-{deg05,deg1,deg5}/`: each run’s block, `run.json`, built
  by `regularize_grid_slack.run_block` from its report, and its `report.json.gz`.
- `selection-adopt-2026-10-23-n303.json.gz` and `.md`: the selection’s report and table.
- `review-303/`: grid-slack’s 0.5-degree drawing at 303, for the owner’s review.

No views or solves are kept; the layer holds the axis tool’s view.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
