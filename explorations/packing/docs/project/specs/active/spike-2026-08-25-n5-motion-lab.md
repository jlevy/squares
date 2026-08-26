# Spike: Interactive `n = 5` Motion Lab

**Date:** 2026-08-25

**Author:** Codex (agent), for the repository owner

**Status:** Implemented spike; retain as a narrow precursor to the atlas application

**Workflow:** W7 pipeline improvement, tracked by `think-vb0v`

## Outcome

The repository now has a deterministic, self-contained HTML+SVG lab for nine `n = 5`
motion scenes:

- the six certified paths in `(R4, R5) × (A, interior, B)` from experiment 042; and
- the displayed `+W` first-order direction at the same three strata, paired with the
  branch-exhaustive second-order obstruction from experiment 036.

The lab supports play, pause, restart, manual scrubbing, stratum selection, owner-branch
selection for the obstruction, square IDs, center trails, tangent predictors, and the
source-declared contact graph.
It starts paused and runs a certified path once per Play action.
Reduced-motion users retain manual scrubbing.

[Open the retained motion lab](../../../../atlas/rendering/n5-motion-lab.html).

## Why This Is a Separate Artifact

The existing publication renderer produces deterministic SVG suitable for embedding in
documents. Its safe profile rejects JavaScript, SMIL, arbitrary CSS, rotation animation,
and dynamic contacts.
Those restrictions are tested and useful.

An interactive scrubber needs JavaScript and must update rotating poses and contact
states. The spike therefore adds a separate HTML profile instead of weakening the safe
SVG serializer:

```text
exp-042 exact R4/R5 functions ─┐
                               ├─> packing_motion_studies.py ─> MotionLab/v1
exp-036 obstruction constants ─┘                                │
                                                                v
                                          render_packing_motion_lab.py
                                                                │
                                                                v
                                                   n5-motion-lab.html

PackingFrame/PackingTrajectory ─> safe SVG renderer ─> document SVGs
```

The HTML lab is not accepted by `validate_safe_tree()` and must not be presented as a
safe publication SVG. The broader interactive basin-atlas application remains tracked by
`think-djvs`; this spike does not complete that feature.

## What the Spike Reuses

| Existing component | Use in the lab |
| --- | --- |
| `cases.n5.rotating_release_paths` | Exact affine center paths, rational half-angle rotation, case inventory, and sample verification for R4/R5 |
| `cases.n5.tangent_cones` | Exact starting centers, coordinate indices, and the displayed `+W` direction retained by exp-035 |
| `cases.n5.second_order_obstruction` | Exact owner-3 and owner-4 contradiction coefficients and source scope |
| `sqpack.render.style` | The established square palette, paper theme, ink, container, and contact colors |
| `sqpack.verify` | Exact feasibility checks at the base, midpoint, and endpoint of every R4/R5 scene during manifest generation |
| Retained exp-035, exp-036, and exp-042 JSON | Evidence status, source identity, refusal boundaries, and byte-for-structure comparison with regenerated tangent, feasibility, and obstruction results |

No runtime or browser dependency was added.
The developer group now declares the Node wheel already used by BasedPyright, so the
test suite can execute the shipped JavaScript without relying on a system Node install.
The generated HTML contains its SVG, CSS, JavaScript, and motion data; it performs no
network requests and loads no external asset.

## Motion Data Contract

`devtools.packing_motion_studies.build_motion_lab_manifest()` produces
`packing.squares:MotionLab/v1`. The manifest is embedded as inert JSON inside the HTML.

| Field | Meaning |
| --- | --- |
| `field` | `Q(sqrt(2))`, its basis, and the exact coefficient encoding |
| `source_records` | Repository-relative exp-035, exp-036, and exp-042 result paths |
| `scenes` | Six certified-path scenes and three obstruction scenes in stable order |
| `container_side` | Exact low-degree coefficients plus a deterministic decimal projection |
| `centre_start` and `centre_derivative` | Exact affine center formula for each square |
| `orientation` | Fixed angle or the R4/R5 rational half-angle formula |
| `angle_derivative_at_zero` | Exact first-order angular velocity used by the tangent predictor |
| `contacts` | Separate base, open-interval, and endpoint physical-pair inventories |
| `evidence` | Status, source experiment, source record, and claim boundary |
| `branches` | Owner-specific exp-036 quadratic contradiction for `+W` |

An exact scalar stores `coefficients_low_degree_first` and a display decimal.
For this field, `[a, b]` means `a + b sqrt(2)`. Browser arithmetic uses the decimal
projection for drawing only; the retained research records and Python exact functions
own the claim.

The browser evaluates the analytic formulas at the scrubbed parameter.
It does not interpolate between a few endpoint polygons.
For R4/R5,

