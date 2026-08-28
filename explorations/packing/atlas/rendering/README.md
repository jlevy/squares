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

### General Motion Lab: setup and free quench

> **Maturity: rough draft, first landed 2026-08-28.** This is a days-old Phase 1 tool
> that grew out of a single `n = 5` spike, and it should be read as an instrument under
> construction rather than a settled part of the toolchain.
> It has never been used to produce a research result.
> Its interfaces are expected to change: the scenario, frame, request, event, and trace
> contracts are versioned precisely so they can be, and Phase 2 is already known to need
> a schema amendment. It has been exercised by its own tests, by one senior engineering
> review whose findings are addressed below, and by manual browser passes — not by
> sustained use. Treat surprising behaviour as a likely defect in the lab, not as a
> finding about packings, and check anything it shows you against the exact and verifier
> paths that own those claims.

The served Motion Lab turns the numerical quench into an inspectable local experiment.
Choose a square count, starting container side, and seed; drag the resulting unit
squares; use setup-only snapping to assemble temporary chunks; and then release those
chunks into an unconstrained quench.

From the exploration root, start the loopback service and open the lab in the default
browser:

```bash
uv run --frozen --all-extras --group dev python \
  -m devtools.serve_packing_motion_lab serve --open
```

The service prints its URL, normally `http://127.0.0.1:8765/`. It binds only to IPv4
loopback, makes no remote request, and answers only requests whose `Host` header is
`127.0.0.1` or `localhost`. That last check is what a loopback bind alone does not give:
a page whose own hostname re-resolves to loopback reaches the service as a same-origin
caller, and the `Host` header is the only part of such a request that still names it.
Reach the lab by one of those two names, not through a hostname that points at loopback.
The exact `n = 5` scenario is also available from the Scenario control and at
`http://127.0.0.1:8765/exact-n5`.

#### Setup and run workflow

1. Set **Squares**, **Starting side**, and **Seed**, then choose **New pose**.
   **Randomize all** changes all three fields while retaining the resulting seed for
   replay.
2. Drag one square to translate its current temporary chunk.
   Release it near a square edge, square vertex, or container wall to apply the nearest
   valid snap. Shift-drag rotates the entire chunk about its center; the rotation buttons
   and `Q` / `E` keys provide the same operation.
3. Read the Geometry row before running.
   Red dashed boundaries identify overlaps or squares outside the container; the editor
   reports these states instead of silently repairing them.
4. Choose **Release + run quench**. This discards every temporary group and sends only
   the container side, square centers, angles, solver choice, and numerical budgets.
   Of those, the optimizer consumes only the centers and angles.
   **Starting side** frames the setup and draws the released pose at the scale you
   placed it; the quench re-minimizes the side and never treats the declared value as a
   bound, so two runs differing only in that field return identical numbers.
   Setup snapping is a placement aid, not an optimizer constraint.
5. Step, scrub, or play the returned trace.
   Download saves the exact canonical response bytes, including the request needed for
   replay. A run that the service rejects clears the timeline and disables the download,
   so nothing named a trace can be saved from a failed run.

The timeline uses one visual grammar across numerical runs:

| Phase | Geometry | Meaning |
| --- | --- | --- |
| Setup released | Ordinary solid squares | The editor pose after all temporary-group metadata was discarded |
| Fixed-angle LP | Blue solid boundaries | Translation and container-side optimization with angles fixed |
| Angular probe | Violet dashed ghosts over the last accepted solid pose | A tested angle state; it has not replaced the accepted packing |
| Rejected probe | Red short-dashed ghosts | A tested angle state that the solver rejected |
| Accepted rotation | Green solid boundaries | A probe promoted to the accepted numerical state |
| Cell change | Amber label and timeline mark | The active separating-axis assignment changed |
| Stop | Neutral solid state | The retained terminal state and its stopping reason |

Smooth motion between retained endpoints is illustrative.
The numbered endpoints and downloaded trace are the numerical record.

The per-event counters are scoped to the single solver call each event reports, and are
labelled that way. They do not add up to the run, and they are not meant to: one LP call
is reported twice, once as the fixed-angle state it produced and once as the angular
probe that asked for it.
The `fixed-point` events are the ones in bijection with LP calls, and the gate pins
their sum to the run total.
Read run totals from the result record, which the stop event displays directly.
A large run may retain thousands of low-level events, so the visible timeline is a
41-event moving window and autoplay targets a 160-event sample while preserving setup,
accepted rotations, cell changes, and stop events.
The slider, Previous and Next controls, downloaded trace, and replay command still reach
every retained event.

#### Service and evidence boundaries

Phase 1 accepts at most 20 squares, 1,000 sweeps, and a 300-second numerical budget.
The request parser rejects unknown fields, duplicate JSON keys, editor groups, contact
locks, and other undeclared constraints.
It returns typed JSON errors rather than treating malformed input as a numerical result.
The browser and command-line paths call the same request validator and trace adapter.

An editor start may overlap or leave the container, and a quench may stop at a sweep or
time budget without converging.
Those are visible outcomes, not successful packings.
Any promising endpoint is only a numerical candidate until it is exported, independently
checked, and promoted through the campaign’s ordinary evidence rules.
Persistent rigid chunks, contact locks, hinges, and soft magnetic penalties are not
implemented; the active plan keeps them behind a separate Phase 2 semantic decision.

The shared implementation lives in these repository-owned components:

| Component | Owner |
| --- | --- |
| Scenario, frame, request, event, and trace records | `src/sqpack/motion_lab/contracts.py` |
| Temporary-group and snap geometry | `src/sqpack/motion_lab/snap.py` |
| Read-only quench observation and phase projection | `src/sqpack/motion_lab/trace.py` |
| Shared palette, compact theme, and browser reducers | `src/sqpack/motion_lab/assets/` |
| Live HTML profile and loopback adapter | `devtools/render_general_motion_lab.py` and `devtools/serve_packing_motion_lab.py` |

