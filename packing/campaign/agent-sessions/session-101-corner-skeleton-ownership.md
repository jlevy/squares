---
title: session-101 — corner-skeleton ownership at 96/25
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-101
  title: Corner-skeleton ownership at 96/25
  date: '2026-09-08'
  started_at: '2026-09-08T04:28:00Z'
  deadline_at: '2026-09-08T06:58:00Z'
  branch: claude/squares-n11-constraints-wl9atd
  goal: >-
    Decide Agenda 030's cell BC-293 (H-128): whether a valid D4-symmetric measure at side
    96/25 exists with T-018's four corner atoms, scaled by 384/381, at weight at least 3/20
    and total mass below 11 + 3/20, so that X-021's Corollary C.2 turns it into the theorem
    that every packing of eleven unit squares at 96/25 has four distinct squares containing
    the four corner atoms; record the price M(forced) - M(free) either way.
  workflow_phases:
  - workflow: research-loop
    focus: insight
    recording: contemporaneous
    clock_role: work
    commitment: BC-293
    bead: think-1136
    objective: >-
      Re-derive the ownership step exactly, build a lane-owned bounded column-generation
      driver on sqpack.fractional (an LP bound change, no geometry change), run it at 96/25
      seeded with T-018 scaled by 384/381 on the density-matched grids, decide every final
      measure with the exact eighth-turn sweep, and read the price on one site set.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 110
    started_at: '2026-09-08T04:28:00Z'
    deadline_at: '2026-09-08T06:18:00Z'
    expected_output: >-
      The session-101 section of results/agenda-030/lane-c-n10-transfer.md with every run's
      inputs, exact verdicts, the price, and the scripts in its appendix.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: >-
      The bounded LP does not converge inside its wall on the density-matched site set, or
      the exact sweep refuses every final measure on Condition 1, 3, 4 or 5.
    fallback: >-
      Publish the best unconverged mass with its site set and rows as the scoped
      obstruction, and leave the theorem conditional.
    outcome: >-
      Decided against the hypothesis on the retained shrink and net. On the density-matched
      site set (637 orbits after column generation) the least four-bound measure has exact
      rationalised mass 23596423/2000000 = 11.7982 (valid by the sweep on Conditions 1, 3, 4,
      5; corner weights 600001/4000000), the five-bound 47276821/4000000 = 11.8192, the free
      22524199/2000000 = 11.2621 on the same site set and rows, price 33507/62500 = 0.536112;
      the priced program M - w_c leaves the corner orbit at zero at any price, so the position
      and not the bound is what fails. FLOORTOKEN From the free measure, Lemma C' for sets
      proves the four-corner pair containment theorem at 96/25: four distinct squares each
      containing one of its corner's two marks (3152/3175, 2336/3175), (2336/3175, 3152/3175),
      pair mass 106251/400000 above epsilon = 524199/2000000 by 441/125000. RUN5TOKEN
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-c-n10-transfer.md
    stop_reason: >-
      The cell's question is decided and its falsifier met; the remaining computation
      (a settled dual for the floor) does not fit the block and is handed on.
    next_action: >-
      Write the record, validate the records tier, commit on lane/bc-293-corner-skeleton.
  - workflow: documentation-pass
    focus: process
    recording: contemporaneous
    clock_role: finalization
    commitment: BC-293
    bead: think-1136
    objective: >-
      Write the result section and this record, run the records tier, commit; no research
      in this phase.
    status: stopped
    entered_by: planned_checkpoint
    switch_reason: The runs are terminal; what remains is the record and its validation.
    budget_minutes: 40
    started_at: '2026-09-08T06:18:00Z'
    deadline_at: '2026-09-08T06:58:00Z'
    expected_output: This record, the result section, one commit on the lane branch.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: The lane clock ends before the records tier is green.
    fallback: Commit what is written and name the failing check in the report.
    outcome: >-
      Result section appended to lane C's report with the derivation, every run's inputs and
      exact verdicts, the price, the pair theorem, the floor, the obstructions and the scripts;
      the three load-bearing measures exported beside it; this record written; the records
      tier run with the three integration-time failures named. DRYRUNTOKEN
    evidence:
    - packing/campaign/agent-sessions/session-101-corner-skeleton-ownership.md
    stop_reason: The lane clock; nothing further is planned in this session.
    next_action: >-
      The coordinator disposes H-128 on the recorded verdict and decides whether the
      frozen obstruction needs an experiment id.
  primary_bead: think-1136
  status: stopped
  certification_pending: think-1136
  budget:
    wall_minutes: 150
    checkpoint_minutes: 30
    finalization_minutes: 40
  stop_conditions:
  - The 2.5 hour lane clock from 04:28Z; no extension.
  - A converged bounded run decided by the exact sweep, or the obstruction with the converged mass.
  - No identifier allocation, no registry, hypothesis, agenda or sqpack edit, no push.
  progress:
    metric: >-
      exactly verified mass of the least column-generation measure at 96/25 with the four
      corner atoms at weight at least 3/20, against the 11.15 criterion
    before: >-
      Unmeasured; H-128 registered on 2026-09-08 with the 3.85 free run at 11.23 unconverged
      as the only neighbour.
    after: >-
      11.7982115 exactly (23596423/2000000), valid, above the 11.15 criterion; the free value on
      the same site set 11.2620995 and, after nine more column rounds, 11.18961275; every reading
      an upper reading on a finite site set. FLOORSHORT
  delegations: []
  outputs:
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-c-n10-transfer.md
  - packing/campaign/agent-sessions/session-101-corner-skeleton-ownership.md
  checks:
  - Every final measure of runs 1, 2, 4, 5 and 6 decided by certificate.verify(workers=1); Conditions 1, 3, 4, 5 hold for each, Condition 2 fails as the mass says.
  - The corner-orbit premise d^2 = 4633032392704/1385114794281 > 2B^2 = 99540529/50000000 and the pair premises decided in Fraction arithmetic before any run.
  - Run 4 replayed run 2's LP objectives to the last printed digit.
  - uv run --frozen --all-extras --group dev packing-validate --records on the lane commit; expected failures named in the result section (close report and SYNOPSIS drift, and the rollup, all rendered by the coordinator at integration); no full gate run, certification pending under think-1136.
  stop_reason: >-
    The lane's bounded question is decided and recorded; the session stops at its clock
    without a full gate run, so certification is pending under think-1136, and no resource
    rollup exists for this lane's log yet.
  next_action: >-
    Under think-1136 the coordinator runs the certifying gate on the lane commit, attaches
    the resource rollup, and disposes H-128 on the recorded verdict.
---
# session-101 — corner-skeleton ownership at 96/25

The lane's result, with every input, every exact verdict and the scripts, is the
`Session-101` section of
[lane C's report](../series/series-000-smoke-and-calibration/results/agenda-030/lane-c-n10-transfer.md).
This record is the handoff: what was attempted, what came back, and what should happen
next.

In one sentence: the bounded measure H-128 asked for does not exist on the retained shrink
and net at the precision this block could buy (the least valid four-bound measure has mass
`23596423/2000000 ≈ 11.798`, against the `11.15` criterion, and pricing the corner orbit
shows the position rather than the bound is the obstacle), but the free measure at `96/25`
proves a weaker four-corner theorem outright: four distinct squares each containing one of
two marks near its corner. The price `M(forced) − M(free)` is `33507/62500 = 0.536112` on
one site set. The floor for the net is the unfinished part.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
