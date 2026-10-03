---
title: n17 Cost Reduction by Performance Engineering
date: 2026-10-02
status: planning-review
---
# n17 Cost Reduction by Performance Engineering

**Session:** 168, BC-418, lane F2. **Baseline:** `c045e43f`, with W7 and A admitted
under exp-249 and the [residue process review](review-2026-10-02-n17-residue-process.md)
costing the global half at $4\times10^{3}$ to $4\times10^{4}$ CPU-hours, almost all of
it exact arithmetic in Python.
**Question:** how far can the *rate*, the CPU-seconds per row, per facet inequality and
per branch-and-bound node, be cut per certificate and per verification, and what does
that do to the total?
Lane F1’s [pruning review](review-2026-10-02-n17-cost-reduction-pruning.md) covers the
count and size of certificates; section 6 here multiplies the two.

This review changes no bound, verdict or frontier field.
Its measurements are profiles of the retained tools and micro-benchmarks on rows taken
from the W7 and A certificates, run read-only on one worker: `profile_all.sh`,
`bench_collision.py`, `bench_sweep.py`, `bench_load.py`, `bench_bbverify.py`,
`bench_dropin.py`, `bench_dropin2.py` and a Rust comparison under `rustbench/`. Their
outputs and sources are kept in
[`handoff/f2/`](../../../packing/campaign/explorations/X048-session-168-pilots/handoff/f2/)
in X048, the scripts with a `.txt` suffix and the binary `.prof` dumps left out.
They are planning evidence, outside the record for the usual reason.
The container was shared with three other lanes throughout (load average 6 to 11 on four
cores) and cProfile inflates call-heavy Python by two to three times, so every absolute
time below comes from a retained receipt, and every speedup is a ratio of two runs made
back to back in one process on the same input.

## Summary

- **The verifiers are the cost, not the producers.** From the receipts, W7’s kernel
  certificate cost 838 CPU-seconds to produce, 930 to check and 4,258 to verify (71%);
  A’s branch-and-bound certificate cost 544 to produce and 1,550 to verify (74%). The
  cost model’s unit costs are mostly verification, and the standing verifiers are the
  slowest code in the pipeline: the kernel verifier proves each row’s cover by exact
  area subtraction at 5.2 times the checker’s sweep, and checks every collision facet in
  `Fraction` at 23 times the checker’s integer form; the branch-and-bound verifier
  re-validates every cut 5.1 times, once per bound that cites it.
- **Fraction’s own overhead is about two thirds of every Python tool.** In the profiles,
  `fractions.py` dispatch, `isinstance` and `math.gcd` take 55% to 65% of the kernel
  producer, checker and verifier and 17% to 20% of the branch-and-bound verifier; the
  branch-and-bound producer is the exception, with 41% of its uninstrumented time inside
  HiGHS.
- **Measured levers.** On W7’s heaviest rows, homogeneous integers beat `Fraction` by 23
  times on collision facets, a cache of the facet sets by core pair adds 1.85, and
  gmpy2’s `mpq` rebound in place of `Fraction` gives 10.9 on the same collision code,
  3.9 on the checker’s sweep, 4.7 on the verifier’s area cover and 4.7 on the whole
  branch-and-bound verifier, with identical check counts; python-flint gives 2 to 4; a
  Rust port on `num-bigint` beats the checker’s Python integers by only 2.3 because it
  allocates, so a compiled gain of 5 to 10 on the integer parts is an estimate that
  needs GMP or fixed-width words.
- **The ranked plan** (section 5) rewrites the two verifiers’ hot loops first, then
  rebinds the kernel to gmpy2, then compiles the kernel’s collision and sweep behind the
  resident-process protocol the repository already uses.
  The first four steps are days of work and take a W7-sized certificate from 6,026 to
  about 750 CPU-seconds (8 times) and an A-sized one from 2,094 to about 760 (2.7
  times); the compiled steps are weeks and reach about 15 to 23 times on the kernel.
- **Soundness is untouched as long as the verifier stays separate code and the two sides
  use different arithmetic.** Backend swaps, caches of pure exact functions and row
  parallelism change no obligation; a changed checker costs one re-check of the admitted
  objects (minutes after step 3), which is why the checker should be frozen before the
  batch; a compiled verifier must share no geometry code with a compiled checker, and
  the cheapest diversity is to leave the verifier on CPython’s integers when the checker
  moves to GMP.
