---
type: is
id: is-01m1t775xk82nbnwe87nsgmf77
title: The page stylesheet is written in classes against a vendor written in types
kind: bug
status: open
priority: 1
version: 1
labels:
  - explainer
  - print
dependencies: []
created_at: 2026-09-06T02:02:07.667Z
updated_at: 2026-09-06T02:02:07.667Z
---
Three defects a reader found in the PDF, plus three more an audit found behind them, are
all one shape. This bead names the shape and proposes the structural fix; the individual
symptoms are fixed already.

## The shape

kpress writes type-qualified selectors — `.kpress p`, `.kpress-prose p`, `.kpress li` —
which are (0,1,1). `explainer-shell.html` writes class-only selectors — `.colophon`,
`.hint`, `.centred` — which are (0,1,0). **The page loses to the vendor by default, on
every property, and says nothing when it does.** CSS error recovery and cascade
resolution are both silent by specification.

Confirmed instances, each measured:

| page rule | lost to | effect |
|---|---|---|
| `.colophon { text-align: center !important }` (0,1,0) | this page's own `.kpress p { text-align: left !important }` (0,2,0) | colophon printed flush left |
| `.colophon { margin-block: 2.5rem 0 }` (0,1,0) | `.kpress-prose p` / `.kpress p` margins (0,1,1) | 10.4px gap instead of 40px, **in both media** |
| `.hint { margin: 0 }` (0,1,0) | `.kpress-prose p { margin-block: 0.75rem }` (0,1,1) | hint paragraphs carry vendor margins |
| `:root { --kpress-print-font-size: 12pt }` | kpress declaring the same token on `.kpress`, where it is also consumed | document shipped 11pt under 1.25in margins |

The last one is the same disease in token form: a declaration at the root shadowed by the
vendor's own declaration on the element that reads it. Compare `.cert-page .boxed-text p`
— same author, same property, written type-qualified at (0,2,1), and it wins.

## Why nothing caught it

Every check looked at the screen. The print block is a second, differently parameterised
instance of the whole design — base 18px → 12pt, line-height 1.5 → 1.4, measure 720px →
576px, plus about thirty override rules — and it received none of the review the screen
design gets. `render_explainer_pdf --check` compares two renders for byte equality, which
is reproducibility, not correctness: it passed cleanly on all three defects, because two
identical renders of a wrong page still agree.

`devtools/check_print_layout.py` now measures the print layout at the column the PDF
actually has. That closes the observation gap. It does not close the authoring one.

## The structural fix: cascade layers

kpress contains **zero** `!important` across all six of its stylesheets, so there is no
arms race to win — only a specificity mismatch to stop fighting.

    @layer trump, kpress, page;

Wrap the inlined vendor CSS in `@layer kpress` (in `kpress_css()`) and the page's own
`<style>` in `@layer page`. Then every *normal* declaration in the page sheet beats every
kpress rule at any specificity, which is strictly stronger than what the `!important`
was buying, and specificity inside the page sheet keeps meaning what it says. `trump`
stays empty, first in order, reserved for the day kpress ships an `!important` — because
for important declarations the layer order reverses and the first-declared layer wins.

Two cautions. **Putting only the page sheet in a layer is worse than doing nothing**:
unlayered normal declarations beat all layered ones, so the page would lose
unconditionally. And `@page` nested inside `@layer` is unverified in Chromium — kpress's
`print.css` opens with a top-level `@page`, so hoist those out of the wrap, or verify
with a MediaBox and margin assertion before adopting.

With layers in place, blanket rules can move to `:where()` (specificity 0,0,0) and named
exceptions beat them by merely existing, which makes the colophon class of bug
structurally impossible. `:where()` without the layers is strictly worse than today.

## Cheap guards worth adding with it

- A static lint: `!important` outside the `trump` layer is an error.
- A static lint: any `top`/`left`/`bottom`/`translate` whose value names
  `--kpress-font-size-base` or `--kpress-print-font-size` is an error. That is the
  bullet-position disease, and it names both vendor rules directly.
- A build assertion that the inlined kpress CSS still contains no `!important`, which
  turns the hedge the comments currently guess at into a measured fact.
