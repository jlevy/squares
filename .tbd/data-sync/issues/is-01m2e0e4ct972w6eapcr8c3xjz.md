---
type: is
id: is-01m2e0e4ct972w6eapcr8c3xjz
title: Publish the PR156 draft checkpoint with exact local gates and final hosted CI
kind: task
status: in_progress
priority: 1
version: 5
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
updated_at: 2026-09-13T19:22:37.839Z
started_at: 2026-09-13T18:35:26.795Z
---
Review and commit durable reviews, run-sheet status, records, and accepted source changes; reconcile origin/main with the merge-upstream shortcut; run required push gate; push PR156 as draft; update body with unique cost, exact head, admitted/refused contracts and remaining gates; wait for final hosted CI and sync beads. Do not mark ready while coordinator and run-sheet admission remain refused.

## Notes

At local PR156 head 5a890a1b, 31 commits ahead of remote 52e4ab65. Reader finite-clock repair a5701e73, coordinator three-finding repair dbbf8495, verifier R3 repair 2ea77405, and durable refusal reviews/run-sheet status are committed. Pinned Rust Flowmark hook passed. Updated records tier passed 32/74 in 43.48s and documentation links/footers pass; edit tier is running. Independent reader exact-head review has 23/23 real-binder controls so far, full suite pending. Coordinator review found finite phase-sum overflow think-dgfk and infinite deadline identity think-0osz; isolated repair in progress. Verifier R3 repair awaits independent review. Remote head/CI are stale, required --push not yet run on settled head, no positive profile/BC329 target.
