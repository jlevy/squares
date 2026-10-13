# Research: Exact Arithmetic and Verifier Performance

**Date:** 2026-09-30

**Author:** Codex (Astra mathematical and source review; Sol profiling), for the squares
project

**Status:** Complete: source survey, mathematical review, reduction ablation, and
bounded verifier comparison.
Alternative libraries and a full external certificate replay remain unmeasured;
production defaults are unchanged.

**Tracking:** `think-i5x7` and `think-ss4a`, under `think-3cwg`.

## Overview

The present Rust rectangle-density kernel is slower than the Python path in the retained
matched runs.
That is a fact about these implementations and workloads, not evidence that
exact verification in Rust is inherently slow.
Both implementations spend much of their work below the language interpreter, in
arbitrary-precision integer arithmetic.
Their libraries use different rational-reduction and greatest-common-divisor algorithms,
and the Rust boundary also performs work that the internal Python path does not.

Source inspection identifies a specific, testable inefficiency: the pinned Rust rational
library cross-cancels a multiplication and then passes the result through a general
reducing constructor.
For canonical inputs, the product is already reduced.
The Python implementation exploits that invariant.
A bounded operating-system sample places most sampled query stacks in Rust’s coverage
arithmetic, with GCD, shifts, subtraction, and allocation prominent.
This identified an arithmetic experiment; the sample alone cannot assign a speedup.

The controlled multiplication ablation now supplies that measurement.
On the fixed 128-polygon workload, omitting the final reduction lowered median Rust
child CPU from 0.555 to 0.483 seconds, **12.9%**, with exact agreement in every pair.
Python’s production coverage path still used less CPU on that workload.
The result isolates one avoidable cost.
A subsequent paired verifier experiment found 14.5% lower Rust child CPU and 17.9% lower
median invocation wall time on the retained external 1,000-node workload, with identical
exact reports. That capped workload remains inconclusive; production defaults are
unchanged.
GMP-backed Rust and Python arithmetic, pure-Rust alternatives, and homogeneous
integer geometry remain unmeasured options for this kernel.

