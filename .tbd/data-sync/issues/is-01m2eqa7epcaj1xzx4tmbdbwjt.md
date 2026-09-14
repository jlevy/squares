---
type: is
id: is-01m2eqa7epcaj1xzx4tmbdbwjt
title: Verify separate native usage account for H162 preregistration PR
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - cost
  - pr
dependencies:
  - type: blocks
    target: is-01m2eddtqbpv11d9g5yk0s8cv0
parent_id: is-01m2eddtqbpv11d9g5yk0s8cv0
created_at: 2026-09-14T01:08:13.397Z
updated_at: 2026-09-14T01:08:19.047Z
---
For the H-162/exp-160 preregistration branch, derive a branch-exclusive native agent-time/model/token interval from native task records if available. Keep it separate from PRs #156/#157/#161-#166, the BC329 controls, and the future exp-158 target. Report verified numbers with source and exclusions, or an explicit attribution limit in the cost-first PR body. Do not infer token totals from elapsed time or double count shared coordinator work.
