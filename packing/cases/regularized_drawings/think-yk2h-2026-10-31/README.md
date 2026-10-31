# Regularization Runs on the Four Decimal Kingbird Witnesses (think-yk2h)

These are the strong generators’ runs on the house witnesses at 39, 55, 290 and 291:
decimal Kingbird witnesses (`resources/web/known-best-packings/sources.json`) that an
agent set aside on 15 October 2026 on the axis tool’s refusal alone, with no strong run
(think-y1x3’s audit; think-yk2h). The regularization gate of 26 October (#831) let them
stand without the owner’s word until 9 November 2026 (`default_drawings.UNRATIFIED`),
and the intake sweep listed each for the owner.
Its remedy was to run both strong generators on each witness and settle it, and these
runs do that. None of the four witnesses changed: this is no adoption.

## How They Were Run

On 31 October 2026, from 04:59Z to 05:36Z, in the branch
`claude/bold-ritchie-xo28us-regularize` at `main` `3978a7f61`, lane L5 of the intake
pass of that day (epic think-3guf). From `packing/`, at most two processes, `nice`, on a
four-core host shared with other lanes, in run directories no run in the index names:

```sh
RUNS=/tmp/.../runs
for t in "deg05 0.5" "deg1 1" "deg5 5"; do set -- $t
  python -m devtools.regularize_grid_slack --n 39 55 290 291 \
    --run-dir $RUNS/yk2h-2026-10-31-n39-291-grid-$1 --near-axis-degrees $2
done
python -m devtools.regularize_evand run --run-dir $RUNS/yk2h-2026-10-31-n39-291-evand \
  --n 39 55 290 291 --workers 1
python -m devtools.regularize_select --evand-run $RUNS/yk2h-2026-10-31-n39-291-evand \
  --grid-run $RUNS/yk2h-2026-10-31-n39-291-grid-deg05 $RUNS/yk2h-2026-10-31-n39-291-grid-deg1 \
  $RUNS/yk2h-2026-10-31-n39-291-grid-deg5 --workers 2 \
  --output $RUNS/yk2h-2026-10-31-n39-291-selection.json \
  --markdown $RUNS/yk2h-2026-10-31-n39-291-selection.md
python -m devtools.regularize_evand layer --run-dir $RUNS/yk2h-2026-10-31-n39-291-evand --repo-root ..
```

Grid-slack took 23.2, 23.3 and 23.3 CPU-seconds by its reports at 0.5, 1 and 5 degrees.
Evan Daniel’s driver took 1,600 s of wall at one worker on a host at a load of 3 to 7,
most of it at 290 and 291. A first selection was stopped by a container restart; the
second took 158 s of wall at two workers.
That is under half a CPU-hour in all, far under the 40 CPU-hour item cap.
`layer` admitted the view at 39; then `render_regularized_atlas --update`,
`default_drawings --update`, `flip_regularization --update`, `regularized_drawings` and
`render_results --update` recorded the decisions.

## What They Decided

| n | Grid-slack (0.5, 1, 5 degrees) | Evan Daniel’s regularizer | Drawn now |
| --- | --- | --- | --- |
| 39 | A view in the bound frame, at $U$, exactly verified on both routes, one to one, largest move $2 \times 10^{-19}$: nothing visible changes (row 10, no change) | Its solved view at $U$ changes the pose: eleven squares move, by at most 0.072, and square 26 turns, by at most 0.0033 degrees, without a recorded angle change; admitted (row 10), an exactly verified view at most $U$ replacing a numerically checked witness, worse on no goal | Evan Daniel’s view, **regularized** |
| 55 | A view in the bound frame, at $U$, exact, one to one: nothing visible changes | Its solved view at $U$, exact, one to one: nothing visible changes | the house drawing, **decided no better** |
| 290 | A view at the witness’s side, which is $U$, exact, one to one, largest move $6 \times 10^{-31}$: nothing visible changes | Its same-side view: nothing visible changes; its solved view is held at row 4, $1.75 \times 10^{-19}$ above $U$ | the house drawing, **decided no better** |
| 291 | As at 290 | As at 290 | the house drawing, **decided no better** |

The measures of each view that changes nothing are the house drawing’s: at 39, 1 light,
3 uneven and no near-axis square, with 74 / 74 house and stage sides; at 55, 2, 6 and 0
with 122 / 122; at 290, 4, 31 and 0 with 1,018 / 1,018; at 291, 4, 31 and 0 with 1,024 /
1,024. No view is below $U$, so there is no register candidate, and none goes to review.

`default_drawings --compare` against `main`’s record: 39 was drawn from its house
witness, exempt without the owner’s word, and is now drawn by Evan Daniel’s view,
regularized, with the same measures; 55, 290 and 291 keep their house drawings, now
decided no better. `SETTLED`’s four exemptions are replaced by decisions at 55, 290 and
291 on the same witnesses, and `UNRATIFIED` is empty.

**For the owner.** At 55, 290 and 291 each view is an exact packing at $U$ that the
selection leaves undrawn because nothing visible changes, so the numerically checked
house drawing stays the picture.
Whether exactness alone should earn such a view the picture is the policy’s improvement
rule to say; under today’s rule, row 10’s “no change” decides it.

## Files

- `yk2h-2026-10-31-n39-291-evand/`: the driver’s `receipt.json` and its `report.json.gz`
  for each count.
- `yk2h-2026-10-31-n39-291-grid-{deg05,deg1,deg5}/`: each run’s block, `run.json`, built
  by `regularize_grid_slack.run_block` from its reports, and its `report.json.gz` for
  each count.
- `selection-yk2h-2026-10-31-n39-291.json.gz` and `.md`: the selection’s report and
  table; the report keeps the run directories as run.

No views or solves are kept here; the view drawn at 39 is in the layer.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
