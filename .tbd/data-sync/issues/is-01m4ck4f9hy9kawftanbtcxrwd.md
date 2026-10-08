---
type: is
id: is-01m4ck4f9hy9kawftanbtcxrwd
title: "C4: preserve prepared math metrics for stored reader font preferences"
kind: bug
status: in_progress
priority: 1
version: 3
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4cecqqmt13gys8265mpra32
hold: null
hold_until: null
created_at: 2026-10-08T01:48:05.297Z
updated_at: 2026-10-08T11:19:55.047Z
started_at: 2026-10-08T01:49:34.126Z
---
Independent Astra review reproduced saved kpress.proseFont=sans selecting sans prose with serif prepared math, and kpress.fontSet=system selecting KaTeX glyphs with KPress metrics. Prepare compatible prepaint visual profiles while preserving one semantic subtree and the global 2MB bound.
