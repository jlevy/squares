---
title: Packing Strategies as a Shared Language
description: One declarative document describing a sequence of optimisation strategies, executed by the Python tools, animated by the workbench, and later run by the Rust engine
author: Joshua Levy (github.com/jlevy) with Claude Opus 5 assistance
---
# Feature: Packing Strategies as a Shared Language

**Date:** 2026-09-09

**Author:** Joshua Levy, with Claude Opus 5 assistance

**Status:** Draft

## Overview

A **packing strategy** is a small declarative document naming a sequence of optimisation
phases: what to do first, what to do next, and when to stop each one.
Nothing hard-codes a sequence; a strategy is data, and the same document is executed by
the Python search tools, animated by the workbench, and — once it earns the cost — run
by the Rust engine.

This is the companion to the
[atlas video plan](plan-2026-09-07-known-best-atlas-video.md).
That plan is about what a viewer *sees*; this one is about what a run *is*. The
workbench becomes the place a strategy is watched and edited rather than a place where
an animation style is chosen from a fixed menu.

The shape comes from a measured decomposition.
Finding a good packing splits into two problems that want different mechanisms:

1. **Assembly.** Given a rough grouping or contact graph, put the squares into roughly
   that arrangement — the right neighbours touching, not yet the right angles.
2. **Tightening.** Given something roughly correct, squeeze it toward the smallest
   container, letting every angle drift as it must.

Both are measured below, and a single mechanism is good at one or the other, never both.

## Goals

- One JSON Schema for a strategy, in the repository’s existing `softschema` convention,
  so a strategy validates identically in Python, JavaScript and Rust.
- A mechanism registry that is the only place knowing how to run a phase, so a new
  mechanism or a faster backend is one entry rather than a rewrite.
- Strategies runnable headless for experiments and playable in the workbench for
  inspection, from the same document and the same recorded trace.
- Sweeps over *strategies*, not only over parameters: which sequence of strategies gets
  closest, measured against the known records.

## Non-Goals

- Not a new schema convention.
  The repository already validates `packing.squares:X/vN` contracts with `jsonschema`,
  and ships `jsonschema-rs` for the Rust side.
  Pydantic would be a third convention and a Python-first bias for a document whose
  whole point is being language-neutral.
- Not a rewrite of `sqsearch`. The Rust engine gains a strategy reader when the Python
  executor has proved which phases are worth having.
- Not a claim that any strategy reaches a record.
  Nothing here has crossed 1.2 per cent above the best known at `n = 11`.

## Background

### What has been measured

Every number below is from this branch and is reproducible from the tools named.

**A penalty force cannot produce a packing at all.** Across 48 runs of the workbench
physics, zero ended feasible; the least overlap anywhere was `0.0042` of a unit side,
and thirteen times the steps moved it from `0.004578` to `0.004570`. A penalty settles
where the springs balance the walls, and the residue there is pressure over stiffness.

**A projection always does.** Divide and concur searched with relaxed-reflect-reflect
ended on an exactly feasible packing in 28 of 28 runs, each re-checked out of process by
`sqpack.verify`. At `n = 5` it reached `2.7082031` against the proved `2.7071068`.

**Every mechanism tried is trapped by the trivial grid.** Each failed ratchet run used
exactly 48 solver calls — eight step halvings at six attempts, no acceptance between.
A grid of `k` squares in a row needs a container of exactly `k`, so the first tightening
makes the whole topology infeasible at once, with no small repair.

**Structure declared from a random start only costs.** Walking the constraint ladder
cold at `n = 11`: nothing packed 4 runs of 4, three declared edges packed 2, seven
packed 1, all fourteen packed none, and no rung ever reached tighter than 4 per cent
above the record. The control settles it — the true graph and a *rewired* graph of the
same size with wrong edges are indistinguishable, so only the constraint count was
registering.

**Because the search realises a contact graph degenerately.** Given `n = 11`’s graph and
a slack container, all fourteen declared contacts are satisfied and the result is
useless: every angle collapses to about 44 degrees and two *undeclared* squares end up
`0.012` apart, essentially stacked.
The graph is realised inside a 45-degree lattice.
Contacts made and worst overlap were identical at weights 1, 2 and 3, so this is not a
weighting problem.

