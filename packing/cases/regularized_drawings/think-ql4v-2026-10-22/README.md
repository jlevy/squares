# Regularization Runs After the 22 October Adoption of T-225 (think-ql4v)

These are the strong generators’ runs on the witnesses that the adoption of 22 October
2026 wrote: Evan Daniel’s display-regularized views of 20 October (T-225), adopted as
the house best packings under
[the house rule](../../../campaign/result-import.md#the-house-rule) after the
[review of 21 October 2026](../../../../docs/project/reviews/review-2026-10-21-evand-regularized-views.md).
The house rule regularizes each re-housed count in the pull request that adopts it.
Each new witness is itself Evan Daniel’s regularization of the packing it credits:
Francisco Couzo’s #678 packing (T-223) at 204 and 260, and his own #674 packing (T-199)
at 229.

## How They Were Run

On 22 October 2026, from 00:56Z to 01:30Z, in the adoption’s branch
(`claude/stoic-thompson-ku09fw`), after `adopt_houses`,
`build_known_best_atlas --update --n 204 229 260`,
`regularize_axis_components --update-atlas --n 204 229 260` and
`default_drawings --update`, which read all three counts as pending.
From `packing/`, at most two processes, `nice`, on a four-core host shared with another
lane:

```sh
python -m devtools.regularize_grid_slack --n 204 229 260 --run-dir $RUNS/adopt-2026-10-22-n204-260-grid-deg05
python -m devtools.regularize_grid_slack --n 204 229 260 --run-dir $RUNS/adopt-2026-10-22-n204-260-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n 204 229 260 --run-dir $RUNS/adopt-2026-10-22-n204-260-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/adopt-2026-10-22-n204-260-evand --n 204 229 260 --workers 2
python -m devtools.regularize_select --evand-run $RUNS/adopt-2026-10-22-n204-260-evand \
  --grid-run $RUNS/adopt-2026-10-22-n204-260-grid-deg05 $RUNS/adopt-2026-10-22-n204-260-grid-deg1 \
  $RUNS/adopt-2026-10-22-n204-260-grid-deg5 --workers 2 \
  --output $RUNS/adopt-2026-10-22-n204-260-selection.json \
  --markdown $RUNS/adopt-2026-10-22-n204-260-selection.md
```

The first two grid-slack runs ran side by side.
Grid-slack took 51.7, 53.0 and 46.2 CPU seconds at 0.5, 1 and 5 degrees, as their
reports record. Evan Daniel’s driver took 2,066 CPU seconds over 1,801 s of wall at two
workers: 204 and 260 finished in about three minutes each, and 229 ran to the driver’s
600-second timeout on its solve and each retry (row 1, no view).
The selection took 85 s of wall at two workers.
That is about 37 CPU-minutes in all, most of it the 229 timeouts, under the 40 CPU-hour
item cap. The run directories carry no dot, so each grid-slack run’s id is its
directory’s name. Then the `layer` command the selection printed admitted the one chosen
view, and `render_regularized_atlas --update`, `default_drawings --update` and
`regularized_drawings` recorded it.

## What They Decided

| n | Outcome | Drawn now |
| --- | --- | --- |
| 204 | No view is drawn. Grid-slack’s views at 0.5, 1 and 5 degrees draw no change (row 10, no square moved beyond $10^{-16}$). Evan Daniel’s solved view, with the same light, uneven and near-axis squares (6 / 34 / 6) and sides (509 / 555), lies $8.91 \times 10^{-12}$ below the witness’s side: a register candidate (row 3), not drawn. Settled in `default_drawings.SETTLED` | the house drawing |
| 229 | Grid-slack’s 0.5-degree view admitted at row 10 at the witness’s side: 3 light, 26 uneven, 0 near-axis squares, 12 classes, 12 hues, house and stage sides 639 / 657, against the house drawing’s 637 / 657, the only goal it improves. The views at 1 and 5 degrees are the same. Evan Daniel’s driver timed out (row 1, no view) | grid-slack 0.5 |
| 260 | No view is drawn. Evan Daniel’s same-side and solved views and grid-slack’s views each draw no change (2 light, 16 uneven, 0 near-axis squares, 780 / 780 sides). Settled in `default_drawings.SETTLED` | the house drawing |

`default_drawings --compare` against `main`’s record (`d7923b8d`):

- 204: grid-slack’s half-degree view of T-223 (34 uneven, 6 near-axis, 497 full shared
  sides) gives way to the house drawing of T-225 (34 uneven, 6 near-axis, 509), decided
  no better.
- 229: the axis tool’s view of T-199 (55 uneven, 24 near-axis, 455), decided no better,
  gives way to grid-slack’s view of T-225 (26 uneven, 0 near-axis, 639), regularized.
- 260: the axis tool’s view of T-223 (36 uneven, 0 near-axis, 736), decided no better,
  gives way to the house drawing of T-225 (16 uneven, 0 near-axis, 780), decided no
  better.

No strong view gives way to a worse drawing on a goal of the improvement rule.
`SETTLED`’s entries at 229 (owed to think-cyeo, the owner’s row-7 review of grid-slack’s
views of T-199) and 260 (owed to think-fltj, the same for T-223) were decided on the
earlier witnesses: 229 is regularized now and 260 settled again, owing nothing.
The register candidate at 204 is a smaller packing by the regularization policy’s row 3,
to be registered as a result before any drawing takes it.

## Files

- `adopt-2026-10-22-n204-260-evand/`: the driver’s `receipt.json` and each count’s
  `report.json.gz`.
- `adopt-2026-10-22-n204-260-grid-{deg05,deg1,deg5}/`: each run’s block, `run.json`,
  built by `regularize_grid_slack.run_block` from its reports, and each count’s
  `report.json.gz`.
- `selection-adopt-2026-10-22-n204-260.json.gz` and `.md`: the selection’s report and
  table.

No views, solves or drawings are kept; the layer holds the admitted view.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
