# Fixed-Core Packet Calibration: Mathematical and Admission Review

Date: 2026-09-12. Reviewed source revision: `5095241d266d3f8df8cc223cf1ad213e5a740d36`.
Workflow entry: W7 instrument admission, mathematical and experimental-design review.
Owners: `think-zypf` implements the command, `think-vy5i` measures it, and `think-1mma`
owns independent admission before `think-17qa` can register BC329.

**Verdict: the calibration has a small, analytically solved fixture that can exercise
every positive acceptance route, and its target-free implementation contract is
independently accepted.
Operational admission still requires the integrated measurement tools, fresh
full-profile runs, and independent readback.** The mathematical design review executed
no coverage sweep, calibration profile, certificate replay, or BC329 target.
The later implementation review ran only target-free controls.
The answers below are derivations, not measured profile outputs.

The existing plan’s 14,404 direction-record count is correct.
Those records measure a complete invocation and publication shape; they do not reproduce
BC329’s geometry size, arithmetic difficulty, interval branching, or memory demand.

## The Fixture

Freeze one separately named fixture, for example `fixed-core-calibration-cross/v1`, with
these exact inputs:

| Input | Value |
| --- | --- |
| $n$ | $2$ |
| Container side $L$ | $\frac{3}{4}$ |
| Core side $B$ | $\frac{1}{2}$ |
| Half-tangent limit $T$ | $\frac{1}{2}$ |
| Steps $K$ | $2880$ |
| Net | $t_k = k/5760$, for `0 <= k <= 2880` |
| Symmetry | D4 |
| Center $o$ | $(\frac{3}{8}, \frac{3}{8})$ |
| Offset $a$ | $\frac{3}{16}$ |
| Point atom | $o$, weight $\frac{1}{2}$ |
| Horizontal threshold atom | $\lbrace(\frac{3}{16},\frac{3}{8}), o, (\frac{9}{16},\frac{3}{8})\rbrace$, threshold 2, weight $\frac{3}{4}$ |
| Vertical threshold atom | $\lbrace(\frac{3}{8},\frac{3}{16}), o, (\frac{3}{8},\frac{9}{16})\rbrace$, threshold 2, weight $\frac{3}{4}$ |

There are five distinct sites, one positive point atom, and two positive two-of-three
threshold atoms. The center is invariant under D4; D4 permutes the two threshold atoms.
Freeze their order, member order, rational serialization, fixture identifier, and
provenance before executing a profile.
The source is this construction, with no T-025, T-026, or BC329 ancestry.

This is preferable to a point-only or zero-weight threshold fixture because both charge
languages affect the expected answer.
It also improves on putting all five sites so near the center that every core contains
all of them: some admissible cores here contain exactly two members of each triple,
while others contain all three.

### Coverage from first principles

Let a core orientation have nonnegative unit components $(c,s)$ and write $S=c+s$. This
covers the forward and reflected nets; `1 <= S <= sqrt(2)`. A core centered at
`p=o+(dx,dy)` is admissible precisely when

```text
|dx| <= r,  |dy| <= r,  r = (L - B*S)/2.
```

Every direction has a nonempty center domain because `L^2 - 2*B^2 = 1/16 > 0`. Also
`r <= 1/8`. The center atom lies strictly inside every core: its distance from $p$ is at
most `sqrt(2)/8 < 1/4`, and a square of side $1/2$ contains its concentric radius-`1/4`
disk in every orientation.

Choose the horizontal endpoint on the same side of $o$ as $p$’s x coordinate.
Its x distance from $p$ is `a-|dx|`, whose absolute value is at most $a$, because
`|dx| <= 1/8 < a`. Its y distance is at most $1/8$. Thus its squared distance from $p$
is at most

```text
(3/16)^2 + (1/8)^2 = 13/256 < 1/16 = (B/2)^2.
```

The center and this endpoint are strictly inside the core, so the horizontal threshold
fires. Choosing the vertical endpoint by the sign of `dy` proves the same for the
vertical threshold.
The radial slack is at least `(4-sqrt(13))/16 > 1/64`; it is positive
uniformly over the whole admissible domain and every orientation.

Consequently every admissible core has exactly the same raw charge:

