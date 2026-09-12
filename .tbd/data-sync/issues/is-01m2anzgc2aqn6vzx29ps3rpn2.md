---
type: is
id: is-01m2anzgc2aqn6vzx29ps3rpn2
title: Publish BC329 admission work as a stacked progress PR
kind: task
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: root publication lane
labels:
  - n11
  - pr
dependencies: []
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T11:27:55.777Z
updated_at: 2026-09-12T13:30:53.449Z
---
Commit the admitted runner and scheduler repairs on codex/n11-bc329-runner-publication-stack, push the exact head, and open a clean draft PR stacked on PR #149. Lead the PR body with measured implementation, validation, and agent costs; state that no BC329 scientific target has run; enumerate the open calibration and documentation gates; verify the base/head relationship and hosted CI. Update the PR at each later calibration, admission, or scientific milestone without conflating work completed on PRs #148 and #149.

## Notes

Runner implementation is committed at 5095241d; exact-head pre-push is running. PR149 advanced by one CI-classification commit and will be merged into this stack before the final exact-head gate, push, and draft PR creation. The PR body is staged at /private/tmp/bc329-pr-body.md. No BC329 target has run.
