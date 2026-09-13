---
type: is
id: is-01m2e0e4ct972w6eapcr8c3xjz
title: Publish the PR156 draft checkpoint with exact local gates and final hosted CI
kind: task
status: in_progress
priority: 1
version: 14
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: codex@spud10.local
labels:
  - n11
dependencies:
  - type: blocks
    target: is-01m2csyyq4nzfqppqj639avs51
  - type: blocks
    target: is-01m2dzgknq7k2cj3ea91thkcmj
  - type: blocks
    target: is-01m2e0qcksvn1sygh0tn3kj11d
  - type: blocks
    target: is-01m2e9ggafpy2xvk0r0rgy1p8w
parent_id: is-01m2ctdap5jwdr8h4qb8dxwt8z
child_order_hints:
  - is-01m2e7adq6sc2j6mzgsx89sg8h
hold: null
hold_until: null
created_at: 2026-09-13T18:28:24.089Z
updated_at: 2026-09-13T21:07:05.969Z
started_at: 2026-09-13T18:35:26.795Z
---
Review and commit durable reviews, run-sheet status, records, and accepted source changes; reconcile origin/main with the merge-upstream shortcut; run required push gate; push PR156 as draft; update body with unique cost, exact head, admitted/refused contracts and remaining gates; wait for final hosted CI and sync beads. Do not mark ready while coordinator and run-sheet admission remain refused.

## Notes

2026-09-13 21:03 UTC publication handoff: PR #156 draft branch codex/n11-bc329-runner-publication-stack pushed by fast-forward 52e4ab65..9c56e9019b97be0511d5afe590790b362b93e9e4; clean worktree, remote API confirms exact head, main d507f5c7 still ancestor. Cost-first PR body updated at https://github.com/jlevy/squares/pull/156 with current 56-file +31842/-169 diff, conservative 40-root/86-session usage subtotal cutoff, and explicit no-target scope. Local records 32/74, edit 45/74, 1165 doc links/footers and final source integrations passed. First --push at 9c failed Cairo loader collection; corrected --push ran 1292.99s and FAILED reachable behavioral step with unretained exact failure (terminal output truncated). Standalone exact-head reachable rerun passed 5511 tests, 9 skipped, 57 deselected in 2002.14s; this does not convert failed full --push into a pass. Hosted CI for exact 9c is currently PENDING: geometry, macOS, prepare, suite, sweeps, validate; merges-into-main passed. Do not mark PR ready or claim profile/BC329 science: three full-shape profiles and target remain unrun, integrated operational admission remains under think-pp3j. The PR157 coordinator must preserve source-closure review because PR157 changes five PR156 source paths; old-base PR157 green CI is not combined-head validation.
