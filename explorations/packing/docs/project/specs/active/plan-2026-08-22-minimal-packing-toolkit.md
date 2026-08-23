# Feature: Minimal Packing Toolkit

**Date:** 2026-08-22 (last updated 2026-08-22)

**Author:** Claude (agent), for samanthadrakova@gmail.com

**Status:** Draft

## Overview

A minimum kit of composable pieces for running the first real experiments on `s(n)`:
**search for candidate packings, verify them exactly and fast, and iterate** — with
`n = 11` and `n = 12` as the working cases, and with the proof lane reachable from the
same parts rather than needing a second system.

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

A small Rust core with thin Python bindings, built so the fast path and the exact path
are the same code.

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

### API Changes

New, and additive — nothing existing is removed:

```python
import sqpack

pk = sqpack.load("trump11")            # or sqpack.Packing(squares, side)
cert = sqpack.verify(pk)               # exact by default
cert.valid                             # True
cert.contacts                          # 14 pairs, with exact-zero witnesses
cert.separations                       # 41 pairs, each with its axis and sign
cert.to_json()                         # the third-party-checkable object

sqpack.verify(pk, scalar="f64", tol=1e-9)   # fast and explicitly unsound
```

```python
run = sqpack.search(n=12, seed=42, budget=...)   # deterministic in seed
run.basins                                        # each with key, side, verdict
sqpack.search(n=12, seed=42, workers=32).digest == run.digest   # must hold
```

The Python `sqpack.verify_packing(..., sign=...)` signature stays as-is so `test.sh`
keeps passing unchanged.

## Implementation Plan

### Phase 1: The verification core

The spine. Everything else depends on it, and it is independently useful the moment it
lands — it delivers the first exact re-verification of the record corpus.

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

**Done when:** `sqpack.verify(pk)` returns a certificate in **under 10 ms** for `n = 11`
(against 0.35 s today), the Rust and Python verdicts agree everywhere, and every
analytically-optimized record in the corpus verifies exactly.

### Phase 2: Search, and the `n = 11` / `n = 12` experiments

- [ ] `sqpack-search`: annealing and perturbed-billiard moves over `sqpack-core`,
  counter-based RNG, fixed-slot reductions, basin recording.
- [ ] `PoseBox` scalar and a `hits_all_poses(points, box)` entry point — the proof-lane
  hook, with subdivision left to the caller.
  One worked example, no proof attempt.
- [ ] Python bindings for search and basin inspection.
- [ ] **E1 — corpus re-verification.** Verify every analytically-optimized record
  exactly. Record filter rates per `n`.
- [ ] **E2 — rediscover `n = 11`.** Search from randomness and check whether Trump’s
  basin is reached, how often, and at what cost.
  A test with a known answer.
- [ ] **E3 — `n = 12`.** Search for anything beating the trivial grid at side 4. A
  negative result here is a real datum: nothing has ever beaten it, and nobody has
  published how hard they looked.
- [ ] **E4 — basin statistics** for `n = 11` and `n = 12`, in the shape Ellsworth
  published for `s(51)` — basin count, record-basin frequency, expected time to hit —
  but reproducible from a seed, which his are not.
- [ ] Write the results into the frontier corpus and the research docs.

**Done when:** the same seed produces the same basin digest on 1 worker and on 32, E2
reaches Trump’s basin, and E3/E4 produce numbers worth putting in a document.

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
- Does `PoseBox` want subdivision inside the core or left to the caller?
  Left out for now; E-lane experience should decide.
- For E3, what counts as a sufficient negative result on `n = 12`? “We searched and
  found nothing” needs a stated budget to mean anything.

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
