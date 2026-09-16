---
title: X-034 — the workbench's blind physics, measured as a search
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-034
  title: The Workbench's Blind Physics, Measured as a Search
  date: '2026-09-12'
  author: Claude Opus 5, unattended
  campaign: packing.squares
  brief: >-
    The workbench animates each step from one known-best packing to the next with a contact
    simulation. In blind mode the run starts from the previous record and is not given the
    destination poses. This exploration measured that run as a search: whether it ends on a
    packing, and how close the best of many seeded runs gets to the known-best side.
  sources:
  - packages/workbench/src/application.js
  - packages/workbench/tools/workbench_tools/benchmark.py
  - packing/campaign/results/annealing/summaries.json
  - docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
  proposes: [H-207, H-208, H-209, H-210, H-211, H-212]
---
# X-034: The Workbench’s Blind Physics, Measured as a Search

**Renumbered 2026-09-14** from X-029, which main had already assigned to the BC303 T2
exact-geometry draft; before 2026-09-13 this report was X-028. It also proposed H-206,
retired on 2026-09-14; that id stays consumed.

**Rewritten 2026-09-14.** This report keeps only what survived checking.
Earlier versions reported numbers from runs whose arrangements were never checked to be
packings, and from inline analyses whose code was not kept.
That text is recoverable at commit `a40d272c`; none of it is repeated here.

## Summary

- **A blind run is not blind.** It starts from the known-best packing for the previous
  `n`, closes its walls onto the known-best side, places the new square with a
  coarse-grid proposal, and in the style measured here welds squares into blocks chosen
  by matching the two records.
  Only the destination poses are withheld.
  It is one point on a range of how much of the answer a search is given.
- **The runs did not end on packings.** None of the 123,190 seeded blind runs in the
  repaired rounds ended without overlapping squares; the median deepest overlap was
  0.083 of a unit side.
  A container side read from such an arrangement is a bounding box around overlaps, so
  every number taken that way has been discarded.
- **Repaired to a packing, a single run is worse than the trivial grid.** At every `n`
  and every shake level measured, the median run needs a larger container than
  `ceil(sqrt(n))`.
- **The best of many runs sometimes comes close and never reaches a record.** At shake
  level 6 the best of the first 1,000 seeds was 0.28% above `s(5)` and 0.42% above
  `s(10)`. At `n = 17` and `n = 29` no run in 5,000 beat the grid.
- **How hard an `n` is depends on the scale and the budget.** In `closed` at the best of
  the first 1,000 seeds, `n = 26` did better than `n = 11` and `n = 17`; at the best of
  5,000, or in excess over the record, `n = 11` did better than `n = 26`. Six `n`, one
  seed stream each, cannot show how difficulty depends on `n`.
- **The shake dial is a search parameter that the page sets for looks.** At levels 0, 2
  and 4 no run in 3,000 beat the grid at `n = 5`, 10 or 11. At levels 6, 8 and 10 the
  best run did in eight cells of nine, and the ninth did within 5,000 seeds.
  These runs used the page’s defaults of the time: level 3, a pair law of rigidity 0.15
  and repulsion 2500 with no attraction, and a 0.8 s moving span.
  #171 ships level 9 on a 0–20 dial, under a different law and beat, and no level has
  been measured under those.

## 1. What a Blind Run Is

The workbench draws the step from the packing of `n - 1` squares to the packing of `n`
by simulating it:

1. The squares start at the known-best poses for `n - 1`, centred in a container 12%
   larger than the known-best side for `n`.
2. The new square is dropped, upright, into the emptiest cell of a coarse grid.
3. Contact forces between squares, wall forces and a decaying shake act while the walls
   close onto the known-best side.
   The walls keep closing while the deepest overlap is at most 0.08 of a unit side, and
   they never go below the known-best side.
4. In the `bodies` style, which every run in this report used, squares are welded into
   rigid blocks in their starting arrangement.
   Which squares share a block comes from matching the record for `n - 1` against the
   record for `n`, so it is information about the destination.

The page has three ways to finish the step:

| mode | what the run is given about the destination |
| --- | --- |
| snap | the destination poses, and it ends on them by construction |
| free | the destination poses as a pull, without the snap |
| blind | no poses; still the known-best side, and in `bodies` style the matched blocks |

So “blind” is conditioned on a great deal: the previous record, the reference side, the
proposal and, in `bodies` style, which squares move together.
Any claim about it is a claim about improving a known packing toward a known side, not
about finding a packing from nothing.

## 2. One Trial Per `n`, Until Runs Were Seeded

Every generator on the page was seeded from `n` alone, so a given `n` and parameter set
had exactly one blind trial.
That is right for an animation, which must reproduce across builds, and it makes a
success rate meaningless.

`setSeed` folds a run seed into every generator.
Seed 0 reproduces the page exactly, so the existing checks pass unchanged.

## 3. The Runs Were Not Packings

