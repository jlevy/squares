# Regularization Runs After the Adoption of Issues 1021, 1022 and 1031 (think-78aj)

These are the strong generators’ runs on the three witnesses that the adoption of Joost
de Winter’s issues 1021, 1022 and 1031 wrote in the pass of 20 November 2026, under
[the house rule](../../../campaign/result-import.md#the-house-rule), on the accepted
verdicts of the two stage 4 reviews of 18 November 2026
([review-2026-11-18-de-winter-1021-1022.md](../../../../docs/project/reviews/review-2026-11-18-de-winter-1021-1022.md),
pull request 1033, and
[review-2026-11-18-de-winter-1031.md](../../../../docs/project/reviews/review-2026-11-18-de-winter-1031.md),
pull request 1036):

| n | House | Replaces | Adopted |
| ---: | --- | --- | --- |
| 268 | T-331 | T-320 | 20 November 2026 |
| 270 | T-332 | T-321 | 20 November 2026 |
| 299 | T-333 | T-325 | 20 November 2026 |

All three are new arrangements relative to the packing they replace and to the house
before it.

## How They Were Run

In the records branch `claude/intake-2026-11-20-import-1021`, after `adopt_houses` had
written each count, `build_known_best_atlas --update`, `regularize_axis_components
--update-atlas` on the count and `default_drawings --update`. From `packing/`, at most two
processes, on a shared host, in run directories named for the adoption’s day and its
counts, the grid-slack directories named without a dot (a run id is `^[a-z0-9-]+$`):

```sh
P=adopt-2026-11-20-n268-270
N="268 270"
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg05
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n $N --workers 2
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 2 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
```

At 268 and 270 grid-slack’s three runs ran one after another from 07:59Z to 08:09Z on 20
November and the driver from 08:09Z to 08:12Z. `adopt_houses` prints the grid-slack
directories as `-grid-0.5`, `-grid-1` and `-grid-5`; the runs were made under those
names, and the first layer wrote a run id with a dot, which the index schema refuses. The
three directories were renamed, the selection was run again on them, unchanged in every
decision, and its one `layer` command, grid-slack’s 0.5-degree run at 270, wrote the view
from an empty `--run-dir` in the lane’s scratch space. Then the guide’s render-and-record
step.

SECTION299RUN

## What They Found

[selection-adopt-2026-11-20-n268-270.md](selection-adopt-2026-11-20-n268-270.md) is the
selection’s table at 268 and 270, and its JSON beside it the full report.
The figures are light, uneven and near-axis squares, angle classes and hues, then full
shared sides (house and stage), against the axis tool’s view of the new witness:

| n | View drawn | Goals before → after | Shared sides before → after | Evan Daniel’s driver |
| ---: | --- | --- | --- | --- |
| 268 | the axis tool’s view, decided no better | 0, 0, 0, 13, 13 (unchanged) | 838, 844 (unchanged) | solved view held at row 4, 1.69 × 10⁻¹⁹ above the side |
| 270 | grid-slack’s 0.5-degree view, row 10 | 12, 36, 5, 19, 19 → 8, 21, 0, 14, 14 | 683, 724 → 735, 737 | KKT solve 4.56 × 10⁻¹⁸ below the side, held at row 3 |
ROW299

- **268 decided no better.** Grid-slack finds no view at any threshold: a re-solved
  centre moves 10.2 in the contact re-solves, and relaxed rows overlap at this side in
  the anchored ones. The driver’s solved view lies 1.69 × 10⁻¹⁹ above the side, so it is
  held at row 4. No view is adoptable, so the axis tool’s view of the new witness, which
  already has no light, uneven or near-axis square, stays drawn, and
  `default_drawings.SETTLED` decides the count no better on T-331’s witness, naming these
  four runs.
- **270 drawn.** All three grid-slack thresholds draw the same view, admitted at row 10,
  better on every goal and both totals; the 0.5-degree run’s is drawn. 270 leaves
  `SETTLED`, where the pass of 18 November had decided it on T-321’s witness.
- **The KKT solve at 270.** The driver reached a KKT local minimum 4.56 × 10⁻¹⁸ below
  T-332’s side, verified exactly by both routes. T-332’s own uniform-contraction margin is
  2.56 × 10⁻⁵⁸ (the packet’s `measure/contraction-n270-own.json`), so under the owner’s
  option D (think-b0w5) the solve would be a new result below the house. It is held at
  row 3 as a register candidate and not admitted: what it waits on is registration and a
  stage 4 review, which think-4z8z carries with the project’s other candidates.
SECTION299FOUND

## Retained Here

| Directory or file | What |
| --- | --- |
| `adopt-2026-11-20-n268-270-grid-deg05/`, `-grid-deg1/`, `-grid-deg5/` | each run’s block, `run.json`, written by `regularize_grid_slack.run_block` from its reports, and the two reports, `n-<count>/report.json.gz` |
| `adopt-2026-11-20-n268-270-evand/` | the driver’s `receipt.json` and its two reports |
| `selection-adopt-2026-11-20-n268-270.json.gz`, `.md` | the selection’s report and table |
RETAIN299

The runs at 268 and 270 cost about 572 CPU-seconds for grid-slack’s three runs (216, 178
and 178, the seconds their reports record, summed) and 324 CPU-seconds for the driver by
its receipt, with two selections of about ten to fifteen minutes’ wall each on a loaded
host.
COST299

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
