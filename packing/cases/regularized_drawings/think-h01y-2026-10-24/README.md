# Regularization Runs After the 24 October Adoption of T-231 (think-h01y)

These are the strong generators’ runs on the witness that the adoption pass of 24
October 2026 wrote at 204. That pass adopted Mykhailo Polkovskyi’s second 204 file of
issue #719 (T-231) as the house best packing, under
[the house rule](../../../campaign/result-import.md#the-house-rule), after the
[review of 23 October 2026](../../../../docs/project/reviews/review-2026-10-23-mishapolk-n204.md).
The house rule regularizes each re-housed count in the pull request that adopts it.
The new witness is T-229’s packing at its solved side, 1.48e-11 lower: Francisco Couzo’s
packing, re-solved by Polkovskyi.
The pass is dated 24 October because the pass of 23 October had already moved 204 (to
T-229), and one day’s archive holds one prior state a count.

## How They Were Run

On 23 October 2026, from 06:40Z to 06:52Z, on the records branch
`claude/intake-2026-10-23`, for the pass dated 24 October, the day its pull request is
to merge. They ran after `adopt_houses`, `adopt_houses --refresh --n 204`,
`build_known_best_atlas --update`, `regularize_axis_components --update-atlas --n 204`
and `default_drawings --update`, which read 204 as pending.
From `packing/`, at most two processes, `nice`, on a four-core host shared with other
lanes, with the run directories `adopt_houses` printed, named `-grid-deg05`,
`-grid-deg1` and `-grid-deg5` as the layer’s schema requires:

```sh
python -m devtools.regularize_grid_slack --n 204 --run-dir $RUNS/adopt-2026-10-24-n204-grid-deg05
python -m devtools.regularize_grid_slack --n 204 --run-dir $RUNS/adopt-2026-10-24-n204-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n 204 --run-dir $RUNS/adopt-2026-10-24-n204-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/adopt-2026-10-24-n204-evand --n 204 --workers 2
python -m devtools.regularize_select --evand-run $RUNS/adopt-2026-10-24-n204-evand \
  --grid-run $RUNS/adopt-2026-10-24-n204-grid-deg05 $RUNS/adopt-2026-10-24-n204-grid-deg1 \
  $RUNS/adopt-2026-10-24-n204-grid-deg5 --workers 2 \
  --output $RUNS/adopt-2026-10-24-n204-selection.json \
  --markdown $RUNS/adopt-2026-10-24-n204-selection.md
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. \
  --grid-run $RUNS/adopt-2026-10-24-n204-grid-deg05 --grid-counts 204
```

Grid-slack took 30.2, 32.4 and 32.1 CPU seconds at 0.5, 1 and 5 degrees, as their
reports record. Evan Daniel’s driver took 93.1 CPU seconds over 118.2 s of wall at two
workers. The selection took 107 s of wall and the layer step 104 s. That is about 7
CPU-minutes in all, well under the 40 CPU-hour item cap, as priced before the runs (5 to
25 CPU-minutes, `adopt_houses --dry-run`). Then `render_regularized_atlas --update`,
`default_drawings --update` and `regularized_drawings` recorded them.

## What They Decided

| n | Outcome | Drawn now |
| --- | --- | --- |
| 204 | Grid-slack’s half-degree view admitted at row 10 at the witness’s side: 6 light, 34 uneven and 6 near-axis squares, 19 classes and hues, house and stage sides 505 / 543, against 14 / 59 / 11, 24 classes and 421 / 511 for the axis tool’s view of the new witness. The 1- and 5-degree views gain the same. Evan Daniel’s same-side view is refused at row 7, a house or stage total of shared sides falling. His solve certifies the witness’s own side, `14808642830513087197802415708703/10^30`, digit for digit, so no view lies below it | grid-slack 0.5 |

`default_drawings --compare` against `main`’s record: at 204, grid-slack’s half-degree
view of T-229 (34 uneven, 6 near-axis, 505 full shared sides) gives way to grid-slack’s
half-degree view of T-231 (34 uneven, 6 near-axis, 505), regularized.
The runs decided it, so it is not pending, and no strong view gives way to a worse
drawing. These are the same figures the runs of 22 October found on T-229’s witness, as
expected of one packing re-solved by $2 \times 10^{-11}$.

## Files

- `adopt-2026-10-24-n204-evand/`: the driver’s `receipt.json` and the count’s
  `report.json.gz`.
- `adopt-2026-10-24-n204-grid-{deg05,deg1,deg5}/`: each run’s block, `run.json`, built
  by `regularize_grid_slack.run_block` from its reports, and the count’s
  `report.json.gz`.
- `selection-adopt-2026-10-24-n204.json.gz` and `.md`: the selection’s report and table.

No views, solves or drawings are kept; the layer holds the admitted view.

## Re-Dating

The pass is dated by the day its pull request merges.
If that is not 24 October 2026, the pass moves with it: the key of
`upper_bound_houses.LATER_PASSES`, the archive
`devtools/house-adoption-prior-state-2026-10-24.json.xz`, the run directories and run
ids here and in the layer’s index, this directory’s name, and the dates the writer puts
in `n-204.md`, T-229’s and T-231’s notes and `test_house_adoption.MOVED_LATER`. The
comments that date it are in `upper_bound_houses.py`, `adopt_houses.py`,
`sqpack/cli/validate.py` (`SCREEN_FINDINGS`), `test_known_best_atlas.py` and
`test_translation_escape_screen.py`, and the prose in the two packets’ READMEs, the
atlas README, `resources/README.md`, `source-coverage.yaml` and #719’s requests entry;
`release.py` dates it in the papers’ no-change record and in v0.4.22’s first
publication. `git grep -e 2026-10-24 -e '24 October'` finds every place.
`stamp_landed --apply --date` the merge day writes T-231’s `landed`, and
`release_pin --update` follows it as the last commit.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
