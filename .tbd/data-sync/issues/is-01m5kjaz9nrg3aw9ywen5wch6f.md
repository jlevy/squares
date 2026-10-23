---
type: is
id: is-01m5kjaz9nrg3aw9ywen5wch6f
title: "Atlas triangle follows the page scroll: Large at the top, then Medium, Small and a pan along the left edge"
kind: feature
status: closed
priority: 2
version: 4
delegate: claude-code@spud10.local
labels:
  - site
  - atlas
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-23T05:04:32.551Z
updated_at: 2026-10-23T17:56:45.586Z
started_at: 2026-10-23T05:04:36.294Z
closed_at: 2026-10-23T17:56:45.585Z
close_reason: "Merged in PR 746 (cc91ee1b81): the Atlas follows the scroll, with review A's findings fixed and the owner's 23 October site requests."
resolution: null
duplicate_of: null
---
Owner request 2026-10-22. On the homepage preview and atlas.html, an untouched Triangle reached by scrolling down from the top of the page starts at Large. As the row at the reader's focus line grows wider than the screen, the size steps to Medium, then Small; past that the triangle's horizontal scroller pans so the left end of the focus row stays in view. It reuses the existing size tabs and the existing horizontal scroller and animates every size change with the existing FLIP move. A size or view choice, a manual horizontal pan, or a jump to a tile ends the following for the page view and leaves the reader's state alone. A fragment, an explicit size, Grid or an embedded view never starts it.

## Notes

PR https://github.com/jlevy/squares/pull/746 (head 61e2fc28a): pinned sticky stage, S-curve zoom, spline framing, eased stop to the left edge, diagonal wheel pan; expander removed; choosers 7/8 size.
