---
type: is
id: is-01m0r4jb9qj3fk9sjm9senp9gz
title: negctl leaves the repo holding a deliberate sabotage if it is interrupted
kind: bug
status: closed
priority: 0
version: 8
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels:
  - focus-efficiency
dependencies:
  - type: blocks
    target: is-01m0r7r9k8dcz960yqpx69vwnm
parent_id: is-01m0pqfp4rm5r4fy7ys6t03h0w
created_at: 2026-08-23T20:21:37.206Z
updated_at: 2026-08-23T22:58:40.299Z
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

2026-08-23 23:0x, from the PR #16 closeout. NOT A DISPUTE OF THE FIX -- a note that it is not visible anywhere yet, so it cannot be lost silently.

This bead is closed with a detailed close reason (snapshot-based controls, reaped checker children, shared atomic activity lease, SIGTERM/SIGKILL rehearsals, 27 isolated controls, 74 reconciled defect records). None of that is in any pushed branch as of now:

  origin/main                              8926a7c  -- D-035 outstanding, negctl unchanged
  origin/codex/pr14-square-packing-review  a7e7adc  -- D-035 outstanding, negctl unchanged, 65 defects
  origin/claude/thinking-scratchpad-...    2ce0209  -- stacked on a7e7adc, same

The "74 defect records" in the close reason against 65 on the newest pushed commit says the work is real and ahead of what is published. So: push it. Until it lands, `tbd ready` shows no D-035 work while D-035 is live in every branch that exists, which is the one failure mode a closed bead can cause.

Practical consequence for anyone working from a pushed branch right now: negctl still mutates tracked files in place and restores in a `finally:` that SIGKILL does not run. Run `git status` before `git add -A`. That advice retires the moment the fix is pushed.
