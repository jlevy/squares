---
type: is
id: is-01m0ttfnkek9mx0kv3rgqjth3r
title: Define and enforce packing module boundaries
kind: feature
status: closed
priority: 1
version: 5
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels:
  - engineering-maturity
  - architecture
dependencies:
  - type: blocks
    target: is-01m0ttgkhcyks8na3prg20kk8c
  - type: blocks
    target: is-01m0ttgtaj1j5rp28wxw84v4wr
  - type: blocks
    target: is-01m0tth2dgvwnagwh2975ac6k3
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T21:23:06.989Z
updated_at: 2026-08-24T22:55:28.140Z
closed_at: 2026-08-24T22:55:28.139Z
close_reason: Implemented and documented one-way maintained, research, campaign, CLI, case, developer-tool, and benchmark boundaries; architecture tests reject old locations and reverse imports; complete validation passed.
resolution: null
duplicate_of: null
---
Implement the reviewed module structure for shared packing foundations, stable research-loop machinery, explicit case modules, command entry points, and scratch work. Enforce the dependency direction case to loop to foundation; shared modules may not import a named packing, hypothesis, campaign round, or value of n. Keep one Python distribution unless the inventory demonstrates a real packaging boundary. Move callers, tests, and docs together without compatibility aliases for repository-owned imports. Acceptance: imports and ownership match the documented map, reusable layers contain no case-specific policy, and focused plus full validation remain green.
