---
type: is
id: is-01m0r4jb9qj3fk9sjm9senp9gz
title: negctl leaves the repo holding a deliberate sabotage if it is interrupted
kind: bug
status: closed
priority: 0
version: 7
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels:
  - focus-efficiency
dependencies:
  - type: blocks
    target: is-01m0r7r9k8dcz960yqpx69vwnm
parent_id: is-01m0pqfp4rm5r4fy7ys6t03h0w
created_at: 2026-08-23T20:21:37.206Z
updated_at: 2026-08-23T22:51:36.085Z
closed_at: 2026-08-23T22:51:36.084Z
close_reason: "Resolved by eliminating live-worktree sabotage entirely: negctl now runs controls in a stable snapshot of current tracked and non-ignored bytes, checker children are stopped and reaped before sandbox cleanup, every gate/runner critical section uses the shared atomic activity lease, writer capabilities are stripped from descendants, and real simultaneous-acquisition plus SIGTERM/SIGKILL rehearsals cover the lifecycle. The full normal ./test.sh gate passed in 129 seconds with all 27 isolated controls, 74 reconciled defect records, three activity checks, and three isolation/crash checks."
---
D-035. Hit for real on 2026-08-23, mid-session.

tools/negctl.py tests each guard by CORRUPTING a tracked source file in place, running the check, asserting it fails, and restoring the bytes in a `finally:` block. `finally` covers exceptions. It does not cover SIGKILL, a killed process group, an OOM, a machine sleeping, or an agent harness cancelling a tool call.

What happened: a `./test.sh` run was interrupted during the negative-controls step. The mutation left behind was the D-031 seam control -- `% steps` stripped from `_quantize_angle`, which is precisely the subtle, flattering basin-splitting bug the project had just spent a day finding. The next gate run failed with `FAIL an angle one ULP below pi/2 keys as one at zero`, which reads exactly like a regression in the code under test rather than like a dirty tree.

Two things make this worse than a normal dirty-tree problem:

1. The mutations are DESIGNED to be subtle and to point in the flattering direction. That is the whole purpose of a negative control. So the residue is the most dangerous possible thing to leave in a working tree.
2. `git add -A && git commit` would have committed it. In an unattended session that commits on a cadence, this is a live path to shipping a deliberate sabotage of basin identity with a green-looking history.

WHAT TO BUILD

- Write a marker file naming the file, its checksum and the control before mutating; on startup, if the marker exists, restore from the recorded bytes and refuse to run until it is clean. `.gate-running` already establishes the marker pattern in this repo.
- Install signal handlers for SIGINT and SIGTERM that restore before exiting. This does not cover SIGKILL, which is why the marker is the primary mechanism and the handler is the courtesy.
- Have the gate refuse to start when the marker is present, with a message that says what to do.
- Consider mutating a COPY in a temp dir and pointing the check at it via an env var, which removes the hazard rather than detecting it. Note the constraint that killed the last attempt at this: the check must import the real module under test, not a pasted copy, so the copy has to be import-path-visible.
- Have runner.py's commit step refuse to stage a file the negctl marker names.

## Notes

2026-08-23 second-pass design after adversarial review: eliminated live-source mutation and recovery entirely. negctl snapshots all current tracked/non-ignored bytes twice into a temporary Git repo; controls mutate only that copy, reset between cases, and discard evidence if live source changes. Real SIGTERM test kills/reaps a TERM-ignoring checker; real SIGKILL test proves live bytes untouched. Gate and every runner CLI use the atomic activity lease; full gate still required before closure. Related findings: D-068 through D-074 and beads think-5zzb, think-xe5l, think-tg66, think-1pyr, think-6wgw, think-06vo, think-v8ve.
