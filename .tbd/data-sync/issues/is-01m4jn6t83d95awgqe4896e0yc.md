---
type: is
id: is-01m4jn6t83d95awgqe4896e0yc
title: Align web atlas layout goldens with approved asymmetric compact gaps
kind: bug
status: in_progress
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4h9s465x7mphy1xxkmdyqc9
hold: null
hold_until: null
created_at: 2026-10-10T10:19:45.766Z
updated_at: 2026-10-10T10:26:07.300Z
started_at: 2026-10-10T10:20:31.804Z
---
Ha739 delta gate exposed 18 site_atlas_views assertions: initial Small capacity remains expected15 but new20percent horizontal gap yields16; uniform-height check incorrectly equates vertical and horizontal gap after independent25percent vertical tightening. Inspect actual renderer contracts and fix exact stale expectations without weakening reserved size, common heights, complete rows, right alignment, segment gaps or measured ratio acceptance. Root owns source publication and tracking.

## Notes

Exact stale expectations identified: initial Small placement capacity15 should be16 after approved tighter horizontal spacing; settled capacity remains15. Uniform row geometry should compare measured vertical distance with computed row_gap_px, not independently sized horizontal gap_px. Only two test assertions changed; same tolerances, uniform height/pitch, full row bounds/right edges, drawing scale, segment separation and0.8/0.75 measured ratios retained. Focused/full-file serial qualification pending.
