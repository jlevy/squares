# One-minute proof that `s(11) ≥ 381/100`

Let `K = [0,381/100]²`, and let `μ` be the nonnegative atomic measure in
[`certificate.json`](certificate.json).
Suppose eleven interior-disjoint unit squares `S_i ⊂ K` exist.
For each `i` separately, reduce its orientation modulo quarter-turns and, when
necessary, reflect it across `x = y`; its orientation then lies in `[0,π/4]`, and this
reflection preserves `μ`. Some net angle differs from that orientation by an absolute
angle `d ≥ 0` with `tan d ≤ D`. The concentric closed square of side `B` at that net
angle has half-width

```text
(B/2)(cos d + sin d) ≤ (B/2)(1 + D) < 1/2,
```

so it lies strictly inside the reflected unit square.
Pulling it back gives a closed square `P_i ⊂ int(S_i)` with `μ(P_i) ≥ 4001/4000 > 1`.
The `P_i` are disjoint, hence

```text
μ(K) ≥ Σ_i μ(P_i) > 11,
```

contrary to `μ(K) = 434547/40000 < 11`. Thus no packing fits in `K`; any smaller
container embeds in `K`, so `s(11) ≥ 381/100`.

Only invariance under `(x,y) ↦ (y,x)` is used.
Full D4 invariance is stronger than necessary.
No compactness or attainment claim is needed.

## The four exact facts

1. The 1,121 rational atoms lie in `K`, have nonnegative weights, are invariant under
   coordinate swap, and have total weight `434547/40000 < 11`.
2. With `T = 207107/500000`, `t_k = Tk/180`, and `θ_k = 2 arctan(t_k)`,
   `T² + 2T − 1 = 309449/250000000000 > 0`; therefore `θ_180 ≥ π/4`.
3. The largest half-gap tangent is `D = 207107/90000000`, and
   `B(1 + D) = 899996306539/900000000000 < 1` for `B = 9977/10000`.
4. For every `k = 0,…,180`, every contained closed side-`B` square at orientation `θ_k`
   has mass at least `4001/4000`.

Facts 1–3 are short rational calculations.
Fact 4 is the irreducible computer-assisted lemma; 181 asserted minima are not by
themselves a proof.

## Exact finite form of fact 4

For each `k`, put

```text
c_k = (1 − t_k²)/(1 + t_k²),   s_k = 2t_k/(1 + t_k²),
h_k = (B/2)(c_k + s_k).
```

The required finite lemma is that, for every `(X,Y) ∈ [h_k,L−h_k]²`,

```text
Σ w_i ≥ 4001/4000,
```

where the sum is over exactly those atoms satisfying

```text
|c_k(x_i−X) + s_k(y_i−Y)| ≤ B/2,
|−s_k(x_i−X) + c_k(y_i−Y)| ≤ B/2.
```

Every number here is rational.
At fixed `k`, rotate the centre to `(U,V)`. Each atom then contributes on one closed
axis-aligned rectangle, whose four edge coordinates join a finite event grid.
Covered mass is constant on every open grid cell.
On an event boundary it can only increase, because the rectangles are closed and all
weights are nonnegative.
It is therefore enough to score every open event cell meeting the rotated
feasible-centre square.

The standard-library-only [`minimal_verify.py`](minimal_verify.py) does exactly that
with integer prefix sums.
It binds the retained file’s SHA-256
`b121edbd044b6f326022d8783551efd947c95eec2738269857d039358ac6ae6a`, examines 567,130,649
feasible cells, recomputes the minimum `4001/4000`, and scales every weight by
`3999/4001` to exhibit a must-refuse C4 witness at `3999/4000`. The larger
self-contained verifier in [`thirdparty/verify.py`](thirdparty/verify.py), when pointed
explicitly at the current certificate, independently obtains the same minimum and
directly re-sums sampled minimizing cells.
The separate interval branch-and-bound in
[`../../src/sqpack/fractional/interval.py`](../../src/sqpack/fractional/interval.py)
checks a doubled 361-direction net without using the reflection premise and obtains the
same one-point enclosure.
The older third-party package’s [`check.py`](thirdparty/check.py) provides the
independent known-answer control and fully checks the retained `19/5` rung, but is not
evidence for the extra `1/100` proved here.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
