---
type: is
id: is-01m0ttfx53tjv841cn2v2anyf2
title: Standardize packing CLIs and replace ambiguous entry-point names
kind: task
status: open
priority: 1
version: 5
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels:
  - engineering-maturity
  - cli
dependencies:
  - type: blocks
    target: is-01m0ttg3v5303w5k65gc8th28m
  - type: blocks
    target: is-01m0ttgbpts9xfvqz0wck4781q
  - type: blocks
    target: is-01m0tth2dgvwnagwh2975ac6k3
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T21:23:14.721Z
updated_at: 2026-08-24T21:24:53.040Z
---
Inventory maintained command surfaces and give each a descriptive name, typed argument boundary, self-contained help, explicit inputs, outputs, side effects, evidence tier, and examples. Define consistent meanings for check, verify, replay, render, run, and update. Keep command adapters thin over one programmatic implementation; provide structured JSON or JSONL where automation consumes data, route diagnostics to stderr, and test partial failures and exit codes. Update repository-owned callers together rather than retaining aliases with no external consumer.

## Notes

Coordinate campaign command changes with think-ldq2; CLI cleanup must not create a second lifecycle or validation contract.
