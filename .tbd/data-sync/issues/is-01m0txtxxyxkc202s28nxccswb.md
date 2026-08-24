---
type: is
id: is-01m0txtxxyxkc202s28nxccswb
title: Synchronize the synopsis gate-defect enumeration
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
created_at: 2026-08-24T22:21:41.693Z
updated_at: 2026-08-24T22:31:45.738Z
closed_at: 2026-08-24T22:31:45.737Z
close_reason: D-200 removed the duplicate synopsis enumeration; D-201 synchronized both mutation anchors and expected diagnostics. Derived counts and the complete negative-control suite are the checkpoint criteria.
resolution: null
duplicate_of: null
---
The synopsis aggregate correctly says nine defects were gate-detected after D-198, but the explanatory sentence still says eight and its explicit list omits D-198. Record this as D-200, update the complete enumeration together with D-199's new aggregate, and strengthen the existing synopsis mutation anchor so the count and list cannot drift silently.

## Notes

D-200 recorded. The duplicate id enumeration is removed rather than adding another drifting authority; the existing derived aggregate and mutation control remain the enforced surface.
