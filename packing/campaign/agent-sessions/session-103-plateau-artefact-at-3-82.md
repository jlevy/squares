---
title: session-103 — the exactly-eleven plateau at 191/50 as a site artefact (BC-297)
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-103
  title: The exactly-eleven plateau at 191/50 as a site artefact (BC-297, H-133)
  date: '2026-09-08'
  started_at: '2026-09-08T04:37:49Z'
  deadline_at: '2026-09-08T07:07:49Z'
  branch: claude/squares-n11-constraints-wl9atd
  resource_rollups: [packing/campaign/resource-usage/agent-ade07b22e00a3de2a.yaml]
  goal: Decide exactly whether the restricted covering value of exactly eleven that two
    site sets reached at side 191/50 is an artefact of Trump-shaped B-cores overlapping only
    in site-free strips (H-133); if so, add sites in the strips and re-run column generation
    for a certificate below eleven; otherwise read the tight-cell census and the exact-cover
    verdict. Agenda 030 cell BC-297, one lane of the first wave, 2.5 hours on one worker.
  workflow_phases:
  - workflow: research-loop
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: The thirty-minute artefact test (reconstruct the site sets, scale Trump's
      packing to 191/50, clamp its eleven B-cores into the admissible domain, decide exactly
      whether every pairwise overlap is site-free and report the strip geometry), then the
      branch the verdict selects, with a checkpoint every thirty minutes.
    commitment: BC-297
    bead: think-4uon
    status: stopped
    entered_by: session_start
    switch_reason: null
    budget_minutes: 150
    started_at: '2026-09-08T04:37:49Z'
    deadline_at: '2026-09-08T07:07:49Z'
    expected_output: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-f-plateau-at-3-82.md
      with the exact artefact verdict, the strip geometry, every run with its inputs and
      exact verdict, and the census if reached; this record; one README line.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: The deadline, or a frozen candidate below eleven (then freeze and stop,
      allocating nothing).
    fallback: Publish the same fields at the scope reached; a census above one million
      cells with no clustering is recorded as the obstruction.
    outcome: Not site-free. The grid seed at BC-191's density (counts 25, 34, 41; 3365
      sites, BC-200's recorded seed) puts 45 sites in two or more of Trump's clamped cores,
      BC-200's retained 12761-site state 822, and the grid plus T-018's atoms scaled by
      382/381 162; the fourteen overlap strips are 0.0124 to 0.0254 wide because the clamp
      moves wall cores inward by 0.0062 to 0.0088; a perturbation search bottoms out at 5
      doubly covered sites. The plateau is a site artefact in the general sense only; the
      instrument's duals are near-axis fractional families with exact pointwise depth 1.99
      (run 0) and 1.67 (exp-060), with about one per cent of their weight near Trump's
      angle. Run 1 (grid plus 484 strip sites, column generation, 2400 s deadline) stopped by
      the generator's own criterion after 66 column rounds at 11.072443 (rationalised
      553677/50000 over 384 atoms, exactly swept as a valid measure of mass above eleven);
      see the lane document for its table. The census of the one
      exactly decided measure (mass 2223761/200000, valid, 213 atoms) is 0 cells exactly
      tight, 442292 within 1/1000 of one in 6000 components and 1934092 within the gap
      13/110 in 18440 components over 21997353 reachable cells, spread over the whole centre
      domain and not on Trump's cores; recorded as the obstruction to the exact cover. No
      claim frozen; H-133 recommended refuted as stated with the general mechanism
      confirmed.
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-f-plateau-at-3-82.md
    stop_reason: The block's deadline; every priority through the census was reached and
      the shrink tax was not started.
    next_action: BC-303 (think-znzj) reads this lane; if the plateau is pursued again, continue BC-200's
      cutting-plane loop from its retained state rather than seeding strips at Trump's
      contacts, and retain the state of any run that stops at exactly eleven.
  primary_bead: think-4uon
  status: stopped
  budget:
    wall_minutes: 150
    checkpoint_minutes: 30
  stop_conditions:
  - Stop at the 2.5-hour deadline whatever the state; a promising result does not extend
    the clock.
  - Freeze a candidate only if the exact restricted value falls below eleven and the exact
    sweep accepts it; allocate no identifier.
  - Record every input with every result (site set, added sites as rationals, net, shrink,
    warm start, rounds, deadline, machine load); a float value is context, not a claim.
  progress:
    metric: exact verdicts on the plateau's mechanism at 191/50
    before: Two runs at exactly 11.000000 with no retained log, state or measure; H-133 open
      with the Trump-strip mechanism conjectured and the site set's pitch quoted as 0.047.
    after: The Trump-strip mechanism decided exactly and refuted on every reconstructible
      site set; the seed's coordinate gaps measured (0.0021 to 0.0705); the general
      site-invisible-overlap mechanism decided exactly (dual depth 1.985950 on grid plus
      strips); one run with the strips filled recorded with its table; one census of the
      near-tight cells with its locality against Trump's cores; the exact-cover route
      recorded as an obstruction at this measure.
  delegations: []
  outputs:
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-f-plateau-at-3-82.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/README.md
  - packing/campaign/agent-sessions/session-103-plateau-artefact-at-3-82.md
  checks:
  - 'full gate: fast at cbe9fd76: passed'
  - Artefact test decided in exact rational arithmetic with the repository's Square.covers
    and square_at on the reconstructed grid seed, BC-200's retained state and the
    grid-plus-T-018 seed; the grid seed's count 3365 matches BC-200's recorded initial_sites.
  - Run 0's candidate swept exactly with one worker (least cell mass 200009/200000 at
    direction 0, Condition 5 holds, Condition 2 fails at mass 2223761/200000); the census
    reads the same integer mass grid and reports matches_declared_least_cell_mass true.
  - Run 1 driven by devtools.run_fractional_colgen with its round table, row log and JSON
    summary retained in the scratchpad and reproduced in the lane document; no candidate
    below eleven, so decide_certificate was not invoked on a claim.
  - packing-validate --records run from the worktree before the final commit; its outcome is
    stated in the lane's report to the coordinator, including the one check this record
    cannot satisfy on its own (no resource receipt of its own exists for a lane sub-agent;
    the coordinator attaches one at integration).
  stop_reason: The 2.5-hour block ended with the lane's priorities through the census
    complete; no full gate was run in the lane, no claim was frozen, and the resource
    receipt is the coordinator's to attach at integration.
  next_action: Under think-4uon the coordinator integrates the lane document, attaches the
    resource receipt, runs the certifying gate and dispositions H-133 in BC-303 (think-znzj).
