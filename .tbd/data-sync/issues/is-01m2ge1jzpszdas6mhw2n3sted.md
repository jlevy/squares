---
type: is
id: is-01m2ge1jzpszdas6mhw2n3sted
title: Make the separator between the stage and the controls draggable
kind: feature
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-14T17:04:41.966Z
updated_at: 2026-09-14T17:04:44.232Z
---
Owner request 2026-09-14: the boundary between the rendered stage and the controls panel becomes a grabbable handle that sets their sizes. Reuse metabrowser's resize handle look (styles.css .resize-handle: 4 px strip, 12 px hit area via ::after, transparent at rest, accent on hover and while dragging, body cursor and user-select none while resizing, hidden in print) and extend its behaviour, which lacks it: pointer events with capture and pointercancel, touch-action none, role=separator with aria-orientation/valuenow/min/max, keyboard arrows (Shift for larger), Home/End, double-click reset, min/max clamping re-applied on window resize, and a persisted size in localStorage. The stage's layout() must honour the chosen size.
