---
title: "session-051 — block 2 of the overnight run: the enumeration reprice and the exact-LP gate"
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-051
  primary_bead: think-kp7o
  status: completed
  title: "Block 2 of the overnight run: the enumeration reprice and the exact-LP gate"
  date: '2026-08-31'
  started_at: '2026-08-31T06:09:00Z'
  deadline_at: '2026-08-31T08:09:00Z'
  goal: >-
    Agenda-010 block 2, 120 minutes: BC-095 (price X-003 stage-1 at the chunk level in
    counted LP solves, with the measured orbit quotient and the realizability
    prefilter actually applied and an omission-control design stated -- the number
    D-405 says the queue never had) then BC-096 (measure the exact LP at the full
    n = 11 cell against T-2's 1.28 ms float baseline). Block 1 closed early, so this
    block starts two hours inside the run's schedule; the same unattended rules hold,
    and the D-405 lesson cuts both ways -- every factor in the price is either counted
    exactly or measured on a named sample, never estimated silently.
  workflow_phases:
  - workflow: efficiency-loop
    recording: contemporaneous
    clock_role: work
    focus: efficiency
    commitment: BC-095
    bead: think-kp7o
    objective: >-
      Build the pricing tool (OR-1): exact counts for the chunk-level stage-1 label
      space X-003 defines at n = 11 with k <= 5 assemblies (partitions, skeleton
      choices, angle-class assignments, inter-assembly contact hypotheses), the
      symmetry quotient computed at the chunk level rather than borrowed from the
      size-five scaffold measurement, the realizability prefilter's acceptance rate
      and per-candidate cost measured on a named sample of the retained size-five
      scaffold atlas, and the total in counted LP solves (D-126) at T-2's measured
      per-solve cost.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 75
    started_at: '2026-08-31T06:09:00Z'
    deadline_at: '2026-08-31T07:24:00Z'
    expected_output: >-
      devtools/price_stage1_enumeration.py printing the priced ladder with every
      factor labeled counted or measured, plus the go/no-go statement written into
      agenda-010's BC-095 evidence and the bead.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --push
    kill_condition: >-
      Any factor in the price that cannot be counted or measured inside the budget is
      named as unpriced rather than estimated -- a price with a silent guess in it is
      D-405 again, and the phase stops before shipping one.
    fallback: >-
      Ship the tool with the factors it could price and a typed unpriced-factor list;
      the go/no-go then says what remains unknown instead of a number.
    outcome: >-
      devtools/price_stage1_chunks.py prices the space with every factor's standing
      labeled. Counted: 44 partition families at K <= 6; raw labels 4.357e20 with a
      Burnside orbit floor of 2.763e18 (D4 times interchangeable-chunk permutations),
      and a restricted-slice grid down to K <= 3 under X-008's measured wall seatings
      at 24,611,472 raw / 2.250e6 orbit floor. Measured here: the local-realizability
      prefilter accepts 0.457 of the first 300 size-five isomorph-free scaffolds at
      4.8 ms per candidate (beside the retained n = 4 exhaustive 26/124 = 0.210).
      Named as ASSUMED: the square-to-chunk transfer of that rate. The go/no-go:
      exhaustive stage-1 is out of reach above K <= 3 by orders of magnitude -- K <= 3
      with measured seatings prices at ~2.1e8 sweep-inclusive LP solves (~73 h at the
      retained 1.28 ms) or ~3 h realization-only, K <= 4 at ~1.4e11, and Trump's own
      decomposition (about five chunks) sits outside the exhaustive range. Four tests
      pin the counted closed forms as the enumerator's omission control.
    evidence:
    - packing/devtools/price_stage1_chunks.py
    - packing/tests/test_price_stage1_chunks.py
    stop_reason: >-
      BC-095's exit met: the price exists as a tool, the factors carry their standing,
      and the go/no-go is a number with its assumptions named rather than an
      impression.
    next_action: >-
      Phase 2 under think-nu4y: the exact-LP measurement at Trump's full cell.
  - workflow: efficiency-loop
    recording: contemporaneous
    clock_role: work
    focus: efficiency
    commitment: BC-096
    bead: think-nu4y
    objective: >-
      BC-096: measure sqpack.exact_lp at Trump's full n = 11 cell, from scratch and
      float-seeded, against T-2's 1.28 ms float baseline, re-verifying the recon
      report's figures first-hand before they enter the record.
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: >-
      BC-095 closed its exit inside its budget, and the delegated recon left phase 2 a
      run-and-record measurement.
    budget_minutes: 30
    started_at: '2026-08-31T06:16:00Z'
    deadline_at: '2026-08-31T06:46:00Z'
    expected_output: >-
      The measured cost of the exact route at full cell scale, recorded beside the
      float baseline in the agenda and the bead.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest tests/test_promote_exact_lp.py -q
    kill_condition: >-
      A measurement disagreeing with the retained test's recorded figures by more than
      host variance -- that would be a finding about the record, not a number to
      average away.
    fallback: >-
      Record the discrepancy as the phase outcome and leave the agenda evidence
      unmoved.
    outcome: >-
      First-hand on this container: assembly 0.41 s for the 1,056-row, 23-variable
      cell; phase 1 (feasible basis from the program's own coefficients) 58.8 s over
      42 pivots; phase 2 22.1 s over 16 pivots; the optimum lands on the published
      side exactly (is_zero). Against the test file's recorded ~100 s on its own host
      and ~2.6 s float-seeded with zero pivots. Per exact pivot ~1.4 s at degree 8.
      Consequence for BC-105: per-stratum exact certification costs seconds
      (float-seeded) to ~81 s (from scratch), so the pipeline sweeps in float and
      certifies winners exactly -- the split the quench already uses -- and exact
      certification of a whole K <= 3 stratum class (~1e6 survivors) is out of reach.
    evidence:
    - packing/tests/test_promote_exact_phase1.py
    - packing/tests/test_promote_exact_lp.py
    stop_reason: >-
      BC-096's exit met: the cost is measured on this host, consistent with the
      retained figures, and the route decision it feeds is recorded.
    next_action: >-
      Close block 2 at its boundary; the checkpoint BC-098 opens as session-052 with
      every dependency complete.
  budget:
    wall_minutes: 120
    finalization_minutes: 15
  progress:
    metric: >-
      Whether BC-104's go/no-go rests on counted and measured factors, and whether
      BC-105's certification route is decided by a measured exact-LP cost.
    before: >-
      The enumeration price in the record was quoted without its artifact and misread
      it (D-405, amended this session); the exact LP's full-cell cost exists only as a
      test file's own note, not as recorded agenda evidence.
    after: >-
      Both numbers exist with their standing labeled: the stage-1 price is an interval
      with its one assumption named and a K <= 3 tractability boundary, and the exact
      LP is measured at full cell scale with the float-sweep/exact-certify split it
      implies. The checkpoint has real evidence to resequence on.
  stop_conditions:
  - >-
    Any candidate mathematical verdict is recorded unresolved with needs_review;
    no verified_* field moves tonight.
  - >-
    Nothing is pushed without packing-validate --push green on the exact tree.
  - >-
    The 20-minute continuity reminder and the 14:07Z finalization alarm are the
    owner's; this run may not delete or disable either (OR-8, D-395).
  delegations:
  - task: >-
      Read-only reconnaissance for BC-096: where the exact Trump n = 11 cell lives in
      the tree (the T-2 rebuild that returns the published side to 4.4e-16 from the
      cell alone), how to assemble that cell's rows for sqpack.exact_lp.solve with
      FieldElement coefficients, what feasible starting vertex is available, and what
      the float baseline path is -- with file:line references and any API mismatches
      named.
    operator: claude-sub-agent-exact-cell-recon
    status: completed
    recording: contemporaneous
    outcome: >-
      BC-096's measurement largely exists in the tree: tests/test_promote_exact_phase1.py
      already solves Trump's full exact cell from its own coefficients -- 23 variables,
      1,056 rows, 25,367 coefficients (1,842 outside Q) -- at a recorded ~100 s
      (73 s phase 1 over 42 pivots, 27 s phase 2 over 16 pivots), with the float-seeded
      path at ~2.6 s and 0 pivots; the 4.4e-16 figure belongs to the float
      independent_lp_cell route, and the exact route lands the published side exactly.
      The quench's cell is a different, 99-row formulation; the exact one mirrors
      independent_lp_cell's 16-rows-per-pair shape. No glue is missing: the phase-2
      measurement reduces to running the retained paths with recorded granularity.
    evidence:
    - packing/tests/test_promote_exact_phase1.py
    - packing/tests/test_promote_exact_lp.py
    - packing/cases/trump11/independent_lp_cell.py
    - packing/cases/trump11/packing.py
    files:
    - no repository file written; read-only investigation
    checks:
    - report reviewed under OR-2; load-bearing claims re-verified before the measurement runs
    uncertainty: >-
      OR-2 posture: the ~100 s and ~2.6 s figures are the test file's own recorded
      claims and are re-measured first-hand in phase 2 before entering the agenda.
    elapsed_seconds: 171
    elapsed_quality: platform_measured
    next_action: >-
      Fold into phase 2 (BC-096) when it opens.
    validation_command: >-
      uv run --frozen --all-extras --group dev pytest tests/test_promote_exact_phase1.py -q
    kill_condition: >-
      A report whose cell-assembly route contradicts the retained T-2 evidence on a
      first-hand check.
    fallback: >-
      Assemble the cell from the retained Trump certificate directly, slower.
    write_scope:
    - no repository writes; read-only investigation
    phase: 1
    started_at: '2026-08-31T06:10:00Z'
    deadline_at: '2026-08-31T06:50:00Z'
    excluded_commands: [git, tbd, packing-validate]
  outputs:
  - packing/campaign/agent-sessions/session-051-block2-reprice-and-lp-gate.md
  - packing/devtools/price_stage1_chunks.py
  - packing/tests/test_price_stage1_chunks.py
  checks:
  - uv run --frozen --all-extras --group dev packing-validate --records
  - uv run --frozen --all-extras --group dev packing-validate --push
  resource_rollups:
  - packing/campaign/resource-usage/913a5de0-f775-52cc-8f42-a03fcbd8234b.yaml
  - packing/campaign/resource-usage/a35f6c5f493ae6cf0.yaml
  stop_reason: >-
    Both block-2 commitments met their exits inside budget; the D-405 amendment this
    block forced is recorded where the wrong claims lived.
  next_action: >-
    The checkpoint opens as session-052 on `BC-098` under `think-cjxk`, with all four
    dependencies complete and two measured prices in hand.
---
# Session-051 — Block 2: the Reprice and the Exact-LP Gate

Contemporaneous record; the frontmatter is the session.
Agenda-010 owns the block plan; the D-405 correction is the reason this block exists.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
