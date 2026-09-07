# BC-254 Target Instrument: Independent Readiness Review

Disposition: **GO for the coordinator’s instrument-readiness decision after the parser
fix.** The initial review was NO-GO because canonical rational validation occurred after
a potentially unbounded conversion.
The coordinator repaired that defect, and independent regressions pass.
No other blocking mathematical or engineering finding was identified within this
commission.

This is not target authorization, an H-099 verdict, or acceptance of a retained
mathematical result.
No Trump target rows, target LP, or arrangement were evaluated.

## Scope

This W7 pipeline-improvement/correctness review belongs to BC-254 / H-099 /
`think-bv9t`, in Session 089 phase 5 (renumbered on upstream integration).
Its commissioned window was `2026-09-06T20:13:11Z`–`2026-09-06T20:38:11Z`. The author
confirmed the implementation and report stable after stopping writes at `20:12:57 UTC`.
The coordinator subsequently authorized the narrowly scoped parser repair under
`think-q25u` and declared that fix stable before the final replay.
Final control and documentation checks were complete by `20:31:45 UTC`, within the
commissioned window.
Session accounting remains coordinator-owned.

The review covered the complete [frozen design](bc-254-support-screen-spec.md),
[author report](bc-254-target-readiness-slice-02.md), retained
[Trump construction](../../../../../cases/trump11/packing.py), relevant exact-field,
packing-verification and LP interfaces, and all six implementation/test files:

- [support_ceiling.py](../../../../../src/sqpack/full_size_density/support_ceiling.py)
- [support_screen.py](../../../../../src/sqpack/full_size_density/support_screen.py)
- [check_full_size_density_support_ceiling.py](../../../../../devtools/check_full_size_density_support_ceiling.py)
- [run_full_size_density_support_screen.py](../../../../../devtools/run_full_size_density_support_screen.py)
- [test_full_size_density_support_ceiling.py](../../../../../tests/test_full_size_density_support_ceiling.py)
- [test_full_size_density_support_screen.py](../../../../../tests/test_full_size_density_support_screen.py)

The reviewer changed only this report and the authorized
[independent controls](../../../../../tests/test_full_size_density_support_screen_review.py).
The coordinator, not the reviewer or original author, changed the parser.

## R1 — High: Reject Exponent Syntax Before Conversion

Before the fix, `_rational` checked the input’s string length, called
`checked_rational`, then compared the normalized result with the input.
Python’s `Fraction` accepts exponent notation.
A short string such as `1e1000000000` could therefore request a huge integer allocation
before the checker rejected its spelling.
The 4096-character and 2 MiB limits did not bound that allocation.
A wall alarm was not an adequate substitute for rejecting this syntax before arithmetic.

The retained regression
`test_noncanonical_exponent_is_refused_before_fraction_construction` mutates a side-two
toy packet’s radius and replaces the conversion function with a guarded wrapper.
The wrapper raises if that string reaches conversion; it never constructs the huge
integer. The pre-fix run failed exactly at that wrapper, with the source-control test
passing. No dangerous exponent conversion was executed.

The stable repair adds a bounded ASCII integer or numerator/positive-denominator lexical
check before conversion, retaining normalization equality afterward.
The latter still rejects safely bounded spellings such as `-0`, `0/3`, and `2/4`.
Expanded public-packet controls reject positive and negative exponents, decimals,
Unicode digits, underscores, whitespace, leading zeros, invalid denominators, empty
strings, and overlength strings before conversion.
Canonical strings reach the separate geometry guards.
**R1 is resolved in the reviewed working tree.**

## Mathematical Checks

The source-only replay independently confirms 88 labelled images, 60 distinct
placements, and eight orbits.
The orbit sizes are `(4, 8, 8, 8, 8, 8, 8, 8)` and original-square counts are
`(3, 1, 2, 1, 1, 1, 1, 1)`. Each distinct member receives its labelled preimage count
divided by eight, equivalently $n_O/m_O$. Four members have six preimages, eight have
two, and 48 have one: $4(6)+8(2)+48=88$. The averaged mass is exactly $\sum_O n_O=11$.
The reviewer’s source test replaces both row-sequence entry points and the optimizer
with failing functions, so this control cannot silently generate target rows or solve
the target LP.

D4 averaging preserves almost-everywhere feasibility: the eight transformed exceptional
sets have a null union, and the group permutes the complete support without changing
total weight. Exact reduced field-coordinate keys preserve distinct geometry and all
preimages. The original packing is checked for unit geometry, containment, and exact
pairwise separation.
There is no floating deduplication or assumption that the original packing itself is
symmetric.

