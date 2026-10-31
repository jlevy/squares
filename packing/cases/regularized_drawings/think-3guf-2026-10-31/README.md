# Regularization Runs After the Adoptions of 31 October 2026 (think-3guf)

These are the strong generators’ runs on the eight witnesses that the adoption pass of
31 October 2026 wrote, under
[the house rule](../../../campaign/result-import.md#the-house-rule), after the stage 4
reviews of that day:

| n | House | Certificate |
| ---: | --- | --- |
| 130 | T-259 | Mykhailo Polkovskyi’s re-solve of Francisco Couzo’s issue 843 packing (issue 846) |
| 172, 204, 260, 293 | T-257 | Evan Daniel’s certificates of issue 845 |
| 232, 307 | T-256 | Francisco Couzo’s certificates of issue 844 |
| 299 | T-258 | Evan Daniel’s certificate of his update to issue 824 |

The house rule regularizes each re-housed count in the pull request that adopts it.

## How They Were Run

On 31 October 2026, from 08:40Z to 09:23Z, in the records branch
`claude/bold-ritchie-xo28us-upper` (#852), after `adopt_houses` had written the eight
counts into the pass of 31 October, and after
`build_known_best_atlas --update --n 130 172 204 232 260 293 299 307`,
`regularize_axis_components --update-atlas --n ...` and `default_drawings --update`,
which read all eight as pending.
From `packing/`, at most two processes, `nice`, on a four-core host shared with other
lanes, in run directories named as `adopt_houses` prints them, with no dot in the
grid-slack names, since a run’s id takes none:

```sh
N="130 172 204 232 260 293 299 307"; P=adopt-2026-10-31-n130-307
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg05
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n $N --workers 1
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 2 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
```

then the three `layer` commands the selection printed (grid-slack’s 0.5-degree run at
260 and 293, its 1-degree run at 232 and its 5-degree run at 130, 172 and 204), then
`render_regularized_atlas --update`, `default_drawings --update`,
`flip_regularization --update`, `regularized_drawings` and `render_results --update`,
and `default_drawings --retain-runs`, which keeps the grid-slack runs’ index blocks
under [`settled-runs/`](../settled-runs/).

Grid-slack took 448, 308 and 488 CPU seconds at 0.5, 1 and 5 degrees.
Evan Daniel’s driver took 1,501 CPU seconds over 1,600 s of wall at one worker, 562 of
them at 204. The selection took 372 s of wall at two workers, at most 12.4 CPU-minutes.
That is about 66 CPU-minutes in all, under the 40 CPU-hour item cap.

## What They Decided

| n | Outcome | Drawn now |
| ---: | --- | --- |
| 130 | Grid-slack’s 5-degree view at the witness’s side, admitted: fewer light and uneven squares, angle classes and hues than the axis tool’s view, more full shared sides. Evan Daniel’s regularizer solved the witness to a KKT local minimum 2.50e-13 below its side, held at row 3 as a register candidate | grid-slack’s 5-degree view |
| 172 | Grid-slack’s 5-degree view, admitted: no uneven or near-axis square, fewer angle classes, more full shared sides. The regularizer’s view went to review at row 7 | grid-slack’s 5-degree view |
| 204 | Grid-slack’s 5-degree view, admitted. The regularizer’s solve did not certify: its exact point is not a local minimum (the issue’s own solver did not converge here either) | grid-slack’s 5-degree view |
| 232 | Grid-slack’s 1-degree view, admitted. The regularizer’s solve is not jammed and draws no view | grid-slack’s 1-degree view |
| 260 | Grid-slack’s 0.5-degree view, admitted. The regularizer’s solve failed | grid-slack’s 0.5-degree view |
| 293 | Grid-slack’s 0.5-degree view, admitted. The regularizer’s solve failed | grid-slack’s 0.5-degree view |
| 299 | Decided no better (`SETTLED`): every view, the regularizer’s certified KKT solve at the witness’s side and grid-slack’s at all three thresholds, is refused at row 7, a house or stage total of shared sides falling | the axis tool’s view |
| 307 | Decided no better (`SETTLED`): grid-slack’s views are refused at row 7; the regularizer’s KKT solve is 3.75e-12 below the side, held at row 3 as a register candidate | the axis tool’s view |

Every admitted view is at its witness’s side, so no drawing proves another bound.
The two register candidates are smaller packings than the new houses at 130 and 307;
they are registered and reviewed as a result of their own before any adoption
(think-ruu2), as the regularization guide’s
[Register Candidates](../../../../docs/project/guides/regularization-process.md#register-candidates)
asks.

## Files

- `adopt-2026-10-31-n130-307-evand/`: the driver’s `receipt.json` and each count’s
  `report.json.gz`.
- `adopt-2026-10-31-n130-307-grid-{deg05,deg1,deg5}/`: each count’s `report.json.gz`;
  the runs’ blocks are in `../settled-runs/` and the layer’s index.
- `selection-adopt-2026-10-31-n130-307.{json.gz,md}`: the selection’s report and table.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
