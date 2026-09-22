---
type: is
id: is-01m32ssx2nkebzvt6mqqrv5b1z
title: Draw the outer container border under the squares, not over them
kind: bug
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m32t2yc3xenfb97kxn844rc7
created_at: 2026-09-21T20:16:32.852Z
updated_at: 2026-09-21T20:21:41.067Z
---
Owner's report: where a packed square meets the container wall, the green outer box's border paints over the square's black border. The black border should win.

Fix the paint order so the container's outline is drawn before the squares rather than after, or lower its z-index equivalently in the SVG/canvas draw order. Check both the Animate scene and the captured SVG frames, since they are separate renderers and only one may be wrong.

Visible at any n whose packing reaches the wall, which is most of them; n = 98 in the cut video is a clear case.
