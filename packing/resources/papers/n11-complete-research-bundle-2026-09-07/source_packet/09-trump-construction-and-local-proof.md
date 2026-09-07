# Trump's Exact Construction and Local Closure

The full formulas and local theorem follow. The source theorem's 'awaiting review' line predates BC-241; the review-scope extract at the end records the later review. Numerical radius constants remain dependent on retained branch records, without a new independent replay of the entire radius generator. Formula code specifies every corner in Q(u); it can be transcribed into any exact algebra system, but its sqpack import is not bundled. File 18 is the local diagram. Large per-branch proof receipts are summarized, not reproduced.

<a id="source-1"></a>

## Source 1: `packing/cases/trump11/packing.py`

Snapshot `4d305597a505`, source lines 1-end.

```python
"""Walter Trump's 1979 packing of 11 unit squares, exactly.

This is the best known packing for `n = 11`, the smallest case where `s(n)`
is unknown, and the smallest where the optimal packing is believed to need a
tilt that is neither 0 nor 45 degrees.

The layout is reconstructed from David Ellsworth's SVG on the *Squares in
Squares* record page: six axis-aligned squares plus a block of five rotated
by `a`, where the block's offsets `x0, r1, u1, v1, v2` are the closed forms
given there.

Everything is expressed in `Q(u)` with `u = tan(a/2)`, so `cos a` and
`sin a` are rational in `u` and no transcendental function appears.  The
minimal polynomial of `u` is derived in `derive_field.py`; the container side
is then `s = (6u + 4) / (-u^2 + 2u + 1)`, whose minimal polynomial is the
published degree-8

    s^8 - 20s^7 + 178s^6 - 842s^5 + 1923s^4 - 496s^3 - 6754s^2 + 12420s - 6865
"""

from __future__ import annotations

from sqpack.field import NumberField

# Minimal polynomial of u = tan(a/2), highest degree first, and an isolating
# interval containing the intended root (a is about 40.18 degrees).
U_MIN_POLY = (5, -10, -2, 14, 12, -6, 2, 2, -1)
U_INTERVAL = ("36/100", "37/100")

# Minimal polynomial of the container side, as published.
S_MIN_POLY = (1, -20, 178, -842, 1923, -496, -6754, 12420, -6865)


def build():
    """Return ``(squares, side, field)`` for Trump's packing.

    ``squares`` is a list of 11 squares, each a list of four corners in
    order; every coordinate is a :class:`~sqpack.field.FieldElement`.
    """
    field = NumberField(U_MIN_POLY, U_INTERVAL)
    squares, side = build_in(field, field.alpha)
    return squares, side, field


def build_in(field, u):
    """The same construction, over any field in which ``u = tan(a/2)`` lives.

    Split out from :func:`build` so the exact round trip can rebuild this packing
    inside ``Q(s)`` from a recovered ``u`` without a second copy of the closed forms.
    A second copy would be a second thing to keep correct, and the round trip's whole
    claim is that it reconstructs *this* packing rather than one that resembles it.
    """
    K = field.rational

    one_plus_u2 = K(1) + u * u
    cos_a = (K(1) - u * u) / one_plus_u2
    sin_a = (K(2) * u) / one_plus_u2
    assert (cos_a * cos_a + sin_a * sin_a - K(1)).is_zero()

    # s = 2 + (2 + sin a) / (cos a + sin a), rationalised in u.
    side = (K(6) * u + K(4)) / (K(1) + K(2) * u - u * u)

    r1 = K(1) - (side - K(3)) * cos_a
    u1 = ((K(1) + r1) * cos_a - K(1)) / sin_a
    v1 = cos_a - sin_a
    v2 = (side - K(1)) / sin_a - r1 - (K(3) + u1) * (cos_a / sin_a)
    x0 = K(1) + K(2) / cos_a - (side - K(2)) * (sin_a / cos_a)

    def axis_aligned(x, y):
        return [(x, y), (x + K(1), y), (x + K(1), y + K(1)), (x, y + K(1))]

    def tilted(ox, oy):
        # The block transform is translate(1,1) . rotate(a) . translate(0,-r1)
        corners = []
        for dx, dy in ((K(0), K(0)), (K(1), K(0)), (K(1), K(1)), (K(0), K(1))):
            px, py = ox + dx, oy + dy - r1
            corners.append((K(1) + cos_a * px - sin_a * py, K(1) + sin_a * px + cos_a * py))
        return corners

    squares = [
        axis_aligned(K(0), K(0)),
        axis_aligned(side - K(1), K(0)),
        axis_aligned(x0, side - K(1)),
        axis_aligned(K(0), side - K(1)),
        axis_aligned(K(1), side - K(1)),
        axis_aligned(K(0), side - K(2)),
        tilted(K(0), K(0)),
        tilted(u1, -K(1)),
        tilted(K(1), v1),
        tilted(u1 + K(1), v1 - K(1)),
        tilted(u1 + K(2), -v2),
    ]
    assert len(squares) == 11
    return squares, side


def side_satisfies_published_polynomial(side, field) -> bool:
    """Check ``P(side) == 0`` exactly for the published degree-8 polynomial."""
    acc = field.zero
    for c in S_MIN_POLY:
        acc = acc * side + field.rational(c)
    return acc.is_zero()
```

