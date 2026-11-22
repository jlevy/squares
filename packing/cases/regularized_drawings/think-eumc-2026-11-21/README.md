# Strong Drawing Runs for the Issue-1062 Adoption at 232

The completed strong-generator runs found no adoptable view of T-340’s witness.
The axis tool’s view stays drawn, and `default_drawings.SETTLED` records
`decided-no-better` for the exact source, revision and side of the new house.

The three grid-slack runs, at 0.5, 1 and 5 degrees, produced no view: every attempted
placement had relaxed rows that overlap at the witness’s side.
Evan Daniel’s solved view passed both maintained exact routes and improved all seven
drawing goals, but its exact side exceeds the new upper bound and the current drawing by
about `1.57595316236e-19`. The selector holds it at row 4. Its same-side attempt was
refused as `literal-too-large`. There is no selected view, register candidate or
admission command.

These results do not alter the certificate’s finite-feasibility claim.
The inherited Kodaj–JoeGun layout and local-solve attribution, Joost de Winter’s
certificate authorship, and Alex Chilton’s source compilation are recorded in the
[case](../../../frontier/n-232.md).
No local or global optimum is established.

## Retained Evidence

The run directory names are the original names.
The reports, Evan Daniel’s receipt, and the selection are preserved without rewriting
their contents; gzip copies decode to the original bytes.
Absolute paths in those historical run records describe the original execution
environment and are not required by the settlement reader.

| Retained files | Meaning |
| --- | --- |
| `adopt-2026-11-21-n232-grid-deg05/`, `-grid-deg1/`, `-grid-deg5/` | Each run’s `n-232/report.json.gz` and its `run.json`, derived by the maintained `regularize_grid_slack.run_block` |
| `adopt-2026-11-21-n232-evand/` | The driver’s `receipt.json` and `n-232/report.json.gz` |
| [Selection table](selection-adopt-2026-11-21-n232.md) and `selection-adopt-2026-11-21-n232.json.gz` | All four candidates and the exact reasons none is adoptable |

No `layer` admission is needed.
The
[regularization guide](../../../../docs/project/guides/regularization-process.md#when-a-witness-changes)
requires retaining these runs and settling the new witness before the adoption lands.

## Execution and Cost

The runs finished on 21 November 2026 during local adoption preparation, after the atlas
refresh, axis regularization and default-drawing measurement, with one worker per
command. The house adoption is recorded on 22 November UTC; the original source,
certificate review and these drawing runs keep their 21 November dates:

```bash
P=adopt-2026-11-21-n232
python -m devtools.regularize_grid_slack --n 232 --run-dir "$RUNS/$P-grid-deg05"
python -m devtools.regularize_grid_slack --n 232 --run-dir "$RUNS/$P-grid-deg1" --near-axis-degrees 1
python -m devtools.regularize_grid_slack --n 232 --run-dir "$RUNS/$P-grid-deg5" --near-axis-degrees 5
python -m devtools.regularize_evand run --n 232 --run-dir "$RUNS/$P-evand" --workers 1
python -m devtools.regularize_select --evand-run "$RUNS/$P-evand" \
  --grid-run "$RUNS/$P-grid-deg05" "$RUNS/$P-grid-deg1" "$RUNS/$P-grid-deg5" \
  --workers 1 --output "$RUNS/selection.json" --markdown "$RUNS/selection.md"
```

Grid-slack’s reports record 1,628.73, 1,424.35 and 1,358.71 elapsed seconds.
Those figures include supervision pauses and are not independent CPU measurements.
The maintained run-block writer repeats those reported seconds in its historical cost
fields; they do not establish CPU consumption.
Evan Daniel’s receipt reports 72.41 seconds of wall time and 56.06 process CPU-seconds.

The dedicated guard journal for adoption and all four runs records 4,762.7 watched
seconds, maximum kernel pressure 1, peak process-tree footprint 0.87 GiB, and 383 pauses
with matching resumes (3,546.8 paused seconds).
It records no abort or killed process.
The later retention and settlement work reuses these completed outcomes and performs no
new solve.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
