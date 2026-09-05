---
type: is
id: is-01m1stehah9y66xvcdapvvytyf
title: "Explainer: three mobile legibility gaps below the touch-action fix"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-05T22:18:57.233Z
updated_at: 2026-09-05T22:18:57.233Z
---
Measured 2026-09-05 at 390x844 and 360x800. The touch-action bug from the same audit is fixed; these three are what remain.

1. SVG figure labels fall to 9.5-11 CSS px. The number line (viewBox 0 0 700 92) renders at 323x42 and the coarsening chart (0 0 700 250) at 323x115, a uniform 0.46x with no mobile layout switch, so 'Stromquist 2003', 'Trump 1979 packing' and the chart footnote land at 9.5px, axis ticks and bar values at 10-10.5px, and '381/100 = 3.81, proved below' at 11px, directly under a 17.1px caption.

2. Interactive controls are under 44px: buttons 34px tall, header chips 28px, range sliders 16px. 22 of 24 non-prose controls miss 44 in at least one dimension. The atom figure's own hit regions are a separate matter and not fixable by sizing -- a 1px scan of the 339x339 canvas found 353 regions, median 5x5 px, only 9.7% of the canvas a hit at all.

3. Display math scrolls correctly in its own container and the full width is reachable (max scrollLeft equals the overflow exactly, so the centred-overflow trap does not bite) but there is no fade, mask or persistent scrollbar. Worst case at 390: 655px of content in a 358px box, 45% off-screen, with tau*(L,B) stopping mid-glyph at the margin.
