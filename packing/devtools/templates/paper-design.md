# Design System

This is the one description of how every page of the site looks: the explainer, the
overview, News, Atlas, About, case and result records, Frontier, papers, tutorials,
Visualize, and the profile directory and person profiles.
Each stylesheet implements what is written here and points back to it; when a page needs
something new, it is added here first and then to the stylesheet that owns it.

Shared foundations and component styles carry it, from the bottom up, with the paper’s
text tokens shared by all:

| Layer | File | Owns |
| --- | --- | --- |
| KPress | `vendor/kpress` | Fonts, Markdown typography, math, themes, print |
| Text | [paper-type.css](paper-type.css) | The type base, reading measure, heading scale, role scales and pinned faces every page shares |
| Paper | [paper-publication.css](paper-publication.css) | The publication layer every paper shares: figures, panels, components and print rules |
| Site | [site.css](site.css), [site-nav.css](site-nav.css) | Site pages and the navigation bar every page carries, the explainer and the workbench included |
| Site components | [site-result.css](site-result.css), [site-contributor.css](site-contributor.css) | Result articles and person profiles, using the shared text and overlay roles |

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
| Substantive section headings | 21.6px | 14.4pt | Serif italic, 1.2 of the prose base |
| Collection/navigation headings | 21.6px | Shared role | Sans upright at medium weight |
| Heading leading | 1.15 | KPress’s 1.2 | `--paper-heading-leading`: every heading, a card’s and a popover’s headline, and a page’s subtitle; the explainer’s hero title keeps KPress’s 1.05 |
| Space above a section heading | 48.6px | 37.8pt | `--paper-section-space`: 2.7 of the prose base on screen, 2.8 in print |
| Space below a section heading | 27.2px | 15.6pt | `--paper-section-space-below`: 1.7rem on screen, 1.3rem in print |
| Figure labels and controls | 18.05px | About 12.0333pt | Sans, 0.95 of the sans base |
| Captions and end footnotes | 17.48px | About 11.6533pt | Shared sans size: 0.92 of the sans base; 1.4rem side inset |
| Colophon | 16.15px | About 10.7667pt | Sans, 0.85 of the sans base |
| Navigation links | 17.48px | Not printed | Sans medium at the caption size, 0.92 of the sans base: one step under the prose |
| Section tabs | 15.73px | Not printed | The navigation size times the shared 0.9 button-label scale |
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

Text button labels share a small letter spacing through `--paper-button-letter-spacing`,
an alias of KPress’s existing caps spacing (0.021em). Native buttons, menu controls,
action links, chooser tabs and filter buttons use that one token; formulas keep normal
tracking.

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
Primary content uses the normal foreground (`--kpress-doc-text`), including
descriptions, handles, account links, result summaries, credits and resources.
Navigation and chrome always use the shared sans face: menus, contents links, collection
headings, disclosure labels, counts and browsing controls.
Substantive exposition remains serif, and an inline citation or link in that exposition
inherits its surrounding prose.
Standalone introductions use the shared serif prose face, including the homepage’s
contributor, reporting and learning invitations.
The retained `site-navigation-copy` class controls those introductions without making
their narrative into chrome.
`site-navigation-heading` is the sans collection-heading role, including profile
Records, Results, Credited Work, Other Reviewed Records, Resources, and Related News.
Tutorial, repository-document, and mathematical-paper sections retain serif exposition
headings. H1 and H2 labels use Title Case; mathematical symbols, identifiers, and proper
names retain their case.
Display-label corrections preserve existing anchor IDs.
Navigation, buttons, filters, table contents and metadata retain their sans roles.
All Results opens with its title and actions directly above the table, without an
introductory explanation of the register.

Secondary metadata such as dates, breadcrumbs, captions and provenance may use KPress’s
gray (`--kpress-doc-muted`, carried as `--site-support-color`) on the web and black in
print.

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
of 0.02, the most that keeps its dark fill in sRGB. Recorded results use yellow at level
2 without the chroma boost.
Incomplete results retain the shared lower-bound red diluted into the page background.
Superseded standings keep the neutral gray fill.
`devtools.rung_scale` computes these too, and `tests/test_rung_scale.py` holds this
table to its output and every ratio to 4.5:1.

| Status | Light fill | Text contrast | Dark fill | Text contrast |
| --- | --- | --- | --- | --- |
| `confirmed` | `oklch(78.5% 0.087 158)` `#88caa4` | 9.3:1 | `oklch(38.8% 0.069 158)` `#1f5036` | 7.9:1 |
| `reviewed` | `oklch(84.0% 0.063 250)` `#accef3` | 10.9:1 | `oklch(34.2% 0.050 250)` `#243a51` | 9.9:1 |
| `proved` | `oklch(78.5% 0.087 145)` `#96c897` | 9.3:1 | `oklch(38.8% 0.069 145)` `#2b4e2d` | 8.0:1 |
| `open` | `oklch(84.0% 0.083 95)` `#dbcb8c` | 10.9:1 | `oklch(34.2% 0.070 95)` `#443800` | 9.9:1 |
| `recorded` | `oklch(84.0% 0.063 95)` `#d7cb9c` | 10.9:1 | `oklch(34.2% 0.050 95)` `#413818` | 9.9:1 |

Result-kind tags in All Results and News topic tags share the same neutral background
and corresponding colored topic ink.
Verification, confirmation, status and significance keep their separate palettes.
Topic backgrounds intentionally match; the shared label and colored ink identify each
topic. `devtools.rung_scale` checks gamut and at least 4.5:1 text contrast in both
themes.

| Topic | Light fill | Text contrast | Dark fill | Text contrast |
| --- | --- | --- | --- | --- |
| `lower-bound` | `oklch(95.0% 0.004 265)` `#edeef1` | 7.3:1 | `oklch(29.0% 0.008 265)` `#292b2f` | 7.3:1 |
| `upper-bound` | `oklch(95.0% 0.004 265)` `#edeef1` | 6.8:1 | `oklch(29.0% 0.008 265)` `#292b2f` | 7.8:1 |
| `optimality` | `oklch(95.0% 0.004 265)` `#edeef1` | 7.3:1 | `oklch(29.0% 0.008 265)` `#292b2f` | 7.3:1 |
| `uniqueness` | `oklch(95.0% 0.004 265)` `#edeef1` | 7.0:1 | `oklch(29.0% 0.008 265)` `#292b2f` | 7.6:1 |
| `simplification` | `oklch(95.0% 0.004 265)` `#edeef1` | 7.0:1 | `oklch(29.0% 0.008 265)` `#292b2f` | 7.6:1 |
| `formalization` | `oklch(95.0% 0.004 265)` `#edeef1` | 7.0:1 | `oklch(29.0% 0.008 265)` `#292b2f` | 7.6:1 |
| `rigidity` | `oklch(95.0% 0.004 265)` `#edeef1` | 7.0:1 | `oklch(29.0% 0.008 265)` `#292b2f` | 7.6:1 |
| `case-exclusion` | `oklch(95.0% 0.004 265)` `#edeef1` | 7.0:1 | `oklch(29.0% 0.008 265)` `#292b2f` | 7.6:1 |
| `restricted-optimality` | `oklch(95.0% 0.004 265)` `#edeef1` | 7.0:1 | `oklch(29.0% 0.008 265)` `#292b2f` | 7.6:1 |
| `method-limit` | `oklch(95.0% 0.004 265)` `#edeef1` | 7.0:1 | `oklch(29.0% 0.008 265)` `#292b2f` | 7.6:1 |
| `correction` | `oklch(95.0% 0.004 265)` `#edeef1` | 7.0:1 | `oklch(29.0% 0.008 265)` `#292b2f` | 7.6:1 |
| `audit` | `oklch(95.0% 0.004 265)` `#edeef1` | 7.0:1 | `oklch(29.0% 0.008 265)` `#292b2f` | 7.6:1 |
| `project` | `oklch(95.0% 0.004 265)` `#edeef1` | 7.1:1 | `oklch(29.0% 0.008 265)` `#292b2f` | 7.5:1 |
| `engineering` | `oklch(95.0% 0.004 265)` `#edeef1` | 7.2:1 | `oklch(29.0% 0.008 265)` `#292b2f` | 7.4:1 |
| `verification` | `oklch(95.0% 0.004 265)` `#edeef1` | 7.0:1 | `oklch(29.0% 0.008 265)` `#292b2f` | 7.6:1 |

Result-kind tags, News tags, dropdown options and selected summary chips share one
neutral surface: `--site-news-topic-bg` is `oklch(95% 0.004 265)` in light mode and
`oklch(29% 0.008 265)` in dark mode.
Their text uses the corresponding topic hue; uncoded subjects retain neutral ink.
All options retain that surface when unchecked, selected or hovered; a visible check
identifies selection.
Status, result-kind and significance palettes are unchanged.
The shared ink lightness/chroma tokens give every News label at least 4.5:1 contrast on
the neutral surface in both themes, measured below.

| News topic | Light | Against the neutral surface | Dark | Against the neutral surface |
| --- | --- | --- | --- | --- |
| `lower-bound` | `oklch(43.0% 0.080 25)` `#763d39` | 7.3:1 | `oklch(80.0% 0.090 25)` `#f2a7a1` | 7.3:1 |
| `upper-bound` | `oklch(43.0% 0.080 145)` `#315b33` | 6.8:1 | `oklch(80.0% 0.090 145)` `#99ce9a` | 7.8:1 |
| `optimality` | `oklch(43.0% 0.080 310)` `#5d4371` | 7.3:1 | `oklch(80.0% 0.090 310)` `#d0aeea` | 7.3:1 |
| `uniqueness` | `oklch(43.0% 0.000 265)` `#505050` | 7.0:1 | `oklch(80.0% 0.000 265)` `#bebebe` | 7.6:1 |
| `simplification` | `oklch(43.0% 0.000 265)` `#505050` | 7.0:1 | `oklch(80.0% 0.000 265)` `#bebebe` | 7.6:1 |
| `formalization` | `oklch(43.0% 0.000 265)` `#505050` | 7.0:1 | `oklch(80.0% 0.000 265)` `#bebebe` | 7.6:1 |
| `rigidity` | `oklch(43.0% 0.000 265)` `#505050` | 7.0:1 | `oklch(80.0% 0.000 265)` `#bebebe` | 7.6:1 |
| `case-exclusion` | `oklch(43.0% 0.000 265)` `#505050` | 7.0:1 | `oklch(80.0% 0.000 265)` `#bebebe` | 7.6:1 |
| `restricted-optimality` | `oklch(43.0% 0.000 265)` `#505050` | 7.0:1 | `oklch(80.0% 0.000 265)` `#bebebe` | 7.6:1 |
| `method-limit` | `oklch(43.0% 0.000 265)` `#505050` | 7.0:1 | `oklch(80.0% 0.000 265)` `#bebebe` | 7.6:1 |
| `project` | `oklch(43.0% 0.080 70)` `#6b4716` | 7.1:1 | `oklch(80.0% 0.090 70)` `#e3b47d` | 7.5:1 |
| `engineering` | `oklch(43.0% 0.080 45)` `#744029` | 7.2:1 | `oklch(80.0% 0.090 45)` `#efac8d` | 7.4:1 |
| `verification` | `oklch(43.0% 0.080 250)` `#2a527a` | 7.0:1 | `oklch(80.0% 0.090 250)` `#91c3f6` | 7.6:1 |

### Significance and the Other Inks

A significance rung is drawn in an ink of its own on the page, not on a chip:
`--site-significance`, a dark teal at hue 205, between the confirmation green and the
verification blue so it reads as neither, and darker and bluer than the accent so it
never reads as a link; it is light in dark mode.
Every score uses `overview_sections.significance_mark`: an S label and five segments in
one square-cornered border box, 4.8em wide at the shared note size and sans medium
weight. The label and bars have a 0.18em gap, smaller than a word space but visibly
separate. Each bar is 0.5em wide and 0.6em tall; the first S bars are solid and the rest
are empty outlines. The border uses the label’s own ink, with 0.18em horizontal padding.
The box keeps the same width from S0 through S5, while its accessible name states the
score and its tooltip gives the level’s meaning in the rubric that scored it: a result’s
from the significance ladder in `epistemics.md`, a News post’s from the short label
rubric in `result-import.md` (“Label the PR and Prepare News”). News, Results tables,
ladders, result overviews, case records and popovers share this component; significance
continues to describe importance rather than V/C assurance.
It keeps the shared chip height, 1.45em. It is the second column of a table of results,
narrow, and it stands first among the rungs in a result’s overview, a case record and
the rating ladders.

Recent contributions use the warm `--site-new-result` text ink, lighter in dark mode.
Bound and proof indicators use red for recent contributions.
`devtools.rung_scale` measures both inks against the page’s background in each theme,
and `tests/test_rung_scale.py` holds this table to its output.
Both inks stay inside sRGB and exceed 4.5:1 against the page in each theme.

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
| `--kpress-measure` | 35em of the shared prose base | 630px at the 18px base; the width of actual prose, excluding padding |
| `--kpress-font-size-h2` | 1.2 of the base | 21.6px at every width; KPress steps it to 1.4 from a 64rem pane |
| `--paper-font-scale-sans` | 19/18 | The 19px sans base of captions, cards and notes |
| `--paper-font-weight-sans-medium`, `-bold` | 550, 680 | The sans medium and bold |
| `--paper-title-scale`, `-subtitle-`, `-support-`, `-note-`, `-colophon-` | 1.5, 1.25, 0.95, 0.92, 0.85 | The roles in the table above |

What a reader sees, measured with `devtools.measure_site_pages type` on the explainer,
the tutorial, the readme and the homepage, identical on all four where the role occurs:

| Role | Face | Size / line height at 1280px | At 390px |
| --- | --- | --- | --- |
| Paragraph and list item | PT Serif | 18 / 27px | Same |
| h1 (page title) | Source Sans 3, upright caps | Shared page-title role | Same |
| h2 | PT Serif italic | 21.6 / 25.92px | Same |
| h3 | Source Sans 3, 550 | 21.6px | 20.7px |
| h4 | Source Sans 3 italic, 540 | 21.6px | 20.16px |
| Table cell | Source Sans 3, 410 | 17.1px | 16.2px |
| Inline code | Planetaire Mono Text | 14.76 / 22.14px | Same |
| Inline math | KPress Math Text (serif) | 18px, the text’s own em | Same |
| Reading column | — | 630px: the shared 35em prose measure | The column less the page and document gutters |

h3 and h4 keep KPress’s own step up at a 64rem pane.
Every published page H1 uses the shared upright sans-serif, all-caps title treatment,
including Markdown reports, the profile directory and profiles.
The explainer retains its publication title size (28.5px); mathematical notation
preserves its case and face.
The homepage sets its summary lists and tables a step smaller, in `site.css`.

**Line breaks.** No text on the site breaks inside a word.
KPress sets `overflow-wrap: break-word` on every page, which cuts a run of characters
only when it is longer than a whole line.
The site adds `overflow-wrap: anywhere` in two places, both runs with no space in them
by nature: a case record’s exact decimal (`.site-case-decimal`, as many as 67 digits)
and a repository path in a result overview’s links (`.site-result-links code`).
`anywhere` also lets a grid column or a table cell shrink to one character, which sets a
label a letter to a line, so it never goes on prose, on a label or on a column holding
either. Contributor names, source labels, locators and credited-work lists keep normal
word wrapping; an unbroken identifier or URL wider than its whole line can wrap with
`break-word`. No sheet uses `word-break` to break words, and none hyphenates.
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
always draws at 410. Every rule in `site.css`, `site-result.css` and
`site-contributor.css` that sets the sans face also sets its shared weight, which
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
| Caption | Shared support leading 1.4; 16.15px under the homepage’s hero, 17.48px elsewhere | The papers’ `--paper-support-leading`; the hero’s caption is a size of its own in `site.css` |
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

Tutorial diagrams use the same semantic `figure` and `figcaption` components as the
papers. Wide atlas canvases use the papers’ existing `crop_to_container` view for the
packing itself, with the same shared 24rem stage width; source SVGs remain intact.
The composed quotient-map, certificate, and owner-case diagrams retain their full
viewports. Images remain centred by KPress; captions use the shared sans note size,
support leading, note inset, and caption spacing tokens from `paper-type.css`. Caption
prose is upright, and links, mathematical notation, and evidence qualifications remain
part of the caption.
Tutorial H3 labels consistently use Title Case while their case-insensitive anchor
addresses remain stable.

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
The main case-record interval below the icons and the visual summary’s bound statement
use serif text with serif math.
The number-line labels and detail panels remain sans.
A card’s headline and note are prose whose mathematical runs are set as math, so a case
a note names, such as $n = 21$, is sans math too, never upright words.
Documents write math as LaTeX (`$…$`) rather than in code spans;
`devtools.check_math_markup` holds the documents already migrated to it.
Code uses Planetaire Mono Text at KPress’s calibrated monospace size.
Literal source code keeps its Unicode characters.
Two site-only KaTeX subsets supply AMS’s blackboard-R outline for `ℝ` and Main’s
outlines for `↔` and `≤` within the monospace family, preserving ordinary ASCII glyphs
and metrics.
Both subsets travel through the shared asset bundle; standalone paper styles
keep their existing declarations.

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
Every page `render_overview.kpress_page` or `static_content_page` writes names the same
shared stylesheets and scripts: KPress’s stylesheets with their faces, KaTeX’s pruned
stylesheets and faces, the relation glyphs, `paper-type.css`, `site-nav.css`,
`site.css`, `site-result.css` and `site-contributor.css`, the math pipeline, KPress’s
flattened client behaviors and the page’s own programs.
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
- **Article programs.** Record shells precede their classic programs.
  The shared article loader precedes generic popover handling and the row and case
  controllers. Person-name links navigate directly to complete profile pages.
  Input responses can fetch a complete record page and its declared prepared-math asset;
  only the selected article enters the host document, under the loading, ID and focus
  contract in **Article Pages and Overlays**, below.
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
The subsequent measurement used `cases/index.html#n-11`; this table has no row for that
intermediate directory.
The current directory is Atlas, and individual records are complete pages at
`cases/N.html`.

