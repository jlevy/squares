---
title: exp-130 — the robust end-band theorems at 96/25
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-130
  series: series-000
  title: >-
    Widen the robust end band [0°, α] ∪ [45° − β, 45°] excluded at 96/25 until the exact
    decision fails, and register the widest bands decided
  date: '2026-09-08'
  hypotheses: [H-130]
  tier: confirmatory
  subject:
    label: >-
      the composition-(11, 0) class program on end-cell unions [0°, α] ∪ [45° − β, 45°] at
      side 96/25, shrink B = 9977/10000, on the retained 181-direction net, over the
      79 × 79 and 119 × 119 product site grids inset 1/10 from the walls
    engine: >-
      sqpack 0.2.0 fractional.classcert — solve_class_program proposes, decide_class_program
      decides on the event-cell sweep — driven by the lane's bandlib.py and widen.py, which
      are listed verbatim in lane B's appendix of scripts as run
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
      the planning lane's own points, replayed on the same inputs before anything was
      widened: the (6, 6) end band [0°, 1.4503°] ∪ [43.7565°, 45°] (Theorem 1.11) must
      return the planning lane's exact mass 10959/1024 to the fraction, and lane B's
      end-cell rows at grid 79 stand as the prereq controls H-130 declared. Every
      non-refutation is then checked against the depth oracle: the LP dual of a class whose
      grid-79 value stays at or above eleven is read by direction with histogram.py and
      handed to ceiling.py through ceiling_check.py, so a site-set reading cannot be
      recorded as an obstruction.
    candidate: >-
      the end band widened cell by cell on the same site set — symmetric (a = b) from the
      planning lane's a = b = 6 until Condition 2' fails, then asymmetric from the widest
      symmetric success, one end held and the other pushed; then the failing points rerun on
      the 119 × 119 grid with everything else unchanged. Each point is one solve_class_program
      search followed by decide_class_program on the rationalised point reached, decided
      regardless of convergence because the exact sweep is complete and the loop's rows are a
      subset of the placements.
    runs_per_condition: 1
    interleaved: false
    operator: >-
      the BC-295 lane agent of agenda-030, bead think-ndqj, session-102; the record was
      written by a separate record lane from the frozen result section
    commit: f010f32f
    dirty: false
    entry_point: >-
      packing/src/sqpack/fractional/classcert.py, reached through the lane's bandlib.py and
      widen.py, whose full text is in lane B's "Appendix: scripts as run (session-102)"
    command: >-
      from packing/, PACK_JOBS=1 OMP_NUM_THREADS=1 uv run --frozen --all-extras --group dev
      python widen.py widen_g79.jsonl 79 7 13, then the same script with grid 119 for the
      points grid 79 could not refute; the scripts live in the session scratchpad and are
      reproduced verbatim in the result section's appendix, so the appendix is the artifact
      to re-run from, not a repository console script
    budget: >-
      the research phase of session-102 — 78 minutes of a 150-minute session clock on one
      worker — with the row loop capped at a hundred rounds per point
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-b-angle-classes.md
  effort:
    timebox: 78m, the research phase of session-102 inside its 150-minute clock
    wall_seconds: 2231
    stopped_by: criterion
  results:
  - shape: determination
    role: outcome
    question: >-
      Is there an exact-decided robust end band [0°, α] ∪ [45° − β, 45°] excluded at 96/25
      with α + β of at least 3°?
    outcome: criterion_met
    checked_by: >-
      decide_class_program at thresholds (1, 0) for the composition (11, 0). Theorem A,
      cells 0–6 ∪ 174–180 on grid 79, is [0°, 1.7139°] ∪ [43.5293°, 45°] with α + β =
      3.1846°, mass 5529/512 = 10.798828125 over 152 D4-closed atoms and least covered core
      4099/4096 on every one of its fourteen class directions. Theorem B, cells 0–39 ∪
      174–180 on grid 79, is [0°, 10.3875°] ∪ [43.5293°, 45°] with α + β = 11.8582°, mass
      351/32 = 10.96875 over 216 atoms and least core 4101/4096 over 47 directions.
      Theorem C, cells 0–39 ∪ 172–180 on grid 119, is [0°, 10.3875°] ∪ [43.0737°, 45°] with
      α + β = 12.3138°, mass 11083/1024 = 10.8232421875 over 296 atoms and least core
      4101/4096 over 49 directions. Conditions 1, 3 and 4 hold at every one of the three,
      with B(1 + D) = 899996306539/900000000000 < 1 for the net.
  - shape: record
    role: mechanism
    metric: widest exact-decided α + β of an end band excluded at 96/25, in degrees
    direction: higher
    score: 12.3138
    score_str: 'Theorem C, 12.3138° on grid 119; 11.8582° (Theorem B) on grid 79'
    standing_best: 2.6937
    standing_best_source: >-
      the planning lane's (6, 6) point, [0°, 1.4503°] ∪ [43.7565°, 45°], decided on one site
      set in a planning lane and never registered
    beat_record: true
    runs: 40
  - shape: determination
    role: guard
    question: >-
      Did either declared falsifier occur — a fractional packing on the end cells of value at
      least eleven at 96/25, or eleven pairwise disjoint B-cores at end-cell directions inside
      the container?
    outcome: criterion_met
    checked_by: >-
      Neither. No refuted point produced a core of mass below one at any class direction, so
      Condition 5' never failed on a band this record claims, and no eleven disjoint B-cores
      exist in the container at all: 96/25 ÷ (9977/10000) = 3.8489 is below every known side
      for eleven unit squares. The site-set duals that did reach eleven on grid 79 were sent
      to ceiling.py and all three fail as continuum obstructions — exact maximum depth 2, 2
      and 1291/568, scaling their totals to 11/2, 11/2 and 6392/1291 = 4.9512 — so every
      grid-79 non-refutation is a site-set reading and is recorded as one.
  verdict:
    decision: accepted
    primary_criterion: >-
      an exact-decided robust end band [0°, α] ∪ [45° − β, 45°] excluded at 96/25 with
      α + β of at least 3°
    reason: >-
      H-130's criterion is met and passed three times over: Theorem A clears the 3° bar by
      0.1846° on grid 79 in the shape the hypothesis asked for, Theorem B by 8.8582° on the
      same grid, and Theorem C by 9.3138° on grid 119 — each an exact decision of
      decide_class_program, none of them using Stromquist's Theorem 3 or its lemmas.
