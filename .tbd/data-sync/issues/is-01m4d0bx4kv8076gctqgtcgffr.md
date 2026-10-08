---
type: is
id: is-01m4d0bx4kv8076gctqgtcgffr
title: "n17: implement and preregister the first eight-state shared-centre exact LP pilot"
kind: task
status: in_progress
priority: 1
version: 4
spec_path: docs/project/research/research-2026-10-07-n17-shared-centre-lp-readiness.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
hold: null
hold_until: null
created_at: 2026-10-08T05:39:20.323Z
updated_at: 2026-10-08T19:15:43.170Z
started_at: 2026-10-08T19:15:43.156Z
---
---
title: n17 Shared-Centre LP Readiness
date: 2026-10-07
status: proposed
---
# n17 Shared-Centre LP Readiness

A future pilot can test whether the pairwise incircle relaxations remain feasible when
all pairs share the same seventeen centres.
The geometry and certificate contract below have sole-Astra mathematical review.
The bounded adapter, numerical proposal layer, pilot source, and readiness controls are
**not implemented or registered**. No LP was evaluated during this handoff, and no
runtime or exclusion is predicted.

## Accepted Evidence and Pilot Selection

The
[accepted corner-cardinality result](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-308-n11-corner-cardinality/README.md)
binds the original twenty-four cells and the current ninety-five distance-two assignment
orbits. Its capacity relaxation has survivors, which do not establish physical packings.
Use its three generated-byte roles: `corner_descriptor`, `corner_certificate`, and
`corner_replay`. Inherit the accepted cover, named catalogue, D4 actions, partition, and
theorem premises without claiming to reprove them.

The fresh finite results in
[exp313](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-313-h-321-incircle-projection-redundancy.md)
and
[exp314](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-314-h-322-incircle-disk-projection.md)
tested 228 relevant pairs across all ninety-five states.
They found 102 pairs with an extreme vertex strictly inside the fixed octagon and 114
with an extreme vertex inside the open unit disk.
Exp314 checked 1,357 exact squared norms and found zero pairs whose entire difference
hull lies in the open disk.
Both completed with fresh verification; these are route-selection results, not ordinary
assignment exclusions or census entries.

Before a target, freeze the first eight assignment records in increasing numerical
canonical-mask order and a separate accepted endpoint mask.
The endpoint must have an exact feasible thirty-four-coordinate certificate under the
same constraints as the pilot.
Its inherited root or capacity-survivor metadata is insufficient for that check.
Freeze the union of the pilot and endpoint pair rosters: some of the endpoint’s 136
pairs may be absent from exp313’s table.
Reconstruct every required pair from the original cells.
Any incomplete or unresolved pilot state prevents a complete-eight verdict; retain valid
individual certificates as partial evidence.

## Shared Geometry and Rows

At $U=1169/250$, reconstruct the closed centre domains

$$
E_i=C_i\cap[1/2,U-1/2]^2,\qquad D_{ij}=E_j-E_i.
$$

The exact original polygon $C_i$ comes from the accepted catalogue.
Keep points and segments.
An empty $E_i$ requires separate review and is refused by this narrow pilot.
For the eight signed normals $(\pm7,\pm3)$ and $(\pm3,\pm7)$, construct

$$
H_{ij}=\operatorname{conv}\!\left(\bigcup_n
   \{\delta\in D_{ij}:n\cdot\delta\ge7\}\right).
$$

Use the reviewed exact clipping and hull primitives.
Every centre of a physical unit square lies in its $E_i$. Disjoint square interiors
imply centre distance at least one, so its pair difference belongs to this outer convex
relaxation. Feasibility of the relaxation does not prove a packing.

For each state, order its occupied catalogue indices increasingly and use variables
$(x_0,y_0,\ldots,x_{16},y_{16})$. Include every facet of all seventeen $E_i$ and all 136
$H_{ij}$. A pair plane $n\cdot\delta\le b$ becomes $n\cdot(c_j-c_i)\le b$: its four
coefficients are $(-n_x,-n_y)$ at $i$ and $(n_x,n_y)$ at $j$. Give each row a stable
identity containing the source cells and plane index.
Preserve exact coefficients, right sides, and any positive normalization scale.

The standing
[`closed_planes`](../../../packing/devtools/verify_n17_kernel_certificate.py) represents
a point by four axis bounds and a segment by its supporting line in both directions and
two endpoint bounds.
Omitting these equality constraints would enlarge the wrong model.
Empty $H_{ij}$ needs an explicitly reviewed disposition; it must never be treated as a
pair with no constraints.

## Proposal and Exact Acceptance

Installed SciPy 1.17.1 supports a numerical phase-one proposal:

```python
linprog(
    c=[0] * 34 + [1],
    A_ub=[[*row, -1] for row in A],
    b_ub=b,
    bounds=[(None, None)] * 34 + [(0, None)],
    method="highs-ds",
    options={"time_limit": frozen_solver_seconds},
)
```

This minimizes $\rho$ subject to $Ax-\rho\mathbf1\le b$ and $\rho\ge0$. The centre
variables must be free; SciPy’s default nonnegative bounds change the model.
The proposed dual is $y=-\texttt{ineqlin.marginals}$, with $y\ge0$, $A^Ty=0$, and
$\sum y\le1$. A positive optimum uses $\sum y=1$. Neither floating-point status,
positive $\rho$, nor small residuals constitute proof.

Accept only one of these exact certificates:

