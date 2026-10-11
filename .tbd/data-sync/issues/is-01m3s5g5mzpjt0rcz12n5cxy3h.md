---
type: is
id: is-01m3s5g5mzpjt0rcz12n5cxy3h
title: Expose bounded progress from long proof replays without granting partial credit
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3qw8b5q2xgjp85cxx24134c
created_at: 2026-09-30T12:44:14.366Z
updated_at: 2026-10-06T08:27:25.626Z
---
The final center and capture replays currently write their detailed receipt only at exit. Process liveness is visible, but phase/step/row progress and estimated remaining work are not, which impedes efficient supervision. Add low-overhead diagnostic progress at completed owner/node boundaries, with wall and CPU accounting separated from acceptance. Progress must never be reusable proof authority; final source rechecks, complete inventories and contradiction/endpoint joins remain required. Preserve frozen in-flight implementations: this follow-up must not restart or delay the current n11 proof jobs. Measure overhead and test timeout/failure reporting with small controls before adoption.
