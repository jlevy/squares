# Design System

This is the one description of how every page of the site looks: the explainer, the
overview, Atlas, About, case and result records, Frontier, papers, tutorial and
Visualize. Each stylesheet implements what is written here and points back to it; when a
page needs something new, it is added here first and then to the stylesheet that owns
it.

Three layers carry it, from the bottom up, with the paper’s text tokens shared by all:

| Layer | File | Owns |
| --- | --- | --- |
| KPress | `vendor/kpress` | Fonts, Markdown typography, math, themes, print |
| Text | [paper-type.css](paper-type.css) | The type base, reading measure, heading scale, role scales and pinned faces every page shares |
| Paper | [paper-publication.css](paper-publication.css) | The publication layer every paper shares: figures, panels, components and print rules |
| Site | [site.css](site.css), [site-nav.css](site-nav.css) | Site pages and the navigation bar every page carries, the explainer and the workbench included |

The paper and site layers read the same values from `paper-type.css`, under their own
prefixes, `--cert-` and `--site-`, so a site page and the explainer set a role at the
same size and weight.
Every site value is a KPress token or derived from one, so it follows the theme and the
print rules.

The explainer uses serif prose for sustained reading and sans serif text for figures,
captions, notes, and controls.
The web page and PDF share this hierarchy, with sizes scaled for each medium.
Keep these conventions reusable across papers.

[paper-publication.css](paper-publication.css) contains the publication layer both
papers share, above KPress and `paper-type.css`. Both
[n11-lower-bounds-explainer-shell.html](n11-lower-bounds-explainer-shell.html) and
[n11-optimality-review-shell.html](n11-optimality-review-shell.html) inline that
stylesheet;
[n11-lower-bounds-explainer-article.md](n11-lower-bounds-explainer-article.md) and
[n11-optimality-review-article.md](n11-optimality-review-article.md) contain the
separate articles. KPress supplies the fonts, Markdown typography, math, themes, and
general print behavior.
`paper-type.css` sets the type proportions and reading measure, and the publication
layer sets the figure layout and the paper’s components.

## Typography Roles

Sizes below are the CSS values for each medium.
Compare the final PDF when absolute point sizes matter: browser print scaling can change
physical sizes.

| Role | Web | Print | Treatment |
| --- | --- | --- | --- |
| Prose | 18px | 12pt | Serif, with KPress prose emphasis |
| Sans base | 19px | 12⅔pt | A size ratio of 19/18 against prose |
| Main title | 28.5px | 19pt | Sans, 1.5 of the sans base |
| Subtitle | 23.75px | About 15.8333pt | Sans caps, 1.25 of the sans base |
| Title credits and date | 19px | 12⅔pt | Sans base size |
| Section headings | 21.6px | 14.4pt | Serif italic, 1.2 of the prose base |
| Heading leading | 1.15 | KPress’s 1.2 | `--paper-heading-leading`: every heading, a card’s and a popover’s headline, and a page’s subtitle; the explainer’s hero title keeps KPress’s 1.05 |
| Space above a section heading | 48.6px | 37.8pt | `--paper-section-space`: 2.7 of the prose base on screen, 2.8 in print |
| Space below a section heading | 27.2px | 15.6pt | `--paper-section-space-below`: 1.7rem on screen, 1.3rem in print |
| Figure labels and controls | 18.05px | About 12.0333pt | Sans, 0.95 of the sans base |
| Captions and end footnotes | 17.48px | About 11.6533pt | Shared sans size: 0.92 of the sans base; 1.4rem side inset |
| Colophon | 16.15px | About 10.7667pt | Sans, 0.85 of the sans base |
| Navigation links and section tabs | 17.48px | Not printed | Sans medium at the caption size, 0.92 of the sans base: one step under the prose |
| Button labels | The control’s sans size | The control’s sans size | Uppercase through `--paper-button-label-case`, shared by native buttons, action links and section tabs |
| Popover article title | 1.25 of the popover body | Not printed | Sans medium, normal capitalization; `--paper-popover-title-scale` |
| Popover section heading | 1.1 of the popover body | Not printed | Sans medium; `--paper-popover-section-scale`; deeper headings use the body size |
| Site name in the bar | 19px | Not printed | Sans bold caps at the sans base |
| Sans weights | 410 regular, 550 medium, 680 bold | Same | Preserve serif weight settings |
| Supporting text color | KPress gray text role | Solid black | Preserve semantic diagram and status colors |

Figure labels retain their readable size; captions and end footnotes use a slightly
smaller shared size and inset on both sides.
Screen theme colors still apply in both light and dark mode.
Print uses a white ground and black prose, labels, captions, and notes; semantic diagram
colors retain their meaning.
Links have no persistent underline on the web or in print.
Links within supporting text inherit its gray or black; links in the main prose retain
the accent color. Caption leads use bold weight to distinguish the figure number without
changing its size or color.

Every button label uses uppercase sans text, including popover actions, Atlas controls,
paper controls and Workbench controls (`think-rfy8`). The shared rule lives in
`paper-type.css`; labels keep natural spelling in source and accessible names.
Card titles use Chicago Manual of Style Title Case (`think-foi5`), following tbd’s
common documentation guidelines.
Articles, coordinating conjunctions, and prepositions stay lowercase unless they begin
or end a title. Mathematical symbols, acronyms, and proper names retain their case; card
descriptions retain sentence case.
Action links use the same rule as native buttons.

Case, result and document popovers use the same compact sans heading hierarchy
(`think-1rg7`). A fetched result article keeps its main heading; the small preview title
is removed when the article loads, so the title appears once.
While loading or after a failed request, the short preview title remains available.
Document iframe previews apply the same hierarchy within the embedded page
(`?view=embed`); the full page keeps its standalone heading scale.
Result section labels (`.site-result-heading`) are the exception: they retain their
small uppercase sans treatment, with their own caps size and spacing.

## Color

One accent, the teal `--kpress-doc-accent`, is the only link and emphasis color:
`oklch(51.09% 0.0861 186.4)` in the light theme and `oklch(76.68% 0.0861 186.4)` in the
dark. Both the paper and site layers alias KPress’s separate link blue to it.
Supporting text uses KPress’s gray (`--kpress-doc-muted`, carried as
`--site-support-color`) on the web and black in print.

The packing palette is the fixed set of square fills in `SQUARE_HUE_PALETTE`
(`packing/src/sqpack/render/style.py`), shaded by contact count in the figures.
Page colors that are not the accent take their hues from it:

| Use | Hue | Chroma | Source in the palette |
| --- | --- | --- | --- |
| Verification rung (`V`) | 250 | Rises with the level | The blue square, `#166eac` |
| Confirmation rung (`C`) | 158 | Rises with the level | The green square, `#158655` |
| Significance (`S`) | 205 | One ink, the same at every level | Between the blue and the green |

Every chip carries the page’s own text colour, black in light mode, on a light fill, and
in dark mode light text on a dark fill.
Significance is no chip (the owner, 2026-10-03, `think-m3m4`): its rung is drawn on the
page in its own ink, a dark teal (**Significance**, below).
A plain chip is a 16% tint of the muted gray over the page background, and an accent
chip a 22% tint of the accent.

### The Rung Scale

A rung’s fill is one rule,
`oklch(base + step × level, chroma-base + chroma-step × level, hue)`, so its saturation
and its strength both rise with the level: level 0 is nearly the page background, and
the top rung is the most saturated and the furthest from it.
Four tokens set the scale in each theme, and the two ladders that carry a hue share
them:

| Token | Light | Dark |
| --- | --- | --- |
| `--site-rung-base`, the lightness at level 0 | 95% | 25% |
| `--site-rung-step`, what a level adds to it | −5.5% | +4.6% |
| `--site-rung-chroma-base`, the chroma at level 0 | 0.015 | 0.012 |
| `--site-rung-chroma-step`, what a level adds to it | 0.024 | 0.019 |

No chip has a value of its own; a level’s fill is always these tokens at that level.

The text is the page’s own at every step, with no switch to a second text colour: the
scale stops where that text still reads.
Every fill is inside sRGB, so a browser shows the chroma written here, and the text’s
contrast on it is 6.1:1 or better in light mode and 5.3:1 or better in dark, against the
4.5:1 that WCAG AA asks of body text.
The fills and ratios below are what `devtools.rung_scale` computes from the tokens in
`site.css` and KPress’s page colours; run it after changing a token.
`tests/test_rung_scale.py` holds this table to its output, the order to monotonic, and
every ratio to 4.5:1.

| Rung | Light fill | Text contrast | Dark fill | Text contrast |
| --- | --- | --- | --- | --- |
| `V0` | `oklch(95.0% 0.015 250)` `#e7f0f8` | 15.4:1 | `oklch(25.0% 0.012 250)` `#1d2227` | 13.6:1 |
| `V1` | `oklch(89.5% 0.039 250)` `#cadff6` | 13.0:1 | `oklch(29.6% 0.031 250)` `#212e3c` | 11.7:1 |
| `V2` | `oklch(84.0% 0.063 250)` `#accef3` | 10.9:1 | `oklch(34.2% 0.050 250)` `#243a51` | 9.9:1 |
| `V3` | `oklch(78.5% 0.087 250)` `#8ebeef` | 9.1:1 | `oklch(38.8% 0.069 250)` `#264768` | 8.2:1 |
| `V4` | `oklch(73.0% 0.111 250)` `#70adeb` | 7.5:1 | `oklch(43.4% 0.088 250)` `#27537f` | 6.7:1 |
| `V5` | `oklch(67.5% 0.135 250)` `#4f9be6` | 6.1:1 | `oklch(48.0% 0.107 250)` `#266097` | 5.5:1 |
| `C0` | `oklch(95.0% 0.015 158)` `#e7f2eb` | 15.4:1 | `oklch(25.0% 0.012 158)` `#1d231f` | 13.5:1 |
| `C1` | `oklch(89.5% 0.039 158)` `#c8e5d3` | 13.2:1 | `oklch(29.6% 0.031 158)` `#1f3227` | 11.6:1 |
| `C2` | `oklch(84.0% 0.063 158)` `#a9d8bb` | 11.1:1 | `oklch(34.2% 0.050 158)` `#20402e` | 9.7:1 |
| `C3` | `oklch(78.5% 0.087 158)` `#88caa4` | 9.3:1 | `oklch(38.8% 0.069 158)` `#1f5036` | 7.9:1 |
| `C4` | `oklch(73.0% 0.111 158)` `#65bd8d` | 7.8:1 | `oklch(43.4% 0.088 158)` `#1a5f3e` | 6.5:1 |
| `C5` | `oklch(67.5% 0.135 158)` `#3aaf76` | 6.4:1 | `oklch(48.0% 0.107 158)` `#0f6f46` | 5.3:1 |

The status chips take fills from the same scale, so one status reads the same wherever
it is drawn and turns over with the page (the owner, 2026-10-02, `think-c19o`): a
result’s `confirmed` is the confirmation rungs’ green at C3’s strength and its
`reviewed` the verification rungs’ blue at V2’s, and a case’s `proved` is a green and
its `open` a yellow, each a hue and a level of the scale, and the yellow a chroma boost
of 0.02, the most that keeps its dark fill in sRGB. The other statuses, the kinds and
the standings keep the plain chip.
`devtools.rung_scale` computes these too, and `tests/test_rung_scale.py` holds this
table to its output and every ratio to 4.5:1.

| Status | Light fill | Text contrast | Dark fill | Text contrast |
| --- | --- | --- | --- | --- |
| `confirmed` | `oklch(78.5% 0.087 158)` `#88caa4` | 9.3:1 | `oklch(38.8% 0.069 158)` `#1f5036` | 7.9:1 |
| `reviewed` | `oklch(84.0% 0.063 250)` `#accef3` | 10.9:1 | `oklch(34.2% 0.050 250)` `#243a51` | 9.9:1 |
| `proved` | `oklch(78.5% 0.087 145)` `#96c897` | 9.3:1 | `oklch(38.8% 0.069 145)` `#2b4e2d` | 8.0:1 |
| `open` | `oklch(84.0% 0.083 95)` `#dbcb8c` | 10.9:1 | `oklch(34.2% 0.070 95)` `#443800` | 9.9:1 |

### Significance and the Other Inks

A significance rung is drawn in an ink of its own on the page, not on a chip:
`--site-significance`, a dark teal at hue 205, between the confirmation green and the
verification blue so it reads as neither, and darker and bluer than the accent so it
never reads as a link; it is light in dark mode.
The rung is its letter and level, `S4`, at the sans medium weight, then as many short
bars in the same ink as its level, one to five, so a column of them reads as a meter
(`overview_sections.significance_mark`). It is the second column of a table of results,
narrow, with a new result’s star after the bars, and it stands first among the rungs in
a result’s overview, a case record and the rating ladders.

The recent-bound star is the one warm mark, `--site-new-result`, lighter in dark mode so
it keeps its contrast there.
`devtools.rung_scale` measures both inks against the page’s background in each theme,
and `tests/test_rung_scale.py` holds this table to its output: the significance ink is
text, held to 4.5:1, and the star a symbol, held to 3:1, both inside sRGB.

| Ink | Light | Against the page | Dark | Against the page |
| --- | --- | --- | --- | --- |
| `--site-significance` | `oklch(42.0% 0.070 205)` `#05585f` | 8.2:1 | `oklch(80.0% 0.085 205)` `#77ced8` | 10.2:1 |
| `--site-new-result` | `oklch(52.0% 0.190 25)` `#be222a` | 6.1:1 | `oklch(66.0% 0.170 25)` `#e8605b` | 5.5:1 |

### Every Colour Is a Token

Every colour the site and its papers paint with is a custom property, so a colour is
tried and changed in one place, and a dark theme or a print sheet redefines the token
rather than every rule that uses it (the owner, 2026-10-03, `think-zhlc`). A rule says
`var(--site-shadow)`, never `oklch(0% 0 0 / 0.15)`; a mix of the page’s own colours
stays in the rule that paints with it, since a token resolves where it is declared and
the dark theme’s page colours are set below the root, and its ratio is the token:
`color-mix(in oklch, var(--kpress-doc-muted) var(--site-chip-tint),
var(--kpress-doc-bg))`. `devtools.check_colour_tokens` holds every served stylesheet to
this: no hex colour, no colour function that names a number of its own, and no named
colour in a property that paints, outside a custom property, and every token a rule
paints with is declared.
Two declarations are allowed, each with its reason in the checker, and an allowance that
names nothing fails: the folio’s ink in a printed paper’s `@page` margin boxes.
`tests/test_colour_tokens.py` holds the stylesheets to it, with a negative control for
each rule.

Every hover, a table’s group row and a targeted row take one gentle wash, `--site-wash`,
defined in `site-nav.css` because every page carries it: KPress’s hover surface in light
mode, and a 9% tint of the text in dark mode, where KPress’s own is a light gray that
light text cannot sit on.

## Text

Every page sets its reading text as the explainer does, from one file,
[paper-type.css](paper-type.css), which the explainer’s shell, every KPress page and the
Visualizer’s navigation shell inline right after KPress’s stylesheets.
No page declares these tokens itself; `tests/test_overview.py` fails a layer that does,
and `tests/test_site_text_tokens.py` pins what they resolve to in Chromium.

| Token | Value | Resolves to |
| --- | --- | --- |
| `--kpress-host-font-size-base` | `18px` | Every KPress size, from `--kpress-font-size-base` |
| `--kpress-measure` | 40 of the base | 720px, the width KPress’s default 45 gives at 16px |
| `--kpress-font-size-h2` | 1.2 of the base | 21.6px at every width; KPress steps it to 1.4 from a 64rem pane |
| `--paper-font-scale-sans` | 19/18 | The 19px sans base of captions, cards and notes |
| `--paper-font-weight-sans-medium`, `-bold` | 550, 680 | The sans medium and bold |
| `--paper-title-scale`, `-subtitle-`, `-support-`, `-note-`, `-colophon-` | 1.5, 1.25, 0.95, 0.92, 0.85 | The roles in the table above |

What a reader sees, measured with `devtools.measure_site_pages type` on the explainer,
the tutorial, the readme and the homepage, identical on all four where the role occurs:

| Role | Face | Size / line height at 1280px | At 390px |
| --- | --- | --- | --- |
| Paragraph and list item | PT Serif | 18 / 27px | Same |
| h1 (a report’s title) | PT Serif | 30.6 / 36.72px (1.7 of the base) | Same |
| h2 | PT Serif italic | 21.6 / 25.92px | Same |
| h3 | Source Sans 3, 550 | 21.6px | 20.7px |
| h4 | Source Sans 3 italic, 540 | 21.6px | 20.16px |
| Table cell | Source Sans 3, 410 | 17.1px | 16.2px |
| Inline code | Planetaire Mono Text | 14.76 / 22.14px | Same |
| Inline math | KPress Math Text (serif) | 18px, the text’s own em | Same |
| Text line | — | 800px: the measure and both 2.5rem insets | The column less the page margin |

h3 and h4 keep KPress’s own step up at a 64rem pane.
The explainer’s title is its own role (sans caps, 28.5px); a report’s h1 is the Markdown
title and keeps KPress’s ratio of the same base.
The homepage sets its summary lists and tables a step smaller, in `site.css`.

**Line breaks.** No text on the site breaks inside a word.
KPress sets `overflow-wrap: break-word` on every page, which cuts a run of characters
only when it is longer than a whole line.
The site adds `overflow-wrap: anywhere` in two places, both runs with no space in them
by nature: a case record’s exact decimal (`.site-case-decimal`, as many as 67 digits)
and a repository path in a result overview’s links (`.site-result-links code`).
`anywhere` also lets a grid column or a table cell shrink to one character, which sets a
label a letter to a line, so it never goes on prose, on a label or on a column holding
either. No sheet uses `word-break` to break words, and none hyphenates.
A name set as code, such as the evidence identifier `E-nagamochi-lower`, is one word
too, though a browser may end a line on any of its hyphens.
`render_frontier_page.evidence_links` puts each name, with the comma after it, in one
inline box (`.site-name`): a line breaks before the box and never inside it, and only a
name longer than the whole line wraps, inside its box.
A result overview’s links are boxes of the same kind, each link that holds a code name.
A label column has no width of its own; it is as wide as its labels (**Visual summary**,
below). A case file’s own prose is a KPress document like every report, and KPress may
still end a line on the hyphen of a code span there.
`tests/test_overview.py` holds the sheets to this, and `devtools.preview_site --press`
fails on any word broken across lines in what a press opens (**Print and Verification**,
below).

**Sans weights.** Sans text is set at one of three weights on every page, the regular
410, the medium 550 and the bold 680 (`--site-font-weight-sans-light`, `-medium` and
`-bold`, which alias the paper’s). A face is not inherited with a weight: a rule that
sets the sans face and no weight leaves its text at the serif’s 400, a step lighter than
the sans’s regular and lighter than the mathematics in it, which the sans composite
always draws at 410. Thirty-one rules of `site.css` and `site-result.css` did, a card’s
note, every popover, the table tools, the rating ladders and the case records among
them. So every rule in those two sheets that sets the sans face sets its weight, which
`tests/test_site_glyphs.py` holds, and `devtools.measure_site_pages glyphs` reports any
sans run a page draws at another weight.
Two weights are KPress’s own and stand: a table’s head at 650 and an `h4` at 540. A
formula in a medium or bold run keeps the regular weight of its composite, since
KPress’s sans math tables are built at the regular and the bold alone.

**One value a role.** `devtools.measure_site_pages glyphs --view summary` lists every
role’s distinct settings across the pages; measured over the two papers and the fifteen
KPress pages at 1280 and 390 pixels, a role is set one way on every page it occurs on,
with these exceptions:

| Role | Settings | Why |
| --- | --- | --- |
| h3, h4, table cell (documents) | 21.6px and 17.1px at 1280, 20.7px, 20.16px and 16.2px at 390 | KPress’s own step at a 64rem pane |
| h3 (a case record’s sections) | 19px | The record’s own heading, at the sans base (`.site-case-heading`) |
| Table cell (site tables) | 17.48px, and 15.73px as a row card on a phone | The results and atlas tables are set at the note size |
| Page title | Leading 1.05 on the papers, 1.15 on the site pages | The explainer’s title keeps KPress’s leading, which its prepared math is fitted to; the reviews share its layer |
| Caption | Leading 1.4 on the papers, 1.35 on the site pages; 16.15px under the homepage’s hero, 17.48px elsewhere | The papers’ `--paper-support-leading`; the hero’s caption is a size of its own in `site.css` |
| Colophon | Line height 1.5 on the papers, the face’s own on the site pages | One line either way |
| Chip | The papers’ format chips at 16.15px, the site’s at 17.48px | Two components |
| Table head | 650, and 550 for a group row | KPress’s head; the site’s group rows are medium |

**Faces.** Every page carries byte-identical `@font-face` blocks (PT Serif and its
punctuation face, Source Sans 3, Planetaire Mono Text, the KaTeX faces and KPress’s math
composites), because every page takes them from the same functions,
`render_n11_lower_bounds_explainer.kpress_css`, `katex_css` and `relation_face_css`: the
published papers, workbench and site pages link them as shared files (**Shared Assets**,
below). `devtools.measure_site_pages faces` compares them block by block, reading a
linked stylesheet as the page’s own.
KPress leads each family token with an embedding host’s hook, `--kpress-host-font-sans`
and its siblings, so an application embedding a KPress fragment can supply its own face.
The site does not honor those hooks: a viewer that injects one would draw the page in a
face it does not ship, which is the rule every text run here is held to.
`paper-type.css` sets each hook to `initial`, important, on KPress’s own scopes, so
KPress’s stack, led by the inlined face, always applies.
A reader’s own choice of system fonts still works: KPress’s `data-kpress-font-set`
switch sets the family tokens themselves, not the hooks.
Its system stack (`style-tokens.css`, the block for `[data-kpress-font-set="system"]`)
applies only under that attribute, which only a saved reader preference stamps.

## Math

