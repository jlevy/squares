---
type: is
id: is-01m4c4x8d0nc0gdmp7qxd32dgz
title: "PR421 A1: scope confirmation citations to the bound actually certified"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: codex@17e132e9b179
labels: []
dependencies: []
parent_id: is-01m4bvqnk2d26b8ydnvt3h07n1
hold: null
hold_until: null
created_at: 2026-10-07T21:39:28.800Z
updated_at: 2026-10-07T21:39:51.738Z
started_at: 2026-10-07T21:39:51.738Z
---
Senior review A at e64676d5 identifies all12 newreported bounds erroneously marked confirmed by olderweaker T098/T113/T101. Preserve oldverified records; include oldcert evidence in reported-value citation onlyifdeclaredprecisionboundsagree, preserve applicableconstruction evidence. Regeneratecitationview and add all12mismatch and genuinesamebound controls. Fix lowerreportedlayer, replay scopedinputs, push and getA1 strongfollowup atnewhead. Root publishedformalreview; engineeringownerrepair_followup_import.
