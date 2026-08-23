---
type: is
id: is-01m0r2atvyphxm28s5819fn3rg
title: "Rehearse the recovery path: claim -> ledger -> release -> ledger, against a scratch record"
kind: task
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - focus-process
dependencies: []
parent_id: is-01m0pw7redm194km37gpb3cvmf
created_at: 2026-08-23T19:42:33.854Z
updated_at: 2026-08-23T21:32:08.874Z
---
D-032 and D-033 are one lesson: PR #13 merged with `release` and `run` never once executed, and both were broken. `release` is the step that runs when a round dies at 3am, so it is the step least likely to be exercised by hand and worst to have broken.

Neither fix left an unconditional check. ledger.py validating every artifact at load time (the D-005 guard) does catch an invalid stub, and a gate run during an in-progress round does exercise the lease comparison -- but both only fire if a gate run happens to coincide with a round in flight. That is luck, not a guard.

What to build: a preflight step that rehearses claim -> ledger -> release -> ledger end to end and asserts the record is schema-valid at every point, including that the released round carries an `effort` block with `stopped_by: error`.

The constraint that makes this real work rather than a one-liner: claim and release MUTATE the real record, so preflight cannot call them against it -- a preflight that leaves an in-progress round behind is worse than no preflight. It needs a scratch copy of the record directory and the runner pointed at it, which means the record root has to become a parameter rather than a constant.

Do not solve this by pasting the claim/release logic into the test. That exact mistake was already made once here: the first rehearsal step reimplemented the allocator instead of importing it, and tested a copy of the code rather than the code. Import the real functions or the rehearsal proves nothing.