**Building the groups inverts that.** A face-to-face contact is unambiguous — shared
orientation, centres one unit apart along a face normal — so the edge-edge subgraph can
be walked and laid out.
That builds 7 of 8 face contacts exactly at `n = 11` and 11 of 13 at `n = 17` before any
relaxation. Handing it to the same solver with the same declared contacts at the same
sides, changing only where the run starts:

| side | excess | random start | built groups | face contacts kept |
| ---: | ---: | :---: | :---: | :---: |
| 4.264792 | +10 % | 1/8 | **5/8** | 8 of 8 |
| 4.109709 | +6 % | 2/8 | **4/8** | 8 of 8 |
| 4.032167 | +4 % | 2/8 | **4/8** | 8 of 8 |

**And tightening is a separate problem that construction does not touch.** At +2 per
cent both arms are 0 of 8. That wall belongs to the *protocol*, not the search: a
fixed-side cold solve has no continuation, while the container ratchet, which tightens
gradually and carries each packing forward, had already reached `3.9234` (+1.2 per
cent). The two are not comparable, which is exactly why a strategy needs more than one
phase.

### What the records look like, which constrains what a phase may assume

- **Contact kinds carry the most information per bit.** An edge-edge contact pins a
  pair’s relative orientation to a quarter turn without naming an angle; a corner
  contact joins nothing.
  `n = 11` is 8 edge-edge of 14, `n = 17` is 13 of 24, `n = 26` is 42 of 50.
- **Orientations at the records are exact, not approximate.** Allowing half a degree,
  two degrees or five degrees collapses the angle-class count on only one of ten records
  tested.
- **Perturbed faces are real but not universal.** At `n = 5, 10, 11, 17, 26, 40` every
  corner contact joins squares 36 to 45 degrees apart — genuinely tilted.
  Slipped faces appear at the untidy records: seven of `n = 29`’s corner contacts sit at
  0.3 to 4.5 degrees, and two of `n = 37`’s at 2.9. A phase that assumes a perturbation
  will find none at 11 and 17.
- **Constraints must be bands, never equalities.** Declared exactly, the record becomes
  a *repelling* fixed point: from Trump’s own `n = 11` packing with its contacts
  declared, the drift is 0.0000 at 200 steps, 0.0012 at 1,000 and 0.2839 at 4,000,
  deterministically, at every relaxation above 0.1. Exact tangency makes the constraint
  sets meet non-transversally, the degenerate case the flow-limit result excludes.

## Design

### Approach

A strategy is a list of phases.
Each phase names a mechanism, carries that mechanism’s own parameters, and declares when
it stops. The executor threads one state — poses, container side, and the declared
structure — from phase to phase, and records a trace so the same run can be replayed.

```yaml
softschema:
  contract: packing.squares:PackingStrategy/v1
strategy:
  name: assemble-then-tighten
  n: 11
  phases:
    - mechanism: assemble
      structure: {source: record, use: face-contacts}
      side: {relative_to: record, factor: 1.12}
    - mechanism: project
      constraints: {contacts: face-contacts, band: 0.02, weight: 2.0}
      relaxation: 0.1
      until: {feasible: true, or_steps: 6000, or_stalled_for: 2000}
    - mechanism: ratchet
      constraints: {contacts: face-contacts, band: 0.02, weight: 2.0}
      schedule: {start: 0.05, halve_on_failure: true, floor: 1.0e-3}
      until: {stalled_for: 24}
    - mechanism: relax
      constraints: {band: 0.05, weight: 1.0}
      until: {stalled_for: 2000}
```

The `structure` block is the constraint ladder, and its rung is a field rather than a
separate code path: `partition`, `contact-graph`, `contact-graph-with-types`,
`with-wall-contacts`. A strategy says how much it was told, which is what makes a
comparison between strategies honest.

### Components

