# Shared Segments Restrict Separating Supports

Date: 2026-09-08. Status: analytic proof.
Scope: local projected separation for two owners of one segment.

Let

```text
sigma = m + [-ell/2,ell/2] e_x.
```

Suppose interior-disjoint unit squares `Q1,Q2` both lie within distance `delta` of
`sigma`. For any unit separating normal `v`, oriented from `Q1` toward `Q2`, write

```text
alpha = max_{Q1} v·x,
beta  = min_{Q2} v·x,
r_v   = ell |v_x|/2 + delta.
```

Then

```text
v·m - r_v <= alpha <= beta <= v·m + r_v.
```

Nearest points on the two compact squares have projections in the displayed interval;
separation gives the middle inequality.
The separating-axis theorem supplies a normal parallel to an edge normal of one square.
If `H_i(v)` is square `i`’s projection half-width, then

```text
H_1(v) + H_2(v)
    <= v·(c_2-c_1)
    <= H_1(v) + H_2(v) + ell |v_x| + 2delta.
```

The upper gap is sharp.
At `m = (48/25,1)`, the axis-parallel squares

```text
[108/125,233/125] x [1/2,3/2],
[247/125,372/125] x [1/2,3/2]
```

each lie exactly `3/500` from the nearest endpoint of the segment and have horizontal
gap `14/125 = ell + 2delta`. Thus shared ownership need not mean that the squares touch.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
