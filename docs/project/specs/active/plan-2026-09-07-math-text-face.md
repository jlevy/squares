---
title: Math Text Face Integration
description: Take kpress's math text face (letters and digits from PT Serif inside KaTeX) into the explainer page, its PDF, and the validation tiers, and keep the measurements in a devtool
author: Claude (agent), for samanthadrakova@gmail.com
date: 2026-09-07
status: active
---
# Feature: Math Text Face Integration

**Date:** 2026-09-07 (last updated 2026-09-07)

**Status:** Implemented (2026-09-07) except the Safari and Firefox checks and the pull
request.

**Workflow entry:** feature implementation from spec.
**Tracking:** epic `think-rk9v`; squares tasks `think-58av` (integration, blocked on the
kpress feature), `think-do8b` (devtool), `think-0vju` (verification).
The feature itself is tracked in kpress’s own tbd as epic `kpr-sc4f`, with the deferred
sans-math and Greek-sizing features `kpr-7f9z` and `kpr-c2tr`.

## Overview

The explainer page sets prose in PT Serif and mathematics in KaTeX, and the two disagree
in x-height and weight.
The research that diagnosed it and the feature that fixes it live in kpress, on the
vendored `squares/page-fixes` branch, because both are about kpress typography rather
than this paper:
[the research brief](../../../../vendor/kpress/docs/project/research/research-2026-09-07-math-text-face.md)
and [the feature plan](../../../../vendor/kpress/docs/math-text-face.plan.md).
What the feature does, why, and how it is built are those two documents’ to state; this
plan takes what they decided as given and adds only what this page needs.

This plan is the squares side: what the renderer, the PDF export and the validation
tiers need so the page picks the feature up, and where the measurements that settled the
design live afterwards.

## Goals

- The explainer page and its PDF render with the math text face through the submodule,
  with no change to what the page’s own stylesheet says about math.
- Every existing check still passes: render self-agreement, PDF self-agreement, print
  layout, supporting typography.
- The measurements and comparisons from the research live in a devtool, not in one-off
  scripts (OR-1).

## Non-Goals

- The feature itself, its option, its CSS and its metrics generator: kpress’s plan.
- Sans math: deferred, tracked in kpress as `kpr-7f9z`. Greek sizing shipped inside the
  kpress feature (KaTeX’s Greek scaled to PT Serif’s x-height and cap height inside the
  composite), so it is not a squares concern.

## Background

What is specific to this page, found while prototyping the feature on it:

- The renderer inlines everything.
  `kpress_css` rewrites `url("../fonts/…")` to data URIs; `katex_css` keeps only the ten
  KaTeX faces in `KATEX_FACES` and drops the rest.
  The composite family names `../katex/fonts/…` sources, which the rewrite did not match
  before this change.
- The composite’s shape (two `@font-face` blocks per slot, the rest falling through the
  family stack) is the kpress plan’s to describe.
  What follows from it here: a composite face is reachable only if its slot’s KaTeX face
  is, so the bold-italic slot (PT Serif Bold Italic beside `KaTeX_Math-BoldItalic`) is
  dropped from the page with the face it accompanies.
- Inlining composes families from two sources, so the page carries a second copy of each
  face the composite names: three PT Serif copies and three scaled Greek copies of KaTeX
  faces, about 216 KB of base64, plus the 32 KB metrics table.
  The page grows from 1,177 KB to 1,441 KB. Accepted for now, and recorded here rather
  than discovered later; the way down is for kpress to ship the composite’s faces as
  subsets (the 62 Latin glyphs, the Greek range), which the generator already has the
  tooling for.
- The page renders its own math: the explainer template calls `katex.render` directly
  (`tex()` in the shell and the walkthrough script), so the metrics table has to be
  inlined and applied before those calls, not only inside kpress’s `katex-init.js`.
- The `\mkern1mu` kern the renderer adds between a function name and its parenthesis
  (`s(n)`) is what keeps the PT Serif italic, which has no italic correction of its own,
  from setting the parenthesis against the letter.
  It stays.
- The display blocks carry `padding-block: 0.45rem`, which is what hid the one-pixel
  numerator overflow of the CSS-only routes; with the metrics table it is no longer
  doing that job, and can stay for the headroom it was added for.
- Sans contexts: figure captions, the mass line and the panels are set in Source Sans
  and their math now carries PT Serif letters rather than Computer Modern.
  Either is a serif in a sans line; consistency of the math face across the document is
  the usual choice, and restricting the feature to prose contexts is one selector if the
  captions read better the old way.
