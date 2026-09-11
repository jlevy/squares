---
type: is
id: is-01m27jp30839zqz4xabt5echwc
title: "The stage reads brighter than the PDF at the same hex: area, not palette"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-11T06:32:38.151Z
updated_at: 2026-09-11T06:32:38.151Z
---
The owner reports the workbench still looks brighter than the PDF export. The numbers say they are identical, so what is left is a display question and the fix is a choice rather than a correction.

The chain, measured at every link:
  * the PDF's content streams carry #257260, #4b9582, #36816e, #dd87b8 ... (FlateDecode streams, 'rg' operators, DeviceRGB)
  * the SVG renderings carry the same hexes
  * the workbench's resting frame paints the same hexes — pixel census of a 940px render of n = 17 side by side: #4b9582, #dd87b8, #5fa995, #257260, #3fa8f1 on both halves

Two effects remain, both real and neither a data difference:
1. AREA. The workbench draws one packing filling the stage; the atlas draws a grid of small panels. The same fill over a patch three times larger reads as markedly more saturated. This is the larger of the two.
2. COLOUR MANAGEMENT. The PDF is DeviceRGB with no ICC profile, so a viewer renders it through the display profile as generic RGB; on a wide-gamut display that is duller than the same numbers tagged sRGB in a browser.

So 'match the SVGs' and 'look like the PDF' are in tension, and the tension is the size. If the owner wants the stage toned, the honest way is a declared chroma trim on the RESTING fills — a stage presentation setting, defaulting to the exact atlas values — rather than changing the palette, which would break the byte match the exported still depends on.

Needs the owner's call: exact match (today), or a trim, and at what fraction.
