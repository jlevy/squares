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
      1.248677, depth-scaled 8.918484); that family, 89090463224/9989418081 = 8.918484, is
      verified from its bytes by replay_ceiling_family --check and by verify_ceiling
      re-declared at 9977/10000 on the 203-direction net; 5.927446 of it lies outside
      Trump's neighbourhood and only 0.026704 within 1 degree of 40.18 degrees; the
      polisher's one round did not improve it (LP 11.00 on the near-tight set, exact
      depth 4/3).
      Four corner boxes at the retained (B, net): loop floor 6.173135, polished
      6.260870, site LP 7.14 with unconverged rows. Central box, single corner box
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
      Corrected 2026-09-08: the named scratch state is absent, and the embedded unit_loop
      cannot safely resume its own merged-net indices. Start from retained
      packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-family.json;
      transport all geometry by 10000/9977 with devtools.transport_ceiling_family and
      verify the unit control before building the guarded polisher. Preserve exact source
      and destination nets on every resume. No target search is part of this correction.
  primary_bead: think-7lp3
  status: stopped
  certification_pending: think-7lp3
  resource_rollups: [packing/campaign/resource-usage/agent-a2247da4712316276.yaml]
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
      a B = 1 family of value 8.918484 (2877776 vertices, verified twice) and a
      four-corner-box restricted family of value 6.260870 at the retained (B, net);
      the Trump split and the single-region sub-restrictions of both; every region
      classified undecided with the reason.
  delegations: []
  outputs:
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-d-contacts-and-closing-route.md
  - packing/campaign/agent-sessions/session-100-duality-kill-tests-and-unit-value.md
  checks:
  - 'uv run --frozen --all-extras --group dev packing-validate --records at 06:05Z: green on every step this lane owns (schema, session clocks, gate grammar, resource rollups with 53 terminal sessions all present, ledger re-rendered); two steps fail, synopsis agrees with the artifacts and every session cost is attributed, because a new terminal session must be named by SYNOPSIS.md Current Handoff and by the session-close report, both coordinator-owned files this lane may not edit; devtools.close_session --render at integration clears both.'
  - verify_ceiling on every frozen family from its bytes (the polisher's own pass and the loop's), and the restricted driver's exact disjointness assertion on every family it judged.
  stop_reason: >-
    Lane clock exhausted at the block deadline; results published at the scope reached.
    Stopped with certification pending under think-7lp3: no full gate was run in the
    lane, and the resource receipt is the lane's own transcript rolled up before the
    block closed, a contemporaneous lower bound the coordinator regenerates at closeout.
  next_action: >-
    Coordinator: keep H-129 open and use the dated correction's retained exp-070 family,
    exact unit transport, and net-bound resume contract. The original scratch state has
    not been recovered. The certification debt under think-7lp3 clears only with the next
    qualifying gate on the integrated branch; source replay and instrument controls come
    before a separately registered target continuation.
---
# Duality Kill Tests and the B = 1 Value at 96/25

Lane BC-294 of [Agenda 030](../agendas/agenda-030-parallel-structural-lanes-at-n11.md)
under [H-129](../hypotheses/H-129-unit-shrink-fractional-value-near-u.md), run as one
2.5-hour research lane on a machine shared with five other agents.
The mathematics and every input are in the Session-100 section of
[lane D’s result document](../series/series-000-smoke-and-calibration/results/agenda-030/lane-d-contacts-and-closing-route.md);
this record is the handoff.

What the block established, all at `q = 96/25`: a verified `B = 1` family of value
`89090463224/9989418081 = 8.918484` (the loop’s iteration-0 support; one polisher round
did not improve it), of which `5.927446` lies outside Trump’s neighbourhood; a verified
family off the four corner boxes of value `6.260870` at the retained `(B, net)`; the
proved floor `ν*₁(q) ≥ 10` from `s(10)`; and the reading that no region is a kill and
none is alive at the cell’s standard, so routes (b) and (c) and every capture design
survive untested and BC-204 has no threshold to aim at yet.
H-129 is recommended `open`. No claim is frozen and no experiment id is needed.

No full gate was run in this lane; the records tier is the only check claimed, and the
record is stopped with certification pending under `think-7lp3`.

## Correction of 2026-09-08: Recoverable Evidence and Safe Resume

The original clocks, measurements and scripts are preserved.
The claimed scratch family and state are absent from this checkout, so their
eight-point-nine replay cannot be repeated from this PR. The embedded `unit_loop.py`
also remaps every loaded row from 181 to 203 directions even when its input is already
its own 203-direction state; using it to resume that state changes angles or raises an
index error.

The operational control is exp-070’s retained `bc-232-leg-01-family.json`, whose exact
weight is `21342289572/2055263195`. Scaling its complete geometry by `10000/9977` gives
unit squares in side `38200/9977 < 96/25`, with the same depth and weight.
The
[lane-D correction](../series/series-000-smoke-and-calibration/results/agenda-030/lane-d-contacts-and-closing-route.md#correction-of-2026-09-08-duality-scope-cap-and-retained-continuation)
owns the proof, command and remaining dependencies.
This stronger baseline supersedes the proposed restart from the unavailable state; it
does not settle H-129.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
