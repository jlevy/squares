# The Remaining Eight Segments Have Sharp Capacity Four

Date: 2026-09-08. Status: analytic proof.
Scope: local ownership capacity at `q = 96/25`; no global packing count follows.

A unit square within `delta = 3/500` of a segment of length `ell = 1/10` has its center
within

```text
R = 1/sqrt(2) + ell/2 + delta = 1/sqrt(2) + 7/125 < 4/5
```

of the segment midpoint.
The centers of two interior-disjoint unit squares are at least one apart, because each
square contains an open disk of radius `1/2`.

Two nonzero radii shorter than `4/5` making an angle at most 75 degrees have endpoints
less than one unit apart.
For fixed angle, squared distance is convex in each radius, so its maximum on
`[0,4/5]^2` occurs at an endpoint pair and is at most

```text
(16/25) max(1, 2 - 2 cos(75 degrees)) < 24/25 < 1,
```

using `cos(75 degrees) = (sqrt(6)-sqrt(2))/4 > 1/4`. Among five rays from the midpoint,
one cyclic angular gap is at most 72 degrees, giving the forbidden center distance.
A center at the midpoint cannot coexist with another center in the disk of radius
`R < 1`. Thus at most four squares can own any one of these segments.

The eight segment midpoints in question have both coordinates in `[1,q-1]`. Four
axis-parallel unit squares with a common vertex at any one of those midpoints are
contained in the container and have disjoint interiors.
The capacity bound four is therefore sharp.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