That one page was slow before any math ran: it carried every case’s record in one 9MB
document, and parsing and styling that took several seconds on its own (think-cy3a). The
intermediate record directory carried the index alone, 1.9MB, and fetched one record.
The current publication contract is described under **Case records**, below.
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
| From the bar’s rule to the breadcrumb | Shared trail margin | 1rem, 16px | `site-nav.css` |
| From the breadcrumb to a page’s title | Shared trail margin | 2.5rem, 40px; paper format chips occupy part of this gap | `site-nav.css` |
| Fallback opening space where the trail is absent | `--site-page-top` | 4rem, 64px | `site-nav.css` |
| How much nearer the bar an opening picture starts | `--site-hero-lift` | 0.5rem, 8px | `site.css` |
| Above a section heading (`h2`) | `--paper-section-space` | 2.7 of the prose base, 48.6px | `paper-type.css` |
| Below a section heading (`h2`) | `--paper-section-space-below` | 1.7rem, 27.2px | `paper-type.css` |
| Above a visible site-title H1 or H2 | `--site-title-space-above` | 6.25rem, 100px | `site.css` |
| Below a visible site-title H1 or H2 | `--site-title-space-below` | 2rem, 32px | `site.css` |
| Below a page’s title, and below its subtitle | `--site-subtitle-space` | 2rem, 32px | `site.css` |
| Above and below a table | `--site-table-space` | 2rem, 32px | `site.css` |
| Above and below a tally set as its own line | `--site-tally-space` | 1.25rem, 20px | `site.css` |
| Between a wide block and the edge of the page’s content area | `--site-wide-gutter` | 0.5rem, 8px | `site.css` |

A page’s title, or the picture that opens the homepage, starts `--site-page-top` under
the bar’s rule on every page, the explainer and the optimality paper included.
The Videos page and the Workbench carry no section tabs under that rule since
2026-10-22; like every page with a trail, theirs starts 1rem under the rule.
Every section heading on the site pages and the explainer takes the two section tokens;
print reads its own values of both (2.8 of the base and 1.3rem), which are the paper’s.
On the explainer the credits start 2.25rem under the title on screen and 2rem in print.

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

### Tallies

A tally is a line of counts with a dot between each two, such as the profile directory’s
“75 people · 114 records · 219 results · 725 credits · 48 resources”.
Every tally is spaced by the same two tokens (the owner, 2026-10-23: “a little more gap
around the tallies, as a vertical gap as well”).

- **Between counts.** Every dot is `site_tallies.TALLY_SEPARATOR`, a span holding a
  space, the dot and a space, and no renderer joins counts with a bare dot.
  `--site-tally-gap` (0.15em) widens each of its two word spaces, so the dot stands
  0.35em from the counts in the site’s sans, the space the dot between a result’s record
  links has. It was one word space, 0.2em. The spaces stay in the text, so a long tally
  still wraps beside a dot.
- **Above and below.** A tally set as a line of its own, the directory’s summary and a
  profile’s stacked Records, Results and Credits, stands `--site-tally-space` (1.25rem)
  clear of the blocks either side, on screen; it took a paragraph’s 0.75rem. Where a
  larger margin meets it, a table’s below the directory’s summary or a section heading’s
  below a profile’s counts, the larger one stands.
  A card’s tally keeps the card’s own padding, and a table cell’s keeps the cell’s.

`tests/test_overview.py` pins both tokens and the rules that read them;
`tests/test_site_navigation.py` measures them in Chromium on the directory’s summary and
a profile’s counts and resource cards.

## Article Pages and Overlays

Case records, result records and person profiles are complete HTML pages.
Their addresses carry the site’s navigation, colophon, shared styles, prepared
mathematics where needed, and metadata.
An ordinary link reaches the complete record with scripts disabled, from a local file,
or when enhancement fails.
The same article can appear in an overlay on another page; its content and source links
come from its complete page.

| Component | Complete address | Native entry | Enhancement |
| --- | --- | --- | --- |
| Case record | `cases/N.html` | Case link, index entry or neighboring-record link | `a[data-case]`, atlas tiles and frontier rows load `article.site-case` in the shared case panel |
| Result record | `result/t-nnn.html` | Result ID link or **Open Result Record** | Pressing the rest of a result row loads `article.site-result[data-result-overview]` in that row’s panel |
| Person profile | `profiles/ID.html` | Public-name link | Native navigation reaches the complete profile from every page and open article panel |
| Profile directory | `profiles/index.html` | Home/About **All Profiles** button or About navigation menu | Full public names, reviewed-result/significance and credit tallies, resource counts, and public account links in a surname-sorted native table; name links navigate directly to profiles |
| News article | `news.html#ID` | Linked announcement title or bookmarked article | Homepage and archive reuse the authored article; its profile links navigate directly |
| Card preview | The card’s ordinary target | Native `popovertarget` button and action link | The card’s preview remains authored in the page; it is not an article fetch |
| Framed card preview | Target page with `?view=embed` | Native card button and **Expand** | The frame loads on first opening and uses its own document |

The components have one article-loading boundary,
[article-loader.js](../overview/article-loader.js), exposed as
`siteArticles.loadArticle(address, selector)`. It accepts same-origin HTTP(S) pages,
fetches their HTML, and parses it in an inert template.
It selects only the named article and removes script elements from it; fetched page
programs never run.
Relative links and images resolve against the response URL, including
after a redirect. Local fragments target the copied article when their IDs exist there,
and otherwise resolve against the complete page.

The loader caches pristine articles by URL and selector and gives each consumer a new
clone. Each clone gets a unique ID prefix, with matching fragment, ARIA, label and SVG
references, so a heading, source anchor or SVG definition cannot collide with the host
page or another record.
It loads the page’s declared prepared-math stylesheet from the shared CSS assets before
returning the article.
Mathematics is already prepared by the renderer; the overlay does not execute the
fetched page’s math or theme programs.
Failed article and stylesheet requests leave no successful cache entry and can be
retried.

Renderers put the overlay shells before their classic programs.
Program order is the shared article loader, generic popover handling, then the relevant
row, case and contributor controllers.
`kpress_page` and `static_content_page` supply these shells and programs, including on
standalone records, so a profile reached from a case can navigate to another case.
The generic handler keeps local source-anchor navigation inside a panel and closes it
for ordinary links leaving the panel.
Legacy card previews still use their native markup and their own body or frame.

Opening a case moves focus to its close button.
Escape and outside clicks close it.
Replacing a case or result panel hides the source panel and retains the original page
opener as the return target.
Closing restores that target when it remains connected and the reader has not moved
focus elsewhere. Person-name links navigate directly to profiles, including from an open
panel. Modified clicks and explicit new-tab links keep native navigation.
Case requests use a generation counter; a newer request, Escape, or a closed source
panel prevents a late success or failure from reopening a panel or navigating.
Result bodies have their own per-panel generations and retry on a later opening after
failure. Browser tests exercise these sequences on generated pages.

| Responsibility | Source owner | Retained checks |
| --- | --- | --- |
| Shared text, spacing, themes and overlay frame | `paper-type.css`, `site.css`, `site-nav.css` | `test_site_text_tokens.py`, `test_site_glyphs.py`, `test_site_wide_blocks.py`, `test_overview.py` |
| Case article, Atlas directory and panel | `render_case_pages.py`, `forward.js`, `case-popover.js` | `test_site_case_records.py`, `test_site_math_faces.py` |
| Result article and row entry | `result_overview.py`, `render_overview.iter_result_fragments`, `overview_sections.py`, `row-popover.js`, `site-result.css` | `test_result_overview.py`, `test_site_result_popover.py`, `test_site_case_records.py`, `tests/node/overview_rows/` |
| Contributor article and directory | `render_contributors.py`, `site-contributor.css` | `test_render_contributors.py`, `test_site_contributor_popovers.py` |
| Canonical News articles, homepage selection and direct profile links | `render_changelog.py`, `news_highlights.py`, `site_topics.py`, `site.css` | `test_changelog.py`, `test_news_highlights.py`, `test_site_homepage.py` |
| Inert fetch, cache, scoped IDs, replacement and focus | `article-loader.js`, `popover.js` and the article controllers | `test_site_contributor_popovers.py`, `test_site_case_records.py` |
| Identity and reviewed credit spans | `sqpack.contributors`, `sqpack.contributor_occurrences`, `contributor_credit.py` | `test_contributors.py`, `test_contributor_occurrences.py`, schema gate |
| Routes, metadata, build inputs and sparse evidence | `site_urls.py`, `site_documents.py`, `preview_site.py`, `pages_scope.py`, `run_negative_controls.py` | `test_site_urls.py`, `test_site_documents.py`, `test_pages_scope.py`, `test_snapshot_copy_roster.py` |

Test filenames in this map are under `packing/tests/`; browser programs are under
`packing/devtools/overview/`. Publication verification reads every complete page’s head
and fetches the result pages named by the tables.
Component changes update this guide and their owning stylesheet or renderer together;
plans point here for presentation contracts.

## Site Components

Each component has one owning stylesheet and renderer, listed in **Article Pages and
Overlays**, above. Shared frames and controls live in [site.css](site.css); result and
contributor articles use their component sheets and the same text tokens.

- **Navigation bar.** One fixed-width row of sans links in the page’s header slot, the
  same on every page, the explainer and the workbench included, led by the site name,
  “The Squares Project”, set in capitals by CSS (`text-transform`, lightly tracked) so
  its text is unchanged, and a step heavier.
  The bar’s type is tied to the body’s on the scale above (Typography Roles), never set
  in pixels or rem. A link is one step under the 18px prose and no more: the caption
  size, 0.92 of the sans base, 17.48px, which is the first size of the scale under 18px
  (`--site-nav-font-size`; the step between, 0.95, is 18.05px, not under the prose).
  Section tabs apply `--paper-button-label-scale`, 0.9, to that navigation size, giving
  15.73px. The site’s name is the sans base, 19px (`--site-nav-name-size`), the size
  sans text takes beside the prose, so with its weight and capitals it reads as the
  name. Both tokens are in `site-nav.css` and are computed from the host base
  (`--kpress-host-font-size-base`), which is the same on every page, so the bar is one
  size on every page and at every width.
  `devtools.measure_site_pages header` reports the four sizes, `preview_site` fails a
  page whose bar is not one step under its body (`type_problems`), and
  `tests/test_site_wide_blocks.py` holds the relation in a browser at 1280, 768 and 390
  pixels, where desktop links keep one line and the phone exposes a Menu control.
  The name’s text stands on the links’ baseline.
  The bar aligns its items by their baselines (`align-items: baseline`), and each label
  stays on one line, with no offset in pixels.
  Every item of the bar is set on one line, `--site-nav-line`, a length (1.43 of the
  link size, the face’s own leading there), so the larger name is no taller than a link:
  the links stand where they do without the name, and the current link’s underline is
  the same distance over the rule at every width.
  `devtools.measure_site_pages baselines` reports each label’s baseline, measured with a
  zero-size inline box on the text’s line and not read from a box’s edge; `preview_site`
  fails a page whose name or links are off by more than half a pixel
  (`baseline_problems`); and `tests/test_site_wide_blocks.py` holds it in a browser.
  Below 72rem the home link reads “Squares”, also set in capitals, to leave room for the
  destinations. At every width its accessible label is “The Squares Project home”.
  Every item takes the cards’ gentle wash on hover and nothing underlines on hover; the
  current page alone is underlined in the accent; a current ancestor uses accent text at
  the shared sans bold weight (680) without an underline.
  The edition appears only in the closing credit (below).
  Every page renders it from the one partial, `site-nav.html`, and it has the same box
  on every page at every width.
  The shared Headroom carrier is sticky and preserves its place in the document.
  Scrolling down hides it; the first meaningful upward scroll shows it again.
  It stays visible at the top, while navigation has focus, and while the theme menu is
  open, or while a navigation disclosure is open.
  Resize and anchor navigation account for the full carrier height, including tabs;
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
  Its five entries are **Overview**, **News**, **Results**, **Learn**, and **About**, in
  that keyboard order, followed by the GitHub and theme utilities.
  Overview and News link directly to their pages.
  Results, Learn, and About each use one button containing the label and chevron.
  The whole button opens its list.
  Its first entry leads to substantive content: Visual Atlas, Tutorials, or The Squares
  Project. Results, Learn and About have no category page or URL. Results contains Visual
  Atlas (`atlas.html`), Frontier Survey (`frontier.html`), All Results (`results.html`),
  Verification (`verification.html`), and Report a Result (`report.html`), in that
  order. About contains The Squares Project, Contributor Profiles, and Project
  Documentation. The hierarchy and destination paths live in `site_navigation.py`;
  `site-nav.html` supplies the shared shell.
  Learn puts Tutorials first, followed by Papers.
  The Tutorials page ends with a shared **Read Papers** action to `papers.html`.

  Each unified trigger uses the navigation face, line, medium weight, and muted text,
  with a Lucide chevron at `--site-icon-size`, aligned on the capital height.
  Labels retain Title Case.
  A button has a minimum 2rem square target; its open or hovered state takes
  `--site-wash` and accent text.
  The menu chevron retains its down-pointing closed state and up-pointing open state.
  Expansion uses a negative 180-degree turn; collapse reverses the same path to zero.
  This changes its travel direction while preserving both resting states.
  Native disclosures retain their existing glyphs and states.
  The list uses the page background, document border, and shared shadow, with 0.3rem
  inner padding and links padded 0.45rem by 0.7rem. Links and buttons show a 2px
  document-link outline with 2px clearance on keyboard focus.
  The current content link and its top-level category are underlined; an ancestor uses
  the accent and shared sans bold weight (680). A fragment destination does not also
  claim the current page.

  `overview/navigation.js` enhances ordinary navigation lists, without application-menu
  roles. Enter or Space toggles the unified button; Tab follows ordinary document order.
  Escape closes the open list and restores its button.
  Outside activation closes the list without preventing the target action.
  Opening a group closes its sibling, and opening a theme or article popover dismisses
  navigation disclosures.
  Arrow Down or Up on a disclosure opens the list and focuses its first or last link.

  Below 48rem, a labelled Menu button exposes the same groups vertically.
  The unified triggers fill their row, have at least 2.5rem height, and reveal their
  children beneath the parent.
  The open navigation scrolls within the available viewport height.
  The shared head bootstrap reserves the collapsed navigation geometry before paint, so
  the footer controller does not shift a paper when it initializes.
  Without JavaScript, enhancement buttons are hidden and the content links remain
  exposed. Print and embedded articles omit the global header.

  Category and nested pages carry a sans, muted breadcrumb trail above their title, at
  the shared note size and support leading, 1rem below the navigation and 2.5rem above
  the title. Its first label aligns with the header logo text, independently of the
  35em/630px prose column.
  The trail replaces the article’s usual top gap.
  Ancestors with a destination are links; Results, Learn and About are plain container
  text with no URL. Chevrons separate the items, and the current title is plain text
  with `aria-current="page"`. Standalone pages with no parent, including Overview and
  News, omit both the visible trail and BreadcrumbList data.
  Learn has no category page; its content pages carry the plain Learn ancestor.
  Below 40rem, trails with at least three items put the current page on its own row, so
  the arriving sans face cannot move it between the ancestry’s rows.
  The trail shares the header’s 70rem content track, responsive gutters and link
  hit-area inset through `--site-nav-track`, `--site-nav-gutter`,
  `--site-nav-link-inset` and `--site-nav-name-outset`. Its smaller sans type does not
  change that geometry.
  Contributor profiles and the directory retain the same 35em text width as other prose.
  Tables and figures keep their wider tracks.
  `site_navigation.py` supplies the same ancestry for the visible trail and structured
  BreadcrumbList data.
  Cases belong to Results → Visual Atlas, result articles to Results → All Results,
  profiles to About → Contributor Profiles, chapters to About → Research Synopsis, and
  verification guidance to Results.
  Paper details link their Papers catalogue; the tutorial articles link their Tutorials
  catalogue after Learn.
  Overlays and print hide the visible trail.
  The workbench is an application rather than a KPress page, so its build
  (`workbench_tools.build_site`) takes the bar, its stylesheet, the theme bootstrap and
  the theme control’s script from `render_overview.nav_shell`, in a shell that gives it
  the page margins and header rule KPress gives the others; the application fills the
  window below it. Only the shared bar and trail follow the theme there: the workbench
  itself has no dark mode yet.

- **Videos and Workbench.** Videos (`visualize.html`) and Workbench (`workbench/`) are
  separate destinations in the Learn dropdown.
  Neither page carries a Film/Workbench switcher below the global navigation.

