# Research: Infrastructure for Square-Packing Exploration

**Date:** 2026-08-22 (last updated 2026-08-25)

**Author:** Claude (agent), for samanthadrakova@gmail.com

**Status:** Complete

## Overview

This document decides what to build.
It synthesizes the two prior tooling studies —
[algorithms and tooling](research-2026-08-22-square-packing-algorithms-and-tooling.md),
which found no purpose-built exact verifier in the surveyed ecosystem and argued for a
filtered exact-predicate kernel over a real algebraic number field, and
[the FrankenSim study](research-2026-08-22-frankensim-rust-toolkit-for-square-packing.md),
which found most of the pieces of that architecture already built for a different
purpose — and turns them into a concrete build order.

**Current implementation note (2026-08-25).** The repository now ships the first
purpose-built slice of that design: `Witness/v1`, exact rational and real-algebraic
separating-axis checks, certified number-field preconditions, and a public
`packing-witness` command.
The broad filtered kernel, automatic source-corpus import, and a general interval
existence certifier remain unbuilt.
The design below is therefore a rationale and roadmap, not a claim that every described
layer is still missing.

The design principle is Alan Kay’s: **simple things should be simple, complex things
should be possible.** For this project that has a precise reading.
Simple is *“is this packing valid?”* — one call, no setup, and an answer before you have
finished reading the line.
Complex is *“run 65,536 annealing chains with reproducible randomness and formally check
every candidate that clears a threshold”* — which should be reachable by composing the
same primitives, not by writing a second system.

The single design decision that makes both work is that **the geometric predicate is
written once and is generic over its scalar type.** If making a check exact requires a
different implementation of the separating-axis test, the design has failed: the two
implementations will drift, and the fast one will be the one that is wrong.

Three findings frame the rest.

1. **Latency has three tiers here, not one, and the tiers want different languages.**
   Most of this project’s computation is attached to an LLM call and is therefore free —
   a 350 ms verification is invisible next to a 3-second model turn.
   A small, identifiable part runs `10⁹`–`10¹²` times inside a search loop and is
   nothing of the kind.
   The boundary between those two is where the API belongs.
2. **The measured gaps are large enough to decide the architecture, and they are not
   uniform.** Rust beats Python by **48×** on the separating-axis predicate (57 ns
   versus 2,726 ns per pair test, measured below).
   FLINT beats pure-Python field arithmetic by **177×** at algebraic degree 8 and by
   **578×** at degree 62 — the advantage *grows* exactly where the record table gets
   hard.
3. **Determinism is a correctness requirement, not an optimization.** The most valuable
   artifact this field has produced is Ellsworth’s basin statistics for `s(51)` — 3,004
   basins, 4 of them the record.
   A search that cannot reproduce its own runs cannot publish that kind of number, and
   that is the main thing an open engine could contribute that the closed one has not.

## Questions to Answer

1. Which parts of this research are performance-critical, and which are not?
2. What is the right language boundary, and what belongs on each side?
3. What are the building blocks, in what order should they be built, and what makes them
   composable rather than monolithic?
4. Is SymPy the right symbolic layer, and if not, what replaces it and where?
5. What should be taken from FrankenSim, and what should be deliberately left?
6. What should *not* be built?

## Scope

**Included:** the computational infrastructure for searching, verifying, and reasoning
about unit-square packings; the language and library choices behind it; the performance
budget of each part; and the discipline needed for results to be citable.

**Excluded:** the mathematics of `s(n)` (see
[the `n = 11` report](research-2026-08-22-packing-11-unit-squares.md)); the record
history; and any judgement about whether a given search strategy will succeed.
This is about the substrate, not the program that runs on it.

## Findings

### The three latency tiers

Almost every infrastructure mistake available here comes from treating this as one
performance problem.
It is three, and they have budgets that differ by nine orders of magnitude.

