# Regularization Runs After the Adoption of T-238 (think-tqb5)

These are the strong generators’ runs on the witness that the adoption pass of 24
October 2026 wrote at 303: Amund Kristiansen’s dilation certificate of issue #755
(T-238), adopted as the house best packing under
[the house rule](../../../campaign/result-import.md#the-house-rule) after the
[review of 23 October 2026](../../../../docs/project/reviews/review-2026-10-23-amundsk-n303.md).
The house rule regularizes each re-housed count in the pull request that adopts it.
The new witness is another arrangement of T-230’s packing, found from it: one to one
with it, 12 squares beyond a tenth and five more tilted.

## How They Were Run

On 23 October 2026, from 17:59Z to 18:06Z, in the #755 records branch
(`claude/intake-2026-10-23-755`), after `adopt_houses` had written 303 into the pass of
24 October, and after `build_known_best_atlas --update`, `regularize_axis_components
--update-atlas --n 303` and `default_drawings --update`, which read 303 as pending.
From `packing/`, at most two processes, `nice`, on a four-core host shared with other
lanes, in run directories named as `adopt_houses` prints them but with no dot in the
grid-slack names, since a run’s id takes none:

```sh
python -m devtools.regularize_grid_slack --n 303 --run-dir $RUNS/adopt-2026-10-24-n303-grid-deg05
python -m devtools.regularize_grid_slack --n 303 --run-dir $RUNS/adopt-2026-10-24-n303-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n 303 --run-dir $RUNS/adopt-2026-10-24-n303-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/adopt-2026-10-24-n303-evand --n 303 --workers 2
python -m devtools.regularize_select --evand-run $RUNS/adopt-2026-10-24-n303-evand \
  --grid-run $RUNS/adopt-2026-10-24-n303-grid-deg05 $RUNS/adopt-2026-10-24-n303-grid-deg1 \
  $RUNS/adopt-2026-10-24-n303-grid-deg5 --workers 2 \
  --output $RUNS/adopt-2026-10-24-n303-selection.json \
  --markdown $RUNS/adopt-2026-10-24-n303-selection.md
python -m devtools.regularize_evand layer --run-dir "$(mktemp -d)" --repo-root .. \
  --grid-run $RUNS/adopt-2026-10-24-n303-grid-deg05 --grid-counts 303
```

Grid-slack took 26.8, 25.2 and 25.3 CPU seconds at 0.5, 1 and 5 degrees, as their
reports record. Evan Daniel’s driver took 239.8 CPU seconds over 258.2 s of wall at two
workers. The selection took 42 s of wall.
That is about 5.3 CPU-minutes in all, well under the 40 CPU-hour item cap.
Then `render_regularized_atlas --update`, `default_drawings --update`,
`regularized_drawings` and `render_results --update` recorded the decision.

## What They Decided

| n | Outcome | Drawn now |
| --- | --- | --- |
| 303 | Grid-slack’s view at 0.5 degrees is admitted (row 10): at the witness’s side, one to one with it, largest move 0.379, with the axis tool’s light, uneven and near-axis counts (9, 37, 0), its 46 angle classes and 19 hues, and more shared sides, 760 / 776 against 756 / 774 for the house and the stage. The 1 and 5 degree views are the same view or no better. Evan Daniel’s regularizer solves the witness to a certified KKT local minimum and gives a solved view $2.17 \times 10^{-11}$ below the witness’s side, which the selection holds as a register candidate (row 3) and never admits | grid-slack’s view |

`default_drawings --compare` against `main`’s record: 303 was drawn by the axis tool’s
view of T-230, decided no better (`SETTLED`, owing the owner’s row-7 review think-ykgh),
and is now drawn by grid-slack’s view of T-238, regularized.
No strong view gives way.
`SETTLED`’s entry at 303, decided on T-230’s witness, is removed, since the count no
longer needs it; the row-7 review it owed was of a view of T-230’s witness.

**The register candidate.** Evan Daniel’s driver re-solved the witness exactly
(`solve_status: KKT local min`, gate `certified`) to the rational side
17.909762327453569781414351410156, a view of the same packing, one to one with it, 37
squares moved. By the policy’s row 3 it is a smaller packing, to be registered as a
result through the import runbook, crediting the packing’s finder and the regularizer,
and adopted once validated.
Registering it needs a register id this pull request does not hold, so it waits in its
own bead; the driver’s receipt and report here record it, and the same command
reproduces the view.

## Files

- `adopt-2026-10-24-n303-evand/`: the driver’s `receipt.json` and its `report.json.gz`
  for 303.
- `adopt-2026-10-24-n303-grid-{deg05,deg1,deg5}/`: each run’s block, `run.json`, built
  by `regularize_grid_slack.run_block` from its report, and its `report.json.gz`.
- `selection-adopt-2026-10-24-n303.json.gz` and `.md`: the selection’s report and table;
  the table’s run directories are written as `$RUNS` here, and the report keeps them as
  run.

No views or solves are kept; the layer holds grid-slack’s view.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
