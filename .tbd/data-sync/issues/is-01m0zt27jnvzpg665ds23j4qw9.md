---
type: is
id: is-01m0zt27jnvzpg665ds23j4qw9
title: Standardize time-sliced experiment-loop startup guidance
kind: task
status: in_progress
priority: 2
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-26-overnight-constructive-enumeration.md
labels:
  - packing
dependencies: []
parent_id: is-01m0ypc5cd4z6ktb1vejj1td3n
created_at: 2026-08-26T19:51:58.804Z
updated_at: 2026-08-26T23:19:47.936Z
---
Update the authoritative experiment-loop and agent-startup guidance so every new agent begins with an explicit bounded plan, works in slices of at most 30 minutes, targets an integration checkpoint around four hours, reassesses elapsed time and the remaining critical path at each boundary, and delegates genuinely independent work to sub-agents when slots are available. Keep the guidance general, concise, and compatible with existing W1-W7 workflow entry contracts; regenerate any dependent document map or synopsis views.

## Notes

Implemented in AGENTS.md, the authoritative and mirrored experiment-loop skills, campaign README, and agent-session README: fixed roughly four-hour checkpoints, <=30-minute slices, measured re-estimation, protected finalization reserve, independent sub-agent delegation, and one integration owner. Mirror and skill checks pass. Leave open with the parent until the PR 45 strict/CI continuation closes.
