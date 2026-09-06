# A Quantitative Local Theorem at Trump’s 11-Square Packing

Status: BC-240 terminal author packet, awaiting the source-distinct BC-241 review.\
Launch revision: `c55726e1e885227f63110131c0a914665175ff89`.\
Official T+0: `2026-09-06T03:31:00Z`.

Walter Trump’s exact 11-square placement is quantitatively isolated in one labelled,
anchored, fixed-side chart.
The preferred retained constants give a sup-norm radius of at least

`rho_row = 808514697/200000000000 = 0.004042573485...`

and a quadratic side constant of at most

`C_row = 2574612531/200000000 = 12.873062655`.

These constants do not establish global optimality, global uniqueness, or capture of a
different contact type.
The theorem is local to the chart and active-feature packet defined below.

## Exact Witness and Chart

Let `u` be the unique root in `(36/100, 37/100)` of

`5u^8 - 10u^7 - 2u^6 + 14u^5 + 12u^4 - 6u^3 + 2u^2 + 2u - 1`.

Put

`U = (6u + 4)/(1 + 2u - u^2)`.

The exact witness in [`packing.py`](packing.py) has

`U = 3.87708359002281417730789706010096270637645566846...`,

and `U` satisfies

`U^8 - 20U^7 + 178U^6 - 842U^5 + 1923U^4 - 496U^3 - 6754U^2 + 12420U - 6865 = 0`.

Anchor the container as `[0,U]^2`, with its lower-left corner fixed at the origin, and
retain the square labels from `packing.py`. A chart point is

`z = (x_0, y_0, theta_0, ..., x_10, y_10, theta_10) in R^33`.

Square `i` has centre `c_i = (x_i,y_i)` and corners

`c_i + R(theta_i) q_m`, where `q_m` runs through `(+-1/2,+-1/2)` in the retained corner
order. Angles use the local representatives at the exact witness; this chart does not
cross a quarter-turn identification.
They are measured in radians.
The chart norm is

`||z-z_*||_infinity = max_k |z_k-z_{*,k}|`.

Here a packing means that every closed unit square lies in the container and distinct
squares have disjoint interiors; boundary touching is allowed.

The side is fixed at `U` in the 33 chart variables.
A varying side is written `U + sigma` separately; it is not a thirty-fourth coordinate
in the stated norm. The curvature calculation is valid on the declared box
`||z-z_*||_infinity <= 1/64`.

The proof does not quotient the local coordinates by symmetry.
The labels and angle representatives stay fixed.
The retained exact matching guard places every distinct `D4` image and relabelling
beyond a threshold of `1/8`; the theorem uses the exact half-distance cap `1/16`. For
the cone and modulus arguments, a hypothetical nonzero displacement is normalized to sup
norm one. Its unit sphere is the union of the 66 faces obtained by fixing one of 33
coordinates to `+1` or `-1`. Stress scale is irrelevant: the proof uses positivity,
`A_b^T lambda_b = 0`, positive far-wall stress, and scale-invariant stress ratios.

## Theorem

Let `z_*` be Trump’s exact labelled pose from `packing.py`. Define the two retained
constant pairs

| Derivation | Radius lower bound | Quadratic constant upper bound |
| --- | ---: | ---: |
| Uniform curvature | `rho_uniform = 288616983/125000000000` | `C_uniform = 2808470331/125000000` |
| Per-row curvature | `rho_row = 808514697/200000000000` | `C_row = 2574612531/200000000` |

The per-row pair is the preferred invocation.
Both pairs use the same labelled, anchored sup-norm chart.

For either row of the table, write its constants as `(rho,C)`.

1. **Fixed-side isolation.** If `z` is a labelled packing of the 11 closed unit squares
   in `[0,U]^2` and `||z-z_*||_infinity < rho`, then `z = z_*`.

2. **Side stability and equality.** Suppose the same labelled pose fits in `[0,s']^2`,
   anchored at the same origin, where `s' <= U` and `||z-z_*||_infinity < rho`.
   Embedding `[0,s']^2` in `[0,U]^2` and applying the first conclusion gives `z = z_*`.
   Because `z_*` touches all four walls of its exact container, `s' = U`. Thus equality
   in this local side comparison occurs only at the retained labelled pose.

3. **Quadratic side bound.** Let `v = z-z_*`. A feasible pose at side `U + sigma` in the
   same ball satisfies

   `sigma >= -C ||v||_infinity^2`.

The gap and branch-completeness guards in the retained calculation ensure that every
feasible pose in the stated ball selects one of those branches.
The theorem therefore does not assume a branch chosen by an external heuristic.

## Proof From the Retained Certificates

The exact witness check establishes containment, all 55 pair separations, the 14
zero-gap pair contacts, the 20 corner coordinates on the boundary, and the degree-eight
number-field identity.

