---
type: is
id: is-01m1sc1f36v1gqedwhmtat95k8
title: "Explainer PDF: print margins are too wide"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T18:07:08.902Z
updated_at: 2026-09-05T18:39:05.065Z
closed_at: 2026-09-05T18:39:05.065Z
close_reason: 0.70in from kpress's --kpress-print-page-margin, with nothing stacking on top; overridden to 0.55in, measured 0.565in of ink inset, twelve pages to eleven. Below about 0.56in the 708px paragraph cap binds while figures keep widening, so this is as far as it usefully goes.
resolution: null
duplicate_of: null
---
The printed page leaves too much white on all sides. The @page rule takes var(--kpress-print-page-margin) from kpress and the content wrapper adds its own max-width and padding on top. Needs the full chain from paper edge to first text pixel measured, then one value changed.