---
# session-103 — the exactly-eleven plateau at 191/50 as a site artefact

Research lane BC-297 of
[Agenda 030](../agendas/agenda-030-parallel-structural-lanes-at-n11.md), on
[H-133](../hypotheses/H-133-plateau-site-artefact.md), run as one 2.5-hour block on one
worker of a shared four-core host.
The result document is
[lane F](../series/series-000-smoke-and-calibration/results/agenda-030/lane-f-plateau-at-3-82.md);
this record carries the clocks, the stop conditions and what was checked.

The block ran in the order the cell prescribes: the artefact test first, exact and
within its thirty minutes; then, because the overlaps were not site-free, one
column-generation run with the strips filled anyway (to record what the instrument does
on that site set) and the tight-cell census on the block’s one exactly decided measure.
The shrink tax was not started.
Checkpoints were written at thirty-minute intervals in the scratchpad and committed as
work in progress on the lane branch.

## Integration Certification Addendum — 2026-09-08

The corrected integration checkpoint combines the 62-step fast pass at `cbe9fd76`, the
passing structured negative-control, slow and exhaustive component receipts at that same
revision, and four unchanged full-only geometry passes recorded in the retained raw
stdout from the failed `ef8a2e72` invocation.
The reviewed `ef8a2e72..cbe9fd76` source diff leaves those four components unaffected.
Together that log and the structured receipts cover all 69 declared validation steps.
The `ef8a2e72` full invocation remains failed; the later component runs are not called a
full invocation.

This later integration result discharges only the record’s certification debt.
It does not extend this stopped session’s clock, rerun its science, change a scientific
verdict, supply a missing artifact, or complete any target recorded as partial, stopped,
unrun or absent.
The original stop reason, resource accounting and unfinished complements
remain historical facts.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
