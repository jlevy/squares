---
type: is
id: is-01m1t6y17vkyy59cks6s769ny4
title: kpress positions the list bullet from a font size, so it drops in print
kind: bug
status: open
priority: 2
version: 1
labels:
  - explainer
  - print
  - upstream
dependencies: []
created_at: 2026-09-06T01:57:07.963Z
updated_at: 2026-09-06T01:57:07.963Z
---
Reported by a reader against the PDF: "▪ Every unit square that can be placed in the
contain" — the bullet sitting at the baseline instead of the middle of the line.

## Cause

kpress draws the bullet as an absolutely positioned `::before` rather than a `::marker`
(`list-style-type: none`, `content: "\25AA\FE0E"`), and places it with

    top: calc(var(--kpress-font-size-base) * 0.1);
    font-size: var(--kpress-bullet-size);

The offset is a constant fraction of a font size, tuned for one type size. The print
media block sets a different base (18px → 12pt) and a different bullet multiplier, and
the constant does not follow. Measured, marker centre against the first line box's
centre: **+0.35px on screen, −1.88px in print**.

## Fixed here, in the page's own layer

`explainer-shell.html` overrides it with geometry that does not name a font size:

    .cert-page.kpress-prose ul > li { line-height: 1lh; }
    .cert-page.kpress-prose ul > li::before {
      align-items: center; display: flex; height: 1lh; top: 0;
    }

A marker box exactly one line box tall, pinned to the top of the first line, glyph
centred inside it. `line-height: 1lh` on the `li` is what makes `1lh` on the marker mean
the line the marker belongs to: without it the marker's own smaller `font-size` rescales
the inherited unitless line-height and its box comes out short. On the `line-height`
property `lh` resolves against the parent's computed value rather than the element's,
which avoids the circularity; here the two differ by 0.02px.

After: **−0.09px on screen, −0.01px in print**. `check_print_layout` holds it there in
both media, at 1px tolerance.

## Still to do upstream

The fix belongs in kpress, not in one page's override. The general rule worth stating
there: vertical alignment of a marker to text is a baseline-alignment problem, and any
`top` or `translateY` constant on a marker is a bug. kpress already does this correctly
for printed ordered lists — `display: grid` with `align-items: baseline` — so `ul` can
follow `ol` rather than needing anything new. A `::marker` would also restore the
`L`/`LI`/`Lbl`/`LBody` semantics the tagged PDF is currently paying for and discarding.
