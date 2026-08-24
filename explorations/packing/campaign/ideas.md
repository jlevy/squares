<!-- Campaign idea board. HAND-WRITTEN: this is an input, not a generated view.
Its referential integrity with the registry is checked by ledger.py, not its content. -->

# Idea board — the `s(n)` search campaign

**Campaign question.** What is the structure of the `s(n)` landscape — how many basins,
how rare is the record’s, and which proposers reach which — with records as corollaries
rather than the objective.

That framing is adopted from the
[search-philosophy report](../docs/project/research/research-2026-08-23-search-philosophy-and-landscape-cartography.md):
**the map is the deliverable.** The campaign’s earlier question ("which strategies reach
the standing best") is the special case that asks only about one basin.

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

**Ids `H-001`–`H-015` belong to the
[standing review’s register](../docs/project/reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md#the-hypothesis-register)**,
and are now all codified as artifacts, so the two numberings stay aligned.
This campaign’s own claims start at `H-016`; later entries include both new hypotheses
and formally carried open questions.
Budgets are in **pair-tests**, tiers S/M/L = `1e9`/`1e11`/`1e13`.

## Status vocabulary

`raw` — thought of, not yet testable.
`shaped` — clear what would test it, no instrument yet.
`registered` — in the registry as `H-NNN`; the [ledger](ledger.md) owns it from here on.
`parked` — plausible, deliberately not now.
`dead` — killed without spending a round.

## Orientation

`s(11)` is pinned to `[3.788854, 3.877084]`. The upper end is Walter Trump’s 1979
packing — six axis-aligned squares plus a tightly constrained block of five tilted at
`≈40.1819°`; the tilt is numerically characterized through a trigonometric equation, not
established here as an algebraic number.
Both endpoints have stood for over two decades.
This is the fourth-smallest open gap at `n ≤ 100`, and the smallest open gap whose
standing record is nontrivial rather than a grid.

What the
[baseline](series/series-000-smoke-and-calibration/experiments/exp-001-baseline-sweep.md)
established: the stock annealer at 100M moves per chain recovers `s(10)` to `4.2e-04`
and does not beat the `n = 12` grid, but reaches only `3.9144` at `n = 11` — a gap of
`3.7e-02` to Trump. The `n = 12` result is not a negative control because the relevant
optimum is not proved; only the proved positive controls validate this machinery.
Everything below is a theory about why, or a way around it.

**The strategy premise, which reorganises everything below.** Record constructions may
be unusually constrained and may have low hit probability under specified baseline
proposers. If H-012 confirms that conditional claim, scaling the same proposer merely
multiplies effort against the measured probability.

*The premise omitted the non-isolated case.* Even if some record constructions are
rigid, no converse follows: a non-record optimum can be a positive-dimensional terminal
family rather than a point.
The exact `n = 3` side-2 sliding family proves that the current key splits one connected
component. At `n = 5`, two matching side/contact summaries are an unresolved identity
signal: raw contact counts establish neither rank deficiency, dimension, nor
connectivity ([D-034](../defects.md)). Until the census defines what it counts, the
denominator of “rare” is not a number, and the premise is untestable rather than merely
untested. The baseline is consistent with that — five independent seeds landing in a
narrow band five times narrower than the remaining gap is consistent with repeatedly
finding one score region — but consistent is not evidence, and
[H-012](hypotheses/H-012-record-basins-are-rare.md) is registered to kill the premise
cheaply if it is wrong.

**The building block everything waits on** is
[H-002](hypotheses/H-002-lp-in-cell-polish.md): for fixed angles, minimising `s` is a
linear program, already verified against Trump’s packing to `9e-16`. It turns “where the
annealer stopped” into “which cell this is”, which makes endpoint candidates
reproducible and numerically polishable.
Component identity, countability, and exact value require separate evidence.

Two further observations constrain most of these ideas.
**Trump’s packing is a strong rigidity candidate**, but this repository has not yet
supplied the active-constraint rank or interval proof needed to call it isolated.
Its apparent local jamming is a reason to test whether named random-start proposers miss
it. [H-018](hypotheses/H-018-basin-entry.md) has already been refuted as registered; its
finite-refiner residual motivates H-021 through H-023 but is not a runnable basin-width
experiment. It uses exactly two observed tilt classes, `0°` and one non-trivial angle, a
structural prior an unconstrained search does not exploit.

The [search-strategy catalogue](../frontier/search-strategies.yaml) enumerates 20 search
families drawn from this problem and adjacent optimization practice; it is a working
map, not an exhaustive history.
`strategy_refs` on each hypothesis cites into it, so the ledger can report which whole
families remain untried.

## The quench spine — what every other strategy runs on

| # | Idea | Status | H | From | Why it might work, or not |
| --- | --- | --- | --- | --- | --- |
| 1 | LP-in-cell polish, alternating with angle moves | registered | [H-002](hypotheses/H-002-lp-in-cell-polish.md) | [X-001](explorations/X-001-standing-review-and-search-philosophy.md) | **Measured ([exp-006](series/series-000-smoke-and-calibration/experiments/exp-006-lp-quench-n5-n10-n11.md)):** the cell solve is exact (`4.4e-16`), but the quench is a *polisher, not a rescue* — 1.1–1.3× on annealer output, because it optimises whichever basin it is handed |
| 2 | Canonical basin identity: `D₄` + relabel geometric key, contact graph up to isomorphism | shaped |  | review R-1 | Without it “basin” is undefined and basin statistics are not statistics |
| 3 | Basin atlas as a soft-schema artifact, descriptors versioned alongside | shaped |  | strategy doc | The deliverable, on the strategy report’s framing |
| 4 | Pair-test counter as the budget currency | shaped |  | review R-10 | Machine-independent; replaces this campaign’s move counter |
| 4a | The angle optimum is a kink, so derivative-based smooth local models are misspecified there | registered | [H-019](hypotheses/H-019-angle-optimum-is-a-kink.md) | [exp-006](series/series-000-smoke-and-calibration/experiments/exp-006-lp-quench-n5-n10-n11.md) | **Confirmed ([exp-010](series/series-000-smoke-and-calibration/experiments/exp-010-angle-kink-n11.md)):** one-sided slopes `0.175` vs `0.384` at the optimal tilt. On the tested starts, descent stalls five orders short and the tested Powell/Nelder–Mead runs do worse; that is not a general impossibility result for derivative-free methods. |
| 4b | Non-smooth angle search: bracket over merged angle classes | **works** |  | [exp-007](series/series-000-smoke-and-calibration/experiments/exp-007-quench-bracket-n5.md)–[exp-009](series/series-000-smoke-and-calibration/experiments/exp-009-quench-bracket-n11.md) | Reaches the analytic optimum to machine precision at `n = 5` and `n = 10` (`2e-15`, `1e-15`), where descent reaches `3e-08` and `5e-03`. The tested `n = 11` starts remain far from Trump; component identity is unresolved |
| 25 | Retain the fixed-cell LP’s primal-dual equilibrium-load certificate; test normalized loads as descriptors and block-move signals | registered | [H-031](hypotheses/H-031-load-guided-block-moves.md) | [depth review G-2](../docs/project/reviews/review-2026-08-23-mathematical-frontier-strategy.md) | The dual balances a nonzero container objective, so it is not automatically a free-framework self-stress or an angle certificate; its search value gets a held-out paired test |
| 26 | Kink-codimension candidate: known record cells have strictly positive first-order growth in every independent class-angle direction | registered | [H-027](hypotheses/H-027-record-angle-cones.md) | [depth review G-4](../docs/project/reviews/review-2026-08-23-mathematical-frontier-strategy.md) | T-3 supplies one one-dimensional slice, not a law; test the full local directional model at `n=11` and the two-direction prediction at `n=17` |
| 31 | Generalized one-sided feasible-tangent screen at Trump’s packing | registered | [H-026](hypotheses/H-026-trump-first-order-rigidity.md) | [depth review G-1](../docs/project/reviews/review-2026-08-23-mathematical-frontier-strategy.md) | Fourteen pair contacts plus eleven wall incidences are feature counts, not a rank theorem; enumerate nonsmooth branches and either exhibit a mechanism or certify no first-order fixed-side motion |

## The premise, and the census that tests it

| # | Idea | Status | H | From | Why it might work, or not |
| --- | --- | --- | --- | --- | --- |
| 5 | Census the `n ≤ 10` landscape to saturation | registered | [H-011](hypotheses/H-011-small-n-census.md) | [X-001](explorations/X-001-standing-review-and-search-philosophy.md) | Runs on existing Python plus the validated LP — no Rust. Gates the atlas |
| 6 | Locate the record basin in the quench-frequency ranking | registered | [H-012](hypotheses/H-012-record-basins-are-rare.md) | [X-001](explorations/X-001-standing-review-and-search-philosophy.md) | The load-bearing premise, killable in the cheapest tier |
| 7 | Basin-entry: perturb Trump’s exact packing, measure the return rate | registered | [H-018](hypotheses/H-018-basin-entry.md) | this campaign | **Measured ([exp-005](series/series-000-smoke-and-calibration/experiments/exp-005-basin-entry-n11.md)):** refuted as stated. The finite-quench residual scaled with `eps` and decreased with effort; component attraction remains unresolved |
| 8 | Saturation curves are lawful, so coverage is estimable | registered | [H-007](hypotheses/H-007-saturation-curves.md) | review H-7 | Turns negative results into held-out coverage estimates rather than visual plateau claims |
| 9 | False-basin rate `r(n)` — float basins the stronger verifier rejects | registered | [H-008](hypotheses/H-008-false-basin-rate.md) | review H-8 | A measured validity-perimeter rate; zero is a legitimate result |
| 10 | Symmetry dedup ratio, raw versus canonical counts | registered | [H-009](hypotheses/H-009-symmetry-dedup-ratio.md) | review H-9 | Required before comparison with any published count; ambiguity stays as bounds |
| 10a | Contact count predicts attraction frequency | registered | [H-003](hypotheses/H-003-basin-frequency-and-contacts.md) | review H-3 | A held-out predictor test, not a definition of rigidity or component identity |
| 10b | Terminal endpoints are identifiable often enough to census | registered | [H-021](hypotheses/H-021-endpoint-identifiability.md) | this campaign | Measurement-system gate: at most 5% unresolved support on every cell through `n=8` |
| 32 | Adaptive multilevel splitting estimates a rare target event more efficiently than independent restarts | registered | [H-029](hypotheses/H-029-adaptive-splitting.md) | [depth review G-5](../docs/project/reviews/review-2026-08-23-mathematical-frontier-strategy.md) | Pass exact synthetic probabilities and an independent `n=10` reference before registering any Trump-component event |
| 28 | Calibrated extreme-value sensitivity analysis on a large fixed-budget endpoint sample | raw |  | [depth review G-5](../docs/project/reviews/review-2026-08-23-mathematical-frontier-strategy.md) | A held-out-stable fit may decide whether the next budget rung is worth buying; it cannot establish the proposer’s support at every budget, and the existing archive is too small |

## Proposers — the strategies the spine makes cheap

| # | Idea | Status | H | From | Why it might work, or not |
| --- | --- | --- | --- | --- | --- |
| 11 | Angle-class two-level search | registered | [H-001](hypotheses/H-001-angle-class-reduction.md) | [X-001](explorations/X-001-standing-review-and-search-philosophy.md) | Algorithmic paired comparison; the corpus-wide angle-count claim is separate |
| 11a | Verified records through `n=30` use at most three angle classes | registered; counterexample candidate | [H-024](hypotheses/H-024-record-angle-class-count.md) | split from review H-1 | The primary `n=29` SVG appears to have six classes; verify that pose first, then replace the brittle class bound with effective angular rank/compressibility if it survives |
| 12 | δ-continuation: fixed-side projection while walking `δ` down | registered | [H-013](hypotheses/H-013-delta-continuation.md) | review H-13 | A verified path gives an upper bound on minimax clearance; numerical branch coalescence is not a feasible-component merge certificate |
| 13 | MAP-Elites over mechanism descriptors | registered | [H-015](hypotheses/H-015-map-elites-illumination.md) | review H-15 | Keeps the loss, changes what is retained. Descriptors are frozen before comparison |
| 14 | Neighbor-transfer seeding from `n ± 1` records | registered | [H-004](hypotheses/H-004-neighbor-transfer-seeding.md) | review H-4 | Corrected to an equal-budget `n=11` comparison; the original `n=12` side-4 target was vacuous |
| 15 | Superdisk continuation from circles to squares | registered | [H-014](hypotheses/H-014-superdisk-continuation.md) | review H-14 | Last in line: the only item needing new geometry |
| 16 | Stock annealer, all cells, fixed budget | registered | [H-016](hypotheses/H-016-stock-annealer-reaches-standing-best.md) | this campaign | Refuted by exp-001. The null |
| 17 | Same annealer, 100× the budget | registered | [H-017](hypotheses/H-017-budget-scaling.md) | this campaign | Park behind a short budget-response ladder; one long run cannot distinguish a flat response from a threshold crossing |
| 18 | Billiard / inflation | raw |  | `search:11` | Produced records at `n = 29, 37`; δ-continuation is its principled cousin |
| 19 | Constructor DSL proposed by an LLM, evaluated by LP + exact check | raw |  | strategy doc | Sequenced behind the first atlas artifact — there must be something verified to read |
| 33 | Effective orientation compression: few fitted class angles retain nearly all record quality even when raw classes are numerous | registered | [H-025](hypotheses/H-025-record-angle-compressibility.md) | successor to H-024 | The `n=29` six-class candidate kills a universal raw count, not a quantitative refit criterion |
| 34 | Public-parent surgery reproduces held-out 2026 UnitSquare improvements before chasing unseen records | registered | [H-030](hypotheses/H-030-public-parent-surgery.md) | [depth review G-10](../docs/project/reviews/review-2026-08-23-mathematical-frontier-strategy.md) | Known parent/child geometries turn construction grammar into a falsifiable methods test |
| 36 | Finite instances of current asymptotic stack/trapezoid primitives improve a public parent | registered | [H-035](hypotheses/H-035-asymptotic-primitive-finite-transfer.md) | [depth review G-9](../docs/project/reviews/review-2026-08-23-mathematical-frontier-strategy.md) | Bridges active 2025–26 theory to finite records without pretending finite success improves an exponent |

## Targets and calibration

| # | Idea | Status | H | From | Why it might work, or not |
| --- | --- | --- | --- | --- | --- |
| 20 | `s(17)` as the mechanism-matched calibration target | registered | [H-020](hypotheses/H-020-oblique-record-finding-n17.md) | strategy doc | The nearest case whose record uses genuinely oblique structure. `n = 5, 10` do not exercise it. A one-seed probe already returned exactly `5.0`, the trivial grid |
| 21 | `n = 11` at inflated `δ` as a continuous progress metric | shaped |  | strategy doc | Define a fixed-side feasibility/projection family; the minimum inflation needed for a preregistered target-component hit rate is the scalar, and smaller is better |
| 22 | Cleemann-style 3-4-5 construction at `n=97`, with `n=78` as a diagnostic | registered | [H-005](hypotheses/H-005-m2-minus-3-construction.md) | review H-5 | A specific upper-bound construction claim; the next `m²-3` proof target `n=61` is separate H-033 |
| 23 | LP duals as unavoidable-set generators (proof lane) | registered | [H-006](hypotheses/H-006-lp-dual-unavoidable-sets.md) | review H-6 | Quantitative cross-resolution support screen; never itself a proof |
| 24 | Stromquist falsifier triple | registered | [H-010](hypotheses/H-010-stromquist-triple.md) | review H-10 | Known-answer falsifier control followed by a separate certificate leg |
| 29 | Reference-cell two-angle value sheets `Φ_C(a₁,a₂)` at `n=11`, then `n=17` | registered | [H-028](hypotheses/H-028-reference-cell-angle-sheets.md) | [depth review G-6](../docs/project/reviews/review-2026-08-23-mathematical-frontier-strategy.md) | Cheap for one imported cell and assignment; a global two-class lower envelope is a separate multi-cell search and is not claimed |
| 30 | Fractional-piercing ceiling of the pure ten-point method at `n=11` | registered | [H-034](hypotheses/H-034-fractional-piercing-ceiling.md) | [depth review G-3](../docs/project/reviews/review-2026-08-23-mathematical-frontier-strategy.md) | `τ*(U_s)>10` rules out ten points; `τ*≤10` does not produce an integral set. Bašić–Slivková is the direct integral-piercing precedent; continuous discretization needs two-sided certification |
| 37 | Exact quotient topology of the optimal configuration set at `n=3…6` | registered | [H-032](hypotheses/H-032-small-n-optimal-moduli.md) | basin ontology | The analytic `n=3` family is the calibration; sampling keys cannot answer connectedness or strata |
| 38 | Extend the proved `m²-3` family from `m=7` to `m=8`, i.e. decide `s(61)=8` | registered | [H-033](hypotheses/H-033-m2-minus-3-at-n61.md) | Bentz 2010/2016 | The natural next exact-value case; Bašić–Slivková gives a weaker specialized bound, not the theorem |
| 39 | Robustify Stromquist’s exact `0°/45°` exclusion to a nonzero angle neighborhood | registered | [H-036](hypotheses/H-036-robust-restricted-orientation.md) | proof frontier | A tractable structural theorem between one exact restricted class and the unrestricted record |
| 40 | Close the asymptotic waste exponent gap `1/2` versus `3/5` | registered | [H-037](hypotheses/H-037-asymptotic-waste-exponent.md) | Bui 2025; McClenagan 2026 | A separate mathematical lane; finite constructor optimization supplies experiments but not the exponent verdict |
| 41 | Classify the exact number fields, elimination systems, and mechanism associations of verified record witnesses | registered | [H-038](hypotheses/H-038-record-number-fields.md) | algebraic frontier | Metadata follows the verified active cell, never a superseded decimal row; a failed degree law is retained |
| 42 | Improve the lower bound for `s(12)` and ultimately decide whether `s(12)=4` | registered | [H-039](hypotheses/H-039-s12-proof-frontier.md) | proof frontier | H-010 first calibrates the whole Stromquist implication; CEGIS then alternates candidate resources with continuous escape witnesses |
| 43 | Walk adjacent active LP cells instead of resampling cell volume | registered | [H-040](hypotheses/H-040-active-cell-neighbor-walk.md) | piecewise-linear geometry | Compare new verified cells per LP solve at `n=5,10`; a cell is not automatically a component or basin |

## Open questions

Not claims, so they cannot be hypotheses.
Registered as `kind: open_question` when worth carrying formally.

- <a id="the-shape-of-the-search-space"></a>**How wide is Trump’s basin?** **Not yet a
  defined measurement.**
  [exp-005](series/series-000-smoke-and-calibration/experiments/exp-005-basin-entry-n11.md)
  found no width to measure: under a finite local quench the return residual scaled with
  the perturbation and decreased with more effort.
  That measures this refiner’s convergence behavior, not a basin radius — so the width
  question is only answerable once a converged quench and terminal-component relation
  are both available ([H-021](hypotheses/H-021-endpoint-identifiability.md)). The stock
  schedule, meanwhile, moves far from the reference even from `eps = 1e-5`, which
  reframes `exp-003` as partly a refinement failure without assigning a component.
- **What does the searcher actually find at `n = 11`?** The baseline’s `3.9144` is some
  configuration. How many distinct local optima does it have, and how many tilt angles do
  they use? A histogram over restarts would say whether the search is finding one wrong
  answer repeatedly or many.
- **Does any run ever produce a two-tilt configuration unprompted?**
- **[What is the certified local geometry of Trump’s packing?](hypotheses/H-022-trump-local-geometry.md)**
  The exact contacts do not by themselves establish isolation or local optimality.
- **[Are the observed `n=5` endpoints in one terminal family?](hypotheses/H-023-n5-terminal-connectivity.md)**
  Six endpoints from six proposals do not decide their connectivity.
  Six endpoints from six draws show non-saturation, not its cause.

## Dead ends

Killed without spending a round, with the reason.
This section is why the campaign does not rediscover its own mistakes.

- **`14 + 20 = 34` proves Trump is isostatic.** The verifier’s twenty is a count of
  boundary corner coordinates.
  A flush axis-aligned edge contributes two such coordinates but one wall constraint;
  the exact pose has eleven square-wall incidences, so the proposed equality count
  double-counted. The remaining system is nonsmooth, and neither the corrected feature
  count nor a smooth Jacobian decides rigidity.
  Replaced by H-026’s generalized one-sided tangent screen.

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
