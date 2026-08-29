---
title: Generalized Square-Packing Motion Lab
description: Shared interactive scenarios for exact motions, setup-only snapping, and numerical quench traces
author: Codex, for the project maintainer
---
# Feature: Generalized Square-Packing Motion Lab

**Date:** 2026-08-25 (last updated 2026-08-26)

**Author:** Codex (agent), for the repository maintainer

**Status:** Phase 1 complete; Phase 2 paused pending explicit constraint semantics

**Workflow:** W7 pipeline improvement

**Tracking:** `think-23td`

## Overview

Turn the narrow `n = 5` motion spike into a small family of square-packing labs without
building a separate user interface for every experiment.
One shared shell will own square rendering, scenario selection, editing, playback,
evidence labels, solver-phase explanations, and the visual system.
Scenario adapters will supply the geometry and behavior.

The first new scenario is a **setup-only snap-and-quench playground**. The user may set
the square count and container side, randomize a seeded starting pose, drag or rotate
individual squares, and snap touching squares into temporary Tetris-like chunks.
Chunks move and rotate together while the user prepares the starting configuration.
When the user starts the quench, the lab discards every snap relationship and sends only
the squares’ positions and angles to the existing unconstrained optimizer.

The lab will then show the quench as a typed sequence rather than as one
undifferentiated animation.
Fixed-angle linear-programming work, angular search, cell changes, accepted states,
rejected probes, and the final stop will have different labels and motion grammar.
The retained solver states are numerical evidence; display interpolation between them is
not silently presented as a feasible continuous path.

Later scenarios may preserve a contact or a whole rigid group during optimization.
Those modes require an explicit constraint model and are outside the first delivery.

## Goals

- Provide one shared Motion Lab shell and a small scenario interface so exact paths,
  numerical quenches, and later constraint experiments reuse the same components.
- Keep the current exact `n = 5` release-path and obstruction study as a known-answer
  scenario with its existing evidence boundaries.
- Add a setup-only snap workflow for quickly assembling touching clusters at arbitrary
  square angles.
- Release all editor snap groups when optimization starts; the first numerical scenario
  remains the existing unconstrained quench.
- Support seeded random starts with a user-selected square count and starting container
  side, plus direct position and angle editing.
- Record and replay the quench’s existing decisions without adding solver calls or
  changing its endpoint.
- Make the fixed-angle LP and rotational search visibly and textually distinct.
- Reuse the established 20-color square palette, pure-black packing boundaries, and
  tempered-yellow contact color from the publication renderer.
- Adapt the compact typography, neutral surfaces, 6 px radii, border treatment, focus
  states, and restrained buttons from `tbd web` into a repository-owned Motion Lab
  theme.
- Keep every retained artifact deterministic and self-contained when its scenario does
  not need a live numerical backend.
- Preserve claim status: an exact path, a numerical solver state, an editor preview, and
  an illustrative tween must never share an unlabeled visual treatment.

## Non-Goals

- Replacing or weakening the script-free publication SVG renderer.
- Claiming that quench output is exact, optimal, or a certified continuous motion.
- Keeping setup snaps active during the first quench implementation.
- Solving rigid-body, contact-equality, hinge, rolling-contact, or magnetic-penalty
  optimization in Phase 1.
- Completing the basin-atlas explorer tracked by `think-djvs`.
- Porting the Python quench to JavaScript or adding a browser build framework.
- Adding a general-purpose canvas, diagramming, or game engine.
- Copying `tbd`’s bead-specific table, filter, tag, or status components into this lab.
- Using rounded cards, gradients, shadows, or color as decoration.

## Background

The [implemented spike](spike-2026-08-25-n5-motion-lab.md) proves that a generated,
self-contained HTML+SVG document can replay analytic square motions, show source-backed
contacts and first-order predictors, and keep exact and illustrative geometry separate.
It covers one specialized `n = 5` family.
Its CSS, controls, timeline behavior, and scene logic are still embedded in one
generator, so another scenario would currently repeat much of that work.