This work concerns the separate rectangle-density verifier.
The independently confirmed $n = 11$ optimality result, T-060, is already complete; its
[whole-proof review](../reviews/review-2026-09-29-n11-optimality-census-contract.md#whole-proof-acceptance)
does not depend on this performance investigation.
Completing or accelerating the native rectangle pipeline is a different obligation.

## Questions to Answer

1. What do the Python and Rust paths actually compute, and which costs are comparable?
2. Which arithmetic differences are established by pinned source or measurement?
3. Which representation, library, and bridge choices preserve the verifier’s exact
   contract, and what is the smallest experiment that can distinguish them?

## Scope

The subject is the exact weighted intersection-area primitive in
[`sqverify_exact`](../../../packing/sqverify_exact/src/lib.rs), its
[Python reference](../../../packing/src/sqpack/rectangle_density.py), and the
[resident-process adapter](../../../packing/src/sqpack/rust_rectangle_geometry.py).
The survey covers rational arithmetic over arbitrary-precision integers, GMP and FLINT
bindings, pure-Rust alternatives, delayed normalization, homogeneous coordinates, and
certified filters.

It does not re-run the accepted T-060 proof, complete the external rectangle
certificate, replace its box bound, or establish a library speed ranking.
Current ecosystem versions below are a dated survey, not a recommendation to float
production dependencies.

## Findings

### The Geometry Contract Comes Before the Language Choice

For an admitted polygon $P$, the kernel returns the exact rational value

$$
F(P)=\sum_j \rho_j\thinspace\operatorname{area}(P\cap R_j),
\qquad \rho_j\geq 0,
$$

where each $R_j$ is an axis-aligned rectangle with rational coordinates.
Each intersection uses four half-plane clips followed by the shoelace area formula.
Both paths already skip rectangles whose bounding boxes have no positive-area overlap
with the polygon.

The Python coordinator owns candidate admission, angle and center-box subdivision,
lower-bound selection, and the final verification decisions.
Rust replaces the area queries, not that whole program.
For example, if a polygon lies inside every square represented by a center box,
nonnegative density makes its mass a valid lower bound for every one of those squares.
Improving this lower-bound polygon can reduce the number of boxes; accelerating its
integral can reduce the cost per box.
Those are separate changes.

An empty polygon, point, or segment has zero area here.
A rectangle touching the polygon only along a boundary also contributes zero area.
These facts justify the existing area shortcuts.
They do not justify discarding points or segments in a closed-set coverage proof such as
T-060 capture. Reusing an optimization across those two contracts requires a new
argument.

The current Rust path uses `BigRational` from `num-rational = 0.4.2`, backed by
`num-bigint = 0.4.6`; the Python path uses CPython 3.14.7 `Fraction`. The
[Cargo manifest](../../../packing/sqverify_exact/Cargo.toml) already enables release
optimization, thin LTO, and one code-generation unit.
This is not a comparison against an accidentally unoptimized Rust debug build.

### What the Retained Measurements Establish

The [matched backend receipt][matched] binds the input, sources, release binary, exact
normalized reports, and timings:

| Workload | Exact outcome in both paths | Python wall | Rust wall | Rust child CPU |
| --- | --- | ---: | ---: | ---: |
| Analytic $n = 3$, all 201 angles, 1,781 nodes | `VERIFIED`; reports identical | 0.504 s | 3.800 s | 1.044 s |
| External $n = 11$, angle 1, fixed 1,000 nodes | `INCONCLUSIVE`; reports identical | 13.252 s | 24.085 s | 10.889 s |

Wall time includes admission, child startup, communication, computation, and shutdown.
The receipt does not record Python process CPU; its zero *child* CPU means that Python
did not launch a child, not that its computation was free.
These observations establish the reported outcomes and elapsed times.
They do not isolate arithmetic throughput or give a stable Rust/Python speed ratio under
other host loads.

The [transport experiment][transport] held 128 four-vertex queries and their exact
values fixed, comparing singleton messages with a batch in three alternating pairs.
They are angle-1 squares on a deterministic 16-by-8 center grid, rather than a trace of
every common-core polygon generated by a verifier traversal.
The median batch/singleton query-wall ratio was **0.9924**, with a range of
**0.9854–0.9959**. It missed the preregistered requirement of at most 0.75 in every
pair. Child CPU was about 0.543–0.548 seconds; coordinator CPU was about 0.006–0.009
seconds. Batching messages did not materially improve that query workload.
Startup can still matter for short sessions, and this experiment alone does not
distinguish parsing, validation, and arithmetic inside the child.

The later [OS sampling receipt][sample] retains the unchanged binary identity, 184
density rectangles, 128 polygons, raw sample hash, and
[compressed raw sample](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/rust-exact-os-sample-2026-09-30.txt.gz).
Of 538 samples under `query_session`, 524 occurred in the coverage branch and 12 in the
polygon-parsing branch.
Top-of-stack counts included 181 for `BigUint::gcd`, 84 for a right shift, and 81 for
subtraction. These are nested sampling observations, not additive CPU percentages or
invocation counts. They point to arithmetic as the useful next target on this workload;
convexity validation appears secondary in this sample.

The child lived for roughly 0.74 seconds, less than the requested two-second sampling
window. Startup stacks and sampling perturbation prevent a calibrated cost allocation.
Use the unsampled transport receipt for its ratios, not the sampled run.
In particular, the sample cannot say how much time a removed GCD, a different GCD
algorithm, or fewer allocations would save.

### Runtime Cost and Investigation Cost Are Different Records

The measurements above concern seconds of program execution.
Reading library source, reviewing arithmetic invariants, designing controls, and writing
this report consume agent and human elapsed time outside those measurements.
No token cost or total research labor is inferred from a child CPU receipt.

The earlier [infrastructure report][older-report] called some computations effectively
free beside a model turn.
That was an interactive-latency judgment about particular small operations.
It does not make cumulative verification, repeated failed experiments, or the work of
investigating them free.
Retain separate accounts for execution cost, coordination and analysis time, and any
actually recorded service usage.

### Python Already Calls Native Integer Arithmetic

CPython’s `Fraction` methods are Python code, but their integer arithmetic and
`math.gcd` execute in C. In 3.14.7, multiplication and division cross-cancel, then use
an internal constructor for coprime integers instead of reducing again.
Addition has a denominator-GCD optimization.
See the pinned
[`fractions.py`](https://raw.githubusercontent.com/python/cpython/v3.14.7/Lib/fractions.py).

The two-integer `math.gcd` fast path calls `_PyLong_GCD`, whose large-integer path uses
Lehmer-style quotient batching with a Euclidean fallback.
CPython is not using GMP here.
See the pinned
[`mathmodule.c`](https://raw.githubusercontent.com/python/cpython/v3.14.7/Modules/mathmodule.c)
and
[`longobject.c`](https://raw.githubusercontent.com/python/cpython/v3.14.7/Objects/longobject.c).

The pinned `num-bigint` GCD instead uses a binary/Stein algorithm: shifts, subtraction,
and comparisons on integer magnitudes.
Its integer magnitude uses a vector, and cloning that magnitude clones the storage.
These are source differences, not a measured ranking of the algorithms on our operand
distribution. See
[`num-bigint 0.4.6`](https://raw.githubusercontent.com/rust-num/num-bigint/num-bigint-0.4.6/src/biguint.rs).

Consequently, moving a Python expression into Rust can remove interpreter work while
adding more or more expensive native arithmetic.
A language-level expectation cannot decide the net result.

### Why the Last Multiplication Reduction Can Be Omitted

A rational is stored as two integers.
Normalization replaces representations such as $6/8$ with $3/4$ by dividing numerator
and denominator by their greatest common divisor.
It also fixes the denominator’s sign.
Repeating this work after every arithmetic expression can be costly when those integers
grow; proving that a particular result is already reduced avoids work without changing
precision.

Use the private invariant

$$
\frac ab,\frac cd\in\mathbb Q,\qquad
b,d>0,\quad \gcd(|a|,b)=\gcd(|c|,d)=1.
$$

Set $g_1=\gcd(|a|,d)$ and $g_2=\gcd(|c|,b)$. Then

$$
\frac ab\frac cd=
\frac{(a/g_1)(c/g_2)}{(b/g_2)(d/g_1)}.
$$

The two numerator factors are each coprime to each denominator factor.
Two of the four coprimality statements follow from the original canonical fractions; the
other two follow from removing the full cross-GCDs.
Thus the displayed numerator and denominator are coprime already, and the denominator is
positive. A subsequent general GCD cannot cancel anything.

Zero is included: canonical zero is $0/1$. Multiplying it by $c/d$ gives $g_1=d$ and
$g_2=1$, hence exactly $0/1$. Division has the same argument after taking the reciprocal
of a nonzero divisor and restoring a positive denominator.
This is an invariant proof, not permission to skip reduction on arbitrary integer pairs.

In `num-rational 0.4.2`, the general multiplication/division paths cross-cancel and then
call `Ratio::new`, which ordinarily reduces again; there are special-case shortcuts.
Borrowed binary operators also forward through cloned operands.
Its public `new_raw` constructor permits noncanonical representations, so the library
must support a broader input contract than this private kernel.
The surplus reduction for *our canonical inputs* is not a general library correctness
bug. The same source also contains denominator-LCM addition and overflow-avoiding
recursive rational comparisons.
See the
[pinned implementation](https://raw.githubusercontent.com/rust-num/num-rational/num-rational-0.4.2/src/lib.rs).

The safe experiment changes only a private operation whose inputs satisfy the invariant.
It must not replace every `Ratio::new` with `new_raw`, weaken input parsing, or allow
unreduced raw values to enter later canonical operations.
A normalized constructor at admission and invariant-preserving operations form an
inductive argument for every intermediate result.

Addition offers a separate possible optimization.
Let

$$
g=\gcd(b,d),\qquad t=a(d/g)+c(b/g),\qquad h=\gcd(|t|,g).
$$

Then the reduced sum is

$$
\frac{t/h}{(b/g)(d/h)}.
$$

To see why only $g$ can contribute a common factor, write $b=gb'$ and $d=gd'$ with
$\gcd(b',d')=1$. The integer $t=ad'+cb'$ is coprime to both $b'$ and $d'$ by the
canonical input assumptions.
Only the shared denominator factor $g$ remains to cancel.
This justifies the formula, but changing addition together with multiplication would
confound the reduction experiment below.
Addition and division were left unchanged.

### Measured: Removing the Final Multiplication Reduction

The [arithmetic A/B receipt][arithmetic-ab] was produced by the reusable benchmark’s
`--build-variants` path.
It built two release binaries from the same frozen source with Rust 1.98.0 on
`aarch64-apple-darwin`, the same dependency lock, and no added Rust flags.
Both helpers perform the same cross-cancellation and integer arithmetic.
One ends in `Ratio::new`; the other ends in `Ratio::new_raw`. The production expressions
remain under the default configuration, with both experimental features off.

The benchmark compared the same 128 polygons in three alternating Rust pairs and checked
every exact output against Python in each pair:

| Measured path | CPU median | CPU range | Median query or function wall |
| --- | ---: | ---: | ---: |
| Rust normalized helper, whole child | 0.554884 s | 0.553031–0.556015 s | 0.581953 s |
| Rust coprime helper, whole child | 0.483236 s | 0.480792–0.485800 s | 0.533755 s |
| Python production `_coverage_polygon`, process | 0.318475 s | 0.316500–0.319834 s | 0.341721 s |

The preregistered continuation criterion was a candidate CPU median at most 90% of the
normalized baseline’s median, with nonoverlapping ranges.
It passed. Candidate/baseline CPU ratios were 0.8694, 0.8755, and 0.8691; the reduction
in median CPU was **12.912%**. The default kernel was not switched to the experimental
helper.

The candidate’s accompanying [differential control run][coprime-controls] passed 210
polygon comparisons, 10 refusals, and two verifier controls: the complete analytic
fixture over all 201 angles, and external angle 1 capped at 100 nodes.
The latter remained inconclusive with the same normalized report as Python.
These are additional correctness checks, not a timed full-verifier performance
comparison.

This is evidence that eliminating the final reducing constructor saves work on this
workload. It is not a measurement of pure GCD time: child CPU includes startup, parsing,
convexity admission, clipping, allocation, area accumulation, and output.
The controlled baseline uses the new helper with reduction retained, so the experiment
isolates that constructor choice rather than claiming a paired speedup over the
historical production binary.
The older production receipt remains a separate observation.

The optimized child’s median CPU was still about **1.52 times** the Python process CPU.
Those paths return equal areas but retain the admission and ownership differences
described below. The result does not assign the remaining gap to binary versus Lehmer
GCD, establish a GMP advantage, or predict a full-verifier speedup.
It supports the next matched verifier control while leaving other arithmetic hypotheses
open.

The receipt binds `lib.rs` beginning `87e7c231`, benchmark `bff40e28`, normalized binary
`e0a006b5`, and coprime binary `d25afa57`; its full hashes and executed build commands
are retained. The two builds took 16.96 and 14.69 seconds separately.
Build time is reported setup cost, not part of the subsecond query measurements or an
estimate of agent labor.

### The Bounded Verifier Comparison Also Improves

The [follow-up receipt][verifier-ab] compares a freshly built default Rust binary with
the reviewed coprime binary through the existing Python verifier.
The [maintained benchmark][verifier-benchmark] runs three alternating pairs on each of
two fixtures: all 201 analytic angles, and external angle 1 capped at 1,000 nodes.
Every run must match the retained normalized report digest, including pending geometry.
This fixes the mathematical work rather than comparing elapsed time alone.

All twelve runs matched: the analytic fixture verified with 1,781 nodes, while the
external fixture remained inconclusive after 1,000 nodes.
No external certificate was accepted by this experiment.

| Fixture and metric | Default median | Coprime median | Reduction |
| --- | ---: | ---: | ---: |
| External Rust child CPU | 9.924059 s | 8.485798 s | 14.49% |
| External invocation wall | 11.742820 s | 9.646504 s | 17.85% |
| Analytic Rust child CPU | 0.876950 s | 0.669636 s | 23.64% |
| Analytic invocation wall | 1.572126 s | 1.359246 s | 13.54% |

The predeclared rule required at least 10% lower median external child CPU, separated
CPU ranges, and no more than 5% median wall regression on either fixture.
It passed. External CPU ranges were 9.909474–9.992796 seconds for default and
8.389309–8.632168 seconds for coprime.
Wall measurements were noisier: paired external wall ratios were 0.837, 0.802, and
0.971, and their ranges overlapped.
The 17.85% figure is a median observation, not a guaranteed wall-time improvement.

This comparison measures the whole default-versus-specialized implementation change;
unlike the preceding normalized-helper ablation, it does not isolate only the final
constructor. It supports a reviewed production-adoption decision for this kernel, not a
prediction about other certificates, a Python speed comparison, or complete external
verification. The default remains unchanged in this report’s accompanying code.

The twelve invocation walls sum to 75.04 seconds, separate from the 6.43-second default
release build. The receipt records coordinator CPU, child CPU, verification wall, and
invocation wall for every run.
Two earlier setup attempts produced no timed verifier trials: one used an incorrect
Python module entrypoint, and one refused a different build-feature artifact identity.
The corrected build and source identities were recorded before timing; the failed setup
attempts are retained in `think-ss4a` rather than counted as trials.
Preparation and review consumed additional agent time that was not separately metered.

The benchmark source begins `ef07125f`, the receipt `8518e1a3`, the fresh default binary
`0a8714df`, and the coprime binary `d25afa57`. Both builds are joined to the same Rust
sources, compiler, and flags; only the intended feature selection differs.

### Equal Results Do Not Mean Equal Primitive Work

The two kernels implement the same clipping and area identities, yet source inspection
shows additional differences:

- Rust admits untrusted polygons by checking edge/vertex orientation pairs.
  The internal Python path receives polygons constructed by its own geometry routines
  and does not repeat this admission.
  Retain the external check; a separate validated internal type would need an explicit
  construction argument.
- An all-inside Python clip can return the original immutable tuple, and retained
  vertices can be shared.
  Rust’s corresponding `to_vec()` and point clones copy rational storage.
  Borrowed or reusable buffers are a possible independent optimization.
- Shoelace expressions have the same exact value but different intermediate expression
  grouping. Canonicalization cost depends on those intermediate numerators and
  denominators, not just on the final answer.
- General rational comparisons, reductions, and temporary ownership differ between the
  libraries. The sample does not separate their individual contributions.

These facts make a port a useful correctness boundary without making it an automatic
performance improvement.
They also explain why an arithmetic microbenchmark, an exact kernel benchmark, and an
end-to-end verifier benchmark answer different questions.

### Upstream C++ and Stronger Bounds Are Separate Comparisons

The retained [tooling overview](../guides/verification-tooling.md) records that the
upstream C++ verifier uses outward-rounded binary64 interval arithmetic and different
box bounds. It is not the same arbitrary-precision rational computation written in
another language. Its smaller traversal and cheaper operations can both matter.
A complete upstream run versus a capped, inconclusive independent run is not a matched
throughput comparison.

Cutoffs also belong to the mathematical input.
The nominal $1.0001$, the exact rational $10001/10000$, and the effective binary64 value
$2252024993666617/2251799813685248$ are distinct.
Any comparison must preserve the actual cutoff, angular range, node budget, subdivision
order, and box-bound choice.

The [retained derivative diagnostic][derivative] evaluated all 13 pending boxes from a
fresh fixed-work frontier.
It closed **zero additional boxes**: the derivative bound was below the common-core
bound on every box, so their maximum was unchanged.
Seven queued boxes were already closable by the common-core bound; they were not
derivative gains. The approximately 1.16-second preflight-plus-diagnostic result met its
time budget but missed the preregistered new-closure criterion.
This result does not justify a production or Rust derivative implementation.
A bound change needs evidence of less verification work; a primitive change needs
evidence of cheaper equal work.

## Arithmetic Libraries and Bridges

The following is an option inventory, not a speed ranking.
Versions were checked against official documentation, release records, or tagged source
on 2026-09-30. The deployed baseline remains the pinned versions above.

| Option | Exact rational implementation | Why it is relevant here | Dependency or contract consequence |
| --- | --- | --- | --- |
| CPython 3.14.7 `Fraction` | Python rational operations over C integers and GCD | Existing independent reference; efficient canonical formulas already present | No new arithmetic dependency; preserve its exact input semantics |
| `num-rational 0.4.2` / `num-bigint 0.4.6` | Pure-Rust general ratio over big integers | Current baseline; narrow normalization and ownership experiments are possible | MIT/Apache-2.0 dual-licensed crates; current pins are older than the surveyed bigint release |
| Rug 1.30.0 / `gmp-mpfr-sys 1.7.1` | GMP rational arithmetic through a Rust interface | Direct native alternative without moving the geometry back to Python | LGPL-3.0-or-later wrappers and a C build; select only needed features |
| gmpy2 2.3.1 `mpq` | GMP rationals exposed to Python | Tests a native integer/rational engine while retaining Python geometry orchestration | LGPL-3.0-or-later; explicit adapter needed, not a silent `Fraction` substitution |
| python-flint 0.9.0 `fmpq` | FLINT exact rationals, with GMP-backed large integers | Useful if the same work also needs polynomial or algebraic operations | MIT wrapper, LGPL-3.0-or-later FLINT; wrapper license does not replace native-library licenses |
| Malachite 0.12.0 `Rational` | Pure-Rust canonical rationals and integer algorithms | Alternative normalization, integer algorithms, and small-value representation | LGPL-3.0; API explicitly still evolving |
| dashu-ratio 0.6.0 `RBig` / `Relaxed` | Pure-Rust fully reduced or partially reduced rationals | A ready comparison of normalization policies | MIT/Apache-2.0; relaxed values need their own representation invariant |

The pinned num crate licenses and dependency relationship are recorded in
[`num-rational`’s manifest](https://raw.githubusercontent.com/rust-num/num-rational/num-rational-0.4.2/Cargo.toml)
and
[`num-bigint`’s manifest](https://raw.githubusercontent.com/rust-num/num-bigint/num-bigint-0.4.6/Cargo.toml).
The option-specific sources and limits follow.

### A Newer Pure-Rust Integer Version Is Its Own Experiment

The surveyed `num-bigint` documentation is at 0.5.1. Its release history records inline
single-digit storage and Burnikel–Ziegler division in 0.4.7, followed by a division
regression fix in 0.5.1. Those changes make an upgrade worth evaluating, not
automatically faster or interchangeable.
`num-rational 0.4.2` depends on the 0.4 bigint series, so adding a separate 0.5
dependency does not change the backing type of its `BigRational` alias.
Check the resolved graph and relevant fixes before selecting an upgrade arm.
See the
[release history](https://raw.githubusercontent.com/rust-num/num-bigint/num-bigint-0.5.1/RELEASES.md)
and [current API](https://docs.rs/num-bigint/0.5.1/num_bigint/).

### GMP Through Rust or Python

Rug provides GMP-backed `Integer` and `Rational`. Its borrowed operations can produce
incomplete-computation values that are assigned into existing storage; using that API
carefully can avoid unnecessary temporaries.
Its rational feature requires integers but does not require enabling floating-point or
complex arithmetic. A geometry port must preserve exact numerator/denominator conversion
at the boundary. These are API options, not measured gains in this project.
See [Rug 1.30.0](https://docs.rs/rug/1.30.0/rug/).

`gmp-mpfr-sys 1.7.1` bundles GMP 6.3.0, MPFR 4.2.2, and MPC 1.4.1, with the latter two
optional. Its documented build requirements include command-line developer tools on
macOS, a C toolchain and build utilities on Linux, and a GNU/MSYS2 route on Windows.
System-library and cross-compilation modes have explicit restrictions.
The build also supports a C-library cache; place it, Cargo targets, and temporary files
on the project’s external scratch volume.
Keep the native library tests enabled when establishing a new build.
See the [binding documentation](https://docs.rs/gmp-mpfr-sys/1.7.1/gmp_mpfr_sys/).

GMP’s manual describes binary, Lehmer, and subquadratic GCD families.
This establishes that “GMP” is not just another name for the pinned binary-GCD
implementation; it does not predict which path or crossover dominates our actual
operands. The manual also requires canonical rational operands for its rational
arithmetic, with special care after direct numerator/denominator mutation.
See [GCD algorithms](https://gmplib.org/manual/Greatest-Common-Divisor-Algorithms) and
[rational functions](https://gmplib.org/manual/Rational-Number-Functions).

gmpy2 exposes the same broad native-arithmetic option to Python through `mpz` and `mpq`.
The 2.3.1 release provides CPython 3.14 wheels, including macOS ARM64. That makes a
local comparison practical without establishing its speed.
Our verifier requires actual `Fraction` values at admission, so an experiment must
convert admitted exact pairs once at a geometry boundary and convert exact results back;
broadening public admission or mixing float conversions would change the experiment.
See the [official overview](https://gmpy2.readthedocs.io/en/latest/overview.html) and
[release metadata](https://pypi.org/project/gmpy2/2.3.1/).

GMP itself offers LGPL-3.0-or-later or GPL-2.0-or-later licensing choices; Rug and its
binding crate publish LGPL-3.0-or-later terms.
A distributed native binary or wheel must account for the actual linked libraries and
their license terms, not just this repository’s MIT code license.
This is a packaging decision to record for the selected build, not evidence for or
against its arithmetic speed.
See [GMP’s copying conditions](https://gmplib.org/manual/Copying).

### FLINT Is Relevant, but the Earlier Benchmark Is a Different Workload

python-flint exposes exact `fmpq` rationals as well as polynomial and other algebraic
types. FLINT’s `fmpz` uses an inline small-integer representation and GMP storage for
larger values. The Python wrapper is MIT-licensed; FLINT is LGPL-3.0-or-later.
See the [`fmpq` API](https://python-flint.readthedocs.io/en/latest/fmpq.html),
[integer representation](https://raw.githubusercontent.com/flintlib/flint/v3.4.0/doc/source/fmpz.rst),
[wrapper release and compatibility](https://github.com/flintlib/python-flint),
[wrapper license](https://raw.githubusercontent.com/flintlib/python-flint/0.9.0/LICENSE),
and [FLINT project](https://github.com/flintlib/flint).

The August infrastructure report measured large gains for polynomial arithmetic modulo a
number-field polynomial.
Rectangle clipping uses scalar rational coordinates and area accumulation.
Neither those old ratios nor a claim to use FLINT in every arithmetic loop establishes a
scalar clipping speedup.
FLINT deserves a matched arm if it simplifies shared arithmetic needs; a GMP rational
arm is the more direct initial comparison for this particular primitive.

### Other Pure-Rust Representations

Malachite provides canonical rationals and integer algorithms derived in part from GMP
and FLINT. Its documented small-value representation keeps a rational inline when both
components fit its limb-sized limits.
Its public API remains under development, and its license is LGPL-3.0. These facts
justify considering it without assuming that avoiding a C dependency makes it slower or
faster. See the [project documentation](https://www.malachite.rs/) and
[rational API mapping](https://www.malachite.rs/mapping/num-rationals/).

Dashu distinguishes fully reduced `RBig` from `Relaxed`, whose normalization removes
common powers of two without requiring full reduction.
That is a useful explicit model for delaying GCD work.
It can also permit larger intermediate numerators and denominators; conversion,
comparison, equality, and output normalization must respect the chosen type.
Its documentation itself calls for benchmarking the choice.
See [dashu-ratio 0.6.0](https://docs.rs/dashu-ratio/latest/dashu_ratio/) and
[crate metadata and license](https://docs.rs/crate/dashu/latest).

The sampled workload’s largest source integer component was 101 bits in Sol’s source
inspection. That says little about intermediate sizes after clipping and accumulation.
Measure their distribution before choosing a library on the basis of either small-value
storage or asymptotic large-integer algorithms.
In particular, the pinned Lehmer/Stein difference alone does not establish that it
explains the observed timing gap at these sizes.

## Representation and API Options

### Homogeneous Integers Can Remove Many Local Divisions

Represent a point by integers $(X,Y,Z)$ with $Z>0$, meaning $(X/Z,Y/Z)$. An axis cut
$x\geq p/q$, with $q>0$, becomes the integer sign test

$$
qX-pZ\geq 0.
$$

Orientation is the sign of the determinant of three homogeneous points, because the
product of their denominators is positive.
An edge line is a cross product of its endpoint triples; intersecting it with the cut
line is another cross product.
For a genuine finite crossing, choose the sign of the resulting triple to keep $Z>0$.
Parallel lines, coincident endpoints, and boundary ties still require explicit exact
handling.

This can postpone normalization during clipping and orientation checks.
It does not eliminate rational area accumulation:

$$
2A=\left|\sum_i
\frac{X_iY_{i+1}-Y_iX_{i+1}}{Z_iZ_{i+1}}
\right|.
$$

Unreduced coordinates can grow substantially.
A complete design must choose where to normalize, how to compare equivalent triples, and
how to bound intermediate resource use.
A single fixed denominator for all points is not automatically preserved: line
intersections introduce new divisors.
Checked machine-integer fast paths with arbitrary- precision fallback are another
possibility; unchecked overflow is not.

This reasoning is consistent with the homogeneous-coordinate distinction in
[CGAL’s kernel manual](https://doc.cgal.org/latest/Kernel_23/index.html).
The repository’s accepted integer collision helper uses a related technique for a
different family of predicates.
Its prior speed measurements cannot be transferred to this clipping-and-area kernel.

### Certified Filters Need a Different Decision Contract

A rigorous enclosure $[L,U]$ of an exact value $F$ can certify $F\geq T$ when $L\geq T$
and $F<T$ when $U<T$. Otherwise, refine the enclosure or use an exact fallback.
Equality must remain covered by that policy.
A rounded floating-point estimate with an arbitrary epsilon is not such an enclosure.

Every source conversion and operation contributing to the enclosure needs a sound error
bound or directed rounding.
Overflow, underflow, NaNs, and compiler contraction rules belong to that argument.
MPFR supplies explicitly controlled rounding operations, while CGAL’s lazy exact number
design combines interval approximations with deferred exact evaluation.
Neither fact makes an arbitrary floating-point geometry routine certified.
See the [MPFR manual](https://www.mpfr.org/mpfr-current/mpfr.html) and
[CGAL lazy exact numbers](https://doc.cgal.org/latest/Number_types/classCGAL_1_1Lazy__exact__nt.html).

There are two distinct applications here.
An exact sign predicate may use a filter and fall back when ambiguous while leaving
constructed coordinates exact.
Alternatively, a new area-bound backend could return certified lower and upper bounds.
The existing API returns the *exact integral as a rational*, so returning a safe lower
bound in that field would still violate its contract.
A bound backend requires an explicit result type and reviewed caller logic.

The coordinator often needs only a lower bound that reaches the cutoff, so an exact
integral may supply more information than that decision requires.
A certified bound API could exploit this, falling back to exact evaluation when
inconclusive. That is a substantive design option, but its reports and proof obligations
differ from an equal-output arithmetic substitution.

Likewise, exact orientation predicates alone do not make rounded intersection vertices
or shoelace areas exact.
A scalar-generic formula is useful organization, but an interval sign result has an
“undetermined” case, and approximate constructions have a different contract.
Sharing syntax does not discharge those proof obligations.
Separate reference and optimized implementations can be valuable independent checks when
their common mathematical specification and limits are explicit.

### A Native Bridge Changes More Than Call Overhead

The current resident process amortizes table loading and provides a killable boundary
for timeouts or malformed responses.
The adapter checks binary identity, request sequence, table identity, output structure,
and exact rational results.
A library swap inside that boundary can preserve these properties while testing
arithmetic alone.

An in-process Rust extension could remove process startup and JSON communication, using
[PyO3](https://pyo3.rs/v0.29.0/) and [Maturin](https://www.maturin.rs/) for bindings and
packaging.
It would also move failure containment, cancellation, interpreter integration,
and platform-wheel work into that extension.
The fixed-work batching result gives little reason to make this the first throughput
experiment. If introduced, pass an admitted polygon batch across the boundary, not each
individual rational operation.

Rug is a high-level Rust interface over native libraries; using it would still be a
native verifier, with a larger arithmetic dependency.
Conversely, Python driving GMP through gmpy2 is already native arithmetic.
Rust’s `unsafe_code = "deny"` on our own crate does not establish that every dependency
or FFI implementation contains no unsafe code.

A Rug-versus-gmpy2 agreement would compare geometry and bridges but share GMP
arithmetic. Keep the CPython reference and analytic controls when claiming independent
arithmetic cross-checks.
Record the exact dependency graph, features, compiler settings, linked libraries, and
source/binary identities for each measured arm.

## Recommendations

First, use the successful fixed-node verifier comparison to review adoption of the
canonical multiplication helper.
The measured benefit passes the predeclared continuation rule, while production
geometry, subdivision, protocol, and input admission remain unchanged.
Retain the exact differential and refusal controls when changing the default.
Neither experiment completes the external certificate or establishes native speed parity
with the upstream verifier.

Second, collect representative operand sizes and operation counts in a separate
diagnostic build.
If GCD or allocation remains costly, compare one alternative arithmetic
engine on the exact same kernel workload.
Rug and gmpy2 offer a useful pair because they separate geometry/bridge costs while
sharing GMP; Malachite or Dashu provides a distinct pure-Rust arm if its dependency
tradeoffs fit the project.
Keep these library comparisons separate from the completed final-reduction ablation.

Third, preserve the existing exact interface for this sequence.
Consider homogeneous clipping or certified area bounds only when the measurements
justify their larger implementation and review cost.
The negative derivative diagnostic provides no present reason to adopt that bound, and
the upstream interval verifier is not a drop-in exact arithmetic replacement.

## Next Steps: Separate Adoption From Further Diagnosis

The reduction question and the bounded verifier comparison now have positive results.
The 100-node correctness comparison and the timed 1,000-node comparison both preserve
the exact reports; the complete analytic fixture also passes.
A capped external run still earns no complete-certificate credit, regardless of its
elapsed time.

For adoption and subsequent comparisons, preserve the frozen binary/source identities,
node and angle limits, exact cutoff, subdivision order, bound choice, and performance
criterion.
Keep alternating pairs and separate wall, coordinator CPU, and child CPU. Keep
source/protocol refusals, deadline behavior, tangency and degenerate-area controls, and
canonical numerator/denominator assertions.
A timeout remains incomplete.

To diagnose the residual cost, collect representative operand sizes and operation counts
in a separate instrumented build, outside timing runs.
Then choose one experiment: change the integer/rational engine while keeping formulas
and geometry fixed, or change one ownership/normalization policy while keeping the
engine fixed. A primitive trace would distinguish GCD-engine cost from how often the
rational layer calls it.
A homogeneous geometry or new bound implementation changes more and should be evaluated
as its own hypothesis.

Python comparison arms must continue to use the bounding-box-pruned `_coverage_polygon`
reference.
The completed A/B does so; timing a naive sum over all rectangles would charge
Python for work its deployed implementation avoids.
Preserve the same input bytes, query values, and build provenance in every library arm.
Record negative results, and report fewer nodes separately from cheaper equal work.

## Methodology and Evidence Limits

This report combines source inspection, official documentation, an independent algebraic
invariant argument, and retained measurements.
It runs no new geometry proof.
The matched and transport receipts pin the baseline `lib.rs` digest beginning
`07fc7c68`, release binary `407021f0`, and candidate `8e3339ee`; the receipts contain
the full identities.
The OS sample uses that same binary.
The later kernel and bounded-verifier comparisons have their own build and source
bindings and passed their respective diagnostic continuation criteria.
Source changes or new library versions need new measurements rather than relabeling the
historical receipts.

The report refreshes the scope of the older infrastructure recommendations without
discarding their original measurements.
Its floating-point separating-axis and number-field multiplication workloads remain
different from scalar exact rectangle clipping.
No blanket claim about Rust, Python, GMP, FLINT, or pure-Rust arithmetic follows from
any one of them.

## References and Retained Artifacts

- [Matched Python/Rust exact reports][matched]: result identities and bounded verifier
  timings.
- [Fixed-work transport diagnostic][transport]: three paired singleton/batch
  observations.
- [Rust child sampling receipt][sample]: source-bound stack observations and
  limitations.
- [Canonical multiplication A/B][arithmetic-ab]: executed build provenance, three paired
  exact comparisons, CPU ranges, and the passed diagnostic criterion.
- [Coprime-kernel differential controls][coprime-controls]: 210 polygons, 10 refusals,
  complete analytic verification, and the capped external verifier comparison.
- [Bounded verifier A/B][verifier-ab]: twelve exact report matches, paired CPU and wall
  measurements, and the passed bounded performance criterion.
- [Reusable bounded verifier benchmark][verifier-benchmark]: fixed workloads, source
  admission, and supervised paired execution.
- [Sampled transport run](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/rust-exact-os-sample-transport-2026-09-30.json):
  retained for provenance, not the unsampled timing baseline.
- [Derivative frontier diagnostic][derivative]: all 13 declared pending boxes, no new
  threshold closures.
- [Reusable transport benchmark](../../../packing/benchmarks/bench_rectangle_rust_transport.py)
  and [exact kernel checker](../../../packing/devtools/check_exact_rust_kernel.py).
- [Verification tooling overview](../guides/verification-tooling.md): current proof and
  native verifier status.
- [August infrastructure study][older-report]: earlier search-predicate and number-field
  benchmarks, with a different performance scope.

[matched]: ../../../packing/resources/web/wand125-tools-2026-09-29/receipts/native-rust-backend-matched-2026-09-30.json
[verifier-ab]: ../../../packing/resources/web/wand125-tools-2026-09-29/receipts/rust-exact-bounded-verifier-ab-2026-09-30.json
[verifier-benchmark]: ../../../packing/benchmarks/bench_rectangle_rust_verifier_ab.py
[transport]: ../../../packing/resources/web/wand125-tools-2026-09-29/receipts/rust-transport-fixed-2026-09-30.json
[sample]: ../../../packing/resources/web/wand125-tools-2026-09-29/receipts/rust-exact-os-sample-2026-09-30.json
[arithmetic-ab]: ../../../packing/resources/web/wand125-tools-2026-09-29/receipts/rust-exact-arithmetic-ab-2026-09-30.json
[coprime-controls]: ../../../packing/resources/web/wand125-tools-2026-09-29/receipts/rust-exact-coprime-differential-2026-09-30.txt
[derivative]: ../../../packing/resources/web/wand125-tools-2026-09-29/receipts/derivative-frontier-2026-09-30/result.json
[older-report]: research-2026-08-22-infrastructure-for-packing-exploration.md

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