```text
m = 1/2 + 3/4 + 3/4 = 2.
M = 1/2 + (3/4)*floor(3/2) + (3/4)*floor(3/2) = 2.
M/n = 1;   m > M/n.
alpha = 1/m = 1/2.
```

The raw object deliberately has $M=n$; running a normalized-certificate budget gate on
it before normalization would be wrong.
The raw sweep is permitted to measure this candidate, and the prescribed normalization
makes the budget strictly feasible.

At direction zero, the interior center $(9/32,9/32)$ has each triple’s center and nearer
endpoint inside and its farther endpoint outside: both traces have size exactly two.
At $(3/8,3/8)$ both traces have size three.
Both centers have charge 2. These are exact independent membership anchors.
A mutation from `count >= 2` to `count > 2` changes the first anchor’s charge to $1/2$,
so the known answer detects it.

For each net direction, an independent admissible anchor in the rotated frame is

```text
u = 3*(c+s)/8,   v = 3*(c-s)/8.
```

It is the physical center $o$ and has charge 2 before normalization and 1 afterward.
The sweep may choose a different minimizing witness.
Do not require its witness to equal this anchor: require its exact charge,
admissibility, and the existing dense/slab witness agreement contract instead.

### Net, normalization, and dilation

For adjacent half-tangents, the tangent of half the angular gap is
`(t_(k+1)-t_k)/(1+t_k*t_(k+1))`. Its largest value is at $k=0$, giving $D=1/5760$. The
endpoint test is `T^2+2*T-1=1/4 > 0`, and strict coarse containment is

```text
B*(1+D) = 5761/11520 < 1.
```

Normalize every weight by $1/2$, preserving coordinates, atom membership, thresholds,
net, and ordering. The point weight becomes $1/4$; both threshold weights become $3/8$.
The resulting minimum and budget are both 1, and the budget condition is $1 < 2$. Every
normalized closed-form condition holds.

The exact integer representation matters for interpreting interval rows:

| Quantity | Raw | Normalized |
| --- | --- | --- |
| Common weight scale | 4 | 8 |
| Point integer mass | 2 | 2 |
| Threshold integer masses | 3, 3 | 3, 3 |
| Integer budget | 8 | 8 |
| Rational budget | 2 | 1 |
| Rational minimum | 2 | 1 |

The normalized interval table has three rows and three member slots per row over five
sites.
Point-row padding must use the false sentinel; it must not count the center again.
Every expected interval direction has integer lower and upper bounds 8, corresponding to
rational $[1,1]$ on scale 8.

The generic dilation replay must obtain

```text
Q = sqrt(1+D^2)/(B*(1+D))
  = 2*sqrt(33177601)/5761,
Q^2 = 132710404/33189121.

S_limit = L*Q = 3*sqrt(33177601)/11522,
S_limit^2 = 298598409/132756484.

strict_factor_test_left_multiplier  = 33189121/132710400,
strict_factor_test_right           = 33177601/33177600.
```

Its relation is `>=`, `endpoint_certificate` is false, and `requires_compactness` is
false. The source minimum and budget are both 1. The side and factor are positive; their
squared values suffice to check the surds without a decimal tolerance.
$33177600=5760^{2} < 33177601 < 5761^{2}=33189121$, so the surd is irrational.
There is no comparison with T-026 in the calibration contract.

The exact geometry establishes the correct interval answer and uniform positive coverage
slack.
It does not establish a measured box count, a completion time, or that the current
split heuristic finishes under its 500,000-box allowance.
Require zero stalls and zero exhausted directions in the real runs.
Treat any failure as a calibration refusal and investigate it; do not weaken the
expected enclosure or pretend the mathematical proof was a measurement of the interval
program.

## Full Record Shape and Required Calls

For $K=2880$, the complete labels and counts are:

| Route | Required real computation | Retained direction rows |
| --- | --- | --- |
| Raw | `run_raw_sweep`, which calls `minimum_charge` for each direction | `0` through $2880$: 2,881 |
| Normalized exact | `run_exact_route`, which calls dense and slab `minimum_charge` independently for each direction | $0$ through $2880$: 2,881 rows, each carrying both results |
| Reflected interval | `run_interval_route` with `enclose=True`, via `verify_threshold_by_intervals` | `0` through $2880$, then `1'` through `2880'`: 5,761 |
| Dilation | `run_dilation_replay` / `build_limit_record`, which reopens normalized bytes and runs `verify_threshold` | `0` through $2880$: 2,881 |
| Total | Four route collections | **14,404** |

