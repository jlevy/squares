---
type: is
id: is-01m28rbhzfwrfnq9f47pbezxk6
title: The gap bar's scale is two formulas, not a tuned headroom
kind: task
status: closed
priority: 3
version: 2
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-11T17:30:58.926Z
updated_at: 2026-09-11T17:31:08.464Z
closed_at: 2026-09-11T17:31:08.463Z
close_reason: "Done in 0f0b5c55: the bar runs sqrt(n) to sqrt(n)+1, both labelled, span one unit side at every n, with the open territory darkened to 0.62."
resolution: null
duplicate_of: null
---
Done in the commit above, recorded because the REASONING is the durable part and a later change is likely to want it.

The bar used to run from the proved lower bound to the record plus a headroom proportional to the open gap, clamped between one and ten per cent. That made every bar its own scale: the same distance meant a different thing at n = 11 and at n = 300, and nothing on it could be labelled.

It now runs between two formulas a reader can check in their head. sqrt(n) on the left: n unit squares have area n, so no box with a smaller side holds them. sqrt(n) + 1 on the right: n unit squares fit a grid of side ceil(sqrt(n)), and ceil(sqrt(n)) < sqrt(n) + 1. Span one unit side at every n, so two bars are comparable, and both ends carry their formula as a label rather than a number.

Measured against the corpus: no record exceeds the grid bound; the furthest any sits above the area bound is 0.586 of a side at n = 2, median 0.458.

If a later change wants a tighter right end, ceil(sqrt(n)) is the honest one -- it is the grid itself rather than a loosening of it -- at the cost of a span that varies from 0 to 0.97 across n, and of being exactly zero at every perfect square. That trade is why sqrt(n) + 1 was chosen.
