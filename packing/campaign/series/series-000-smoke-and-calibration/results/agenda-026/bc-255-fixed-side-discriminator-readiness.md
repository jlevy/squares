# BC-255: Fixed-Side Discriminator Readiness

Status: author control checkpoint, 2026-09-06; independent adapter review and
coordinator acceptance pending.
The original exact-angle source review was accepted by the coordinator before this
commission. This is BC-255 / H-036 / `think-rpzg`, Session 089 phase 6, W7
pipeline-improvement/correctness, commissioned for `20:33:03–21:03:03 UTC`. No
target-side or perturbed-angle geometry was evaluated.

The separate
[discriminator command](../../../../../devtools/run_restricted_orientation_discriminator.py)
is implemented. Its source control returns all seven original obligations true, with
unchanged source coordinates and stratum counts.
The 39 focused source, adapter, and architecture tests pass.
These are instrument controls, not an H-036 outcome or a coordinator declaration of
target readiness.

## Fixed Experiment Interface

From `packing/`, the source-only command is:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_restricted_orientation_discriminator --source-control --timeout-seconds 10
```

After independent review and a separately committed prospective experiment, the one
candidate command is:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_restricted_orientation_discriminator --target-fixed-side --timeout-seconds 10
```

The second command has **not been run**. It constructs exactly $q=1939/500$ and uses the
unchanged $P_{10}$, $P_{12}$, A-triple, and $K_4$ coordinate-reflection formulas from
the [assessment](bc-255-restricted-angle-assessment.md#candidate-conditional-cover).
No side, angle, point-set, or search option is exposed.
The candidate checks only exact 0° and 45°, in that order.
The coordinator and committed experiment own authorization; the CLI does not claim to
verify a research freeze or Git history.

The [design](bc-255-angle-instrument-design.md#next-frozen-discriminator-and-price) sets
the interpretation: a completely checked escape rejects this sufficient point-set
mechanism and parks its continuous-angle extension.
It does not refute H-036. Passing all seven exact-angle clauses permits considering the
continuous-angle instrument; it does not prove any nearby angle or accept H-036.

## Exact Core and Scope

The small extraction in
[the source module](../../../../../cases/stromquist/restricted_orientation.py) shares
`point_sets(side)` and `replay_point_sets(side, ten, twelve)` with the adapter.
`source_points(field)`, `source_replay()`, and the original source-only CLI retain their
fixed source side, coordinates, and results.
The source geometry loops, clipping, membership masks, canonical region, and strict
localization-complement regions are unchanged.
A new guard refuses inventories other than ten and twelve distinct points.

All arithmetic is in $\mathbb Q(\sqrt2)$ with the positive root in $(1,2)$. At each of the
two fixed orientations, the core retains singleton events, intervening open intervals,
and every reachable product stratum, including closed containment contacts, segments,
and points. It checks the seven clauses separately:

- Axis ten-set coverage and axis twelve-set coverage.
- 45° ten-set-avoider localization to the four $K_4$ images of $R=[1,q/2]\times[0,1]$.
- Containment of each of $A_1$, $A_2$, and $A_3$ by every canonical avoider.
- 45° twelve-set coverage.

The containing side is $s_0=2+(4/3)\sqrt2$ for the source control, and only the explicit
unrun candidate substitutes $q$. No full arrangement over angles, LP, point
optimization, or eleven-square search is part of this instrument.

The strict-sublevel counting argument remains conditional on all auxiliary clauses
throughout H-036’s full angle neighborhoods.
A concentric closed unit square lies strictly inside the enlarged open square used in
that argument; this is why its boundary hits are allowed.
Only a reflection of the whole configuration is justified by $K_4$. A single escaping
closed unit square is neither an eleven-square packing nor automatically a
counterexample to the source’s larger-open-box statement.

## Returned Escapes and Interrupted Runs

Before exporting a completed angle, the adapter decodes each retained escape and
rechecks corner containment, closed point membership, and the named region/forcing
failure. This uses oriented corner determinants through `direct_membership`, not the
producer’s projection masks, event ownership, or clipped polygon.
It also compares both reported membership masks with those recomputed values.
The serializer uses canonical `poly[a,b]` coordinates; the parser permits two ASCII
rational coefficients of at most 256 characters each.
It rejects decimals, exponent notation, noncanonical fractions, unsupported degree, and
oversized input before expensive conversion where applicable.

This check is independent of the cell producer, not independent of every foundation: it
shares the exact field, fixed-angle direction function, point-set input, and direct
membership routine with the source controls.
Complete no-escape conclusions still rely on the reviewed exhaustive-stratum argument.
The command’s JSONL child receipts are local progress records, not an externally
supplied proof-certificate format.

There is one geometry worker and a thin controller.
The worker installs a POSIX alarm before constructing any geometry, including when its
internal `--worker` entry is invoked directly.
The controller also gives `subprocess.run` the same timeout, including child startup.
Integer caps are limited to 1–10 seconds and are passed to the child; unsupported or
missing modes and out-of-range caps refuse before dispatch.
Python/uv startup, controller parsing, and OS termination overhead are reported
separately from the worker’s mathematical time; ten seconds is not a promise about that
extra overhead.

An angle is exported only after its full center-domain pass and returned-escape checks
finish. If the worker stops during 45°, the completed 0° clauses remain checked and the
five 45° clauses remain unchecked.
If it stops before completing 0°, all seven remain unchecked.
Unexported work within an interrupted angle is not counted as evidence, even if the
worker had already encountered an escape.
A cut-off final JSON line is discarded, never treated as a completed angle.
Missing, duplicated, reordered, vacuous, or internally inconsistent completion records
refuse. A timeout or worker failure exits nonzero.

The final JSON always carries all seven Boolean-or-null outcomes, explicit checked and
unchecked lists, retained escapes, and `h036_outcome: unresolved` and
`theorem_acceptance: false`. A completed negative auxiliary determination is a completed
command, with status `auxiliary_obstruction_retained`; it is not reported as a proof.

## Controls and Measured Cost

The
[eight adapter tests](../../../../../tests/test_restricted_orientation_discriminator.py)
cover unchanged source results; partial/reordered/missing/vacuous receipts; unsupported
modes and caps; exact target argument forwarding with mocked execution; a mocked worker
timeout and alarm cancellation; a side-four escape and side-one closed boundary hit;
each individual failed A-point in side-four toy geometry; forged angle, side semantics,
center, and strict-box claims; and the coordinate parser’s exponent/Unicode/size guards.
The target fixtures contain protocol strings only.
They never construct its field element, point sets, event cells, or target geometry.

The source CLI returned source side `poly[2,4/3]`, ten and twelve points, no escapes,
and all seven obligations true.
Its reachable event-product stratum counts by source dimension are `[280, 526, 247]` at 0° and
`[406, 841, 444]` at 45°, matching the
[retained source control](bc-255-theorem3-source-control-slice-01.md#execution-record).
The six 45° avoiding strata and one canonical avoiding stratum are unchanged.
Clipping can lower a stratum's dimension, so these are not counts of the final clipped
vertices, segments and rectangles.

Commands ran under frozen Python 3.14 with existing dependencies and cache.
These are single-run development costs on the shared host, not isolated performance
comparisons. Process CPU is `/usr/bin/time -p` user plus system time.

| Check | Result | Wall seconds | CPU seconds |
| --- | --- | ---: | ---: |
| Original source tests before extraction | 7 passed; pytest 1.72 seconds | 2.10 | 1.95 |
| New adapter controls | 8 passed; pytest 1.62 seconds | 2.01 | 1.85 |
| Bounded source CLI | Seven clauses checked; no escape | 2.11 | 1.70 |
| Final focused source/adapter/review/boundary tests | 39 passed; pytest 12.35 seconds | 12.60 | 12.11 |
| Final focused Ruff check | Zero findings | 0.17 | 0.04 |
| Final focused Ruff format check | Three files already formatted | 0.02 | 0.02 |
| Focused BasedPyright | Zero errors, warnings, or notes | 0.94 | 1.45 |

The bounded source worker reported 1.579762 wall seconds and 1.576228 CPU seconds; the
controller reported 1.635849 seconds.
The source CLI overlapped focused lint/type checks.
No target cost or target stratum count was measured.

The final focused test command was:

```bash
/usr/bin/time -p uv run --frozen --all-extras --group dev pytest -q tests/test_restricted_orientation_discriminator.py tests/test_stromquist_restricted_orientation.py tests/test_stromquist_restricted_orientation_review.py tests/test_module_boundaries.py
```

Lint, formatting, and type commands used `ruff check`, `ruff format --check`, and
`basedpyright`, respectively, on the adapter, source module, and adapter test file, with
the same frozen uv prefix and `/usr/bin/time -p`. TDD first failed on the missing shared
helper and missing adapter module before their implementations.
Initial lint and optional-type findings were corrected; no geometry control failed.
The independent adapter reviewer reproduced a nonzero child exit with a truncated final
JSON line losing its completed prefix.
The controller now discards that unfinished line for nonzero exits as well as parent
timeouts; the final checks above follow this fix.
One intermediate combined command’s completion output was not retained, so the table
uses the complete final rerun and does not claim a sum of all worker cost.

## Review Boundary and Next Slice

The source-distinct adapter review owns any readiness conclusion.
Root owns the prospective experiment, shared records, integration gate, publication, and
scientific disposition.
The fixed-side candidate remains unrun.
The next mathematical decision, if commissioned after review, is exactly the one
ten-second command above, with no second point set or automatic longer run.

The remaining proof risks are the actual truth of the candidate auxiliary clauses,
boundary/case completeness, and transfer over the untouched ±0.25° neighborhoods.
The exact-angle adapter does not build the event-order, feasibility-event, or algebraic
boundary instrument priced by the design.
A surviving exact-angle screen is necessary for this fixed point-set extension, not
sufficient for H-036.

Only this report, the adapter, its tests, and the permitted small source extraction were
authored. No dependency, registry, bead, Git, source archive, original source-test, or
shared-view changes were made by this worker.
Experiment-loop and tbd separated instrument controls from target authority; Practical
Prose and Flowmark guided the report’s organization and formatting.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