- **The total.** Rate alone takes $4\times10^{3}$ to $4\times10^{4}$ CPU-hours to about
  750 to 6,100 with the Python-level steps and 450 to 2,800 with the compiled kernel:
  hundreds only at the model’s low end.
  Multiplied into F1’s plan, its 600 to 1,450 CPU-hours becomes about 120 to 245 with
  the Python-level steps and 75 to 130 compiled; with the size lever corrected below,
  185 to 360 and 100 to 180. F1’s falsified case, a tail of a thousand per-state nodes,
  lands at 750 to 2,240 or 330 to 1,000. The correction: on the measured split, halving
  rows halves a node’s cost rather than quartering it, since only the collision share
  scales with rows squared.

## 1. Where the Time Goes

### 1.1 Per Certificate, From the Receipts

| Certificate | Producer | Checker | Verifier | Total | Verifier share |
| --- | ---: | ---: | ---: | ---: | ---: |
| W7, kernel: 58 steps, 3,712 rows, 7,752 collision regions, 430,000 region–partner-row pairs, 30.95 million facet inequalities | 838 s | 930 s (indexed sweep) | 4,258 s | 6,026 s = 1.67 h | 71% |
| A, branch and bound: 41,598 nodes, 639,609 bounds, 324,934 cuts, 4,504 Farkas closures | 544 s (499 without the recorder) | — | 1,550 s | 2,094 s = 0.58 h | 74% |

Sources: `receipts/kernel-closure-W7-reproduce.json`,
`certificates/W7/verification.json`, `receipts/bb-A-certified.json`,
`certificates/A/verification.json`. The checker alone on W7’s saved objects with the
reference all-pairs sweep (`--check-saved`) took 1,634 s against 930 with the indexed
sweep; the two prove the same cover.
A stalled kernel node costs its producer and checker and no verifier: NW7 1,217 s, P5
1,084 s, W7 without side-N0 1,688 s.

### 1.2 The Kernel Producer and Checker

Profiled on W7’s first round at 64 rows (7 steps, 448 rows, 1,308 collision regions;
receipt `kernel-W7-round1.json`, producer 389 s, checker 529 s) and on B at 16 rows to a
certified stall (12 steps, 192 rows; producer 27 s, checker 17 s uninstrumented).
Shares are of the tool’s own cumulative profile time.

| Tool | Where | Share | What it is |
| --- | --- | ---: | --- |
| Checker | `covers.indexed_union_cover` | 66% | the exact vertical sweep: event construction 33%, probes 31% |
| Checker | `collision.integer_universal_collision` | 11% | the homogeneous-integer facet checks |
| Checker | `sequential.admit_partner_covers` | 7% | every live partner row’s hull and strict core, every step |
| Checker | hulls, strict cores, parsing | 16% |  |
| Producer | `producer.collision_region` | 48% | the facets of $Q_r-Q_i$ by edge merge, 37%; float location and integer admission |
| Producer | `producer.subtract` | 28% | exact convex subtraction of forbidden and collision regions |
| Producer | `producer.partner_cover` | 7% |  |
| Producer | seed, kernel points, compression | 17% |  |

`Fraction` internals (`forward`, `_richcmp`, `_from_coprime_ints`, `gcd`, `isinstance`)
are 65% of the round-1 profile and about two thirds of the B profile.
The checker’s `events` and `probes` counts in the receipts are the sweep’s unit of work;
at 64 rows W7 had 314,780 events over 3,712 rows.

### 1.3 The Kernel Verifier

Profiled on W7 in sample mode, two rows per step plus every row of the closure step (168
rows in full, 362 collision regions, 1.17 million facet inequalities), 1,529 s under the
profiler.

| Where | Share of the sample | Scales with |
| --- | ---: | --- |
| `covered_by_area` (cover by exact area subtraction, `subtract_pieces`, `clip_closed`) | 41% | rows times regions per row |
| `check_partners` (every live partner row’s hull and strict core, every step: 19,282 rows) | 30% | steps times partner rows |
| `check_collisions` (`minkowski_diff` hull in `Fraction` per region and partner row, then every facet at every vertex) | 9% | rows times partner rows times facets |
| `compress`, seed, final state, load | 5% |  |
| `Fraction` internals, across the above | 63%; `math.gcd` alone 17% |  |

