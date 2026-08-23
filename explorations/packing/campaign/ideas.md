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
and are reserved even where not yet codified as artifacts, so the two numberings stay
aligned.
This campaign’s own claims start at `H-016`. Reserved ids are declared below and
checked: a reservation that has been fulfilled is flagged as stale rather than left
claiming the id is unwritten.

<!-- reserved-ids: H-003 H-004 H-005 H-006 H-007 H-008 H-009 H-010 H-013 H-014 H-015 -->
Budgets are in **pair-tests**, tiers S/M/L = `1e9`/`1e11`/`1e13`.

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

What the
[baseline](series/series-000-smoke-and-calibration/experiments/exp-001-baseline-sweep.md)
established: the stock annealer at 100M moves per chain recovers `s(10)` to `4.2e-04`
and correctly refuses to beat the `n = 12` grid, but reaches only `3.9144` at `n = 11` —
a gap of `3.7e-02` to Trump.
So the instrument works and the target is genuinely hard.
Everything below is a theory about why, or a way around it.

**The strategy premise, which reorganises everything below.** Records are rigid; rigid
optima live in rare basins; so scaling a volume-weighted sampler multiplies effort
against a probability the problem drives toward zero.
The baseline is consistent with that — five independent seeds landing in a narrow band
five times narrower than the remaining gap is what repeatedly finding the same wrong
funnel looks like — but consistent is not evidence, and
[H-012](hypotheses/H-012-record-basins-are-rare.md) is registered to kill the premise
cheaply if it is wrong.

**The building block everything waits on** is
[H-002](hypotheses/H-002-lp-in-cell-polish.md): for fixed angles, minimising `s` is a
linear program, already verified against Trump’s packing to `9e-16`. It turns “where the
annealer stopped” into “which cell this is”, which is what makes basins nameable,
countable, and exactly valued — and it is this campaign’s missing tier 2.

Two further facts constrain most of these ideas.
**Trump’s packing is rigid**, so it is an isolated point in configuration space rather
than a basin with width — which is a reason to expect random restarts to miss it, and
the reason [H-018](hypotheses/H-018-basin-entry.md) is the most informative cheap thing
runnable today. And **it uses exactly two distinct tilts**, `0°` and one free angle,
which is a strong structural prior an unconstrained search does not exploit.

The [search-strategy catalogue](../frontier/search-strategies.yaml) enumerates 20 ways
anyone has ever found a packing; `strategy_refs` on each hypothesis cites into it, so
the ledger can report which whole families remain untried.

## The quench spine — what every other strategy runs on

| # | Idea | Status | H | From | Why it might work, or not |
| --- | --- | --- | --- | --- | --- |
| 1 | LP-in-cell polish, alternating with angle moves | registered | [H-002](hypotheses/H-002-lp-in-cell-polish.md) | [X-001](explorations/X-001-standing-review-and-search-philosophy.md) | **Measured ([exp-006](series/series-000-smoke-and-calibration/experiments/exp-006-lp-quench-n5-n10-n11.md)):** the cell solve is exact (`4.4e-16`), but the quench is a *polisher, not a rescue* — 1.1–1.3× on annealer output, because it optimises whichever basin it is handed |
| 2 | Canonical basin identity: `D₄` + relabel geometric key, contact graph up to isomorphism | shaped |  | review R-1 | Without it “basin” is undefined and basin statistics are not statistics |
| 3 | Basin atlas as a soft-schema artifact, descriptors versioned alongside | shaped |  | strategy doc | The deliverable, on the strategy report’s framing |
| 4 | Pair-test counter as the budget currency | shaped |  | review R-10 | Machine-independent; replaces this campaign’s move counter |
| 4a | The angle optimum is a kink, so smooth methods cannot converge to it | registered | [H-019](hypotheses/H-019-angle-optimum-is-a-kink.md) | [exp-006](series/series-000-smoke-and-calibration/experiments/exp-006-lp-quench-n5-n10-n11.md) | **Confirmed ([exp-010](series/series-000-smoke-and-calibration/experiments/exp-010-angle-kink-n11.md)):** one-sided slopes `0.175` vs `0.384` at the optimal tilt. Descent stalls five orders short; Powell and Nelder-Mead do *worse* |
| 4b | Non-smooth angle search: bracket over merged angle classes | **works** |  | [exp-007](series/series-000-smoke-and-calibration/experiments/exp-007-quench-bracket-n5.md)–[exp-009](series/series-000-smoke-and-calibration/experiments/exp-009-quench-bracket-n11.md) | Reaches the analytic optimum to machine precision at `n = 5` and `n = 10` (`2e-15`, `1e-15`), where descent reaches `3e-08` and `5e-03`. No effect at `n = 11`: wrong basin |

## The premise, and the census that tests it

