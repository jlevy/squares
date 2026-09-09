---
title: H-138 — a ten-times longer cooling schedule, at equal budget, leaves the trivial grid
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-138
  kind: hypothesis
  claim: >-
    Raising only the anneal length from 400,000 to 4,000,000 steps per restart, at the
    same pair-test budget and with the single-square move set untouched, lowers the
    median best side over five seeds by at least 0.01 against the stock control with
    disjoint seed ranges, on at least half the cells of the non-grid subset.
  lane: search
  derived_from: []
  strategy_refs: ['search:10']
  criterion:
    shape: paired
    metric: best_side
    direction: candidate lower by at least 0.01 on at least 6 of the 11 cells
    threshold: 0.01
  instrument: >-
    devtools/run_arm_sweep.py over sqsearch --steps, at equal --budget-pair-tests, gated
    by sqsearch --selftest and re-checked pose by pose by packing-campaign verify-archive
  instrument_ready: true
  regime: >-
    sqsearch 0.1.0 at the commit under test, f64 screening, 8 chains, 1.25e9 pair tests
    per chain, 4 rayon threads, seeds 1-5, one host
  instance: {axis: n, point: 11}
  sweep:
    axis: n
    points: [5, 10, 11, 17, 19, 26, 27, 29, 37, 50, 52]
  priority: 1
  cost_estimate: 5.5e11 pair tests, about 25 minutes wall per arm on a loaded 10-core host
  prereqs: []
  replication: false
  registered: '2026-09-08'
  runner:
    command: './sqsearch/target/release/sqsearch --n {n} --seed {seed} --chains 8 --threads 4 --budget-moves 9223372036854775807 --budget-pair-tests 1250000000 --steps 4000000'
    cells: [5, 10, 11, 17, 19, 26, 27, 29, 37, 50, 52]
    seeds: [1, 2, 3, 4, 5]
    timebox: 1h
  notes: >-
    Registered mid-calibration, after the exp-134 ablation that was meant to REFUTE this
    kind of explanation turned up a positive. It is registered before the round that
    scores it and before any of the round's cells were run under it, which is what keeps
    it a prediction. The survey this campaign is built on argues the opposite -- Johnson
    and colleagues' Observations 4 and 5 find nothing worth having in schedule changes,
    and the survey's own section 4 is titled "the move set, not the cooling schedule" --
    so a confirmation here is a correction to the design input, not a vindication of it.
---
# H-138 — the factor the ablation was supposed to rule out

## How this came to be registered

Arm B’s win needed a guard.
A simultaneous perturbation at scale `temperature` displaces the configuration much
further per proposal than a single-square move does, so before the win could be read as
“the collective move matters”, the alternative had to be excluded: that it is simply a
hotter search wearing a structural costume.

[exp-134](../series/series-000-smoke-and-calibration/experiments/exp-134-arm-calibration.md)
pass 3 ran that ablation on the held-out cells.
Raising `t_hot` from `0.25` to `0.5`, `1.0`, `2.0` and `4.0` changed **nothing**: every
seed still returned exactly the trivial grid, so arm B’s effect is not exploration
temperature. Turning off reseeding changed nothing either.

The seventh arm in that pass was not a temperature change.
`--steps 4000000` lengthens each anneal tenfold, so the same pair-test budget buys a
tenth as many restarts, each cooled ten times more slowly.
It left the grid on three seeds of six, at a median of `4.9146` against the control’s
`5.0`.

That is a positive from an ablation designed to produce a negative, and it is exactly
the kind of result that must become a registered prediction rather than a sentence in
someone’s summary. Hence this artifact, written before the round.

## Why it matters more than its size suggests

The owner’s question was framed as *“with the right amount of simulated annealing”*, and
the survey’s answer was that the schedule is the least important part.
On the published evidence that answer is well supported: Johnson, Aragon, McGeoch and
Schevon found no non-adaptive schedule worth substituting for geometric cooling
(Observation 5) and no simple-minded adaptive schedule worth its running time
(Observation 4), while changing only the neighbourhood bought two whole colours at equal
time. The 2026-09-08 survey builds section 4 on that.

If a schedule-length change alone can leave the grid where four temperature changes
cannot, then the schedule *length* is not the schedule *shape*, and the two have been
conflated.
Anneal length trades restarts against cooling rate at fixed budget, which is a
resource-allocation question rather than a cooling-law question — and no source in the
survey measured it.

## What would refute it

Fewer than six of eleven cells improving by `0.01` with disjoint seed ranges.
The most likely shape of a refutation is that the effect is real at `n = 18` and absent
everywhere else, which would make it a fact about one case rather than about schedules,
and the sweep is what can tell those apart.

## Limits declared before the round

- One alternative length, chosen because it is the one the ablation happened to run.
  Nothing here brackets an optimum, and a tenfold step is a coarse instrument.
- At fixed budget, longer anneals mean fewer restarts.
  This claim cannot separate “slower cooling helps” from “fewer, deeper descents help”,
  and a round that wanted to would have to vary the two independently.
- `f64` screening only; nothing here can be certified.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