Math takes the face of the text around it: serif math in serif prose, sans math in sans
text.
KPress chooses the face from a fixed list of sans contexts (a table, a `<details>`,
a caption, a footnote), so a site style must not set text inside one of those contexts
in the serif face, or the other way round; set the text in the face KPress will pick for
its math. The outer math em follows the surrounding text in inline and display formulas;
KaTeX still controls the internal sizes of scripts and nested expressions.
One exception: a headline that is mathematics standing alone, such as $n = 11$, is set
in the serif face, on a card, in a popover and in any heading, though the headline’s own
face is sans. A headline with words in it, such as “Earlier $n = 11$ lower bounds”, is
not one: its math follows the words into the sans.
The exception’s element is marked `data-math-face="serif"`, which the host adapter’s
sans test (`host_math_init.js`) honours before it reads the surrounding face.
`overview_sections.headline_math_face` marks a card’s headline and its popover’s when
the value is all math, and a result overview marks the $n = N$ over each of its cases in
its markup. The case popover has no headline of its own: the record it shows names its
case in its head (**Case records**, below).
Popovers carry no `data-kpress-prose-font` mark, so every other formula in them follows
its own text. The rule holds on every surface, walked formula by formula on the built
site: a card’s headline and note, a popover, a case’s visual summary, a table’s cells,
heads, summaries and disclosures, a caption, a footnote, a case record’s head, panels
and detail, a page’s subtitle, and a sans heading are sans text with sans math; prose
and its lists are serif with serif math.
A card’s headline and note are prose whose mathematical runs are set as math, so a case
a note names, such as $n = 21$, is sans math too, never upright words.
Documents write math as LaTeX (`$…$`) rather than in code spans;
`devtools.check_math_markup` holds the documents already migrated to it.
Code uses Planetaire Mono Text at KPress’s calibrated monospace size.

**A formula is drawn as its text is.** Beside the face, a formula takes the size of the
text it sits in (KaTeX’s outer em is 1 of its text’s on every surface), its colour, and
the regular weight of the composite it is set in: 400 in the serif, and in the sans the
410 of `--kpress-font-weight-sans-regular`, the weight KPress built the sans math tables
at. It is also rasterised as its text is, `text-rendering: auto`, with one exception.
The publication layer sets `text-rendering: geometricPrecision` on its formulas, because
the explainer’s prepared widths are measured in linear advances, and takes it back to
`auto` on macOS, where CoreText’s advances are already linear and Chromium draws a
`geometricPrecision` run lighter than the `auto` text beside it.
The stylesheet knows macOS by `data-squares-native-math-metrics`, which a head script
stamps on the root before the body paints (`explainer/native-math-metrics.js`). So off
macOS a formula of the two papers is `geometricPrecision` beside `auto` text, by that
rule, and on every other page of the site it is `auto` everywhere.

The stylesheet and the script are one layer.
The optimality paper once inlined the stylesheet without the script, so on macOS its
formulas stayed at `geometricPrecision`, and the same formula held 15 to 17% less ink
than on the explainer in the light theme and 23 to 26% less in the dark one.
No computed size, weight, face or colour differed between the two pages.
Both renderers now take the pair from
`render_n11_lower_bounds_explainer.publication_layer`, the paper’s renderer refuses a
value its shell has no place for, and the same formula’s ink on the two pages agrees
within 0.2%.

`devtools.measure_site_pages glyphs` is the measurement.
For every role of text and for the formulas of every surface it reports the face asked
for and the platform face the browser drew, weight, size, colour and how the glyphs are
rasterised, and for a formula its ink: the area its glyphs paint, in square em, on a
shot at twice its size.
`--view differences` lists every property a page sets differently from the explainer,
`--view problems` what a page sets off the rules of this section and of **Text**, and
`--style` adds one declaration to see what it changes, which is how the cause was
confirmed: with `text-rendering: geometricPrecision` alone added, three of the
explainer’s formulas held exactly the ink the paper’s did (0.5268, 0.1171 and 0.1215
square em), and with `auto` alone added the paper’s came within 0.2% of the explainer’s.
`tests/test_site_glyphs.py` holds the paper to the explainer property by property and by
ink, tells each paper it is on macOS and that it is not (the difference never shows on a
Linux runner otherwise), and names a paper whose head script is taken out.

## Shared Assets

The site’s pages link their design system rather than carry it.
Every page `render_overview.kpress_page` writes names the same stylesheets and scripts:
KPress’s stylesheets with their faces, KaTeX’s pruned stylesheets and faces, the
relation glyphs, `paper-type.css`, `site-nav.css`, `site.css` and `site-result.css`, the
math pipeline, KPress’s flattened client behaviors and the page’s own programs.
Inlined, they came to about 1.8 MB a page, 0.95 MB after gzip, and a reader’s browser
fetched them again on every page, since a page’s own bytes were all it could cache.

- **Where they live.** `devtools/site_assets.py` publishes each as a file under the
  site’s `assets/`, named by its content: `css/site.<hash>.css`,
  `fonts/pt-serif-latin-400-normal.<hash>.woff2`, `js/table.<hash>.js`, where the hash
  is the first sixteen hex digits of the bytes’ SHA-256 (KPress’s `content_hash`). A
  file’s name changes when its bytes do, so a cached copy is never stale, and a reader
  fetches each once for every page of the site.
- **How a page names them.** By a relative path from where the page is served:
  `assets/…` from the root, `../assets/…` from `cases/`. A stylesheet names its faces
  from beside itself, `../fonts/…`, so it reads the same from every page.
  `kpress_page` writes every address from the root, and `render_case_pages.rebase_links`
  moves a script’s `src` with every other link when a page stands in a directory.
- **What a page may fetch.** Its shared assets and nothing else to be drawn:
  `render_overview.assert_fetches_only_assets` refuses a script or stylesheet with any
  other source, a CSS import, and a `url()` in the page’s own text that is not a data
  URI or a fragment.
- **Faces.** Every face keeps `font-display: block`, so a face that arrives late holds
  the text it draws invisible, laid out in its fallback’s advances; the visible text
  around it moves when it arrives.
  The faces a page draws its first screen in, PT Serif’s regular, italic and bold and
  Source Sans 3’s upright, are declared beside the stylesheets
  (`site_assets.PRELOADED_FACES`). Emphasis counts: the frontier’s opening paragraphs
  set italic and bold PT Serif, and while those two waited for the layout that
  discovered them, their arrival moved the paragraphs by a CLS of 0.134 or 0.209 on the
  hosted runner. The two emphasis preloads add 64,484 bytes at high priority to every
  page, 34,896 for the italic and 29,588 for the bold.
  Only a reader’s first page pays: the files are shared and named by their content, so
  later pages read them from cache.
  Not every page draws them: measured in Chromium on 2026-10-09 across the twelve
  top-level pages at 390 and 1280px, `visualize.html` draws neither, `index.html`,
  `papers.html` and `cases/index.html` draw the italic but not the bold, and
  `readme.html` and `epistemics.html` draw the bold only below the first screen.
  A first visit that lands on one of those pages fetches a face early that it draws late
  or never. A per-page preload list in `site_assets.preload_tags` would remove that cost
  and is not built. A small prepaint program activates these hints with anonymous CORS on
  HTTP and HTTPS, and without CORS for local files; choosing the mode before requesting
  the fonts avoids WebKit’s file-origin cache failure while preserving shared HTTP font
  downloads. With JavaScript disabled, the same stylesheets load their faces normally.
  While regular PT Serif loads, the default prose stack uses metric-adjusted local
  Georgia or Times New Roman/Liberation Serif aliases to keep opening paragraphs stable.
  The delayed-face regression checks both fallback families, final PT Serif attribution,
  paragraph geometry and the existing layout-shift limit; saved sans and system choices
  retain their more specific stacks.
  A preload can still lose the race to the first layout.
  Source Sans 3 did on the runner, where its fallback is DejaVu Sans, about a quarter
  wider: at 390px a navigation link wrapped to the bar’s second line and the hero’s
  summary took two more lines, and their return was a CLS of 0.251. So on screen
  `paper-type.css`, which every page carries, puts a metric-adjusted local Arial
  (Liberation Sans on Linux) behind Source Sans 3, regular for its 410 and bold for its
  550 and heavier, with Source Sans 3’s ascent and descent and only its unicode range,
  so it stands in for nothing the shipped face draws once loaded.
  The fix is measured in Chromium only.
  `test_frontier_sans_arrival_keeps_the_navigation_in_place` runs there and fails up
  front, saying so, where neither Arial nor Liberation Sans is installed.
  WebKit is not covered: on the hosted WebKit runner `load()` on these local-only faces
  rejected (run 37888293870), so the explainer’s font probe skips them, and whether
  WebKit lays text out in them was not measured.
  Safari applies `size-adjust` from version 17, but by MDN’s compatibility data on
  2026-10-09 ships `ascent-override`, `descent-override` and `line-gap-override` only in
  Technology Preview, so there the alias would keep Arial’s own ascent and descent.
  The rest are fetched when a page first draws in them, and a face no page draws, a
  print instance, only when one prints.
- **What a build writes.** `render_overview.write_site` writes exactly the files its
  pages name, with the faces their stylesheets name.
  Each producer preserves other producers’ files and refuses different bytes at an
  existing content-addressed path.
  Producer checks compare their own files; the assembled-site check validates the
  complete output.
- **What the deploy checks.** `check_published_site`, live and with `--local`, holds
  every file a page names, and every face a named stylesheet names, to being served with
  the bytes its name was given for.
- **A page whole.** A tool or test that reads a page as one file, or opens it with
  nothing beside it, puts the shared files back in it: `site_assets.SiteAssets.inlined`
  from a render, `site_assets.inlined_from` from a built site.

Paper renderers retain self-contained output for offline tools.
Publication prepares math before `site_assets.link_inline_assets` extracts styles, fonts
and scripts; the lower-bound paper preserves all four measured font contexts.
A tool that loads a page without its directory uses `site_assets.read_inline_page`,
resolving resources from the page’s path.
Paper metadata includes the article title, credits, recorded publication and revision
dates, scholarly citation tags, and breadcrumbs.

The lower-bound paper has a specific 1,500,000-byte HTML allowance within the site’s
2,000,000-byte hard limit.
Its prepared publication measures 1,417,109 bytes: 187,933 bytes before preparation and
1,229,176 bytes for the measured math across four saved font preferences.
The 800,000-byte target applies to the other papers.
This exception keeps each font choice ready before paint without fetching primary
mathematical content.

The published workbench owns `workbench/assets/` and `workbench/data/`. Its corpus is a
separate content-addressed JSON file.
The loader checks the HTTP response and decodes the corpus before starting the
application; failures remain visible above the viewport.
Its policy permits same-origin resources and connections.
The favicon stays inline so the workbench artifact can run independently of the root
site. The candidate generator continues to produce one self-contained file.
Browser checks serve published output over HTTP, and the reproducibility check compares
every emitted file.
`devtools.measure_site_pages load --network fast-4g --after index.html` measures what a
reader’s second page costs; on 2026-10-04 it moved 1.0 to 1.3 MB on every page before
this change.

## Math Loading

Published pages carry complete mathematics in their initial HTML. Interactive
mathematics uses the explainer’s shared runtime:

- **Faces and styles.** KaTeX’s faces pruned to those a page can reach, inlined as data
  URIs for offline tools and linked from shared files in published pages, and switched
  from `font-display: swap` to `block`, so no formula is drawn in a host face and
  redrawn; KPress’s math composites; the three relation glyphs (`relation_face_css`).
- **Scripts.** `render_n11_lower_bounds_explainer.katex_js`: KaTeX, KPress’s metric
  tables and shared runtime, and the explainer’s host adapter, `squaresMath`
  (`probes/render_n11_lower_bounds_explainer/host_math_init.js`). KPress’s own entry
  points, `auto-render.min.js` and `katex-init.js`, are left out: `katex-init.js`
  typesets every formula on the page in one task at DOMContentLoaded.
- **Per-formula readiness.** The runtime lays a formula out hidden, waits for the faces
  its glyphs need, and reveals that formula alone; a formula whose faces fail keeps its
  readable fallback.
- **Batching.** `squaresMath.batch` submits sixteen formulas per task, so a formula that
  is ready shows while later ones are still being submitted.

The lower-bound paper also measures formula geometry in four font contexts with pinned
Chromium; its publication command always prepares the formulas, and `--prepare-math`
remains accepted for existing callers.
Its client hydrates those boxes and puts interactive panels first in the queue.
The other papers and ordinary content pages use `site_math.prepare` to render visual
KaTeX beside semantic MathML without launching a browser.
Their prose, captions and headings select the matching serif or sans math profile.
The published papers and content pages remain readable with JavaScript disabled.
Dense frontier table cells display exactly their existing semantic MathML, once per
formula, under `data-site-native-math="frontier"`; they omit the visual KaTeX spans.
The page’s prose still uses prepared KaTeX. Native MathML structures and operators use
the platform’s math font.
The text tokens (`mi`, `mn`, `mtext`, and `ms`) use the table’s sans reader font on
screen and in print.
The browser readability check requires a visible, nonempty MathML subtree in each marked
cell, under the ordinary load and layout budgets.

Interactive formulas use the shared runtime.
A formula whose faces miss the runtime’s wait is retried twice after the page and its
fonts load, and the paper marks completion with `math-ready`. The review papers retain
their runtime for browser and print tools (`render_n11_optimality_review.math_scripts`).
A formula that asks for a face the page does not ship keeps its MathML, and the paper’s
PDF refuses to print with a formula untypeset.

In the client-runtime measurements below, each client layout cost a style pass over the
whole document, 6ms a formula on the synopsis against 0.9ms with KPress’s
`:has(.kpress-toc)` layout rules removed: those selectors made every change inside the
column re-match the page’s grid.
Those measurements concern client typesetting; published prose uses prepared math.

`devtools.measure_site_pages load` measures a built site in cold Chromium contexts
(median of three loads, milliseconds from navigation start; “visible math” is the first
frame at which every formula in the first viewport is typeset and showing, “blocking”
the long tasks’ time over 50ms). The historical client-runtime comparison below uses
`3e8274909` as its before-build and the shared runtime as its after-build:

| Page | Width | DOMContentLoaded | Visible math | Load-time math done | Longest task | Blocking |
| --- | --- | --- | --- | --- | --- | --- |
| `papers/n11-lower-bounds-explainer.html` | 1280 | 712 → 993 | 727 → 1,008 | 947 → 1,238 | 132 → 128 | 211 → 263 |
| `tutorial.html` | 1280 | 2,233 → 594 | 2,235 → 595 | 2,458 → 741 | 1,875 → 198 | 2,101 → 182 |
| `synopsis.html` | 1280 | 14,040 → 1,089 | 14,704 → 1,668 | 14,704 → 1,758 | 13,002 → 847 | 16,123 → 1,179 |
| `results.html` | 1280 | 568 → 236 | 600 → 387 | 600 → 387 | 82 → 75 | 32 → 25 |
| `readme.html` | 1280 | 608 → 233 | 642 → 297 | 642 → 322 | 74 → 98 | 28 → 48 |
| `index.html` | 1280 | 3,331 → 686 | 3,595 → 811 | 3,595 → 903 | 2,152 → 152 | 2,507 → 219 |
| `cases.html#n-11` | 1280 | 7,958 → 5,362 | 8,106 → 5,386 | 8,106 → 5,509 | 3,773 → 2,399 | 7,247 → 4,130 |
| `papers/n11-lower-bounds-explainer.html` | 390 | 696 → 1,156 | 710 → 1,171 | 932 → 1,421 | 121 → 128 | 205 → 263 |
| `tutorial.html` | 390 | 2,336 → 651 | 2,338 → 652 | 2,541 → 743 | 1,924 → 191 | 2,163 → 175 |
| `synopsis.html` | 390 | 14,969 → 1,361 | 15,657 → 1,363 | 15,657 → 1,525 | 13,922 → 326 | 17,132 → 880 |
| `results.html` | 390 | 166 → 190 | 214 → 240 | 214 → 240 | 79 → 87 | 29 → 37 |
| `readme.html` | 390 | 213 → 202 | 278 → 276 | 278 → 285 | 75 → 79 | 29 → 29 |
| `index.html` | 390 | 2,455 → 775 | 2,687 → 855 | 2,687 → 897 | 1,940 → 236 | 2,198 → 248 |
| `cases.html#n-11` | 390 | 8,118 → 5,100 | 8,266 → 5,190 | 8,266 → 5,275 | 3,925 → 2,566 | 7,416 → 3,810 |

“Load-time math done” is the frame at which every displayed formula is typeset or, on a
page that defers the rest, the frame that page marks `math-ready`. The explainer’s own
output changed only by its stylesheet, so its row is the run-to-run noise of the shared
host the two runs were measured on, a few hundred milliseconds; an earlier run of the
same after-build measured it at 705 to 743ms. The `cases.html#n-11` rows are the case
records as they stood until 2026-10-03, every record on one page.
`measure_site_pages load` now opens the record page, `cases/index.html#n-11`, in their
place, and this table has no row for it yet.

That one page was slow before any math ran: it carried every case’s record in one 9MB
document, and parsing and styling that took several seconds on its own (think-cy3a). The
record page carries the index alone, 1.9MB, and fetches the one record a reader asks for
(**Case records**, below).
Ordinary content pages now prepare their visual math at build time with
`site_math.prepare`, without a browser; these historical timings do not measure that
publication contract.

## Spacing

The vertical space between a page’s blocks is set on screen by a few tokens, each
declared once and read wherever that space occurs.
Print keeps KPress’s spacing and the paper’s, so the explainer’s PDF does not move when
one of them changes.

| Space | Token | Screen value | Declared in |
| --- | --- | --- | --- |
| From the bar’s rule to a page’s first block, or from the section tabs where a page has them | `--site-page-top` | 4rem, 64px | `site-nav.css` |
| From the bar’s rule to the section tabs, and from them to an application | `--site-tabs-space` | 0.7rem, 11.2px | `site-nav.css` |
| How much nearer the bar an opening picture starts | `--site-hero-lift` | 0.5rem, 8px | `site.css` |
| Above a section heading (`h2`) | `--paper-section-space` | 2.7 of the prose base, 48.6px | `paper-type.css` |
| Below a section heading (`h2`) | `--paper-section-space-below` | 1.7rem, 27.2px | `paper-type.css` |
| Below a page’s title, and below its subtitle | `--site-subtitle-space` | 1.5rem, 24px | `site.css` |
| Above and below a table | `--site-table-space` | 2rem, 32px | `site.css` |
| Between a wide block and the edge of the page’s content area | `--site-wide-gutter` | 0.5rem, 8px | `site.css` |

A page’s title, or the picture that opens the homepage, starts `--site-page-top` under
the bar’s rule on every page, the explainer and the optimality paper included.
The film’s page has section tabs under that rule, and its film starts the same space
under the tabs. Every section heading on the site pages and the explainer takes the two
section tokens; print reads its own values of both (2.8 of the base and 1.3rem), which
are the paper’s. On the explainer the credits start 2.25rem under the title on screen
and 2rem in print.

`--site-table-space` is the space above and below every table, and above and below the
rating ladders. A site table (`.site-table`) takes it above its filter bar, which keeps
its own 0.5rem to the table, and below its wrap; and a document’s own table, which
KPress wraps and already sets 2rem from the text, reads the same token, so one value
moves every table on the site.
Where a larger margin meets it, as a section heading’s does below the disclosure, the
larger one stands.

`--site-wide-gutter` is the least space between a wide block and the edge of the page’s
content area: a table with its filter bar, a row of cards, the atlas grid, the film.
The content area is the page inside its margin, which is where KPress clips a narrow
page, and its width is KPress’s page container’s, `100cqw`. A wide block’s room is that
width less the gutter on either side (`--site-wide-room`), and the wide track, a table’s
bleed and the film all stop there.
The gutter is KPress’s own document gutter, so a wide block with no room to spare is
exactly as wide as the text: 40 pixels from either edge of the window between 768 and
about 1180 pixels wide (1456 for the Frontier page), and 16 on a phone.
The room is never measured from the window.
`100vw` counts a scrollbar that the layout does not, so a block sized from it ran 16
pixels under the document’s clip at 768 pixels, and 7.5 more with a scrollbar, cutting
the first letters of the filter labels and the end of the count.
Nothing that scrolls sideways gives the gutter up either: in KPress’s narrow band a
document’s own table keeps to its column and scrolls inside its wrap, where KPress would
run it under the clip, and a result overview’s bounds scroll inside their own box rather
than past the popover’s margin.
On a phone a results table’s row cards are padded 0.5rem at the sides.
`devtools.preview_site` fails a build on any wide block that runs past an ancestor which
clips or scrolls sideways (`--clips`, and with `--shots`), at 1024, 768 and 390 pixels,
as laid out and again with a scrollbar’s 15 pixels taken from the layout;
`tests/test_site_wide_blocks.py` holds the pages to none.

`devtools.measure_site_pages space` measures these on a built site: the white space
above and below every table and heading, in pixels between boxes, at each width asked
for, with each heading’s size and line height, and each table’s distance from the
window’s edges or its popover’s. `tests/test_overview.py` pins each token’s value and
the rule that reads it.

## Site Components

Each component is defined once in [site.css](site.css) and used on every page that needs
it.