At `z_*`, 11 square-wall incidences contribute 20 wall tangent rows, and 14 pair
contacts contribute 24 raw zero-gap separating-axis features.
The complete wall active set is:

| Square | Wall | Supporting corners | Tangent rows |
| ---: | --- | --- | ---: |
| 0 | left | 0, 3 | 2 |
| 0 | bottom | 0, 1 | 2 |
| 1 | right | 1, 2 | 2 |
| 1 | bottom | 0, 1 | 2 |
| 2 | top | 2, 3 | 2 |
| 3 | left | 0, 3 | 2 |
| 3 | top | 2, 3 | 2 |
| 4 | top | 2, 3 | 2 |
| 5 | left | 0, 3 | 2 |
| 7 | bottom | 0 | 1 |
| 10 | right | 1 | 1 |

The complete pair-contact active set and its local option counts are:

| Pair | Raw feature options | Derivative-distinct options | Rows after selecting one option |
| --- | ---: | ---: | ---: |
| 0–6 | 1 | 1 | 1 |
| 1–9 | 1 | 1 | 1 |
| 2–8 | 1 | 1 | 1 |
| 2–10 | 1 | 1 | 1 |
| 3–4 | 2 | 1 | 2 |
| 3–5 | 2 | 1 | 2 |
| 4–5 | 4 | 4 | 2 |
| 4–8 | 1 | 1 | 1 |
| 5–6 | 1 | 1 | 1 |
| 6–7 | 2 | 2 | 2 |
| 6–8 | 2 | 2 | 2 |
| 7–9 | 2 | 2 | 2 |
| 8–9 | 2 | 2 | 2 |
| 9–10 | 2 | 2 | 2 |

The two raw features for 3–4 are exact derivative aliases, as are the two for 3–5.
Across the 14 contacts, 24 raw feature options therefore collapse to 22
derivative-distinct local options; the raw option product is 512, and exact derivative
deduplication gives 128 branches.
Independently, every selected branch has 22 pair tangent rows, so its 20 wall rows make
a 42-row matrix. Pairs `(0,4)` and `(2,5)` each have an incidental zero projection but
also a strictly separating feature; they are locally interior and contribute no active
row. Every `A_b` has 33 columns and exact rank 33. The exp-013 record retains the full
512-to-128 map.
For every branch `b`, it also retains an exact positive stress `lambda_b`
satisfying

`A_b^T lambda_b = 0`,

and an exact full-rank certificate.
If `A_b v >= 0`, then the positive weighted sum `lambda_b^T A_b v` is zero.
Every row product is therefore zero, and rank 33 forces `v = 0`. The exact replay
confirmed this conclusion for all 128 branches, with no unresolved cone.

For a quantitative bound, BC-199 defines

`kappa_b = min_{||w||_infinity=1} max_j (-(A_b w)_j)`.

The retained radius computation solved the 66 faces of the 33-dimensional unit cube for
every branch, using floating arithmetic only to propose candidates and exact arithmetic
for the bounds and deciding vertices.
The uniform and row-weighted passes each contain 8,448 face programs, for 16,896 across
the two passes. It found two exact modulus classes: the minimum lower value is
`0.011480272061506444...`, while the other class has lower value
`0.016423844897818726...`. All 128 branch moduli were completed.

Let `g_j` be an active wall or pair-separation function.
On the declared box, the uniform calculation bounds its second-order remainder by

`|R_j(v)| <= (K/2) ||v||_infinity^2`,

with `K = 4972105219/500000000`. The per-row calculation retains the corresponding
row-specific bounds.
For a feasible point at side `U + sigma` with `sigma <= 0`, an active branch row has

`a_j v + sigma e_j + R_j(v) >= 0`,

where `e_j` is one on the right and top wall rows and zero elsewhere.
Since `sigma e_j <= 0`, every row obeys

`a_j v >= -(K/2)||v||_infinity^2`.

The modulus supplies a row with

`a_j v <= -kappa_b ||v||_infinity`.

For nonzero `v`, these inequalities force

`||v||_infinity >= 2 kappa_b/K`.

Taking the minimum over the branches and then the declared-box, inactive-gap, and
symmetry caps gives the uniform lower bound `rho_uniform`. For the per-row pass, let
`K_j` bound the second-order remainder of row `j` and scale that row by `2/K_j`. The
retained weighted modulus is

`kappa_b^row = min_{||w||_infinity=1} max_j (-(2/K_j) a_j w)`.

The same two inequalities force `||v||_infinity >= kappa_b^row`, which gives `rho_row`
after the shared caps.
The binding caps are the respective modulus bounds.
The other uniform caps are `1/64` for the declared box, at least `0.005875508797...` for
inactive-feature stability (with retained short lower bound `5875508797/1000000000000`),
and `1/16` for symmetry.
They are all larger than `rho_uniform`; the retained per-row minimum likewise binds
before the shared caps.

