# Packing Atlas

The atlas connects retained packing observations and abstract enumeration records to
stable, document-ready views.
Its collections have deliberately different claim semantics:

| Collection | Contents | Claim boundary |
| --- | --- | --- |
| [`atlas.schema.yaml`](atlas.schema.yaml) and [`rendering/`](rendering/README.md) | Typed endpoint observations and explanatory figures indexed by [`manifest.json`](rendering/manifest.json) | A view may expose retained evidence but cannot promote its tier |
| [`known-best/`](known-best/README.md) | One normalized construction and house SVG for every `n = 1..100`, plus separate calibration annotations | Feasible retained constructions; no new optimality or H-044 verdict |
| [`prospective/`](prospective/source-availability-101-324.json) | Complete source-availability map for `n = 101..324` and the license-safe normalized seed | Source corpus only; contact and hypothesis annotations are prohibited |
| [`enumerated/`](enumerated/README.md) | All 11,013 abstract signed-contact orbits at scaffold size five | Incidence labels only; no geometry, realization, feasibility, or packing claim |

Within every collection, data and presentation remain separate.
An atlas row or abstract identity owns typed content; an SVG is a deterministic view of
that content. Drawing an object cleanly cannot turn a candidate into a certificate, a
source listing into geometry, or an abstract contact graph into a packing.

## Examples

![Walter Trump’s exact packing of eleven unit squares.](rendering/trump11-overview.svg)

*A final-state overview for the smallest open case.
Translucent tempered-yellow marks expose its exact contact structure; exact source
expressions remain available in SVG metadata without crowding the page.*

![The exact quotient map of optimal configurations for three unit squares.](n-003-optimal-moduli.svg)

*A different atlas object: the complete proved quotient space, with representative
packings attached to its distinguished strata.*

![The high-precision Kingbird packing of twenty-nine unit squares.](rendering/kingbird29-overview.svg)

*A larger construction whose roughly 100-digit source is numerically checked at 160
decimal digits of working precision and tolerance `1e-80`. It exercises all 20 fixed
cool colors and their deterministic reuse without overstating the retained source as
verified or exact.*

## Add or Regenerate an Example

From `explorations/packing`, inspect and rebuild the current set with:

```bash
uv run --frozen --all-extras --group dev python -m devtools.render_packing_gallery --list
uv run --frozen --all-extras --group dev python -m devtools.render_packing_gallery --update
uv run --frozen --all-extras --group dev python -m devtools.render_packing_gallery --check
```

To add a case, adapt its typed retained source to a `PackingFrame` or
`PackingTrajectory`, add the render and manifest entry in
[`devtools/render_packing_gallery.py`](../devtools/render_packing_gallery.py),
regenerate, and embed the listed artifact in the corresponding `frontier/n-NNN.md` body.
The deterministic SVG gate checks the manifest, documentation links, safe SVG subset,
and retained bytes together.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
