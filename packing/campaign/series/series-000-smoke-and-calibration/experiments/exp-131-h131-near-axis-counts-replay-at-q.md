---
title: exp-131 — the near-axis and near-45° counts at 96/25, replayed under a registered round
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-131
  series: series-000
  title: >-
    Replay every planning-lane angle count at 96/25 and U with the exact verifier, under a
    registered round
  date: '2026-09-08'
  hypotheses: [H-131]
  tier: confirmatory
  subject:
    label: >-
      the composition-(11, 0) class program on the eight cell unions H-131 names, at sides
      96/25 and 3877084/10⁶ ≥ U, shrink B = 9977/10000, on the retained 181-direction net
      over the 79 × 79 product site grid inset 1/10 from the walls
    engine: >-
      sqpack 0.2.0 fractional.classcert — solve_class_program proposes, decide_class_program
      decides on the event-cell sweep, class_minima supplies the nine-point control — driven
      by the lane's bandlib.py, replay.py and nine_replay.py, listed verbatim in lane B's
      appendix of scripts as run
    engine_commit: f010f32f
    assurance: verified
    method: exact-algebraic
    host_system: >-
      linux x86_64, four cores at load average eight shared with five other lanes, one
      worker (PACK_JOBS=1, OMP_NUM_THREADS=1), project Python 3.14
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      each row carries the planning lane's own exact mass as its control and must reproduce
      it to the fraction on the same inputs; the planning lane's figures are in lane B §2.3.
      Two further controls stand outside the table: Theorem 1.5's nine-point control, the
      pushed set at {1 − δ, L/2, L − 1 + δ}² replayed through class_minima at both sides for
      δ ∈ {0, 1/200, 1/100}, whose declared falsifier is an admissible B-core at a direction
      of the leading eighteen cells that misses all nine atoms; and the L/4 grid control at
      both sides, run by the same script.
    candidate: >-
      the eight counts H-131 states, decided rather than cited: at 96/25 the classes 0–24,
      0–39, 171–180, 149–169 and 117–180, and at 3877084/10⁶ the classes 0–24, 0–29 and
      175–180. The two end-cell rows the planning lane also decided — 0–5 alone and the
      union 0–5 ∪ 175–180, Theorem 1.11 — and the trailing-six class 175–180 at 96/25 were
      replayed with them. Each row is one solve_class_program search followed by
      decide_class_program on the rationalised point reached, decided regardless of
      convergence because the exact sweep is complete and the loop's rows are a subset of
      the placements.
    runs_per_condition: 1
    interleaved: false
    operator: >-
      the BC-295 lane agent of agenda-030, bead think-ndqj, session-102; the record was
      written by a separate record lane from the frozen result section
    commit: f010f32f
    dirty: false
    entry_point: >-
      packing/src/sqpack/fractional/classcert.py, reached through the lane's bandlib.py,
      replay.py and nine_replay.py, whose full text is in lane B's "Appendix: scripts as run
      (session-102)"
    command: >-
      from packing/, PACK_JOBS=1 OMP_NUM_THREADS=1 uv run --frozen --all-extras --group dev
      python replay.py replay.jsonl, then the same runner on nine_replay.py for the two
      controls; the scripts live in the session scratchpad and are reproduced verbatim in the
      result section's appendix, so the appendix is the artifact to re-run from, not a
      repository console script
    budget: >-
      the first task of the research phase of session-102 — part of 78 minutes on one worker
      inside a 150-minute session clock — with the row loop capped at a hundred rounds per
      class
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-b-angle-classes.md
  effort:
    timebox: 78m, the research phase of session-102 inside its 150-minute clock
    wall_seconds: 1870
    stopped_by: criterion
  results:
  - shape: determination
    role: outcome
    question: >-
      Does every count H-131 states decide exactly on the stated site set, with the class
      mass below the next integer above the stated count?
    outcome: criterion_met
    checked_by: >-
      decide_class_program at thresholds (1, 0) for the composition (11, 0), on
      build_site_grid(side, 79, 1/10). At 96/25: class 0–24, [0°, 6.4537°], exact mass
      4611/512 = 9.00586, least core 2049/2048, at most nine; class 0–39, [0°, 10.3875°],
      10765/1024 = 10.51270, least core 1025/1024, at most ten; class 171–180,
      [42.8453°, 45°], 9989/1024 = 9.75488, least core 2053/2048, at most nine within
      2.1547° of 45°; class 149–169, [37.7333°, 42.6166°], 41529/4096 = 10.13892, least core
      1037/1024, at most ten within 2.44° of 40.194°; class 117–180, [30.0149°, 45°],
      42589/4096 = 10.39771, least core 4147/4096, at most ten. At 3877084/10⁶: class 0–24,
      10065/1024 = 9.82910, least core 4101/4096, at most nine; class 0–29, [0°, 7.7671°],
      10243/1024 = 10.00293, least core 4097/4096, at most ten; class 175–180,
      [43.7565°, 45°], 5201/512 = 10.15820, least core 2051/2048, at most ten within 1.2435°
      of 45°. Every one of the eight reproduces the planning lane's exact mass to the
      fraction, and Condition 5' holds on each, which is what makes the floor of the mass
      the count bound by Theorem 1.5's counting step.
  - shape: determination
    role: guard
    question: >-
      Did any declared count falsifier occur — a core of mass below one at some direction of
      a class H-131 names, a class mass reaching N + 1, or N + 1 pairwise disjoint B-cores at
      directions of the class inside the container?
    outcome: criterion_met
    checked_by: >-
      None on any class H-131 names. The single Condition 5' failure in the whole replay is
      the trailing-six class 175–180 at 96/25 alone, least core 1021/1024 at direction 175,
      which the planning lane also left float-only and which H-131 does not rest on at that
      side: the same bound follows from the decided class 171–180, since [43.7565°, 45°] is
      contained in [42.8453°, 45°]. The two end-cell rows also replayed exactly — 0–5 at
      2305/256 = 9.00391 with least core 4097/4096, and Theorem 1.11's union 0–5 ∪ 175–180
      at 10959/1024 = 10.70215 with least core 1025/1024, refuting the composition (11, 0).
  - shape: determination
    role: guard
    question: >-
      Does Theorem 1.5's pushed nine-point set still pierce the leading cells at both sides,
      so the counting step the bounds rest on is sound on this net?
    outcome: criterion_met
    checked_by: >-
      nine_replay.py drove class_minima over the pushed set at {1 − δ, L/2, L − 1 + δ}² at
      both sides for δ ∈ {0, 1/200, 1/100}, plus the L/4 grid control, and the section
      records that no falsifier occurred: no admissible B-core at a direction of the leading
      eighteen cells missed all nine atoms. The per-run cell counts are in the lane's queue
      log in the session scratchpad rather than in the result section, so they are not
      restated here.
  verdict:
    decision: accepted
    primary_criterion: >-
      every count H-131 states, decided exactly by decide_class_program on the stated site
      set, with the class mass below the next integer above the stated count
    reason: >-
      All eight counts are now decided under a registered round rather than cited from a
      planning lane, every exact mass reproduces the planning lane's to the fraction, and no
      declared falsifier occurred — so H-131 is confirmed as stated and its counts may be
      cited as results of this record, on the site set this record names.
