---
type: is
id: is-01m4whgqb9hc2tmad1p1nmr7x7
title: Update the atlas tab-group contract for the new drawing chooser
kind: bug
status: closed
priority: 2
version: 3
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wcjctchxg9qv8jp0za5g13
hold: null
hold_until: null
created_at: 2026-10-14T06:27:40.520Z
updated_at: 2026-10-14T07:21:25.609Z
started_at: 2026-10-14T06:28:04.068Z
closed_at: 2026-10-14T07:21:25.609Z
close_reason: Fixed, independently reviewed, and merged in regularization stack main9f48ccc80cee8dcf94c7cadbcaded01408f94fa2; exact-head Packing and Pages CI pass. Deployment tracked by parent think-azzv.
resolution: null
duplicate_of: null
---
Hosted PR591 Packing suite-b onlyfailure: test_overview_sections atlas preview expects8tabs, but Regularized|Original adds2. Update this existing static contract to account for the approved chooser without dropping checks of324cases/canonicalrows/defaults.
