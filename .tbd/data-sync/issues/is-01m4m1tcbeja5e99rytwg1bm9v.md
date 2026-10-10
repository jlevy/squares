---
type: is
id: is-01m4m1tcbeja5e99rytwg1bm9v
title: Publish the full triangular poster preview with immutable image identity
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T23:19:24.269Z
updated_at: 2026-10-10T23:19:42.022Z
started_at: 2026-10-10T23:19:42.021Z
---
Trace the homepage 324-PDF thumbnail against canonical and served PNG/SVG/PDF bytes. The user requests the full high-resolution triangular poster, not a crop or the separate Row comparison. Preserve the canonical dated PDF destination and avoid regeneration when current artifacts are already correct. Publish a content-identified image so an old same-name browser cache cannot retain the former rectangular poster.
