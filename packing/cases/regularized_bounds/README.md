# Regularized Views Registered as Verified Upper Bounds

This directory holds the certificates of T-155: the exact views of the regularization
run of 11 and 12 October 2026 whose sides lie below their cases’ verified upper bounds,
registered as results under the
[regularization policy](../../../docs/project/policies/regularization-policy.md) (row 3,
“register first”, and the owner’s answer to its question 3 of 12 October 2026,
“regularize and correct always”). Under `grid-slack-2026-10-13/` it holds the second
batch, T-156, the grid-slack view of $n = 290$ ([below](#the-grid-slack-batch)). Under
the policy’s question 16, as the owner answered it on 13 October 2026, a side below the
verified upper bound is registered as a result however it was made, and is a new upper
bound only where no earlier certificate stated that side exactly, as Evan Daniel’s had
at 33 of T-155’s counts, and no larger count’s verified upper bound is at or below it.
T-156’s bound was not new: T-155’s certificate at $n = 291$ is at the same side and
already implied it by monotonicity, and T-156 is kept as the certificate of $n = 290$’s
own packing at that side.
[`devtools.register_regularized_bounds`](../../devtools/register_regularized_bounds.py)
wrote everything here and holds it to the case records.

## What Is Here

| Path | What it is |
| --- | --- |
| `views/n-NNN.yaml.gz` | Each registered view, a rational centre-basis Witness/v2, byte for byte as the run wrote it, gzip-compressed |
| `selection.json` | One row per count: the view, its exact side and display, the bound the record held before and the margin, the printed side and closed form, the drawing decision, the identity measured on the retained view against the witness, and the regularization in the register’s terms; a grid-slack row also records the next count’s ceiling where it already implies the bound |
| `exact-decision.json` | Each retained view decided over $\mathbb{Q}$ by both maintained exact routes |
| `negative-controls.json` | Three mutants of each view, decided by both routes |
| `grid-slack-2026-10-13/` | The second batch (T-156), with the same four kinds of file |

## How the Views Were Chosen

The run drove Evan Daniel’s exact solver and regularizer, vendored under
[`vendor/evand-regularize/`](../../../vendor/evand-regularize/README.md) (MIT), over
every count’s known-best witness with `devtools.regularize_evand run` (`conservative`,
`coincide`, the source orientation, 80 digits), and this project’s same-side re-solve
fixed each result at the witness’s side where it could.
Each count yields up to two views, the regularizer’s certificate at the side its solve
reached (`solved`) and the same-side view at the witness’s side $s_W$ (`same`). A view
whose side lies below the case’s verified upper bound $U$ is held at row 3 of the
policy’s decision table until it is registered.

`select` read the reports of the full run and its re-runs, a later run’s report
replacing an earlier one’s at the same count, and took every count with a view at row 3
except three sets: $n = 17$, which the owner holds (think-x4v4), the 42 counts
jlevy/squares#518 re-houses, and the nine jlevy/squares#553 re-housed after the run,
whose witnesses those pull requests replace.
At each count it registered the view with the least exact side, so that no view of the
count lies below the new bound.
A later `select` records every row-3 view’s side in its row (`row_three_sides`), so the
choice can be checked without the run’s report.
This selection predates that field.
Its rows show the choice at 34 counts: at 33 one view alone was at row 3, and at one a
`solved` view was taken over the same-side view, whose side is the witness’s own and
which `--check` compares with it.
At the other 25 a `same` view was taken over a `solved` one, whose side is in the run
reports alone. It refused any report whose witness or bound was not the checkout’s.

Of 71 counts with a view at row 3, 59 are registered here and 12 are left out: $n = 17$;
70, 102, 103, 123, 126, 129, 146, 232, 267 and 295, which jlevy/squares#518 re-houses;
and 176, where #553’s certificate proves $s(176) \le 13.8128562532770564$ (T-151), below
the side of the run’s view.
At 33 counts the registered view is the regularizer’s certificate, and its side is
exactly the side of Evan Daniel’s earlier certificate of the same packing (T-101), which
the record had carried rounded up at the fourteen decimals the catalogue prints.
Those 33 bounds are previously published, in Evan Daniel’s certificates of 5 October
2026, and T-101’s replay by two checkers that share no code with each other or with the
source already proves each; there the case records cite that replay and the source’s own
beside this package’s decision, and what is new is a second certificate at the same side
and the record carrying the side exactly.
At the other 26 it is a same-side view at the witness’s side: at 25 of them
$6.6 \times 10^{-20}$ to $1.8 \times 10^{-19}$ below that certificate’s side, and at
$n = 29$ $5.4 \times 10^{-20}$ below the endpoint of the interval certificate (T-009).
Every registered side lies $5.4 \times 10^{-20}$ to $9.9 \times 10^{-15}$ below the
verified upper bound it replaces.

At 37 counts the view draws the same picture as the witness; at the other 22 it redraws
the packing. Each case record carries the registered side as its verified upper bound’s
`exact_form` and keeps the decimal it printed before as `value`, which lies above the
side and so still bounds it from above, as the records at $n = 70$ and elsewhere print a
rounded value beside a rational exact form.
The bound’s agreement with the catalogue’s printed side at the printed precision is
therefore what it was: it agrees wherever the catalogue prints a decimal alone, apart
from $n = 29$, and trails wherever the catalogue prints a closed form, which each side
lies above.

## How Each View Was Decided

`decide` decompresses each view and decides it, every pair and every wall over
$\mathbb{Q}$, by `sqpack.witness.exact_verify` on its centre-basis witness and by
`devtools.check_rational_witness_independent` on its rational corners.
The run that made the views decided them with the same two checkers, so this is a
reproduction with the producer’s code, not a second implementation.

`controls` makes three mutants of each view and decides each on both routes: the
tightest pair’s second square moved along the pair’s best separating face axis by its
gap plus one unit of the side’s denominator, doubled until the independent checker’s
pair gap is negative; the box shrunk past its least top or right clearance by that unit;
and the box shrunk by the unit alone.
Both routes must refuse the first two and accept the third wherever the clearance
exceeds the unit.
The overlap is judged by the independent checker’s own pair gap, so its
refusal of that mutant is circular; the mutant is invalid regardless, since a negative
gap on every face axis means, by the separating-axis theorem, that the two interiors
meet.

Both routes accepted all 59 views on 12 October 2026, 1,051,241 pair decisions each, in
438.4 CPU seconds for the two.
The 33 regularizer certificates clear every wall by $5 \times 10^{-21}$ and every pair
by about $10^{-20}$; the 26 same-side views touch a wall and a neighbour exactly, and
both routes accept contact, which is sound for $s(n)$. All 177 controls reached their
required outcomes on both routes (1,307.2 CPU seconds): the overlap and the shrink past
the clearance were refused at every view, and the one-unit shrink was accepted at the 33
regularizer certificates and refused at the 26 same-side views, which touch the top or
right wall. At those 26 views the least top or right clearance is 0, so the shrink past
the clearance and the one-unit shrink are the same mutant, refused under both names: the
177 decisions are of 151 distinct mutants.

## Reproduce

From `packing/`, with the project’s Python:

```bash
uv run --frozen --all-extras --group dev python -m devtools.register_regularized_bounds decide
uv run --frozen --all-extras --group dev python -m devtools.register_regularized_bounds controls
uv run --frozen --all-extras --group dev python -m devtools.register_regularized_bounds --check
```

`--batch grid-slack` after `decide` or `controls` decides the second batch.
`select` needs the run directories, which are outside the repository; the solved points
they hold are not retained here.

## The Counts

`Exact side` is the registered side, cut and rounded up where long; `Printed as` the
record’s `value`; `Below the earlier bound by` the margin under the verified upper bound
the record held before; `Below T-101’s side by` the margin under the side of Evan
Daniel’s certificate of the same packing; and `Agrees` whether the bound as printed and
the catalogue’s printed side agree at the printed precision.
`Drawing` is the run’s word for the view as a drawing, then its word once the view is
registered; the regularized layer decides the drawing on its own.

| n | View | Exact side | Printed as | Below the earlier bound by | Below T-101’s side by | Agrees | Drawing | Moved, largest |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 28 | `solved` | `5.82444461667405929702…` | `5.82444461667406` | `7.0e-16` | 0 | yes | no-change, then no-change | none |
| 29 | `same` | `5.93383346267692918969…` | `5.93383346267692918974379895098` | `5.4e-20` | — | no | held, then admit | 3, `1.3e-2` |
| 37 | `same` | `6.59861960924436011618…` | `6.59861960924437` | `9.9e-15` | `6.6e-20` | yes | held, then admit | 7, `1.7e-1` |
| 39 | `solved` | `6.81072208306864885177…` | `6.81072208306865` | `1.1e-15` | 0 | yes | held, then review | 11, `7.3e-2` |
| 41 | `same` | `6.92669309446880223159…` | `6.92669309446881` | `7.8e-15` | `6.9e-20` | yes | held, then admit | 5, `2.4e-2` |
| 50 | `same` | `7.57142857142857142858…` | `7.57142857142858` | `8.6e-15` | `7.6e-20` | no | held, then admit | 6, `9.6e-3` |
| 53 | `same` | `7.82287565553229529526…` | `7.82287565553230` | `4.7e-15` | `7.8e-20` | no | held, then refuse | 3, `3.7e-2` |
| 54 | `same` | `7.84666719284348978295…` | `7.84666719284349` | `2.2e-16` | `7.8e-20` | no | held, then admit | 8, `6.9e-2` |
| 55 | `solved` | `7.94577100750391297904…` | `7.94577100750392` | `7.0e-15` | 0 | yes | no-change, then no-change | none |
| 69 | `solved` | `8.82719465572973891502…` | `8.82719465572974` | `1.1e-15` | 0 | yes | no-change, then no-change | none |
| 71 | `same` | `8.94407155757031550657…` | `8.94407155757032` | `4.5e-15` | `8.9e-20` | yes | held, then admit | 3, `2.8e-2` |
| 83 | `solved` | `9.63475764863108202936…` | `9.63475764863109` | `8.0e-15` | 0 | yes | held, then admit | 14, `3.1e-2` |
| 87 | `solved` | `9.83881526994826226037…` | `9.83881526994827` | `7.7e-15` | 0 | yes | held, then admit | 6, `2.9e-3` |
| 101 | `same` | `10.5355339059327376221…` | `10.53553390593274` | `2.4e-15` | `1.1e-19` | no | no-change, then no-change | none |
| 104 | `solved` | `10.7071067811865475246…` | `10.70710678118655` | `2.5e-15` | 0 | no | no-change, then no-change | none |
| 107 | `solved` | `10.8466671928434897831…` | `10.84666719284349` | `2.2e-16` | 0 | no | held, then admit | 4, `1.1e-1` |
| 109 | `solved` | `10.9497474683058326710…` | `10.94974746830584` | `7.3e-15` | 0 | no | no-change, then no-change | none |
| 122 | `same` | `11.5355339059327376221…` | `11.53553390593274` | `2.4e-15` | `1.2e-19` | no | no-change, then no-change | none |
| 124 | `same` | `11.6568542494923801953…` | `11.65685424949239` | `9.8e-15` | `1.2e-19` | no | no-change, then no-change | none |
| 125 | `solved` | `11.7071067811865475246…` | `11.70710678118655` | `2.5e-15` | 0 | no | no-change, then no-change | none |
| 128 | `same` | `11.8250919682136870292…` | `11.82509196821369` | `3.0e-15` | `1.2e-19` | yes | no-change, then no-change | none |
| 145 | `same` | `12.5355339059327376221…` | `12.53553390593274` | `2.4e-15` | `1.3e-19` | no | no-change, then no-change | none |
| 147 | `same` | `12.6568542494923801953…` | `12.65685424949239` | `9.8e-15` | `1.3e-19` | no | no-change, then no-change | none |
| 148 | `same` | `12.6568542494923801953…` | `12.65685424949239` | `9.8e-15` | `1.3e-19` | no | no-change, then no-change | none |
| 149 | `solved` | `12.7071067811865475246…` | `12.70710678118655` | `2.5e-15` | 0 | no | no-change, then no-change | none |
| 151 | `solved` | `12.8228756555322952954…` | `12.82287565553230` | `4.7e-15` | 0 | no | held, then refuse | 1, `8.3e-1` |
| 170 | `solved` | `13.5355339059327376222…` | `13.53553390593274` | `2.4e-15` | 0 | no | no-change, then no-change | none |
| 171 | `solved` | `13.5714285714285714288…` | `13.57142857142858` | `8.6e-15` | 0 | no | held, then admit | 12, `2.1e-2` |
| 173 | `same` | `13.6568542494923801953…` | `13.65685424949239` | `9.8e-15` | `1.4e-19` | no | no-change, then no-change | none |
| 174 | `solved` | `13.7071067811865475246…` | `13.70710678118655` | `2.5e-15` | 0 | no | no-change, then no-change | none |
| 178 | `same` | `13.8466671928434897830…` | `13.84666719284349` | `2.2e-16` | `1.4e-19` | no | held, then admit | 16, `1.3e-1` |
| 197 | `same` | `14.5355339059327376221…` | `14.53553390593274` | `2.4e-15` | `1.5e-19` | no | no-change, then no-change | none |
| 198 | `solved` | `14.5714285714285714288…` | `14.57142857142858` | `8.6e-15` | 0 | no | held, then admit | 12, `2.1e-2` |
| 200 | `same` | `14.6568542494923801953…` | `14.65685424949239` | `9.8e-15` | `1.5e-19` | no | no-change, then no-change | none |
| 201 | `solved` | `14.7071067811865475246…` | `14.70710678118655` | `2.5e-15` | 0 | no | no-change, then no-change | none |
| 202 | `solved` | `14.7279220613578554394…` | `14.72792206135786` | `4.6e-15` | 0 | no | no-change, then no-change | none |
| 203 | `solved` | `14.7781745930520227686…` | `14.77817459305203` | `7.2e-15` | 0 | no | no-change, then no-change | none |
| 204 | `solved` | `14.8228756555322952954…` | `14.82287565553230` | `4.7e-15` | 0 | no | held, then review | not one to one |
| 205 | `solved` | `14.8244511461240882237…` | `14.82445114612409` | `1.8e-15` | 0 | yes | no-change, then no-change | none |
| 226 | `same` | `15.5355339059327376221…` | `15.53553390593274` | `2.4e-15` | `1.6e-19` | no | no-change, then no-change | none |
| 227 | `same` | `15.5710678118654752441…` | `15.57106781186548` | `4.8e-15` | `1.6e-19` | no | held, then admit | 1, `2.9e-1` |
| 229 | `same` | `15.6568542494923801953…` | `15.65685424949239` | `9.8e-15` | `1.6e-19` | no | no-change, then no-change | none |
| 230 | `solved` | `15.6829268292682926831…` | `15.68292682926830` | `7.3e-15` | 0 | no | held, then admit | 32, `3.5e-2` |
| 231 | `solved` | `15.7071067811865475246…` | `15.70710678118655` | `2.5e-15` | 0 | no | no-change, then no-change | none |
| 233 | `solved` | `15.7781745930520227686…` | `15.77817459305203` | `7.2e-15` | 0 | no | no-change, then no-change | none |
| 234 | `solved` | `15.8228756555322952955…` | `15.82287565553230` | `4.7e-15` | 0 | no | held, then admit | 6, `9.9e-2` |
| 235 | `same` | `15.8266056334285680696…` | `15.82660563342857` | `1.9e-15` | `1.6e-19` | yes | no-change, then no-change | none |
| 257 | `solved` | `16.5355339059327376222…` | `16.53553390593274` | `2.4e-15` | 0 | no | no-change, then no-change | none |
| 260 | `same` | `16.6568542494923801953…` | `16.65685424949239` | `9.8e-15` | `1.7e-19` | no | no-change, then no-change | none |
| 262 | `solved` | `16.7071067811865475246…` | `16.70710678118655` | `2.5e-15` | 0 | no | no-change, then no-change | none |
| 264 | `solved` | `16.7781745930520227686…` | `16.77817459305203` | `7.2e-15` | 0 | no | no-change, then no-change | none |
| 265 | `solved` | `16.7781745930520227686…` | `16.77817459305203` | `7.2e-15` | 0 | no | no-change, then no-change | none |
| 291 | `same` | `17.5355339059327376221…` | `17.53553390593274` | `2.4e-15` | `1.8e-19` | no | no-change, then no-change | none |
| 293 | `solved` | `17.6341463414634146344…` | `17.63414634146342` | `5.4e-15` | 0 | no | held, then admit | 27, `3.5e-2` |
| 294 | `same` | `17.6568542494923801953…` | `17.65685424949239` | `9.8e-15` | `1.8e-19` | no | no-change, then no-change | none |
| 296 | `solved` | `17.7071067811865475246…` | `17.70710678118655` | `2.5e-15` | 0 | no | no-change, then no-change | none |
| 298 | `solved` | `17.7781745930520227686…` | `17.77817459305203` | `7.2e-15` | 0 | no | held, then refuse | 2, `7.8e-1` |
| 299 | `solved` | `17.8228756555322952955…` | `17.82287565553230` | `4.7e-15` | 0 | no | held, then review | not one to one |
| 300 | `same` | `17.8241233884785434709…` | `17.82412338847855` | `6.5e-15` | `1.8e-19` | yes | no-change, then no-change | none |

## The Grid-Slack Batch

The owner wrote on 13 October 2026: “Any new upper bounds should also be recorded as
results. Pure regularization should not be considered a new result, but it is a credited
part of the frontier record” (the policy’s section 9, question 16). The policy reads it
so: a side below the case’s verified upper bound $U$ is registered as a result however
it was made, and it is a new upper bound only where no larger count’s verified upper
bound is at or below it; otherwise the result says that its bound follows by
monotonicity and names the result that proves it.
A view of [`devtools.regularize_grid_slack`](../../devtools/regularize_grid_slack.py),
this project’s port of Evan Daniel’s coincidence placement, whose side lies below $U$ is
registered so, as a batch of its own; T-156 registered the first, and its bound was not
new (below).

**The view.** The grid-slack run of 13 October 2026 at 5 degrees, recorded in the
regularized layer’s index as `grid-slack-deg5-1013-a`, made a view of $n = 290$ at the
witness’s own side,
$s_W = 70142135623730950488016887242097/4000000000000000000000000000000$, which is
$17.53553390593273762200422181052425$ exactly.
That lies `2.4e-15` below the $U$ the record held, Evan Daniel’s certificate side
rounded up at fourteen decimals (T-101), and `1.8e-19` below that certificate’s own
side. The catalogue’s closed form, $14 + (5/2)\sqrt{2}$, lies `4.8e-33` below it, so the
bound still trails the printed side.
It is the same packing certified at a tighter rational side, not a new one: no square
moves by more than `6e-31` and none turns.
Evan Daniel’s regularizer gave no view of $n = 290$ below $U$ in the full run, whose
selection does not list it.
Run again here at 0.5 degrees, the generator’s default, the generator made the same view
byte for byte.

**A bound already implied.** $s(290) \le s(291)$, since deleting a square from a packing
of 291 leaves a packing of 290 in the same square.
T-155 registered $n = 291$ on 12 October 2026 at exactly this side, so from that day its
certificate proved the bound T-156 registers, while $n = 290$’s verified upper bound
still lay above the next count’s. Review B of jlevy/squares#587 found this, deleting
square 139 from T-155’s certificate, the square the $n = 290$ witness lacks, and
deciding the rest valid on both exact routes.
The owner decided on 13 October 2026 to keep T-156 and say so: its bound follows from
T-155 by monotonicity, and the grid-slack view is a certificate of $n = 290$’s own
packing, the catalogue’s, at that side.
The selection row records the next count’s ceiling where it implies the bound
(`implied_by`), and the case record says both.

**Selection.** `select --batch grid-slack --run-dir RUN ... --n 290` decides each named
run’s view by the policy’s table against the case record’s $U$
(`regularize_grid_slack.decided`) and takes the row-3 view with the least exact side,
the first run named among equals.
Its row keys every row-3 side by run (`run_sides`, `runs_at_row_3`), where a row of the
first batch keys them by output (`row_three_sides`, `outputs_at_row_3`), and records the
witness’s own side as read from the witness (`witness_side`), which `--check` reads
again. It refuses a view of another generator, one not derived from the checkout’s
witness, one not at that witness’s own side or labelled other than the same-side view,
one whose side lies above the next count’s verified upper bound, which already proves
more than the view and whose count is registered by monotonicity instead, two runs of
one name, and a count the owner holds or another batch registers, and it writes the view
and the selection only once every refusal has run.

**Decision.** Both maintained routes accepted the view on 13 October 2026, 41,905 pair
decisions each, in 14.9 CPU seconds for the two; it touches a wall and a neighbour
exactly, and both accept contact.
The three controls reached their required outcomes (48.2 CPU seconds): the overlap and
the shrink past the clearance were refused, and so was the one-unit shrink, which at a
least clearance of 0 is the same mutant.

**Drawing.** No change, before registration and after: the view draws the same picture
as the witness, so the atlas draws nothing new at $n = 290$.

| n | View | Exact side | Printed as | Below the earlier bound by | Below T-101’s side by | Agrees | Drawing | Moved, largest |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 290 | `same` | `17.5355339059327376221…` | `17.53553390593274` | `2.4e-15` | `1.8e-19` | no | no-change, then no-change | none |

## Credit

The packings are the ones the Kingbird catalogue credits to their finders, as T-101 and
T-009 record them, and the register entry’s regularizations name those results.
The solver and the regularizer are Evan Daniel’s
([evand/square-packing](https://github.com/evand/square-packing), MIT); the run, the
same-side re-solve, the exact decisions and the registration are this project’s. T-156’s
view was made by this project’s port of his coincidence placement, not his code; the
method stays credited to him, and the regularization, the decision and the registration
are this project’s.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
