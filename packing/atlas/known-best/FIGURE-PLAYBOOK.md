# Composite figure playbook

How [`known-best-1-100.svg`](known-best-1-100.svg) and
[`known-best-1-324.svg`](known-best-1-324.svg) are built, where every fact on them comes
from, and what to do when the data or the renderer changes.
Everything on both is decided the same way; where they differ is the encoding, and
[“The two composites”](#the-two-composites) is where that is measured.
Everything under `atlas/known-best/` is generated; nothing here is edited by hand, the
figures and their exports included.

## Rebuild it

```bash
uv run --frozen --all-extras --group dev python -m devtools.build_known_best_atlas --update
```

That rebuilds 324 witnesses, 324 individual renderings, both composite SVGs, every PNG
raster and both PDFs, the manifest, and the frontier back-links.
Each composite’s exports are one family: a single run draws all of them from the same
SVG, and a single `--check` reports every one that has fallen behind.
It is idempotent: a second run changes nothing.
It also takes about eleven minutes at 324 cases, nearly all of it in the witnesses’
feasibility receipts rather than in the drawing.
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

Today that reports 287 degrees known over the corpus, 36 stored upstream and **251
derived here** — each one a fact the corpus could hold and does not.

## The rule that matters

The figure reports **what is known about the packing**, never **how this repository
happens to store it**.

That distinction was learned the hard way.
`claim.coordinate_provenance` in the witness files — named `claim.assurance` until this
defect was fixed — names the provenance of one record’s coordinates, not the standing of
the mathematics.
An earlier cut of this figure read it as the latter and badged `n = 5` —
proved optimal, side `2 + √2/2` — as “numerically verified”, because that witness stores
decimals. Anything sourced from the witness layer is about our records.
Facts about the mathematics live in `frontier/n-NNN.md`.

## Field by field

Every count in the third column is the figure’s hundred, which is also what its legend
prints; the poster counts the same fields over its own 324 cases and prints those
instead, so the two legends differ while the rules behind them do not.

| Shown | Source | Verify by |
| --- | --- | --- |
| `s(n) = …` vs `s(n) ≤ …` | `packing.status` (`proved` / `open`) | 35 proved; equality only for those |
| Side value | `reported_upper_bound.value` | Matches the witness side to its stated precision |
| `s(n) ≥ …` second line | `verified_lower_bound.value`, shown where `status` is `open` | 65 lines; cut off rather than rounded, so the printed bound stays true |
| ★ lower bound first proved here | `verified_lower_bound.evidence` cites first-party evidence the register scores as novel | 7 cases: `n = 11, 12, 17, 18, 19, 20, 21`; drawn as a polygon, since no figure font carries a star |
| `=` exact value known | `exact_form`, else `minimal_polynomial` or `algebraic_degree` | Evaluate the form, compare against the witness side |
| `≈` only known numerically | none of the three present | 5 cases: `n = 29, 55, 68, 69, 71` |
| `deg d` | `algebraic_degree` | Present for 11 cases; absence is not a claim of low degree |
| `R` rigidity established | derived, see below | Perfect squares by exact tiling, plus the first-party arguments at `n = 5` and `n = 11`; a catalogue annotation is shown muted and not counted |
| Hue | angle class of the square | Right angles pinned to hue 0, 45° tilts to hue 1 |
| Shade | full-side contact count, 4 down to 0 | `_contact_shade` in `src/sqpack/render/color.py` |

### Exactness

`exact_form` and `minimal_polynomial` are **hand-transcribed** from
`resources/web/kingbird-squares-in-squares.md`. That catalogue prints a radical inline
as `$s = <radical> = \Nn{<decimal>}$`, or a locked degree as
`$s = {}^{d}🔒 = \Nn{<decimal>}$` followed by the polynomial.
Match an entry to an `n` by its printed decimal, never by position.

Two traps, both of which have already bitten:

- One entry, `n = 54`, is rendered as a multi-line `\begin{aligned}` block instead of
  the single-line form.
  It was missed on the first pass and recorded as having no exact form, which put a
  wrong badge in a published figure.
- Nothing re-reads these fields from the source.
  `devtools/check_source_coverage.py` parses only the decimal, so a second miss would
  also be invisible. Tracked in `think-k5z2`.

A failed integer-relation search over a retained side is **not** evidence that a value
is not algebraic. Retained sides run 30–100 digits, and PSLQ needs roughly
`degree × coefficient-digits`; the search that finds nothing for `n = 29` also finds
nothing for `n = 51`, whose degree-12 polynomial is recorded.

### Rigidity

Do not read `reported_upper_bound.rigid` as a boolean about the world.
It is non-null exactly where `catalogue_pictured` is true, so `false` means “the
catalogue pictured this and did not write Rigid”, not “this packing has play”.
Taken literally it says `n = 1` is not rigid, which is false: one unit square exactly
fills a `1 × 1` container.

The upstream catalogue is not at fault.
It annotates rigidity for four packings, is silent otherwise, and never asserts
non-rigidity anywhere.
The collapse of silence into `false` is ours.

So the figure derives the badge from two sound sources instead:

1. `n` a perfect square.
   The `k²` unit squares exactly tile a `k × k` container, leaving no slack, so nothing
   can move. Ten cases on the figure, `k = 1..10`; eighteen on the poster, which adds
   `k = 11..18` — `n = 121, 144, 169, 196, 225, 256, 289, 324`. The derivation is the
   argument, not a list: it reads each record’s own `rigidity` block, so a new perfect
   square earns the badge by tiling rather than by being added to a set.
2. The catalogue annotates “Rigid”: `n = 5, 11, 28, 40`, at lines 44, 80, 163 and 224,
   each identified by the side value printed above it.

Absence of `R` on the figure means rigidity is **not established by a source or by the
tiling argument**. It no longer means the corpus is silent about the packing.
`frontier/n-NNN.md` now carries a first-party `rigidity` block for every `n`, written by
`devtools/assess_frontier_rigidity.py` from two sound arguments:

- **296 records are positively NOT rigid** across the corpus, 84 of them in the figure’s
  hundred. The translation escape screen exhibits a square, a direction and an exact
  distance, which is a certificate of motion.
  The smallest certified slide is `2.03e-4` against witness coordinates carrying 28 or
  more digits, so none of these is numerical noise.
- **Eighteen are rigid by exact tiling**, the same eighteen the poster badges and the
  first ten of which the figure badges.
- **Eight are `undetermined`**, which is a result rather than an absence: `n = 28, 40`
  because the screen finds no single-square translation but cannot rule out rotation or
  coordinated motion, and `n = 68, 69, 103, 105, 110, 131` because their witness
  geometry is excluded.
- **Two are the assessment tool’s own refusals**, `n = 5` and `n = 11`, which it leaves
  to a stronger argument and which now carry one.
  `n = 5` held `undetermined` on a first-party exact argument rather than on a screen
  miss —
  [`X-007`](../../campaign/explorations/X-007-the-n5-optimum-flexes-once-and-that-once-is-shut.md)
  settles its infinitesimal cone exactly and refuses the one free direction at second
  order — and second-order rigidity is not local rigidity, so it stayed there until
  `T-014` wrote the missing step out.

The screen’s asymmetry is why the figure derives its badge from the record rather than
from the screen. A hit proves non-rigidity; a miss proves nothing.

**The badge is two badges, and that is [`D-385`](../../../defects.md).** It used to be
one: a solid `R` earned by `n` alone, from a hard-coded set of the four packings the
catalogue annotates, which rendered a source’s word identically to an exact tiling
argument — the field split failing to reach the figure.
Now `established` means the record’s own `rigidity` block says `locally-rigid`, and
nothing else does: **twelve** solid badges on the figure and **twenty** on the poster —
the tilings plus `n = 11`’s own `verified` argument and `n = 5`’s, both of which the old
rule credited to Kingbird.
The catalogue’s annotation is still shown, because dropping it would lose a fact the
corpus holds, but as a **muted** `R` on a `not-established` entry with its own legend
line and its own total: `n = 28, 40`.

`n = 5` is why the distinction is worth the second glyph, and it is also why the glyph
is not decoration.
[`X-007`](../../campaign/explorations/X-007-the-n5-optimum-flexes-once-and-that-once-is-shut.md)
established more about it than the catalogue ever said and still not local rigidity, so
it held the muted badge for three days while carrying first-party evidence in the
frontier. It moved to a solid badge on 2026-09-03 only when the missing step was written
out, checked against a complete local accounting, independently reviewed and registered
as `T-014` — on the proof, never on the annotation.

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

The middle step refreshes generated tables that also quote frontier values.
It rewrites only the rows whose content actually changed, so a run over an unchanged
tree leaves an empty diff and the formatter’s typography survives in the rows it does
not touch.

## If you change the palette or the renderer

Color and layout reach past this directory, so rebuild the rest too:

```bash
for m in build_contact_scaffold_atlas \
         render_known_best_contact_overlays render_packing_gallery \
         profile_known_best_chunks census_known_best_chunks; do
  uv run --frozen --all-extras --group dev python -m devtools.$m --update
done
```

Changing the canvas size means four edits, not one: the card metrics in
`devtools/build_known_best_atlas.py`, the pinned dimensions in
[`known-best-atlas.schema.yaml`](known-best-atlas.schema.yaml), the expected dimensions
in `tests/test_known_best_atlas.py`, and the `width` and `height` on the `img` tag in
`devtools/templates/explainer-article.md`, which reserves the space the page scrolls
past. The card metrics are shared, so an edit to them moves both composites; the schema
pins each canvas under its own stem, so a silent resize of either fails the gate.
The last three pin every raster each composite publishes — for the figure, the 1x
preview, the 2x export and the link-preview crop — so a canvas change that moves one and
not the others is caught rather than shipped.
Only the builder needs a single edit: each raster derives its size from the canvas
constants and its own whole-number scale.

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

The PDF uses a receipt rather than a byte comparison because cairo assigns font-subset
tags per process, so two runs of identical input are not byte-identical across
processes.

Two behavioral tests hold the claims themselves: right angles and 45° tilts take hues 0
and 1 across the whole atlas, and unpinned classes are ordered by descending class size.

## Fonts

The figure sets Helvetica with Arial as the metric-compatible fallback.
No webfont is referenced and nothing is fetched at render time.
Helvetica offers regular and bold and nothing between: any weight from 560 up resolves
to bold, so asking for a semibold silently yields bold.
Small card labels stay regular and earn legibility from a darker gray instead.

Legend rows are centered with the Helvetica advance-width table in the builder, not a
per-character estimate.
A uniform estimate cannot center mixed strings; it put the two rows 107px and 189px off
center, in opposite directions.

## The two composites

The corpus publishes two figures of itself: the 10-by-10 **figure** of `n = 1..100`, and
the 18-by-18 **poster** of the whole corpus, `n = 1..324`. They share a builder, a
record, a palette and a card design; 324 falls into 18 columns of 18 with no short row,
which is why the poster stops where the catalogue’s completeness statement does.
The figure is untouched by everything below, byte for byte.

### A composite is a specification

`KNOWN_BEST_COMPOSITES` in `src/sqpack/known_best.py` is the whole of it.
Four fields say what a figure draws — first `n`, last `n`, columns, filename stem — and
the rest of the geometry follows: rows, the canvas, the legend and footer baselines, the
layout string, the manifest record and the figure record’s own legend totals.
Nothing is absolute, which is what a second entry demonstrated: eighteen columns is
eight more column pitches of width, and eighteen rows moves the legend and all three
footer lines by eight row pitches.

|  | figure | poster |
| --- | --- | --- |
| Cases | `n = 1..100` | `n = 1..324` |
| Grid | 10 by 10 | 18 by 18 |
| Canvas | 2400 × 2896 units | 4224 × 4912 units |
| Squares drawn | 5,050 | 52,650 |
| Rasters | 1x, 2x, link-preview card | 1x |
| PDF page | 25 × 30.17 in | 44 × 51.17 in |

The remaining fields are the decisions a figure of another size has to make: which
rasters it publishes, whether it publishes a link-preview crop, and what it may leave
out of a square to stay inside a byte budget.
The poster publishes one raster, and the reason is measured rather than assumed: its 1x
export is 2,369,558 bytes, a 2x of the same drawing is 5,055,264 at 83 megapixels, and
the PDF carries that detail at any zoom for 491,026. The figure’s 3x was rejected at
2,150,682 on exactly that argument, so a poster 2x at more than twice the price is not a
close call. It publishes no link-preview card either: the card is one page’s unfurl, and
that page already has one.

The accessible `<title>` and `<desc>` are the one thing a specification cannot compute —
nothing spells “one through three hundred twenty-four” from two integers — so they are
written per stem in `SUMMARY_PROSE`, and a composite with no entry there refuses to
render rather than borrowing another figure’s words.

### The byte budget, measured

The house encoding spends about 460 bytes on every square the figure draws: the
`points`, the fill, a stroke repeated on each polygon, and six per-square `data-*` facts
that let a reader interrogate the drawing without the record beside it.
On the poster it would spend 490, because a wider canvas and larger grids make each
coordinate longer. At 5,050 squares that is a 2.3 MB file.
At 52,650 it is 24.6 MB, which is not a file to commit, so the poster spends less per
square — and what it stops spending was chosen against measurements rather than guessed.
`build_known_best_atlas --report` prints them for whatever is committed:

```bash
uv run --frozen --all-extras --group dev python -m devtools.build_known_best_atlas --report
```

Each lever below was measured on its own and in combination, on the same 52,650 squares:

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
whose container is 158 units wide and whose PDF page is 44 inches.

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
  on the 44-inch page.

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
onto the 18 unpinned slots, and the corpus already asks for 106 angle classes in one
frame (`n = 273`) where the first hundred asked for 14. Feeding a class count to
`square_fill_palette` would leave its closest pair 0.04 degrees apart, so the wrap is
the answer and `tests/test_render_colors.py` measures both halves of that.
And the corpus, not the drawing, is the constraint: a card needs a frontier record whose
facts are sourced to the same standard as the rest, which is why nothing above `n = 324`
is drawn — no source makes a completeness claim there.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