The numerical backend already has the two operations the new scenario needs:

1. [`solve_to_fixed_point()` and `solve_cell()`](../../../../packing/src/sqpack/research/quench.py)
   hold every angle and one separating-axis cell fixed while an LP minimizes the
   container side and square centers.
2. [`quench()` and `quench_bracket()`](../../../../packing/src/sqpack/research/quench.py)
   change angles outside that LP, re-solve the fixed-angle problem, and return typed
   counters and stop reasons.

[`deterministic_start()`](../../../../packing/cases/campaign_smoke/basin_events.py)
already draws seeded centers and angles inside a requested starting side.
The draw may overlap; that is useful behavior to expose honestly rather than hiding it
behind a picture of a feasible packing.

The quench currently returns its endpoint and aggregate counters, not the accepted
states and phase events needed for an explanatory animation.
The implementation therefore needs observation hooks around existing work, not a second
optimizer.

## Design

### Product Model: One Shell, Several Scenarios

The Motion Lab will separate a shared shell from scenario-specific behavior.

| Scenario | Source | User operations | Output and evidence |
| --- | --- | --- | --- |
| Exact `n = 5` motions | exp-035, exp-036, exp-042 and exact case functions | choose R4, R5, or `+W`; select stratum; scrub or play | exact certified paths or a labeled first-order predictor and second-order obstruction |
| Setup-only snap and free quench | edited or seeded floating-point poses plus the existing quench | randomize, drag, rotate, snap into chunks, release and run | typed numerical trace and independently checked endpoint |
| Persistent contacts (later) | explicit user-authored contact constraints | choose which contacts survive the run | constrained numerical trace; no exactness claim without separate evidence |
| Rigid groups (later) | explicit relative transforms within selected groups | translate or rotate glued polyomino-like bodies | constrained numerical trace with named rigid-group semantics |

The current exact artifact remains at its stable path.
A general lab entry point may offer all installed scenarios, while a deep link or
generated standalone artifact opens one scenario directly.
Both entry points use the same source assets and component code.

### Shared Components

The second scenario justifies promoting the reusable pieces out of the spike generator.
The target layout is:

```text
src/sqpack/motion_lab/
  contracts.py              versioned scenario, frame, and trace types
  snap.py                   setup-only contact candidates and group editing
  trace.py                  quench observer and trace serialization
  scenarios/
    exact_n5.py             adapter for the retained analytic studies
    free_quench.py          editor seed and numerical-run adapter
  assets/
    motion-lab.css          shared visual tokens and components
    motion-lab.js           stage, editor, timeline, and scenario controller

devtools/
  render_packing_motion_lab.py  deterministic standalone artifact builder
  serve_packing_motion_lab.py   loopback-only numerical service
```

The exact file names may change during implementation, but the ownership boundaries do
not:

- **Scenario registry:** lists scenario identity, evidence kind, supported controls,
  initial state, and runner type.
- **Stage renderer:** draws the container, squares, selection state, contacts, trails,
  axis hints, and phase overlays from one common pose-frame type.
- **Setup editor:** owns selection, pointer and keyboard movement, rotation, snapping,
  group membership, reset, and deterministic randomization.
- **Timeline:** consumes analytic parameter values or recorded solver events and exposes
  play, pause, restart, step, and scrub with reduced-motion behavior.
- **Evidence panel:** displays scenario source, frame kind, feasibility status, solver
  phase, stop reason, and the limits of the current mark.
- **Transport:** calls the loopback numerical service only for scenarios that declare
  that capability. Exact standalone scenarios perform no network request.
- **Theme:** imports square identity colors from `sqpack.render.style` and owns the
  separate compact UI tokens described below.

The browser code uses the capability declaration to reveal controls.
It does not contain scenario-name conditionals spread through rendering and interaction
code.

### Shared Scenario Contract

The shared shell consumes three runner shapes:

