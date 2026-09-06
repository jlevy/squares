# BC-231 First Implementation Slice

BC-231 (`think-7mk4`), W7, 2026-09-06. Base: `c14451f5`. The coordinator authorized this
control-only slice within `19:11:26–19:41:26 UTC`; source changes stabilized at
`19:28 UTC`. The [BC-230 theorem](bc-230-adaptive-core-contract.md) and
[reviewed control matrix](bc-230-control-matrix.md) remain unchanged.

The two project routes agree on a small nonuniform control and a complete small scalar
specialization. H-095 remains instrument-blocked: there is no adaptive JSON loader,
standalone route, retention decision, or target search in this slice.

## Exact Control

The control specification was reported before execution: `n = 11`, `L = 6/5`, a center
atom at `(3/5, 3/5)` of weight `1`, and the four axis sites `(3/10, 3/5)`,
`(9/10, 3/5)`, `(3/5, 3/10)`, `(3/5, 9/10)` of weight `1/10` each.
These five distinct sites have total mass `7/5` and form complete D4 orbits.

| Cell | Half-tangent | Core side | Closed boundary tangents | Maximum mismatch | Minimum mass |
| --- | --- | --- | --- | --- | --- |
| 0 | `0` | `7/10` | `[0, 1/4]` | `1/4` | `6/5` |
| 1 | `1/4` | `3/4` | `[1/4, 56/71]` | `1/4` | `13/10` |
| 2 | `9/20` | `4/5` | `[56/71, 1]` | `16/89` | `7/5` |

The strict containment products are `7/8`, `15/16`, and `84/89`. The three predicted
minimum masses agree with direct atom summation over every reachable open event cell,
the production sweep, and zero-width interval enclosures.
The reflected interval directions retain their source cells’ sides and have the same
respective minima. This is P4 development evidence from two project routes, not
completion of its mandatory three-route control.

The independent test oracle uses separating-axis overlap to select reachable cells and
direct membership to score them; it uses no production clipping, span selection, or
prefix sums. Direct membership also establishes the boundary-union oracle at one single
event boundary and one multiple-event intersection.
Those checks prepare P5; they do not replace later route-specific boundary receipts.

## Source and Checks

The new [exact adapter](../../../../../src/sqpack/fractional/adaptive.py) derives cell
geometry and calls the existing per-direction sweep with each `B_k`. The new
[interval adapter](../../../../../src/sqpack/fractional/adaptive_interval.py) derives
seams and mismatches separately, then calls the existing directed-rounding center-box
search. Neither API exposes an acceptance or retention verdict.
Legacy code and retained certificate bytes are unchanged.

[Ten tests](../../../../../tests/test_fractional_adaptive.py) cover the nonuniform
control, a complete three-direction scalar comparison, exact sweep witnesses, seam
ownership and geometry mutations, strict-containment equality, incomplete and unequal
orbits, a signed weight, complete-zero-orbit invariance, and unsupported center domains.
For the retained n=11, n=12, and n=17 source objects, this slice checks scalar geometry,
total mass, and unchanged bytes only; it does not replay their full coverage decisions.

From `packing/`, with the existing Python 3.14 environment:

```bash
UV_CACHE_DIR=/private/tmp/squares-uv-bc231-cache uv run --frozen --all-extras --group dev python -m pytest -q \
  tests/test_fractional_adaptive.py tests/test_fractional_certificate.py \
  tests/test_fractional_interval.py tests/test_fractional_sweep_integer.py \
  tests/test_decide_certificate.py \
  -m 'not exhaustive_exact and not exhaustive_interval and not slow'
```

Result: `152 passed, 22 deselected in 14.03s`; all ten new tests are included.
The initial test failed because the adaptive module did not exist; the final
new-test-only run passed ten tests in `0.29s`. Scoped Ruff and BasedPyright checks
passed with zero findings.
These are development-test elapsed times, not per-route decision-cost measurements.

## Remaining Boundary

The existing project sweep constructs a spurious polygon from reversed coordinate bounds
when a core’s admissible center domain is empty; the interval and scalar standalone
routes refuse empty or singleton domains.
The new exact control adapter refuses both before invoking that sweep.
This slice therefore supports positive-area center domains only.
Complete adaptive retention still needs a declared handling of those boundary cases; no
theorem premise was changed.
PR 100’s open ceiling/cutting corrections were inspected but not imported, and neither
new coverage route calls those modules.

BC-231 still requires the closed bounded JSON parser, independent standalone verifier
under normal and optimized Python, all retained positive/source/refusal replays, the
remaining format and premise-preserving mutations, and a frozen-byte three-route
retention command with exact per-cell agreement and cost receipts.
In particular, the pure cover-validator branches, T10’s independently frozen subunit
witness, full D4 folding controls, and route-disagreement refusals remain unimplemented.
Independent review and the full control matrix are prerequisites to any candidate or
BC-234 synthesis. The next bounded slice can add the loader and pure cover controls; the
coordinator must price further work after the two initially selected slices.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
