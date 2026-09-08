---
title: session-108 — what the segment cover and the corner pair localise at 96/25 (BC-299)
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-108
  title: What the segment cover and the corner pair localise at 96/25 (BC-299, H-126, H-111)
  date: '2026-09-08'
  started_at: '2026-09-08T15:34:22Z'
  deadline_at: '2026-09-08T18:04:22Z'
  branch: claude/squares-n11-constraints-wl9atd
  resource_rollups: [packing/campaign/resource-usage/agent-aabf7fb69affb7684.yaml]
  goal: State exactly the localisation that Theorem E.4 (ten segments) and the four-corner
    pair theorem give for eleven unit squares at 96/25, prove what can be proved, read the
    trade-off between an anchor class and its price on the retained shrink and net, and
    answer the cell's band question with a theorem or the escaping square. Agenda 030 cell
    BC-299, one lane of the first wave, 2.5 hours on one worker.
  workflow_phases:
  - workflow: research-loop
    focus: insight
    recording: contemporaneous
    clock_role: work
    objective: The localisation theorems by hand (the grazing localisation of the escape
      class, the corner square's four candidate segments and its non-pinning witness, the
      shared-segment split, the weak-duality pricing lemma and its ownership corollary);
      then one free covering LP at 96/25 with its dual saved, the dual verified exactly as a
      fractional packing and its charge read on every anchor class; then the band search
      with an exact witness; a checkpoint every thirty minutes.
    commitment: BC-299
    bead: think-4ifm
    status: stopped
    entered_by: session_start
    switch_reason: null
    budget_minutes: 150
    started_at: '2026-09-08T15:34:22Z'
    deadline_at: '2026-09-08T18:04:22Z'
    expected_output: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-g-anchors-at-q.md
      with the theorems and proofs, every run with its inputs and exact verdict, the
      trade-off table, the obstructions and every script; this record; one README line.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: The deadline, or a two-branch certificate below its threshold decided by
      the exact sweep (then freeze and stop, allocating nothing).
    fallback: Publish the same fields at the scope reached.
    outcome: >-
      Theorem G.1 (proved from E.4 and the net's Hausdorff bound 0.00325) says every
      core avoiding Stromquist's ten points at 96/25 lies within 1/100 of a segment centred
      on a point it does not contain, so the escape class is K4 times the union of four thin
      grazing classes and Lemma B's branch 1 is free; Proposition G.2 (exact 45-degree
      square at centre (38/25, 3/4)) shows the corner square is not pinned to the corner
      segment and can be near any of four; Proposition G.3 records that eleven squares and
      ten segments give only a shared segment, not ownership. Lemma G.4 (weak duality on a
      site set) and Corollary G.4.2 prove that an anchor established by the ownership lemma
      is unpriceable on its own site set at every threshold. Run 1 (the free LP on
      session-101's 619-orbit, 4645-site set, 65 s at load 0.35 to 1.5) converged at
      11.386020, its measure exactly swept as valid at mass 45544287/4000000; its dual,
      rationalised down and symmetrised, is an exactly verified fractional packing of value
      45544013/4000000 (depth at most 15999983/16000000 at every site) charging the corner
      pair 1.002367 (dead), the P10-avoiders 3.608, and the grazing classes 0.841, 0.822,
      0.000 and 0.142 (corner, wall-middle, row-outer, row-inner), so on this site set only
      the row types can carry a branch-2 measure, with necessary thresholds 1.39 and 1.45
      (1.51 for a K4-symmetric measure on the row-inner type).
      Theorem G.6: an exact contained unit square at tilt 13.0477 degrees (tan(psi/2) =
      137/1198, centre (53/35, 1398/985)) avoids all ten points with its centre outside both
      wall rectangles, so the wall-rectangle localisation holds for no band reaching 13.05
      degrees; the float search reads the first avoider anywhere at 11.65 degrees (exact
      witness at 11.67 in the bottom wall rectangle). No certificate, no bound, no claim
      frozen; H-126 recommended open with the corner-anchor obstruction recorded, H-111 open
      with its anchor domain now concrete.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-g-anchors-at-q.md
    stop_reason: The lane's three priorities were reached at their honest scope inside the
      block; the threshold program for the row types and the event-cell filter were not
      started.
    next_action: BC-303 (think-znzj) reads this lane; the first run afterwards is the
      D4-symmetric threshold program for the row-inner grazing class on the run-1 site set
      at w in {3/2, 2, 5/2}, decided by the exact sweep.
  primary_bead: think-4ifm
  status: stopped
  budget:
    wall_minutes: 150
    checkpoint_minutes: 30
  stop_conditions:
  - Stop at the 2.5-hour deadline whatever the state; a promising result does not extend
    the clock.
  - Freeze a candidate only if a two-branch measure falls below its threshold and the exact
    sweep accepts it; allocate no identifier.
  - Record every input with every result (site set, net, shrink, rows, rationalisation,
    machine load); a float optimum is context, never a claim; a found pose is a theorem
    only after its rational rounding is decided exactly.
  progress:
    metric: exact statements about what the two proved premises localise at 96/25, and
      exact readings of the anchor's price on the retained instrument
    before: E.4 and the corner-pair theorem proved separately; the cell's band question
      open with lane C's 27.5-degree interior escape; no pricing of any anchor at 96/25.
    after: The grazing localisation theorem with Lemma B's branch 1 free; the corner
      square's non-pinning witness and four-segment localisation; the pricing lemma with the
      ownership corollary; one exactly verified fractional packing on session-101's site
      set with the charge of every anchor class tabulated; the exact 13.05-degree escape
      and the 11.67-degree wall-rectangle avoider.
  delegations: []
  outputs:
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-g-anchors-at-q.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/README.md
  - packing/campaign/agent-sessions/session-108-anchors-at-q.md
  checks:
  - Run 1's rationalised measure swept exactly with one worker (Conditions 1, 3, 4, 5 hold,
    least cell 400001/400000 at direction 0, Condition 2 fails at mass 45544287/4000000).
  - The dual rationalised down and symmetrised, its depth at every one of the 4645 sites
    bounded above by an exact rational sum over float-flagged memberships with a
    conservative band, maximum 15999983/16000000; the script refuses to continue if any
    site exceeds one.
  - Every charge an exact rational sum; segment-distance tests carry the sampling error on
    the conservative side; the corner-pair and avoidance predicates decided in Fraction
    arithmetic with the repository's Square.covers.
  - Both band witnesses decided exactly in Fraction arithmetic (containment, rectangle
    membership, ten strict frame margins); the search's readings labelled as readings.
  - packing-validate --records run from the worktree before the final commit; its outcome
    is stated in the lane's report to the coordinator, including the one check this record
    cannot satisfy on its own (no resource receipt of its own exists for a lane sub-agent;
    the coordinator attaches one at integration).
  certification_pending: think-kbci
  stop_reason: The 2.5-hour block ended with the lane's priorities reached at their honest
    scope; no full gate was run in the lane, no claim was frozen, and the resource receipt
    is the coordinator's to attach at integration.
  next_action: Under think-kbci the coordinator integrates the lane document, attaches the
    resource receipt, runs the certifying gate, and carries H-126 and H-111 and this lane's
    unfinished complement into BC-304 (think-yrw1), the agenda closeout, which
    already has this lane's reading from the first-wave selection.
---
# session-108 — what the segment cover and the corner pair localise at 96/25

Research lane BC-299 of
[Agenda 030](../agendas/agenda-030-parallel-structural-lanes-at-n11.md), on
[H-126](../hypotheses/H-126-insertion-saturation-corner-structure.md) and
[H-111](../hypotheses/H-111-resource-anchor-case-exclusion.md), run as one 2.5-hour
block on one worker of a shared four-core host.
The result document is
[lane G](../series/series-000-smoke-and-calibration/results/agenda-030/lane-g-anchors-at-q.md);
this record carries the clocks, the stop conditions and what was checked.

The block ran in the order the dispatch prescribed: the localisation theorems first, by
hand, from the two proved premises; then one free covering LP at `96/25` on the site set
that proved the corner-pair theorem, its dual turned into an exactly verified fractional
packing and its charge read on every anchor class the cell named; then the band question
answered by an exact escaping square.
The threshold program for the surviving classes and the event-cell filter were not
started. Checkpoints were written at thirty-minute intervals in the scratchpad and
committed as work in progress on the lane branch.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