- **Analytic:** a scenario evaluates a pose and evidence at any declared parameter.
- **Recorded:** a scenario supplies ordered `TimelineEvent` values for replay.
- **Interactive solver:** a scenario edits an initial pose, submits a run request, and
  receives a recorded trace that the same timeline replays.

All three normalize to the same visible frame fields:

| Field | Meaning |
| --- | --- |
| `scenario_id` | stable scenario key |
| `frame_kind` | editor preview, exact path, numerical state, probe, or illustrative tween |
| `container_side` | source value and browser projection where available |
| `squares` | stable IDs, centers, angles, and established palette indices |
| `phase` | setup, fixed-angle LP, angular search, cell change, stop, or analytic path |
| `evidence` | source and claim boundary for the frame |
| `overlays` | typed contacts, trails, tangent marks, cell axes, or selection marks |

The shell may hide an unsupported control, but it cannot infer stronger evidence from a
scenario’s geometry.

### Setup-Only Snap Behavior

Snapping is an editor operation over rigid poses.
It does not add an optimizer constraint.

1. Ordinary drag translates the selected square or existing editor group.
2. Near a stationary square or container wall, the editor enumerates exact-contact
   translations along the separating-axis normals of the moving and stationary squares.
3. The editor keeps candidates within the normalized snap threshold, rejects a candidate
   that introduces an overlap with a nonmember, and chooses one deterministically by
   pointer displacement, stationary ID, moving ID, axis order, and sign.
4. The chosen translation moves the whole selected group and sets the contact gap to
   zero at browser precision.
5. The two editor groups merge.
   Later ordinary drags translate the merged group as one temporary chunk.
6. Shift-drag or the visible rotation handle rotates the selected chunk about its
   centroid while preserving member-relative transforms.
   Keyboard controls provide the same operation without requiring a pointer modifier.
7. Rotating or translating may expose another valid snap candidate and merge two chunks.
8. A visible **Snapping** toggle allows free placement.
   Manual or seeded starts may still contain overlap; the lab marks that condition
   rather than silently repairing it.
9. **Run quench** displays a release confirmation in the run summary, discards the group
   graph, and submits only `side`, `x`, `y`, and `theta` plus explicit solver settings.

The interface must say “setup groups release when optimization starts” beside the run
control and in the trace’s initial event.
The service rejects editor group or contact-lock fields in the Phase 1 run payload, so a
front-end bug cannot accidentally turn a setup aid into a scientific constraint.

### Random Starts and Direct Editing

The free-quench scenario starts with explicit controls for:

- square count `n`;
- starting container side;
- integer seed;
- solver and declared numerical budget; and
- snapping on or off.

Randomize uses the existing deterministic proposer semantics and records the inputs in
the trace. The service declares the tested `n` and budget envelope instead of promising
that every larger instance is interactive.
Known-answer acceptance covers at least `n = 5`, `n = 10`, and `n = 11`.

Direct editing supports square selection, translation, continuous angle adjustment,
reset to the last seed, and a readable pose table.
Numerical values use radians in the contract and may show degrees in the interface.
The lab folds equivalent square angles into `[0, pi/2)` before a run, matching the
quench’s square symmetry.

### Quench Trace and Phase Grammar

Tracing observes the existing solver path.
It must not run an additional LP, change iteration order, alter tolerances, or introduce
a new stopping rule.
With tracing enabled or disabled, endpoint arrays, counters, convergence, and stop
reason must match.

`QuenchTrace/v1` records:

- the initial edited pose and the fact that setup groups were released;
- each fixed-angle fixed-point result already computed by the solver;
- angular probes and whether each was accepted, rejected, unsettled, infeasible, or cut
  off by budget;
- accepted angle updates;
- separating-cell changes and a stable digest of the selected axes;
- objective side, centers, angles, solver counters, and elapsed work at each retained
  state; and
- the typed final result plus an independent feasibility check.

The UI uses both words and motion shape to distinguish phases:

| Phase | What is mathematically changing | Display rule |
| --- | --- | --- |
| Fixed-angle LP | centers and container side change while all angles stay fixed | solid squares translate and the container edge moves; persistent label `LP · positions + side`; same-cell endpoint interpolation may be marked feasible because that cell is convex |
| Angular probe | one square or angle class is proposed, followed by a fixed-angle solve | dashed orientation ghost and arc mark; label `ANGLE · proposal`; rejected probes appear as timeline ticks rather than replacing the accepted pose |
| Accepted angle step | the solver retains the proposed angle and its LP-settled pose | commit the dashed ghost to solid, then enter the next LP event |
| Cell change | one or more pairwise separating axes change | discrete `CELL` marker and optional axis overlay; do not imply a continuous cell-preserving path |
| Stop | the solver converges, reaches a budget, refuses a cell, or hits a limit | persistent typed outcome with counters and independent check status |

Only retained solver evaluations are numerical frames.
Rotation between sampled angles and any cross-cell tween are visual interpolation unless
separate evidence proves a feasible path.
The timeline and evidence panel label such frames `illustrative tween` and allow users
to step directly between authoritative states.

### Visual System

#### Packing Geometry

[`src/sqpack/render/style.py`](../../../../packing/src/sqpack/render/style.py) remains
the source of truth for packing marks.
The lab imports or serializes these tokens; it does not keep a second handwritten
palette.

```text
#378c3f  #00aeee  #c1a0fb  #00b393  #3d63be
#78d7d6  #877deb  #9fce85  #0096b1  #854888
#83c4ff  #3bb360  #008376  #7acfe9  #0079bf
#86a2ff  #865eb1  #7fd6b1  #00afb9  #c18dd8
```

- Square fills use that sequence by stable square ID.
- The container and every square boundary use pure black.
- Tempered yellow `#e3c64a` remains reserved for source-backed or computed physical
  contacts.
- Square identity is never encoded by the UI accent or solver-phase colors.
- Labels remain available so color is not the only identity channel.

#### Interface Chrome