| Tier | Budget per operation | What lives here | Right tool |
| --- | --- | --- | --- |
| **Agent** | 1–10 s | Deriving a number field from a published polynomial; parsing the record corpus; verifying one packing; recovering a minimal polynomial; rendering a table; anything an agent calls between model turns | Python, SymPy, whatever is clearest |
| **Interactive** | 10 ms – 1 s | Verifying a packing in a notebook; querying the frontier corpus; a bulk re-verification of all 184 pictured records | Python over a native core |
| **Inner loop** | 10 ns – 1 µs, executed `10⁹`–`10¹²` times | The separating-axis predicate inside an annealing sweep; the three-parameter decision inside an unavoidable-set search | Native, monomorphized, no allocation |

**The agent tier is genuinely free, and it is most of the work.** A model turn costs
seconds. The complete exact verification of Trump’s packing — 55 pairs, exact arithmetic
in `ℚ(u)`, no floating point in the decision path — costs **0.35 s of unoptimised pure
Python**. Optimising that is optimising noise.
This is the tier where “simple should be simple” is the only requirement that matters,
and where a dependency on SymPy costs nothing.

**The inner-loop tier is a different problem entirely**, and the fact that it *shares
its geometry* with the agent tier is the whole design difficulty.

### Measured: where the time actually goes

