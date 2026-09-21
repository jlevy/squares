---
type: is
id: is-01m32szhzvqgp7awv3kd69m95p
title: Shrink the n headline slightly and enlarge the packing box
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
created_at: 2026-09-21T20:19:38.106Z
updated_at: 2026-09-21T20:19:38.106Z
---
Owner's request, two adjustments to the stage:

- The `n = ...` headline below the packing box should be a little smaller in font size.
- The big packing box itself should be slightly larger.

Both are stage geometry in the 1920x1080 poster's own coordinates, under the `--stage-*` tokens in `packages/workbench/assets/workbench.css`. The stage sizes are chosen and measured for video and do not follow the UI scale, and the type scale has a floor because a device scale below one blurs it -- so check the headline stays above that floor.

Interacts with think-sc44, which moves the facts column's left edge inward to about x = 1080: a larger box and a wider column both eat the middle gap, so do them together and measure the result rather than each alone. The box currently ends at x = 1060.

The headline's rolling numerals are positioned by `layoutHeadline`, which measures and sets `--stage-numeral-left` once the faces land, so a size change must be re-measured rather than assumed. Verify in a captured frame at 1920x1080.