---
# exp-130 — The First Rung of the Band Ladder, Decided

[H-130](../../../hypotheses/H-130-robust-end-band-theorem-at-q.md) asked for one thing:
an end band around `0°` and `45°`, wide enough that `α + β ≥ 3°`, that no packing of
eleven unit squares at side `96/25` can lie inside — decided exactly, not transported
from Stromquist. Lane BC-295 of
[agenda 030](../../../agendas/agenda-030-parallel-structural-lanes-at-n11.md), bead
`think-ndqj`, ran the widening in
[session-102](../../../agent-sessions/session-102-angle-band-theorems-at-q.md) and froze
three theorems. This record registers them.
Everything below is read from
[lane B’s session-102 section](../results/agenda-030/lane-b-angle-classes.md#session-102--angle-band-theorems-at-9625-2026-09-08),
which holds the widening tables, the proofs, and the scripts.

## What was tested, and what would have refuted it

The class is `[0°, α(a)] ∪ [45° − β(b), 45°]` for `a` leading and `b` trailing half-gap
cells of the net, with `α(a)` the exact upper tangent of cell `a − 1` and `45° − β(b)`
the exact lower tangent of cell `181 − b`. Both ends are closed.
The question is whether the composition-`(11, 0)` class program refutes that class: if
the class measure has total mass below eleven while every direction of the class carries
a covered core of mass at least one, then eleven pairwise disjoint `B`-cores at class
directions cannot fit, so no packing of eleven has all its folded angles in the band.

The falsifiers were fixed before the runs: **a fractional packing on the end cells of
value at least eleven at `96/25`, or eleven pairwise disjoint `B`-cores at end-cell
directions in the container.** Neither occurred.
A non-refutation on a site set is neither of those — it is a site-set reading, and every
one of them is labelled as such below.

## Inputs, fixed for every point

Side `q = 96/25`. Shrink `B = 9977/10000`. The retained 181-direction net from
`cases/n11_fractional_certificate/certificate.json`: half-tangent limit `207107/500000`,
180 equal steps, cell width about `0.264°` at the axis end and `0.225°` at the diagonal
end. Site set `build_site_grid(96/25, 79, 1/10)` — the `79 × 79` product grid inset
`1/10` from the walls, folded into `D4` orbits, `6241` sites in `820` orbits — and, for
the refinement, `build_site_grid(96/25, 119, 1/10)` with `14 161` sites.
Composition `(11, 0)`; `rows_per_direction = 3`; the row loop capped at a hundred
rounds, with the point reached decided regardless of convergence, because the exact
sweep is complete and the loop’s rows are a subset of the placements.
Rationalisation at scale `4096` with the standard bump `1 + 10⁻⁶`. Exact thresholds
`(1, 0)`. A class is a union of half-gap cells and its folded range is the closed union
of the cells’ exact-tangent bounds (`DirectionClasses.cell_bounds`).

Legal touching is retained throughout: a square’s `B`-core lies in its open interior
(Condition 4), so the cores of a packing are pairwise disjoint even where squares touch.

## The three theorems, and their exact domains

**Theorem A — the band H-130 asked for.** No packing of eleven unit squares in
`[0, 96/25]²` has every folded angle in `[0°, 1.7139°] ∪ [43.5293°, 45°]`; exactly, in
the closed set of angles whose tangent lies in
`[0, 40385865000000/1349699746833857] ∪ [1077991935000000/1134804266494367, 1]`. Cells
`0–6 ∪ 174–180`, grid 79, converged in 49 rounds.
Mass `5529/512 = 10.798828125` over 152 `D4`-closed atoms, least covered core
`4099/4096` on every one of the fourteen class directions, Conditions 1, 3 and 4 holding
with `B(1 + D) = 899996306539/900000000000 < 1`. Here `α + β = 3.1846°`, which clears
H-130’s `3°` criterion **by `0.1846°`**. This is the statement the hypothesis asked for
and the one that decides it.

**Theorem B — the widest on grid 79.** The same for `[0°, 10.3875°] ∪ [43.5293°, 45°]`,
tangent in
`[0, 12271089750000/66942386977163] ∪ [1077991935000000/1134804266494367, 1]`. Cells
`0–39 ∪ 174–180`, grid 79, 41 rounds, mass `351/32 = 10.96875` over 216 atoms, least
core `4101/4096` over the 47 class directions.
Here `α + β = 11.8582°`, clearing the criterion by `8.8582°`.

**Theorem C — the widest decided at all.** The same for
`[0°, 10.3875°] ∪ [43.0737°, 45°]`, tangent in
`[0, 12271089750000/66942386977163] ∪ [177594252500000/189956166180167, 1]`. Cells
`0–39 ∪ 172–180`, grid 119, 81 rounds, mass `11083/1024 = 10.8232421875` over 296 atoms,
least core `4101/4096` over the 49 class directions.
Here `α + β = 12.3138°`, clearing the criterion by `9.3138°`.

Theorem C contains Theorem B contains Theorem A. Equivalently, since `96/25 = 3.84`:
every packing of eleven unit squares at side at most `3.84` has a square whose folded
angle lies in `(1.7139°, 43.5293°)` — farther than `1.7139°` from `0°` and than
`1.4707°` from `45°` — and, by Theorem B, one whose folded angle lies in
`(10.3875°, 43.5293°)`. Trump’s packing satisfies all three with room, as it must: its
five tilted squares sit at `40.18°`, inside `(10.39°, 43.53°)`.

## How the band was widened

Symmetric first, `a = b`, from the planning lane’s `a = b = 6`: the `(6, 6)` control
returned the planning lane’s exact mass `10959/1024 = 10.70215` to the fraction,
`(7, 7)` refuted at `5529/512`, and `(8, 8)` did not, its exact mass reaching
`5637/512 = 11.00977` with Condition 2′ failing.
From the widest symmetric success the widening went asymmetric: the trailing end held at
seven cells (`β = 1.4707°`) and the leading end pushed from `(8, 7)` to `(40, 7)`, every
point refuted, with the float value pinned at `10.7761` across the whole run from
`1.71°` to `9.08°` of axis width.
Pushing the trailing end instead — `(6, 8)`, `(3, 8)`, `(1, 8)`, `(1, 10)` — fails on
grid 79 at every axis width, including a single axis cell.
The `45°` end is the binding end.

Then the failing points were rerun on grid 119 with nothing else changed, and grid 119
refuted `(8, 8)`, `(7, 8)`, `(9, 9)`, `(10, 10)`, `(11, 11)`, `(12, 12)`, `(40, 8)` and
`(40, 9)` — the last being Theorem C. It also lowered the value of `(7, 7)` from
`10.799` to `43857/4096 = 10.70728`. The site set, not the relaxation, was what stopped
the diagonal end on grid 79.

## Limits

- **A non-refutation on a site set is not a falsification.** This is lane B §3.2 and the
  exp-064 lesson, and this round is the sharpest illustration of it yet: `(8, 8)` reads
  as “not refuted” on grid 79 and is refuted on grid 119 with nothing else changed.
  Every grid-79 row in the widening table that failed Condition 2′ is a grid-79 reading
  only.
- **The duals that reach eleven are not obstructions.** `ceiling.py`, driven through
  `ceiling_check.py`, decides the symmetrised dual families exactly: continuum depth `2`
  for the `(8, 8)` and `(7, 8)` duals and `1291/568` for the band toward `40.19°`,
  scaling their totals to `11/2`, `11/2` and `6392/1291 = 4.9512`. A depth of two is two
  cores of a near-integral family overlapping in a region containing no site — at grid
  79 the spacing is `0.0467` and a `B`-core is `0.9977` wide.
  The fractional obstruction the site set shows is an artefact of the site set.
- **The ladder’s true rung is not here.** `(13, 13)` and `(40, 10)` at grid 119 were cut
  off by the clock rather than decided, so neither end is known to be exhausted there,
  and the widest exact-decided band is a property of the site set as much as of the
  side. What is registered is a lower bound on the rung, not the rung.
- **Wall times are not comparable.** Every measurement ran at load average eight on four
  cores with one worker; the declared `2231` seconds is the sum of the per-point wall
  times in the three widening tables and nothing else — the dual and ceiling work is
  reported as a guard here and its time is not counted in it.
- **Nothing about a packing bound.** The theorems restrict where the angles of a packing
  of eleven can be. They give no new side, and no result is written to the frontier
  register.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