All measurements taken in this container on 2026-08-22; see [Methodology](#methodology).
They are indicative of relative cost, not of what tuned code on a known machine would
achieve — the caveat the FrankenSim study argues should attach to every number.

**The inner-loop predicate.** The separating-axis test for two unit squares at arbitrary
angles, evaluated over a fixed mix of separated and overlapping placements:

| Implementation | Rate | Per test |
| --- | --- | --- |
| Python (this repo’s float backend, same algorithm) | 366,797 /s | 2,726 ns |
| Rust, `-O -C target-cpu=native -C lto`, `f64` | **17,660,641 /s** | **57 ns** |

A **48× gap** on the operation a search executes most.
Expressed as budget rather than ratio: one CPU-hour buys 1.3 G pair-tests in Python,
63.6 G in single-core Rust, and about 2,000 G on 32 cores.
The published `s(51)` campaign — 3,004 basins at ~23.6 s each on a GPU — is the scale
this has to reach to be interesting, and that is the difference between a plausible CPU
campaign and an impossible one.

**Exact field arithmetic.** One multiplication in `ℚ(α)` with dense random elements, at
the algebraic degrees that actually occur in the record table:

| Degree | Occurs at | Pure Python (`fractions.Fraction`) | python-flint (`fmpq_poly mod m`) | Speedup |
| --- | --- | --- | --- | --- |
| 8 | `s(11)` | 215.5 µs | 1.2 µs | **177×** |
| 18 | `s(17)` | 1,071.7 µs | 3.0 µs | **363×** |
| 40 | `s(300)` | 5,978.7 µs | 13.1 µs | **457×** |
| 62 | `s(1453)` | 13,490.5 µs | 23.3 µs | **578×** |

Two things to read from this.
The speedup **grows with degree**, so pure Python is worst exactly where the problem is
hardest — the record table reaches degree 62, and the whole point of an exact verifier
is to handle the analytically solved cases rather than the easy ones.
And the absolute numbers say the crossover is not close: at degree 62 a single field
multiplication in Python costs more than 13 ms, which is a quarter of a second for a
hundred of them.

### The one decision that makes simple and complex the same system

The separating-axis test has a property that decides the architecture: **every quantity
it tests is a polynomial in the configuration variables.** Four candidate axes, eight
dot products per axis, no divisions and no square roots.
That means the identical algorithm is correct over `f64`, over intervals, and over an
exact algebraic field — only the scalar type changes.

So the predicate is written **once**, generic over a `Scalar` trait supplying `+ − ×`
and a sign decision, and instantiated at:

| Scalar | Decides | Cost | Used for |
| --- | --- | --- | --- |
| `f64` with a tolerance | approximately | 57 ns | search inner loop |
| `f64` plus an error bound, escalating | strictly, when the margin is wide | ~60 ns typical | filtered kernel’s first stage |
| Interval (outward-rounded) | strict separation only; *never* equality | ~µs | second stage |
| `ℚ(α)` exact | everything, including exact zero | ~µs–ms by degree | contacts, and only contacts |

This repo’s Python verifier already has the shape right —
`verify_packing(..., sign=exact_sign)` versus `sign=float_sign(1e-9)` is exactly this
generic, and the two backends share one implementation of the test.
Rust monomorphizes it at zero cost instead of paying dynamic dispatch per call.

**Why the staging matters more than any single stage.** In a record packing only `O(n)`
pairs actually touch; the rest are separated by a wide margin.
For `n = 11`, 14 pairs of 55 have exactly zero gap and 41 are strictly separated.
A filtered kernel settles those 41 in floating point and pays the exact price only on
the 14. That is CGAL’s `Exact_predicates_*` design, and it is why “exact verification”
is cheap in practice rather than catastrophic.

**The correction that must not be lost.** The FrankenSim probe established that
Shewchuk’s `orient2d` — exact for its `f64` inputs — settles 47 of the 55 pairs and
finds **8 with no separating axis at all**: at 16 significant digits the published
packing genuinely overlaps.
That is a true statement about the *rounded* configuration and the wrong answer about
the real one. So the predicate *ladder* transfers from computational geometry, and **the
number type must not**: exact-for-`f64` answers a question we are not asking.
Any design that reaches for the excellent existing Rust Shewchuk crates (`robust`,
`geometry-predicates`) as the exact stage has made this mistake.

### The layers to build

Five layers, each independently useful, each the substrate for the next.
The Kay test applied to each: what is the one-line version, and what is the hard thing
it still permits?

**L0 · `sqpack-core` (Rust).** Geometry and predicates.
Corner generation, the separating-axis test, container containment, and uniform-grid
bucketing so pair enumeration is `Θ(n)` rather than `Θ(n²)`. Generic over `Scalar`; no
allocation on the hot path; no I/O. *Simple:* `separated(&a, &b)`. *Possible:*
instantiate it over an exact field and get a certificate instead of a guess.
This is the layer both the search and the verifier depend on, and the reason they cannot
drift apart.

**L1 · `sqpack-exact` (Rust).** The `Scalar` implementations and the filtered ladder.
`f64`, an outward-rounded interval type, and an algebraic type over `ℚ(α)`: elements as
polynomials of degree `< deg m` reduced modulo the minimal polynomial, exact zero by
representative test, exact sign by rational interval evaluation with bisection.
Back it with FLINT rather than reimplementing — the measurements above are the argument,
and the degree-62 cases are where a hand-rolled implementation would fail quietly.
*Simple:* `verify(packing)` returns a decision, not a tolerance.
*Possible:* stage-by-stage filter-rate telemetry, so the cost model is measured rather
than assumed.

**L2 · `sqpack-search` (Rust).** The engines.
Perturbed billiard/inflation and simulated annealing over L0, with three properties
copied deliberately from FrankenSim:

- **Counter-based RNG keyed by logical work identity** — `(seed, kernel, tile, index)`
  with `O(1)` random access, so a restart is reproducible and a basin is addressable.
- **Fixed-slot reductions folded in tile order**, so worker count never changes the
  answer.
- **Speculative races with loser cancellation**, which is precisely the shape of “run
  65,536 chains and keep the best”.

*Simple:* `anneal(n, budget)`. *Possible:* resume a campaign bit-exactly, or replay one
basin from its key alone.

**L3 · `sqpack` (Python, PyO3 bindings).** The surface almost everything actually
touches. Loading a packing from the corpus, verifying it, querying the frontier data,
plotting. This is where the agent tier lives, and it should feel like a small library,
not a framework. Every function here is allowed to be “slow” — the tier budget is
seconds.

**L4 · Corpus tooling (Python).** The SVG record parser that turns the catalogue’s
33-digit decimal entities and Mathematica `Root[…]` comments into `(x, y, θ)` triples
with their algebraic definitions — the missing geometry noted in the
[frontier corpus](../../../frontier/README.md) and tracked as its own work item.
Agent tier, run once per record, performance irrelevant.

### Symbolic and exact arithmetic: what to use where

The question “is SymPy the right choice?”
has a tier-dependent answer, which is why it has felt ambiguous.

**Keep SymPy at the agent tier.** `derive_field.py` runs once per packing, takes under a
second, and is read by humans.
Its clarity is worth more than its speed, and its speed is irrelevant at that tier.
Replacing it would be optimizing the wrong thing.

**Use FLINT wherever arithmetic is in a loop.** Measured above at 177–578×, growing with
degree. Two access routes:

- `python-flint` (confirmed working here at 0.9.0) exposes `fmpq_poly` and `arb`, which
  is everything the field layer needs.
  Note that **Calcium’s `ca_t` is not exposed** in 0.9.0 — `hasattr(flint, "ca")` is
  `False` — although FLINT’s generic-rings interface reaches it.
  Calcium is the *conceptually right* abstraction for this problem, since it constructs
  extension fields lazily and lets equality of algebraic numbers be decided rather than
  approximated; it is worth watching rather than depending on today.
- `flint-sys` FFI from Rust for L1, or `rug` (GMP/MPFR/MPC) if the dependency surface
  matters more than the last factor of two.
  `malachite` is the pure-safe-Rust option and avoids the C toolchain, at some
  performance cost.

**Use `msolve` for elimination.** Turning contact equations into a minimal polynomial is
an F4 Gröbner computation plus real root isolation, and `msolve` is the fastest
open-source implementation of exactly that; recent comparative work puts competing
implementations within a factor of about 1.4 of it.
This is agent-tier work — once per packing — but “once” on a hard system can still be
hours, which is where the constant factor earns its place.

**Use PARI `algdep` or LLL directly for numeric-to-symbolic recovery.** Recovering a
degree-40 or degree-62 minimal polynomial from a thousand-digit decimal is an
integer-relation problem.
This is the step that makes the Jacobian-determinant trick matter: it keeps the pipeline
a *root-finding* problem, which reaches the precision `algdep` needs, instead of a
*minimization* problem, which does not.

**What not to reach for.** A Mathematica dependency, because the corpus’s exact data
being trapped in a Mathematica dialect is already the problem, not the solution.
A second language runtime (Julia’s Oscar/Nemo are excellent and would buy nothing that
FLINT does not, at the cost of a whole toolchain).
And a general computer-algebra system written in Rust: the requirement here is narrow —
one number field, four arithmetic operations, an exact sign — and FFI to FLINT is the
short path.

### What to take from FrankenSim, and what to leave

The FrankenSim study’s own conclusion was that the transferable asset is the design, not
the code. Sharpened into a list, with the reason each item is on it:

**Take, in priority order.**

1. **Counter-based RNG keyed by logical work identity.** This is the single
   highest-value import.
   It is what makes basin statistics mean something, and basin statistics are the most
   informative artifact this field has.
2. **Fixed-slot reductions in tile order.** Worker-count invariance by construction
   rather than by testing.
3. **The staged predicate ladder shape** (`Filtered → Adaptive → Exact`) with per-stage
   filter-rate tests — the shape, over our number types.
4. **Determinism classes as a declared, lint-enforced property.** Every component
   declares `Deterministic`, `DeterministicPerIsa`, or `Fast`, and the mode is stamped
   into every recorded result so a `Fast` run cannot be quoted as bit-stable.
   For a project whose output is records other people will cite, this is worth more than
   it costs.
5. **The two determinism lints**, which are about a hundred lines of `xtask`: ban
   `.powi(n)` for `|n| > 3`, and ban platform `libm` in any component claiming cross-ISA
   reproducibility. Both are documented there with the incident that motivated them; the
   `powi` story — a golden hash re-pinned with a plausible but wrong justification, when
   the real mover was optimization-level-dependent `powi` — is the better cautionary
   tale.
6. **The measurement discipline.** Median and interquartile dispersion on every timing,
   a machine fingerprint, and a baseline-promotion protocol that refuses to run on a
   loaded host. “A benchmark without variance bars is folklore.”
7. **Claim integrity as its own defect class.** Any surface that can report a stronger
   epistemic state than its evidence establishes is a bug of a distinct kind.
   A float verifier returning “valid” is the canonical instance.

**Leave.**

- **The crates themselves.** The MIT-with-rider licence aside, a dependency drags in a
  pinned nightly, seven sibling checkouts at exact heads, and a constellation that does
  not currently resolve.
  The ideas are small; reimplement them.
- **`Evidence<T>` and the governance apparatus.** Right at the scale of a hundred-crate
  multiphysics system with model-form uncertainty.
  A packing verifier has one kind of uncertainty and a two-valued answer;
  `Result<Certified, NotProven>` carries the whole story.
- **A roofline crate.** Adopt the discipline, not the code.
- **GPU, for now.** The record engine is a GPU annealer, but 32 Rust cores buy roughly
  2,000 G pair-tests per hour, and CPU is where determinism and exactness are tractable.
  Revisit after measuring a CPU campaign, not before.

### Determinism is a correctness requirement here

Worth stating separately because it is easy to file under “nice to have”.

The reason to build an open search engine at all is not that it would find better
packings than the closed one — that is unlikely and unnecessary.
It is that a search whose randomness is a pure function of `(seed, kernel, tile, index)`
can answer questions the current tooling cannot: how many basins are there, how rare is
the record basin, how does that rarity scale with `n`, does a given move set change the
basin distribution. Ellsworth published that for two values of `n` and it immediately
became the most quantitative thing known about the problem’s landscape.

A tolerance-based verifier undermines this in a specific way.
If the acceptance test has a blind spot — and as the tooling study establishes, every
float verifier does, since no tolerance both accepts exact contacts and rejects small
overlaps — then a basin count includes configurations that are not packings.
The exact verifier is not a luxury bolted onto the search; it is what makes the search’s
output a measurement.

## Key Insights

1. **Three latency tiers, not one, and most of the work is in the free tier.** Anything
   attached to an LLM call has a budget of seconds, and the full exact verification of
   `s(11)` costs 0.35 s in unoptimised Python.
   Optimizing the agent tier is optimizing noise; the discipline is knowing which code
   is not in it.
2. **The predicate is a polynomial, so one implementation serves every precision.** Four
   axes, eight dot products, no division and no square root.
   That single structural fact is what lets “simple” and “complex” be the same system:
   the scalar type changes, the algorithm does not.
3. **The measured gaps are decisive and unequal.** 48× for the search predicate (Rust
   over Python); 177–578× for field arithmetic (FLINT over pure Python), *growing with
   algebraic degree*. The second is the more consequential, because it grows precisely
   toward the record table’s hard cases.
4. **Filtering, not raw exact speed, is what makes exactness affordable.** Only the
   `O(n)` touching pairs need the exact path — 14 of 55 at `n = 11`. A staged kernel
   spends floating-point time on the 41 and exact time on the 14.
5. **Exact-for-`f64` is the wrong exactness.** Shewchuk predicates answer exactly the
   question “do these rounded coordinates overlap”, and the published 16-digit decimals
   *do* overlap on 8 pairs.
   The ladder’s shape transfers; its number type does not.
   This is the most specific technical trap in the whole design.
6. **Determinism is what would make an open engine worth building.** Not speed — the
   closed engine is fast.
   Reproducible randomness keyed by work identity is what turns a search into a
   measurement, and basin statistics are the field’s most informative artifact.
7. **SymPy is not the problem; SymPy in a loop is.** Keep it where clarity matters and
   the tier is seconds.
   Replace it with FLINT where the same operation runs a thousand times, and with
   `msolve` where the operation is elimination.
8. **The most valuable single artifact is still not the search.** It is a
   machine-readable record corpus plus an exact checker: it makes every published record
   independently auditable for the first time, it is a few hundred lines on top of
   FLINT, and every other item on this list consumes it.

## Recommendations

The build order, with the Kay test as the acceptance criterion for each.
Items 1–3 are cheap and unlock everything else; 4–5 are the actual research programme.

1. **L4 corpus parser, then L1 exact kernel, in that order.** The parser is agent-tier
   Python and turns the catalogue into data; the kernel makes that data checkable.
   Together they aim to make every supported record independently auditable.
   *Acceptance:* `sqpack.verify(corpus["s(11)"])` is one line and returns a decision,
   not a tolerance; and the same call works at degree 62 without a different code path.
2. **L0 in Rust, generic over `Scalar`, with the Python verifier kept as the oracle.**
   The existing pure-Python implementation becomes the differential-test reference:
   every Rust predicate result must match it on the whole corpus.
   That is what stops the fast path from being the wrong one.
   *Acceptance:* one predicate implementation, four scalar instantiations, zero
   divergence on the corpus.
3. **Instrument before optimizing anything else.** Per-stage filter rates in the kernel,
   and order statistics with a machine fingerprint on every timing.
   The FrankenSim rule is the right one: no performance claim without a benchmark, a
   target, a fingerprint, and an acceptance band.
4. **L2 search, CPU-first, determinism from day one.** Counter-based RNG and fixed-slot
   reductions are cheap at the start and near-impossible to retrofit.
   Aim first at reproducing known records for small `n`, which is a test with a known
   answer, before aiming at anything unknown.
   *Acceptance:* the same seed reproduces the same basin on 1 core and on 32.
5. **The proof lane reuses all of it.** Verifying that a candidate point set is
   unavoidable — “does every unit square in `[0,k]²` contain a point of `P`?” — is a
   decision over three parameters `(x, y, θ)`, which is L0’s geometry with a different
   quantifier. Searching for such sets is L2 with a different objective.
   Nothing automated has ever run in this lane, and it is the one where a new result
   would be a theorem rather than a record.

**What not to build:** a GPU engine before a CPU one is measured; a computer-algebra
system in Rust; a dependency on the Franken crates; a governance layer; and a second
implementation of the separating-axis test for any reason whatsoever.

## Open Questions

- [ ] What is the real filter rate on the record corpus — what fraction of pairs
  actually need the exact path at each `n`? The `n = 11` figure is 14 of 55, but that is
  one case and it is the smallest.
- [ ] Does the CPU budget actually reach the published GPU campaign?
  32 cores gives roughly 2,000 G pair-tests per hour by extrapolation from a single-core
  measurement; the extrapolation assumes linear scaling and no memory-bandwidth wall,
  and neither has been tested.
- [ ] Is `rug` or `flint-sys` the right Rust binding for L1, and how much does the
  pure-safe-Rust alternative (`malachite`) cost in practice at degree 40–62?
- [ ] When Calcium’s `ca_t` becomes reachable from `python-flint`, does its lazy field
  construction remove the need to recover the number field by hand — the step the
  tooling study identifies as the expensive one?
- [ ] Does the annealing move set need exact arithmetic anywhere, or is
  float-plus-refine plus a final exact check sufficient?
  Cheap to test and it decides how much of L1 the search actually links against.
- [ ] What does an unavoidable-set decision cost per evaluation, and is the search space
  small enough that L2’s machinery is even needed for the proof lane?

## Methodology

Conducted 2026-08-22. This document is a synthesis of two prior studies plus original
measurement; the prior studies’ own methodology sections cover their sources.

**Measurements taken here.**

- **Separating-axis predicate, Rust.** A self-contained
  `rustc -O -C target-cpu=native -C lto` binary, 20,000,000 pair tests over 4,096
  deterministic pseudo-random placements mixing separated and overlapping cases, timed
  as a single batch after the case table is built.
  Reported: 17,660,641 tests/s, 56.6 ns/test.
- **The same predicate, Python.** Same algorithm, same case-generation logic and seed,
  200,000 tests. Reported: 366,797 tests/s, 2,726 ns/test.
  The comparison holds the algorithm fixed and varies only the language.
- **Field multiplication.** One multiplication in `ℚ(α)` at degrees 8, 18, 40 and 62,
  comparing this repo’s `sqpack.field.NumberField` (`fractions.Fraction`) against
  `python-flint`’s `fmpq_poly` reduced modulo the minimal polynomial.
  Operands are **dense** random elements with rational coefficients, which is the honest
  case; an earlier sparse trial understated the pure-Python cost by an order of
  magnitude and is not reported.
  Minimal polynomials are random with a checked sign-change interval, since arithmetic
  cost, not irreducibility, is what is being measured.
- **Library availability.** `python-flint` 0.9.0 installed and checked directly:
  `fmpq_poly` and `arb` present, `ca` **absent** — the Calcium claim in this document is
  from that check, not from documentation.

**All figures are single-machine and unpinned.** This container’s CPU was not
characterised, no baseline was promoted, and no acceptance band is attached — which by
the standard this document itself recommends means they are indicative, not citable.
They are reported as ratios wherever the ratio is what carries the argument.

**Not established.** No Rust field-arithmetic implementation was built or measured, so
the L1 recommendation rests on the Python-binding measurement plus the general
expectation that FFI overhead is small relative to a degree-62 multiplication.
Multi-core scaling was extrapolated linearly from a single-core figure and not measured.
No comparison was run against CGAL.

**Confidence.** High for the measured ratios and for the architectural conclusions that
follow from the predicate being polynomial.
Medium for the build order, which encodes a judgement about what is most useful first
rather than a measurement.
Low for the multi-core extrapolation, which is flagged above and in
[Open Questions](#open-questions).

## References

Prior studies in this repository, which this document synthesizes:

- [Algorithms and Tooling for Square Packing](research-2026-08-22-square-packing-algorithms-and-tooling.md)
  — the exact-verification argument, the tool-stack survey, the record-format analysis.
- [FrankenSim as a Rust Toolkit for Square Packing](research-2026-08-22-frankensim-rust-toolkit-for-square-packing.md)
  — the determinism engineering, the certified-arithmetic layer, the measurement
  discipline.
- [Packing 11 Unit Squares in a Square](research-2026-08-22-packing-11-unit-squares.md)
  — the mathematics, and the research programme this infrastructure serves.

Libraries and tools referenced:

- [FLINT](https://flintlib.org/) — `fmpq_poly`, `arb` ball arithmetic, and Calcium for
  exact real and complex fields.
  [python-flint](https://pypi.org/project/python-flint/) is the Python binding;
  [Calcium’s design](https://fredrikj.net/math/calcium2020lfant.pdf) is the reference
  for lazy exact-field construction.
- [msolve](https://msolve.lip6.fr/) — F4 Gröbner bases and real root isolation; the
  fastest open-source polynomial-system solver.
- [`rug`](https://crates.io/crates/rug) (GMP/MPFR/MPC bindings) and
  [`malachite`](https://www.malachite.rs/) (pure safe Rust) — the two Rust
  arbitrary-precision options.
- [`inari`](https://github.com/unageek/inari) — IEEE 1788 interval arithmetic in Rust.
- [`robust`](https://github.com/georust/robust) and
  [`geometry-predicates`](https://crates.io/crates/geometry-predicates) — Rust ports of
  Shewchuk’s adaptive predicates.
  Correct for `f64` inputs, and therefore the wrong exactness for this problem; see
  [the ladder discussion](#the-one-decision-that-makes-simple-and-complex-the-same-system).
- [`jagua-rs`](https://github.com/JeroenGar/jagua-rs) — MPL-2.0 collision-detection
  engine for 2-D irregular cutting and packing, with continuous rotation.
  The tooling study’s recommended foundation for a search engine.
- [CGAL `Exact_predicates_exact_constructions_kernel`](https://doc.cgal.org/latest/Kernel_23/index.html)
  — the filtered-kernel design this document copies.
- [PyO3](https://pyo3.rs/) — the Rust/Python binding layer for L3.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
