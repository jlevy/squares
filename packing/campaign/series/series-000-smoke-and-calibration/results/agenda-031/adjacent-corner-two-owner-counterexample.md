# Adjacent Corner Pairs Can Each Have Two Owners

Date: 2026-09-08. Status: exact analytic counterexample, independently reviewed.
Scope: four-square local ownership compatibility at `q = 96/25`; no eleven-square
packing or global ownership count is asserted.

Let

```text
a = 3152/3175,   b = 2336/3175,   B = 9977/10000,
A = (120/100,71/100),    B_L = (71/100,165/100),
A' = (264/100,71/100),   B_R = (313/100,165/100).
```

A diamond of unit side centered at `c` is

```text
D(c) = {p : |p_x-c_x|+|p_y-c_y| <= 1/sqrt(2)}.
```

Use the four diamonds centered at `A`, `B_L`, `A'`, and `B_R`. All four lie strictly
inside `[0,q]^2`: the smallest wall clearance of a center is `71/100`, whose square
exceeds `1/2`. Their pairwise center distances in the one-norm take the values
`143/100`, `36/25`, `121/50`, and `287/100`, all greater than `sqrt(2)`. Their interiors
are therefore pairwise disjoint, with positive gaps.

The two left corner marks `(a,b)` and `(b,a)` belong respectively to the concentric
`B`-cores of the diamonds centered at `A` and `B_L`. Their one-norm displacements from
those centers are `2959/12700` and `4337/6350`, both less than `7/10`, and

```text
2(7/10)^2 < (9977/10000)^2.
```

Reflection across `x=q/2` supplies the two right corner marks in the diamonds centered
at `A'` and `B_R`.

The same marks also lie inside the selected nearest-net cores, rather than merely an
arbitrary contained concentric core.
In each unit square’s frame, the mark has sup norm less than `(7/10)/sqrt(2)` about the
center. For the canonical nearest net direction, the angular error obeys

```text
tan(|d|) <= 207107/90000000 < 3/1000.
```

Changing to that core frame therefore multiplies the coordinate bound by at most
`1+3/1000`. The exact comparison

```text
2(7/10)^2(1003/1000)^2 = 49294441/50000000
                       < 99540529/100000000
                       = (9977/10000)^2
```

puts both coordinates strictly inside the selected core.

This four-square construction refutes the proposed local claim that two adjacent
corner-pair mark sets cannot each have two distinct owners.
It does not supply an eleven-square configuration, decide whether this local pattern
extends to eleven squares, or exclude any additional segment or corner roles.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
