# Feature: Deterministic SVG Rendering Toolkit

**Date:** 2026-08-24 (last updated 2026-08-24)

**Author:** Codex (agent), for the repository owner

**Status:** Draft

## Overview

Build a small packing-specific toolkit that turns typed solution data into clean,
self-contained SVG. The simplest output is a document-ready view of one final packing.
Two optional view levels add a start/final comparison and a trajectory animation.
Mathematical annotation is an independent option, so an overview can remain visually
quiet while the same SVG carries exact formulas, source values, and evidence status for
inspection or machine use.

The toolkit should be exact about its inputs and claims, byte-repeatable as an artifact,
and honest about the limits of rendering.
SVG viewers are required to support only a finite floating-point range and may differ in
fonts and rasterization.
Exact rational or algebraic values therefore belong in structured metadata and adjacent
XML comments; rendered coordinates are documented decimal projections of those values,
not a proof that every pixel is exact.

## Goals

- Produce byte-identical SVG for the same semantic input, renderer version, and render
  specification, independent of hash randomization, locale, time zone, worker count, or
  input map order.
- Make the base figure compact, legible in print and on screen, self-contained, and safe
  to embed in Markdown, HTML, office documents, and reports.
- Support three progressive view levels: final overview, start/final comparison, and
  optional trajectory animation.
- Preserve numerical provenance without clutter: visible summary labels when requested,
  full-precision source decimals and exact expressions in metadata, and concise XML
  comments beside the elements they describe.
- Keep claim status visible.
  A renderer must distinguish a candidate, a numerically verified packing, a certified
  upper bound, and a proved optimum; it must not turn a solver endpoint into a “minimum”
  by typography.
- Reuse the exact `n = 3` quotient map as a known-answer control and make later atlas
  views use the same rendering spine.
- Keep the core renderer in the Python standard library unless a measured visual or
  compatibility gap justifies a pinned optional dependency.

## Non-Goals

- A general charting, graph-layout, or illustration framework.
- The interactive basin-atlas explorer tracked by `think-djvs`. This toolkit supplies
  its deterministic static-export layer but not filtering, linked views, or a browser
  application.
- A new verifier, optimizer, interpolation algorithm, or mathematical certificate.
- Treating an interpolated animation as a feasible path.
  Only retained trajectory frames have the evidence carried by their source records.
- Video, GIF, presentation, or raster export in the core API.
- Editing the archived Kingbird provenance SVGs.
  They remain source evidence.
- Pixel-identical rasterization across unrelated SVG engines and font installations.

## Background

The repository already contains three useful SVG patterns.

[`n-003-optimal-moduli.svg`](../../../../atlas/n-003-optimal-moduli.svg) is visually
clear, self-contained, accessible at the document level, dark-mode aware, and rebuilt
byte for byte by [`check_small_n_moduli.py`](../../../../tools/check_small_n_moduli.py).
Its renderer is one hard-coded function, however.
Layout, theme, topology, labels, packing glyphs, and serialization are coupled, and it
has no reusable packing view, precision policy, start/final comparison, or animation
contract.

The archived Kingbird
[`n = 11`](../../../../resources/papers/kingbird-square-11-provenance.svg) and
[`n = 29`](../../../../resources/papers/kingbird-square-29-provenance.svg) files
preserve the other half of the target: exact construction formulas in comments and
33–100 digit entity values directly in the geometry.
They are excellent provenance artifacts, but their DTD entities, deprecated `xlink`
references, and external `svgDisp.js` script are poor defaults for portable document
embedding.

The current visualization ladder already requires packing glyphs first, typed evidence
edges, exact families as regions rather than point clouds, and explicit separation of
observed, inferred, and certified facts.
This toolkit implements the common rendering substrate without expanding the scientific
claims in that ladder.

The external survey supports a narrow design rather than a new dependency stack:

