# Composite figure playbook

How [`known-best-1-100.svg`](known-best-1-100.svg) is built, where every fact on it
comes from, and what to do when the data or the renderer changes.
Everything under `atlas/known-best/` is generated; nothing here is edited by hand, the
figure and its exports included.

## Rebuild it

```bash
uv run --frozen --all-extras --group dev python -m devtools.build_known_best_atlas --update
```

That rebuilds 100 witnesses, 100 individual renderings, the composite SVG, both of its
PNG rasters and its PDF, the manifest, and the frontier back-links.
The exports are one family: a single run draws all four from the same SVG, and a single
`--check` reports every one of them that has fallen behind.
It is idempotent: a second run changes nothing.
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

Today that reports 95 degrees known, 11 stored upstream and **84 derived here** — each
one a fact the corpus could hold and does not.

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

| Shown | Source | Verify by |
| --- | --- | --- |
| `s(n) = …` vs `s(n) ≤ …` | `packing.status` (`proved` / `open`) | 35 proved; equality only for those |
| Side value | `reported_upper_bound.value` | Matches the witness side to its stated precision |
| `s(n) ≥ …` second line | `verified_lower_bound.value`, shown where `status` is `open` | 65 lines; cut off rather than rounded, so the printed bound stays true |
| ★ lower bound first proved here | `verified_lower_bound.evidence` cites first-party evidence the register scores as novel | 7 cases: `n = 11, 12, 17, 18, 19, 20, 21`; drawn as a polygon, since no figure font carries a star |
| `=` exact value known | `exact_form`, else `minimal_polynomial` or `algebraic_degree` | Evaluate the form, compare against the witness side |
| `≈` only known numerically | none of the three present | 5 cases: `n = 29, 55, 68, 69, 71` |
| `deg d` | `algebraic_degree` | Present for 11 cases; absence is not a claim of low degree |
| `R` rigidity established | derived, see below | Perfect squares by area; the rest from catalogue annotation |
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
   can move. Ten cases.
2. The catalogue annotates “Rigid”: `n = 5, 11, 28, 40`, at lines 44, 80, 163 and 224,
   each identified by the side value printed above it.

Absence of `R` on the figure means rigidity is **not established by a source or by the
tiling argument**. It no longer means the corpus is silent about the packing.
`frontier/n-NNN.md` now carries a first-party `rigidity` block for every `n`, written by
`devtools/assess_frontier_rigidity.py` from two sound arguments:

- **84 records are positively NOT rigid.** The translation escape screen exhibits a
  square, a direction and an exact distance, which is a certificate of motion.
  The smallest certified slide is `2.03e-4` against witness coordinates carrying 28 or
  more digits, so none of these is numerical noise.
- **Ten are rigid by exact tiling**, the same ten the figure badges.
- **Five are `undetermined`**, which is a result rather than an absence: `n = 28, 40`
  because the screen finds no single-square translation but cannot rule out rotation or
  coordinated motion, `n = 68, 69` because their witness geometry is excluded, and
  `n = 5` for a different reason from any of them.
  `n = 5` reads `undetermined` on a first-party exact argument rather than on a screen
  miss —
  [`X-007`](../../campaign/explorations/X-007-the-n5-optimum-flexes-once-and-that-once-is-shut.md)
  settles its infinitesimal cone exactly and refuses the one free direction at second
  order — and the property stays where it is only because second-order rigidity is not
  local rigidity and the enum has no word for it.
  The assessment tool no longer owns that record, so `n = 5` and `n = 11` are the two it
  leaves to a stronger argument.

The screen’s asymmetry is why the figure derives its badge from the record rather than
from the screen. A hit proves non-rigidity; a miss proves nothing.

**The badge is two badges, and that is [`D-385`](../../../defects.md).** It used to be
one: a solid `R` earned by `n` alone, from a hard-coded set of the four packings the
catalogue annotates, which rendered a source’s word identically to an exact tiling
argument — the field split failing to reach the figure.
Now `established` means the record’s own `rigidity` block says `locally-rigid`, and
nothing else does: **twelve** solid badges, the ten tilings plus `n = 11`’s own
`verified` argument and `n = 5`’s, both of which the old rule credited to Kingbird.
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
for m in build_prospective_atlas build_contact_scaffold_atlas \
         render_known_best_contact_overlays render_packing_gallery \
         profile_known_best_chunks census_known_best_chunks; do
  uv run --frozen --all-extras --group dev python -m devtools.$m --update
done
```

Changing the canvas size means four edits, not one: the constants in
`devtools/build_known_best_atlas.py`, the `height` constants in
[`known-best-atlas.schema.yaml`](known-best-atlas.schema.yaml), the expected dimensions
in `tests/test_known_best_atlas.py`, and the `width` and `height` on the `img` tag in
`devtools/templates/explainer-article.md`, which reserves the space the page scrolls
past. The schema pins the height deliberately, so a silent resize fails the gate.
The last three now pin both rasters, the 1x preview and the 2x export, so a canvas
change that moves one and not the other is caught rather than shipped.
Only the builder needs a single edit: each raster derives its size from the canvas
constants and its own whole-number scale.

## Staleness cannot pass quietly

Each derived artifact carries a receipt naming the source it was built from:

| Artifact | Receipt | Checked by |
| --- | --- | --- |
| Composite SVG | rebuilt and compared in full | `build_known_best_atlas --check` |
| PNG preview, 1x | source SVG sha256 in a tEXt chunk | same |
| PNG export, 2x | source SVG sha256 in a tEXt chunk | same |
| PDF export | source SVG sha256 after `%%EOF` | same, and `render_composite_pdf --check` |

All four receipts are the digest of one SVG, which is what makes “the rasters match the
PDF” checkable rather than asserted: two rasterisers of one drawing differ only in how
they antialias an edge, whereas two drawings differ in what they show.

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

## Extending to n = 1..200

The drawing is not the constraint; the corpus is.
In order:

1. Extend the frontier corpus past `n = 100`. `atlas/prospective/` already seeds
   `n = 101..324` from a source map, but prospective records carry no `status`,
   `exact_form` or `rigid`, so every column in the table above needs populating before a
   card can be honest.
2. Re-run the transcription against the catalogue for the new range, with the two traps
   above in mind. Do this only after `think-k5z2` lands, so a miss is caught rather than
   shipped.
3. Widen the palette. It holds 20 hues, and `_hue_slots` extends beyond that by
   farthest-point separation, but the pinned hues 0 and 1 and the minimum separation
   both need rechecking at the new count.
4. Re-lay the grid. `SUMMARY_COLUMNS`, `SUMMARY_ROWS` and the canvas height are
   constants; 200 cards at ten columns doubles the height, and the legend and footer
   baselines are absolute.
5. Confirm the perfect-square rigidity derivation still covers `k = 11..14`, and that no
   new case is silently badged from the unreliable stored flag.

The honest constraint is step 1. The drawing can hold 200 cards as soon as there are 200
cases whose facts are sourced to the same standard as the first hundred.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
