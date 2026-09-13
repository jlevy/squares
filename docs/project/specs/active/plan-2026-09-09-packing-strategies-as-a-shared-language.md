---
title: Packing Strategies as a Shared Language
description: Contracts for executable strategies, checked results, and illustrative animation across the workbench and research tools
author: Joshua Levy with agent assistance
---
# Feature: Packing Strategies as a Shared Language

**Updated:** 2026-09-12, against PR #155 head `6e191a35`, stacked on PR #125.

**Status:** Python executor and SVG adapters exist; shared browser execution and
semantic conformance are incomplete.
Contract repairs precede package extraction.

**Workflow:** W7 pipeline-improvement.
The [stack review](../../reviews/review-2026-09-12-workbench-stack-architecture.md)
records the findings and cross-plan sequence.

## Ownership and Current State

This plan owns what a strategy requests, what a run records, and how those records reach
a renderer. The workbench plan is the governing source for final product outcomes,
implementation order, and release acceptance.
Local phases here specify the contract work within that sequence, not an alternative
roadmap. The [workbench plan](plan-2026-09-11-workbench-from-spike-to-product.md) owns
the application and standalone package; the
[annealing plan](plan-2026-09-11-annealing-as-a-search.md) owns benchmark validity,
statistics, and the deferred Search mode; the
[video plan](plan-2026-09-07-known-best-atlas-video.md) owns illustration design and
capture deliverables.

| Surface | Present at the reviewed head | Remaining work |
| --- | --- | --- |
| Strategy description | `packing/strategies/packing-strategy.schema.yaml`, examples, and `devtools.packing_strategy.MECHANISMS` | Enforce accepted fields and record the complete executed configuration. |
| Python mechanisms | Scatter, grid, assemble, project, ratchet, relax, guide, container | Extract reusable algorithms from devtools; reject unsupported capabilities. |
| Animation interchange | `packing-animation.schema.yaml`, `animation_from_trace`, `export_animation_svg` | Validate geometry and provenance before assigning evidence; enforce time, identity, and cardinality. |
| Renderer | `sqpack.render` supports rotation and changing container side | Reuse its model, palette, and evidence distinctions through browser adapters. |
| Capture | `devtools.capture_video` captures the workbench page | Trace playback and page simulation are distinct paths; receipts must identify the path used. |
| Browser | Workbench and Motion Lab have their own runtime models | Workbench does not yet execute the shared strategy schema. |
| Rust | Search engine and experimental controls exist | No shared strategy executor is delivered by this stack. |

A schema file does not establish agreement among implementations.
In particular, `structure.source` accepts `record`, `given`, and `random`, while the
Python executor loads the retained record for every nonempty structure request.
Browser and Rust strategy readers remain future work.

## Phase 1: Repair the Contracts Before Reuse

**Beads:** `think-sdmi` and `think-karf`. These precede standalone package extraction,
`think-zisr`.

### Checked results and imported animation

`animation_from_trace.py` treats omitted `feasible` as true and creates a passing
numerical receipt. An import containing two coincident squares consequently exports with
`numerically-checked` metadata.
Imported claims must not create their own evidence.

- Validate finite coordinates, active square count, container side, pair separation, and
  wall containment before assigning numerical evidence.
- Keep unverified frames illustrative or candidate.
  Record the actual validator, arithmetic, tolerance, and result with checked frames.
- Distinguish raw simulation, repaired geometry, retained witness, and guided
  illustration. A repaired score belongs to the repaired arrangement.
- Validate retained-record references; a reference must not silently replace unrelated
  supplied geometry with a known answer.
- Preserve square identity, each frame’s own side, and monotone time.
  Adding a square needs explicit presence/arrival semantics.
  Padding an illustration with coincident waiting squares must not preserve a claim of
  feasibility.

Acceptance includes coincident squares, wall escape, omitted feasibility, nonfinite
poses, mismatched counts, and a retained valid packing as a positive control.
SVG and browser imports must refuse false evidence consistently.

### Executable strategy semantics

- Reject `source: given` and `source: random` until implemented, or implement them with
  explicit inputs. Record the source actually used.
- Enforce exactly `n` active poses at solver boundaries.
  A grid request whose side is too small must fail or return an explicitly infeasible
  arrangement of all `n` squares; it must not drop squares to fit.
