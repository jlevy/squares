---
type: is
id: is-01m0r2atvyphxm28s5819fn3rg
title: "Rehearse the recovery path: claim -> ledger -> release -> ledger, against a scratch record"
kind: task
status: closed
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - focus-process
dependencies: []
parent_id: is-01m0rkz14t04yjme92gnfncfv7
created_at: 2026-08-23T19:42:33.854Z
updated_at: 2026-10-10T22:49:30.718Z
closed_at: 2026-10-06T08:33:06.685Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): D-032 and D-033 fixed; packing/tests/test_campaign_runner_trust_boundary.py on origin/main runs the real claim/execute/release functions against a scratch record tree, including test_run_releases_the_round_and_still_reports_when_a_step_refuses (asserts effort.stopped_by == error) and test_a_released_round_is_committed
resolution: null
duplicate_of: null
---
D-032 and D-033 are one lesson: PR #13 merged with `release` and `run` never once executed, and both were broken. `release` is the step that runs when a round dies at 3am, so it is the step least likely to be exercised by hand and worst to have broken.

Neither fix left an unconditional check. ledger.py validating every artifact at load time (the D-005 guard) does catch an invalid stub, and a gate run during an in-progress round does exercise the lease comparison -- but both only fire if a gate run happens to coincide with a round in flight. That is luck, not a guard.

What to build: a preflight step that rehearses claim -> ledger -> release -> ledger end to end and asserts the record is schema-valid at every point, including that the released round carries an `effort` block with `stopped_by: error`.

The constraint that makes this real work rather than a one-liner: claim and release MUTATE the real record, so preflight cannot call them against it -- a preflight that leaves an in-progress round behind is worse than no preflight. It needs a scratch copy of the record directory and the runner pointed at it, which means the record root has to become a parameter rather than a constant.

Do not solve this by pasting the claim/release logic into the test. That exact mistake was already made once here: the first rehearsal step reimplemented the allocator instead of importing it, and tested a copy of the code rather than the code. Import the real functions or the rehearsal proves nothing.
