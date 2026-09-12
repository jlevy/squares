---
type: is
id: is-01m2aqpewzn7a55te03bfefzr7
title: Make interval refutation outrank speculative tail failures
kind: bug
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - tooling
dependencies: []
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T11:57:56.510Z
updated_at: 2026-09-12T16:11:31.578Z
closed_at: 2026-09-12T16:11:31.578Z
close_reason: Implemented, integrated, independently reviewed, and published on the clean PR 156 stack by f1e397cd. Their remaining follow-up risks are separately tracked under calibration, parent preflight, partial-direction integration, and admission beads; no BC329 scientific target ran.
resolution: null
duplicate_of: null
---
The bounded completion-order interval scheduler drains all futures in a landed batch. If the batch contains an earlier-in-net refutation and an exception at a speculative index beyond that new cutoff, it currently raises the irrelevant tail exception, making the result schedule-dependent; the prior net-order path would retain the refuting prefix. Define deterministic precedence so an accepted earlier cutoff cancels and ignores failures strictly beyond it while failures at or before the retained prefix remain errors. Add controlled-batch tests. This does not block BC329's enclose=True complete route, where early refutation is disabled, but it is a real shared-scheduler contract gap.