The producer’s projection forms and replay’s orientation-corrected determinants give the
same strict interior test, including reflected corner traversals.
Replay checks all supporting lines, not merely the boundary segments.
Every retained rational radius is positive and satisfies strict margins greater than
twice the radius.
Unit edge length bounds each normal coordinate by one, so the resulting
closed neighborhood has constant incidence and positive area.
Its row is necessary for almost-everywhere feasible weights; no isolated point is
treated as a positive-area obstruction.

The center-first fallback is finite under its exact nonparallel guard.
Each of at most $4|\mathcal F|$ supporting lines excludes at most one of the
$4|\mathcal F|+1$ dyadic trials.
Each trial stays within its representative square, because its projection displacement
is at most $3/16<1/2$. Only exact supporting-line equalities are skipped.
The fixed extension has 36 candidates, and first-occurrence deduplication preserves the
row order. Every orbit column has a positive initial coefficient, yielding finite
coordinate bounds before optimization.

The adapter uses `min -mᵀa`, rows `A` and `-I`, and the independent active `-I` basis at
the feasible point zero.
Its incidence multipliers have the correct sign: `Aᵀy - z = m`, with nonnegative `y` and
`z`. Replay directly checks `Aᵀy ≥ m` and returns `sum(y)`, establishing the upper bound
by weak duality without solver status.
It also checks nonnegative primal weights, every row inequality, equality of objectives,
and the retained mass-eleven feasible control.
A bound below eleven is refused as a contradiction of that control.

## Independence and Execution Limits

The checker uses separate explicit D4 coordinate maps and determinant incidence, and
does not solve an LP. An additional algebraic-toy test disables the producer’s image,
projection-row, and optimizer paths while determinant upper replay succeeds; altered
incidence and an oversized radius are then refused.

This is not a wholly source-disjoint implementation.
Exact field arithmetic, the retained source constructor and source validator, scalar
upper checking, `primal_value`, and the fixed point-sequence routines are shared.
A correlated sequence bug could affect both producer and checker.
The packet alone also does not attest actual pivot history, elapsed cost, or that the
initial certificate was replayed before extension; the final extended packet does not
retain that initial certificate.
The runner enforces the initial replay and conditional extension in code, while the
packet checks the declared sequence and bounded receipt fields.

These limits do not weaken the checked upper inequality: every admitted row is
separately shown necessary, so a valid nonnegative upper witness bounds the specified
support even without complete arrangement coverage.
They do limit claims about independent protocol and execution-history verification.
A finite-row optimum above eleven is not an almost-everywhere feasible dual weighting.

The CLI requires an explicit mode, caps each solve at 64 pivots and the solve count at
two, and bounds the runner subprocess and checker to at most 60 seconds.
The internal worker also has a wall alarm.
Timeout or pivot refusal leaves the screen unresolved; it does not select a new grid,
direction, support, basis, or solver.
The file reader checks a regular leaf and opened descriptor, rejects symlinks, bounds
the payload, and rejects duplicate keys, floats, non-finite values, and noncanonical
rational strings.

## Independent Controls and Cost

All commands used the existing frozen Python 3.14 environment from `packing/`, with
`UV_CACHE_DIR=/private/tmp/squares-uv-bc231-cache` and `UV_OFFLINE=1`. The final
combined command was:

```shell
/usr/bin/time -p uv run --frozen --all-extras --group dev python -m pytest -q tests/test_full_size_density_support_ceiling.py tests/test_full_size_density_support_screen.py tests/test_full_size_density_support_screen_review.py
```

| Review check | Outcome | Pytest seconds | Process wall seconds | Process CPU seconds |
| --- | --- | ---: | ---: | ---: |
| Original author controls | 12 passed | 0.49 | 0.71 | 0.68 |
| Pre-fix reviewer controls | 1 passed; R1 regression failed safely | 0.67 | 0.90 | 0.84 |
| Final author and reviewer controls | 45 passed | 1.27 | 1.54 | 1.49 |

The final suite includes 33 reviewer test cases.
CPU is reported user plus system time.
These are individual control timings, not comparative performance evidence.
Ruff and BasedPyright passed with no findings on the reviewer test file; intermediate
private-interface and regex-style findings in that file were corrected before final
validation.

Target row generation, target optimization, complete target certificate replay, and peak
memory remain unmeasured.
The source-control timing does not establish that the full target command fits 60
seconds. No full validation gate was run by this reviewer.

## Coordinator Prerequisites

Before any target work, the coordinator must integrate the parser fix and review
controls, complete shared validation, decide readiness, and freeze the instrument,
source, exact command, output location, and process/pivot limits.
Preserve the execution receipt separately from the mathematical certificate.
A capped refusal remains a valid unresolved outcome, not permission for an unplanned
extension.

H-099 remains unresolved.
An upper certificate at most eleven would retire only its specified support claim.
A larger finite-row optimum would still require the complete almost-everywhere depth
check before any dual claim.
This review changes no frozen criterion and accepts no target result.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
