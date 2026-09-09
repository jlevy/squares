# Paper Design

The explainer uses serif prose for sustained reading and sans serif text for figures,
captions, notes, and controls.
The web page and PDF share this hierarchy, with sizes scaled for each medium.
Keep these conventions reusable across papers.

[explainer-shell.html](explainer-shell.html) contains the local CSS layer above KPress;
[explainer-article.md](explainer-article.md) contains the article.
KPress supplies the fonts, Markdown typography, math, themes, and general print
behavior. The local layer sets the paper’s type proportions, reading measure, and figure
layout.

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
| Figure labels and controls | 18.05px | About 12.0333pt | Sans, 0.95 of the sans base |
| Captions and end footnotes | 17.48px | About 11.6533pt | Shared sans size: 0.92 of the sans base; 1.4rem side inset |
| Colophon | 16.15px | About 10.7667pt | Sans, 0.85 of the sans base |
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

## Token Ownership

KPress owns the regular sans weight in `--kpress-font-weight-sans-regular`. Its font
generators read that token to produce matching math metrics and print faces; the paper’s
CSS and print instancer use the same source.
Change that token and regenerate the fonts, metrics, and prepared page together.
The loading and generation contract is documented in the
[KPress font and math architecture](../../../vendor/kpress/docs/project/architecture/arch-2026-09-08-font-and-math-loading.md).

The local typography block owns the sans/prose size ratio and the paper’s medium and
bold weights. `--paper-font-size-support` sizes figure labels; `--paper-font-size-note`
and `--paper-note-inset` size and inset captions and endnotes.
They share `--paper-support-color` and `--paper-support-leading`. Resolve the sans base
once in the prose scope: nested sans components must inherit the resolved size without
multiplying the ratio again.
Apply print overrides at the same scopes as KPress theme declarations, including
footnote popovers.

The paper’s role sizes, heading scale, and reading measure remain explicit local
choices. Certificate selection, interactive panels, and diagram geometry stay with the
explainer.

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
Math uses KPress’s matching serif or sans composite and metrics.
The outer math em follows its surrounding text in inline and display formulas; KaTeX
still controls the internal sizes of scripts and nested expressions.
Code uses Planetaire Mono Text at KPress’s calibrated monospace size.

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
uv run --frozen --all-extras --group dev python -m devtools.render_explainer --prepare-math
uv run --frozen --all-extras --group dev pytest tests/test_explainer.py -q
uv run --frozen --all-extras --group dev python -m devtools.inspect_explainer_typography --check-supporting --check-math --theme light
uv run --frozen --all-extras --group dev python -m devtools.inspect_explainer_typography --check-supporting --check-math --theme dark --width 390
uv run --frozen --all-extras --group dev python -m devtools.check_print_layout
uv run --frozen --all-extras --group dev python -m devtools.render_explainer_pdf --update
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

The linear-program display is reflowed within the print column.
`check_print_layout` guards its width so an overflowing equation cannot silently shrink
the whole PDF page.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
