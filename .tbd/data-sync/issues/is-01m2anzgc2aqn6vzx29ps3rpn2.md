---
type: is
id: is-01m2anzgc2aqn6vzx29ps3rpn2
title: Publish the BC329 baseline runner as a stacked draft PR
kind: task
status: in_progress
priority: 1
version: 8
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
updated_at: 2026-09-12T14:29:55.720Z
---
Commit the admitted baseline runner on codex/n11-bc329-runner-publication-stack, push the exact head, and open a clean draft PR stacked on PR #149. Lead the PR body with measured implementation, validation, and agent costs; state that no BC329 scientific target has run; enumerate every remaining hardening, calibration, admission, documentation, and scientific gate; and verify the base/head relationship and hosted CI. Later scientific documentation, accounting, and final PR-body reconciliation belong to think-zd1b, think-92jm, and think-iexs.

## Notes

Runner implementation is committed at 5095241d. Its first exact-head pre-push passed 46/74 steps with 5,156 tests in 1,096.64s. Current PR149 head 4d00ab68 merged without conflict as 5fa83cc7; a clean 23-path source manifest and 45-step edit gate pass. The first merged-head pre-push ran 1,118.21s with 5,155 tests passing but one copied-tree control unable to find uv because the invocation omitted uv from child PATH. Focused diagnosis passed after adding project PATH and writable UV_CACHE_DIR. The corrected sandboxed run reached 5,150 passed in 1,124.67s but six process/loopback controls were denied by the macOS sandbox, so it is diagnostic only. An unrestricted exact-head pre-push is running as session 28481 with a retained transcript. Draft PR body records all rejected and accepted costs plus a native child-task subtotal. No BC329 target has run.