The UI token subset is adapted from
[`tbd`’s authoritative web stylesheet](https://github.com/jlevy/tbd/blob/bed816dca101de6e646c8573a292884064652b6b/packages/tbd/src/web/styles.css)
at commit `bed816dca101de6e646c8573a292884064652b6b`. The source is MIT licensed and
owned by the same repository maintainer.
This plan copies the values needed for portability; implementation must not depend on
the local `/Users/levy/wrk/github/tbd` checkout.

| Role | Motion Lab token |
| --- | --- |
| page background | `hsl(215 0% 100%)` |
| secondary panel | `hsl(220 20% 97%)` |
| border | `hsl(215 15% 87%)` |
| text | `hsl(215 20% 10%)` |
| muted text | `hsl(215 9% 43%)` |
| focus and selected control | `hsl(220 82% 55%)` |
| information | `hsl(211 72% 42%)` |
| success | `hsl(149 68% 30%)` |
| warning | `hsl(38 82% 36%)` |
| error | `hsl(0 64% 46%)` |
| sans stack | `system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif` |
| monospace stack | `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace` |
| type scale | 15 px title, 14 px body, 12 px compact chrome/data |
| weights | 500 repeated labels, 650 headings and selected primary state |
| radius | 6 px |
| UI transition | 150 ms `ease`; 1 ms under reduced motion |
| focus | 2 px accent outline with 1 px offset |

Component rules carry more weight than the literal tokens:

- Use one page surface, thin dividers, and a compact toolbar.
  Do not wrap every section in a large rounded card.
- Use 6 px radii for controls and floating panels.
  A full pill is reserved for bounded operational state such as `running`, `paused`, or
  `stopped`.
- Desktop text controls use compact `4px 8px` padding.
  Coarse-pointer layouts raise the hit target to 44 px without making the desktop
  interface bulky.
- Icon-only controls are borderless at rest and show a panel background and border only
  on hover, focus, or an open state.
- Sans text describes the interface.
  Monospace is reserved for square IDs, angles, objective values, cells, run IDs, source
  paths, and solver counters.
- Small uppercase section labels use the 12 px compact scale and modest `0.04em`
  tracking.
- Shadows are limited to temporary menus or tooltips.
  The stage, toolbar, timeline, and readout use borders and spacing.
- Color is semantic. Phase names, icons, line patterns, and text carry the distinction
  when color vision or monochrome output removes the hue.
- UI motion describes a view change.
  Solver/data motion describes a retained numerical event.
  Reduced-motion users can step and scrub every authoritative state with animation
  collapsed to 1 ms.

The existing spike’s 18 px cards, 10 px buttons, oversized heading, and separate neutral
palette are replaced when it moves onto the shared shell.

### API Changes

The Python surface is additive.
Names below are directional; implementation may adjust them while preserving the
contracts.

```python
trace = quench_bracket(
    x,
    y,
    theta,
    time_budget=budget,
    observer=trace_observer,
)

scenario = ScenarioDefinition(
    id="free-quench",
    runner="interactive-solver",
    capabilities={"edit", "snap-once", "randomize", "quench"},
)
```

The loopback service exposes a narrow same-origin API:

- `GET /` returns the generated shared shell and embedded scenario inventory.
- `POST /api/quench` accepts a versioned run request and streams or returns
  `QuenchTrace/v1` as newline-delimited JSON.
- The server binds to loopback only, performs no remote request, enforces the declared
  `n` and numerical budgets, and returns typed failures.

Standalone exact artifacts inline their scenario data, CSS, and JavaScript and keep
`connect-src 'none'`. The served numerical profile changes the policy only to permit
same-origin loopback requests.

## Implementation Plan

### Bead Map

`think-23td` is the implementation epic.
The first seven children implement and validate Phase 1. `think-mn9j` is paused because
this plan requires a separate semantic decision before persistent constraints become
implementation work.

| Bead | Deliverable | Blocked by | Status |
| --- | --- | --- | --- |
| `think-9yz7` | Shared scenario, pose-frame, request, event, and trace contracts | — | Complete |
| `think-2f8m` | Zero-behavior-change quench trace observation | `think-9yz7` | Complete |
| `think-no7o` | Shared shell, compact theme, and exact `n = 5` migration | `think-9yz7` | Complete |
| `think-5t0r` | Setup-only snap geometry and editor-group reducer | `think-9yz7` | Complete |
| `think-la6m` | Loopback free-quench service and deterministic replay | `think-9yz7`, `think-2f8m` | Complete |
| `think-0l1y` | Free-quench editor and phase-aware trace playback | `think-no7o`, `think-5t0r`, `think-la6m` | Complete |
| `think-kcdq` | Known-answer, browser, accessibility, documentation, and full validation | `think-0l1y` | Complete |
| `think-mn9j` | Phase 2 semantic gate for persistent contacts and rigid groups | `think-kcdq`; paused | Paused |

### Phase 1: Shared Shell and Setup-Only Snap-and-Quench

- [x] Extract shared pose, scenario, timeline, stage, controls, evidence, and theme code
  from the current spike without changing its mathematical claims.
- [x] Generate the stable exact `n = 5` artifact through the shared shell and retain its
  analytic formula and Python/JavaScript parity controls.
- [x] Add the free-quench scenario with seeded random starts and direct pose editing.
- [x] Implement deterministic setup-only snapping, temporary editor groups, group
  translation, Shift-drag/handle rotation, keyboard equivalents, reset, and a snapping
  toggle.
- [x] Release all group metadata at run start and reject constraint fields at the Phase
  1 service boundary.
- [x] Add zero-behavior-change trace observation to the existing quench and serialize
  typed phase events.
- [x] Render LP, angular-search, cell-change, accepted, rejected, and stop events with
  the phase grammar in this plan.
- [x] Add the compact shared visual theme using the existing packing palette and the
  documented `tbd web` token subset.
- [x] Save or download a deterministic run request and trace so another agent can replay
  a reported behavior without local memory.
- [x] Document the serve, regenerate, replay, and validation commands in the rendering
  README.

Phase 1 acceptance requires an end-to-end run from an assembled editor chunk, proof that
the chunk releases before the quench, a replayable trace, distinct LP and rotation
presentation, and an independently checked endpoint.

#### Phase 1 validation receipt

Phase 1 passed its merge checkpoint on 2026-08-26:

- 40 focused Motion Lab tests covered the versioned contracts, unchanged traced and
  untraced quench endpoints, exact `n = 5` compatibility, snap geometry, group release,
  loopback request validation, canonical replay, browser reducers, reduced-motion
  behavior, and the CSS token contract.
- The retained one-square transport fixture regenerated byte for byte as a 144-event
  trace, replayed through the command-line path, and ended at a packing accepted by the
  independent separating-axis verifier.
  It is a pipeline control, not a packing result.
- Real-browser QA assembled a two-square chunk, translated and rotated it through both
  visible and Shift-drag controls, released it before the run, distinguished fixed-angle
  LP states from angular probes and accepted rotations, and kept a 769-event trace to 42
  simultaneous timeline controls.
  Wide and narrow layouts had no control overflow, and the browser console remained
  clean.
- The ordinary full `packing-validate` gate passed all 32 stages in 274.95 seconds of
  wall time. Its 166 behavioral tests, 83 deterministic SVG controls, exact `n = 5`,
  `n = 10`, and `n = 11` verification lanes, 67 negative controls, schema checks, defect
  reconciliation, and documentation checks all passed.

Browser inspection exposed D-348: expanding every low-level solver event into a DOM
control made long traces unwieldy.
The repaired timeline renders a 41-event moving window and samples autoplay while
retaining every event for stepping, download, and replay.

A senior engineering review before merge found six further defects, all of them in the
new instrument and none in the quench, the verifier, or the exact scenario: D-350 (a
rejected run left the previous trace downloadable), D-351 (replay promised byte fidelity
and checked semantics), D-352 (a timeline counter changed meaning on the stop event),
D-353 (the release note named a solver input the solver never receives), an unguarded
second implementation of the snap reducer in the browser, and a loopback service that
trusted its own bind against DNS rebinding.
All six are fixed, each with a control that fails without the fix, except where the
defect is prose about a boundary rather than a computed value.
The review also surfaced D-349 in `quench_bracket` itself, which is deferred to its own
round under `think-7dwo` because correcting it changes numbers the engine has already
reported.

Phase 1 therefore lands as a working but very new instrument.
It has produced no research result, its contracts are versioned in the expectation that
they will change, and the defect distribution above is the honest statement of its
maturity: the parts with years of controls behind them held, and everything written in
the last few days needed a review pass to be trusted at all.

### Phase 2: Explicit Persistent Constraints

- [ ] Specify separate `contact-lock` and `rigid-group` contracts; a setup snap does not
  become persistent unless the user explicitly promotes it.
- [ ] Show every active constraint in geometry, controls, request data, trace events,
  and exported replay.
- [ ] Add constrained fixed-angle and angular-search formulations with typed
  infeasibility and degree-of-freedom checks.
- [ ] Compare constrained results with the unconstrained control from the identical
  starting pose.
- [ ] Add a constraint scenario only after independent geometry and solver controls
  establish what “stays touching” and “stays rigid” mean at edge, vertex, and wall
  contacts.

Hinges, rolling contacts, and soft magnetic penalties need separate plan amendments if
the two explicit constraint types do not answer the geometric questions.

## Testing Strategy

### Shared Shell and Scenarios

- Run the existing exact `n = 5` source, formula, evidence, and JavaScript parity checks
  through the new scenario adapter.
- Prove that every scenario uses the same palette assignment, stage renderer, timeline,
  control primitives, and evidence panel.
- Test capability-driven control visibility so scenario additions do not add scattered
  scenario-name branches.
- Retain byte determinism and the no-network policy for standalone artifacts.

### Setup Editor

- Use known-answer edge-edge, vertex-edge, wall, arbitrary-angle, group-merge, and
  deterministic tie cases for snap geometry.
- Check that the chosen snap has zero displayed gap within the declared browser
  tolerance and introduces no new nonmember overlap.
- Check that translating and rotating a chunk preserves every member-relative transform.
- Check pointer, Shift-drag, visible-handle, and keyboard paths against the same editor
  state reducer.
- Mutate the snap threshold, candidate ranking, rotation pivot, and group release to
  prove each control can fail.

### Numerical Trace

- Run tracing on and off from identical starts and require equal endpoint arrays,
  counters, convergence, and stop reason.
- Replay trace counters against the solver’s aggregate counters and require ordered,
  complete terminal events.
- Reject a request containing editor groups or persistent contacts in Phase 1.
- Verify the final pose independently with the existing numerical verifier and retain
  its tolerance and result.
- Cover converged, budget, infeasible, unsettled-cell, solver-failure, and
  user-cancelled outcomes.
- Prove that rejected angle probes do not replace the accepted stage pose.

### Visual and Interaction Review

- Check the exact 20 square colors, black boundaries, and tempered-yellow contact token
  against `sqpack.render.style` rather than against a copied expected list alone.
- Add a CSS contract that rejects large card radii, ad hoc font sizes, decorative
  shadows, and color literals outside the Motion Lab token block and square-palette
  injection.
- Test wide, narrow, keyboard-only, coarse-pointer, reduced-motion, and no-script exact
  views.
- Manually inspect drag, snap, group rotation, run release, LP playback, angular
  playback, timeline stepping, focus order, and text contrast in a real browser.
- Keep phase text and line patterns understandable in a monochrome screenshot.

The ordinary full `packing-validate` command remains the merge checkpoint.

## Rollout Plan

1. Land the shared shell with the exact `n = 5` scenario as the compatibility control.
2. Add the setup-only free-quench scenario and loopback service behind an explicit
   developer command.
3. Retain one small deterministic numerical trace as a replay known answer; do not
   retain arbitrary user runs by default.
4. Promote the general lab in the atlas and project README after browser QA and the full
   validation gate pass.
5. Start Phase 2 only through an updated spec and implementation beads that name the
   intended constraint semantics.

Numerical results discovered in the lab are candidates.
They enter the research corpus only after export, independent verification, provenance,
and the ordinary campaign record rules.

## Open Questions

- What tested `n` and solver-budget envelope gives acceptable interactive latency on the
  supported development machines?
  The service must publish the measured envelope before the control is labeled general.
- Should live runs stream each trace event as it occurs or return a completed trace for
  immediate replay? Phase 1 may choose either transport, but the stored `QuenchTrace/v1`
  bytes and UI behavior must be the same.
- Which physical-contact representation should Phase 2 preserve: one selected SAT-axis
  equality, a named vertex-edge incidence, or a full contact manifold?
  No persistent contact mode ships until that choice has independent controls.

## References

- [Interactive `n = 5` Motion Lab spike](spike-2026-08-25-n5-motion-lab.md)
- [Retained `n = 5` lab](../../../../packing/atlas/rendering/n5-motion-lab.html)
- [Deterministic SVG rendering plan](plan-2026-08-24-deterministic-svg-rendering-toolkit.md)
- [Packing rendering guide](../../../../packing/atlas/rendering/README.md)
- [Existing quench implementation](../../../../packing/src/sqpack/research/quench.py)
- [`tbd web` UI source at the inspected commit](https://github.com/jlevy/tbd/blob/bed816dca101de6e646c8573a292884064652b6b/packages/tbd/src/web/styles.css)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
