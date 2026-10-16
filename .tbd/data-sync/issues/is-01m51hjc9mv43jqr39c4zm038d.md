---
type: is
id: is-01m51hjc9mv43jqr39c4zm038d
title: Correct News chooser state colors and tighten article tag spacing
kind: bug
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-16T05:04:46.887Z
updated_at: 2026-10-16T05:05:12.374Z
started_at: 2026-10-16T05:05:12.360Z
---
News filter topic choices should be gray when inactive, use their topic fill when active, and show a pale version of that color on hover, without text underlining or inset selection underlines. Preserve shared compact sizing, wrapping, tallies, focus visibility and transitions. Tighten excess space above/below article tags so title, date, topic metadata and paragraphs follow a consistent rhythm on both homepage and News. Reuse documented design tokens, verify actual browser states in light/dark and desktop/mobile, then review, PR and deploy within the existing authorized News work.
