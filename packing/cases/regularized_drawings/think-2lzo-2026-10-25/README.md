# Regularization Runs After the Adoption of T-243 at 182 (think-2lzo)

These are the strong generators’ runs on the witness that the adoption pass of 25
October 2026 wrote at 182: Evan Daniel’s certificate `s182-1024.cert` at
`evand/square-packing@d99925d` (T-243, issue 806), adopted as the house best packing
under [the house rule](../../../campaign/result-import.md#the-house-rule) after the
[review of 25 October 2026](../../../../docs/project/reviews/review-2026-10-25-evand-n182.md).
The house rule regularizes each re-housed count in the pull request that adopts it.
The new witness is Daniel’s packing from an L-cut of Francisco Couzo’s 211 packing
(T-188), an arrangement of Daniil Ostashev’s design, and another arrangement than
T-174’s, the house it replaces.

## How They Were Run

On 25 October 2026, from 06:44Z to 06:58Z, in the records branch
`claude/intake-2026-10-25-issue806-n182`, after `adopt_houses` had written 182 into the
pass of 25 October, and after `build_known_best_atlas --update --n 182`,
`regularize_axis_components --update-atlas --n 182` and `default_drawings --update`,
which read 182 as pending.
From `packing/`, at most two processes, `nice`, on a four-core host shared with other
lanes, in run directories named as `adopt_houses` prints them but with no dot in the
grid-slack names, since a run’s id takes none:

```sh
python -m devtools.regularize_grid_slack --n 182 --run-dir $RUNS/adopt-2026-10-25-n182-grid-deg05
python -m devtools.regularize_grid_slack --n 182 --run-dir $RUNS/adopt-2026-10-25-n182-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n 182 --run-dir $RUNS/adopt-2026-10-25-n182-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/adopt-2026-10-25-n182-evand --n 182 --workers 1
python -m devtools.regularize_select --evand-run $RUNS/adopt-2026-10-25-n182-evand \
  --grid-run $RUNS/adopt-2026-10-25-n182-grid-deg05 $RUNS/adopt-2026-10-25-n182-grid-deg1 \
  $RUNS/adopt-2026-10-25-n182-grid-deg5 --workers 2 \
  --output $RUNS/adopt-2026-10-25-n182-selection.json \
  --markdown $RUNS/adopt-2026-10-25-n182-selection.md
python -m devtools.regularize_evand layer --run-dir $RUNS/adopt-2026-10-25-n182-evand --repo-root ..
```

Grid-slack took 106.4, 106.5 and 109.5 CPU seconds by its reports at 0.5, 1 and 5
degrees.
Evan Daniel’s driver took 263 CPU seconds over 266 s of wall at one worker: 30 s
to solve, 11 s to regularize and 219 s for the same-side view.
The selection took 222 s of wall at two workers, at most 7.4 CPU-minutes.
That is 10 to 17 CPU-minutes in all, well under the 40 CPU-hour item cap.
The selection admitted one view, so `layer` ran once; then
`render_regularized_atlas --update`, `default_drawings --update`,
`flip_regularization --update`, `regularized_drawings` and `render_results --update`
recorded it, and `SETTLED`’s entry at 182, made on T-174’s witness, was removed.

## What They Decided

| n | Outcome | Drawn now |
| --- | --- | --- |
| 182 | Evan Daniel’s regularizer solves the witness to a certified KKT local minimum and draws a same-side view, one to one with the witness, 49 squares moved, the largest by 0.381, admitted at row 10. Grid-slack’s view, the same at all three thresholds, is at the witness’s side too, one to one, largest move 0.263, also admitted at row 10. The selection takes the regularizer’s, which no other adoptable view dominates: against the axis tool’s view of the witness it keeps 2 light, 4 uneven and no near-axis squares, and has fewer angle classes and hues (15 and 15 against 20 and 19) and more full shared sides (429 and 455 against 409 and 441, house and stage). No view is below the house, so there is no register candidate | Evan Daniel’s regularizer’s view |

Measured pose by pose (`devtools.measure_identity`), the drawn view is the source’s own
display view, `s182-1024_regularized.cert` in the
[packet](../../../resources/web/evand-n182-2026-10-25/README.md), to
$1.9 \times 10^{-19}$: Evan Daniel’s regularizer at `675a5ea`, which the layer runs,
reproduces the view his source published beside the certificate.
It is a pure regularization at the house’s side and proves no other bound.

`default_drawings --compare` against `main`’s record: 182 was drawn by the house drawing
of T-174’s witness, decided no better (`SETTLED`), with 12 uneven and no near-axis
squares and 443 full shared sides, and is now drawn by Evan Daniel’s regularizer’s view
of T-243’s witness, regularized, with 4 uneven, no near-axis squares and 429 full shared
sides. No strong view gives way to a worse drawing.

## Files

- `adopt-2026-10-25-n182-evand/`: the driver’s `receipt.json` and its `report.json.gz`
  for 182.
- `adopt-2026-10-25-n182-grid-{deg05,deg1,deg5}/`: each run’s block, `run.json`, built
  by `regularize_grid_slack.run_block` from its report, and its `report.json.gz` for
  182\.
- `selection-adopt-2026-10-25-n182.json.gz` and `.md`: the selection’s report and table;
  the report keeps the run directories as run.

The drawn view is in the layer,
`atlas/known-best/regularized/n-182-regularized.yaml.gz`; no other views or solves are
kept.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
