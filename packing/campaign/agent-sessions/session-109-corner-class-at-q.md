---
title: session-109 — the corner-class LP under the corner-pair condition at 96/25 (BC-292)
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-109
  title: The corner-class LP under the corner-pair condition at 96/25 (BC-292, H-126, H-127)
  date: '2026-09-08'
  started_at: '2026-09-08T15:35:02Z'
  deadline_at: '2026-09-08T18:05:02Z'
  branch: claude/squares-n11-constraints-wl9atd
  resource_rollups: [packing/campaign/resource-usage/agent-a0db35ca8af021cbd.yaml]
  goal: Decide exactly, on stated site sets at side 96/25 with the retained shrink and
    net, whether pricing the four corner squares' cores above the rest gives a covering
    surplus, using session-101's corner-pair theorem as the proved premise (each corner's
    core contains one of two known marks); report the flush-four program and the mark
    branches with their exact residuals, a certificate with its complement if one closes,
    or the scoped obstruction. Agenda 030 cell BC-292, one lane of the second wave, 2.5
    hours on one worker.
  workflow_phases:
  - workflow: research-loop
    focus: insight
    recording: contemporaneous
    clock_role: work
    objective: Build the region-class row generator (the mark rectangles as event lines),
      run the flush-four program on grid 79 with inset 1/10, decide it exactly on both
      sides (rationalised primal by the sweep, dual packing in Fractions), then the
      symmetric mark branches and a corner-refined site set, with a checkpoint every
      thirty minutes.
    commitment: BC-292
    bead: think-kx2l
    status: stopped
    entered_by: session_start
    switch_reason: null
    budget_minutes: 150
    started_at: '2026-09-08T15:35:02Z'
    deadline_at: '2026-09-08T18:05:02Z'
    expected_output: A Session-109 section in packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-a-corner-structure.md
      with the question, the falsifiers, every run with its inputs and exact verdicts,
      the branches with exact residuals, the obstruction and the appendix scripts; this
      record; one README line.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: The deadline, or an exactly decided measure with a negative residual
      (then freeze and stop, allocating nothing).
    fallback: Publish the same fields at the scope reached; the runs not started are
      recorded as the complement with the instrument gap that stopped them.
    outcome: >-
      Runs 1 and 2 report exact primal and dual bounds for the mark-union program and
      free control on site set A. Runs 3 and 3b report an exact obstruction for the
      opposite-both branch there. The union's ratio gain is 0.000535 to 0.000573;
      the branch slice residual is at least 28690/78939. Run 4 stopped during row
      generation without an exact decision, and run 5 did not run. The original
      driver and raw outputs are missing from the retained appendix, so these remain
      reported lane readings pending artifact recovery and replay.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-a-corner-structure.md
    stop_reason: An external usage limit halted run 4 before convergence; the remaining
      branch and refinement runs were not completed.
    next_action: Recover the missing driver and exact supports, replay runs 1 through
      3b on site set A, and carry run 4, run 5, the original corner-box class and the
      corrected banking-domain extension into the agenda closeout. The reported
      obstructions do not decide other site sets or clipped-domain banking cases.
  primary_bead: think-kx2l
  status: stopped
  budget:
    wall_minutes: 150
    checkpoint_minutes: 30
  stop_conditions:
  - Stop at the 2.5-hour deadline whatever the state; a promising result does not extend
    the clock.
  - Freeze a candidate only if an exactly decided measure has a negative residual;
    allocate no identifier.
  - Record every input with every result (site set, grid, inset, net, shrink, group,
    mark set, composition, thresholds, scale, rounds, machine load); a float optimum is
    context, not a claim.
  progress:
    metric: exact decisions of the corner-class program at 96/25
    before: Theorem A sound and unrun; the 3.81 census reading that the corner region's
      minimum equals the global minimum; H-127 open; the corner-pair theorem proved but
      unpriced.
    after: Reported exact bounds for the mark-union and opposite-both programs on site
      set A; run 4 partial, run 5 unrun; the ratio/slice equivalence and safe core
      clip corrected in the 2026-09-08 review. Original run artifacts remain to be
      recovered before independent replay.
  delegations: []
  outputs:
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-a-corner-structure.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/README.md
  - packing/campaign/agent-sessions/session-109-corner-class-at-q.md
  checks:
  - For completed runs 1, 2, 3 and 3b, the lane reports each rationalised measure swept
    exactly in one worker on sqpack.fractional.sweep's
    integer mass grid over all 181 directions, with the eight marks carried as zero-weight
    atoms so that the class cells are unions of whole event cells; the class threshold is
    the least class-cell mass and the free threshold the least cell mass, both reported
    as fractions with the direction that attains them; group closure of the atoms
    re-checked exactly before every sweep.
  - For those completed runs, the lane reports each dual packing re-derived in Fraction
    arithmetic from its rows' float centres
    (centre inside the closed centre domain, coverage counts per orbit, mark containment),
    the symmetrised depth checked on every orbit, and the bound read only from the exact
    objects; where the bound sits on the knife-edge (the branch slices) the dual's tight
    system was solved exactly and re-verified rather than rounded.
  - The row generator smoke-tested at grid 21 end to end (exact residual 71/250, exact
    dual 14/11) before the grid-79 runs; the free control on the same site set reproduces
    the corner-pair theorem's mark orbit as a heavy orbit and its exact dual lambda_free
    brackets the free optimum on both sides.
  - The registered corner-box region read against the run-1 packing by an exact
    sufficient test (a vertex of the concentric unit square inside the open box), which
    gives 3.48 of the 4 lambda needed, so the registered region is reported undecided
    rather than read across from the mark region.
  - packing-validate --records run from the worktree before the final commit; its outcome
    is stated in the lane's report to the coordinator, including the one check this record
    cannot satisfy on its own (no resource receipt of its own exists for a lane sub-agent;
    the coordinator attaches one at integration).
  certification_pending: think-kbci
  stop_reason: An external usage limit halted the lane during run 4. Runs 4 and 5,
    the remaining mark branches and the banking-domain extension are unfinished;
    the retained appendix lacks the original driver and raw outputs.
  next_action: Under think-kbci the coordinator integrates the lane section, attaches the
    resource receipt, runs the certifying gate, and carries H-126 and H-127 and this lane's
    unfinished complement into BC-304 (think-yrw1), the agenda closeout, which
    already has this lane's reading from the first-wave selection.
