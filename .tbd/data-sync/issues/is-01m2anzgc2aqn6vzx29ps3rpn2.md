---
type: is
id: is-01m2anzgc2aqn6vzx29ps3rpn2
title: Publish the BC329 baseline runner as a stacked draft PR
kind: task
status: in_progress
priority: 1
version: 10
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: root publication lane
labels:
  - n11
  - pr
dependencies:
  - type: blocks
    target: is-01m2axbxf0xz00ezc32q4mesn2
  - type: blocks
    target: is-01m260z2959dmcmn61pn2z7jsk
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T11:27:55.777Z
updated_at: 2026-09-12T14:45:13.478Z
---
Commit the admitted baseline runner on codex/n11-bc329-runner-publication-stack, push the exact head, and open a clean draft PR stacked on PR #149. Lead the PR body with measured implementation, validation, and agent costs; state that no BC329 scientific target has run; enumerate every remaining hardening, calibration, admission, documentation, and scientific gate; and verify the base/head relationship and hosted CI. Later scientific documentation, accounting, and final PR-body reconciliation belong to think-zd1b, think-92jm, and think-iexs.

## Notes

Draft stacked PR #156 is open at https://github.com/jlevy/squares/pull/156, base
claude/lower-bound-proof-strategies-n62nyx (PR #149), head
codex/n11-bc329-runner-publication-stack at 5fa83cc7; GitHub reports MERGEABLE.
Every hosted check completed successfully on that exact head: build, Firefox and WebKit
font loading, geometry, macOS portability, mergeability, packing-required, prepare,
suite, sweeps, and validate passed; policy-deferred jobs skipped.

Runner implementation is 5095241d; first exact-head pre-push passed 46/74 steps with
5,156 tests in 1,096.64s. PR #149 head 4d00ab68 merged without conflict as 5fa83cc7;
clean 23-path source manifest and 45-step edit gate pass. Rejected costs retained in the
PR body: 42.91s edit with missing venv PATH, 1,118.21s pre-push with missing uv, 13.99s
focused environment diagnosis, and a sandboxed pre-push with 5,150 passes in 1,124.67s
but six denied process/loopback controls. An unrestricted exact-head pre-push is running
as session 28481 with a retained transcript. The body includes a separate native
child-task subtotal and says no BC329 target has run.

Keep this bead open until session 28481 gives a valid exact-head result and that result
is added to the PR. Subsequent repair, partial-direction, calibration, documentation,
and target work remain separate blocking beads.