In a full run every row is checked, so the per-step partner share shrinks to a few per
cent and the extrapolated split is about four fifths cover and a sixth collision.
That extrapolation is the one number here that a full profiled run would sharpen; the
micro-benchmarks of section 2 measure both parts directly.

### 1.4 The Branch and Bound

Profiled on A for 60 s (1,778 nodes; the certified run is 13.1 ms per node
uninstrumented, 41,598 nodes in 544 s).

| Where | Share | What it is |
| --- | ---: | --- |
| `tighten` (bound tightening) | 53% | 36 HiGHS re-solves per node at about 150 µs each, 16%; `dual_bound` in Python interval floats, 11%; result marshalling and `changeColsCost`, the rest |
| `relaxation` → `pair_term` | 41% | `option_halfplanes` 17%, `hull_cuts` 17% (`plane_min` 10%) |
| `clip_to_box` (exact `Fraction` clipping of boxes to cells, LRU-cached) | 21% | counted inside the two rows above |
| interval primitives `imul`, `dn`, `up`, `iadd` | 35% of self time | 16 million `math.nextafter` calls per minute |

HiGHS itself is 5.4 of the 13.1 ms per node, so the Python parts bound any rewrite of
this producer at about 2.4 times unless the number of LP solves per node changes, which
is F1’s Taylor relaxation (its section 4.2), not a rate lever.

### 1.5 The Branch-and-Bound Verifier

Profiled on A in sample mode (1,052 nodes, 17,974 bounds, 42,534 cut checks, 200 s).

| Where | Share | What it is |
| --- | ---: | --- |
| `check_bounds` → `combination_min` | 79% / 71% | the Farkas and bound combinations, C3 and C4 |
| of which `row_of` → `plane_box_min` → `clip_polygon` | 67% | re-validating a cut (C2) by clipping the d-box by every possible plane of its pair |
| `math.gcd` | 17% of self time | `Fraction` normalisation |
| gzip, read, JSON decode | 11% (about 4% in full mode, where each chunk is read twice) | 483 MB of canonical JSON in 86 files, 12.7 million rational strings |

Over the whole certificate there are 1,652,060 cut references for 324,934 distinct cuts:
each cut is validated 5.1 times on average, since `row_of` recomputes the minimum over
the pair’s planes every time a bound’s multipliers cite the cut.

### 1.6 Fixed Costs

Loading is small today and grows in share as the arithmetic shrinks: W7’s 88 MB node
takes 0.5 s to gunzip, 0.1 s to digest, 1.8 s to decode and 5.7 s to parse its 2.0
million rationals into `Fraction`; A’s 483 MB takes 2.3, 0.7 and 29 s to decode, and
`load_tree` plus the node pass read every chunk twice, about 60 s of the 1,550.
Certificate size itself is a size lever (F1, section 4.1).

## 2. The Levers, Measured

Every ratio is one run against another on the same rows of W7’s step 3 (the heaviest:
256 collision regions against 384 live partner rows), in one process, on the project
interpreter with gmpy2 2.3.1 and python-flint 0.9.0 installed into a scratch
environment. The Rust comparison is `rustbench/`, built with `num-bigint` 0.4 in release
mode, on the same facet instances exported to JSON.

### 2.1 Collision Facets

60 regions against every live row of their partner: 3,840 region–partner-row pairs,
596,900 inequalities, every variant verifying the same count.

| Form | µs per pair | Against |
| --- | ---: | --- |
| `Fraction`, the verifier’s form: hull of pairwise differences, then facets (`universal_collision`) | 8,224 | 1 |
| `Fraction`, the same without the query-domain check | 5,816 |  |
| gmpy2 `mpq`, the same code | 534 | 10.9 over `Fraction` |
| python-flint `fmpq`, the same code | 1,456 | 4.0 over `Fraction` |
| Homogeneous integers, the checker’s form (`integer_universal_collision`) | 354 | 23 over the verifier’s form |
| gmpy2 `mpz` homogeneous | 242 | 1.46 over Python integers |
| Python integers with the facet set cached per (core, partner core) and the domain minimum per (partner row, normal) | 192 | 1.85 over the checker’s form; 960 facet sets served 3,840 pairs |
| Rust `num-bigint`, uncached | 154 | 2.3 over the checker’s form |
| Rust `num-bigint`, cached | 99 | 1.9 over the Python cache |