- Audit admitted phase fields against their consumers, including stop conditions,
  targets, structural hints, and trace options.
  Unsupported choices fail before a run.
- Resolve the mismatch between the schema’s promised generated seed and the executor’s
  default zero. Record the actual seed, parameters, implementation, source revision,
  termination reason, and work counters; a strategy name cannot reproduce a run.
- Preserve use of guidance or retained answers through downstream phases.
  A relax phase cannot turn a guided start into an independent discovery.
- Keep intermediate container sizes in traces.
  The executor currently overwrites them with the final phase side when it constructs
  animation frames.

Acceptance is a small matrix of schema-valid requests that either execute as declared or
produce an explicit unsupported-capability error, plus adapter round trips.
Tests check behavior rather than the spelling of source code.

## Phase 2: Extract Algorithms and Adapters

**Depends on:** Phase 1 and the annealing plan’s record repairs.

The standalone package will live at `packages/workbench/` (`think-zisr`). The workbench
plan owns its tree and build acceptance.
Its boundary with Python is:

- Browser and Node consumers import the same JavaScript simulation modules.
  They accept plain state/configuration and produce state/events without a DOM.
- Python algorithms belong under `packing/src/sqpack/`, following its existing
  `research`, `render`, and `motion_lab` boundaries.
  Extract reusable functions from `divide_and_concur.py`, `run_projection_ratchet.py`,
  `known_structure.py`, and `packing_strategy.py` where current consumers justify them.
- Workbench-specific command parsing, benchmarks, capture, and build adapters move into
  `packages/workbench/tools/`. General-purpose research orchestration remains outside
  the package. Keep an old devtools wrapper only for a named consumer during migration,
  with an explicit removal condition.
- Export catalogue and palette data into an explicit, versioned input bundle.
  Ordinary browser and headless runs must not traverse spike paths or need a Python
  checkout.
- Adapt existing `sqpack.render.PackingTrajectory` and Motion Lab contracts at their
  boundaries rather than adding a third competing definition of evidence or identity.

Python projection and browser soft-contact simulation are different algorithms today.
Give each implementation an identifier and capabilities; a shared schema does not
promise identical trajectories.
Cross-implementation checks establish common invariants where the methods coincide.
The same JavaScript engine should have exact browser/Node parity for a fixed supported
runtime, seed, and step sequence.

## Phase 3: Animation Consumes Finished Frames

The animation engine consumes checked or explicitly illustrative sequences without
invoking a solver while drawing a frame.
Its clock is independent of wall time, so seeking, scrubbing, capture, and playback
request the same state.

Presentation controls include correspondence, easing, dwell/move/correct/settle timing,
palette, overlays, viewport, captions, and guided landing.
Run configuration includes proposals, force law, annealing schedule, repair policy, and
restart seed. An illustration may depict physics or interpolate retained records while
retaining its provenance.

Acceptance:

- Replay a recorded run without loading the solver.
- Draw a hand-authored illustration without requiring a benchmark record.
- Produce the same frame through seek and capture at the same time.
- Preserve feasibility and guidance in visible labels or the export’s accessible
  description.
- Represent changes in `n`, container side, and orientation explicitly.

## Phase 4: Optional Backends and New Mechanisms

After the portable engine and run contract pass, expose additional mechanisms through
adapters. The existing Python LP quench, projection/ratchet search, and Rust search are
candidates. Browser builds offer only methods that actually run there; local-service
methods are separately declared capabilities.

GitHub Pages serves the package build at `https://jlevy.github.io/squares/workbench/`.
It cannot execute Python or start a Rust process.
A local backend or future browser-compatible backend is optional, with a visible
capability check. Neither is a prerequisite for browser packing or replay.

New physics and optimization experiments follow the annealing plan.
Search remains deferred until record/statistics repairs, shared resolution, and package
extraction are complete.

## Validation and Migration Limits

Preserve browser lint/type checks, focused geometry controls, Pages build checks, and
renderer tests.
Add boundary tests for the defects above and route fast tests through the
existing [validation tiers](../../../../development.md#validation-tiers).

Keep temporary CLI wrappers until their consumers and reproduction commands migrate.
Remove obsolete probes through `think-cqfc`’s consumer audit.
Source archives, negative results, and research provenance remain research records;
generated pages, video, caches, and large raw trial streams remain outside Git.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