- **Navigation bar.** One fixed-width row of sans links in the page’s header slot, the
  same on every page, the explainer and the workbench included, led by the site name,
  “Square Packing”, set in capitals by CSS (`text-transform`, lightly tracked) so its
  text is unchanged, and a step heavier.
  The bar’s type is tied to the body’s on the scale above (Typography Roles), never set
  in pixels or rem. A link, and a section tab, is one step under the 18px prose and no
  more: the caption size, 0.92 of the sans base, 17.48px, which is the first size of the
  scale under 18px (`--site-nav-font-size`; the step between, 0.95, is 18.05px, not
  under the prose). The site’s name is the sans base, 19px (`--site-nav-name-size`), the
  size sans text takes beside the prose, so with its weight and capitals it reads as the
  name. Both tokens are in `site-nav.css` and are computed from the host base
  (`--kpress-host-font-size-base`), which is the same on every page, so the bar is one
  size on every page and at every width.
  `devtools.measure_site_pages header` reports the four sizes, `preview_site` fails a
  page whose bar is not one step under its body (`type_problems`), and
  `tests/test_site_wide_blocks.py` holds the relation in a browser at 1280, 768 and 390
  pixels, where the links keep one line, one line and two lines.
  Case 11, the site’s icon, sits before the name as its mark, 18px square, inside the
  same link, so it takes the same hover.
  The name’s text stands on the links’ baseline.
  The bar aligns its items by their baselines (`align-items: baseline`), and the name is
  a row of its own, the mark and the text, whose baseline would be its first item’s, the
  foot of the mark; so the text is the one item of that row aligned by its baseline
  (`align-self: baseline`), which makes the row’s baseline the text’s, at any size of
  either, with no offset in pixels.
  The mark stays centred on the name’s line.
  Every item of the bar is set on one line, `--site-nav-line`, a length (1.43 of the
  link size, the face’s own leading there), so the larger name is no taller than a link:
  the links stand where they do without the name, and the current link’s underline is
  the same distance over the rule at every width.
  `devtools.measure_site_pages baselines` reports each label’s baseline, measured with a
  zero-size inline box on the text’s line and not read from a box’s edge; `preview_site`
  fails a page whose name or links are off by more than half a pixel
  (`baseline_problems`); and `tests/test_site_wide_blocks.py` holds it in a browser.
  Narrower than 56rem, where the bar with the name would wrap, the name gives way and
  the mark alone leads home, labelled “Square Packing home” for a screen reader.
  Every item takes the cards’ gentle wash on hover and nothing underlines on hover; the
  current page alone is underlined in the accent.
  The edition appears only in the closing credit (below).
  Every page renders it from the one partial, `site-nav.html`, and it has the same box
  on every page at every width.
  The shared Headroom carrier is sticky and preserves its place in the document.
  Scrolling down hides it; the first meaningful upward scroll shows it again.
  It stays visible at the top, while navigation has focus, and while the theme menu is
  open. Resize and anchor navigation account for the full carrier height, including tabs;
  reduced motion disables animated travel.
  `overview/headroom.js` handles ordinary, static-content, paper and Workbench shells
  once (`think-byu7`). The bar sits 1rem below the top of the window on every page, the
  explainer and the workbench included: `site-nav.css` narrows KPress’s page top margin
  (`--kpress-page-margin-block-start`) from 2.5rem. Below the bar, every page’s first
  block starts one shared space under its rule, `--site-page-top` (4rem, in
  `site-nav.css`): KPress’s document padding above the column is dropped on screen, the
  column’s own top padding is the token, and the first block (a hero or a document’s
  title) adds no margin of its own.
  A page that opens on a picture, the homepage’s packing, starts it `--site-hero-lift`
  (0.5rem) nearer the bar, since a drawing has no line spacing above its edge.
  On the explainer the source chips sit in that space and the title starts the token
  below them. Print keeps KPress’s spacing, so the explainer’s PDF does not move.
  Its entries are Overview, Results, Papers, Frontier, Visualize and GitHub, in that
  order on every page: the order is the partial’s, `site-nav.html`, which is the one
  place it is written, and it is the keyboard’s order too.
  On a phone, where the links take two lines, the first holds Overview, Results, Papers
  and Frontier and the second Visualize, GitHub and the gear.
  Papers leads to the papers page (`papers.html`) and is current on it and on both
  papers, the explainer and the tutorial, which keep their own addresses.
  Visualize leads to the film (`visualize.html`) and is current on both pages of the
  Visualize section, the film and the workbench.
  The workbench is an application rather than a KPress page, so its build
  (`workbench_tools.build_site`) takes the bar, its stylesheet, the theme bootstrap and
  the gear’s script from `render_overview.nav_shell`, in a shell that gives it the page
  margins and header rule KPress gives the others; the application fills the window
  below it. Only the bar and the section tabs follow the theme there: the workbench
  itself has no dark mode yet.

- **Section tabs.** A section that spans pages carries one small tab bar under the
  navigation bar; the Visualize section is the one that does, with two tabs, **Film**
  (`visualize.html`, the section’s first page) and **Workbench** (`workbench/`). Each
  tab is a real link to its own page, so the bar needs no script, and a tab can be
  opened, bookmarked and shared; every existing `workbench/` address lands on the
  Workbench tab. The bar is a centred strip with square corners and the cards’ thin
  border, a hairline between tabs, in the bar’s sans at the links’ own size
  (`--site-nav-font-size`) and medium weight: a tab is gray, takes the nav items’ wash
  and accent on hover, and the current tab is filled with a 16% accent tint over the
  page background in the page’s own text colour.
  It is `.site-tabs`, rendered by `render_overview.visualize_tabs`, and defined in
  `site-nav.css` rather than `site.css` because the workbench carries only the bar’s
  stylesheet. On the film’s page it opens the document; on the workbench it sits in the
  application shell under the bar, above the application.
  The same strip also switches a view in place: there it is a `tablist` of buttons
  (`role="tab"`), each stripped of a button’s own chrome and taking the strip’s type,
  the selected one filled as the current page’s link is.
  The dedicated Atlas uses it for its Grid and Triangle views (**Atlas views**, below)
  and for its Small, Medium and Large tiles (**Atlas sizes**, below); `site-nav.css`
  draws both forms, and the header rules above take only the `nav` strip.
  From the top, both pages read bar, rule, tabs, content: the tabs stand under the rule
  that runs under the bar, never over it.
  They are in the header slot, whose lower border is that rule, so a header that holds
  tabs gives up its border and the bar draws the rule at its own foot (`:has()`, in
  `site-nav.css`), where it is on every other page and as long.
  The tabs start `--site-tabs-space` (0.7rem, 11.2px) under the rule.
  On the film’s page the first block starts `--site-page-top` under the tabs; on the
  workbench, where the application starts at the shell’s lower edge, the tabs keep the
  same 0.7rem below them.
  Measured at 1280px, on both pages: the bar from 16 to 67.6px with the rule its last
  pixel, the tabs from 78.8 to 115.4px, then the film at 179.4px and the application at
  126.6px; at 390px, where the bar wraps to two lines, the rule ends at 84.8px, the tabs
  run from 96.0 to 132.6px, the film starts at 196.6px and the application at 143.8px.
  `devtools.measure_site_pages header` reports these, `preview_site` fails a built page
  whose tabs start over the rule (`tabs_problems`), and `tests/test_site_wide_blocks.py`
  holds both pages to it in a browser.
  It is hidden in print and in the embed view.

- **Theme control.** A small gray gear, an inline SVG, ends the navigation bar on every
  page, the explainer and the workbench included.
  It follows GitHub within the centered navigation track at every width.
  Its SVG is centered on the navigation font’s capital height; its wrapper shares the
  text baseline. It takes the nav items’ wash on hover and while its menu is open, and
  never underlines. Pressing it opens a compact menu, a native popover under the gear
  with square corners and the cards’ border and shadow, of three choices, each an icon
  and a word: System, Light and Dark.
  The current choice is in the accent with a check at its end.
  Choosing applies at once, closes the menu and keeps the choice across pages and
  visits; the menu also closes on Escape, an outside click or tabbing away.
  The gear is a button named “Color theme” with `aria-haspopup="menu"` and
  `aria-expanded`; the menu is a `role="menu"` of `menuitemradio` items carrying
  `aria-checked`, and the arrow keys, Home and End move between them.
  On a phone the whole bar wraps onto centred lines, so every link stays in view, and
  the gear ends the last line.
  The choice is KPress’s own reader preference, the `kpress.theme` key its head
  bootstrap applies before first paint, so no page flashes the wrong theme and every
  stylesheet keys only on `data-kpress-resolved-theme`, never on `prefers-color-scheme`.
  System follows the operating system as it changes.
  The embed view has no navigation bar and so no gear, and a framed page follows the
  choice its parent makes, live.
  `overview/theme.js` is the script, and it announces a change as `squares:themechange`
  for anything drawn on a canvas.
  Adapted from metabrowser’s settings gear, reduced to one chooser with words beside its
  icons.

- **Closing credit.** Every page with a footer ends on the same two centred lines:

  > The Squares Project · github.com/jlevy/squares\
  > v0.4.2-8ac5de · Formatted and typeset with Flowmark and KPress

  The first is the project’s formal name and its repository, shown without its scheme
  and linked. The second is the version and the credit to the two tools, each linked to
  its project. The version is never typed: it is `sqpack.release.PUBLICATION_EDITION`,
  the stamp the atlas footer and the film print (the edition’s semver core and the first
  six characters of the pinned data revision, with the edition’s status ahead of it
  while it has one), so it follows a re-pin and a new edition with no edit.
  One function writes the lines, `render_overview.colophon_lines`: the site’s pages set
  them in KPress’s footer slot as `.site-colophon` (`colophon_html`), and the explainer
  and the optimality paper in their own closing paragraph, `.colophon`, which keeps each
  paper’s type and print rules, so both lines print at the end of each PDF. The
  workbench is an application that fills the window and has no footer; its stage prints
  the same version. A middle dot with a space either side parts a line.
  There are two lines at every width: a line is a block (`.site-colophon-line`), and
  each part beside a dot an inline block (`.site-colophon-part`), so on a phone a line
  breaks at its dot, and a part wider than the page breaks into balanced rows.
  Both rules are in `site-nav.css`, the stylesheet every page carries.
  The type is quiet: the sans face at the colophon scale (0.85 of the sans base,
  16.15px) in the support colour on a site page, KPress’s tiny size in its muted colour
  on a paper; the links take the page’s link colour, and all of it follows the theme.
  A build that prints the version names `release.py` among its declared inputs, as the
  workbench’s does, so a re-pin puts every such page in the Pages workflow’s scope
  (`devtools.pages_scope`); nothing compares a page’s bytes with an earlier build’s.

- **Homepage.** A short problem introduction and a centered **The Squares Project** card
  open the page; the card leads to `about.html`. The next sections are Atlas, Recent
  Major Results, Papers, PDFs, Video, Squares Project Documentation, then More Resources
  (`think-5c8r`, `think-sq1i`). Papers shares all reading cards with the Papers page;
  Squares Project Documentation shares its introductory text and cards with About.
  The PDF downloads and inline video player remain separate sections.
  The introduction has two readable paragraphs defining the packing problem and
  explaining upper/lower bounds (`think-8xzs`). About uses only H1 section headings,
  each with the same `site-title` styling as The Squares Project (`think-6m9n`,
  `think-sq1i`). Main homepage headings share the H1 title style and have an extra
  0.5rem of space above the shared section spacing; the compact Legend label keeps its
  own spacing. The hero graphic opens the case popover, with the case-record link as its
  no-script fallback. Case popovers offer separate record, Frontier-row and Atlas-tile
  actions. Atlas case targets fully expand the grid before scrolling to and highlighting
  the requested tile. Every row containing one card is centered.
  The full project narrative and attribution live on About; documentation cards also
  appear on the homepage; **About** sits immediately before **GitHub** in the shared
  navigation.

- **Page headings.** The homepage opens with “The Square Packing Problem” as its `h1`,
  followed by section `h2`s. The Visualize page shows no title: the bar, the section
  tabs and the film are the page, and its `h1`, “Visualize”, is for a screen reader
  alone (`.site-visually-hidden`, in `site.css`: out of the flow, one pixel, clipped,
  the class for any block a reader does not see and a screen reader should).
  The film after the hidden title is the page’s first block, so on screen it brings no
  margin above and starts `--site-page-top` under the header.
  A page that has a title (the Frontier page, the Results page, the Papers page, the
  canonical case record) sets it in the hero, centred.
  The Frontier page’s title is “The Frontier Survey”, the Results page’s “Every Result”
  and the Papers page’s “Papers”; each stood over a subtitle the owner dictated on 1
  October (“A survey of everything known for cases $n = 1, \ldots, 324$”, “A survey of
  all reviewed results”, “Papers and interactive explanations for specific results”) and
  dropped on 2 October as adding little (`think-wz9d`); the page descriptions in each
  `<head>` are their own constants and stay.
  Individual case pages use their own case heading; the Atlas replaces the former
  separate case-directory hero and index (**Case records**, below).
  A subtitle, where a page has one, is the sans face at 1.1 times the sans base
  (`--site-subtitle-scale`, about 21px), in the page’s own text colour, never gray, with
  the same space above it and below it (`--site-subtitle-space`, 1.5rem). A title with
  no subtitle, a document’s own `h1` among them, stands that space above its first
  paragraph. The page title style (every hero `h1`, and `.site-title`) is the sans face
  in upright caps (not KPress’s italic `h2`) at 1.5 times the sans base, centred.
  The homepage’s first section, The Square Packing Problem, takes it through
  `.site-title`, so it reads as the Frontier page’s title does.
  That section opens with README’s two opening paragraphs: the block between README’s
  `project-intro` markers, read at render time and its links rewritten for the site
  (`site_documents.overview_intro`), so it is edited in `README.md` and nowhere else.
  The site’s own statement follows under its own section heading, The Square Packing
  Project, an ordinary `h2` like the sections after it, and is the only prose the
  template holds there.
  README’s next two paragraphs, what the project covers and its newest major result,
  were a second shared block, `recent-progress`, that opened Recent Results until
  2026-10-02; that section is one paragraph of the template’s own now (**Recent
  results**, below), and README keeps its fuller account unshared, since a shared block
  must read the same in both places and the two are meant to differ.
  `devtools.check_readme` holds the one block: marked once, prose alone with no heading
  or comment, and no case called the central one.

- **Heading leading.** Every heading is set at one line height, 1.15
  (`--paper-heading-leading`, in `paper-type.css`), on screen: a page’s title (an `h1`,
  or the homepage’s `.site-title`), its subtitle, every section heading (`h2` to `h6`)
  on the site pages, the explainer and the optimality paper, a card’s headline
  (`.site-card-value`), a popover’s (`.site-popover-value`, which a row’s popover and
  the $n$ over a result overview’s case use too), a case record’s title and a column’s
  name in the rating ladders.
  Body text, table cells, notes and the small caps labels (a card’s label, a result
  overview’s section label) keep their own line heights.
  The explainer’s hero title keeps KPress’s 1.05, which its prepared math is fitted to,
  and print keeps KPress’s leading, so the explainer’s PDF does not move.
  A formula in a heading or headline takes no line of its own: KPress’s inline math box
  (line height 1.4) and KaTeX’s (1.2) are both set to zero there, so a formula is as
  tall as KaTeX’s struts make it and the line that holds one is no taller than its
  neighbours. A headline’s box carries the room the looser line used to give it as margin
  (0.2rem above and 0.3rem below a card’s, 0.5rem and 1rem a popover’s).

- **Names.** The page at `atlas.html` and its navigation entry are **Atlas**. It
  contains the graphical grid, followed by **The Frontier Survey**: the complete record
  of every case with reported and verified bounds.
  A **Frontier Row** action reaches `#n-N` in the survey table; an **Atlas Tile** action
  reaches `#atlas-n-N` in the fully expanded graphical grid.
  The homepage preview, posters and film also draw from the Atlas.
  Legacy `frontier.html` and `status.html` URLs forward to Atlas while preserving their
  query and fragment. The homepage’s former survey fragments, `#the-frontier-survey` and
  `#the-survey`, reach the survey section on Atlas.

- **Report layout.** Every report page (the tutorial, the synopsis and the other
  documents) has one layout.
  A long report gets a contents rail and a short one does not, by kpress’s own rule
  (seven headings and 800 words), so the choice is never made per page.
  Either way the reading column is centred.
  A document’s own hand-written contents list, which GitHub needs and the site does not,
  is dropped from its page, so the rail never repeats it as an entry.

- **Document pages with contents.** On a wide screen the contents rail stays at the left
  edge and the reading column is centred on the page, under the centred navigation.
  Where the pane is too narrow to centre, the column sits as near centre as the 15rem
  rail allows. The rail is plain text: no frame, only the underlined Contents label, and
  entries that change colour on hover or when current, with no fill or side bar.

- **Site icon and hero.** Both are atlas drawings, reduced to each square’s outline and
  fill. The icon is case 11, Trump’s packing of eleven squares, in the atlas ink on
  white, inlined as a data URI on every page, the workbench included; the same drawing
  is the mark in the navigation bar, drawn there in the bar’s ink, so it is light in
  dark mode. In both, the container’s frame is exactly one pixel of the drawing at its
  size (16px in a tab, 18px in the bar; `packing_svg(frame_px=)`), its outer edge on the
  drawing’s edge and snapped to the pixel grid, so the container reads as a square: one
  crisp pixel on a 1x screen, two on a 2x screen.
  Its squares’ outlines are half that pixel, one device pixel on a 2x screen, so each
  square stays distinct at icon size; the page’s drawings keep their hairline.
  The homepage hero shows one centered native packing for 53 squares (`think-h3ms`). It
  opens that case’s popover, with its canonical case-record link as the no-script
  destination. Its caption reads: “Best known packing for 53 identical squares.
  Colors indicate angle.
  Darker colors mean more common shared faces.”
  The introduction and project card follow the hero.

- **Cards.** A card is a summary with square corners, a thin border, a caps label, a
  value and a supporting note.
  A card section is one wrapping row in the wide track, in a `.site-cards-frame` the row
  measures itself against.
  Any line the cards do not fill centres on it, at every width: four cards on a wide
  screen, a section of three, and the last line of a long section alike.
  A card’s popover is its sibling in the row’s markup but never in the row, since a
  closed popover is not displayed and an open one is in the top layer.
  Print keeps the plain grid of medium columns, filled from the left.
  Cards come in three sizes (Card sizes, below).
  The value is the card’s headline: the sans face at the medium weight
  (`--site-font-weight-sans-medium`, 550), the face and weight of the page title and of
  the sans section headings (`h3`), at 1.15 of the text size (20.7px) and at the
  headings’ leading (**Heading leading**, below), so a headline of two or three lines
  reads as one block. The popover repeats the headline in the same face, weight and
  leading. A card works one of two ways.
  A popover card (`card`) is a button that opens a popover showing where it leads, and
  the popover ends in one button that goes there, centred at its foot.
  A direct card is instead itself the link (`link_card`), an `<a>` with no popover.
  **A card whose target is a full page of the site navigates.** The overview’s five page
  cards, the optimality paper, the explainer, the tutorial, the workbench and the
  Frontier page (**Overview sections**, below), and the Papers page’s three paper cards
  lead to full pages the site serves, so each is a direct card that goes to its page in
  the same tab (`new_tab=False`), with the right arrow for its icon (`data-go="page"`)
  and nothing framed (`think-bc5d`, `think-w82r`). Popovers are for records, targets
  that are not site pages of their own: a result, a case, a repository document rendered
  for its card’s popover.
  A direct card is a link and holds no other link, so what its note names is linked from
  the prose beside it.
  **Every other direct card opens its target in a new tab** (`target="_blank"`,
  `rel="noopener noreferrer"`), so the page the reader chose it from stays where they
  left it: a poster’s PDF, the Visualize page, another project.
  `link_card` refuses `new_tab=False` for anything but a page the site serves, which one
  rule decides (`overview_sections.is_site_page`): an entry of
  `render_overview.SITE_PAGES`, the optimality paper among them, or a directory served
  by its `index.html`, as `workbench/` and the record page, `cases/`, are.
  A case’s record file is no such page: it is the record alone (**Case records**,
  below).
  - When a popover card leads to a repository document the site renders, the popover
    renders that page itself, narrow, in a frame: the page at the same address with
    `?view=embed` added before any fragment, so a filtered view such as
    `atlas.html?recent=true` or a case such as `atlas.html#n-11` arrives as it will be
    seen. The embed view drops the navigation bar and sends every link out of the frame
    to the full window. The button is **Expand**, which opens the page at full size; a
    repository document also offers its source “On GitHub”, which opens it on `main`.
    Every repository link on the site names `main`, never a commit, and is made by
    `devtools/repo_links.py`; the optimality paper’s citations are the one exception
    (**Papers page**, below).
  - When the card leads to another project off the site, it is a direct card.
    It shows the address under the note beside the host’s mark (GitHub’s for a GitHub
    URL, otherwise the site’s favicon where one is saved under
    `devtools/overview/favicons/` by host and inlined, since a page fetches nothing but
    its shared assets, and a globe, `WEB_MARK`, where none is), and opens it in a new
    tab. An other project’s card ends with its tally of results (**Card foot** and
    **Other projects**, below).
  - When the card leads to a poster’s PDF or to the Visualize page, it is a direct card
    headed by the picture it opens (below).
    A PDF card is typed `application/pdf` and never marked `download`, so the browser
    opens it in place.
  - When the card leads to a row, the popover previews the row, read from the same
    record: a result’s claim, why it matters, its rungs and records.
    A result’s row is on the results page, so its card is a page card, with the right
    arrow for its icon, that previews rather than frames: the button, **Open T-NNN in
    the results table**, goes to `all-results.html#t-nnn`. A row on the overview itself
    would scroll, with the down arrow.

  The frame loads only when its popover first opens, so the overview stays light.
  The popover is a native `popover` panel with square corners over a faint scrim, set in
  sans, closed by its `×`, by Escape, or by a click outside, and it works without
  scripting. A card, popover or direct, gains a gentle wash on hover.
  Every popover has the same margin on all four sides, `--site-popover-pad` (1.75rem;
  1.1rem on a phone). Its `×` is a 2.75rem square tap target (`--site-popover-close`) set
  0.6rem in from the corner (0.25rem on a phone), washed on hover.
  Only the first block after it keeps clear of it, so the margins stay even everywhere
  else. A popover’s height has one limit, the window’s: `--site-popover-max-block`, the
  window’s height less `--site-popover-window-margin` above and below, which is 4% of
  that height and never under 1rem nor over 3rem. A card’s or a row’s popover, the case
  popover and a result overview may be that tall and scroll inside past it, each as one
  panel; a framed page is that tall, and its frame scrolls.
  A popover is centred, so the two margins are equal.
  No popover stops at a fixed height, so a taller window shows more: the case popover is
  828, 1104 and 1344 pixels tall in windows 900, 1200 and 1440 pixels tall, and shows
  27%, 36% and 44% of the record for $n = 79$ (`devtools.measure_site_pages popover`,
  2026-10-03). Until that day it framed the one page of every record, at the same
  heights, and its frame showed 21%, 30% and 38%; before the limit was the window’s it
  stopped at 792, 896 and 896 pixels and showed 20%, 23% and 23%. The limit is declared
  as `max-block-size` alone, since `max-height` is the same property and the later of
  the two in a rule is the one that holds.
  A phone, up to 40rem wide, keeps the heights it had: a card’s or a row’s popover up to
  80% of the window and 40rem, a framed page 88% and up to 56rem, and the case popover
  and a result overview the window less half a rem above and below.
  Its gray corner icon and the popover’s button both show where the button goes: down to
  a row on this page, external off the site, right to another page of the site (Arrows,
  below).