The cache works because a core depends only on the row’s angle interval, so a node at 64
rows has at most 64 distinct cores and 4,096 distinct Minkowski differences, against
430,000 pairs in W7. The Rust figure is a floor: `num-bigint` allocates on every
product, and the operands (residual vertices of about 90 bits in numerator and
denominator, median, 148 at most; homogeneous products of 300 to 450 bits) fit a
fixed-width 512-bit word, where the same loop is a few microseconds per pair.
A compiled gain of 5 to 10 over the checker’s Python integers is therefore an estimate,
not a measurement.

### 2.2 The Row Cover

24 rows with 54 regions each (6 forbidden, about 4 collision, the rest residual pieces).

| Form | ms per row | Against |
| --- | ---: | --- |
| Verifier: area subtraction, `Fraction` | 755 | 1 |
| Checker: indexed sweep, `Fraction` | 145 | 5.2 over the verifier |
| Checker: fast sweep, `Fraction` | 203 |  |
| Reference all-pairs sweep (`--check-saved` today) | 759 | 5.2 slower than indexed |
| Verifier: area subtraction, gmpy2 `mpq` | 160 | 4.7 over `Fraction` |
| Verifier: area subtraction, python-flint `fmpq` | 385 | 2.0 over `Fraction` |
| Checker: indexed sweep, gmpy2 `mpq` | 36.7 | 3.9 over `Fraction`; 20.6 over the verifier today |

### 2.3 Drop-In Trials of Whole Tools

Rebinding `Q` (and `Fraction`) to gmpy2’s `mpq` in the loaded module, then running the
same checks on the same objects, Fraction first and `mpq` second in one process:

| Tool | Input | `Fraction` | `mpq` | Gain | Counts |
| --- | --- | ---: | ---: | ---: | --- |
| Branch-and-bound verifier (`check_nodes`) | 2,424 nodes of A, 150 of them `lp` closures and their ancestors | 105.3 ms per node | 22.5 | 4.7 | identical: 109,186 cuts, 46,117 bounds, 150 closures, no failure |
| Kernel verifier (`verify_objects`) | W7’s first 3 steps, 6 rows per step, to the same truncation refusal | 23.0 s | 6.4 s | 3.6 | identical |
| Kernel checker (`replay_sequential`, indexed cover) | W7’s first 3 steps, every row, to the same truncation refusal | 29.9 s | 10.4 s | 2.9 | identical |

`mpq` is a drop-in because it carries `numerator` and `denominator`, hashes and compares
as `Fraction` does, accepts `"p/q"` strings and prints them back the same way, so
canonical JSON and digests are unchanged.
The checker’s method controls (the n11 mask-0 and case-2095 replays, which must match
the frozen checkers bit for bit) compare rationals, which `mpq` equals exactly.

### 2.4 Rows: 64 Against 32

Where it matters for F1’s rank-1 lever, the receipts already compare the two.
Per row, the checker costs 0.167 to 0.196 s at 64 rows (W7, two runs) and 0.138 to 0.166
s at 32 (A to a stall, A at the time cap, W7 at the time cap); the producer costs 0.20
to 0.21 s at 64 and 0.21 to 0.22 at 32 after the collision speedup.
Halving rows therefore halves a node’s producer and checker cost, not quarters it: the
sweep is linear in rows (its cost is regions per row, which does not depend on rows),
and only the collision share, 11% of the checker and about a sixth of the verifier,
scales with rows times partner rows.
An octagon core raises that share, since each Minkowski difference then has up to
sixteen facets rather than eight.
On the measured split, F1’s rank-1 step is about a twofold cut at 32 rows and fourfold
at 16, before any rate lever; the fourfold and sixteenfold figures in its section 4.1
assume a verification that is all facets, which section 1.3 does not bear out.

## 3. The Levers, Estimated

- **Batching.** Pure Python gains nothing from it; its value is at a compiled boundary.
  The repository’s pattern is `sqpack/rust_rectangle_geometry.py`: a resident child
  process (`sqverify_exact`) taking one JSON line per batch, a table digest per session,
  the binary’s digest in every receipt, and Python keeping every proof decision.
  A step’s rows, or a node’s facet instances, are the natural batch; one call per step
  keeps the protocol overhead below a second per node.
