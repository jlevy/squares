---
type: is
id: is-01m5k5w1hs929afqh5mzmf071t
title: Restore case popover header controls, math pager and responsive visual width
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: navigation-components
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T01:26:40.440Z
updated_at: 2026-10-23T01:33:51.471Z
started_at: 2026-10-23T01:27:20.756Z
---
Keep case popover expand/close controls in the upper-right independently of previous/next pager links. Render pager n labels using existing mathematical notation. Let the packing visual use the available popover content width with preserved aspect ratio and no mobile overflow. Preserve canonical case URLs and full-page behavior. Validate real n=5 at desktop/mobile and safely refresh Atlas/case leaves and shared assets; coordinator commits/builds.

## Notes

Additional user refinement included: News Reset stays right-aligned on the SAME row as Topics and Significance at desktop widths; count appears below; narrow layouts wrap without overflow. Runtime source checkpoint sent to coordinator. Original n5 regression reproduced at1280: controls_top74.59 instead of46.6 due sticky offset including28px panel padding. Diagram caps288/224px confirmed desktop/mobile. Fix subtracts padding from sticky inset; fetched diagram uses full content track; canonical page remains compact.
