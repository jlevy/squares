# Regularization Runs After the Adoption of T-240 (think-bk9r)

These are the strong generators’ runs on the witnesses that the adoption pass of 25
October 2026 wrote at 268 and 303: Francisco Couzo’s certificates of issue #763 (T-240),
adopted as the house best packings under
[the house rule](../../../campaign/result-import.md#the-house-rule) after the
[review of 24 October 2026](../../../../docs/project/reviews/review-2026-10-24-couzo-n268-n303.md).
The house rule regularizes each re-housed count in the pull request that adopts it.
Each new witness refines a Kaggle notebook packing and is another arrangement than the
house it replaces: T-174’s at 268 and T-239’s at 303.

## How They Were Run

On 24 October 2026, from 14:32Z to 15:07Z, in the #763 PR B records branch
(`claude/intake-2026-10-24-issue763-pr-b`), after `adopt_houses` had written 268 and 303
into the pass of 25 October, and after `build_known_best_atlas --update`,
`regularize_axis_components --update-atlas --n 268 303` and `default_drawings --update`,
which read both counts as pending.
From `packing/`, at most two processes, `nice`, on a four-core host shared with other
lanes, in run directories named as `adopt_houses` prints them but with no dot in the
grid-slack names, since a run’s id takes none:

```sh
python -m devtools.regularize_grid_slack --n 268 303 --run-dir $RUNS/adopt-2026-10-25-n268-303-grid-deg05
python -m devtools.regularize_grid_slack --n 268 303 --run-dir $RUNS/adopt-2026-10-25-n268-303-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n 268 303 --run-dir $RUNS/adopt-2026-10-25-n268-303-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/adopt-2026-10-25-n268-303-evand --n 268 303 --workers 1
python -m devtools.regularize_select --evand-run $RUNS/adopt-2026-10-25-n268-303-evand \
  --grid-run $RUNS/adopt-2026-10-25-n268-303-grid-deg05 $RUNS/adopt-2026-10-25-n268-303-grid-deg1 \
  $RUNS/adopt-2026-10-25-n268-303-grid-deg5 --workers 2 \
  --output $RUNS/adopt-2026-10-25-n268-303-selection.json \
  --markdown $RUNS/adopt-2026-10-25-n268-303-selection.md
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. \
  --grid-run $RUNS/adopt-2026-10-25-n268-303-grid-deg05 --grid-counts 268 303
```

The grid-slack runs were made in directories named `grid-0.5`, `grid-1` and `grid-5` and
renamed before the selection read them; no report records its directory.
Grid-slack took 24.2, 20.0 and 28.4 CPU seconds at 0.5, 1 and 5 degrees, as their
reports record. Evan Daniel’s driver took 1,708 CPU seconds over 1,982 s of wall at one
worker: 387 at 268 and 1,321 at 303, where the first solve and the stall-stop retry each
timed out at 600 s and the first-pass rung finished it.
The selection took 50 s of wall at two workers, and the layer 25 s. That is about 31
CPU-minutes in all, inside the triage’s 10 to 50 and well under the 40 CPU-hour item
cap. Then `render_regularized_atlas --update`, `default_drawings --update`,
`flip_regularization --update`, `regularized_drawings` and `render_results --update`
recorded the decision.

## What They Decided

| n | Outcome | Drawn now |
| --- | --- | --- |
| 268 | Grid-slack’s view at 0.5 degrees is admitted (row 10): at the witness’s side, one to one with it, largest move 0.400, better than the axis tool’s view of the new witness on every goal: light, uneven and near-axis squares 20, 37 and 6 to 5, 19 and 0, angle classes and hues 14 and 14 to 9 and 9, sides 676 / 729 to 751 / 753. The 1 and 5 degree views are no better. Evan Daniel’s regularizer solves the witness to a certified KKT local minimum $4.48 \times 10^{-12}$ below its side (row 3, a register candidate, never admitted), and its same-side view goes to review (row 7: eight squares’ contact counts fall while no total does) | grid-slack’s view |
| 303 | Grid-slack’s view at 0.5 degrees is admitted (row 10): at the witness’s side, one to one with it, largest move 0.098, with no light, uneven or near-axis square against the axis tool’s 14, 28 and 8, 19 angle classes against 27, and house sides 848 against 736, worse on no goal. The 1 and 5 degree views are the same view. Evan Daniel’s regularizer, on its first-pass rung, solves the witness to a KKT local minimum whose own certificate fails at its relaxed gate, and gives a view $3.63 \times 10^{-12}$ below the witness’s side that all three exact routes here accept (row 3, a register candidate, never admitted); its same-side view is refused for overlap | grid-slack’s view |

`default_drawings --compare` against `main`’s record: 268 was T-174’s house drawing,
decided no better (`SETTLED`), and is now drawn by grid-slack’s view of T-240,
regularized; 303 was drawn by grid-slack’s view of T-239 and is now drawn by
grid-slack’s view of T-240, regularized, with 0 uneven squares against 37 and 848 shared
sides against 760. No strong view gives way to a worse drawing.
`SETTLED`’s entry at 268, decided on T-174’s witness, is removed.

**The review queue.** Evan Daniel’s same-side view at 268 (row 7) is listed for the
owner in the adopting pull request; it is not drawn, and the count is settled on
grid-slack’s view meanwhile.

**The register candidates.** At 268 the regularizer’s certified solve reaches
8437180857934672912242411148233/(5 × 10²⁹), exactly the side of Evan Daniel’s later
certificate at `evand/square-packing@8a8879a`, whose import as reported is think-l49q’s:
that report states this side first, so the view proves no bound beyond it.
At 303 its first-pass solve, whose KKT certificate fails at the relaxed gate, gives a
view at 8953489116897633490914356559681/(5 × 10²⁹), $3.63 \times 10^{-12}$ below T-240,
which all three exact routes here accept: a smaller packing by the policy’s row 3.
Registering either needs a register id this pull request does not hold, as think-8r5w’s
did at 303 before. think-20oj registers both: the 303 view as a smaller packing, and the
268 view with `first_certified_in: T-242`, Daniel’s certificate, once T-242 is on
`main`, since that certificate states the side first.
The driver’s receipt and reports here record both, and the same commands reproduce the
views.

## Files

- `adopt-2026-10-25-n268-303-evand/`: the driver’s `receipt.json` and its
  `report.json.gz` for 268 and 303.
- `adopt-2026-10-25-n268-303-grid-{deg05,deg1,deg5}/`: each run’s block, `run.json`,
  built by `regularize_grid_slack.run_block` from its reports, and its `report.json.gz`
  for 268 and 303.
- `selection-adopt-2026-10-25-n268-303.json.gz` and `.md`: the selection’s report and
  table; the table’s run directories are written as `$RUNS` here, and the report keeps
  them as run.

No views or solves are kept; the layer holds grid-slack’s views.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
