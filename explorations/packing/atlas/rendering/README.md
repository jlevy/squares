# Deterministic SVG Gallery

This directory retains the packing renderer’s document-oriented known answers.
The SVG source is the golden artifact: `python -m devtools.check_svg_rendering --check`
rebuilds each figure in fresh processes, validates the safe subset, and compares bytes.

## Gallery

### `n = 3`: exact moduli

![The exact quotient map of optimal configurations for three unit squares.](../n-003-optimal-moduli.svg)

Two labelled cycles reduce to one quotient interval, with representative packings at its
distinguished strata.
This proved-optimum map is also the non-packing-layout known-answer control for the
shared SVG spine.

### `n = 5`: certified trajectory

![The final frame of the certified exact five-square trajectory.](n5-exact-face-trajectory.svg)

The animated export follows endpoint A, the exact midpoint, and endpoint B. Its
translucent tempered-yellow contact layer describes endpoint B and is revealed only when
the motion arrives there.
Reduced-motion and non-CSS viewers show endpoint B directly.

### `n = 10`: numerical comparison

![A perturbed Göbel ten-square source beside its returned quench endpoint.](gobel10-source-return-comparison.svg)

A retained source perturbation and the endpoint returned by the deterministic quench
share one geometric scale.
The source event is candidate evidence, not an optimality certificate.

### `n = 11`: exact construction overview

![Walter Trump’s exact packing of eleven unit squares.](trump11-overview.svg)

Six axis-aligned squares surround a five-square block tilted at an algebraic angle near
`40.18°`. Translucent tempered-yellow segments show positive-length edge contacts, and
dots in the same highlight color show point contacts.
The figure carries certified-upper-bound evidence and does not call the open case
solved.

### `n = 29`: numerically checked high-precision construction

![The high-precision Kingbird packing of twenty-nine unit squares.](kingbird29-overview.svg)

The retained roughly 100-digit source reconstructs 29 squares.
It is evaluated at 160 decimal digits of working precision and tolerance `1e-80`, and
passes all 406 separating-axis pair checks.
This larger example exercises deterministic reuse of the 20-color sequence.
It remains a numerically checked construction, not a formal verification, exact
certificate, or optimality proof.

## Visualization Levels

The renderer exposes three optional levels through `RenderSpec` and
`devtools.render_packing_svg`:

- `overview` draws one clean final packing and an evidence-qualified side label
- `comparison` uses one shared geometric scale for the start and final frames
- `trajectory` adds one-pass CSS translation while retaining the final frame as the
  underlying static SVG; it rejects angle, shape-offset, or container-size changes that
  the current motion profile cannot represent

Annotations are independent of the view.
`minimal` is suitable for ordinary documents, `numeric` adds projected values, and
`exact` retains source expressions in namespaced metadata and adjacent XML comments.
A binary64 source remains identified as binary64 even in an exact-annotation export.

The fixed 20-color fill sequence spans green, cyan, blue, indigo, and violet.
Its first eleven entries are high-separation anchors for the Trump example; later
entries add deterministic light and dark companions, and assignment repeats by stable
square index. Every square and the container use the same 1.25px pure-black stroke, so
touching shapes do not appear separated by white seams.
Tempered yellow `#e3c64a` is reserved for contact highlights and is not part of the
square palette. The 9px segments and 5.5px-radius dots use 60% opacity, are clipped to
the union of their participating square interiors, and sit above the fills and below the
black outlines. Exact adapters attach certified point and segment contacts in the source
number field; the renderer shows them by default and never infers them from pixels or a
numerical tolerance.
Remove only the visual layer with `--no-contacts`. The contact data remains available to
another `RenderSpec` or an atlas consumer.

## Command-Line Use

List, regenerate, or byte-check the complete discoverable gallery from the exploration
root:

```bash
uv run --frozen --all-extras --group dev python -m devtools.render_packing_gallery --list
uv run --frozen --all-extras --group dev python -m devtools.render_packing_gallery --update
uv run --frozen --all-extras --group dev python -m devtools.render_packing_gallery --check
```

[`manifest.json`](manifest.json) is the stable discovery layer for documentation and
future atlas consumers.
It records each example’s artifact, matching frontier case, evidence tier, view, motion
and contact support, accessible copy, and standalone generator command.
Each rendered file also carries the check kind, method, result, and—when numerical—the
arithmetic, actual precision, rounding, and tolerance in namespaced metadata.

Render the exact Trump construction:

```bash
uv run --frozen --all-extras --group dev python -m devtools.render_packing_svg builtin trump11 \
  --annotations exact --output atlas/trump11-exact.svg
```

For the same geometry with no contact highlight:

```bash
uv run --frozen --all-extras --group dev python -m devtools.render_packing_svg builtin trump11 \
  --no-contacts --output atlas/trump11-geometry.svg
```

Render a retained `BasinEvent/v3` without converting JSON decimals through binary64:

```bash
uv run --frozen --all-extras --group dev python -m devtools.render_packing_svg event result.jsonl \
  --event-id EVENT_ID --view comparison --output atlas/event-comparison.svg
```

Render the certified five-square trajectory:

```bash
uv run --frozen --all-extras --group dev python -m devtools.render_packing_svg n5-face \
  --view trajectory --output atlas/n5-face.svg
```

Invalid source selection, evidence, geometry, comments, references, or motion exits
nonzero before the atomic output boundary replaces a destination.

## Measurements and Portability Review

Initial timing measurements on 2026-08-24 used Python 3.14.6 on macOS 26.5.2 arm64.
Twenty in-process rebuilds of the original three packing figures had a median total
latency of 393.031 ms and a minimum of 378.257 ms; exact verification and contact
extraction dominate this measurement.
Size and conversion measurements were refreshed for the five-figure gallery on
2026-08-25. Timing is observed host evidence and is intentionally absent from
`metrics.json`.

| Figure | SVG bytes | Quick Look PNG bytes |
| --- | ---: | ---: |
| Exact `n = 3` moduli | 14,186 | 85,886 |
| Trump `n = 11` overview | 30,728 | 81,615 |
| Göbel `n = 10` comparison | 18,069 | 38,131 |
| Exact `n = 5` trajectory | 15,648 | 36,774 |
| Kingbird `n = 29` overview | 22,680 | 168,176 |

Quick Look produced all five thumbnails, including the final-state rendering of the
animated figure. Its square-thumbnail mode scales wide SVGs to fill and therefore crops
the sides of the comparison and moduli figures; those thumbnails are conversion smoke
tests, not layout evidence.
A fit-preserving `sips` document conversion rendered the complete declared viewports at
`1200×900`, `960×680`, `1280×680`, and `960×680`. The complete gallery was inspected at
document and screen scale; the pure-black boundaries, cool fills, translucent clipped
contact marks, labels, and final-state attributes survive a renderer that ignores CSS
animation.
The focused checker also proves that both comparison containers lie inside the
declared viewport.

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
