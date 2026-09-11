---
type: is
id: is-01m27jbzefkfmzckxvgnh7pghw
title: "Colour: desaturate first, then shift hue; on the way back, hue first, then saturate"
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-11T06:27:06.821Z
updated_at: 2026-09-11T06:32:38.007Z
closed_at: 2026-09-11T06:32:38.006Z
close_reason: "Built and measured: chroma and hue ride separate interlocking curves, so at every instant at most one of the two is moving and the hue always rotates while drained."
resolution: null
duplicate_of: null
---
The drain and the hue crossfade ride the same curve (restLevel), so a square changes chroma and hue at once. The owner wants them staggered so the hue rotation always happens while the square is drained:

  leaving rest   desaturate first, THEN identity hues take over from the atlas hues
  returning      atlas hues take over from identity first, THEN saturate

A hue rotation at full chroma is the jarring part; doing it in the grey makes the change invisible and leaves only the chroma moving where a viewer is looking.

## Notes

Done, in 206a606b. chromaLevel and hueLevel are separate curves cut to interlock: the chroma drains over the first fifth of the move and returns over the last part of the settle; the hue leaves only after the drain is done and returns before the chroma does. Measured at n = 17, one square through the beat: 1.00s chroma 0.080 hue 174.4 (move starts), 1.30s chroma 0.012 hue 176.1 (drained, still teal), 1.60s chroma 0.015 hue 116.1 (rotated, still drained), 2.40s move ends, 2.60s chroma 0.013 hue 175.9 (rotated back, still drained), 2.80s chroma 0.080 hue 174.4 (saturated, at rest).
