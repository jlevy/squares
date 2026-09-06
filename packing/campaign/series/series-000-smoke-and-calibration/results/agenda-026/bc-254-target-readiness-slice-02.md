# BC-254: Target-Readiness Build and Source Control

Status: implementation and author controls complete; independent review, coordinator
readiness, and experiment freeze remain pending.
No target LP, target row sequence, or arrangement was evaluated.
This W7 pipeline-improvement slice (correctness) belongs to BC-254 / H-099 /
`think-0qcu`, commissioned from
`2026-09-06T19:52:12Z` through `2026-09-06T20:19:58Z`. The
[reviewed design](bc-254-support-screen-spec.md) is unchanged.
The coordinator committed the reviewed toy baseline as `88277d92` before releasing these
implementation files for this slice.

## Exact Source Control

The authorized `trump11-v1` input control rebuilds
[`cases.trump11.packing.build`](../../../../../cases/trump11/packing.py), verifies its
unit geometry, containment, and pairwise separation, and computes the D4 closure.
The producer uses iterative rotations; the checker enumerates eight explicit coordinate
maps. Both retain all source-square/reflection/quarter-turn preimages of each distinct
placement and independently agree on the following metadata, in exact orbit-key order:

| Orbit index | Distinct members $m_O$ | Original squares $n_O$ | Uniform member weight $n_O/m_O$ |
| --- | ---: | ---: | ---: |
| 0 | 4 | 3 | 3/4 |
| 1 | 8 | 1 | 1/8 |
| 2 | 8 | 2 | 1/4 |
| 3 | 8 | 1 | 1/8 |
| 4 | 8 | 1 | 1/8 |
| 5 | 8 | 1 | 1/8 |
| 6 | 8 | 1 | 1/8 |
| 7 | 8 | 1 | 1/8 |

The 88 labelled images yield 60 distinct placements and eight orbit variables.
Each member of orbit 0 has six labelled preimages; each member of orbit 2 has two; the
other 48 placements each have one.
Thus the preimage multiplicities sum to $4(6)+8(2)+48=88$ and the averaged mass is
$\sum_Om_O(n_O/m_O)=11$ exactly.
The side’s reduced coefficients in the declared basis $(1,u,\ldots,u^7)$ are
`(5/2, 37/8, -5, 35/8, 8, 15/8, -15/2, 25/8)`.

This is the retained packing average from the design, not an optimized weighting.
Exact source validity and D4 isometries justify averaging eight packings almost
everywhere; deduplication retains their multiplicities.
No target necessary rows were generated to obtain this control.
It establishes neither an upper ceiling of eleven on this support nor feasibility of any
larger mass.

## Implemented Instrument

[`support_screen.py`](../../../../../src/sqpack/full_size_density/support_screen.py)
binds the exact source and preimages, orders orbit representatives, and implements the
declared center-first sequence.
Its fallback checks the fixed direction `(1, 2)` against every supporting line before
trying the fixed dyadic perturbations.
Only exact boundary equalities are skipped; other guard failures propagate.
It records trial and skipped indices, then admits first-occurrence integer rows with a
positive coefficient in every orbit column.

The extension is the design’s 36 points in increasing `(k, i, j)` order, with boundary
skips and first-occurrence incidence deduplication.
The LP adapter retains its explicit zero basis and 64-pivot limit.
The runner permits at most two solves and independently replays the first certificate
before considering extension.
It reuses an earlier feasible optimum with zero-extended upper multipliers, or starts
the second solve at zero.
A pivot refusal does not select another solver or basis.

[`check_full_size_density_support_ceiling.py`](../../../../../devtools/check_full_size_density_support_ceiling.py)
reconstructs the named source, support keys, preimages, and multiplicities without the
producer’s support constructor.
It recomputes each admitted incidence and strict neighborhood with oriented edge
determinants, checks the uniform control, and verifies the upper witness and matching
rational primal objective without solving.
The checker regenerates point ordering through the shared fixed-sequence routines; its
determinant incidence and neighborhood checks remain separate from their projection
calculations.

The file interface accepts one regular UTF-8 JSON file of at most 2 MiB. It refuses leaf
symlinks, duplicate or unknown keys, floating numbers, non-finite values, noncanonical
rational strings, incorrect coefficient counts, mutated source metadata, invalid rows or
radii, and excessive solve/pivot counts.
It checks the opened descriptor’s file type and uses no-follow/nonblocking flags.
Both checker and runner commands impose a process wall limit of at most 60 seconds.
The internal runner entry also imposes that limit.
Commands emit certificate data on stdout and costs or refusals on stderr; they do not
publish files or acceptance records.

