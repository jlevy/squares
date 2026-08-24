---
type: is
id: is-01m0tzvgynrmw5v2227200by2b
title: "PR 24 review R2: make phase contract resumable and truthful"
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - pr24-review
dependencies: []
parent_id: is-01m0tz8s4yps8zgqwk8cng9qnx
created_at: 2026-08-24T22:56:58.324Z
updated_at: 2026-08-24T22:58:06.673Z
---
PR #24 docs promise per-phase output/check/kill/fallback/clock, but agent-session.schema.yaml lacks those fields and requires placeholder outcome/evidence while active. Add a minimal declared slice contract and real time anchor; condition terminal evidence correctly.
