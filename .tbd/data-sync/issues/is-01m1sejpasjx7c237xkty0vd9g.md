---
type: is
id: is-01m1sejpasjx7c237xkty0vd9g
title: Remove non-scaling-stroke from the shared packing renderer and the T-018 visual
kind: task
status: open
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T18:51:30.520Z
updated_at: 2026-09-05T21:39:04.251Z
---
D-457 removed vector-effect=non-scaling-stroke from the composite atlas. The same attribute is still emitted by sqpack/render/style.py presentation_attributes, sqpack/render/packing.py and devtools/render_t018_proof_visual.py. It is inert under cairosvg (measured identical at scale 1, 2 and 4) and wrong under any browser, which resolves it against display size. Removing it touches every retained case rendering, so it is its own change with its own regeneration and drift check.

## Notes

Measured 2026-09-05 before the merge, and deliberately NOT done on this branch.

In packing/atlas/known-best/rendering/n-011.svg -- the file the explainer inlines as Figure 2 -- every stroked element carries the attribute and every one of them is stroke-width 1.25 (11 polygons and 1 rect). So within that figure there is no unevenness for the removal to fix; only an overall weight difference between Chromium (which honours it, holding 1.25 device px through the page's downscale) and cairosvg (which ignores it). That is real but subtle, and nobody has reported seeing it.

Against that: the 100 rendered SVGs feed known-best-1-100.svg, whose current appearance the user explicitly approved ('Actually, the first one you have now looks the best. It matches the weight'). Removing the attribute at the source would regenerate all 100 renderings plus the composite SVG, PNG, PDF and @2x, changing the figure that was just signed off. That is its own change with its own before/after, not a rider on a branch about to ship.

Do it on its own branch, with the composite regenerated and compared to what is committed now.