- **View choosers.** The Atlas’s Grid and Triangle views and its S, M, L and XL tiles
  use the shared `.site-tabs` strip inside the page.
  These are in-place tablists of buttons, with the selected view filled by the shared
  current-item tint. The strip uses the navigation’s sans size, medium weight, square
  corners and thin border.
  It does not add a second row of page navigation below the header.

- **Theme control.** A small gray Lucide Contrast icon, an inline SVG, ends the
  navigation bar on every page, the explainer and the workbench included.
  It follows GitHub within the centered navigation track at every width.
  Its SVG is centered on the navigation font’s capital height; its wrapper shares the
  text baseline. It takes the nav items’ wash on hover and while its menu is open, and
  never underlines. Pressing it opens a compact menu, a native popover under the icon
  with square corners and the cards’ border and shadow, of three choices, each an icon
  and a word: System, Light and Dark.
  The current choice is in the accent with a check at its end.
  Choosing applies at once, closes the menu and keeps the choice across pages and
  visits; the menu also closes on Escape, an outside click or tabbing away.
  The icon is a button named “Color theme” with `aria-haspopup="menu"` and
  `aria-expanded`; the menu is a `role="menu"` of `menuitemradio` items carrying
  `aria-checked`, and the arrow keys, Home and End move between them.
  On a phone the whole bar wraps onto centred lines, so every link stays in view, and
  the icon ends the last line.
  The choice is KPress’s own reader preference, the `kpress.theme` key its head
  bootstrap applies before first paint, so no page flashes the wrong theme and every
  stylesheet keys only on `data-kpress-resolved-theme`, never on `prefers-color-scheme`.
  System follows the operating system as it changes.
  The embed view has no navigation bar and so no theme icon, and a framed page follows
  the choice its parent makes, live.
  `overview/theme.js` is the script, and it announces a change as `squares:themechange`
  for anything drawn on a canvas.
  The Lucide Contrast geometry uses a filled half-disc and the shared icon size.
  The chooser has words beside its icons.

- **Closing credit.** Every ordinary site page ends with three centered lines: project
  and repository attribution, the linked typesetting tools, and the current edition.
  Papers omit the site edition because their own edition is in their title credits.
  Footer links keep their text and destinations without decorative brand or
  external-link icons; body links retain their usual icon treatment.

  > The Squares Project · github.com/jlevy/squares\
  > Formatted and typeset with Flowmark and KPress\
  > v0.4.2-8ac5de

  The version is `sqpack.release.PUBLICATION_EDITION`, never a typed page-specific
  value. `render_overview.colophon_lines` writes the same attribution and tool links for
  ordinary pages and papers; `colophon_html` adds the ordinary site wrapper.
  Each line is a block (`.site-colophon-line`) and each part beside a middle dot is an
  inline block (`.site-colophon-part`), so a narrow line wraps at a dot before breaking
  within its text. The shared footer-specific rule suppresses generated link icons
  without removing or rewriting the anchors.
  The Workbench application has no footer; its stage carries the publication version.

- **Homepage.** Its menu label is **Overview**; its browser title and link preview are
  the project’s name, **The Squares Project** (the owner, 2026-10-23); its opening H1
  remains **The Square Packing Problem**. Two readable introductory paragraphs define
  the problem and explain upper and lower bounds.
  The sections continue with Visual Atlas, Recently Added (`think-rqen`), News, Results,
  Profiles, Report a Result, Learn, Visuals, About the Squares Project, and More
  Resources. Learning cards preview the Papers and Tutorials catalogues.
  Visuals previews the poster and inline video, with actions to Posters, Videos and
  Workbench. About the Squares Project links directly to `about.html` without repeating
  the documentation catalogue, and retains the old `#squares-project-documentation`
  anchor. Project Documentation remains its own page under About.
  About uses the same site-title styling as The Squares Project (`think-6m9n`,
  `think-sq1i`). Every visible `h1.site-title` and `h2.site-title` shares the
  screen-only 6.25rem margin above it and 2rem below it (`--site-title-space-above` and
  `--site-title-space-below`); compact Legend and introduction-card headings keep their
  own spacing. The hero graphic opens the case popover, with the case-record link as its
  no-script fallback. Case popovers offer separate record, Frontier-row and Atlas-tile
  actions. An Atlas case target scrolls to and highlights the requested tile.
  Every row containing one card is centered.
  The full project narrative and attribution live on About.
  The homepage keeps a concise destination action instead of repeating that material.

