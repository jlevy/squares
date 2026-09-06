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
| Figure text, captions, and footnotes | 18.05px | About 12.0333pt | Shared sans size: 0.95 of the sans base |
| Colophon | 16.15px | About 10.7667pt | Sans, 0.85 of the sans base |
| Sans weights | 410 regular, 550 medium, 680 bold | Same | Preserve serif weight settings |
| Supporting text color | KPress gray text role | Solid black | Preserve semantic diagram and status colors |

The shared figure size applies to readable labels and explanatory text.
Captions and footnotes use the same size so their relationship to the prose remains
consistent. Screen theme colors still apply in both light and dark mode.
Print uses a white ground and black prose, labels, captions, and notes; semantic diagram
colors retain their meaning.
Links have no persistent underline on the web or in print.
Links within supporting text inherit its gray or black; links in the main prose retain
the accent color. Caption leads use medium weight to distinguish the figure number
without changing its size or color.

## Token Ownership

Keep the sans ratio, shared supporting-text size, and weight values together in the
local typography block.
`--paper-font-size-support`, `--paper-support-color`, and `--paper-support-leading`
define the shared role; components consume it instead of setting their own nearby sizes.
Resolve the sans base once in the prose scope: nested sans components must inherit the
resolved size without multiplying the ratio again.
Apply print overrides at the same scopes as KPress theme declarations, including
footnote popovers.

The serif/sans size ratio, common supporting-text role, and independent sans weights are
candidates for KPress tokens after web and print verification.
The paper’s heading scale and reading measure remain explicit local choices.
Certificate selection, interactive panels, and diagram geometry stay with the explainer.

An SVG’s declared font size is in its own coordinate system.
Audit the effective size after its `viewBox` and rendered dimensions scale the drawing;
matching a CSS number alone does not match the caption.
The shared script compensates font sizes using the SVG transform and updates them on
resize and when entering or leaving print.
Label rows leave room for the resulting text size.
On narrow screens, diagrams scroll horizontally rather than shrinking their labels.
Long figure notes remain HTML so they can wrap.

The 100-packing atlas is an explicit exception: it is a standalone SVG with its own
dense grid, title, and labels.
Enlarging every internal label to the caption size would obscure its cells.
Its caption uses the shared role; the linked full-size PDF provides the detailed view.
Math retains KaTeX’s fonts and optical sizing, and code retains its monospace face.

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
uv run --frozen --all-extras --group dev python -m devtools.render_explainer
uv run --frozen --all-extras --group dev pytest tests/test_explainer.py -q
uv run --frozen --all-extras --group dev python -m devtools.inspect_explainer_typography --check-supporting --theme light
uv run --frozen --all-extras --group dev python -m devtools.inspect_explainer_typography --check-supporting --theme dark --width 390
uv run --frozen --all-extras --group dev python -m devtools.check_print_layout
uv run --frozen --all-extras --group dev python -m devtools.render_explainer_pdf --update
```

The typography check compares ordinary supporting text with the caption’s family,
effective size and color, and reports overlapping SVG label boxes and persistent link
underlining. It excludes math, code, and semantic status labels from equality checks.
Inspect the rendered page in both themes and the exported PDF. Compare effective
figure-label sizes with captions and footnotes, and check page breaks after changing
type size. The generated editions live in `packing/site/`; publication and broader
validation requirements are in [development.md](../../../development.md).

An existing print limitation remains: the long linear-program equation exceeds the
nominal text column and can trigger Chromium’s page scaling.
Reflowing that display and checking absolute PDF font sizes is a follow-up to the shared
typography role; figure labels and captions must continue to match when it is addressed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
