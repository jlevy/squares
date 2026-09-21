---
type: is
id: is-01m32htnew2y6jw2qrqfbh9j55
title: Collapse the empty badge row so the OPEN heading holds its position
kind: bug
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
created_at: 2026-09-21T17:57:09.209Z
updated_at: 2026-09-21T18:09:27.582Z
closed_at: 2026-09-21T18:09:27.580Z
close_reason: Badges take the star line's top when there is no star; head-open unchanged at 546px.
resolution: null
duplicate_of: null
---
In the facts panel, the PROVEN badge row (`.badges`, `assets/workbench.css:482`) is absolutely positioned at top 478px with a fixed 40px height. When a record establishes no attributes the row renders empty, leaving a blank band above where it would have been.

Two requirements from the owner:
- No blank space above the badge line when that line is not present.
- The OPEN heading sits at a fixed position either way.

`.head-open` is already absolute at top 546px, so it does not move today -- the visible fault is the empty band, and the fix must not introduce movement in the heading while removing it. Confirm against an n whose record carries no proven attributes.
