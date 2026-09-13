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
  derived_from: [X-028]
  criterion:
    shape: conditions
    metric: closed at the best of a thousand valid runs
    direction: rises from level 0 to a maximum near 6-8, then falls
    threshold: the maximum exceeds the level-3 value by more than one whole gap
  instrument: packing/devtools/bench_annealing.py --sweep anneal=...
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

Best-of-1000 `closed` over 54,000 valid trials, by dial level:

| level | n = 5 | n = 10 | n = 11 |
| ---: | ---: | ---: | ---: |
| 0 | −0.082 | −0.114 | −0.112 |
| 2 | −0.056 | −0.076 | −0.015 |
| 4 | −0.018 | −0.070 | −0.021 |
| 6 | **0.974** | 0.947 | −0.012 |
| 8 | 0.958 | **0.977** | **0.564** |
| 10 | 0.864 | — | — |

Below level 6 the tail never clears the grid at any of the three.
At 6 to 8 it reaches 0.95 to 0.98 at n = 5 and 10, and n = 11 clears the grid for the
first time — 0.564 at level 8, against −0.012 at the level the page ships.

The mechanism this suggests, and does not establish: the shake is the only randomness in
the run, so below some amplitude every restart lands in the same basin and k buys
nothing, while above it the run is thrown out of the basin it needs.
The dial is therefore a search parameter that the page sets for a presentational reason.

**What would refute it.** A level between 0 and 4 whose best-of-k matches 6 to 8’s on a
set of n it was not tuned on; or a maximum that moves with n far enough that “6 to 8” is
not a sweet spot but an artefact of the three n measured.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
