---
type: is
id: is-01m0tzvgynrmw5v2227200by2b
title: "PR 24 review R2: make phase contract resumable and truthful"
kind: bug
status: closed
priority: 1
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - pr24-review
dependencies: []
parent_id: is-01m0tz8s4yps8zgqwk8cng9qnx
created_at: 2026-08-24T22:56:58.324Z
updated_at: 2026-08-24T23:24:48.335Z
closed_at: 2026-08-24T23:24:48.334Z
close_reason: "Fixed in 0775c20: v2 phases now record provenance, expected output, validation, kill/fallback, start/deadline; active and terminal fields are conditionally checked."
resolution: null
duplicate_of: null
---
PR #24 docs promise per-phase output/check/kill/fallback/clock, but agent-session.schema.yaml lacks those fields and requires placeholder outcome/evidence while active. Add a minimal declared slice contract and real time anchor; condition terminal evidence correctly.
