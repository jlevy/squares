---
type: is
id: is-01m4jn6t83d95awgqe4896e0yc
title: Align web atlas layout goldens with approved asymmetric compact gaps
kind: bug
status: in_progress
priority: 1
version: 4
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4h9s465x7mphy1xxkmdyqc9
hold: null
hold_until: null
created_at: 2026-10-10T10:19:45.766Z
updated_at: 2026-10-10T10:40:25.494Z
started_at: 2026-10-10T10:20:31.804Z
---
Ha739 delta gate exposed 18 site_atlas_views assertions: initial Small capacity remains expected15 but new20percent horizontal gap yields16; uniform-height check incorrectly equates vertical and horizontal gap after independent25percent vertical tightening. Inspect actual renderer contracts and fix exact stale expectations without weakening reserved size, common heights, complete rows, right alignment, segment gaps or measured ratio acceptance. Root owns source publication and tracking.

## Notes

Exact stale expectations identified: initial Small placement capacity15 should be16 after approved tighter horizontal spacing; settled capacity remains15. Uniform row geometry should compare measured vertical distance with computed row_gap_px, not independently sized horizontal gap_px. Only two test assertions changed; same tolerances, uniform height/pitch, full row bounds/right edges, drawing scale, segment separation and0.8/0.75 measured ratios retained. Focused/full-file serial qualification pending.

Committed exact reviewed fixes at d83b7c03d92a3f1853c479f45fabb07cb289aa97. Focused serial selection passed116 tests in224.38s, zero failures/errors/skips, including all web atlas cases and four timeout/custody controls. Ruff, formatting and targeted BasedPyright pass with zero findings. Independent senior I and correctness J supplementary inspections report no findings; formal reviews held for publication. Current repair-delta pre-push selects113 files from basea739, explicit jobs8/inner1 gives three pytest workers without deadline or acceptance changes. Final actual hosted qualification still pending; do not close prematurely.
