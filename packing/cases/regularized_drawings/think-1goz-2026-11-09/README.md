# Regularization Runs After the Adoption of Issue 938 (think-1goz)

These are the strong generators’ runs on the witness that the adoption of Doğa Özden’s
issue 938 wrote at 199, under
[the house rule](../../../campaign/result-import.md#the-house-rule), after the stage 4
review of 9 November 2026
([review-2026-11-09-ozden-938.md](../../../../docs/project/reviews/review-2026-11-09-ozden-938.md)):

| n | House | Replaces | Adopted |
| ---: | --- | --- | --- |
| 199 | T-284 | T-127 | 9 November 2026 |

The house is T-282’s packing at 172 with one L step of 27 unit squares (a row of 14
along the top, a column of 13 along the right), at T-282’s side plus one, exactly.

## How They Were Run

In the records branch `claude/bold-ritchie-xo28us-l76`, after `adopt_houses` had written
the count, and after `build_known_best_atlas --update`,
`regularize_axis_components --update-atlas --n 199` and `default_drawings --update`.
From `packing/`, at most two processes, `nice -n 19`, on a four-core host shared with
other lanes, in run directories named for the adoption’s day and count, with no dot in
the grid-slack names (the layer index refuses a dot in a run id):

```sh
N=199; P=adopt-2026-11-09-n199
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg05
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n $N --workers 2
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 2 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
```

Then the one `layer` command the selection printed, for grid-slack’s 0.5-degree run at
199, and the guide’s render-and-record step.
The grid-slack runs were first made under names with a dot (`grid-0.5`) as
`adopt_houses` printed them; the layer index’s schema refuses such an id, so they were
made again under these names, at the same cost, and the first ones were discarded
unrecorded.

## What They Found

[selection-adopt-2026-11-09-n199.md](selection-adopt-2026-11-09-n199.md) is the
selection’s table, and its JSON beside it the full report.

- **199: grid-slack’s 0.5-degree view is drawn**, at the witness’s side, admitted at row
  10: light, uneven, near-axis, angle classes and hues 3, 10, 0, 12 and 12 against the
  house drawing’s 19, 51, 7, 19 and 19, and full shared sides 548 (house) and 576
  (stage) against 464 and 538. Its 1- and 5-degree runs drew the same view.
  It is one to one with the witness, 44 squares moved, the largest by 0.0505.
- Evan Daniel’s driver re-solved the witness: its same-side view was refused at row 7,
  and its certified KKT solve lies 2.63 × 10⁻¹² below the side, about the 172 part’s own
  padding (T-282’s certificate loses 2.53 × 10⁻¹² to uniform contraction), held at row 3
  as a register candidate and not admitted, as at 172 and 270 on the same day.
- Against main’s drawing at 199, the regularized view of T-127’s witness, the new
  drawing is worse on light and uneven squares and on full shared sides: it draws a
  different packing, and that view lapsed with its witness
  (`default_drawings --compare`).
- The flip record decides the new picture’s pose again (`flip_regularization --check`).

## Retained Here

| Directory or file | What |
| --- | --- |
| `adopt-2026-11-09-n199-grid-deg05/`, `-grid-deg1/`, `-grid-deg5/` | each run’s block, `run.json` (the 0.5-degree one the layer index’s own block), and its report at 199, `n-199/report.json.gz` |
| `adopt-2026-11-09-n199-evand/` | the driver’s `receipt.json` and its report at 199 |
| `selection-adopt-2026-11-09-n199.json.gz`, `.md` | the selection’s report and table |

The runs cost about 1.0 CPU-minute for grid-slack’s three runs (twice, with the
discarded first names), 1.6 CPU-minutes for the driver (98.8 CPU seconds by its
receipt), and about 20 seconds for each selection.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
