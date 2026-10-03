# Session 168 Handoff: Work Stopped Mid-Flight

At about 21:15 UTC on 2026-10-02, every running lane stopped at an account usage limit
that resets on 2026-10-07. This folder keeps what those lanes had produced but not yet
committed, so that nothing is lost.
Each item names its bead under `think-tmz6`.

Nothing here was admitted or reviewed when it was filed; N1 has since been admitted.
Code patches apply cleanly to commit `5ac81e86` with `git apply`.

## H-264 Per-State Pilot (`think-e17c`)

`k2/` holds lane K2’s runs of whole 17-cell residue states through the kernel at 32 bins
with collision on and hull limit 16. The states were sampled in `k2/h-sample.json`.

| Receipt | State | Outcome |
| --- | --- | --- |
| `k2/h-F1.json` | F1, distance 6 from the endpoint | certified stall at the 45-minute cap |
| `k2/h-N1.json` | N1, distance 4 | certified stall at the 45-minute cap |
| `k2/h-N1-2h.json` | N1, two-hour ceiling | **`PASS_CERTIFIED_CLOSED`** in 3,723 s, 82 steps, 2,624 rows |

N1’s two-hour run is the first per-state exclusion of a residue state.
Its seed and node are in `../certificates/N1-state-pending/`, named by their SHA-256.

N1 is admitted in
[exp-250](../../../series/series-000-smoke-and-calibration/experiments/exp-250-h267-n17-standing-verifier-admissions.md).
Of the four conditions first set here, the fresh-process `--check-saved` run
(`check-saved.json`) and the standing verifier’s full pass (`verification.json`) were
met. Under OR-16 as amended on 2026-10-03 that full pass is the admission check, so the
clean-worktree repeat and a review of this certificate were not required.

H-264’s falsifier still needs more states: fewer than half of 10 to 20 sampled orbits
closing within two CPU-hours each.

## Capture Pilot 2 (`think-g2qn`)

`c1/capture-pilot2-wip.patch` is lane C1’s unfinished rework of
`devtools/pilot_n17_capture.py` and its test.
It follows the capture-after-pilot review’s specification.

`c1/` also holds partial outputs:

- `box1024-128.partial.json` and its log reach round 11 at 128 live rows.
- `n11-32.json` is the n11 contraction control at 32 rows, reaching round 9 with
  $g\approx0.81$ against n11’s recorded 0.84, so the control behaves.
- `*.frozen.py.txt` are the exact tool bytes those runs imported.

Next: apply the patch, finish and test it, and rerun at 128 and 256 rows against the
review’s falsifier.

## Selector Finish Stage (`think-gygy`)

`s2/selector-finish-stage-wip.patch` is lane S2’s unfinished change to
`devtools/select_n17_sub_patterns.py`, `devtools/survey_n17_residue.py` and their tests.
It adds a long-descent finish stage, so a flag must survive one long descent from its
best pose. `s2/explore.py.txt` is its exploration script.

The re-search of all 90 flags and the full arity-8 sweep were not run.

## Cost Reduction (`think-pqya`, `think-3jp4`)

Lane F1’s pruning review is complete and filed at
`docs/project/reviews/review-2026-10-02-n17-cost-reduction-pruning.md`.

Lane F2’s performance review was not written.
Its profiles and micro-benchmarks are in `f2/`:

- cProfile summaries and stdout for the kernel at 16 bins and W7’s first round;
- 60 s of the branch and bound on A, and a branch-and-bound verifier sample;
- `bench_*.py.txt` with their JSON results, including integer-arithmetic collision;
- `rustbench/`, a Rust micro-benchmark’s sources and build log.

Next: write the performance review from these measurements.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
