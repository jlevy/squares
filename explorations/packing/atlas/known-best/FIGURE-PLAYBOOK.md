# Composite figure playbook

How [`known-best-1-100.svg`](known-best-1-100.svg) is built, where every fact on it
comes from, and what to do when the data or the renderer changes.
Everything under `atlas/known-best/` is generated; nothing here is edited by hand, the
figure and its exports included.

## Rebuild it

```bash
uv run --frozen --all-extras --group dev python -m devtools.build_known_best_atlas --update
```

That rebuilds 100 witnesses, 100 individual renderings, the composite SVG, its PNG
preview and its PDF, the manifest, and the frontier back-links.
It is idempotent: a second run changes nothing.
Then confirm nothing drifted:

```bash
uv run --frozen --all-extras --group dev packing-validate --only "known-best"
```

## What flows in

```
frontier/n-NNN.md ────────────► status, side value, exactness, degree, rigid flag
resources/web/ ───────────────► the retained sources those fields were read from
witnesses/known-best/*.yaml ──► square geometry, and only geometry
src/sqpack/render/color.py ───► hue from angle class, shade from contact count
src/sqpack/render/style.py ───► the twenty base hues
devtools/build_known_best_atlas.py ──► layout, badges, legend, footer
```

## The rule that matters

The figure reports **what is known about the packing**, never **how this repository
happens to store it**.

That distinction was learned the hard way.
`claim.assurance` in the witness files names the provenance of one record’s coordinates,
not the standing of the mathematics.
An earlier cut of this figure read it as the latter and badged `n = 5` — proved optimal,
side `2 + √2/2` — as “numerically verified”, because that witness stores decimals.
Anything sourced from the witness layer is about our records.
Facts about the mathematics live in `frontier/n-NNN.md`.

## Field by field

| Shown | Source | Verify by |
| --- | --- | --- |
| `s(n) = …` vs `s(n) ≤ …` | `packing.status` (`proved` / `open`) | 35 proved; equality only for those |
| Side value | `reported_upper_bound.value` | Matches the witness side to its stated precision |
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

Absence of `R` means rigidity is **not established**, never that the packing is known
loose. Repairing the field is tracked under epic `think-ych6`.

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
It currently flattens typographic quotes in the document it rewrites, so read `git diff`
and keep only the row that actually changed; see `think-93u2`.

## If you change the palette or the renderer

Color and layout reach past this directory, so rebuild the rest too:

```bash
for m in build_prospective_atlas build_contact_scaffold_atlas \
         render_known_best_contact_overlays render_packing_gallery \
         profile_known_best_chunks census_known_best_chunks; do
  uv run --frozen --all-extras --group dev python -m devtools.$m --update
done
```

Changing the canvas size means three edits, not one: the constants in
`devtools/build_known_best_atlas.py`, the `height` constants in
[`known-best-atlas.schema.yaml`](known-best-atlas.schema.yaml), and the expected
dimensions in `tests/test_known_best_atlas.py`. The schema pins the height deliberately,
so a silent resize fails the gate.

## Staleness cannot pass quietly

Each derived artifact carries a receipt naming the source it was built from:

| Artifact | Receipt | Checked by |
| --- | --- | --- |
| Composite SVG | rebuilt and compared in full | `build_known_best_atlas --check` |
| PNG preview | source SVG sha256 in a tEXt chunk | same |
| PDF export | source SVG sha256 after `%%EOF` | `render_composite_pdf --check` |

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