| Component | What it is |
| --- | --- |
| `packing/strategies/packing-strategy.schema.yaml` | What to do. Draft 2020-12, `oneOf` on `mechanism` so each phase validates against its own parameters. |
| `packing/strategies/packing-animation.schema.yaml` | What happened. Frames of poses and a container side on logical time 0 to 1, what the colours should mean but never the colours, and both reference bounds so a gap bar draws without consulting a register. |
| `packing/strategies/lab-components.yaml` and its schema | The lab's parts and what each reads. `environment` is load-bearing: seven are `static` and embed in a scriptless SVG, two are `interactive` and are excluded from the export by construction. |
| `devtools/packing_strategy.py` | Loads, validates, executes. Holds the mechanism registry — the one table that knows how to run a phase. |
| `devtools/known_structure.py` | Already built. Reads any of the 324 witnesses and yields a rung: contact edges, contact kinds, wall contacts, angle classes, thinned and rewired controls, and the constructive face assembly. |
| `devtools/divide_and_concur.py`, `run_projection_ratchet.py` | Already built. The `project` and `ratchet` strategies. |
| The workbench template | Reads a strategy and a trace, plays the phases with their own labels, and lets a phase be edited and re-run. |
| `sqsearch` | Later. Gains a strategy reader through `serde`; `jsonschema-rs` is already a dependency. |

### The registry is the seam

A mechanism is one entry: a name, a parameter schema fragment, and a function from state
to state. Adding the LP quench, an annealing phase, or a Rust-backed `project` is an
entry rather than a change to the executor, and the workbench discovers the available
phases from the schema rather than from a hard-coded menu.

That is also how the performance path stays honest.
A high-performance backend is a *different implementation of the same phase*, selected
by a field, so a strategy can be run in Python and in Rust and the two compared on the
same document.

### API Changes

`solve()` gains an optional trace sink, already added, so a run can be replayed frame by
frame. `ratchet()` already accepts `start_from`/`start_side`, which is what lets one
phase hand its arrangement to the next.

## Implementation Plan

### Phase 1: the contract and the Python executor

- [ ] Write `packing-strategy.schema.yaml` with the four phases that exist today —
  `assemble`, `project`, `ratchet`, `relax` — and the structure-ladder rungs as an enum.
- [ ] Build `devtools/packing_strategy.py`: load, validate, execute, record a trace, and
  emit a run record naming the strategy, the rung, the side reached and the excess over
  the record.
- [ ] Port the four measurements above into strategies, and check each reproduces its
  number. A strategy that cannot restate a result already measured is not yet a
  description of it.
- [ ] Sweep strategies rather than parameters at `n = 11` and `n = 17`, with the rewired
  and thinned controls beside every structured strategy.

### Phase 2: the workbench plays a strategy

- [ ] Load a strategy and its trace; play phases in sequence with per-phase labels and
  the container side shown against the record and the proved lower bound.
- [ ] Edit a phase and re-run, so a strategy can be explored by hand — which is the
  workbench’s original argument, since hand construction found 21 of the 36 non-grid
  cases below 100.
- [ ] Export an edited strategy back out as the same document the headless tools read.

### Phase 3: the atlas ascent, one square at a time

A single directed animation from `n = 1` to `n = 100`, adding one square per step and
landing each time on the retained record.
Directed on purpose: it is not a search, it uses the known endpoints, and the point is
that it is clean, legible and always arrives.

Every frame of it comes from a `guide` phase, so **every frame is labelled guided and
none of it is a search result**. That rule is not decoration.
The same instruments that make this animation possible are the ones used to report what
a search reached, and the two must never be confusable.

**The beat, per step from `n` to `n + 1`.** Five beats, and the middle three are the
ones that had to be measured rather than guessed.

| beat | what happens | why |
| --- | --- | --- |
| **Hold** | the packing at rest, labelled with `n`, its side, and whether it beats the grid | the viewer needs a still frame to read the fact off |
| **Enter** | the new square arrives from outside the container edge | it has to come from somewhere; dropping it in the middle starts the step already overlapping, measured at 0.83 of a unit side |
| **Open** | the container grows to whichever side is larger | the rearrangement needs room, and this is the beat that fixes the measured defect below |
| **Rearrange** | the guided phase drives every square to its matched target | matched, always: unmatched targets send each square to another’s place and they walk through each other |
| **Close** | the container contracts to the new record’s side, squares riding it down | the owner’s own design: add the square, reshuffle without scaling, then scale down |

**The defect this beat exists to fix, stated plainly.** A guided transition between two
*different* `n` is smooth and lands exactly -- residual `0.0004` to `0.0007`, largest
per-frame motion `0.013` to `0.016` -- but squares pass through each other on the way:
peak overlap `0.83` at 10 to 11, `0.49` at 11 to 12, `0.35` at 16 to 17, `0.86` at 17 to
18, with roughly 100 frames of 126 carrying some overlap.
Between two arrangements of the *same* `n` the same machinery is perfectly clean -- peak
overlap `0.0000` across every frame -- so the transit overlap is not the mechanism.
It is that adding a square is a genuine rearrangement with nowhere to do it.
**Open** and **Close** give it somewhere.

