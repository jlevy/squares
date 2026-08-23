---
title: exp-001 — baseline sweep of the stock annealer at n = 10, 11, 12
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-001
  series: series-000
  title: Baseline sweep of the stock annealer at n = 10, 11, 12
  date: '2026-08-22'
  hypotheses: [H-016]
  tier: exploratory
  subject:
    label: stock sqsearch annealer, default parameters
    engine: sqsearch 0.1.0
    engine_commit: 'd6a1057'
    precision: f64_screen
    host_system: Apple M1 Pro, 8 performance + 2 efficiency cores, 32 GB
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: 'the trivial ceil(sqrt(n)) grid, which every chain starts from'
    candidate: 'sqsearch defaults: steps 400000, t_hot 0.25, t_cold 1e-9, lambda 2 -> 1e6, p_rotate 0.35, p_reseed 0.5'
    runs_per_condition: 5
    interleaved: false
    operator: claude-opus-5
    commit: 'd6a1057'
    entry_point: explorations/packing/run_baseline.sh
    command: 'sqsearch --n N --seed S --chains 8 --budget-moves 100000000, for N in 10 11 12 and S in 1..5'
    budget: '12,000,000,000 moves total, 302.4 s wall'
    record: campaign/series/001-smoke-n11/results/exp-001-baseline.jsonl
  results:
  - shape: record
    metric: best_side
    role: outcome
    direction: lower
    score: 3.7075262000644953
    standing_best: 3.7071067811865475
    standing_best_source: 'frontier/n-010.md (proved, 3 + 1/sqrt(2))'
    beat_record: false
    runs: 5
  - shape: determination
    question: 'does the stock annealer reach the standing best at n = 10'
    role: outcome
    outcome: near_miss
    checked_by: 'sqsearch overlap guard (overlap == 0 on every reported packing); scored against frontier/n-010.md'
  - shape: record
    metric: best_side
    role: outcome
    direction: lower
    score: 3.9144165418191186
    standing_best: 3.877083590022814
    standing_best_source: 'frontier/n-011.md (Trump 1979)'
    beat_record: false
    runs: 5
  - shape: determination
    question: 'does the stock annealer reach the standing best at n = 11'
    role: outcome
    outcome: near_miss
    checked_by: 'sqsearch overlap guard (overlap == 0 on every reported packing); scored against frontier/n-011.md'
  - shape: record
    metric: best_side
    role: outcome
    direction: lower
    score: 4.0
    standing_best: 4.0
    standing_best_source: 'frontier/n-012.md (trivial 4x4 grid)'
    beat_record: false
    runs: 5
  - shape: determination
    question: 'does the stock annealer reach the standing best at n = 12'
    role: outcome
    outcome: reached_basin
    checked_by: 'sqsearch overlap guard (overlap == 0 on every reported packing); scored against frontier/n-012.md'
  - shape: conditions
    metric: best_side_n11_across_seeds
    role: mechanism
    control_median: 3.927939617731721
    candidate_median: 3.927939617731721
    control_range: [3.9144165418191186, 3.9361125018580427]
    candidate_range: [3.9144165418191186, 3.9361125018580427]
    overlapping: true
  complexity:
    lines_changed: 0
    new_dependencies: [rayon 1.12]
    new_failure_modes: []
    notes: 'Baseline round; the engine is the change, and it is recorded as the subject.'
  verdict:
    decision: rejected
    primary_criterion: best_side
    reason: >-
      Refutes H-016: the annealer is within 1e-4 of the standing best only at n = 12,
      missing by 4.19e-04 at n = 10 and by 3.73e-02 at n = 11. Also serves as the
      series baseline, since method.control is the trivial grid every chain starts from.
    commit: 'd6a1057'
---
# exp-001 — baseline sweep

## What was measured

The stock `sqsearch` annealer at its default parameters, on every cell of the declared
sweep, five deterministic seeds per cell, eight chains per seed, an equal budget of 100M
moves per chain. 12 billion moves in 302 seconds.

The round tests
[H-016](../../../hypotheses/H-016-stock-annealer-reaches-standing-best.md) — the null
hypothesis that a serious budget on a general-purpose annealer reaches the best known
packing — and establishes the numbers every later round is measured against.

| `n` | role | best | median | range across seeds | standing best | gap |
| --- | --- | --- | --- | --- | --- | --- |
| 10 | positive control | `3.7075262001` | `3.7076711818` | `[3.7075262, 3.7091188]` | `3.7071067812` | `+4.19e-04` |
| 11 | target | `3.9144165418` | `3.9279396177` | `[3.9144165, 3.9361125]` | `3.8770835900` | `+3.73e-02` |
| 12 | negative control | `4.0000000000` | `4.0000000000` | `[4.0000000, 4.0000000]` | `4.0000000000` | `0` |

