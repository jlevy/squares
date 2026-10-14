---
type: is
id: is-01m4xyvc445xv3mc5sc7pt2apv
title: Consolidate single-select and multi-select choosers on the homepage design
kind: bug
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4xwgh6kp2t9j9sy8t5sfztn
hold: null
hold_until: null
created_at: 2026-10-14T19:39:55.383Z
updated_at: 2026-10-14T21:16:32.469Z
started_at: 2026-10-14T19:48:54.913Z
closed_at: 2026-10-14T21:16:32.468Z
close_reason: Delivered in PR604 merge16ea3bd0606c4fae2c343bf11de969301ca0f724. Final-head Packing38634417915/Pages38634417893 passed; deployment38636016372 live audit job116103959611 passed4243of4243checks at that exact revision. Independent reviewsA-H and dispositions are published. Final News has26articles, shared canonicaltopics/compactchoosers, defaultS4/S5, consistentcards/meters, T154/T153/T060highlights; Explanations hasTutorial/Papers/PDFs/Visuals and Film|Workbench; tutorial definitions/anchors preserved, Atlas uncapped withpan. Separate CI and literalcodeglyph follow-ups remain inPR599, without blocking this delivered slice.
resolution: null
duplicate_of: null
---
Replace bespoke News filter button styles with the existing homepage chooser component. Keep single-selection tab semantics and multiple-selection pressed-button semantics while sharing size, spacing, colors, selected/hover/focus states and transitions. Add a retained cross-page computed-style contract and document the shared design rule.
