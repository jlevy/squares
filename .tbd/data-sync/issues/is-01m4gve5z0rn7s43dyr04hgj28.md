---
type: is
id: is-01m4gve5z0rn7s43dyr04hgj28
title: "Admit #472's 12 native kernel certificates (wand125) after clean replay and custody"
kind: task
status: in_progress
priority: 1
version: 5
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: claude-code@vm
labels:
  - n-17
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
child_order_hints:
  - is-01m4h1cx9na53vx9yjzmddwyqm
hold: null
hold_until: null
created_at: 2026-10-09T17:30:09.760Z
updated_at: 2026-10-09T19:14:19.573Z
started_at: 2026-10-09T18:52:23.854Z
---
Issue #472: 12 sub-pattern certificates from this repo's own producer (check_n17_subpattern mode A), standing kernel verifier FULL PASS at blob 1ad706c21 (main f0ec5b6), receipts dirty:true from a wrapper checkout with one hand-edited directory field each; hosted in wand125/square-packing releases (HostedData/v1). Exact projection vs main's 60-entry ledger: -1,047 orbits / -8,240 states -> 3,636 / 28,528; distance-2 tail 95 -> 94 (row 23). Needs: clean-worktree FULL replay under a ledger-listed verifier (main's verifier is now be8135f6, unlisted), Rust parity, custody under a census-readable manifest, admission round. Est. ~2 CPU-h, ~4 agent-h. Owner decision to start.

## Notes

2026-10-09T18:52Z User go-ahead 2026-10-09 ~18:55 UTC: do it here in parallel. Container: 4 cores, 15 GB RAM, cargo present; wand125 release downloads work; uploads.github.com reachable directly (302). Plan: admission-grade replay under listed verifier blob 1ad706c21 (main 3213d651b), forward check under be8135f6e, Rust parity, mirror to jlevy/squares release data/n17-issue-472-kernel-certificates-v1 with HostedData manifest, admission round on branch based on #475. Estimate ~3-4 h wall, ~4-6 CPU-h.



2026-10-09T19:14Z Integrity: 24 objects (411,682,476 B) SHA-256 + manifests OK. Rust parity (toolchain 1.98.0, n17_kernel_verify at 6a0499ba4): 12/12 PASS, all closures all_parent_poses_forbidden, 26 fields agree with contributor Python receipts; total ~12 min loaded. Paperwork: exp-317 registered locally (3d132c3e0 on i472/admission based on 2beac080d); dry-run census 3,636/28,528. Decisions: use ledger release data/n17-x048-session-168-certificates-v1 for custody (census reads only that manifest); parity comparator recorded as declared deviation + OR-1 bead; disclose replay started 18:57 before exp-317 commit (criteria from H-341 at 17:51). Python listed-blob replay in progress.
