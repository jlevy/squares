# BC-255: Fixed-Side Discriminator Review

**GO for the adapter’s bounded readiness scope.** The source/toy controls pass after one
partial-output retention repair.
No target geometry, perturbed-angle evaluation, or H-036 experiment ran.
The coordinator still owns the prospective freeze, target launch, and scientific
disposition; this review neither accepts H-036 nor promises that the target finishes
within ten seconds.

This is `think-w8nx`, Session 089 phase 6, W7 pipeline-improvement/correctness, reviewed
on 2026-09-06 under the `20:44:08–21:03:03 UTC` commission.
The author handed off all four paths as stable at `20:53:30 UTC`. The reviewed work
follows Git base `e70458a9`; its source paths and final controls identify the review
boundary without an additional manifest.

## Mathematical and Execution Scope

The extraction in
[restricted_orientation.py](../../../../../cases/stromquist/restricted_orientation.py)
preserves the original Theorem 3 coordinate formulas at $s_0=2+(4/3)\sqrt2$, including
the three A-points and the unchanged nine remaining twelve-set points.
It does not import the separate Theorem 2 repair.
I compared the extraction against the existing source code, the
[archived Theorem 3](../../../../../resources/papers/stromquist-2003-packing-10-or-11-unit-squares.md),
and the
[earlier independent review](bc-255-theorem3-source-control-independent-review.md).
The original source-only entry point remains source-only.

All seven conclusions remain separate: axis ten-set coverage, 45-degree avoider
localization, containment of each of the three A-points, and twelve-set coverage at both
exact angles.
The replay again returned all seven true, no escape, six 45-degree avoiding
strata, and one canonical avoiding stratum.
The counts by event-product dimension remain `[280, 526, 247]` and `[406, 841, 444]`.
These dimensions belong to the singleton/open-interval products; clipping can reduce
their geometric dimension.

The unchanged exhaustive argument includes singleton events, open intervals, clipped
segments and points, and strict localization-complement constraints.
Its vertex-average witness tests the whole feasible closure, not only the uncut cell
midpoint. The retained source regressions still check exact algebraic signs, boundary
ownership, and a nonvacuous larger-open-box witness for the forced triple.

The normalization is $K_4$ coordinate reflection, not a $D_4$ substitution.
Reflecting the whole configuration preserves the ten-set and the two exact orientations.
A concentric closed unit square lies strictly inside an enlarged open box, so positive
closed-boundary hits can support the strict-sublevel counting argument.
The reverse inference is unavailable: one escaping closed unit square is not
automatically a larger-open-box counterexample or an eleven-square packing.

The [adapter](../../../../../devtools/run_restricted_orientation_discriminator.py)
requires an explicit source or target mode.
Inspection establishes that the latter constructs exactly $1939/500$ with the unchanged
point formulas and visits only 0 and 45 degrees.
Target dispatch was mocked in every test; that construction was not executed.
No nearby-angle result follows, and both completed and interrupted receipts retain
`h036_outcome: unresolved` and `theorem_acceptance: false`.

Each exported angle follows a complete center-domain pass and direct escape replay.
The replay decodes exact power-basis coordinates and recomputes containment, both
membership masks, and the named failed clause using corner determinants rather than
event masks. Eleven independent adapter cases exercise every obstruction clause on
side-four toys, closed-corner membership, invalid containment, interrupted output, and
both timeout paths. The child receipts are trusted local progress records, not an
external proof-certificate format; complete positive decisions still rely on the
reviewed exhaustive algorithm and shared exact field.

The parent supplies a subprocess timeout and the internal worker installs its own POSIX
alarm before geometry.
Both use the requested integer cap in 1–10 seconds.
The independent test invokes the installed handler, verifies its refusal, and checks
handler restoration; the parent-timeout test checks the exact child command and absence
of a fallback. These are source/toy or mocked controls, not a measurement of a hung
target. Wrapper startup, reporting, and OS cleanup are distinct from the capped worker
time.

## Findings and Disposition

One **Medium** retention finding was repaired during review.
A nonzero worker return with a complete input/0-degree prefix and a truncated final JSON
line produced only a parse refusal, discarding the completed prefix.
The retained source-only mock failed in 0.04 seconds.
The author now treats nonzero-return output as interrupted, as the parent-timeout path
already did. The same test passes: the two completed clauses remain checked, the five
unfinished clauses remain unchecked, and the command exits nonzero.
This was lost evidence, not false mathematical acceptance.

Two **Low** publication corrections were sent to the coordinator: repair the malformed
quadratic-field notation in the author report, and describe its counts as dimensions of
event product strata rather than necessarily clipped vertices, segments, or rectangles.
Neither changes the implemented geometry.
No blocking adapter-readiness issue remains.
The small shared helper plus explicit subprocess adapter is appropriate for this slice;
an external certificate framework would add a different contract without helping this
fixed-side decision.

## Replayed Controls and Cost

Final checks ran after the stable handoff under project Python 3.14 with frozen uv and
the existing environment.
Costs are single runs on the shared host, not performance comparisons.
CPU is `/usr/bin/time -p` user plus system time.

| Check | Result | Wall seconds | CPU seconds |
| --- | --- | ---: | ---: |
| Four focused source/adapter test files | 35 passed; pytest 9.15 seconds | 9.38 | 9.33 |
| Bounded source-only CLI | Seven true; no escape; none unchecked | 1.65 | 1.64 |
| Independent test-file Ruff | Zero findings | 0.13 | 0.04 |
| Independent test-file BasedPyright | Zero errors, warnings, or notes | 0.62 | 1.08 |

The source worker reported 1.533711 wall seconds and 1.533341 CPU seconds; its
controller reported 1.586999 seconds.
No target runtime or target stratum count was measured.

From `packing/`, the final behavioral commands used this prefix:

```bash
/usr/bin/time -p env UV_CACHE_DIR=/private/tmp/squares-uv-cache uv run --frozen --no-sync --all-extras --group dev
```

The arguments were:

```bash
python -m pytest -q tests/test_stromquist_restricted_orientation.py tests/test_stromquist_restricted_orientation_review.py tests/test_restricted_orientation_discriminator.py tests/test_restricted_orientation_discriminator_review.py --durations=5
python -m devtools.run_restricted_orientation_discriminator --source-control --timeout-seconds 10
```

Ruff and BasedPyright used the same prefix on
`tests/test_restricted_orientation_discriminator_review.py`. Initial tooling calls
stopped before validation because the default uv cache was not writable; a temporary
cache path and `--no-sync` used the existing environment without installing
dependencies.

Only the independent test file and this report were authored by the reviewer.
Git, registries, experiments, beads, shared session records, and the author’s files
remain coordinator or author owned.
Experiment-loop and tbd kept controls separate from target authority; Practical
Prose/de-slop and Flowmark guided this retained report.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