| # | Idea | Status | H | From | Why it might work, or not |
| --- | --- | --- | --- | --- | --- |
| 5 | Census the `n ≤ 10` landscape to saturation | registered | [H-011](hypotheses/H-011-small-n-census.md) | [X-001](explorations/X-001-standing-review-and-search-philosophy.md) | Runs on existing Python plus the validated LP — no Rust. Gates the atlas |
| 6 | Locate the record basin in the quench-frequency ranking | registered | [H-012](hypotheses/H-012-record-basins-are-rare.md) | [X-001](explorations/X-001-standing-review-and-search-philosophy.md) | The load-bearing premise, killable in the cheapest tier |
| 7 | Basin-entry: perturb Trump’s exact packing, measure the return rate | registered | [H-018](hypotheses/H-018-basin-entry.md) | this campaign | **Measured ([exp-005](series/series-000-smoke-and-calibration/experiments/exp-005-basin-entry-n11.md)):** refuted as stated, but there is no basin wall — return distance is linear in `eps` and halves with 10× effort, so the limit is the refiner |
| 8 | Saturation curves are lawful, so coverage is estimable | raw | `H-007` | review H-7 | Turns negative results into estimates. Reserved id, not yet codified |
| 9 | False-basin rate `r(n)` — float basins the exact verifier rejects | raw | `H-008` | review H-8 | Free: a counter on existing work. Any value is a result |
| 10 | Symmetry dedup ratio, raw versus canonical counts | raw | `H-009` | review H-9 | Free; and required before any comparison with Ellsworth’s counts |

## Proposers — the strategies the spine makes cheap

| # | Idea | Status | H | From | Why it might work, or not |
| --- | --- | --- | --- | --- | --- |
| 11 | Angle-class two-level search | registered | [H-001](hypotheses/H-001-angle-class-reduction.md) | [X-001](explorations/X-001-standing-review-and-search-philosophy.md) | The honest continuous dimension is `n`, not `3n+1`; records use 1–2 angles |
| 12 | δ-continuation: inflate the container, walk `δ` down with re-polish | raw | `H-013` | review H-13 | Rare-event search becomes path-following; merge-`δ` doubles as the atlas’s barrier scale |
| 13 | MAP-Elites over mechanism descriptors | raw | `H-015` | review H-15 | Keeps the loss, changes what is retained. Descriptors must separate the grid funnel from the rigid-rare family |
| 14 | Neighbor-transfer seeding from `n ± 1` records | raw | `H-004` | review H-4 | How the human record table actually advances |
| 15 | Superdisk continuation from circles to squares | raw | `H-014` | review H-14 | Last in line: the only item needing new geometry |
| 16 | Stock annealer, all cells, fixed budget | registered | [H-016](hypotheses/H-016-stock-annealer-reaches-standing-best.md) | this campaign | Refuted by exp-001. The null |
| 17 | Same annealer, 100× the budget | registered | [H-017](hypotheses/H-017-budget-scaling.md) | this campaign | Demoted: H-012 answers it better and cheaper |
| 18 | Billiard / inflation | raw |  | `search:11` | Produced records at `n = 29, 37`; δ-continuation is its principled cousin |
| 19 | Constructor DSL proposed by an LLM, evaluated by LP + exact check | raw |  | strategy doc | Sequenced behind the first atlas artifact — there must be something verified to read |

## Targets and calibration

| # | Idea | Status | H | From | Why it might work, or not |
| --- | --- | --- | --- | --- | --- |
| 20 | `s(17)` as the mechanism-matched calibration target | registered | [H-020](hypotheses/H-020-oblique-record-finding-n17.md) | strategy doc | The nearest case whose record uses genuinely oblique structure. `n = 5, 10` do not exercise it. A one-seed probe already returned exactly `5.0`, the trivial grid |
| 21 | `n = 11` at inflated `δ` as a continuous progress metric | shaped |  | strategy doc | The largest `δ` at which the engine still finds Trump’s cell moves continuously, unlike found/not-found |
| 22 | `m² − 3` at `n = 61, 78, 97`, Cleemann-style `arctan(3/4)` | raw | `H-005` | review H-5 | Honest prior low, cost near zero, analytic attempt needs no engine |
| 23 | LP duals as unavoidable-set generators (proof lane) | raw | `H-006` | review H-6 | First mechanized step anyone would have taken on the proof side |
| 24 | Stromquist falsifier triple | raw | `H-010` | review H-10 | Known-answer test; a failure is a machinery bug by definition |

## Open questions

Not claims, so they cannot be hypotheses.
Registered as `kind: open_question` when worth carrying formally.

- <a id="the-shape-of-the-search-space"></a>**How wide is Trump’s basin?** **Answered,
  and the question was wrong.**
  [exp-005](series/series-000-smoke-and-calibration/experiments/exp-005-basin-entry-n11.md)
  found no width to measure: under a local quench the return distance is linear in the
  perturbation over four decades with no threshold, and halves when effort is multiplied
  by ten. What that measures is the refiner’s convergence rate, not a basin radius — so
  the width question is only answerable once the LP quench
  ([H-002](hypotheses/H-002-lp-in-cell-polish.md)) lands and converges in one solve.
  The stock schedule, meanwhile, cannot hold the basin from `eps = 1e-5`, which reframes
  `exp-003` as partly a polish failure.
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
