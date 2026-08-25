# Deterministic SVG Gallery

This directory retains the packing renderer’s document-oriented known answers.
The SVG source is the golden artifact: `tools/check_svg_rendering.py --check` rebuilds
each figure in fresh processes, validates the safe subset, and compares bytes.

## Gallery

### `n = 3`: exact moduli

![The exact quotient map of optimal configurations for three unit squares.](../n-003-optimal-moduli.svg)

Two labelled cycles reduce to one quotient interval, with representative packings at its
distinguished strata.
This proved-optimum map is also the non-packing-layout known-answer control for the
shared SVG spine.

### `n = 5`: certified trajectory

![The final frame of the certified exact five-square trajectory.](n5-exact-face-trajectory.svg)

The animated export follows endpoint A, the exact midpoint, and endpoint B.
Reduced-motion and non-CSS viewers show endpoint B.

### `n = 10`: numerical comparison

![A perturbed Göbel ten-square source beside its returned quench endpoint.](gobel10-source-return-comparison.svg)

A retained source perturbation and the endpoint returned by the deterministic quench
share one geometric scale.
The source event is candidate evidence, not an optimality certificate.

### `n = 11`: exact construction overview

![Walter Trump’s exact packing of eleven unit squares.](trump11-overview.svg)

Six axis-aligned squares surround a five-square block tilted at an algebraic angle near
`40.18°`. The figure carries certified-upper-bound evidence and does not call the open
case solved.

## Visualization Levels

The renderer exposes three optional levels through `RenderSpec` and
`tools/render_packing_svg.py`:

- `overview` draws one clean final packing and an evidence-qualified side label
- `comparison` uses one shared geometric scale for the start and final frames
- `trajectory` adds one-pass CSS motion while retaining the final frame as the
  underlying static SVG

Annotations are independent of the view.
`minimal` is suitable for ordinary documents, `numeric` adds projected values, and
`exact` retains source expressions in namespaced metadata and adjacent XML comments.
A binary64 source remains identified as binary64 even in an exact-annotation export.

## Command-Line Use

List, regenerate, or byte-check the complete discoverable gallery from the exploration
root:

```bash
uv run --frozen python tools/render_packing_gallery.py --list
uv run --frozen python tools/render_packing_gallery.py --update
uv run --frozen python tools/render_packing_gallery.py --check
```

[`manifest.json`](manifest.json) is the stable discovery layer for documentation and
future atlas consumers.
It records each example’s artifact, matching frontier case, evidence tier, view, motion
support, accessible copy, and standalone generator command.

Render the exact Trump construction:

```bash
uv run --frozen python tools/render_packing_svg.py builtin trump11 \
  --annotations exact --output atlas/trump11-exact.svg
```

Render a retained `BasinEvent/v3` without converting JSON decimals through binary64:

```bash
uv run --frozen python tools/render_packing_svg.py event result.jsonl \
  --event-id EVENT_ID --view comparison --output atlas/event-comparison.svg
```

Render the certified five-square trajectory:

```bash
uv run --frozen python tools/render_packing_svg.py n5-face \
  --view trajectory --output atlas/n5-face.svg
```

Invalid source selection, evidence, geometry, comments, references, or motion exits
nonzero before the atomic output boundary replaces a destination.

## Measurements and Portability Review

Measurements on 2026-08-24 used Python 3.14.6 on macOS 26.5.2 arm64. Twenty in-process
rebuilds of the three packing figures had a median total latency of 195.259 ms and a
minimum of 174.090 ms; the exact number-field fixtures dominate this measurement.
Timing is observed host evidence and is intentionally absent from `metrics.json`.

| Figure | SVG bytes | Quick Look PNG bytes |
| --- | ---: | ---: |
| Exact `n = 3` moduli | 14,204 | 85,892 |
| Trump `n = 11` overview | 5,411 | 60,563 |
| Göbel `n = 10` comparison | 9,583 | 37,754 |
| Exact `n = 5` trajectory | 4,631 | 36,361 |

Quick Look produced all four 900 px thumbnails, including the final-state rendering of
the animated figure.
Its square-thumbnail mode scales wide SVGs to fill and therefore crops the sides of the
comparison and moduli figures; those thumbnails are conversion smoke tests, not layout
evidence. A fit-preserving `sips` document conversion rendered the complete declared
viewports at `1200×900`, `960×680`, `1280×680`, and `960×680`. The complete gallery was
inspected at document and screen scale; the explicit fills, strokes, labels, and
final-state attributes survive a renderer that ignores CSS animation.
The focused checker also proves that both comparison containers lie inside the declared
viewport.

Raster screenshots remain a manual QA aid, not a golden gate.
No pinned `resvg` binary or pinned font bundle is present.
The available ImageMagick path failed while resolving a mutable user Arial font, which
is exactly the environmental input a deterministic raster gate must exclude.
Adopt raster goldens only with a pinned renderer, checked font inputs,
`--skip-system-fonts`, a fixed viewport, and an explicit pixel-difference policy.
The current Unicode captions and exact metadata did not justify a MathJax-to-path
adapter or a new runtime dependency.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
