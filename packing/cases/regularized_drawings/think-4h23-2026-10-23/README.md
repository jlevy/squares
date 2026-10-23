# Regularization Runs After the 23 October Adoption of T-229 (think-4h23)

These are the strong generators’ runs on the witnesses that the adoption pass of 23
October 2026 wrote: Mykhailo Polkovskyi’s re-solves of issue #719 (T-229), adopted as
the house best packings at 105 and 204 under
[the house rule](../../../campaign/result-import.md#the-house-rule) after the
[review of 22 October 2026](../../../../docs/project/reviews/review-2026-10-22-mishapolk-719.md).
The house rule regularizes each re-housed count in the pull request that adopts it.
At 105 the new witness re-solves T-174’s packing (Ryan Xu’s, as Francisco Couzo and
PingYou Ltd refined it), and at 204 Evan Daniel’s display regularization of Couzo’s
packing (T-225).

## How They Were Run

On 22 October 2026, from 14:06Z to 14:10Z, in the stage 4 branch
(`claude/intake-2026-10-22-stage4`), for the pass dated 23 October, the day its pull
request merges. They ran after `adopt_houses`, `build_known_best_atlas --update`,
`regularize_axis_components --update-atlas --n 105 204` and `default_drawings --update`,
which read both counts as pending.
From `packing/`, at most two processes, `nice`, on a four-core host shared with other
lanes, with the run directories `adopt_houses` printed:

```sh
python -m devtools.regularize_grid_slack --n 105 204 --run-dir $RUNS/adopt-2026-10-23-n105-204-grid-0.5
python -m devtools.regularize_grid_slack --n 105 204 --run-dir $RUNS/adopt-2026-10-23-n105-204-grid-1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n 105 204 --run-dir $RUNS/adopt-2026-10-23-n105-204-grid-5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/adopt-2026-10-23-n105-204-evand --n 105 204 --workers 2
python -m devtools.regularize_select --evand-run $RUNS/adopt-2026-10-23-n105-204-evand \
  --grid-run $RUNS/adopt-2026-10-23-n105-204-grid-0.5 $RUNS/adopt-2026-10-23-n105-204-grid-1 \
  $RUNS/adopt-2026-10-23-n105-204-grid-5 --workers 2 \
  --output $RUNS/adopt-2026-10-23-n105-204-selection.json \
  --markdown $RUNS/adopt-2026-10-23-n105-204-selection.md
```

Grid-slack took 22.3, 23.2 and 23.6 CPU seconds at 0.5, 1 and 5 degrees, as their
reports record. Evan Daniel’s driver took 165.7 CPU seconds over 109.9 s of wall at two
workers. The selection took 49 s of wall.
That is about 4 CPU-minutes in all, well under the 40 CPU-hour item cap.
The two `layer` commands the selection printed admitted the chosen views under run ids
the layer’s schema refuses, since a run’s id takes no dot, so the three grid
directories, named as `adopt_houses` prints them, were renamed `-grid-deg05`,
`-grid-deg1` and `-grid-deg5`, as the passes of 19 to 22 October named theirs.
The two dotted run blocks were taken out of the index and the same two `layer` commands
admitted the same views again under the new ids; the views and decisions are unchanged,
and the selection’s report, kept as it ran, names the directories by their first names.
Then `render_regularized_atlas --update`, `default_drawings --update` and
`regularized_drawings` recorded them.

## What They Decided

| n | Outcome | Drawn now |
| --- | --- | --- |
| 105 | Grid-slack’s 1-degree view admitted at row 10 at the witness’s side: 3 light, 8 uneven and 0 near-axis squares, 13 classes and hues, house and stage sides 223 / 241, against 3 / 8 / 0, 14 classes and 215 / 233 for the axis tool’s view of the new witness, the drawing when the selection ran. The 5-degree view gains the same; the half-degree view gains only the totals. Evan Daniel’s same-side and solved views are refused at row 7, a house or stage total of shared sides falling; his solved view is at the witness’s side | grid-slack 1 |
| 204 | Grid-slack’s half-degree view admitted at row 10 at the witness’s side: 6 light, 34 uneven and 6 near-axis squares, 19 classes, house and stage sides 505 / 543, against 14 / 59 / 11, 24 classes and 421 / 511 for the axis tool’s view of the new witness. The 1- and 5-degree views gain the same. Evan Daniel’s same-side view is refused at row 7. His solved view lies $1.48 \times 10^{-11}$ below the witness’s side (row 3), held and not drawn: see below | grid-slack 0.5 |

`default_drawings --compare` against the base branch’s record (#722’s,
`claude/intake-2026-10-22`):

- 105: grid-slack’s 1-degree view of T-174 (7 uneven, 0 near-axis, 226 full shared
  sides), which the adoption of 17 October drew, gives way to grid-slack’s 1-degree view
  of T-229 (8 uneven, 0 near-axis, 223), regularized: worse on uneven squares, angle
  classes, hues and the house and stage totals of full shared sides.
  The runs decided it, so it is not pending; by the house rule the smaller packing is
  kept.
- 204: the house drawing of T-225 (34 uneven, 6 near-axis, 509), decided no better,
  gives way to grid-slack’s half-degree view of T-229 (34 uneven, 6 near-axis, 505),
  regularized.

`SETTLED`’s entry at 204, decided on T-225’s witness by the runs of 22 October, leaves
the list: 204 is regularized now.

**At 204, the author’s own publication.** Evan Daniel’s regularizer solved T-229’s 204
witness to the exact side $14808642830513087197802415708703/10^{30}$,
$1.48 \times 10^{-11}$ below T-229’s. That is, byte for byte, the header side of the
release’s other 204 file, `certificates/n204.cert` at
`Mishapolk/square-packing-records@12fc4667`, which the
[#719 packet](../../../resources/web/mishapolk-issue719-2026-10-22/README.md) pins by
digest only. That side was first published at `1851c2c7` (22 October 2026, 05:29:48Z),
the commit that also first published `n-204.cert`, the certificate T-229 cites; the path
held his larger 204 sides from 13 October (`8bb41af5`, then `70a033f0` on 14 October).
The repository is watched, so the side is already Polkovskyi’s report: the view
reproduces his own publication, in the same commit as T-229’s certificate, and the
credit is his. The run is corroborating evidence, not a result of this project, and is
not registered or drawn.
think-h01y derives and replays `n204.cert`, records it under his credit (T-229 stating
the smaller side, or an entry of its own), then takes it through stage 4 and adoption at
204\. The project’s solved view of T-225 at 204, $8.91 \times
10^{-12}$ below T-225 (think-13e9), lies above T-229 and is superseded by its adoption.

## Files

- `adopt-2026-10-23-n105-204-evand/`: the driver’s `receipt.json` and each count’s
  `report.json.gz`.
- `adopt-2026-10-23-n105-204-grid-{deg05,deg1,deg5}/`: each run’s block, `run.json`,
  built by `regularize_grid_slack.run_block` from its reports, and each count’s
  `report.json.gz`.
- `selection-adopt-2026-10-23-n105-204.json.gz` and `.md`: the selection’s report and
  table.

No views, solves or drawings are kept; the layer holds the admitted views.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
