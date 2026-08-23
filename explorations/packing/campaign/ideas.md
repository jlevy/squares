<!-- Campaign idea board. HAND-WRITTEN: this is an input, not a generated view.
Its referential integrity with the registry is checked by ledger.py, not its content. -->

# Idea board — the `s(n)` search campaign

**Campaign question.** Which search strategies reach the standing best for `s(n)` within
a declared move budget, and what do the ones that fail find instead?

This page is the whole idea space on one screen.
Read it before the registry, the exploration reports, or the ledger — those are deep and
this is wide. Every idea anyone has had about this campaign appears here as one line,
whether or not it has been formalized, tried, or killed.

## How to use it

- **Arriving**: read this page, then [the runbook](README.md), then only the rows you
  are about to work on.
- **New idea**: add a row here first, `status: raw`. Formalizing comes later and does
  not always come.
- **Promoting**: when an idea can be stated so it could be wrong, write
  `hypotheses/H-NNN-*.md` and fill in the `H` column.
  The row stays; it is now a pointer.
- **Killing**: never delete a row.
  Move it to [Dead ends](#dead-ends) with the reason.

Both directions are checked by `ledger.py`: every `H-NNN` named here exists, and every
registered hypothesis appears here.

## Status vocabulary

`raw` — thought of, not yet testable.
`shaped` — clear what would test it, no instrument yet.
`registered` — in the registry as `H-NNN`; the [ledger](ledger.md) owns it from here on.
`parked` — plausible, deliberately not now.
`dead` — killed without spending a round.

## Orientation

`s(11)` is pinned to `[3.788854, 3.877084]`. The upper end is Walter Trump’s 1979
packing — six axis-aligned squares plus a rigid block of five tilted at `≈40.1819°`, a
root of an irreducible degree-8 polynomial.
Both endpoints have stood for over two decades, and this is still the *smallest* open
gap at `n ≤ 100`.

What the [baseline](series/001-smoke-n11/experiments/exp-001-baseline-sweep.md)
established: the stock annealer at 100M moves per chain recovers `s(10)` to `4.2e-04`
and correctly refuses to beat the `n = 12` grid, but reaches only `3.9144` at `n = 11` —
a gap of `3.7e-02` to Trump.
So the instrument works and the target is genuinely hard.
Everything below is a theory about why, or a way around it.

Two facts constrain most of these ideas.
**Trump’s packing is rigid**, so it is an isolated point in configuration space rather
than a basin with width — which is a reason to expect random restarts to miss it, and
the reason [H-004](#the-shape-of-the-search-space) is the most informative cheap thing
to measure.
And **it uses exactly two distinct tilts**, `0°` and one free angle, which is
a strong structural prior an unconstrained search does not exploit.

The [search-strategy catalogue](../frontier/search-strategies.yaml) enumerates 20 ways
anyone has ever found a packing; `strategy_refs` on each hypothesis cites into it, so
the ledger can report which whole families remain untried.

## Budget and schedule — how the engine is driven

| # | Idea | Status | H | From | Why it might work, or not |
| --- | --- | --- | --- | --- | --- |
| 1 | Stock annealer, all cells, fixed budget | registered | [H-001](hypotheses/H-001-stock-annealer-reaches-standing-best.md) | baseline | The null hypothesis. Refuted at `n = 11`, confirmed at 10 and 12 |
| 2 | Same annealer, 100× the budget | registered | [H-002](hypotheses/H-002-budget-scaling.md) | baseline | Separates “needs more compute” from “needs a different method” — the cheapest fork in the whole campaign |
| 3 | Reseed probability sweep | raw |  |  | Currently 0.5 and unmeasured; controls exploration against polish |
| 4 | Temperature schedule variants (linear, adaptive, reheat) | raw |  |  | Geometric is a default, not a finding |
| 5 | Lambda ramp variants | raw |  |  | The overlap weight ramp is unmeasured; too fast may freeze overlaps in |

## Structural priors — exploit what is known about the answer

| # | Idea | Status | H | From | Why it might work, or not |
| --- | --- | --- | --- | --- | --- |
| 6 | Restrict to two distinct tilt angles | registered | [H-003](hypotheses/H-003-two-tilt-restriction.md) | orientation above | Trump’s packing has exactly two; collapses 11 angles to 2 free parameters. Risk: bakes in the answer’s shape, so a win says less than it appears |
| 7 | Seed from the `6 + 5` block structure | shaped |  |  | Strong prior, but assumes the conjecture; only honest as a basin-width probe |
| 8 | Rational-slope tilts `arctan(p/q)` only | raw |  | `search:6` | Produced records elsewhere. Trump’s angle is *not* rational-slope, so this would likely miss `n = 11` — informative as a negative |
| 9 | Seed `n = 11` from the `s(10)` optimum plus one square | raw |  | `search:4` | Cheap; extension has produced records (`search:3`) |
| 10 | Symmetry-restricted search | raw |  |  | Reduces dimension if the optimum has symmetry. Trump’s does not obviously |

## Different search families — the untried columns of the catalogue

| # | Idea | Status | H | From | Why it might work, or not |
| --- | --- | --- | --- | --- | --- |
| 11 | Billiard / inflation | raw |  | `search:11` | The method that actually produced records at `n = 29, 37`. The most conspicuous gap in what this campaign has tried |
| 12 | Basin hopping with NLP polish per restart | raw |  | `search:12` | Polish is tier 2 and does not exist yet; blocked until it does |
| 13 | Population / evolutionary | raw |  | `search:16` | Never aimed at squares-in-squares. The research program’s item 5 |
| 14 | Contact-graph enumeration then algebraic solve | raw |  | `search:17`, `search:18` | How exact values are actually obtained; the natural bridge to tier 3 |
| 15 | SAT / CP at fixed side | raw |  | `search:14` | Awkward under free rotation, per the catalogue’s own note |
| 16 | Richer move set: swap two squares, move a block | raw |  |  | Current moves are single-square translate and rotate only |

## Open questions

Not claims, so they cannot be hypotheses.
Registered as `kind: open_question` when worth carrying formally.

- <a id="the-shape-of-the-search-space"></a>**How wide is Trump’s basin?** It is rigid,
  so possibly a measure-zero attractor.
  Registered as [H-004](hypotheses/H-004-basin-width.md) — measurable by starting *at*
  the known configuration, perturbing by `ε`, and seeing what fraction of runs return.
  The single cheapest thing that would explain the baseline.
- **What does the searcher actually find at `n = 11`?** The baseline’s `3.9144` is some
  configuration. How many distinct local optima does it have, and how many tilt angles do
  they use? A histogram over restarts would say whether the search is finding one wrong
  answer repeatedly or many.
- **Does any run ever produce a two-tilt configuration unprompted?**

## Dead ends

Killed without spending a round, with the reason.
This section is why the campaign does not rediscover its own mistakes.

- **GPU population search.** Measured at 2.5M evals/s on MPS against 18–20M on the CPU’s
  cores: the kernel is elementwise with almost no arithmetic intensity, so it is launch-
  and bandwidth-bound, and MPS forces `float32` — the wrong precision for a geometry
  whose true contacts are exactly zero.
  Revisit only at large `n`.
- **Fixed-side shrink-and-re-anneal outer loop.** Two versions built and measured.
  The first crawled (`2.875` on `n = 5`, where the answer is `2.707`); the second never
  left the grid basin at all, because the trivial grid is exactly jammed and no local
  move escapes it. Replaced by minimising the enclosing side directly, which needs no
  outer loop.
- **Squared overlap penalty.** Gradient vanishes as the overlap closes, so it never
  quite reaches zero. A linear penalty has an exact finite-`lambda` constrained optimum.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
