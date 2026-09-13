---
type: is
id: is-01m2e0e4ct972w6eapcr8c3xjz
title: Publish the PR156 draft checkpoint with exact local gates and final hosted CI
kind: task
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: codex@spud10.local
labels:
  - n11
dependencies:
  - type: blocks
    target: is-01m2csyyq4nzfqppqj639avs51
parent_id: is-01m2ctdap5jwdr8h4qb8dxwt8z
hold: null
hold_until: null
created_at: 2026-09-13T18:28:24.089Z
updated_at: 2026-09-13T19:03:14.376Z
started_at: 2026-09-13T18:35:26.795Z
---
Review and commit durable reviews, run-sheet status, records, and accepted source changes; reconcile origin/main with the merge-upstream shortcut; run required push gate; push PR156 as draft; update body with unique cost, exact head, admitted/refused contracts and remaining gates; wait for final hosted CI and sync beads. Do not mark ready while coordinator and run-sheet admission remain refused.

## Notes

At local PR156 head 0874e912, durable reviews and run-sheet status are committed, F6/F7 reader candidate 95830f9e and six-finding run-set verifier candidate 0874e912 are integrated, and origin/main is an ancestor (merge-upstream no-op). Corrected records/edit tiers passed before the latest source commits. An obsolete-head pre-push run was interrupted immediately when the newer verifier repair arrived; rerun --push on the settled exact head before draft push. Reader Astra review has confirmed new finite aggregate overflow think-px86; coordinator and verifier independent rereviews remain. Remote PR156 head and CI are stale; no positive profile or BC329 target ran.
