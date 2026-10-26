# Regularization of the Exact Algebraic Houses (think-mbdw)

These are the runs that regularized the seven exact algebraic houses the adoption pass
of 23 October 2026 left drawn unregularized
([think-ot5c’s runs](../think-ot5c-2026-10-23/README.md)): PR #574’s algebraic
certificates (T-174) at 153 and 207, and Evan Daniel’s exact forms of issue 639 (T-193)
at 102, 123, 258, 259 and 302. Each witness states its squares in a real number field
$\mathbb{Q}(\alpha)$, of degree 4 to 8, and its side is irrational.

The owner, 26 October 2026, having seen 302 and then 259 drawn unregularized on the home
page: “When something lands on our main rendered lists, the regularization should be
done. There’s no excuse not to, because it should be cheap to calculate.
We should do flipper regularization as well as the general regularization, and that
process should be well defined.”

## What Was Missing, and What Was Built

On 23 October grid-slack had no exact frame on a number-field witness, and Evan Daniel’s
regularizer solved each count to a rational side $1.06 \times 10^{-19}$ to
$1.79 \times 10^{-19}$ above the algebraic $U$, which the owner’s answer to question 13
does not draw. Two pieces were missing, and this pass adds both:

- **A generator for number-field witnesses.** `regularize_grid_slack` version 2 builds
  the witness’s own exact frame over its field (`regularize_same_side.exact_frame(...,
  number_field=True)`), runs its placement in binary64 as before, re-solves the
  placement’s tight contacts exactly over the field at $s_W$, and writes the view in the
  witness’s own field, with its `scalar` block.
  The re-solve’s elimination, its rows and every comparison run in `sqpack.field`’s
  arithmetic (`devtools.exact_scalars`). Version 2 also keeps each unchanged tilted
  square’s own exact rotation: at 258, four squares carry rotations a few $10^{-14}$
  degrees from square 202’s and not equal to it, and merging them onto 202’s, as version
  1 matched, moved the witness’s exact contacts by $3 \times 10^{-31}$, which no
  re-solve closed.
- **A second exact route over a number field.**
  `devtools.check_algebraic_witness_independent` decides a number-field Witness/v2 view
  from its own text and shares no arithmetic, root isolation or geometry with
  `sqpack.field` or `sqpack.witness`: its own Sturm count for the root, mean-value
  enclosures in exact rationals for signs, a gcd for a zero the enclosures cannot
  settle, and the separating-axis theorem over each near pair’s four edge normals with
  every absolute value resolved exactly.
  The policy’s obligation 1 now names it beside `exact_verify`.

#817’s `check_exact_side_packing.py` (not on `main`) was evaluated as the second route.
It decides a configuration that Evan Daniel’s Julia contact-system export states, at the
zero a Krawczyk box isolates over several half-angle tangents, and its readers are built
for that export. The views here are Witness/v2 poses over one primitive element, so the
new checker takes its method, interval enclosures to separate and an exact decision of
every touching gap, and applies it to the witness format directly.

## How They Were Run

On 26 October 2026, from `packing/`, two processes at `nice`, on a four-core host at a
load of 10 to 20 from other lanes:

```sh
python -m devtools.regularize_grid_slack --n 302 259 258 207 153 123 102 \
  --run-dir $RUNS/mbdw-2026-10-26-grid-deg05 --near-axis-degrees 0.5
python -m devtools.regularize_grid_slack --n 302 259 258 207 153 123 102 \
  --run-dir $RUNS/mbdw-2026-10-26-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n 302 259 258 207 153 123 102 \
  --run-dir $RUNS/mbdw-2026-10-26-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_select --grid-run $RUNS/mbdw-2026-10-26-grid-deg05 \
  $RUNS/mbdw-2026-10-26-grid-deg1 $RUNS/mbdw-2026-10-26-grid-deg5 --workers 2 \
  --output $RUNS/selection-mbdw-2026-10-26.json \
  --markdown $RUNS/selection-mbdw-2026-10-26.md
```

then the `layer` commands the selection printed, `render_regularized_atlas --update`,
`default_drawings --update`, `flip_regularization --update`, `regularized_drawings` and
`render_results --update`.

The 21 runs took 28.1 CPU-minutes over 40 minutes of wall; their reports record 43 to
499 seconds of wall a count, nine tenths of it the first exact route,
`sqpack.witness.exact_verify` over the field, and 1 to 12 seconds for the second.
The selection, which decides all 21 views again on both routes, took 31 minutes of wall
at two workers.

## What They Decided

Every run drew a view at the witness’s own side (`same`), which is $U$ exactly, decided
valid on both routes and admitted by row 10. At 102 to 259 the three thresholds draw the
same view, and the selection takes the half-degree one; at 302 the 5-degree view, which
straightens two more squares, dominates the others.
Each improves on the house drawing under the improvement rule and is worse on no goal:

| n | House | Field degree | Light / uneven / near-axis / classes / hues | House / stage sides | View |
| --- | --- | --- | --- | --- | --- |
| 102 | T-193 | 4 | 4 / 11 / 2 / 4 / 4 → 2 / 4 / 0 / 3 / 3 | 254 / 272 → 268 / 272 | grid-slack, 0.5° |
| 123 | T-193 | 6 | 3 / 30 / 2 / 5 / 5 → 1 / 16 / 0 / 3 / 3 | 305 / 312 → 325 / 329 | grid-slack, 0.5° |
| 153 | T-174 | 7 | 0 / 0 / 0 / 3 / 3 → 0 / 0 / 0 / 3 / 3 | 446 / 446 → 474 / 474 | grid-slack, 0.5° |
| 207 | T-174 | 5 | 0 / 0 / 0 / 3 / 3 → 0 / 0 / 0 / 3 / 3 | 640 / 640 → 662 / 662 | grid-slack, 0.5° |
| 258 | T-193 | 8 | 1 / 3 / 1 / 5 / 5 → 1 / 2 / 0 / 4 / 4 | 763 / 766 → 766 / 766 | grid-slack, 0.5° |
| 259 | T-193 | 6 | 111 / 163 / 26 / 44 / 19 → 4 / 20 / 0 / 20 / 19 | 264 / 678 → 777 / 787 | grid-slack, 0.5° |
| 302 | T-193 | 7 | 142 / 204 / 29 / 56 / 19 → 0 / 0 / 0 / 27 / 19 | 284 / 948 → 960 / 962 | grid-slack, 5° |

The table’s `side - U` column in the selection’s Markdown prints a few $10^{-61}$ either
way: that is the binary64 difference from the midpoint of $U$’s isolating interval,
$10^{-60}$ wide, and decides nothing.
The exact comparison finds every view’s side equal to $U$ (`at_most_U`, not `below_U`),
and the layer’s index, written after `VerifiedBound.difference` learned to print an
exact equality as zero, records `0.000e+00`.

No view lies below $U$, so there is no register candidate.
No square’s house or stage contact count falls against the witness.
Evan Daniel’s regularizer was not run again: its runs of 23 October are rational sides
above $U$ (row 4), and his same-side re-solve over a number field is not built.

## Files

- `mbdw-2026-10-26-grid-{deg05,deg1,deg5}/`: each run’s block, `run.json`, built by
  `regularize_grid_slack.run_block` from its reports, and its `report.json.gz` for each
  count.
- `selection-mbdw-2026-10-26.json.gz` and `.md`: the selection’s report and table.

No views are kept here; the layer holds the drawn ones.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