The first two rounds of the benchmark scored the bounding box of each run’s final
arrangement and never checked that the squares were disjoint.
Some parameter cells reported a container below the known-best side, which no packing
can need. That was the signal that something was wrong, and it was missed.

The check that exposed it is a separating-axis test over the final poses, computed in
the harness rather than read from the simulation.
It reports the deepest overlap between any two squares.
The tolerance is chosen.
Beside it is one observation of a control: a snapped run ends on the record’s own poses,
so whatever it scores is float noise.

| mode | n = 5 | n = 11 | n = 17 |
| --- | ---: | ---: | ---: |
| snap | 5.5e-7 | 1.0e-6 | 7.3e-7 |
| free | 3.9e-5 | 4.5e-5 | 3.1e-2 |
| blind | 8.4e-2 | 3.5e-2 | 8.6e-2 |

The harness uses 1e-5 of a unit side: ten times the largest snapped value, a factor of
3.9 below the smallest free value, and more than three orders of magnitude below every
blind value in the table.
The snap and free rows came from a variant of the probe that was run once and not kept;
the committed harness runs blind only, so the control is a recorded observation rather
than a reproducible one.

Across the 123,190 seeded runs of the repaired rounds, no run ended below 1e-5. Of
those, 9,000 are at level 0, where every seed of an `n` repeats one run.
The deepest overlap before repair ranged from 0.002 to 0.118 of a side, with a median of
0.083. These figures come from local copies of the rows, which are not retained, and
`workbench_tools.summarize_annealing --overlaps` recomputes them from regenerated rows.

The overlap is built into the blind schedule.
The walls close onto the known-best side while squares may overlap by up to 0.08, and
the observed overlaps sit at that tolerance.
Squares compressed inside a record-sized box can have a bounding box smaller than the
box, which is how a cell came to report a container below the known-best side.
The details are in
[exp-210](../series/series-000-smoke-and-calibration/experiments/exp-210-h210-blind-runs-are-not-packings.md).

**Everything measured before this check is void.** In `summaries.json` those cells are
the ones marked `resolved: false`: 243 cells across 49 run files.
No number from them appears in the record.

Since then the harness repairs every run before scoring it.
The repair moves squares apart along each overlapping pair’s minimum-penetration axis,
holding angles fixed, until no pair overlaps.
The score is the container that the repaired arrangement needs.

## 4. What a Repaired Run Is Worth

The score is `closed = (grid - side) / (grid - record)`, where `grid` is
`ceil(sqrt(n))`. One is the record, zero is the trivial grid, and a negative value is
worse than the grid.
Raw excess over the record cannot be compared across `n`, because the room between the
record and the grid ranges from 1.12% at `n = 29` to 10.82% at `n = 5`.

### Across `n`, at shake level 6

5,000 seeds per `n`, each run repaired and checked before scoring:

| n | gap to grid | median run | median, above record | best of first 100 | best of first 1,000 | best of 5,000 | best, above record |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 10.82% | −0.074 | 11.62% | −0.015 | 0.974 | 0.977 | 0.25% |
| 10 | 7.90% | −0.099 | 8.68% | 0.874 | 0.947 | 0.974 | 0.20% |
| 11 | 3.17% | −0.107 | 3.51% | −0.035 | −0.012 | 0.476 | 1.66% |
| 17 | 6.94% | −0.104 | 7.66% | −0.062 | −0.062 | −0.061 | 7.36% |
| 26 | 6.74% | −0.101 | 7.42% | 0.120 | 0.212 | 0.230 | 5.19% |
| 29 | 1.12% | −0.857 | 2.07% | −0.370 | −0.193 | −0.110 | 1.24% |

What this shows:

- **One run is worse than doing nothing.** The median is below zero at every `n`.
- **A budget of runs is the method.** A run’s median wall time was 0.3 ms at `n = 5` and
  2.4 ms at `n = 29`, so the best of a thousand takes seconds.
  At `n = 5` the best of the first 1,000 is 0.28% above the record; at `n = 10` it is
  0.42%.
- **No run reached a record.** The closest is at `n = 5`: over 39,871 seeds the best is
  0.15% above `s(5)`.
- **The order across `n` depends on the scale and the budget.** In `closed`, `n = 26`
  beat the grid within its first 100 seeds, `n = 11` needed more than 1,000 and `n = 17`
  never did. In excess over the record the order changes: the best `n = 11` run is 1.66%
  above its record and the best `n = 26` run 5.19%. `closed` is a harsh scale where the
  gap is small, as at `n = 11` and `n = 29`. One seed stream at each of six `n` does not
  show how difficulty depends on `n`.

### Across shake levels, at `n = 5`, 10 and 11

3,000 seeds per cell; each entry is the best of the first 1,000, then the median run:

| level | n = 5 | n = 10 | n = 11 |
| ---: | --- | --- | --- |
| 0 | −0.082 / −0.082 | −0.114 / −0.114 | −0.112 / −0.112 |
| 2 | −0.056 / −0.090 | −0.076 / −0.104 | −0.015 / −0.103 |
| 4 | −0.018 / −0.083 | −0.070 / −0.103 | −0.021 / −0.103 |
| 6 | 0.974 / −0.074 | 0.947 / −0.099 | −0.012 / −0.106 |
| 8 | 0.958 / −0.076 | 0.977 / −0.098 | 0.564 / −0.115 |
| 10 | 0.864 / −0.095 | 0.879 / −0.098 | 0.325 / −0.249 |

What this shows:

- **At level 0 every seed gives the same answer**, because the shake is the only
  randomness in the run.
- **At levels 0, 2 and 4 no run beat the grid** in 3,000 seeds at any of the three `n`.
- **At levels 6, 8 and 10 the best of 3,000 beat it in eight cells of nine.** The ninth,
  `n = 11` at level 6, is the budget rather than the level: the same seed stream beat
  the grid before seed 5,000, as the table across `n` shows.
  At level 8, `n = 11` reached 0.564 in the first 1,000 seeds and 0.616 over 16,319.
- **The median barely moves with the level**, except `n = 11` at level 10, so the dial
  acts on the best run rather than the typical one.
- **The page shipped level 3** when these runs were measured, chosen for how the
  animation looked. Level 3 was not measured after the repair existed.
- **Every cell ran under the page’s previous law and beat.** At `engine_commit`
  `88d452f1` the pair law was rigidity 0.15, repulsion 2500, attraction 0 and range 0,
  and the moving span was 0.8 s, which gives a level-9 run 154 physics steps.
  #171 ships the owner’s defaults: level 9 on a dial widened to 0–20, the pair law 0.35,
  950, 80 and 0.15, and a 0.9 s moving span, 173 steps at level 9. Level 9 lies between
  measured levels, but no level has been measured under these defaults, and none above
  10 under any. From #160 on, every trial’s configuration records its pair law and beat.

## 5. What Is Not Established

- **No spread.** Every “best of the first k” is one observation from one ordered seed
  stream. None of these numbers carries a range or a confidence interval.
- **The runs are not independently re-checkable.** The per-trial rows are not retained,
  and the harness never wrote final poses, so a repaired run’s validity rests on the
  harness’s own separating-axis check.
  Regenerating the rows repeats that check; it is not an independent one.
- **Coverage is thin.** `n = 17`, 26 and 29 have repaired runs at level 6 only.
  Levels 1 and 3 were measured only before runs were repaired, and levels 5, 7 and 9 not
  at all.
- **The repair only translates.** Whether a repair that rotates changes the scores is
  untested. A compaction pass was tried and its code was not kept, so
  [exp-209](../series/series-000-smoke-and-calibration/experiments/exp-209-h211-an-unretained-compaction-pass.md)
  supports no conclusion.
- **The open hypotheses are untested:** whether restarts beat schedule tuning at equal
  cost (H-207), whether the drop decides the outcome (H-208), and whether any setting
  reaches a record (H-209). H-210 and H-211 were registered from the data of exp-210 and
  exp-208, so those rounds are exploratory data, filed under the open question H-212,
  and neither claim has had a test.
- **One instrument.** These are the workbench’s simulation in one headless Chromium on
  one laptop. They say nothing about the campaign’s Rust engine.

## 6. What Follows

- **Re-measure before reusing any number here.** From #160 on, the package benchmark
  keeps each trial’s raw and repaired poses and reports disjoint seed blocks, which is
  what these observations lack.
- **Measure success against how much the run is given.** Blind is one level between
  nothing and the full answer.
  The
  [annealing plan](../../../docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md)
  lays out the levels in between, from the record’s connected components to its contact
  graph and rigid clusters.

## Evidence

- **Retained:** `packing/campaign/results/annealing/summaries.json`, which holds one
  median and one best-of-first-k ladder per cell, per run file.
  `packages/workbench/tools/workbench_tools/summarize_annealing.py` wrote it.
  Cells marked `resolved: true` were scored on runs repaired to packings.
  Several files replay the same seeds, so their trial counts overlap.
- **Not retained:** the per-trial rows, removed from the branch at `6e191a35` to keep
  the diff reviewable.
  The harness never wrote final poses.
- **Checked on 2026-09-14, against local copies of the rows** that are not in the
  repository: `summarize_annealing --check` matched all 59 run files, and `--overlaps`,
  over the 59.7 MB behind the `resolved: true` cells, gave the figures in section 3. No
  run would be refused, every repaired overlap is finite and at most 1e-9, and seeds run
  contiguously from 0.
- **Regenerable:** the [runbook](../results/annealing/README.md#what-is-retained) gives
  the commands that rewrite the rows and re-check them.
  One file, `resolved-5k-a6.jsonl`, was regenerated on #155’s branch and matched its
  summary.
- **Instrument:** these runs used `packing/devtools/bench_annealing.py`, which #160
  replaced with the package benchmark `squares-workbench-benchmark`
  (`packages/workbench/tools/workbench_tools/benchmark.py`).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