The formula is `3*(K+1) + (2*K+1) = 5*K+4`. The reflection of direction zero is omitted
because a quarter turn describes the same square.
Other labels remain even where two labels happen to describe the same direction; the
maintained doubled-net contract counts labels and does not deduplicate them.
Dense and slab results occupy one exact row per direction, so they add 2,881 rows rather
than 5,762. They nevertheless perform 5,762 exact minimizations.
Together with raw and dilation, this profile executes 11,524 exact direction
minimizations and 5,761 interval searches.

All four collections must be produced during that invocation, atomically published, and
read from retained bytes.
A reduced net followed by row replication, injected route returns, or copying the known
value into each output does not qualify.
Current `test_fixed_core_packet.py` includes injected `_raw`, `_exact`, `_interval`, and
`_dilation` controls.
Those test state transitions and refusals; their counters are not evidence of a real
full-profile execution.

The positive profile must pass these expected results:

| Stage | Exact admission requirement |
| --- | --- |
| Raw | Every row’s charge is 2; minimum 2; stable tied argmin index 0; every witness is admissible and replays to 2 |
| Normalization | Exactly `alpha=1/2`; point mass $\frac{1}{4}$, threshold budget $\frac{3}{4}$, total budget 1; all normalized closed-form conditions true |
| Exact | Every row’s dense and slab charge is 1; both witnesses agree as required by the current route; zero disagreements; stable argmin index 0; every witness replays to 1 |
| Interval | Every label present; integer bounds $[8,8]$; aggregate $[1,1]$; every row certified; zero stalls and exhausted budgets; finite, admissible witnesses of exact normalized charge 1 |
| Dilation | Every source-replay row has charge 1 and the expected label; all declarations match normalized bytes; exact factor and side above; source digest equals that of the normalized candidate |
| Publication and readback | Strict schema, exact direction sets, row filenames, counts, inventories, and byte bindings reconstruct; complete receipt only after readback and supervised success |

The calibration command should share the generic kernels and retaining primitives.
It must not call the BC329-specific `execute_packet`, `normalized_record`,
`load_packet_source`, or scientific `write_result` with altered constants.
Those functions carry target source identities, scientific predicates, and T-026
comparison fields.
Factor a small common primitive when needed; keep the scientific state
machine closed. The production calibration invocation has no route-injection switch.

Use the existing strict per-direction reconstruction functions where their parameters
already describe generic rows, or extract their shared logic.
Independent admission must have a separate reconstruction implementation, so that
sharing production readback does not become the only evidence for its own correctness.

## Refutation and Mutation Controls

The full positive profile cannot cover every failure branch.
Keep small maintained negative controls beside it; they need not each produce 14,404
rows. Run the existing relevant generic-kernel tests as well as the calibration-specific
controls.

