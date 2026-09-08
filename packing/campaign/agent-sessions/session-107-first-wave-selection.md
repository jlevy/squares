---
title: session-107 — independent replays of the first wave and the selection (BC-303)
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-107
  title: Independent replays of the first wave and the selection (BC-303)
  date: '2026-09-08'
  started_at: '2026-09-08T15:34:00Z'
  deadline_at: '2026-09-08T18:04:00Z'
  branch: claude/squares-n11-constraints-wl9atd
  resource_rollups: [packing/campaign/resource-usage/agent-a045cfe6da5811e19.yaml]
  goal: Independently replay the strongest claim of each first-wave lane of Agenda 030
    with a reader written from the statement rather than the lane's script (Theorem E.4
    of lane E, the four-corner pair containment theorem of lane C, Theorem C of lane B),
    then select which lane results earn the next sustained block and state the strongest
    claim to freeze with its exact statement. Agenda 030 cell BC-303, 2.5 hours on one
    worker, one computation at a time.
  workflow_phases:
  - workflow: factual-review
    focus: correctness
    recording: contemporaneous
    clock_role: work
    objective: State each falsifier before its replay; write and self-test an interval
      reader for Theorem E.4 from the statement alone (symmetry-reduced pose space, a
      rigid-motion Lipschitz bound on the signed Euclidean distance, exact re-decision of
      every leaf and discard, exact escape decision of every failure); re-sweep the
      exported free measure with the library's verify and re-derive the ownership step;
      rebuild the grid-119 site set and decide the Theorem C class through
      decide_class_program with a driver of my own.
    commitment: BC-303
    bead: think-znzj
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 23
    started_at: '2026-09-08T15:34:00Z'
    deadline_at: '2026-09-08T15:57:00Z'
    expected_output: The replay sections of packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/bc-303-first-wave-selection.md
      with exact verdicts, inputs, box and leaf counts, and every script in its appendix.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: A falsifier of any claim (an exact escape, a failed sweep condition, a
      failed class condition), which is then the result; or the deadline.
    fallback: Report the exact scope each reader covered and what remains, without a
      verdict where none was reached.
    outcome: 'Theorem E.4 agrees at both constants: 24,381 boxes, 10,960 certified leaves,
      1,231 discards, 0 failures on the domain t in [0, 27/64], cx in [1/2, 7/2], cy in
      [1/2, 2] (justified by the segment set''s two reflections), every leaf and discard
      re-decided in Fraction, volume identity 243/128 exact, 0.2 s float and 0.5 s exact
      at load 0.95; the 9/100 set replays and the 8/100 set the lane left unresolved is
      decided (39,515 boxes, 18,004 leaves, no failure; the lane''s own reader then confirms
      it at floor 5e-5 with 366,454 leaves and a clean exact pass), while 7/100 produces 1,405,220
      floor boxes with exact escapes, so the threshold in the length is in (7/100, 8/100].
      The corner-pair theorem agrees: verify gives mass 22524199/2000000 with Conditions
      1, 3, 4, 5 holding (least cell 800003/800000, 14.9 s at load 1.65), the eight pair
      atoms at 106251/800000, per-corner pair mass above epsilon by 441/125000, and the
      cross-corner squared distance 34668544/10080625 above 2B^2. Theorem C agrees and reaches the lane''s rationalised point to the fraction (mass 11083/1024 over 296 atoms, least core 4101/4096 at direction 0 over 49 directions, 81 rounds, 333 s at load 1.3, exact decision 2.6 s).
      One defect found in lane E''s reader: its float domain [0.5, Q - 0.5] stops
      1.4e-16 short of 3.34, a measure-zero gap harmless at 3/500 and closed here.'
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/bc-303-first-wave-selection.md
    stop_reason: The three replays reached their verdicts at 15:57Z, inside the phase budget.
    next_action: Select, with the replays as evidence, in the second phase.
  - workflow: review-planning-oversight
    focus: insight
    recording: contemporaneous
    clock_role: work
    objective: Rank the candidates the cell names (the segment cover toward ownership and
      route (a), the band ladder at grids 119 and 159, the corner-pair anchors for BC-299,
      the B = 1 depth polisher, the plateau's full-dual pricing), state where the review
      disagrees with the lanes' own readings, name the strongest claim to freeze with its
      exact statement, write the session record and the README line, and run the record
      gate.
    commitment: BC-303
    bead: think-znzj
    status: stopped
    entered_by: planned_checkpoint
    switch_reason: The replays are terminal with verdicts; the cell's second question is
      the selection, which is planning work on that evidence.
    budget_minutes: 127
    started_at: '2026-09-08T15:57:00Z'
    deadline_at: '2026-09-08T18:04:00Z'
    expected_output: Sections 5 to 8 of the selection document, this record, one README
      line, a green record gate except the coordinator's re-renders.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: The deadline.
    fallback: Publish the ranking at the scope reached with the replays as its evidence.
    outcome: 'Selected: the segment-mark cover toward an ownership argument (think-qfog)
      as the next sustained block, with an accept rule of an exact-decided theorem beyond
      localisation certified by two readers; the B = 1 depth polisher (think-7lp3) as the
      efficiency block with the kill test as its accept rule and the plateau''s full-dual
      pricing as its first task. Recommended against as blocks of their own: the band
      ladder (queue filler), the corner-pair anchored certificate (its value is bounded by
      an undecided restricted fractional value), the plateau pricing (a diagnostic).
      Strongest claim to freeze: Theorem E.4 in the exact form of the document''s Section
      7, with two independent readers agreeing; the corner-pair theorem second.
      Disagreements recorded: the segment-length threshold, the far-wall sliver, lane C''s
      phase G before the anchor''s value is measured, lane B''s ladder as a block.'
    evidence:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/bc-303-first-wave-selection.md
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/README.md
    stop_reason: The block's deadline; the selection and the record were written and the
      record gate run, with the coordinator's re-renders named as the remaining failures.
    next_action: The coordinator funds the selected cell under think-qfog and the
      efficiency block under think-7lp3, allocates experiment ids for Theorem E.4 and the
      corner-pair theorem, and runs BC-304 (think-yrw1) as the closeout.
  primary_bead: think-znzj
  status: stopped
  budget:
    wall_minutes: 150
    checkpoint_minutes: 30
  stop_conditions:
  - Stop at the 2.5-hour deadline whatever the state; a promising replay does not extend
    the clock.
  - Only exact decisions count as verdicts; a float agreement is context.
  - Allocate no identifier; edit no hypothesis, agenda, registry, sqpack file or another
    lane's file; do not push.
  progress:
    metric: first-wave claims independently replayed with exact verdicts
    before: Three frozen or recommended claims (Theorem E.4, the corner-pair theorem,
      Theorem C), each decided by its own lane's reader or driver only; no selection.
    after: All three replayed with independent readers and exact verdicts (two agree
      outright; Theorem C's verdict is in the document), one companion claim decided that
      the lane could not (segments of length 8/100, then confirmed by the lane's reader
      at a finer floor), one defect in a lane reader recorded
      and closed, the candidates ranked with accept rules, the strongest claim stated
      exactly.
  delegations: []
  outputs:
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/bc-303-first-wave-selection.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/README.md
  - packing/campaign/agent-sessions/session-107-first-wave-selection.md
  checks:
  - 'full gate: fast at cbe9fd76: passed'
  - The E.4 reader's self-tests pass (analytic segment minimiser against a 2001-point
    sampling at 400 random poses, worst discrepancy 1.1e-16; exact polygon distance
    against the float signed distance at 60 random rational poses, no mismatch); every
    certified leaf and discard of every run is re-decided in Fraction; the leaves,
    discards and failures of every run sum exactly to the domain's volume; at length
    7/100 the reader's floor boxes yield exact escapes, so its falsifier side is exercised.
  - The free measure is verified by sqpack.fractional.certificate.verify with one worker
    (Conditions 1, 3, 4, 5 hold; Condition 2 fails at mass 22524199/2000000, as a
    non-certificate should); the pair weights, masses and distances are Fraction
    comparisons.
  - Theorem C is decided by decide_class_program at thresholds (1, 0) on the rationalised
    point reached from build_site_grid(96/25, 119, 1/10); the class's tangent bounds are
    read from DirectionClasses.cell_bounds and converted to degrees for comparison.
  - packing-validate --records run from the worktree before the final commit; the
    failures it reports are the coordinator's re-renders (document-map row, close report,
    ledger, synopsis handoff) and the absent resource receipt, named in the report.
  stop_reason: The block's deadline; the replays and the selection are terminal, the
    record gate was run, no claim was registered (the coordinator allocates the ids), and
    the resource receipt is the coordinator's to attach.
  next_action: Under think-kbci the coordinator integrates this record, attaches the
    resource receipt and runs the certifying gate; then funds the selected block under
    think-qfog and the efficiency block under think-7lp3, and runs BC-304 (think-yrw1) as
    the closeout.
---
# session-107 — independent replays of the first wave and the selection

Selection cell BC-303 of
[Agenda 030](../agendas/agenda-030-parallel-structural-lanes-at-n11.md), run as one
2.5-hour block on one worker of a shared four-core host, one computation at a time.
The result document is
[BC-303, first-wave selection](../series/series-000-smoke-and-calibration/results/agenda-030/bc-303-first-wave-selection.md);
this record carries the clocks, the stop conditions and what was checked.

The block ran in the order the cell prescribes: the falsifiers first, then the three
replays from the largest computation down (Theorem E.4 with a reader of my own design,
the corner pair through the library’s verifier, Theorem C through the library’s class
program), then the selection on that evidence.
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
