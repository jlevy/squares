---
type: is
id: is-01m0vxhwqe5yfntb1697t5rk15
title: "TUTORIAL: write the linear program explicitly and add LP background"
kind: task
status: open
priority: 1
version: 4
spec_path: explorations/packing/docs/project/reviews/review-2026-08-25-tutorial-pedagogy-and-accuracy.md
labels: []
dependencies:
  - type: blocks
    target: is-01m0vxns5mzy4axt8mdrhaachj
parent_id: is-01m0vxe4ntpat4xcagtf04c37z
created_at: 2026-08-25T07:35:59.982Z
updated_at: 2026-08-25T08:01:31.984Z
---
The cell decomposition (**T-2**) is the tutorial's central structural claim, and §2
presents it as four bullet points plus an assertion. Two things are missing: the program
itself, and any context for why "it is a linear program" is good news.

## The program is never written

§2 gives one constraint row—`0 ≤ xᵢ + oᵢₖ,ₓ ≤ s`, with `o` undefined (see think-8hdt)—
and then asserts the result. The separation row, which is the interesting half, appears
only in [`SYNOPSIS.md`](SYNOPSIS.md#why):

> for axis `ν` and order `(i before j)`, `⟨ν, (xᵢ,yᵢ) + oᵢₖ⟩ ≤ ⟨ν, (xⱼ,yⱼ) + oⱼₗ⟩` for
> all `k, l`

A reader of the tutorial alone never sees what a separation constraint looks like, so
"separation along a fixed axis is a linear inequality" has to be taken on faith—and it is
the step the whole decomposition turns on.

Write it in full: objective, variables, containment rows, separation rows, and which
quantities are constants because the angles and the cell are fixed.
State the shape too. At `n = 11` there are `2n + 1 = 23` variables (the tutorial
evaluates `3n + 1 = 34` but never `2n + 1`), and the row count depends on how separation
is written: the synopsis records 1 row per pair in `sqpack.research.quench` versus
`1,056 = 16 × (11 + 55)` in `cases.trump11.independent_lp_cell`, two correct
formulations of the same feasible set.
That contrast is worth keeping—it shows the reader that "the LP" is a modelling choice,
not a canonical object.

Also give the cell count, which the tutorial implies but never states: four candidate
axes times two orders is eight choices per pair, so `8^C(n,2)` cells, `8^55 ≈ 10^49` at
`n = 11`. That number is what makes "all the nonconvexity is in the angles and the
discrete choice of cell" land as a statement about difficulty rather than a reassurance.

## No LP context, and §4 silently depends on it

The tutorial never says what a linear program is or why being one matters.
Not a full introduction—but the reader needs enough to know why this is a win:

- A linear objective over linear constraints; the feasible set is a polyhedron and an
  optimum is attained at a vertex.
- Solvable in polynomial time, and fast in practice at this size—the measured LP quench
  is `1.28 ms` (`SYNOPSIS.md`, "Price the stack rather than argue it").
  Contrast with the 34-dimensional nonconvex problem it replaces.
- Solvable **exactly** over rational coefficients, which is why
  [D-021](defects.md)'s `1e-11` float noise floor is an implementation limit rather than
  a mathematical one. The tutorial states the floor in §8 without saying why an exact LP
  would remove it.
- Duality, at one sentence: the project already leans on it—exp-033 uses "an exact dual
  proving that cell's side minimal", and LP duals as unavoidable-set generators is a
  registered unbuilt lane (H-006).

The concrete argument for this section is §4. Its mechanism for the corner reads:

> Where the LP's optimal **basis** is locally constant, `φ` is smooth and its derivative
> reads off the active constraints. A corner is a **change of optimal basis**.

"Basis" is used three times and never defined. Without it, the explanation of the single
most-developed result in the tutorial is opaque to exactly the audience the document
declares. Either define basis where the LP is introduced, or restate §4's mechanism in
terms of which constraints are active.

## Scope

Background only, sized to the tutorial's job: enough that a reader knows what class of
problem this is and why it is tractable, with references (think-<references>) doing the
teaching.
