# Feature: Minimal Packing Toolkit

**Date:** 2026-08-22 (last updated 2026-08-23)

**Author:** Claude (agent), for samanthadrakova@gmail.com

**Status:** Draft (revised 2026-08-23 — see [Revision history](#revision-history))

## Overview

A minimum kit of composable pieces for running the first real experiments on `s(n)`:
**propose candidate packings, quench them to named basins, verify them exactly, and
accumulate a map** — with `n = 11` and `n = 12` as the working cases, and with the proof
lane reachable from the same parts rather than needing a second system.

The deliverable is the **map**, not a record.
That framing comes from the
[search-philosophy report](../../research/research-2026-08-23-search-philosophy-and-landscape-cartography.md):
records are rigid, rigid optima live in rare basins, and so scaling a volume-weighted
sampler multiplies effort against a probability the problem drives toward zero.
A validated basin atlas of the `n ≤ 11` landscape is publishable, steers search, gives
negative results meaning, and is the empirical shadow of the case analysis a future
proof must walk — whatever happens at the record line.

The design rule throughout is Kay’s: *simple should be simple, complex should be
possible.* Concretely, `verify(packing)` is one call that returns in milliseconds, and
the identical predicate code — with a different scalar type — answers “is every unit
square in `[0,k]²` hit by this point set?”
for a proof attempt.
If a capability needs a second implementation of the separating-axis test, this spec has
failed.

## Goals

- **Verification that is exact and fast enough to be inside a search loop’s outer
  cadence**, not just an offline check.
- **Search that produces reproducible basins**, so the output is a measurement rather
  than an anecdote.
- **One spine, many proposers.** Adding a search strategy should be small, and two
  strategies should be comparable without argument.
  If a new strategy needs its own notion of what a basin is, this spec has failed as
  surely as if it needed a second separating-axis test.
- **Certificates, not booleans** — every “valid” comes with the object that makes it
  checkable by someone who does not trust our code.
- **One predicate, many scalars.** `f64` for speed, intervals for rigour, exact `ℚ(α)`
  for contacts, and pose-boxes for the proof lane.
- **Each piece usable alone.** The verifier without the search; the search without the
  bindings; the corpus without either.

## Non-Goals

- **A GPU engine.** CPU first, measured, per the infrastructure study.
- **Beating any record.** The experiments below are calibration and measurement; a new
  record would be a bonus, not the objective.
- **Lean formalization.** Tracked separately; this spec only ensures the certificate it
  will need exists.
- **Extending the frontier corpus past `n = 100`**, or SVG geometry parsing beyond what
  `n = 11` and `n = 12` require.
- **A proof of anything.** The proof lane gets a *hook*, not an attempt.

## Background

Four research documents lead here, and their conclusions constrain this design:

- [Packing 11 unit squares](../../research/research-2026-08-22-packing-11-unit-squares.md)
  — `s(11)` is open in `[3.788854, 3.877084]`; `n = 12` is the only open case in its
  range and is the better proof target because its conjectured optimum is the integer
  `4`.
- [Algorithms and tooling](../../research/research-2026-08-22-square-packing-algorithms-and-tooling.md)
  — optimal packings *touch*, so no floating-point tolerance is sound: none both accepts
  exact contacts and rejects small overlaps.
  Exact algebraic arithmetic is required, and no purpose-built tool exists.
- [FrankenSim study](../../research/research-2026-08-22-frankensim-rust-toolkit-for-square-packing.md)
  — determinism engineering is the transferable asset: counter-based RNG keyed by
  logical work identity, fixed-slot reductions, and the staged predicate ladder.
- [Infrastructure synthesis](../../research/research-2026-08-22-infrastructure-for-packing-exploration.md)
  — measured: Rust beats Python **48×** on the SAT predicate (57 ns vs 2,726 ns);
  python-flint beats pure-Python field arithmetic **177×** at degree 8 and **578×** at
  degree 62. Three latency tiers, and the language boundary sits between the interactive
  and inner-loop tiers.
- [Lean study](../../research/research-2026-08-22-lean-for-packing-proofs-and-validation.md)
  — the immediate free action is to make the verifier emit a certificate rather than a
  boolean.

What exists today: `sqpack` in Python — exact `ℚ(α)` arithmetic, a separating-axis
verifier generic over the scalar type, Trump’s packing as a worked example, negative
controls, and `test.sh` green.
It verifies `n = 11` in 0.35 s and is **the correctness oracle this spec builds
against**, not something to replace.

## Design

### Approach

Two ideas, one under the other.

**The fast path and the exact path are the same code** — a small Rust core with thin
Python bindings, generic over a scalar type.

**Every search strategy is a proposer over one shared spine.** This is the organising
principle the
[search-philosophy report](../../research/research-2026-08-23-search-philosophy-and-landscape-cartography.md)
implies and it is what this revision adds, because reading the
[hypothesis register](../../reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md#the-hypothesis-register)
as a build list makes it obvious: almost every entry is *a different way of generating
candidate configurations*, followed by *the same pipeline*.

```
proposer ──▶ quench ──▶ canonicalize ──▶ verify ──▶ atlas
   ▲          (LP)        (R-1 keys)     (exact)      │
   └──────────── steering: descriptors, coverage ◀────┘
```

Angle-class search (H-1), neighbour-transfer seeding (H-4), δ-continuation (H-13),
MAP-Elites (H-15), superdisk continuation (H-14), billiard/inflation, an LLM constructor
DSL, and the annealer already built are **all proposers**. They differ only in how they
pick the next configuration to try.
Everything downstream — turning a float configuration into a named basin with an exact
side length, deduplicating it, verifying it, and recording it — is identical for all of
them.

The consequence for build order is the whole point of this revision: **build the spine
once and every strategy in the register becomes small.** Build it per-strategy and each
one is a project, the results are not comparable, and the atlas never exists.
The spine is Phase 2; the proposers are Phase 3 and 4 and are deliberately thin.

The predicate makes this possible: the separating-axis test is four candidate axes and
eight dot products per axis, with **no divisions and no square roots**, so every tested
quantity is a polynomial in the configuration variables.
That is why one implementation is correct over `f64`, over intervals, and over an exact
algebraic field. The existing Python already exploits this (`sign=exact_sign` versus
`sign=float_sign(1e-9)`); Rust monomorphizes it instead of paying dynamic dispatch.

### Components

**`sqpack-core` (Rust).** Geometry and predicates, generic over a `Scalar` trait
providing `+ − ×` and a sign decision.
Corner generation, the separating-axis test, container containment, uniform-grid
bucketing so pair enumeration is `Θ(n)`. No allocation on the hot path, no I/O.

**Scalar implementations.** Four, in priority order:

| Scalar | Decides | Used for |
| --- | --- | --- |
| `f64` + tolerance | approximately | search inner loop |
| `Filtered` (`f64` + error bound, escalating) | strictly when the margin is wide | first stage of the ladder |
| `Algebraic` over `ℚ(α)`, FLINT-backed | everything, including exact zero | contacts, final answers |
| `PoseBox` (interval over a box of `(x, y, θ)`) | a *family* of placements at once | **the proof-lane hook** |

The fourth is the forward-looking one and costs almost nothing now.
If the predicate is generic over `Scalar`, then instantiating it at intervals-over-poses
turns “do these two squares overlap?”
into “can *any* square with pose in this box avoid all these points?”
— which is the unavoidable-set decision, in the same code, with subdivision supplied by
the caller. That is the whole of “complex should be possible” in this design.

**Certificate.** The verifier’s output type stops being a boolean.
For a valid packing it carries, per pair, either the separating axis and the sign of the
gap, or an exact-zero witness; plus the container contacts.
For an invalid one, the offending pair and the axis-by-axis evidence.
This is the object the
[Lean work](../../research/research-2026-08-22-lean-for-packing-proofs-and-validation.md)
will consume, and it is independently re-checkable without re-running the search.

Note the current `separated()` computes exactly this information and then discards it —
it returns `1 / 0 / None` without saying *which* axis.
Retaining it is nearly free.

**`sqpack-search` (Rust).** Perturbed billiard/inflation and simulated annealing over
`sqpack-core`, with three properties that are cheap now and near-impossible to retrofit:

- **Counter-based RNG keyed by `(seed, kernel, chain, index)`** with `O(1)` random
  access, so any basin is addressable and replayable from its key alone.
- **Fixed-slot reductions in chain order**, so worker count never changes the answer.
- **Basin recording**: every local optimum reached, with its key, its refined side
  length, and its verification verdict.

**`sqpack` (Python, PyO3).** The simple surface: load a packing, verify it, run a
search, read basins.
Everything here may be “slow” — this is the agent tier, where the budget is seconds.

**The oracle.** The existing pure-Python verifier is retained permanently as the
differential-test reference.
Every Rust predicate result must match it.

### Stack and boundaries — decided by measurement

Measured on this machine, `n = 11`, before choosing anything:

| Stage | Cost |  |
| --- | ---: | --- |
| Annealer move (Rust or Numba) | 0.025 µs | 40 M/s/core |
| `ctypes` call, 33 f64 into numpy | 0.52 µs |  |
| JSONL round-trip, one candidate | 18.3 µs | 688 B/line |
| Annealer move (pure Python) | 43 µs |  |
| **LP quench (`scipy`/HiGHS)** | **1,283 µs** | 23 variables, 99 constraints |
| **Exact verify (Python `sqpack`)** | **129,000 µs** |  |

Seven orders of magnitude, and three conclusions fall straight out.

**The boundary cannot sit inside a move loop**, where even a bare FFI call costs four
moves. **Everywhere else it is free**: at candidate granularity `ctypes` is 0.04% of a
quench and even JSONL is 1.4%. So transport speed decides nothing here, and the seam
belongs between the proposer and the quench — which is where it already is.

**Most of the programme is quench-dominated, not move-dominated.** The census, the
premise test, δ-continuation, MAP-Elites and angle-class search all spend their time in
the LP, at ~780 candidates/s/core *in any language*. Only an annealing proposer is
move-dominated, and one already exists.

**The slowest stage is the exact verifier**, at 100× the LP and 5,000× the annealer.
That, not the search, is where compiled code earns its place.

The rule this yields, and the reason the phases below are ordered as they are:

> **Write it in Python.
> Accelerate what a profile says is slow, not what looks slow.**

Concretely: the spine is `scipy` and standard library, with no build step and no FFI.
[`sqsearch`](../../../../sqsearch/) stays a native binary behind a JSONL seam, because
it already exists and process isolation is worth having overnight.
If a strategy later needs the quench *inside* its loop, add a `cdylib` crate-type to the
same crate and call it with `ctypes` — 0.52 µs makes that viable, and it costs neither
`maturin` nor wheels.

**PyO3 is deferred, and may never be needed.** Its advantage is passing rich typed
objects, and the certificate — the one genuinely rich interface here — must serialize to
JSON regardless, for Lean and for third-party checking.
Once the durable interface is JSON, a binary or a `cdylib` serves it.
Revisit only if JSON round-trip is measured to bottleneck the exact layer.

**Numba is not used.** It measures equal to Rust, but it would pin `numpy<2.5`, add JIT
warmup, and produce opaque typing errors — the worst failure mode for an unattended run.
Its one real advantage was letting agents prototype a new strategy without a build step,
and that advantage evaporates once the spine is Python: a new quench-dominated strategy
prototypes in plain Python at full speed.

**What this does not change.** The “one predicate, many scalars” bet stays.
It is a claim about the *code*, not about the transport, and the proof lane’s `PoseBox`
still depends on it.
Deferring the Rust core defers when that lands, not whether.

**The spine, block by block.** Each is used by every proposer, so each is built once.

| Block | What it does | Unblocks |
| --- | --- | --- |
| `quench` | LP-in-cell: fix angles and axis assignment, solve the cell (exact in formulation; to solver precision in practice — see the revision note) | H-2; and every basin claim anyone makes |
| `canonicalize` | geometric key (`D₄` + relabel + quantize) and structural key (contact graph up to isomorphism) | R-1, H-9; comparability across move sets |
| `descriptors` | tilt-class count, contact class, oblique-core size, boundary/interior split — computed from canonical data, versioned with the atlas | H-15 steering, H-3 retention, atlas records |
| `verify` | the exact certificate (Phase 1) | H-8’s false-basin rate; any record claim |
| `atlas` | append-only dedup store keyed by canonical identity, with quench frequencies and discovery curves | H-11, H-12, H-7; the deliverable itself |
| `meter` | pair-test counter — the machine-independent budget currency | R-10; any comparison between proposers |

**The proposer interface.** One entry point: given `n`, a budget in pair-tests, a keyed
RNG, and optionally a set of seed configurations, yield candidate configurations.
That is the entire contract.
A proposer never quenches, never canonicalizes, never decides validity, and never writes
the atlas — so a new strategy cannot accidentally change what a basin means, and two
proposers are comparable by construction.

**The experiment-loop harness** (already landed, see
[`campaign/`](../../../../campaign/README.md)): the hypothesis registry, series, run
artifacts, generated ledger, and whole-set invariant checks that the review’s run
protocol calls for. Its run artifacts *are* the review’s “manifests”; its series are
S0–S6.

### API Changes

New, and additive — nothing existing is removed:

```python
import sqpack

pk = sqpack.load("trump11")  # or sqpack.Packing(squares, side)
cert = sqpack.verify(pk)  # exact by default
cert.valid  # True
cert.contacts  # 14 pairs, with exact-zero witnesses
cert.separations  # 41 pairs, each with its axis and sign
cert.to_json()  # the third-party-checkable object

sqpack.verify(pk, scalar="f64", tol=1e-9)  # fast and explicitly unsound
```

```python
run = sqpack.search(n=12, seed=42, budget=...)  # deterministic in seed
run.basins  # each with key, side, verdict
sqpack.search(n=12, seed=42, workers=32).digest == run.digest  # must hold
```

The Python `sqpack.verify_packing(..., sign=...)` signature stays as-is so `test.sh`
keeps passing unchanged.

## Implementation Plan

Every item below is a bead against this spec:

```bash
tbd list --spec explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
tbd ready    # what is unblocked now
```

Phases 2 and 3 are the load-bearing ones.
Phase 2 is runnable in the existing Python plus `scipy`, so it does not wait on Phase
1’s Rust.

### Phase 1: The quench spine

**First, because it is both the highest-leverage phase and the cheapest.** It is `scipy`
and standard library: no Rust, no FFI, no build step.
Until a float configuration can be turned into a named basin with an exact side length,
“basin” is undefined, basin statistics are artifacts of the cooling schedule, and no two
proposers can be compared.
The review’s H-2 is its own register’s top priority for this reason.

- [x] **`quench`: LP-in-cell.** Fix angles and each pair’s separating axis; solve the
  cell’s linear program.
  The single-cell half is already verified — a 1,056-constraint LP at Trump’s angles
  reproduced `s(11)` to solver precision and every centre to `9e-16`. What remains is
  the *loop*: angle moves between LP solves, behaviour at cell boundaries, and
  termination at a genuine cell-optimum.
- [ ] **`canonicalize`: basin identity, two-level.** Geometric key (`D₄` and square
  relabelling, quantized, hashed) as the fast path; contact graph up to isomorphism as
  ground truth.
- [ ] **`descriptors`**, computed from canonical data only, versioned alongside the
  atlas as a soft-schema artifact so archive keys and atlas identities cannot drift.
- [ ] **`atlas`**: append-only, deduplicated by canonical identity, carrying both keys,
  the exact side and its algebraic degree, quench frequency, contact graph, angle
  signature, symmetry group, and neighbour links with their merge-`δ`.
- [ ] **`meter`**: a pair-test counter through the whole pipeline, and `sqsearch`
  emitting it. Budgets, saturation thresholds and every comparison switch to pair-tests.
- [ ] Exact-verify every recorded basin, giving H-8’s false-basin rate for free.

**Done when:** the same float configuration quenches to the same named basin from any
proposer; a perturbed Trump packing quenches back to Trump’s cell with the exact side
(H-2 resolved); the atlas validates against its schema; and `sqsearch` reports
pair-tests.

Everything here is quench-dominated at ~780 candidates/s/core, which is the same in any
language, so there is nothing for compiled code to buy yet.

### Phase 2: The proposer interface

Thin by design. The work here is the boundary, not the strategies.

- [ ] The proposer contract:
  `(n, pair_test_budget, keyed_rng, seeds?) -> configurations`. No quenching, no
  canonicalization, no validity decisions, no atlas writes.
- [ ] Port the existing [`sqsearch`](../../../../sqsearch/) annealer behind it as
  proposer #1, and record **every** quenched local optimum rather than only the best —
  the current engine discards exactly the data the atlas is made of.
- [ ] A uniform multistart proposer, as the null every other proposer is measured
  against.
- [ ] Equal-budget harness: two proposers, one pipeline, comparable basin sets.

**Done when:** multistart and annealing run through one pipeline at equal pair-tests and
their basin sets are directly comparable; adding a proposer touches no spine code.

### Phase 3: The census, the premise, and the atlas

The phase that produces the deliverable.
It is mostly *running* the previous phases.

- [ ] **H-11 — census `n ≤ 10`** to saturation; ship the atlas as a soft-schema artifact
  with its discovery curves.
- [ ] **H-12 — the premise**: locate the record basin in the quench-frequency ranking.
  If record basins are *not* rare, most of the cartography programme stands down and the
  campaign reverts to throughput.
  This is the cheapest available test of it.
- [ ] **E2 — `n = 11`** basin statistics with canonical identity in place.
- [ ] **E3 — `n = 12`**, with a saturation-based standard for what a negative result
  means.
- [ ] Mechanism-matched calibration: `s(17)`, `n = 11` at inflated `δ`, basin-entry
  (H-18). The `n = 5`/`n = 10` ladder validates machinery only — both are 45° mechanisms
  and neither exercises an oblique core.
- [ ] Write results back into the frontier corpus and the research documents.

**Done when:** the atlas exists for `n ≤ 10` with discovery curves attached, H-12 has a
verdict, and the same seed reproduces the same basin digest on 1 worker and on 32.

### Phase 4: Strategy proposers

Each of these is now small, each corresponds to a registered hypothesis with a kill
criterion already written, and — because they are all quench-dominated — each is written
in Python at full speed.

- [ ] **δ-continuation** (H-13): inflate the container, walk `δ` down with a re-quench
  at every step. Its merge-`δ` data is the atlas’s barrier scale, so the same runs pay
  twice.
- [ ] **Angle-class two-level** (H-1): outer over class count and angles, inner the cell
  LP.
- [ ] **Neighbour-transfer seeding** (H-4): seeds built from `n ± 1` records.
- [ ] **MAP-Elites archive** (H-15): keyed on tilt-class × contact-class, because single
  scalars are hackable — the grid maximises contact count.
- [ ] **Billiard/inflation**, the method that produced the `n = 29, 37` records.

**Done when:** each lands as a proposer with no spine changes, and each is measured
against multistart at equal pair-tests on the ladder plus `n = 11`.

### Phase 5: Compiled acceleration, where the profile says

**Deliberately late, and scoped by measurement rather than by ambition.** By this point
the profile of a real campaign exists, and it says what to accelerate.

On the numbers taken before any of this was written, the exact verifier is the
candidate: 129 ms per `n = 11` verification, 100× the LP quench and 5,000× an annealer
move. Verifying every basin in a `10⁵`-basin census would take hours.
Nothing else in the pipeline is close, and the annealer — the thing that looks slowest —
already has a compiled implementation.

So this phase begins by re-measuring, and builds only what the measurement names.

- [ ] `sqpack-core` crate: `Scalar` trait; corners, separating-axis test, containment,
  grid bucketing. Generic, no allocation on the hot path.

- [ ] `f64` and `Filtered` scalars; the staged ladder with per-stage filter-rate
  counters.

- [ ] `Algebraic` scalar over `ℚ(α)` backed by FLINT, with exact zero test and exact
  sign.

- [ ] Certificate type replacing the boolean return; JSON serialization.

- [ ] Retain the separating axis and sign in `separated()` in the Python oracle too, so
  both sides emit the same certificate shape.

- [ ] PyO3 bindings: `load`, `verify`, `Packing`, `Certificate`.

- [ ] Differential test: Rust versus the Python oracle on Trump’s packing, on every
  negative control already in `negative_control.py`, and on every corpus entry with
  exact algebraic data.

- [ ] Extend `test.sh` with the differential test and the certificate round-trip.

- [ ] **E1 — corpus re-verification.** Every analytically-optimized record, exactly,
  with filter rates per `n`. This is what the speed is *for*.

**Done when:** a certificate returns in **under 10 ms** for `n = 11` (against 129 ms
today), the Rust and Python verdicts agree everywhere, and every analytically-optimized
record in the corpus verifies exactly.

**Boundary:** a native binary or a `cdylib` called with `ctypes`, not PyO3 — see
[Stack and boundaries](#stack-and-boundaries--decided-by-measurement).
The certificate’s durable interface is JSON either way.

### Phase 6: The proof lane

- [ ] `PoseBox` scalar and `hits_all_poses(points, box)` — the hook, subdivision left to
  the caller. One worked example, no proof attempt.
- [ ] **H-10 — the Stromquist falsifier triple.** A known-answer test: failure is a
  machinery bug by definition.
- [ ] **H-6 — LP duals as unavoidable-set generators** at side 4 for `n = 12`.

**Done when:** the falsifier reproduces Stromquist’s two-stage result and the dual
support at side 4 has been characterised.

### Phase 7: The LLM lanes

Deliberately last, and gated on Phase 5’s first atlas artifact — there must be something
verified to read.

- [ ] **Atlas reading**: qualitative analysis over verified per-basin descriptors.
- [ ] **Constructor DSL** (the FunSearch shape): programs whose semantics end in LP
  quench plus exact verification, so the evaluator is exact and the model’s error rate
  is affordable. Designable on paper in parallel with earlier phases.
- [ ] **Cross-`n` transfer** of mechanisms, with the atlas as the source.

Grounding rule, non-negotiable: nothing unverified enters a prompt, and nothing leaves a
model into the atlas or the corpus without passing the exact layer.

## Testing Strategy

The existing `test.sh` is the harness; these are additions to it.

**Differential testing against the oracle.** The pure-Python verifier is the reference
implementation. Every Rust verdict must match it on: Trump’s packing, all six
perturbation magnitudes in `negative_control.py` (down to `δ = 10⁻¹⁰⁰`), and every
corpus entry carrying exact algebraic data.
This is what stops the fast path from being the wrong path — the failure mode that
matters most here.

**Negative controls, kept and extended.** The existing controls establish that the exact
verifier rejects any overlap while a float verifier with any tolerance has a blind spot.
Rust must reproduce both halves, including the float verifier’s *failure*: a fast path
that accidentally became sound would mean the test is not testing what it claims.

**Determinism.** Same seed, 1 worker versus 32, bit-identical basin digest.
Asserted, not assumed — this is the property that makes E4 publishable and it degrades
silently.

**Certificate round-trip.** Serialize, re-load, and re-check a certificate without the
original packing object or the search that produced it.
An unverifiable certificate is worse than none.

**Quench idempotence.** Quenching a quenched configuration must be a no-op, and a
configuration perturbed within its cell must quench back to the same canonical key.
This is the property that makes “basin” mean anything, and it degrades silently.

**Canonical identity under symmetry.** The same packing presented under any of the
container’s 8 symmetries and any square relabelling must produce one canonical key.
Verified by construction: generate the orbit, assert a single key.

**Proposer equivalence.** Two proposers seeded to produce the same configurations must
produce identical basin sets — the pipeline, not the proposer, decides what a basin is.

**Performance floors, with the discipline the FrankenSim study argues for.** Assert
against a floor, report median and interquartile dispersion, and record the machine —
never a bare “fast”.
Floors, from measurements already taken:

| Check | Floor | Source of the number |
| --- | --- | --- |
| `f64` SAT throughput | ≥ 10 M pair-tests/s/core | 17.7 M measured in the infrastructure study |
| Exact `n = 11` verification | ≤ 10 ms | 0.35 s in Python; FLINT measured 177× at degree 8 |
| Corpus verification | completes in minutes | scaling from the above |

## Rollout Plan

Everything lands in `explorations/packing/`, alongside what is already there.
The Python `sqpack` package keeps working throughout — Phase 1 adds a faster path and a
richer return type without changing the existing signature, so `test.sh` passes at every
commit.

Rust is additive: `cargo` is not required to run the existing Python suite, and
`test.sh` skips the Rust checks when no toolchain is present, in the same way it already
skips the SymPy-dependent derivation.

No deployment, no consumers outside this repository, no compatibility surface to
maintain.
The one durable interface is the **certificate JSON**, which the Lean work will
consume; version it from the start.

## Open Questions

- Is `flint-sys` or `rug` the right Rust binding for the algebraic scalar, and what does
  the pure-safe-Rust `malachite` alternative cost at degree 40–62? Phase 1 should
  measure rather than assume.
- What is the real filter rate on the corpus — what fraction of pairs need the exact
  path at each `n`? Known only for `n = 11` (14 of 55), and that is the smallest case.
- Does the annealing move set need exact arithmetic anywhere, or is float-plus-refine
  plus a final exact check enough?
  Cheap to test, and it decides how much of the exact layer the search links against.
- **What quantization resolution does the geometric key need?** Too coarse merges
  distinct basins, too fine splits one basin across floating-point noise.
  The structural key is the arbiter, so this is a performance question, but it needs a
  measured answer rather than a guess.
- **How does the atlas scale past `n = 10`?** If H-11 finds no plateau, enumeration is
  out and coverage estimation over descriptor space (H-7) replaces it.
  The fallback is registered; the trigger is not yet measured.
- **Which descriptors actually separate the grid funnel from the rigid-rare family?**
  Tilt-class × contact-class is the minimum the strategy report argues for, but the
  separating power is an empirical question the first atlas answers.
- Does `PoseBox` want subdivision inside the core or left to the caller?
  Left out for now; E-lane experience should decide.
- For E3, what counts as a sufficient negative result on `n = 12`? “We searched and
  found nothing” needs a stated budget to mean anything.

## Revision history

**2026-08-23 (later) — the harness exists, and it changes what a phase item must ship.**

`campaign/runner.py` now executes rounds unattended, and it reads a machine-readable
`runner.command` recipe from each hypothesis rather than the prose `instrument` field.
So a Phase item is not finished when its code works: it is finished when the hypothesis
it unblocks carries a recipe and has `instrument_ready: true` flipped **in the same
change**. Anything less leaves a queue entry that reads runnable to a human and is
invisible to the harness.

Two consequences worth stating here rather than rediscovering:

- **The harness holds no experiment code.** A new proposer is a command obeying the
  contract in `campaign/README.md`, not a branch inside the runner.
  If a Phase item would edit `runner.py`, the contract is wrong and that is what to fix.
- **`meter` (`think-b4jc`) gates cross-proposer comparison, not execution.** Rounds run
  fine on wall-clock budgets; what they may not do until pair-tests exist is claim two
  proposers were compared at equal budget.
  Phase 4 depends on it; Phase 3 does not.

Scheduling of the first long unattended session — which pieces it takes, in what order,
and where the watched half ends — is
[the overnight cartography run](plan-2026-08-23-overnight-cartography-run.md).
This spec stays the enumeration of the pieces; that one is the plan for one night of
them.

**2026-08-23 — what building the quench changed.**

Three claims in this spec and the documents behind it did not survive contact with an
implementation, and are corrected here rather than left to be discovered again:

- **“Exact” belongs to the formulation, not to the build.** For fixed angles and a fixed
  axis assignment the cell optimum *is* the solution of a linear program, and that is
  still true. A floating-point LP solver does not deliver it: at its default tolerance it
  returned a packing violating its own separation constraint, and so a side below the
  standing record ([D-014](../../../defects.md)). Pinned at the solver’s floor the
  residual is about `1e-11` in the side ([D-021](../../../defects.md), open).
  The `polished` tier means *exact within a cell to solver precision*; algebraic
  exactness stays with `sqpack`, and every promotion must route through it.
- **The polish step does not produce rational output.** The review’s R-2 says it does;
  `scipy`/HiGHS returns floats.
  Rational output needs an exact rational LP, which is unbuilt and tracked
  (`think-hg3u`).
- **Basin identity must not inherit the search’s knobs.** A quench whose angle search
  merges nearby angles returns a constrained optimum, so what counts as a basin would
  depend on the merge tolerance ([D-020](../../../defects.md)). Fixed by a free-angle
  pass that certifies the landing point is a genuine local optimum; the general rule is
  in the [postmortem](../../postmortems/postmortem-2026-08-23-soundness-class.md).

And one addition to Phase 1’s definition of done: a new component joins the **soundness
perimeter** ([`tools/perimeter_test.py`](../../../../tools/perimeter_test.py)) in the
same change that introduces it.
The quench did not, which is why D-014 was possible.

**2026-08-23 (second revision) — Python first, compiled code where a profile says.**

The stack was priced rather than argued.
The pipeline spans seven orders of magnitude, from a 0.025 µs annealer move to a 129 ms
exact verification, and the middle of it — the LP quench at 1.28 ms — is where nearly
every planned strategy spends its time, at the same rate in any language.
So Phases 1–4 are pure Python with no build step, and the Rust verification core that
used to open this spec moved to Phase 5, scoped by a profile of a campaign that has
actually run. `PyO3` is deferred and may never be needed, because the certificate must
serialize to JSON regardless.
See [Stack and boundaries](#stack-and-boundaries--decided-by-measurement).

The risk this accepts, stated plainly: a Python spine is slower per candidate than a
compiled one, so if the census needs far more basins than expected, Phase 5 arrives
sooner and larger than planned.
That is the better failure.
The alternative is building a `Scalar`-generic Rust core plus bindings before knowing
which stage is hot — and the measurement says it was the verifier all along, not the
search everyone assumed.

**2026-08-23 (first revision) — revised to flow from the strategy layer, and to absorb a
parallel implementation.**

Two things happened after this spec was written.
The
[search-philosophy report](../../research/research-2026-08-23-search-philosophy-and-landscape-cartography.md)
supplied the strategy layer, reframing the deliverable from a record to a map.
And a parallel branch built an experiment-loop harness and a first search engine against
an earlier version of this plan, without knowledge of the review or the strategy report.

What changed here:

- **The approach is now proposer-over-spine.** Reading the hypothesis register as a
  build list shows almost every entry is a way of *proposing* configurations over one
  shared downstream pipeline.
  Building the spine once is what makes the register cheap; building per-strategy makes
  each entry a project and the results incomparable.
- **The quench spine became a phase of its own** (LP-in-cell, canonical identity,
  descriptors, atlas, pair-test meter) rather than “search and experiments”.
  The original Phase 2 presumed a refiner it never built — the review’s R-2 — which left
  basin identity undefined.
- **The proposer interface, the census and premise test, the strategy proposers, the
  proof lane and the LLM lanes are new**, in dependency order.
- **Budgets are pair-tests** (R-10), and the `n = 5`/`n = 10` ladder is explicitly
  demoted to machinery validation: both are 45° mechanisms and neither exercises the
  oblique core `n = 11` demands.

What the parallel branch contributed, now folded in: the experiment-loop harness
([`campaign/`](../../../../campaign/README.md)) implementing the review’s run protocol
as validated artifacts rather than prose; a working f64 annealer
([`sqsearch`](../../../../sqsearch/)), which becomes a proposer behind the Phase 2
contract; a measured backend decision (Rust and Numba are equivalent, the GPU loses by
8× at this size); and a baseline round whose controls caught two instrument defects
before any strategy was tested.
Its hypotheses were renumbered above this register’s `H-001`–`H-015` block.

## References

Research documents this spec implements:

- [Packing 11 Unit Squares in a Square](../../research/research-2026-08-22-packing-11-unit-squares.md)
- [Algorithms and Tooling for Square Packing](../../research/research-2026-08-22-square-packing-algorithms-and-tooling.md)
- [FrankenSim as a Rust Toolkit for Square Packing](../../research/research-2026-08-22-frankensim-rust-toolkit-for-square-packing.md)
- [Infrastructure for Square-Packing Exploration](../../research/research-2026-08-22-infrastructure-for-packing-exploration.md)
- [Lean for Square-Packing Proofs and Validation](../../research/research-2026-08-22-lean-for-packing-proofs-and-validation.md)

Existing code and data this builds on:

- [`explorations/packing/`](../../../../README.md) — the Python verifier, negative
  controls, and `test.sh`.
- [`explorations/packing/frontier/`](../../../../frontier/README.md) — the per-`n`
  corpus and the datasets the experiments will write back into.

External:

- [`jagua-rs`](https://github.com/JeroenGar/jagua-rs) — MPL-2.0 collision detection with
  continuous rotation, if the hand-rolled bucketing proves insufficient.
- [FLINT](https://flintlib.org/) and [PyO3](https://pyo3.rs/).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
