# Regularization Runs After the Adoption at 127 of Issue 1020 (think-zqot)

These are the strong generators’ runs on the witness that the pass of 18 November 2026
wrote at n = 127 when it adopted Joost de Winter’s issue-1020 certificate, under
[the house rule](../../../campaign/result-import.md#the-house-rule), on the accepted
verdicts of the two stage 4 reviews of 18 November 2026
([review-2026-11-18-de-winter-1015-1017-1020-r127b.md](../../../../docs/project/reviews/review-2026-11-18-de-winter-1015-1017-1020-r127b.md),
the review of record, pull request 1028, and
[review-2026-11-18-de-winter-1015-1017-1020.md](../../../../docs/project/reviews/review-2026-11-18-de-winter-1015-1017-1020.md),
pull request 1025):

| n | House | Replaces | Adopted |
| ---: | --- | --- | --- |
| 127 | T-330 | T-305 | 18 November 2026 |

T-330 is the last of the evening’s three stages (#1015, #1017, #1020, registered as
T-328 to T-330), each a new result under option D (think-b0w5). The new witness’s view
lapses the grid-slack view of T-305’s witness
(`grid-slack-adopt-2026-11-16-n127-305-grid-deg1`).

## How They Were Run

In the records branch `claude/intake-2026-11-18-import-1015`, at 076b4dd94, after
`adopt_houses` had written 127 and after `build_known_best_atlas --update`,
`regularize_axis_components --update-atlas --n 127` and `default_drawings --update`.
From `packing/`, at most two processes, `nice -n 19`:

```sh
P=adopt-2026-11-18-n127
python -m devtools.regularize_grid_slack --n 127 --run-dir $RUNS/$P-grid-deg05
python -m devtools.regularize_grid_slack --n 127 --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n 127 --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n 127 --workers 1
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 2 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
```

Grid-slack’s 0.5- and 1-degree runs ran side by side from 06:48Z to 06:51Z, then its
5-degree run and the driver from 06:51Z to 06:54Z. The grid-slack runs were written into
directories named `$P-grid-0.5`, `$P-grid-1` and `$P-grid-5`, the names `adopt_houses`
prints; a run id is `^[a-z0-9-]+$`, so they were renamed to the names above, which the
reports do not record, and the selection was run again over the renamed directories at
07:08Z, with the same table as the first.

## What They Found

[selection-adopt-2026-11-18-n127.md](selection-adopt-2026-11-18-n127.md) is the
selection’s table, and its JSON beside it the full report.
The figures are light, uneven and near-axis squares, angle classes and hues, then full
shared sides (house and stage), against the axis tool’s view of the new witness:

| n | View drawn | Goals | Shared sides | Evan Daniel’s driver |
| ---: | --- | --- | --- | --- |
| 127 | the axis tool’s view, decided no better | 7, 15, 2, 20, 19 | 222, 283 | same-side view refused (unmatched rotation); KKT solve 7.06 × 10⁻¹⁹ below, held at row 3 |

- **Grid-slack draws no view.** At all three thresholds every attempt’s relaxed rows
  overlap at the witness’s side, from 3 to 24 rows.
- **The driver’s KKT solve is a register candidate.** The driver solves the witness to a
  certified KKT local minimum at side 11.800793726614962238623103308879, verified
  exactly on both routes, 7.06 × 10⁻¹⁹ below T-330’s side.
  The gain is about 3.9 × 10³⁹ times the witness’s own uniform-contraction margin, 1.82
  × 10⁻⁵⁸
  ([contraction-n127-own.json](../../../resources/web/de-winter-s127-issue1020-2026-11-17/measure/contraction-n127-own.json)),
  so under option D the solve is a new result below the house.
  It is one to one with the witness (49 squares moved, the largest by 0.336), and would
  draw 1, 2, 0, 13 and 13 on the goals with 259 and 293 shared sides.
  It is held at row 3 and not admitted: it waits for registration and a stage 4 review,
  which think-4z8z carries with the project’s other candidates.
- **127 decided no better.** No view is adoptable, so the axis tool’s view stays drawn
  and `default_drawings.SETTLED` decides the count no better on its new witness
  (T-330’s), naming these four runs.
- The record’s comparison with the base branch (`default_drawings --compare`) is in the
  pull request: 127 lands decided no better on its new witness, not pending, and no runs
  are owed.
- The flip record decides the new picture’s pose (`flip_regularization --check`).

## Retained Here

| Directory or file | What |
| --- | --- |
| `adopt-2026-11-18-n127-grid-deg05/`, `-grid-deg1/`, `-grid-deg5/` | each run’s block, `run.json`, written by `regularize_grid_slack.run_block` from its report, and the report, `n-127/report.json.gz` |
| `adopt-2026-11-18-n127-evand/` | the driver’s `receipt.json` and its report |
| `selection-adopt-2026-11-18-n127.json.gz`, `.md` | the selection’s report and table |

The runs cost about 527 CPU-seconds for grid-slack’s three runs (175, 173 and 179, the
seconds their reports record, summed), 24 CPU-seconds for the driver by its receipt, and
under a minute for the two selections.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
