---
type: is
id: is-01m2ckzy45b1b28pvt1nbh4gdm
title: Add a bounded experimental multi-run scheduler
kind: task
status: open
priority: 1
version: 12
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-phase-5
  - workbench-roadmap
dependencies:
  - type: blocks
    target: is-01m2b7nakccj4tf1tgs4k86nar
  - type: blocks
    target: is-01m2pkfjhe627n9qa4761eb6zm
  - type: blocks
    target: is-01m2pkfk9z36garp9891702grd
parent_id: is-01m2b7n9tyq13n0zw4tkq4rfss
child_order_hints:
  - is-01m2dvhp7pymsbvgpfjkphq0jd
  - is-01m2dvhspdnayysbczbgrrp7h7
created_at: 2026-09-13T05:31:41.572Z
updated_at: 2026-09-17T03:01:07.719Z
---
Phase 5 after clean Pack/Animate readiness. The typed proposal/force/schedule/repair/objective interfaces live in think-6qxx; this task schedules repeated calls to that same Pack run API. Own seeds/restarts, parameter cells, completed work budgets, responsive progress/cancel, checkpoint/resume manifests where supported, and corrected aggregation. Absolute side works without a reference; excess/closed require identified finite references and positive normalization gap. Declare whether feasible transient snapshots may rank; invalid/cancelled states never rank and status counts remain separate. Acceptance: browser/headless receipts agree, mixed/empty/interrupted/zero-gap controls pass, disjoint blocks preserve unsuccessful attempts, two registry configurations compare under equal completed work, held-out partitions stay fixed.

## Notes

2026-09-13 PR #160 checkpoint: typed registry, disjoint scheduler, deterministic Pack runner, exact-work receipts, cancellation, ledger resume and bounded Search panel implemented; Node and focused browser checks pass. Still open: responsive proposal/Resolve execution, full configurable optimization methods, equal-work browser/headless acceptance, CLI and distributions.

2026-09-16 guidance addition from duplicate think-t0g7: receipts must hash the shared target/application configuration and prove that CLI and browser replay the same seed, schedule, stop condition, trajectory, validity result, and metric vector.


2026-09-17 (PR #190 revision, review finding S10): registered guidance cohorts set SearchSlot.timeoutMs to null, because a timeout changes slot status and partial results by wall clock; receipt identity hashes SearchTrialValue (or its canonical successor), not SearchOutcome, which carries elapsedMs. Guided receipts through the scheduler are think-10yz.


2026-09-17 (PR #190 revision after the cdd9aad8 review): the CLI this note lists as open is a deliverable here. A Node command runs a Search plan headlessly and writes the ledger that think-i5pg re-admits; think-9hdg and think-0epc use it. No such command exists yet: the package's Node tools are build, bundle, corpus-check, KaTeX and kinetics commands, and measure:kinetics is its only measurement script.