| Mutation or negative control | Required result and defect detected |
| --- | --- |
| Change only the positive fixture’s $n$ from 2 to 1 in an explicitly separate control | $m=M/n=2$; strict raw comparison refuses normalization. Equality cannot pass the budget test. |
| Reduce the normalized point weight from $\frac{1}{4}$ to $\frac{1}{8}$, without renormalizing, and update its declared budget honestly | Every core has charge $\frac{7}{8}$; exact and interval coverage fail the threshold 1. Dilation refuses this source. |
| Change a two-of-three implementation to require all three | Direction-zero anchor $(\frac{9}{32},\frac{9}{32})$ has two members per triple; the erroneous raw charge is $\frac{1}{2}$, contrary to the oracle’s 2. |
| Omit the negative triple term in the two-of-three inclusion-exclusion expansion | At the physical center, a three-member trace counts three pairs without the necessary subtraction of two. Direct membership and the known charge expose the excess. |
| Test a separate larger-domain control with $L=\frac{3}{2}$, center $(\frac{3}{4},\frac{3}{4})$, the same offsets and normalized weights | At axis center $(\frac{15}{32},\frac{3}{4})$, exactly one horizontal member and no vertical members or point atom are inside; exact charge is 0. This tests the below-threshold branch that the positive fixture cannot reach. |
| Change a non-argmin row’s charge from 2 to 3, and update its digest and summary consistently | Independent per-direction known-answer validation refuses it even though the global minimum remains 2. Aggregate-only checks are insufficient. |
| Change a witness without updating the binding | Byte readback refuses it. |
| Change a witness to an inadmissible center and update all bindings consistently | Independent exact geometry refuses it. Digests alone do not verify witnesses. |
| Change a normalized weight, site, threshold, order, fixture ID, or source identity | Fixture freezing or normalization reconstruction refuses it. No T-025 ancestry may be substituted. |
| Delete, duplicate, add, or mislabel one row; use a numeric alias such as `01.json` | Exact label-set and filename checks refuse it, even if a reported count is unchanged. |
| Put $[1,1]$ in native normalized interval integer fields | Scale-aware known-answer readback refuses it: these fields must be $[8,8]$. |
| Increase the saved dilation limit or set an endpoint certificate true | Independent rational/surd reconstruction refuses it even after rehashing the file. |
| Substitute the scientific receipt schema or add `packet-accepted`, scientific acceptance, or a T-026 improvement field | The closed calibration schema refuses it; the scientific reader separately refuses an ordinary calibration receipt. |
| Kill or interrupt during each route, normalization publication, or readback; include a termination-resistant grandchild in a lifecycle control | No complete admission survives; the exact published set remains recoverable and the supervised group is terminated and reaped within the stated grace policy. |
| Let readback finish after its deadline, or make the worker exit nonzero after writing a complete candidate receipt | Final admission is revoked. A stale worker summary cannot override the observed process result. |

The larger-domain control’s witness is strictly admissible: its axis core has x range
$[7/32,23/32]$ and y range $[1/2,1]$, inside $[0,3/2]^{2}$. It contains only the
horizontal point $(9/16,3/4)$. This makes the expected zero charge a checked geometric
fact rather than an arbitrary mock return.

A coherently rehashed change to a *different valid* witness need not be a mathematical
refusal: the fixture has many minimizers.
Separate the immutable execution transcript’s byte identity from geometric witness
validity. Mutation tests should say which invariant they intentionally violate.

## Three Fresh Profiles and Their Regimes

`think-vy5i` requires at least three fresh full-profile controls on the intended host.
For its minimum defensible timing summary, run the same frozen fixture, clean code
revision, runtime, requested worker count, time allowances, and publication/readback
policy in three separate invocations.
Vary invocation identity, output directory, process group, and actual scheduling; record
timestamps, cache observations, background load, and run order.
Fresh processes do not establish cold OS caches.
Summarize each phase and the end-to-end profile by median and min–max range.

If “three profiles” instead means testing worker counts 1, 2, and 4, use this matrix:

| Requested workers | macOS effective raw / exact / interval / dilation at reviewed revision | Linux effective route maximums |
| --- | --- | --- |
| 1 | $1 / 1 / 1 / 1$ | $1 / 1 / 1 / 1$ |
| 2 | $2 / 2 / 1 / 1$ | $2 / 2 / 2 / 2$ |
| 4 | $4 / 4 / 1 / 1$ | $4 / 4 / 4 / 4$ |

The interval and dilation schedulers explicitly use serial execution off Linux.
Raw and normalized-exact schedulers request fork pools on the intended macOS host.
These are code-path worker settings, not observed simultaneous utilization; record
actual child PIDs and distinguish the two facts.
Keep the fixture and all other settings fixed while varying workers.

One run per worker count gives three conditions with one observation each.
Pooling those three timings into a median and range would mix regimes.
Either repeat each worker condition at least three times, or run the two auxiliary
worker probes separately from the three required repetitions of the intended production
worker profile. The plans do not require nine runs unless all three worker regimes are
being priced.

Do not vary the fixture, net, atom count, interval resolution, deadline, or box budget
between the three repetitions and then present the spread as host noise.
Any later geometry stress fixture or deliberately short timeout profile is a separately
declared control with its own purpose and disposition.