The original side-two construction and replay entry points remain guarded.
The new target command exists but was not invoked:

```shell
uv run --frozen --all-extras --group dev python -m devtools.run_full_size_density_support_screen --solve-target --source trump11-v1 --timeout-seconds 60
```

Its stdout is the JSON packet accepted by the separate file checker:

```shell
uv run --frozen --all-extras --group dev python -m devtools.check_full_size_density_support_ceiling PATH_TO_PACKET --timeout-seconds 60
```

These commands do not supply research authorization.
The coordinator must freeze the instrument, output path, and acceptance run first.

## Controls and Cost

The 12 focused tests passed with no skips, including the four reviewed toy controls.
New controls cover rational and degree-eight packet/file replay; exact preimage counts;
the perturbed-center sequence and nonparallel refusal; fixed extension order and row
deduplication; one-solve reuse and conditional second-solve routing; pivot refusal;
mutated row ordering, source labels, and serialization; and CLI mode/deadline guards.
There are 46 expected refusal assertions or CLI outcomes across these tests.
The source-only path is tested with a solver replacement that would fail if called.

The initial TDD run failed collection at the missing `load_packet` interface, before the
new implementation existed.
Intermediate focused runs passed 7, then 10, then 12 tests.
The final focused tests plus module-boundary suite passed 26 tests with no skips.
Ruff and BasedPyright passed over the six authorized Python files.

| Check | Scope | Wall seconds | CPU seconds |
| --- | --- | ---: | ---: |
| Trump source/input control | Worker time, excluding interpreter/CLI startup | 0.573108 | 0.566956 |
| Focused tests | 12 passed; pytest reported 0.79 seconds | 0.99 | 0.90 |
| Focused tests and module boundaries | 26 passed; pytest reported 3.82 seconds | 4.05 | 3.78 |
| Final Ruff check | Six Python files | 0.03 | 0.02 |
| Final Ruff format check | Six Python files | 0.02 | 0.02 |
| Final BasedPyright | Zero errors, warnings, or notes | 1.08 | 1.98 |

These are individual development/control timings on the existing Python 3.14.7
environment, not a comparative performance result.
CPU is user plus system time for the timed commands and `process_time` for the input
control. Peak memory and target row/LP/replay costs remain unmeasured.

Commands ran from `packing/`, using the existing frozen environment and dependencies:

```shell
uv run --frozen --all-extras --group dev python -m devtools.run_full_size_density_support_screen --source-control --source trump11-v1 --timeout-seconds 60
/usr/bin/time -p uv run --frozen --all-extras --group dev python -m pytest -q tests/test_full_size_density_support_ceiling.py tests/test_full_size_density_support_screen.py tests/test_module_boundaries.py --durations=5
/usr/bin/time -p uv run --frozen --all-extras --group dev ruff check src/sqpack/full_size_density/support_ceiling.py src/sqpack/full_size_density/support_screen.py devtools/check_full_size_density_support_ceiling.py devtools/run_full_size_density_support_screen.py tests/test_full_size_density_support_ceiling.py tests/test_full_size_density_support_screen.py
/usr/bin/time -p uv run --frozen --all-extras --group dev ruff format --check src/sqpack/full_size_density/support_ceiling.py src/sqpack/full_size_density/support_screen.py devtools/check_full_size_density_support_ceiling.py devtools/run_full_size_density_support_screen.py tests/test_full_size_density_support_ceiling.py tests/test_full_size_density_support_screen.py
/usr/bin/time -p uv run --frozen --all-extras --group dev basedpyright src/sqpack/full_size_density/support_ceiling.py src/sqpack/full_size_density/support_screen.py devtools/check_full_size_density_support_ceiling.py devtools/run_full_size_density_support_screen.py tests/test_full_size_density_support_ceiling.py tests/test_full_size_density_support_screen.py
```

## Acceptance Still Pending

The coordinator still owns source-distinct review of these additions, shared integration
validation, readiness, and a frozen target command and deadline.
The input-control cost does not establish that 60 seconds suffices for target rows,
optimization, and certificate replay together.
The checker proves its exact inequalities; declared pivot counts are a run receipt, not
an independent attestation of execution history.

[H-099](../../../../hypotheses/H-099-trump-d4-finite-support-dual.md) remains
unresolved. A checked upper certificate at most eleven would retire only this specified
support. A larger finite-row optimum would still require a complete almost-everywhere
depth proof before it could supply a dual mass above eleven under the
[BC-242 contract](bc-242-full-size-density-proof-contract.md#almost-everywhere-dual-and-weak-duality).
No placements, arrangements, dependencies, shared records, beads, or Git state were
changed by this worker.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
