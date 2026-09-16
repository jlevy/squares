---
title: H-211 — the shake has a sweet spot, and the shipped value is far below it
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-211
  kind: hypothesis
  claim: >-
    The workbench's shake dial has a maximum for search quality between levels 6 and 8, and
    the shipped default of 3 is far below it. Under the default the best of a thousand valid
    runs never clears the trivial grid at any n; at levels 6 to 8 it reaches within half a
    per cent of the record at n = 5 and 10.
  lane: search
  derived_from: [X-034]
  criterion:
    shape: conditions
    metric: closed at the best of a thousand valid runs
    direction: rises from level 0 to a maximum near 6-8, then falls
    threshold: the maximum exceeds the level-3 value by more than one whole gap
  instrument: packages/workbench/tools/workbench_tools/benchmark.py --sweep anneal=...
  instrument_ready: true
  regime: >-
    the workbench's simulation, trials resolved to packings before scoring; the dial's own
    default is chosen for how the animation looks, not for search
  instance: {axis: n, point: 5}
  sweep: {axis: n, points: [5, 10, 11, 17, 26, 29]}
  priority: 1
  cost_estimate: minutes
  registered: '2026-09-12'
---
# H-211 — the shake has a sweet spot, and the shipped value is far below it

**Identity.** Derived from X-034, which was X-028 until 2026-09-13 and X-029 until
2026-09-14.

**Registered after its data, and untested.** The table below was in hand when this claim
was registered, so exp-208, which reports it, is the exploratory data behind the claim,
filed under the open question [H-212](H-212-the-workbench-physics-as-a-search.md).
The test is a preregistered round on seed blocks or `n` that exp-208 did not use.

The best of the first 1,000 runs in `closed`, with 3,000 repaired runs per cell
([exp-208](../series/series-000-smoke-and-calibration/experiments/exp-208-h211-the-shake-dial.md)):

| level | n = 5 | n = 10 | n = 11 |
| ---: | ---: | ---: | ---: |
| 0 | −0.082 | −0.114 | −0.112 |
| 2 | −0.056 | −0.076 | −0.015 |
| 4 | −0.018 | −0.070 | −0.021 |
| 6 | 0.974 | 0.947 | −0.012 |
| 8 | 0.958 | 0.977 | 0.564 |
| 10 | 0.864 | 0.879 | 0.325 |

At levels 0, 2 and 4 no run beat the grid at any of the three `n`. At levels 6, 8 and 10
the best run beat it in eight cells of nine; the ninth, `n = 11` at level 6, did before
seed 5,000 of the same stream.
Levels 1, 3, 5, 7 and 9 have no repaired runs.

**What the measurement cannot yet say.** The claim compares against level 3, the page’s
default when it was registered, which was not measured.
#171 ships level 9 on a 0–20 dial.
Level 9 lies between the levels measured, but these cells ran under the page’s previous
pair law (rigidity 0.15, repulsion 2500, attraction 0, range 0) and a 0.8 s moving span.
#171 also changes both, to 0.35, 950, 80 and 0.15 and a 0.9 s span, so no cell says how
level 9 searches as shipped.
Nothing above level 10 has been measured under either law.
Each cell is one prefix without spread, and only three `n` were swept.

**What the cells suggest, and do not establish.** The shake is the only randomness in
the run, so at level 0 every seed of an `n` gives the same run.
At levels 2 and 4 the runs do differ, from −0.225 to −0.054 at `n = 5` and level 2, but
none of 3,000 beat the grid; at levels 6, 8 and 10 the best one usually did.
Why a larger shake reaches those few runs is not measured.
The dial is a search parameter that the page sets for a presentational reason.

**What would refute it.** A level between 0 and 4 whose best-of-k matches 6 to 8’s on a
set of n it was not tuned on; or a maximum that moves with n far enough that “6 to 8” is
not a sweet spot but an artefact of the three n measured.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