## Clocks, Memory, and What an Allowance Means

Record parent preflight, launch, source loading, raw, normalization/publication, exact,
interval, dilation, full readback, worker exit, and supervisor cleanup clocks.
State whether phase clocks include their checkpoint writes; overlapping observations
cannot simply be summed.
Use monotonic clocks for duration and deadline arithmetic, with one declared invocation
origin and absolute deadline relationships.
The terminal receipt must include the post-readback and parent-observed exit result.

The parent preflight must itself be bounded.
The reviewed agenda and preflight correctly identify that as an outstanding gate, along
with exact published direction sets for partial interval and dilation receipts.
A worker-only deadline cannot price or limit an unbounded Git/runtime/source preflight.
At every interrupted checkpoint, the receipt must identify exactly which published rows
belong to that checkpoint; count and last row do not identify a sparse completion set.

Retain requested and effective worker settings separately for each route.
Name CPU observations by their actual scope: supervisor, coordinator, selected workers,
or reaped children. Coordinator `process_time` alone is not process-group CPU time.
Cumulative child usage requires a defined baseline, end point, and explanation of which
exited processes it includes.

For memory, retain the sampled sum of resident-set sizes of the observed process group,
with sample count, sampling interval, maximum actual gap, PID membership, observer
errors, and the peak sample time.
A zero-sample run has no measured peak.
Any missing phase or unobserved interval must remain explicit.
Required metrics with an insufficient observation should fail metrics admission,
independently of the mathematical answer.

The sampled sum-of-RSS maximum is a maximum of observed samples.
It can miss a transient peak between samples, excludes processes that escaped or
outlived observation, and can count fork-shared pages more than once.
It does not upper-bound the true continuous maximum or measure unique physical memory.
An independent reviewer can reconstruct the sample maximum; it cannot turn the samples
into a hard memory guarantee.

Inventory every retained artifact by role, relative path, count, and byte size.
Use the existing byte-binding format across publication and readback, where it detects
identity changes. Repository code integrity belongs to Git.
The count 14,404 concerns direction records only; receipts, fixture bytes, normalized
bytes, dilation records, metrics, and logs add files and bytes.
Do not assume byte totals match across repetitions when clocks and process observations
legitimately differ.

Successful repetitions establish that this exact invocation shape completed on this host
under these allowances and that the observer measured something.
Their timing supports an operational-overhead estimate and an explicitly empirical
choice of reserve for preflight, publication, readback, and cleanup.
Three runs do not establish a tail probability, a worst-case bound, or a deadline
guarantee.

BC329 has 1,440 distinct sites and 904 atoms; this fixture has five sites and three
atoms. BC329 also has different rational event coordinates, denominators, domain cells,
and potential interval seams.
Matching direction counts does not match those costs.
Neither a per-direction multiplier nor the calibration’s RSS may be extrapolated into a
BC329 runtime or memory upper bound.
The future 90–120 minute scientific allowance is a prospective resource decision, not a
prediction validated by the easy fixture.
Freeze it before BC329; a timeout remains unresolved under the frozen rule.

## Source-Distinct Admission

The reviewer for `think-1mma` should receive the frozen fixture argument, admitted code
revision, raw artifact directories, and exact invocation records.
It should implement or use a maintained reader that does not import the producer’s
fixture factory, expected answer constants, normalization routine, receipt validator,
direction reconstruction, membership replay, or dilation helper as its oracle.
A second invocation of the same validator is repeatability evidence, not a
source-distinct check.

Admission should map each obligation to bytes and an actual check:

1. Independently derive the fixture geometry, budgets, net, normalization, and dilation
   formulas above. Bind the raw fixture to its reviewed construction.
   Verify the exact mass and member tables; do not trust a producer’s
   `known_answer_passed` flag.
2. Decode every receipt and row with closed schemas, duplicate-key rejection, finite
   numeric checks, and exact rational syntax where required.
   Independently generate the complete forward and reflected label sets and reconstruct
   all four counts and digests.
3. Require every raw direction to equal 2 and every normalized exact/dilation direction
   to equal 1, rather than checking only aggregate minima.
   Reconstruct the stable lowest tied argmin and dense/slab disagreements.
