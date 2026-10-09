---
type: is
id: is-01m4gve5z0rn7s43dyr04hgj28
title: "Admit #472's 12 native kernel certificates (wand125) after clean replay and custody"
kind: task
status: in_progress
priority: 1
version: 3
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: claude-code@vm
labels:
  - n-17
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
hold: null
hold_until: null
created_at: 2026-10-09T17:30:09.760Z
updated_at: 2026-10-09T18:52:26.221Z
started_at: 2026-10-09T18:52:23.854Z
---
Issue #472: 12 sub-pattern certificates from this repo's own producer (check_n17_subpattern mode A), standing kernel verifier FULL PASS at blob 1ad706c21 (main f0ec5b6), receipts dirty:true from a wrapper checkout with one hand-edited directory field each; hosted in wand125/square-packing releases (HostedData/v1). Exact projection vs main's 60-entry ledger: -1,047 orbits / -8,240 states -> 3,636 / 28,528; distance-2 tail 95 -> 94 (row 23). Needs: clean-worktree FULL replay under a ledger-listed verifier (main's verifier is now be8135f6, unlisted), Rust parity, custody under a census-readable manifest, admission round. Est. ~2 CPU-h, ~4 agent-h. Owner decision to start.

## Notes

2026-10-09T18:52Z User go-ahead 2026-10-09 ~18:55 UTC: do it here in parallel. Container: 4 cores, 15 GB RAM, cargo present; wand125 release downloads work; uploads.github.com reachable directly (302). Plan: admission-grade replay under listed verifier blob 1ad706c21 (main 3213d651b), forward check under be8135f6e, Rust parity, mirror to jlevy/squares release data/n17-issue-472-kernel-certificates-v1 with HostedData manifest, admission round on branch based on #475. Estimate ~3-4 h wall, ~4-6 CPU-h.
