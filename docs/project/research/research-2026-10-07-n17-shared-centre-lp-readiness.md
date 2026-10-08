---
title: n17 Shared-Centre LP Readiness
date: 2026-10-07
status: in-progress
---
# n17 Shared-Centre LP Readiness

A future pilot can test whether the pairwise incircle relaxations remain feasible when
all pairs share the same seventeen centres.
The geometry and certificate contract below have sole-Astra mathematical review.
The [guarded endpoint adapter](../../../packing/devtools/n17_shared_centre_lp.py) and
synthetic geometry, custody and resource controls are implemented.
Publication, custody and resource controls passed; the original endpoint round is
recorded as
[H-323](../../../packing/campaign/hypotheses/H-323-shared-centre-endpoint-control.md).
The separate explicit-f1 correction is registered as
[H-324](../../../packing/campaign/hypotheses/H-324-shared-centre-explicit-f1-control.md)
after sole-Astra final action/custody review and all43 synthetic controls passed.
The real corrected endpoint is unrun at registration.
The numerical proposal layer and first-eight pilot remain unimplemented and unexecuted;
no LP runtime or exclusion is predicted.

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

## Endpoint Instrument and Remaining Guards

The endpoint adapter reconstructs every required original-cell domain, all 136 pair
domains and their labelled rows.
Its exact scalar wrapper enforces the operation, cooperative deadline and
reduced-Fraction bit limits throughout the new geometry, centre transformation and
primal checks. Accepted-role and YAML parsing, `build_cover`, D4 reconstruction and
physical witness validity remain inherited premises; they are not claimed as a new
guarded reproof.

The accepted
[exp-235 rational witness](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-235-n17-rational-upper/portable-witness.yaml)
has side $S=4675530093604551/10^{15}<U$. The original H-323 control used exact corner
means translated by $(U-S)/2$, with registered rotation $r3=(y,U-x)$.
[Exp315](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-315-h-323-shared-centre-endpoint-refusal.md)
refused the canonical-mask guard before E/D/H construction or primal checking; fresh
verification was unstarted.
All original-cell membership checks passed.
The accepted raw assignment mask is `3439615`; r3 gives `3730943`, while the unique
canonicalizing action f1 gives `1900015`, with coordinates $(U-y,U-x)$. The design and
source review missed this finite metadata join.
The original criterion, manifest and receipts remain unchanged and unresolved;
correcting the premise needs a separate prospective registration and establishes no
contradiction or feasibility result.

The [synthetic controls](../../../packing/tests/test_n17_shared_centre_lp.py) exercise
closed touching, points and segments, complete pair and row custody, source label
mapping, changed bytes, reduced-rational intermediate growth, deadlines and operation
exhaustion. These controls do not evaluate the physical endpoint or the first eight.
The standing registered-phase runner and POSIX supervisor provide separate phase
processes and owned-group wall, sampled-RSS and cleanup evidence.

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

## Minimal First-Eight Extension

Astra’s bounded source review identifies a smaller producer path after the endpoint
control.
Build each required cell and pair domain once per process: the union contains at
most 24 cells and 276 pairs.
Fresh checking constructs its own cache from the held inputs; it never accepts the
producer’s cached geometry as a premise.

Use one bounded numerical proposal per state with identity row scaling.
First try the proposed finite coordinates or at-most-thirty-five supported dual weights
as exact binary rationals.
Accept only a complete exact primal or Farkas check.
If that fails, permit one proposed basis/support reconstruction per state; singular
bases, excess support and failed exact signs remain unresolved.
Do not scan alternate bases or run exact simplex in this slice.

`solve_square_system` preserves its caller’s scalar operations when every matrix entry,
right side and its `one` are `Guarded`. This avoids shared solver edits and an exact
independence prepass.
The reviewed worst-case scalar count for size $k$ is
$k(k+1)/2+k+k(k+1)+k(k-1)+2k(k-1)(k+1)$: 81,481 operations/comparisons at size 34 and
88,795 at size 35. A prospective 100,000-operation reconstruction subcap covers the
solve and small dual check; it excludes the full all-row primal pass and remains
subordinate to separately registered aggregate limits.

Derive the two containment or four pair coordinate indices from freshly reconstructed
rows. Evaluating those terms checks every inequality while avoiding the dense scan of 34
coefficient-zero tests per row.
At the row ceilings, one sparse pass needs at most 110,806 checked operations, compared
with 538,526 for the current dense scan.
These are algebraic work bounds, not elapsed-time measurements or an executed pilot.

The extension still needs controls for guarded elimination growth/deadlines, singular or
incorrect bases, row/support mutations, negative weights, zero gap, failed cancellation,
false floating-point infeasibility, shared-centre inconsistency and
sparse-versus-complete evaluation with closed degeneracies.
Its allocation must be registered separately; H-323’s 120-second phase limits do not
allocate the eight-state experiment.

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
The endpoint adapter supplies the geometry and primal-reading seam for a future LP
producer. Exact Gaussian reconstruction and Farkas checking still need bounded adapters
before the numerical proposal layer can be qualified.
No first-eight pilot result, ordinary admission or global bound is established here.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
