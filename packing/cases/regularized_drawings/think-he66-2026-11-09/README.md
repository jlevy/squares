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

Then the one `layer` command the selection printed, for the driver’s run at 172.

**270 ran twice.** The axis tool failed on 270’s witness at first: its exact compaction
compounds each slide’s denominators, and on this certificate a slide limit passed 4,300
digits within seconds, where the tool failed while writing the move.
With Python’s limit lifted it was stopped after about 40 CPU-minutes, still inside its
pass cap of n + 2 passes.
Until the tool could refuse such a frame, the layer’s index kept T-224’s view at 270, so
the first runs’ row 7 measured every 270 view against that view of the superseded
witness (743 and 753 full shared sides), and refused grid-slack’s views and the driver’s
solve on totals that, against T-283’s own witness (407 and 727), rise.
The first selection flagged each 270 candidate as measured against another drawing than
the tree’s. The senior review of #937 (L74) found it.

The tool now refuses such a frame (`regularize_axis_components.SLIDE_DIGITS`, refusal
`slide-digits`), which changes no retained record, since each of them was written below
that limit; at 172 the axis tool drew its view in 9 seconds.
With 270’s layer entry refused, the layer holds no view there, and both strong
generators ran again at 270 on T-283’s witness:

```sh
P=adopt-2026-11-09-n270-rerun
python -m devtools.regularize_grid_slack --n 270 --run-dir $RUNS/$P-grid-deg05
python -m devtools.regularize_grid_slack --n 270 --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n 270 --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n 270 --workers 1
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 1 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. \
  --grid-run $RUNS/$P-grid-deg05 --grid-counts 270
```

Then `render_regularized_atlas --update`, `default_drawings --update`,
`flip_regularization --update`, `regularized_drawings` and `render_results --update`.

By the receipts:

- The first runs: grid-slack took 30.35, 30.97 and 30.77 seconds at 0.5, 1 and 5
  degrees, the per-count seconds its reports record, summed; Evan Daniel’s driver took
  262.07 CPU seconds over 263.36 s of wall at one worker, by its `receipt.json`; the
  selection took 85 s of wall at one worker.
- The re-runs at 270: grid-slack took 20.59, 19.59 and 21.00 seconds; the driver took
  205.77 CPU seconds over 207.22 s of wall; the selection took 54 s of wall.
- Each grid-slack run’s `run.json` here is its block: the layer index’s for the re-run’s
  0.5-degree run, whose view is drawn, and the block `regularize_grid_slack.run_block`
  builds from the reports for the others, which the index keeps no block of.

That is about 12 CPU-minutes in all, under the 40 CPU-hour item cap; the axis tool’s
attempts at 270 took about 40 CPU-minutes more before the refusal was written.

## What They Decided

| n | Outcome | Drawn now |
| ---: | --- | --- |
| 172 | Evan Daniel’s view at the witness’s side, admitted: light, uneven and near-axis squares, angle classes and hues 1, 3, 0, 3 and 3 against the axis tool’s 17, 44, 7, 19 and 19, and 511 and 511 full shared sides against 369 and 443 | Evan Daniel’s view |
| 270 | Grid-slack’s 0.5-degree view of the re-run at the witness’s side, admitted at row 10: 6, 13, 0, 30 and 19 against the house drawing’s 40, 140, 26, 37 and 19, and 737 and 747 full shared sides against 407 and 727 | grid-slack’s 0.5-degree view |

The admitted views are at their witnesses’ sides, so no drawing proves another bound.
At both counts Evan Daniel’s regularizer solved the witness to a certified KKT point
below its side, by 2.635 × 10⁻¹² at 172 and 3.253 × 10⁻¹² at 270, 1.04 and 1.01 times
each certificate’s own uniform-contraction margin (2.533 and 3.212 × 10⁻¹²), and the
selection held each at row 3 as a register candidate: a smaller packing is registered
and reviewed as a result of its own first, and is never admitted here.
Nothing here registers them.
Their registration waits on think-wju3 and on the owner’s question about gains near a
certificate’s padding (RV-3, think-ruu2 and think-ikku).
The strong views of the earlier witnesses lapsed with the houses, T-224’s Evan Daniel
view at 270 among them; each count is decided here on its new witness, so nothing is
owed.

## Files

- `adopt-2026-11-09-n172-270-evand/`: the first driver run’s `receipt.json` and each
  count’s `report.json.gz`; its view at 172 is drawn.
- `adopt-2026-11-09-n172-270-grid-{deg05,deg1,deg5}/`: each first grid-slack run’s
  block, `run.json`, and each count’s `report.json.gz`; at 270 their row 7 is the stale
  baseline above.
- `selection-adopt-2026-11-09-n172-270.{json.gz,md}`: the first selection’s report and
  table.
- `adopt-2026-11-09-n270-rerun-evand/` and
  `adopt-2026-11-09-n270-rerun-grid-{deg05,deg1,deg5}/`: the re-runs at 270, likewise.
- `selection-adopt-2026-11-09-n270-rerun.{json.gz,md}`: the re-run’s selection.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