- **Card sizes.** A card is sized by its text, in three sizes it names in
  `data-card-size`; a card that names none is medium.
  Each size is as wide as a column of the grid of its own minimum column the frame fits,
  with 1rem gaps, so cards of one size line up as a grid at every width:
  - `small`, 12rem columns, for a headline and one line, under 80 characters: four to a
    line at 1280 pixels (264px each), four at 1024 (236px) and three at 768 (235px).
  - `medium`, 16rem columns, for a headline and a sentence, 80 to 159 characters: four
    to a line at 1280 pixels (264px), three at 1024 (320px) and two at 768 (360px).
  - `large`, 21rem columns, for a paragraph or a list, 160 characters or more: three to
    a line at 1280 pixels (357px), two at 1024 (488px) and two at 768 (360px).

  On a phone every card takes the whole line.
  The count to a line is `--site-cards-small`, `-medium` or `-large`, each stepped by
  its own container queries: n columns of minimum m and n − 1 gaps need (m + 1)n − 1
  rem, so medium steps at 33, 50 and 67rem and small at 25, 38 and 51rem. No size sets
  more than four cards to a line (the owner, 2026-10-05), so medium stops at four, small
  at four and large at four.
  A section declares one size for all its cards, in `SECTION_CARD_SIZES`
  (`overview_sections.py`), so its lines are one grid; the size is the one its typical
  card’s text asks for, the median card’s, which for an even count is the mean of the
  two middle lengths, and `tests/test_overview.py` holds the two together.
  The page cards, the atlas cards and the other projects are medium; the documents,
  whose notes are a line, are small.
  A section can also be set in lines of its own, in `SECTION_CARD_LINES`, where one
  wrapping row would not set its cards as they are meant to read: the six page cards
  stand one, three and two, the Frontier page alone at the top, then the three parts of
  the $n = 11$ series in reading order, then the tutorial and the workbench.
  Each line is a grid of its own in the section’s one frame, a gap below the line
  before, and none sets more cards to a line than the longest line holds
  (`data-cards-most`, at which the stylesheet caps its size’s count), so the lines share
  one column width and each centres in it: three medium columns at 1280 pixels, the
  Frontier page’s card centred over the papers.
  Wherever the frame fits two medium cards, from 33rem, every line stands as set; on a
  phone every card takes the line.
  The owner asked for the page cards in two rows on 2026-10-02 (`think-ec5k`), and two
  over three was chosen over three over two from screenshots at 1280 pixels; later the
  same day the owner set the Frontier page’s card on a line of its own at the top and
  the rest two and two (`think-ns3d`); the third paper made the line of papers three on
  2026-10-05 (the series plan).
  A card built without a size (`card()` or `link_card()` with no `size=`) takes the
  default for its own text: its headline and note, and a direct card’s address, counted
  as they read, a formula once.

- **Card foot.** A direct card may end with a line that holds links of its own
  (`link_card(foot=)`), as an other project’s card ends with its tally of results.
  A link cannot hold a link, so such a card is a box, `div.site-card.site-card-footed`,
  around the card’s link (`.site-card-main`, everything above the foot) and the foot
  (`.site-card-foot`), inside the one border.
  The box takes the card’s size and place in its row, and washes and shows its corner
  icon while its link is hovered or focused, so it reads as every other card does.
  The foot is set in the sans face at the note size in the support colour, at the card’s
  lower edge, so the feet of a row line up; its links take the page’s link colour.
  A card with no foot stays the link itself.
  The cards’ widths, rows and centring are the same with a foot as without
  (`measure_site_pages cards`, at 1280, 1024, 768 and 390).

- **Other projects.** The overview’s Other Square Packing Projects section leads with
  three websites, the catalogues of the record packings, in the order `CATALOGUE_SITES`
  writes them: David Ellsworth’s Squares in Squares (the record’s `[Kingbird]`), Erich
  Friedman’s original page at the archived address the catalogue links, and Evan
  Daniel’s Square Packing Atlas (the owner, 2026-10-05). Every other card, a repository
  on GitHub (`OTHER_PROJECTS`) or a place off it the record cites results from
  (`OTHER_SITES`: posts, a release, a Zenodo record), follows them, ordered by the
  significance of the results the register cites from each project (the owner,
  2026-10-01): by how many of its results stand at S5, then at S4, and so on down the
  scale, more first at each level and compared in that order, so one result at S5 stands
  before any number below it.
  Projects level on every count stand by their newest result, the most recent first, and
  then by repository name; a project with no registered result comes last, by name.
  The order is computed from `results.yaml` when the page is rendered
  (`overview_sections.ranked_projects`, over `project_tallies` and `project_order`) and
  is kept nowhere by hand; the section’s introduction says the rule in a sentence.
  A result is a project’s where its `attribution.source_keys` names a bibliography key
  the source-coverage register gives a source at the project’s address
  (`project_source_keys`; `PROJECT_EXTRA_KEYS` adds a key two places share, and
  `SOURCE_VENUES` every key the bibliography files under the catalogue’s venue), and a
  result attributed to sources of several listed projects counts for each.
  This project’s own results, and results by others from a source no listed project
  holds, count for none.
  Each card with a result ends with its tally (**Card foot**, above), in the form “6
  results (3 at S4, 3 at S3)”: the total, “1 result” for one, then every level that has
  a result, the highest first, in parentheses, which are kept when there is one level so
  each tally reads the same way.
  The total links to the results table filtered to the project’s results and each count
  to the same table at that level (**Result filters**, **Preset-only controls**, below).

- **Card heroes.** Any card, popover or direct, may be headed by a small picture
  (`hero=` on `card()` and `link_card()`, drawn by `card_hero`). The hero runs edge to
  edge above the caps label in a fixed 16:9 box, covering it from the picture’s top
  edge, so pictures of any shape line up across a row; a hairline parts it from the
  text. It is a file served beside the page, never an address off the site, loads lazily,
  and is decorative (`alt=""`), since the card’s label and value already say what it
  shows. Dark mode dims it slightly (`--site-hero-filter`), since the pictures are prints
  on white. On a hero card the corner icon sits over the picture on a small chip of the
  page background, so it reads on any image.

- **Chips.** Every small label is one `.site-chip`: square corners, the sans face at the
  note size, a solid light fill and no border, lettered in the page’s own text colour.
  A plain chip is a light gray tint; a status chip takes its status’s fill from the rung
  scale (Color, The Rung Scale): a case’s `proved` green and `open` yellow
  (`data-case-status`, written by `case_status_chip` wherever a case’s status is drawn),
  a result’s `confirmed` green and `reviewed` blue (`data-status`). No chip wraps: one
  rule on the component, `white-space: nowrap`, keeps a chip’s words on one line
  wherever it sits, and no other rule lets one break.
  What holds a chip is made wide enough for it.
  A row of chips wraps like words, between chips, a space apart, with a small block
  margin (0.15rem) so a wrapped row never touches the row above, on any page or at any
  width. A rung chip adds `.site-rung-fill` with `data-rung` and `data-level`, and its
  fill strengthens and saturates with the level (Color, The Rung Scale).
  Significance is listed first: wherever a result’s rungs are shown together, in a table
  row, a popover, a result’s overview or a case record, they run S, V, C: the
  significance mark, then the V and C chips (`overview_sections.rung_chips`). A table
  row draws the mark in a column of its own before the Rungs column’s V and C
  (`significance_cell`, `ladder_chips`). The generated register documents keep their own
  order, verification first.
  A kind chip (`kind_chip`) says what a result is, in the rubric’s words, `lower bound`
  or `case exclusion`, and carries `data-kind`. Every result draws one: on a line of its
  own under its rungs in a table, and after the rungs in a popover’s head and a chain’s
  step. A result’s status line follows it (`status_marks`), in a column of its own in a
  table, Status, since 2026-10-02 (`think-ybt5`): it stood under the kind, in the rungs’
  cell, until then, though it is where the result stands and no rung.
  Its first chip is the status, `recorded`, `reviewed`, `confirmed` or `incomplete`
  (`data-status`), which every result has: how far the work on it here has gone, derived
  by `devtools.result_status` from the confirmation rung and the defects on record, and
  defined in `epistemics.md`. Next, where the register records one, is who has the next
  move (`data-activity`): `in analysis` for a replay or review under way here,
  `waiting on source` for a request with another party; its title says what is in hand
  and since when. Last is `superseded` (`data-standing`), on a bound that no case bound
  rests on now, followed in quiet type by the results that supersede it, each a link to
  its row: “by T-060”, the results its cases’ bounds rest on now
  (`overview_sections.supersession_marks`). A result of a kind that is no bound draws it
  only where its entry declares a later result that implies it (`superseded_by`), and
  `superseded in part` where that result implies some of it, as `T-060` does `T-036`’s
  bound and not its equality case.
  That mark’s chip says `superseded` too, and `in part` leads the quiet text after it,
  so the line reads “superseded in part by T-060”, the register’s words; the chip keeps
  its own standing, `data-standing="superseded-in-part"`, and the row stays current.
  The four words as one chip were 150 pixels, the widest chip of the status line, and
  set the column 52 pixels wider than `superseded` does (`think-kmi4`). An id never
  breaks at its hyphen.
  A result that still stands draws no chip for that: `current best` is the default, so
  it is left unsaid. That a bound is only reported is no chip of its own: it is the
  status `recorded`. A second proof of a value another result holds says so by its kind,
  `simplification`, and a result that bounds nothing by its kind too.
  Each of these chips adds no style of its own, so every one is the same plain gray
  chip, one font size, line height and height, and they differ only in their words.
  The Rungs column is as wide as its widest chip, so in a table each chip of the status
  line takes a line. A row keeps its kind and status as `data-kind` and `data-status` for
  the filters; a step of a result’s chain keeps its standing on that case as
  `data-standing`. A novelty chip (`data-novelty`) is always plain gray.

- **Arrows.** Every arrow on the site is one drawing, never a typed character: the
  site’s text face has glyphs for `↑` and `↓` only, so `←`, `→` and `↗` came from a
  different fallback font in each browser and no two arrows matched.
  The drawing is `--site-arrow` in [site.css](site.css), a shaft and an open head in a
  16-unit box, stroke 1.6 with round caps and joins, held as an SVG data URI and painted
  as a mask over `currentColor`, so it takes the colour of the text around it in both
  themes. Each direction is that one drawing turned: **right** as drawn, **left** its
  mirror, **down** a quarter turn clockwise, **up** a quarter turn back, and
  **external** an eighth turn back, pointing up and to the right.
  The other shapes are the sort pair, `--site-arrow-sort`, two small arrows up and down
  in the same stroke, and the double chevron, `--site-arrow-double`, the arrow’s open
  head twice, one over the other, in the same box and stroke: **double-down** as drawn,
  for a control that shows more below, and **double-up** turned half round, for one that
  shows less. The **download** icon uses `--site-arrow-download`: a downward shaft and
  open head above a horizontal baseline, with the same box, stroke and round caps.
  Use it for explicit file-download actions; the homepage **Download PDF** action sits
  immediately before **Explore the Atlas** and downloads the complete 1–324 poster.
  PDF cards continue to open their documents in the browser.
  Every in-place expand/collapse action uses this pair, including both the homepage SVG
  preview and the dedicated Atlas grid (**Action under a table or grid**, below).
  - Inline markup carries `<span class="site-icon-arrow" data-arrow="right">`, written
    only by `overview_sections.arrow_icon(direction)`: a case record’s steps to its
    neighbours (left before the previous case, right after the next), which the left and
    right arrow keys follow in the case popover, the overview’s “See all results” button
    (right) and the atlas’s expander (double-down, then double-up).
    The atlas popover’s stepper, two buttons left and right, went with that popover on
    2026-10-03.
  - The icons CSS draws are pseudo-elements painted from the same token: a card’s corner
    icon and its popover’s button, chosen by `data-go` (down to a row on this page,
    external off the site, right to another page of the site, such as the case popover’s
    **Open the Case Record**), and a sortable header’s indicator (the sort pair while
    unsorted, in the muted gray; up or down in the accent once sorted).
  - The arrow is decorative, `aria-hidden` or generated content, so a link or button
    keeps its own text or `aria-label` as its name.
  - **Hover.** On hover or keyboard focus, the arrow in a link or button moves 2px the
    way it points (external 1.5px up and 1.5px right) on the Motion timing and keeps the
    element’s colour. A card’s corner icon does not move: it fades in with the card’s
    wash. A disabled button’s arrow stays still, and under reduced motion no arrow moves.
  - Sort indicators do not move: a header is a control whose arrow reports a state.

- **Motion.** Every hover and focus change on the site runs on one timing, a fast,
  smooth ease: `--site-hover-duration` (140ms) and `--site-hover-easing` (`ease-out`),
  declared in [site-nav.css](site-nav.css) so every page carries them, the explainer and
  the workbench included, and fed to KPress’s own `--kpress-transition-fast` so its
  contents rail and footnote links match.
  - **The hover transition.** A change of colour, a wash, a text colour, a border or a
    shadow, eases on one token, `--site-hover-transition`: `background-color`, `color`,
    `border-color` and `box-shadow` on that timing (the owner, 2026-10-04,
    `think-g9cu`). Every element whose hover or focus changes one of them carries
    `transition: var(--site-hover-transition)` at rest, not in its hover rule, so the
    change eases in and out: the cards, the bar’s links and tabs, the theme menu, a
    popover’s close cross and action, a table’s rows (their wash on hover, on keyboard
    focus and while their popover is open, which snapped until then), the ladders’
    names, the atlas tiles, the record index and the contents rail, and on a paper’s
    page its links, buttons and readouts (`paper-publication.css`). The token names
    those four properties and never `all`, so a late stylesheet snaps into place rather
    than animating its layout, and it is used alone, never listed beside another
    property, so it still reads under reduced motion.
  - What else a hover moves, an arrow’s nudge or a card icon’s fade, transitions that
    one property (`translate`, `opacity`) on the same timing, never with a literal
    duration.
  - A focus ring (`outline`) is not eased: it shows the moment focus arrives.
  - `tests/test_site_hover_motion.py` holds it: the token declared once, every
    `transition` in `site.css`, `site-nav.css`, `site-result.css`, `paper-type.css` and
    `paper-publication.css` the token or one property on its timing, and every rule
    whose hover or focus changes a colour, a border or a shadow styling an element that
    carries the token at rest, by its own selector, a broader rule’s, or a shared rule
    the test names with its reason; in Chromium, a row, the bar’s links and the close
    cross ease the four properties over 140ms.
  - The workbench’s own controls keep its own motion tokens (`--duration-fast`,
    `--easing-standard`, in `packages/workbench/assets/workbench.css`), under its own
    design contract; only the bar it shares with the site runs on this one.
  - Under `prefers-reduced-motion: reduce` the duration is 0ms and the token `none`, so
    colours change at once and no arrow moves.

- **Rating ladders.** Verification Ladders is a section of the Results page, under its
  table, since 2026-10-02 (the owner, `think-hqb3`); it was the homepage’s section
  between Recent Results and the atlas before that (**Results page**, below, for its
  place and its lead).
  A table of results carries a legend of every rung’s mark right above it, which links
  this section (**Recent results**, below; `think-42dx`, in place of the key of the same
  grid the homepage kept under its table from 2026-10-02). Its diagram, `.site-ladders`,
  is one diagram, which is neither a set of cards nor the shared data table: a column
  for each scored dimension of the rubric, in the order Significance, Verification,
  Confirmation, and a row for each level, the highest at the top, so the rungs of the
  three ladders line up across a row.
  A column is headed by the dimension’s name, which links to its section of
  `epistemics.md`, and the question it answers, with no caps label.
  A cell holds the rung’s chip and a description of exactly two lines, and nothing else:
  the diagram says what each rung means, and carries no tally of the results at it.
  A ladder with no rung at a level leaves its cell empty: Significance has no level 0.
  The section was Verification at a Glance until 2026-10-01; an empty anchor in its
  heading keeps the old fragment, `#verification-at-a-glance`, landing on it, and the
  homepage’s `overview/forward.js` sends both that fragment and `#verification-ladders`
  to the Results page, fragment kept.
  - **Rules.** One rule, in the text’s colour, stands under the column heads.
    No rule stands between the rows: 0.8rem between one rung’s description and the next
    rung (`--site-ladders-row-space`, 0.4rem, either side of a row) keeps them apart and
    lets the rungs read as one ladder.
  - **Heads.** Each column is headed by its name and one short question in the same
    form: “How significant is the result?”, “How was it originally verified?”, “How has
    it been confirmed?” (`DIMENSIONS`).
  - **Wording.** The chip’s `title` is the rubric’s full meaning, read from the tables
    in `epistemics.md` (`rung_meanings`). The description is that meaning, or a short
    form where the meaning does not fit two lines of the narrowest cell
    (`rung_short_meanings`); `RUNG_SHORT_MEANINGS` in `overview_sections.py` is the one
    place a short form is written.
    A description is never clipped and never cut with an ellipsis: one that does not
    wrap to two lines of 25 characters (`SHORT_MEANING_LINE`) stops the build until it
    is given a shorter form.
  - **Rows.** Every rung is the same height at any one width, since each is a chip and a
    two-line box; a significance mark stands as tall as a chip, the chip’s line height
    and margin. A cell arranges the two by its own width.
    With 18rem or more it sets the chip in a rail, 2.25rem, the chip’s own width, or
    3.75rem for significance, the widest mark’s (`--site-ladders-significance-rail`;
    S5’s is 58.8px in the page’s face), and the description beside it, 0.75rem on,
    64.1px a row: at 1280 and 1024 pixels, down to a 980-pixel window, and on a phone
    down to 320 pixels. The rail is never narrower than what stands in it
    (`minmax(rail, max-content)`): at 3.6rem S5’s mark ran 1.2px past it, and a wider
    face, 65px in the fallback and more in some system faces, ran it into the words
    beside it (the owner, 2026-10-05). Every cell turns at the widest rail’s width, so a
    row’s rungs stay one height and a significance description, 1.5rem narrower than the
    others beside its wider rail, is never under its least: at 16.5rem, the chips’
    rail’s, it was set 21.6px short and took a third line (2026-10-03). Narrower, it
    sets the chip on a line of its own and the description under it across the cell,
    91.8px a row, from 979 pixels down to 716, so at 768 and 908. A description is never
    set narrower than 13.5rem (`--site-ladders-meaning-min`).
  - **Columns.** The three columns are equal, and each keeps 0.75rem
    (`--site-ladders-inset`) clear after its words, before the next column’s chip.
    Three columns therefore need 42.75rem: three times the least description and its
    inset.
  - **Phone.** Below 42.75rem of its own width the diagram stacks: one block a ladder,
    in the same order, each under its own head with its rungs from the top.
    Three columns there would set a description narrower than its least.
    The missing rung takes no room.
    The diagram’s width is the wide track’s, which is sized from the page and not the
    window (**Wide bleed**): 1104px at a 1280-pixel window, 944px at 1024, 688px (43rem)
    at 768, where the page’s margin widens, 684px at 716 and 358px at 390. So three
    columns hold from a 716-pixel window up, with a description 217.3px wide at 768 and
    216px at 716, and the ladders stack at 715 and below.
    The inset is what fits them at 768: at 1rem three columns need 43.5rem, more than
    that window’s wide track, and the ladders would stack from 768 to 775 pixels between
    two bands of three columns.
  - **Markup.** A grid with table roles (`role="table"`, a row a level, column headers,
    a visually hidden row header naming the level, cells), not a `<table>`: KPress wraps
    every table in its own scroller and restyles it as `.kpress-table`. Stacking changes
    only the grid’s order, so a screen reader reads the same table, level by level, at
    every width.
  - **Space.** It sits in the wide track and stands `--site-table-space` clear of the
    text above and below it, as a table does.
    Either side it keeps the wide track’s gutter and is never under the page’s clip:
    40px from the window at 1024 and 768 pixels and 16px at 390, which is 8px
    (`--site-wide-gutter`) inside the page’s content area wherever the page clips.

- **Atlas grid.** The complete grid at `atlas.html` holds every tracked case, n = 1 to
  324, as a cached square SVG image with its n beneath.
  The artwork uses dark ink on a white canvas in both page themes.
  The grid bleeds past the wide track as the window grows, to 140rem less the page
  gutters, and its cells keep a readable size (at least 6.4rem, 4.6rem on a phone, at
  the Medium size; **Atlas sizes**, below), so a wider screen shows more cases per row:
  4 at 390 pixels, 10 at 1280, 16 at 1920 and 20 at 2560 (measured on 2026-10-04; the
  figures for 1280 and 1920 had read 11 and 17). A cell washes on hover and on keyboard
  focus, and is a link to its case’s record file, `cases/11.html`, which opens in the
  page’s one case popover (**Case records**, below).
  The wash is the cell’s background, behind the drawing, and it is the only thing that
  changes: every line of the artwork keeps its fixed ink at rest, hovered, focused and
  pressed, in both themes.
  `tests/test_site_drawing_hover.py` checks the loaded SVG, its geometry and exact
  painted colours, and contrast against its own canvas.
  The first hundred cells arrive as static markup with reserved image dimensions; the
  remaining cells are already present in a hidden container.
  Images use native lazy loading, and `overview/atlas-grid.js` changes visibility after
  reader input. Each drawing has a 1000-unit frame, fine enough to show large.
  The triangle is the atlas’s default view; Grid remains an explicit alternative
  (**Atlas views**, below).
  The collapsed count is around 100: Grid finishes complete rectangular rows for the
  current width and tile size; Triangle finishes complete square-number groups.
  Expanded coverage is always all 324 (`think-b2o9`).

