---
type: is
id: is-01m12w4vjhak6vaz2zkgwfbkqc
title: "Composite: settle on Helvetica, drop the webfont idea"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-08-28T00:26:05.264Z
updated_at: 2026-08-28T00:26:05.264Z
---
The font stack named Source Sans 3 first, but it is not installed, so cairo resolved Helvetica through CoreText and the PNG/PDF appearance was host-dependent. Google Fonts was considered and rejected: cairosvg has no webfont support at all, so hotlinking would have meant switching the export to headless Chrome and taking a build-time network dependency in a repo that archives every source locally. Stack is now Helvetica, Arial, sans-serif -- Arial being metric-compatible where Helvetica is absent -- and no webfont is referenced. Note Helvetica exposes only regular and bold here: any weight from 560 up resolves to bold, so small labels stay regular and gain legibility from a darker grey instead.
