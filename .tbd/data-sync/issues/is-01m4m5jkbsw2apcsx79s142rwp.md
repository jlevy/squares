---
type: is
id: is-01m4m5jkbsw2apcsx79s142rwp
title: Match Row reference outline width to the packing container
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-11T00:25:03.608Z
updated_at: 2026-10-11T00:38:42.982Z
started_at: 2026-10-11T00:26:04.036Z
---
The gray web Row reference uses a fixed1px border and the comparison SVG uses a heavier stroke. Use the same normalized renderer stroke and Row scaling as the black packing container, preserving frame size and bottom-left alignment. Verify shared Home/Atlas styles and the separate Row comparison.

## Notes

Native SVG reference now shares black container centerline/stroke width; n19 left/bottom alignment passes on both web surfaces. Two browser nodes passed30.48s, five earlier nodes passed; unit stroke checks passed. Separate324Row comparison regenerated without canonical PDF changes.
