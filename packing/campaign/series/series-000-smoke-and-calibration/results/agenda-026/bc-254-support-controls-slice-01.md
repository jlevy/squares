# BC-254 Control Build: First-Slice Checkpoint

Status: partial instrument, non-target controls passing; independent review and H-099
readiness remain pending.
This checkpoint belongs to BC-254 / H-099 / `think-01q4` and the existing first slice
ending `2026-09-06T19:41:26Z`. The [reviewed design](bc-254-support-screen-spec.md) is
unchanged. No Trump support, target row, target LP, or arrangement was generated.

## Implemented and Checked

[`support_ceiling.py`](../../../../../src/sqpack/full_size_density/support_ceiling.py)
implements exact D4 support deduplication, orbit multiplicities, unit geometry and
containment checks, projection-based incidence, and a positive rational neighborhood
radius. Its control-support constructor refuses every container side other than two.
The rational LP adapter supplies the explicit nonnegativity rows and zero basis, checks
the finite-bound guard, caps pivots at 64, and checks the returned primal point and
upper multipliers arithmetically.

[`check_full_size_density_support_ceiling.py`](../../../../../devtools/check_full_size_density_support_ceiling.py)
regenerates orbit identities from the declared toy seeds using explicit coordinate maps,
then recomputes incidence and strict neighborhood margins with oriented edge
determinants. Its upper check does not call the LP solver.
It also refuses a container side other than two.
There is no target loader, target command, or file-based CLI. This is solver-independent
replay, not completed source-distinct acceptance review.

The four tests in
[`test_full_size_density_support_ceiling.py`](../../../../../tests/test_full_size_density_support_ceiling.py)
passed with no skips.
Their positive controls establish:

- Four overlapping rational D4 placements have row coefficient four and exact ceiling
  one, with a checked positive neighborhood.
- The declared two-variable rational LP has primal point `(1/3, 1/3)`, upper multipliers
  `(4/3, 4/3)`, and exact objective `8/3`.
- The non-target algebraic control in the retained degree-eight field has eight distinct
  orbit members and exact ceiling one.
  It imports the field declaration but does not call the Trump packing builder.
- Reordered, reversed, quarter-turned, and repeated source representations preserve the
  geometric support and replayed bound.

Fifteen expected refusals ran: uncovered LP column, exhausted pivot budget, disabled
target side, omitted support member, Booleanized incidence, Boolean coefficient,
excessive neighborhood radius, six negative/non-exact/malformed multiplier cases,
boundary row point, and containment failure.
A failed guard raises an exception; it is not recorded as a weaker successful
certificate.

## Commands and Measured Cost

All commands ran from `packing/` through the frozen Python 3.14 environment, offline,
using the existing cache.
The failed initial import identified Python `3.14.7`. Times below are `/usr/bin/time -p`
results, including `uv` startup; CPU is user plus system time.
They measure controls and development checks, not H-099’s target cost.

| Check | Result | Wall seconds | CPU seconds |
| --- | --- | ---: | ---: |
| Initial TDD test, before either implementation module existed | Expected collection failure; one import error | 0.30 | 0.28 |
| Final focused pytest command | 4 passed, no skips; pytest reported 0.07 seconds | 0.28 | 0.26 |
| Final focused Ruff check | All checks passed | 0.03 | 0.02 |
| Final focused BasedPyright check | 0 errors, 0 warnings, 0 notes | 0.78 | 1.37 |

Exact final commands:

```shell
UV_OFFLINE=1 /usr/bin/time -p uv run --frozen --all-extras --group dev python -m pytest -q tests/test_full_size_density_support_ceiling.py
UV_OFFLINE=1 /usr/bin/time -p uv run --frozen --all-extras --group dev ruff check src/sqpack/full_size_density/support_ceiling.py devtools/check_full_size_density_support_ceiling.py tests/test_full_size_density_support_ceiling.py
UV_OFFLINE=1 /usr/bin/time -p uv run --frozen --all-extras --group dev basedpyright src/sqpack/full_size_density/support_ceiling.py devtools/check_full_size_density_support_ceiling.py tests/test_full_size_density_support_ceiling.py
```

Intermediate pytest runs passed first one test, then four tests.
The first type check found two diagnostics at the rational-input conversion; an explicit
checked cast fixed them, and both subsequent checks passed.
Ruff formatted only the three authorized Python files.
Formatter time, peak memory, and reasoning CPU time were not measured.
The observed implementation clock interval was `19:31:13–19:38:27 UTC`, before report
finalization; the coordinator owns final active-time accounting.

## Remaining Obligations

The deterministic initial-center fallback, fixed dyadic extension, complete source
preimage receipt, coalesced uniform-packing control, target loader, and bounded target
command are not implemented.
The reusable row routine does not itself sequence those target rows.
Strict serialized packet parsing and a file-based checker interface also remain open;
the current tests exercise typed Python inputs and exact rational-value parsing.

Source-distinct mathematical/code review, shared integration validation, and the
coordinator’s instrument and experiment freeze are still required.
The toy timings do not establish that the proposed 60-second target allowance is
sufficient. H-099 remains not ready, and these toy ceilings are not H-099 outcomes.
No registry, session, ledger, bead, Git metadata, dependency, or file outside the
authorized control paths was changed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
