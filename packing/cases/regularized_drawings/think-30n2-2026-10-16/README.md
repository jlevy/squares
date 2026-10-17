# Regularization Runs for n = 29 on PR #622’s Witness (think-30n2)

These are the strong generators’ runs on the witness that adopting T-195, PingYou Ltd’s
N29 certificate (PR #622), writes at n = 29. They were run the day before the adoption,
which waited for T-195’s stage 4 review
([review of 16 October 2026](../../../../docs/project/reviews/review-2026-10-16-pingyou-n29.md)).
The adoption ran on 17 October 2026 under
[the house rule](../../../campaign/result-import.md#the-house-rule), which adopts a
validated smaller packing in the pass that validates it and regularizes it in the same
pull request.

## How They Were Run

On 16 October 2026, from 22:27Z to 22:31Z, in a local trial branch that was never
pushed. The trial branch held the records pull request #661, the house-rule branch of
#660, and the adoption wiring for T-195. It also held a stand-in accepted review on
T-195, needed only so that `select_houses` would take it.
The trial ran `adopt_houses`, then `build_known_best_atlas --update`, which wrote
`witnesses/known-best/n-029.yaml` with SHA-256
`b7bd539821b3c9ab194dbc6f5efc76b0cb6de9004039004fef0ee23db41058cd`. It then ran
`regularize_axis_components --update-atlas --n 29` and `default_drawings --update`,
which read 29 as pending because Evan Daniel’s view of the earlier witness had lapsed.
Then it ran these commands, from `packing/`, at most two workers, `nice -n 10`:

```sh
python -m devtools.regularize_grid_slack --n 29 --run-dir $RUNS/adopt-2026-10-16-n29-grid-0.5
python -m devtools.regularize_grid_slack --n 29 --run-dir $RUNS/adopt-2026-10-16-n29-grid-1 --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n 29 --run-dir $RUNS/adopt-2026-10-16-n29-grid-5 --near-axis-degrees 5
python -m devtools.regularize_evand run --run-dir $RUNS/adopt-2026-10-16-n29-evand --n 29 --workers 2
python -m devtools.regularize_select --evand-run $RUNS/adopt-2026-10-16-n29-evand \
  --grid-run $RUNS/adopt-2026-10-16-n29-grid-0.5 $RUNS/adopt-2026-10-16-n29-grid-1 \
  $RUNS/adopt-2026-10-16-n29-grid-5 --workers 2 --output selection-n29.json --markdown selection-n29.md
```

The grid-slack runs took 45 CPU-seconds each, Evan Daniel’s driver 9 seconds of wall at
two workers, and the selection 65 seconds of wall at two workers.
The full rebuild of the atlas data took 12 minutes of wall.

## What They Found

The new witness’s house drawing has no light, uneven or near-axis square, 6 angle
classes, 6 hues and 52 full shared sides in both totals.
The lapsed view of the earlier witness measured the same.

- **Grid-slack** at 0.5, 1 and 5 degrees changes no square.
  Both exact routes accept each view at the witness’s side (row 10, no change), and each
  ties the drawing on every goal of the improvement rule, so none is admitted.
- **Evan Daniel’s driver** solves the packing to a view 5.93e-20 above the certificate’s
  side. That is above the new verified bound, so the view is held at row 4. The same-side
  re-solve is refused, because the certificate’s 2,399-digit literal is too large for
  it.

The selection chooses nothing at 29. The adoption of 17 October 2026, the first under
the house rule, wrote the witness byte for byte as above and settles the count as
decided no better, in `default_drawings.SETTLED`. The settlement names these four runs:
`evand-regularize-adopt-2026-10-16-n29-evand` and
`grid-slack-adopt-2026-10-16-n29-grid-{0.5,1,5}`. It also names the new witness’s
source, `[PingYou PR 622 certificate 2026-10-15]`, its path
`resources/web/pingyou-pr622-certificate-2026-10-15/facts/n-029.yaml.gz`, its revision
`31155575ce1e6b461f77bfc9f3e201adf101115b` and its exact side.

## Files

Per run, the retained evidence is the driver’s `receipt.json` and each count’s
`report.json.gz`, and for each grid-slack run a `run.json`, the block
`regularize_grid_slack.run_block` computes from the run’s reports, which is what lets
the settlement name it.
The selection’s JSON report and its table are `selection-n29.json` and
`selection-n29.md`. The run paths in them are the scratch directories the runs were made
in. The runs count for the adoption only where it writes the witness byte for byte as
above. Otherwise the adoption runs them again: about four CPU-minutes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
