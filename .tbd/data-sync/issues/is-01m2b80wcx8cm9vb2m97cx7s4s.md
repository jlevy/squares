---
type: is
id: is-01m2b80wcx8cm9vb2m97cx7s4s
title: Best-of-k is one draw with no spread; report it over disjoint blocks
kind: bug
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies:
  - type: blocks
    target: is-01m2b7nakccj4tf1tgs4k86nar
created_at: 2026-09-12T16:43:15.228Z
updated_at: 2026-09-13T04:52:34.571Z
---
Every best-of-k in the record is **the best of the first k seeds** -- one draw, no spread. Invariant 4 of the loop says a number without its spread is not a result, and these were published without one.

The fix is free: the deep files hold 39,871 trials at n = 5 and 16,319 at n = 11, so best-of-1000 can be taken over disjoint blocks and reported as a median with a range. Done inline over the existing data, it changes what three of the findings mean:

| | single draw | over disjoint blocks | blocks clearing the grid |
| --- | ---: | --- | ---: |
| n=5, shake 6, k=1000 | +0.974 | median **+0.971**, range [-0.017, +0.986] | 34/39 |
| n=11, shake 6, k=1000 | +0.476 | median **-0.016**, range [-0.025, +0.476] | 1/5 |
| n=11, shake 8, k=1000 | +0.564 | median **+0.439**, range [-0.020, +0.616] | 13/16 |
| n=17, shake 6, k=1000 | -0.062 | median -0.067, range [-0.069, -0.061] | 0/5 |
| n=26, shake 6, k=1000 | +0.212 | median **+0.212**, range [+0.160, +0.230] | 5/5 |

- **n = 5 survives and gets stronger.** It was one lucky seed for all anyone could tell; it is 34 blocks of 1000 out of 39.
- **n = 11 at shake 6 was a single lucky seed** and is reported as a result. One block in five clears the grid. At shake 8 it is 13 in 16 -- a real effect that the single-draw table understated as 0.564 vs 0.476.
- **n = 26 is the most reliable instance measured**, 5 blocks of 5, and it is larger than the two the campaign calls hard.

So the harness should report best-of-k as a distribution whenever the pool allows it, and the artifacts citing single draws need the spread added beside them.

## Notes

2026-09-12 review: raw files used for the pasted block table are absent from this Git tree; summaries alone do not recover block extrema or pose-level checks. Recover retained raw artifacts or replay the exact frozen instrument/seed ranges; retain a reusable aggregator plus block/sample/seed manifest and output. Mark prefix ladders as one prefix observation meanwhile, distinguish planned budget from completed counts, exclude rejected trials from the budget-success denominator only when the metric explicitly calls for conditional validity. See updated annealing plan.
