---
type: is
id: is-01m5j10qmw6d55ghhfxg9ekww1
title: Migrate generated site URLs and validate legacy profile links
kind: task
status: in_progress
priority: 2
version: 8
spec_path: docs/project/specs/active/plan-2026-10-22-squaremath-domain.md
delegate: squaremath-implementation
labels: []
dependencies:
  - type: blocks
    target: is-01m5j10r3f4dms3f0mgkphr7fe
parent_id: is-01m5j0rns0p8gq9rrn3wnns7p1
child_order_hints:
  - is-01m5j6xtx90b07z09cavtqdgw4
  - is-01m5j79r46k1ez04dzq3arz7zv
hold: null
hold_until: null
created_at: 2026-10-22T14:42:36.827Z
updated_at: 2026-10-22T16:36:14.622Z
started_at: 2026-10-22T15:44:53.762Z
---
Implement canonical squaremath.org site URLs, explicit legacy profile aliases, live changelog targets, and regressions per plan. Include the required site release-impact disposition for published SYNOPSIS.md/development.md documentation inputs; pre-push reports these pending at current v0.9.0. Preserve github.com/jlevy/squares repository links in PDFs. Plan and guide staged on codex/squaremath-domain.

## Notes

PR #727 https://github.com/jlevy/squares/pull/727, head 73a28c47fb0499999fb1a9b9e8baad78a6589215. Canonical migration, explicit legacy compatibility, publication editions and runbook implemented. Full publication build and assembled audit7333/7333 passed; all67 pre-push prerequisites passed. Reachable normal phase timed out900s then completed rerun846s with12168pass7fail; all7 were stale domain fixtures corrected73a28c47f, full affected file133passed. Remaining pool phase23passed65.85s. Earlier focused64/30/133 suites and Node PDF links passed. Astra initial review only Low plan-status A1, corrected in same commit and delta cleared; formal follow-up pending. Hosted final-head CI running; prior Pages workflow passed and shardC had exactly same7 fixture failures. Owner domain verification confirmed and TXT resolves locally. Production cname still null, routing unchanged; cutover waits final CI, then coordinated owner DNS, HTTPS and redirects. Child881e review disposition and zd14 CI confirmation pending.