4. At every retained raw, dense, slab, and interval witness, derive the rotation
   directly from $t=k/5760$; exchange its components for primed labels.
   Convert retained binary floats to their exact rational values for interval witnesses.
   Recompute physical admissibility and point/threshold membership using closed
   inequalities and no epsilon.
   Dilation rows do not carry witnesses in the current kernel; their labels and known
   charge still require verification, and their source bytes must equal the normalized
   source used by the other routes.
5. Independently verify interval scale 8, every $[8,8]$ integer enclosure, certified
   statuses, zero stalls/exhaustion, and nonempty measured work.
   Recompute the aggregate $[1,1]$. Re-derive every mathematical dilation field with
   rational arithmetic and the positive surd, including endpoint semantics.
6. Validate publication/inventory binding and the final deadline relationships.
   Inspect the actual exit and process-group cleanup evidence.
   Recompute timing/RSS summaries from retained observations and name any limits or
   missing observations.
7. Demonstrate the cross-schema and coherent-tampering refusals above.
   Inspect the execution path and source/runtime manifest to confirm that these rows
   came from real generic kernel calls, with no oracle-based shortcut, copied rows, or
   injected result. Preserve the reviewer identity, reader revision, commands,
   dispositions, and exact receipt identities in the admission record.

A mathematically correct transcript alone cannot prove that a program actually executed
the claimed calls: constant-answer fixtures can be fabricated.
That obligation depends on source inspection, bounded invocation provenance, runtime
binding, and maintained execution controls.
The proposed admission is an audit of a trusted local execution, not cryptographic
remote attestation or a defense against a malicious host.

### Scientific separation is a consumer contract

The outer schema must be exactly `fixed-core-packet-calibration/v1`, with a closed
calibration-only disposition vocabulary.
It cannot carry `packet-accepted` or a scientific acceptance.
`fixed_core_packet.load_result` must refuse it, and the calibration reader must refuse
scientific receipt schemas.
A T-025 source, BC329 packet ID, scientific decision, or T-026 improvement claim in this
receipt is a refusal.

The real `build_limit_record` deliberately emits a generic threshold dilation record for
the positive fixture, and a generic certificate checker may accept the valid normalized
$n=2$ fixture. Claiming that no generic mathematical reader can accept those bytes would
contradict the purpose of a positive control.
Retain that generic output as explicitly scoped calibration material, and make
campaign/claim consumers reject its promotion into BC329 evidence.
There is no new $n=11$ claim in these outputs.

## Remaining Gaps and Source Map

No mathematical obstruction was found to this fixture.
The calibration-only producer, reader, frozen fixture, exact witness checks, common
partial readers, and refusal controls now exist.
A source-distinct correction review of `d924a4bfff54fad8a039ae0cde2103a0e4817848`
accepted the CAL-1 and CAL-7 repairs but reproduced five remaining defects under
`think-bi3f`, `think-1kgu`, `think-lidy`, `think-4wuj`, and `think-1e9p`.

Implementation commit `0533ebaeb90cf42acf20e0029535356282a5624c` adds the missing
Condition 5′ oracle field and a real small-net builder comparison; makes dilation labels
consistent across producer, schema, and common reader; protects the SIGINT launch
window; stages terminal bytes behind fresh deadline and cancellation checks; and
requires two reconstructed positive, error-free RSS observations.
Its combined target-free calibration and fixed-core suites pass 177 tests in 18.07
seconds on Python 3.14. Repository-wide Ruff formatting and lint checks and BasedPyright
report zero findings, and `packing-validate --edit` passes in 50.83 seconds.
These are author-run implementation controls, not source-distinct admission or
host-profile evidence.

A final source-distinct correction review at `b626097000a3f7cc9dbb19fbf3fb787f505c7104`
accepted CAL-2, CAL-3, CAL-4, and CAL-6, retaining the earlier CAL-1 and CAL-7
acceptances. It refused CAL-5 because real SIGINT during either staging-file acquisition
could leave the new descriptor and path outside both cleanup owners.
The first follow-up at `967f7cd46e94a9fddbad653295b146de5740110c` used a main-thread
signal mask. Source-distinct exact-head review refused it because the mask did not cover
an already eligible background thread.
SIGINT, SIGTERM, and SIGHUP at either staging pass could still run the Python handler in
the main thread inside `mkstemp`, before the descriptor and path had a cleanup owner.
The same review found a separate descriptor leak when injected `os.fdopen` failure
occurred before stream adoption.

