---
type: is
id: is-01m1sc1enh7zkd3mqr1h157djj
title: "Explainer PDF: main serif text sets too wide and unevenly"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T18:07:08.465Z
updated_at: 2026-09-05T18:39:04.750Z
closed_at: 2026-09-05T18:39:04.750Z
close_reason: "Not justification and not a mixed font: Chromium rounds every glyph advance to a whole CSS pixel, and 11pt is the worst size in the 9-14pt range. Integer share of glyph moves in the PDF fell from 98.44% to 6.50% with text-rendering: geometricPrecision under print."
resolution: null
duplicate_of: null
---
The printed body text reads loose and irregular. Leading hypotheses: the LocalPunct font sits ahead of PT Serif in the stack so a line may mix two faces, and kpress's print stylesheet justifies p/li/blockquote while headless Chromium has no hyphenation dictionaries. Our ragged-right override wins on p but may miss other elements. Under forensics.