---
# exp-131 — The Angle Counts at `96/25`, Replayed

[H-131](../../../hypotheses/H-131-near-axis-counts-at-q.md) was registered to be
replayed, not to be discovered.
Its counts had been exact-verified in a planning lane on a stated site set, and the
hypothesis says plainly that until a registered round reproduces them they are planning
evidence only. Lane BC-295 of
[agenda 030](../../../agendas/agenda-030-parallel-structural-lanes-at-n11.md), bead
`think-ndqj`, ran that replay as the first task of
[session-102](../../../agent-sessions/session-102-angle-band-theorems-at-q.md).
This record registers it.
Every figure below is read from
[lane B’s session-102 section](../results/agenda-030/lane-b-angle-classes.md#session-102--angle-band-theorems-at-9625-2026-09-08).

## What was tested, and what would have refuted it

For a class `Θ` — a union of half-gap cells of the net — and a claimed bound “at most
`N`”, the class program decides the bound when the class measure has total mass `M` and
every direction of `Θ` carries a covered core of mass at least one (Condition 5′). Each
square of a packing contains its closed `B`-core at the net direction whose cell holds
its angle, and those cores are pairwise disjoint, so at most `⌊M⌋` of them can have an
angle in `Θ`. That is Theorem 1.5’s counting step, and the nine-point control is what
keeps it honest.

The falsifiers were fixed before the runs.
**For a count class: the exact sweep reports a core of mass below one at some direction
of `Θ`, or the exact mass reaches `N + 1`, or `N + 1` pairwise disjoint `B`-cores at
directions in `Θ` fit in `[0, 96/25]²`. For the nine-point control: an admissible
`B`-core at a direction of the leading eighteen cells that misses all nine atoms.** None
occurred on any class H-131 names.

## Inputs, fixed for every row

Side `q = 96/25`, and `3877084/10⁶ ≥ U` for the three `U` rows.
Shrink `B = 9977/10000`. The retained 181-direction net from
`cases/n11_fractional_certificate/certificate.json`: half-tangent limit `207107/500000`,
180 equal steps, cell width about `0.264°` at the axis end and `0.225°` at the diagonal
end.
Site set `build_site_grid(side, 79, 1/10)` — the `79 × 79` product grid inset `1/10`
from the walls, folded into `D4` orbits, `6241` sites in `820` orbits.
Composition `(11, 0)`; `rows_per_direction = 3`; the row loop capped at a hundred
rounds, with the point reached decided regardless of convergence.
Rationalisation at scale `4096` with the standard bump `1 + 10⁻⁶`. Exact thresholds
`(1, 0)`. Folded ranges are the closed union of the cells’ exact-tangent bounds
(`DirectionClasses.cell_bounds`). Legal touching is retained: a square’s `B`-core lies
in its open interior (Condition 4), so the cores are pairwise disjoint even where
squares touch.

## The replay

Each row is one `solve_class_program` search followed by `decide_class_program` on the
rationalised point reached; “least core” is the exact least covered mass over every
direction of the class, and the count bound is `⌊M⌋` whenever Condition 5′ holds.

| class (cells) | folded range, closed | side | rounds | exact `M` | least core | count | planning lane | wall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0–24 | `[0°, 6.4537°]` | `96/25` | 9, converged | `4611/512 = 9.00586` | `2049/2048` | **≤ 9** | `9.00586` | 3 s |
| 0–39 | `[0°, 10.3875°]` | `96/25` | 14, converged | `10765/1024 = 10.51270` | `1025/1024` | **≤ 10** | `10.51270` | 6 s |
| 171–180 | `[42.8453°, 45°]` | `96/25` | 100, cap | `9989/1024 = 9.75488` | `2053/2048` | **≤ 9** | `9.75488` | 67 s |
| 149–169 | `[37.7333°, 42.6166°]` | `96/25` | 100, cap | `41529/4096 = 10.13892` | `1037/1024` | **≤ 10** | `10.13892` | 596 s |
| 117–180 | `[30.0149°, 45°]` | `96/25` | 60, converged | `42589/4096 = 10.39771` | `4147/4096` | **≤ 10** | `10.39771` | 1149 s |
| 0–5 | `[0°, 1.4503°]` | `96/25` | 12, converged | `2305/256 = 9.00391` | `4097/4096` | **≤ 9** | `9.00391` | 1 s |
| 175–180 | `[43.7565°, 45°]` | `96/25` | 100, cap | `9925/1024 = 9.69238` | `1021/1024` at 175 | undecided, 5′ fails | float only | 24 s |
| 0–5 ∪ 175–180 | `[0°, 1.4503°] ∪ [43.7565°, 45°]` | `96/25` | 29, converged | `10959/1024 = 10.70215` | `1025/1024` | **refutes `(11, 0)`** | `10.70215` | 5 s |
| 0–24 | `[0°, 6.4537°]` | `3877084/10⁶` | 17, converged | `10065/1024 = 9.82910` | `4101/4096` | **≤ 9** | `9.82910` | 6 s |
| 0–29 | `[0°, 7.7671°]` | `3877084/10⁶` | 7, converged | `10243/1024 = 10.00293` | `4097/4096` | **≤ 10** | `10.00293` | 4 s |
| 175–180 | `[43.7565°, 45°]` | `3877084/10⁶` | 63, converged | `5201/512 = 10.15820` | `2051/2048` | **≤ 10** | `10.15820` | 9 s |

Every exact mass reproduces the planning lane’s to the fraction, on the same inputs.
So H-131’s list is decided under this record: at `96/25`, at most nine squares have
folded tilt within `6.4537°` of the axes, at most ten within `10.3875°`, at most nine
within `2.1547°` of `45°`, at most ten within `±2.44°` of `40.194°`, and at most ten
with folded tilt in `[30.0149°, 45°]` — so some square is tilted below `30.0149°`. At
`3877084/10⁶ ≥ U`, at most nine within `6.4537°`, at most ten within `7.7671°`, and at
most ten within `1.2435°` of `45°`.

## The one row that stays undecided, and why it costs nothing

The trailing six cells alone at `96/25` fail Condition 5′: the least covered core is
`1021/1024` at direction 175, below one, so the class program declines to give a bound
there. That row was float-only in the planning lane too, and it is not one of H-131’s
claims at `96/25`: the count within `2.1547°` of `45°` comes from the decided class
`171–180`, and `[43.7565°, 45°] ⊂ [42.8453°, 45°]`, so at most nine holds on the smaller
band as well. At `U` the same six cells do decide, least core `2051/2048`, which is the
row H-131’s `U` clause needs.

## The controls

`nine_replay.py` replayed Theorem 1.5’s nine-point control — the pushed set at
`{1 − δ, L/2, L − 1 + δ}²` through `class_minima` — at both sides for
`δ ∈ {0, 1/200, 1/100}`, together with an `L/4` grid control, and no declared falsifier
occurred: nothing produced an admissible `B`-core at a direction of the leading eighteen
cells that missed all nine atoms.
The per-run cell counts are in the lane’s queue log in the session scratchpad, not in
the result section, and are not restated here.
Beyond that, every row is its own control, because each carries the planning lane’s
exact mass and had to reproduce it as a fraction rather than as a rounded figure.

## Limits

- **These are counts on a site set.** Every bound above is a theorem of the exact
  verifier over `build_site_grid(side, 79, 1/10)`. A finer or coarser site set is a
  different measurement, and a non-refutation on a site set is not a falsification —
  lane B §3.2, the exp-064 lesson.
  What transfers unconditionally is the direction of the inequality: a decided mass is
  an upper bound on the count, so refining the site set can only lower it.
- **The floors are sharp in kind, not in width.** Nine squares at any common tilt up to
  `30°` fit in the container, so no covering method gets a near-axis count below nine;
  the only room left in these statements is the width of the band, not the count.
- **Wall times are not comparable.** The measurements ran at load average eight on four
  cores with one worker: the `[30°, 45°]` row took 1 149 s here against 700 s in the
  planning lane. The declared `1870` seconds is the sum of the table’s per-row wall
  times; the two controls were not separately timed in the result section and are not in
  it.
- **Nothing about a packing bound.** These are constraints on where the angles of a
  packing of eleven can be.
  No side is established and no result is written to the frontier register.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
