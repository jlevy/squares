---
title: Math Text Face Integration
description: Take kpress's math text face (letters and digits from PT Serif inside KaTeX) into the explainer page, its PDF, and the validation tiers, and keep the measurements in a devtool
author: Claude (agent), for samanthadrakova@gmail.com
date: 2026-09-07
status: active
---
# Feature: Math Text Face Integration

**Date:** 2026-09-07 (last updated 2026-09-08)

**Status:** The serif integration merged in
[Squares #114](https://github.com/jlevy/squares/pull/114), and the sans adoption and
no-swap fixes merged in [Squares #128](https://github.com/jlevy/squares/pull/128). The
shared runtime follow-up merged in
[KPress #61](https://github.com/jlevy/kpress/pull/61), followed by its architecture
update in [KPress #64](https://github.com/jlevy/kpress/pull/64). Those merged changes
include Planetaire Mono (`kpr-v731`) and
[KPress #65](https://github.com/jlevy/kpress/pull/65)’s font-settings corrections.
The current candidate and continuation checkpoint are recorded below.
Prepared startup and saved-setting support are implemented in
[Squares #135](https://github.com/jlevy/squares/pull/135). Hosted H-006 timing and H-004
geometry checks passed at `dab2a381`; integration with the subsequently merged
[Squares #134](https://github.com/jlevy/squares/pull/134) passed at `dfa0a422`. The
caption-baseline correction at `a10569d1` passed the hosted publication checks: all 13
caption formulas align with surrounding text in both screen and print.
PR #135 records merge and deployment status.
The
[font and math loading architecture](../../../../vendor/kpress/docs/project/architecture/arch-2026-09-08-font-and-math-loading.md)
owns the shared rendering, readiness, and preparation contracts.

**Workflow entry:** feature implementation from spec.
**Tracking:** epic `think-rk9v`; squares tasks `think-58av` (integration, closed),
`think-do8b` (devtool, closed) and `think-0vju` (browser and PDF verification).
The font epic `think-phgo` carries the rest: `think-n4y7` (sans math), `think-q5df`
(paint once) and `think-9r58` (marker, quotes, mono).
The 2026-09-08 review follows W7, pipeline improvement, under `think-z7ab`, with
`think-r54y` for the visible native fallback, `think-ysjq` for shared rendering
readiness, `think-3xrc` for browser gates, and `think-h31m` for CI integration.
`think-7r2x` covers stock-font opt-outs inside sans ancestors and footnote previews.
`think-ws53` covers matching stock metrics when custom font declarations are absent.
The feature itself is tracked in kpress’s own tbd as epic `kpr-sc4f`, with sans math
shipped through `kpr-7f9z`. Greek sizing, deferred as `kpr-c2tr` when this plan was
written, shipped inside the kpress feature and that bead is closed.

## Overview

The explainer page sets prose in PT Serif and mathematics in KaTeX, and the two disagree
in x-height and weight.
The research that diagnosed it and the feature that fixes it live in kpress, because
both are about kpress typography rather than this paper:
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
- Glyph design and metric generation remain in kpress, including the sans composite.
  Greek uses KaTeX glyphs scaled to the surrounding face; adopting a different Greek
  design would be a separate typography change.

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
  With the fourth sans weight gone and the relation glyphs from a shipped face: 17 pages
  and 817,119 bytes on the same host.
  At `a10569d1`, with the mono face adopted and caption baselines corrected: 17 pages
  and 820,692 bytes as `--update` writes the file, 820,598 as `--check` reports it — the
  two modes differ by the 94-byte source receipt and by nothing else, which is why a
  figure here says which one produced it.
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
  documents: [#114](https://github.com/jlevy/squares/pull/114), merged.
- [x] Verify in Playwright WebKit and Firefox, including delayed fonts and mobile width,
  alongside Chromium. The 2026-09-08 local checks pass; the Pages workflow also runs both
  additional engines before deployment.

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
The exception is a real one and not a formality: the figure sets 468 labels in
`font-family="Helvetica, Arial, sans-serif"`, so the export carries nine subsets of
whatever the drawing machine answered that with — nine `Helvetica-Bold` and
`Helvetica-BoldOblique` subsets, 31,331 bytes of font programs, on the Mac that wrote
this.
The page’s own text has no host font in it and the figure inside the page does, and
the two halves of that sentence are said together wherever either is said.
`think-czt4` records it, so the guard’s one accepted exception has a bead like every
pending one ever had.
Measuring the PDF for the math text face showed where the rule was not yet met, and what
the fonts cost:

| Measured 2026-09-07, mono row 2026-09-08 | Web page (1,418 KB) | PDF (946 KB) |
| --- | ---: | ---: |
| PT Serif | 164 KB, four faces | 92 KB, embedded subsets |
| KaTeX faces | 181 KB, eight faces | 25 KB, four embedded subsets |
| KPress Math Text composite | 216 KB, six faces, all duplicate bytes | none (draws the faces above) |
| Source Sans 3 | 75 KB, two variable faces | 345 KB as Type3 outline paths |
| Inline code | system mono | Menlo, 5.6 KB, 134 characters |
| Inline code, since 2026-09-08 | Planetaire Mono Text, 76,352 B of base64 | 3,600 B, one embedded subset |
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
export on the same host was **817,119 bytes**, 24 embedded fonts and no Type3 font of
any kind: the three `KPressPrintSans` weights and the italic, the four PT Serif faces,
five KaTeX faces, the atlas figure’s Helvetica, and Menlo and Georgia while `kpr-v731`,
`kpr-2tmj` and `kpr-asj4` are open.
All three are closed now, and with the mono face adopted the same export is **820,911
bytes as `--update` writes it**, 820,817 as `--check` reports it, and **26 embedded
fonts**: six `KPressPrintSans` instances, the four PT Serif faces, five KaTeX faces,
`KPressQuotes-Regular`, `PlanetaireMonoText-Regular`, and the atlas figure’s nine
`Helvetica-Bold` and `Helvetica-BoldOblique` subsets.
What the subsection below records is an export whose *document* carries no host face.
The nine Helvetica subsets are the figure’s own labels and they stay; they are what
`ATLAS_FACES` and `think-czt4` are for, and `--check` prints them as accepted rather
than passing them in silence.

### Sans mathematics, the shipped quotation marks, and one paint

kpress landed the second composite, `KPress Math Text Sans`, along with the shipped
quotation face and the CSS-drawn list marker
([kpress #57](https://github.com/jlevy/kpress/pull/57), gitlink `7fcc226`). Squares
adopts them through #128.

**Which face, per expression.** The composite is applied on a
`data-kpress-math-face="sans"` mark, and kpress stamps that mark in the same call that
installs the sans metric tables, so the drawn face and the numbers it is laid out from
come out of one decision.
The page embeds kpress’s `katex-math-runtime.js` and calls its public
`kpressMathText.render` API for both article formulas and interactive readouts.
Kpress owns font readiness, metric selection, and revealing the finished expression.
The host supplies its context callback because its `.tex` spans and figure controls
extend kpress’s native markup.

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

**What the initial adoption cost.** This historical comparison ends at the original #128
implementation, `c1dab812`, before the shared-runtime corrections below.
Both sides were measured on one host and browser in one session:

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
Every one is a second copy of bytes the page already carries.
The initial build pruned both 650 slots, removing 93,684 B of stylesheet.
That assumed the default serif reading preference: the three `\mathbf{D}_4` expressions
are in prose, but a saved sans preference makes them request the sans bold face.
[D-486](../../../../defects.md) records the resulting missing-font defect.
The current build retains the normal 650 slot and its static print instance, and
`check_math_faces` exercises both saved prose preferences in screen and print media.
The unused italic 650 slot remains pruned; its `KaTeX_Math-BoldItalic` partner is
outside `KATEX_FACES`. The remaining duplication is `kpr-hhdc` and `think-f8q9`.

The PDF moved 2,284 B for a strictly better file: two embedded print-sans instances
more, `KPressQuotes-Regular` for the marks, and `Georgia`’s 16 KB gone.

**Font readiness.** The shared runtime typesets each expression while hidden, loads the
faces its rendered glyphs require, and then reveals it.
This page also requests all embedded faces: it already carries their bytes, and early
slider, resize, theme, and print callbacks can introduce a different construct.
The native enhancer and custom host use the same rendering API. Repeated calls on one
readout retain the latest requested expression.
If a required face fails or exceeds the wait deadline, native math retains its semantic
MathML and custom formulas retain their raw TeX fallback.

The head bootstrap hides semantic MathML during successful enhancement, preserving its
space until the finished expression is ready.
Without JavaScript, both native MathML and custom TeX remain visible.
The bootstrap watchdog restores the fallback if enhancement fails before completion.
The `math-ready` class marks initial completion; PDF export and browser probes also
await `squaresMath.settled()` after layout and input events, because those events can
schedule more formulas after the initial class is set.

**The quotation marks.** The shell’s print-only prose override is gone.
It existed because kpress borrowed Georgia’s marks through a `local("Georgia")` face, so
a printed page took its apostrophes from whatever the reader owned; kpress ships them
now (`KPress Quotes`, six glyphs of Source Serif 4, 968 B of base64), and keeping the
override would have dropped the shipped face and sent print back to PT Serif’s own
marks. `Georgia` and `LiberationSerif` came off `EXPECTED_HOST_FONTS` with it, so the
guard looks at that family again; `KPressQuotes` joined the owned faces.
`Menlo` stayed on `kpr-v731` until the mono landed, and the subsection below is where it
came off.

**What holds it.** `check_math_faces` is the new gate, and it exists because none of the
three questions is readable in the rendered HTML. It walks every `.katex` node in both
media and compares the mark against the face the words around it resolve to; it
re-typesets one caption fraction and one prose fraction from their own TeX under each
metric set and requires the live geometry to match the set the context asks for and to
differ from the other (0.818 em against 0.8614 em, so there is something to tell apart);
it reads Latin and digit runs through `CSS.getPlatformFontsForNode`, which answers
`Source Sans 3 ExtraLight` for the screen caption and `PT Serif` for the prose.
The print caption uses `KPressPrintSans-400`. It samples the first CSS-exposed formula
rather than counting insertion of a hidden staging node as a paint.
It also fails when the page’s init did not run at all — one inlined IIFE, and a
reference error inside it leaves every other gate green while every formula falls back
to the serif composite.
That is not hypothetical: it happened once on this branch, caught by nothing else.
`sans_instances` was regenerated against the new kpress and its six instances came out
byte-identical, so kpress dropping its own 700 weight did not move this page’s set.

`check_math_loading` delays the browser’s font-load promises, sends slider input and
resize/print events during that delay, and checks for exposed KaTeX or native MathML.
After release it checks final readouts and font status, then repeats with JavaScript
disabled to verify readable fallback content.
The Pages workflow runs the loading check in Chromium, Firefox, and WebKit, and requires
those jobs before deployment.
Both font checkers accept the deployed page URL as well as local HTML, so the same
loading and actual-face probes can verify the published artifact.
These are controlled readiness tests, not measurements of network download speed or a
claim that every source of page layout shift has been eliminated.

### Why the merged fixes still showed a swap

The review reproduced the reported behavior against the original #128 page at `c1dab812`
as well as inspecting what was deployed from main at `2980c5bc`. The changes had reached
different stages:

| Change | What it fixed | What remained |
| --- | --- | --- |
| [Squares #114](https://github.com/jlevy/squares/pull/114) | PT Serif composite and matching KaTeX metrics | Sans contexts and asynchronous rendering |
| [Squares #118](https://github.com/jlevy/squares/pull/118) | Static sans instances embedded in PDF | Served HTML behavior intentionally unchanged |
| [Squares #119](https://github.com/jlevy/squares/pull/119) | Sans weights and font provenance | The older kpress pin still lacked sans-math adoption |
| [Kpress #58](https://github.com/jlevy/kpress/pull/58), included in #57 | Initial composite-font wait | Native fallback exposure and custom host callbacks |
| Original squares #128 | Sans captions and a partial host wait | Still open during review; the wait missed construct faces and early callbacks |

The composites select PT Serif or Source Sans WOFF2 files for Latin letters and digits
through `@font-face` rules and Unicode ranges.
They are not new font binaries with those glyphs physically merged into KaTeX. Greek,
operators, and extensible constructions retain KaTeX glyphs by design.
Inlining the source files removes network requests but does not make browser decoding
synchronous; even a physically merged file would need decoding before use.

The original host wait covered Main, Math, and the composite slots, but not all AMS,
calligraphic, or Size1–4 construct faces.
An initial `ResizeObserver` callback could render Figure 6 before the boot wait.
Native MathML was also visible before enhancement, producing a native-to-KaTeX change
even when the first KaTeX insertion had loaded fonts.
The old insertion check could pass while those paths were still visible.
The shared runtime and delayed-font browser checks cover those paths together.

The final review also reproduced a missing-stylesheet failure in KPress: its custom
metric tables could remain selected while the browser drew stock KaTeX glyphs.
KPress #60 selects stock families and their original metrics together when a composite
family has no registered declarations, independently for serif and sans contexts.
A declared face that fails to load preserves the semantic fallback when the formula
requires it; an unused failed weight does not discard otherwise usable custom math.
Browser regressions cover both cases with actual missing font files.

The integration preserves the work merged in Squares #120 and includes the CI repairs
from #122 and #123. The full checkpoint runs the slow lane, exhaustive tests, and
translation screen in separate jobs, with the remaining checks in a fourth job.
The workflow guards resolve the commands through the validator and require complete,
non-overlapping coverage.
The CI defect is recorded as D-484; the numerical source and earlier defect records from
#120 remain intact.

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
- `think-9r58`, adopted in full: kpress’s CSS-drawn list marker (`kpr-2tmj`) and its
  shipped quotation face (`kpr-asj4`) came first, with the shell’s print-only prose
  override; the mono followed when `kpr-v731` landed Planetaire Mono Text at 0.87.
  `EXPECTED_HOST_FONTS` is empty; the atlas figure’s labels stay on `think-czt4`, which
  records the exception rather than waiting to remove it.
  What remains under the epic is duplication rather than provenance: `kpr-hhdc` and
  `think-f8q9` on the composite’s copies, and `think-y15p` asking kpress to export the
  print family from the package.

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

### The mono face

kpress ships one (`kpr-v731`, Planetaire Mono Text: B612 Mono’s letterforms with Hack’s
punctuation, vendored as latin subsets), and the page takes it.
Inline code was the last role in the document the reader’s machine answered, and
`EXPECTED_HOST_FONTS` is empty because of it.
Not the last in the export: the atlas figure’s labels are still drawn by the machine
that runs it, nine Helvetica subsets on this Mac, and that exception is `ATLAS_FACES`
and `think-czt4` rather than this mapping.

**Four styles for a page that draws one.** The article carries eleven code spans and 179
characters, no fenced block and so no highlighted tokens, and not one of them sits in a
heading, a table, a `<strong>` or an `<em>`; kpress’s own CSS sets no weight or slant on
`code`, and `syntax.css`, which does, scopes every such rule to a `.kpress-code` token
only a fenced block produces.
The export agrees: it embedded `Menlo-Regular` and nothing else, and it embeds
`PlanetaireMonoText-Regular` and nothing else now.
So `regular` alone would have carried every glyph the page draws, and kpress refuses it
— `syntax.css` ships with the design system whether or not a document has a code block,
and a browser answers a style it was not given by shearing or emboldening the one it
has. The refusal is right, and it leaves two honest settings rather than three: all four
styles, or `mono_font: system`, which is the host font again.
The page takes the four.
`render_explainer.MONO_FONT` and `MONO_WEIGHTS` record the decision, and
`mono_stylesheets` puts it through `mono_weights_rejection` — the same gate
`format.mono_weights` and `RenderOptions` are held to — so a narrowed set fails the
render here instead of shipping a page whose code is drawn by shearing.
The stylesheet list itself comes from `mono_css_assets`, the call
`package_asset_manifest` makes, because the mono sheets are not in `DEFAULT_CSS_ASSETS`:
a page that took only that constant would name `Planetaire Mono Text`, declare no face
under it, and go on drawing code from the reader’s machine while reading as though it
had adopted the face.

**One decision, one value.** `data-kpress-mono-font` on `<html>` is kpress’s switch for
the same setting, and the shell carried `planetaire` as a literal beside the constant
that drives the assets.
The literal could not fail — `planetaire` is kpress’s default and only `system` has a
rule of its own — so a shell that drifted to a stale or misspelled value would have gone
on rendering a page that looked right, and a page whose constant moved to `system` would
have declared a face in its markup while shipping none.
The shell stamps `{{MONO_FONT}}` now and `shell_substitutions` fills it from
`MONO_FONT`, so the attribute and the stylesheet list move together and `fill` refuses a
shell placeholder with no value.
The rendered page is byte for byte where it was.

**What it cost.** One host, one browser, one session, Playwright’s pinned headless
shell:

| Measured 2026-09-08 | Before | Gitlink only | After |
| --- | ---: | ---: | ---: |
| Page | 1,859,156 B | 1,865,141 B | 1,944,562 B |
| Page, gzipped (`gzip -9`) | 943,862 B | — | 1,004,083 B |
| PDF, `--update` | 822,950 B | — | 820,921 B |
| PDF, `--check` | — | — | 820,827 B |
| Embedded fonts | 26 | — | 26 |

The page grew 85,406 B, of which 5,985 B is the gitlink bump on its own and 79,421 B is
the face: 57,260 B of woff2 as 76,352 B of base64, plus four stylesheets.
The base64 figure is `4*ceil(n/3)` per file — 17,900, 18,616, 19,788 and 20,048 — and
not on the sum, which pads once and is four bytes short.
Three of those four styles are bytes the page carries and never draws, which is the
price of the no-synthesis contract and is stated here rather than argued away.

**On the wire the number is the compressed one, and it is 60,221 B.** Base64 of a woff2
is incompressible payload in a compressible alphabet, so gzip gives back about three
quarters of it: the three undrawn styles are 58,452 B of base64 and **44,017 B of the
60,221**, measured by gzipping the rendered page with and without their three
`@font-face` blocks.
That is 73% of this branch’s wire cost buying glyphs the page cannot draw, on a page
that compresses to 1,004,083 B — 6.4% larger than before, paid to stop shipping a
different page to every reader.

The PDF went the other way and lost 2,029 B: the mono subset the export needs is smaller
than the Menlo subset it replaced, and the font count is unchanged because one face
swapped for one face.
The subsets are exactly that delta — `PlanetaireMonoText-Regular` embeds as 3,600 B, so
Menlo’s subset was 5,629 B — which is why the mono row of the Font Consistency table
above reads 3,600 B against 5.6 KB rather than the 56 KB a slipped decimal once put
there.

**Two modes, 94 bytes apart, and each figure says which one produced it.** `--update`
writes the file with the `%sqpack-source-html-sha256:` receipt `_with_receipt` appends
after `%%EOF` — 29 bytes of label, 64 of digest and a newline — and `--check` never
writes it, so `--check` reports 94 bytes fewer for the same document; date normalisation
is length-preserving and changes nothing else.
The pair above is one host in one session.
A second worktree of the same commit wrote 820,911 and reported 820,817 — 10 B below
this pair and the same 94 apart — and the review’s independent host measured that same
pair and reproduced the 2,029 B delta against `main`.

**The rung, measured beside the prose.** The mono rung is 0.87 of the base, and it is
kpress’s number to set.
On screen the base is 18px and code computes to 15.66px; under print, 12pt and 13.92px.
Planetaire draws an x-height of 0.560 em against PT Serif’s 0.500, so code’s x-height is
8.77px against the prose’s 9.00px — 97.4%, the “a hair smaller” the rung is chosen for,
and it is what keeps a span from bulging out of its line.
Its advance is 9.427px, 0.602 em, so this page’s 848px prose column holds 89.9 columns;
an 85-column line in a fenced block set against the page’s own cascade fit without a
horizontal scrollbar.
Inside a table the `-small` rung gives 14.094px against a cell at 17.1px, an x-height of
95%, since this page sets its table text at the prose ramp’s `small` (0.95) while the
mono ramp steps by 0.9.

One number does not land where the rung was tuned, and it is left alone because the
ratio is the owner’s. Six of the eleven spans are in footnotes, and footnotes are set in
the sans: against Source Sans 3’s 0.486 em x-height at 18.05px the mono measures 8.77px
to its 8.769px, so code there sits at parity with the text beside it rather than the 97%
it sits at in the serif prose.
kpress derived 0.87 from Planetaire against PT Serif, which is the right pair for the
reading column; the sans is a second pair it does not claim to have tuned.
Read on screen and in the export the difference is not visible, and nothing here is
adjusted for it.

### The provenance guard

`render_explainer_pdf --check` now reads every font dictionary in the export, embedded
and outline alike, and fails on any family that is not one the page ships.
`allowed_families()` is `PTSerif`, `SourceSans3`, `KPressPrintSans`, `KaTeX_`,
`LocalPunct`, `KPressMathText`, and then `ATLAS_FACES` — the 100-best atlas figure’s
accepted exception, `Helvetica` and `LiberationSans`, each carrying `think-czt4`. The
figure’s labels are baked into `known-best-1-100.svg` by `build_known_best_atlas.py`
under the stack `Helvetica, Arial, sans-serif`, so the face in the export is whatever
the drawing machine answered that with, and the export really carries nine such subsets.
The figure stays by the owner’s decision, so the bead records the exception rather than
asking for a change; it is there because an exception without a bead is a defect nobody
wrote down, which is the rule `EXPECTED_HOST_FONTS` states for itself.

Two names and not the figure’s whole fallback chain, and that is what makes the
exception able to fail.
Naming the chain named every face the chain can produce, so the allow-list could not
trip: the labels could change family and the guard would pass in silence.
Listed instead is what the figure has been measured drawing with — Helvetica on this
Mac, Liberation Sans on the Linux runner, where fontconfig aliases both Helvetica and
Arial to the metric-compatible substitute — and `Arial`, which was listed once and which
no machine that draws this figure has been seen to answer with, is now a finding like
any other third face.
Both mappings are matched as host families rather than by bare prefix, so the exception
admits `Helvetica-BoldOblique` and not `HelveticaNeue` or `LiberationSansNarrow`, each
of which is a font a real machine has.
`--check` and `--fonts` print the accepted families and their bead, so the export’s one
host-drawn family is in the output rather than only in a code comment.
The names the page owns stay prefixes, because the page owns everything under them and
the two probes answer in two shapes: a PostScript face in the PDF, and in the browser
the instance a variable face is at, `Source Sans 3 ExtraLight`. `KPressPrintSans` is
where the export’s sans actually is, and the list gets it from kpress rather than
spelling it, through `sans_instances.postscript_prefix`; `SourceSans3` stays beside it,
because a print run that missed the instances falls back to the variable face and the
guard has to know that name too.

`EXPECTED_HOST_FONTS` is the temporary list beside it, and it is empty.
It was dated 2026-09-07 and held four names, each with the bead it waited on: `Menlo`
for the inline code, on `kpr-v731`, and `Georgia` for the list marker and kpress’s
`local("Georgia")` quotation marks, on `kpr-2tmj` and `kpr-asj4`, each beside the
substitute the Linux runner answers with, since the names in it are the host’s —
`DejaVuSansMono` and `LiberationSerif`, both there because `pages.yml` reported them.
The check passes with an entry present and reports it as pending, so the guard could
land before the fixes it waited for; all four came off within two days, the `Georgia`
pair when `kpr-2tmj` and `kpr-asj4` landed and the mono pair when `kpr-v731` did.
The mapping stays in the file with nothing in it, because the shape is the point and the
next wait will use it.
Taking a name off is the half that matters and the half nobody is prompted to do: an
entry here is a family the guard stops looking at, so a quotation mark that went back to
the reader’s own serif would have passed in silence.
A plausible substitute nobody has measured is left off, since a listed name is a face
the guard stops looking at; the generic Linux sans was listed once, and it is the exact
face a relation face that stopped loading comes back as on the machine that gates the
check.
`ATLAS_FACES` is held to the same rule, and was not until 2026-09-08: it named the
atlas figure’s whole fallback chain, which is an exception that cannot fail.

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

## Startup and Layout Follow-Up, 2026-09-08

The owner confirmed that the deployed `33cd4760` page no longer swaps math faces, then
reported slow parameter appearance and neighboring text moving as math arrives.
`think-qcmi` tracks this W7 continuation, with `think-yygv` for the measurement tool,
`think-lkjf` for Squares preparation and scheduling, and `think-gnl0` for the shared
KPress runtime. The upstream counterpart is `kpr-prsb`; `think-fatc` covers preparation
for every saved font setting and complete geometry coverage.

The publication command, `python -m devtools.render_explainer --prepare-math`, now
reserves the measured width, height and baseline of each unbreakable math base.
It prepares all four combinations of custom/system fonts and serif/sans prose.
CSS selects the matching variant before first paint, while inactive variants stay
outside layout and the accessibility tree.
Matching hydration preserves these boxes and natural line breaks.
The
[KPress architecture](../../../../vendor/kpress/docs/project/architecture/arch-2026-09-08-font-and-math-loading.md)
defines the shared contract; Squares owns preparation under its publication styles.

The original HTML includes the default certificate figures and initial parameter math.
Each formula becomes visible when its required glyph fonts are ready, independently of
other formulas. Initial parameter rendering precedes screen heat-map work, which waits
for math to settle; print retains an explicit completion path.
Readable fallback, latest input and certificate switching remain checked behaviors.
List bullets retain KPress’s square dimensions and use the requested downward optical
offset in both screen and print.

Pages checks one prepared artifact across Chromium, Firefox and WebKit, at desktop and
mobile widths under all four saved settings, plus all four settings in Chromium print.
The geometry guard requires every expected visible math base, checks variant selection
and duplicate IDs, and retains negative controls for removed widths, consistently wrong
widths and missing entire reservations.
First-exposure, early-input, no-JavaScript, font-failure and alternate-certificate
checks remain part of publication validation.

Follow-up preview feedback is tracked separately: `think-pbpp` covers reload scroll
restoration, `think-zmdp` covers the lighter math glyphs caused by disabling hinting,
and `think-3k14` requires inline and display math to inherit the surrounding text size
under every saved setting.
`think-nnvo` covers queued formulas outliving the startup watchdog, and `think-jk1r`
covers font-dependent line carriers in print.
These corrections require their own affected checks before publication.

The
[integration plan and experiment record](../../../../packing/benchmarks/math-startup/README.md)
retain the control, failed intermediate runtime and measured default-profile result.
The initial full-observer timing comparison remains under review because observer cost
and the host regime prevent an unqualified latency claim.
The hosted H-003 comparison was rejected; H-005 passes its numerical rule but fails
correctness because of the queued-math and print-carrier defects.
The repaired publication passed H-006 and all 29 H-004 geometry cells on Linux and macOS
at `dab2a381`; the accepted records were committed in `dfa0a422`. Release verification
remains a separate step for the final PR head.

## Continuation Checkpoint: Typography and Publication

The owner requested this checkpoint because account credit was nearly exhausted.
Preserve the working design and finish this slice; do not restart a font architecture or
timing campaign.
The current objective is to publish the reviewed typography work, verify
the deployment, and open the final local HTML and PDF in the OS default browser.

### Branches and Validation Boundary

Squares branch: `codex/math-startup-stability`,
[PR #135](https://github.com/jlevy/squares/pull/135). Commit `2d61e606` merges main
`e8508598`, preserves both sides of the document map and current handoff, renumbers this
font checkpoint to Session 111, and rebuilds the campaign ledger and close report to 109
sessions. Its records tier and every hosted PR check pass: mergeability, validation,
build, suite, geometry, sweeps, Firefox/WebKit font loading, and macOS portability.

The new integration at `93cf54a9` passed 116 focused font, instance, and provenance
tests, then all 45 affected pre-push checks and 1,035 reachable tests in 165.74 seconds.
Its rebuilt page passed the light desktop typography/provenance check: all 13 caption
formulas and 11 inline-code spans have zero baseline offset in screen and print.
Its refreshed PDF is 17 tagged Letter pages (816,939 bytes).
Those artifacts predate the 0.82 mono integration.
The final artifact rebuilt from KPress head `515f4a0` is current and reproducible: two
PDF renders agree at 814,757 bytes, with 17 pages, 24 embedded fonts, and no page-owned
font outlines.

KPress [PR #68](https://github.com/jlevy/kpress/pull/68), tested branch head `515f4a0e`,
branch `codex/reader-reload-baseline-contract`. Squares may pin this filed PR’s branch
commit; both repositories will merge their PRs with merge commits.
The candidate includes the then-current KPress main and the merged
[PR #52](https://github.com/jlevy/kpress/pull/52), merge `149a0c1f`. PR #52’s research
was reconciled with actual browser/PDF behavior and all six checks passed.
It also includes the separate Vitest 4.1.11 security patch; audits are clean.
The candidate’s own PR and any later documentation commit must pass CI before merging.

Candidate validation: the full KPress Python/browser run had 774 passing tests and two
publishing-tree golden failures caused by the new font files.
The two expected trees were regenerated and reviewed; their 13-test replay passed.
Seventy-five focused font/asset tests, three sans-browser cases, 246 JavaScript tests,
lint, types, generator checks, audits, and an isolated wheel/sdist smoke passed.
The Sol typography design-map follow-up, reviewed by Astra, is committed upstream as
`125bada1` under `think-vunf` / `kpr-6q53`. KPress main then advanced through PR #66 to
`d201627`, changing the mono size ratio from 0.87 to 0.82. That source is integrated in
PR #68 head `9a24c2bbe688360b6d6d15ac0a069a43ac306f5e`, including the corrected design
map. Only two generated snapshot conflicts occurred; regeneration and all 47 directly
affected publishing, mono, and asset tests passed.
Hosted run 34294273884 then found that the required browser surface selected `pdf` but
not the `optimize` extra supplying Brotli, and that the new 410 instance measures the
digit advance at 0.498em while one assertion still expected 0.497em at the tolerance
boundary. Commit `f776e21` makes the extra selection consistent across sync, browser
installation, and test execution and updates the assertion to the generated metric.
The focused browser case passes locally and all 57 required browser cases collect.
Astra’s source review found no product blocker and requested one historical-context
correction in the print-sans research narrative; that correction is in the same commit.
The next hosted run cleared those failures and reached 56 of 57 browser cases before a
Linux WebKit rapid pane+fragment reload exposed a missed-`pageshow` race.
Commit `400a9fc` schedules the existing guarded restore when a pane module initializes
after the event; normal pre-event initialization and document hosts are unchanged.
Astra reviewed the repair, and all 27 history unit cases plus the exact WebKit
regression pass locally.
The following hosted run passed the browser job, then found that the publish golden
still named the pre-repair history asset.
Commit `515f4a0` regenerates that one package-owned snapshot; its focused replay passes
locally. Hosted run
[34302772413](https://github.com/jlevy/kpress/actions/runs/34302772413) passes all six
jobs: lint, Python 3.12 through 3.14, browser, and distribution.

### Current Changes and Ownership

- KPress owns regular sans weight 410 at `--kpress-font-weight-sans-regular` in
  `style-tokens.css`. The existing `instance_sans` and `katex_text_metrics` generators
  read that one value and produce matching print instances, composite descriptors, Greek
  scales, metrics, and font warmup requests.
  Supported regular-weight tuning is 200 through 500; larger values can select bold
  fallback operators or collide with the bold slot.
  Medium and bold remain distinct.
- Squares consumes `generator().REGULAR_WEIGHT` for print instances and composite
  reachability; its CSS aliases the upstream token.
  Its medium/bold remain 550/680. Captions and endnotes share 0.92 of the 19px sans base
  (17.48px screen) and a 1.4rem inset on both sides.
  Figure labels retain 0.95 (18.05px).
- The actual Planetaire Mono text baseline was already aligned: all 11 inline code spans
  measured zero offset in screen and print.
  KPress balances inline-code padding at 0.175em above and below, preserving total
  padding and wrapping while lowering the decoration’s edges by 0.075em. The existing
  Squares typography inspector now inventories code baselines and rejects a deliberately
  raised code span. Do not add a glyph transform to this correction.
- Standalone KPress reader panes now flush existing history state before departure and
  restore it on pageshow.
  The original source fails a retained reload test at 2500px to zero.
  Fourteen browser cases and 27 history unit cases pass, including rapid reload,
  fragments, Back/Forward, disposal, and native-host opt-out.
  The pane-only beforeunload hook does not prompt or cancel navigation, but can affect
  Firefox bfcache eligibility.
  Squares uses native document scrolling and gets no reload hook.
  An unchanged-WebKit real-fragment quirk has a narrowly scoped test exception; other
  native cases retain the one-pixel position check.
- The KPress PDF helper warms each margin font at its actual weight token, including the
  410 footer, and the folio CSS reads the matching prose-weight token.
  Squares mirrors that existing helper contract while its credit footer is disabled.
- The canonical KPress loading architecture already documents font composition,
  synchronous staging, per-formula readiness, optional preparation, and measured
  baseline/strut requirements.
  The latest requested design consolidation belongs in its existing `kpress-design.md`,
  with links to that architecture.
  [Paper Design](../../../../packing/devtools/templates/paper-design.md) owns the
  Squares-specific typography roles and points upstream.

### Remaining Work in Order

1. Merge KPress PR #68’s green, reviewed head with a merge commit.
   Squares pins that exact filed-PR head.
2. Push this final Squares integration and wait for every hosted PR check.
   The final local HTML and PDF are current.
   Light desktop and dark narrow typography, math-face readiness, print layout, and
   delayed-font startup pass.
   Caption and endnote math inherit the 410 sans face and surrounding size; all caption
   and inline-code baseline offsets are zero in screen and print.
   Chromium, Firefox, and WebKit each report 347 held loads, 164 readable prepared
   wrappers, and no early, fallback, unready, raw, or unreadable math.
3. Merge Squares PR #135’s exact green head with a merge commit, verify the Pages
   edition stamp and live math-loading smoke, then open the final HTML and PDF in the OS
   default browser. Keep its frozen cost receipt as a dated lower bound; do not
   regenerate it or relabel older timings as measurements of the new source.
   Wait for all PR checks, resolve any new main conflict, and merge the exact head.
4. Wait for the main Pages deployment.
   Run `check_published_site --commit FULL_SHA` and a live `check_math_loading` smoke.
   Open fresh local HTML and PDF URLs with the OS default browser, then close the
   resolved beads and sync.

### Beads and Observed Limitations

`think-qcmi` is the active continuation parent.
The current slice is `think-bccr` (410 and support roles), `think-y54j` (code
decoration/baseline), `think-vunf` (typography design map), `think-qju8` (upstream
ownership), `think-d32d` (caption baselines), `think-uwow` (CI timing record), and
`think-y4cs` (main integration).
Related implementation children remain recorded under the parent.
Upstream: `kpr-3y8q` (410), `kpr-37if` (code padding), `kpr-gj9v` (baseline contract),
and `kpr-n1j6` (reader reload).
`kpr-6q53` tracks the unified typography design map.
`kpr-i91n` (PR #52 reconciliation) is closed and synced.

`think-x65m`, the owner’s rectangular-looking bullets under “Elements of the project,”
is closed after verification.
All 29 visible markers have square CSS boxes in ten observations across desktop/narrow,
device scales 1/2, and print.
The parent and nested items measure 3.65625 by 3.65625 CSS pixels on screen and 3.25 by
3.25 in print.
A slight tall appearance occurs in some crops; a tested 73px scroll change
leaves the crops identical.
Rasterization remains a hypothesis, not a confirmed geometry defect.
Preserve the requested 0.04em optical offset; do not add a pixel-snapping runtime
without evidence. The existing `check_print_layout` marker guard and preview helper
retain the method.

The atlas’s embedded Helvetica remains an accepted standalone-figure exception under
`think-czt4`. Font subsetting and broad CI timing-noise policy are separate follow-ups;
neither is required to finish this publication slice.

### Non-Obvious Setup and Retained Evidence

Use the repository’s Python 3.14 environment at `packing/.venv`, never PATH `python3`.
KPress is the `vendor/kpress` submodule.
Put local caches, review crops, generated previews, and other disposable evidence under
the repository’s gitignored `attic/`. From `packing/`, run frozen project commands with
`PYTHON_CPU_COUNT=4` and, on macOS, `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib`. Do
not commit or format while repository-snapshot tests are running.

The retained startup campaign is
[packing/benchmarks/math-startup](../../../../packing/benchmarks/math-startup/README.md).
H-006 measured `dab2a381`: 12 interleaved pairs per width, 48 valid observations, 14.18%
faster parameter readiness at 1280px and 31.42% at 390px under the unchanged acceptance
rule. H-004 had zero measured movement in all 29 cells on both Linux and macOS. Accepted
records and raw observations were committed in `dfa0a422`. These are historical
source-qualified results, not a timing claim for this checkpoint.

Local optical evidence belongs under `attic/`, including the Planetaire, balanced code
padding, and list-marker review crops.
Reproduce it with the retained tools rather than depending on disposable files.

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
