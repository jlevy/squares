---
type: is
id: is-01m4daq6byexd6a1zayqqvdxtg
title: Synchronize case popover collapsed state with native close
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4d2n7hjcxy6nh0wkvy8bpmj
hold: null
hold_until: null
created_at: 2026-10-08T08:40:15.998Z
updated_at: 2026-10-08T08:42:25.349Z
started_at: 2026-10-08T08:42:25.348Z
---
Final full CI37748134343 at a910a0e6 failed one browser contract: after Escape hides #pop-case, a frontier row still has aria-expanded=true. All 3243 other shard-C tests and every deep research/portability job passed. Diagnose native beforetoggle versus queued toggle state/focus handling, correct the source behavior without sleeps or weaker assertions, and add a deterministic regression covering closure and pending fetch invalidation. Preserve source focus semantics and rapid close/reopen behavior. Coordinator owns bead mutations, commits, source pinning, PR updates and final validation.
