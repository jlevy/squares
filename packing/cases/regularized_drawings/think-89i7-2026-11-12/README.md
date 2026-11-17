# Regularization Runs After the Adoption of Issue 959 (think-89i7)

These are the strong generators’ runs on the witness that the adoption of Doğa Özden’s
issue 959 wrote at 179, under
[the house rule](../../../campaign/result-import.md#the-house-rule), after the stage 4
review of 11 November 2026
([review-2026-11-12-ozden-959.md](../../../../docs/project/reviews/review-2026-11-12-ozden-959.md)):

| n | House | Replaces | Adopted |
| ---: | --- | --- | --- |
| 179 | T-294 | T-291 | 12 November 2026 |

The house is a further arrangement of T-291’s packing, the same author’s issue 954,
adopted the day before and regularized in
[think-f65n-2026-11-11](../think-f65n-2026-11-11/README.md).
The adoption is a pass of its own day, since the pass of 11 November had already moved
179 and a day’s archive holds one prior state a count.

## How They Were Run

In the records branch `claude/bold-ritchie-xo28us-l107`, after `adopt_houses` had
written the count, and after `build_known_best_atlas --update`,
`regularize_axis_components --update-atlas --n 179` and `default_drawings --update`.
From `packing/`, at most two processes, `nice -n 19`, in run directories named for the
adoption’s day and its count, with no dot in the grid-slack names (the layer index
refuses a dot in a run id):

```sh
N=179; P=adopt-2026-11-12-n179
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg05
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n $N --workers 1
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 2 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
```

Then the one `layer` command the selection printed, for Evan Daniel’s driver, and the
guide’s render-and-record step.
The axis tool’s refresh replaced its index entry at 179, its view of T-291’s witness,
with its view of the new witness, so the selection was measured against a drawing of the
new witness.

## What They Found

[selection-adopt-2026-11-12-n179.md](selection-adopt-2026-11-12-n179.md) is the
selection’s table, and its JSON beside it the full report.
The view is drawn at the witness’s side, admitted at row 10, and better on every goal it
changes; the figures are light, uneven and near-axis squares, angle classes and hues,
then full shared sides (house and stage), the drawing before against the view:

| n | View drawn | Goals before → after | Shared sides before → after | KKT solve below the side (row 3, held) |
| ---: | --- | --- | --- | --- |
| 179 | Evan Daniel’s same-side view | 6, 11, 5, 17, 17 → 0, 0, 0, 4, 4 | 497, 530 → 552, 552 | 2.645 × 10⁻¹² |

- Grid-slack’s runs at 1 and 5 degrees were admitted at row 10 as well, and its run at
  0.5 degrees went to review at row 7. None is chosen: Evan Daniel’s view is taken first
  and no other view dominates it.
- Evan Daniel’s certified KKT solve lies 2.645 × 10⁻¹² below the side, at
  13880960371555579594835501178639/10³⁰, which is s(70) + 5 + 1.4 × 10⁻¹⁹. That is about
  the certificate’s own contraction margin (2.566 × 10⁻¹²), and it is the s(70) + 5
  configuration the review’s F9 measures.
  It is held at row 3 as a register candidate, not admitted, as at 156, 172, 180, 199,
  268, 269 and 270 and at 179 for T-291; its registration is RV-3’s (think-ruu2,
  think-ikku), and nothing here registers it.
- The flip record decides the new picture’s pose again (`flip_regularization --n 179`):
  the published pose.

## Retained Here

| Directory or file | What |
| --- | --- |
| `adopt-2026-11-12-n179-grid-deg05/`, `-grid-deg1/`, `-grid-deg5/` | each run’s `run.json`, written from its report, and the report, `n-179/report.json.gz` |
| `adopt-2026-11-12-n179-evand/` | the driver’s `receipt.json` and its report |
| `selection-adopt-2026-11-12-n179.json.gz`, `.md` | the selection’s report and table |

The runs cost about 26 CPU-seconds for grid-slack’s three runs, 49.0 CPU-seconds for the
driver by its receipt, and about a minute of wall for the selection.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
