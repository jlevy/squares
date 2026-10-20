# Regularization Runs for 204 and 260 After the 20 October Adoption (think-xu4d)

These are the strong generators’ runs on the two witnesses that the adoption of 20
October 2026 wrote: Francisco Couzo’s certificates of issue 678 (T-223) at 204 and 260,
adopted as the house best packings under
[the house rule](../../../campaign/result-import.md#the-house-rule) after the
[review of 20 October 2026](../../../../docs/project/reviews/review-2026-10-20-upper-bound-imports-678.md).
The house rule regularizes each re-housed count in the pull request that adopts it.

## How They Were Run

On 20 October 2026, from 23:01Z to 23:14Z, in the adoption’s branch
(`claude/intake-2026-10-20-couzo-678-stage4`), after `adopt_houses`,
`build_known_best_atlas --update --n 204 260`,
`regularize_axis_components --update-atlas --n 204 260` and `default_drawings --update`,
which read both counts as pending.
From `packing/`, at most two processes, `nice -n 10`, on a four-core host shared with
other lanes at load averages of 17 to 24:

```sh
python -m devtools.regularize_grid_slack --n 204 260 --run-dir $RUNS/adopt-2026-10-20-n204-260-grid-deg05
python -m devtools.regularize_grid_slack --n 204 260 --run-dir $RUNS/adopt-2026-10-20-n204-260-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n 204 260 --run-dir $RUNS/adopt-2026-10-20-n204-260-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/adopt-2026-10-20-n204-260-evand --n 204 260 --workers 2
python -m devtools.regularize_select --evand-run $RUNS/adopt-2026-10-20-n204-260-evand \
  --grid-run $RUNS/adopt-2026-10-20-n204-260-grid-deg05 $RUNS/adopt-2026-10-20-n204-260-grid-deg1 \
  $RUNS/adopt-2026-10-20-n204-260-grid-deg5 --workers 2 \
  --output $RUNS/adopt-2026-10-20-n204-260-selection.json \
  --markdown $RUNS/adopt-2026-10-20-n204-260-selection.md
```

The first two grid-slack runs ran side by side.
Grid-slack took 65.1, 65.5 and 42.5 CPU seconds at 0.5, 1 and 5 degrees, as their
reports record; Evan Daniel’s driver took 222.2 CPU seconds (497 s of wall at two
workers); the selection took 97 s of wall at two workers.
That is about 7 CPU-minutes in all, under the 5 to 25 a count the runbook prices.
The run directories carry no dot, so each grid-slack run’s id is its directory’s name.
Then the `layer` command the selection printed admitted the one chosen view, and
`default_drawings --update`, `render_regularized_atlas --update` and
`regularized_drawings` recorded it.

## What They Decided

| n | Outcome | Drawn now |
| --- | --- | --- |
| 204 | grid-slack’s 0.5-degree view admitted at row 10 at the witness’s side: 6 light, 34 uneven, 6 near-axis squares, 21 classes, 19 hues, house and stage sides 497 / 549, against the axis tool’s view’s 16 / 62 / 11, 26, 19 and 414 / 513; it moves every square one to one, by at most 0.442. The views at 1 and 5 degrees are the same. Evan Daniel’s solved view lies $1.39 \times 10^{-9}$ below the witness’s side: a register candidate (row 3), not drawn | grid-slack 0.5 |
| 260 | No view is admitted. Evan Daniel’s same-side view (2 light, 16 uneven, 0 near-axis, house sides 780) and grid-slack’s views (2 / 28 / 0, 769) each improve on the axis tool’s view (5 / 36 / 0, 736) on light and uneven squares and both totals, but some squares’ contact counts fall while no total does, 29 for his and 2 for grid-slack’s: row 7, for the owner’s review (think-fltj). His solved view lies $2.51 \times 10^{-11}$ below the witness’s side: a register candidate (row 3), not drawn. Settled in `default_drawings.SETTLED` | the axis tool’s view, until a review record admits one |

At 204 the strong view the earlier house drew (Evan Daniel’s of T-186, 19 uneven and no
near-axis squares) gives way to grid-slack’s view of the new house best packing, with 34
uneven and 6 near-axis squares; the house moved to a packing $2.04 \times 10^{-5}$
smaller, and the owner’s rule adopts the smaller packing and draws the best view of it.
At 260 the earlier house best packing was the catalogue’s packing, regular as published.
The two register candidates are smaller packings by the regularization policy’s row 3:
each is registered as a result before any drawing takes it, which this pass does not do.

## Files

- `adopt-2026-10-20-n204-260-evand/`: the driver’s `receipt.json` and each count’s
  `report.json.gz`.
- `adopt-2026-10-20-n204-260-grid-{deg05,deg1,deg5}/`: each run’s block, `run.json`,
  built by `regularize_grid_slack.run_block` from its reports, and each count’s
  `report.json.gz`.
- `selection-adopt-2026-10-20-n204-260.json.gz` and `.md`: the selection’s report and
  table.

No views, solves or drawings are kept; the layer holds the admitted view.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
