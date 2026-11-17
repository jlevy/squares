# Regularization Runs After the Adoption of Issue 983 (think-14i2)

These are the strong generators’ runs on the witness that the adoption of Doğa Özden’s
issue 983 wrote at 228, under
[the house rule](../../../campaign/result-import.md#the-house-rule), on the accepted
verdict of the stage 4 review of 14 November 2026, read from its frozen findings at
about 19:25Z, before its post-freeze checks were done
([review-2026-11-14-ozden-983.md](../../../../docs/project/reviews/review-2026-11-14-ozden-983.md)):

| n | House | Replaces | Adopted |
| ---: | --- | --- | --- |
| 228 | T-300 | T-174 | 14 November 2026 |

The house is a new arrangement relative to T-174’s packing (Francisco Couzo’s, as
PingYou Ltd improved it), from the author’s column-band proposal designer.

## How They Were Run

In the records branch `claude/bold-ritchie-xo28us-l160`, after `adopt_houses` had
written the count, and after `build_known_best_atlas --update --n 228`,
`regularize_axis_components --update-atlas --n 228` and `default_drawings --update`.
From `packing/`, at most two processes, `nice -n 19`, in run directories named for the
adoption’s day and its count, the grid-slack directories named without a dot from the
start, since the index’s schema refuses one (a run id is `^[a-z0-9-]+$`):

```sh
N=228; P=adopt-2026-11-14-n228
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg05
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n $N --workers 1
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 2 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
```

Then the one `layer` command the selection printed, for grid-slack’s 1-degree run, with
its empty `--run-dir` in the lane’s scratch space rather than a new temporary directory,
and the guide’s render-and-record step.
The axis tool’s refresh drew its view of the new witness first, so the selection was
measured against a drawing of the new witness.
The settlement of 228 on T-174’s witness (decided no better by the runs of 17 October,
think-3mry) lapsed with the adoption and is taken off.

## What They Found

[selection-adopt-2026-11-14-n228.md](selection-adopt-2026-11-14-n228.md) is the
selection’s table, and its JSON beside it the full report.
The view is drawn at the witness’s side, admitted at row 10, and better than the axis
tool’s view of the new witness on every goal of the improvement rule; the figures are
light, uneven and near-axis squares, angle classes and hues, then full shared sides
(house and stage):

| n | View drawn | Goals before → after | Shared sides before → after | Evan Daniel’s driver |
| ---: | --- | --- | --- | --- |
| 228 | grid-slack’s 1-degree view | 35, 78, 12, 30, 19 → 0, 4, 0, 16, 16 | 475, 577 → 672, 680 | same-side view held for review at row 7; certified KKT solve 3.01 × 10⁻¹² below the side, held at row 3 |

- Grid-slack’s three runs each drew a view one to one with the witness (largest move
  0.122), each admitted at row 10. The 1- and 5-degree runs drew the same view, and the
  0.5-degree run’s, at 18 classes and hues and 665 and 673 shared sides, is worse than
  it on those goals, so the selection drew the 1-degree run’s.
- Evan Daniel’s driver solved the witness to a certified KKT local minimum and drew a
  same-side view, better than the axis tool’s on every goal, which its row 7 holds for
  review: 32 per-square counts fell while no total did.
  Its certified KKT solve lies 3.013 × 10⁻¹² below the side, 1.02 of the certificate’s
  own contraction margin (2.949 × 10⁻¹²), so its solved view is held at row 3 as a
  register candidate and not admitted; registering a solved side about the certificate’s
  own padding below it, here 6.4 × 10⁻¹⁴ beyond the contracted side, is RV-3’s question
  (think-ruu2, think-ikku), as at 156, 172, 179, 180, 199, 268, 269 and 270.
- The record’s comparison with the base branch: T-174’s witness was drawn as its house
  drawing (665 full shared sides, no uneven or near-axis square, decided no better); the
  new witness draws grid-slack’s view (4 uneven, no near-axis square, 672 full shared
  sides). No strong view gives way to a worse drawing, and no runs are owed.
- The flip record decides the new picture’s pose (`flip_regularization --check`): the
  published pose, by quadrants.

## Retained Here

| Directory or file | What |
| --- | --- |
| `adopt-2026-11-14-n228-grid-deg05/`, `-grid-deg1/`, `-grid-deg5/` | each run’s block, `run.json`, summed from its report, and the report, `n-228/report.json.gz` |
| `adopt-2026-11-14-n228-evand/` | the driver’s `receipt.json` and its report |
| `selection-adopt-2026-11-14-n228.json.gz`, `.md` | the selection’s report and table |

The runs cost about 31 CPU-seconds for grid-slack’s three runs, 112 CPU-seconds for the
driver by its receipt, and seconds for the selection.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