| Source | Pattern to retain | Reason not to use it as the core |
| --- | --- | --- |
| Ellsworth/Kingbird and the [online catalogue](https://kingbird.myphotos.cc/packing/squares_in_squares__triangular_table.html) | inspectable SVG source, high-precision construction data, reused geometry | external script and DTD/entity dependence; presentation is packing-specific but not an overview/comparison API |
| [UnitSquare result figures](https://hmbelvedere.com/) and the [Wikimedia `n = 11` SVG](https://commons.wikimedia.org/wiki/File:Packing_11_unit_squares_in_a_square_with_side_length_3.87708359....svg) | compact downloadable geometry and precise claim language | final-state publication artifacts, not a reusable trajectory renderer |
| Matplotlib [SVG font modes](https://matplotlib.org/stable/users/explain/text/fonts.html#fonts-in-svg) and [SVG configuration](https://matplotlib.org/stable/users/explain/configuration.html#svg-backend-parameters) | optional text-as-path output for cross-machine appearance; fixed ID salt for reproducibility | a broad plotting dependency, and text paths trade editability and small files for visual consistency |
| [MathJax SVG output](https://docs.mathjax.org/en/v4.1/web/convert.html#creating-stand-alone-svg-images) | local font-path caches can make complex formula SVG self-contained | a separate JavaScript toolchain whose path output should be optional, not required for a simple packing glyph |
| [SVG 2 structure](https://www.w3.org/TR/SVG2/struct.html) and [animation](https://www.w3.org/TR/SVG/animate.html) | native `title`, `desc`, `metadata`, grouping, and declarative animation | animation support is not mandatory, so every animated artifact needs a useful static fallback |

## Design

### Approach

Separate scientific data, presentation policy, and XML serialization:

```text
PackingFrame(s) -> RenderSpec -> semantic scene -> deterministic SVG serializer
                       |               |
                       |               +-> exact metadata and comments
                       +-> overview | comparison | trajectory
```

The semantic scene is deliberately small.
It needs groups, paths, rectangles, lines, circles, text, definitions, metadata, and
animation nodes. It does not need a general DOM, CSS engine, layout solver, or
graph-layout algorithm.

### View and Annotation Profiles

View level and annotation level are orthogonal.
Callers can therefore request an exact but visually minimal overview or a richly labeled
static comparison without animation.

| View | Visible content | Static fallback |
| --- | --- | --- |
| `overview` | one final frame, container, squares, concise claim label | the view itself |
| `comparison` | start and final frames at the same geometric scale, plus the declared objective change | the view itself |
| `trajectory` | a finite, one-pass transition through retained frames | the final frame, fully visible when animation is unsupported or reduced |

| Annotation | Visible content | Embedded content |
| --- | --- | --- |
| `none` | geometry and essential claim status | renderer identity and source record key |
| `summary` | side, frame label, validity/evidence tier, and selected active features | all source numeric strings used by the render |
| `exact` | selected exact formulas where they help the reader | versioned structured metadata plus concise element-adjacent XML comments |

Additional overlays such as square IDs, contacts, residuals, or active constraints are
flags within an annotation profile, not new view levels.

### Semantic Input Model

The renderer consumes immutable typed values rather than raw dictionaries:

- **`ScalarSource`** records the source string, value kind (`binary64`, decimal,
  rational, algebraic expression, or interval), declared precision, and optional
  provenance reference.
  Converting a float records its shortest round-trippable decimal; it does not invent
  extra precision.
- **`SquarePose`** records a stable square ID, centre coordinates, angle in a declared
  unit, side length, and optional exact expressions.
  The coordinate and angle convention is explicit in the document metadata.
- **`PackingFrame`** records the container, ordered poses, source record key, frame
  label, objective value, evidence tier, and verification summary.
- **`PackingTrajectory`** records ordered frames and whether they are retained solver
  states, a certified feasible path, or illustrative endpoint interpolation.
- **`RenderSpec`** records the view, annotations, overlays, fixed theme, viewport,
  numeric projection policy, animation duration, and final fallback frame.

Adapters may read existing `BasinEvent/v3` JSONL, the built-in exact packings, and later
atlas records. The renderer itself does not know those storage schemas.

### Exact Values and Mathematical Annotations

There are three representations because they serve different purposes:

1. **Source value.** Preserve the exact expression, interval, rational string, or full
   decimal exactly as supplied.
   This is the semantic record.
2. **Projected SVG number.** Serialize a deterministic decimal suitable for the SVG
   coordinate system. Normalize negative zero, trailing zeros, exponent form, and locale.
   The projection precision is part of `RenderSpec` and metadata.
3. **Human label.** Round only for reading and show the precision or inequality implied
   by the evidence. A high-precision decimal is never silently shortened into an exact
   equality.

The root `<metadata>` contains a versioned `sqpack` XML namespace with the input source
key, renderer/schema versions, profile, coordinate convention, evidence status, and
every source value used by the drawing.
Under `exact` annotation, each meaningful group also gets a concise adjacent comment,
for example:

```xml
<!-- sqpack: square=8 x=(3+sqrt(2))/2 y=1+sqrt(2)/4 theta=pi/4 -->
<g id="square-8">...</g>
```

Comments are for source inspection; structured metadata is the machine contract.
Neither is substituted into an XML DTD. Simple visible mathematics uses Unicode text.
Complex TeX-to-path labels remain an optional adapter until the base renderer proves a
need for them.

SVG numeric attributes cannot carry a proof of exact geometry.
The SVG 2 specification requires support for finite single-precision values and merely
recommends higher precision for transformations.
Validation and exact claims therefore trace to the source record and verifier, never to
a reparse of rendered pixels.

### Deterministic Serialization

The serializer has one canonical output policy:

- UTF-8, LF line endings, one terminal newline, fixed indentation, and escaped XML text
- stable element order, attribute order, IDs, definition order, palette assignment, and
  numeric formatting
- no timestamp, random ID, environment path, implicit font discovery result, or map
  iteration order in retained output
- local `<defs>` and `<use>` only; no script, event handler, render-time network
  reference, DTD, external entity, `foreignObject`, or deprecated `xlink`
- comments validated against the XML character and comment grammars; invalid source text
  is rejected rather than silently rewritten
- fixed `viewBox` with explicit `width` and `height`; presentation attributes are
  materialized in the document profile so office and PDF converters need not implement
  CSS variables
- atomic writes and a parse-before-replace check in the CLI

Exact byte replay remains the artifact regression contract.
XML canonicalization with comments may be used diagnostically, but it does not replace
the readable retained format.

### Visual System

The base theme is a fixed paper theme: neutral background, high-contrast boundary and
text, restrained colorblind-safe square colors, consistent line weights, generous
padding, and no shadows, filters, gradients, or decorative motion.
Square identity is also available through labels and stable order, so color is not the
only encoding.

The layout is geometry-first.
Overview and comparison views reserve most of the canvas for the packing, keep displayed
precision to one quiet caption, and move full values to metadata.
Comparison panels share one coordinate scale; otherwise a smaller final container could
look unchanged. A monochrome theme and a screen-dark theme can be added as fixed
alternatives after the paper theme passes the same contrast and legibility checks.

The visual benchmark is a small retained gallery, not a vague claim of “publication
quality”: the current `n = 3` map, Trump `n = 11`, a rotated higher-`n` witness, and one
start/final quench pair.
Each is reviewed at document thumbnail size, normal screen size, and print scale against
the strongest local and online examples listed above.

### Animation Semantics

Animation is declarative and self-contained.
Stable square IDs map frames to the same objects.
Nested groups separate translation and rotation so the renderer can animate both without
decomposing arbitrary matrices.
The container and labels may change, but the viewport remains fixed to the union of all
frames.

The default trajectory renderer uses only retained frames.
If a caller supplies only endpoints, it may explicitly request `illustrative`
interpolation.
The SVG then says in visible text and metadata that intermediate poses are
not verified and may overlap.

The animation runs once, does not loop, and freezes on the final frame.
The underlying nonanimated attributes describe the final frame, so engines that ignore
SVG animation still show the useful result.
The output includes a reduced-motion rule and always has a separately reproducible
`comparison` export.
Scrubbing, playback controls, and interactive editing belong to the later atlas
application.

### Components

- **`sqpack/render/model.py`**: immutable scalar, pose, frame, trajectory, evidence, and
  render-spec types plus validation
- **`sqpack/render/scene.py`**: the minimal semantic scene and stable layout helpers
- **`sqpack/render/svg.py`**: numeric formatting, XML escaping, metadata, deterministic
  serialization, and declarative animation nodes
- **`sqpack/render/packing.py`**: overview, comparison, trajectory, packing glyph,
  contact overlay, and visual tokens
- **`sqpack/render/adapters.py`**: explicit adapters for `BasinEvent/v3`, built-in
  packings, and the exact small-`n` model
- **`tools/render_packing_svg.py`**: atomic CLI for retained and ad hoc SVG output
- **`tools/check_svg_rendering.py`**: semantic, mutation, deterministic replay, and
  portability checks integrated into `test.sh`

The package name is `render`, not `visualization`: it owns deterministic artifact
generation, while mathematical view design remains with `think-vcnx` and interactive
exploration remains with `think-djvs`.

### API Changes

The library surface is additive:

```python
from sqpack.render import AnnotationLevel, RenderSpec, ViewLevel, render_packing_svg

svg = render_packing_svg(
    final,
    start=start,
    trajectory=frames,
    spec=RenderSpec(
        view=ViewLevel.COMPARISON,
        annotations=AnnotationLevel.EXACT,
    ),
)
```

The CLI mirrors the same concepts rather than exposing style internals:

```bash
uv run --frozen python tools/render_packing_svg.py \
  result.jsonl --event-id EVENT_ID --view comparison \
  --annotations exact --output atlas/example.svg
```

Invalid or ambiguous inputs fail before writing.
In particular, comparison requires a start and final frame, animation requires stable
square identity, exact annotation requires a declared source representation, and “proved
optimum” requires that evidence tier in the input.

## Implementation Plan

Implementation is tracked by `think-c311`; the later interactive explorer `think-djvs`
depends on it.

### Phase 1: Deterministic Static Spine

- [ ] Write failing checks for stable numeric formatting, XML escaping, stable IDs,
  shuffled input order, locale/time-zone independence, invalid comment text, malformed
  inputs, and exact metadata round trips.
- [ ] Implement the immutable model, minimal scene, standard-library serializer, paper
  theme, overview, comparison, and annotation profiles.
- [ ] Add `BasinEvent/v3`, built-in packing, and exact small-`n` adapters without moving
  storage-schema logic into the renderer.
- [ ] Rebuild the `n = 3` SVG through the shared spine while preserving its topology,
  stratum distinctions, semantic IDs, accessible description, and byte-replay gate.
- [ ] Retain the four-figure benchmark gallery and record file size, element count, and
  render latency. Each static SVG must remain smaller than its lossless reference PNG at
  the review viewport, with no external resource.
- [ ] Review the gallery in a browser and at least one nonbrowser document renderer at
  thumbnail, screen, and print sizes before accepting the theme.

### Phase 2: Trajectories and Portable Animation

- [ ] Write failing checks for stable frame matching, unsupported-animation fallback,
  one-pass final state, reduced motion, invalid durations, mismatched square sets, and
  explicit rejection of unmarked endpoint interpolation.
- [ ] Implement retained-frame animation, the opt-in illustrative endpoint mode, and
  visible/electronic evidence labels.
- [ ] Add contact and active-feature overlays that remain semantically typed across
  frames; never infer a contact from screen-space proximity.
- [ ] Decide from the benchmark gallery whether complex visible formulas justify a
  separate pinned MathJax-to-path adapter.
  Keep it outside the core dependency set and retain text alternatives if added.
- [ ] Document the library and CLI, add the checker to `test.sh`, and expose the static
  export seam to the later basin-atlas work.

## Testing Strategy

**Semantic and failure tests.** Parse every generated document with the standard XML
parser. Check source/frame identity, evidence labels, exact-value recovery, coordinate
conventions, accessible names, and forbidden external features.
Mutation controls must reject a missing square, duplicate ID, altered exact expression,
reordered trajectory, unmarked illustrative interpolation, and stale retained SVG.

**Determinism tests.** Render the same fixture in fresh processes with shuffled input
maps, different supported locales and time zones, and different hash seeds.
Compare bytes, not hashes computed by the same process.
Regenerate every retained fixture in `test.sh` and byte-compare it with the committed
artifact.

**Geometry tests.** Independently project every pose to its four corners and compare the
serialized transforms with the semantic model.
Run the existing verifier on each retained packing frame.
Animation does not grant validity to intermediate frames; only input frames with
verification evidence receive a verified label.

**Known-answer control.** The `n = 3` quotient map must retain its two labelled
12-cycles, unlabelled four-cycle, `D4 x S3` interval, three packing glyphs, and distinct
active-signature/stabilizer semantics.
This catches a renderer that is attractive but mathematically lossy.

**Visual and portability review.** Inspect reference renders from Chrome and a
nonbrowser document path such as Quick Look, LibreOffice, or a PDF converter.
Text must not clip at target sizes; line weights must remain visible in print;
monochrome must preserve identity; unsupported animation must show the final state.
Screenshot comparison becomes a gate only after its renderer and font inputs are pinned;
until then, retained SVG plus structured layout checks are the deterministic contract.

**Performance and size.** Record serialization time and uncompressed size for all four
fixtures. Static rendering must remain negligible beside packing verification, and the
base SVG must remain smaller than its reference lossless PNG. Trajectory size must grow
linearly with retained frame count and reuse style and shape definitions.

The final implementation gate is the repository’s full `./test.sh`, focused Ruff and
BasedPyright checks, deterministic fixture replay, and `make format-check`.

## Rollout Plan

1. Land the additive model, serializer, CLI, static fixtures, and checks without
   changing archived provenance SVGs or atlas storage contracts.
2. Route `check_small_n_moduli.py` through the toolkit and deliberately review the one
   retained `n = 3` golden update.
3. Add comparison and animation artifacts only for retained source records.
   Documents continue to embed the static overview or comparison; animated SVG is an
   explicit browser-oriented export.
4. Let `think-vcnx` use the toolkit’s visual tokens and evidence semantics, and let
   `think-djvs` consume its static-export API after their separate data and view
   contracts are ready.

The old `svg_text()` path is removed only after the shared renderer reproduces the
known-answer semantics and all replay checks pass.

## Acceptance Criteria

- Two fresh-process renders of every fixture are byte-identical under the determinism
  matrix.
- `overview`, `comparison`, and `trajectory` produce valid self-contained SVG; each has
  a useful final static rendering with scripting and animation disabled.
- `exact` annotation round-trips every source expression and decimal used by the
  renderer, and the SVG source remains readable to a human.
- No generated file contains a DTD, external entity, script, event handler, render-time
  network reference, `foreignObject`, or deprecated `xlink` attribute.
  Provenance URLs may appear only as inert metadata or text.
- The `n = 3` topology and strata remain unchanged and byte-replay through the new
  renderer.
- Candidate, verified construction, certified upper bound, and proved optimum are
  visibly and structurally distinct evidence states.
- The benchmark gallery passes thumbnail, screen, print, monochrome, reduced-motion, and
  nonbrowser-renderer review.
- Static fixtures beat their lossless PNG references in file size, and measurements are
  recorded rather than asserted.
- The implementation adds no required runtime dependency and the full repository gate
  passes.

## Open Questions

- Do complex visible formulas occur often enough to justify an optional text-to-path
  adapter, or are Unicode labels plus exact metadata clearer and smaller?
- Should the first animation fixture use the retained `n = 10` source-return events or a
  smaller synthetic path whose every intermediate frame can be independently verified?
  The latter is the safer known-answer control; the former better represents the real
  workflow.

## References

- [Minimal packing toolkit plan](plan-2026-08-22-minimal-packing-toolkit.md)
- [Mathematical frontier strategy: basin ontology and visualization ladder](../../reviews/review-2026-08-23-mathematical-frontier-strategy.md#basin-ontology-and-visualization-ladder)
- [`n = 3` exact-moduli experiment](../../../../campaign/series/series-000-smoke-and-calibration/experiments/exp-014-h-032-n3-optimal-moduli.md)
- [SVG 2: document structure, descriptive elements, and metadata](https://www.w3.org/TR/SVG2/struct.html)
- [SVG 2: real-number precision](https://www.w3.org/TR/SVG2/types.html#Precision)
- [SVG animation model](https://www.w3.org/TR/SVG/animate.html)
- [W3C reduced-motion technique](https://www.w3.org/WAI/WCAG22/Techniques/css/C39)
- [Matplotlib SVG font modes](https://matplotlib.org/stable/users/explain/text/fonts.html#fonts-in-svg)
- [Matplotlib SVG backend reproducibility settings](https://matplotlib.org/stable/users/explain/configuration.html#svg-backend-parameters)
- [MathJax stand-alone SVG guidance](https://docs.mathjax.org/en/v4.1/web/convert.html#creating-stand-alone-svg-images)
- [Canonical XML 1.1](https://www.w3.org/TR/xml-c14n/)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