## What was tried

Nothing but the defaults — that is the point of a baseline.
The work in this round went into the instrument, and two defects it found are worth more
than the numbers.

**The first search formulation did not work, and the positive control is what said so.**
Fixing a container side and asking whether the squares fit needs an outer loop that
decides when an anneal has failed, and it starts from the trivial grid, which is exactly
jammed: shrinking it by any amount at all is infeasible, and only a wholly different
tilted configuration helps.
Two versions were built and measured.
The first crawled — `2.875` on `n = 5`, where the answer is `2.707`. The second, with
the move size tied to the shrink being attempted, never left the grid basin at all and
returned the grid for every `n`. Both would have produced a night of confident,
meaningless numbers at `n = 11`.

The replacement removes the container from the variables entirely.
The smallest axis-aligned square holding a configuration is computable from the
configuration, so the search minimises `required_side + lambda * total_overlap` with
`lambda` ramped upward — no feasibility oracle, no shrink schedule, and a reward for
every move that compacts the packing.
The overlap penalty is linear rather than squared, because a linear penalty has an exact
finite-`lambda` constrained optimum while a squared one’s gradient dies as the overlap
closes.

**The declared budget did not bind.** A restart cap stopped every chain before
`--budget-moves` did, so the budget was inert and two strategies compared “at equal
budget” would have had unequal work.
The tell was that results got *worse* at a larger declared budget.
After the fix the `s(5)` control improved 18-fold, from a gap of `2.97e-04` to
`1.64e-05`.

## Result

**H-016 is refuted.** Its claim was `1e-4` on *every* cell, and only `n = 12` meets
that: `n = 10` misses by `4.19e-04` and `n = 11` by `3.73e-02`. The two failures are
nothing alike, and separating them is the round’s real output.

Both guard cells behave.
The positive control lands `4.19e-04` from a proved optimum that is *not* the grid — it
needs a genuine 45° tilted family, so recovering it exercises the part of the search
that matters. The negative control returns exactly `4.0` on all five seeds and never
below, so the geometry is not manufacturing packings that do not exist.

At `n = 11` the seed range is `[3.9144, 3.9361]`, a spread of `2.2e-02` — five times
narrower than the `3.73e-02` distance still to Trump.
Every seed lands well short, in a band of its own.
That is not the signature of a search that is nearly there.

## What the prediction got wrong

Nothing about `n = 11`; that failure was expected, and it is a failure of *exploration*
— the search never reaches the right region at all.

The surprise was `n = 10`, and it was surprising enough to be written down wrong first:
the draft of this artifact called `n = 10` a confirmation, because the search plainly
found the right basin.
It did not meet the criterion.
`4.19e-04` is outside the `1e-4` H-016 declared, and the generated frontmatter said so
while the prose did not.
Measuring, missing, and calling it a pass is exactly what pre-registration exists to
stop, and it took the generated table sitting next to the prose to catch it.
So `n = 10` is a failure of *polish*: the annealer finds the right basin and then stops
improving inside it.
That is a different defect from `n = 11`’s, it has a different fix, and one criterion
could not tell them apart.
The tier-2 numerical refinement step is more urgent than it looked when the tiers were
laid out, and a future criterion should probably score basin-finding and basin-polishing
separately.

## Annotation, 2026-08-23: renumbered on merge

This round was recorded against `H-001`. When the campaign merged with the standing
review’s hypothesis register — which owns `H-001` through `H-015` — the claim was
renumbered to `H-016`, and the references above follow.
Nothing about the measurement changed; the ids did.
The registry conflict is exactly the one
[`traps.md`](../../../../../.agents/skills/experiment-loop/references/traps.md) predicts
for parallel campaigns, and it is recorded here rather than erased.

## Limits

- `f64` screening only.
  No claim here is certified, and none may be: a record packing has pairs touching at
  exactly zero separation — 14 of Trump’s 55 — which no floating-point check can decide.
- `reached_basin` is scored by a `1e-4` numerical proxy, not by comparing contact
  graphs. At `n = 10` the search may have found a different configuration of nearly equal
  side.
- One host, one engine version, one parameter set.
  Nothing here says anything about other schedules, move sets, or restart policies;
  those are the registry’s open rows.
- Five seeds is enough to see the spread, not enough for a confirmatory interval.
  The round is `exploratory` and is marked so.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
