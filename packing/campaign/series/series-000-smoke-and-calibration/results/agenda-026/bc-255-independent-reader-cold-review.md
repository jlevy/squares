# BC-255: Independent Reader Cold Review

Disposition: **GO for the bounded independent reader’s source-only readiness.** The two
missing public-boundary regressions pass without a checker change.
The combined source/toy reader suite passes 12 tests.
This is not acceptance or rejection of H-104, and does not change H-036.

This review is `think-slox`, W7 pipeline-improvement/correctness, commissioned for
`21:15:25–21:30:00 UTC` on 2026-09-06. The author declared the reader stable at 21:13:28
UTC. Reviewed inputs are
[the independent checker](../../../../../devtools/check_restricted_orientation_discriminator.py),
[its source/toy controls](../../../../../tests/test_restricted_orientation_packet_review.py),
and the previously reviewed
[fixed-side adapter contract](bc-255-fixed-side-discriminator-readiness.md).
No target-side field element, point set, geometry, optimizer, or target packet was
constructed or evaluated.
The coordinator owns the prospective target lease and acceptance of this readiness
checkpoint.

## Mathematical and Receipt Boundary

The checker imports no producer geometry or project exact-field implementation.
It represents $a+b\sqrt2$ by two `Fraction` values.
If the coefficients have opposite signs, comparison of $a^2$ with $2b^2$ determines the
result, reversed when $a<0$. Zero coefficients and coefficients of the same sign are
handled separately. This is exact arithmetic; no approximate square root or interval
tolerance decides a sign.

For a 45° closed unit square, the independent point test is
$|\Delta x+\Delta y|\leq\sqrt2/2$ and $|\Delta y-\Delta x|\leq\sqrt2/2$. Its coordinate
half-extent is also $\sqrt2/2$. These are the correctly scaled rotated unit-square
conditions. The axis-oriented conditions use half-extent $1/2$. Boundary equality is
admitted, as required for the closed-unit strengthening; only the later strict-sublevel
packing argument can turn those hits into interior hits of enlarged open squares.

The independent formula transcription retains the four coordinate-reflection seeds,
checks the ten-set as a set of ten distinct points, and preserves the twelve-set’s
ordered coordinates and first-three A labels.
It does not substitute D4 symmetry for $K_4$. Localization tests the full union
$1\leq x\leq s-1$ with $y\leq1$ or $y\geq s-1$, after containment is checked.
Triple forcing requires a ten-set avoider in the closed canonical rectangle and tests
the named A-point separately.
Every returned escape must also match independently recomputed ten-set and twelve-set
masks.

Receipt validation requires exactly seven Boolean-or-null outcomes, matching checked and
unchecked inventories, and a completed-angle prefix of `0,45`. Positive completion
requires both angles and a supplied producer exit code of zero.
Every false clause requires exactly one directly verified escape.
Thus one verified false clause can reject the conjunction while other clauses remain
unchecked. A failed process without such a witness remains unresolved; it is not a
mathematical negative.

The positive decision is deliberately **not a standalone exhaustive certificate**. The
reader independently binds point formulas and checks receipt consistency, but it does
not reconstruct every event stratum from a packet’s counts.
Positive assurance therefore also needs the reviewed exhaustive producer algorithm, the
actual successful run, and the experiment’s recorded source/output custody.
The operator supplies the producer exit status; this CLI does not attest process history
or a Git revision. Both output paths retain `h036_outcome: unresolved` and
`standalone_exhaustive_certificate: false`.

The bounded coordinate parser rejects exponent notation and non-ASCII/noncanonical
rationals before conversion where applicable.
The JSON loader limits input to 256 KiB, rejects duplicate keys and nonfinite numbers,
and runs inside the ten-second alarm.
It is a path reader, not a regular-file or symlink-confinement API. This review assumes
the coordinator supplies the intended retained packet path; the alarm bounds a blocked
read rather than declaring every path an ordinary file.

## Added Boundary Regressions

The new
[cold-review test file](../../../../../tests/test_restricted_orientation_packet_boundary_review.py)
imports only the independent reader, not the producer or its field/geometry helpers.
It adds three tests:

1. **CLI alarm during input loading.** The test invokes the public `main`, verifies that
   the ten-second alarm is armed before loading, and triggers the handler that the CLI
   actually installed. It requires JSON `decision: unresolved`, exit 1, no
   geometry/decision call, alarm cancellation, and restoration of the prior handler.
   Signal delivery is mocked; this is a deterministic control of the installed handler
   and cleanup, not a ten-second OS scheduling measurement.
2. **Partial negative through the file-reading CLI.** A toy at the original source side
   replaces only the formula binding.
   Its ten points lie near $(3,3)$, while the twelve-set contains the nine integer-grid
   covering points and three extras.
   The contained square centered at $(1/2,1/2)$ misses the ten-set and hits the first
   twelve-set point on a closed corner.
   The partial packet has this one false axis clause, true axis twelve-cover, and five
   unchecked 45° clauses.
   The actual loader and geometric reader must return `rejected` despite the supplied
   nonzero producer exit, while leaving H-036 unresolved.
   Removing the negative witness must instead refuse with exit 2. This artificial
   formula binding is a control of conjunction semantics, not a negative source-theorem
   result.
3. **Quadratic signs and rotated boundary equality.** Eleven explicit rational
   coefficient cases cover zero, same-sign, and opposite-sign branches.
   A rotated square contains its two opposite diagonal boundary points and excludes
   rational outward perturbations of each.
   No decimal approximation supplies the expected mask.

The author tests additionally replay the unchanged source result and independent formula
binding, all seven named escape predicates on side-four toys, near-cancellation signs,
missing/changed receipt fields, and malformed packet input.
Their source fixture calls the original source producer only; the independent reader
itself does not import that producer.
All tests passed against the unchanged checker.
The new tests fill missing regression coverage rather than demonstrate a repaired
implementation defect.

## Validation and Cost

Commands ran from `packing/` using the existing frozen Python 3.14 environment and
cache, without dependency changes.
These are single-run development costs on the shared host.
CPU is `/usr/bin/time -p` user plus system time; no target throughput is inferred.

| Check | Result | Wall seconds | CPU seconds |
| --- | --- | ---: | ---: |
| Cold-review boundary controls | 3 passed; pytest 0.04 seconds | 0.32 | 0.26 |
| Final combined reader controls | 12 passed; pytest 2.25 seconds | 2.48 | 2.35 |
| Final focused Ruff check | Zero findings | 0.03 | 0.02 |
| New test file format check | Already formatted | 0.02 | 0.02 |
| Final focused BasedPyright | Zero errors, warnings, or notes | 0.85 | 1.51 |

```bash
/usr/bin/time -p uv run --frozen --all-extras --group dev pytest -q tests/test_restricted_orientation_packet_review.py tests/test_restricted_orientation_packet_boundary_review.py
```

`ruff check` and `basedpyright` used the same prefix on the checker and both test files;
`ruff format --check` covered the newly authored test file.
An initial test-only tuple style finding was corrected before the final checks.
No test failed, no check was skipped, and no checker source was edited.
Formatting and intermediate runs are not summed into a claimed total agent cost.

Only the cold-review test file and this report were written.
There were no target, registry, bead, Git, or other shared-record changes.
No further source-only blocker was found.
Root must accept this checkpoint and record a prospective target lease before
H-104/exp-114 opens.
The tbd review/TDD and experiment-loop guidelines kept the evidence and authority
separate; Practical Prose and Flowmark guided this report.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
