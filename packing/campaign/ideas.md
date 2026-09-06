<!-- Campaign idea board. HAND-WRITTEN: this is an input, not a generated view.
Its referential integrity with the registry is checked by ledger.py, not its content. -->

# Idea board — the `s(n)` search campaign

**Campaign question.** What is the structure of the `s(n)` landscape — how many basins,
how rare is the record’s, and which proposers reach which — with records as corollaries
rather than the objective.

That framing is adopted from the
[search-philosophy report](../../docs/project/research/research-2026-08-23-search-philosophy-and-landscape-cartography.md):
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
[standing review’s register](../../docs/project/reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md#the-hypothesis-register)**,
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

`s(11)` is pinned to `[3.81, 3.877084]`. The upper end is Walter Trump’s 1979 packing —
six axis-aligned squares plus a tightly constrained block of five tilted at `≈40.1819°`;
the tilt is numerically characterized through a trigonometric equation, not established
here as an algebraic number.
That end has stood since 1979; the lower end moved on 2026-09-04, for the first time
since Stromquist stated `2 + 4/√5 = 3.788854` in 2003. This is the fourth-smallest open
gap at `n ≤ 100`, and the smallest open gap whose standing record is nontrivial rather
than a grid.

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
component.
At `n = 5`, exp-033 proves the two equal-side keys share one exact fixed-angle
optimal face, and exp-034 embeds it in a two-parameter angle-and-slide sheet of optima.
This does not prove their complete nonsmooth stationary identity, and raw contact counts
alone still establish neither rank deficiency, dimension, nor connectivity
([D-034](../../defects.md)). Until the census defines what it counts, the denominator of
“rare” is not a number, and the premise is untestable rather than merely untested.
The baseline is consistent with that — five independent seeds landing in a narrow band
five times narrower than the remaining gap is consistent with repeatedly finding one
score region — but consistent is not evidence, and
[H-012](hypotheses/H-012-record-basins-are-rare.md) is registered to kill the premise
cheaply if it is wrong.

**The building block everything waits on** is
[H-002](hypotheses/H-002-lp-in-cell-polish.md): for fixed angles, minimising `s` is a
linear program, already numerically checked against Trump’s packing to `9e-16`. It turns
“where the annealer stopped” into “which cell this is”, which makes endpoint candidates
reproducible and numerically polishable.
Component identity, countability, and exact value require separate evidence.

Two further observations constrain most of these ideas.
**Trump’s packing is locally isolated.** Exp-013 proves this from the complete finite
branch system and exact zero-cone certificates; it does not give an explicit radius or
show why named random-start proposers miss it.
[H-018](hypotheses/H-018-basin-entry.md) has already been refuted as registered; its
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
| 25 | Retain the fixed-cell LP’s primal-dual equilibrium-load certificate; test normalized loads as descriptors and block-move signals | registered | [H-031](hypotheses/H-031-load-guided-block-moves.md) | [depth review G-2](../../docs/project/reviews/review-2026-08-23-mathematical-frontier-strategy.md) | The dual balances a nonzero container objective, so it is not automatically a free-framework self-stress or an angle certificate; its search value gets a held-out paired test |
| 26 | Kink-codimension candidate: known record cells have strictly positive first-order growth in every independent class-angle direction | registered | [H-027](hypotheses/H-027-record-angle-cones.md) | [depth review G-4](../../docs/project/reviews/review-2026-08-23-mathematical-frontier-strategy.md) | T-3 supplies one one-dimensional slice, not a law; test the full local directional model at `n=11` and the two-direction prediction at `n=17` |
| 31 | Exact branchwise linearized-cone screen at Trump’s packing | confirmed | [H-026](hypotheses/H-026-trump-first-order-rigidity.md) | [exp-013](series/series-000-smoke-and-calibration/experiments/exp-013-h-026-trump-tangent.md) | All 128 derivative-distinct cones are zero by exact positive-stress certificates, covering 512 raw branches; the finite-branch lemma locally isolates the pose |

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
| 32 | Adaptive multilevel splitting estimates a rare target event more efficiently than independent restarts | registered | [H-029](hypotheses/H-029-adaptive-splitting.md) | [depth review G-5](../../docs/project/reviews/review-2026-08-23-mathematical-frontier-strategy.md) | Pass exact synthetic probabilities and an independent `n=10` reference before registering any Trump-component event |
| 28 | Calibrated extreme-value sensitivity analysis on a large fixed-budget endpoint sample | raw |  | [depth review G-5](../../docs/project/reviews/review-2026-08-23-mathematical-frontier-strategy.md) | A held-out-stable fit may decide whether the next budget rung is worth buying; it cannot establish the proposer’s support at every budget, and the existing archive is too small |

## Proposers — the strategies the spine makes cheap

| # | Idea | Status | H | From | Why it might work, or not |
| --- | --- | --- | --- | --- | --- |
| 11 | Angle-class two-level search | registered | [H-001](hypotheses/H-001-angle-class-reduction.md) | [X-001](explorations/X-001-standing-review-and-search-philosophy.md) | Algorithmic paired comparison; the corpus-wide angle-count claim is separate |
| 11a | Formally supported records through `n=30` use at most three angle classes | **unresolved**; the `n=29` serialization lacks a formal feasibility certificate | [H-024](hypotheses/H-024-record-angle-class-count.md), [exp-012](series/series-000-smoke-and-calibration/experiments/exp-012-h-024-n29-angle-classes.md) | split from review H-1 | Six numerical classes do not satisfy the registered formal-witness prerequisite |
| 11b | The retained `n=29` serialization has at most three numerical angle classes under its declared arithmetic | **numerically rejected** by six classes | [H-042](hypotheses/H-042-n29-numerical-angle-classes.md), [exp-037](series/series-000-smoke-and-calibration/experiments/exp-037-h-042-n29-numerical-angle-classes.md) | successor to H-024 | Preserves the useful observation without upgrading numerical feasibility to formal support |
| 12 | δ-continuation: fixed-side projection while walking `δ` down | registered | [H-013](hypotheses/H-013-delta-continuation.md) | review H-13 | A verified path gives an upper bound on minimax clearance; numerical branch coalescence is not a feasible-component merge certificate |
| 13 | MAP-Elites over mechanism descriptors | registered | [H-015](hypotheses/H-015-map-elites-illumination.md) | review H-15 | Keeps the loss, changes what is retained. Descriptors are frozen before comparison |
| 14 | Neighbor-transfer seeding from `n ± 1` records | registered | [H-004](hypotheses/H-004-neighbor-transfer-seeding.md) | review H-4 | Corrected to an equal-budget `n=11` comparison; the original `n=12` side-4 target was vacuous |
| 15 | Superdisk continuation from circles to squares | registered | [H-014](hypotheses/H-014-superdisk-continuation.md) | review H-14 | Last in line: the only item needing new geometry |
| 16 | Stock annealer, all cells, fixed budget | registered | [H-016](hypotheses/H-016-stock-annealer-reaches-standing-best.md) | this campaign | Refuted by exp-001. The null |
| 17 | Same annealer, 100× the budget | registered | [H-017](hypotheses/H-017-budget-scaling.md) | this campaign | Park behind a short budget-response ladder; one long run cannot distinguish a flat response from a threshold crossing |
| 18 | Billiard / inflation | raw |  | `search:11` | Produced records at `n = 29, 37`; δ-continuation is its principled cousin |
| 19 | Constructor DSL proposed by an LLM, evaluated by LP + exact check | raw |  | strategy doc | Sequenced behind the first atlas artifact — there must be something verified to read |
| 33 | Effective orientation compression: few fitted class angles retain nearly all record quality even when raw classes are numerous | registered; promoted after the six-class numerical observation | [H-025](hypotheses/H-025-record-angle-compressibility.md) | successor to H-024 | Exp-012’s serialized `n=29` geometry has six numerical classes; a quantitative refit criterion is less brittle |
| 34 | Public-parent surgery reproduces held-out 2026 UnitSquare improvements before chasing unseen records | registered | [H-030](hypotheses/H-030-public-parent-surgery.md) | [depth review G-10](../../docs/project/reviews/review-2026-08-23-mathematical-frontier-strategy.md) | The public parents and reported children make a falsifiable methods test, but the child SVGs are rounded renderings; H-030 waits on surgery-grade pose reconstruction rather than treating pixels as verified geometry |
| 36 | Finite instances of current asymptotic stack/trapezoid primitives improve a public parent | registered | [H-035](hypotheses/H-035-asymptotic-primitive-finite-transfer.md) | [depth review G-9](../../docs/project/reviews/review-2026-08-23-mathematical-frontier-strategy.md) | Bridges active 2025–26 theory to finite records without pretending finite success improves an exponent |
| 46 | Stratified chunk enumeration: partition `n` into aligned bar/L/rectangle chunks plus `j` rotating chunks, enumerate skeletons and chunk/wall contact hypotheses, then glued-LP screen, soft LP, and class bracketing | shaped |  | [X-003](explorations/X-003-stratified-chunk-enumeration.md) | Stages 2–5 are the existing quench plus glue rows; the free combinatorics collapses from `8^C(n,2)` to roughly `8^C(k,2)` at the chunk level. Aligned stage-1 values cannot rank strata, so every surviving stratum gets a coarse angle sweep before triage |
| 47 | Chunk-grammar rediscovery ladder: freeze the grammar on `n = 5`, `n = 10`, and the Hämäläinen `45°` class optimum, then one preregistered shot at `n = 11`, with `n = 17` as differentiator and `n = 16` as guard | registered | [H-045](hypotheses/H-045-chunk-grammar-rediscovery.md) | [X-003](explorations/X-003-stratified-chunk-enumeration.md) | Gensane–Ryckelynck 2005 and SCIP/Xpress 2026 already rediscover Trump at cost; a cold `n = 17` rediscovery would be a first on this archive’s evidence. Deterministic LP-solve accounting satisfies the D-126 work-unit rule by construction |
| 48 | Trump predecessor continuation: trace the class-angle objective on Trump’s chunk arrangement from `0°` to `40.18°`, recording cell-change events | registered | [H-046](hypotheses/H-046-regular-predecessor-continuation.md) | [X-003](explorations/X-003-stratified-chunk-enumeration.md) | Tests whether the record is continuously connected to its aligned regular form through the stratum family; seconds of wall time on the built quench |
| 49 | Chunk-expressibility of the record corpus: do standing records at `n <= 30` already partition into at most six one-angle bar/L/rectangle chunks? | registered | [H-044](hypotheses/H-044-chunk-expressibility-of-records.md) | [X-003](explorations/X-003-stratified-chunk-enumeration.md) | The coverage prior the whole enumeration design rests on, and the only one measurable from archived geometry with no search. Exp-037’s six numerical classes at `n = 29` are why `K` is six rather than three |
| 51 | Chunk-regular predecessors as a coordinate system: round any pose to exact intra-chunk contacts and snapped class angles, re-quench, and ask whether it returns | registered | [H-047](hypotheses/H-047-chunk-regular-predecessors.md) | [X-003](explorations/X-003-stratified-chunk-enumeration.md) | Tests the representation on ordinary non-record endpoints as well as records, so it is not fitted to twenty examples. A round trip makes predecessors the search object rather than configurations |
| 52 | Glued-chunk screen fidelity: does rigid-tile ranking keep the soft-mode winner in its top decile on the proved cells? | registered | [H-048](hypotheses/H-048-glued-screen-fidelity.md) | [X-003](explorations/X-003-stratified-chunk-enumeration.md) | The enumerator’s cost model assumes it; proved cells make a screen failure an instrument fact rather than a landscape one, and glued aligned strata are where D-059 instability would show |
| 53 | Import full record geometry and per-case angle inventories for every `n <= 100` | shaped |  | [X-003](explorations/X-003-stratified-chunk-enumeration.md) | Most frontier entries carry a side value with no imported geometry witness and a null `tilt_angles_deg`; the corpus is the input every chunk measurement reads |
| 54 | The `n = 90` primitive: do 20 unit squares pack squeezably in a `4 x 6` rectangle, completing Arslanov’s decomposition at `m = 10`? | registered | [H-049](hypotheses/H-049-squeezable-20-in-4x6.md) | [X-009](explorations/X-009-where-a-new-packing-is-reachable.md) | The one finite question standing between the grid and `s(90) < 10` after Cantrell’s February 2025 `n = 110` result; a refusal closes the route by lemma rather than budget |
| 55 | The `n = 71` angle merge: does the incumbent’s `0.0358°` two-class split survive a bracketed single-angle LP sweep of its sixteen-square block? | registered | [H-050](hypotheses/H-050-n71-angle-split-load-bearing.md) | [X-009](explorations/X-009-where-a-new-packing-is-reachable.md) | The cheapest question at the one annealed size whose catalogue records cold search failing; a refutation is a direct search lead and a confirmation prices the last `2.7e-5` |

## Targets and calibration

| # | Idea | Status | H | From | Why it might work, or not |
| --- | --- | --- | --- | --- | --- |
| 20 | `s(17)` as the mechanism-matched calibration target | registered | [H-020](hypotheses/H-020-oblique-record-finding-n17.md) | strategy doc; [X-011](explorations/X-011-controls-are-not-targets.md) | The nearest case whose record uses genuinely oblique structure. `n = 5, 10` do not exercise it, and a one-seed probe returned the trivial grid. This search calibration is separate from the new weighted lower-certificate lane at the same `n` |
| 21 | `n = 11` at inflated `δ` as a continuous progress metric | shaped |  | strategy doc | Define a fixed-side feasibility/projection family; the minimum inflation needed for a preregistered target-component hit rate is the scalar, and smaller is better |
| 22 | Cleemann-style 3-4-5 construction at `n=97`, with `n=78` as a diagnostic | registered | [H-005](hypotheses/H-005-m2-minus-3-construction.md) | review H-5 | A specific upper-bound construction claim; the next `m²-3` proof target `n=61` is separate H-033 |
| 23 | LP duals as unavoidable-set generators (proof lane) | registered | [H-006](hypotheses/H-006-lp-dual-unavoidable-sets.md) | review H-6 | Quantitative cross-resolution support screen; never itself a proof |
| 24 | Stromquist conditional-forcing reconstruction | refuted | [H-010](hypotheses/H-010-stromquist-triple.md) | [exp-016](series/series-000-smoke-and-calibration/experiments/exp-016-h-010-stromquist-printed-figure14.md) | An exact strict box avoids all twelve printed Figure 14 points; this rejects the proof as printed, not its numerical lower bound |
| 29 | Reference-cell two-angle value sheets `Φ_C(a₁,a₂)` at `n=11`, then `n=17` | registered | [H-028](hypotheses/H-028-reference-cell-angle-sheets.md) | [depth review G-6](../../docs/project/reviews/review-2026-08-23-mathematical-frontier-strategy.md) | Cheap for one imported cell and assignment; a global two-class lower envelope is a separate multi-cell search and is not claimed |
| 30 | Fractional-piercing ceiling of the pure ten-point method at `n=11` | registered | [H-034](hypotheses/H-034-fractional-piercing-ceiling.md) | [depth review G-3](../../docs/project/reviews/review-2026-08-23-mathematical-frontier-strategy.md) | `τ*(U_s)>10` rules out ten points; `τ*≤10` does not produce an integral set. Bašić–Slivková is the direct integral-piercing precedent; continuous discretization needs two-sided certification |
| 37 | Exact quotient topology of the optimal configuration set at `n=3…6` | active; `n=3,4` solved by exp-014/015 | [H-032](hypotheses/H-032-small-n-optimal-moduli.md) | basin ontology; [X-011](explorations/X-011-controls-are-not-targets.md) | The exact controls are permanent, but after twelve H-023 rounds `n = 5` gets one final bounded discriminator with a matched `n = 10` transfer; without transfer the lane parks |
| 38 | Extend the proved `m²-3` family from `m=7` to `m=8`, i.e. decide `s(61)=8` | registered | [H-033](hypotheses/H-033-m2-minus-3-at-n61.md) | Bentz 2010/2016 | The natural next exact-value case; Bašić–Slivková gives a weaker specialized bound, not the theorem |
| 39 | Robustify Stromquist’s exact `0°/45°` exclusion to a nonzero angle neighborhood | registered | [H-036](hypotheses/H-036-robust-restricted-orientation.md) | proof frontier | A tractable structural theorem between one exact restricted class and the unrestricted record |
| 40 | Close the asymptotic waste exponent gap `1/2` versus `3/5` | registered | [H-037](hypotheses/H-037-asymptotic-waste-exponent.md) | Bui 2025; McClenagan 2026 | A separate mathematical lane; finite constructor optimization supplies experiments but not the exponent verdict |
| 41 | Classify the exact number fields, elimination systems, and mechanism associations of verified record witnesses | registered | [H-038](hypotheses/H-038-record-number-fields.md) | algebraic frontier | Metadata follows the verified active cell, never a superseded decimal row; a failed degree law is retained |
| 42 | Improve the lower bound for `s(12)` and ultimately decide whether `s(12)=4` | registered | [H-039](hypotheses/H-039-s12-proof-frontier.md) | proof frontier | Exp-016/017 now calibrate failure and success of the forcing architecture; CEGIS can alternate candidate resources with continuous escape witnesses |
| 43 | Walk adjacent active LP cells instead of resampling cell volume | registered | [H-040](hypotheses/H-040-active-cell-neighbor-walk.md) | piecewise-linear geometry | Compare new verified cells per LP solve at `n=5,10`; a cell is not automatically a component or basin |
| 44 | Repair Stromquist’s printed Figure 14 set without changing the proof architecture | confirmed | [H-041](hypotheses/H-041-repaired-stromquist-point-set.md) | [exp-017](series/series-000-smoke-and-calibration/experiments/exp-017-h-041-stromquist-repaired-figure14.md) | Moving only `G.x` from `.8` to `.79` yields a complete exact five-node certificate and independently restores the stated lower bound |
| 45 | Extract proper incidence-minimal rigidity cores from every Trump derivative branch | registered | [H-043](hypotheses/H-043-trump-incidence-rigidity-cores.md) | successor to exp-013 | Exact grouped wall/contact cores test whether every fixed-side branch contains structural first-order redundancy; they do not supply a radius or global theorem |
| 50 | Certified restricted-class optimality: rigorous per-stratum optima over an interval angle sweep, proving statements of the shape “no `k`-chunk packing beats Trump” | raw |  | [X-003](explorations/X-003-stratified-chunk-enumeration.md) | The successor shape to Stromquist’s Theorem 3, the only bespoke restricted-class theorem at `n = 11`; blocked on the exact LP that is D-021’s named general fix, so the numerical enumerator comes first |

## Shaped by the 2026-08-31 frontier delta

| # | Idea | Status | H | From | Why it might work, or not |
| --- | --- | --- | --- | --- | --- |
| 56 | Weighted-atom lower certificates at `n = 17`, with monotone transfer to `n = 18, 19` | shaped |  | [X-011](explorations/X-011-controls-are-not-targets.md) | The 4.5058 fixed certificate and source verifier are retained and replayed; an independently written accumulator checks implementation agreement while sharing the source proof assumptions, and the value does not improve `n = 20` |
| 57 | Cross-scale exact/interval construction ladder: `18 → 50 → 54 → 39 → 55` | shaped |  | [X-011](explorations/X-011-controls-are-not-targets.md) | Candidate controls increase representation and scale demands; `n = 19` is an exact cross-field mechanism contrast, `n = 53` is the representation refusal, and `n = 51` is a separate rare-basin benchmark |
| 58 | Parent-child rigid-pose reconstruction under bounded UnitSquare serialization models at `n = 68, 69` | shaped |  | [X-011](explorations/X-011-controls-are-not-targets.md) | A conservative corners-to-pose bridge must verify public-parent provenance and consider nearest rounding, truncation, and declared export semantics; it may emit only tolerance-qualified contacts or a typed refusal |
| 59 | Dated record-event and reproducibility corpus | shaped |  | [X-011](explorations/X-011-controls-are-not-targets.md) | Current values, supersession events, construction genealogy, source geometry, code/settings/seeds, and certificates have different coverage; a normalized event record would make the missing layer explicit |
| 60 | Blinded `n = 68` public-parent surgery calibration under a fixed grammar and tier-S budget | registered | [H-051](hypotheses/H-051-n68-blinded-surgery-calibration.md) | [X-011](explorations/X-011-controls-are-not-targets.md) | The one-case pilot has its own falsifiable hit rule and information barrier; either outcome calibrates the method but cannot adjudicate H-030’s two-of-six claim |
| 61 | Independently accumulate the fixed `n = 17` weighted certificate and compare every exact invariant | registered | [H-052](hypotheses/H-052-n17-independent-certificate-agreement.md) | [X-011](explorations/X-011-controls-are-not-targets.md) | Changes the implementation while holding the proof input fixed; exact agreement increases confidence in the retained certificate machinery without claiming an independent proof method or adopting the bound |
| 62 | Recover compatible rigid poses for the fixed UnitSquare `n = 68, 69` parent-child pairs under explicit serialization models | registered | [H-053](hypotheses/H-053-unitsquare-rigid-pose-serialization.md) | [X-011](explorations/X-011-controls-are-not-targets.md) | Directly tests whether the visible near-square distortions are explainable by declared serialization cells; provenance or precision ambiguity produces a typed refusal rather than invented geometry |
| 63 | Reconstruct the reported `n = 50`, `L = 53/7` packing as a complete exact rational certificate | registered | [H-054](hypotheses/H-054-n50-exact-rational-reconstruction.md) | [X-011](explorations/X-011-controls-are-not-targets.md) | A tractable exact control separates side-expression recognition from full-pose reconstruction and calibrates the verifier before harder algebraic witnesses |
| 64 | Promote the selected `n = 54` witness into its reported nested-radical field | registered | [H-055](hypotheses/H-055-n54-nested-radical-promotion.md) | [X-011](explorations/X-011-controls-are-not-targets.md) | Tests an exact algebraic lift at moderate scale; BC-111 must select this case, otherwise it remains registered and unmeasured |
| 65 | Promote the selected `n = 39` witness to a degree-five root-isolated interval certificate | registered | [H-056](hypotheses/H-056-n39-degree-five-interval-certificate.md) | [X-011](explorations/X-011-controls-are-not-targets.md) | Tests the interval path when radicals are unavailable; BC-111 must select this case, otherwise it remains registered and unmeasured |
| 66 | Test parent-bound three-process execution on the fixed `n = 17` exp-052 residue | registered | [H-057](hypotheses/H-057-n17-parent-bound-parallel-speedup.md) | [X-011](explorations/X-011-controls-are-not-targets.md) | Three fixed ordinals and paired exact-byte checks test whether a later continuation is worth routing; they do not decide H-052 or transfer a bound to `n = 18, 19` |
| 67 | Recover one compatible rigid pose for the fixed UnitSquare `n = 68` parent through a production adapter | registered | [H-058](hypotheses/H-058-n68-one-parent-production-serialization.md) | [X-011](explorations/X-011-controls-are-not-targets.md) | A parent-only provenance and serialization determination leaves the child blinded; it does not decide H-053 or open H-051 |
| 68 | Verify that the frozen `n = 50` producer refuses an existing result before every downstream seam | registered | [H-059](hypotheses/H-059-n50-producer-refusal-ordering.md) | [X-011](explorations/X-011-controls-are-not-targets.md) | A prospective sentinel round leaves exp-050 immutable and validates only the successor protocol, not H-054 or `n = 50` feasibility |
| 69 | Upgrade Goebel’s exact `n = 5` second-order obstruction to fixed-side local rigidity | registered | [H-060](hypotheses/H-060-n5-local-rigidity.md) | [X-007](explorations/X-007-the-n5-optimum-flexes-once-and-that-once-is-shut.md) | The Puiseux coefficient argument can close T-012 only after a checked neighborhood reduces nonoverlap to the twenty active contact-normal inequalities and an independent reviewer verifies the curve-selection hypotheses; success proves local rigidity of this pose, not global uniqueness |
| 70 | First-party fractional unavoidable-set certificates on the Burns–Massaccesi architecture, aimed first at `n = 12` with the side fixed before synthesis | registered | [H-061](hypotheses/H-061-n12-first-party-fractional-certificate.md) | Agenda 017 planning, from [X-010](explorations/X-010-two-lanes-two-ladders.md) lane A and [X-011](explorations/X-011-controls-are-not-targets.md) | The generation side of the adopted `4.5058` architecture does not exist here; an LP with the exact event-cell sweep as its separation oracle would produce certificates at every Nagamochi-only size, and any certificate above `2 + 4/√5` at `n = 12` is the first `n = 12`-specific bound. The threshold `19/5` is fixed by `H-039`’s rule and later rungs are registered one at a time |

## Shaped by X-013 and X-014, 2026-09-05

The nine measurements proposed by the two most recent exploration reports, entered on
the board so that a costed, falsifiable proposal has a row rather than aging out of
context (the W7 audit of 2026-09-05 found that X-011’s proposals reached the board and
X-013’s and X-014’s did not).

| # | Idea | Status | H | From | Why it might work, or not |
| --- | --- | --- | --- | --- | --- |
| 71 | Move the generator’s accept-or-reject decision to the interval route, on the integer sweep as baseline (`BC-190`) | shaped |  | [X-013](explorations/X-013-where-the-certificate-should-go-next.md) proposal 1 | Decides `361` doubled-net directions without Condition 1 and was `22.7×`–`44.2×` faster on two atom counts before agenda-020’s integer sweep; killed if its own exponent drifts toward quadratic when re-fitted, or by any disagreement between the routes |
| 72 | Point the next certificate search at `n = 26`, side `5.5218`, once `BC-191` prices the side | shaped |  | [X-013](explorations/X-013-where-the-certificate-should-go-next.md) proposal 2 | Predicted gain `+0.3987`, tied with `n = 51` and `n = 39` at a third of `n = 51`’s gate time; killed if a converged run at `5.52` needs mass above `26` or lands its attained ratio below `0.90` |
| 73 | Measure the covering value’s growth in the side: one genuinely converged restricted optimum past `5.5` | shaped |  | [X-013](explorations/X-013-where-the-certificate-should-go-next.md) proposal 3 | Six measured values sit in a side band of width `0.98`, two unconverged; the first point outside it decides whether growth stays loosely quadratic before the sides the top prizes need |
| 74 | Decide the `n = 11` plateau: `τ*(L)` at `3.82` on a third site set to convergence, and at `3.815`; the fractional packing dual `ν*(L)` at `3.82`, `3.85`, `3.87` | registered | [H-064](hypotheses/H-064-n11-fractional-packing-floor.md) | [X-014](explorations/X-014-closing-from-both-ends.md) measurement 1 | Two site sets stop at exactly eleven and the rejection route caps at `1152/175`; nothing kills it — either outcome fixes the ladder’s top and the tree’s working side |
| 75 | Quantify Trump’s rigidity radius: `κ_b`, `Λ_b/‖λ_b‖₁` on all `128` branches, a curvature bound `K`, `ρ₀ = min_b 2κ_b/K` and the stress constant `C` | shaped |  | [X-014](explorations/X-014-closing-from-both-ends.md) measurement 2; `BC-176` and [H-022](hypotheses/H-022-trump-local-geometry.md) own the theorem form | Exact linear algebra on `cases.trump11.tangent_cones`; killed if `ρ₀` falls below `10⁻⁶` in the chart, since no tree reaches a box that small |
| 76 | Census of tight event cells (mass at most `1 + ε`, `ε ∈ {0, 0.01, 0.05, 0.1}`) on the retained `381/100` certificate and on the `3.82` atom set | registered | [H-065](hypotheses/H-065-n11-near-tight-cell-census.md) | [X-014](explorations/X-014-closing-from-both-ends.md) measurement 3; Corollary 1b | A per-cell readout of the mass grid the sweep already fills; killed if the tight set at `ε = 0.05` covers most of the centre domain |
| 77 | Twelve class certificates at a rational side just above `U`, one per composition `n₁`, with the near-axis class the union of the net’s first nineteen half-gap cells | registered | [H-063](hypotheses/H-063-n11-class-certificate.md) | [X-014](explorations/X-014-closing-from-both-ends.md) measurement 4; Lemma 3 | A threshold change to the covering program, no new geometry; killed if the `n₁ = 0` class fails to certify above `U` |
| 78 | The handshake: one conditional certificate at side `U − 0.01` with all eleven squares boxed at radius `0.05` about Trump’s pose | shaped |  | [X-014](explorations/X-014-closing-from-both-ends.md) measurement 5; Lemma 2 multi-box form | Needs the domain generalisation and a quarter-turn net; time one node first with a coarse net; killed if the conditional value stays at or above `11` |
| 79 | The `n = 13` calibration: Bentz’s corner-restricted configuration at side `399/100` as a conditional certificate with two boxed squares and their forced points as cores | shaped |  | [X-014](explorations/X-014-closing-from-both-ends.md) measurement 6 | A case the classical method closes by hand; killed if the boxed case still returns mass at or above `13`, which would say conditioning cannot close even that |
| 80 | Measure the `m = 5` covering wall: bisect `n = 20` from `24/5` toward the ceiling `4.9885` on four pre-registered rungs, reading the `n = 21` criterion at each | registered | [H-062](hypotheses/H-062-n20-covering-wall.md) | [X-015](explorations/X-015-the-map-and-the-three-programs.md), from X-013 and X-014 | The one place in the register where the covering value is the only thing that can bind before the ceiling, since the best packing at `n = 20, 21` is the grid; the finite-difference estimate puts the `n = 20` wall at `4.92`–`4.94` and the `n = 21` wall above the ceiling |
| 81 | Run the existing generator at `n = 13`, side `399/100`, as a zero-build calibration of the grid-frontier program against a case Bentz closed by hand | shaped |  | [X-015](explorations/X-015-the-map-and-the-three-programs.md) | The extrapolated covering value at the ceiling is about `12.06`–`12.24 < 13`, so one unconditional certificate may reach within `0.0092` of `s(13) = 4`; a converged optimum at or above `13` says the endgame at `m = 4` is a tree |
| 82 | The `B = 1` route: closed-square covering with open-box counting at an integer side, certified over the direction continuum by angle-interval branch and bound, first at `n = 13` (side `4`) and then `n = 21` (side `5`) | shaped |  | [X-015](explorations/X-015-the-map-and-the-three-programs.md); X-014 §"`n = 12` Is a Different Proof"; BC-193 | The only route past the ceiling `⌈√n⌉/(1 + D)`: a quarter-turn net alone buys nothing at `B = 1`, so the instrument needs Condition 5 at every angle; Bentz’s `s(46) = 7` is one such certificate at side exactly `7`, already audited here |

## Registered by X-016 and Agenda 025, 2026-09-05

| # | Idea | Status | H | From | Why it might work, or not |
| --- | --- | --- | --- | --- | --- |
| 83 | Use Massaccesi-style inset margins only to propose an `n = 11` fractional seed, then release the support and compare it with an equal-budget unrestricted control | registered | [H-070](hypotheses/H-070-n11-inset-seed-release.md) | [X-016](explorations/X-016-after-381-two-managers-one-proof-boundary.md) and agenda-025 BC-233 | A seed clustered away from walls may reach a better column set sooner, but the claim fails on equal or larger exact mass and remains unresolved on unmatched stopping states; it proves neither that walls are irrelevant nor that the inset grid is unavoidable |
| 84 | Shrink the T-018 core with the atoms fixed, normalize by the exact minimum mass, then dilate to a rational side above T-022 | registered | [H-090](hypotheses/H-090-n11-fixed-atom-core-shrink.md) | [X-016](explorations/X-016-after-381-two-managers-one-proof-boundary.md), coordinator satellite think-zq2u | Coverage may fall below one and still work if it stays above total mass divided by eleven; finite atom events can also cause an immediate discontinuous loss |
| 85 | Test a smaller core above the exact corner event lost by H-090, with the same mass-normalization rule | registered | [H-091](hypotheses/H-091-n11-narrow-core-shrink.md) | exp-110, coordinator satellite think-jthr | The first negative excludes only sides below `1849127/1853400`; side `997696/1000000` is above that event and leaves enough containment slack to beat T-022 if all remaining cells retain mass above `M/11` |

## Post-3.81 Planning Questions

BC-250 codified these directions from
[X-016](explorations/X-016-after-381-two-managers-one-proof-boundary.md) and the
[three-model strategy review](../../docs/project/reviews/review-2026-09-05-strategy-gpt-56-pro-gemini-grok.md).
The [agenda allocation](agendas/agenda-024-post-381-24h-portfolio.md#current-allocation)
owns scheduling; the registry and generated ledger own claim scope and status.
Open questions are registered but not runnable experiments.
Row 86 belongs to the pending refined-core transport.

| # | Idea | Status | H | Crux |
| --- | --- | --- | --- | --- |
| 87 | Scalar certificate at 61/16 | registered | [H-093](hypotheses/H-093-n11-scalar-61-16-certificate.md) | Use the existing instrument once; a floating objective is not a certificate. |
| 88 | Change relative weights and event-guided site support | registered | [H-094](hypotheses/H-094-n11-weight-and-site-redesign.md) | Escape the fixed-weight restriction, starting with exact bad-pose rows. |
| 89 | Adaptive cores and nonuniform angle cells | registered | [H-095](hypotheses/H-095-n11-adaptive-core-certificate.md) | A complete containment/coverage decision must precede synthesis. |
| 90 | Rational angle-cell kernels | registered | [H-096](hypotheses/H-096-n11-angle-cell-kernels.md) | Extra captured mass matters; extra area alone does not. |
| 91 | Existential witness menus | registered | [H-097](hypotheses/H-097-n11-existential-witness-menus.md) | Prove the whole-pose-box selection statement before a global verifier. |
| 92 | Segment-supported measures | registered | [H-098](hypotheses/H-098-n11-segment-measures.md) | Exact intersection mass replaces binary atom incidence. |
| 93 | Nonuniform weights on the exact D4 Trump support | registered | [H-099](hypotheses/H-099-trump-d4-finite-support-dual.md) | A necessary-row LP can certify a support ceiling; D>11 needs full a.e.-depth verification. |
| 94 | Full-size area density below Trump | registered | [H-100](hypotheses/H-100-below-trump-area-density.md) | Continuum coverage and mass below eleven at a separately selected side. |
| 95 | Equality density at Trump | registered | [H-101](hypotheses/H-101-trump-equality-density.md) | Requires both an actual density and complete compatible equality-set classification. |
| 96 | Complete restricted angle or wall-support theorems | registered | [H-102](hypotheses/H-102-complete-restricted-angle-support-families.md) | Start from H-036; proof and falsifier test the same claim independently. |
| 97 | Typed global capture with conditional/configuration cuts | registered | [H-103](hypotheses/H-103-complete-typed-global-capture.md) | Complete coverage, sound cuts, and exact local capture are separate obligations. |

Exact basis recovery and Lean replay support the relevant candidate or assurance bead;
they are not additional mathematical hypotheses without a specific method comparison.

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
- **[What quantitative local geometry remains after exp-013?](hypotheses/H-022-trump-local-geometry.md)**
  Exact contacts alone did not establish isolation; exp-013 now does.
  The live question is an explicit radius, side-perturbation stability, and transferable
  stress structure.
- **[Are the observed `n=5` endpoints in one terminal family?](hypotheses/H-023-n5-terminal-connectivity.md)**
  Exp-033 connects the equal-side pair inside one exact fixed-angle optimal face; full
  stationary connectivity and unequal-side clearance remain open.
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
  Replaced by H-026’s exact branchwise linearized-cone screen, confirmed by exp-013.

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
