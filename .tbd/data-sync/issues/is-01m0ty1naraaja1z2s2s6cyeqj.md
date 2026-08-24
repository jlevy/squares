---
type: is
id: is-01m0ty1naraaja1z2s2s6cyeqj
title: Update negative-control diagnostics with the final defect total
kind: bug
status: closed
priority: 1
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - bookkeeping
dependencies: []
parent_id: is-01m0t3n7z9fj0p7wwt1kn4nzqk
created_at: 2026-08-24T22:25:22.262Z
updated_at: 2026-08-24T22:34:42.380Z
closed_at: 2026-08-24T22:31:45.746Z
close_reason: D-200 removed the duplicate synopsis enumeration; D-201 synchronized both mutation anchors and expected diagnostics. Derived counts and the complete negative-control suite are the checkpoint criteria.
resolution: null
duplicate_of: null
---
During the D-199/D-200 integration, controls.yaml advanced both mutation anchors but left their expected checker diagnostics at the pre-edit totals. Record as D-201, update anchor and expected output together after the final count, run all negative controls, and keep the recurrence visible.

## Notes

Follow-up: the first gate after closure showed the gate-aggregate expectation was semantically reversed: mutating 11 to 10 yields a checker diagnostic that the prose is not 11 of 203, not not 10. D-204 tracks the distinct correction; D-201 still records the stale pre-integration totals.
