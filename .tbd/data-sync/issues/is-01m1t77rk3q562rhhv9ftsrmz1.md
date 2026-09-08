---
type: is
id: is-01m1t77rk3q562rhhv9ftsrmz1
title: "Explainer stylesheet: dead selectors, unreachable print rules, and two cargo-cult !importants"
kind: chore
status: open
priority: 3
version: 1
labels:
  - explainer
dependencies: []
created_at: 2026-09-06T02:02:26.787Z
updated_at: 2026-09-06T02:02:26.787Z
---
Residue from the print-cascade audit. None of these is a live defect; all of them are
maintenance surface that made the real bugs harder to see.

## Rules that can never apply

- **`.intro`** — `break-before: page`, `margin-block-start: 1.6rem`, and
  `.intro .section-head { margin-block-start: 0 }`. There is no `.intro` element: not in
  `explainer-article.md`, not synthesised in `render_explainer.py`, not in the rendered
  body. The comment says "the title block is a title page"; page 1 of the PDF carries the
  hero, the "What Is This?" heading and eight body paragraphs.
- **`.legend i { border: 1px solid currentColor; print-color-adjust: exact }`** — every
  `.legend` sits inside `div.panel`, and `.panel` is `display: none` 61 lines earlier in
  the same print block. Same for `.kv`, `.hint`, `.readout`, `.ctl`, `.btns`,
  `.tip-panel` and `.caps`. (`.mass-line` is a direct child of the `figure` and does
  print.)
- **`.cert-page input[type="range"]`** in the print hide-list — every range input is
  inside `.ctl` inside `.panel`, already hidden.
- Selectors matching nothing in the rendered page: `.section-head`, `.deck`, `.tag`,
  `.fig-title`, `.tip`.

## Two `!important` declarations that defend against nothing

`.cert-figure[data-cert="…"][hidden] { display: block !important }` is (0,3,0) against
`.cert-figure[hidden] { display: none }` at (0,2,0) — it already wins. The UA `[hidden]`
rule is a lower origin at normal weight, and were it important, an author important would
lose anyway. The switch sets the attribute, never an inline style, so there is no inline
declaration to beat. Its sibling `.cert-figure:not([data-cert="…"]) { display: none
!important }` has no competing `display` declaration at all in the state it targets.

Dropping both changes nothing. That leaves the whole `!important` surface at two
declarations, both in the print block, both with an argument written next to them.

## A comment describing rules that no longer exist

The block above the figure caps documents "canvas cap 4.5in / img 7in"; the rules are
3.2in and 5in, per the second comment directly below it. The superseded block should have
gone with the change.

## `@media (max-width: 52rem)` also matches when printing

Letter minus 1.25in margins is 576px and the root font size is 16px, so 52rem = 832px and
the block applies on paper. Its two declarations are inert today — `.split` is already
`display: block`, `.panel` already `display: none` — but the block is not print-guarded,
and the next declaration added there will apply to the PDF with nothing saying so.

## Fragile by class shape

`<div class="doc-links screen-only">` is kept off paper by source order alone: both
`.doc-links { display: flex }` and `.screen-only { display: none }` are (0,1,0). Remove
`screen-only` and the chip row prints, one of the chips being a `<button>`.

`<div class="credits centred">` survives the print left-align rule only because it is a
`<div>`. One blank line inside that raw-HTML block turns its four `<span>`s into
markdown-it paragraphs, which carry no `.centred` of their own and would be forced left —
exactly what happened to the colophon.

`.trump svg rect[fill="#ffffff"]` themes a generated SVG by literal colour string. A
renderer emitting `#FFFFFF`, `#fff` or `white` drops dark-mode theming with no error.