**What has to be built.**

- [ ] A `container` mechanism, so the side is a phase rather than a side effect of
  another one. **Open** and **Close** are that mechanism run twice with different
  targets.
- [ ] Correspondence across a change of `n`: 100 squares matched against 101 targets.
  The rectangular assignment already handles the shape; what it needs is a rule for
  which square is *new*, and the honest one is whichever target the assignment leaves
  over.
- [ ] The ascent as one strategy document per step, generated for `n = 1..100`, so the
  whole film is data and a single step can be re-run and re-watched on its own.
- [ ] Capture end to end: play the trace in the workbench’s Animate tab, record it, and
  write a receipt naming every strategy document and the record each step landed on.
- [ ] A guard in the capture path that refuses to export a frame from a guided phase
  without its label.

**What is deliberately not in it.** No search.
No claim about any `n`. The ascent shows what is known, and the
[video plan](plan-2026-09-07-known-best-atlas-video.md) owns how it looks; this phase
owns only that each step is a correct, clean, repeatable transition between two retained
packings.

### Phase 4: use the renderer that exists, and lift the two limits that stop it

The first draft of this phase said to extract a renderer. That was wrong, and checking
before building is what caught it: `sqpack.render` **is** the renderer -- `render_packing_svg`
with its own colour, style, contact and number modules -- and `sqpack.render.motion`
already emits **CSS-keyframe animated SVG** from a `PackingTrajectory`, which is very close
to the embeddable artifact this phase wants.

What is actually wrong is that the prototypes bypassed it. The v1 slideshow copies the
poster's colours and draws its own panels; the v2 workbench embeds pose JSON and draws in
JavaScript at run time. The motion lab uses `sqpack.render.numbers` and little else. So the
defect is not a missing renderer, it is four surfaces declining to share the one that
exists.

**Two restrictions block reuse, and they are stated in the code rather than implied.**
`validate_translation_only_trajectory` refuses a trajectory whose container side changes,
and refuses any frame where a square's angle differs from its final angle -- *"trajectory
rendering does not yet support rotation"*. Both are fatal here. Squares rotate: six of
`n = 11`'s fourteen contacts join squares 40.2 degrees apart. And the atlas ascent changes
the container at every step, by construction.

**So the work, in order.**

- [ ] Lift rotation. A CSS keyframe can carry `rotate` beside `translate`, so the frame
      model already has what it needs; what has to change is the validator, the keyframe
      emitter, and the choice of rotating the short way round a quarter turn.
- [ ] Lift the constant-container restriction, so a trajectory may resize. That is the
      `container` mechanism from Phase 3 seen from the rendering side.
- [ ] Feed a `PackingStrategy` trace into `PackingTrajectory`, which is the one adapter
      that turns everything already built into something watchable.
- [ ] Then the embeddable component: a trace in, one self-contained animated `.svg` out,
      no build step and no JavaScript, so it drops into the explainer page or any other.
      **This first, not a whole embedded motion lab** -- a component that can be dropped in
      is worth more than a lab that has to be hosted, and it is the smaller thing.
- [ ] A simplified interactive lab on the explainer page comes after, once there is
      something worth playing with.
- [ ] The video path is the same trace at a fixed size and rate, then an encoder, then a
      receipt. Capture cost is already measured: about 42 ms per frame at 1080p and 145 ms
      at 4K in the pinned headless browser, with repeated captures of one instant
      byte-identical, which is what makes the export reproducible and not merely repeatable.
- [ ] A guard on both exporters refusing a frame from a `guide` phase without its label.

### Phase 5: publishing, which is nearly free

**Yes, and most of it already runs.** `.github/workflows/pages.yml` builds and deploys
today, the repository is public, and the site lives at `https://jlevy.github.io/squares/`.
`packing/site/` is gitignored, so the page is rendered in CI and deployed rather than
committed -- which is the same rule the spikes follow, and the reason nothing here needs a
policy change to publish multi-megabyte artifacts.

