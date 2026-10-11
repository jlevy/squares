# Composite figure playbook

How [`known-best-1-100.svg`](known-best-1-100.svg) and
[`known-best-1-324.svg`](known-best-1-324.svg) are built, where every fact on them comes
from, and what to do when the data or the renderer changes.
Both use one annotation renderer; their layouts and geometry encodings differ, as
[“The two composites”](#the-two-composites) records.
The geometry records, figures and exports under `atlas/known-best/` are generated.
The curated `credit-attributions.json` supplies lower-bound and optimality
acknowledgments with their roles, citations and evidenced chronology.
This playbook and the README document their construction.

## Rebuild it

The data layer and the drawings are updated separately:

```bash
uv run --frozen --all-extras --group dev python -m devtools.build_known_best_atlas --update
uv run --frozen --all-extras --group dev python -m devtools.build_known_best_atlas --update-composites
```

The first rebuilds the data: 324 witnesses, 324 individual renderings, the manifest, and
the frontier back-links.
It takes about eleven minutes at 324 cases, nearly all of it in the witnesses’
feasibility receipts.
Run it when the data changes.

The second redraws both composite SVGs, every PNG raster and both PDFs from the retained
witnesses, in about a minute.
Run it at a version bump, or when you want the figures to show the current data; a data
change does not require it.
Each composite records the data commit and date it was drawn from and may trail the data
until the next version.
Both put the data date before a middle dot and the edition in their diagram-credit
block: the figure uses a footer and the poster its upper-left information block.
[Release assets](../../../development.md#release-assets-are-drawn-at-a-version-bump-or-on-demand)
has the rule, and `--check-composites` lists the cards that trail.
It refuses to draw while the pinned data revision is stale or the data has uncommitted
changes.

For a layout change, refresh the composite geometry in both data records without
rebuilding any witness:

```bash
uv run --frozen --all-extras --group dev python -m devtools.build_known_best_atlas --update-composite-records
```

This command preserves case facts and legend totals and refuses unrelated record changes
before writing either [`manifest.json`](manifest.json) or
[`composite-figure.json`](composite-figure.json).
Those records and their schema contracts are release data.
Commit them, run `python -m devtools.release_pin --update`, commit the new pin, then run
`--update-composites` to draw under that identity.

Each composite’s exports are one family: a single run draws all of them from the same
SVG, and a single `--check` reports every one that has fallen behind.
These commands are idempotent: a second run changes nothing.
Then confirm nothing drifted:

```bash
uv run --frozen --all-extras --group dev packing-validate --only "known-best"
```

## What flows in

```
frontier/n-NNN.md ───┐
resources/web/ ──────┼──► composite-figure.json ──► the drawing
derived here ────────┘         (every claim, with its provenance)

witnesses/known-best/*.yaml ──► square geometry, and only geometry
src/sqpack/render/color.py ───► hue from angle class, shade from contact count
src/sqpack/render/style.py ───► the twenty base hues
```

Every fact the figure states is decided in `devtools/build_composite_figure_data.py`,
written to [`composite-figure.json`](composite-figure.json), and validated against
[`composite-figure.schema.yaml`](composite-figure.schema.yaml).
The renderer reads that record and derives nothing of its own, so the drawing and the
data cannot disagree.

Each fact carries where it came from, because a bare null cannot separate “transcribed”,
“missed in transcription”, “the source is silent” and “nobody knows” — and conflating
those is what put a wrong badge on n=54:

| Provenance | Meaning |
| --- | --- |
| `frontier` | Read from the case’s frontier record |
| `catalogue` | Transcribed here from the retained catalogue, not carried by the frontier |
| `derived` | Computed by this repository from a fact it already holds |
| `absent` | No source on hand supplies it, which is not a claim about mathematics |

To see where the figure knows more than the records do:

```bash
uv run --frozen --all-extras --group dev python -m devtools.build_composite_figure_data --review
```

Today that reports 292 degrees known over the corpus, 45 stored upstream and **247
derived here** — each one a fact the corpus could hold and does not.

## The rule that matters

The figure reports **what is known about the packing**, never **how this repository
happens to store it**.

That distinction was learned the hard way.
`claim.coordinate_provenance` in the witness files — named `claim.assurance` until this
defect was fixed — names the provenance of one record’s coordinates, not the standing of
the mathematics.
An earlier cut of this figure read it as the latter and badged $n = 5$ —
proved optimal, side $2 + \sqrt{2}/2$ — as “numerically verified”, because that witness
stores decimals. Anything sourced from the witness layer is about our records.
Facts about the mathematics live in `frontier/n-NNN.md`.

## Field by field

Unless noted otherwise, counts in the third column describe the figure’s hundred, which
is also what its legend counts.
Each counted legend item includes the depicted total after a slash: 100 for the figure,
324 for the poster. Both composites use the contribution flags described below for their
recent result markers and accents.

| Shown | Source | Verify by |
| --- | --- | --- |
| $s(n) = \ldots$ vs $s(n) \le \ldots$ | `packing.status` (`proved` / `open`) | 45 proved; equality only for those |
| Side value | `reported_upper_bound.value` | Matches the witness side to its stated precision |
| $s(n) \ge \ldots$ second line | `verified_lower_bound.value`, shown where `status` is `open` | 55 lines; cut off rather than rounded, so the printed bound stays true |
| Crimson recent-result accents, since August, 2026 | The canonical contribution flags in `devtools/result_status.py`, using original construction or proof dates and the shared `RECENT_SINCE` cutoff | 81 cases in the figure and 297 in the poster; both accent upper numerals, lower numerals and optimality badges independently |
| `=` exact value known | `exact_form`, else `minimal_polynomial` or `algebraic_degree` | Evaluate the form, compare against the witness side |
| `≈` only known numerically | none of the three present | 3 cases: $n = 29, 55, 71$ |
| $\deg d$ | `algebraic_degree` | Printed for 30 cases with degree at least 2; absence is not a claim of low degree |
| `R` known rigid | `rigidity.known_rigid` from the canonical assessment, see below | 14 cases in the figure and 22 in the poster; the one dark badge preserves source assertions, proof status and dates in metadata |
| Hue | angle class of the square | Right angles pinned to hue 0, 45° tilts to hue 1 |
| Shade | full-side contact count, 4 down to 0 | `_contact_shade` in `src/sqpack/render/color.py` |

### Exactness

`exact_form` and `minimal_polynomial` are **hand-transcribed** from
`resources/web/kingbird-squares-in-squares.md`. That catalogue prints a radical inline
as `$s = <radical> = \Nn{<decimal>}$`, or a locked degree as
`$s = {}^{d}🔒 = \Nn{<decimal>}$` followed by the polynomial.
Match an entry to an $n$ by its printed decimal, never by position.

Two traps, both of which have already bitten:

- One entry, $n = 54$, is rendered as a multi-line `\begin{aligned}` block instead of
  the single-line form.
  It was missed on the first pass and recorded as having no exact form, which put a
  wrong badge in a published figure.
- Nothing re-reads these fields from the source.
  `devtools/check_source_coverage.py` parses only the decimal, so a second miss would
  also be invisible. Tracked in `think-k5z2`.

A failed integer-relation search over a retained side is **not** evidence that a value
is not algebraic. Retained sides run 30–100 digits, and PSLQ needs roughly
`degree × coefficient-digits`; the search that finds nothing for $n = 29$ also finds
nothing for $n = 51$, whose degree-12 polynomial is recorded.

### Rigidity

Do not read `reported_upper_bound.rigid` as a boolean about the world.
It is non-null exactly where `catalogue_pictured` is true, so `false` means “the
catalogue pictured this and did not write Rigid”, not “this packing has play”.
Taken literally it says $n = 1$ is not rigid, which is false: one unit square exactly
fills a $1 \times 1$ container.

The upstream catalogue is not at fault.
It annotates rigidity for four packings, is silent otherwise, and never asserts
non-rigidity anywhere.
The collapse of silence into `false` is ours.

So the figure derives the badge from two sound sources instead:

1. $n$ a perfect square.
   The $k^2$ unit squares exactly tile a $k \times k$ container, leaving no slack, so
   nothing can move. Ten cases on the figure, `k = 1..10`; eighteen on the poster, which
   adds `k = 11..18` — $n = 121, 144, 169, 196, 225, 256, 289, 324$. The derivation is
   the argument, not a list: it reads each record’s own `rigidity` block, so a new
   perfect square earns the badge by tiling rather than by being added to a set.
2. The catalogue annotates “Rigid”: $n = 5, 11, 28, 40$, at lines 44, 80, 163 and 224,
   each identified by the side value printed above it.

Absence of `R` on the figure means rigidity is **not established by a source or by the
tiling argument**. It no longer means the corpus is silent about the packing.
`frontier/n-NNN.md` now carries a first-party `rigidity` block for every $n$, written by
`devtools/assess_frontier_rigidity.py` from two sound arguments:

- **302 records are positively NOT rigid** across the corpus, 86 of them in the figure’s
  hundred. The translation escape screen exhibits a square, a direction and an exact
  distance, which is a certificate of motion.
  In the hundred the smallest certified slide is `2.03e-4` against witness coordinates
  carrying 28 or more digits, except at $n = 68$, whose witness is Francisco Couzo’s
  binary64 pose since 2026-09-29 and whose smallest slide, `8.6e-11`, is still five
  orders of magnitude above that pose’s rounding, and at $n = 69, 83$ and $87$, whose
  witnesses since 2026-10-05 are a binary64 parse of the catalogue’s pictures and whose
  smallest slides, $0.040$, `3.7e-4` and `2.8e-3`, are further above it still; every
  record also has a square that slides at least $0.048$. None of these is numerical
  noise.
- **Eighteen are rigid by exact tiling**, the same eighteen the poster badges and the
  first ten of which the figure badges.
- **Two are `undetermined`**, which is a result rather than an absence: $n = 28, 40$
  because the screen finds no single-square translation but cannot rule out rotation or
  coordinated motion. $n = 69$ was the third, its rendering’s geometry excluded, until
  its record moved on 2026-10-05 to the catalogue’s packing (T-088), which the screen
  reads and finds a translating square in; $n = 68, 103, 105, 110$ and $131$ were
  excluded too until their records moved from UnitSquare renderings to Couzo’s packings
  (T-056).
- **Two are the assessment tool’s own refusals**, $n = 5$ and $n = 11$, which it leaves
  to a stronger argument and which now carry one.
  $n = 5$ held `undetermined` on a first-party exact argument rather than on a screen
  miss —
  [`X-007`](../../campaign/explorations/X-007-the-n5-optimum-flexes-once-and-that-once-is-shut.md)
  settles its infinitesimal cone exactly and refuses the one free direction at second
  order — and second-order rigidity is not local rigidity, so it stayed there until
  `T-014` wrote the missing step out.

The screen’s asymmetry is why the figure derives its badge from the record rather than
from the screen. A hit proves non-rigidity; a miss proves nothing.

**The printed badge is one dark `R` for known rigid.** The canonical assessment combines
a verified local-rigidity result with an explicit catalogue assertion for the matching
displayed witness. Fourteen cases in the figure and twenty-two in the poster carry it:
the exact tilings, the verified arguments at $n = 5, 11$, and the catalogue assertions
at $n = 28, 40$. A numerical screen that finds no motion contributes no positive claim.
Source assertions, verification status, determination dates and recorded dates stay
distinct in the structured metadata, so one icon does not promote an assertion to a
verified proof.

[`D-385`](../../../defects.md) exposed a disagreement between the record and its
rendering. The record still preserves the separate established and catalogue assurance
fields; the current presentation combines their known-rigid positives into one count.
The same-bound alternatives 52b, 149b and 296b do not confer rigidity on the displayed
unsuffixed packings, each of which has a certificate of motion.

$n = 5$ shows why the assurance distinction remains important in metadata, even when the
printed badge is one dark `R`.
[`X-007`](../../campaign/explorations/X-007-the-n5-optimum-flexes-once-and-that-once-is-shut.md)
established more about it than the catalogue ever said and still not local rigidity.
Its earlier rendering held a muted badge for three days while carrying first-party
evidence in the frontier.
Its assurance became verified local rigidity on 2026-09-03 only when the missing step
was written out, checked against a complete local accounting, independently reviewed and
registered as `T-014` — on the proof, never on the annotation.

### Checking one claim by hand

```bash
grep -n "3.87708359002281" resources/web/kingbird-squares-in-squares.md
```

Read the entry above the hit for its exact form, degree or `Rigid.` annotation, then
compare against `frontier/n-011.md`.

## If you change the data

```bash
uv run --frozen --all-extras --group dev python -m devtools.build_known_best_atlas --update
uv run --frozen --all-extras --group dev python -m devtools.render_research_tables
uv run --frozen --all-extras --group dev packing-validate
```

Commit, then re-pin the data revision, which is one line and rebuilds nothing:

```bash
uv run --frozen --all-extras --group dev python -m devtools.release_pin --update
```

The composites are not redrawn for a data change.
The middle step refreshes generated tables that also quote frontier values.
It rewrites only the rows whose content actually changed, so a run over an unchanged
tree leaves an empty diff and the formatter’s typography survives in the rows it does
not touch.

## If you change the palette or the renderer

Redraw the composites (`--update-composites`), since the change is to the drawing.
Color and layout reach past this directory, so rebuild the rest too:

```bash
for m in build_contact_scaffold_atlas \
         render_known_best_contact_overlays render_packing_gallery \
         profile_known_best_chunks census_known_best_chunks; do
  uv run --frozen --all-extras --group dev python -m devtools.$m --update
done
```

Change an arrangement in its `CompositeSpec` in `src/sqpack/known_best.py`. The canvas
follows the number of columns and rows at the shared card scale; changing card metrics
in `devtools/build_known_best_atlas.py` affects both composites.
Update the pinned geometry in
[`known-best-atlas.schema.yaml`](known-best-atlas.schema.yaml) and
[`composite-figure.schema.yaml`](composite-figure.schema.yaml), the expected dimensions
and placements in `tests/test_known_best_atlas.py`, and any consumer that declares the
changed image’s dimensions.
The figure’s consumer is the `img` tag in
`devtools/templates/n11-lower-bounds-explainer-article.md`. Each raster derives its size
from the canvas and its own whole-number scale, and the PDF keeps the SVG’s intrinsic
dimensions. Refresh the layout records, commit and re-pin as above, then redraw the
composites.

## Staleness cannot pass quietly

Each derived artifact carries a receipt naming the source it was built from:

| Artifact | Receipt | Checked by |
| --- | --- | --- |
| Composite SVG | rebuilt and compared in full | `build_known_best_atlas --check` |
| PNG preview, 1x | source SVG sha256 in a tEXt chunk | same |
| PNG export, 2x (figure only) | source SVG sha256 in a tEXt chunk | same |
| Link-preview card (figure only) | source SVG sha256 in a tEXt chunk | same |
| PDF export | source SVG sha256 after `%%EOF` | same, and `render_composite_pdf --check` |

Within one composite every receipt is the digest of one SVG, which is what makes “the
rasters match the PDF” checkable rather than asserted: two rasterisers of one drawing
differ only in how they antialias an edge, whereas two drawings differ in what they
show. Both commands cover both composites, and `render_composite_pdf --check` takes a
`--stem` only to narrow itself to one.

The published downloads are
[`square-packings-100-20261008.pdf`](square-packings-100-20261008.pdf) and
[`square-packings-324-20261008.pdf`](square-packings-324-20261008.pdf).
Their names carry the fixed edition date; the embedded PDF dates still follow the
drawing’s data date.
SVG and PNG filenames retain their internal composite stems.

The PDF uses a receipt rather than a byte comparison because cairo assigns font-subset
tags per process, so two runs of identical input are not byte-identical across
processes.

Two behavioral tests hold the claims themselves: right angles and 45° tilts take hues 0
and 1 across the whole atlas, and unpinned classes are ordered by descending class size.

## Fonts

Both composites use the retained bold and bold italic faces in
`devtools/fonts/atlas-print/`, derived from Liberation Sans 2.1.5 under its OFL license
and renamed SquaresAtlasPrint.
The license and reproduction notes accompany the fonts.
Layout reads advances and ink bounds from those files.
SVGs embed the faces; native PDF and PNG exporters register them for their process and
refuse a substituted face.
Nothing is fetched at render time, and no font is installed system-wide.
Math variables select the explicit italic face; parentheses use the upright face.

Both information blocks use the same renderer and normalized leading of 1.50. Each block
gap is three body-font ems, measured between visible ink rather than baselines, so
capitals, ascenders and descenders do not change the apparent gap.
The title, problem description and all ordinary text are black.
Case numbers remain gray, with red reserved for recent results and colored swatches
retained for tilt and contact keys.

## The two composites

The corpus publishes two figures of itself: the 10-by-10 **figure** of `n = 1..100`, and
the triangular **poster** of the whole corpus, `n = 1..324`. They share a builder, a
record, a palette and a card design.
The poster’s row $k$ holds $n = (k-1)^2 + 1$ through $k^2$. Each whole row is
right-aligned, leaving the upper-left corner free for a left-aligned information block.
Eighteen complete rows cover the catalogue’s range, with thirty-five cards in the final
row; no grid suffix moves onto a second line.
A $k×k$ grid label in the separator marks each row’s first retained regular axis-aligned
grid packing; the count stays in the ordinary card caption.
Dimensions and `GRID` form one line rotated 90 degrees counterclockwise, centered on the
drawing’s height. The renderer measures its retained-font ink and leaves the normal
horizontal inter-box clearance before the first grid outline, refusing a label that
exceeds the separator.
Web views keep the separator and omit these print-only labels.
The threshold comes from the canonical atlas manifest, not a count formula or the
derived regularized view.
Where an irregular prefix precedes the grid suffix, half a drawing width separates the
segments by 79 units horizontally.
All-grid rows receive no added gap and place their marker before the first card.
Both layouts use a 287-unit row pitch and 203-unit column pitch.
Compared with the 214-unit column and 307-unit row pitches, visible horizontal box gaps
decrease by about 20% and the clearance from final annotation ink to the next row
outline decreases by about 25%. The figure keeps its 10-by-10 geometry, card scale and
square encoding.
Triangle bound captions use five decimal places rather than the figure’s
six, with upper bounds rounded upward, lower bounds downward and exact equalities to
nearest. Measured side captions that leave less than five units beside the degree use
four places instead; the renderer refuses a caption that still overlaps.
Current fallback cases are $n = 146, 205, 235, 266, 300$, derived from widths rather
than a case list. The pure shared display helper shortens only the printed numeral; the
canonical values and display records retain their precision.
The retained-label check applies the same formatting policy, so shortening the captions
cannot hide a stale bound.

### A composite is a specification

`KNOWN_BEST_COMPOSITES` in `src/sqpack/known_best.py` is the whole of it.
First $n$, last $n$, columns, filename stem and placement say what a figure draws.
The remaining geometry follows: rows, the canvas, the legend and footer baselines, the
layout string, the manifest record and the figure record’s own legend totals.
The triangle keeps the figure’s card and label sizes.
Its eighteen complete logical rows fit a thirty-five-column envelope.
The longest row’s cards start at $x = 180$; its first drawing starts at $x = 204$. Rows
begin at $y = 120$ and share the figure’s 287-unit pitch, preserving drawing and caption
scale while keeping the annotation clearance consistent.
The canvas includes 120-unit outside clearance for markers and top/bottom margins.
All informational text occupies the upper-left block at $x = 204..2804$, starting at
$y = 120$: title, all badge meanings and counts, hue and shade keys, explanation,
construction, lower-bound and optimality-proof credits and closing project details.
The renderer derives the block’s bottom from the final line’s retained-font ink extent.
The 2600-unit block uses 144-unit title type, 66-unit type for the two-line definition,
and 48-unit type for every subsequent legend, credit and closing line, all in the same
retained body font at weight 700. The first two tilt swatches contain black 90° and 45°
labels, shared with the website and the grid figure.
The information starts at $x = 204$, exactly the left edge of the first drawing in the
final row; card boundaries include additional caption room.
The definition and every body line use normalized leading 1.50. All 48-unit lines have a
72-unit baseline pitch, with clear gaps between sections.
Rendering refuses lines wider than the block, overlapping documentation lines and text
that intersects a card.
The problem definition spans two lines above the legend, breaking after “can”: “The
square packing problem asks for the side $s(n)$ of the smallest square that can hold $n$
unit squares, where the squares are free to rotate but cannot overlap”.
The printed text has no final period.
It sets $s$ and both $n$ tokens in italic with upright parentheses.
The print legend has eight semantic items in two left-aligned columns: four status rows
and four recency, color and degree rows.
The website retains only the shared tilt-color and contact-shade entries.
The final right-column item is the unbadged text “deg is the algebraic degree of that
side length”.
Each counted item includes the number of depicted cases as its denominator.
The four rows share the body’s 72-unit baseline pitch.

Three separate paragraphs begin “Best packings due to”, “Lower bounds due to” and
“Optimality proofs due to”.
Complete canonical names remain intact and appear once within each paragraph.
All recorded construction finders and improvers appear; current lower-bound source
authors receive the second paragraph.
The third paragraph credits mathematical proof authors and explicitly distinguishes
formalization and verification contributions.
Method, prerequisite and historical lower-bound credits remain in the structured
metadata.

Names run from older to newer evidenced result or contribution dates.
Non-overlapping date intervals establish precedence; alphabetical ties leave partial
dates at their original precision.
A later improver’s source does not redate inherited authors, and a retrieval or snapshot
date does not establish publication priority.
Line balancing preserves that order and omits final periods and bracketed citations.
The widest of the three balanced construction-credit lines sets the common width for all
three credit paragraphs; complete names and role prefixes remain indivisible.

Both diagrams use the same full-corpus $n = 1..324$ acknowledgments.
SVG metadata states that credit scope separately from the depicted range and retains the
complete source citations, original statuses, contribution roles and case associations.
The curated input is `credit-attributions.json`; `devtools.atlas_credit_attributions`
validates its roles and chronology without deciding proof acceptance or modifying
scientific facts.

The shared block gap separates the credits from “Diagram by Joshua Levy”.
The data date, a middle dot and the generated edition follow on the next line.
Another block gap precedes exactly “The Squares Project” and “github.com/jlevy/squares”.
Both final lines use the same 48-unit body font, weight 700 and 72-unit pitch as the
legend and credits.
They are plain black text without a hyperlink or PDF annotation; both
start at the information block’s left edge.
The final line’s lower extent determines the block’s bottom; it is not a fixed estimate.
The renderer checks the information rectangle against every card; all text stays inside
the upper-left whitespace.
The poster has no publication subtitle; its closing date is the date of the recorded
data commit. The recent-result accent follows the upper construction, certified lower
bound and optimality proof independently.
A recent proof can color an optimality badge while its older construction’s upper-bound
caption stays neutral.
The shared row model declares separate non-grid and grid segments, kept together on one
line. All rows share the final drawing’s right edge, with 120 units of clearance outside
the card envelope on the right and bottom.
Cards retain their logical row and column identities; physical and logical row counts
both equal eighteen.
SVG metadata records 35 physical columns and 18 physical lines, matching the manifest
and figure record. The same pure segment plan supplies cards, markers, canvas dimensions
and export receipts.
Partial crops allocate only surviving segments, and generic row-major geometry needs no
canonical preflight.
The packing drawings and card captions retain their original scale.

|  | figure | poster |
| --- | --- | --- |
| Cases | `n = 1..100` | `n = 1..324` |
| Arrangement | 10 by 10, row-major | 18 complete right-aligned rows |
| Canvas | 2150 × 3823 units | 7497 × 5361 units |
| Squares drawn | 5,050 | 52,650 |
| Rasters | 1x, 2x, link-preview card | 1x |
| PDF page | 22.40 × 39.82 in | 78.09 × 55.84 in |

The remaining fields are the decisions a figure of another size has to make: which
rasters it publishes, whether it publishes a link-preview crop, and what it may leave
out of a square to stay inside a byte budget.
The poster publishes one raster.
On the rectangular poster, a 2x raster measured 5,055,264 bytes at 83 megapixels, while
its vector PDF measured 491,026 bytes and preserved the detail at any zoom.
The triangle uses a wider canvas and keeps the same export set.
It publishes no link-preview card either: the card is one page’s unfurl, and that page
already has one.

The accessible `<title>` and `<desc>` are the one thing a specification cannot compute —
nothing spells “one through three hundred twenty-four” from two integers — so they are
written per stem in `SUMMARY_PROSE`, and a composite with no entry there refuses to
render rather than borrowing another figure’s words.

### The byte budget, measured

The house encoding spends about 460 bytes on every square the figure draws: the
`points`, the fill, a stroke repeated on each polygon, and six per-square `data-*` facts
that let a reader interrogate the drawing without the record beside it.
On the rectangular poster it spent 490, because a wider canvas and larger grids made
each coordinate longer.
At 5,050 squares that is a 2.3 MB file.
At 52,650 it is 24.6 MB, which is not a file to commit, so the poster spends less per
square — and what it stops spending was chosen against measurements rather than guessed.
`build_known_best_atlas --report` prints them for whatever is committed:

```bash
uv run --frozen --all-extras --group dev python -m devtools.build_known_best_atlas --report
```

Each lever below was measured on its own and in combination on the rectangular poster’s
52,650 squares.
The triangle keeps the same encoding; `--report` gives its current sizes.

| Encoding | SVG bytes | Per square |
| --- | --- | --- |
| The house encoding, as the figure draws it | 25,806,333 | 490.1 |
| No per-square `data-*` | 16,307,720 | 309.7 |
| No `data-*`, stroke shared per card | 13,235,841 | 251.4 |
| No `data-*`, coordinates at 3 decimals | 9,270,230 | 176.1 |
| **All three, which is what ships** | **6,198,351** | **117.7** |
| All three, at 2 decimals | 5,849,278 | 111.1 |

Three things that table settles.
The first lever is the largest single one and still leaves the file at 15.6 MiB, so the
`data-*` attributes were never the whole story.
The two obvious levers together reach 8.84 MiB, which is over the 8 MiB budget, so a
third was needed rather than optional.
And the last row is why the coordinates stop at three decimals rather than two: the
fourth lever buys 5.6 percent and gives up a factor of ten of precision, on a drawing
whose containers are 158 units wide.

What each lever is, and where the fact it drops still lives:

- **No per-square `data-*`.** The hue index, shade index, contact count, orientation and
  angle class of every square are carried per case by
  [`rendering/n-NNN.svg`](rendering/) and by
  [`composite-figure.json`](composite-figure.json), both of which the poster is drawn
  from; the figure keeps them, so the encoding that supports inspection is still
  published. The poster’s `sqpack:profile` metadata records the omission and where to
  read the facts instead, so a copy of the file that travels alone still says what was
  left out of it.
- **One stroke per card, not per polygon.** The colour, width and linejoin are identical
  on all 52,650 squares and cost 61 bytes each where they are repeated.
  They move to a `g` of their own inside the card — not to the card itself, because a
  card also holds text, and text that inherits a stroke is drawn outlined.
- **Coordinates at three decimals.** Emitted with an explicit rounding stated in the
  specification and recorded in the drawing’s metadata, never inherited from the ambient
  decimal context, which is [`D-359`](../../../defects.md).
  A thousandth of a unit is 1/158,000 of a container: below one device dot at 1200 dpi
  at the poster’s intrinsic print scale.

The per-`n` renderings keep all three.
They are where a reader interrogates one packing; the poster is where a reader sees the
corpus.

### What is checked

- `build_known_best_atlas --check` rebuilds both composites and compares them in full,
  then reads every export’s receipt.
- `render_composite_pdf --check` covers every published stem unless `--stem` narrows it.
- [`known-best-atlas.schema.yaml`](known-best-atlas.schema.yaml) and
  [`composite-figure.schema.yaml`](composite-figure.schema.yaml) pin each stem’s grid,
  square count, canvas and raster sizes in a `contains` clause of its own, so a silent
  resize of either fails the gate.
- `tests/test_known_best_atlas.py` asserts the poster’s size against the 8 MiB budget
  and reads all three encoding decisions back off the drawing, and holds the figure’s
  SVG byte-for-byte against the committed copy.

### What a third would take

Another entry in `KNOWN_BEST_COMPOSITES`, a `SUMMARY_PROSE` entry for its stem, a
`contains` clause in each schema, and a literal block in the canvas test.
No new constants, and no second copy of the builder.

Two things are worth knowing before adding one.
The palette does not widen: the renderer holds 20 hues and wraps class registrations
onto the 18 unpinned slots, and the corpus already asks for 52 angle classes in one
frame ($n = 301$) where the first hundred asked for 14. Feeding a class count to
`square_fill_palette` would leave its closest pair 0.43 degrees apart, so the wrap is
the answer and `tests/test_render_colors.py` measures both halves of that.
And the corpus, not the drawing, is the constraint: a card needs a frontier record whose
facts are sourced to the same standard as the rest, which is why nothing above $n = 324$
is drawn — no source makes a completeness claim there.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
