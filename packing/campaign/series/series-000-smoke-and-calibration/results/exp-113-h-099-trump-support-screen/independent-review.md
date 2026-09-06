# exp-113: Independent Protocol and Output Review

Review disposition: **GO for the checked finite-row result.** The one independent file
replay passed with exact optimum $56/5$. This exceeds eleven, so H-099 remains
unresolved. The retained primal weights are not certified almost-everywhere feasible.
This reviewer ran no optimizer or separate target-generation command.

This review is tracked by `think-ez3v` under target commission `think-2rxf`, with a
commissioned window of `2026-09-06T20:45:50Z`–`2026-09-06T21:00:50Z`. The coordinator
owns Session 089 phase 7, experiment recording, hypothesis disposition, and acceptance.

## Protocol and Source Checks

The [prospective experiment](../../experiments/exp-113-h-099-trump-support-screen.md)
preserves
[H-099’s criterion](../../../../hypotheses/H-099-trump-d4-finite-support-dual.md) and
the limits established in the
[instrument review](../agenda-026/bc-254-target-readiness-independent-review.md).
The selected source is `trump11-v1`, and the engine revision is
`e70458a9c40cfab46d2f2233b0dfbb47501a4de8`. A read-only Git comparison found no
difference between that revision and the seven reviewed density implementation/test
files. The coordinator committed the prospective protocol at `b3046532` before target
execution. Before replay, the reviewer checked that the isolated checkout
`/private/tmp/squares-launch-check.Y1eqVE` had the frozen HEAD and a clean Git status.
The coordinator reported that the pre-execution record gate passed all 31 selected
checks at `cc18f64c`; this reviewer did not rerun that shared gate.

The protocol fixes the exact Trump D4 support, center-first sequence and conditional
dyadic extension, exact arithmetic, zero start with the negative identity active basis,
at most two solves with 64 pivots each, and a 60-second producer cap.
It separately allocates one file replay with its own 60-second cap.
Startup, teardown, and review costs are distinct from worker time.
No unchanged retry is authorized after timeout, pivot refusal, malformed output, or a
missing premise.

The reviewed source control preserves all 88 labelled preimages on 60 distinct
placements in eight orbits and has exact feasible mass eleven.
The protocol admits no new placement, direction, grid, basis, or solver.
A failed producer’s empty stdout is not a certificate.
Refusal or incomplete output remains unresolved and must not become a mathematical
negative.

The existing producer and checker are appropriate for this bounded discriminator; no
additional arrangement implementation or alternate solver is needed to test an upper
ceiling. Exact field arithmetic, source validation, scalar checks, and sequence
generation are shared.
The determinant incidence calculation and explicit D4 maps are separate, and file replay
never invokes optimization.
These are the independence limits already disclosed before execution, not an
execution-history attestation.

## Consequence Boundary

Every admitted incidence row has a certified positive-area neighborhood, so every
almost-everywhere feasible weighting on this support satisfies that row.
D4 averaging preserves feasibility and total weight, allowing one variable per orbit
without losing a feasible mass.
For a replayed nonnegative upper witness $y$,

$$
A^T y\geq m,\qquad m^Ta\leq y^TAa\leq\mathbf1^Ty=V.
$$

If $V=11$, this upper bound and the retained feasible mass-eleven average establish that
the maximal feasible mass on the specified finite support is exactly eleven.
That rejects H-099’s fixed-support claim.
It neither constructs a mass-eleven area density nor proves global packing optimality or
a global continuum-dual ceiling.

If $V>11$, even a matching feasible finite-row primal point leaves H-099 unresolved:
finite rows do not prove almost-everywhere depth.
A reported value below eleven contradicts the retained feasible control and must be
refused. These conclusions use the
[BC-242 semantics](../agenda-026/bc-242-full-size-density-proof-contract.md), without
assuming strong duality or attainment for the continuum problem.

## Output Review

The coordinator dispatched the completed [packet](packet.json) after producer exit zero.
The reviewer invoked the frozen file checker exactly once, starting at the observed
clock `2026-09-06T20:58:01Z`, from the isolated checkout’s `packing/` directory.
The command used the existing Python 3.14 interpreter, with no UV synchronization or
dependency change:

```shell
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 PYTHONPATH=src /usr/bin/time -p /Users/levy/wrk/github/squares/packing/.venv/bin/python3 -m devtools.check_full_size_density_support_ceiling /Users/levy/wrk/github/squares/packing/campaign/series/series-000-smoke-and-calibration/results/exp-113-h-099-trump-support-screen/packet.json --timeout-seconds 60
```

Standard output was retained in [replay.json](replay.json), and standard error and
`time` output in [replay.log](replay.log).
The checker exited zero, reporting:

```json
{"finite_row_optimum": "56/5", "scope": "specified finite support only; no almost-everywhere depth claim"}
```

The packet contains 20 admitted rows and pivot receipts `[6, 8]`, within the frozen
limits. Its orbit primal is $(1,0,2/5,1/10,0,1/10,3/10,0)$. The nonzero upper
multipliers, at zero-based row indices $(0,3,7,10,18,19)$, are
$(4/5,16/5,16/5,8/5,4/5,8/5)$. Substitution into the retained rows gives
$A^Ty=(4,8,8,8,8,8,8,8)=m$ and $\mathbf1^Ty=(4+16+16+8+4+8)/5=56/5$. The primal
objective is $4+8(2/5+1/10+1/10+3/10)=56/5$.

The checker verified every row’s source binding, determinant incidence, positive
neighborhood, rational upper inequality, matching primal objective, and the mass-eleven
source control. It regenerated the fixed sequence within that authorized replay; the
reviewer ran no separate row-generation command.
Pivot counts remain execution receipts, not independently attested solver history.

| Process | Exit | Wall seconds | CPU seconds |
| --- | ---: | ---: | ---: |
| Coordinator producer, from retained [run.log](run.log) | 0 | 19.69 | 17.36 |
| Reviewer’s one file replay | 0 | 9.10 | 9.06 |

CPU is retained user plus system time.
The producer log separately reports worker wall time `19.561851291917264` seconds and
CPU `17.245133` seconds, excluding outer startup and teardown.
The reviewer observed replay completion by `20:58:31 UTC`. Neither process hit its cap,
and neither was retried.
These are single-run costs, not statistical performance comparisons.
Peak memory was not measured.

The maximum almost-everywhere feasible mass on this fixed support therefore lies between
$11$ and $56/5$. The upper endpoint is attained for the finite-row relaxation, not yet
for the complete depth constraints.
The experiment neither rejects nor confirms H-099. Complete depth verification remains a
scientific dependency; this result authorizes no extra grid or support extension inside
exp-113.

No Blocker, High, Medium, or Low finding was identified in the protocol or dispatched
output. Coordinator disposition, shared validation and publication remain separate from
this independent evidence check.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