- The PDF pipeline is unaffected.
  The recommended page exported through `render_explainer_pdf.render_pdf_bytes` gives
  the same 14 pages as the current one; `check_print_layout` reports both clean; two
  consecutive exports agree byte for byte after date normalisation; in the file the math
  letters and digits come from the `PTSerif-Regular` and `PTSerif-Italic` subsets the
  prose already embeds, at the prose’s 11.2pt, while `≤`, `√`, the fraction bar and the
  Greek still come from the embedded KaTeX faces; the PDF is 35 KB smaller because
  `KaTeX_Main-Bold` is no longer needed.
  The check ran the exporter against the installed Google Chrome (`SQPACK_CHROMIUM`),
  since Playwright’s pinned headless shell is not downloaded on the development machine;
  the layout engine is the same, the bytes are not.

## Design

### Approach

Nothing in the page’s template or stylesheet changes.
The renderer learns to inline the composite’s KaTeX-side sources and the metrics asset,
the submodule gitlink moves to the commit that carries the feature, and the checks run.
The measurement scripts from the research become one devtool with three commands.

### Components

- `vendor/kpress` gitlink bump to the branch commit that carries the feature, and the
  `pyproject.toml` comment that lists what the branch carries.
- `devtools/render_explainer.py`: `inline_font_urls` resolves any relative woff2 `url()`
  against its stylesheet’s directory and fails on any source a kept block still fetches;
  `katex_css` takes both KaTeX stylesheets from kpress’s `KATEX_CSS_ASSETS`, prunes the
  composite’s faces by the reachability of their slot’s KaTeX face
  (`COMPOSITE_SLOT_FACES`, checked against the stylesheet’s face count), and leaves
  `KATEX_FACES` unchanged; `katex_js` inlines the KaTeX bundle and
  `katex/katex-text-metrics.js` from `KATEX_JS_ASSETS`, asserts their order, and appends
  the install call with the same three opt-out guards as kpress’s `katex-init.js`, since
  the page renders its own mathematics before that script would.
- `devtools/compare_math_fonts.py`: `metrics` prints the x-height, cap height, digit
  height, ascender, operator centre, hairline and stem of the shipped faces from their
  woff2 files; `variants` builds pages from the rendered explainer by injecting CSS from
  a small spec, after switching the page’s own math text face off (the opt-out attribute
  on `<html>`), so every variant is measured against the stock KaTeX baseline the
  research compared; `shots` takes Playwright element screenshots of named paragraphs
  and display blocks in each variant and stacks them into montages.
  fontTools in the dev group, pinned past the 14-day cool-off.
- Validation: `render_explainer --check`, `sans_instances --check`,
  `render_explainer_pdf --check`, `check_print_layout`,
  `inspect_explainer_typography --check-supporting`; the Pages workflow already checks
  out the submodule and installs the headless shell, so it needs no change.
  None of these are `packing-validate` tiers: the explainer is built and checked in
  `.github/workflows/pages.yml`, which is where `sans_instances --check` belongs too,
  after the browser is installed and before the PDF is drawn, since it needs both the
  rendered page and a browser.

### Print sans embedding

The page’s sans came out of the PDF as Type3 outline paths.
Chromium embeds a variable font only at its default position, and this page prints
Source Sans 3 at 410, 550, 600 and 680; Preview smooths embedded text and leaves outline
paths alone, so the captions, footnotes, hero and footer read a step lighter than the
serif and the mathematics beside them.

The fix is static instances at those four weights in both styles.
kpress’s `devtools/instance_sans.py` generates them; `devtools/sans_instances.py` writes
them to `packing/devtools/templates/fonts/` and hands them to `render_explainer_pdf`,
which injects them into the loaded document as one `@media print` block of data-URI
`@font-face` rules immediately before it prints.
The served page never sees them, so the screen keeps the variable font and
`site/index.html` does not gain a byte.
`render_explainer`’s inliner is what holds that: it drops every `@font-face` for the
`Source Sans 3` family out of kpress’s stylesheets, and skips a stylesheet the prune
empties, so registering `print-fonts.css` upstream left the rendered page byte for byte
where it was.

Two checks hold the rest.
`sans_instances --check` regenerates the instances in memory and compares them byte for
byte, then probes the rendered page under `media: print` and fails on any weight and
style the declared set does not answer, naming the element that asks for it.
`render_explainer_pdf --check` scans the exported bytes for font dictionaries and fails
if a face the page ships is a Type3 font, or if it can see no font dictionary at all.
It does not fail on the host’s own fonts: three characters in the sans line are in no
face the document carries, so the reader’s machine draws them, and on macOS that machine
font is variable too.
Those are reported rather than refused, because failing on them would pass on Linux and
fail on a Mac for a glyph nobody here chose.

### API Changes

