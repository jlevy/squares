# Packing Atlas

The atlas connects retained packing observations to stable, document-ready views.
It has two deliberately separate layers:

- [`atlas.schema.yaml`](atlas.schema.yaml) is the contract for semantic endpoint
  observations and provisional summaries.
- [`rendering/`](rendering/README.md) is the deterministic gallery of explanatory SVGs.
  Its [`manifest.json`](rendering/manifest.json) maps each rendered artifact to a
  frontier case, evidence tier, view, motion and contact semantics, accessible copy, and
  exact generator command.

The separation matters.
An atlas row is scientific data; a figure is a presentation of typed source data.
The renderer may expose evidence already present in its input, but it cannot promote a
candidate to a certificate or make a conjectured minimum proved by drawing it cleanly.

## Examples

![Walter Trump’s exact packing of eleven unit squares.](rendering/trump11-overview.svg)

*A final-state overview for the smallest open case.
Translucent tempered-yellow marks expose its exact contact structure; exact source
expressions remain available in SVG metadata without crowding the page.*

![The exact quotient map of optimal configurations for three unit squares.](n-003-optimal-moduli.svg)

*A different atlas object: the complete proved quotient space, with representative
packings attached to its distinguished strata.*

![The high-precision Kingbird packing of twenty-nine unit squares.](rendering/kingbird29-overview.svg)

*A larger verified numerical construction that exercises all 20 fixed cool colors and
their deterministic reuse without overstating the retained source as exact.*

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
