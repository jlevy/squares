---
type: is
id: is-01m1ezpew7ra12fkmz6dg4631f
title: "BC-123: profile parent-bound n = 17 parallel speedup"
kind: task
status: closed
priority: 0
version: 7
spec_path: packing/campaign/agendas/agenda-014-mechanism-first-continuation-and-provenance-closure.md
labels:
  - packing
  - agenda-014
  - overnight
dependencies:
  - type: blocks
    target: is-01m1ezq3vt2qxebtra6ddhg78p
parent_id: is-01m1ezp304q3fv8gjahq8n92q2
hold: null
hold_until: null
created_at: 2026-09-01T17:19:00.997Z
updated_at: 2026-09-02T02:30:42.256Z
closed_at: 2026-09-02T02:30:42.254Z
close_reason: "BC-123 completed with a typed contamination stop: retained the exact serial arm, removed the incomplete parallel arm, and left exp-053 unresolved and review-pending."
resolution: null
duplicate_of: null
---
Test exact same-input three-process speedup and deterministic merge guards before authorizing another long n = 17 continuation.

## Notes

Coordinator-only hold: remove only after agenda-013 BC-121 is terminal AND the final PR revision is green.

Resumed: Agenda-013 BC-121 is terminal; terminal revision fa33ea79 and activation revision e7600e83 both passed local and hosted validation.