```text
c_i(u) = c_i(0) + u d_i
theta_1(u) = 2 atan(sigma u / 2)
0 <= u <= -1 + 3 sqrt(2) / 4
```

with `sigma = -1` for R4 and `sigma = +1` for R5.

## Visual and Evidential Grammar

| Mark | Meaning |
| --- | --- |
| Solid filled square | Source-backed pose on a certified R4/R5 path, or the fixed base pose in the `+W` view |
| Dashed cyan square | First-order tangent predictor; not an independently certified path |
| Dotted gray line | Center trail over the displayed parameter interval |
| Tempered-yellow center link | Source-declared contact-graph relation, not a physical gap segment |
| Red hatched badge | The displayed `+W` direction is obstructed at second order |

R4/R5 scenes carry `exact-universal-feasible-path`. This is a certificate for those six
explicit fixed-side paths, not a classification of all paths, stationarity, local
minimality, or global optimality.

The `+W` scenes carry `branch-exhaustive-second-order-obstruction`. Their dashed squares
show the linear prediction only.
The lab does not manufacture an acceleration or draw a quadratic pose.
It shows the base contact graph without asserting that any contact opens, persists, or
closes along a feasible `+W` motion.
The owner selector changes the displayed contradiction for the same geometry:

- owner 4 requires extra side `(sqrt(2)/8)t^2 + o(t^2)`; and
- owner 3 has a necessary upper-bound minus lower-bound residual `-(1/4)t^2 + o(t^2)` in
  the displayed common-angle specialization.
  The full branch also subtracts a positive margin times `|theta_3 - theta_4|`.

## Run and Check

From `explorations/packing/`:

```shell
uv run --frozen --all-extras --group dev python \
  -m devtools.render_packing_motion_lab \
  --output atlas/rendering/n5-motion-lab.html

uv run --frozen --all-extras --group dev python \
  -m devtools.render_packing_motion_lab \
  --output atlas/rendering/n5-motion-lab.html --check

uv run --frozen --all-extras --group dev pytest -q tests/test_motion_lab.py
```

The first command atomically regenerates the retained artifact.
The second is read-only and fails if the retained bytes differ.
The focused tests check:

- all six R4/R5 projections against the exact case functions at the base, midpoint, and
  endpoint;
- opposite R4/R5 rotation signs and the exact contact-event inventory;
- both exp-036 quadratic branch coefficients and the obstruction-only label;
- the browser pose, tangent, phase, parameter-label, scene-description, and
  control-state functions against all nine Python scenes at the base, midpoint, and
  endpoint;
- byte determinism and equality with the retained HTML;
- the no-network and no-dynamic-injection restrictions; and
- native controls, reduced-motion handling, accessible SVG text, and a no-script static
  fallback.

The ordinary full `packing-validate` run includes these tests through the project test
suite.

## Findings

The existing renderer supplied almost all noninteractive infrastructure: stable square
identity, color tokens, provenance rules, exact adapters, and a final-state fallback
convention.
Extending its CSS grammar was unnecessary and would have mixed an interactive
application with a document-safety profile.

The analytic R4/R5 formulas are a better browser boundary than sampled frames.
The motion remains smooth at any scrubber position, and the renderer does not need to
infer an angle or contact from pixels.
Center trails are affine; only square 1 uses the rational half-angle rotation.

The contact overlay exposed a useful distinction.
Experiment 042 records exact contact and owner-axis inventories, but the spike does not
yet compute moving physical contact segments.
It draws labeled graph edges between square centers and states that limitation next to
the figure.

## Limits and Unfinished Work

- The in-app browser available during the spike could not reach the task’s localhost
  server and blocked direct local-file navigation.
  Source, semantic, determinism, and interaction-structure checks passed, but this
  session did not complete browser-based visual inspection or click-through QA.
- The lab covers one exact `n = 5` family and one obstruction.
  It is evidence that the manifest boundary is useful, not yet evidence for promotion
  into `sqpack.render`.
- Contact links show graph incidence rather than physical contact points or segments.
- The tangent overlay shows a first-order pose predictor.
  It does not expose arbitrary gradients, Hessians, or unproved second-order
  accelerations from `exact_jets.py`.
- Static document export remains the existing safe SVG renderer.
  The HTML artifact is interactive research tooling and should not be embedded where
  scripts are forbidden.
- There is no video, GIF, raster, or presentation export.

## Disposition

Retain the spike in `devtools/` and the generated example in `atlas/rendering/`. Keep
the publication renderer unchanged.
Promote the scene contract into shared package code only after a second concrete motion
family uses it.

The next bounded follow-up should begin with visual QA in a browser that can reach the
artifact. If the UI survives that review, add one second source adapter before designing
a general jet layer.
Physical moving-contact geometry and portable static snapshots are separate follow-ups;
neither is required to use the current lab.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
