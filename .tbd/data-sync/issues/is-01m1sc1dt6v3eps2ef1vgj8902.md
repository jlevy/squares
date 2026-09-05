---
type: is
id: is-01m1sc1dt6v3eps2ef1vgj8902
title: "Atlas: only the bound number should carry the new-result accent, not the s(n) >= prefix"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T18:07:07.590Z
updated_at: 2026-09-05T18:14:55.059Z
closed_at: 2026-09-05T18:14:55.059Z
close_reason: The accent now colours the numeral alone; s(n) >= keeps the caption grey. The separating space stays in the text rather than becoming a dx advance, measured identical in cairosvg and Chromium. Pinned by test_only_the_bound_numeral_carries_the_new_result_accent.
resolution: null
duplicate_of: null
---
In the 1-100 composite SVG the whole lower-bound line is set in FIRST_PARTY_ACCENT_COLOR on starred cases. The new result is the bound itself, so only the numeral should be red; the s(n) >= prefix stays in the body colour. Affects the SVG, the PNG preview and the PDF.
