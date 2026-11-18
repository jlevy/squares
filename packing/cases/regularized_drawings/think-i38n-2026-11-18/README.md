# Regularization Runs After the Adoption of Issue 1009 (think-i38n)

These are the strong generators’ runs on the thirteen witnesses that the adoption of
Mykhailo Polkovskyi’s issue 1009 wrote in the pass of 18 November 2026, under
[the house rule](../../../campaign/result-import.md#the-house-rule), on the accepted
verdicts of the two stage 4 reviews of 17 November 2026
([review-2026-11-17-polkovskyi-1009.md](../../../../docs/project/reviews/review-2026-11-17-polkovskyi-1009.md),
pull request 1014, and
[review-2026-11-17-ozden-de-winter-1005-1007.md](../../../../docs/project/reviews/review-2026-11-17-ozden-de-winter-1005-1007.md),
pull request 1013, which accepts the certificates of issues 1005 to 1007 that #1009 is
smaller than at 262, 292 and 295):

| n | House | Replaces | Adopted |
| ---: | --- | --- | --- |
| 147 | T-314 | T-302 | 18 November 2026 |
| 156 | T-315 | T-287 | 18 November 2026 |
| 180 | T-316 | T-288 | 18 November 2026 |
| 210 | T-317 | T-174 | 18 November 2026 |
| 260 | T-318 | T-269 | 18 November 2026 |
| 262 | T-319 | the case record’s own house, the Kingbird catalogue’s 16 + √2/2 packing (T-101’s exact certificate, T-155’s ceiling) | 18 November 2026 |
| 268 | T-320 | T-289 | 18 November 2026 |
| 270 | T-321 | T-283 | 18 November 2026 |
| 272 | T-322 | T-174 | 18 November 2026 |
| 292 | T-323 | T-146 | 18 November 2026 |
| 295 | T-324 | T-193 | 18 November 2026 |
| 299 | T-325 | T-277 | 18 November 2026 |
| 307 | T-326 | T-279 | 18 November 2026 |

Five of the thirteen (156, 180, 270, 299, 307) are re-solves of the packing they
replace, each a new result under option D (think-b0w5) because its side is below its
predecessor’s shrunk to first contact; three (147, 260, 268) are further arrangements of
the packing they replace; and five (210, 262, 272, 292, 295) are new arrangements or
further arrangements of another packing (at 262 and 292, of Joost de Winter’s issue-1007
and issue-1006 packings, T-312 and T-311).

## How They Were Run

In the records branch `claude/intake-2026-11-17-import-1009`, after `adopt_houses` had
written all thirteen counts in the pass of 18 November, and after
`build_known_best_atlas --update`, `regularize_axis_components --update-atlas` on the
thirteen counts and `default_drawings --update`. From `packing/`, at most two processes,
`nice -n 19`, in run directories named for the adoption’s day and its lowest and highest
count, the grid-slack directories named without a dot (a run id is `^[a-z0-9-]+$`):

```sh
P=adopt-2026-11-18-n147-307
N="147 156 180 210 260 262 268 270 272 292 295 299 307"
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg05
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n $N --workers 1
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 2 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
```

Grid-slack’s three runs ran one after another from 22:36Z to 23:04Z on 17 November, and
the driver beside them from 22:36Z to 23:49Z. Then the selection’s commands:
`regularize_evand reclassify --refresh-bounds` on a copy of the driver’s run, its
`layer` from that copy, and one `layer` for grid-slack’s 0.5-degree run at 147, 156,
210, 260, 268, 292, 295 and 299, with empty `--run-dir` directories in the lane’s
scratch space; then the guide’s render-and-record step.
The axis tool’s refresh drew its view of each new witness first, so the selection was
measured against a drawing of the new witness, or against the witness itself at 292 and
295, where the axis tool draws no view.

## What They Found

[selection-adopt-2026-11-18-n147-307.md](selection-adopt-2026-11-18-n147-307.md) is the
selection’s table, and its JSON beside it the full report.
The figures are light, uneven and near-axis squares, angle classes and hues, then full
shared sides (house and stage), against the axis tool’s view of the new witness (at 292
and 295, the witness):

| n | View drawn | Goals before → after | Shared sides before → after | Evan Daniel’s driver |
| ---: | --- | --- | --- | --- |
| 147 | grid-slack’s 0.5-degree view, row 10 | 7, 16, 11, 20, 19 → 1, 6, 0, 10, 10 | 320, 389 → 389, 397 | same-side view refused at row 7 (a total of shared sides falls); solved view held at row 4 |
| 156 | grid-slack’s 0.5-degree view, row 10 | 5, 9, 1, 19, 19 → 2, 4, 0, 18, 18 | 337, 364 → 356, 366 | solved view held at row 4 |
| 180 | the driver’s same-side view, row 10 | 17, 34, 9, 25, 19 → 4, 9, 0, 8, 8 | 423, 481 → 513, 515 | drawn; solved view held at row 4 |
| 210 | grid-slack’s 0.5-degree view, row 10 | 3, 6, 0, 24, 19 (unchanged) | 500, 544 → 506, 544 | solve failed, again at 100 digits: no view |
| 260 | grid-slack’s 0.5-degree view, row 10 | 9, 28, 3, 29, 19 → 3, 9, 0, 26, 19 | 500, 608 → 596, 638 | KKT solve 1.01 × 10⁻¹⁴ below the side, held at row 3 |
| 262 | the driver’s same-side view, row 10 | 23, 53, 37, 58, 19 → 0, 0, 0, 2, 2 | 489, 712 → 822, 822 | drawn; solved view held at row 4 |
| 268 | grid-slack’s 0.5-degree view, row 10 | 28, 104, 41, 65, 19 → 0, 0, 0, 28, 19 | 495, 833 → 834, 846 | KKT solve 1.63 × 10⁻¹⁵ below, held at row 3 |
| 270 | the axis tool’s view, decided no better | 17, 82, 36, 38, 19 (unchanged) | 516, 727 (unchanged) | KKT solve 5.73 × 10⁻¹⁵ below, held at row 3 |
| 272 | the driver’s same-side view, row 10 | 3, 12, 5, 27, 19 → 2, 5, 2, 23, 19 | 667, 741 → 693, 741 | drawn (its solve stopped at the stall floor); KKT solve 3.86 × 10⁻¹⁷ below, held at row 3 |
| 292 | grid-slack’s 0.5-degree view, row 10 | 107, 120, 109, 85, 19 → 3, 15, 0, 38, 19 | 88, 826 → 846, 870 | same-side view to review at row 7 (105 per-square counts fall, no total does); KKT solve 1.03 × 10⁻¹³ below, held at row 3 |
| 295 | grid-slack’s 0.5-degree view, row 10 | 83, 93, 126, 165, 19 → 5, 11, 0, 49, 19 | 58, 692 → 815, 897 | same-side view to review at row 7 (96 counts fall); KKT solve 4.16 × 10⁻¹⁹ below, held at row 3 |
| 299 | grid-slack’s 0.5-degree view, row 10 | 18, 40, 20, 49, 19 → 6, 20, 2, 31, 19 | 635, 773 → 775, 817 | KKT solve 6.20 × 10⁻¹⁵ below, held at row 3 |
| 307 | the axis tool’s view, decided no better | 5, 19, 2, 27, 19 (unchanged) | 709, 791 (unchanged) | KKT solve 1.34 × 10⁻¹⁵ below, held at row 3 |

- **Eleven counts drawn.** The selection takes the first adoptable view that no other
  adoptable view dominates, the driver’s views first and then grid-slack’s by rising
  threshold. At 180, 262 and 272 that is the driver’s same-side view, admitted at row 10;
  it is also better than grid-slack’s on angle classes at all three, and at 180 and 262
  on hues and both totals of shared sides.
  Elsewhere it is grid-slack’s 0.5-degree view.
  Its three thresholds drew the same view at every count but 299, where the 1- and
  5-degree runs drew one with a light and an uneven square more, two angle classes fewer
  and four more shared sides of each kind, so neither dominates and the 0.5-degree view
  is drawn. At 210 the view is better only on the house total of shared sides (500 to
  506), which the improvement rule admits.
- **270 and 307 decided no better.** At 270 grid-slack finds no view at any threshold
  (relaxed rows overlap at this side), and the driver’s only view is its KKT solve.
  At 307 grid-slack’s views at all three thresholds go to review at row 7, 11 per-square
  counts falling while no total does, and the driver’s solve is a KKT point.
  No view is adoptable at either, so the axis tool’s view stays drawn and
  `default_drawings.SETTLED` decides each count no better on its new witness (T-321’s
  and T-326’s), naming these four runs.
  210 and 272 leave `SETTLED`: both were settled on T-174’s witnesses (think-3mry), and
  both new witnesses are regularized.
- **The KKT solves.** At eight counts the driver reached a KKT local minimum below the
  certificate’s side by 4.16 × 10⁻¹⁹ (295) to 1.03 × 10⁻¹³ (292), each solved view
  verified exactly by both routes.
  Each gain exceeds the new house’s own uniform-contraction margin (the packet’s
  `measure/contraction-nNNN-own.json`): 1.46 times it at 292 (1.03 × 10⁻¹³ against 7.03
  × 10⁻¹⁴), 1.40 times at 295 (4.16 × 10⁻¹⁹ against 2.97 × 10⁻¹⁹), and about 10¹⁰ to 3 ×
  10¹² times at 260, 268, 270, 272, 299 and 307, whose margins lie near 3.4 × 10⁻²⁷. So
  under the owner’s option D (think-b0w5) each is a new result below its house (review
  A3 of #1023; `test_the_held_solves_below_the_new_houses_pass_option_d`). Each is held
  at row 3 as a register candidate and not admitted: what it waits on is registration
  and a stage 4 review, which think-4z8z carries with the project’s other candidates.
  At 270, 299 and 307 they are the points the driver held on 9 November 2026
  (think-he66, think-463r), which the owner left credited to Polkovskyi’s re-solves
  (think-frl5).
- The record’s comparison with the base branch (`default_drawings --compare`) is in the
  pull request: every count lands regularized or decided no better on its new witness,
  none pending, and no runs are owed.
- The flip record decides each new picture’s pose (`flip_regularization --check`): ten
  of the thirteen are turned, twelve decided by quadrants and 262 by `grid-4`.

## Retained Here

| Directory or file | What |
| --- | --- |
| `adopt-2026-11-18-n147-307-grid-deg05/`, `-grid-deg1/`, `-grid-deg5/` | each run’s block, `run.json`, written by `regularize_grid_slack.run_block` from its reports, and the thirteen reports, `n-<count>/report.json.gz` |
| `adopt-2026-11-18-n147-307-evand/` | the driver’s `receipt.json` and its thirteen reports |
| `selection-adopt-2026-11-18-n147-307.json.gz`, `.md` | the selection’s report and table |

The runs cost about 1,637 CPU-seconds for grid-slack’s three runs (387, 605 and 644, the
seconds their reports record, summed), 3,661 CPU-seconds for the driver by its receipt
(the solve at 210 failed and was retried at 100 digits, and the solve at 272 was retried
with the `probe-flat-stall-stop` patch), and about half a CPU-hour for the selection and
the two layers.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
