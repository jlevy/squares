---
type: is
id: is-01m32svwep5f1qatwy5hj65zgh
title: Widen the facts column by about 10 per cent, taking it from the gap
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
created_at: 2026-09-21T20:17:37.749Z
updated_at: 2026-09-21T20:17:37.749Z
---
Owner's request: the right-hand portion of the stage -- the gap bar and everything under it -- should have less padding on its left, making the whole column about 10 per cent wider, while still clearing the packing box. The middle of the frame currently wastes space.

Current geometry, in stage pixels (1920x1080): the packing ends at x = 1060 and the facts column starts at x = 1160, per the `.bound-star` comment in `packages/workbench/assets/workbench.css`. The column's own elements sit at `left: 6px` within it.

Moving the column's left edge from 1160 to about 1080 gives roughly 10 per cent more width (760 -> 840). Check the widest content still fits: the chained bound is the binding case, and the CSS notes the widest over the corpus is `10.055385 <= s(101) <= 10.535534`, measured at 643 px against a 694 px column at 38 px type. More width is slack there, but the gap bar and its tick labels also scale and should be re-measured rather than assumed.

Verify in a captured frame at 1920x1080, not just in the browser pane, and check a high-n case where the packing box is at its largest.
