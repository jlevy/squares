---
type: is
id: is-01m0vxjmmmmrfc9xr67ckahra5
title: "TUTORIAL: say what the quench map actually is—one algorithm, not a family"
kind: task
status: open
priority: 1
version: 4
spec_path: explorations/packing/docs/project/reviews/review-2026-08-25-tutorial-pedagogy-and-accuracy.md
labels: []
dependencies: []
parent_id: is-01m0vxe4ntpat4xcagtf04c37z
created_at: 2026-08-25T07:36:24.468Z
updated_at: 2026-08-25T08:01:33.249Z
---
§3 spends most of its length on what the quench is *not*—not a fixed-angle solve
(Trap 1), not a component classifier (Trap 2)—and gives the map itself one line:

> This project's quench is three stages: **solve the LP in the current cell → re-read
> the cell and re-solve to a fixed point → move the angles → repeat.**

Read as a newcomer, that sentence does not answer four questions it raises, and it
miscounts its own structure: stage 1 is the first iteration of stage 2's loop, and there
are **two** nested repeats, not one.
So a reader also cannot tell whether "the quench map" names a class of deterministic
refinements or one particular algorithm. It is one particular algorithm.

## The four questions, answered from `sqpack.research.quench`

**What type of solve is it?** A linear program, over `2n + 1` variables ordered
`[s, x₀…x_{n−1}, y₀…y_{n−1}]`. Containment is four inequalities per square against the
variable side. Separation is **one** inequality per pair—not four—because the cell fixes
the axis *and* the sign, and fixing the sign is exactly what removes the absolute value
and leaves something linear. Solved through `scipy.optimize.linprog` over HiGHS at a
pinned `1e-10` feasibility, with every returned solution re-checked against the rows it
was given rather than trusting the solver's success flag ([D-014](defects.md)).

**What determines the current cell?** `choose_cell` reads it off the *incoming pose*.
For each of the `C(n,2)` pairs it evaluates all four candidate axes—two edge normals
from each square—computes the signed gap `|d| − h` (centre difference projected on the
axis, minus the summed projected half-extents), and takes the axis with the greatest
separation, or least overlap, plus the sign saying which square is on the low side.
The cell is therefore a **function of the current configuration**, not an independent
input. That single fact is what makes stage 2 necessary, and the tutorial never states
it.

**What does "move the angles" mean?** Cyclic coordinate search over the merged angle
**classes**, one class at a time, each minimised by **golden-section search**
(`_bracket_min`) inside a window `span` that narrows only when a whole sweep fails to
improve. No derivative is used, deliberately: §4's corner makes a smooth local model
misspecified. An optional final free pass brackets each of the `n` angles individually,
to test whether a class-converged point is genuinely stationary or an artifact of the
merge tolerance `class_tol`.

**Repeat until when, and why?** Two loops:

- *Inner.* Solve, re-read the cell from the solution, repeat until `choose_cell` returns
  the same cell it was given—a **cell fixed point**—capped at 12 iterations.
  It can also stop *unsettled*, each with a typed reason retained as evidence: a cell
  cycle (which first attempts an adjacent-cell closure), a re-read that came back worse,
  an LP refusal, or the cap. An unsettled incumbent may be used as exploratory data;
  callers "may not call an outer quench converged from it".
- *Outer.* Sweep the angle classes until no sweep improves and `span` has shrunk below
  `span_min`, or `tol` is met, or `max_sweeps` (200—a backstop, not a budget) or the
  wall-clock `time_budget` runs out.

**Why the inner loop exists** is the missing "why", and the module docstring states it:
a single `solve_cell` optimises the cell suggested by the incoming centres, but its own
solution may lie in a *different* cell, so its value is a path-dependent upper bound.
That makes `s(θ)` ill-defined, and an angle search over an ill-defined objective
optimises a moving target—measured here as the cause of Powell and Nelder–Mead doing
worse than plain descent, which is the fact §4 reports without explaining.
Iterating to a cell fixed point removes the path dependence.

## Why this is a gap and not a detail

1. **The basin definition depends on the choice of refiner.** `SYNOPSIS.md` is
   explicit—a point-basin "is defined *relative to a specific quench*".
   Two refiners are two different maps and induce two different basin decompositions.
   The tutorial has two: `quench` descends on the angles, `quench_bracket` brackets, and
   §4 reports swapping one for the other moving `n = 5` from `3.4e-08` to `2.2e-15`—
   without noting that this changes what "basin" refers to in §3.
2. **It sharpens §3's own lesson.** §3 says whatever defines a basin "must be
   independent of the *search's* own knobs", then describes a quench that has knobs
   (`class_tol`, `span`, `span_shrink`, `tol`, `max_sweeps`, `time_budget`).
   The tension is real and already resolved in the record: [D-020](defects.md) is that
   defect, and the free pass exists precisely to test for merge-tolerance artifacts.
   Saying so turns an apparent contradiction into the point being made.

## Proposal

Replace the one-line summary with a short numbered account that separates the two loops,
names the solve as an LP in `2n + 1` variables, says the cell is read off the pose, says
the angle step is derivative-free bracketing over classes, and gives the
path-dependence reason for iterating to a fixed point.
Keep Stillinger–Weber as the *general* notion and mark this as one member of it, with
"basin" relative to it. Name that tolerances exist; leave their values to
`SYNOPSIS.md` and the module.
