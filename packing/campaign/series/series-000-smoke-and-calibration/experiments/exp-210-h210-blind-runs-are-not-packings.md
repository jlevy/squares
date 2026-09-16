---
title: exp-210 — blind runs of the workbench's physics end with squares overlapping
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-210
  series: series-000
  title: Blind runs of the workbench's physics end with squares overlapping
  date: '2026-09-12'
  hypotheses:
  - H-212
  tier: exploratory
  known_defects: [D-067]
  subject:
    label: the workbench's contact simulation in blind mode, which withholds the destination poses
    engine: workbench page, build 4.4 MB, branch claude/annealing-search-benchmark
    engine_commit: d3c3a778
    assurance: numerically-checked
    method: numerical-f64
    tolerance: 1e-5 of a unit side of deepest pairwise overlap, chosen; the snapped observation
      beside it was run once and not kept (think-2ngs)
    host_system: macOS on Apple silicon, one headless Chromium
    selftest_passed: false
    precision:
      binary_bits: 53
      rounding: nearest-even
    migration_annotation: '2026-09-13: source reference mapped from pre-purge ee27f8e3 to reachable
      d3c3a778; the retained harness and workbench source trees compare equal in Git. Original
      run provenance was not recaptured. The 15,000 trials are the three summaries.json entries
      named in record: the command wrote the 12,000 in guarded-a6.jsonl, and 500 seeds at each
      of n = 5, 11 and 17 at shake levels 0 and 3, whose commands were not recorded, wrote
      guarded-a0.jsonl and guarded-a3.jsonl.'
  instance:
    axis: n
    point: 11
    role: target
  method:
    operator: claude-opus-5, unattended
    control: none retained; the snapped trajectory, which ends on the record's poses by
      construction, was measured once with a probe variant that was not kept (think-2ngs)
    candidate: the blind trajectory, which starts from the previous record and is not given the
      destination poses
    trials: 15000
    interleaved: false
    commit: d3c3a778
    entry_point: packing/devtools/bench_annealing.py
    command: python -m devtools.bench_annealing --n 5 10 11 17 26 29 --seeds 2000 --anneal 6
      --budget 900
    record: packing/campaign/results/annealing/summaries.json, entries guarded-a6.jsonl,
      guarded-a0.jsonl and guarded-a3.jsonl
  results:
  - shape: determination
    question: does any blind run end on an arrangement with no overlapping squares, checked
      by a separating-axis test over the final poses written in the harness rather than read
      off the simulation
    role: guard
    outcome: invalid
  complexity:
    lines_changed: 96
    new_failure_modes:
    - a trial can now be refused as invalid rather than recorded as poor
    notes: The check is the change; the simulation was not touched. It voided every result
      recorded before it.
  verdict:
    decision: unresolved
    primary_criterion: the deepest pairwise overlap in the final arrangement
    reason: Every blind run observed ended overlapping, but the snapped control was measured
      once with a probe variant that was not kept, and neither the trials nor their final poses
      are in the repository, so the observation cannot be re-checked from it.
    commit: d3c3a778
  effort:
    stopped_by: dependency
    wall_seconds: unrecorded-historical
    migration_annotation: '2026-09-13: no complete elapsed-time receipt was retained. Per-trial
      median milliseconds and approximate prose budgets cannot recover total wall or operator
      time. This marker records missing history and is unavailable to new experiments.'
---
# exp-210 — Blind Runs of the Workbench’s Physics End With Squares Overlapping

**Renumbered 2026-09-13** from exp-206, which the older divide-and-concur experiment
keeps.

**Rewritten 2026-09-14** to remove superseded framing and layered corrections.
The previous text is at commit `a40d272c`.

**Exploratory data, filed under the open question
[H-212](../../../hypotheses/H-212-the-workbench-physics-as-a-search.md).** These runs
came first, at `d3c3a778`, and H-210 was registered from them at `385707be`, so they
cannot also be its test.

## What Was Measured

A blind run starts from the known-best packing for `n - 1`, drops the new square into
the emptiest cell of a coarse grid, and runs contact forces, wall forces and a decaying
shake while the container contracts toward the known-best side for `n`. It is not given
the destination poses.
In the `bodies` style the benchmark used, squares also move as rigid blocks whose
membership comes from matching the two records.

The measurement is the deepest overlap between any two squares in the arrangement the
run **ends on**. A separating-axis test computes it from the final poses, in the
harness, without using the simulation’s own bookkeeping.
The page’s `maxPenetration` is a running maximum over the whole trajectory and says
nothing about where the squares stopped.

## A Chosen Tolerance Beside an Unretained Control

| mode | n = 5 | n = 11 | n = 17 |
| --- | ---: | ---: | ---: |
| snap: ends on the record’s poses by construction | 5.5e-7 | 1.0e-6 | 7.3e-7 |
| free: pulled toward the destination poses, not snapped | 3.9e-5 | 4.5e-5 | 3.1e-2 |
| blind: not given the destination poses | 8.4e-2 | 3.5e-2 | 8.6e-2 |

The snapped row is the float noise the stored poses carry.
The snap and free rows came from a variant of the probe that was run once and not kept.
The committed harness runs blind only, so this control is recorded, not reproducible.
The tolerance, 1e-5 of a side, was chosen rather than derived from it.
It is ten times the largest snapped value and a factor of 3.9 below the smallest free
value; the blind values are more than three orders of magnitude above it.

## Result

Every blind run observed ended with at least one pair of squares overlapping.
The repaired rounds wrote a row per run.
Local copies of those rows, which are not retained, cover 123,190 runs: none ended below
1e-5, and the deepest overlap before repair ranged from 0.002 to 0.118 of a side, with a
median of 0.083.

## What It Means

- **Nothing measured before this check describes a packing.** A side read from the final
  arrangement was a bounding box around overlapping squares, and a bounding box shrinks
  when squares are allowed to intersect.
  That is why some early parameter cells reported a container below the known-best side.
  Those results are void and appear nowhere in the record.
- **Scoring needs a repair step.** The harness now separates overlapping squares,
  translation only with angles held, and scores the container that the repaired
  arrangement needs.
  [X-034](../../../explorations/X-034-the-workbench-physics-as-a-search.md) reports what
  repaired runs are worth.

## Why the Overlap Survives

The page’s own schedule allows it.
In blind mode the walls close toward the known-best side, and the contraction advances
whenever the deepest overlap is at most `BLIND.overlapTol`, which is 0.08 of a unit side
(`workbench.js`, the blind branch of the trajectory loop).
The walls stop at the known-best side and never go below it.

So a blind run is squeezed into the record’s own container while squares may overlap by
up to 0.08. The observed overlaps, with a median of 0.083, sit at that tolerance.
It also explains the early cells that reported a container below the known-best side:
squares compressed inside a record-sized box can have a smaller bounding box than the
box.

The snapped and free modes add target springs that pull each square toward its
destination. Blind mode has none, so nothing drives the overlap out.

## Evidence

The per-trial rows are not retained and the harness never wrote final poses, so the
repository alone cannot re-check this result; the runbook regenerates the rows.
The blind rows are cheap to reproduce: from `packing/`, run
`uv run --frozen --all-extras --group dev squares-workbench-benchmark --n 5 11 17 --seeds 200`.
Each trial row it writes under `campaign/results/annealing/` carries `overlap`, the
deepest pairwise overlap before repair.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
