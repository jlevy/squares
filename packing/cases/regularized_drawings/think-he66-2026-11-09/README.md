# Regularization Runs After the Adoption of Issues 935 and 936 (think-he66)

These are the strong generators’ runs on the two witnesses that the adoption of Doğa
Özden’s further arrangements of issues 935 and 936 wrote, under
[the house rule](../../../campaign/result-import.md#the-house-rule), after the stage 4
review of 9 November 2026
([review-2026-11-09-ozden-935-936.md](../../../../docs/project/reviews/review-2026-11-09-ozden-935-936.md)):

| n | House | Replaces | Adopted |
| ---: | --- | --- | --- |
| 172 | T-282 | T-257 | 9 November 2026 |
| 270 | T-283 | T-224 | 9 November 2026 |

## How They Were Run

In the records branch `claude/bold-ritchie-xo28us-l71` (#937), after `adopt_houses` had
written both counts, and after `build_known_best_atlas --update`,
`regularize_axis_components --update-atlas --n 172 270` and `default_drawings --update`.
From `packing/`, at most two processes, `nice -n 19` on two cores, on a four-core host
shared with other lanes, in the run directories `adopt_houses` printed, with no dot in
the grid-slack names:

```sh
N="172 270"; P=adopt-2026-11-09-n172-270
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg05
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n $N --workers 1
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 1 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
```

Then the one `layer` command the selection printed, for the driver’s run at 172, the
settlement of 270 in `default_drawings.SETTLED`, and
`render_regularized_atlas --update`, `default_drawings --update`,
`flip_regularization --update`, `regularized_drawings` and `render_results --update`.

The axis tool refuses 270’s witness.
Its exact compaction compounds each slide’s denominators, and on this certificate a
slide limit passed 4,300 digits within seconds, where the tool failed while writing the
move; with Python’s limit lifted it ran more than half an hour without converging.
The tool now refuses such a frame (`regularize_axis_components.SLIDE_DIGITS`, refusal
`slide-digits`), which changes no retained record, since each of them was written below
that limit. At 172 the axis tool drew its view in 9 seconds.

By the receipts:

- Grid-slack took 30.35, 30.97 and 30.77 seconds at 0.5, 1 and 5 degrees, the per-count
  seconds its reports record, summed; each run’s `run.json` here is the block
  `regularize_grid_slack.run_block` builds from its reports, since none of its views is
  drawn and the layer’s index keeps no block of it.
- Evan Daniel’s driver took 262.07 CPU seconds over 263.36 s of wall at one worker, by
  its `receipt.json`.
- The selection writes no cost.
  It took 85 s of wall at one worker.

That is about 7 CPU-minutes in all, under the 40 CPU-hour item cap; the refused axis
runs at 270 took about 40 CPU-minutes more before the refusal was written.

## What They Decided

| n | Outcome | Drawn now |
| ---: | --- | --- |
| 172 | Evan Daniel’s view at the witness’s side, admitted: light, uneven and near-axis squares, angle classes and hues 1, 3, 0, 3 and 3 against the axis tool’s 17, 44, 7, 19 and 19, and 511 and 511 full shared sides against 369 and 443 | Evan Daniel’s view |
| 270 | Decided no better (`SETTLED`): grid-slack’s views at all three thresholds are refused at row 7, a house or stage total of shared sides falling, and the axis tool refuses the witness | the house drawing |

The admitted view is at its witness’s side, so no drawing proves another bound.
At both counts Evan Daniel’s regularizer solved the witness to a certified KKT point
below its side, by 2.63 × 10⁻¹² at 172 and 3.25 × 10⁻¹² at 270, about each certificate’s
own uniform-contraction margin (2.53 and 3.21 × 10⁻¹²), and the selection held each at
row 3 as a register candidate: a smaller packing is registered and reviewed as a result
of its own first, and is never admitted here.
Nothing here registers them.
The strong views of the earlier witnesses lapsed with the houses, T-224’s Evan Daniel
view at 270 among them; each count is decided here on its new witness, so nothing is
owed. At 270 the drawing the site shows is less regular than the lapsed view (140 uneven
and 26 near-axis squares against 10 and 0); the solved view at 270, once registered and
reviewed, is the one that would draw it regularized.

## Files

- `adopt-2026-11-09-n172-270-evand/`: the driver’s `receipt.json` and each count’s
  `report.json.gz`.
- `adopt-2026-11-09-n172-270-grid-{deg05,deg1,deg5}/`: each run’s block, `run.json`, and
  each count’s `report.json.gz`.
- `selection-adopt-2026-11-09-n172-270.{json.gz,md}`: the selection’s report and table.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
