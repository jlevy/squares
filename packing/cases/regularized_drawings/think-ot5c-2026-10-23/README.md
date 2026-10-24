# Regularization Runs After the 23 October Adoption of the Algebraic Houses (think-ot5c)

These are the strong generators’ runs on the witnesses that the adoption pass of 23
October 2026 wrote once the house writer took an algebraic side (think-ot5c): PR #574’s
algebraic certificates (T-174) at 70, 153 and 207, and Evan Daniel’s exact forms of
issue 639 (T-193) at 102, 123, 258, 259, 295 and 302. Each new house best packing’s side
is irrational, the one root of an integer polynomial, and its witness states its squares
in a real number field.
The house rule regularizes each re-housed count in the pull request that adopts it
([result-import.md, “The House Rule”](../../../campaign/result-import.md#the-house-rule)).
Where the house has an algebraic side these runs cannot regularize it yet: no rational
view is `same` or `bound` at an irrational side, and no number-field view is decided on
two exact routes. So each count draws its exact house, and its regularization is still
owed, under think-mbdw.

## How They Were Run

After `adopt_houses`, `build_known_best_atlas --update --n` for the nine counts,
`regularize_axis_components --update-atlas` (which refuses a number-field witness,
`unsupported-scalar-kind`) and `default_drawings --update`, which read 70 and 295 as
regular as published and the other seven as pending.
From `packing/`, at most two processes, `nice`, on a four-core host shared with other
lanes:

```sh
N="102 123 153 207 258 259 302"
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/adopt-2026-10-23-n70-302-grid-deg05 --near-axis-degrees 0.5
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/adopt-2026-10-23-n70-302-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/adopt-2026-10-23-n70-302-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/adopt-2026-10-23-n70-302-evand --n $N --workers 2
python -m devtools.regularize_evand run --run-dir $RUNS/adopt-2026-10-23-n258-302-evand --n 258 259 302 \
  --workers 2 --timeout 2400 --regularize-timeout 2400
python -m devtools.regularize_select --evand-run $RUNS/adopt-2026-10-23-n70-302-evand \
  $RUNS/adopt-2026-10-23-n258-302-evand --grid-run $RUNS/adopt-2026-10-23-n70-302-grid-deg05 \
  $RUNS/adopt-2026-10-23-n70-302-grid-deg1 $RUNS/adopt-2026-10-23-n70-302-grid-deg5 --workers 2 \
  --output $RUNS/adopt-2026-10-23-n70-302-selection.json \
  --markdown $RUNS/adopt-2026-10-23-n70-302-selection.md
```

The grid-slack run directories carry no dot, since a run’s id takes none.
Grid-slack has no exact frame on a number-field witness, so each of its runs ends at
once with no view at all seven counts.
Evan Daniel’s driver ran first from 07:42Z to 08:48Z on a host at a load of about 25,
1,139.4 CPU seconds over 3,943 s of wall at two workers; at 258, 259 and 302 each of its
solves timed out at 600 s. The coordinator approved a second run of those three at 2,400
s, which ran at a load of about one from 15:10Z: 583.4 CPU seconds over 542 s of wall at
two workers.
That is about 0.5 CPU-hours in all, with the 685 route CPU seconds of the 18
jobs that decided T-193’s six derived witnesses over their fields, under the 40 CPU-hour
item cap. No `layer` command followed, since the selection chose no view.

## What They Decided

| n | House best packing | Outcome | Drawn now |
| --- | --- | --- | --- |
| 102 | T-193 | Evan Daniel’s regularizer solves the witness to a rational side $1.06 \times 10^{-19}$ above $U$, not drawn; grid-slack draws no view | the exact house, regularization owed (think-mbdw) |
| 123 | T-193 | His regularizer’s side is $1.16 \times 10^{-19}$ above $U$, not drawn; grid-slack draws no view | the exact house, regularization owed (think-mbdw) |
| 153 | T-174 | His regularizer’s side is $1.29 \times 10^{-19}$ above $U$, not drawn; grid-slack draws no view | the exact house, regularization owed (think-mbdw) |
| 207 | T-174 | His regularizer’s side is $1.49 \times 10^{-19}$ above $U$, not drawn; grid-slack draws no view | the exact house, regularization owed (think-mbdw) |
| 258 | T-193 | His regularizer timed out in its first run and in its second solves to a side $1.66 \times 10^{-19}$ above $U$, not drawn; grid-slack draws no view | the exact house, regularization owed (think-mbdw) |
| 259 | T-193 | As at 258, $1.66 \times 10^{-19}$ above $U$, not drawn; grid-slack draws no view | the exact house, regularization owed (think-mbdw) |
| 302 | T-193 | As at 258, $1.79 \times 10^{-19}$ above $U$, not drawn; grid-slack draws no view | the exact house, regularization owed (think-mbdw) |

Each is recorded in `default_drawings.SETTLED` on its new witness as
`regularization-owed`: not regularized, with the regularization of the exact house owed
(`owed`, naming think-mbdw).
It was first recorded as decided no better, and review A4 of #756 gave it a state of its
own, since no view was judged.
`PENDING_ALLOWED` cannot hold these counts: since the house rule it defers only a
corrected witness, and an adoption moved these houses.
At 70 and 295 the new house drawings have no uneven and no near-axis square, so they
read regular as published and no run was owed.
No view lies below a witness’s side, so there is no register candidate.

At 153, 207, 259 and 302 the strong view drawn before the adoption was a view of the
earlier rational house, which lies just above the new algebraic $U$: by
$1.57 \times 10^{-14}$, $2.42 \times 10^{-12}$, $1.56 \times 10^{-31}$ and
$1.79 \times 10^{-39}$. Each lapsed with its witness.
Whether to keep a rational view just above an algebraic $U$ was the owner’s question 13
(think-r8cn). The owner answered it on 23 October 2026: the best record is always the
record, and a regularized drawing may change the side only as a strict improvement.
So none of these views is kept, nor any of the seven row-4 sides above, and no count
gains an `ABOVE_U` exception.
At 153 and 207 the new house drawings have no uneven and no near-axis square; at 259 and
302 they have 163 and 204 uneven squares, where the lapsed views had 20 and none.

`default_drawings --compare` against `main`’s record lists each re-housed count’s
drawing before and after; its table is in the pull request.

## Files

- `adopt-2026-10-23-n70-302-evand/` and `adopt-2026-10-23-n258-302-evand/`: the driver’s
  `receipt.json` for each run and its `report.json.gz` for each count.
- `adopt-2026-10-23-n70-302-grid-{deg05,deg1,deg5}/`: each run’s block, `run.json`,
  built by `regularize_grid_slack.run_block` from its reports, and its `report.json.gz`
  files.
- `selection-adopt-2026-10-23-n70-302.json.gz` and `.md`: the selection’s report and
  table.

No views or solves are kept.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
