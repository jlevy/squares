---
type: is
id: is-01m336y5tjaf1xvy8mh6mp2fad
title: Build a transition contract checker that measures every square's color path and the view, frame by frame
kind: feature
status: closed
priority: 0
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m32t2yc3xenfb97kxn844rc7
created_at: 2026-09-22T00:06:04.355Z
updated_at: 2026-09-22T01:18:11.338Z
closed_at: 2026-09-22T01:18:11.337Z
close_reason: "Built at 06029438e: transition_contract (pure rules: no third hue, hue turns only through grey, no lightness snap, no chroma bump, a one-way bounded view within and across steps, a box that grows only on the move's first frame, a scarlet arrival, still pairs that do not recolor, and a sweep that sampled nothing fails), check_transitions (probes/transitions/sweep.js at 60 fps; --all, --trace), console script squares-workbench-check-transitions, 18 unit tests over recorded fills, and wired into check_frontend so every pull request runs the 16 declared steps. The whole corpus passes: 323 steps, 38,637 frames. Join-window exemption left open as think-orbz."
resolution: null
duplicate_of: null
---
The systematic answer to a run of about ten visual regressions in one session (yellow mid-blend, grey flash, view jerk, vanishing red, red->green->red thrash, the whole grid flashing olive). Every one passed 206 Node tests, 341 Python tests and check_animate_view, because none of them check what the animation LOOKS like over time. Each was found by the owner watching, then diagnosed with one-off JavaScript run in a browser pane -- which is exactly the one-off measurement OR-1 forbids, and is why the same class of bug kept coming back.

Build it as a probe plus a Python check, run in the gate, so a change to colour or motion is measured against the invariants before anyone watches it:

- **No third hue.** For each square across a step, every sample above a chroma floor has a hue near its start hue or its end hue. A blend never shows a colour neither end has.
- **Symmetric crossing.** Chroma falls monotonically into a crossing and rises monotonically out of it, and the rise shows no hue the fall did not.
- **No view jerk.** The viewBox size is monotone within a step and across the step boundary, with a per-frame bound, and never reverses.
- **The box never grows** after its one instant at the move's start.
- **The arriving square is saturated scarlet** for a declared minimum number of frames, on a grid fill and on a matched step.
- **Still pairs do not recolour** squares that do not move.

The corpus sample must include the cases that broke: n = 8, 9, 10, 11 (grid fills and the 10->11 jerk), 49..53 (matched), 96..102 (grid-fill run), and a step where ceil(sqrt(n)) changes.