---
# session-109 — the corner-class LP under the corner-pair condition at 96/25

Research lane BC-292 of
[Agenda 030](../agendas/agenda-030-parallel-structural-lanes-at-n11.md), on
[H-126](../hypotheses/H-126-insertion-saturation-corner-structure.md) and
[H-127](../hypotheses/H-127-corner-class-surplus-at-q.md), run as one 2.5-hour block on
one worker of a shared four-core host.
The result document is the Session-109 section of
[lane A](../series/series-000-smoke-and-calibration/results/agenda-030/lane-a-corner-structure.md);
this record carries the clocks, the stop conditions and what was checked.

**Record correction, 2026-09-08.** This account now distinguishes the completed reported
runs from the interrupted and unrun work; it adds no rerun or certification.

The block began in the order the cell prescribes.
The region-class row generator was written first (the marks’ coverage rectangles as
event lines, so the corner class needs no clip), smoke-tested at grid 21, and run on
grid 79 with inset `1/10` plus the eight marks; the flush-four program under D4, the
free control on the same sites, and then the two mark branches whose stabilisers contain
a reflection — the opposite-both branch under `D2` and the U branch under one axis
reflection. The U branch stopped during round 21 without an exact decision; the
flush-four program on a corner-refined site set did not run.
Runs 1, 2, 3 and 3b report decisions on both sides: the rationalised measure by the
integer event-cell sweep, and a dual packing re-derived in `Fraction` arithmetic, with
the tight vertex solved exactly for the branch.
Their driver, supports and raw outputs were not included in the retained appendix and
must be recovered for independent replay.
Checkpoints were written at thirty-minute intervals in the scratchpad and committed as
work in progress on the lane branch.

The lane found a ratio optimum of one for the opposite-both branch on site set A. The
review corrected its extension to every site set: ratio and slice forms have the same
exclusion power, while the slice `w_f = 1` exposes a positive residual that the ratio’s
banking point can hide.
The lane also reported that a folded site set must seed every mark whatever the group,
or a branch’s LP acquires a free ray.
Theorem B’s three-plus-one clip, the pinwheel and asymmetric mark branches, and H-127’s
registered corner-box region were not reached; the section records each with the
instrument gap that would have to be closed first.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
