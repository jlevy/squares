---
type: is
id: is-01m12tqnvbtc7z2a1rjgs0svwj
title: "Composite: small grey text needs a genuinely heavier weight"
kind: task
status: closed
priority: 3
version: 2
labels: []
dependencies: []
created_at: 2026-08-28T00:01:24.842Z
updated_at: 2026-10-06T08:29:01.731Z
closed_at: 2026-10-06T08:29:01.730Z
close_reason: "Done on main: build_known_best_atlas.py sets the small card labels bold (SUMMARY_SMALL_WEIGHT = 700) over a darker grey, since Helvetica has no semibold."
resolution: null
duplicate_of: null
---
The s-bound and degree labels were set to font-weight 500 but still render at regular. Source Sans 3 is not installed locally so the stack falls back to a family whose 500 maps to 400. Raise to 560 so renderers round to the semibold face.
