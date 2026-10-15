---
type: is
id: is-01m4zh3apr6q86jmjggvd08bhr
title: Keep site release checks within component-owned validation
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
hold: null
hold_until: null
created_at: 2026-10-15T10:18:04.887Z
updated_at: 2026-10-15T10:20:56.537Z
started_at: 2026-10-15T10:20:56.536Z
---
A site release cut currently schedules the same cross-component pytest list as infographic/paper cuts, including whole-atlas composites and exhaustive proof sweeps. A manual invocation during PR617 integration entered unchanged exhaustive_exact cases; it was interrupted and a focused release/date/claim selection retained. Make cut_release validation component-aware and use the shared quick-tier predicate for ordinary cut iteration, with deeper evidence selected explicitly at the owning checkpoint. Preserve every scientific assertion and full checkpoint obligation; prove selection identities and component ownership without duplicating expensive runs.