The
[generalized Motion Lab plan](../../docs/project/specs/active/plan-2026-08-25-generalized-motion-lab.md)
owns the contracts, evidence grammar, Phase 1 acceptance criteria, and explicit Phase 2
gate.

#### What the first review found

Phase 1 was reviewed before it landed, and the findings are worth keeping visible rather
than folding silently into the history, because they say what kind of tool this is.
None were mathematical: the quench, the verifier, and the exact scenario were untouched.
All six were in the new instrument — a failed run that left the previous trace
downloadable, a replay command that promised byte fidelity and checked only semantics, a
timeline counter that changed meaning on its last event, a control labelled as a solver
input that the solver never receives, an unguarded second implementation of the snap
reducer in the browser, and a loopback service that trusted its own bind.
All six are fixed; the four that were defects in a computed value or a retained artifact
are D-350 through D-353, and each has a control that fails without its fix.
The other two were a missing guard and a missing check rather than a wrong answer, so
they carry no defect ID.

The review also found D-349, which is not in this tool at all: `quench_bracket` drops
the LP work of a free sweep that aborts on its budget.
That one is deferred, because correcting it changes numbers the engine has already
reported.

That distribution is the honest summary of this tool’s maturity.
The parts with years of controls behind them held; everything written in the last few
days had defects in it, and a single review pass found six.
Expect more.

### `n = 5`: exact interactive scenario

[Open the self-contained motion lab](n5-motion-lab.html).

The self-contained HTML+SVG artifact exposes the six certified
`(R4, R5) × (A, interior, B)` paths from experiment 042 and the displayed `+W` direction
obstructed by experiment 036. It has a parameter scrubber, one-pass playback for
certified paths, source-declared contact-graph states, center trails, first-order
predictors, and owner-branch obstruction readouts.

This file is an interactive research artifact, not a safe publication SVG. Dashed
geometry is a tangent predictor; in the `+W` view it is explicitly not a feasible path.
The document SVG renderer and its script-free safety profile remain unchanged.
See the
[motion-lab spike record](../../docs/project/specs/active/spike-2026-08-25-n5-motion-lab.md)
for its analytic data contract, evidence boundary, tests, and known limits.
The shared shell retains this artifact as the offline compatibility control; it still
has `connect-src 'none'` and does not require the loopback service.

### `n = 10`: numerical comparison

![A perturbed Göbel ten-square source beside its returned quench endpoint.](gobel10-source-return-comparison.svg)

A retained source perturbation and the endpoint returned by the deterministic quench
share one geometric scale.
The left panel’s squares carry deliberately distinct, tiny angle perturbations, so its
angle-coded hues differ; the returned axis-aligned endpoint shares one hue.
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

The default color contract is `--hue angle --shade contacts`: equal orientations modulo
a quarter turn share a hue, while the number of full-side contacts selects one of five
shades. Four flush sides use the darkest shade and no flush sides use the lightest.
Angle classes use the full retained numeric precision with a `1e-6`-radian seed
tolerance; strict full-side contacts merge seeds that represent the same physical
orientation. The defaults use 20 hue families, five shades, and a `0.2` total lightness
span. `--hues`, `--shades-per-hue`, and `--shade-span` customize those values;
`--shade contrast` and the legacy `--hue index --shade sequence` remain explicit
alternatives.

The near-wall outliers in retained `n = 68` are a useful precision check.
Their orientations are about `0.009°` to `0.080°` off axis, more than 100 times the
angle tolerance—and their endpoints do not form full-side contacts.
Their different hues therefore expose real offsets in that numerical witness rather than
rounding noise.

Every square and the container use the same 1.25px pure-black stroke, so touching shapes
do not appear separated by white seams.
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

Regenerate or byte-check the interactive motion lab:

```bash
uv run --frozen --all-extras --group dev python \
  -m devtools.render_packing_motion_lab \
  --output atlas/rendering/n5-motion-lab.html

uv run --frozen --all-extras --group dev python \
  -m devtools.render_packing_motion_lab \
  --output atlas/rendering/n5-motion-lab.html --check
```

Run a saved numerical request, then replay the canonical trace byte for byte:

```bash
uv run --frozen --all-extras --group dev python \
  -m devtools.serve_packing_motion_lab run \
  --request request.json --output trace.json

uv run --frozen --all-extras --group dev python \
  -m devtools.serve_packing_motion_lab replay trace.json
```

The retained small known answer exercises setup release, fixed-angle LP states, angular
probes, one accepted rotation, and a sweep-limit stop:

```bash
uv run --frozen --all-extras --group dev python \
  -m devtools.serve_packing_motion_lab replay \
  atlas/rendering/free-quench-n1-trace.json
```

[`free-quench-n1-request.json`](free-quench-n1-request.json) is the input;
[`free-quench-n1-trace.json`](free-quench-n1-trace.json) is the 144-event canonical
output. The focused test regenerates the trace, compares its bytes, asserts its declared
endpoint, and checks that endpoint through the independent separating-axis verifier.
This fixture is a transport and presentation control, not a new packing result.

Byte-identical replay requires the same locked numerical environment and a request that
stops deterministically, as the retained sweep-limited fixture does.
An arbitrary request that reaches its wall-clock budget can legitimately replay to a
different cutoff on a materially different machine; the strict replay command reports
that drift instead of hiding it.

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
document and screen scale; the pure-black boundaries, square fills, translucent clipped
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
