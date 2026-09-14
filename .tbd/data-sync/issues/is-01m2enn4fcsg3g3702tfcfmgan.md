---
type: is
id: is-01m2enn4fcsg3g3702tfcfmgan
title: Verify separate native usage accounts for X030 and X031 documentation PRs
kind: task
status: open
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
refs:
  - kind: pr
    url: https://github.com/jlevy/squares/pull/165
    at: 2026-09-14T00:59:35.309Z
  - kind: pr
    url: https://github.com/jlevy/squares/pull/166
    at: 2026-09-14T00:59:35.310Z
labels:
  - n11
  - cost
  - pr
dependencies:
  - type: blocks
    target: is-01m2eddtqbpv11d9g5yk0s8cv0
parent_id: is-01m2eddtqbpv11d9g5yk0s8cv0
created_at: 2026-09-14T00:39:13.643Z
updated_at: 2026-09-14T00:59:35.310Z
---
For PR #165 X030 and its separately stacked X031 child, derive disjoint branch-attributable agent-time/model/token intervals from native task data if available. Exclude PR #156, #157, T1, T2 geometry, H161, reader admission, and shared coordinator overlap. Reconcile actual branch heads and update the cost-first PR bodies with verified numbers or an explicit documented inability to attribute them. Do not invent a token total from active time or double count shared work.
