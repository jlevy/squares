---
title: Math Text Face Integration
description: Take kpress's math text face (letters and digits from PT Serif inside KaTeX) into the explainer page, its PDF, and the validation tiers, and keep the measurements in a devtool
author: Claude (agent), for samanthadrakova@gmail.com
date: 2026-09-07
status: active
---
# Feature: Math Text Face Integration

**Date:** 2026-09-07 (last updated 2026-09-08)

**Status:** Implemented (2026-09-07) and merged as
[jlevy/squares#114](https://github.com/jlevy/squares/pull/114). The sans composite, the
per-node metric tables, the paint-once wait, the shipped quotation marks and the box
list marker were adopted on 2026-09-08 (Font Consistency → Sans mathematics).
The Safari and Firefox checks by hand are the only work left.

**Workflow entry:** feature implementation from spec.
**Tracking:** epic `think-rk9v`; squares tasks `think-58av` (integration, closed),
`think-do8b` (devtool, closed) and `think-0vju` (verification, open — it carries the
Safari and Firefox checks).
The font epic `think-phgo` carries the rest: `think-n4y7` (sans math), `think-q5df`
(paint once) and `think-9r58` (marker, quotes, mono).
The feature itself is tracked in kpress’s own tbd as epic `kpr-sc4f`, with sans math
deferred as `kpr-7f9z`. Greek sizing, deferred as `kpr-c2tr` when this plan was written,
shipped inside the kpress feature and that bead is closed.

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
  with no math rules of the page’s own.
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
  The page grows from 1,177 KB to 1,418 KB. Accepted for now, and recorded here rather
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
- The PDF pipeline needed no change of its own, but the figures first recorded here came
  from a silently scaled export and are superseded.
  Historical, before `b555aa1a`: the recommended page exported through
  `render_explainer_pdf.render_pdf_bytes` gave the same 14 pages as the page before it,
  with the math letters and digits at the prose’s 11.2pt, and the file 35 KB smaller for
  having no further use for `KaTeX_Main-Bold`; measured against the installed Google
  Chrome (`SQPACK_CHROMIUM`), because Playwright’s pinned headless shell was not
  downloaded on the development machine at the time.
  Both of those numbers were symptoms.
  The LP display equation ran 42px past the print column, and Chromium fits an
  overflowing document by shrinking all of it, so a 12pt document printed at 93.2% —
  11.2pt — over 14 pages; `check_print_layout` did not see it, because it measured
  column boxes and the run that overflowed was inline content inside one.
  Measured 2026-09-07 on this branch: the page prints at the designed 12pt on 16 pages
  and two consecutive exports agree after date normalisation, with
  `render_explainer_pdf --check` reporting 983,958 bytes locally and 948,440 bytes on CI
  (run 34161478114), both on Playwright’s pinned headless shell — the bytes follow the
  browser build and the host’s fonts, the layout does not.
  After `main`’s content merge: 17 pages and 830,153 bytes on macOS with the same pinned
  shell, the extra page being content rather than typography.
  Current, with the fourth sans weight gone and the relation glyphs from a shipped face:
  17 pages and 817,119 bytes on the same host.
  In the file the math letters and digits still come from the `PTSerif-Regular` and
  `PTSerif-Italic` subsets the prose already embeds, while `≤`, `√`, the fraction bar
  and the Greek come from the embedded KaTeX faces.

## Design

### Approach

The renderer learns to inline the composite’s KaTeX-side sources and the metrics asset,
the submodule gitlink moves to the commit that carries the feature, and the checks run.
The measurement scripts from the research become one devtool: three commands for the
measurements themselves, and two more that hold each route’s CSS to its metric plan.

The page’s shell was to be left alone, and this plan said so until the work was done.
Three things in it changed.
The page writes its own `<html>` rather than taking kpress’s shell, so it stamps
`data-kpress-math-text="prose"` itself — kpress’s own default, stated here because
nothing else would state it.
Its footnote rules stand aside for kpress’s backref control, so the control keeps the
accent instead of the source-link colour.
And print sets the footnote references in the sans they wear on screen, at 0.75em.
Nothing the page says about mathematics itself changed.

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
- `devtools/templates/explainer-shell.html`: `data-kpress-math-text="prose"` on
  `<html>`; a `:not(.kpress-footnote-backref)` exemption, so the source-link colour no
  longer overrides kpress’s footnote control; and the print rules that set the footnote
  reference in the sans at 0.75em.
- `devtools/check_print_layout.py`: the document’s own overflow past the page box, with
  the scale Chromium would apply and the widest run named, so the next overflow fails
  the check instead of shrinking every page.
- `devtools/compare_math_fonts.py`: `metrics` prints the x-height, cap height, digit
  height, ascender, operator centre, hairline and stem of the shipped faces from their
  woff2 files; `variants` builds pages from the rendered explainer by injecting CSS from
  a small spec, after switching the page’s own math text face off (the opt-out attribute
  on `<html>`), so every variant is measured against the stock KaTeX baseline the
  research compared; `shots` takes Playwright element screenshots of named paragraphs
  and display blocks in each variant and stacks them into montages.
  `check` and `verify` hold each route’s CSS to its own metric plan — the first by
  reading both descriptions, the second by drawing representative inputs in a browser
  and comparing the advance it inks with the width KaTeX placed it in.
  fontTools in the dev group, pinned past the 14-day cool-off.
- Validation: `render_explainer --check`, `sans_instances --check`,
  `render_explainer_pdf --check`, `check_print_layout`,
  `inspect_explainer_typography --check-supporting`, `check_math_faces`; the Pages
  workflow already checks out the submodule and installs the headless shell, so the only
  change it needed was the last of those.
  None of these are `packing-validate` tiers: the explainer is built and checked in
  `.github/workflows/pages.yml`, which is where `sans_instances --check` belongs too,
  after the browser is installed and before the PDF is drawn, since it needs both the
  rendered page and a browser.

### Print sans embedding

The page’s sans came out of the PDF as Type3 outline paths.
Chromium embeds a variable font only at its default position, and this page prints
Source Sans 3 at 410, 550 and 680; Preview smooths embedded text and leaves outline
paths alone, so the captions, footnotes, hero and footer read a step lighter than the
serif and the mathematics beside them.

The fix is static instances at those three weights in both styles.
kpress’s `devtools/instance_sans.py` generates them; `devtools/sans_instances.py` writes
them to `packing/devtools/templates/fonts/` as
`kpress-print-sans-latin-{weight}-{style}.woff2` and hands them to
`render_explainer_pdf`, which injects them into the loaded document as one
`@media print` block of data-URI `@font-face` rules immediately before it prints.
The served page never sees them, so the screen keeps the variable font and
`site/index.html` does not gain a byte.
`render_explainer`’s inliner is what holds that: it drops every `@font-face` for the
print sans family out of kpress’s stylesheets, and skips a stylesheet the prune empties,
so registering `print-fonts.css` upstream left the rendered page byte for byte where it
was.

That family is `KPress Print Sans`, and no file on this side spells it.
The instances are a modified Source Sans 3, whose OFL reserves the name “Source”, so
kpress declares them under a name of its own; the prune, the probe that recognises the
print stack, and the PostScript prefix (`KPressPrintSans-410`) the PDF scan watches for
all read it back off the loaded generator through `sans_instances.print_family`. A
literal would go on naming a family nothing declares the next time kpress renames it —
which is how the rename that produced this paragraph was found.

The generator is repository content, not package content: `instance_sans.py` lives in
kpress’s `devtools/` and the kpress wheel does not ship it.
So `render_explainer` needs `vendor/kpress` checked out and not merely kpress installed,
which the gitlink already guarantees — every path here resolves kpress from the
submodule rather than from an index — and a missing generator is reported as an
uninitialised submodule rather than as an import error.
`think-y15p` asks kpress to export the family from the package, which would leave the
generator as a fallback rather than the only source.

Two checks hold the rest.
`sans_instances --check` regenerates the instances in memory and compares them byte for
byte, then probes the rendered page under `media: print` and fails on any weight and
style the declared set does not answer, naming the element that asks for it.
The probe reads generated content as well as text nodes — `::before`, `::after` and
`::marker` on every element with a box, wherever the pseudo’s `content` draws something
— because kpress numbers footnote items with `li.kpress-footnote-item::before`, a real
sans run in no text node, and a walk over text alone left the weight it asks for outside
the check. What stays outside is the `@page` margin box, which is not in the document
tree at all; `render_explainer_pdf` covers that side by resolving `--kpress-font-sans`
and `--kpress-font-prose` at the root and loading each by name before it prints, so a
face used only in a margin box cannot have its first request land inside `page.pdf()`.
`render_explainer_pdf --check` scans the exported bytes for font dictionaries and fails
if a face the page ships is a Type3 font, or if it can see no font dictionary at all.
It did not fail on the host’s own fonts while three characters in the sans line were in
no face the document carried, because failing on them would have passed on Linux and
failed on a Mac for a glyph nobody here chose.
Those three now come from a shipped face, and the provenance guard below replaced the
exemption with a named list.

### API Changes

- `python -m devtools.compare_math_fonts {metrics,variants,shots,check,verify}`; `shots
  --element` takes extra CSS selectors, so an element outside the fixed set can join a
  montage.
- `python -m devtools.sans_instances` writes the instances, `--check` verifies them and
  probes the page, `--weights` lists every family, weight and style the page draws in
  under both media with the declaration behind each; `print_face_css()` is what
  `render_explainer_pdf` injects, and `PRINT_FACES` is the declared set.
  `print_family()` and `postscript_prefix()` hand kpress’s family and the PostScript
  name derived from it to the two other modules that need them, so the name has one
  definition and it is kpress’s.
- `python -m devtools.render_explainer_pdf --fonts` lists what the export embedded, what
  it drew as outlines, and which host families are pending on a bead;
  `allowed_families()` and `EXPECTED_HOST_FONTS` are the provenance rule, and
  `shipped()` and `host_font_bead()` are how the on-screen probe asks the same question.
- `relation_face_css(static)` in `render_explainer`, behind the shell’s
  `{{RELATION_CSS}}`: the three relation glyphs subset out of KaTeX_Main.
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
- [x] Give the footnote controls back to kpress and print the references in the sans.
- [x] Print display mathematics at the prose size, and measure document overflow in
  `check_print_layout` so a run past the print column fails rather than scales the
  document (`b555aa1a`).
- [x] Confirm the PDF `--check` on the pinned headless shell in CI: run 34161478114
  reports two agreeing renders over 16 pages, with the print layout clean.
- [x] Open a pull request that leads with what the branch cost and links the two kpress
  documents: [#114](https://github.com/jlevy/squares/pull/114), open and under review.
- [ ] Verify in Safari and Firefox (Playwright WebKit and Firefox builds, or by hand).
  Chromium is verified through the render, print-layout and PDF checks; the other two
  engines are open under `think-0vju`.

## Testing Strategy

- The four existing checks above, plus the PDF check on CI’s pinned browser and the
  page-overflow measurement `check_print_layout` gained, which has a test of its own and
  a `--self-check` that overflows the print column on purpose and holds the gate to
  failing at the right size and naming the block that did it.
- `compare_math_fonts metrics` reproduces the brief’s table for the shipped faces;
  `shots` reproduces the current-versus-recommended montages; `check` reconciles every
  route’s CSS with its metric plan and runs under pytest, and `verify` compares drawn
  advances with KaTeX’s own widths in a browser, which is a gate rather than a test.

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
research note. It was taken on 2026-09-07 against the page as it stood before this
branch, on the machine that wrote the table; the 979,521 bytes quoted elsewhere for the
same export are a different host on a different day, and figures from two hosts do not
subtract — the bytes follow the Chromium build and the fonts the machine has.

The one pair that does subtract is two renders of one page in one browser at one moment.
Measured that way when the instances landed, on macOS with Playwright’s pinned headless
shell: **1,024,108 bytes with the sans in Type3 outlines and 830,153 with it in fonts**,
17 pages either way, and the five `SourceSans3-*` outline fonts gone from the file.
That is the figure `devtools/sans_instances.py` and the pull request both state.

With the fourth sans weight gone and the relation glyphs from a shipped face, the same
export on the same host is **817,119 bytes**, 24 embedded fonts and no Type3 font of any
kind: the three `KPressPrintSans` weights and the italic, the four PT Serif faces, five
KaTeX faces, the atlas figure’s Helvetica, and Menlo and Georgia while `kpr-v731`,
`kpr-2tmj` and `kpr-asj4` are open.

### Sans mathematics, the shipped quotation marks, and one paint

kpress landed the second composite, `KPress Math Text Sans`, along with the shipped
quotation face and the CSS-drawn list marker (kpress #57, gitlink `7fcc226`). This page
adopted all three on 2026-09-08.

**Which face, per expression.** The composite is applied on a
`data-kpress-math-face="sans"` mark, and kpress stamps that mark in the same call that
installs the sans metric tables, so the drawn face and the numbers it is laid out from
come out of one decision.
This page cannot run kpress’s `katex-init.js` — the article’s `.tex` spans and the
figures’ readouts are neither of the two node shapes its loop knows, and the readouts
are re-typeset on every pointer move — so the loop stays the page’s and everything in
that file that is a **decision** is spliced out of it at render time rather than copied:
`TEXT_FACE_OPT_OUT`, `SANS_CONTEXT`, `FACE_SAMPLE`, `KATEX_FAMILIES`, `COMPOSITE_FONTS`
and `FACE_WAIT_MS`, each read as its own `const` declaration and checked for shape.
The sans-role list is the one kpress’s design says lives in that file and nowhere else,
so a copy here would have been a third place for it to be wrong in.

A node is in a sans context if kpress’s roles say so **or** if the words around it are
measurably sans: the first family of the container’s computed `font-family` against the
first family of the `--kpress-font-sans` in scope on the same element, both read from
the same medium, so the test follows the print stack under print without naming either.
The measured half is this page’s and it is a measurement rather than a list because the
page has a dozen containers kpress has never heard of — the mass line, the field
tooltip’s panel, the direction readouts, the captions’ key-value rows.
A list would have been wrong the day it was written: the page’s own
`--kpress-katex-size-sans` rule, the nearest thing it had to a statement of this, misses
the six direction readouts that its own `--kpress-font-sans` rule covers.
The walk climbs past `.kpress-math`, `.kpress-math-render`, `.tex`, `.tex-d` and
`.katex`, which declare the prose face themselves; asking one of those answers for the
formula rather than for the sentence around it, and it put all five footnote expressions
on the wrong side when it was tried.

Two defects came out of that walk and both are fixed here.
The five footnote expressions above, and the three direction readouts, which `updateK`
built as detached spans and typeset before attaching: a detached element has no cascade,
so `closest` found no ancestor and `getComputedStyle` answered with nothing, and those
three came out of the serif composite inside a sans panel.
They are attached before they are typeset now.

**What it costs.** Measured on one host, one browser, one moment, before and after:

| Measured 2026-09-08 | Before | After |
| --- | ---: | ---: |
| Page | 1,478,860 B | 1,725,338 B |
| Page, gzipped | 714,206 B | 867,547 B |
| PDF | 817,108 B | 819,392 B |
| Inlined faces | 24 | 30 |

The sans composite is 6 of those faces and 174,568 B of base64: the Source Sans Latin
pair, their two KaTeX Greek partners, and kpress’s two static print instances at 400,
which are what put `KPressPrintSans-400` and `KPressPrintSans-400Italic` in the export
instead of Type3 outline paths.
Every one of them is a second copy of bytes the page already carries, which is what
makes the prune worth taking to the weight rather than only to the style: the 650 slots
go, and with them 93,684 B of stylesheet.
KaTeX reaches a bold table from `\mathbf`, `\boldsymbol` and `\textbf` only, and the
page sets none of the three in a sans context — its three `\mathbf{D}_4` are prose.
That is a claim about what the built page renders, so `check_math_faces` holds it rather
than a comment. The italic 650 slot would have gone anyway on the partner rule, since
`KaTeX_Math-BoldItalic` is outside `KATEX_FACES`. The remaining duplication is
`kpr-hhdc` and `think-f8q9`, unchanged.

The PDF moved 2,284 B for a strictly better file: two embedded print-sans instances
more, `KPressQuotes-Regular` for the marks, and `Georgia`’s 16 KB gone.

**Painted once.** `kpressMathFaces` settles when both composites and the two KaTeX
families the stylesheet names after them have loaded, or at kpress’s three-second
ceiling, whichever is first; the ceiling is floored at three seconds here, since that is
the block period `font-display: block` already gives a face and a shorter wait would
hand back the repaint it was preventing.
Both of the page’s render sites are behind it, and `math-ready` — the class the PDF pass
and the print-layout check wait on — is set inside the gated block, so the print pass
gets the settled page for free.
Measured on the built page: the first `.katex` node is inserted at 181–214 ms, with all
28 faces the page inlines already loaded and none of the waited families outstanding.

**The quotation marks.** The shell’s print-only prose override is gone.
It existed because kpress borrowed Georgia’s marks through a `local("Georgia")` face, so
a printed page took its apostrophes from whatever the reader owned; kpress ships them
now (`KPress Quotes`, six glyphs of Source Serif 4, 968 B of base64), and keeping the
override would have dropped the shipped face and sent print back to PT Serif’s own
marks. `Georgia` and `LiberationSerif` came off `EXPECTED_HOST_FONTS` with it, so the
guard looks at that family again; `Menlo` stays, on `kpr-v731`. `KPressQuotes` joined
the owned faces.

**What holds it.** `check_math_faces` is the new gate, and it exists because none of the
three questions is readable in the rendered HTML. It walks every `.katex` node in both
media and compares the mark against the face the words around it resolve to; it
re-typesets one caption fraction and one prose fraction from their own TeX under each
metric set and requires the live geometry to match the set the context asks for and to
differ from the other (0.818 em against 0.8614 em, so there is something to tell apart);
it reads one Latin run of each through `CSS.getPlatformFontsForNode`, which answers
`Source Sans 3 ExtraLight` for the caption and `PT Serif` for the prose; and it checks
the paint-once record.
It also fails when the page’s init did not run at all — one inlined IIFE, and a
reference error inside it leaves every other gate green while every formula falls back
to the serif composite.
That is not hypothetical: it happened once on this branch, caught by nothing else.
`sans_instances` was regenerated against the new kpress and its six instances came out
byte-identical, so kpress dropping its own 700 weight did not move this page’s set.

Tracked under epic `think-phgo`, with the kpress work under `kpr-b4mq`:

- `think-988s`, this branch: the page’s own print sans instances injected at PDF time
  (the section above).
- `think-y15p`: ask kpress to export the print-fonts wait and the print sans family from
  the package. Both are private or repository-only today, so this side mirrors the
  margin-box wait and loads the family by path; the duplication is what let the
  margin-box step go missing in the first place.
- `think-zlxl`, done: one sans bold and one sans medium across the design system.
- `think-xd7t`, done: the font provenance guard, on both sides.
  `render_explainer_pdf --check` reads an allow-list of the shipped families, with
  Helvetica as the atlas’s documented exception, and `inspect_explainer_typography` is
  the on-screen equivalent.
  The three relation glyphs the page took from the reader’s machine (`≥`, `≈`, `→`) now
  come from a shipped face, and the `.rel` class that marked three of their sites is
  gone with them.
- `think-f8q9`: subset the eight inlined KaTeX faces to the glyphs the page’s
  mathematics uses, after kpress ships the composite’s own subsets (`kpr-hhdc`, which
  recovers most of the 216 KB).
- `think-n4y7` and `think-q5df`, this branch: the sans composite, the per-node table
  selection, and the paint-once wait (the section above).
- `think-9r58`, the marker and the quotes half done on this branch: kpress’s CSS-drawn
  list marker (`kpr-2tmj`) and its shipped quotation face (`kpr-asj4`) are adopted, the
  shell’s print-only prose override is gone, and `EXPECTED_HOST_FONTS` is down to
  `Menlo` and `DejaVuSansMono`. The mono half waits on `kpr-v731` (Planetaire Mono Text
  at 0.87), and with it the last two entries.

### One bold, one medium

The owner’s rule (2026-09-07): the caption labels are bold, and that bold is the same
weight as the bold in the title credits and everywhere else in the sans.
`sans_instances --weights` is the audit that answers it.
It lists every family, weight and style the page draws in, under screen and under print,
with the run count, a few of the elements that ask, and the declaration behind each —
read out of the cascade through CDP’s `CSS.getMatchedStylesForNode`, because
`getComputedStyle` resolves a token to a number before any script can see which token it
was.

It found two weights that were nobody’s token.
The caption label sat at the medium where the credits were bold, and the footnote
controls at kpress’s literal 600, which is neither.
The sans now draws in three weights and every one of them is a token:

| Context | Token | Weight |
| --- | --- | ---: |
| Captions, footnotes, figure text, chips, colophon | `--cert-font-weight-sans-light` | 410 |
| Title, subtitle, verdict badges, footnote controls, diagram medium labels | `--cert-font-weight-sans-medium` | 550 |
| Title credits, **caption labels**, diagram emphasis labels | `--cert-font-weight-sans-bold` | 680 |

Four literals went with it.
`.rel { 400 }` is gone with the class (below).
The diagram labels’ SVG `font-weight` attributes are markers rather than weights now:
the shell maps `[font-weight="550"]` and `[font-weight="650"]` to the medium and the
bold, so a token moves them with everything else.
The footnote reference, the arrow back from each source and the tooltip’s navigation
link are set once, for both media, at the medium; kpress sets all three from one literal
600, and 550 is 50 units below it and still reads as a mark at the 0.75em they run at.
Dropping 600 took two instanced faces out of the PDF. The serif keeps kpress’s own 650
for `strong`, because the paper profile scopes its bold token to sans components on
purpose — one sans bold is the rule, not one weight for two families.

### The provenance guard

`render_explainer_pdf --check` now reads every font dictionary in the export, embedded
and outline alike, and fails on any family that is not one the page ships.
`allowed_families()` is `PTSerif`, `SourceSans3`, `KPressPrintSans`, `KaTeX_`,
`LocalPunct`, `KPressMathText`, and then `Helvetica`, `Arial` and `LiberationSans` as
the 100-best atlas figure’s documented exception: its labels are baked into
`known-best-1-100.svg` by `build_known_best_atlas.py` under the stack
`Helvetica, Arial, sans-serif`, so the face in the file is whichever of the three the
drawing machine has — Helvetica on a Mac, Arial on Windows, and Liberation Sans on a
Linux runner, where fontconfig aliases both names to the metric-compatible substitute.
All three are the one figure, and it stays by the owner’s decision, so no bead removes
it. The three are matched as host families rather than by bare prefix, so the exception
admits `Helvetica-BoldOblique` and not `HelveticaNeue`, `ArialUnicodeMS` or
`LiberationSansNarrow`, each of which is a font a real machine has.
The names the page owns stay prefixes, because the page owns everything under them and
the two probes answer in two shapes: a PostScript face in the PDF, and in the browser
the instance a variable face is at, `Source Sans 3 ExtraLight`. `KPressPrintSans` is
where the export’s sans actually is, and the list gets it from kpress rather than
spelling it, through `sans_instances.postscript_prefix`; `SourceSans3` stays beside it,
because a print run that missed the instances falls back to the variable face and the
guard has to know that name too.

`EXPECTED_HOST_FONTS` is the temporary list beside it, dated 2026-09-07, each entry
naming the bead it waits on: `Menlo` for the inline code, on `kpr-v731`, and `Georgia`
for the list marker and kpress’s `local("Georgia")` quotation marks, on `kpr-2tmj` and
`kpr-asj4`. The check passes with these present and reports them as pending, so the
guard could land before the fixes it waits for; `think-9r58` empties the mapping.
Each entry carries the substitute the Linux runner answers with, since the names in it
are the host’s: `DejaVuSansMono` and `LiberationSerif`, both of them there because
`pages.yml` reported them.
Both `Georgia` entries came off on 2026-09-08, when `kpr-2tmj` and `kpr-asj4` landed and
the gitlink moved to them; `Menlo` and its substitute are what is left.
Taking a name off is the half that matters and the half nobody is prompted to do: an
entry here is a family the guard stops looking at, so a quotation mark that went back to
the reader’s own serif would have passed in silence.
A plausible substitute nobody has measured is left off, since a listed name is a face
the guard stops looking at; the generic Linux sans was listed once, and it is the exact
face a relation face that stopped loading comes back as on the machine that gates the
check.

`inspect_explainer_typography --check-supporting` asks the same question of the screen.
It walks every element in `.cert-page` that holds text and asserts through
`CSS.getPlatformFontsForNode` that each resolves to a face the document carries, in
screen and in print media, reporting offenders by element path.
Two details are load-bearing and both were measured rather than assumed.
The answer is asked for per element, because kpress’s viewport is a containment boundary
and a subtree aggregate taken at `body` comes back empty — a walk that trusted it would
report a clean page it never looked at.
And `isCustomFont` alone is not enough: `LocalPunct` was a real `@font-face` whose
source was `local("Georgia")`, so Blink called the reader’s own serif a custom font.
kpress ships those six glyphs now, so that particular face is gone and the rule it
taught is not. kpress’s chrome around the document is out of scope, deliberately: the
tooltip and the theme control are set in `system-ui` because they are the reader’s
interface, and none of it prints.

The guard earned its keep on the branch that added it.
The relation face below, declared at `100 900` against Source Sans 3’s own `200 900`,
won Blink’s weight matching for every character and then had no glyph for any of them:
every upright sans run on the page came from the reader’s machine, fourteen glyphs of
the title in `.SFNS-Regular`, and the sans face reported `unloaded`. Nothing else on the
page looked different enough to notice.

### The relation glyphs

`≥`, `≈` and `→` are in no text face the page ships — Source Sans 3 and PT Serif carry
231 and 216 code points and none of the three — so the reader’s machine drew them, and
on macOS the PDF wrote them as outline paths.
The earlier treatment named the weight in a `.rel` class and left the family to the
host, which fixed a weight bug and left the provenance one.

Of the routes a shipped face allows, setting the title as mathematics would put `s(11)`
and its digits in Computer Modern and break the line’s agreement with the subtitle and
credits under it. So the glyphs come from KaTeX_Main, subset to those three code points
and declared as a `unicode-range` face on `Source Sans 3 Variable` itself, which reaches
the chart labels and the caption prose that no class did.
Three measurements settled the rest:

- **Bold, not Regular.** `compare_math_fonts metrics` puts the rule thickness of the
  minus — the bar every relation here is drawn on — at 40 thousandths of an em in
  KaTeX_Main-Regular and 60 in its Bold, against Source Sans 3’s own 62 at the 410 the
  captions run at, 78 at the 550 of the title and 100 at the 680 of a caption label.
  Bold is within 3% of the sans at 410 and at 77% of it at 550; Regular is at 65% and
  51%, the hairline the earlier three-way comparison saw and rejected.
- **Scaled to 70%.** A mathematics face draws its relations for a mathematics line:
  KaTeX_Main-Bold’s `≈` is 765 of ink on an advance of 894 against Source Sans 3’s `=`
  at 441 on 509. Unscaled it collided with its neighbours in the coarsening chart —
  `inspect_explainer_typography` reported four overlaps of 7 to 8 pixels in print.
  70% is where that check passes and where the sign still reads as a relation; at 57%,
  the width of the sans’s own `=`, it reads as a mark.
  The literal space before the sign in those five labels came out with it: the glyph
  carries its own space in its side bearings.
- **One face over the whole weight range.** The relation cannot change weight between
  the title and a caption the way the host’s fallback did, which is what the class it
  replaces was for.

What it costs is stated rather than hidden: scaling takes the stroke down with the
width, so the relation is lighter than the sans’s own signs at every size.
It is accepted because the alternative is not a better-looking relation, it is a
different relation for every reader.
The fix that would settle it is a sans that carries the three characters — Source Sans 3
does upstream, and the woff2 kpress ships is a Latin subset that does not.

## Open Questions

- Whether captions and panels keep the math text face or revert to the KaTeX faces (see
  Background). Adopting the sans composite settles the version of this that was about
  mixing two text faces inside one caption; what is left is the narrower question of
  whether a caption wants mathematics in its own face at all.

## References

- [Research: Harmonizing the Reading Face with KaTeX Mathematics](../../../../vendor/kpress/docs/project/research/research-2026-09-07-math-text-face.md)
  and [Math Text Face](../../../../vendor/kpress/docs/math-text-face.plan.md), in
  kpress.
- [`render_explainer.py`](../../../../packing/devtools/render_explainer.py),
  [`render_explainer_pdf.py`](../../../../packing/devtools/render_explainer_pdf.py),
  [`sans_instances.py`](../../../../packing/devtools/sans_instances.py),
  [`check_print_layout.py`](../../../../packing/devtools/check_print_layout.py),
  [`inspect_explainer_typography.py`](../../../../packing/devtools/inspect_explainer_typography.py),
  [`check_math_faces.py`](../../../../packing/devtools/check_math_faces.py).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
