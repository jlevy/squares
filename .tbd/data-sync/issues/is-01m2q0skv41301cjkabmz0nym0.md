---
type: is
id: is-01m2q0skv41301cjkabmz0nym0
title: A failing command group stops every other step in the validation run
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels:
  - ci
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-17T06:27:50.240Z
updated_at: 2026-09-17T06:27:50.240Z
---
Found 2026-09-17 by the PR #185 rebuild analysis against PR #188 head 16d5e14d. packing/src/sqpack/cli/validate.py:1076-1080, _command_groups calls context.processes.stop() for any exception, including StepFailureError from an ordinary nonzero exit, and the process registry is shared across every step of the run (replace(context, step_name=...) keeps the same processes object); the stopping flag is never reset. Reproduced with attic/pr185/probe_command_groups.py in the consolidate-stack worktree: at --jobs 2 an unrelated concurrent command fails 'exited -15'; at --jobs 1 every later step fails 'validation is stopping; rejected new subprocess'. Fails closed, so no unsafe verdict, but one real failure is reported as many and other steps' verdicts and timings are lost; the docstring's 'as a failure in the outer step pool does' is inaccurate. Fix: keep ordinary failures inside the step (let running groups finish, raise the earliest declared failure), as the ported _concurrent_commands does, or stop the registry only on BaseException. Planned to land with the rebuilt PR #185, which already touches this code.
