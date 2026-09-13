---
type: is
id: is-01m2e0e4ct972w6eapcr8c3xjz
title: Publish the PR156 draft checkpoint with exact local gates and final hosted CI
kind: task
status: in_progress
priority: 1
version: 8
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
updated_at: 2026-09-13T20:02:16.361Z
started_at: 2026-09-13T18:35:26.795Z
---
Review and commit durable reviews, run-sheet status, records, and accepted source changes; reconcile origin/main with the merge-upstream shortcut; run required push gate; push PR156 as draft; update body with unique cost, exact head, admitted/refused contracts and remaining gates; wait for final hosted CI and sync beads. Do not mark ready while coordinator and run-sheet admission remain refused.

## Notes

PR156 committed clean head 9c56e901 includes final run-sheet blob 29517a3f, reviewed and accepted for scoped command wiring. Records 32/74 and edit 45/74 pass; 1165 documentation links/footers pass. Origin/main d507f5c7 is already an ancestor; merge-upstream was no-op. First required --push attempt on this head stopped at test collection after 58.56s because host libcairo was absent from loader path; development.md explicitly requires DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib. I verified Homebrew libcairo exists and Python 3.14 imports cairosvg successfully with that env. Corrected --push rerun pending; no push or hosted CI yet. No positive profile or BC329 target.
