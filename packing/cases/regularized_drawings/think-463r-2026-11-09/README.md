# Regularization Runs After the Adoption of Issues 927 to 931 (think-463r)

These are the strong generators’ runs on the five witnesses that the adoption of Doğa
Özden’s further arrangements of issues 927 to 931 wrote, under
[the house rule](../../../campaign/result-import.md#the-house-rule), after the stage 4
review of 9 November 2026
([review-2026-11-09-ozden-927-931-five.md](../../../../docs/project/reviews/review-2026-11-09-ozden-927-931-five.md)):

| n | House | Replaces | Adopted |
| ---: | --- | --- | --- |
| 232 | T-275 | T-256 | 9 November 2026 |
| 268 | T-276 | T-270 | 9 November 2026 |
| 299 | T-277 | T-263 | 9 November 2026 |
| 303 | T-278 | T-272 | 9 November 2026 |
| 307 | T-279 | T-256 | 9 November 2026 |

## How They Were Run

In the records branch `claude/bold-ritchie-xo28us-l63` (#932), after `adopt_houses` had
written the five counts, and after `build_known_best_atlas --update`,
`regularize_axis_components --update-atlas --n 232 268 299 303 307` and
`default_drawings --update`, which read all five as pending.
From `packing/`, at most two processes, `nice -n 19` on two cores, on a four-core host
shared with another lane, in the run directories `adopt_houses` printed, with no dot in
the grid-slack names:

```sh
N="232 268 299 303 307"; P=adopt-2026-11-09-n232-307
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg05 --near-axis-degrees 0.5
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n $N --run-dir $RUNS/$P-grid-deg5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/$P-evand --n $N --workers 2
python -m devtools.regularize_select --evand-run $RUNS/$P-evand \
  --grid-run $RUNS/$P-grid-deg05 $RUNS/$P-grid-deg1 $RUNS/$P-grid-deg5 --workers 2 \
  --output $RUNS/selection-$P.json --markdown $RUNS/selection-$P.md
```

Then the three `layer` commands the selection printed: grid-slack’s 0.5-degree run at
232 and 303, its 1-degree run at 299 and its 5-degree run at 268. Then
`build_known_best_atlas --update` again, `render_regularized_atlas --update`,
`default_drawings --update`, `flip_regularization --update`, `regularized_drawings` and
`render_results --update`.

By the receipts:

- Grid-slack took 210.52, 229.16 and 270.30 seconds at 0.5, 1 and 5 degrees, the
  per-count seconds its reports record, summed; each run’s `run.json` here is its block
  in the layer’s index.
- Evan Daniel’s driver took 1,730.10 CPU seconds over 1,130.15 s of wall at two workers,
  by its `receipt.json`.
- The selection writes no cost.
  It took 306 s of wall at two workers, so at most 10.2 CPU-minutes.

That is about 51 CPU-minutes in all (2,440 receipt seconds and at most 612 for the
selection), under the 40 CPU-hour item cap.

## What They Decided

| n | Outcome | Drawn now |
| ---: | --- | --- |
| 232 | Grid-slack’s 0.5-degree view, admitted: light, uneven and near-axis squares, angle classes and hues 4, 14, 0, 27 and 19 against the axis tool’s 18, 86, 9, 36 and 19, and 538 and 572 full shared sides against 395 and 550 | grid-slack’s 0.5-degree view |
| 268 | Grid-slack’s 5-degree view, admitted: 0, 0, 0, 27 and 19 against 11, 77, 12, 40 and 19, and 653 and 723 full shared sides against 492 and 677 | grid-slack’s 5-degree view |
| 299 | Grid-slack’s 1-degree view, admitted: 5, 11, 1, 29 and 19 against 28, 57, 22, 52 and 19, and 771 and 829 full shared sides against 586 and 739 | grid-slack’s 1-degree view |
| 303 | Grid-slack’s 0.5-degree view, admitted: 0, 0, 0, 40 and 19 against 61, 137, 19, 59 and 19, and 734 and 814 full shared sides against 374 and 769 | grid-slack’s 0.5-degree view |
| 307 | Decided no better (`SETTLED`): grid-slack’s views at all three thresholds go to review at row 7, 13 per-square counts falling while no total does | the axis tool’s view |

Every admitted view is at its witness’s side, so no drawing proves another bound.
At all five counts Evan Daniel’s regularizer solved the witness to a certified KKT point
below its side, by 3.30 to 3.53 × 10⁻¹² (232: 3.37, 268: 3.30, 299: 3.53, 303: 3.48,
307: 3.48), and the selection held each at row 3 as a register candidate: a smaller
packing is registered and reviewed as a result of its own first, and is never admitted
here. Nothing here registers them;
[The Held Points Under Option D](#the-held-points-under-option-d) says what each is now.
The strong views of the earlier witnesses lapsed with the houses; each count is decided
here on its new witness, so nothing is owed.

## The Held Points Under Option D

The owner’s option D of 17 November 2026 (think-b0w5) settles the question the five held
points waited on (think-5c9z): a re-certification of a standing packing is a new result
only if its side is below its predecessor’s once the predecessor is shrunk until its
squares first touch (`devtools.contraction_margin`). On 18 November 2026 lanes
w7-optd-1118 and w7r2-optd-1118 (think-8yyy) measured each point against the house it
was solved from. The table compares the points with the current houses, including the
adoptions at 268 and 299 in the pass of 20 November.

| n | Solved from | That house’s margin | Gain | Share | The house now | Disposition |
| ---: | --- | ---: | ---: | ---: | --- | --- |
| 232 | T-275 | 2.997814e-12 | 3.372932e-12 | 1.1251 | T-307, 1.88e-3 below the point | no candidate |
| 268 | T-276 | 3.192868e-12 | 3.295234e-12 | 1.0321 | T-331, below the point | no candidate |
| 299 | T-277 |  |  |  | T-333, below the point | no candidate |
| 303 | T-278 | 3.402014e-12 | 3.481634e-12 | 1.0234 | T-278, above the point | candidate |
| 307 | T-279 |  |  |  | T-326, 1.34e-15 above the point | candidate, credit by think-frl5 |

At 232 and 268 each point is a new result against the house it was solved from.
T-307 (Kodaj’s packing as JoeGun improved it) and de Winter’s T-331 now lie below the
respective points. The house rule therefore excludes both points from adoption.
The receipts are each house’s own margin, both maintained routes deciding the
certificate and its contraction
([option-d/contraction-n232-t275.json](option-d/contraction-n232-t275.json),
[option-d/contraction-n268-t276.json](option-d/contraction-n268-t276.json)), against the
solved side in the driver’s report
(`adopt-2026-11-09-n232-307-evand/n-N/report.json.gz`). At 303 the solve was regenerated
as a certificate and measured against T-278 directly
([option-d/contraction-n303-t278.json](option-d/contraction-n303-t278.json), beside
[option-d/n-303-solve.cert](option-d/n-303-solve.cert)). At 299 and 307 the points are
the ones the driver reaches on Polkovskyi’s re-solves (T-325, T-326) of #1023, measured
there against those houses’ own margins; the owner left new-result status and credit
with Polkovskyi, the record noting the project’s earlier solves (think-frl5). T-333
retired the candidate at 299. The remaining candidates at 303 and 307 have
classification and receipts.
Their registration, stage 4 review and adoption are think-4z8z’s, beside the candidate
at 130
([think-ruu2-2026-10-31](../../register_candidates/think-ruu2-2026-10-31/README.md)).
`tests/test_restatements.py` holds the shares at 232, 268 and 303 and each point’s place
against today’s house.

From `packing/`, each house’s own margin:

```bash
python -m devtools.contraction_margin --n 232 'T-275=packet:ozden-s232-upper-bound-2026-11-09' \
  --out cases/regularized_drawings/think-463r-2026-11-09/option-d/contraction-n232-t275.json
python -m devtools.contraction_margin --n 268 'T-276=packet:ozden-s268-upper-bound-2026-11-09' \
  --out cases/regularized_drawings/think-463r-2026-11-09/option-d/contraction-n268-t276.json
```

## Files

- `adopt-2026-11-09-n232-307-evand/`: the driver’s `receipt.json` and each count’s
  `report.json.gz`.
- `adopt-2026-11-09-n232-307-grid-{deg05,deg1,deg5}/`: each run’s block, `run.json`, and
  each count’s `report.json.gz`.
- `selection-adopt-2026-11-09-n232-307.{json.gz,md}`: the selection’s report and table.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