At `v = 0`, a far-wall row requires `sigma >= 0`. This proves the fixed-side and
side-stability conclusions.
Multiplying the branch inequalities by `lambda_b` cancels the linear terms.
If `Lambda_b > 0` is the stress on the right and top wall rows, then

`sigma Lambda_b + sum_j lambda_{b,j} R_j(v) >= 0`.

The uniform remainder bounds give

`sigma >= -(||lambda_b||_1 K/(2 Lambda_b)) ||v||_infinity^2`.

The retained exact stress identity shows that `||lambda_b||_1/Lambda_b` is invariant on
each branch stress cone and agrees across all 128 branches.
Maximizing the resulting constant gives `C_uniform`. Applying the retained per-row
remainder sum gives the smaller `C_row`. This proves the quadratic clause.

## Machine-Checkable Assumptions and Inputs

The theorem depends on these immutable or hash-bound inputs:

| Input | SHA-256 | Role |
| --- | --- | --- |
| `packing/campaign/series/series-000-smoke-and-calibration/results/exp-013-h-026-trump-tangent.json` | `60a4b7c48034b37063509a8a641974ed5eae86dccd056e9cbc6cf2fd7f2f0661` | 512-to-128 branch map, exact stresses, and exact tangent certificates |
| `packing/campaign/series/series-000-smoke-and-calibration/results/bc-199-trump-isolation-radius.json` | `db124b9956d8051682388cbba3b16772e65406a0003debba1c92b915c0c489a8` | Per-branch moduli, curvature bounds, caps, radii, and quadratic constants |
| `packing/cases/trump11/packing.py` | `3b4eae938c37c13af6252ac5d83fa99aa95f6b1627b99920c5df8be94c56bea9` | Exact witness and side identity |
| `packing/cases/trump11/tangent_cones.py` at the BC-199-producing revision | `31f1c09ff296fdb99a8f6e1f26803350c043796029c40c43b33c1d5637e8dc86` | Record-producing tangent implementation |
| `packing/cases/trump11/tangent_cones.py` at launch | `17302de574d9f7bc377cbc1dc4c537dc60976d6a1e4e63432adb5fa184058765` | Current exact replay implementation |
| `packing/cases/trump11/isolation_radius.py` at launch | `3b4f754b8a77c0a6edb12a8f669e705594817992f9983956d308aa7b343031b4` | Retained radius derivation source; not executed in BC-240 |
| `packing/cases/trump11/verify_exact.py` at launch | `29156a613a23fa8a9e915500d71841938bb714b9b7669c23dbcb973463071c52` | Exact witness verifier |

The current `tangent_cones.py` differs from the record-producing revision only by
removing an unused `field` argument from `exact_pivot_rows` and adjusting its callers.
The exact record replay passed with the current source.
The BC-199-producing `isolation_radius.py` has SHA-256
`56a2c6f474f1e236eb33d2dbdd799c7a88310de57ab4f7998d98755cc8065bc4`. The current source
adjusts two calls for the removed argument and expands a provenance comment on
Archimedes’ bounds.
The BC-199 result did not freeze the generator’s own source hash; the
table records its launch hash and this comparison without upgrading either source
version to a frozen input or replaying the generator.

The following guards are premises of the packaged theorem and were true in the retained
records or the author replay:

- `u` is squarefree and irreducible over the rationals and has exactly one root in its
  isolating interval
- the exact witness is valid and its published side polynomial vanishes
- the local active inventory contains all 512 raw selections and maps them to 128
  derivative-distinct 42-row systems
- every one of the 128 tangent systems has an exact zero-cone certificate and none is
  unresolved
- all 128 modulus calculations completed, each branch row matches a tied elementary
  gradient, and the box, gap, and symmetry caps remain above the quoted radii
- all rational bounds use the anchored 33-variable sup norm stated here

## Author Replay

The author ran two retained checks from `packing/` at launch revision
`c55726e1e885227f63110131c0a914665175ff89`. Both used the project environment’s Python
3.14.7 interpreter; the environment’s `python` symlink resolves to
`/opt/homebrew/opt/python@3.14/bin/python3.14`.

```sh
uv run --frozen python -m cases.trump11.verify_exact
```

It exited zero and reported:

```text
Exact verification of Trump's 11-square packing
VALID: 11 squares, 55 pairs tested
  container: 20 corner coordinates exactly on the boundary
  pairs:     14 separated with zero gap, 41 strictly
  field:     Q(u), degree 8, u = tan(a/2)
  interval refinements needed: 0
  wall time: 0.139 s
  P(s) == 0 for the published degree-8 polynomial: True
  s = 3.87708359002281417730789706010096270637645566846
  published (Ellsworth, 33 digits):
      3.87708359002281417730789706010096
```