- **Rust.** Measured as a floor in section 2.1 (2.3 on `num-bigint`); estimated 5 to 10
  over the checker’s Python integers on collision with GMP (`rug`) or fixed-width
  integers, and 10 to 20 over `Fraction` on the sweep, since `Fraction` spends two
  thirds of its time in interpreter dispatch that a compiled rational type does not pay.
  Build: two to four weeks for a batched exact-geometry crate (clip, hull, Minkowski
  facets, the sweep) with differential tests against the Python checker on W7, the A
  stall and the n11 replays; the same again for a separate verifier crate.
- **Avoiding repeated recomputation in the verifiers.** Measured in counts: the
  branch-and-bound verifier validates each cut 5.1 times (section 1.5), so a cache per
  round of the cut’s validated minimum cuts its dominant share by that factor, about 2.2
  on the whole verifier; the kernel verifier rebuilds a `Fraction` hull for every
  region–partner-row pair where 4,096 distinct ones exist (section 2.1), and re-proves
  every live partner row’s core strict at every step (30% of the sample profile) where
  the row changes only when its owner steps.
  Both are memoisation of pure exact functions on their inputs.
- **Producer-side operand shrinking.** Core vertices carry 64-bit denominators (median)
  from `envelope_core`’s trig and shrink loop, and every downstream product inherits
  them; snapping the core inward to the $2^{-24}$ grid is a smaller, still strict core
  (`strict_core` decides), and halves the bits of every residual vertex, collision plane
  and facet product. Estimated 1.2 to 1.5 on all three tools, more in Rust where it
  decides whether operands fit a machine word.
  Rounding partner-cover domains outward would do the same for the collision step but
  the grammar pins the domain to the exact hull of the residual vertices
  (`admit_partner_covers`, `same(...)`), so it is a checker change.
- **Parallelism.** Across patterns and states the work is embarrassingly parallel, as
  the residue process review says; CPU-hours are unchanged and the wall time divides by
  the workers. Within a node, the rows of a step are independent in the producer
  (`produce_row`), the checker (`check_row`) and the verifier (`check_step`’s loop)
  given the step’s prior state, so a process pool over rows divides a step’s wall time
  by about 0.8 times the cores, at the cost of pickling the partner covers once per
  step. A parallel branch and bound must keep the certificate’s invariant that a parent’s
  record precedes its children’s chunk, which the verifier’s chunk-ordered node pass
  relies on; a central id counter with buffered flushing does it.
- **python-flint.** Measured at 2 to 4 (sections 2.1 and 2.2), below gmpy2 on the same
  code; not worth a second dependency.

## 4. Soundness and the Standing Verifiers

**Producer.** Nothing it computes is evidence, so floats, caches, grids, snapped cores
and parallel rows are all admissible; the checker is the gate, as now.

**Checker.** Safe: an exact arithmetic backend swap (gmpy2’s `mpq` and `mpz`, or the
homogeneous-integer form the collision step already uses), memoisation of pure exact
functions (facet sets by core pair, domain minima by partner row), the indexed sweep in
`--check-saved` in place of the reference sweep (the frozen n11 record states they prove
the same cover and report the same events), and row-level parallelism.
Not safe: any float test that decides to skip an inequality, and any value taken from
the producer rather than re-derived.
Every checker change is a new digest in the receipts’ `kernel_sha256`, so the admitted
saved objects are re-checked (W7’s 27 minutes become about 8 after step 3) and the n11
method controls re-run; that is cheap once and expensive across a thousand certificates,
so the checker is frozen before the batch and only the producer moves afterwards.

**Verifiers.** The independence rule is that a verifier imports nothing from
`sqpack.hull_kernel`, the checker tool, the selector or the branch and bound, and
re-derives everything from the cells and the objects.
The same optimisations apply, written separately: an integer facet check by edge merge
(a different algorithm from the checker’s hull, so the two must agree on every facet), a
sweep of its own, a cut cache.
Two consequences for compiled code:

- A Rust verifier shares no geometry crate with a Rust checker; it may share the
  big-integer dependency, as the two Python verifiers share CPython’s `int` and
  `fractions`, and that choice should be written down in the ledger’s `verifiers:` entry
  rather than left implicit.
