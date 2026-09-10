# T-025: A Threshold Certificate Proves `s(11) >= 191/50`

Eleven unit squares with pairwise disjoint interiors do not fit in a square of side
`191/50 = 3.82`. The proof is a certificate of a new kind: a weighted family of *point
atoms* and *threshold atoms* whose total budget is below eleven while every admissible
core is charged at least one.
It is decided from its frozen bytes by two verifiers that fail differently, and the
theorem it rests on was reviewed adversarially before the certificate was registered.

```text
s(11) >= 191/50 = 3.82
```

This is an endpoint certificate, not a limit: the side is the container side itself, and
nothing here claims a strict inequality.
The exact ceiling family retained beside it shows that no certificate of the earlier
one-body point-atom form exists at this side for this shrink, on any net containing its
six directions; the threshold atoms are what pass that ceiling.

## The Theorem

Fix the container `Q = [0, L]^2`, an integer `n >= 1`, a shrink `0 < B < 1`, and a
finite *net* of half-tangents `0 = t_0 < t_1 < ... < t_K` with `t_K^2 + 2 t_K - 1 >= 0`;
the net direction `theta_k = 2 arctan t_k` then runs from `0` to at least `pi/4`. Let
`D = max_k (t_{k+1} - t_k) / (1 + t_k t_{k+1})` be the largest half-gap tangent.
An *admissible core* is a closed square of side `B` at a net direction, contained in
`Q`.

A *point atom* `(p, w)` with `w >= 0` charges `w` to every core containing `p`. A
*threshold atom* `(S, k, w)` with `S` a finite set of distinct points, `1 <= k <= |S|`
and `w >= 0` charges `w` to every core `P` with `|P ∩ S| >= k`. The *budget* of a family
is

```text
M = sum over point atoms of w  +  sum over threshold atoms of w * floor(|S| / k).
```

A point atom is the case `|S| = k = 1`. The conditions are:

- **Condition 1 and 1'.** The point atoms and the threshold atoms are each closed under
  the eight symmetries of `Q`, with the weight constant on each orbit (the image of
  `(S, k, w)` is `(gS, k, w)` and must be present).
- **Condition 2'.** `M < n`.
- **Condition 3.** The net reaches `pi/4`: `t_K^2 + 2 t_K - 1 >= 0`.
- **Condition 4.** `B (1 + D) < 1`.
- **Condition 5'.** Every admissible core is charged at least `1`.

**Theorem.** Under Conditions 1, 1', 2', 3, 4 and 5', no `n` closed unit squares with
pairwise disjoint interiors fit in `Q`. Hence `s(n) >= L`.

## The Proof

Suppose `U_1, ..., U_n` are unit squares in `Q` with pairwise disjoint interiors.

**Cores.** Take `U_i` at orientation `phi_i in [0, pi/2)`. If `phi_i > pi/4`, reflect
the whole picture in the diagonal `(x, y) -> (y, x)`, which maps `Q` to itself and
`phi_i` to `pi/2 - phi_i in (0, pi/4)`. By Condition 3 the reflected orientation lies in
some interval `[theta_k, theta_{k+1}]`, and the nearer endpoint is within an angle `d`
with `tan d <= D`. The concentric closed `B`-square `P_i` at that net direction has
half-width across the unit square’s edge normal equal to

```text
(B/2)(cos d + sin d) = (B/2) cos d (1 + tan d) <= (B/2)(1 + D) < 1/2,
```

so `P_i` lies in the interior of the (reflected) unit square, and in particular in `Q`:
it is an admissible core.
Undoing the reflection where one was used gives a core `P_i ⊂ int(U_i)` for every `i`,
and Condition 1' makes the charge invariant under the reflection (the map
`A -> g^{-1} A` is a bijection of the family preserving `k` and `w`, so reindexing the
sum gives `c(gP) = c(P)`), so `c(P_i) >= 1` for every `i` by Condition 5'.

**Disjointness.** `P_i ⊂ int(U_i)` and the interiors are pairwise disjoint, so the
closed cores `P_1, ..., P_n` are pairwise disjoint as closed sets.
This is the one place Condition 4 is used, and it is used the same way for point atoms.

**Counting.** A point atom charges at most one of pairwise disjoint cores, so its total
charge is at most `w`. For a threshold atom `(S, k, w)`, the traces `P_i ∩ S` are
pairwise disjoint subsets of `S`; each charged core has a trace of at least `k` points;
so if `q` cores are charged then `q k <= |S|` and `q <= floor(|S| / k)`, and the atom’s
total charge is at most `w floor(|S| / k)`. Summing over the family,

```text
n <= sum_i c(P_i) <= M < n,
```

a contradiction. Nothing above used `n` except Condition 2', so the same family proves
the theorem for every integer above its budget.

**Why finitely many cells decide Condition 5'.** At a net direction, in the frame
rotated to it, the core with centre `c` contains a point `s` exactly when `c` lies in a
closed axis-parallel square `R_s` of side `B` about `s`. Take the event grid formed by
the edges of every `R_s` over every point of every atom, point atoms and threshold
points alike, together with the extremes of the centre domain.
On an open cell the trace `T(c) = {s : c in R_s}` is constant; on a grid line, `T(c)`
contains the trace of every adjacent open cell because each `R_s` is closed; and every
point of the centre domain is in the closure of an open cell that meets the domain.
The charge is a monotone function of the trace, so its minimum over the domain is
attained on an open cell, and a sweep over open cells decides Condition 5'. A threshold
atom enters the sweep’s integer difference array through the inclusion-exclusion
identity

