---
title: session-100 — duality kill tests and the B = 1 value at 96/25
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-100
  title: Duality kill tests and the B = 1 value at 96/25
  date: '2026-09-08'
  started_at: '2026-09-08T04:27:52Z'
  deadline_at: '2026-09-08T06:57:52Z'
  branch: claude/squares-n11-constraints-wl9atd
  goal: >-
    BC-294 of Agenda 030 under H-129: measure the shrink-free (B = 1) depth-one fractional
    packing value at side 96/25 with a direction net dense near 0 and 40.18 degrees, split
    its weight against Trump's placements, and the restricted fractional values at 96/25
    off the four corner boxes and the central box, each as an exactly verified family
    (verify_ceiling) with every input recorded; classify each region as kill, alive or
    undecided by X-021's Lemma D.
  workflow_phases:
  - workflow: research-loop
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: >-
      One 2.5-hour lane on one shared core: the B = 1 cutting-plane loop at 96/25 warm from
      BC-200's state, a depth polisher on its support, exact verification, the Trump
      split, then the four-corner-box and central-box restricted loops at the retained
      shrink, then the result section, this record and the records tier.
    bead: think-7lp3
    status: stopped
    entered_by: session_start
    switch_reason: null
    budget_minutes: 150
    started_at: '2026-09-08T04:27:52Z'
    deadline_at: '2026-09-08T06:57:52Z'
    expected_output: >-
      A Session-100 section in results/agenda-030/lane-d-contacts-and-closing-route.md with
      the exact verified values, the inputs, the classification table and the scripts; the
      frozen families and states under the lane scratchpad; a recommended status for H-129.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      verify_ceiling refuses a produced family (K2 depth above 1), or the loop cannot
      complete one iteration inside its thirty-minute budget on the shared machine.
    fallback: >-
      Publish every started region with its classification or the word undecided, the
      reason and the inputs; leave 3.86 and 3.87 to the next session.
    outcome: >-
      B = 1 at 96/25: the loop completed one iteration before its process was killed
      (site LP 11.1698 with unconverged rows, raw dual 11.1363, exact maximum depth
      1.248677, depth-scaled 8.918484); the depth polisher on that support gives a
      verified family of value UNIT_VALUE (unit regime, re-declared at 9977/10000 on
      the 203-direction net), with OUTSIDE_WEIGHT of it outside Trump's neighbourhood.
      Four corner boxes at the retained (B, net): loop floor 6.173135, polished
      CORNERS_VALUE, site LP 7.14 with unconverged rows. Central box, single corner box
      and corner triangle: lower bounds read off the verified families only. No region
      is a kill and none is alive at the cell's standard; every region is undecided
      with its inputs recorded. 3.86 and 3.87 were not started.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-d-contacts-and-closing-route.md
    stop_reason: >-
      Block deadline 06:57:52Z; the machine ran at load 5 to 8 throughout, so the
      B = 1 loop bought one iteration and the restricted loop three, and the central-box
      loop was cancelled to protect the polishers and the write-up.
    next_action: >-
      Run the B = 1 loop at 96/25 to convergence on an unloaded core from the saved state
      (scratchpad/lane-294/unit-3-84/unit-state-96-25.json), polish every iteration's
      support, then 3.86 and 3.87; make the polisher an instrument step of the loop.
  primary_bead: think-7lp3
  status: in_progress
  budget:
    wall_minutes: 150
    checkpoint_minutes: 30
  stop_conditions:
  - Stop at 06:57:52Z whatever the state of the runs; a promising result does not extend the clock.
  - Only verify_ceiling on a frozen family, or an exactly decided LP, turns a number into a claim; a float optimum is context.
  - No identifiers allocated, no hypothesis, agenda, registry or other lane's file edited, nothing pushed.
  progress:
    metric: exactly verified depth-one families at 96/25 with their restricted and Trump-split readings
    before: >-
      No B = 1 reading at any side; the only restricted readings were lower bounds read off
      the BC-200 family at 191/50 moved to 96/25 (8.87 off a unit corner box, 7.10 off the
      central box), the site LP at 191/50 sitting at 11.0556 against a depth-scaled 9.9079.
    after: >-
      Two verified families at 96/25 with their bytes retained under the lane scratchpad:
      a B = 1 family of value UNIT_VALUE (2877776 vertices, unit regime) and a
      four-corner-box restricted family of value CORNERS_VALUE at the retained (B, net);
      the Trump split and the single-region sub-restrictions of both; every region
      classified undecided with the reason.
  delegations: []
  outputs:
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-d-contacts-and-closing-route.md
  - packing/campaign/agent-sessions/session-100-duality-kill-tests-and-unit-value.md
  checks:
  - 'uv run --frozen --all-extras --group dev packing-validate --records: RECORDS_RESULT'
  - verify_ceiling on every frozen family from its bytes (the polisher's own pass and the loop's), and the restricted driver's exact disjointness assertion on every family it judged.
  stop_reason: >-
    Lane clock exhausted at the block deadline; results published at the scope reached.
    The record stays in_progress because a terminal record needs a resource rollup that
    only the coordinator can produce honestly from the session log; the coordinator
    terminalises it as stopped with certification_pending think-7lp3.
  next_action: >-
    Coordinator: attach the rollup, set status stopped and certification_pending
    think-7lp3, apply the recommended H-129 status (open), and hand the saved B = 1 state
    to a convergence run on an unloaded core before 3.86 and 3.87.
---
# Duality Kill Tests and the B = 1 Value at 96/25

Lane BC-294 of [Agenda 030](../agendas/agenda-030-parallel-structural-lanes-at-n11.md)
under [H-129](../hypotheses/H-129-unit-shrink-fractional-value-near-u.md), run as one
2.5-hour research lane on a machine shared with five other agents.
The mathematics and every input are in the Session-100 section of
[lane D’s result document](../series/series-000-smoke-and-calibration/results/agenda-030/lane-d-contacts-and-closing-route.md);
this record is the handoff.

What the block established, all at `q = 96/25`: a verified `B = 1` family of value
`UNIT_VALUE` (the loop's own depth-scaled value was `8.918484`; the polisher recovered the
rest from the same support), of which `OUTSIDE_WEIGHT` lies outside Trump's neighbourhood;
a verified family off the four corner boxes of value `CORNERS_VALUE` at the retained
`(B, net)`; the proved floor `ν*₁(q) ≥ 10` from `s(10)`; and the reading that no region is
a kill and none is alive at the cell's standard, so routes (b) and (c) and every capture
design survive untested and BC-204 has no threshold to aim at yet.
H-129 is recommended `open`. No claim is frozen and no experiment id is needed.

No full gate was run in this lane; the records tier is the only check claimed, and the
record is stopped with certification pending under `think-7lp3`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