- Arithmetic diversity costs nothing and buys a check on the library: if the checker
  moves to GMP (gmpy2 or `rug`), leave the verifiers on CPython’s integers, so no single
  arithmetic implementation underlies both sides of an admission.

A new verifier is a new digest in the ledger’s `verifiers:` list; admitted entries’
receipts stay valid under the old digest, so verifier work never forces re-verification,
unlike checker work.
A compiled verifier needs `sqverify_exact`’s pinning (`rust-toolchain.toml`,
`Cargo.lock`, the binary’s SHA-256 in every receipt, `check_exact_rust_kernel.py`’s
reproducibility check) before its digest can be listed.

## 5. The Ranked Plan

Per-certificate costs are CPU-seconds for a W7-sized kernel certificate (today 6,026)
and an A-sized branch-and-bound certificate (today 2,094), each step applied on top of
the ones above it. Gains marked *m* are measured in section 2 on the component they name
and combined by the shares of section 1; *e* are estimated.

| Rank | Step | Build | Gain on its tool | Kernel: P + C + V | Branch and bound: P + V | Soundness and verifiers |
| ---: | --- | ---: | --- | ---: | ---: | --- |
| 1 | Kernel verifier, in CPython integers with no new dependency: facets in homogeneous integers by edge merge with the facet and minimum caches (*m* 23 × 1.85 on a sixth), a sweep of its own in place of area subtraction (*m* 5.2 for the sweep; *e* 3–5 more for homogeneous integers over `Fraction`, by analogy with the collision measurement), partner cores proved once per owner step rather than per step | 2–3 days, then re-verify W7 (about 10 min) | verifier 5–13; 8.5 used below | 838 + 930 + 500 = 2,270 | — | obligations unchanged; new verifier digest; W7’s old receipt stays valid |
| 2 | Branch-and-bound verifier: cache the validated cut minimum per round (*m* 5.1 fewer C2 checks → 2.2), rebind to gmpy2 `mpq` (*m* 4.7) | 1 day, then re-verify A (about 5 min) | verifier 6–8 (*m*, *e* for the product) | — | 544 + 220 = 764 | as above; the branch-and-bound producer uses floats and HiGHS, so GMP on its verifier shares nothing with it |
| 3 | Kernel checker and producer: gmpy2 `mpq` and `mpz` throughout `sqpack.hull_kernel` (*m* 2.9 on the checker as a drop-in, 3.9 on the sweep alone), the facet cache in the checker (*m* 1.85 on 11%), the indexed sweep in `--check-saved` (*m* 5.2 on the fresh-process check); the kernel verifier stays on CPython integers (section 4) | 2 days: `uv add gmpy2` pinned, the rebinding, the n11 method controls, re-check W7 | checker 3–3.5, producer 4–5 (*e* from the checker’s 2.9 and the sweep’s share) | 200 + 280 + 500 = 980 | — | checker digest changes once; freeze after this step |
| 4 | Producer: snap cores to the $2^{-24}$ grid; row-parallel producer, checker and verifier for wall time | 2 days | 1.2–1.5 (*e*) on all three; wall ÷ cores | about 750 | — | producer-only; parallel rows change no obligation |
| 5 | Rust exact-geometry crate for the checker’s collision and sweep (and the producer’s, which may share it), batched per step behind the resident protocol, differential-tested against the Python checker; the kernel verifier may then take gmpy2 (*m* 4.7 on its remaining `Fraction` parts, 1.46 on integers), since it no longer shares arithmetic with the checker | 2–4 weeks | checker and producer 5–10 (*e*; *m* floor 2.3); verifier about 2 | 80 + 80 + 250 = 410 | — | the Python checker remains the reference; the crate is pinned and its digest recorded |
| 6 | A separate Rust verifier crate | 2–4 weeks | verifier 3–5 (*e*) | about 260 | — | no shared geometry code with step 5, and a different integer library from it; listed in `verifiers:` with its pinning |
| 7 | Branch-and-bound producer: interval arithmetic and pair terms in Rust (`highs-sys`) or vectorised; `clip_to_box` on `mpq` | 1–2 weeks | at most 2.4 (*m* HiGHS floor) | — | 280 + 220 = 500 | producer-only |
| 8 | Certificate I/O: one chunk pass in the branch-and-bound verifier; fewer, larger chunks | 1 day | about 2 on a share that is 4% today and 25% after step 2 | — | about 450 | format unchanged |