<a id="source-2"></a>

## Source 2: `packing/cases/trump11/isolation-theorem.md`

Snapshot `4d305597a505`, source lines 1-233.

<a id="source-2-a-quantitative-local-theorem-at-trumps-11-square-packing"></a>

### A Quantitative Local Theorem at Trump’s 11-Square Packing

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

<a id="source-2-exact-witness-and-chart"></a>

#### Exact Witness and Chart

Let `u` be the unique root in `(36/100, 37/100)` of

`5u^8 - 10u^7 - 2u^6 + 14u^5 + 12u^4 - 6u^3 + 2u^2 + 2u - 1`.

Put

`U = (6u + 4)/(1 + 2u - u^2)`.

The exact witness in [`packing.py`](09-trump-construction-and-local-proof.md#source-1) has

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

<a id="source-2-theorem"></a>

#### Theorem

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

<a id="source-2-proof-from-the-retained-certificates"></a>

#### Proof From the Retained Certificates

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

<a id="source-3"></a>

## Source 3: `packing/cases/trump11/isolation-theorem.md`

Snapshot `4d305597a505`, source lines 349-367.

<a id="source-3-replay-boundary-and-refusals"></a>

#### Replay Boundary and Refusals

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

## Later BC-241 Review Scope

Source: `packing/campaign/series/series-000-smoke-and-calibration/results/bc-241-trump-local-theorem-review.json` at `4d305597a505ebfbe85f1851fa7148374661e622`; selected scope/disposition fields only. The old handoff status is the receipt's status at authorship; the scoped evidence was subsequently integrated. Full branch matrices and replay logs are omitted.

```json
{
  "scope": "Retained-record-dependent labelled anchored fixed-side local isolation and side stability in the 33-coordinate sup norm. No global capture, uniqueness or optimality; no independent full radius-generator replay.",
  "status": "terminal_source_distinct_packet_awaiting_closure_manager_disposition",
  "retained_record_review": {
    "disposition": "accept_retained_record_dependent_local_scope",
    "claim_scope": {
      "retained_bc199_text": "Lower bound on the chart-distance radius, in the anchored centre-angle chart at fixed side U = Trump's exact side: no chart point within rho_0 of the labelled pose in the sup norm is a packing in [0, U]^2 other than the pose itself. Side-stability clause: a packing of side s' <= U embedded in [0, U]^2 is a feasible pose at side U, so any such packing within rho_0 of the pose is the pose, which touches all four walls, hence s' = U; on the same ball a packing at side U + sigma satisfies sigma >= -C ||v||^2 for every branch stress. No optimality, no uniqueness beyond the ball, no global statement, and nothing about a different geometrical arrangement of the unit squares.",
      "established": [
        "local fixed-side isolation in the labelled anchored 33-variable sup-norm chart",
        "local side stability for s'<=U with equality only at the retained pose",
        "local quadratic lower bound on side displacement in the same certified ball"
      ],
      "refused": [
        "a full pose-side chart theorem",
        "a theorem for a different labeling or contact type outside the certified ball",
        "global optimality of Trump's side",
        "global uniqueness",
        "global capture",
        "an independent replay of all radius face linear programs",
        "recreation of missing per-face primal or dual witnesses",
        "any frontier or standing-best change"
      ]
    },
    "radius_generator_executed": false,
    "unreviewed_generator_obligations": [
      "Complete 128-by-66 uniform and weighted radius face witnesses are absent.",
      "The retained weighted aggregate rational is not independently recovered from every weighted face.",
      "Full inactive-gap and symmetry geometry producers are not rerun; retained guards are exact input premises."
    ]
  }
}
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
