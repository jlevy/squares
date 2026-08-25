---
type: is
id: is-01m0vxv0f1v7nqpeq5a2kfwjwq
title: "TUTORIAL: explain why one primitive element always suffices, and what fixes its degree"
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m0vxe4ntpat4xcagtf04c37z
created_at: 2026-08-25T07:40:58.720Z
updated_at: 2026-08-25T07:40:58.720Z
---
§5 works entirely through Trump's packing, where the field is `ℚ(u)` with one primitive
element of degree 8. Nothing says whether "one `α`" is a fact about square packings, a
fact about Trump specifically, or an artifact of the example.
A reader is left to assume the number of roots needed could be anything, which is the
natural reading and is wrong in an interesting way.

Three separate questions hide behind "how many roots do we need", and the tutorial
answers none of them.

## 1. How many primitive elements? Always one

By the **primitive element theorem**, every finite extension of `ℚ` is simple, since
characteristic zero makes every finite extension separable.
So however many algebraic coordinates a packing has—`3n + 1` of them, each its own
algebraic number of its own degree—there is a single `α` with
`ℚ(x₁, y₁, θ-values, …, s) = ℚ(α)`. One primitive element, one minimal polynomial, one
isolating interval, and every coordinate becomes a polynomial in `α` with rational
coefficients.

That is the load-bearing fact under §5's whole procedure, and it is why step 1 can say
"put the configuration in `ℚ(α)` for one primitive element" as though it were an
obviously available move. It is available, but for a reason worth one sentence.

Worth pairing with the point §5 already makes well: only **one root** of that minimal
polynomial is the intended one, which is why an isolating interval is part of the field
data and why "the intended real root must be isolated from the others" is one of the two
guesses that must be discharged.

## 2. What is the degree? Unbounded, and an open empirical question

The primitive element theorem gives no bound on `[ℚ(α) : ℚ]`. The degree is whatever the
active contact system forces after elimination.
Observed: **8** at `n = 11` (Trump), and the record table reaches **degree 62**
(`research-2026-08-22-infrastructure-for-packing-exploration.md`), which is also where
pure-Python exact arithmetic is 578× slower than a FLINT-backed scalar.
[H-038](campaign/hypotheses/H-038-record-number-fields.md) registers exactly this as an
open question—which fields, degrees, Galois groups and discriminants occur, and how they
are determined by the active cell and angle-class mechanism—and notes that a degree is a
descriptor, not a ceiling, and that the `n = 69` witness does **not** inherit the
degree-82 polynomial of its superseded parent.

So: *how many roots* is one; *of what degree* is open, and the tutorial can say so
honestly rather than leaving the impression that degree 8 is typical.

The counterpoint worth keeping is §4's "rational-slope tilts would need no number field":
at a Pythagorean angle such as `arctan(3/4)` every coordinate is rational and the degree
is 1. The degree is a property of the mechanism, not of `n`.

## 3. Is a packing guaranteed to be algebraic at all? Not pointwise

This is the question with the most interesting answer, and it connects straight to the
tutorial's own Trap 2.

The *optimal side* is algebraic. With the half-angle substitution `u_i = tan(θ_i/2)`,
`cos θ_i = (1−u_i²)/(1+u_i²)` and `sin θ_i = 2u_i/(1+u_i²)`, so validity defines a closed
semialgebraic set over `ℚ` with no transcendental functions anywhere—this is already
stated in `research-2026-08-22-square-packing-algorithms-and-tooling.md`.
The set of feasible sides is then a projection of a semialgebraic set, hence semialgebraic
by Tarski–Seidenberg, hence a finite union of points and intervals with algebraic
endpoints. Its infimum is algebraic, and compactness gives attainment.

An individual optimal *configuration* need not be. Where the optimum is a positive-
dimensional terminal family, the family is cut out by polynomials but a point of it has
a free parameter: the `n = 3` sliding family is exactly `(t, 3/2)` for `t ∈ [1/2, 3/2]`,
and `t` may be transcendental. The `n = 5` angle-and-slide sheet is a two-parameter
version of the same thing.

So "recover the field" is well posed for a **rigid** optimum whose active constraints pin
it down—which is why exp-013's local-isolation theorem for Trump's pose matters beyond
its own statement—and is not well posed for a point chosen arbitrarily on a family.
That is the same distinction §3 draws between a point-basin and a terminal component,
arriving from the algebraic side, and the tutorial would be stronger for connecting them.

## Proposal

A short subsection in §5, after "The number field": one primitive element always
suffices and why; the degree is unbounded, is 8 here and 62 in the corpus, and is
[H-038](campaign/hypotheses/H-038-record-number-fields.md)'s open question; the side is
algebraic by semialgebraicity but a point on a terminal family need not be, which is why
this pipeline targets rigid optima.

**Verify before writing.** The Tarski–Seidenberg argument above is standard but is *not*
currently asserted anywhere in this directory—the closest statements are the
semialgebraic-feasible-set remarks in the algorithms report.
Treat it as a claim to be checked (W2) before it enters the tutorial, and attribute
attainment to a compactness result (`resources/papers/martin-2000-compactness-theorems-geometric-packings.pdf`)
rather than to assertion.
