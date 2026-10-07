---
type: is
id: is-01m4aj1fjtr7gaa8x3p76rr12r
title: "OR18: guard new branch and staged Git blob storage"
kind: task
status: in_progress
priority: 1
version: 2
delegate: guzhou-codex-graph-gate
labels: []
dependencies: []
parent_id: is-01m44m1c47h22mb1g0kzppc54q
hold: null
hold_until: null
created_at: 2026-10-07T06:50:29.849Z
updated_at: 2026-10-07T06:50:31.171Z
started_at: 2026-10-07T06:50:31.170Z
---
Scoped added-storage sub-slice only: explicit PR base/head, all newly reachable historical blob objects plus tip/index reintroductions, dedup; proposed5MiB/blob20MiB total; no scanner or proof-input runtime binding changes, no math target. Tiny Git controls and CI gate. Local contract control/OCT07_B_PLAN.md; source/checks under current Guzhou9h authorization.
