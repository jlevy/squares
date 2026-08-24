---
title: session-001 — reset PR 15 to the tight research loop
softschema:
  contract: packing.squares:AgentSession/v1
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-001
  title: Reset PR 15 to the tight research loop
  date: '2026-08-23'
  goal: >-
    Quarantine the abandoned isolation detour, correct the stable research record, and
    leave one visible, measured delegation loop on a clean reviewable PR.
  focus: process
  primary_bead: think-m79h
  status: completed
  budget:
    wall_minutes: 240
    max_cycles: 8
  stop_conditions:
  - The branch cannot reach a clean normal gate without expanding into a new subsystem.
  - A correction needs mathematical or product judgment from the user.
  - Three consecutive focused checks fail for the same cause.
  - Two cycles do not move the declared progress metric.
  progress:
    metric: reviewable PR checkpoint with one reconciled record and visible delegation
    before: >-
      Stable pushed checkpoint a7e7adc plus an uncommitted hostile-isolation prototype,
      false bead closure claims, and inconsistent experiment timing records.
    after: >-
      Isolation prototype preserved only in a named local attic stash; stable beads
      reconciled; focused timing, provenance, n=12 and H-002 corrections implemented;
      versioned session contract integrated; normal gate green in 126 seconds with 30
      controls and 74 defect entries.
  delegations:
  - task: Recover the pre-reset working snapshot so useful ideas could be preserved safely
    operator: recover_pre_reset_snapshot
    status: completed
    outcome: Reconstructed the exact recoverable prototype and enabled it to be quarantined in a named local attic stash.
    evidence:
    - Eleven tracked paths and one untracked activity module were recovered before the stash.
    - git diff --check passed on the recovered snapshot.
    files: []
    checks: [git diff --check]
    uncertainty: The prototype is retained for reference but none of its implementation claims landed.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Reuse only a focused timeout or crash-recovery pattern if later measurement justifies it.
  - task: Inventory the existing autonomous research loop and identify the smallest missing layer
    operator: autonomous_loop_inventory
    status: completed
    outcome: Found that the repository already has the scientific loop; only a small outer session and delegation record was missing.
    evidence:
    - Nine codified hypotheses, eleven experiments, nine raw JSONL archives and one exploration already exist.
    - tbd, runner state, schemas, ledgers and stop rules cover work below the outer agent loop.
    files: []
    checks: [Read-only cross-artifact inventory]
    uncertainty: Agent, wait and retry timing had not previously been captured.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Add one validated session artifact and keep the persistent goal as controller.
  - task: Inventory measured loop latency and stable record drift
    operator: loop_timing_inventory
    status: completed
    outcome: Established practical loop tiers and found the omitted exp-011 time and wall-versus-CPU unit error.
    evidence:
    - Stable normal-gate checkpoint was 108 seconds; older strict/deep gates were 291–298 seconds.
    - Exp-011 raw summaries total 397.474 seconds, bringing all eleven rounds to 23.0 wall-minutes.
    files: []
    checks: [Read-only timing and artifact reconciliation]
    uncertainty: The stable 108-second run has no retained per-stage breakdown or repetitions.
    elapsed_seconds: null
    elapsed_quality: unavailable
    next_action: Capture a versioned repeated normal-gate benchmark under think-xzew.
  - task: Correct experiment effort totals, units, round counts and active n=12 instructions
    operator: measurement_corrections
    status: completed
    outcome: All terminal rounds now carry wall time; generated and living totals agree at eleven rounds and 23.0 wall-minutes.
    evidence:
    - The five retained exp-011 summaries sum exactly to 397.474 seconds.
    - A new mutation control removes wall_seconds and observes ledger refusal.
    files:
    - campaign/ledger.py
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-011-h-020-n17.md
    - run_baseline.sh
    checks:
    - campaign/ledger.py --check
    - tools/validate_schemas.py
    - tools/check_synopsis.py
    - focused negative control
    uncertainty: The normal gate still needs to run on the integrated changes.
    elapsed_seconds: 900
    elapsed_quality: operator_reported_approximate
    next_action: Integrate with defects D-066 through D-068 and run the checkpoint gate.
  - task: Reconcile H-002 with the quench experiments that already measured it
    operator: h002_record_cleanup
    status: completed
    outcome: H-002 now names the built instrument and preserves its refuted universal claim and useful local role.
    evidence:
    - Exp-007 and exp-008 reach machine precision on tested n=5 and n=10 outputs.
    - Exp-009 remains 6.29e-02 above the n=11 standing best.
    files: [campaign/hypotheses/H-002-lp-in-cell-polish.md]
    checks: [campaign/ledger.py --check, git diff --check]
    uncertainty: No global convergence, basin identity or exact-certification claim follows.
    elapsed_seconds: 480
    elapsed_quality: operator_reported_approximate
    next_action: Record D-069 and keep proposal rather than polish as the current bottleneck.
  - task: Make runner terminal timing and execution provenance survive separate steps
    operator: runner_timing_provenance
    status: completed
    outcome: Execute appends one timing/provenance receipt; record and release consume it without substituting record-time HEAD.
    evidence:
    - Exp-011 execution provenance was restored to 60a50cc.
    - The focused preflight exercised receipt parsing; integration review added the direct artifact-mapping regression under D-074.
    files:
    - campaign/runner.py
    - campaign/series/series-000-smoke-and-calibration/experiments/exp-011-h-020-n17.md
    checks:
    - campaign/runner.py preflight
    - campaign/ledger.py --check
    - Ruff
    - BasedPyright
    - git diff --check
    uncertainty: >-
      No actual search round was run. The first focused preflight parsed the receipt but
      did not exercise its artifact-field mapping; integration review added D-074 and a
      direct mutation-tested mapping check.
    elapsed_seconds: 720
    elapsed_quality: operator_reported_approximate
    next_action: Exercise the integrated receipt and artifact mapping in the normal gate.
  - task: Apply and verify the final mechanical Python formatting pass
    operator: delta_hygiene_audit
    status: completed
    outcome: >-
      Ruff formatted the latest runner delta, identified one line-length miss, applied
      the requested wrap, and left both changed Python files clean.
    evidence:
    - The first formatter pass completed in 0.6 seconds and exposed one E501 line.
    - The focused follow-up fixed only that line and completed in about 1.9 seconds.
    files: [campaign/runner.py]
    checks: [Ruff format-check, Ruff check, BasedPyright, git diff --check]
    uncertainty: No semantic review or full gate was delegated.
    elapsed_seconds: 2.5
    elapsed_quality: operator_reported_approximate
    next_action: Parent performs integration review and the normal gate.
  outputs:
  - README.md autonomous-loop contract
  - campaign/agent-sessions/session-001-pr15-review-reset.md
  - defects.yaml D-066 through D-074
  checks:
  - Delegated focused checks passed.
  - The first integrated gate stopped at the lint floor on two Ruff-format diffs.
  - A delegated mechanical format and lint pass completed in about 1.5 seconds.
  - The pre-commit review found and fixed D-074, whose first regression parsed the receipt but did not exercise its artifact mapping.
  - The final normal gate passed in 126 seconds with 30 controls and 74 defects.
  - The branch is based directly on merged PR 14 at 8926a7c with no merge conflict.
  stop_reason: >-
    Completed the declared reviewable checkpoint: the detour is quarantined, records
    and beads reconcile, the retained loop is documented and the normal gate is green.
  next_action: Resume the broader Correctness and Insight review from the ready bead queue, beginning with the highest-priority mathematical ambiguity.
