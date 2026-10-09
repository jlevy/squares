---
type: is
id: is-01m4er1sp28wpk94dg47yct64v
title: "n17 stack A1: qualify current heads with required CI and full checkpoint"
kind: task
status: in_progress
priority: 1
version: 17
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: claude-code@vm
labels:
  - n-17
dependencies:
  - type: blocks
    target: is-01m4fhz39j0nmrca9x38tyrnsg
parent_id: is-01m4eq9mdaejkedd1b09qqn09p
hold: null
hold_until: null
created_at: 2026-10-08T21:52:29.377Z
updated_at: 2026-10-09T08:32:28.598Z
started_at: 2026-10-08T22:00:55.817Z
---
A1 remains open. Propagate #404 commit 1af586ef43446655dfe0401902a096042526dd0a through #454 at 1b1c0945 and #461 at 79ebfd59; apply the scoped equivalent to standalone #464 at 51368bec. Root Packing 37891105634, Pages 37891105643 and mergeability 37891099687 pass. A published follow-up covering the root repair and complete research checkpoints remain open. The other three latest Packing runs fail only the three source-copy assertions; do not rerun unchanged sources. Preserve the 192 MiB cap, scientific inputs and all proof/resource ceilings. Root worker selection is 199,926,018 bytes; broad local push remains failed/interrupted and unqualified. Qualify changed sources once, using direct-branch full dispatch and blank pull_request where exposed; verify checkout and main ancestry. Supporting #452/#453 need no repeat run at unchanged source/base. The older 224 MiB proposal is unapplied and is not the selected remedy. https://github.com/jlevy/squares/issues/405

## Notes

2026-10-09 08:40 UTC takeover by claude-code@vm per the explicit handoff. Plan changed: instead of propagating 1af586ef through #454/#461 and qualifying three layers, the stack is folded into #404 (see think-rdd5). Measured folded tree 200,420,648 bytes < 201,326,592 cap.
