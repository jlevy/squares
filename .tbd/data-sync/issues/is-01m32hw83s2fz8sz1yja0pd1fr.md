---
type: is
id: is-01m32hw83s2fz8sz1yja0pd1fr
title: "Colour transitions dip through grey: mix lerps OKLab rectangularly, not polar OKLCH"
kind: bug
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
created_at: 2026-09-21T17:58:01.076Z
updated_at: 2026-09-21T18:13:16.639Z
closed_at: 2026-09-21T18:13:16.638Z
close_reason: mix interpolates polar OKLCH with shortest-arc hue; both tests verified by mutation.
resolution: null
duplicate_of: null
---
Squares flicker chromatically as they change colour. The owner's guess was RGB interpolation; the cause is close to that in spirit but one space over.

`mix()` in `packages/workbench/src/view/colour.ts:264` converts both endpoints to OKLab and lerps the three RECTANGULAR coordinates (L, a, b) independently. The palette itself is built polar, through `oklchHex(L, C, h)`, so every colour the page uses has a well-defined hue and chroma -- and then mixing throws that away.

A straight line between two points in the a-b plane is a chord, and a chord passes nearer the neutral axis than either endpoint. The further apart the two hues, the deeper the chroma dip in the middle. That dip is the flash.

The worst case is the one that shows most: `colour.ts:568` mixes a green fill toward `scarletFill` for the newly placed square. Green to scarlet is roughly a half turn of hue, so the chord passes very near grey and the new square desaturates to something muddy on its way in, then saturates again. `colour.ts:559` mixes a moving shade toward a settled shade through the same path.

Fix: interpolate polar. Lerp L, lerp C, and lerp hue along the SHORTEST arc, then go back through `oklchHex`, which already gamut-maps by bisection. Chroma then stays up across the whole transition and there is no grey mid-point.

Two things to watch:
- Shortest-arc hue needs the wrap handled, or a mix crossing 0/360 travels the long way round -- which is the same artifact with a different shape.
- `rampFill` at `colour.ts:447` already lerps the three OKLCH components and feeds `oklchHex`, which is the polar form done right. That is the shape `mix` should take.

Separately worth checking once mixing is polar: `desaturate()` drains chroma during the move and `chromaLevel` restores it over the settle, so there are two chroma schedules running. If the flicker survives the polar fix, they are stacking.
