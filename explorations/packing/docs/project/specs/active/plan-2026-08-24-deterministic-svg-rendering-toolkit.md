# Feature: Deterministic SVG Rendering Toolkit

**Date:** 2026-08-24 (last updated 2026-08-24)

**Author:** Codex (agent), for the repository owner

**Status:** Implemented, including the contact visualization and compositing extension

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
- Use the same pure-black boundary stroke for the container and every packed square so a
  white separator cannot make an exact contact look like a gap.
  Use a fixed, deterministic 20-color palette confined to cool green, cyan, blue,
  indigo, and violet hues.
- Support three progressive view levels: final overview, start/final comparison, and
  optional trajectory animation.
- Preserve numerical provenance without clutter: visible summary labels when requested,
  full-precision source decimals and exact expressions in metadata, and concise XML
  comments beside the elements they describe.
- Keep claim status visible.
  A renderer must distinguish a candidate, a numerically verified packing, a certified
  upper bound, and a proved optimum; it must not turn a solver endpoint into a “minimum”
  by typography.
- Attach exact contact geometry whenever an adapter still has access to a certified
  algebraic construction.
  Render it as an optional 60%-opaque tempered-yellow highlight: segments for
  positive-length edge contacts and dots for point-to-edge, corner, or wall contacts.
  Place highlights above square fills and below pure-black boundaries, and reserve
  yellow for contact highlighting rather than square identity.
  Clip each mark to the union of its participating square interiors so the wider
  highlight cannot spill into unrelated empty space.
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

