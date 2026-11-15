# Regularization Runs After the Adoption of Issues 984 and 985 (think-17ex)

These are the strong generators’ runs on the witnesses that the adoption of Roberto
Ono’s issues 984 and 985 wrote at 228 and 147 in the pass of 15 November 2026, under
[the house rule](../../../campaign/result-import.md#the-house-rule), on the accepted
verdict of the stage 4 review of 14 November 2026
([review-2026-11-14-ono-984-985.md](../../../../docs/project/reviews/review-2026-11-14-ono-984-985.md)),
whose frozen findings this lane read at 21:45Z and whose final head it read at 21:56Z on
14 November, after its own replay, controls, measurements and registration were
committed:

| n | House | Replaces | Adopted |
| ---: | --- | --- | --- |
| 147 | T-302 | the case record’s own house, the Kingbird catalogue’s 45-degree packing (T-155’s exact ceiling) | 15 November 2026 |
| 228 | T-301 | T-300 | 15 November 2026 |

Both houses are new arrangements: at 228 relative to T-300’s packing (Doğa Özden’s
column-band packing) and every other registered packing there, five band periods cut
from Francisco Couzo’s 404; at 147 relative to the 45-degree packing it shares with 148,
one band period cut from Evan Daniel’s 229.

## How They Were Run

In the records branch `claude/bold-ritchie-xo28us-l164`, after `adopt_houses` had
written both counts at 00:01Z on 15 November, and after
`build_known_best_atlas --update`,
`regularize_axis_components --update-atlas --n 147 228` and `default_drawings --update`.
From `packing/`, at most two processes, `nice -n 19`, in run directories named for the
adoption’s day and its lowest and highest count, the grid-slack directories named
without a dot, since the index’s schema refuses one (a run id is `^[a-z0-9-]+$`):

```sh
P=adopt-2026-11-15-n147-228
python -m devtools.regularize_grid_slack --n 147 228 --run-dir $RUNS/$P-grid-deg05
python -m devtools.regularize_grid_slack --n 147 228 --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n 147 228 --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n 147 228 --workers 1
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 2 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
```

Then the one `layer` command the selection printed, for grid-slack’s 0.5-degree run at
147, with its empty `--run-dir` in the lane’s scratch space rather than a new temporary
directory, and the guide’s render-and-record step.
The axis tool’s refresh drew its view of each new witness first, so the selection was
measured against a drawing of the new witness.
The view of T-300’s witness at 228 (grid-slack’s 1-degree view, run of 14 November)
lapsed with the adoption.

## What They Found

[selection-adopt-2026-11-15-n147-228.md](selection-adopt-2026-11-15-n147-228.md) is the
selection’s table, and its JSON beside it the full report.
The figures are light, uneven and near-axis squares, angle classes and hues, then full
shared sides (house and stage), against the axis tool’s view of the new witness:

| n | View drawn | Goals before → after | Shared sides before → after | Evan Daniel’s driver |
| ---: | --- | --- | --- | --- |
| 147 | grid-slack’s 0.5-degree view, admitted at row 10 | 5, 39, 0, 8, 8 → 3, 20, 0, 8, 8 | 349, 377 → 377, 385 | same-side view refused at row 7; certified KKT solve 3.415 × 10⁻⁹ below the side, held at row 3 |
| 228 | the axis tool’s view, decided no better | 1, 17, 1, 11, 11 (unchanged) | 644, 656 (unchanged) | same-side view refused at row 7; KKT solve 4.289 × 10⁻⁹ below the side, its certificate invalid, held at row 3 |

- **147.** Grid-slack’s three runs each drew a view one to one with the witness (largest
  move 0.049); the selection draws the 0.5-degree run’s, better than the axis tool’s
  view on light and uneven squares and both totals of shared sides.
- **228.** Grid-slack’s three runs each drew a view one to one with the witness (largest
  move 0.329), better on uneven and near-axis squares, classes, hues and both totals,
  but each goes to review at row 7, two per-square counts falling while no total does;
  Evan Daniel’s same-side view is refused at row 7, a total of shared sides falling.
  No view is adoptable, so the axis tool’s view stays drawn and
  `default_drawings.SETTLED` decides the count no better on T-301’s witness, naming
  these four runs.
- **The KKT solves.** At 147 the driver certified a KKT point 3.415 × 10⁻⁹ below the
  side, 1.16 of the certificate’s own contraction margin (2.934 × 10⁻⁹), beyond it; at
  228 it reached a local minimum of the side, strict modulo 129 exact flat motions,
  4.289 × 10⁻⁹ below the side, 1.23 of the margin (3.488 × 10⁻⁹), beyond it, whose
  rational certificate did not validate.
  Both are held at row 3 as register candidates and not admitted; registering them is
  RV-3’s question (think-ruu2, think-ikku).
  Each side agrees with the side-only leaderboard entry its issue quotes first
  (Nevska’s, at both counts) at all 24 printed places, so those entries are, to their
  printed precision, the local optima of these two arrangements.
- The record’s comparison with the base branch (`default_drawings --compare`): at 147
  the catalogue’s 45-degree witness was regular as published, its house drawing (no
  uneven or near-axis square, 506 full shared sides); the new witness draws grid-slack’s
  view (20 uneven, no near-axis square, 377 full shared sides).
  At 228 T-300’s witness drew grid-slack’s view (4 uneven, no near-axis square, 672 full
  shared sides); the new witness is decided no better and draws the axis tool’s view (17
  uneven, 1 near-axis, 644). That strong view gave way with the witness it was drawn
  from: the new witness is a new arrangement, and every strong view of it goes to review
  or is refused. No count is left pending, and no runs are owed.
- The flip record decides each new picture’s pose (`flip_regularization --check`): at
  147 the published pose, by quadrants; at 228 a half turn with a flip, mirrored across
  the rising diagonal, by quadrants.

## Retained Here

| Directory or file | What |
| --- | --- |
| `adopt-2026-11-15-n147-228-grid-deg05/`, `-grid-deg1/`, `-grid-deg5/` | each run’s block, `run.json`, summed from its reports, and the reports, `n-147/report.json.gz` and `n-228/report.json.gz` |
| `adopt-2026-11-15-n147-228-evand/` | the driver’s `receipt.json` and its reports |
| `selection-adopt-2026-11-15-n147-228.json.gz`, `.md` | the selection’s report and table |

The runs cost about 25.0 CPU-seconds for grid-slack’s three runs, 1,593 CPU-seconds for
the driver by its receipt (the solve at 228 timed out once and was solved again with the
`probe-flat-stall-stop` patch), and seconds for the selection.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
