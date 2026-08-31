---
type: is
id: is-01m12tqnvbtc7z2a1rjgs0svwj
title: "Composite: small grey text needs a genuinely heavier weight"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-08-28T00:01:24.842Z
updated_at: 2026-08-28T00:01:24.842Z
---
The s-bound and degree labels were set to font-weight 500 but still render at regular. Source Sans 3 is not installed locally so the stack falls back to a family whose 500 maps to 400. Raise to 560 so renderers round to the semibold face.
