---
type: is
id: is-01m0ttevapnhz0sgm9r09gweew
title: Inventory and classify packing code by maturity and dependency
kind: task
status: closed
priority: 0
version: 7
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels:
  - engineering-maturity
dependencies:
  - type: blocks
    target: is-01m0ttfczkhxs9fqa6kwphy8rx
  - type: blocks
    target: is-01m0ttfnkek9mx0kv3rgqjth3r
  - type: blocks
    target: is-01m0ttfx53tjv841cn2v2anyf2
  - type: blocks
    target: is-01m0tth2dgvwnagwh2975ac6k3
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T21:22:40.084Z
updated_at: 2026-08-24T22:55:26.900Z
closed_at: 2026-08-24T22:55:26.899Z
close_reason: Implemented inventory and maturity map in the plan, development guide, README, and enforced directory layout; the complete 31-step validation gate passed on 2026-08-24.
resolution: null
duplicate_of: null
---
Build the engineering orientation inventory before moving code. Classify every maintained Python and Rust module, shell entry point, command, generator, and campaign subsystem as E0-E3; record its purpose, callers, emitted artifacts, evidence role, expected lifetime, tests, known limitations, and proposed dependency layer. Propose concrete shared-foundation, stable research-loop, case-specific, command, and scratch locations with one-way dependencies. Acceptance: the full tracked code surface is accounted for, ambiguous classifications are explicit decisions, and the inventory identifies cleanup targets without performing file moves.
