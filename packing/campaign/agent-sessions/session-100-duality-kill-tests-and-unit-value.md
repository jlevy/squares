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
    status: OUTCOME_STATUS
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
    outcome: OUTCOME_TEXT
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-d-contacts-and-closing-route.md
    stop_reason: STOP_REASON
    next_action: NEXT_ACTION
  primary_bead: think-7lp3
  status: stopped
  certification_pending: think-7lp3
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
    after: PROGRESS_AFTER
  delegations: []
  outputs:
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-d-contacts-and-closing-route.md
  - packing/campaign/agent-sessions/session-100-duality-kill-tests-and-unit-value.md
  checks:
  - CHECKS_LINE
  stop_reason: STOP_REASON
  next_action: NEXT_ACTION
---
# Duality Kill Tests and the B = 1 Value at 96/25

Lane BC-294 of [Agenda 030](../agendas/agenda-030-parallel-structural-lanes-at-n11.md)
under [H-129](../hypotheses/H-129-unit-shrink-fractional-value-near-u.md), run as one
2.5-hour research lane on a machine shared with five other agents.
The mathematics and every input are in the Session-100 section of
[lane D’s result document](../series/series-000-smoke-and-calibration/results/agenda-030/lane-d-contacts-and-closing-route.md);
this record is the handoff.

BODY_SUMMARY

No full gate was run in this lane; the records tier is the only check claimed, and the
record is stopped with certification pending under `think-7lp3`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
