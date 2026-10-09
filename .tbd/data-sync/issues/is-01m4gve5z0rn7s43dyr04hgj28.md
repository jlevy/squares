---
type: is
id: is-01m4gve5z0rn7s43dyr04hgj28
title: "Admit #472's 12 native kernel certificates (wand125) after clean replay and custody"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
labels:
  - n-17
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-09T17:30:09.760Z
updated_at: 2026-10-09T17:30:09.760Z
---
Issue #472: 12 sub-pattern certificates from this repo's own producer (check_n17_subpattern mode A), standing kernel verifier FULL PASS at blob 1ad706c21 (main f0ec5b6), receipts dirty:true from a wrapper checkout with one hand-edited directory field each; hosted in wand125/square-packing releases (HostedData/v1). Exact projection vs main's 60-entry ledger: -1,047 orbits / -8,240 states -> 3,636 / 28,528; distance-2 tail 95 -> 94 (row 23). Needs: clean-worktree FULL replay under a ledger-listed verifier (main's verifier is now be8135f6, unlisted), Rust parity, custody under a census-readable manifest, admission round. Est. ~2 CPU-h, ~4 agent-h. Owner decision to start.
