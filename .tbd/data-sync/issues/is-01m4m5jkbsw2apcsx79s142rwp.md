---
type: is
id: is-01m4m5jkbsw2apcsx79s142rwp
title: Match Row reference outline width to the packing container
kind: bug
status: in_progress
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-11T00:25:03.608Z
updated_at: 2026-10-11T01:04:51.674Z
started_at: 2026-10-11T00:26:04.036Z
---
The gray web Row reference uses a fixed1px border and the comparison SVG uses a heavier stroke. Use the same normalized renderer stroke and Row scaling as the black packing container, preserving frame size and bottom-left alignment. Verify shared Home/Atlas styles and the separate Row comparison.

## Notes

Gray reference uses z-index 0 behind packing z-index 1 in isolated tiles on Home and Atlas. Renderer-normalized stroke width and bottom-left alignment preserved. Three web/print regression checks passed (row-layering-final.log); independent Astra review E approved. Implemented in e047478b8; final PR head 53c8d37a2 adds formatting only. Awaiting matching final CI.