The external survey supports a narrow design rather than a new dependency stack.
The decisive finding is that Python’s standard
[`xml.etree.ElementTree`](https://docs.python.org/3.11/library/xml.etree.elementtree.html)
already preserves caller-specified attribute order, emits comments, pretty-prints, and
provides C14N 2.0 canonicalization.
It is the smallest adequate tree and serializer for the required safe SVG subset.

| Library or tool | Strength worth retaining | Decision |
| --- | --- | --- |
| `xml.etree.ElementTree` | ordered attributes, comments, indentation, namespace-aware trees, and diagnostic canonicalization in the Python standard library | **Use in the core.** Build a small SVG-safe helper layer on it; do not build a parallel scene graph or XML serializer. |
| [`svg.py`](https://github.com/orsinium-labs/svg.py) | pure Python, typed SVG elements, no third-party runtime dependencies | Do not add it initially. Its element types are attractive, but this project still needs its own scalar provenance, safe-element policy, comment placement, and exact byte contract. Reconsider only if hand-written element helpers become a measured maintenance problem. |
| [`drawsvg`](https://github.com/cduck/drawsvg) | convenient SVG-native animation and notebook display | Keep as a design reference, not a dependency. Notebook widgets, Cairo-backed raster output, and its broader object model are outside the retained-artifact path. |
| [`svgwrite`](https://svgwrite.readthedocs.io/en/stable/overview.html) | SVG 1.1/Tiny factories and optional validation | Do not use. Its own documentation describes it as an `ElementTree` wrapper and says direct `ElementTree` is sufficient when the SVG vocabulary is known. |
| [`lxml`](https://lxml.de/) | mature XML APIs and canonicalization | Do not use. Standard-library C14N covers the diagnostic need, while `lxml` adds a compiled dependency without improving the rendering contract. |
| [`resvg`](https://github.com/linebender/resvg) | high-quality static SVG rasterization, a maintained conformance suite, explicit font-file loading, and a system-font-off mode | **Use as an optional pinned visual-QA renderer if the toolchain spike succeeds.** It is not a runtime dependency and cannot validate animation because it intentionally supports only static SVG. |
| [CairoSVG](https://cairosvg.org/documentation/index.html) | Python SVG-to-PNG/PDF conversion tested against W3C samples | Keep as a nonbrowser portability option, not a core dependency. Cairo and FFI system requirements make it a less hermetic golden renderer than `resvg`. |
| Matplotlib [SVG font modes](https://matplotlib.org/stable/users/explain/text/fonts.html#fonts-in-svg) and [SVG configuration](https://matplotlib.org/stable/users/explain/configuration.html#svg-backend-parameters) | optional text-as-path output and fixed ID salt | Do not use for packing geometry. It is a broad plotting dependency and text paths trade editability and size for visual consistency. |
| [MathJax SVG output](https://docs.mathjax.org/en/v4.0/options/output/svg.html) | local font-path caches make individual formula SVGs self-contained | Defer to a pinned, optional formula adapter. Unicode labels plus exact metadata remain the base path. |
| [SVGO](https://svgo.dev/docs/plugins/) and [Scour](https://github.com/scour-project/scour) | mature size optimization and cleanup | Do not post-process retained artifacts. Their purpose includes rewriting precision, IDs, comments, descriptions, or metadata—the fields this format treats as evidence and a replay contract. Measure unoptimized output first. |
| Ellsworth/Kingbird and the [online catalogue](https://kingbird.myphotos.cc/packing/squares_in_squares__triangular_table.html) | inspectable SVG source, high-precision construction data, and reused geometry | Retain as provenance and a visual reference, not as the embedding format: the archived files depend on DTD entities, deprecated `xlink`, and external script. |
| [UnitSquare result figures](https://hmbelvedere.com/) and the [Wikimedia `n = 11` SVG](https://commons.wikimedia.org/wiki/File:Packing_11_unit_squares_in_a_square_with_side_length_3.87708359....svg) | compact publication geometry and precise claim language | Retain as visual benchmarks. They are final-state figures, not a reusable comparison or trajectory API. |
| [SVG 2 structure](https://www.w3.org/TR/SVG2/struct.html), [CSS Animations](https://www.w3.org/TR/css-animations-1/), and [W3C reduced-motion technique C39](https://www.w3.org/WAI/WCAG22/Techniques/css/C39) | native `title`, `desc`, `metadata`, grouping, generated keyframes, and preference-aware motion | Use generated CSS motion as progressive enhancement around final-state SVG attributes. Enable it only under `prefers-reduced-motion: no-preference`; unsupported CSS therefore falls back to the final frame. |

## Design

### Approach

Separate scientific data, presentation policy, and XML serialization:

```text
source record -> adapter -> PackingFrame(s) -> RenderSpec -> ElementTree -> SVG text
                    |             |                         |             |
                    |             +-> exact source values   |             +-> atomic file
                    +-> evidence and provenance             +-> safe SVG validation
```

`ElementTree` is the scene tree.
The toolkit supplies constructors only for its allowed SVG subset: groups, polygons,
paths, rectangles, lines, circles, text, definitions, metadata, comments, and one
renderer-owned motion stylesheet.
It does not add a second DOM, CSS engine, layout solver, or graph-layout algorithm.

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
Certified contacts are enabled by default when a frame carries them; callers can remove
`Overlay.CONTACTS`, and the CLI exposes `--no-contacts`, for a geometry-only export.
That choice removes graphical marks only: an `exact` annotation export still retains the
attached contact coordinates in XML comments.

### Semantic Input Model

The renderer consumes immutable typed values rather than raw dictionaries:

- **`ScalarSource`** stores the original string, value kind (`binary64`, decimal,
  rational, algebraic expression, or interval), a finite `Decimal` projection, declared
  precision, and optional provenance reference.
  `scalar_from_float()` uses Python’s shortest round-trippable representation; it does
  not invent digits.
- **`Point2`** stores two sourced scalars.
- **`RigidPose`** stores the centre and angle in radians for motion.
  It is optional because an exact corner construction need not have an equally useful
  exact angle expression.
- **`SquareGeometry`** stores a stable square ID and four ordered exact-or-sourced
  corners, plus an optional rigid pose.
  Static output always uses the corners; trajectory output additionally requires a pose
  for every square in every frame.
- **`VerificationSummary`** stores the verifier name, result, and counts without
  rerunning or upgrading the verifier’s claim.
- **`ContactFeature`** stores one exact point or a nondegenerate exact segment, the one
  or two square IDs involved, and an optional container-wall identity.
  A point has no `end`; a segment has distinct `start` and `end` points.
  Contact coordinates must be rational or algebraic sources rather than binary64 or free
  decimal projections.
- **`PackingFrame`** stores the container side, square sequence, source record key,
  frame label, objective, evidence tier, verification summary, and inert provenance.
- **`PackingTrajectory`** stores ordered frames and a declared trajectory kind: retained
  solver states, certified feasible path, or illustrative endpoint interpolation.
- **`RenderSpec`** stores the view, annotations, overlays, fixed theme, viewport,
  numeric projection policy, duration, and final fallback frame.

Adapters may read existing `BasinEvent/v3` JSONL, the built-in exact packings, and later
atlas records. The renderer itself does not know those storage schemas.

### Exact Values and Mathematical Annotations

There are three representations because they serve different purposes:

1. **Source value.** Preserve the exact expression, interval, rational string, or full
   decimal digit sequence exactly as supplied.
   Insignificant JSON spelling choices such as exponent versus fixed notation are not a
   separate mathematical value, but parsing must not round the supplied digits through
   binary64 before constructing `ScalarSource`. This is the semantic record.
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

### Certified Contact Geometry

Contact extraction belongs between an exact construction and its rendering adapter.
It must not run on projected SVG coordinates, screen distance, or a display tolerance.
The first implementation consumes the repository’s `FieldElement` packings used by the
Trump `n = 11` and certified `n = 5` adapters; numerical `BasinEvent` and Göbel pose
arrays carry no contact highlights unless a later source supplies an independent
certificate.

The extractor uses only exact addition, subtraction, multiplication, and sign tests:

1. Require a valid packing report and stable square IDs before extracting anything.
2. For each square and each container wall, classify exact-zero vertex coordinates.
   One vertex produces a point contact.
   Two adjacent vertices produce one edge segment, without redundant endpoint dots.
3. Have the exact verifier retain the stable pair indices whose best separation is
   exactly zero. Validate the retained count and index ordering, then inspect only those
   pairs. Reusing the verifier’s classification avoids a second quadratic SAT sweep.
4. Intersect the two polygon boundaries by testing edge endpoints against closed edge
   segments. Collinearity is an exact cross-product zero; membership uses the sign of
   `(p-a)·(p-b)` and needs no division.
   A shared positive-length interval becomes one segment.
   Otherwise the unique shared endpoint becomes one point.
5. Reject a reported touching pair with no boundary intersection, two disjoint contact
   points, a zero-length segment, or an unknown square/wall reference.
   Deduplicate exact points and orientation-equivalent segments, then sort stable
   feature IDs before constructing the frame.

This endpoint-on-segment algorithm is sufficient for two valid convex polygons with
disjoint interiors: a noncollinear edge crossing would imply an overlap, while a
positive-length boundary intersection is necessarily collinear.
It avoids the division and root-selection problems of a generic line-line intersection
and keeps every emitted coordinate in the source number field.

The exact adapters always attach this inventory because retaining semantic contact data
has no visual cost. Display remains a `RenderSpec` choice.
The paper profile defaults to showing available contacts; approximate frames remain
visually unmarked rather than presenting tolerance-based guesses as facts.

#### Contact Compositing and Mark Design

Contact geometry and contact display remain separate decisions.
Exact adapters attach the sorted point and segment inventory on every certified frame.
A render can omit the visual group without deleting those semantic features or their
exact annotations.

Each packing panel uses three explicit geometry passes in document order:

1. **Fills.** Emit each square once with the color selected by stable square index from
   the fixed 20-color cool palette and no stroke.
2. **Contacts.** Project certified contact points and segments through the same panel
   transform as the squares.
   Emit them in one optional panel-scoped group using the `#e3c64a` tempered-yellow
   contact token at 60% opacity.
   Clip every mark to the union of the exact projected polygons for the squares named by
   that contact.
3. **Outlines.** Re-emit the square boundaries and container boundary with `fill="none"`
   and an opaque `#000000` 1.25px stroke.

This ordering is part of the retained SVG contract, not a renderer accident.
The 9px contact stroke is wider than the black outline, so a shared-edge highlight
remains visible on both sides of the authoritative boundary while the black centerline
stays unobscured. A point contact uses the same yellow token and a 5.5px radius, leaving
a visible halo around the black corner or edge.
Participant-union clipping contains the wide marks inside the squares that establish the
contact. The outline pass contains no fill, and the fill pass contains no stroke, so
antialiasing cannot create a second gray or white seam.

Yellow is reserved for contact highlights in this profile.
It is not added to `SQUARE_FILL_PALETTE`. That tuple contains 20 fixed cool colors, and
`color_for_square()` selects `palette[index % 20]` without hashes or mutable state.
Pure black is reserved for packing geometry boundaries; the softer ink token may still
be used for text.

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

The implementation uses `ET.register_namespace()`, namespace-qualified tags, and
`ET.indent()`. `serialize_svg()` is the sole text boundary: it applies the fixed XML
declaration and terminal newline, then reparses with a comment-preserving `TreeBuilder`
before returning bytes to a caller.
`canonicalize_svg()` is test-only evidence that semantic XML is stable; retained output
continues to use the readable serializer.

### Visual System

The base theme is a fixed paper theme: neutral background, high-contrast boundary and
text, restrained colorblind-safe square colors, consistent line weights, generous
padding, and no shadows, filters, gradients, or decorative motion.
The 20 square colors form a deterministic cool sequence across green, cyan, blue,
indigo, and violet. The first 11 entries maximize visible separation in the Trump
overview; the remaining entries broaden the reusable atlas sequence.
Container and square outlines use the same opaque pure-black 1.25px stroke.
Certified contact segments and points use 60%-opaque tempered yellow `#e3c64a`, placed
below the black outline and above the fills and clipped to their participant-square
union. Yellow is not a square color in this profile.
Square identity is also available through labels and stable order, so color is not the
only encoding.

The layout is geometry-first.
Overview and comparison views reserve most of the canvas for the packing, keep displayed
precision to one quiet caption, and move full values to metadata.
Comparison panels share one coordinate scale; otherwise a smaller final container could
look unchanged. A monochrome theme and a screen-dark theme can be added as fixed
alternatives after the paper theme passes the same contrast and legibility checks.

The visual benchmark is a small retained gallery, not a vague claim of “publication
quality”:

- `atlas/n-003-optimal-moduli.svg`, the exact quotient-map known-answer control
- `atlas/rendering/trump11-overview.svg`, an exact algebraic final packing
- `atlas/rendering/gobel10-source-return-comparison.svg`, a retained numerical start and
  final pair from experiment 031
- `atlas/rendering/n5-exact-face-trajectory.svg`, the certified algebraic segment from
  experiment 033, with endpoint A, the exact midpoint, and endpoint B

Each is reviewed at document thumbnail size, normal screen size, and print scale against
the strongest local and online examples listed above.

### Animation Semantics

Animation is declarative and self-contained.
Stable square IDs map frames to the same objects.
Nested groups separate translation and rotation so the renderer can animate both without
decomposing arbitrary matrices.
The container and labels may change, but the viewport remains fixed to the union of all
frames.

The renderer does not invent frames for retained or certified trajectory kinds.
Retained trajectories use the supplied solver states; a certified adapter may supply
exact samples plus its full-path certificate, as the `n = 5` face does.
If an uncertified caller supplies only endpoints, it may explicitly request
`illustrative` interpolation.
The SVG then says in visible text and metadata that intermediate poses are not verified
and may overlap.

The underlying SVG transform attributes always describe the final frame.
Generated CSS keyframes override them only inside
`@media (prefers-reduced-motion: no-preference)`, run once, do not loop, and use a
forwards fill whose final keyframe equals the underlying transform.
Engines that ignore CSS or do not affirmatively expose a no-preference setting therefore
show the final useful result without motion.
Contact geometry in a trajectory describes the final frame only.
The underlying static SVG shows it, while the no-preference animation hides the contact
group until the final keyframe so stationary contact marks never appear to describe an
earlier moving pose.
Every trajectory also has a separately reproducible `comparison` export.
Scrubbing, playback controls, and interactive editing belong to the later atlas
application.

### File and Function Map

The package is deliberately flat enough that ownership stays obvious.
Private helpers named below are part of the implementation map, not public API.

#### `sqpack/render/__init__.py`

- Re-export only `AnnotationLevel`, `EvidenceTier`, `Overlay`, `PackingFrame`,
  `PackingTrajectory`, `RenderSpec`, `TrajectoryKind`, `ViewLevel`, and
  `render_packing_svg`.
- Define no behavior and import no repository storage schema.

#### `sqpack/render/model.py`

- Define `ScalarKind`, `EvidenceTier`, `ViewLevel`, `AnnotationLevel`, `Overlay`,
  `ContainerWall`, and `TrajectoryKind` as string enums with stable serialized values.
- Define frozen dataclasses `ScalarSource`, `Point2`, `RigidPose`, `SquareGeometry`,
  `VerificationSummary`, `ContactFeature`, `PackingFrame`, `PackingTrajectory`, and
  `RenderSpec`.
- `validate_scalar_source()` rejects empty source strings, non-finite projections,
  invalid precision, and an exact kind with no exact source.
- `validate_square_geometry()` requires a non-empty stable ID, four corners in boundary
  order, distinct adjacent projected points, and a finite optional pose.
- `validate_frame()` requires a positive container side, a non-empty square sequence,
  unique square IDs, deterministic square and feature order, valid contact participants,
  exact contact coordinates, nondegenerate segments, and evidence/verification
  consistency.
- `validate_trajectory()` requires at least two frames, one square-ID set and order,
  monotonically increasing logical frame times, motion poses, and a trajectory-kind
  claim consistent with frame evidence.
- `validate_render_request()` enforces the cross-product rules: comparison needs start
  and final, trajectory needs a trajectory, `exact` needs complete declared source
  representations, and a proved-optimum label can only come from that input evidence
  tier. A binary64 source remains binary64 under `exact` annotation.

#### `sqpack/render/numbers.py`

- `scalar_from_float()`, `scalar_from_decimal()`, `scalar_from_fraction()`, and
  `scalar_from_exact()` are the only constructors that cross from repository numeric
  types into the rendering model.
- `project_decimal()` applies the declared significant-digit policy under a local
  decimal context.
- `format_svg_number()` emits plain ASCII decimal notation, normalizes negative zero,
  removes insignificant trailing zeros, and rejects exponent output outside the policy.
- `format_visible_number()` applies only the label precision and returns the evidence-
  appropriate relation marker (`=`, `~`, `<=`, or interval text) separately from the
  digits.
- `format_points()` and `format_values()` serialize sequences in input order.
- No module-global decimal context is mutated.

#### `sqpack/render/contacts.py`

- `_same_point()`, `_cross()`, and `_point_on_segment()` implement exact point equality,
  collinearity, and closed-segment membership without division.
- `_pair_contact_geometry()` returns one exact point or segment for a pair already
  classified as touching and rejects geometry inconsistent with that exact SAT result.
- `_wall_contact_geometry()` classifies one square against one named container wall and
  replaces two adjacent zero vertices with one segment.
- `contact_features_from_exact()` enumerates exact wall and pair contacts, converts
  their source coordinates through the adapter’s scalar function, assigns stable IDs,
  and returns a sorted immutable feature tuple.
- The module accepts the current algebraic `FieldElement` construction boundary.
  It does not expose a tolerance and does not consume `Point2` projections.

#### `sqpack/verify.py`

- `Report.touching_pair_indices` retains the stable indices when the verifier classifies
  a zero-gap pair. Existing count fields remain unchanged; exact contact extraction
  consumes the indices only from a valid exact report over the same construction.

#### `sqpack/render/svg.py`

- Define `SVG_NS`, `SQPACK_NS`, `svg_tag()`, `sqpack_tag()`, `element()`, and `sub()` on
  top of `xml.etree.ElementTree`.
- `append_title_desc()` emits non-empty descriptive children before graphical children,
  matching the SVG accessibility guidance and older viewer behavior.
- `append_metadata()` writes the versioned source-value, evidence, profile, and
  coordinate-convention contract under the `sqpack` namespace.
- `append_exact_comment()` validates XML characters and forbids `--` and a trailing
  hyphen before inserting `ET.Comment` adjacent to the described group.
- `append_local_use()` accepts fragment-only `href` values and rejects `xlink`.
- `validate_safe_tree()` walks the tree and rejects elements or attributes outside the
  supported profile, duplicate IDs, scripts, event handlers, `foreignObject`, external
  URL-bearing attributes, and nonlocal references.
- `validate_safe_tree()` accepts at most one renderer-marked motion `<style>`, rejects
  `url(`, `@import`, and arbitrary caller CSS, and verifies that motion declarations are
  scoped to the no-preference media query.
- `serialize_svg()` copies and indents the tree, validates it, emits UTF-8 with the
  fixed declaration and one terminal LF, and reparses the result with comment
  preservation.
- `canonicalize_svg()` calls `ET.canonicalize(..., with_comments=True)` for diagnostic
  comparisons only.
- `write_svg_atomic()` uses the already-required `strif.atomic_output_file`; it never
  replaces a destination until serialization and reparse have succeeded.

There is no `scene.py`. `ElementTree` is the minimal scene representation, so a second
node hierarchy would add conversion code without a second semantic contract.

#### `sqpack/render/style.py`

- Define frozen `Theme` and `LayoutMetrics` dataclasses.
- Provide fixed `PAPER_THEME` first; add `MONOCHROME_THEME` and `SCREEN_DARK_THEME` only
  after the same contrast and fixture checks exist.
- `color_for_square()` hashes no data: it assigns the stable palette by validated square
  order, with labels available as the noncolor identity channel.
- Keep every approved presentation value explicit in one module: `SQUARE_FILL_PALETTE`,
  `SQUARE_FILL_OPACITY`, `PACKING_BOUNDARY_COLOR`, `PACKING_BOUNDARY_WIDTH`,
  `CONTACT_HIGHLIGHT_COLOR`, `CONTACT_HIGHLIGHT_OPACITY`,
  `CONTACT_HIGHLIGHT_STROKE_WIDTH`, `CONTACT_HIGHLIGHT_POINT_RADIUS`, and
  `CONTACT_CLIP_POLICY`. `PAPER_THEME` and `LayoutMetrics` derive from those constants
  instead of repeating literals.
- `PAPER_THEME.container` is the stroke for both the container and every packed square;
  it is pure black rather than the softer text ink.
  `PAPER_THEME.contact` is the reserved tempered-yellow contact token and never enters
  the square palette.
- `evidence_style()` maps every evidence tier to one label, stroke pattern, and icon
  token; callers cannot supply arbitrary claim text.
- `presentation_attributes()` materializes fill, stroke, opacity, font, and line weight
  on retained elements instead of depending on CSS custom properties.

#### `sqpack/render/packing.py`

- `render_packing_svg()` is the public pure function.
  It validates the request, builds one tree, delegates optional motion, and returns
  serialized text.
- `build_packing_document()` creates the root, accessibility text, metadata, background,
  panels, and caption bands in stable order.
- `_select_frames()` maps the view profile to exactly one final frame, a start/final
  pair, or the trajectory frames.
- `_shared_extent()` and `_panel_layout()` compute one geometry scale for all comparison
  panels and a fixed union viewport for trajectory output.
- `_project_point()` maps mathematical coordinates into panel coordinates with the
  explicit upward mathematical `y` convention.
- `_append_packing_panel()` projects each square once, then emits stable `fills`,
  `contacts`, and `outlines` groups in that order before labels and other annotations.
- `_append_square_fill()` emits one stroke-free colored polygon; `_append_container()`
  and `_append_square_outline()` emit the final pure-black outline pass; and
  `_append_square_id()` emits optional labels above all geometry.
- `_append_contact_overlay()` emits tempered-yellow `<line>` nodes for segments and
  `<circle>` nodes for points inside one panel-scoped group between the fill and outline
  passes. It defines each participating projected square once, then gives every mark a
  stable user-space clip path composed of local `<use>` references to those shapes.
  `_append_feature_overlay()` handles other typed features.
  Neither infers contact or activity from projected screen distance.
- `_append_caption()` uses `format_visible_number()` and evidence tokens so typography
  cannot upgrade a claim.

#### `sqpack/render/motion.py`

- `match_square_tracks()` returns square histories in final-frame order and rejects
  missing, duplicate, or reordered identities.
- `keyframe_percentages()` normalizes logical frame times to deterministic percentages
  from zero through 100.
- `unwrap_quarter_turn_angles()` chooses the shortest equivalent unit-square rotation
  modulo `pi/2`, using a deterministic tie rule.
- `square_keyframes()` and `container_keyframes()` produce deterministic CSS transform
  keyframes for nested translation/rotation groups and the container within the fixed
  union viewport.
- `append_square_motion()` and `append_container_motion()` set final-state transform
  attributes and stable CSS selectors; they do not emit SMIL nodes.
- `append_motion_styles()` enables the one-pass animation only inside
  `prefers-reduced-motion: no-preference`, leaving final underlying attributes visible
  everywhere else.
- `append_final_overlay_motion()` and the renderer-owned CSS grammar hide a final-only
  contact group during active motion and reveal it at the final keyframe.
- No function synthesizes intermediate evidence.
  Illustrative endpoint interpolation is labeled on the root, caption, description, and
  metadata.

#### `sqpack/packings/n5_equal_side_face.py`

- Define frozen `EqualSideFace` with the `Q(sqrt(2))` field, exact side, parameter
  bound, fixed centres, moving-square endpoint centres, and orientation classes already
  proved by experiment 033.
- `build_equal_side_face()` reconstructs the exact object without importing a checker or
  any rendering type.
- `centres_at()` evaluates the affine face at an exact field parameter and rejects a
  parameter outside the certified interval.
- `check_n5_equal_side_face.py` remains the independent certificate consumer, while the
  rendering adapter becomes a second consumer of this domain fixture.
  Mathematical construction data therefore does not live in `sqpack.render`.

#### `sqpack/render/adapters.py`

- `frame_from_pose_arrays()` normalizes centre/angle arrays, calls the independent
  `sqpack.verify.corners_from_poses()` geometry door, and preserves the supplied scalar
  strings.
- `frames_from_basin_event()` validates a `BasinEvent/v3` through an adapter-local
  schema boundary, derives the start’s enclosing side, and returns start/final frames
  without importing `tools/basin_census.py`.
- `frame_from_gobel10()` adapts `sqpack.packings.gobel10.pose()` as a numerical
  construction with its retained source ID, URL, and digest.
- `frame_from_trump11()` adapts `sqpack.packings.trump11.build()` from exact corner
  elements, recording number-field coefficient strings, the published side formula, and
  its exact contact inventory.
- `trajectory_from_n5_equal_side_face()` reconstructs endpoint A, the exact midpoint,
  and endpoint B from `sqpack.packings.n5_equal_side_face`, then marks the trajectory as
  a certified feasible path without owning the algebraic construction.
  Each exact frame receives its own contact inventory before projection.
- `_enclosing_side()` and `_normalize_pose()` are adapter-only conversions shared by
  event and pose-array adapters; they do not become new verification functions.

#### Existing files changed

- `tools/check_small_n_moduli.py`: rename `svg_text()` to `render_n3_moduli_svg()` and
  replace string-built XML with shared `svg.py` helpers, number formatting, and visual
  tokens. Keep quotient topology and its domain-specific layout in this tool; do not
  force graph views into `packing.py`. Its three packing glyphs use the same pure-black
  stroke and width for their container and inner squares.
- `tools/check_n5_equal_side_face.py`: consume
  `sqpack.packings.n5_equal_side_face.build_equal_side_face()` while keeping
  feasibility, optimality, source alignment, and negative controls in the checker.
- `tools/basin_census.py`: keep the storage contract and producer behavior unchanged.
  Any duplicated pose-bound helper is removed only after the adapter has focused tests.
- `test.sh`: add `step_svg_rendering()` and a `STEPS` entry.
  The step runs the focused checker and byte-replays every retained SVG; it remains
  read-only.

#### New tools and retained artifacts

- `tools/render_packing_svg.py`: `parse_args()`, `build_source_parser()`,
  `load_event()`, `load_builtin()`, `build_spec()`, and `main()`. Source selection uses
  explicit `event`, `builtin`, and `n5-face` subcommands.
  `load_event()` parses decimal tokens without an intermediate binary64 round-trip, and
  output always goes through `write_svg_atomic()`. `--contacts` is on by default and
  `--no-contacts` removes the overlay without discarding attached semantic features.
- `tools/check_svg_rendering.py`: `build_fixtures()`, `run_model_controls()`,
  `run_number_controls()`, `run_xml_controls()`, `run_geometry_controls()`,
  `run_animation_controls()`, `run_determinism_matrix()`, `run_portability_controls()`,
  `run_gallery_controls()`, and `main()`.
- `tools/render_packing_gallery.py`: `build_gallery_sources()`, `render_gallery()`,
  `render_n3_moduli()`, `build_gallery_manifest()`, `build_gallery_metrics()`,
  `write_gallery()`, `check_gallery()`, and `main()`. The manifest joins artifacts to
  frontier cases, evidence, accessible copy, motion semantics, and exact regeneration
  commands; aggregate update and check modes include all four artifacts.
- Retain the three new files under `atlas/rendering/` named in the visual benchmark.
  The existing `atlas/n-003-optimal-moduli.svg` stays at its published path.
- Retain `atlas/rendering/manifest.json` as the byte-checked discovery layer consumed by
  the frontier and atlas documentation.
- Record deterministic fixture byte size, element count, renderer version, viewport, and
  optional pinned PNG size in `atlas/rendering/metrics.json`; it is regenerated and
  compared byte for byte by the checker.
  Record observed serialization latency with the host/runtime fingerprint in
  `atlas/rendering/README.md`; timing is benchmark evidence, not a byte-replay field.

The package name is `render`, not `visualization`: it owns deterministic artifact
generation, while mathematical view design remains with `think-vcnx` and interactive
exploration remains with `think-djvs`.

### Call Flows

The ordinary CLI path is:

```text
main
  -> load_event | load_builtin | trajectory_from_n5_equal_side_face
  -> PackingFrame | PackingTrajectory
  -> build_spec
  -> render_packing_svg
       -> validate_render_request
       -> build_packing_document
       -> append_square_motion (trajectory only)
       -> validate_safe_tree
       -> serialize_svg
  -> write_svg_atomic
```

The exact `n = 3` control intentionally shares only the XML and style spine:

```text
build_n3_model -> render_n3_moduli_svg
               -> svg element helpers + number formatting + visual tokens
               -> serialize_svg -> retained byte replay
```

This boundary prevents a packing renderer from becoming a graph-layout framework while
still proving that metadata, accessibility, safety, and serialization work for a second
kind of mathematical figure.

### API Changes

The library surface is additive:

```python
from sqpack.render import AnnotationLevel, RenderSpec, ViewLevel, render_packing_svg

svg = render_packing_svg(
    final,
    start=start,
    trajectory=trajectory,
    spec=RenderSpec(
        view=ViewLevel.COMPARISON,
        annotations=AnnotationLevel.EXACT,
    ),
)
```

The CLI mirrors the same concepts rather than exposing style internals:

```bash
uv run --frozen python tools/render_packing_svg.py \
  event result.jsonl --event-id EVENT_ID --view comparison \
  --annotations exact --output atlas/example.svg
```

Invalid or ambiguous inputs fail before writing.
In particular, comparison requires a start and final frame, animation requires stable
square identity, exact annotation requires a declared source representation, and “proved
optimum” requires that evidence tier in the input.

## Implementation Plan

Implementation is tracked by `think-c311`; the later interactive explorer `think-djvs`
depends on it.

Implementation completed on 2026-08-24. The retained gallery, focused checker, CLI,
exact construction fixture, and repository gate implement the contracts below.
Raster screenshots remain manual because the host has neither a pinned `resvg` binary
nor pinned fonts; `atlas/rendering/README.md` records the measured decision.

### Bead Map

The implementation shortcut produced this child graph under the `think-c311` epic.
Blockers express only real file/API prerequisites; the serializer and adapter work can
begin in parallel after the shared typed contract is established.

| Bead | Deliverable | Blocked by |
| --- | --- | --- |
| `think-5681` | typed rendering model and exact numeric projection | — |
| `think-lo8v` | safe deterministic `ElementTree` SVG spine | `think-5681` |
| `think-tkes` | numerical and exact source adapters | `think-5681` |
| `think-wt8n` | paper theme, overview, and comparison renderer | `think-5681`, `think-lo8v` |
| `think-acxh` | explicit-source CLI and atomic output | `think-tkes`, `think-wt8n` |
| `think-fceb` | exact `n = 3` quotient-map migration | `think-wt8n` |
| `think-hzk5` | static safety, determinism, replay, and `test.sh` gate | `think-acxh`, `think-fceb` |
| `think-90ix` | certified and illustrative accessible trajectories | `think-hzk5` |
| `think-ov1d` | typed square, contact, and active-feature overlays | `think-90ix` |
| `think-c8n2` | benchmark gallery, metrics, and pinned-renderer decision | `think-acxh`, `think-fceb`, `think-90ix`, `think-ov1d` |
| `think-f46b` | documentation, spec reconciliation, and full final gate | `think-hzk5`, `think-90ix`, `think-ov1d`, `think-c8n2` |
| `think-ogiq` | pure-black borders and exact point/segment contact visualization | — |

### Phase 1: Deterministic Static Spine

- [x] Write failing checks for `model.py`, `numbers.py`, and `svg.py`: stable numeric
  formatting, XML escaping, stable IDs, shuffled input order, locale/time-zone
  independence, invalid comment text, malformed inputs, forbidden SVG features, and
  exact metadata round trips.
- [x] Implement the immutable model and the `ElementTree`-based safe serializer.
- [x] Implement `style.py` and the `overview` and `comparison` paths in `packing.py`.
- [x] Add `BasinEvent/v3`, Göbel `n = 10`, Trump `n = 11`, and exact `n = 5` adapters
  without moving storage-schema logic into the renderer.
- [x] Add the explicit-source CLI and atomic output boundary.
- [x] Rebuild the `n = 3` SVG through the shared XML, numeric, and style spine while
  preserving its topology, stratum distinctions, semantic IDs, accessible description,
  and byte-replay gate.
- [x] Add the focused checker to `test.sh` with mutation and fresh-process determinism
  controls before retaining new fixtures.

### Phase 2: Trajectories and Portable Animation

- [x] Write failing checks for stable frame matching, unsupported-animation fallback,
  one-pass final state, reduced motion, invalid durations, mismatched square sets, and
  explicit rejection of unmarked endpoint interpolation.
- [x] Implement the certified three-frame `n = 5` path first, then retained-frame CSS
  animation and the opt-in illustrative endpoint mode.
- [x] Add contact and active-feature overlays that remain semantically typed across
  frames; never infer a contact from screen-space proximity.
- [x] Retain the four-figure benchmark gallery and metrics.
  Each static SVG must remain smaller than its lossless reference PNG at the review
  viewport, with no external resource.
- [x] Run the pinned-renderer availability spike and review the gallery in a nonbrowser
  document renderer at thumbnail, screen, print, monochrome, and reduced- motion
  settings. Promote raster screenshots to a gate only if renderer and font inputs are
  fully pinned.
- [x] Decide from the gallery whether complex visible formulas justify a separate pinned
  MathJax-to-path adapter.
  Keep it optional and retain text alternatives if added.
- [x] Document the library and CLI and expose the static export seam to the later
  basin-atlas work.

### Phase 3: Boundary and Contact Semantics

- [x] Add failing controls proving that container and square strokes share one
  pure-black token while deterministic square assignment uses the approved 20-color cool
  palette and never uses the reserved yellow.
- [x] Add exact known-answer controls for a wall-edge segment, wall-point contact,
  square-edge segment, square point-to-edge contact, strict separation, deduplication,
  and rejection of inconsistent contact geometry.
- [x] Implement exact source-space contact extraction and attach it in the Trump and
  `n = 5` adapters; leave numerical candidate sources unmarked.
- [x] Render contact segments and points by default, preserve an explicit no-contact
  export, and keep final-frame contacts hidden until a trajectory ends.
- [x] Reserve tempered yellow `#e3c64a` for contacts and emit geometry in explicit
  fill/contact/outline order, with 60% contact opacity and opaque pure-black boundaries
  in the top pass.
- [x] Clip each contact mark to the exact projected union of its participating squares,
  using stable local definitions and references rather than duplicating polygon geometry
  for every mark.
- [x] Regenerate and inspect all retained figures at document scale.
  Confirm that black shared borders show touching geometry without false white gaps and
  that the clipped contact overlay remains readable across the fixed cool palette.
- [x] Run focused lint, type, determinism, safe-SVG, CLI, and byte-replay checks
  followed by the full repository gate; update the gallery measurements and
  documentation.

## Testing Strategy

**Semantic and failure tests.** Parse every generated document with the standard XML
parser. Check source/frame identity, evidence labels, exact-value recovery, coordinate
conventions, accessible names, and forbidden external features.
Mutation controls must reject a missing square, duplicate ID, altered exact expression,
reordered trajectory, unmarked illustrative interpolation, and stale retained SVG.

**Determinism tests.** Render the same fixture in fresh processes with shuffled input
maps, different available locales and time zones, and different hash seeds.
Compare bytes, not hashes computed by the same process.
Regenerate every retained fixture in `test.sh` and byte-compare it with the committed
artifact.

**Geometry tests.** Independently project every pose to its four corners and compare
static polygon coordinates and trajectory transforms with the semantic model.
Run the existing verifier on each retained packing frame.
Animation does not grant validity to intermediate frames; only input frames with
verification evidence receive a verified label.
Exercise exact contact extraction against hand-sized point and segment fixtures, then
check the Trump pair-contact count against its verifier report.
Assert that candidate pose arrays never acquire contacts through a visual tolerance.

**Known-answer control.** The `n = 3` quotient map must retain its two labelled
12-cycles, unlabelled four-cycle, `D4 x S3` interval, three packing glyphs, and distinct
active-signature/stabilizer semantics.
This catches a renderer that is attractive but mathematically lossy.

**Visual and portability review.** Inspect reference renders from Chrome and a
nonbrowser document path such as Quick Look, LibreOffice, or a PDF converter.
Text must not clip at target sizes; line weights must remain visible in print;
monochrome must preserve identity; unsupported animation must show the final state.
The first raster-golden candidate is pinned `resvg` with `--skip-system-fonts` and an
explicit checked-in or digest-pinned font file.
Because `resvg` intentionally ignores animation, Chrome remains the animation review
path. Test that the no-preference media query is the only rule that enables motion and
that its absence leaves final attributes.
Screenshot comparison becomes a gate only after pinning the renderer and font inputs;
until then, retained SVG plus structured layout checks are the deterministic contract.

**Performance and size.** Record observed serialization latency and uncompressed size
for all four fixtures, but byte-replay only deterministic structural metrics.
Static rendering must remain negligible beside packing verification.
The base SVG must remain smaller than its reference lossless PNG. Trajectory size must
grow linearly with retained frame count and reuse style and shape definitions.

The final implementation gate is the repository’s full `./test.sh`, focused Ruff and
BasedPyright checks, deterministic fixture replay, and `make format-check`.

## Rollout Plan

1. Land the additive model, serializer, CLI, static fixtures, and checks without
   changing archived provenance SVGs or atlas storage contracts.
2. Route `check_small_n_moduli.py` through the toolkit and deliberately review the one
   retained `n = 3` golden update.
3. Add comparison and animation artifacts only for retained source records or the exact
   certified `n = 5` path.
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
- Every packing outline and its container share the same pure-black 1.25px stroke.
  Square assignment deterministically cycles through the fixed 20-color cool palette,
  which contains no yellow.
- Exact Trump and `n = 5` frames retain stable point/segment contact features; numerical
  candidate frames retain none.
  Contact display defaults on, can be disabled explicitly, and never marks a trajectory
  before its final frame.
  Every point and segment is 60%-opaque tempered yellow and is clipped to the union of
  the exact participant-square polygons.
- The benchmark gallery passes thumbnail, screen, print, monochrome, reduced-motion, and
  nonbrowser-renderer review.
- Static fixtures beat their lossless PNG references in file size, and measurements are
  recorded rather than asserted.
- The implementation adds no required runtime dependency and the full repository gate
  passes.
- The core contains no custom XML serializer or parallel scene graph; `ElementTree` is
  covered by byte replay, safe-subset validation, and comment-preserving reparse tests.
- The optional raster-QA decision records the exact `resvg` version and font inputs, or
  records why raster goldens remain manual.

## Resolved Decisions and Deferred Questions

- **Resolved:** use standard-library `ElementTree`, not a custom scene graph or a new
  SVG generation dependency.
- **Resolved:** use the exact `n = 5` equal-side face as the first animation fixture.
  Its endpoints, midpoint, feasibility, and evidence tier are already reproducible.
- **Resolved:** extract contacts in exact source space, always attach them to exact
  frames, and make their 60%-opaque tempered-yellow display default-on but removable.
  Do not infer contact from decimal projections or pixels.
- **Resolved:** render fills, contacts, and outlines as separate ordered passes.
  Keep contact marks below pure-black boundaries, reserve yellow for highlights, and use
  a deterministic 20-color cool palette for square identity.
- **Resolved:** clip wide contact marks to the union of their participating square
  interiors. Define projected square clip shapes once per panel and reuse them through
  stable fragment-only `<use>` references.
- **Deferred with an explicit gate:** add MathJax paths only if the gallery demonstrates
  that Unicode labels plus exact metadata are materially worse for a recurring formula.
- **Deferred with an explicit gate:** add raster screenshot comparisons only if `resvg`,
  fonts, viewport, and pixel comparison policy can be pinned without a fragile system
  dependency.

## References

- [Minimal packing toolkit plan](plan-2026-08-22-minimal-packing-toolkit.md)
- [Mathematical frontier strategy: basin ontology and visualization ladder](../../reviews/review-2026-08-23-mathematical-frontier-strategy.md#basin-ontology-and-visualization-ladder)
- [`n = 3` exact-moduli experiment](../../../../campaign/series/series-000-smoke-and-calibration/experiments/exp-014-h-032-n3-optimal-moduli.md)
- [SVG 2: document structure, descriptive elements, and metadata](https://www.w3.org/TR/SVG2/struct.html)
- [SVG 2: real-number precision](https://www.w3.org/TR/SVG2/types.html#Precision)
- [CSS Animations Level 1](https://www.w3.org/TR/css-animations-1/)
- [W3C reduced-motion technique](https://www.w3.org/WAI/WCAG22/Techniques/css/C39)
- [Python `xml.etree.ElementTree`](https://docs.python.org/3.11/library/xml.etree.elementtree.html)
- [`svg.py`](https://github.com/orsinium-labs/svg.py)
- [`drawsvg`](https://github.com/cduck/drawsvg)
- [`svgwrite` overview](https://svgwrite.readthedocs.io/en/stable/overview.html)
- [`resvg`](https://github.com/linebender/resvg)
- [CairoSVG documentation](https://cairosvg.org/documentation/index.html)
- [SVGO plugins](https://svgo.dev/docs/plugins/)
- [Scour](https://github.com/scour-project/scour)
- [Matplotlib SVG font modes](https://matplotlib.org/stable/users/explain/text/fonts.html#fonts-in-svg)
- [Matplotlib SVG backend reproducibility settings](https://matplotlib.org/stable/users/explain/configuration.html#svg-backend-parameters)
- [MathJax SVG output options](https://docs.mathjax.org/en/v4.0/options/output/svg.html)
- [Canonical XML 2.0](https://www.w3.org/TR/xml-c14n2/)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
