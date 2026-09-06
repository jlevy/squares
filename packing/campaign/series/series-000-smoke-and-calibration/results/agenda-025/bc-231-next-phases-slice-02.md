# BC-231 Second Implementation Slice

BC-231 (`think-7mk4`), W7, 2026-09-06. The coordinator authorized
`19:39:02–20:09:02 UTC`; source and tests stabilized at `19:55 UTC`, following slice-01
commit `184fa6c9`. The [BC-230 contract](bc-230-adaptive-core-contract.md) and
[control matrix](bc-230-control-matrix.md) remain unchanged.

The project now loads the bounded adaptive JSON format and exercises the pure F4/F5
cover refusals. This is control-only implementation evidence: H-095 remains
instrument-blocked, and there is no adaptive retention command or target result.

## Implemented Boundary

The new [loader](../../../../../src/sqpack/fractional/adaptive_io.py) enforces the
closed top-level and angle-cell key sets, literal variant/rule/ownership fields, exact
integer types, canonical rational strings, duplicate-key and nonfinite-token refusals,
and the frozen byte, atom, angle-cell, and rational-text limits.
Structural and bounded-format checks finish before angle geometry.
Declared totals and claims must match the parsed instance.
Existing in-memory guards enforce containment, nonnegative distinct atoms, listed-domain
D4 completeness, total mass below `n`, and the axis-core method ceiling.
The committed geometry adapters and scalar loader are unchanged.

`load_bytes` returns an `AdaptiveInput`, not an acceptance result.
Its minimum declaration remains unverified, including null or a subunit rational;
Condition 5 and the later declared-minimum comparison have not run.
`load(path)` reads at most the byte limit plus one and does not provide retention
rereads or artifact binding.

Atom coordinates are container `(x,y)` coordinates.
Angle-cell boundaries are tangents on the folded orientation arc, not center-space
event-cell boundaries.
Existing sweep witness centers remain rotated `(u,v)` coordinates; they must be
converted before a later receipt compares them with container-coordinate witnesses.
This slice creates no decision receipt.

## Controls and Checks

The serialized P4 fixture is the unchanged five-atom control from
[slice 01](bc-231-next-phases-slice-01.md): `L = 6/5`, total mass `7/5`, and core sides
`7/10`, `3/4`, `4/5`. Both project routes still give per-angle-cell minima `6/5`,
`13/10`, `7/5`. The small equal-side scalar fixture also passes after a test-only JSON
serialization. Retained n=11, n=12, and n=17 objects supply geometry and atom-data round
trips only; no full coverage or source replay ran, and their bytes are unchanged.

The [102 new tests](../../../../../tests/test_fractional_adaptive_io.py) include every
required key, the frozen input limits and inclusive byte/rational boundaries, malformed
structures, geometry and measure mutations, and these branch-reachability controls:

- F4 calls the pure validator on `[0,1/3]`, `[1/3,2/3]`, `[2/3,1]`, then reaches named
  gap and overlap refusals by changing the second lower endpoint to `2/5` and `1/4`.
  Patched parser and declaration checks would fail the tests if invoked.
- F5 directly reaches the axis and fold endpoint refusals.
  Its serialized n=12 mutation recomputes every dependent field and reaches the named
  final-seam refusal at `q_K = 164144306/142927847 > 1`. A separate stale mismatch
  mutation takes the earlier declaration-equality branch.
  This ordering requires a loader-side algebraic comparison before complete-cover
  validation; it is not another independent route.

From `packing/`, using Python 3.14 and the frozen environment:

```bash
UV_CACHE_DIR=/private/tmp/squares-uv-bc231-cache uv run --frozen --all-extras --group dev python -m pytest -q \
  tests/test_fractional_adaptive_io.py tests/test_fractional_adaptive.py \
  tests/test_fractional_certificate.py tests/test_fractional_interval.py \
  tests/test_fractional_sweep_integer.py tests/test_decide_certificate.py \
  -m 'not exhaustive_exact and not exhaustive_interval and not slow'
```

Result: `254 passed, 22 deselected in 17.44s`. Scoped Ruff and BasedPyright checks on
the two new Python files report zero findings.
The TDD start failed on the missing module; development also caught an invalid
exception-clause spelling and a test that incorrectly treated the required per-cell
`square_side` as unknown.
Both were corrected.
Test duration is not a route-cost measurement.
The coordinator owns snapshot validation and independent review.

### Coordinator review

The coordinator independently read the loader, its refusal tests and the BC-230
serialized contract, then replayed the loader and first-slice adaptive tests under
Python 3.14. No finding was identified in this control-only boundary.
The review checked canonical rational spelling, noncoercive integer fields, bounded
reads, declaration order, F4/F5 branch reachability, and the explicit separation
between loading and a coverage or retention verdict.
This does not complete the missing standalone, source-replay, or triad obligations.

## Remaining Work and Price

The following are planning estimates in active worker minutes, not measured run costs or
authorization for another slice.
They price the remaining BC-231 contract, not an H-095 target search.

| Remaining obligation | Active minutes |
| --- | --- |
| Independent standard-library checker, its own parser/geometry, and normal versus `-O` controls | 35–55 |
| Three-route orchestration, per-cell receipts, coordinate normalization, byte binding, disagreement and skipped-route refusals | 40–65 |
| Full scalar/source compatibility and legacy-refusal harnesses | 20–35, plus replay runtime |
| T10 independent full-grid fixture generation, frozen witness, and all three routes checking that same witness | 35–75, plus replay runtime |
| Remaining boundary, eight-sector folding, and orbit-stabilizer controls | 20–35 |
| Empty/singleton policy review and any explicitly selected follow-on | 10–20 |
| Independent review, fixes, and focused integration validation | 20–35 |

The working total is **180–320 active minutes plus unpriced full replays**. T10 and the
receipt integration are the largest uncertainties.
Equal verdicts or minima alone do not satisfy T10: its independently frozen angle cell,
direction, container-coordinate center, and mass must be checked by all three routes.
No such witness has been frozen.

The current adapters continue to refuse empty or singleton center domains.
The loader does not reinterpret that refusal as a coverage result, and the all-empty
`least_cell_mass` policy remains unresolved.
The next useful selected slice would commission the standalone route on P4 and the
frozen format mutations; the coordinator must choose it explicitly.
The previously mentioned 180 minutes is neither a completion promise nor automatic
authority to continue.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
