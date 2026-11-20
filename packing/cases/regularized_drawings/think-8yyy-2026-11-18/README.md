# Regularization Runs After the Adoption at 172 and 199 (think-8yyy)

These are the strong generators’ runs, of 18 November 2026, on the two witnesses that
the adoption at 172 and 199 wrote under
[the house rule](../../../campaign/result-import.md#the-house-rule), once the owner’s
option D of 17 November 2026 (think-b0w5) made Joost de Winter’s re-solves new results:
each is below its predecessor’s certificate shrunk until its squares first touch, 1.0399
of the margin T-282’s certificate carries.
The stage 4 review of 11 November 2026
([review-2026-11-11-de-winter-939-946.md](../../../../docs/project/reviews/review-2026-11-11-de-winter-939-946.md))
accepts both certificates.

| n | House | Replaces | Adopted |
| ---: | --- | --- | --- |
| 172 | T-286, issue 946 | T-282 | 21 November 2026 |
| 199 | T-285, issue 939 | T-284 | 21 November 2026 |

The adoption was written on 18 November and moved to the pass of 21 November 2026, the
day the branch merges, since a day’s archive holds one prior state a count; the
witnesses it writes are built from the retained packets and did not change, so these
runs and their directory names stand.

## How They Were Run

In lane w7-optd-1118’s records branch, after `adopt_houses` had written both counts,
`build_known_best_atlas --update --n 172 199`,
`regularize_axis_components --update-atlas --n 172 199` and `default_drawings --update`.
From `packing/`, at most two processes, `nice -n 19`, `PACK_JOBS=2`, in run directories
named for the adoption’s day and its lowest and highest count, the grid-slack
directories named without a dot:

```sh
P=adopt-2026-11-18-n172-199
python -m devtools.regularize_grid_slack --n 172 199 --run-dir $RUNS/$P-grid-deg05
python -m devtools.regularize_grid_slack --n 172 199 --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n 172 199 --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n 172 199 --workers 1
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 2 \
  --output $RUNS/$P-selection.json --markdown $RUNS/$P-selection.md
```

Grid-slack’s three runs ran one after another beside the driver, on 18 November between
03:55Z and 04:03Z. Then the selection’s two `layer` commands, the driver’s from its run
and grid-slack’s 0.5-degree run at 199 from an empty `--run-dir` in the lane’s scratch
space, and the guide’s render-and-record step.
Grid-slack’s reports record 111, 119 and 159 CPU-seconds; the driver’s receipt records
455 seconds of wall time at one worker.

## What They Found

[selection-adopt-2026-11-18-n172-199.md](selection-adopt-2026-11-18-n172-199.md) is the
selection’s table, and its JSON beside it the full report.
The figures are light, uneven and near-axis squares, angle classes and hues, then full
shared sides (house and stage), against the axis tool’s view of the new witness:

| n | View drawn | Goals before → after | Shared sides before → after |
| ---: | --- | --- | --- |
| 172 | Evan Daniel’s driver’s same-side view, row 10 | 12, 31, 6, 18, 18 → 1, 3, 0, 3, 3 | 394, 455 → 511, 511 |
| 199 | grid-slack’s 0.5-degree view, row 10 | 14, 37, 6, 18, 18 → 3, 10, 0, 12, 12 | 490, 550 → 584, 598 |

Both views are at their witnesses’ sides, so no drawing proves another bound.
The driver refused its view at 199 at row 7. Its solve of each witness reached the side
the witness states: no register candidate.
At 172 that is T-286’s own point, the exact local optimum of T-282’s arrangement that
the driver reached from T-282’s witness on 9 November (think-wju3). Against `main`’s
record before the adoption, both counts were regularized on the earlier witnesses and
are regularized again on the new ones, with the same view at 172 and 36 more shared
sides at 199 (`default_drawings --compare`).

## Files

- `adopt-2026-11-18-n172-199-evand/`: the driver’s `receipt.json` and each count’s
  `report.json.gz`.
- `adopt-2026-11-18-n172-199-grid-{deg05,deg1,deg5}/`: each run’s block, `run.json`
  (`regularize_grid_slack.run_block`), and each count’s `report.json.gz`.
- `selection-adopt-2026-11-18-n172-199.{json.gz,md}`: the selection’s report and table.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