- **Atlas views.** The atlas is one set of tiles under two views, **Grid** and
  **Triangle**, chosen by a strip over the tiles (`atlas_view_tabs`): the section tabs’
  strip (**Section tabs**, above) as a `tablist` of two buttons, Triangle selected by
  default and the one tab in the page’s tab order, with the arrow keys, Home and End
  moving between the two and selecting the tab the focus lands on
  (`overview/atlas-view.js`). Grid uses the stylesheet’s rectangular layout; the page is
  rendered with Triangle selected.
  The strip is present in the first response, and scripting handles its controls.
  Without scripting, ordinary links reach all case records and the complete frontier.
  The triangle sets the cases by the grid bound: row $k$ holds the $2k - 1$ cases
  $n = (k - 1)^2 + 1$ to $k^2$, the ones that need a square of side $k$, and ends at
  $k^2$ on the right edge, so the perfect squares $1, 4, 9, 16, \ldots$ run down it;
  those are the cases whose best packing is the $k \times k$ grid itself, and their
  tiles are numbered in the text’s colour at the medium weight.
  Ten rows show the first hundred cases, the last 19 tiles wide; eighteen show all 324,
  the last 35 wide. A one-line key under the triangle said what the rows are until
  2026-10-02, when the owner dropped it as obvious (`think-l38m`), with the line under
  the expander that said every case is in the frontier survey and has a case record:
  each tile opens its case record, and the Frontier page is a page card.
  Triangle is the default without a view parameter; `?atlas=grid` selects Grid, and
  existing `?atlas=triangle` links retain their meaning.
  View changes use `history.replaceState` so every other parameter and the fragment keep
  their places. Bootstrap query state and selected controls agree before tiles are
  placed. The homepage’s scoped preview retains its own compact Grid state.
  **Wrapping, by one rule at every width.** A line holds as many tiles as the block’s
  width allows at the least tile width, `--site-atlas-tile-min` (1.625rem, 26px, which
  keeps a tile over a pointer target’s 24px with its three-figure number legible under
  it; 2.5rem, 40px, under 40rem or with a coarse pointer, for a finger), and never more
  than the longest row holds.
  A row wider than a line wraps in reading order, as text does: its first line is full,
  from the row’s first case at the left edge; further full lines follow, each from the
  left edge; and what is left over goes on its last line, right-aligned, so the row
  still ends at $k^2$ on the right edge, in the same column as the rows that fit.
  So 19 tiles at eight to a line are lines of 8, 8 and 3, the 3 ending at the square,
  and a row that fits is one right-aligned line.
  The next row always starts a new line, and where any row wraps the space over a new
  row is 0.4 of a tile rather than 0.12, so a row’s lines read as one group.
  Where some rows fit and the later ones wrap, as on a phone from row 5, the picture
  reads as one column of squares down the right edge with the wrapped rows flowing in
  from the left to meet it; the owner chose this over the earlier cut, which put the
  remainder first and read back to front.
  Where a case stands, `place(n, per)`, is one pure function of the case and the tiles a
  line holds, tested in Node (`tests/node/overview_atlas_view`); the script writes each
  tile’s line and column as custom properties, the stylesheet lays the tiles out from
  them (`grid-area`), and the placement is redone on the frame after a resize and when
  the expander opens or closes.
  At Medium a tile is its line’s share of the block, `100cqi` over the tiles a line
  holds and no wider than `--site-atlas-tile-max` (4.5rem), with its inset, its number
  and the space over a row as fractions of it, so the triangle keeps its proportions.
  Measured in Chromium: at 1280 pixels 63px tiles for the hundred and 34px for all 324,
  no row wrapping; at 1024, 50 and 27px; at 768, 36px for the hundred, and 26px for all
  324 with rows 14 to 18 wrapping at 26 to a line; at 390, 45px tiles at eight to a
  line, rows 5 to 10 wrapping (`devtools.measure_atlas_views layout`). **The move.** A
  change of view, and the expander’s change in either view, moves every tile from where
  it was to where it is: one read of every tile’s box and of each element after the
  tiles, the change of layout, one read more, then one Web Animation a tile on
  `transform` alone, a translation and a scale about the tile’s corner, all started in
  one batch for `--site-atlas-move-duration` (360ms) with `--site-atlas-move-easing` (an
  ease-out). A tile outside the window before and after is not animated; a tile the
  expander shows for the first time fades in; and what follows the tiles moves with
  them, so nothing jumps under them.
  Under `prefers-reduced-motion: reduce` the duration is 0ms and the view switches at
  once. A second press mid-move reads the tiles where they have got to, cancels the first
  move and starts from there, with the focus kept on the tab pressed.
  The final layout is the stylesheet’s, correct with no animation at all, and nothing in
  the block transitions its place (`transition: none` on the box of tiles, the drawings
  and the numbers): KPress’s reduced-motion rule gives every classed element a 0.01ms
  transition of every property, under which the triangle was laid out for one frame with
  the grid’s gaps, 1344 pixels wide at 1280, before it settled.
  `devtools.measure_atlas_views` measures the layouts (`layout`), times the moves
  (`move`) and pictures both (`shots`); `tests/test_site_atlas_views.py` holds the page
  to all of it in Chromium.
  Timed at 1280 pixels, the median of five: the press’s handler runs 8ms for the hundred
  cases and 24ms for all 324, with 64 and 225 tiles in the window moving over 383 and
  420ms; the hundred miss no frame, and all 324 miss ten of 39 at 120Hz, the longest
  18ms.

- **Atlas sizes.** Beside the view tabs, in one row over the tiles that wraps under them
  on a phone, a second strip of the same tabs chooses the size of the tiles
  (`atlas_size_tabs`, think-ht8t): **Small**, **Medium** and **Large**, Medium selected
  by default and the strip’s one stop in the page’s tab order, with the keys of the view
  tabs. Medium is the atlas as it was before it offered a choice; the page is rendered at
  it, and without scripting the strip stays `hidden`. The size is one token,
  `--site-atlas-scale` on the block (1, Small 0.667, Large 1.5), set by its
  `data-atlas-size`, and applies in either view.
  In the grid it scales the least cell, `--site-atlas-cell-min` (6.4rem, 4.6rem on a
  phone): at 1280 pixels a line holds 15 tiles at Small, 10 at Medium and 7 at Large,
  and on a phone 6, 4 and 3. In the triangle it scales the most a tile may be and, at
  Small, the tile’s share of its line, never under the least tile, so Small keeps the
  tiles a line holds and draws each smaller, centred.
  Large holds fewer to a line, as many as tiles half as wide again as Medium’s leave
  room for (`perLineAt`, tested in Node), so where the triangle already fills the block
  its long rows wrap by the one rule: at 1280 pixels the hundred go from 19 to a line to
  13, rows 8 to 10 wrapping, and all 324 from 35 to 23; on a phone the hundred go from 8
  to 5. A block wide enough that Medium’s tiles stop at the most a tile may be lets
  Large grow them first.
  A change of size is a change of layout and moves every tile as a change of view does
  (**Atlas views**, above).
  The size is in the address as `?size=small` or `?size=large` (Medium has none),
  written and read as the view is, before any tile is placed.
  `tests/test_site_atlas_views.py` reads each size in Chromium, and
  `devtools.measure_atlas_views` measures every layout at every size (`layout`), times
  the changes of size in each view (`move`) and pictures them (`shots`).

- **Atlas marks.** A tile carries up to two marks beside its number, each hung out of
  the flow so the number stays centred: the new-result star after it, and the
  regularized layer’s badge before it.
  The star is the site’s one star in its warm ink (`atlas_star`, `.site-star`), on every
  case whose verified lower bound is a new result, the rule the frontier table’s Recent
  column stars by (`render_frontier_page.recent_lower_bounds`, think-wwtt); it is hidden
  from assistive technology, and the tile’s name ends “new result” instead, as a starred
  row’s does in a table of results.
  A case that `atlas/known-best/regularized/` keeps a derived view of (X-049) is drawn
  from that view, the record’s exact frame with its nearly axis-aligned squares
  straightened, each square shaded by the house rule on the regularized pose, and its
  tile carries the layer’s badge, a dot in the accent, and says “regularized view” in
  its name; every other case is drawn from its house rendering.
  `devtools.render_regularized_atlas` draws those views from the layer’s index, so a
  view the layer gains joins the atlas at the next render; its `--check` holds the
  drawings to the index.
  The tile opens the same case record as any other, whose drawing is the house one: the
  regularized layer is the atlas’s view, not the record’s. Until 2026-10-04 the house
  drawing was the default and a **House** and **Regularized** strip swapped a second
  tile in for each such case; the owner dropped the choice for the regularized drawings
  alone (think-k8x9), and the page stopped shipping the second set, 264 KB. A key under
  the two strips, on a line of its own, names both marks in words, each beside its mark
  as on a tile, “new result” and “regularized view”, the second a link to the atlas
  README’s section on the layer (`atlas_legend`), in the support colour at the note
  size, as the tables of results key their star: a star without a key reads as
  decoration, and a regularized drawing is shown only labelled as one.
  It ships `hidden` with the strips.
  At the smallest tile, 26 pixels with a three-figure number, the star is set at 0.8 of
  the number’s size and both marks stay inside their tile:
  `devtools.measure_atlas_views` holds every layout to that (`mark_problems`), and
  `tests/test_site_atlas_views.py` holds which tiles carry which mark to the records.

- **Action under a table or grid.** Where one control follows a table or a grid, it is
  the site’s one action button, `.site-action`, in a centred `.site-action-row`: the
  look of a popover’s action (**Popovers**, the accent fill with the page’s background
  for the text, the medium sans at the note size, `0.45rem 0.9rem` of padding and square
  corners, darkened a step on hover and keyboard focus), with its icon from the one set
  after the label at the label’s size, the arrow right where the control is a link that
  navigates and the double chevron where it is a button that shows more or less in
  place. Both forms share one rule in `site.css`, and the row sets `--site-action-space`
  (1.2rem) above itself and a table’s own space, `--site-table-space` (2rem), below, so
  text that follows a button stands as clear of it as of a table; where a heading
  follows, its larger space takes over (the owner, 2026-10-02, `think-0o9u`; nothing
  below until then). The rule is scoped to the page, `.kpress .site-action-row`, since
  the row is a paragraph and KPress’s `.kpress-prose p` margin outranked it, which had
  set both of its margins to 0.75rem. Homepage actions are **Expand** and **Explore the
  atlas** beside each other under the preview, then **View all results** under Recent
  Major Results. All use uppercase labels through `paper-type.css`. The dedicated Atlas’s
  expander uses the same style.
  The Frontier, Results and Papers pages end their tables with no action, so none
  carries one. `tests/test_site_atlas_views.py` reads both in Chromium at 1280 and 390
  pixels and holds their colours, type, height, padding and centring to each other.

- **Homepage Atlas preview.** Embed the retained 1-to-324 SVG atlas, preserving its
  drawing geometry and colors, with case-number and applicable-star labels
  (`think-hyd6`, `think-ngcg`). Initially show six square-number Triangle rows, cases 1
  to 36. Omit the printed poster title and footer.
  Both pages use `SiteAtlasView` for layout and animation.
  Prepare the remaining native SVG drawings during initialization from an embedded
  compressed payload; retain the existing two-megabyte page ceiling.
  **Show More** immediately animates from 36 to 100 cases on the first click, and from
  100 to all 324 on the second, retaining Triangle throughout.
  There is no click-time request or delay.
  At full coverage the button becomes **Show Less**, restoring 36. Its accessible name
  states the next case count; double-down chevrons mean more expansion and double-up
  means collapse. Persistent case links retain case popovers and ordinary page
  destinations. The homepage instance keeps its state local; dedicated Atlas view
  controls and URL state retain their existing behavior.
  Without scripting, the compact SVG preview and Explore link remain available.
  The homepage does not insert explanatory selection/tile prose above the graphic.

- **About and Papers.** About separates the project narrative into paragraphs for its
  origins, subsequent work, independent results, and current role.
  **Contribute Your Results!** is an H1 over the reporting invitation; project
  documentation remains on About.
  Papers holds the paper, tutorial, and PDF cards.
  About no longer carries Reading and Research; omit redundant Frontier Survey and
  Workbench cards from both pages (`think-h21i`).

- **Atlas expander.** The dedicated Atlas initially targets 100 cases (`ATLAS_FIRST`),
  finishing whole rectangular Grid rows or square-number Triangle groups for the current
  width and tile size (`think-b2o9`). One button, centred under it, reads **Show More**
  with the double chevron down and expands the grid in place; it then reads **Show
  Less** with the chevron up and collapses it.
  It carries `aria-expanded` and `aria-controls` (the box of tiles, `ATLAS_PANEL`), and
  its name for assistive technology says what it does and how many cases that is, “Show
  more: all 324 cases” and “Show less: the first N”, with N updated for the completed
  preview rows; the visible label stays short.
  The expander’s row ends the block: the sentence that followed it is gone since
  2026-10-02 (`think-l38m`), and the next section’s heading brings its own space.
  It is the action under a table or grid (above), set `--site-atlas-toggle-space` below
  the grid. All 324 links ship in the page.
  Existing links move across the visible and hidden-container boundary as the collapsed
  cutoff changes, without cloning drawings or losing case state.
  The remaining box uses `display: contents`, and expansion reveals it; the expanded
  case count is strictly 324. Collapsing keeps the button in view.
  The case popover steps through all 324 cases from any cell, the grid expanded or not,
  since a step loads the neighbouring record in place and closing returns focus to the
  cell pressed. Without scripting the button’s row stays `hidden`, since it would do
  nothing. In the triangle, expanding changes how many tiles a line holds, since the
  longest row grows from 19 to 35, so the hundred move into their smaller places as the
  rest fade in, by the same move a change of view makes (**Atlas views**, above).

- **Wide bleed.** A wide block (`.site-wide`) takes the wide track, `--site-wide`, less
  the page gutters (`--site-wide-gutter` on either side; **Spacing**, above).
  Two kinds bleed past it.
  The atlas grid bleeds at every width, up to `--site-bleed-max` (140rem). A data table
  bleeds only above `--site-table-bleed-from` (80rem, 1280 pixels): from there it grows
  one pixel for each pixel of window, `--site-table-wide`, until it reaches the page
  gutters or `--site-table-max` (100rem, 1600 pixels), past which its columns would only
  spread apart and a row would be harder to follow.
  So nothing changes at 1280 pixels or narrower, and on a large screen a table’s text
  columns wrap less. The frontier table, whose own track is 86rem, is the page’s content
  area less its gutters up to 1456 pixels and goes from 1376 to 1600 above that.
  The tables of results are the one exception: they bleed from 74rem, 1184 pixels, which
  they needed while they held nine columns (eight from 2026-10-02, `think-ybt5`,
  `think-e4o3`, nine with the significance’s from 2026-10-03, `think-m3m4`), whose
  floors came to 1198 pixels, more than the 1104 of the wide track.
  Since the Details column moved into the row’s popover on 2026-10-04 (`think-46fw`)
  they hold eight, whose floors come to 1095.5 pixels with every row showing.
  They fit from about 1176, are 1200 pixels wide at 1280, as the frontier table is
  there, with 104.5 to spare, 1360 at 1440 and 1520 at 1600, and they go on past the
  1600 other tables stop at, to a cap of their own, `--site-results-table-max` (112rem):
  1792 pixels at 1920 (`think-bcmc`). Below 1176 they scroll in their wrap: by 151.5
  pixels at 1024 and 407.5 at 768 with every row showing.
  The rule takes any `.site-wide` that is or holds a `.site-table-wrap`, so a new table
  bleeds with no rule of its own.

- **Visual summary.** A case has one view wherever it is shown, its visual summary
  (`render_case_pages.visual_summary`, a `section.site-case-summary`): every case record
  opens with it, so the record page and the case popover show it, and a result overview
  shows it for each case the result is about (**Result Overview**, below).
  It is the ascent film’s panel for the case, laid out for a page with the drawing
  first: the known-best packing centred and large, captioned in a record with its side
  and its credit; then the gap bar (a number line from one below
  $\lceil\sqrt{n}\,\rceil$ to two above it, the integers and the values of $\sqrt{n}$
  and $\sqrt{n} + 1$ marked, the two bounds as bold rules with their values above and
  the open span between them shaded); under PROVEN the bound as one statement, the
  proved lower bound in scarlet and the best known side in green, with the star for a
  recent lower bound; the badges; the citation, one line per bound with this project’s
  note; and what is OPEN. A citation line is a table row of two cells, the label
  (“lower” or “upper”) and the source, so the label column is as wide as the wider label
  however it is drawn, and the source wraps between words beside it.
  The drawing is as wide as the column allows up to 28rem on the record page and 18rem
  in a result overview, and in the case popover it fills the panel’s width, growing and
  shrinking with the panel and square at every width (the owner, 2026-10-04,
  `think-u214`; 24rem until then), short of the panel’s height less 8rem, the room the
  caption and the actions held at the panel’s foot take, so the whole square shows at
  one scroll of the panel: 608 of the panel’s 934 pixels in a 1280 by 800 window, 700 at
  1280 by 900, the full width on a tablet or a phone.
  The facts under it keep to 40rem, in the sans face at the note size.
  Its lines keep the weight they have at 12rem across, however large it is shown
  (`think-pkz0`): the drawing strokes its frame 1.2 and each square’s outline 0.6 of the
  102 units its box is wide (`render_frontier_page.packing_svg`), weights that grow with
  the drawing, so the popover’s drawing, 58rem across on a laptop, drew them 11 and 5.5
  pixels heavy, and at a 24rem weight a zoomed drawing still read as heavy-lined (the
  owner, 2026-10-05). The stylesheet draws them in the page’s own units instead
  (`vector-effect: non-scaling-stroke`), at the same share of the figure’s width
  (`100cqi`) up to 12rem (`--site-case-figure-lines`): 2.3 and 1.1 pixels from 12rem up,
  and as the drawing draws them below it.
  `tests/test_case_pages.py` reads the two shares from the drawing itself, so the
  stylesheet and the drawing cannot part.
  All of it is written when the page is rendered, from the film’s own facts
  (`atlas_film_facts`, read from the atlas figure and `bound-citations.json`), its math
  as kpress’s markup; the gap bar’s labels are placed then too
  (`result_overview.gap_bar`), each value centred on its mark, and two values too close
  to sit side by side set either side of their marks.
  The block keeps the classes of the atlas popover it came from, `.site-atlas-pop`,
  which every atlas cell opened until 2026-10-03, when the case popover took its place
  (the owner, `think-7aar`, `think-necq`).

