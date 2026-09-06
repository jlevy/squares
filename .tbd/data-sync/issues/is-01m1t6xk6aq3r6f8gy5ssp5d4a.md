---
type: is
id: is-01m1t6xk6aq3r6f8gy5ssp5d4a
title: Footnote reference can open a line after inline math, and CSS cannot join it
kind: bug
status: open
priority: 2
version: 1
labels:
  - explainer
  - print
dependencies: []
created_at: 2026-09-06T01:56:53.578Z
updated_at: 2026-09-06T01:56:53.578Z
---
A reader found a footnote reference alone on a line in the PDF:

    s(11) ≤ 3.8770835 …
    3

## Mechanism, confirmed

KaTeX renders inline math as `<span class="base">` with `display: inline-block`. An
atomic inline is treated as U+FFFC OBJECT REPLACEMENT CHARACTER, line-break class **CB**,
and UAX #14 **LB20** gives `÷ CB` and `CB ÷` — a break is permitted on both sides of it
with no whitespace present. After a letter there is no break opportunity at all (LB23),
which is why a reference after a plain word never strands. The document's four references
all follow inline math, so all four sit on the one construction that can break.

The wrap falls between the math and the full stop that follows it. The stop then travels
down with the reference, which is why the reader's paste shows only the `3`.

## The CSS fix does not work — measured

The obvious remedy is U+2060 WORD JOINER via `::before`, since LB11 (`× WJ`, `WJ ×`)
outranks LB20. On a reproduction of the exact construction, swept over 310 column widths:

    plain           reference opens its line at 20 of 310 widths
    sup WJ only     20 of 310    (no change)
    katex + sup WJ  20 of 310    (no change)

Neither helps, for two reasons. The reference's own `::before` sits *after* the full
stop, downstream of where the break falls. And `::after` on the math span is generated
*inside* that inline-block, so it cannot join the box to what follows it. CSS has no way
to insert content between two siblings when one of them is a text node.

## What would work

A structural wrap at render time: `<span class="nobr">[math][punctuation][reference]</span>`
with `white-space: nowrap`, injected in `render_explainer.py`, which already
post-processes the rendered body. Cost: an unbreakable run containing an atomic inline
cannot be broken by `overflow-wrap` either, so a long formula near the end of a line will
overflow the measure instead of wrapping. That trade is why this is filed rather than
shipped.

## Not currently reproducing

At the settings this page now uses (1.25in margin, 12pt, 576px column) no reference
strands, swept at 1px over 300–660px. The margin and type change made earlier this
session reflowed the document past it. It will come back on any content change.

## Guarded

`devtools/check_print_layout.py` detects it. Two earlier definitions of the check read
clean on a document that was not — comparing the reference's top against the preceding
text's top misses the case where a full stop wraps down with it, and a Range's
`getClientRects` returns one rect per box rather than per line, so its last rect is
always the single character before the reference. The definition that works is the union
of every rect vertically overlapping that last one: it fires at 20 of 310 widths on the
reproduction where both earlier ones fired at none.