The second repair at `85d3f529c29114cf6b202fb1b09445c0dc002bc1` makes the Python handler
consult a nesting-aware staging critical section, then raises the recorded signal after
ownership and cleanup are established.
It also keeps raw-descriptor ownership until `os.fdopen` succeeds and closes the
descriptor on adoption failure.
Maintained subprocess controls exercise both staging passes for all three signals from
the main thread and an already eligible background thread, plus adoption failure at both
passes. They check exact signal provenance, partial publication, prior-handler and mask
restoration, descriptor closure, staging-file absence, the closed receipt envelope, and
the strict retained-artifact set.
The combined target-free calibration and fixed-core suites pass 192 tests in 25.44
seconds on Python 3.14; Ruff and BasedPyright report zero findings.
These are author-run controls.

A source-distinct exact-head review at `fcb538c29b846fb5e7c33bd962772ada9c21aedd`
accepts CAL-5 and retains every prior CAL-1 through CAL-7 acceptance.
The reviewer independently passed 54 bounded lifecycle controls, including combined
signal and adoption faults and the two staging return boundaries; ten fixture, source,
and readback controls; four real launch controls; the 192-test focused suite; and the
configured Ruff and BasedPyright checks.
The review is scoped to the inspected POSIX implementation on the current macOS Python
3.14 host. It does not admit Linux execution, SIGKILL, host failure, blocked operating
system calls, cleanup-filesystem failure, or signal storms.

Operational admission remains unmeasured.
Before closing the calibration work:

- Integrate and independently accept the observed-worker contract, maintained
  three-profile coordinator, source-distinct receipt reader, and final
  [run sheet](../specs/archive/plan-2026-09-13-n11-bc329-three-profile-run-sheet.md).
- Run at least three fresh repetitions of the intended profile, retaining complete
  metrics and all 14,404 direction rows per run.
- Admit those receipts through source-distinct readback before any BC329 registration.

The common target-free preflight repairs are retained in integrated commit
`d6bbe20172d4048a9f156b1c3c4fcfe8f1b64014` and the combined runner was independently
accepted at `421c344545873647dd26f856320d93dbfd59413a`. They cover `think-rvhu`,
`think-fmju`, `think-42zc`, `think-5fdx`, `think-g7vg`, and `think-pvmv`: literal Git
pathspec and tracked-output overlap handling; operational lockfile and launch-failure
taxonomy; fresh time calculations across launch; resolved Git administrative-directory
refusal; and signal cleanup.
The calibration command does not replace that independent runner review.

The reviewed sources were:

- [BC329 preflight](review-2026-09-10-n11-bc329-packet-preflight.md),
  [agenda-035](../../../packing/campaign/agendas/agenda-035-n11-daytime-strategy.md),
  and the
  [active daytime plan](../specs/archive/plan-2026-09-10-n11-daytime-strategy-and-explainer.md)
- [fixed_core_packet.py](../../../packing/devtools/fixed_core_packet.py) and its
  [target-free controls](../../../packing/tests/test_fixed_core_packet.py)
- [threshold.py](../../../packing/src/sqpack/fractional/threshold.py),
  [threshold_interval.py](../../../packing/src/sqpack/fractional/threshold_interval.py),
  and [interval.py](../../../packing/src/sqpack/fractional/interval.py)
- [decide_threshold_certificate.py](../../../packing/devtools/decide_threshold_certificate.py)
  and [dilation_corollary.py](../../../packing/devtools/dilation_corollary.py)
- Read-only `tbd show think-zypf think-vy5i think-1mma think-17qa`, observed on
  2026-09-12

The original mathematical design review treated the source’s 156-test summary as prior
recorded evidence rather than rerunning it.
The later exact-head CAL-5 review independently ran the 192-test focused suite and the
controls reported above.
Neither review establishes the three operational profiles, BC329 coverage,
normalization, retention, or a stronger lower bound.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