```text
[m >= k] = sum_{j >= k} (-1)^(j - k) C(j - 1, k - 1) C(m, j),
```

where `m = |T ∩ S|` and `C(m, j)` counts the `j`-subsets of `S` whose rectangles all
contain the cell: each is a closed rectangle with event-coordinate corners, so the atom
is a signed sum of rectangle indicators whose value on every open cell is the
nonnegative, monotone `w [m >= k]`. The signs are internal to that exact expansion and
never reach the theorem.

## Frozen Premises

| Quantity | Value |
| --- | --- |
| Certificate bytes | [`certificate.json`](certificate.json), SHA-256 `3935651af614eb3e9a1926179925f98643beb17ed1764a323fe83a527f4bad5c`, 673,639 bytes |
| Container, shrink | `L = 191/50`, `B = 9977/10000` |
| Net | `t_k = 207107 k / 90000000`, `k = 0..180` (181 directions, angle limit `207107/500000`); `D = 207107/90000000`; `B(1 + D) = 899996306539/900000000000 < 1` |
| Point atoms | 584, in 79 D4 orbits (67 of size 8, 12 of size 4 on mirrors), mass `271052551/31250000 = 8.673681632` |
| Threshold atoms | 320, in 40 orbits of 8, every one `2`-of-`3`, budget `143352577/62500000 = 2.293641232` |
| Total budget | `685457679/62500000 = 10.967322864 < 11`, margin `2042321/62500000 = 0.032677136` |
| Least cell charge | `100000203/100000000 = 1.000002030`, attained at direction 69 (about `18.0°`) |

Conditions 1, 1', 2', 3 and 4 are decided in closed form from the bytes, and were
recomputed independently of `sqpack` in the review named below.

## Two Decisions of Condition 5'

Both routes run through `devtools.decide_threshold_certificate`, which reads the file
back and prints `RETAINABLE` only when both accept and agree on the least charge to the
digit.

- **Exact event-cell sweep** (`sqpack.fractional.threshold`): the difference array
  above, over all 181 net directions; least charge `100000203/100000000` at direction
  69; the dense-grid and slab evaluations agree at every direction; the charge at the
  witness centre, re-evaluated by direct membership counting, agrees.
- **Interval branch and bound** (`sqpack.fractional.threshold_interval`):
  directed-rounding interval arithmetic over boxes of centres on the doubled net
  (`theta_k` and `pi/2 - theta_k`, 361 directions, so Condition 1' is never invoked for
  this decision). A threshold atom counts for a box only when at least `k` of its points
  have coverage rectangles whose inner enclosures contain the whole box, a lower bound
  by construction; an unresolved point is dropped rather than assumed.
  All 361 directions certified, none stalled, 1,639,903 boxes, enclosure of the least
  charge of width zero at `100000203/100000000`. Per-direction minima take two values
  only: that one at 86 directions and `1000002031/1000000000` at the other 275.

The two routes share the loader, the closed-form conditions, the weight scale and the
net, and nothing of how Condition 5' is decided.

## Review

[`review-2026-09-09-threshold-certificate-theorem.md`](../../../docs/project/reviews/review-2026-09-09-threshold-certificate-theorem.md)
attacked the theorem and the tool before registration: closed disjointness and the
budget, the trace argument at the edges, D4 invariance, the last net gap, open cells and
boundaries, the inclusion-exclusion identity and its `int64` headroom, forgeries a wrong
budget rule would admit, and the candidate’s own conditions.
It found no soundness defect; its open items were the second route, the controls and
this statement, all of which this package now carries.

## Scope

The bound is the container side itself.
The exact depth-one family
[`ceiling-family-191-50.json`](../../campaign/series/series-000-smoke-and-calibration/results/agenda-034/ceiling-family-191-50.json)
(88 closed `B`-squares, total weight exactly eleven, maximum depth one) proves that no
D4-symmetric point-atom measure of mass below eleven satisfies Condition 5 at this side,
shrink and net; the threshold atoms carry `2.29` of this certificate’s budget, which the
point method cannot have.
Nothing here bounds the side from above, decides fit at a larger side, or proves a
strict inequality at `191/50`. [T-026](t-026-dilation-limit-proof.md) measures these
atoms on 720- and 1440-step nets and proves the resulting weak dilation-limit bound
`s(11) >= 955000*sqrt(518400042893309449)/179696714646249`. That finite-net result does
not decide further refinements.

## Replay

From `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m cases.n11_threshold_certificate
uv run --frozen --all-extras --group dev python -m devtools.decide_threshold_certificate \
  cases/n11_threshold_certificate/certificate.json
uv run --frozen --all-extras --group dev python -m devtools.decide_threshold_certificate \
  --quick cases/n11_threshold_certificate/certificate.json
```

The first replays the package; the second is the two-route gate (about ninety seconds on
three workers); the third is the interval route alone, which cannot retain.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
