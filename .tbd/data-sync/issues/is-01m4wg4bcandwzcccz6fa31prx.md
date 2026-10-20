---
type: is
id: is-01m4wg4bcandwzcccz6fa31prx
title: Navigate directly from the profiles overview to person pages
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4kvnfe7f9nak96hc7bgdwer
hold: null
hold_until: null
created_at: 2026-10-14T06:03:26.473Z
updated_at: 2026-10-14T06:06:13.386Z
started_at: 2026-10-14T06:03:43.007Z
closed_at: 2026-10-14T06:06:13.385Z
close_reason: Requested navigation implemented and verified in live local browser; automated browser run blocked by external scratch ENOSPC, recorded in notes.
resolution: null
duplicate_of: null
---
Owner requests native navigation from the profiles directory to individual pages instead of opening a popover. Retain contextual credit popovers on result surfaces. Update existing browser checks and design documentation, rebuild local preview.

## Notes

Implemented direct directory anchors; contextual result/case popovers retained. Updated design guide and existing regression coverage. Renderer test passed; automated browser fixtures failed ENOSPC before test execution. Live local browser verified Profiles -> Manasseh Ahmed standalone URL -> Profiles breadcrumb return. Ruff lint passed, formatting applied. Local preview8790 rebuilt for directory; committed locally, not yet pushed.
