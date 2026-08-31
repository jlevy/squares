---
type: is
id: is-01m0y3tt3prw8terc481327qt6
title: Publish revision-keyed validation receipts across research agents
kind: feature
status: open
priority: 0
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-research-loop-efficiency-infrastructure.md
labels:
  - packing
  - focus-efficiency
  - performance
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-26T04:04:12.533Z
updated_at: 2026-08-26T04:04:12.533Z
---
Eliminate duplicate validation across parent and delegated research work by publishing one reusable receipt per canonical key: source identity, validation surface, platform, worker settings, resolved program, and normalized arguments. Acceptance: one run per key; waiting agents reuse only an exact, fresh receipt; failures propagate without masking; stale or canceled runs cannot satisfy a later key; and a comparable research slice cuts duplicate validation command-seconds by at least 50% with blocked wait at most 30 seconds when the parent has independent work.