- **Web Atlas labels.** Tiles show only the case number and any recent-result star
  (`think-ngcg`). Bounds, algebraic degrees, and evidence icons belong in the case
  popover. The PDF graphics retain their full labels.
  Homepage and dedicated Atlas expansion controls share **Show More**/**Show Less**
  labels and double chevrons.

- **Case badges.** A case’s properties have one mark on the site, the film’s badges:
  optimal (O), exact (=), numerical (≈) and rigid (R, outlined when it is the
  catalogue’s), each its glyph in a small square, solid or outlined
  (`.site-atlas-badge`, `result_overview.badge_glyph`); a new result is the star and
  what is open the outlined “?”. The visual summary lists them with their words.
  Where a case is one line, a record’s head beside its status chip, a frontier row and a
  broad result’s list of cases under it, they are the glyphs alone, each named for a
  screen reader and in a tooltip (`result_overview.case_badges`, `.site-case-badges`;
  the owner, 2026-10-03, `think-7cbx`). In a table they are a step smaller, 1rem, and a
  block of their own under the chip, so a row of whole numbers stays the two lines its
  drawing is high.

- **Evidence tooltips.** Case-property glyphs (optimal, exact, numerical and rigid) and
  S/V/C levels use one shared styled tooltip treatment (`think-tg0p`). Each tooltip
  explains its icon or level, appears on hover or keyboard focus, and uses the shared
  overlay colors and transitions with reduced-motion support.
  Fetched case/result content receives the same enhancement.
  PDFs retain their existing graphical labels.

- **Scrollbars.** Every screen surface uses thin scrollbars with transparent tracks and
  corners (`think-7y0v`). `paper-type.css` defines the shared size and thumb-strength
  tokens, using each surface’s muted theme color.
  Popovers, tables, mathematical expressions and horizontally scrolling diagrams inherit
  the same treatment. Forced-color mode retains the platform’s scrollbar colors.

- **Case records.** Every case has one record at an address of its own, `cases/11.html`,
  and every way to a case opens that record: an atlas tile, a frontier row and a link
  (the owner, 2026-10-02 and 03, `think-t21m`).
  - **The canonical record.** `cases/N.html` is a complete styled page with its own
    title, canonical address, metadata and record article.
    It is readable without scripts and supplies the article fetched into the case
    popover.
  - **The directory.** `atlas.html` is the case directory, with interactive graphics
    followed by the Frontier Survey.
    Old `cases/`, `cases/index.html`, and `cases.html` directory links forward there
    while preserving case selections.
    Individual case-record addresses remain canonical.
  - **The case popover.** A page that opens cases carries one shared `#pop-case`
    (`render_case_pages.case_popover`). Atlas tiles, Frontier rows and `a[data-case]`
    links open the matching canonical record there.
    Its centered compact **Case Record** label sits above a larger typeset $n = N$ count
    (`think-g28m`). Case-property icons come first on the status line, followed by any
    recent-result star and notes, then textual tags such as “proved”.
    The close control, Escape, outside click, and focus return remain shared behavior.
    Previous and next controls and left/right arrow keys change the case in place.
    There is no **All cases** control.
    The sticky footer offers **Case Record**, **Frontier Survey Row**, and **Atlas
    Diagram** destinations, all with the same right-arrow design.
    Case changes update every destination.
    The packing diagram is centered above the number line and supporting facts at every
    width, using the shared case-summary layout.
    The sticky action footer has matching padding above and below its buttons.
    Long formulas scroll within the prose, and the panel fits the phone viewport.
    Fetch failures use the link’s canonical case page as the fallback.
  - **The record.** Its header shows previous and next steps, the mathematical case
    count, ordered status marks, and the verified interval as display-size math.
    Then the visual summary (above).
    Then, under a rule, the bounds as bordered sans panels, one per bound (best known,
    verified upper, reported lower, verified lower) and the gap, as many abreast as fit
    and none narrower than 17rem, which holds the usual evidence names whole.
    Each panel shows its value as math when it has a closed form (a lone fraction at
    full size) and as figures when it is a decimal, the recorded decimal in full
    beneath, then its credit, source, minimal polynomial as math and evidence.
    Below come the register’s results for the case, each a line with its rungs as chips;
    the verification, how the bounds were verified and the case’s disposition as
    `STATUS.md` writes them, which a frontier row’s own popover said until 2026-10-03;
    rigidity, open questions, evidence and sources; and the links to the frontier row
    and to the case file “On GitHub”.
    Last, under a rule, the case file’s own prose, whose formulas are set as LaTeX.
  - **One render.** Every record is rendered once, in one kpress page of every record,
    so its prose, math and links are rendered as any page’s are; the record page and
    each record file are cut from it (`render_case_pages._rendered`), and each record’s
    links are written again from `cases/` (`rebase_links`). In the one render a record
    is a `<section>`, since the page’s own article holds every record, and in its file
    an `<article>`. Its headings’ ids are made again within the record alone, from their
    text with kpress’s own slugger (`_own_ids`), so a heading added to one case file
    never renumbers another record’s and breaks a shared `cases/N.html#…`. The page
    model’s list of headings, the records’, is emptied on the record page, which has no
    contents rail. A footnote in a case file is refused: kpress gathers footnotes at the
    foot of the one render, outside every record.
  - **Why not 324 pages.** Until 2026-10-04 every site page inlined its shell, about 1.8
    MB of faces and KaTeX, so 324 full pages would have carried it 324 times.
    The record page carried it once, 1.9 MB with the index, and the record files are the
    records alone: 16 KB for $n = 1$ to 217 KB for $n = 11$, 10.4 MB for all 324
    (measured 2026-10-03). The shell is now shared (**Shared Assets**, below), and the
    record page is 41 KB; one page of records still keeps a record’s address one
    fragment of one page, and its popover and its page the same file.
    The former combined record address, `cases.html`, now forwards case selections to
    the Atlas directory (**Document cards and moved pages**, below).

- **Media cards.** PDF cards appear on the homepage under **PDFs** and on `papers.html`.
  Their eyebrow label is “PDF”. The homepage video is a separate native inline player
  with controls, `playsinline` and `preload="none"`, showing the retained poster until
  clicked. It does not autoplay.
  The full player also appears on `visualize.html`. The two posters open their PDFs.
  Retain the poster SVG links and source README on the Papers page.
  The dedicated Atlas page contains the atlas controls and cases, without media cards.
  A single-card group is centered.

- **The film.** The Visualize section’s Film tab, `visualize.html`, is the n = 1 to 324
  film at full size directly under the section tabs, with no page title and no subtitle
  (**Page headings**, above).
  It is as wide as the window allows less the page gutters, up to 120rem, but never so
  tall that it will not fit the window whole (`.site-film-frame`), and embedded inline,
  with its controls. Its poster, `ascent-n1-324-poster.png`, published beside the
  explainer’s assets, shows until playback starts, at the video’s own 16:9, so starting
  moves nothing. The film starts when the page is visited.
  Its markup mutes it (`muted`, which a browser requires of a film it starts unasked)
  and marks it `data-autoplay`, and `overview/film.js`, which only this page carries,
  sets `autoplay` and plays it.
  It does not loop. **Visiting the page therefore starts the film’s download**, a 216 MB
  file on the release, which the browser fetches as it plays.
  A reader who asks for reduced motion (`prefers-reduced-motion: reduce`) keeps the
  poster and the play control, and so does a reader without scripts, the page framed in
  a card’s popover, and a browser that refuses to start the film.
  For them nothing is fetched until they press play: the markup keeps `preload="none"`
  and has no `autoplay` of its own, since markup cannot make that depend on the motion
  preference. No other film on the site starts unasked: the explainer’s stays as it was,
  fetching nothing until a reader presses play, and the overview embeds no video.
  The tools that open the film’s page in a browser (`preview_site`,
  `measure_site_pages header` and `baselines`, the browser tests) open it under reduced
  motion (`preview_site.motion_for`), so none of them starts the download; every other
  page they open as any reader’s. `tests/node/overview_film/` runs the script against a
  stand-in film. A caption and a note in the support colour follow at the reading
  measure: what the film shows, its length, the shorter 1 to 100 film, the release both
  are on, and the Workbench.

- **Tables.** Every data table is one component, `.site-table` on a KPress table, in a
  `.site-table-wrap` that scrolls sideways if the table cannot fit.
  It is set in the sans face at the note size, with sortable headers and filters above.
  No table divides its rows under group rows: a table is one flat list, and what would
  have been a heading is a column or a filter.
  A row with detail opens its popover (**Row popovers**, below), a frontier row its
  case’s record (**Frontier table**, below), and no cell expands on its own.
  Rows are separated by a light rule, not zebra stripes, and a row takes the wash on
  hover. The site’s tables have no outer frame: KPress draws a border round every table,
  and on the results tables and the frontier table it was clutter (the owner,
  2026-10-02, `think-wadm`), so the rule under the header and the rule under each row
  are all their lines.
  Cells are padded 0.55rem by 0.5rem, top-aligned, at line height 1.4 (the frontier
  table centres its cells and keeps 0.4rem at their sides: **Frontier table**, below).
  Headers sit at the bottom of their cell, aligned as their column is: text columns to
  the start, number columns (`.num`, tabular figures) to the end.
  The short columns (the id, n and date, `.site-col-id`, `.site-col-n` and
  `.site-col-date`) are as narrow as their content, the id and the date on one line,
  which leaves the spare width to the long text column.
  The two tables of results, the overview’s recent table and the results page’s, are one
  table: one header (`result_head`) and one row (`result_table_row`), so the same
  columns in the same order.
  They are the date; the significance, S, its mark (**Significance and the Other Inks**,
  above) and a new result’s star after it; the result, its summary whole, method and
  all; the cases, n; the credit, the finder first and “after …”, what the result builds
  on, quiet after it, in full; the rungs, verification and confirmation, with the kind
  on a line under them; the status line, its chips one under another (**Chips**, above);
  the details, the result’s records (its case link, the register, its evidence, source
  and reviews), a link to a line; and the id, the last column and the row’s trigger, as
  narrow as an id, under the 6rem KPress keeps a cell to.
  The owner set that order on 2026-10-02: the id led and the date closed the row until
  then (`think-t090`); the status line stood under the kind (`think-ybt5`); and the
  records stood on a quiet line under the summary, a dot between two links, where the
  result’s cell holds the claim alone now (`think-e4o3`). Significance left the rungs
  for a column of its own, the second, on 2026-10-03, and a new result’s star left the
  result’s text for it (`think-m3m4`). The status cell sorts on the status word; the
  details do not sort.
  On a phone each row is a card that places its cells by class, not by column, so the
  card reads as before: the id, the cases and the rungs on its first line, the
  significance under the id and the status under the rungs, the claim with its details
  on a line under it, a dot drawn between two links, then the credit and the date.
  The tables are two filters of one table, and differ only in where the filter bar
  starts, which sets the rows that begin `hidden` and the count, and in a row’s key: on
  the results page a row is the result’s own address (`id="t-018"`), and on the overview
  it names the result as `data-result`. Every other byte of a row and of its popover is
  the same, so each shows the result’s records in its details and each opens its popover
  from the id. The line under the overview’s table, “See all results”, links the overview
  to the results page, and so does a status line that names the results superseding its
  own: each named result links to its row on the results page
  (`overview_sections.result_url`), in place there and across from the overview.
  Both sort on any column whose header carries the sort pair.
  The widths follow from each column’s floor and from what the n column asks for.
  The id, the significance, the rungs, the status, the details and the date are as
  narrow as what they hold.
  The significance is as wide as its widest mark, S5’s five bars and a star, 77 pixels
  with the cell’s 0.2rem padding either side: its bars are 0.36em wide, 0.2em after the
  label, and the star takes the cell’s end padding (trimmed on 2026-10-03, `think-r3rd`,
  from 90 pixels, which set the table 7.8 past its frame at 1280). The details are as
  wide as their widest link, “evidence 10”, 102 pixels, and a result with many records
  is the tallest row: T-075’s sixteen links stand 410 pixels.
  The rungs column is as wide as its widest chip, since no chip wraps: the two rungs
  share a line, and the widest kind, “restricted optimality”, sets it at 180 where a row
  with one shows. The kind takes a line under the rungs, and the status column is as wide
  as its widest chip, 114 pixels, its chips one under another.
  The credit column is at least 11.5rem wide, which holds the longest name on one line
  (“Queuingtheorydotcom”, 167 pixels of the 184), so a credit wraps between names and
  never inside one; KPress’s own floor, 6rem, set it a word to a line.
  The result column is at least 16.55rem, 265 pixels, and no formula holds it wider.
  KaTeX sets a formula as pieces a line cannot end inside, one up to each relation or
  binary operator at its top level, and the widest piece in either table is 249 pixels,
  the numerator of T-033’s quotient.
  A quotient of more than 24 digits sets its solidus as a binary operator
  (`overview_data.breakable_quotients`), so a line may end after it: four results state
  one of 33 to 40 digits, which as one piece is up to 395 pixels wide.
  A formula in a summary is set in the line and not in KPress’s inline box, so the words
  after it follow on the same line.
  Its last piece is set in the line too: a browser may end a line after any box, even
  before a comma, so the comma after a formula goes on with the formula’s last piece and
  no line begins with it.
  The n column holds a result’s cases, each count or range in a box a line cannot end
  inside (`overview_sections.case_list`), so a range is never cut at its dash, and it
  reads from the start of the cell, as text does.
  A cell of up to four values stays on one line.
  A cell of five or more wraps and asks for `--site-cases-measure`, 24ch, which is 209
  pixels and a column of 225. The three such results take 2, 2 and 6 lines there:
  T-044’s 8 values, T-046’s 9 and T-056’s 23, which a column as narrow as one value sets
  on 15 lines, a row 386 pixels tall.
  The table gives the n column its measure before the result and the credit share the
  spare width, and where the window is short of room the n column narrows first, to half
  its measure at the least, a range and a count to a line.
  Where no row showing holds a long list, as in a view of one kind of short lists, the
  column is as narrow as its lists, under 96 pixels, so a single case has no empty
  column beside it. The overview as it opens shows T-056’s list since it starts at S3
  (`think-x60s`). With every row showing, the date, significance, result, n, credit,
  rungs, status and id columns measure 100, 77, 389, 225, 220, 180, 114 and 56 pixels at
  a 1440-pixel window, where the table is 1360 and gives the n column its whole measure:
  T-056’s list takes 6 lines, a row 165 pixels tall, under the 182 of T-044’s row.
  At 1280 the result and credit columns are at their floors, 265 and 184, and the n
  column still has its whole measure, 225, so the list takes 6 lines there too; at 1024
  and 768 every column is at its floor, the n column at 120 and its list on 12 lines,
  and the table runs 151.5 and 407.5 pixels past its 944- and 688-pixel frames.
  The floors come to 1095.5 pixels, so a table fits its frame down to a window of about
  1176 pixels and scrolls sideways in its wrap below that (measured 2026-10-04). A
  result’s records, its case files, register entry, evidence, sources and reviews, are
  the last entry of its row’s popover, one line with a dot between two links; the
  overview the popover fetches links each of them again.
  They were a Details column, a link to a line, from 2026-10-02 to 2026-10-04
  (`think-46fw`): a column of links made every row harder to read for what most readers
  open a row to see. `devtools.measure_site_pages columns` and `chips` measure all of
  this on a built site: each column’s width, the most lines a cell takes, the words a
  line break splits and the tallest row a column sets; the values of a list of cases cut
  across lines, the widest piece of typeset math, the formulas a line ends inside
  anywhere but after a relation or a binary operator, and the punctuation that begins a
  line; and every chip’s font size, box and lines.
  `tests/test_site_result_columns.py` holds both tables to it in a browser.
  Secondary content in a cell, such as a credit or an “after …” list, takes
  `.site-cell-quiet`, which sets it in the support colour and the sans face.
  It keeps the table’s size, so the quiet text does not become harder to read.
  Every table stands `--site-table-space` clear of the text above and below it
  (**Spacing**, above).
  Wide tables bleed on large screens, as **Wide bleed** above describes.
  On a phone, a table of results becomes one card per row: the id, the cases and the
  rungs on its first line, the significance under the id and the status under the rungs
  on its second, and a list of five values or more, or a long one, on a line of its own
  under them, the card’s width.
  The significance stood on the first line until review found the cases left no width
  beside it on 34 of 70 cards (`think-uer5`), and no cell of a card shows anything past
  its own box (`test_on_a_phone_each_row_is_a_card_that_fits`). A date cell leads with
  the date and then says what it dates, `published` or `established`, in the support
  colour (`date_cell`): under the date on a wide table, which keeps the column narrow,
  and beside it on a phone.
  In both tables of results a new result’s star follows its significance mark, in the S
  column (`new_result_star`, `significance_cell`), where it hung after the result’s text
  until 2026-10-03 (`think-m3m4`). The rule is the atlas’s, asked of a result instead of
  a case (`overview_data.starred_results`): the verified lower bound of a case rests on
  the result now, and that bound is recent, so a superseded result and an upper bound
  carry no star. The star is never the only signal: it is an image whose name and tooltip
  say “New result” and the cases, the row’s own name ends “new result”, the legend under
  each table of results shows it as “new result” (`rung_legend`), and the Results page’s
  prose says what it marks (`star_legend`). A superseded result’s row reads quieter, its
  text in the support colour, in every site table, by one rule on
  `tr[data-current="false"]`; its chips keep their fills.
  A row reached by its address (`atlas.html#n-11`, `all-results.html#t-018`) takes the
  wash, in every site table.

- **Frontier table.** The frontier atlas’s table is a site table of ten columns, in this
  order (`render_frontier_page.HEADERS`): the drawing, n, Recent, Status, Best known
  packing, Verified upper, Reported lower, Verified lower, Gap and Records.
  The left edge of a row says which case it is and whether its bound is new, and what is
  known follows.
  - **The drawing** of the best known packing has the first column to itself.
    Its header shows no words and is named “Packing” for a screen reader (`aria-label`).
    The cell is the drawing alone, an inline SVG with no wrapper, and the column is the
    drawing and the row’s start padding.
    Its side is `--site-frontier-thumb`, two lines of the table’s text (2.8 times the
    note size, 49 pixels; it was 2.6rem, 42 pixels, set under the number).
    Every row holds two lines at least, since its Records cell is the case file’s link
    over the link to the case’s record, so the drawing never makes a row taller than its
    text does. The drawing is no link: pressing it opens the case’s record, as pressing
    anywhere else on the row does.
  - **The case number** is the number alone and the only bold text in a row, in
    `--site-font-weight-sans-bold`. It is a link to the case’s record file,
    `cases/11.html`, which is where a reader without scripts goes.
  - **A row opens its record.** The whole row is one control for its case, as a results
    row is for its detail: it takes focus, and a click anywhere on it but on its own
    links and controls, or Enter or Space while it has focus, opens the case’s record in
    the page’s one case popover (**Case records**, above), and the row reads as expanded
    while the record shows.
    The row names its record file in `data-case-href`, and its name for a screen reader
    is “n = 11, proved: open its case record”.
    The Records cell is the case file on GitHub, `n-011.md`, over a quiet link to the
    record, “Record”. Until 2026-10-03 each row opened a popover of its own, behind
    “Details” in that cell; what it said is in the record (`think-necq`).
  - **Recent** holds the star of a recent verified lower bound, third, as narrow as its
    heading. It sorts, and “recent only” filters on it.
  - **Centring.** Every body cell is centred on its row’s height
    (`vertical-align: middle`), so a value of one line sits level with the drawing and
    with the middle of a neighbour of three lines.
    No cell is exempt: the longest, a fraction over its decimal and its credit, is four
    lines, and reads as one block beside the others.
    Headers keep the foot of their cell, as in every site table.
  - **Decimals.** A bound set as a closed form that is not a whole number (a fraction, a
    radical) has its decimal on a quiet line under it, `.site-approx`, in the four bound
    columns and under the gap.
    Where the decimal is the whole value it reads `= 4.695`, and where it is cut,
    `≈ 3.96861554…`. The digits are the closed form’s own
    (`render_frontier_page.exact_decimal`): a rational is divided in whole numbers,
    anything else is evaluated to 30 significant digits, and both are cut after eight
    places and never rounded, the page’s one rule for a decimal.
    They are not the record’s `value`, which a lower bound may hold to fewer places
    (`15680/3951` is recorded as `3.968615`); that value stays the cell’s sort key.
    A whole number, and a root shown as a decimal already, carry none.
    The credit follows on its own line and wraps between words, never inside a name.
  - **Widths.** The table fits the 1200 pixels a 1280-pixel window gives it, with 6 to
    spare, and scrolls sideways in its wrap below that, on a phone too: it has no card
    layout. Every column is as wide as what it holds, without KPress’s 6rem floor, which
    set n and the star in 96 pixels each.
    A cell keeps 0.4rem at either side (`--site-frontier-cell-inline`) where the other
    tables keep 0.5rem, and the Records cell half a rem more at its start, which keeps a
    decimal in the gap clear of the case file’s name.
    At 1280 the columns are 56, 42, 88, 85, 196, 165, 185, 152, 139 and 91 pixels.
    Before the drawing had its column the table was 1282 pixels wide at every window
    width and ran 82 past its track at 1280.
  - **Bytes.** The page is held under 4 MiB (`tests/test_frontier_page.py`), 3.50 MB
    since its rows’ popovers went and the case badges came (measured 2026-10-03), and a
    row’s markup is paid 324 times, so a cell carries a class and no wrapper it can do
    without.
  - **Checks.** `tests/test_site_frontier_table.py` holds the order, the drawing’s
    column and size, the bold number, the centring, the fit at 1280, the decimal under a
    fraction, sorting and filtering, and each row as one control that names its record,
    in a browser at 1280, 1024, 768 and 390 pixels; a record is fetched, so what a row
    opens is held where the page is served (`tests/test_site_case_records.py`, **Print
    and Verification**, below).
    `tests/test_frontier_page.py` holds every decimal to its closed form’s exact value.
    `devtools.measure_site_pages columns` reports the widths.

- **Result filters.** The complete results page has a tools bar for every registered
  result. The overview’s recent table has a static scope label and a link to that page.
  `overview_sections.result_filters` writes it and `overview/table.js` drives it.
  Every table’s bar, the frontier table’s too, is set at the control size,
  `--site-font-size-control`, 0.8 of the sans base and a step under the table’s own
  text, its controls and their labels alike, so it reads as the table’s tools (the
  owner, 2026-10-02, `think-gwcu`; it was the support size).
  On a touch screen a field keeps 16 pixels at least, under which a phone’s browser
  zooms the page into it.
  A control at its no-filter value, a select’s “All” (every bar’s no-filter choice is
  its empty value) or an empty field’s placeholder, is gray, and a control that filters
  is the text colour, so the bar says at a glance what narrows the table; a checkbox’s
  words are its value, gray unchecked and the text colour checked.
  The count at the bar’s end, what the table holds now, is the text colour, where the
  labels are gray (the owner, 2026-10-02, `think-pcei`). It is the stylesheet’s alone,
  with no script.
  - **Facets.** A result’s row carries each facet as an attribute
    (`overview_sections.result_facets`), and the bar has one control for each:

| Control | Row attribute | Reads as |
| --- | --- | --- |
| Significance | `data-s`, the S level | a floor: S4 and up |
| Verification | `data-v`, the V level | a floor: V4 and up |
| Confirmation | `data-c`, the C level | a floor: C3 and up |
| Kind | `data-kind`, the register’s `kind` | equal to the kind chosen |
| Status | `data-status` | equal to the status chosen |
| Hide superseded | `data-current`, `true` or `false` | checked: the result is not superseded |
| Source | `data-source`, `ours` or `others` | this project’s, or others’ |
| Case n | `data-n`, counts and ranges (`18-21 26`) | the result covers that n |
| Max age | `data-date`, a whole ISO date | dated at most that many days ago |
| Project (preset only) | `data-project`, the slugs of the listed projects the result is attributed to | the list has the project chosen |
| At significance (preset only) | `data-s`, the S level | equal to the level chosen |

```
A rung select offers All, then each level of the rubric above its lowest as a floor,
the top level bare (S5). Kind offers the kinds the register holds, in the rubric's
order and words. Status offers the statuses the register's results have.
A date the register gives only to the year is the first day of it (`1979-01-01`).
Max age is a number of days, and empty is no limit. There is no date range.
```

- **Composition.** The filters compose: a row shows when it passes every one, and an
  empty control, or an unchecked one, passes every row.

- **Preset-only controls.** Project and At significance follow the bar’s own controls
  and are out of the bar (`hidden`, on their labels) until a link sets them:
  `all-results.html?project=evand-square-packing` opens the table on the results
  attributed to one listed project, and `&s=4` on those at S4 exactly, where the
  Significance floor would keep S5 as well.
  The other projects’ cards link this way (**Other projects**, above).
  While a preset control filters, its label is in the bar with the choice it holds, the
  project by its owner and repository, so the reader sees what narrows the table, and
  choosing All takes it out again.
  A project’s slug is its owner and repository in lower case, hyphenated
  (`overview_sections.project_slug`).

- **Status.** The select offers each status some result has, in the workflow’s order:
  `recorded`, `reviewed`, `confirmed`, `incomplete`. It is the chip the row draws, so
  what a reader filters by is what a reader sees.
  A link can preset it, as it can any control: `all-results.html?status=recorded` is the
  results recorded and not yet replayed here, which is how the overview points at them.

- **Hide superseded.** One checkbox, straight after Status, hides exactly the superseded
  results: the bounds no case bound rests on now, because a later or a stronger result
  holds the case (`overview_sections.is_superseded`), and the results of other kinds
  whose entries declare a later result that implies the whole of them.
  Every other result stays: one that still holds a bound, verified or reported, a result
  of a kind that is no bound, such as a rigidity, a simplification or the limit of a
  method, which no better bound supersedes, and one superseded only in part.
  A result that holds one case of several is not superseded, and neither is a bound
  better than its case holds that the case records have not taken in yet: it is pending
  adoption, since nothing has replaced it.
  For a bound the word is derived from the case records
  (`render_recent_results.standing`), so the checkbox and the `superseded` chip cannot
  disagree, and `devtools.check_standing` holds it to the bounds each entry states.
  A result superseded in part draws the same `superseded` chip with “in part” after it,
  and the checkbox keeps its row: the chip’s `data-standing`, `superseded-in-part`,
  tells the two marks apart.
  A row carries the answer as `data-current`, `false` where it is superseded.
  Superseded is the result’s place on the frontier and no status, so the checkbox and
  Status ask different questions and compose as every pair of controls does: a confirmed
  result may be superseded or not, and with the box checked each status shows its rows
  that are not. The Frontier page’s bar pairs its Status with “open only” in the same
  way. The label is the checkbox’s own `<label>`, on one line, and the box takes the
  site’s accent when checked.
  A checkbox is shorter than a select, so every tools bar sets its controls on one
  baseline (`align-items: baseline`): the checkbox’s words, the other labels’ and the
  count read level, on the Frontier page’s bar too.

- **Defaults.** Recent Results on the overview contains only results of significance S3
  and up, at most 180 days old and not superseded (`RECENT_DEFAULTS`). The renderer
  selects those rows and writes their count and scope into the HTML. The complete
  results page includes every row and starts at All, no maximum age and Hide superseded
  clear (`RESULTS_DEFAULTS`). Its other controls start at All too.
  The bar has no reset control: a fresh page load restores the HTML defaults unless the
  address presets a supported filter.

- **Age.** The renderer measures the overview’s 180-day window from the newest
  `registered` date in the register (`reference_date`). This keeps two renders of one
  source tree identical, and the initial subset stays visible without scripts.
  On the complete results page, an age filter measures from the reader’s own day when
  the script applies a query preset or responds to a control change.

- **One flat list.** A table of results has no heading row among its rows, on either
  page: every row is a result, in one order, newest first by the date the table shows,
  until a reader sorts it.
  Whose a result is, and what it builds on, is read from its credit, and the Source
  filter narrows the table to this project’s results or to others’.
  `RESULTS.md`, the generated register document, keeps its groups.

- **A row named by the address** (`all-results.html#t-048`) shows whatever the filters
  hide, so a link to a result never lands on nothing.
  The script keeps it, and without scripts one rule, `.site-table tr[hidden]:target`,
  shows it.

- **Links.** A link can open the complete table filtered: each query parameter presets
  the control it names, `s-min=3`, `source=ours`, `n=17`, `age=30`, `current=true`; an
  empty value, `s-min=&age=&current=`, clears a default, and so does `current=false`. On
  the overview, the ordinary “Browse and filter every result” link reaches the complete
  table. With scripts, it carries supported query parameters from the current address so
  a filter for older results reaches the full dataset.

- **A row’s popover** follows it through filtering and sorting, since the row finds it
  by id (**Row popovers**, below).

The bar wraps onto further lines as the page narrows; on a phone each control takes
about a line. Without scripts a filter cannot be changed, so nothing stays filtered:
under `@media (scripting: none)` every row shows, and the bar, which would do nothing,
does not. `tests/node/overview_table/` runs the script’s filters, alone and wired to a
stand-in table, and `tests/test_overview.py` checks the static recent subset, its
complete table link and the complete page’s controls.
`tests/test_site_result_filters.py` uses Hide superseded on the complete page, by
pointer and by keyboard, and measures its label at 1280, 768 and 390 pixels.

- **Row popovers.** The row is the unit: a table row with detail opens one popover for
  the whole row. This is the site’s one way to show a row’s own detail, and no cell holds
  a `<details>` or expands on its own.
  Two tables use it: the recent table on the overview and the results table.
  The Frontier page’s rows had a popover each until 2026-10-03; a frontier row now opens
  its case’s record in the case popover instead, as one control in the same way
  (`overview/case-popover.js`; **Frontier table**, above).
  - **Pressing.** A click anywhere on the row opens its popover, and so does Enter or
    Space while the row has keyboard focus.
    A link, button or form control inside the row keeps its own behaviour, so a record
    link still leaves the page.
    A click that ends a text selection selects rather than opens.
  - **Look.** The whole row takes the wash on hover, from the shared table rule.
    A row with detail keeps the wash on keyboard focus, with a 2px accent ring inside
    its edge, and while its popover is open (`aria-expanded="true"`), and shows the
    pointer anywhere on it.
  - **The popover** is a card’s popover (`.site-popover`, with `.site-row-pop`): the
    caps label, the headline (its math serif only where the headline is mathematics
    standing alone, as on a card), the close cross, Escape and a click outside, and one
    button at its foot when the row leads somewhere else.
    Opening moves focus to the close cross.
    Closing returns focus to the row, unless the reader has already moved it, as a press
    on another row does.
  - **Markup** is written only by `overview_sections.row_detail`, in three pieces.
    The row is `<tr data-row-popover="ID" aria-label="…">`, the label its accessible
    name. One cell holds the row’s native trigger,
    `<button class="site-row-open" popovertarget="ID">`, around the row’s own key, such
    as a result’s id, and styled as that text.
    The popover follows the table, outside every cell, so it takes no style from the
    table: `<div class="site-popover site-row-pop" id="ID" popover role="dialog"
    aria-labelledby="ID-title">`, holding the close cross, the `.site-card-label`, the
    headline `.site-popover-value` with the id `ID-title`, the body in
    `.site-row-pop-body`, and the optional `.site-popover-actions`. The ids are
    `pop-result-t-nnn`.
  - **Without scripting** the trigger opens the popover, as a card’s button does, and is
    the row’s one tab stop.
    `overview/row-popover.js` makes the row the control: it gives the row
    `tabindex="0"`, `aria-expanded` and `aria-controls`, and takes the trigger out of
    the tab order, so each row stays one stop.
    The row carries no `tabindex` in the HTML, since a focusable row that did nothing
    would be a dead stop for a reader without scripts.
  - **Sorting and filtering** (`overview/table.js`) move and hide rows.
    A row finds its popover by id, so the popover follows its row.
  - **Content.** One function writes a row’s popover body,
    `overview_sections.result_row_popover_body`, on the overview and the results page
    alike. A result’s popover has no button, on the overview or the results page: the row
    pressed is the result’s row in either table.
  - **Deferred bodies.** A body too heavy to render once per row when the page loads can
    wait in a template: `row_detail(deferred=True)` writes it as
    `<template data-row-pop-body>` inside `.site-row-pop-body`, which the browser parses
    but neither lays out nor typesets, and the script places it just before the popover
    first opens, however it is opened.
    Its math is typeset then, as any popover’s is.
    A deferred body costs the same bytes; what it saves is the work of rendering every
    row’s body at load. Without scripts a template stays inert, so `fallback` is written
    beside it in a `<noscript>`, and is what that reader’s popover shows.
    No table uses it at present.
  - **Fetched bodies.** A body too heavy to carry in the page at all is written once, as
    a file beside the pages, and fetched: `row_detail(source="…")` writes the file’s
    address as `data-row-pop-src` on `.site-row-pop-body`, whose content in the page is
    then a short form of the body.
    The script fetches the file when the row is first pressed or its popover first
    opens, puts it in place of the short form, and has its math typeset.
    The page gains only the address.
    Where the file cannot be had, without scripts, on a page read from a file or off the
    network, the short form stays, and the next opening asks again.
    A result’s row does this: its short form is the result’s claim, significance and
    novelty, and its file is the result’s whole overview (**Result Overview**, below).
    Besides its shared assets and a page a card’s popover frames, a page fetches one
    other thing, a case’s record file, into the case popover or the record page (**Case
    records**, above).

  `tests/node/overview_rows/` runs the script against a stand-in document, and
  `tests/test_overview.py` holds every row of the two pages to this markup, the frontier
  table to having no row popover, and every cell free of `<details>`.

- **Overview sections.** The homepage is an overview: each of its sections is a short
  lead, one compact paragraph at most, the section’s key structural element where it has
  one (the recent table, the atlas grid), and one way onward to the page that holds the
  full account. A fact has one home.
  What a page defines is stated on that page and nowhere else, and the overview names it
  and links it: the Results page’s ratings, with the rating ladders that define every
  rung (**Rating ladders**, above, the homepage’s own section until 2026-10-02), its
  kinds, statuses and dating rule, with how many results stand at each status; the
  Frontier page’s counts, its audit of its sources, the seventeen-square history before
  this project, and when a bound by others counts as verified, which is the rule its
  verified columns apply.
  Each table of results keeps its own key to the star, since a star without one reads as
  decoration: the legend under it shows the star as “new result” (`rung_legend`), and
  the Results page’s prose says what it marks (`star_legend`). The atlas note links the
  recent table, and its legend, in place of a third.
  The Frontier page opens with the survey’s account, its audit, its recent counts and
  the seventeen-square history, and ends its prose with the key to its columns, beside
  the table. The way onward follows the section’s shape: a section whose key element is a
  table or a grid ends in the one action button (**Action under a table or grid**,
  below), and a section that is prose leads on with direct cards (**Cards**, above), as
  The Squares Project does with its page cards.
  The page cards under The Squares Project are the site’s reading and working pages, the
  Frontier page alone on the first line, then the three papers and the workbench two to
  a line (**Card sizes**, above); the Results page is reached from Recent Results.
  The owner set this shape on 2026-10-02 (`think-f1tu`): the overview “a little more
  structured and a little less verbose”, the survey’s account moved into the Frontier
  page, Recent Results slimmed to the essentials and its table, and “cards that point to
  the frontier and the results pages where appropriate”.
  That left the Frontier page’s card in a section of its own, The Frontier Survey,
  beside a card to the recent cases (`frontier.html?recent=true`, the query the table
  script presets a filter from), until the owner dropped the section later the same day
  and moved the card to every case up to the page cards (`think-ec5k`); the query still
  works, and nothing on the homepage links it.
  `tests/test_overview.py` holds each section’s prose to one paragraph of its own where
  this applies, the cards to their pages, and the three pages to saying each thing once.

- **Recent results.** The homepage’s **Recent Major Results** section sits directly
  below the Atlas preview.
  It contains up to twelve current results of significance S4 or higher from the last
  180 days, newest first, excluding superseded results (`think-5c8r`). The preview has
  no count/scope sentence or introductory text explaining the links.
  The table shares the full Results page’s columns, sorting, result popovers and mobile
  row cards. Filtering and older results remain on `all-results.html`, whose defaults are
  unchanged. A result’s ordinary link opens its canonical article without scripts.
  **View all results**, in the shared uppercase action style, follows the table.
  The homepage displays the rung legend as a centered card beneath the preview table.
  Its small-caps **LEGEND** heading is centered; Significance, Verification and
  Confirmation occupy separate lines.
  Icons and chips share one left-hand column, with their labels aligned in a second
  column. Omit “What each rung means” helper text from this card.
  The entire card is one keyboard-accessible link to
  `all-results.html#verification-ladders`, with no nested links.
  The full ratings explanation remains on the Results page.

- **Results page.** Every registered result is one row of the results table on its own
  page, `all-results.html`, “Results” in the navigation bar after Atlas.
  (`results.html` was `RESULTS.md` rendered as a reader document, so the table’s page
  took the other name; since 2026-10-01 `results.html` is a forwarder to this page.)
  The page has the Frontier page’s shape: a hero title, “Every Result”, whose id is
  `every-result`, a subtitle, the prose that names the three ratings and points at the
  ladders, defines the kinds, statuses and dating rule, with how many results stand at
  each status where the statuses are defined (`status_counts`, each count the link to
  those rows), and the table under its filters (**Result filters**, above), which start
  with significance at All, no maximum age and Hide superseded clear, so every result
  shows, newest first, in one flat list.
  Under the table stands **Verification Ladders** (`#verification-ladders`, with the
  empty anchor `#verification-at-a-glance` the section carried on the homepage), since
  2026-10-02 (the owner, `think-hqb3`): a lead that defines the three ratings once, S, V
  and C in the ladder heads’ words, with the policy for results by others; the diagram
  (**Rating ladders**, above); and then what the diagram does not show, the three
  assurance labels on evidence, where finite precision falls short, and the audit of
  published work. It stands under the table rather than above it so a reader meets the
  table without a long preamble; the opening paragraph points down to it, and the
  homepage’s Recent Results links it.
  Each row keeps its id, the result’s own (`#t-018`), which is where the overview’s
  recent table and each case record’s results link.
  A row opens its result’s popover, the full claim and its novelty label, with the id in
  its first cell as the trigger (**Row popovers**, above).
  The overview keeps the newest results and ends that table with a “See all results”
  line and the right arrow, in the sans face at the note size.
  The table used to be the overview’s Every Result section, and its old addresses still
  arrive: the overview’s `overview/forward.js` sends `#every-result`, any `#t-nnn`,
  `#verification-ladders` and `#verification-at-a-glance` to the results page with the
  fragment kept, and every other fragment the overview lacks to the explainer, as
  before. `tests/node/overview_forward/` runs the forwarder, and `tests/test_overview.py`
  holds every row id to the form it recognises.

- **Document cards and moved pages.** The overview’s documentation section has one card
  for each repository document the site renders, in the order of
  `render_overview.DOCUMENT_PAGES`: `README.md` and `epistemics.md` first, then
  `SYNOPSIS.md`, `conventions.md` and `development.md`. `RESULTS.md`, `STATUS.md` and
  `defects.md` were cards and pages until 2026-10-01 (`think-bk2e`); the first two are
  generated views of the record the results table and the frontier atlas show, and the
  defect log is internal to the repository.
  A link to either register, in a reader document or a case record, leads to the page
  that shows it, at the result’s row when the link’s text is a result’s id, and a link
  whose text names the file opens the file on `main` (`site_documents.RECORD_PAGES`,
  `_record_links`). A page that moved or was withdrawn is still served at its old
  address, as a forwarder (`render_overview.MOVED_PAGES`,
  `templates/site-forwarder.html`): `forward.js` reads where a visit goes from the root
  element’s `data-moved-to` and sends it there with its query string and fragment, and a
  reader without scripts gets a refresh and a link.
  `results.html` goes to the results table, `status.html` to the frontier atlas,
  `defects.html` to the defect log on GitHub, and `cases.html`, every case record on one
  page until 2026-10-03, to the record page, `cases/`, whose script shows the case a
  fragment such as `#n-11` names (**Case records**, above).
  No page of the site links a forwarder; `tests/test_site_documents.py` and
  `preview_site.moved_links` hold the pages to that, and `check_published_site` asks the
  deployed site for each one.

- **Papers page.** The site’s papers, the optimality paper, the explainer and the
  tutorial, share one entry in the navigation bar, “Papers”, after Results.
  It leads to `papers.html`: a hero title, “Papers”, a subtitle, a short introduction
  and one large card for each paper (`data-card-size="large"`), saying what the paper
  is. The cards come from one ordered list, `overview_sections.PAPERS`, each entry a
  paper’s address, label, title, description and card size, so a new paper is one entry.
  Each is a direct card: a paper is a full page the site serves, so its card is the link
  itself and goes to the paper in the same tab, as the overview’s page cards do, with no
  popover and no framed preview (`link_card`, `new_tab=False`; see Cards).
  A link holds no other link, so what a description names is linked from the page’s
  introduction (`templates/papers-article.md`), which links T-060’s row and the
  optimality paper. The optimality paper is first: it explains the result that stands,
  T-060, where the explainer proves the lower bounds T-060 superseded and the tutorial
  is the background to both.
  The explainer’s card names the newer optimality proofs, and reads the same on the
  overview. The page has no popover, so it carries no popover script.
  The two papers are served under `papers/`, each by its slug, with its Markdown and its
  PDF beside it under the same slug: `papers/n11-optimality-review.html` and
  `papers/n11-lower-bounds-explainer.html`. The tutorial stays at `tutorial.html`.
  Papers is the current entry on the papers page and on each of them.
  The addresses the papers had before 2026-10-01, `explainer.html` and
  `n11-optimality/t-060-explainer.html` with its directory, each serve a forwarder: a
  page of a few lines that sends a reader on with the query string and the fragment they
  came with (`overview/forward.js`, which reads the root element’s `data-moved-to`),
  with a refresh and a link for a reader without scripts, the new address as its
  canonical URL, and the paper’s link preview (**Page Metadata and Social Cards**,
  below). Nothing on the site links an old address.
  The optimality paper has its own renderer, shell and Pages job
  (`render_n11_optimality_review`), and takes the publication layer and the site’s math
  pipeline from the shared functions (**Math**, above); it carries the bar as the
  explainer does, through `render_overview.nav_html`, with the links climbing one level
  to the site’s root. Its page shares the explainer’s publication layer and
  `paper-type.css`, and keeps only its diagrams’ rules in
  [n11-optimality-review.css](n11-optimality-review.css).
  There a table keeps to the column and scrolls inside its own wrap, and a diagram drawn
  in fixed ink keeps a light ground on the dark theme, as the construction in its first
  figure does. Its front, the formats row, the title and the credits, is the papers’ one
  component (**The Papers’ Front**, below).

  **The paper’s citations name a commit, the one exception to links on `main`.** A paper
  cites the evidence as it stood when it was typeset: its links carry anchors into
  reviews and receipts that keep changing on `main`, and a reader checking a claim
  should land on the text the paper read.
  The hazard that links on `main` avoid, a commit that a squash merge leaves on no
  branch, does not reach the deployed paper: the deploy builds it from the commit it
  deploys, which `main` keeps (`render_n11_optimality_review.link_revision`).
  `check_published_site` holds each citation on the page and in its Markdown to that
  commit and to its tree, and fails one that names `main` or any other commit.
  A pull request’s build names a commit that may not outlive the merge; it is checked
  and never published.

## Result Overview

A result’s row, in Recent Results and in the results table, opens a popover with the
full overview of that result.
`devtools/result_overview.py` writes the popover’s body, `result_popover_html`, and
[site-result.css](site-result.css) holds its styles, apart from `site.css` and linked
after it on every page.
The body is one `.site-result` block with no ids, no script and no `<table>`, so it does
not depend on the popover around it.
Its popover is up to 62rem wide and as tall as the window allows (**Cards**, above), and
scrolls as one panel.

No page carries an overview.
Between them they run to about 2.8 MB (`result_overview --audit`) and two pages list the
results, so each is written once, as `result/t-nnn.html` beside the pages
(`render_overview.result_fragments`), and a row’s popover fetches its own when it first
opens (**Row popovers**, Fetched bodies).
A fragment is the one block and nothing else: it has no shell, and its links are written
from the site’s root, so only a page there may place it.
The directory is `result/`, not `results/`, since `results.html` is still served, as the
forwarder where `RESULTS.md` was a page.
`tests/test_overview.py` holds the two pages under a size ceiling each, and
`check_published_site` asks the deployed site for every overview the results table
names.

- **Head.** The popover’s own caps label, the result’s id, and its headline, the
  result’s summary, stand above the body and are in the page, so they do not change when
  the overview lands. The body opens with the significance mark, the V and C rung chips,
  the kind chip and the status line, as the tables show them; then the date and what it
  dates, in the tables’ order (`date_cell`), the credit and the cases, in the support
  colour; the claim at the note size; where the entry declares a later result that
  implies it (`superseded_by`), a paragraph under the claim that opens “Superseded in
  part by T-060.”, the later result linked, and says what it implies and what still
  stands; and a closed disclosure with the significance, composition, next rung and
  novelty.
- **The case.** A result about one case, or up to four, shows each case’s visual summary
  as the case’s record opens with it (**Visual summary**, above), smaller and with no
  caption under the drawing: the packing drawn at the atlas’s scale
  (`render_case_pages.visual_summary` at `ATLAS_UNITS`), at most 18rem wide, then the
  gap bar, the bound as one statement with the lower bound in scarlet and the best known
  side in green, the badges, the citation and what is open.
  Its facts are the film’s own (`atlas_film_facts`), and it is written, its gap bar’s
  labels placed, when the fragment is rendered.
  Where the result is about more than one case, each panel is headed by its $n$. Under
  the panel, the case record’s verified and reported bounds and the gap form a small
  grid, each value linking to its field in the case file.
- **Many cases.** A result about more than four cases says so and lists them in a box
  that scrolls, one row each: the n linking to the case’s record file, the two bounds in
  the film’s colours, the gap, the status chip, the frontier row and the case file.
- **The chain.** Every register result on the same case, oldest first, down one rule:
  the date and what it dates, the id linking to its row, what it established, its chips,
  and its credit, bibliography entry, source packet and register entry.
  The rule beside the result the overview is about is the accent, and a superseded step
  reads quieter, as a superseded row does.
  Where a result stands differently on this case than across its whole scope, the step
  says both. A broad result’s chain opens on request.
- **Links.** One list for this site (each case’s record file, `cases/11.html`, and its
  frontier row, or for a result about more than four cases the frontier survey and every
  case record at `cases/`; the result’s row; the explainer for $n = 11$) and one for
  GitHub, every link on `main` through `devtools/repo_links.py`: the register entry,
  each evidence entry and each cited source’s bibliography entry at its line, the source
  packet, the artifacts, the review, and the case file with its four frontmatter bounds.
  A repository path is set as code.
  Rendering fails on a link whose target is not in the tree, on a page or record file
  the site does not serve and on a fragment no row carries.

A section heading in the overview is a caps label, so it holds no formula: capitals
would change the formula’s letters.
`tests/test_result_overview.py` holds every part and every link.

## Page Metadata and Social Cards

One function, `render_overview.head_tags`, writes every page’s title, description,
canonical link and link preview from a small record of the page (`PageMeta`): its own
name, one description, the path it is served at, and whether it is a paper.
The site’s own pages, every paper and the workbench call it, and no shell writes one of
these tags itself, so the set cannot differ between page kinds.

| Tag | Rule |
| --- | --- |
| `<title>` | Articles use the page’s own name. Other pages append a middle dot and “The Squares Project”; the overview’s is the project’s name alone. |
| `meta name="description"` | One or two plain sentences about this page and no other, at most 160 characters |
| `link rel="canonical"` | The address the page is served at, in full, built from `render_overview.SITE_URL`; a directory’s `index.html` is the directory |
| `og:title`, `twitter:title` | The page’s own name, without the project’s |
| `og:description`, `twitter:description` | The description, unchanged |
| `og:url` | The canonical address |
| `og:type` | `article` for the papers and the tutorial, with `article:published_time` and `article:modified_time` where the paper states its dates; `website` for every other page |
| `og:site_name`, `og:locale` | “The Squares Project” and `en_US` |
| `og:image`, `twitter:image` | The site’s one card, `social-card.png` at the site’s root, in full |
| `og:image:type`, `og:image:width`, `og:image:height` | `image/png`, 1200 and 630 |
| `og:image:alt`, `twitter:image:alt` | What the card shows |
| `twitter:card` | `summary_large_image` |
| `link rel="icon"` | The site’s icon, once (`render_overview.favicon_html`), which each shell writes beside the set |

The card is the overview’s hero, the best packing known of 53 squares, at 1200 by 630:
the hero’s own drawing in the light theme’s ink on its background, with the project’s
name under it as the bar sets the site’s name, drawn as outlines so no machine’s fonts
decide it. `devtools.social_card` draws it when the site is built, and it is not checked
in. Every page uses the one image, the papers included: their previews differ by title
and description, and the alt text stays what the card shows, since Open Graph’s
`og:image:alt` describes the picture and not the page.

A forwarder previews the page it leads to (`render_overview.forwarder_head`). An old
address is still shared, from dated records, other people’s pages and bookmarks, and
GitHub Pages cannot answer it with a redirect a crawler follows; the crawlers that draw
link previews run no script and do not reliably follow a refresh.
So a forwarder to a page of the site carries that page’s own identity: its head is
written from the record the page writes its own head from
(`render_overview.forwarded_metas`), so its canonical link and `og:url` are where it
leads, its name, its kind and its description are the page’s, a paper’s dates come with
them, and the card and the icon are the site’s. Its body still says the page has moved
and links it.
Until 2026-10-03 a forwarder carried only its title and its canonical link,
so a shared old link previewed as a bare title or as nothing.
The one forwarder that leads off the site, `defects.html` to the defect log on GitHub,
carries its title and a canonical link to that address, in full, and no card: the site
does not write the page it leads to, so its preview could not say what that page shows.

A result’s overview is a fragment fetched into a popover and has no head.
A case’s record file is the record alone but has the whole set and the icon, since it is
the address a case is shared by (**Case records**, above): its own name is “n = 11 ·
Case Records”, and its description a sentence of its own.

`check_published_site` holds the deployed pages to these rules after each deploy: one of
each tag and the site’s icon, the canonical link and `og:url` equal to the page’s
address, no description shared by two pages (a forwarder, which carries its page’s, is
not a page), each forwarder by its rule and to the name, kind and description of the
page it leads to, as that page’s own head gives them, and a card that is a PNG of the
declared size; it reads the case records it samples as pages.
`check_published_site --local DIR` asks the same of a built directory, and reads every
HTML file there that is a document (with a doctype, an `<html>` or a `<head>`), every
case record and any page no list names among them, so a page added later fails the check
until it carries the set; it holds a forwarder to the page it leads to wherever that
page is in the directory too.
`devtools.preview_site` runs it, and so do two of the Pages workflow’s jobs: `overview`
on its own build, which has no paper and no workbench, and `publish` on the assembled
site, where every forwarder is beside the page it leads to.
`check_published_site --local DIR --inventory` prints what every file’s head carries.

## Token Ownership

KPress owns the regular sans weight in `--kpress-font-weight-sans-regular`. Its font
generators read that token to produce matching math metrics and print faces; the paper’s
CSS and print instancer use the same source.
Change that token and regenerate the fonts, metrics, and prepared page together.
The loading and generation contract is documented in the
[KPress font and math architecture](../../../vendor/kpress/docs/project/architecture/arch-2026-09-08-font-and-math-loading.md).

`paper-type.css` owns the type base, the reading measure, the h2 scale, the heading
leading, the space around a section heading, the sans/prose size ratio, the paper’s
medium and bold weights and the role scales; the explainer’s shell and `site.css` alias
them and never restate them.
`--paper-font-size-support` sizes figure labels; `--paper-font-size-note` and
`--paper-note-inset` size and inset captions and endnotes.
They share `--paper-support-color` and `--paper-support-leading`. Resolve the sans base
once in the prose scope: nested sans components must inherit the resolved size without
multiplying the ratio again.
Apply print overrides at the same scopes as KPress theme declarations, including
footnote popovers.

The paper’s role sizes, heading scale, and reading measure are explicit choices, made
once for every page.
Certificate selection, interactive panels, and diagram geometry stay with the explainer.

An SVG’s declared font size is in its own coordinate system.
Audit the effective size after its `viewBox` and rendered dimensions scale the drawing;
matching a CSS number alone does not match the intended label size.
The shared script compensates font sizes using the SVG transform and updates them on
resize and when entering or leaving print.
Label rows leave room for the resulting text size.
On narrow screens, diagrams scroll horizontally rather than shrinking their labels.
Long figure notes remain HTML so they can wrap.

The 100-packing atlas is an explicit exception: it is a standalone SVG with its own
dense grid, title, and labels.
Enlarging every internal label to the figure-label size would obscure its cells.
Its caption uses the shared role; the linked full-size PDF provides the detailed view.

## The Papers’ Front

Every paper opens the same way, and one component writes it: `devtools.paper_front`,
from a small record each renderer keeps (`PaperFront`: the slug, the title, who oversaw
the paper, its agents, its version, its dates, the source it explains where that is
someone else’s work, and the series it is part of).
The page, the Markdown edition and the PDF, which takes its title and its dates from the
page, follow from that record; no article carries a copy, only the slot
`{{FRONT_MATTER}}`.

The front is, in order:

- **The formats row.** Three chips at the top corner of the page, on screen only: MD,
  the Markdown the page is rendered from, and PDF, its typeset PDF, each beside the page
  under its slug; then GITHUB, the project, with its mark.
  The row is navigation, so the Markdown edition leaves it out.

- **The title.** A Markdown `h1` in the hero, centred, in the page-title role.

- **The credits.** One line each, in the owner’s form (2026-10-01): names in bold,
  addresses as plain links, the version plain.

  ```
  From the original proof by **Queuingtheorydotcom**
  github.com/Queuingtheorydotcom/11SquaresOptimal

  Human oversight: **Joshua Levy**
  Agents: **GPT-6 Astra** and **GPT-6 Sol**
  Draft v0.1.5 (version history)
  Original proof September 29, 2026 · Last revised October 4, 2026

  Part III of 3 in the n = 11 series
  Part I: New Lower Bounds for Square Packing for n = 11
  Part II: A Review of the Certified Lower Bound s(11) > 31/8 for 11 Squares
  ```

  A paper that explains someone else’s work credits its source first, by the author’s
  name and the work’s address, and a line’s space sets the paper’s own credits apart; a
  paper that explains the project’s own proofs begins at its own credits.
  Then who oversaw it, the agents, the version line and the dates line, with a line’s
  space before the dates.
  The project’s repository is not a line of the credits on any paper: the footer every
  page carries names it, and so does the GITHUB chip.

- **The version line.** The paper’s own version, plain: `EXPLAINER_VERSION` for the
  explainer, `THRESHOLD_REVIEW_EDITION` (“Draft v0.1.0”) for the threshold-bound review
  and `OPTIMALITY_REVIEW_EDITION` (“Draft v0.1.5”) for the optimality review, all from
  `sqpack.release`. Never the site’s edition and never the data hash: the site’s version
  goes on no paper (the owner, 2026-10-01: papers are individually versioned, and a
  paper’s version history reflects versions of the paper, not of the website).
  A paper that has had more than one edition links its version history, the section at
  the foot of the explainer that lists the paper’s own editions (`EXPLAINER_HISTORY`),
  each with the day it was first published and what changed in the paper; a paper at its
  first version has no history to link.

- **The dates line.** One grammar on every paper: `<What> <Month D, YYYY>` parts joined
  by a middle dot. When first publication and revision fall on the same day, show
  “Published October 8, 2026” once.
  When they differ, show “First published” and end with “Last revised”, the day the
  article last changed.
  Source dates such as “Original proof September 29, 2026” keep their labels, even when
  they share a publication date.
  `paper_front` applies this display rule to HTML, Markdown, and the page printed as
  PDF. The source record retains both publication and revision dates for metadata.
  Every value is `sqpack.release`’s, and `devtools.artifact_dates` holds each to its
  rule.

- **The series strip.** Under the dates, after a line’s space, which part of the series
  the paper is (“Part II of 3 in the n = 11 series”), then each other part on a line of
  its own, by its numeral and its title, the title linking that paper.
  It is written from the site’s one list of papers, `render_overview.PAPERS`, through
  `paper_front.series(slug)`, so every paper names the others by the same titles and in
  reading order, I, II, III (the series plan, 2026-10-05). A link is page-relative on
  the page (`n11-optimality-review.html`), which works on the site and in a local
  preview, and the site’s address in the Markdown edition, which is read away from the
  site, as every link from one paper to another is (`devtools.paper_links`).

- **The closing.** The paper’s own last sections (the explainer’s version history, the
  review’s sources and verification record), then the footnotes, then the colophon every
  page shares (`render_overview.colophon_lines`), on a paper without its version part:
  the project and its repository, then “Formatted and typeset with Flowmark and KPress”.

In the Markdown edition the front is the title as a heading and the credits as a list,
one item a line, bold and linked as the page is.
In the head, the title is the paper’s name, without a site suffix, and the revised day
is `article:modified_time`; every paper’s first publication is `article:published_time`
(**Page Metadata and Social Cards**, above).

The credits are one grid column the width of the page (`.credits`, in the publication
layer), an address in them may break anywhere, and the three lines’ spaces are `1lh`, on
`.credits-source + .credits-own`, on `.publication-date` and on
`.publication-date + .series`.

`devtools.paper_structure` reads every rendered paper, from a built site or from the
published one, and prints every structural axis side by side, each paper against Part I:
the head, the formats row, the title, each line of the credits with what is bold and
linked in it, the version and dates lines, the series strip, the heading case (where
notation such as `s(11)` or `k-of-m` is not a word that takes a capital), the figures
and their captions, the tables, the footnotes, the closing, the Markdown edition’s
opening and the PDF’s title, size and dates.
A form axis is one every paper sets one way; a content axis is each paper’s own, such as
how many figures it has, or which part of the series it is.
`tests/test_paper_structure.py` fails when a form axis differs.
`devtools.measure_site_pages credits` measures the front as laid out, the kind, the
weight, the gap above and the width of every line and chip, and
`tests/test_site_glyphs.py` holds every paper’s front to the first’s in a browser at
1280 and 390 pixels.

## The n = 11 Series

The three papers on $n = 11$ are one series, read in order, and every listing of them
keeps that order: the Papers page, the home cards (one line of three), README and each
paper’s strip.
[The series plan](../../../docs/project/specs/active/plan-2026-10-05-n11-explainer-series.md)
holds the decisions and their evidence; these are the rules a change to any of the three
keeps.

| Part | Slug | Explains |
| --- | --- | --- |
| I | `n11-lower-bounds-explainer` | The project’s point and 2-of-3 certificates: T-018, T-025, T-026 |
| II | `n11-threshold-bound-review` | Kleddamag’s `s(11) > 31/8` (T-037): k-of-m charges, parents with strict cores over angle rows, the exact sweep |
| III | `n11-optimality-review` | Queuingtheorydotcom’s `s(11) = T` (T-060): cover, pose invariant, charge transfer, symmetry, capture, isolation |

- **Every paper stands alone, and each concept has one owner.** One paper derives a
  concept in full; another gives a recap of at most a paragraph that links the owner’s
  section. Part I owns the problem, sites, point charges (its “atoms”), cores, mass,
  event cells and the direction net; Part II owns which k-of-m families pay, parents and
  strict cores, the signed inclusion–exclusion and the exact sweep, and the boundary and
  attainment arguments; Part III owns the construction, the cover and everything after.
- **The papers link as a series.** Each lineage section names the previous paper as an
  antecedent, not a premise; each closing bridge names the next; each front carries the
  strip. A link from one paper to another is written `{{PAPER:<slug>#<anchor>}}` in the
  article and filled by the renderer (`devtools.paper_links`); it may name only a fixed
  heading, never one whose id is built from data.
  `check_published_site` holds every such link, on the page and in the Markdown, to a
  heading the target paper has, on the deployed site and on a local build
  (`preview_site --serve`), which are the only places all three papers are.
- **Every term is defined before it is used, in reading order.** That holds for words,
  symbols and lemmas. A roadmap or preamble may name a later concept only with a forward
  marker (“defined in Section 4”), a heading may name what its section defines, and a
  caption may use a term defined earlier but may define none.
  Each paper keeps a term registry, `templates/<slug>-terms.yaml`, and
  `devtools.paper_terms` walks the rendered page in document order and fails a use ahead
  of its definition, a definition outside its section, and a bold run in prose that
  defines nothing registered; `templates/n11-series-terms.yaml` names each shared
  concept’s owner, and a symbol that means two things in two papers fails unless the
  plan lists the clash.
- **Every formula is typeset, the same way in every paper.** A formula is LaTeX the
  page’s math pipeline sees, so no TeX ever reaches the reader as text: a display
  formula is a `$$` block in every paper, with a blank line before and after, never run
  into its sentence and never hand-wrapped; a caption in an HTML block writes its math
  the way its paper’s pipeline reads it there (`$…$` in Parts II and III, which
  `caption_math` typesets; a `<span class="tex">` run in Part I); and a title’s formula
  is math, which one shared rule (`.hero h1 .tex, .hero h1 .kpress-math` in
  `paper-publication.css`) keeps out of the hero’s caps.
  `devtools.paper_terms` rule 7 fails any `$` or TeX command left in a paper’s prose,
  captions or title, and any display formula outside a `$$` block.
- **Credit is accurate and early.** A review says in its first two sections what the
  source added and what it inherited, each item named by result id or source file.
- **One notation.** Part I’s symbols are fixed, because it is published and oldest; Part
  II fits around them, and Part III renames a symbol only where it clashes with Part I,
  and only to one that collides with nothing in the three papers or `TUTORIAL.md` §10.

The notation the series shares (the plan’s §3 has every row with its evidence):

| Object | Part I | Part II | Part III |
| --- | --- | --- | --- |
| Container side under test | $L_0$ | $L_0 = 191/50$ | $L_0$ (was $S$) |
| Proved bound | $L$ | $31/8$, or $L_0/A$; never $L$ or $T$ | $T$ |
| Parent side | — | $A = 764/775$ | local $A(a, b)$, $A_i$ (listed clash) |
| Core and its side | $Q_i$, $P$; $B$ | $Q$; $B$, one per row | $Q$; no $B$ (writes $(191/50)/U$) |
| Charge of a core | $\mu(Q)$, mass | $C(Q)$ | “charge at least $\Gamma_i$” |
| Per-core floor; total budget | $1$; $\sum w$ | $\Gamma$, $M$ | $\Gamma_i$ (was $q_i$); $b$ |
| Threshold set and size | $S$, $\lvert S\rvert$ | $S$, $m = \lvert S\rvert$ | — |
| Cores one charge pays | $r$ | $r$ | — |
| Packed square or parent angle | $\varphi$ | $\varphi$; a row covers $\tan(\varphi/2) \in [a, b]$ | $\theta_i$, $t_i$ |
| Net or core direction | $\theta_k = 2\arctan t_k$ | $\theta = 2\arctan t$ | — |
| Angle mismatch | $d$ | $d$ | — |
| Quarter turn | — | — | $\operatorname{rot}(x, y) = (-y, x)$ |
| Symmetry group | $\mathbf{D}_4$ | $\mathbf{D}_4$ | $\mathbf{D}_4$ |

The words follow the same rule: a *point charge* (Part I’s atom) and a *k-of-m charge*
(threshold k, m sites; never “m-of-k”) are the objects, and *the charge* $C(Q)$ is what
a core receives; “atom” appears in Parts II and III only to gloss Part I’s name.
A *site* is a charge’s position; Part III’s Voronoi sites are *cover sites*. A *bound
gap* is the distance from a bound to $T$, never a bare “gap”.
Each paper states one unnumbered **Theorem**; lemmas are bold-named, unnumbered and
unique across the series, and a reference across papers reads “Paper II’s Budget lemma”,
deep-linked.

## Figures

A figure is its drawing, centred in the column, with its caption under it.
The caption is a `figcaption` in the shared caption role, and it is where a figure’s
title and every sentence about it go.
A drawing carries its labels and nothing else: the name of a cell, a node or a panel, an
axis value, a short formula beside what it measures.
No title is lettered across the top of an SVG and no sentence under it.

A paper opens on its object.
Parts I and III open on a packing, set one way: the atlas rendering cut to its
container’s outline (`render_n11_lower_bounds_explainer.crop_to_container`), with the
atlas’s own lettering gone, in a centred stage (`.stage.trump`) 24rem wide on screen and
3in in print, linked to the rendering in the repository.
Part II’s object is a change of method, so it opens on its first figure, what changed
from T-026 to T-037 (the series plan amends “both papers open on a packing”,
2026-10-05). The optimality paper’s first figure used to be the atlas’s whole canvas,
960 units wide for a container of 536, with the atlas’s caption under the drawing: the
packing stood 18% of the figure’s width left of the column’s centre, over a line of its
own text.

The other diagrams of that paper carried a title or sentences of explanation in the
drawing as well; those are in the captions now.
What a caption states that is data, a count of rows, of regions or of margins, it names
as a placeholder (`{{LOCAL_MARGINS}}`) and the figure module supplies from the receipt
the figure is drawn from (`caption_facts`), so a caption cannot retype a number.
A caption writes its mathematics as LaTeX, as the prose does: a figure is an HTML block,
where KPress leaves `$…$` literal, so `render_n11_optimality_review.caption_math` puts
KPress’s math markup in its place for the page, and the Markdown edition keeps the
`$…$`. The formula is then set in the caption’s own sans, where it used to be Unicode
text in characters the sans does not carry.

`devtools.measure_site_pages figures` reports every figure: how far its drawing, and
what the drawing paints, stand from the centre of the column, the widest run of text in
it as a share of its width, any text that reads as a sentence, and its caption; each row
carries its problems.
A wide diagram that scrolls sideways on a phone and an apparatus with controls beside
its drawing are not held to the centre.
`tests/test_site_glyphs.py` holds every paper to none at 1280 and 390 pixels.

Parts II and III draw the same object the same way (the series plan, §6.1):

- **One stroke and colour role per object.** The container is a neutral outline; a
  parent is a filled square; a core is a dashed inner square; a point charge is a dot
  whose area is proportional to its weight, as in Part I; a k-of-m charge is a thin hull
  through its m sites with a `k/m` badge; a centre domain is hatched.
  The roles and the shared `_svg`, `_text` and `_polygon` helpers live in
  `devtools/paper_figures.py`, in fixed inks on a light ground.
  Part I’s canvas figures keep their own palette.
- **The series bound ladder** (`paper_figures.bound_ladder`): the rungs Stromquist
  (T-010), T-018, T-025, T-026, T-033, T-037 with T-061, and T-060 with Trump, evenly
  spaced and labelled with the register’s values, with no linear axis, since on one
  T-037 to $T$ is 0.0021 of the range.
  It is Part II’s second figure and stands in Part III’s lineage section.
- **Static SVG from hash-pinned data.** Every number a caption states comes from the
  figure module’s `caption_facts()`; a label uses only glyphs the shipped face carries
  ($\Gamma$, $L_0$, $\le$ and subscripts are typeset in the caption otherwise); and a
  figure fits 390 pixels without scrolling sideways.

## Print and Verification

Print uses Letter paper with 1.25-inch side margins and 0.75-inch top and bottom
margins, ragged-right prose, embedded reading fonts, and fractional glyph advances.
The title has extra top padding; page numbers sit inside the bottom margin and are
omitted on the first page.
Supporting text uses 1.4 line-height on the web and 1.32 in print.
Print source notes use compact list spacing and a 1.5rem gap before the colophon to keep
the closing credit on the same page.
Set the print SVG width before pagination so its font measurements match the exported
page. Interactive controls disappear, the default certificate determines the printed
figures, and the atlas occupies its own page.
Preserve the hierarchy when adjusting page breaks or figure dimensions.

From `packing/`, render and check the result:

```shell
uv run --frozen --all-extras --group dev python -m devtools.render_n11_lower_bounds_explainer --prepare-math
uv run --frozen --all-extras --group dev pytest tests/test_n11_lower_bounds_explainer.py -q
uv run --frozen --all-extras --group dev python -m devtools.inspect_n11_lower_bounds_explainer_typography --check-supporting --check-math --theme light
uv run --frozen --all-extras --group dev python -m devtools.inspect_n11_lower_bounds_explainer_typography --check-supporting --check-math --theme dark --width 390
uv run --frozen --all-extras --group dev python -m devtools.check_print_layout
uv run --frozen --all-extras --group dev python -m devtools.render_n11_lower_bounds_explainer_pdf --update
```

The typography check compares ordinary captions and endnotes with their shared role, and
figure labels with theirs, including effective SVG sizes.
It reports overlapping SVG label boxes and persistent link underlining.
Math and code have separate context and baseline inventories; semantic status labels
retain their distinct treatment.
Inspect the rendered page in both themes and the exported PDF, and check page breaks
after changing type size.
The generated editions live in `packing/site/`; publication and broader validation
requirements are in [development.md](../../../development.md).

The site pages are checked together by building the whole site and screenshotting every
page at a desktop and a phone width:

```shell
uv run --frozen --all-extras --group dev python -m devtools.preview_site --shots /tmp/shots
```

It scrolls each page to its foot first, so what a page places or loads lazily is in the
shot, and fails on console errors, a page wider than its viewport, math left untypeset,
any formula set in the wrong face (the Math rule above, its headline exception
included), and a row of cards off the centre of its line (more than a pixel between its
two slacks).
`--page cases/index.html#n-11` walks one page at a fragment, here the record
page showing case 11, which fetches its record from the build the preview serves, and
`--press SELECTOR` presses a card or an atlas cell on each page that has one, then walks
and shoots what it opened, since a popover a script fills has no math until it opens.
What a press opens is also checked for a word broken across lines, in the popover and in
a page it frames: a break between two letters or digits, or on a hyphen of a name the
site sets as code, unless the run is 24 characters or longer and wider than its line
(`preview_site.split_problem`). `devtools.measure_site_pages cards` reports the rows the
preview reads: each card section’s lines, their cards’ widths and the slack at either
end. `devtools.measure_site_pages ladders` reports the rating ladders as laid out: every
rung’s height, each description’s box and the lines its words take, the room between the
diagram and whatever clips it sideways, and with `--shots DIR` a picture of the diagram
at each width, light and dark.
`tests/test_site_ladders.py` holds those rows and that room in a browser at nine widths,
the narrowest of each layout among them.
`devtools.measure_site_pages math` reports every formula’s face beside its text’s,
counted by surface. `devtools.measure_site_pages glyphs` reports how every run of text
and every formula is drawn, and `--view problems` fails on a page set off the rules of
**Text** and **Math**, above: on a built site,

```shell
uv run --frozen --all-extras --group dev python -m devtools.measure_site_pages glyphs SITE --page papers/n11-lower-bounds-explainer.html --page papers/n11-optimality-review.html --view differences --markdown
```

lists every property the optimality paper sets differently from the explainer, and names
an address in place of `SITE` to measure the published pages.
`devtools.measure_site_pages space` reports the space around every table and heading
(**Spacing**, above).
`devtools.measure_site_pages popover` reports what each `--press` opens at each
`--width` and `--height`: the popover’s box, the window’s margin around it, whether it
scrolls itself, as the case popover does, or a frame inside it, the share of its content
it shows without scrolling, and its broken words.
`tests/test_site_math_faces.py` runs the same walk wherever a browser is installed, over
the overview, the results table, the Frontier page and the records of $n = 11$ and
$n = 29$, each record file served as the site serves it and shown in the record page,
with a control that marks a worded headline for serif math and requires the walk to name
it. `tests/test_site_case_records.py` serves the overview, the Frontier page, the record
page, every record file and the forwarders, and holds the ways in to a record in a
browser: a frontier row and an atlas cell open the case popover on the case’s record,
its visual summary first, which the arrow key and the record’s own step move to the next
case in place; a record file arrives at the record page with its own address and title,
a step pushes the next address and Back returns; `cases.html#n-17` arrives at case 17;
and without scripts a record file is read where it is.
`tests/test_overview.py` holds the cards and chips to the rules above.

The linear-program display is reflowed within the print column.
`check_print_layout` guards its width so an overflowing equation cannot silently shrink
the whole PDF page.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