**The explainer keeps its URL, and that is a requirement rather than a convenience.**
It is already published at `https://jlevy.github.io/squares/` and may be linked from
elsewhere, so nothing here moves `site/index.html`. Everything new is a *sibling
directory* beneath it, which leaves the existing page byte-identical and its address
untouched.

`upload-pages-artifact` takes `packing/site` whole, so **a subdirectory is a URL**:

| path | what | size today |
| --- | --- | ---: |
| `/` | the explainer | 1.1 MB |
| `/workbench/` | the workbench, its own URL | 3.1 MB |
| `/atlas/` | the slideshow | 3.5 MB |
| `/embed/n-011.svg` | one embeddable animation per case | small |

About eight megabytes against a soft limit of a gigabyte, so size is not the question.

**Three existing constraints decide the work, and all three are already enforced.**

*Self-containment.* The renderer refuses a page that references anything outside itself --
no external script or stylesheet, no CSS import, no `url()` that is not a data URI. The
workbench is already one self-contained file, and the embeddable SVG is designed to be, so
both clear it. It is also the reason the embed can be dropped into someone else's site at
all.

*Determinism.* The build renders twice and fails unless the two agree byte for byte. Both
spike generators already assert byte-identical regeneration, so this costs nothing to
adopt and is what makes a published animation reproducible rather than merely repeatable.

*The path filter.* The workflow only rebuilds when an input changes, and
`test_the_pages_filter_covers_every_render_input` compares that filter against
`RENDER_INPUTS` declared in the renderer. **A new generator must declare its inputs**, or
the test fails and names what is missing. That is a constraint worth having: it is what
stops a published page from going stale when the data under it moves.

**What has to be built.**

- [ ] A `site/workbench/` and `site/atlas/` build step, writing into the same tree the
      artifact already uploads, and never touching `site/index.html`. Simplest as another
      job whose output `build` collects before uploading, so a workbench failure cannot
      publish a broken explainer -- the existing page's checks stay exactly as they are and
      keep gating the deploy.
- [ ] A link from the explainer to `/workbench/`, which is the only change the existing
      page needs and the reason to give the workbench a stable address at all.
- [ ] `RENDER_INPUTS` entries for the two generators and their data, and the workflow's
      two `paths:` lists extended to match, which the test will confirm.
- [ ] The embed directory, one SVG per case, generated from traces.

**The one real caveat.** A 3.1 MB single file is a slow first load on a phone, and the
workbench carries all 323 transitions whether or not a visitor opens one. Splitting the
data from the page would fix it and would break self-containment, so if it matters the
answer is a smaller default payload -- the twenty-five-pair build already exists at 714 kB
-- rather than an external fetch.

## Testing Strategy

Every phase asserts the invariant it is responsible for, not an arrangement that
happened to come out of a run — the fault that broke five checks earlier on this branch.
`assemble` asserts the declared face contacts are exact before relaxation.
`project` asserts that whatever it calls solved is feasible under `sqpack.verify` out of
process. `ratchet` asserts the reported side is one at which a packing was found, never
smaller. Strategies in the repository are validated against the schema in the fast tier,
and the four reproduction strategies run in the slow tier.

## Open Questions

- Where does the LP quench enter — as a terminal phase on every strategy, or as a
  mechanism a strategy may schedule?
  The survey is explicit that the projection loop should not be asked for the final
  digits, and `n = 5`’s residual `0.0011` is entirely the ratchet’s floor.
- Should a phase be able to *fail over* to another, rather than a strategy being a
  straight line? The grid trap argues for it and nothing else does yet.
- Is there a phase between assembly and tightening that repairs the cycles greedy
  placement cannot close — 1 of 8 at `n = 11`, 2 of 13 at `n = 17`?
- Memory (`think-dh4k`) is a phase that needs a permutation-invariant coordinate before
  it can exist. Which of the contact-graph signature, angle-class census or chunk
  taxonomy is it?

## References

- [The atlas video plan](plan-2026-09-07-known-best-atlas-video.md), whose workbench
  this gives something to play
- [Simulation mechanisms survey](../../research/research-2026-09-09-simulation-mechanisms-for-packing.md)
- [Annealing survey](../../research/research-2026-09-08-annealing-for-square-packing.md)
- [exp-160](../../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-160-projection-search.md),
  the projection search’s first measurements
- [X-025](../../../../packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md),
  which carries the constraint ladder and the memory thread

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