- A rational thirty-four-vector satisfying **every** reconstructed row $Ax\le b$.
- Nonnegative rational multipliers on identified original rows satisfying $A^Ty=0$
  exactly and $b^Ty<0$. A zero gap proves no contradiction and retains boundary contact.

A dual proposal may suggest at most thirty-five supported rows.
Reconstruct its weights from $[A_S^T;\mathbf1^T]y=(0,\ldots,0,1)$, select independent
equations exactly, solve the resulting square system, then check all thirty-five
equations and the complete original row identities.
Do not silently truncate a larger proposal.
If positively scaled rows were used, map multipliers back with the retained scales
before checking the original system.
A primal basis proposal may select thirty-four independent active rows, solve them
exactly, and check the result against all rows.
Singular bases, failed reconstruction, nonfinite numeric proposals, or uncertified signs
are unresolved.

## Reusable Code and Remaining Guards

[`sqpack.exact_lp`](../../../packing/src/sqpack/exact_lp.py) uses the standard library
and `sqpack.verify`; it does not import SciPy.
Its reusable functions are:

| API | Role |
| --- | --- |
| `LinearRow`, `ExactLP` | Labelled `<=` rows with free variables |
| `solve_square_system`, `independent_rows` | Exact Gaussian solution and rank selection |
| `certify_vertex` | Exact basis reconstruction and all-row primal checks; a zero objective suffices here |
| `check_infeasibility` | Independent nonnegative-weight, cancellation, and negative-bound check |
| `prove_infeasible`, `feasible_basis`, `solve_from_scratch` | Existing exact Bland-rule search, an optional future producer |

The existing search’s 400-pivot default is a work count, not a wall guarantee.
These APIs do not enforce a 4,096-bit ceiling or a cooperative deadline inside
elimination and accumulation.
A bounded adapter must establish those checks before claiming that assurance.
HiGHS’s `time_limit` bounds its solver phase only; import, geometry, reconstruction, and
checking still need an outer supervisor.

The prospective geometry bounds are $E_i\le36$, $D_{ij}\le72$, each closed clip at most
73 vertices, and at most 584 raw clip-output vertices per pair.
Each of eight clipping lines introduces at most two new vertices, so $H_{ij}\le88$. A
state has at most $17\times36+136\times88=12,580$ rows, including the point and segment
representations. At most 276 catalogue pairs suffice for the combined pilot and endpoint
roster.

A future allocation proposes 120 seconds construction and 120 seconds fresh checking,
with a 240-second outer TERM ceiling, ten seconds for KILL cleanup, and sampled 4 GiB
current RSS per live process.
The implementation must preregister solver, reconstruction, work, output, and arithmetic
limits before any target.
This allocation has no measured feasibility or speed forecast.

## Required Readiness and Disposition

Controls must cover exact feasible and infeasible systems, zero-gap touching, degenerate
point and segment $H$, shared-centre inconsistency despite individually feasible pairs,
positive row scaling, sign-flipped marginals, a tiny false floating-point infeasibility,
singular or failed reconstruction, row omissions, byte changes, and resource stops.
Require clean-process reconstruction and the exact endpoint feasible control.
Existing
[`test_exact_lp_infeasibility.py`](../../../packing/tests/test_exact_lp_infeasibility.py)
and [`test_promote_exact_lp.py`](../../../packing/tests/test_promote_exact_lp.py)
contain relevant certificate and basis controls; they were inventoried, not rerun for
this handoff.

Fresh checking must reconstruct the selected geometry and row map, verify the exact
certificate, compare mathematical payloads, and recheck all named generated inputs after
proof work. Curated source identity remains Git provenance.
A verified contradiction can support only a separately reviewed ordinary-assignment
result; any census admission still needs the standing composition and deduplication
contract. A verified primal is a relaxation survivor.
Resource exhaustion is incomplete; absence of a certificate is unresolved.
No new LP engine, pilot result, ordinary admission, or global bound is established by
this readiness handoff.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->

## Notes

Astra read-only intake of [#413's 07:47 update](https://github.com/jlevy/squares/issues/413#issuecomment-6055253328):
31 reported patterns comprise four reported standing-FULL passes, sixteen fast-verifier-only
passes and eleven computed results. Row 19 moves into the fast-only group; rows 30 and 31
are new computed results. None changes the admitted census, unresolved roster or bound.

Preserve the reviewed first eight canonical shared-centre P8 assignments and the separate
exact endpoint calibration. A square-placement exclusion does not imply this weaker LP
is infeasible; LP survival does not contradict such an exclusion. No LP was run here.
The bounded adapter and arithmetic/deadline guards still need implementation.

Before expensive new exclusion targeting, `think-ewea` reconciles all 31 patterns by
exact catalogue, frame, cap, closed angle domain, boundary convention, guards and D4
equality versus containment against the 60 admitted classes, current 95-orbit roster and
first eight. Unadmitted overlap is scheduling metadata. Repackaged rows 1–4 and #358
require fresh manifest identities. The reported floating placement for class `14355456`
is neither an exact packing nor a seventeen-square assignment certificate.
PR410 kernel qualification does not discharge branch-and-bound certificate intake.

The immutable [LP readiness contract](https://github.com/jlevy/squares/blob/ecb0bf82c38958089c7a41aa3980ce62dcc848b8/docs/project/research/research-2026-10-07-n17-shared-centre-lp-readiness.md)
and [issue coordination contract](https://github.com/jlevy/squares/blob/ecb0bf82c38958089c7a41aa3980ce62dcc848b8/docs/project/reviews/review-2026-10-07-n17-issue-coordination.md)
retain the proof premises and acceptance requirements.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
