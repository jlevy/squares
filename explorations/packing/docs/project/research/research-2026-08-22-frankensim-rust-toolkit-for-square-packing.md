# Research: FrankenSim and the Franken Constellation as a Rust Toolkit for Square Packing

**Date:** 2026-08-22 (last updated 2026-08-22)

**Author:** Claude (agent), for samanthadrakova@gmail.com

**Status:** Complete

## Overview

This document is a first-hand study of
[FrankenSim](https://github.com/Dicklesworthstone/frankensim), Jeffrey Emanuel’s
agent-coded Rust simulation framework, and the six sibling repositories it depends on.
The question behind it is practical: we want the most efficient possible toolkit for
searching for square packings, verifying proposed ones exactly, and supporting proof
efforts — and this is a large, recent, performance-conscious Rust codebase in an
adjacent domain. What in it is worth taking?

It follows two earlier documents: `research-2026-08-22-packing-11-unit-squares.md` (the
mathematics of `s(11)`) and
`research-2026-08-22-square-packing-algorithms-and-tooling.md` (the algorithms and
tooling for search and exact verification).
The second of those concluded that no purpose-built exact verifier exists and that the
right architecture is a filtered exact-predicate kernel over a real algebraic number
field. FrankenSim turns out to contain most of the pieces of exactly that architecture,
built for a different purpose.

Four findings frame everything below.

1. **The certified-arithmetic layer is directly on target.** `fs-ivl` is a from-scratch
   safe-Rust implementation of Shewchuk’s adaptive exact predicates, outward-rounded
   interval arithmetic, affine forms, Taylor models, and Krawczyk root certification.
   Run against Trump’s 11-square packing, it reproduces our exact verifier’s answer pair
   for pair.
   [Measurements below.](#measured-what-fs-ivl-can-and-cannot-certify-about-a-packing)

2. **The determinism engineering is the most valuable transferable asset**, more so than
   any single algorithm.
   A three-class determinism taxonomy, counter-based RNG keyed by logical work identity,
   fixed-slot tile reductions, lint-enforced bans on platform `libm` and on `powi`, and
   golden hashes coupled to semantic-surface versions together solve the problem a
   massively parallel packing search actually has: making a GPU or many-core stochastic
   search reproducible.

3. **The performance methodology is unusually disciplined and worth copying wholesale.**
   Measured machine axes rather than spec sheets, median plus interquartile dispersion
   on every timing, a baseline-promotion protocol that refuses to run on a loaded host,
   and a standing rule that a performance claim without a machine fingerprint and
   acceptance band is not a claim.

4. **The repository does not build from its own documented quick start**, and its own
   scorecard reports zero ledgered run records and zero external validation datasets.
   Both facts are verified below.
   This is a machine for making honest claims that has not yet made many validated ones
   — which is roughly what its authors say about it.

## Questions to Answer

1. How is FrankenSim built, and how does a simulation actually get assembled and run?
2. Does it build and pass its tests, and what did that take?
3. Which parts, if any, help with square packing — search, exact verification, or proof
   support?
4. What Rust performance-engineering practices does it encode, and are they backed by
   evidence?
5. What other repositories by the same author carry reusable practices or libraries, and
   what is the licensing reality for using any of it?
6. What should our own square-packing toolkit actually look like as a result?

## Scope

**Included:** the FrankenSim workspace at commit `1d48077`, its seven sibling
repositories at the heads recorded in `constellation.lock`, and everything in them
bearing on high-performance deterministic numerical Rust — build configuration,
determinism policy, exact and certified arithmetic, parallel execution, RNG, allocation,
benchmarking methodology, and test/lint infrastructure.

**Excluded:** the physics content (FEEC, CutFEM, LBM, BEM, aeroacoustics, the Wright
Flyer model) except where a technique transfers; the governance, evidence-packaging, and
program-management machinery except as it bears on performance claims; FrankenSQLite,
FrankenPandas, and FrankenNetworkx beyond identification, as none is on the path to a
packing toolkit.

## Findings

### Scale, and what that scale is made of

| repository | crates | `.rs` files | lines of Rust |
| --- | --- | --- | --- |
| frankensim | 166 | 1,904 | 1,891,839 |
| asupersync | (single crate) | 4,245 | 3,331,636 |
| frankensqlite | 27 | 1,043 | 1,248,565 |
| frankenscipy | 19 | 1,444 | 746,272 |
| frankenpandas | 14 | 708 | 478,024 |
| franken_numpy | 10 | 385 | 467,912 |
| frankentorch | 13 | 720 | 429,513 |
| franken_networkx | 12 | 103 | 202,916 |
| **total** |  | **10,554** | **≈8.8M** |

Counts are of tracked `.rs` files at the pinned heads, taken from the checkouts.
asupersync’s total is dominated by tests: 1,327 test files and 766 fuzz targets against
314 source files.

FrankenSim’s own prose is on the same scale — a 127 KB README, a 162 KB changelog, and
five planning documents between 65 KB and 242 KB. The tracker reports 2,160 open beads,
1,791 of them blocked, 369 actionable.

### Architecture

The workspace is flat — 166 crates under `crates/`, 162 of them direct workspace members
(the WASM surfaces sit outside), no nested workspaces — with a seven-layer discipline
enforced by a custom `xtask` check rather than by directory structure:

| layer | name | responsibility |
| --- | --- | --- |
| L0 | SUBSTRATE | hardware topology, arenas, SIMD dispatch, two-lane execution, determinism |
| L1 | BEDROCK | dense/sparse/FFT math, certified arithmetic, AD, RNG and QMC |
| L2 | MORPH | regions, charts, representation routing, meshing, geometry certificates |
| L3 | FLUX | FEEC/DEC physics, CutFEM, LBM, BEM/FMM, solvers, adjoints |
| L4 | ASCENT | shape, topology, global, Bayesian and multi-objective optimization |
| L5 | LUMEN | path tracing, chart rendering, scientific visualization |
| L6 | HELM | script IR, sessions, capabilities, ledgers, planner, reports |

Each crate declares `layer = "L<n>"` under `[package.metadata.frankensim]`, and
`xtask check-layers` enforces that lower layers never depend on higher ones.
Each crate also carries a `CONTRACT.md` declaring, among other things, exactly one
*determinism class* — which is lint-enforced and decides which code rules bind.

The recurring abstraction is `Evidence<T>` / `Certified<T>` from `fs-evidence`: a value
carrying four uncertainty slices (numerical enclosure, statistical e-values, model-form
discrepancy, sensitivity summary) that compose *conservatively* — “composition cannot
outrank its weakest operand”.
Certificates travel inside values rather than alongside them.

### Building and testing it

The documented quick start is `cargo run --manifest-path tools/bootstrap/Cargo.toml`
followed by `cargo test --workspace`. Neither step behaved as documented.

**The bootstrap materializes 6 of 7 siblings.** It shallow-clones each repository at the
exact head in `constellation.lock` and verifies content, refusing to repurpose an
existing checkout at a different head — a fail-closed behaviour that is correct and that
caught our own earlier hand-clone.
`franken_numpy` fails its integrity check with a `raw-tracked-source-mismatch` on
`legacy_numpy_code/numpy/doc/make.bat`, attributed in the error text to a case-folding
checkout collision.

**The workspace does not resolve at its own recorded pins.** `crates/fs-ad/Cargo.toml`
requires

```toml
ft-autograd = { path = "../../../frankentorch/crates/ft-autograd",
                package = "frankentorch-autograd", optional = true }
ft-core     = { path = "../../../frankentorch/crates/ft-core",
                package = "frankentorch-core",     optional = true }
```

but at the pinned FrankenTorch head (`f00c3ce7`, the one the bootstrap verifies) those
packages are named `ft-autograd` and `ft-core`. Cargo therefore fails at manifest
resolution for the *entire* workspace — including crates that have nothing to do with
automatic differentiation — with

```
error: no matching package named `frankentorch-autograd` found
```

Both dependencies are optional and off by default, so deleting the two `package = …`
renames is a sufficient fix; that is what our probe harness does.
The finding is that the recorded constellation pin and the workspace manifest disagree,
so a clean checkout following the documented steps cannot build anything.

**With that one fix, it builds and passes.** Compiling the seven crates most relevant
here took **12 seconds** on the pinned nightly (`nightly-2026-07-06`, rustc
1.99.0-nightly). Their test suites:

| crate | outcome |
| --- | --- |
| fs-math, fs-ivl, fs-rand, fs-simd, fs-alloc, fs-evidence | **652 tests passed, 0 failed** (77 s) |

The suites are substantive, not smoke tests: `fs-ivl` alone runs a containment fuzz
battery, a directed-rounding audit, an exact-predicate corpus, a Taylor-model battery,
and an error-free-transform bridge casebook.
`fs-alloc` ships 11 `compile_fail` doctests proving that arena allocations cannot escape
their scope — lifetime enforcement verified as a test rather than asserted in prose.

**Known-red tests are on the record.** `suite-known-red.json` lists exactly four
deliberately failing tests, all in `fs-ledger`, all blocked on one upstream
FrankenSQLite defect (`ON DELETE CASCADE` actions running before the parent row is
deleted), each with a named owner bead and an honest disposition.
The registry’s own note says a test may enter it “only with a named owner bead and an
honest disposition — never to make a failure invisible.”

### Measured: what fs-ivl can and cannot certify about a packing

This is the experiment that decides whether any of this is useful to us.
`fs-ivl` offers two independent routes to a geometric decision, and we ran both against
Trump’s 11-unit-square packing, from the f64 roundings of the exact coordinates our own
verifier produces.

| method | pairs settled | pairs not settled |
| --- | --- | --- |
| Outward-rounded `Interval` arithmetic | **41 / 55** proven strictly separated | 14 |
| Exact `orient2d` (Shewchuk adaptive) | **47 / 55** have a separating edge line | 8 |

Two results, both sharper than expected.

**The interval result is an exact match with our own exact verifier.** Our number-field
verifier finds 41 strictly separated pairs and 14 pairs touching with exactly zero gap.
`fs-ivl`’s interval arithmetic proves 41 and cannot settle 14 — and the *sets are
identical*, pair for pair:

```
(0,6) (1,9) (2,8) (2,10) (3,4) (3,5) (4,5) (4,8) (5,6) (6,7) (6,8) (7,9) (8,9) (9,10)
```

Two unrelated implementations — Python exact arithmetic in `Q(u)` of degree 8, and Rust
outward-rounded floating-point intervals — agree exactly on which separations are
strict. This is independent confirmation of both, and a clean empirical demonstration of
the claim in the previous research doc: **interval arithmetic buys precisely the strict
separations and nothing more.** The 14 contacts are exactly the pairs no amount of
interval precision can settle, because their true separation is zero.

**The exact-predicate result is a genuine surprise, and a useful one.** `orient2d` is
exact for f64 inputs, so its verdict is a proof about the *rounded* configuration.
It finds 8 pairs with no separating axis at all:

```
(1,9) (2,8) (2,10) (5,6) (6,8) (7,9) (8,9) (9,10)
```

For convex polygons, no separating edge-normal axis means the interiors intersect.
**At 16 significant digits, the published packing is not a valid packing** — eight pairs
genuinely overlap. Cross-checked in floating point, the overlaps are at the last-bit
scale: the deepest is `−4.4 × 10⁻¹⁶`, the smallest strictly positive gap is
`1.1 × 10⁻¹⁶`.

A naive float SAT gap computation disagrees with the exact predicate *in both
directions*: it reports 7 negative gaps, of which 2 are pairs `orient2d` proves are
fine, and it reports exactly `0.0` for 3 pairs that `orient2d` proves overlap.
That is the tolerance blind spot from the previous document, caught in the wild, on real
published data.

The practical lesson for our toolkit: an exact predicate over f64 answers a *different
and weaker* question than we need.
It certifies the rounded configuration exactly — which is useful for catching the kind
of error above — but the rounded configuration is not the packing.
Certifying the packing still requires the algebraic coordinates.

### Measured: is a counter-based stream really schedule-independent?

The second experiment tests the property a parallel packing search depends on.
`fs-rand` draws are a pure function of `(seed, kernel, tile, index)` — never of which
thread ran when — with random access by index.
Drawing 64 tiles × 32 values in sequential, reversed, and worker-interleaved order:

```
sequential  0xc244d3a5be766ac2
reversed    0xc244d3a5be766ac2
interleaved 0xc244d3a5be766ac2
```

Bit-identical. `Stream::at(index)` matches the sequential prefix, and seeking to index
`2⁶³` costs the same as seeking to index 0 (1.29 ms versus 1.32 ms per 100,000 seeks,
about 13 ns per 128-bit draw).

That is the whole trick behind reproducible parallel stochastic search, and it is about
forty lines of Philox.
It is the single most portable idea in the repository.

### Rust performance engineering, as practised

#### Build configuration

```toml
[profile.release]
lto = "thin"
codegen-units = 1
debug = "line-tables-only"

[profile.bench]
inherits = "release"
```

with a comment requiring that changes to this profile “justify the performance,
determinism, and cancellation tradeoffs”.
Notably *not* fat LTO — the stated framing is “deterministic-friendly,
performance-honest defaults”.
`-Z threads=4` enables the parallel compiler frontend.
The nightly toolchain is pinned to a date, with a comment recording *why*: a floating
`nightly` resolved differently on CI than on local workers, so clippy lint sets drifted
and produced CI-only failures no local lane could reproduce.

#### The deliberate absence of a global `target-feature`

`.cargo/config.toml` contains an unusually instructive comment.
It is tempting to set a workspace-wide `-C target-feature=+fma` to fix what they call
the **libm-FMA trap**: on baseline x86-64, `f64::mul_add` lowers to a per-element libm
`fma()` *call*, measured at about 1 GFLOP/s, which caps any `mul_add`-heavy kernel.
They refuse the global flag, because it would make every binary require FMA and bypass
the runtime ISA admission/dispatch contract.
The fix is per-kernel instead: put the hot loop behind a
`#[target_feature(enable = "fma")]` function with a runtime `is_x86_feature_detected`
gate, a scalar fallback, and a registered unsafe capsule whose arithmetic semantics are
pinned against its scalar twin.

The same file carries a correction of an earlier measurement that had been misread as
evidence about contraction semantics, with instructions not to infer from it.
That is the house style: the reasoning and the retraction both stay in the file.

#### Floating-point policy

`fs-math` is the policy layer, normative for every crate:

- **Strict mode.** `det::` functions are pure-IEEE implementations, bit-identical on
  every conforming target by construction.
  Deterministic-mode kernels must not call platform libm — `sqrt` is the exception,
  since IEEE-754 requires correct rounding for it.
- **FMA contraction.** Implicit contraction is forbidden; explicit `mul_add` is
  encouraged, because it is exactly rounded and therefore deterministic everywhere.
- **Subnormals** are never flushed; any flag implying FTZ/DAZ is a policy violation.
- **NaN** payloads are never relied on; `canonical_nan()` is the interchange value and
  `total_cmp` does deterministic tie-breaking.
- **ULP budgets** are declared per function, and tests assert the *measured* maximum
  against the declared budget.
- A `STRICT_CORE_GOLDEN_HASH` fingerprints the whole operation tree, recorded on both an
  M4 Pro and a Threadripper PRO 5995WX over a canonical 25,000-point frame.

#### Determinism classes

Every crate declares exactly one class, and the class decides which rules bind:

| class | guarantee |
| --- | --- |
| `Deterministic` | bit-identical across runs, worker counts, build modes, **and ISAs** |
| `DeterministicPerIsa` | bit-identical across runs, workers and build modes on one ISA; last-ULP cross-ISA drift admitted and scoped |
| `Fast` | statistical or tolerance envelopes only; the mode is stamped into every event so a `Fast` result cannot be laundered into a bit-stable claim |

`Deterministic` crates route every transcendental through `fs_math::det` and are
registered in `LIBM_DOCTRINE_CRATES`. Promotion between classes shifts last-ULP outputs,
so every golden in the crate re-freezes in the same change.

#### Determinism lints that actually run

Two `xtask` checks encode the doctrine as enforcement rather than documentation:

- **`check-libm`** flags any raw `.sin(`, `.cos(`, `.exp(` … in a crate that claims
  cross-ISA determinism, with the message that “platform libm is not correctly rounded
  and differs across ISAs”.
  Dev-only oracle comparisons escape with a `// det-ok: <reason>` comment on the same or
  preceding line.
- **`check-powi`** flags `.powi(n)` for any `|n| > 3`. The reason is recorded in
  `docs/GOLDEN_POLICY.md` and is the best cautionary tale in the repository: a golden
  hash was re-pinned with a plausible but wrong justification, when the actual mover was
  optimization-level-dependent `f64::powi`. The re-pin froze release-mode bits while
  debug still produced the old value, so the sentinel’s verdict depended on the build
  profile.

#### Golden hashes coupled to semantic surfaces

`golden-couplings.json` declares, for every golden hash, the file and constant that
carry it, the upstream *semantic surfaces* it depends on, and the surface version it was
frozen against. Surfaces declare a `pub const <NAME>_VERSION: u32` and bump it on any
change that can move downstream bits.
`xtask check-goldens` fails when a surface drifts from the registry, naming every
dependent golden that must be deliberately re-frozen.
An upstream semantic change therefore *points at* its downstream goldens instead of
surprising them.

#### Execution

`fs-exec` is the piece whose shape a packing search would want to copy:

- A **work-stealing tile pool** where per-worker deques are seeded with
  weight-proportional contiguous tile runs, steal order is CCD-local-first from measured
  topology, and reductions are folded into **fixed slots in tile order** — so results
  are bit-identical across worker counts and steal schedules by construction.
- A `Cx` context carrying the cancellation gate polled at tile boundaries, a tile-scoped
  arena, the `StreamKey` RNG identity, a budget slice, and the execution mode.
- **Speculative races** with loser cancellation and deterministic victory — the natural
  shape for running many annealing restarts and killing the losers.
- **Resumable and forkable solvers** with bit-exact pause–serialize–resume.
- **Panic containment**: a panicking tile is caught, siblings drain through the gate,
  and the run returns a structured error with full tile provenance rather than aborting
  the process mid-campaign.

#### Memory

`fs-alloc` allocates every arena block at **128-byte alignment unconditionally** (a
superset of Apple’s 128-byte and x86-64’s 64-byte cache lines), pads shared slots with
`CachePadded` against false sharing, makes 2 MiB-and-up chunks THP-eligible on Linux
while *recording the decision and every fallback* rather than claiming it silently, and
treats out-of-memory as a `Result` rather than an abort.
Arenas are scoped 1:1 to units of work, so cancellation reclaims everything at a cost
independent of allocation count.

#### SIMD

`fs-simd` resolves dispatch **once** into a function table keyed by measured capability
— no per-call branching in hot loops — with a scalar Tier 0 that is always available and
serves as the correctness reference.
Architecture intrinsics live in registered unsafe capsules with adjacent `SAFETY.md`
files, audited by `xtask check-unsafe` against a workspace registry; the workspace
default is `unsafe_code = "deny"`. Under Miri the table routes to scalar.
The determinism contract is explicit: per tier, every primitive has a fixed evaluation
and reduction shape; across tiers, elementwise fused operations match bitwise, while
reductions may differ within a documented envelope — “that difference is machine
identity, never run jitter”.

#### How performance claims are made

There is no criterion dependency, no `[[bench]]` target, and no `benches/` directory
anywhere in FrankenSim (verified: zero matches across every manifest).
Performance is instead an evidence problem handled by `fs-roofline`:

- **Machine axes are measured, never taken from spec sheets** — bandwidth from a
  STREAM-triad probe, peak FLOPs from an in-house FMA chain with independent accumulator
  lanes so the autovectorizer can fill the SIMD units.
  The compute axis is therefore “compiler-achievable peak”, which is conservative in the
  honest direction for a limit that divides other kernels’ attainment.
- **Every timing reports order statistics** — median, p25, p75, min, max, and relative
  interquartile dispersion — after discarded warmup runs.
  The module’s own summary: “A benchmark without variance bars is folklore.”
- **Baselines are promoted, not written.** A candidate needs at least three mutually
  agreeing quiet probes, a named operator, a justification, a promotion day, and an age
  policy. A loaded host **refuses** promotion.
  Writes serialize under an OS file lock and land by atomic rename, so a crash leaves
  the prior store intact.
- **Promotion is not attestation.** The committed baseline files are explicitly
  “operator-trusted and tamper-evident, but contain neither an attestation nor an atomic
  authority-policy decision”, and a run grounded only in them is report-only, never
  citable. Axis re-probes drift-check at 25%; values below floor constants (5 GB/s, 5
  GFLOP/s single-thread) are treated as evidence the probe ran in a crushed environment
  rather than as data.

The standing rule in `AGENTS.md`: “Do not write ‘fast’ unless there is a benchmark,
target, machine fingerprint, and acceptance band,” and “treat performance regressions as
test failures once baselines exist.”

By contrast **asupersync does use criterion** — 44 benchmark files behind an opt-in
`criterion-benches` feature so that ordinary builds never compile benchmark plumbing —
plus 766 `cargo-fuzz` targets with scripted seed corpora, `proptest`, and `trybuild`
compile-fail contracts.
The Franken-only dependency rule binds the *production* graph; dev and test graphs use
the normal ecosystem freely.

### The crates worth knowing about

| crate | what it is | relevance to packing |
| --- | --- | --- |
| **`fs-ivl`** | outward-rounded intervals, affine forms, Taylor models, Shewchuk `orient2d`/`orient3d`/`incircle`/`insphere` with Simulation of Simplicity, Krawczyk/interval-Newton root certification with a completeness receipt | **highest.** The exact-predicate ladder and the certified-root machinery are the two things a rigorous packing prover needs |
| **`fs-rand`** | Philox streams keyed by `(seed, kernel, tile, index)`, O(1) random access, Sobol/Owen QMC, alias tables | **highest.** Makes parallel search reproducible |
| **`fs-exec`** | tile pool with fixed-slot deterministic reductions, `Cx` cancellation, speculative races, resumable solvers | **high.** The execution shape a restart-heavy search wants |
| **`fs-math`** | deterministic elementary functions, ULP budgets, error-free transforms, double-double | **high.** `eft`/`dd` are the doubling primitives an exact kernel needs |
| **`fs-dfo`** | CMA-ES in information-geometric form, BIPOP restarts, Nelder–Mead, NSGA-II/III, MOEA/D, hypervolume — “the whole evolution is a pure function of the seed” | **high.** A credible complement to simulated annealing for the continuous `(x, y, θ)` problem |
| `fs-alloc` | 128-byte-aligned scope arenas, hugepage policy, sharded pools | medium. Standard technique, unusually well documented |
| `fs-simd` | tiered dispatch resolved once, scalar reference, capsule discipline | medium |
| `fs-query` | certified convex separation by Frank-Wolfe on the Minkowski difference, with a `[lo, hi]` bracket where both bounds stay valid under early stop and a `separation_proven` flag | medium. 3-D and support-function based; SAT is simpler and exact for our 2-D squares, but the *contract shape* is worth copying |
| `fs-evidence` | `Evidence<T>`/`Certified<T>` with conservative composition | medium. The right way to type a “verified/unverified” result |
| `fs-detaudit` | worker-matrix bit-identity audits with first-divergence localization, cross-ISA divergence classification | medium-high for a parallel search |
| `fs-propcheck` | in-house property testing with integrated shrinking; failures print a case seed that replays exactly | medium |
| `fs-ascent`, `fs-bo`, `fs-opt` | L-BFGS with strong Wolfe, trust-region Newton-Krylov; Gaussian-process Bayesian optimization; a typed optimization problem IR over manifold variables | medium |

Nothing in FrankenSim addresses packing, nesting, or 2-D collision between rotated
rectangles. `fs-contact` does broad-phase over certified motor tubes and convex/SDF
narrow-phase, but for 3-D multibody dynamics.

### Sibling repositories

| repository | what it is | relevance |
| --- | --- | --- |
| **asupersync** | “spec-first, cancel-correct, capability-secure async for Rust”: tasks owned by regions that close to quiescence, cancellation as a bounded protocol, a deterministic replayable lab runtime | high for the execution layer; also the fuzz/bench methodology |
| **frankenscipy** | clean-room Rust SciPy, `#![forbid(unsafe_code)]`, 19 crates, a Condition-Aware Solver Portfolio that inspects conditioning and emits an audit trail for its algorithm choice. `fsci-opt` has BFGS, L-BFGS-B, Nelder–Mead, Powell, Newton-CG, trust-exact, Wolfe line searches, least squares | high — local refinement of a packing is exactly `minimize` with bounds |
| frankentorch | Rust PyTorch: autograd tape, kernels, optimizers | low-medium; forward duals in `fs-ad` cover our needs |
| franken_numpy | Rust NumPy: dtypes, ufuncs | low |
| frankensqlite | Rust SQLite: pager, B-tree, WAL, MVCC, planner, VDBE | low for packing; the ledger substrate |
| frankenpandas, franken_networkx | Rust pandas and NetworkX | low |

### Licensing reality

Every repository in the constellation ships **“MIT License (with OpenAI/Anthropic
Rider)”**. The rider grants no rights to OpenAI, Anthropic, their affiliates, or “any
person or entity acting directly or indirectly on behalf of, for the benefit of, or
under the direction of” them, and defines “use” to include benchmarking, testing,
analyzing, indexing, and incorporation into any dataset, training corpus, evaluation
harness, or ML pipeline.
Breach terminates the licence automatically.

Anyone evaluating these crates as dependencies should read it first; it is not a
standard MIT grant and a downstream distributor inherits the obligation to carry it
unmodified. For the present work, the requester’s position is that this is their own
research, not for Anthropic’s benefit, and that the author encourages it.

Independent of the rider, the practical coupling argues against depending on the code
directly: `fs-ivl` pulls in `fs-evidence` and `fs-math`, the workspace requires a pinned
nightly and seven sibling checkouts at exact heads, and — as measured above — that
constellation does not currently resolve.
The transferable asset is the design.

### Honest calibration

FrankenSim’s own artifacts are the best source on its maturity, and they are unusually
candid.

- `capability-maturity.json`: “Nothing here is L4 or L5, because the external V&V corpus
  and any written support policy do not exist yet — that is the honest state, not an
  oversight.”
- `vv-scorecard.md`: 34 registered datasets, **0 ledgered run records**, **0 of 8
  adversarial challenges executed**, `false_acceptance_total: NO-DATA`,
  `interval_coverage: NO-DATA`, and zero external datasets on the blind-predictive-
  validation, field-monitoring, transferability, and independent-reproduction axes.
- `spine-e2e-summary.json`: the end-to-end lane executes 4 of 6 stages and its own
  no-claim says it “proves the executing producer prefix and its refusal boundary only …
  this is NOT an end-to-end simulation result.”

The repository also defines a **claim-integrity defect class**: a defect exists whenever
any public surface — API return type, certificate, report line, README sentence, CLI
export, ledger row — “can assert a *stronger* epistemic state than its actual evidence
establishes”. These are tracked as their own countable, gateable class with mandatory
severity labels, on the principle that “a false certificate is worse than an ordinary
wrong answer”. Under-claiming is explicitly never a defect.

That concept is the single best import for our square-packing work, because it names
exactly the failure mode the previous research document identified: a float verifier
that returns “valid” is a claim-integrity defect.

The counterweight is proportion.
Around fifty `xtask` policy checks, a 547 KB source manifest with a 1.4 MB SPDX
projection, governance JSON for moonshot portfolios and go-to-market wedge selection,
and 1,791 blocked beads are a lot of apparatus around four executing pipeline stages.
A reader should take the *techniques* — which are real, tested, and measured — without
assuming the surrounding ceremony carries its own weight.

## Key Insights

1. **Two independent verifiers agreeing pair-for-pair is the strongest evidence in
   either research document.** Our exact `Q(u)` verifier and FrankenSim’s interval
   arithmetic were written for different purposes in different languages by different
   authors, and they partition the same 55 pairs into the same 41 and the same 14. That
   is what independent confirmation looks like, and it settles that the 14 contacts are
   a property of the packing rather than an artifact of either implementation.

2. **The published 16-digit coordinates are not a valid packing.** Eight pairs overlap
   by about `10⁻¹⁶`. Nobody was wrong: the record *is* the algebraic number, and the
   decimals are a rendering of it.
   But it means any pipeline that consumes the published decimals and checks them
   numerically is checking something that is false, and the only reason it passes is a
   tolerance. This is the practical case for algebraic ground truth.

3. **Reproducible parallel search is a solved problem, and the solution is small.**
   Counter-based RNG keyed by logical work identity plus fixed-slot reductions in tile
   order gives bit-identical results across worker counts and steal schedules.
   Measured here: three different traversal orders, one hash.
   That property is what would let a packing search publish basin statistics that mean
   something.

4. **The most valuable performance practice is not an optimization.** It is the rule
   that a performance claim needs a measured machine axis, a dispersion bar, a
   fingerprint, and an acceptance band.
   Optimizations are cheap to find and easy to fool yourself about; the measurement
   discipline is what makes them stick.

5. **`powi` and platform `libm` are the two concrete determinism traps to lint for.**
   Both are documented here with the incidents that motivated them.
   `f64::powi` expands differently under different optimization levels, so a value can
   differ between debug and release in the same build; platform libm differs across ISAs
   and libm versions. Neither is obvious until it costs a day.

6. **Exact predicates over f64 answer a weaker question than exact predicates over
   algebraic numbers, and the difference matters exactly here.** `orient2d` is exact for
   its f64 inputs, which is the right tool for meshing, where the inputs *are* the
   coordinates. For packing, the f64 coordinates are a rounding of the real ones, so the
   exact answer is about the wrong configuration.
   The staged filter architecture still transfers; the number type must not.

7. **Scale is not the same as maturity, and this repository says so itself.** 8.8M lines
   of Rust, zero ledgered run records, four executing pipeline stages of six.
   The reason it is still worth studying is that the individual layers are tested,
   measured, and honest about their boundaries — and those layers are what we would
   reuse.

## Recommendations

### The architecture to build

Nothing here changes the conclusion of the previous document — grid-bucket, then run SAT
with predicates evaluated in the packing’s number field — but it fills in every layer
around it. A concrete Rust toolkit, in priority order:

1. **`packing-exact`: the verifier.** Real algebraic number arithmetic over `Q(α)` with
   exact zero test and exact sign, plus a filtered kernel: fast float evaluation with an
   error bound, escalating to exact only when the sign is in doubt.
   Model the staging directly on `fs-ivl::predicates`
   (`Stage::{Filtered, Adaptive, Exact}` with per-stage filter-rate tests).
   Use FLINT/`fmpq_poly` or CGAL’s algebraic kernel underneath rather than
   reimplementing — the previous document’s measurements say the pure-Python version is
   two to three orders of magnitude off, and this is the one place where the algebraic
   degree (up to 62 in the record table) makes the constant factor matter.

2. **`packing-search`: the engine.** Copy three things exactly:
   - **counter-based RNG keyed by `(seed, kernel, tile, index)`** with O(1) random
     access. This is the whole basis of reproducible restarts and of publishable basin
     statistics.
   - **fixed-slot reductions folded in tile order**, so worker count never changes the
     answer.
   - **speculative races with loser cancellation**, which is precisely the shape of “run
     65,536 annealing chains and keep the best”.

   Use `rayon` or a small custom pool; the discipline is what matters, not the pool.

3. **Adopt the determinism-class taxonomy verbatim.** Declare each component
   `Deterministic`, `DeterministicPerIsa`, or `Fast`, and stamp the mode into every
   recorded result so a `Fast` run cannot be quoted as a bit-stable one.
   For a project whose output is records other people will cite, this is worth more than
   it costs.

4. **Adopt the two determinism lints on day one.** Ban raw `.powi(n)` for `|n| > 3` and
   ban platform `libm` in any component claiming cross-ISA reproducibility, with a
   `// det-ok:` escape for dev-only oracles.
   Roughly a hundred lines of `xtask`.

5. **Adopt the roofline measurement discipline, not a roofline crate.** Measure the
   machine before interpreting the kernel; report median and interquartile dispersion;
   refuse to promote a baseline measured on a loaded host; record the fingerprint.
   This is the part that would let us make a defensible claim about search throughput.

6. **Adopt the claim-integrity defect class as a review category.** Any surface that can
   report “valid packing” on evidence that does not establish it is a bug of its own
   kind.

### What not to do

- **Do not depend on the Franken crates.** The rider aside, a dependency drags in a
  pinned nightly, seven sibling checkouts at exact heads, and a constellation that does
  not currently resolve.
  Reimplement the three or four ideas that matter; they are small.
- **Do not reimplement Shewchuk from scratch** unless the input type genuinely is f64.
  For algebraic coordinates the predicate ladder is the right *shape* but the wrong
  arithmetic.
- **Do not adopt the evidence/governance apparatus.** `Evidence<T>` is a good idea at
  the scale of a hundred-crate multiphysics system with model-form uncertainty.
  A packing verifier has one kind of uncertainty and a two-valued answer; a
  `Result<Certified, NotProven>` carries the whole story.

### Worth a follow-up conversation with the author

Three questions where he has already done the work and we would otherwise redo it:
whether `fs-ivl`’s Krawczyk machinery has been pushed to multivariate boxes (we need
`(x, y, θ)` triples, and the crate is currently 1-D); whether the tile pool’s fixed-slot
reduction has a published worker-count-invariance measurement we could cite; and whether
the `powi`/libm lint pair caught anything beyond the two incidents recorded in
`GOLDEN_POLICY.md`.

## Open Questions

- [ ] Does the `frankentorch-autograd` / `ft-autograd` naming mismatch reflect a stale
  `constellation.lock`, or a rename in FrankenSim that never propagated?
  Worth reporting upstream either way — it blocks every clean checkout.
- [ ] `franken_numpy` fails its own bootstrap integrity check on a case-folding
  collision. Is that specific to case-sensitive Linux checkouts, or does it reproduce on
  macOS where the README says the pin is “case-collision-safe”?
- [ ] `fs-ivl`’s `newton_roots_bounded` returns a completeness receipt over an
  `Interval` domain — one dimension.
  Is there a multivariate box version anywhere in the workspace, or is that genuinely
  unbuilt?
- [ ] What actually happens to throughput under the tile pool’s fixed-slot reduction
  versus an unordered one?
  The determinism argument is airtight; the cost is not stated anywhere we found.
- [ ] `fs-dfo`’s CMA-ES is described as a pure function of the seed and golden-hashed.
  How does its wall-clock compare to a purpose-built annealer on a packing-shaped
  objective? This is the most promising untested substitution for our search.
- [ ] Does any Franken repository have a 2-D geometry kernel we missed?
  Our search found none, but the workspace is large enough that a negative result from
  grep is weak.

## Methodology

Work was done on 2026-08-22 against a fresh checkout of `dicklesworthstone/frankensim`
at commit `1d48077` in `attic/`, with its siblings materialized by the repository’s own
bootstrap tool at the heads in `constellation.lock`.

**Read directly.** The workspace `Cargo.toml`, `.cargo/config.toml`,
`rust-toolchain.toml`; `AGENTS.md` (toolchain, dependency policy, unsafe policy, core
invariants, the Gauntlet, the performance program); `docs/DETERMINISM_CLASSES.md`,
`docs/GOLDEN_POLICY.md`, the libm-doctrine and claim-integrity sections of
`docs/CONVENTIONS.md`; the `xtask` implementations of `check-powi` and `check-libm`;
`perf-baselines/README.md`; the crate documentation and public APIs of `fs-ivl`,
`fs-math`, `fs-rand`, `fs-simd`, `fs-alloc`, `fs-exec`, `fs-evidence`, `fs-query`,
`fs-dfo`, `fs-roofline`, `fs-detaudit`, `fs-propcheck`; `suite-known-red.json`,
`spine-metrics.json`, `spine-e2e-summary.json`, `capability-maturity.json`,
`vv-scorecard.md`; and the READMEs and manifests of asupersync and frankenscipy.

**Run.** The bootstrap tool (twice — the first run correctly refused a hand-made clone
at the wrong head). `cargo build` and `cargo test` for `fs-math`, `fs-ivl`, `fs-rand`,
`fs-simd`, `fs-alloc`, `fs-evidence`, and `fs-substrate`: 12 s to build, 652 tests
passing in 77 s. Both experiments below.

**Two experiments, written for this study.** Sources and a self-cleaning runner are in
[`explorations/packing/frankensim-probe/`](../../../frankensim-probe/README.md); nothing
from FrankenSim is vendored there.

- `packing_sat.rs` runs the separating-axis test on Trump’s 11-square packing through
  `fs_ivl::Interval` and through `fs_ivl::orient2d`. The f64 coordinates were emitted
  from our own exact verifier in `explorations/packing/`, so the two implementations
  share inputs but no code.
- `schedule_invariance.rs` draws 64 tiles × 32 values from `fs_rand` in sequential,
  reversed and worker-interleaved order and folds each into a hash.

**Cross-checks.** The 14 pairs `fs-ivl` cannot settle were compared as a set against the
14 zero-gap pairs from our exact verifier: identical.
The 8 pairs `orient2d` finds unseparated were re-checked with an independent
floating-point SAT gap computation, which disagreed in both directions — 7 negative
gaps, 2 of them on pairs `orient2d` proves are fine, and exact `0.0` on 3 pairs
`orient2d` proves overlap.
That disagreement is itself reported above rather than reconciled, because `orient2d` is
the exact authority for f64 inputs and the float gap is not.

**One modification to the checkout, made and reverted.** The two `package = …` renames
in `crates/fs-ad/Cargo.toml` were removed to let Cargo resolve the workspace, and
restored afterwards; the checkout is clean apart from build-generated `Cargo.lock`
changes. The probe runner applies and reverts the same patch itself, so the experiments
reproduce without leaving a modified checkout.

**Not established.** We did not build or test the full 166-crate workspace, only the
seven crates on the path to this question — so “652 tests pass” is a statement about
those crates, not about FrankenSim.
We did not run `xtask check-all`, the roofline harness, or any end-to-end lane.
Timings are from one container (Linux, x86-64) with no quiet-host discipline, and by the
repository’s own standards are report-only.
Line counts are of tracked `.rs` files and include tests and fuzz targets.
The bead and maturity figures are the repository’s own committed snapshots, which its
notes say trail the live tracker.

**Link audit.** All eight cited GitHub URLs return 403 to an automated checker, which is
ordinary bot-blocking; all eight were cloned successfully from those exact URLs during
this research, which is stronger verification than a status code.

**Confidence.** High for everything measured here (builds, test counts, both
experiments, the cross-checks) and for the policy documents, which were read in full.
High for the pin mismatch, which reproduces from a clean bootstrap and is confirmed by
Cargo’s own error. Medium for the architecture summary, which rests on crate
documentation and public APIs rather than on reading 1.9M lines.
Medium for the maturity characterization, which rests on the repository’s committed
self-assessment.

## References

FrankenSim and siblings (all MIT with the OpenAI/Anthropic rider):

- [FrankenSim](https://github.com/Dicklesworthstone/frankensim) — the subject; studied
  at commit `1d48077`.
- [asupersync](https://github.com/Dicklesworthstone/asupersync) — cancel-correct
  structured-concurrency runtime; the criterion/cargo-fuzz methodology.
- [FrankenSciPy](https://github.com/Dicklesworthstone/frankenscipy) — `fsci-opt` local
  optimizers, `#![forbid(unsafe_code)]`.
- [FrankenTorch](https://github.com/Dicklesworthstone/frankentorch),
  [FrankenSQLite](https://github.com/Dicklesworthstone/frankensqlite),
  [FrankenNumpy](https://github.com/Dicklesworthstone/franken_numpy),
  [FrankenPandas](https://github.com/Dicklesworthstone/frankenpandas),
  [FrankenNetworkx](https://github.com/Dicklesworthstone/franken_networkx).

Techniques FrankenSim implements, at their sources:

- J. R. Shewchuk, “Adaptive Precision Floating-Point Arithmetic and Fast Robust
  Geometric Predicates”, *Discrete Comput.
  Geom.* 18 (1997) 305–363 — the `orient2d` ladder.
- H. Edelsbrunner and E. P. Mücke, “Simulation of Simplicity”, *ACM Trans.
  Graph.* 9 (1990) 66–104 — the symbolic-perturbation tie-breaking.
- J. K. Salmon, M. A. Moraes, R. O. Dror, D. E. Shaw, “Parallel Random Numbers: As Easy
  as 1, 2, 3”, *SC’11* — Philox.
- R. Krawczyk, “Newton-Algorithmen zur Bestimmung von Nullstellen mit Fehlerschranken”,
  *Computing* 4 (1969) 187–201 — the root-certification step.
- S. Williams, A. Waterman, D. Patterson, “Roofline: An Insightful Visual Performance
  Model”, *CACM* 52 (2009) — the harness’s model.

Companion documents in this repository:

- `research-2026-08-22-packing-11-unit-squares.md` — the mathematics of `s(11)`.
- `research-2026-08-22-square-packing-algorithms-and-tooling.md` — search and
  verification tooling; the exact verifier whose output is cross-checked here.
- [`explorations/packing/`](../../../README.md) — the exact verifier and the FrankenSim
  probes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
