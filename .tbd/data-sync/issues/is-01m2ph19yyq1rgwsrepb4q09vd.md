---
type: is
id: is-01m2ph19yyq1rgwsrepb4q09vd
title: "Port concurrent exact-verification subprocesses from PR #185"
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels:
  - ci
  - focus-efficiency
dependencies:
  - type: blocks
    target: is-01m2kam88w7r9959zvwcswccx3
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-17T01:52:25.053Z
updated_at: 2026-09-17T16:07:06.975Z
closed_at: 2026-09-17T16:07:06.969Z
close_reason: "Landed with PR #185 (merge d7f9d94d, 2026-09-17), reviewed by an independent Fable reviewer (APPROVE WITH NITS, https://github.com/jlevy/squares/pull/185#issuecomment-5717474006)."
resolution: null
duplicate_of: null
---
PR #185 (head f462ccbb, commit e848aa36) ran exact verification's 17 subprocesses concurrently via _command_workers and _concurrent_commands, with tests test_concurrent_commands_join_in_declared_order_and_report_the_first_declared_failure and test_exact_verification_takes_the_cpus_its_neighbours_leave. PR #188, which supersedes #185, did not carry it: at da2259fb validate.py:2229 still calls the serial _commands, and neither helper nor test exists (the new _command_groups at validate.py:1050 serves a different step). This was not a recorded decision. It only speeds the checks job (94.65 s), which does not set the pull-request wall (suite_b, 143.98 s), so it is not a #188 merge blocker. Port it on a fresh branch after #188 merges, keeping declared-order joins and first-declared-failure reporting, and re-measure the checks tier.

## Notes

2026-09-17 owner request: make PR #185 ready to merge and sequence it with #188 rather than only closing it. Plan: merge #188 first; rebuild #185 as a stacked follow-up on codex/ci-topology-reconcile carrying only the work #188 lacks (think-5hfr's concurrent exact-verification subprocesses and anything else the compatibility analysis finds unique), base codex/ci-topology-reconcile until #188 merges, then main. Close as superseded only if nothing unique remains. Old head f462ccbb will be backed up before the branch is updated.


2026-09-17: ported on rebuilt PR #185 (stacked on #188) as 498dd08e; local push tier passed at 80a5976f (6,630 passed). Close when #185 merges.