```sh
uv run --frozen python -m cases.trump11.tangent_cones \
  --replay campaign/series/series-000-smoke-and-calibration/results/exp-013-h-026-trump-tangent.json
```

It exited zero and reported:

```json
{
  "branch_count": 128,
  "determination_outcome": "criterion_met",
  "elapsed_seconds": 11.023023,
  "exact_nonzero_directions": 0,
  "exact_zero_certificates": 128,
  "raw_branch_count": 512,
  "record_replayed": true,
  "schema_version": 1,
  "selftests": {
    "duplicate_branch_records_are_rejected": true,
    "flexible_cone_has_no_positive_stress": true,
    "rigid_cone_has_positive_stress": true,
    "trump_wall_omission_has_exact_nonzero_direction": true,
    "u_interval_contains_exactly_one_root": true,
    "u_polynomial_irreducible_over_Q": true,
    "u_polynomial_squarefree": true
  },
  "unresolved_cones": 0
}
```

An initial login-shell invocation of the witness command exited before Python started
because the managed environment denied `fnm` state and the default uv cache.
The exact command then ran unchanged in a non-login approved environment.
This operational retry produced no alternate scientific result.

After both checks completed, the coordinator advanced the shared checkout to
`15514b502e68f3a2f1a4dfea6f2e80795664bdcf` for an unrelated CI-only fix.
A static diff from the launch revision across the six hash-bound theorem inputs was
empty. BC-240 remains bound to the launch revision, and neither check was repeated after
the shared HEAD changed.
Upstream reconciliation later passed through merge
`a70e002e690725ce4c576caf8c057bee25ff3479` and CI-only revision
`8cc0af436b0249db8cc8f44e2a6659a573aeda08`. The coordinator again reported an empty
launch diff across all six inputs and agenda-026. No scientific command was restarted.
Before the author’s terminal declaration, the shared checkout advanced again to merge
`c44562409e7b48578df99fcae9e1cf61856158bc`, joining the 8cc0af43 line with c743d7bb.
This is a shared-head provenance update only: BC-240 remains launch-bound, and no
scientific command was repeated.

## Replay Boundary and Refusals

BC-240 did not run `cases.trump11.isolation_radius`. That program has `--record` but no
`--replay`, and the BC-199 artifact does not retain every per-face primal and dual
witness from either 66-face-per-branch modulus pass.
The tangent replay and byte-identical BC-199 aggregate therefore do not constitute an
independent replay of the radius calculation.
BC-241 must review the aggregate arithmetic and selected generator steps from sources
distinct from this author.

The packet refuses each stronger statement:

- no full radius-generator replay or recreation of the missing per-face witnesses
- no theorem in an unanchored chart or a chart that includes side as a normed variable
- no assertion about a different labeling or contact type outside the certified ball
- no global optimality, global uniqueness, or global capture theorem for `s(11)`
- no change to the frontier or the standing description of Trump’s construction as the
  verified known best

## Unexecuted BC-241 Control Matrix

The source-distinct reviewer should first verify the frozen hashes, classify all source
drift, replay the exact exp-013 tangent endpoint, recompute the aggregate rational
minimum, caps, and norm conversions from BC-199, and audit selected branch and face
calculations against the archived generator source.
It should then run these falsifying controls:

| Control | Mutation | Required refusal |
| --- | --- | --- |
| Active-row identity | Change one coefficient in a retained active row before matching it to the elementary functions | Exact row identification no longer matches the tied elementary gradient |
| Branch sign | Multiply one selected separating-axis row by `-1` while retaining its recorded stress | The exact stress residual or retained branch signature no longer verifies |
| Norm conversion | Replace one per-row factor `2/K_j` by `1/K_j` | The weighted modulus no longer reproduces the retained preferred radius; the norm-conversion comparison rejects it |

The BC-240 author is not eligible to certify those controls.

## Manifest and Review Notes

BC-240 writes only this document and
`packing/campaign/series/series-000-smoke-and-calibration/results/bc-240-trump-local-theorem.json`.
It does not edit an agenda, campaign ledger, frontier record, schema, tbd state, or Git
reference. The JSON companion carries the same constants, input hashes, replay outputs,
claim boundary, and unreviewed obligations in machine-readable form.

At the author’s terminal static snapshot, JSON parsing, Flowmark checking, whitespace
checking, retained-record comparison, input hashing, and the launch-to-current input
diff all passed. Every author-started command had returned and no background command
session had been opened.
Host-wide `pgrep` and `ps` enumeration were unavailable in the managed sandbox, so this
packet does not substitute that bounded session evidence for the coordinator’s host-wide
no-process check.

Review should reject the packet if a constant does not match the retained BC-199 bytes,
if the chart or norm changes, if any branch is unresolved, if the current source drift
is not semantics-neutral, or if local isolation is used as a global conclusion.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