---
# Session 001 — reset PR 15 to the tight research loop

This session returned the branch to the intended architecture: a persistent goal and
`tbd` drive the outer loop; small focused tools execute work; mathematical ideas and
measurements enter the existing campaign record; defects enter the categorized logbook;
and this artifact makes delegation and elapsed time visible.

The isolation prototype is recoverable only from the local, nonportable stash named
`attic: overengineered D035 isolation prototype before autonomous-loop reset`; it is not
part of the PR. The only retained robustness changes are local to the existing runner:
subprocess timeboxes, durable execution timing and provenance, and explicit terminal
stop reasons.

## Delegation summary

| Task | Result | Elapsed |
| --- | --- | ---: |
| Recovery | Prototype recovered, then quarantined | not captured |
| Loop inventory | Existing architecture mapped; one outer-session gap identified | not captured |
| Timing inventory | Stable tiers and effort defects identified | not captured |
| Measurement correction | Eleven-round, 23.0-wall-minute record reconciled | about 15 minutes |
| H-002 correction | Canonical hypothesis reconciled with four measured rounds | about 8 minutes |
| Runner correction | Execution timing and provenance made durable across steps | about 12 minutes |
| Python hygiene | Final formatter, lint and type pass delegated | about 2.5 seconds |

The missing early elapsed values are recorded as missing rather than estimated.
Future delegation briefs require elapsed wall time in the return contract.

The final integrated normal gate passed in 126 seconds after the earlier lint stop and
the D-074 pre-commit correction; all 30 mutation controls fired and all 74 defect
records reconciled.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
