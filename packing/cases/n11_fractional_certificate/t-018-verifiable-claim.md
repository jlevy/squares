# Verifiable Claim: $s(11) \ge 19/5$

Everything needed to check, with your own tools and without trusting this repository,
that eleven unit squares do not fit in a square of side $19/5 = 3.8$. Paste this file
into any coding agent, or read it yourself: the claim, the theorem it instantiates, its
proof, and a verifier in Python’s standard library alone.

## The Claim

Let $s(n)$ be the side of the smallest square that contains $n$ unit squares with
pairwise disjoint interiors, the unit squares free to rotate.
(Formally $s(n)$ is the infimum of the sides that admit such a packing.)

**Claim.** $s(11) \ge 19/5$.

The witness is the certificate file
[`certificate-19-5.json`](https://github.com/jlevy/squares/blob/main/packing/cases/n11_fractional_certificate/certificate-19-5.json):
425 weighted points and a net of 181 rational directions.
The verifier below decides five conditions on that file in exact rational arithmetic,
and the theorem below shows that the five conditions imply the claim.
The same theorem and the same verifier decide
[`certificate.json`](https://github.com/jlevy/squares/blob/main/packing/cases/n11_fractional_certificate/certificate.json),
1121 points, for the tighter bound $s(11) \ge 381/100$.

## The Theorem

The argument is a weighted, fractional form of the classical unavoidable-set argument
for square packing, in the shape Gustavo Massaccesi used for $n = 17$ in August 2026
after Sam Burns proposed the weighted form.
Neither the theorem nor the certificate shape is this project’s; the $n = 11$ instance
is.

**Data.** An integer $n \ge 1$; rationals $L > 0$ (the container side) and $B > 0$ (the
shrunken side); a direction net of rationals $0 = t_0 < t_1 < \cdots < t_K$, standing
for the angles $\theta_k = 2 \arctan t_k$; and finitely many atoms $(x_i, y_i, w_i)$
with rational coordinates and rational weights $w_i \ge 0$. For a set $Q$ in the plane
write $\operatorname{mass}(Q) = \sum \{\, w_i : (x_i, y_i) \in Q \,\}$. The container is
the closed square $K = [0, L]^2$.

**Hypotheses.**

- **Condition 1.** The weighted atom set is invariant under the eight symmetries of $K$:
  for every atom, each of the eight images of its site under
  $(x, y) \mapsto (x, y), (L - x, y), (x, L - y), (L - x, L - y), (y, x), (L - y, x), (y, L - x), (L - y, L - x)$
  is a site of the same total weight.
  The proof uses only the reflection $(x, y) \mapsto (y, x)$; the certificate declares
  the full group, and checking it is a stronger hypothesis, hence safe.
- **Condition 2.** $\sum_i w_i < n$.
- **Condition 3.** $\theta_K \ge \pi/4$. Since $\tan(\pi/8) = \sqrt{2} - 1$ is the
  positive root of $t^2 + 2t - 1$ and that polynomial increases for $t \ge 0$, this is
  exactly $t_K^2 + 2 t_K - 1 \ge 0$, a rational inequality.
- **Condition 4.** $B(1 + D) < 1$, where
  $D = \max_k (t_{k+1} - t_k) / (1 + t_k t_{k+1})$. Since $\theta = 2 \arctan t$, half
  the gap between adjacent net angles is $\arctan t_{k+1} - \arctan t_k$, whose tangent
  is exactly that quotient, so $D$ is the tangent of the largest half-gap.
- **Condition 5.** For every $k$ and every closed square $Q$ of side $B$ whose edges
  make angle $\theta_k$ with the axes and which lies inside $K$:
  $\operatorname{mass}(Q) \ge 1$.

**Conclusion.** $n$ unit squares with pairwise disjoint interiors do not fit in $K$.
Hence $s(n) \ge L$.

## The Proof

Suppose closed unit squares $S_1, \dots, S_n \subset K$ have pairwise disjoint
interiors. We derive $n \le \sum_i w_i$, contradicting Condition 2.

1. **Orientation reduction.** A square is unchanged by a quarter turn, so its
   orientation $\varphi$, the angle its edges make with the axes, may be taken in
   $[0, \pi/2)$. If $\varphi > \pi/4$, apply the reflection $R(x, y) = (y, x)$. It maps
   $K$ onto itself and sends a direction at angle $\alpha$ to angle $\pi/2 - \alpha$, so
   $R(S_j)$ is a unit square in $K$ with orientation $\pi/2 - \varphi \in (0, \pi/4)$.
   Write $S'_j$ for $S_j$ or $R(S_j)$, whichever has orientation
   $\varphi' \in [0, \pi/4]$.
2. **A net angle nearby.** By Condition 3 and $t_0 = 0$, the net angles run from $0$ to
   at least $\pi/4$, so $\varphi'$ lies in some $[\theta_k, \theta_{k+1}]$, and the
   nearer endpoint $\theta$ satisfies
   $d := |\varphi' - \theta| \le (\theta_{k+1} - \theta_k)/2$. Since $\tan$ increases on
   $[0, \pi/2)$, $\tan d \le D$.
3. **A concentric shrunken square.** Let $Q$ be the closed square of side $B$, centered
   at the center of $S'_j$, with orientation $\theta$. Its support function in the
   direction of any edge normal of $S'_j$ is $(B/2)(\cos d + \sin d)$, while $S'_j$
   extends $1/2$ from its center in that direction, so $Q$ lies in the open interior of
   $S'_j$ as soon as $B(\cos d + \sin d) < 1$. Now
   $\cos d + \sin d = \cos d \,(1 + \tan d) \le 1 + \tan d \le 1 + D$, and Condition 4
   gives $B(1 + D) < 1$. Hence $Q \subset \operatorname{int}(S'_j) \subset K$, strictly
   inside.
4. **Condition 5 applies.** $Q$ is a closed $B$-square at the net angle $\theta$ lying
   inside $K$, so $\operatorname{mass}(Q) \ge 1$.
5. **Pull back.** Let $P_j = Q$ if $S'_j = S_j$, and $P_j = R(Q)$ otherwise.
   Then $P_j \subset \operatorname{int}(S_j)$, and
   $\operatorname{mass}(P_j) = \operatorname{mass}(Q) \ge 1$ because by Condition 1 the
   weighted atom set is invariant under $R$: the atoms inside $R(Q)$ are the images of
   the atoms inside $Q$, with the same weights.
6. **Count.** The interiors of the $S_j$ are pairwise disjoint, so the $P_j$ are
   pairwise disjoint and each atom lies in at most one of them.
   With $w_i \ge 0$, $n \le \sum_j \operatorname{mass}(P_j) \le \sum_i w_i < n$.
   Contradiction.

So no such packing exists in $[0, L]^2$. If $s(n) < L$, the definition of the infimum
gives a packing in some square of side $L' < L$, which sits inside $[0, L]^2$; therefore
$s(n) \ge L$.

Two remarks a careful reader will want settled.
First, $Q$ is closed and Condition 5 counts atoms on its boundary.
This never double-counts, because step 3 puts $Q$ strictly inside the interior of one
unit square. Second, Condition 5 quantifies over every $B$-square inside $K$ at a net
angle, a superset of the squares the proof meets.
A stronger hypothesis can only make the theorem harder to apply, never unsound.

## How to Check It

Save the certificate file and the verifier, then run the verifier on the file with any
CPython 3.10 or later.
It needs nothing outside the standard library.

```
python verify_minimal.py certificate-19-5.json
```

It prints one line per condition, then a verdict.
For the $19/5$ certificate the verdict is `VERIFIED: s(11) >= 19/5`, with Condition 5
reporting the least covered mass $50003/50000$ at direction $0$ and center
$(53/100, 53/100)$ over 90,546,593 cells across 181 directions.
It takes about half a minute in pure Python.
The verifier decides Condition 5 by enumerating, for each net direction, the finitely
many cells of center positions on which the set of atoms under the square is constant,
and checking the mass on every reachable cell, so the sweep is exact rather than
sampled.

The exit status is 0 only when all five conditions hold.
Perturb the file, by lightening one atom, dropping an orbit member, or shortening the
net, and the verifier refuses it, naming the condition that fails.

## The Verifier

```python
#!/usr/bin/env python3
"""Decide a fractional unavoidable-set certificate for s(n) >= L, exactly.

Usage:  python verify_minimal.py certificate.json

Standard library only, CPython 3.10 or later. Every decision is made in
fractions.Fraction. One line is printed per condition, then VERIFIED or REFUSED,
and the exit status is 0 only when all five conditions hold.

THE THEOREM. Let s(n) be the least side of a square containing n unit squares
with pairwise disjoint interiors, rotation allowed. A certificate names an
integer n >= 1, rationals L > 0 (container side) and B > 0 (shrunken side), a
net of rationals 0 = t_0 < ... < t_K standing for the angles 2 arctan(t_k), and
atoms (x_i, y_i, w_i) with rational coordinates and weights w_i >= 0; the mass
of a set is the total weight of the atoms in it. If
  Condition 1  the weighted atoms are invariant under the eight symmetries of
               the container [0, L]^2;
  Condition 2  the total weight is strictly less than n;
  Condition 3  2 arctan(t_K) >= pi/4, decided as t_K^2 + 2 t_K - 1 >= 0;
  Condition 4  B (1 + D) < 1 for D = max_k (t_{k+1} - t_k) / (1 + t_k t_{k+1}),
               the tangent of the largest half-gap between adjacent net angles;
  Condition 5  every closed square of side B at a net angle that lies inside
               [0, L]^2 has mass at least 1;
then n unit squares with disjoint interiors do not fit in [0, L]^2, so s(n) >= L.
(Each unit square, reflected in the diagonal if its angle exceeds pi/4, contains
strictly inside it a B-square at the nearest net angle, of mass >= 1; the n such
squares are disjoint, so the total weight is at least n, against Condition 2.)
"""

# ruff: noqa: N803, N806  -- L, B, D, F, U, V, X, Y are the theorem's own symbols.

import json
import sys
from bisect import bisect_left, bisect_right
from fractions import Fraction
from itertools import accumulate, pairwise
from math import lcm
from pathlib import Path


def load(path):
    """The certificate as (n, L, B, tangents, atoms); any other shape is refused."""
    record = json.loads(Path(path).read_text())

    def rational(value):
        if not isinstance(value, str):  # a JSON float would be rounded: refuse it
            message = f"rationals must be strings such as '19/5', got {value!r}"
            raise TypeError(message)
        return Fraction(value)

    n, K = record["n"], record["direction_steps"]
    if not (isinstance(n, int) and isinstance(K, int) and n >= 1 and K >= 1):
        message = "n and direction_steps must be integers, n >= 1 and direction_steps >= 1"
        raise ValueError(message)
    L, B, T = (rational(record[key]) for key in ("outer_side", "square_side", "angle_limit"))
    if not (L > 0 and B > 0 and T > 0):
        message = "outer_side, square_side and angle_limit must be positive"
        raise ValueError(message)
    atoms = []
    for atom in record["atoms"]:
        x, y, w = (rational(value) for value in atom)
        if w < 0:
            message = f"negative weight {w} at ({x}, {y})"
            raise ValueError(message)
        atoms.append((x, y, w))
    return n, L, B, [T * k / K for k in range(K + 1)], atoms


def symmetric(atoms, L):
    """Condition 1. The eight maps form a group, so checking every site of the support
    against every image is the whole of invariance."""
    weight = {}
    for x, y, w in atoms:
        weight[x, y] = weight.get((x, y), 0) + w
    for (x, y), w in weight.items():
        flips = [(p, q) for p in (x, L - x) for q in (y, L - y)]
        for p, q in flips + [(q, p) for p, q in flips]:  # the eight symmetries of [0, L]^2
            if weight.get((p, q), 0) != w:
                return (
                    f"({x}, {y}) has weight {w} but ({p}, {q}) has {weight.get((p, q), 0)}",
                    False,
                )
    return f"{len(atoms)} atoms, {len(weight)} sites, invariant under the 8 symmetries", True


def extent(polygon, axis, low, high):
    """Range of the other coordinate over the part of a convex polygon with
    low <= coordinate[axis] <= high: that part's vertices are the polygon's vertices in
    the slab and the crossings of its edges with the slab's two boundary lines."""
    points = [p for p in polygon if low <= p[axis] <= high]
    for p, q in zip(polygon, polygon[1:] + polygon[:1], strict=True):
        for bound in (low, high):
            if (p[axis] - bound) * (q[axis] - bound) < 0:  # a strict crossing
                f = (bound - p[axis]) / (q[axis] - p[axis])
                points.append((p[0] + f * (q[0] - p[0]), p[1] + f * (q[1] - p[1])))
    values = [p[1 - axis] for p in points]
    return min(values), max(values)


# Condition 5 at one direction, decided over the continuum of centers by a finite sweep.
# In the coordinates u = c x + s y, v = -s x + c y the placed square is axis-parallel:
# the closed B-square centered at (U, V) contains the atom at (u_i, v_i) iff
# |u_i - U| <= B/2 and |v_i - V| <= B/2, and it lies inside [0, L]^2 iff its center
# (X, Y) has h <= X, Y <= L - h with h = B(|c| + |s|)/2. That closed square of centers,
# F, has nonempty interior (2h < L is checked). The lines u = u_i +- B/2,
# v = v_i +- B/2 and the four lines bounding F cut the plane into open cells. The mass
# is constant on a cell (each atom's box has its edges on the lines); a point on a
# cell's boundary has at least the cell's mass (a closed box meeting the cell contains
# its closure); and every point of F is in the closure of a cell meeting F (F has
# interior points arbitrarily near it, and an open set is not covered by finitely many
# lines). So the least mass over F is the least over the cells meeting F. A cell
# (a, b) x (a', b') with [a, b] inside F's u-projection meets F iff a' < hi and lo < b',
# where [lo, hi] is the v-range of F within the closed strip a <= u <= b: the open
# strip's part of F projects onto an interval between (lo, hi) and [lo, hi].


def least_mass(L, B, t, atoms, scale):
    """The least mass over every admissible center at one net direction, with a center
    (X, Y) that attains it and the number of cells decided."""
    c, s = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)  # exact: c^2 + s^2 = 1
    half, h = B / 2, B * (abs(c) + abs(s)) / 2
    if 2 * h >= L:
        message = f"no B-square at t = {t} fits inside the container with room to spare"
        raise ValueError(message)
    rotated = [(c * x + s * y, -s * x + c * y, w) for x, y, w in atoms]
    corners = ((h, h), (L - h, h), (L - h, L - h), (h, L - h))
    F = [(c * x + s * y, -s * x + c * y) for x, y in corners]
    umin, umax = min(u for u, _ in F), max(u for u, _ in F)
    vmin, vmax = min(v for _, v in F), max(v for _, v in F)
    U = sorted({u + d for u, _, _ in rotated for d in (-half, half)} | {umin, umax})
    V = sorted({v + d for _, v, _ in rotated for d in (-half, half)} | {vmin, vmax})
    ui, vi = {u: i for i, u in enumerate(U)}, {v: j for j, v in enumerate(V)}

    # grid[i][j] becomes the scaled mass on the cell (U[i], U[i+1]) x (V[j], V[j+1]):
    # a two-dimensional difference array, then two prefix sums, all in integers.
    grid = [[0] * len(V) for _ in U]
    for u, v, w in rotated:
        i0, i1, j0, j1 = ui[u - half], ui[u + half], vi[v - half], vi[v + half]
        m = int(w * scale)
        grid[i0][j0] += m
        grid[i0][j1] -= m
        grid[i1][j0] -= m
        grid[i1][j1] += m
    grid = [list(accumulate(row)) for row in grid]  # prefix sums along v ...
    columns = [list(accumulate(column)) for column in zip(*grid, strict=True)]  # ... then u
    grid = [list(row) for row in zip(*columns, strict=True)]

    strips, cells = [], 0
    for i in range(ui[umin], ui[umax]):  # the strips within F's u-projection
        lo, hi = extent(F, 0, U[i], U[i + 1])
        j0, j1 = bisect_right(V, lo) - 1, bisect_left(V, hi) - 1
        row = grid[i][j0 : j1 + 1]
        cells += len(row)
        strips.append((min(row), i, j0 + row.index(min(row))))
    best, i, j = min(strips)

    # A center in the least cell and in F: v strictly between the cell's v-bounds and
    # F's v-range on the strip, then u strictly inside F's u-range at that v.
    lo, hi = extent(F, 0, U[i], U[i + 1])
    Vc = (max(V[j], lo) + min(V[j + 1], hi)) / 2
    left, right = extent(F, 1, Vc, Vc)
    Uc = (max(U[i], left) + min(U[i + 1], right)) / 2
    X, Y = c * Uc - s * Vc, s * Uc + c * Vc
    direct = sum(
        w
        for x, y, w in atoms
        if abs(c * (x - X) + s * (y - Y)) <= half and abs(-s * (x - X) + c * (y - Y)) <= half
    )
    if not (h <= X <= L - h and h <= Y <= L - h and direct == Fraction(best, scale)):
        message = f"center ({X}, {Y}) covers {direct}, the grid says {Fraction(best, scale)}"
        raise AssertionError(message)
    return Fraction(best, scale), (X, Y), cells


def decide(n, L, B, tangents, atoms):
    """Print every condition with its numbers; return 0 if all hold, else 1."""
    verdicts = []

    def report(number, detail, *, holds):
        verdicts.append(holds)
        print(f"Condition {number} {'holds' if holds else 'fails'}: {detail}", flush=True)

    detail, holds = symmetric(atoms, L)
    report(1, detail, holds=holds)
    total = sum(w for _, _, w in atoms)
    report(2, f"total mass {total} against n = {n}", holds=total < n)
    t, slack = tangents[-1], tangents[-1] ** 2 + 2 * tangents[-1] - 1
    report(3, f"t_K = {t}, t_K^2 + 2 t_K - 1 = {slack}", holds=slack >= 0)
    D = max((b - a) / (1 + a * b) for a, b in pairwise(tangents))
    report(4, f"D = {D}, B(1 + D) = {B * (1 + D)}", holds=B * (1 + D) < 1)
    scale = lcm(*(w.denominator for _, _, w in atoms))
    sweep, cells = [], 0
    for k, t in enumerate(tangents):
        mass, center, count = least_mass(L, B, t, atoms, scale)
        sweep.append((mass, k, t, center))
        cells += count
        print(".", end="", file=sys.stderr, flush=True)
    mass, k, t, (X, Y) = min(sweep)
    report(
        5,
        f"least covered mass {mass} at direction {k} (t = {t}), center ({X}, {Y}); "
        f"{cells} cells over {len(tangents)} directions",
        holds=mass >= 1,
    )
    print(f"VERIFIED: s({n}) >= {L}" if all(verdicts) else "REFUSED")
    return 0 if all(verdicts) else 1


if __name__ == "__main__":
    if len(sys.argv[1:]) != 1:
        sys.exit(__doc__)
    try:
        certificate = load(sys.argv[1])
    except (OSError, KeyError, TypeError, ValueError) as error:
        sys.exit(f"not a certificate of the expected shape: {error}")
    sys.exit(decide(*certificate))
```

## What Is and Is Not Claimed

This file decides the $19/5$ rung, and its proof covers exactly what the five conditions
establish: that eleven unit squares do not fit in a square of side $3.8$. The same
theorem and the same verifier decide the $381/100$ certificate at the URL above, which
is the bound the project states.
Nothing here depends on the correctness of any other code in the repository, and nothing
here claims that $19/5$ or $381/100$ is the true value of $s(11)$: the best known
packing puts $s(11) \le 3.8770835\ldots$, and the gap is open.
