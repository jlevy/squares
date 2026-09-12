---
type: is
id: is-01m2ag6b030mv58gf58yyka1as
title: Reconcile the BC329 runner source lock with the published T-026 claim
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - tooling
dependencies: []
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T09:46:48.180Z
updated_at: 2026-09-12T09:46:48.180Z
---
The unfinished fixed_core_packet.py pins T-026 blob e12789cd with SHA fe786eff, while PR148 head 989fd544 carries the published T-026 limit blob baeb8c43 and standalone-claim SHA 04fd6bbc. The observed diff is endpoint_status prose; mathematical fields and the T-025 input appear unchanged. Rebase the runner onto the publication stack, independently compare all consumed mathematical fields, update the source/revision lock deliberately, add or retain a refusal control for unexpected source drift, and leave a clean committed branch. Do not weaken or bypass the source binding and do not register or run BC329 until this and the parent admission are complete.
