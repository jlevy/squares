# BC-254: Independent Pair-Separator Review

Disposition: **GO for bounded instrument readiness**, subject to coordinator acceptance
and a new prospective experiment.
The proposed target allowance remains one 30-second producer and one separately
dispatched 30-second file replay.
No target pair geometry, candidate construction, target binding roundtrip, LP, new row,
or support extension ran in this review.
H-099 remains unresolved.

This is `think-0u56`, W7 correctness, commissioned for 2026-09-06, 21:47:00–21:57:00
UTC. The author declared the five-file build stable at 21:43:14 UTC. Reviewed sources
are the [readiness report](bc-254-pair-separator-readiness.md),
[separator](../../../../../src/sqpack/full_size_density/pair_separator.py),
[producer CLI](../../../../../devtools/run_full_size_density_pair_separator.py),
[file checker](../../../../../devtools/check_full_size_density_pair_separator.py), and
[author controls](../../../../../tests/test_full_size_density_pair_separator.py).
No production-code blocker or cheaper replacement for the bounded certificate check was
found.

## Mathematical Check

The accepted family consists of contained exact unit squares with nonnegative rational
weights, deduplicated by geometry without summing repeated weights.
Each eligible pair has distinct geometry and weight sum strictly greater than one.
Exact SAT contact is handled as separation, including zero gap; only `None` selects
strict overlap.

For overlapping convex squares, the producer’s contained corners and segment
intersections include every vertex of their intersection.
Collinear shared-edge endpoints are included by closed membership.
With positive intersection area, averaging these points gives a strict interior point:
for each defining halfplane, at least one intersection vertex has positive margin.
The implementation additionally checks every square and container margin and refuses if
it cannot obtain a positive rational lower bound.
It never accepts the geometric argument in place of these exact checks.

The reader proves a positive-area box independently of the producer’s intersection and
projection routines.
Orientation-corrected edge determinants are inward distances because the validated
square edges have unit length.
Their normals have $L^1$ norm at most $\sqrt2<2$. Requiring every margin to exceed $2r$,
with rational $r>0$, proves that the whole open $L^\infty$ box of radius $r$ lies inside
both squares and the container.
Its area is $4r^2>0$. The selected pair contributes depth greater than one there; other
nonnegative weights cannot undo the violation.

The box need not avoid other squares’ boundaries.
This is sufficient to refute the weight assignment’s a.e. feasibility, but does not
produce an LP point row: such a row still needs the separately declared full-support
off-boundary guard.

The reader enumerates eligible pairs itself in canonical family order.
Each separation record must name the next pair, and its supplied unit axis must put
every corner of the first square on or below every corner of the second in projection.
This independently proves the two closed halfplanes, permitting contact.
A witness must follow the complete separated prefix and name its immediate next pair.
A no-hit result must contain a valid separation for every eligible pair.
Missing, repeated, or reordered prefix entries cannot establish either completion claim.

## Binding, Independence, and Process Boundaries

Static inspection of the retained
[exp-113 packet](../exp-113-h-099-trump-support-screen/packet.json) and binding code
confirmed the eight fixed per-member weights $(1,0,2/5,1/10,0,1/10,3/10,0)$ and parent
ceiling label $56/5$. The producer and checker reconstruct the support through their
previously reviewed distinct D4 routes, then compare the complete geometry/weight
signature. Parent version, source, support metadata, weights, and bound use exact
serialized equality; Boolean and floating stand-ins do not equal the required integer or
rational-string encodings.
The target binding paths were inspected, not executed.

The binder deliberately does not recheck parent LP rows, multipliers, or pivot history.
The next experiment must therefore pin the already accepted parent by repository path
and Git revision. Parent acceptance remains a prerequisite, not an inference from this
separator’s binding check.

Candidate-pair certificate reasoning is independent of producer SAT, edge-axis
selection, intersection construction, and eligible-pair enumeration.
The exact field kernel, square validation, canonical key, control constructors, and
packet signature remain shared.
Reconstruction validates the original source packing with its accepted SAT validator.
The passing no-producer-geometry control does not claim that this source validation
primitive was independently replaced.

The file reader bounds bytes and refuses final-path symlinks, nonregular files,
duplicate keys, floats, and nonfinite JSON values.
Rational strings receive a bounded canonical lexical check before conversion.
The outer CLI subprocess deadline covers worker startup and execution; worker alarms
also cover input loading and computation.
Failed or timed-out workers do not publish partial stdout as a valid certificate.
Prospective target commands must use the ordinary outer entry points, not the internal
`--worker` mode.

## Controls and Measured Cost

The new
[review controls](../../../../../tests/test_full_size_density_pair_separator_review.py)
add three cases without constructing a target:

- A hand-built rational toy witness, independent of the producer’s witness generator,
  passes with minimum margin $1/4$ and radius $1/16$. Radius $1/8$ is refused at the
  reader’s strict $2r$ boundary; zero radius, a square-boundary point, zero excess, and
  an unsupported no-hit replacement are refused.
- Both public worker entry points install their alarm before their input/work call,
  report unresolved with no stdout when that installed handler fires, cancel the alarm,
  and restore the prior handler.
  Signal delivery is mocked; no 30-second sleep or target dispatch is used.
- The actual reader CLI accepts the hand-built toy file with candidate-only scope, then
  refuses a symlink, directory, and duplicate-key file without publishing a result.

The final combined source/toy run passed **42 tests in 4.40 seconds** of pytest time,
with **4.65 seconds process wall and 4.56 seconds CPU** (`user 4.31`, `sys 0.25`). The
author suite includes the degree-eight rotated toy, strict rational sliver, complete
prefix mutations, triple limitation, and separate-process original/uniform source
controls. No test was skipped.

```bash
/usr/bin/time -p uv run --frozen --all-extras --group dev pytest -q tests/test_full_size_density_pair_separator.py tests/test_full_size_density_pair_separator_review.py
```

Commands ran from `packing/` with the existing frozen Python 3.14 environment.
Focused Ruff over all five Python files passed in 0.02 seconds wall; BasedPyright
reported zero errors, warnings, or notes in 0.97 seconds wall.
A review-test closure lint finding and formatting drift were corrected; the final
new-test formatting check passed in 0.02 seconds.
No production source changed.
These are single-run development costs, not target runtime measurements or total
agent-time accounting.

A checked witness retires only exp-113’s fixed weights.
Complete pair exhaustion leaves their full a.e. feasibility and H-099 unresolved: the
retained triple toy has depth $6/5$ despite no overweight pair.
Timeout or refusal also leaves the candidate unresolved.
No unchanged retry, higher-order separator, reweighting, or support extension follows
automatically.

Only the new review test and this report were written.
The coordinator owns readiness, prospective records, Git, and beads.
Experiment-loop and tbd guided the evidence boundary and source/toy controls; Practical
Prose and Flowmark guided the report.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