- **News.** News is the second navigation item and carries eligible public
  announcements. The changelog record retains excluded historical entries and their
  reasons; `CHANGELOG.md` contains the complete history.
  Its H1 uses the shared sans-serif caps.
  Factual and mathematical body paragraphs and lists use the shared prose role, which
  defaults to serif text and mathematics and follows the reader’s font preference.
  Titles, dates, topic chips, significance, artifact and publication metadata,
  references and controls use the sans face.
  Dates and publication records use the shared support gray; the main prose retains the
  normal foreground and metadata links keep the shared link affordance.
  Each eligible entry is one hairline-bordered card containing its actual article once.
  News and Learn share an article heading: an optional eyebrow, the title, the original
  publication date, then optional topic tags and significance metadata.
  The title uses the Learn card’s sans face, medium weight, size and leading; it stays
  upright, left aligned and in the theme’s text foreground.
  A linked article title inherits the heading’s color and typography.
  News headlines use surnames when unambiguous.
  Article text follows the authored record.
  Linked mentions use the shared short surname-or-handle label, following
  [Attribution Policy](../../../attribution.md#website-and-pdf-presentation).
  The renderer preserves the authored record while applying that link-label policy.
  Profile links navigate directly to their complete pages from both homepage previews
  and the News archive.
  Keep published handles and organization names intact.
  Full identities remain in canonical attribution and source-reference records.
  The date is a prominent sans-base line in medium weight, with a machine-readable
  `time` value. Paper dates come from the oldest edition in each component’s retained
  publication history.
  Tutorial dates name their first site deployments; manuscript creation and later
  revisions do not restamp them.
  News and homepage highlights retain each announcement’s frozen date.
  No current site edition or filesystem timestamp supplies a date.
  Learn uses the eyebrow for the paper’s series part or tutorial label.
  News places smaller Results-style topic chips on the left and the shared significance
  meter at the right below the date, followed by the article.
  The chips retain shared fills, corners and leading at 85% of the note-size chip scale.
  Shared article headers place 0.3rem between title and date; News uses a 0.25rem header
  gap and 0.4rem after the header.
  The prose block adds 0.25rem of padding above and below its text, with 0.5rem between
  paragraphs. Publication records start 1rem below the prose block and have their own
  sans wrapper so formulas follow the text role of their block.
  Homepage News and the archive use the same card renderer and CSS roles.
  Every post has an explicit importance score and a plain rationale.
  The meter’s accessible label names its S level; its shared tooltip gives the level’s
  short meaning in the News label rubric (`result-import.md`, “Label the PR and Prepare
  News”), as the archive’s S buttons do (`render_changelog.news_significance_meanings`).
  An S button explains itself on hover and keyboard focus, never on a mouse press.
  Its explanation opens above the filters and below the site header while the header
  shows, or below the filters when there is no room between, so it lies over neither a
  filter control nor the header’s links (`data-site-tooltip-outside`); a press dismisses
  it. The source record retains the post’s rationale.
  Its S and five bars remain one tightly paired mark.
  Homepage highlights keep the announcement’s significance and assurance qualifiers,
  with one S meter per card.
  News includes only S3, S4 and S5; S1/S2 remain in the full GitHub changelog, with old
  News bookmarks forwarded there.
  Archive controls offer S3/S4/S5 and default to S4/S5 and all topics, with OR within a
  facet and AND across facets.
  One unboxed Reset filters action restores the defaults, right aligned above the News
  item count on desktop and narrow screens.
  Significance remains an inline S3/S4/S5 segmented group using the homepage
  Grid/Triangle chooser’s shared type, sizing, borders and states; it is never a
  dropdown. Topics uses one compact multiselect disclosure.
  Its summary reads All, None, one selected topic, or the first topic and +N, using the
  selected topic’s shared chip.
  Opening exposes ordinary pressed buttons in a labelled group; choosing a topic or All
  topics leaves it open.
  Up/Down, Home and End move focus among choices; Enter or Space activates the focused
  button. Escape closes the list and restores its trigger.
  Outside activation and focus leaving the group dismiss it.
  The panel fits within the viewport gutters and scrolls internally on short screens.
  It shares the navigation surface, shadow, focus outline, motion timing and down/up
  chevron with negative 180-degree expansion, including reduced-motion support.
  `overview/filter-menu.js` owns disclosure, focus and the summary; the News controller
  retains selection and URL state.
  Group names remain accessible without separate visible headings.
  They use the cards’ sentence-case labels and corresponding topic-colored ink on the
  same neutral gray background in both themes.
  Selected options show a leading check, so selection never rests on hue alone.
  The check’s place is held while hidden, keeping the option’s position stable.
  Keyboard focus keeps the shared visible outline.
  Each topic’s muted tally counts articles at the selected significance levels,
  independently of topic selection.
  Counts use the Results control row, right aligned above the cards; an empty state
  describes a selection without matches.
  URL state preserves unrelated query parameters and browser history; a low-score
  bookmark widens the filters to reveal its target.
  Without JavaScript the controls stay hidden and complete eligible articles remain
  visible, with a link to the full changelog.
  After the enhancement loads, about ten lines are visible.
  Clicking or tapping the card or its small shared arrow in the footer expands or
  contracts it inline; Enter and Space activate the button.
  A short fade marks the clipped edge.
  News disclosure footers center their expand/contract control on the content through
  one rule; ordinary navigation actions keep their own roles.
  Height, fade and arrow rotation share the existing motion timing and honor reduced
  motion. Hover adds a subtle green wash without changing height.
  Article links retain their ordinary actions; body-link focus reveals the article.
  Eligible entry and legacy date fragments reveal their corresponding card.
  Bookmarks for excluded entries, and dates with no eligible articles, forward to the
  retained GitHub changelog.
  Topic labels reuse the square-cornered chip geometry with distinct News subject
  metadata and the common neutral background.
  Their corresponding colored ink keeps News subjects distinct from the result/status
  fill palettes. These subject labels assert no result kind or verification status.
  Results and News use the shared topic vocabulary and sentence-case labels in
  `devtools/site_topics.py`. News uses the shared vocabulary’s subset without Correction
  and Audit, including Project, Engineering and Verification.
  News filters offer the topics present in the archive, in the shared vocabulary’s
  order. Topic chips explicitly reset text transformation, small caps and letter spacing,
  so parent headings cannot change their casing.
  The chip renderer preserves each consumer’s filter attribute.
  Full result records retain the result’s real kind, status, claim and credit.
  The homepage’s News box shows the three newest News articles at the levels it opens
  on, ordered by the announcement’s frozen date and stable ID, followed by **All News**.
  It opens on S5 alone where the three newest S5 articles all fall within 30 days of the
  build’s reference day, the newest day its records say anything reached `main`, and
  otherwise on S4 and S5, decided at render time and never from the clock
  (`news_highlights.default_levels`; the owner, 22 October 2026, and #736’s review A).
  Above the cards, at the right, sits the archive’s own significance filter in its
  compact form (`render_changelog.news_filters(compact=True)`): the same buttons,
  smaller and lighter through the `--site-chooser-compact-scale` token, with no topics
  or reset, and the archive’s live count kept out of sight for screen readers.
  With no article to show, the box says “No news yet.”
  and draws no filter.
  A press shows the newest three at the chosen levels; the box carries the newest three
  of each level for that, hidden until chosen, and keeps its opening levels without
  scripts. **All News** carries a changed choice to the archive as `news-s`. Each preview
  uses the archive’s title, date, topic chips, complete article and disclosure.
  Its title links to the stable News article anchor.
  Keep claim qualifications in that shared article; result records carry the detailed
  verification, confirmation and status marks.
  The archive ends with a shared action button, “Full changelog”, using the
  external-link arrow and linking to the complete GitHub changelog.
  About keeps one short News link; its old history bookmarks forward without duplicating
  the feed.

- **Page headings.** The homepage opens with “The Square Packing Problem” as its `h1`,
  followed by visible section `h1`s in the same title style.
  The Videos page shows no title: the bar, its trail and the film are the page, and its
  `h1`, “Videos”, is for a screen reader alone (`.site-visually-hidden`, in `site.css`:
  out of the flow, one pixel, clipped, the class for any block a reader does not see and
  a screen reader should).
  The film after the hidden title is the page’s first block, so on screen it brings no
  margin above and starts `--site-page-top` under the header.
  A page that has a title (the Frontier page, the Results page, the Papers page, the
  canonical case record) sets it in the hero, centred.
  The Frontier page’s title is “Frontier Survey”, the Results page’s “Results” and the
  Explanations page’s “Explanations”; each stood over a subtitle the owner dictated on 1
  October (“A survey of everything known for cases $n = 1, \ldots, 324$”, “A survey of
  all reviewed results”, “Papers and interactive explanations for specific results”) and
  dropped on 2 October as adding little (`think-wz9d`); the page descriptions in each
  `<head>` are their own constants and stay.
  Individual case pages use their own case heading; the Atlas replaces the former
  separate case-directory hero and index (**Case records**, below).
  A subtitle, where a page has one, is the sans face at 1.1 times the sans base
  (`--site-subtitle-scale`, about 21px), in the page’s own text colour, never gray, with
  the same space above it and below it (`--site-subtitle-space`, 2rem). A title with no
  subtitle, a document’s own `h1` among them, stands that space above its first
  paragraph. The page title style (every `.site-page h1`, every hero `h1`, and
  `.site-title`) is the sans face in upright caps (not KPress’s italic `h2`) at 1.5
  times the sans base, centred.
  On screen, `h1.site-title` and `h2.site-title` use `--site-title-space-above`
  (6.25rem) above and `--site-title-space-below` (2rem) below the title on every content
  page. The first page heading has no top margin, including a heading after breadcrumbs
  in the initial article or header; the page container supplies its normal top padding.
  Print keeps its existing heading spacing.
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

- **Detail labels and values.** Across standalone case and result records, tables and
  popovers, `.site-detail dt` uses the muted support color and medium sans weight.
  `.site-detail dd` uses the primary reading color, dark in the light theme and light in
  the dark theme.

- **Names.** The page at `atlas.html` and its navigation entry are **Visual Atlas**. It
  opens with all 324 packings visible, with no local section navigation.
  **Frontier Survey**, at `frontier.html`, is a separate Results destination with the
  same title in its menu, heading, and breadcrumb.
  Its complete 324-row bounds table follows a concise key to the reported/verified
  distinction, verification requirements, gap, decimals, and table controls.
  Audits and case histories belong in the case records.
  A **Frontier Row** action reaches `#n-N` in the survey table; an **Atlas Tile** action
  reaches `#atlas-n-N` in the graphical grid.
  The homepage preview, posters and film also draw from the Atlas.
  Legacy Atlas survey fragments (`#the-frontier-survey`, `#the-survey`,
  `#best-known-results`, `#frontier-table`, and `#n-N`) reach the corresponding Frontier
  Survey fragment with query state preserved.
  The homepage’s former survey fragments reach the same page.
  `status.html` retains its Atlas forwarding destination.

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
  A card section is one wrapping row inside the prose track, in a `.site-cards-frame`
  the row measures itself against.
  Its outer edges align with the shared 35em prose column, including on profile pages
  and in groups whose markup retains `site-wide`. Data tables, packing figures, the
  atlas and video stages keep their explicit wider tracks.
  A prose note does not become wider by sharing a visual block’s wrapper.
  The column count is capped to the number of actual cards, so one- and two-card groups
  fill the track without empty columns.
  A final partial row in a longer group remains centered.
  Explicit multirow sections follow this same rule.
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
  and nothing framed (`think-bc5d`, `think-w82r`). Record links and rows can preview
  complete case, result and contributor pages through the article overlays above.
  A card’s authored preview or framed repository document keeps its own native card
  behavior. A direct card is a link and holds no other link, so what its note names is
  linked from the prose beside it.
  **Every other direct card opens its target in a new tab** (`target="_blank"`,
  `rel="noopener noreferrer"`), so the page the reader chose it from stays where they
  left it: a poster’s PDF, the Visualize page, another project.
  `link_card` refuses `new_tab=False` for anything but a page the site serves, which one
  rule decides (`overview_sections.is_site_page`): an entry of
  `render_overview.SITE_PAGES`, the optimality paper among them, or a directory served
  by its `index.html`, as `workbench/` and `profiles/` are.
  A case record and a person profile are complete pages too; case links use the article
  controllers described above.
  - When a popover card leads to a repository document the site renders, the popover
    renders that page itself, narrow, in a frame: the page at the same address with
    `?view=embed` added before any fragment, so a filtered view such as
    `frontier.html?recent=true` or a case such as `frontier.html#n-11` arrives as it
    will be seen. The embed view drops the navigation bar and sends every link out of the
    frame to the full window.
    The button is **Expand**, which opens the page at full size; a repository document
    also offers its source “On GitHub”, which opens it on `main`. Every repository link
    on the site names `main`, never a commit, and is made by `devtools/repo_links.py`;
    the optimality paper’s citations are the one exception (**Papers page**, below).
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
    the results table**, goes to `results.html#t-nnn`. A row on the overview itself
    would scroll, with the down arrow.

  The frame loads only when its popover first opens, so the overview stays light.
  The popover is a native `popover` panel with square corners over a faint scrim, set in
  sans, closed by its `×`, by Escape, or by a click outside, and it works without
  scripting. A card, popover or direct, gains a gentle wash on hover.
  Every popover has the same margin on all four sides, `--site-popover-pad` (1.75rem;
  1.1rem on a phone). Prose panels use `--site-popover-text-width`, the normal
  `--kpress-measure` plus their two padding insets, capped inside 1rem viewport gutters.
  This rule applies to result panels; case visualizations keep their wider stage and
  responsive gutters. Its header groups the Lucide maximize-2 and close icons at the
  upper right, each in a 2.75rem square tap target (`--site-popover-close`), set 0.6rem
  in from the corner (0.25rem on a phone) and washed on hover or keyboard focus.
  The expand glyph has diagonal outward arrows.
  KPress’s retained sprite has no maximize-2 symbol, so both inline and sprite-backed
  controls inline the same paths.
  The maximize link sits immediately left of Close, uses the bottom full-page action’s
  destination and accessible label, and leaves that bottom action in place.
  A panel with no full page, including a detail whose action only scrolls within its
  host page, has Close alone.
  Case stepping updates both full-page links together; opening either article still puts
  keyboard focus on Close.
  The controls use the same 1.25rem Lucide icon size, and the case controls stay in
  reach while its panel scrolls.
  Only the first text block reserves their combined width.
  The article keeps its full measure and the margins stay even elsewhere.
  A popover’s height has one limit, the window’s: `--site-popover-max-block`, the
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

- **Collection actions.** A link to a complete collection uses **All …**, such as All
  Results, All Profiles, All Resources, All News, All Papers, All Tutorials, or All
  Posters, followed by the existing decorative right-arrow component.
  These read **View All …** until the owner dropped the leading “View” on 2026-10-23,
  which also made **View Visual Atlas** and **View Videos** plain **Visual Atlas** and
  **Videos**. The link remains an anchor with its real destination, styled by
  `.site-action` inside `.site-action-row`: the shared accent fill, note-sized sans
  label on the button-label scale, 0.45rem by 0.9rem padding, 0.5rem icon gap, and the
  shared hover and focus state.

- **Card sizes.** A card is sized by its text, in three sizes it names in
  `data-card-size`; a card that names none is medium.
  Each size is as wide as a column of the grid of its own minimum column the frame fits,
  with 1rem gaps, so cards of one size line up as a grid at every width:
  - `small`, 12rem minimum columns, for a headline and one line, under 80 characters.
  - `medium`, 16rem minimum columns, for a headline and a sentence, 80 to 159
    characters.
  - `large`, 18rem minimum columns, for a paragraph or a list, 160 characters or more.

  At the 630px desktop prose width, three small cards or two medium or large cards fit
  on one row. A group of two small cards also uses two full-width columns rather than
  reserving an empty third slot.
  Two large cards fit from 37rem; this shared threshold applies to every catalogue,
  including Tutorials.
  On a phone every card takes the whole line.
  The count to a line is `--site-cards-small`, `-medium` or `-large`, each stepped by
  its own container queries: n columns of minimum m and n − 1 gaps need (m + 1)n − 1
  rem, so medium steps at 33, 50 and 67rem, small at 25, 38 and 51rem, and large at 37,
  56 and 75rem. No size sets more than four cards to a line (the owner, 2026-10-05), so
  medium stops at four, small at four and large at four.
  A section declares one size for all its cards, in `SECTION_CARD_SIZES`
  (`overview_sections.py`), so its lines are one grid; the size is the one its typical
  card’s text asks for, the median card’s, which for an even count is the mean of the
  two middle lengths, and `tests/test_overview.py` holds the two together.
  Learn’s Tutorial section is the one explicit exception: its two brief introductory
  cards use the papers’ large reading-card layout to give readers a prominent starting
  point. Tutorial and Papers remain separate sections when checking typical text lengths.
  The page cards, the atlas cards and the other projects are medium; the documents,
  whose notes are a line, are small.
  A section can also be set in lines of its own, in `SECTION_CARD_LINES`, where one
  wrapping row would not set its cards as they are meant to read: the six page cards
  stand one, three and two, the Frontier page alone at the top, then the three parts of
  the $n = 11$ series in reading order, then the tutorial and the workbench.
  Each line is a grid of its own in the section’s one frame, a gap below the line
  before, and none sets more cards to a line than the longest line holds
  (`data-cards-most`, at which the stylesheet caps its size’s count).
  Actual card count remains a further cap, so a short row fills the prose width without
  an empty slot. Wherever the frame fits two medium cards, from 33rem, every line stands
  as set; on a phone every card takes the line.
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
  The foot is set in the sans face at the note size in normal foreground, at the card’s
  lower edge, so the feet of a row line up; its links take the page’s link colour.
  A card with no foot stays the link itself, unless it has an independent byline.
  With `link_card(byline=)`, `.site-card-main` is a content container: the linked
  heading, the byline, a separate source-address link, then the description.
  The byline retains native profile links and never sits inside the source link.
  The cards’ widths, rows and centring are the same with a foot as without
  (`measure_site_pages cards`, at 1280, 1024, 768 and 390).

- **Other projects.** Homepage and profile Resources cards rank catalogues, repositories
  and other cited websites together.
  The catalogue inventory includes David Ellsworth’s Squares in Squares (the record’s
  `[Kingbird]`), Erich Friedman’s archived page and Evan Daniel’s Square Packing Atlas;
  none receives a fixed position ahead of the significance order.
  Cards sort by their primary-authored result counts at S5, then S4, down through S1,
  descending at every level, so one result at S5 stands before any number below it.
  Ties sort by newest result first, then displayed resource name and exact URL.
  Resources with no registered primary result follow those with results, by name and
  URL. The same rule sorts each profile’s subset, including evidenced personal websites
  with no registered result.
  The order is computed from `results.yaml` when rendered (`ranked_projects`,
  `resource_cards` and the shared `project_order`); inventory insertion order is not a
  presentation rule. A project’s source keys define its scope (`project_source_keys`,
  with `PROJECT_EXTRA_KEYS` and `SOURCE_VENUES` for shared packets and catalogue
  venues). Reviewed person roles determine primary Results and received Credits for
  resolved bylines, including prerequisite exclusions in shared source packets.
  A resource without resolved byline IDs retains results explicitly attributed to its
  source keys when a bibliography author span is reviewed as non-person or unresolved.
  This establishes project authorship while leaving personal identities and credit
  counts unresolved. Acknowledgments and later citations do not establish authorship.
  A card’s repository or website title opens that source.
  Below the repository heading, its byline begins with “By” and the author: a known
  person links to their profile using their full public name, while an organization or
  an unreviewed identity stays plain text.
  Exact curated author names and evidenced aliases identify people; repository owner
  strings alone do not establish personal identity.
  Multiple authors keep separate profile links.
  The repository icon and address appear directly beneath the byline, before the
  description. The same order applies to resource cards on profile pages.
  These links sit beside the project link in the card’s structure, never inside it, and
  remain in the same tab.
  Cards share the result-and-credit tally component with profiles.
  Mixed significance levels read “6 results (3 at S4, 3 at S3), 12 credits (2 at S4, 10
  at S3)”; a single occupied level reads “1 result (at S5), 2 credits (at S4)”. The
  level breakdown runs highest first and omits empty levels.
  Results are distinct registered IDs with reviewed primary authorship.
  Credits count distinct person/result pairs received for the project’s explicitly
  linked work, excluding acknowledgments given by the project and its authors’ unrelated
  work. The Results total links to the table filtered to the project’s primary results
  and each significance count to the same table at that level (**Result filters**,
  **Preset-only controls**, below).

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
  a result’s `confirmed` green, `reviewed` blue, `recorded` yellow and `incomplete`
  light red (`data-status`). Bound-kind chips use lighter versions of the shared bound
  hues: lower bounds red and upper bounds green.
  Optimality uses violet, Project amber, and Engineering orange; News and Results use
  the same topic palette.
  Superseded chips remain gray.
  These fills adapt to the page theme and apply in tables, records and popovers.
  No chip wraps: one rule on the component, `white-space: nowrap`, keeps a chip’s words
  on one line wherever it sits, and no other rule lets one break.
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
  `simplification` or `formalization`, and a result that bounds nothing by its kind too.
  Each of these chips adds no style of its own, so every one is the same plain gray
  chip, one font size, line height and height, and they differ only in their words.
  The Rungs column is as wide as its widest chip, so in a table each chip of the status
  line takes a line. A row keeps its kind and status as `data-kind` and `data-status` for
  the filters; a step of a result’s chain keeps its standing on that case as
  `data-standing`. A novelty chip (`data-novelty`) is always plain gray.

- **Control labels.** Shared `--paper-button-label-scale` is 0.9: actions use 90% of
  their contextual note-size sans label, navigation tabs and Atlas toggles use 90% of
  their contextual navigation-size sans label, and Workbench buttons use 90% of their
  contextual body label.
  Keep the original line boxes, padding and click areas.

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
  Every in-place expand/collapse action uses this pair, such as the recent table’s
  **Earlier results** (**Action under a table or grid**, below).
  - Inline markup carries `<span class="site-icon-arrow" data-arrow="right">`, written
    only by `overview_sections.arrow_icon(direction)`: a case record’s steps to its
    neighbours (left before the case’s count, right after it), which the left and right
    arrow keys follow in the case popover, the overview’s “All Results” button (right)
    and the recent table’s **Earlier results** (double-down, then double-up).
    The atlas popover’s stepper, two buttons left and right, went with that popover on
    2026-10-03, and the atlas’s expander on 2026-10-22.
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
    change eases in and out: the cards, the bar’s links, the theme menu, a popover’s
    close cross and action, a table’s rows (their wash on hover, on keyboard focus and
    while their popover is open, which snapped until then), the ladders’ names, the
    atlas tiles, the record index and the contents rail, and on a paper’s page its
    links, buttons and readouts (`paper-publication.css`). The token names those four
    properties and never `all`, so a late stylesheet snaps into place rather than
    animating its layout, and it is used alone, never listed beside another property, so
    it still reads under reduced motion.
  - **Navigation disclosure.** Results, Learn and About use the same 140ms ease-out
    timing for their dropdown’s opacity and quarter-rem vertical travel and their
    chevron’s negative half-turn.
    The mobile Menu list uses that timing too.
    A discrete display transition lets the exit finish; closed lists are inert
    immediately, with focus restored to their trigger when needed.
    The head bootstrap still reserves collapsed geometry before paint.
    Reduced motion sets these transitions to zero, including over KPress’s
    classed-element fallback.
  - What else a hover moves, an arrow’s nudge or a card icon’s fade, transitions that
    one property (`translate`, `opacity`) on the same timing, never with a literal
    duration.
  - A focus ring (`outline`) is not eased: it shows the moment focus arrives.
  - `tests/test_site_hover_motion.py` holds it: the token declared once, every
    `transition` in `site.css`, `site-nav.css`, `site-result.css`, `paper-type.css` and
    `paper-publication.css` the token or named properties on its timing, including the
    navigation’s discrete display transition, and every rule whose hover or focus
    changes a colour, a border or a shadow styling an element that carries the token at
    rest, by its own selector, a broader rule’s, or a shared rule the test names with
    its reason; in Chromium, a row, the bar’s links and the close cross ease the four
    properties over 140ms.
  - The workbench’s own controls keep its own motion tokens (`--duration-fast`,
    `--easing-standard`, in `packages/workbench/assets/workbench.css`), under its own
    design contract; only the bar it shares with the site runs on this one.
  - Under `prefers-reduced-motion: reduce` the duration is 0ms and the token `none`, so
    colours and disclosure state change at once, with no animated arrow travel.

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
    A cell at least 20.5rem wide places its mark in a rail beside the description:
    2.25rem for V/C chips or 6.25rem for the significance meter, then a 0.75rem gap and
    at least 13.5rem for the two-line meaning.
    All cells turn together, preserving uniform row heights; narrower cells put their
    meanings below the mark.
    The rail uses `minmax(rail, max-content)` so a reader’s enlarged meter remains clear
    of its description. The three-column boundary is 1100px; on the stacked diagram the
    side-by-side boundary is 360px. Retained browser checks cover both sides of each
    boundary and a 20% enlarged-meter control.
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
  The grid fills the available page width less its edge gutters, and its cells keep a
  readable size (at least 6.4rem, 4.6rem on a phone, at the Medium size; **Atlas
  sizes**, below), so a wider screen shows more cases per row: 4 at 390 pixels, 10 at
  1280 and 16 at 1920. A cell washes on hover and on keyboard focus, and is a link to
  its case’s record file, `cases/11.html`, which opens in the page’s one case popover
  (**Case records**, below).
  The wash is the cell’s background, behind the drawing, and it is the only thing that
  changes: every line of the artwork keeps its fixed ink at rest, hovered, focused and
  pressed, in both themes.
  `tests/test_site_drawing_hover.py` checks the loaded SVG, its geometry and exact
  painted colours, and contrast against its own canvas.
  All 324 cells arrive as visible static markup with reserved image dimensions, on the
  dedicated Atlas and the homepage alike; the homepage’s preview showed only its first
  hundred until 2026-10-22. Images use native lazy loading, and `overview/atlas-grid.js`
  prepares them row by row after first paint.
  Each drawing has a 1000-unit frame, fine enough to show large.
  Triangle is the atlas’s default view, following the scroll from Large when reached
  from the top of the page (**Atlas follows the scroll**, below); Grid remains available
  under the view tabs (**Atlas views**, below).

- **Atlas views.** The atlas is one set of tiles under two views, **Grid** and
  **Triangle**, chosen by a strip over the tiles (`atlas_view_tabs`): the section tabs’
  strip (**Section tabs**, above) as a `tablist` of two buttons in that order, Triangle
  selected by default and the one tab in the page’s tab order, with the arrow keys, Home
  and End moving between the two and selecting the tab the focus lands on
  (`overview/atlas-view.js`). The page is rendered in Triangle; its static tile
  positions and container arithmetic lay it out before the atlas scripts run.
  The strip is present in the first response, and scripting handles its controls.
  Without scripting, ordinary links reach all case records and the complete frontier.
  The triangle sets the cases by the grid bound: row $k$ holds the $2k - 1$ cases
  $n = (k - 1)^2 + 1$ to $k^2$, the cases covered by the same side-$k$ grid bound,
  ending at $k^2$. The perfect squares $1, 4, 9, 16, \ldots$ are the cases whose best
  packing is the $k \times k$ grid itself, and their tiles are numbered in the text’s
  colour at the medium weight.
  Eighteen rows show all 324 cases, the last 35 tiles wide.
  A one-line key under the triangle said what the rows are until 2026-10-02, when the
  owner dropped it as obvious (`think-l38m`), with the line under the expander that said
  every case is in the frontier survey and has a case record: each tile opens its case
  record, and the Frontier page is a page card.
  The address names Grid as `?atlas=grid`; Triangle has no parameter and is selected
  when the parameter is absent or invalid.
  Existing `?atlas=triangle` links also open Triangle.
  A change of view writes the address with `history.replaceState`, preserving every
  other parameter and the fragment.
  The head bootstrap selects the view before the body is painted, and its Grid selection
  overrides the static Triangle markup.
  **Complete rows at a readable scale.** Both views use the same scaled cell minimum,
  `--site-atlas-cell-min` (6.4rem, 4.6rem under 40rem), and the same horizontal gaps,
  `--site-atlas-cell-gap` (0.5rem, 0.35rem under 40rem). Grid’s viewport capacity sets
  the drawing width in both views, even when it exceeds the longest bound row.
  Triangle keeps every bound row complete, with its non-grid and grid segments side by
  side and an extra separator of half the displayed drawing’s width.
  Every perfect-square endpoint aligns to the canvas’s right edge.
  Narrow screens pan the canvas inside the atlas without shrinking or breaking rows; the
  initial scroll position shows the right edge before scripts run.
  Each row reserves its drawing and count-caption height, without prose-image margins,
  and the shared cell gap, 0.5rem on desktop and 0.35rem on a phone.
  There is no blank logical-row padding.
  Rows 1 and 2 have no non-grid prefix and need no horizontal separator.
  The first retained axis-aligned grid packing in each row begins its grid segment
  without an additional caption.
  Its threshold comes from the manifest’s canonical `source.kind = exact-grid` entries
  through `sqpack.known_best.grid_transitions`, which checks that each row has an
  unbroken grid suffix and exposes both half-open segments.
  This is separate from the derived drawing layer: row 8 starts at $n = 56$, and row 15
  at $n = 212$. The web legend describes only tilt colors and contact shades.
  `place(n, per, starts)` computes each tile’s complete row and local segment column,
  tested against an independent layout in Node (`tests/node/overview_atlas_view`). The
  script writes custom properties; the stylesheet places the tiles within the two
  segment containers, whose static metadata matches placement before atlas scripts run.
  Resize repeats the placement.
  Grid flattens the segment containers into its ordinary layout.
  A tile shares the block’s width after reserving the gaps, and uses Grid’s drawing
  inset, so switching layouts preserves the drawing size.
  At Medium, Grid holds ten tiles at 1280 pixels and four on a 390-pixel phone.
  Triangle keeps that drawing width across all eighteen complete rows.
  The controls and legend are centered above the scroll frame.
  **The move.** A change of view moves every tile from where it was to where it is: one
  read of every tile’s box and of each element after the tiles, the change of layout,
  one read more, then one Web Animation a tile on `transform` alone, a translation and a
  scale about the tile’s corner, all started in one batch for
  `--site-atlas-move-duration` (360ms) with `--site-atlas-move-easing` (an ease-out).
  A tile outside the window before and after is not animated; a tile that had no box
  before the change fades in.
  The tile viewport grows or shrinks over the same 360ms, moving following content
  through normal page flow.
  Changes without a height reveal move following content with FLIP. Under
  `prefers-reduced-motion: reduce` the duration is 0ms and the view switches at once.
  A second press mid-move reads the tiles where they have got to, cancels the first move
  and starts from there, with the focus kept on the tab pressed.
  The final layout is the stylesheet’s, correct with no animation at all, and nothing in
  the block transitions its place (`transition: none` on the tile track, row and segment
  wrappers, drawings, and numbers): KPress’s reduced-motion rule gives every classed
  element a 0.01ms transition of every property, under which the triangle was laid out
  for one frame with the grid’s gaps, 1344 pixels wide at 1280, before it settled.
  `devtools.measure_atlas_views` measures the layouts (`layout`), times the moves
  (`move`) and pictures both (`shots`); `tests/test_site_atlas_views.py` holds the page
  to all of it in Chromium.

- **Atlas sizes.** Beside the view tabs, in one row over the tiles that wraps under them
  on a phone, a second strip of the same tabs chooses the size of the tiles
  (`atlas_size_tabs`, think-ht8t): **S**, **M**, **L** and **XL**, each named in full by
  its title, Small selected on narrower screens and Medium from 75rem upward, with the
  keys of the view tabs.
  XL joined on 2026-10-23 for a triangle that follows the scroll, which opens at it
  (**Atlas follows the scroll**, below).
  CSS and the synchronous bootstrap agree before the first paint, avoiding a size jump.
  An explicit URL or chooser selection overrides this automatic default (`think-mp47`).
  The size is one token, `--site-atlas-scale` on the block (1, Small 0.667, Large 1.5,
  XL 2.25), set by its `data-atlas-size`, and applies in either view.
  It scales the shared cell minimum, `--site-atlas-cell-min`, so both views fit more
  tiles at Small and fewer at Large (`perLineAt`, tested in Node).
  At 1280 pixels a line holds 15 tiles at Small, 10 at Medium and 7 at Large, and on a
  390-pixel phone 6, 4 and 3. Triangle preserves that drawing width on complete,
  right-aligned rows, with horizontal panning when needed.
  A change of size is a change of layout and moves every tile as a change of view does
  (**Atlas views**, above).
  Explicit size choices persist as `?size=small`, `?size=medium` or `?size=large`,
  written and read before any tile is placed.
  Automatic resizing applies only while the size remains unchosen.
  `tests/test_site_atlas_views.py` reads each size in Chromium, and
  `devtools.measure_atlas_views` measures every layout at every size (`layout`), times
  the changes of size in each view (`move`) and pictures them (`shots`).

- **Atlas follows the scroll.** A Triangle reached from the top of either Atlas page,
  with no size, Grid, fragment or embedding in the address, follows the page’s scroll
  (think-apqd, the owner, 2026-10-22). The head bootstrap marks the root
  `data-site-atlas-follow`, so the first paint is already XL, and `atlas-view.js` keeps
  it there until the reader scrolls.
  The browser paints the page before its programs run, and the triangle would stand at
  its right end and then jump left to its framing, so it is kept out of sight until
  `atlas-view.js` frames it and then fades in where it stands, a quarter of a second; if
  the program never runs, the stylesheet shows it after two seconds.
  - The triangle is laid out once, at XL, on a stage the height of the window that the
    browser pins (`position: sticky`) while an empty runway after it scrolls past.
    Each row takes one transform, its pan, its place and its zoom, so no frame lays out
    or redraws a tile and the page’s own scroll is never touched.
    Two earlier designs were measured and dropped: laying the tiles out again each frame
    cost about 60 milliseconds, since every tile carries some 300 inherited custom
    properties and every drawing is redrawn, and scrolling the page back under the
    reader’s row fought the browser’s own scrolling, so the triangle shook.
    On a narrow page kpress clips the document with `overflow-x: hidden`, which would
    pin the stage to the document; while following, the site clips it instead.
  - The point at the focus line, halfway down the window, passes it at the page’s own
    speed. The first rows stand centred; over the first three rows the middle of the
    window eases to a third of the way along the reader’s row
    (`--site-atlas-follow-across`), where each row’s grid first breaks, so the triangle
    slides right, keeping that row’s left end in view.
    Rows are read between rows on a monotone spline, and the pan meets each limit on a
    bend a quarter of the stage wide.
    From the page’s top the pan sets off from rest (the owner, 2026-10-23): it once ran
    at most of its speed from the first pixel of scroll, since the rows at the focus
    line were already widening.
    The framing follows a point that starts where the pan would first move and comes up
    to the point at the focus line over 0.6 of the stage’s height or width, whichever is
    less, with no speed or acceleration at the start and no lag at the end (`launch`),
    running up to two fifths faster than the path to make up the slow start.
    The reader’s own row still keeps its left end in view throughout.
  - The zoom is a straight line in the scroll with rounded ends: the tiles shrink by one
    width a pixel, from where the reader’s row first needs it, over at least one and a
    half windows, from XL down to Small, or to where the case numbers, drawn at
    `--site-atlas-follow-number`, would pass `--site-atlas-follow-number-least`. It
    finishes by the time the triangle’s bottom reaches the stage’s, and neither starts
    nor stops with a jolt.
    A zoom timed by the point at the focus line instead shrank the tiles fastest at its
    end, since that point runs faster as the tiles shrink.
  - Going down, the top of the triangle slides off to the right, the triangle zooms out,
    and the pan slides along the left side; at the bottom the rows slow to a stop while
    it slides on to the left edge.
  - All of it is a function of the scroll, so going back up retraces it to XL at the
    top. A sideways wheel or swipe pans the triangle while the page scrolls, so a
    diagonal gesture moves both ways.
    That pan holds while the reader pauses and eases back onto the path as they scroll
    on, by a factor of e a window, and eases away back at the top.
    The last of the motion slides to the triangle’s left edge, and the reader’s pan
    holds on top of it there too, so the triangle at rest at the bottom still pans by
    hand, from its left edge to its right end.
    Until 2026-10-23 the slide overrode the pan, and on a phone a finger could no longer
    move the triangle at the end (the owner).
    A swipe down wobbles a little sideways, most as it starts, and the pan once counted
    the wobble, so the triangle sometimes went left and then right (the owner,
    2026-10-23). Sideways travel now pans only past 16 pixels and a quarter of the
    vertical travel, both counted over the last 150 milliseconds or so, then one for one
    until the gesture is mostly vertical again.
  - The size tabs show the size nearest the zoom, and nothing is written to the address.
    A size or view tab, or a jump to a tile’s fragment, ends the following for the page
    view; a pressed size returns the tiles to that size’s own layout with the usual
    move. `tests/test_site_atlas_follow.py` reads all of it a frame at a time in
    Chromium, and `tests/node/overview_atlas_view` holds its arithmetic.
  - When the following ends, by a tab, a fragment or the keyboard, the block takes the
    size the tabs show, so Grid or the static triangle opens at the size the reader was
    looking at, and the row at the middle of the stage keeps its place.
  - A reader who asks for reduced motion is never followed: the bootstrap does not mark
    the root, and the script ends the following if the setting changes.
  - Keyboard focus moving onto a tile the stage does not show ends the following and
    brings the tile into view; a pressed tile still opens its case and keeps it.
  - A new width, a turned phone or the browser’s zoom lays the triangle out again in one
    frame, after the tiles take their new size; a change of height under a fifth of the
    stage, a phone’s toolbar coming and going, leaves it where it stands.
  - The rows are wrapped in one picture, one compositor layer, which takes the one
    transform; the stylesheet stops a sideways swipe over it from going back in history,
    and prints the stage as the reader sees it, without its runway.
  - These came from the senior engineering review of 23 October (PR 746, review A).

- **Atlas scale.** A third strip chooses **Fixed**, **Row** or **Global** on the website
  only. Row is selected by default.
  Fixed retains equal displayed enclosing-container sizes.
  Row scales each drawing by its selected witness’s enclosing side divided by the
  logical row’s grid side, $k = \lceil\sqrt{n}\rceil$; grid reference containers retain
  the same displayed size across rows.
  Where the actual container is smaller, Row shows a thin gray outline of the grid-sized
  reference container.
  The outline reuses the packing renderer’s SVG frame and centered stroke, matching its
  line width and bottom-left edges at each Row scale.
  It sits inside the image margin, appears in both layouts, and disappears in Fixed and
  Global. Global scales each drawing against the largest enclosing side among the cases
  shown, every case on either page; the box of tiles names that side before scripts run.
  Row uses those logical groups in either view, independent of responsive wrapping.
  Size still controls tile slots; scale changes only drawing size, preserving count
  positions, complete rows and the regular-grid separator.
  The drawing side comes from the canonical selected witness, including the regularized
  view where it is the published drawing, rather than from a lower bound or an area
  estimate. The address uses `?scale=fixed` or `?scale=global`; Row omits the parameter.
  Control changes preserve size, view, unrelated parameters and the fragment.
  Invalid values select Row.
  Static ratios and the head bootstrap reserve the selected drawing scale before scripts
  mount. The controls share the tabs’ keyboard behavior and give an accessible
  explanation of each choice.
  PDF drawing scales stay fixed.

- **Atlas marks.** Homepage and dedicated Atlas tiles carry only the centered case
  count. Triangle’s grid segment starts with the ordinary count and its accessible name
  says “first grid packing in row”.
  Dimension and `GRID` captions belong to the print diagrams.
  Counts use one size, including at the start of a grid segment.
  Drawing sizes follow the same selected scale in both views.
  Lower-bound statements show five decimal places, and their number-line labels two,
  truncated downward without changing recorded values or the number line’s positions.
  The centered key under the tabs contains only tilt-angle colors and full-side contact
  shades, one entry in each left-aligned column.
  The first two tilt swatches label their pinned angles as `90°` and `45°`. The complete
  eight-item legend, including status counts, recency and algebraic degree, remains in
  the printable diagrams.
  The key uses the support colour at the note size (`atlas_legend`) and describes no
  layout mechanics. The web swatch is a square at the legend text’s 1em size.
  Angle numerals use 0.65em and medium sans weight, centered inside the square; swatch
  groups and explanations share a baseline.
  On containers at most 52rem wide, the two legend items stack so wrapped explanations
  remain inside the viewport.
  After web review, printable swatches use the adjacent text’s size (19 or 48 pixels),
  with bold angle labels at 0.6 of that size (11.4 or 28.8 pixels) to preserve the print
  font’s inset. Packing drawings and explanatory text keep their geometry.
  The printed posters put “recent result (since August, 2026)” after the degree key,
  with only “recent result” in red, the suffix in black, and no count.
  Both 100- and 324-case SVG, PNG and PDF exports share that legend (`think-rxkc`). A
  case whose default picture is its retained derived view in
  `atlas/known-best/regularized/` (X-049; the regularization policy’s section 12, as
  `atlas/known-best/default-drawings.json` records it) uses that drawing directly,
  without a website layer badge, label or legend link.
  The index and atlas documentation keep the provenance.
  `devtools.render_regularized_atlas` draws the views and its `--check` verifies them
  against the index. Each tile opens the same case record, which draws the same picture
  first and keeps the house rendering one click away, under *As published*, with its
  source’s credit. `devtools.measure_atlas_views` checks count centering, actual outline
  and count-ink clearances, first-grid horizontal separation, uniform row pitch,
  complete rows and their right endpoints; `tests/test_site_atlas_views.py` checks the
  selected counts against the canonical manifest and verifies the initial CSS layout and
  actual scroll-frame extent too.

- **Action under a table or grid.** Where one control follows a table or a grid, it is
  the site’s one action button, `.site-action`, in a centred `.site-action-row`: the
  look of a popover’s action (**Popovers**, the accent fill with the page’s background
  for the text, the medium sans at the note size, `0.45rem 0.9rem` of padding and square
  corners, darkened a step on hover and keyboard focus), with its icon from the one set
  after the label at the label’s size, the arrow right where the control is a link that
  navigates, the external arrow for an off-site destination, and the double chevron
  where it is a button that shows more or less in place.
  Navigation components always use the sans face, including links styled as action
  buttons. Their shared rules set the font explicitly so a prose container cannot supply
  a serif face. Inline citations within prose retain the surrounding text’s face.
  Both forms share one rule in `site.css`, and the row sets `--site-action-space`
  (1.2rem) above itself and a table’s own space, `--site-table-space` (2rem), below, so
  text that follows a button stands as clear of it as of a table; where a heading
  follows, its larger space takes over (the owner, 2026-10-02, `think-0o9u`; nothing
  below until then). The rule is scoped to the page, `.kpress .site-action-row`, since
  the row is a paragraph and KPress’s `.kpress-prose p` margin outranked it, which had
  set both of its margins to 0.75rem. Homepage actions are **Download PDF** and **Visual
  Atlas** beside each other under the preview, then **All Results** under Recent Major
  Results. The atlas’s **Show More** stood before **Download PDF**, and **Show Less**
  under the dedicated Atlas, until 2026-10-22. All use uppercase labels through
  `paper-type.css`. The Frontier, Results and Papers pages end their tables with no
  action, so none carries one.
  `tests/test_site_atlas_views.py` reads **All Results** and **Visual Atlas** in
  Chromium at 1280 and 390 pixels and holds their colours, type, height and padding to
  each other. `tests/test_site_headroom.py` allows 0.25px of visible capital-ink centring
  error across font rasterizers, holds arrow geometry within 0.1px and preserves the hit
  area. Controlled label shifts of one pixel in either direction must exceed the ink
  limit at both widths.

- **Homepage Atlas preview.** Reuse the dedicated Atlas’s per-case SVG drawings,
  overview, view/size/scale controls, color legend, complete row and segment placement,
  with responsive Small/Medium sizing and Row drawing scale by default.
  Preserve drawing geometry and colors with case-number labels (`think-hyd6`,
  `think-ngcg`). Show all 324 cases, as the dedicated page does, in Triangle by default;
  Grid sets them in rectangular rows for the chosen size and width.
  Both pages use the same tile markup, `SiteAtlasView` layout and animation.
  Center the complete canvas when it fits; when it is wider than the viewport, preserve
  the complete rows and horizontal panning to either endpoint.
  All 324 case links and image references ship in the page.
  Prepare the SVG drawings row by row during startup, with reserved tile and image
  dimensions, so a change of view or size needs no click-time preparation.
  Immutable image loading is distinct from layout readiness; cached or prepared drawings
  do not imply that every browser performs zero later requests.
  Persistent case links retain case popovers and ordinary page destinations.
  The homepage instance keeps its state local; dedicated Atlas controls and URL state
  retain their existing behavior.
  Without scripting, both pages show all 324 cases, and the homepage keeps its **View
  Visual Atlas** link.
  Until 2026-10-22 the homepage opened on its first 100 cases with a **Show More**
  button (**Atlas expander**, below).

- **About and Learn.** About separates the project narrative into paragraphs for its
  origins, subsequent work, independent results, and current role.
  The narrative closes with the owner’s group-chat invitation, linked as **ojoshe on X**
  to his X account; link text naming only the handle would become his profile link.
  The invitation left About when the reporting invitation moved to `report.html` on
  2026-10-22 and was restored at the owner’s request on 2026-10-23; `report.html` keeps
  it too. **Report a Result** is an H1 over the reporting invitation, which asks for the
  name to credit and ends in a **Report a Result** button opening the repository’s
  result form; the old `#contribute-your-results` anchor stays on the heading.
  The overview carries a short reporting summary after Profiles, with a **Report a
  Result** link to the full invitation on `report.html`. The homepage’s **About the
  Squares Project** section links to `about.html`; Project Documentation has its own
  `documentation.html` destination.
  Between the narrative and reporting invitation, **Profiles** briefly introduces the
  contributors and cited authors tracked here.
  Home carries the same invitation.
  The centered **All Profiles** action uses the shared button and right arrow and
  navigates to `profiles/index.html`, whose full-name table links directly to profiles.
  The directory opens with the owner’s three-paragraph introduction, kept as written,
  before its summary line and table (the owner, 2026-10-23). Neither invitation lists
  names. The directory and individual profiles keep **About** active in the shared
  navigation; their breadcrumbs return to About, with **Profiles** as the additional
  parent on each person’s page.
  Learn holds Tutorial, Papers, PDFs, Visuals, and Resources sections.
  About no longer carries Reading and Research; omit redundant Frontier Survey and
  Workbench cards from both pages (`think-h21i`).

- **Atlas expander.** Retired on 2026-10-22 (the owner): both surfaces now show all 324
  cases, with scripts or without, and the tiles end the block.
  Until then one button, centred under the tiles, read **Show More** with the double
  chevron down and **Show Less** with it up; the homepage opened on its first hundred
  cases (`ATLAS_FIRST`, finishing whole Grid rows or Triangle’s first ten rows,
  `think-b2o9`), the dedicated Atlas opened on all 324 and could collapse to them, and
  the cases past the cutoff waited in a hidden box.
  With the button went the hidden box, the cutoff, the stylesheet’s switch from the
  hundred cases’ 19-tile triangle to all 324 cases’ 35, the homepage’s status line for a
  missing script, and the no-script style that revealed the rest.
  The triangle’s static canvas is now the widest row’s 35 tiles, and the box of tiles
  names its last row’s extra gap and Global’s reference side itself.
  The case popover steps through all 324 cases from any cell, since a step loads the
  neighbouring record in place and closing returns focus to the cell pressed.
  A diagram fragment, `#atlas-n-N`, finishes any move, focuses its tile and centres it
  in the window. Fitting canvases are centered; complete rows pan horizontally when they
  exceed the viewport.
  Shared FLIP animates the actual centered positions, with instant geometry under
  reduced motion.

- **Wide bleed.** A wide block (`.site-wide`) takes the wide track, `--site-wide`, less
  the page gutters (`--site-wide-gutter` on either side; **Spacing**, above).
  The track is forty times the shared type base plus 24rem, 1104px at the 18px base.
  It is independent of the prose measure, thirty-five times the shared base, so changes
  to reading lines preserve the room tables and card grids need.
  Two kinds bleed past it.
  The atlas grid fills the available page width less its edge gutters, with no fixed
  maximum. Complete Triangle rows still pan horizontally when they exceed that frame.
  A data table bleeds only above `--site-table-bleed-from` (80rem, 1280 pixels): from
  there it grows one pixel for each pixel of window, `--site-table-wide`, until it
  reaches the page gutters or `--site-table-max` (100rem, 1600 pixels), past which its
  columns would only spread apart and a row would be harder to follow.
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

- **Video playback.** A paused film has a large keyboard-accessible Play video target
  over its picture, with a prominent central play icon.
  Native controls remain exposed below the target.
  Playback hides the overlay; pause or completion restores it.
  No-JS readers retain native controls.
  The homepage never starts playback unasked.
  The overlay uses the shared theme, focus and hover-motion rules (`think-34tf`).

- **Row-scale comparison.** Row-scaled Atlas packings share the enclosing frame’s bottom
  baseline and left edge.
  Smaller packings leave the gray reference square visible above and to the right.
  The reference used the muted-text gray until 2026-10-23, when the owner asked for a
  lighter one: it now takes `--site-atlas-reference-ink`, 69% muted gray mixed with the
  page background, the lightest mix that keeps a graphic’s 3:1 contrast in both themes
  (3.05:1 light, 4.77:1 dark), the same shade in every tile and lighter than the
  container and the muted text.
  A halfway mix, first chosen, read 2.14:1 in the light theme (review A, A14). Scaling
  anchors at the shared renderer’s frame inset, preserving its margins and original
  geometry (`think-m05q`). Fixed and Global scales retain their positioning.
  Gray reference frames use the same centered SVG stroke and displayed line width as the
  black container (`think-y6lt`). Web count labels use medium weight, up to 1rem, every
  count at the same weight: the perfect-square endpoints were bold (`think-ju2n`) until
  2026-10-23, when the owner made them match the rest.

- **Page headings.** Every ordinary page H1 uses the shared centered sans-serif caps
  style and title spacing automatically.
  The `site-title` class gives selected H2 sections the same treatment; a new H1 needs
  no styling class. Popover detail and mathematical record headings retain their
  dedicated compact rules.

- **Small choosers.** Inline single-select and multi-select choices share the homepage
  Atlas’s `site-tabs site-chooser-small` component in `site-nav.css`. The text uses the
  Results widget control size scaled by seven eighths (`think-ticj`; a little smaller,
  the owner, 2026-10-22), with 0.57rem inline padding.
  Every chooser button, the filter-menu trigger and Reset filters is 24 pixels tall, the
  floor a tap target needs, with its label’s capitals in the middle (the owner,
  2026-10-23). The label’s line is trimmed to its capitals (`text-box: trim-both cap
  alphabetic`) and the button centers it; the trigger trims its label and summary the
  same way, and a summary chip centers its own capitals on their baseline.
  Leading and padding alone left the capitals 0.35px high at 1x and 0.86px high on a 2x
  screen, where the browser rounds the font’s ascent and the half leading in device
  pixels. A browser without `text-box` centers the untrimmed 1.35-leading line in the
  same 24 pixels. `test_every_compact_chooser_centers_its_capitals` holds every label to
  a quarter pixel on the Atlas, the homepage, News and Results, at 1x and 2x. Borders,
  hover, keyboard focus and motion use the same rules on every page.
  Topic choices inside the shared multiselect disclosure always use the common neutral
  News surface with topic-colored ink and a check when selected.
  They have no label underline or inset selection mark.
  Single-select tabs keep `aria-selected` and arrow-key navigation; multi-select groups
  use native buttons with `aria-pressed`. Group names remain accessible when visually
  hidden. Each compact choice owns its border, so wrapped rows fit their buttons.
  News keeps significance inline and puts only Topics in the shared filter disclosure.
  It has one unboxed Reset filters action, right aligned above the item count.
  Chooser strips wrap at narrow widths; pages only place the groups.
  All action groups use a shared 0.7rem gap and wrap together at narrow widths; no
  section owns separate button spacing.
  Filter counts use the Results `site-table-tools` row and `site-count` role, aligned to
  the right above the items they describe, with the shared control typography.

- **Visual summary.** A case has one view wherever it is shown, its visual summary
  (`render_case_pages.visual_summary`, a `section.site-case-summary`), shared by the
  record page, case popover and each case in a result overview (**Result Overview**,
  below). It is the ascent film’s panel for the case, laid out for a page with the
  drawing first: the known-best packing centred and large, captioned in a record with
  its side and its credit; then the gap bar (a number line from one below
  $\lceil\sqrt{n}\,\rceil$ to two above it, the integers and the values of $\sqrt{n}$
  and $\sqrt{n} + 1$ marked, the two bounds as bold rules with their values above and
  the open span between them shaded); under PROVEN the bound as one statement, the
  proved lower bound in scarlet and the best known side in green; the badges; the
  citation, one line per bound with this project’s note; and what is OPEN. A citation
  line is a table row of two cells, the label (“lower” or “upper”) and the source, so
  the label column is as wide as the wider label however it is drawn, and the source
  wraps between words beside it.
  A case record opens with the centered Case Record eyebrow, the large $n = N$ heading
  between its two steps, its packing diagram, then badges and main bound formula.
  Until 2026-10-23 the diagram came before the heading; the owner then put the steps on
  the heading’s line, and the diagram, which fills a case popover’s width, would have
  carried them below the fold of a laptop’s window and to a new height for each case.
  Result case panels keep the diagram-before-count order, having no steps.
  The number line and supporting facts follow.
  The drawing fits the available width up to 20rem, 18rem in narrower containers and
  14rem in the smallest containers.
  Canonical records and fetched popovers share these rules.
  Main bound statements use serif math; number-line labels and facts use sans.
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

- **Web Atlas labels.** Tiles show only the case number, in ordinary ink.
  Case headings, table counts, and dates also keep ordinary ink.
  Gray Row reference frames paint behind the black packing container.
  Bounds, algebraic degrees, and evidence icons belong in the case popover.
  The PDF graphics retain their full labels.

- **Case badges.** A case’s properties have one mark on the site, the film’s badges:
  optimal (O), exact (=), numerical (≈) and known rigid (one dark R), each its glyph in
  a small square, solid or outlined (`.site-atlas-badge`,
  `result_overview.badge_glyph`); an open bound uses the outlined “?”. The visual
  summary lists them with their words.
  Recent upper constructions, verified lower proofs and optimality each have independent
  flags from `result_status.recent_contributions_by_case`, rendered in the new-result
  ink. An optimality proof can therefore make O red while the historic upper construction
  and equality numeral remain in ordinary ink, as for $n = 11$. The displayed bound
  numeral follows its own contribution flag; R stays dark.
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
    popover. `static_content_page` supplies the styled shell, navigation, colophon and
    shared article overlays; the record remains readable and printable on its own.
  - **The directory.** `atlas.html` is the graphical case directory, with all 324
    packings visible by default.
    The separate `frontier.html` provides the complete bounds table.
    Old `cases/`, `cases/index.html`, and `cases.html` directory links forward there
    while preserving case selections.
    Individual case-record addresses remain canonical.
  - **The case popover.** A page that opens cases carries one shared `#pop-case`
    (`render_case_pages.case_popover`). Atlas tiles, Frontier rows and `a[data-case]`
    links open the matching canonical record there.
    Its centered compact **Case Record** label sits above a larger typeset $n = N$ count
    (`think-g28m`). Case-property icons come first on the status line, followed by notes
    and textual tags such as “proved”.
    The shared article loader supplies prepared, rebased and ID-scoped clones (**Article
    Pages and Overlays**, above).
    The close control, Escape, outside click, and focus return remain shared behavior.
    The record’s previous and next steps (**The record**, below) and the left and right
    arrow keys change the case in place.
    In the popover the record’s label shares the line of the icons at the upper right,
    and the drawing, the count and its steps start below them.
    In the fetched popover, the packing figure uses the panel’s full content width while
    mathematical prose retains the shared reading measure.
    The standalone page keeps its compact drawing width.
    There is no **All cases** control.
    The sticky footer offers **Case Record**, **Frontier Survey Row**, and **Atlas
    Diagram** destinations, all with the same right-arrow design.
    Case changes update every destination.
    The packing diagram is centered directly below the Case Record eyebrow and above the
    count, icons, number line and supporting facts, sharing the full record layout.
    The sticky action footer has matching padding above and below its buttons.
    Long formulas scroll within the prose, and the panel fits the phone viewport.
    Fetch failures use the link’s canonical case page as the fallback.
  - **The record.** Its header shows the mathematical case count between its previous
    and next steps, then ordered status marks, and the verified interval as display-size
    math. The steps share the count’s line (the owner, 2026-10-23): a left arrow at the
    line’s left end and a right arrow at its right end, each alone, in the link ink, its
    ink meeting the left or right edge of the drawing’s frame below, on a 2.75rem target
    that ends at the line’s end.
    The line is as wide as the frame, which is drawn 1000 units in a view of 1020. Each
    names the case it loads in its accessible name and tooltip (“Previous case, n = 16”)
    rather than in visible text.
    The count stays centred whether the case has two neighbours or, at 1 and 324, one.
    The line comes straight after the label, above the diagram, so the steps stand at
    one height for every case and, in the popover, just below its icons.
    Until that day the steps, each an arrow beside its neighbour’s count, ran across the
    record’s first line above the label, and in the popover they kept clear of the
    corner’s icons (`think-0dxa`). The standalone and fetched articles share
    `--site-case-max`: the reading measure plus the foundation column insets, capped at
    48rem. It resolves at the root so a fetched article keeps the same width regardless
    of the opening page’s layout band.
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
    so its prose, math and links are rendered as any page’s are; each complete record
    article is cut from it (`render_case_pages._rendered`), prepared and wrapped by
    `static_content_page`. Each record’s links are written again from `cases/`
    (`rebase_links`). In the one render a record is a `<section>`, since the page’s own
    article holds every record, and in its file an `<article>`. Its headings’ ids are
    made again within the record alone, from their text with kpress’s own slugger
    (`_own_ids`), so a heading added to one case file never renumbers another record’s
    and breaks a shared `cases/N.html#…`. The page model’s list of headings, the
    records’, is emptied on the record page, which has no contents rail.
    A footnote in a case file is refused: kpress gathers footnotes at the foot of the
    one render, outside every record.
  - **Shared assets and old addresses.** Complete case pages reference the site’s hashed
    fonts, CSS and programs (**Shared Assets**, above); their articles carry the
    record-specific bytes.
    `cases.html` and the former `cases/` directory forward to `atlas.html`, preserving
    registered case selections (**Document cards and moved pages**, below).

- **Visuals.** The homepage groups its print and film under **Visuals**. One centered
  featured card, up to 42rem wide, shows the complete 324-case triangle poster without
  cropping and links directly to its PDF. Its high-resolution PNG comes from the
  canonical builder and is published through `SiteAssets.image_file`, so the immutable
  fingerprint changes with its bytes rather than reusing a cached Grid picture
  (`think-t2yf`). Posters retains both the 100- and 324-case PDF cards.
  Their eyebrow label is “PDF”. The homepage video is a native inline player with
  controls, `playsinline` and `preload="none"`, showing the retained poster until
  clicked. It does not autoplay.
  The full player also appears on `visualize.html`. Below the homepage media, **All
  Posters** links to `posters.html`, **Videos** to `visualize.html`, and **Open
  Workbench** to `workbench/`, in the shared action row.
  Retain the poster SVG links and source README on the Posters page.
  The dedicated Atlas page contains the atlas controls and cases, without media cards.
  A single-card group is centered.

- **The film.** The Videos page, `visualize.html`, shows the n = 1 to 324 film at full
  size below its breadcrumb and Videos title (**Page headings**, above).
  It is as wide as the window allows less the page gutters, up to 120rem, but never so
  tall that it will not fit the window whole (`.site-film-frame`), and embedded inline,
  with its controls. Its poster, `ascent-n1-324-poster.png`, published beside the
  explainer’s assets, shows until playback starts, at the video’s own 16:9, so starting
  moves nothing. The film starts when the page is visited.
  Its markup mutes it (`muted`, which a browser requires of a film it starts unasked)
  and marks it `data-autoplay`, and the shared `overview/film.js`, sets `autoplay` and
  plays it. It does not loop.
  **Visiting the page therefore starts the film’s download**, a 216 MB file on the
  release, which the browser fetches as it plays.
  A reader who asks for reduced motion (`prefers-reduced-motion: reduce`) keeps the
  poster and the play control, and so does a reader without scripts, the page framed in
  a card’s popover, and a browser that refuses to start the film.
  For them nothing is fetched until they press play: the markup keeps `preload="none"`
  and has no `autoplay` of its own, since markup cannot make that depend on the motion
  preference. No other film on the site starts unasked: the explainer’s stays as it was,
  fetching nothing until a reader presses play, and the overview’s inline video starts
  only when a reader presses play.
  The tools that open the film’s page in a browser (`preview_site`,
  `measure_site_pages header` and `baselines`, the browser tests) open it under reduced
  motion (`preview_site.motion_for`), so none of them starts the download; every other
  page they open as any reader’s. `tests/node/overview_film/` runs the script against a
  stand-in film. A caption in the support colour and a note in normal foreground follow
  at the reading measure: what the film shows, its length, the shorter 1 to 100 film,
  the release both are on, and the Workbench.

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
  above); the result, its summary whole, method and all; the cases, n; the credit, the
  finder first and “after …”, what the result builds on, quiet after it, in full; the
  rungs, verification and confirmation, with the kind on a line under them; the status
  line, its chips one under another (**Chips**, above); the details, the result’s
  records (its case link, the register, its evidence, source and reviews), a link to a
  line; and the id, the last column and the row’s trigger, as narrow as an id, under the
  6rem KPress keeps a cell to.
  The owner set that order on 2026-10-02: the id led and the date closed the row until
  then (`think-t090`); the status line stood under the kind (`think-ybt5`); and the
  records stood on a quiet line under the summary, a dot between two links, where the
  result’s cell holds the claim alone now (`think-e4o3`). Significance left the rungs
  for a column of its own, the second, on 2026-10-03 (`think-m3m4`). The status cell
  sorts on the status word; the details do not sort.
  On a phone each row is a card that places its cells by class, not by column, so the
  card reads as before: the id, the cases and the rungs on its first line, the
  significance under the id and the status under the rungs, the claim with its details
  on a line under it, a dot drawn between two links, then the credit and the date.
  Both tables use the same row renderer.
  The homepage publishes a bounded Recent Major Results subset, while the Results page
  includes every result and its filter bar.
  On the Results page a row has its result address (`id="t-018"`); on the homepage it
  names the result as `data-result`. Both retain the result’s details and native record
  link, and open the same canonical article through the shared row popover.
  The line under the overview’s table, “All Results”, links the overview to the results
  page, and so does a status line that names the results superseding its own: each named
  result links to its row on the results page (`overview_sections.result_url`), in place
  there and across from the overview.
  Both sort on any column whose header carries the sort pair.
  The widths follow from each column’s floor and from what the n column asks for.
  The id, the significance, the rungs, the status, the details and the date are as
  narrow as what they hold.
  The significance column holds the shared 4.8em meter, with the cell’s 0.2rem padding
  either side and room for a new-result star.
  The details are as wide as their widest link, “evidence 10”, 102 pixels, and a result
  with many records is the tallest row: T-075’s sixteen links stand 410 pixels.
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
  column beside it. In the earlier S3 homepage layout measured for `think-x60s`, the
  initial view included T-056. The following measurements describe that layout, before
  the bounded S4 Recent Major Results subset.
  With every row showing, the date, significance, result, n, credit, rungs, status and
  id columns measure 100, 77, 389, 225, 220, 180, 114 and 56 pixels at a 1440-pixel
  window, where the table is 1360 and gives the n column its whole measure: T-056’s list
  takes 6 lines, a row 165 pixels tall, under the 182 of T-044’s row.
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
  Secondary metadata in a cell takes `.site-cell-quiet`, which uses the support colour
  and the sans face. Credited people retain normal foreground, including when the shared
  compact cell treatment is used.
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
  The Results legend defines the red recency text once.
  A superseded result’s metadata reads quieter in the support colour; its substantive
  summary keeps the normal foreground and its chips keep their fills.
  A row reached by its address (`frontier.html#n-11`, `results.html#t-018`) takes the
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
  - **Recent** records whether a verified lower bound is recent.
    It sorts, and “recent only” filters on it.
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
    made short columns unnecessarily wide.
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
  - **Property badges.** Rigid, optimal, and exact-value glyphs use the same shared tag
    font-size and height tokens as the Status chip.
    Each square retains its accessible property name and the table’s compact centred
    alignment.
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
| Significance | `data-s`, the S level | one of the selected S1–S5 segments |
| Verification | `data-v`, the V level | a floor: V4 and up |
| Confirmation | `data-c`, the C level | a floor: C3 and up |
| Kind | `data-kind`, the register’s `kind` | equal to the kind chosen |
| Status | `data-status` | equal to the status chosen |
| Hide superseded | `data-current`, `true` or `false` | checked: the result is not superseded |
| Source | `data-source`, `ours` or `others` | this project’s, or others’ |
| Case n | `data-n`, counts and ranges (`18-21 26`) | the result covers that n |
| Max age | `data-date`, a whole ISO date | dated at most that many days ago |
| Project (preset only) | `data-project`, the slugs of the listed projects the result is attributed to | the list has the project chosen |

Significance uses the same inline segmented buttons as News and the homepage Atlas, with
S1 through S5 in ascending order and every level selected by default.
Several selected levels combine with OR; the selection combines with other facets by
AND. Verification and confirmation retain their floor selects, with All followed by the
rubric’s levels above its lowest, the top level bare.
Kind offers the kinds the register holds, in the rubric’s order and words.
Status offers the statuses the register’s results have.
A date the register gives only to the year is the first day of it (`1979-01-01`). Max
age is a number of days, and empty is no limit.
There is no date range.

- **Composition.** The filters compose: a row shows when it passes every one, and an
  empty text/select control or an unchecked flag passes every row.
  No selected significance segments shows no rows.

- **Significance addresses.** Exact `s=4` links and noncontiguous selections such as
  `s=1,3,5` set the visible S segments.
  Legacy `s-min=3` and `s-max=4` bounds select their intersecting levels; exact and
  threshold parameters compose when both occur.
  Clicking a segment writes the selected levels to `s`, or `s=none` when none remain;
  selecting every level removes that constraint.
  It preserves unrelated parameters, other facet controls and row bookmarks.
  Back and Forward restore the selection and count; a fresh bare archive address
  restores all five levels.
  Hidden legacy S controls adapt published URLs and never reappear as dropdowns.

- **Preset-only controls.** Project follows the bar’s own controls and is out of the bar
  (`hidden`, on its label) until a link sets it:
  `results.html?project=evand-square-packing` opens results attributed to one listed
  project, and `&s=4` selects only S4 through the visible segments.
  The other projects’ cards link this way (**Other projects**, above).
  While a preset control filters, its label is in the bar with the choice it holds, the
  project by its owner and repository, so the reader sees what narrows the table, and
  choosing All takes it out again.
  A project’s slug is its owner and repository in lower case, hyphenated
  (`overview_sections.project_slug`).

- **Status.** The select offers each status some result has, in the workflow’s order:
  `recorded`, `reviewed`, `confirmed`, `incomplete`. It is the chip the row draws, so
  what a reader filters by is what a reader sees.
  A link can preset it, as it can any control: `results.html?status=recorded` is the
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

- **Defaults.** Recent Major Results on the homepage contains at most 12 results of
  significance S4 and up, at most 180 days old and not superseded (`RECENT_DEFAULTS`).
  The renderer selects the rows; the homepage has no filter bar, count or scope line.
  The complete results page includes every row and starts at All, no maximum age and
  Hide superseded clear (`RESULTS_DEFAULTS`). Its other controls start at All too.
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

- **A row named by the address** (`results.html#t-048`) shows whatever the filters hide,
  so a link to a result never lands on nothing.
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
    name. One cell holds the row’s native entry, styled as its key.
    Generic `row_detail` writes a `<button class="site-row-open" popovertarget="ID">`;
    `result_row` uses an ordinary `<a class="site-row-open" href="result/t-nnn.html">`
    around the result’s ID, so the complete result remains reachable without scripts.
    The popover follows the table, outside every cell, so it takes no style from the
    table: `<div class="site-popover site-row-pop" id="ID" popover role="dialog"
    aria-labelledby="ID-title">`, holding the close cross, the `.site-card-label`, the
    headline `.site-popover-value` with the id `ID-title`, the body in
    `.site-row-pop-body`, and the optional `.site-popover-actions`. The ids are
    `pop-result-t-nnn`.
  - **Without scripting** a result ID navigates to the complete record.
    A generic row’s native popover button, where used, opens its authored body as a
    card’s button does. `overview/row-popover.js` makes the row the control: it gives the
    row `tabindex="0"`, `aria-expanded` and `aria-controls`. It takes a generic native
    popover button out of the tab order; ordinary result links remain links with their
    own behavior and tab stops.
    The row carries no `tabindex` in the HTML, since a focusable row that did nothing
    would be a dead stop for a reader without scripts.
  - **Sorting and filtering** (`overview/table.js`) move and hide rows.
    A row finds its popover by id, so the popover follows its row.
  - **Content.** One function writes a row’s popover body,
    `overview_sections.result_row_popover_body`, on the overview and the results page
    alike. Every result panel keeps an **Open Result Record** action to its complete
    page, where the same article can be read, shared and printed independently.
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
    The script asks the shared article loader for the complete page when the row is
    first pressed or its popover first opens, then places its prepared article clone in
    place of the short form (**Article Pages and Overlays**, above).
    The page gains only the address.
    Where the file cannot be had, without scripts, on a page read from a file or off the
    network, the short form stays, and the next opening asks again.
    A result’s short body points to the persistent **Open Result Record** action.
    That ordinary link reaches the complete result and remains when a fetch fails.
    A later opening tries again.
    The page carries neither a second full overview nor a root-relative HTML fragment;
    its source is the complete result page (**Result Overview**, below).
    Case panels use the same loader for their complete pages.

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
  That left the Frontier page’s card in a section of its own, Frontier Survey, beside a
  card to the recent cases (`frontier.html?recent=true`, the query the table script
  presets a filter from), until the owner dropped the section later the same day and
  moved the card to every case up to the page cards (`think-ec5k`); the query still
  works, and nothing on the homepage links it.
  `tests/test_overview.py` holds each section’s prose to one paragraph of its own where
  this applies, the cards to their pages, and the three pages to saying each thing once.

- **Recently Added.** Directly below the Atlas preview, the homepage lists what reached
  `main`, and with it the site, on the newest arrival day and the seven before it, one
  native disclosure a day, newest first, the newest open
  (`overview_sections.recently_added`, the owner, 22 October 2026, `think-rqen`). Each
  day holds every result that arrived, at any significance, by its `landed`
  (`added_entry`, its id linking to its row in All Results, and the day’s link opening
  All Results on that day, `?added=`); each count whose house best packing changed,
  under the result that holds it now; and each source’s dated beyond-horizon rows, one
  line a source with its count, its span of counts, its credit and how many are since
  superseded, linking to the source’s packet on GitHub, since no page of the site lists
  those rows. Houses and rows are placed by the day `main` first held them, which
  `devtools.stamp_landed` writes into `packing/frontier/landings.yaml` at the merge step
  as it writes `landed`; nothing that renders reads Git (OR-18). One window bounds all
  three, ending on the newest of those days (`arrival_reference`), and the introduction
  names the days shown.
  The summary tallies the three and wraps between them.
  The section draws with `results.css`’s rollup classes, and its introduction links All
  Results and News. `tests/test_home_recent.py` holds it to the records and to 40,000
  bytes.

- **Recent results.** The homepage’s **Recent Major Results** section sits below
  Recently Added and News.
  It contains up to twelve current results of significance S4 or higher from the last
  180 days, newest first, excluding superseded results (`think-5c8r`). The preview has
  no count/scope sentence or introductory text explaining the links.
  The table shares the full Results page’s columns, sorting, result popovers and mobile
  row cards. Filtering and older results remain on `results.html`, whose defaults are
  unchanged. A result’s ordinary link opens its canonical article without scripts.
  One **All Results** action follows the table and links to `results.html#all-results`.
  The homepage omits the verification legend; the full explanation is on Verification.

- **All Results.** Results is a menu container with no landing page.
  All Results (`results.html`) is the one complete sortable, filterable result table.
  Its menu label, H1, browser title, breadcrumbs, and result-record ancestry agree.
  Visual Atlas, Frontier Survey, and Verification share one action row below the table,
  with no collection actions above it.
  Filters start with significance at All, no maximum age and Hide superseded clear, so
  every registered result shows once, newest first.
  Each row keeps its own ID (`#t-018`), shared result popover, and ordinary canonical
  article link. The homepage retains its bounded recent preview with one **All Results**
  action. `recent-results.html` and `all-results.html` are compatibility forwarders to
  `results.html`, preserving queries and result-row fragments.
  Old recent section fragments map to `#all-results` on the complete table.
  Visual Atlas (`atlas.html`) provides the graphical case directory; Frontier Survey
  (`frontier.html`) provides the complete bounds table and its reading key.
  Verification (`verification.html`) contains verification, evidence, credit and status
  guidance and links to Project Epistemics (`epistemics.html`). Legacy verification
  fragments retain their Verification targets.
  Each substantive destination has its own page and a plain current breadcrumb item
  under Results. Result article trails link All Results; cases link Visual Atlas.
  `site_navigation.py` supplies the same ancestry for visible and structured trails.

- **Document cards and moved pages.** Repository-document pages also use the papers’
  shared upper-right source-action row.
  GitHub links the actual repository source and MD its raw Markdown; neither invents a
  PDF edition. `SiteDocument.source` supplies the path for every hosted document, and
  Synopsis chapters share `SYNOPSIS.md`. The chip markup and styles have one
  implementation across papers and documents.
  Source controls before a document’s first heading preserve its normal page-top
  spacing. The overview’s documentation section has one card for each repository document
  the site renders, in the order of `render_overview.DOCUMENT_PAGES`: `README.md` and
  `epistemics.md` first, then `SYNOPSIS.md`, `conventions.md` and `development.md`.
  `RESULTS.md`, `STATUS.md` and `defects.md` were cards and pages until 2026-10-01
  (`think-bk2e`); the first two are generated views of the record the results table and
  the frontier atlas show, and the defect log is internal to the repository.
  A link to either register, in a reader document or a case record, leads to the page
  that shows it, at the result’s row when the link’s text is a result’s id, and a link
  whose text names the file opens the file on `main` (`site_documents.RECORD_PAGES`,
  `_record_links`). A page that moved or was withdrawn is still served at its old
  address, as a forwarder (`render_overview.MOVED_PAGES`,
  `templates/site-forwarder.html`): `forward.js` reads where a visit goes from the root
  element’s `data-moved-to` and sends it there with its query string and fragment, and a
  reader without scripts gets a refresh and a link.
  `all-results.html` goes to `results.html`, `status.html` to the frontier atlas,
  `defects.html` to the defect log on GitHub, and `cases.html`, every case record on one
  page until 2026-10-03, to `atlas.html`; registered case selections such as `#n-11`
  reach the corresponding row on `frontier.html` (**Case records**, above).
  The profile directory and the profiles served under `contributors/` until 2026-10-13
  forward to their pages under `profiles/` (**Person Profiles**, below).
  No page of the site links a forwarder; `tests/test_site_documents.py` and
  `preview_site.moved_links` hold the pages to that, and `check_published_site` asks the
  deployed site for each one.

- **Learning catalogues.** Learn is a menu container with no page or URL. Papers
  (`papers.html`) contains all four papers, with the three parts of the $n = 11$ series
  in reading order followed by the methods survey.
  Tutorials (`tutorials.html`) presents both the basic introduction and advanced
  companion with their full introductions.
  Posters (`posters.html`) contains the two infographic posters; each paper’s PDF and
  source editions remain with that paper on Papers.
  The old `downloads.html` page forwards to Posters, preserving query and fragment.
  `papers.html#pdfs` forwards to `posters.html#pdfs`, and `posters.html#paper-editions`
  reaches Papers. Videos, Workbench, and Resources have their own substantive
  destinations. Only Overview carries summary previews.
  Published Papers fragments forward to the corresponding full catalogue or Videos page,
  retaining queries; without scripts, ordinary links at the old anchors reach the same
  content. Reading cards come from `overview_sections.PAPERS`, each entry a document’s
  address, label, title, description and card size.
  Each card links directly to its document in the same tab, with no popover or framed
  preview (`link_card`, `new_tab=False`; see Cards).
  Links cited by descriptions belong in the section introduction rather than inside a
  linked card. The standalone papers keep their existing `papers/` addresses and
  independent publication editions.
  The tutorials remain `tutorial.html` and `tutorial-advanced.html`, using the
  reader-document pipeline.
  Learn is the active navigation ancestor on its papers, tutorials, downloads, Videos,
  Workbench, and Resources.
  The full film is served at `visualize.html`. Shared article overlays remain available
  for marked record and contributor links elsewhere on the page; the reading cards
  themselves navigate directly.
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

A result’s row, in the homepage preview and All Results, opens a popover with the full
overview of that result.
`devtools/result_overview.py` writes the popover’s body, `result_popover_html`, and
[site-result.css](site-result.css) holds its styles, apart from `site.css` and linked
after it on every page.
The complete page wraps one `article.site-result[data-result-overview]` with a title,
neighboring-result navigation, the site’s shell and metadata.
Its single H1 keeps separate record-ID and headline spans.
At screen widths up to 40rem, the ID occupies its own line so font arrival cannot push
the headline off a shared line.
Desktop and print keep the inline title.
Heading math resets inherited uppercase transformation, caps and letter spacing;
variables retain their mathematical case.
The article has its own IDs and prepared math and may contain a native table for a broad
result’s cases. The shared loader scopes those IDs and resolves links when the article
enters a panel, so its content can be read outside the originating table.
Its popover uses the shared reading-measure width cap and may be as tall as the window
allows (**Cards**, above), and scrolls as one panel.

Listing pages carry a short native link and an action rather than every full overview.
Each result is published once as `result/t-nnn.html`
(`render_overview.iter_result_fragments`, materialized by `result_fragments`), and a
row’s popover extracts its article through the shared loader when it first opens (**Row
popovers**, Fetched bodies).
The historic function names refer to complete pages.
The complete page’s links are written from `result/`; a fetched clone resolves them
against the response address, so any page of the site can place it.
The singular directory `result/` stays distinct from the canonical `results.html` index
and a host’s extensionless `/results` spelling.
`tests/test_overview.py` holds the listing pages under their size ceilings, and
`tests/test_result_overview.py` holds a broad result’s complete page under its own
budget without dropping case rows, credit links or article content.
`check_published_site` asks the deployed site for every overview the results table
names.

- **Head.** The popover’s shell label and summary name the panel while it loads.
  After a successful fetch, the canonical article’s `h1` becomes its single visible
  headline and accessible name; the duplicate shell label and summary are removed.
  The shared loader’s scoped heading ID is preserved for references.
  Loading failures retain the shell title and native link.
  The pristine cached article and standalone page keep their title.
  The body opens with the significance mark, the V and C rung chips, the kind chip and
  the status line, as the tables show them; then the date and what it dates, in the
  tables’ order (`date_cell`), with date and case metadata in the support colour and
  credited people in normal foreground; the claim at the note size; where the entry
  declares a later result that implies it (`superseded_by`), a paragraph under the claim
  that opens “Superseded in part by T-060.”, the later result linked, and says what it
  implies and what still stands; and a closed disclosure with the significance,
  composition, next rung and novelty.
- **The case.** A result about one case, or up to four, shows each case’s visual summary
  as the case’s record opens with it (**Visual summary**, above), smaller and with no
  caption under the drawing: the packing drawn at the atlas’s scale
  (`render_case_pages.visual_summary` at `ATLAS_UNITS`), at most 18rem wide, then the
  gap bar, the bound as one statement with the lower bound in scarlet and the best known
  side in green, the badges, the citation and what is open.
  Its facts are the film’s own (`atlas_film_facts`), and it is written, its gap bar’s
  labels placed, when the complete page is rendered.
  Where the result is about more than one case, each panel is headed by its $n$. Under
  the panel, the case record’s verified and reported bounds and the gap form a small
  grid, each value linking to its field in the case file.
- **Many cases.** A result about more than four cases says so and lists them in a native
  table inside a scrolling box, one row each: the n linking to the case’s record file,
  the two bounds in the film’s colours, the gap, the status chip, the frontier row and
  the case file. Identical consecutive bounds and badges use native row spans; every case
  retains the same six logical cells and links.
  Browser checks expand the DOM spans to verify the complete table.
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
  the site does not serve and on a result page no row carries.

A section heading in the overview is a caps label, so it holds no formula: capitals
would change the formula’s letters.
`tests/test_result_overview.py` holds every part and every link.

## GitHub Links

Repository and document links use the existing GitHub brand mark.
Issue links use Lucide `circle-dot`; pull-request links use Lucide `git-pull-request`,
matching the open-issue and branch shapes GitHub readers recognize.
The retained SVGs in `devtools/overview/icons/` supply both inline reference icons and
the shared stylesheet’s decorative masks: Lucide 1.17.0 under ISC, and the existing
Octicons GitHub mark under MIT. The KPress sprite has no GitHub brand glyph.

At publication, `site_github_links.decorate_github_links` classifies exact
`github.com/owner/repo/issues/N` and `/pull/N` routes with one data attribute.
Repository owners named `issues` and query strings containing those words keep the
GitHub mark. Link targets, labels and nested code or mathematics stay intact; bare
account handles keep their account text.
The shared stylesheet paints a compact mark in the link’s colour beside its first line,
including on pages without JavaScript and inside fetched popovers.
Links with an existing SVG, image or card icon receive no second mark.
These screen decorations do not change paper pagination.

## Person Profiles

[Attribution Policy](../../../attribution.md) owns preferred names, verified aliases,
person/project distinctions and exceptions.
This guide owns their presentation.

Profile Resources reuse the homepage resource-card renderer: resource title, author
byline, source-address link, description and available result/significance and credit
tally retain the same order and link targets.
A profile does not introduce a second resource inventory.
Available GitHub issue and pull-request evidence uses linked number labels such as
“#123”, with the corresponding Lucide issue or branch-style pull-request icon.
Accessible labels identify the repository and reference type; references come from
recorded evidence rather than inferred authorship.

Account links share one renderer and glyph set in the directory and on profiles.
GitHub uses the filled Octicons mark already used on resource cards; X uses the filled
Simple Icons silhouette (CC0). Brand icons have no outline stroke.
Generic website links inline the same Lucide `external-link` glyph used by KPress’s
reader-control icon system, so standalone pages need no sprite dependency.
The table keeps account usernames visible beside the marks and adapts spacing and
wrapping, not icon shape or link semantics.
Account marks use a compact shared icon-size token, also used by the navigation GitHub
mark and Contrast icon.
Navigation replaces the GitHub text with the shared mark and retains an accessible
GitHub label; control hit areas remain independent of glyph size.
The directory uses the shared wide-table bleed on larger screens.
Account labels have room to read; if a long username wraps, its icon aligns with the
first line. Narrow screens retain the standard table scrolling treatment without
page-level overflow.
Profile handles, account links, resource descriptions and credited work use the normal
document foreground in each theme.
Their content role is primary; an account handle is not muted metadata.
Evidence and breadcrumb metadata may retain the secondary text role.

The profile directory at `profiles/` is a native table: full real or public **Name**,
**Records**, **Results**, **Credits**, **Years active**, **Resources**, and
**Accounts**. Its default order uses the shared evidenced surname key, falling back to
the public handle when no surname is established.
Every column uses the Results table’s shared sortable-heading interaction: pointer,
Enter and Space update the order and `aria-sort`, while the initial Name order remains
announced. Tally columns sort their numeric counts, including zero when its display cell
is blank. Years active sorts by the first recorded activity year.
Missing years, resources and accounts stay last in either direction.
Native anchors and the complete surname-ordered table remain available without scripts.
The directory name contains only the full real or public name, in shared sans bold.
Account and resource links retain regular weight.
Additional handles appear on the individual profile, while account usernames remain in
the Accounts column.
The Accounts column contains public GitHub, X and Substack account profiles.
Personal and publication websites belong in Resources, alongside project repositories,
displayed as domains or owner/repo labels with shared icons.
These website resources derive from the existing evidenced profile links rather than
duplicate stored records.
The Name column reserves 16rem so most full names stay on one line.
Accounts and Resources retain 12rem minimum widths without reserving percentages that
would squeeze names.
Resource addresses wrap at normal URL boundaries, with an emergency break for a segment
too long to fit. Icons stay beside the first line.

The directory introduction totals people, distinct supported current Records, distinct
primary Results, credited person/result pairs and unique linked resources.
Records are the intersection of the union of primary-authored result IDs with the shared
current-record index; global records without a profiled primary author do not inflate
this total. Shared Records, Results and Resources count once across the directory, while
each person retains their own counts in the table.
Years active uses evidenced dates of the person’s own authored or established work,
including original publications without a dedicated registered result.
A later result citing that work does not extend the original author’s activity range.
Import dates, archive capture dates and undated catalogue ownership are not activity
evidence. Equal endpoints render as one year (“2003”); different endpoints render as a
range. Unknown years stay blank.

Results and Credits occupy separate directory columns.
A zero result or credit count leaves its cell blank.
The Records, Results and Credits cells keep each nonzero total on its first line and
start the muted parenthetical significance breakdown on the next line.
The shared tally remains inline on cards and other compact surfaces.
Individual profiles show Records, Results, and Credits above Resources, each metric on
its own line with its links and significance breakdown intact.
[Attribution Policy](../../../attribution.md) defines the two disjoint per-person
buckets: Results are primary-authored results; Credits are results that explicitly
credit the person in another role.
Each person counts once per result in the appropriate bucket, even when the source
repeats their name.
Both significance tallies use the score of the result being reported.
An S5 result by A crediting B and C gives A one S5 result and B and C one S5 credit
each. Global credits count unique person/result pairs, not unique result IDs or raw
occurrence spans.

Case credits alone do not establish authorship of every result for that case, and owning
a resource does not establish authorship of its contents.
Raw reviewed span counts remain census diagnostics.
`site_tallies` owns the joins, counting and shared wording.
A single occupied level reads “1 result (at S5)” or “1 credit (at S5)”; mixed levels
read “12 results (1 at S5, 2 at S4, 9 at S3)” and the same pattern for credits.
Profile and table variants change layout only.
Project cards scope both tallies to the project’s reported results and evidenced credit
associations, not its owner’s global count.
Zero reviewed credits means no established associations in this record, not no
contribution. Technical records, News, and compact credit labels use the shared
surname-or-handle naming policy.
Resource bylines and descriptions, explanatory papers and reader documents, and About
introductions use full public names.
Directory names remain full so people can be identified while browsing.
The Contributor Profiles directory opens with one serif sentence identifying its
purpose. Its tallies, table, links and controls retain their shared sans roles; detailed
column definitions remain in the documentation.
The Accounts column has a 16rem minimum and keeps account identifiers on one line.
Narrow screens scroll the table inside its wrapper; resource URLs keep their own
wrapping rules.

Home and About share a short Profiles invitation and the **All Profiles** action
(`render_contributors.profile_preview`), with no name list or metadata reads.
Breadcrumbs appear only on lower-level pages, including the Profiles directory and
individual profiles.
Top-level Home, About and News pages have no breadcrumb.
On nested pages the breadcrumb sits nearer the navigation, with a larger gap below it
before the title; pages without a breadcrumb retain their normal top spacing.
The table’s native name anchor goes directly to the person’s profile.
Separate Records, Results and Credits columns use the shared significance tally.
Records are the current subset of authored Results across every result kind, including
formalization. Known zero counts stay blank; unresolved record classification shows a
Review pending link rather than implying zero.
Each tally links only to a section or filter that contains that exact population;
significance counts are plain text when no corresponding filter exists.
Resource and account links remain separate keyboard stops because they lead to distinct
destinations. Resource addresses link to their actual websites or repositories; avoid
empty fragment links when no resources are known.
Compact **Accounts** links show platform icons and usernames for public account
profiles. Website and repository addresses appear under **Resources** with appropriate
icons. Their accessible names and titles distinguish the platform, account and person.
The scoped directory script extends the pointer hit area to blank row space while
preserving account links, controls, modifiers and text selection.
It adds no popover or replacement table semantics; native links work without JavaScript.
The table retains shared KPress spacing, numeric alignment and horizontal overflow on
small screens.
It includes cited paper authors as well as the project’s contributors; the
page title and heading say **Contributor Profiles**, and its table label is
**Profiles**. The directory and profile pages keep **About** active in the shared
navigation. The account links precede the Years active and Handles fields on individual
profiles. Their breadcrumbs link to About’s `#profiles` section; each profile also links
to the full directory.
News articles and their homepage previews also use ordinary profile links.
Each profile’s breadcrumb navigates back to the directory.
Each profile has one complete article at `profiles/ID.html`; the directory, credited
names in tables and records, and the standalone profile use that address.
Person-name links navigate directly to the complete profile across About, News,
resources, tables, cases, and results, including links inside an open article panel.
The native address also preserves keyboard activation and modified clicks.

The profiles were served under `contributors/` until 2026-10-13 (think-0v2c); each
address served there is a registered forwarder to its profile
(`render_overview.LEGACY_PROFILES`), and no page links one.
A profile added since has only its `profiles/` address.
Module, record, schema, CSS class and `data-contributor*` names keep the contributor
vocabulary of the records under `packing/contributors/people/`. A person’s identity is
the profile URL, while original labels remain in the occurrence record.

`render_contributors.contributor_article` writes the complete profile article:
breadcrumb, public name, optional real name when different, selected alternate names,
optional bio, structured public links, reviewed credited work, source locators and
identity evidence. Unknown real names, accounts and biography facts are omitted.
The optional bio is one Markdown paragraph of at most five sentences, with sources
supporting its claims.
The renderer permits safe inline Markdown, escapes raw HTML, disables images and checks
links with the same HTTP(S) policy as structured links.
Sentence count is an editorial review rule; the loader validates paragraph shape and
evidence references.

Only the explicit `display_aliases` selection appears under **Handles**; the full
evidenced alias registry remains available for reviewed credit matching.
Structured links show the account handle or public URL beside the shared GitHub, X or
web icon (`site_icons.account_icon`). The link’s accessible name includes its platform.
`render_contributors.account_links` renders both the centered profile row with visible
handles and the compact, wrapping directory icons; both share styling and retain
external destinations.
Cited external work stays separate from personal account links.
`site_resources.Resource` projects the existing `OTHER_PROJECTS`, `OTHER_SITES` and
`CATALOGUE_SITES` inventories into one typed record per exact URL, including artifact
paths and comment fragments, with title, description, original byline, kind and resolved
profile IDs. Homepage cards, profile **Resources** lists and directory resource counts
consume this projection.
No person record duplicates these curated facts.
A curated whole byline resolves only to a unique evidenced public identity; compound
bylines match exact unique full names, preserving relationships such as “after.”
Descriptions do not establish ownership, and organizations stay distinct from people.
A resource with explicitly reviewed mixed-role credits can name its profile IDs directly
and use the label Contributors.
The ordinary By label is reserved for its author byline; support work does not become
proof authorship through resource membership.
Each resource appears once per credited person; its count is independent of reviewed
credit counts. Equal repeated URLs deduplicate, while conflicting metadata fails.
Resource descriptions and bylines use scoped prose linking with the profile subject
excluded; source titles and external destinations remain intact.
Related News lists the titles and dates of eligible announcements whose summary or
details explicitly link the person’s record, each at its stable News entry anchor.
No profile record stores a second event chronology.
Source IDs link to their public URL or archived source, with the locator beside them.
One closed native **Sources** disclosure contains the source list, biography sources
when present, and identity evidence linking the supported fields to those sources.
Credited work links reviewed occurrences to cases, results or bibliography entries,
retaining role and original public label.
Repeated mentions of the same work, role and label collapse, while distinct bibliography
records remain distinct and link their own entry lines.
Long credit collections use an initially open native disclosure; the complete collection
remains in the article.
Identity joins come from the reviewed occurrence manifest, not spelling matches.
The
[contributor plan](../../../docs/project/specs/active/plan-2026-10-10-contributor-profiles.md)
defines evidence, identity, census and maintenance requirements.

Biographies include evidenced years when describing dated work, and named papers or
projects link to their retained source, publication or tracking page.
The standalone bio inherits the shared 18px serif prose; the directory and profile H1s
use the shared sans-serif, all-caps page-title role.
The overlay inherits sans at the same 18px base and regular weight; its name and section
headings use the shared compact overlay scales, medium weight and heading leading.
Page section headings retain their serif italic role; overlay section headings are
upright sans. Typography comes from the shared rules rather than profile-specific sizes.
Handles, account links, credits and resources use the shared note role and normal
foreground. Breadcrumbs and provenance may use the support color; the Sources toggle
inherits the standard KPress summary role.
Identity terms use the shared medium weight.
Nested metadata never multiplies the note size.
`profile_links.link_prose` identifies people by exact full names or reviewed account
links, then applies the naming policy for that context.
Technical introductions, News summaries and details, and biographies use short labels;
resource descriptions and explanatory narrative use full public names.
Generated full-name links retain `data-profile-name="full"` so relinking and the
built-site audit preserve that choice.
Temporary matching-scope wrappers are removed after rendering.
It links unique exact full names and verified account links whose visible label matches
the same person, preserving authored text and source-work links.
Name matching permits soft-wrapped whitespace and checks collisions on the same
normalized spelling.
Existing links, quotations, code, mathematics and structured table credits are excluded;
biographies also exclude their own subject.
Raw aliases and surnames are never inferred.
The built-site audit reports remaining full-name mentions by page, with ambiguous names
listed separately.

The article adds no padding above the page’s shared top space.
The breadcrumb, article body, and headings keep equal left and right insets.
Long source identifiers and URLs wrap only when wider than a whole line.
Themes and standalone print read the shared KPress and paper tokens; no profile-specific
face, color palette or print scale is introduced.

[site-contributor.css](site-contributor.css) implements these roles.
`tests/test_render_contributors.py` checks safe prose, route and build integration,
source checkout and distinct work links.
`tests/test_site_contributor_popovers.py` checks direct profile navigation from
generated pages, including open case and result panels, and preserves their focus and
request-race checks.
Profile typography, equal insets, and overflow are checked at desktop and phone widths
in both themes. Profile schema checks and the occurrence tests hold the identity and
credit evidence contract.

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

Case and result records and person profiles are complete pages and carry the whole set
and the icon. A case’s name identifies its square count and bounds; a result’s name
combines its ID and summary; a profile’s name is the evidenced public name.
Each has its own record-derived description and canonical address.
The directory has its own identity at `profiles/`. Article overlays extract the body of
these pages, so the host page keeps its own head while the full record remains
independently shareable.

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

- **The credits.** Names and roles follow [Attribution Policy](../../../attribution.md).
  One line each, with names in bold, addresses as plain links, the version plain.

  ```
  From the original proof by **Manasseh Ahmed**
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

Tutorials use the same credit component, with human oversight, agents, original
publication date and revision date directly below the title.
Their Markdown sources retain a readable list; the site presents that list as centered
credits. Tutorials do not borrow the site’s edition number.

The credits are one grid column the width of the page (`.credits`, in the shared
typography layer), an address in them may break anywhere, and the three lines’ spaces
are `1lh`, on `.credits-source + .credits-own`, on `.publication-date` and on
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
[The series plan](../../../docs/project/specs/done/plan-2026-10-05-n11-explainer-series.md)
holds the decisions and their evidence; these are the rules a change to any of the three
keeps.

| Part | Slug | Explains |
| --- | --- | --- |
| I | `n11-lower-bounds-explainer` | The project’s point and 2-of-3 certificates: T-018, T-025, T-026 |
| II | `n11-threshold-bound-review` | Overbeck’s `s(11) > 31/8` (T-037): k-of-m charges, parents with strict cores over angle rows, the exact sweep |
| III | `n11-optimality-review` | Ahmed’s `s(11) = T` (T-060): cover, pose invariant, charge transfer, symmetry, capture, isolation |

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
uv run --frozen --all-extras --group dev python -m devtools.preview_site --shots "$TMPDIR/shots"
```

It scrolls each page to its foot first, so what a page places or loads lazily is in the
shot, and fails on console errors, a page wider than its viewport, math left untypeset,
any formula set in the wrong face (the Math rule above, its headline exception
included), and a row of cards off the centre of its line (more than a pixel between its
two slacks). `--page cases/11.html` walks a complete case record from the build the
preview serves, and `--press SELECTOR` presses a card or an atlas cell on each page that
has one, then walks and shoots what it opened, since a popover a script fills has no
math until it opens.
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
a standalone record stays at its complete address, neighboring links navigate to the
next complete page and Back returns; `cases.html#n-17` arrives at case 17; and without
scripts the complete record is read where it is.
`tests/test_overview.py` holds the cards and chips to the rules above.

`tests/test_site_contributor_popovers.py` adds generated directory, standalone profile,
case and result entry points to this browser map.
It checks article-only loading, relative and fragment links, scoped IDs, overlay
replacement, return focus, cancelled and late requests, no-script and failed-fetch
navigation, and profile roles at 1280px and 390px in light and dark themes.
Its design fixture adds long public source IDs and URLs and checks equal body insets and
zero horizontal overflow.
Optional `SQPACK_CONTRIBUTOR_DESIGN_SHOTS` retains representative and stress screenshots
in the task’s external scratch.
Route and sitemap coverage, stale-output removal, sparse evidence checkout and
publication input filters are held by the owner/test map in **Article Pages and
Overlays**, above. The shared stylesheet, color-token and browser floor checks cover the
contributor stylesheet and controller programs as other site components.

The linear-program display is reflowed within the print column.
`check_print_layout` guards its width so an overflowing equation cannot silently shrink
the whole PDF page.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
