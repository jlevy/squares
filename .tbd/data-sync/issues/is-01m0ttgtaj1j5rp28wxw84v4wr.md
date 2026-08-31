---
type: is
id: is-01m0ttgtaj1j5rp28wxw84v4wr
title: Organize retained one-off checks into explicit case modules
kind: task
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels:
  - engineering-maturity
  - architecture
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T21:23:44.593Z
updated_at: 2026-08-24T22:55:28.148Z
closed_at: 2026-08-24T22:55:28.148Z
close_reason: Implemented and documented one-way maintained, research, campaign, CLI, case, developer-tool, and benchmark boundaries; architecture tests reject old locations and reverse imports; complete validation passed.
resolution: null
duplicate_of: null
---
Move retained configuration-, theorem-, source-, hypothesis-, and n-specific code into clearly named case modules, beginning with the Trump, Stromquist, and n=5 surfaces identified by the inventory. Each case must state its narrow question, inputs, evidence tier, retained outputs, limits, and focused self-tests or negative controls. Extract a helper into a shared layer only for a demonstrated common contract and second consumer. Acceptance: agents can distinguish case evidence from reusable mechanisms by path and docs, case modules import shared layers only in the allowed direction, and no generic framework is imposed on isolated mathematical work.
