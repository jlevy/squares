# Regularization Runs After the Adoption of Issue 1001 (think-0y9m)

These are the strong generators’ runs on the five witnesses that the adoption of
JoeGun’s issue 1001 wrote in the pass of 16 November 2026, under
[the house rule](../../../campaign/result-import.md#the-house-rule), on the accepted
verdict of the stage 4 review of 16 November 2026
([review-2026-11-16-joegun-1001.md](../../../../docs/project/reviews/review-2026-11-16-joegun-1001.md)).
The same day’s pass had moved 90 only, so these counts join it.

| n | House | Replaces | Adopted |
| ---: | --- | --- | --- |
| 127 | T-305 | PingYou Ltd’s refinement of Francisco Couzo’s refinement of Ryan Xu’s packing (T-174) | 16 November 2026 |
| 204 | T-306 | Evan Daniel’s packing of issue 914 (T-268) | 16 November 2026 |
| 232 | T-307 | Doğa Özden’s further arrangement of Couzo’s refinement of Alex Chilton’s packing (T-275) | 16 November 2026 |
| 264 | T-308 | Mishapolk’s tighter certificate of Daniil Ostashev’s composition (T-186) | 16 November 2026 |
| 305 | T-309 | PingYou Ltd’s tighter certificate of Couzo’s refinement of Nate Chaoweeraprasit’s packing (T-174) | 16 November 2026 |

Each house is Tomáš Kodaj’s public Kaggle packing as JoeGun improved it, a new
arrangement relative to the house it replaces.

## How They Were Run

In the records branch `claude/bold-ritchie-xo28us-l187`, after `adopt_houses` had
written the five counts at 07:01Z on 16 November, and after
`build_known_best_atlas --update`,
`regularize_axis_components --update-atlas --n 127 204 232 264 305` and
`default_drawings --update`. From `packing/`, at most two processes, `nice -n 19`, in
run directories named for the adoption’s day and its lowest and highest count, the
grid-slack directories named without a dot, since the index’s schema refuses one:

```sh
P=adopt-2026-11-16-n127-305
N="127 204 232 264 305"
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg05
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n $N --workers 2
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 2 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
```

Then the three `layer` commands the selection printed, one for each grid-slack run, and
the guide’s render-and-record step.
The axis tool’s refresh drew its view of each new witness first, so the selection was
measured against a drawing of the new witness.
At 127 the earlier witness’s settlement (`decided-no-better`, think-3mry) was taken off
`default_drawings.SETTLED`, since these runs decide the new witness.

## What They Found

[selection-adopt-2026-11-16-n127-305.md](selection-adopt-2026-11-16-n127-305.md) is the
selection’s table, and its JSON beside it the full report.
The figures are light, uneven and near-axis squares, angle classes and hues, then full
shared sides (house and stage), against the axis tool’s view of each new witness:

| n | View drawn | Goals before → after | Shared sides before → after | Evan Daniel’s driver |
| ---: | --- | --- | --- | --- |
| 127 | grid-slack at 1 degree | 17, 23, 24, 44, 19 → 1, 2, 0, 18, 18 | 107, 227 → 244, 290 | KKT local minimum 1.2175 × 10⁻¹⁰ below the side, held at row 3 |
| 204 | grid-slack at 5 degrees | 15, 47, 9, 35, 19 → 2, 5, 0, 25, 19 | 312, 465 → 409, 491 | its exact solve failed, at 80 and at 100 digits: no view |
| 232 | grid-slack at 0.5 degrees | 8, 37, 4, 29, 19 → 4, 28, 0, 25, 19 | 575, 602 → 598, 608 | KKT local minimum 4.0164 × 10⁻⁹ below the side, held at row 3 |
| 264 | grid-slack at 1 degree | 37, 96, 25, 65, 19 → 4, 28, 0, 39, 19 | 453, 719 → 697, 723 | KKT local minimum 1.9066 × 10⁻¹¹ below the side, held at row 3 |
| 305 | grid-slack at 0.5 degrees | 72, 100, 47, 109, 19 → 2, 13, 0, 67, 19 | 391, 786 → 787, 869 | KKT local minimum 1.9146 × 10⁻¹⁰ below the side, held at row 3 |

- **The views.** Grid-slack’s three runs each drew a same-side view of every count, one
  to one with its witness; the selection draws, at each count, the one better than the
  axis tool’s view on the most goals, admitted at row 10.
- **The KKT solves.** The driver certified a KKT local minimum below the side at 127,
  232, 264 and 305, each held at row 3 as a register candidate and not admitted;
  registering them is RV-3’s question (think-ruu2, think-ikku).
  No report states those sides.
  Against each certificate’s own contraction margin (the packet’s
  `measure/contraction-nNNN-own.json`), the step is about 1.006 times the margin at 127,
  273 times at 232, 1.007 times at 264 and 1.004 times at 305: beyond the margin at
  each, by a hair at three of them.
- **The comparison with the base branch** (`default_drawings --compare`): at 127 the
  earlier witness drew its house (settled no better); at 204, 232, 264 and 305 a strong
  view of the earlier witness gave way to this witness’s grid-slack view, which the
  compare names as worse on some goals than the earlier witness’s view (angle classes
  and shared sides at 204, uneven squares at 232 and 305, more at 264). Those views
  lapsed with their witnesses, and these runs decide the new ones, so no runs are owed.
- The flip record decides each new picture’s pose (`flip_regularization --check`): a
  mirror at 127, and a quarter turn at 204, 232, 264 and 305, by quadrants.

## Retained Here

| Directory or file | What |
| --- | --- |
| `adopt-2026-11-16-n127-305-grid-deg05/`, `-grid-deg1/`, `-grid-deg5/` | each run’s block, `run.json`, summed from its reports, and each count’s report, `n-NNN/report.json.gz` |
| `adopt-2026-11-16-n127-305-evand/` | the driver’s `receipt.json` and each count’s report |
| `selection-adopt-2026-11-16-n127-305.json.gz`, `.md` | the selection’s report and table |

The runs cost about 74, 78 and 115 CPU-seconds for grid-slack’s three runs, 408
CPU-seconds for the driver by its receipt, and about 90 seconds for the selection: under
12 CPU-minutes in all, far inside the owner’s 40 CPU-hours an item.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
