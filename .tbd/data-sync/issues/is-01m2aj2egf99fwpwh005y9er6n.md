---
type: is
id: is-01m2aj2egf99fwpwh005y9er6n
title: Define and test crash durability for BC329 partial receipts
kind: bug
status: open
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m2aj2ewckram8ww4458w74hr
  - type: blocks
    target: is-01m2aj7q4y8raaw35s0jq3ty2y
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T10:19:37.870Z
updated_at: 2026-09-12T10:22:41.525Z
---
The WIP calls atomic_write_text and describes partial output as durable, but rename atomicity alone does not fsync file content or its directory. State the required crash model. If process or host-crash durability is part of admission, fsync the file and containing directory at declared checkpoints and test the call/order contract; otherwise narrow the claim and acceptance language to atomic process-level retention. Do not advertise durable scientific partials beyond the property actually established.