Steps 1 to 4 are the near-term gain: 6 times on a kernel certificate after step 3 and 8
after step 4, 2.7 on a branch-and-bound one, in about two weeks.
Step 5 is where the kernel reaches 15 times, and 23 with step 6; neither is on the
critical path until the count and size levers have been measured, since a Rust kernel
built for 64-row envelope cores would be rebuilt for F1’s octagon.

## 6. The Total

**Rate alone, under the current cost model.** Every exact-arithmetic term of the residue
process review’s revised model (the flags, Q1’s classes, the per-state tail, the
near-endpoint states, the capture, re-verification) carries the per-certificate factors
above; the float search terms (stage 2, about 180 CPU-hours; F1’s sweep, 35) do not.
The per-state tail, the near-endpoint states and the capture are kernel work, and the
classes are routed by structure, so the mix is about nine tenths kernel by CPU. Steps 1
to 4 give 8 on a kernel unit and 2.7 on a branch-and-bound unit, about 7 blended; steps
5 and 6 give 15 to 23 on a kernel unit and, with step 7, 4.2 on a branch-and-bound unit,
about 15 blended. So $4\times10^{3}$ to $4\times10^{4}$ CPU-hours becomes about 750 to
6,100 with the Python-level steps and about 450 to 2,800 compiled, the branch and
bound’s HiGHS floor being what holds the compiled figure up.
Re-verification after a checker change falls from 1,000 to 3,000 CPU-hours per change to
100 to 300, and the point stands that there should be no such change after step 3.
Hundreds of CPU-hours is reached by rate alone only at the low end of the model’s count.

**Multiplied into F1’s plan.** F1’s arithmetic (its section 6) is 90 flags at 50 to 250
CPU-hours, the sweep at 35, 40 to 120 class certificates at 20 to 360, a tail of 200
orbits at 400, and the capture at 100 to 400: 600 to 1,450 in all, of which 35 is float
search. Dividing the exact terms by 7 gives 120 to 245 CPU-hours with steps 1 to 4, and
by 15 gives 75 to 130 compiled.
F1’s size lever at 32 rows is a twofold cut on the measured split (section 2.4), which
F1 counts as fourfold, so its class and tail terms read twice as large here: the
corrected plan is 1,025 to 2,205 before the rate, 185 to 360 with steps 1 to 4 and 100
to 180 compiled. F1’s falsified case, a per-state tail of a thousand orbits at 5 to 15
CPU-hours each at today’s size, is 5,000 to 15,000 today, 750 to 2,240 with steps 1 to 4
and 330 to 1,000 compiled.
So the two reviews compose as F1 says they do: count and size take the model to about
$10^{3}$, the Python-level rate steps take that to hundreds when the tail is short, and
with a tail of a thousand the compiled steps bring it to the high hundreds at the
model’s low unit cost and not otherwise.

**What decides the order.** Steps 1 to 3 pay whatever F1’s measurements show, since
every certificate is verified; step 5 is worth starting only after W7 has been re-run
with the octagon core at 32 and 16 rows (F1’s rank 1), because the core’s shape sets the
facet count and the row count sets the batch, and both change what the crate should be
built for.

## Evidence Status

| Kind | Items |
| --- | --- |
| Measured from the receipts | the per-certificate costs of W7 and A and their shares; the stall costs; the per-row costs at 32 and 64 rows; the counts of rows, regions, pairs, facets, cuts, bounds and references |
| Measured here, planning evidence | the five profiles and their shares; the collision, cover and load micro-benchmarks; the `mpq` drop-in trials; the Rust `num-bigint` comparison; the cut-reference ratio |
| Extrapolated from a sample | the kernel verifier’s full-run split (four fifths cover, a sixth collision) |
| Estimated | the composed per-certificate costs in section 5; an integer sweep’s gain over `Fraction` (3 to 5); the compiled gains (5 to 10 on integers, 10 to 20 on the sweep); operand shrinking at 1.2 to 1.5; the totals in section 6 |
| Derived here, needing review | the independence and diversity rules for compiled verifiers; the claim that the sweep is linear in rows and only the collision share quadratic; the freeze-before-batch rule |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
