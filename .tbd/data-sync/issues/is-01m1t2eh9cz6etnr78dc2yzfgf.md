---
type: is
id: is-01m1t2eh9cz6etnr78dc2yzfgf
title: Define post-3.81 proof-language concepts in X-016 and the tutorial
kind: task
status: in_progress
priority: 1
version: 3
labels:
  - documentation
  - research
dependencies: []
parent_id: is-01m1sn5t0dm6rjj200pw5p1b7a
hold: blocked
hold_until: null
created_at: 2026-09-06T00:38:45.791Z
updated_at: 2026-09-06T01:31:44.392Z
---
Backfill X-016 with clear working definitions for its proof, fractional, stationary, and closure terminology. Promote the durable concepts needed by general readers into TUTORIAL.md, including typed contacts, Fritz-John/KKT branches, feature ties, zero multipliers, rattlers, and the boundaries among stationarity, rigidity, and global proof. Format, validate, commit, and update PR #89.

## Notes

Implemented in commit 9da7a876 on PR #89; current branch head is 74560389. X-016 now defines the fractional, typed-contact, Fritz-John, multiplier, rattler, stationary-backbone, local-closure, and exact-cover vocabulary it uses. TUTORIAL.md promotes the durable concepts and distinguishes stationarity, rigidity, local isolation, and global optimality. Flowmark, frontmatter/YAML validation, document map/footer/link checks, synopsis consistency, lint/type checks, focused tests, and all substantive push-tier checks pass. Hosted run 34002932978 fails only because session-087 agenda-022 phase 2 remains truthfully in_progress beyond its deadline; PR #87 owns that live session. Do not edit its state solely to green CI. Heartbeat monitor-squares-upstream-and-deepen-research-plan watches PR #87, origin/main, and PR #89, and should clear this hold, rerun checks, close this bead, sync, and delete itself when the upstream gate resolves.