- `python -m devtools.compare_math_fonts {metrics,variants,shots}`.
- `python -m devtools.sans_instances` writes the instances, `--check` verifies them and
  probes the page; `print_face_css()` is what `render_explainer_pdf` injects, and
  `PRINT_FACES` is the declared set.
- `python -m devtools.render_explainer_pdf --fonts` lists what the export embedded and
  what it drew as outlines.
- `inline_font_urls(css, stylesheet_dir)`: the second argument is the directory the
  stylesheet is served from, where it was the fonts directory; every relative woff2
  `url()` resolves against it.
- `katex_js(static)` beside `katex_css(static)`; `COMPOSITE_SLOT_FACES` names the KaTeX
  face under each composite slot.

## Implementation Plan

One phase; the kpress feature landed first.

- [x] Bump the gitlink; extend `inline_font_urls`; inline the metrics asset ahead of the
  page’s KaTeX calls; render and run every check.
- [x] Add `devtools/compare_math_fonts.py` and fontTools to the dev group; regenerate
  the brief’s metrics table and montages with it and check they agree.
- [ ] Verify in Safari and Firefox (Playwright WebKit and Firefox builds, or by hand),
  and confirm the PDF `--check` on the pinned headless shell in CI.
- [ ] Open a pull request that leads with what the branch cost and links the two kpress
  documents.

## Testing Strategy

- The four existing checks above, plus the PDF check on CI’s pinned browser.
- `compare_math_fonts metrics` reproduces the brief’s table for the shipped faces;
  `shots` reproduces the current-versus-recommended montages.

## Rollout Plan

The page picks the feature up on the gitlink bump and its next Pages deploy.

## Font Consistency

The owner’s rule (2026-09-07): the explainer resolves every text run to a face the page
ships, on screen and in the PDF. The one exception is the 100-best atlas figure, whose
Helvetica is baked in by its own pipeline (`build_known_best_atlas.py`) and stays.
Measuring the PDF for the math text face showed where the rule was not yet met, and what
the fonts cost:

| Measured 2026-09-07 | Web page (1,418 KB) | PDF (946 KB) |
| --- | ---: | ---: |
| PT Serif | 164 KB, four faces | 92 KB, embedded subsets |
| KaTeX faces | 181 KB, eight faces | 25 KB, four embedded subsets |
| KPress Math Text composite | 216 KB, six faces, all duplicate bytes | none (draws the faces above) |
| Source Sans 3 | 75 KB, two variable faces | 345 KB as Type3 outline paths |
| Inline code | system mono | Menlo, 56 KB, 134 characters |
| List bullets | system serif | Georgia, 16 KB, 48 bullets |
| Atlas figure | Helvetica by design | 54 KB, accepted |

The PDF column is the kpress side of the same measurement, recorded in kpress’s plan and
research note. With the print sans faces the PDF is 794 KB.

Tracked under epic `think-phgo`, with the kpress work under `kpr-b4mq`:

- `think-988s`, this branch: the page’s own Source Sans 3 instances injected at PDF time
  (the section above).
- `think-xd7t`: the font provenance guard.
  `render_explainer_pdf --check` gains an allow-list of the shipped families, with
  Helvetica as the atlas’s documented exception, and `inspect_explainer_typography` the
  on-screen equivalent.
  The three relation glyphs the page still takes from the reader’s machine (`≥`, `≈`,
  `→` in the hero and `.rel`) move to a shipped face.
- `think-f8q9`: subset the eight inlined KaTeX faces to the glyphs the page’s
  mathematics uses, after kpress ships the composite’s own subsets (`kpr-hhdc`, which
  recovers most of the 216 KB).
- `think-9r58`: adopt kpress’s mono face (`kpr-v731`, Source Code Pro until `kpr-aq8o`
  decides the final face), its CSS-drawn list marker (`kpr-2tmj`) and PT Serif quotation
  marks (`kpr-asj4`); then the shell’s print-only prose override goes.

## Open Questions

- Whether captions and panels keep the math text face or revert to the KaTeX faces (see
  Background).

## References

- [Research: Harmonizing the Reading Face with KaTeX Mathematics](../../../../vendor/kpress/docs/project/research/research-2026-09-07-math-text-face.md)
  and [Math Text Face](../../../../vendor/kpress/docs/math-text-face.plan.md), in
  kpress.
- [`render_explainer.py`](../../../../packing/devtools/render_explainer.py),
  [`render_explainer_pdf.py`](../../../../packing/devtools/render_explainer_pdf.py),
  [`sans_instances.py`](../../../../packing/devtools/sans_instances.py),
  [`check_print_layout.py`](../../../../packing/devtools/check_print_layout.py),
  [`inspect_explainer_typography.py`](../../../../packing/devtools/inspect_explainer_typography.py).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
