# Stromquist’s Segment Helper: An Independent Derivation

**Date:** 2026-09-07. **Status:** elementary derivation independently reviewed by a
second mathematics agent and the coordinator; no numerical target or packing bound.
Source:
[Stromquist Memo I](../../../packing/resources/papers/stromquist-1984-packing-unit-squares-inside-squares-i-six-unit-squares.pdf),
printed pp. 13, 15–17, with Figures 12–13 on p. 16 checked from the scan.
The threshold printed throughout is 1/2, not the OCR’s 2.

## Claim and resource

Let A=(1,1), B=(3/2,1), C=(2,1), D=(1,3/2), E=(3/2,3/2). Let T_v=[(1,0),A] and
T_h=[A,B]. An open square Q_A of side >1 in [0,3]^2 containing A and avoiding D consumes
strictly more than 1/2 total length on T_v and T_h. An open square Q_B of side >1
contained in [0,3]^2, containing B and avoiding A,C,E, leaves strictly less than 1/2
total length in the A-connected complementary portions of those segments.
Consequently the two open squares cannot be disjoint.
These hypotheses follow from A and B both being isolated.

The A-connected qualification matters.
The full complement of Q_B on the two segments can include another component below its
vertical trace. Q_A cannot reach that component without intersecting Q_B, because the
intersection of a convex open square with a segment is an interval and Q_A contains A.

The following derivation proves the geometric inequalities without assuming the source
figures’ simultaneous wall/point contacts are a complete list of configurations.

## Notation and identities

Write s=sin(theta), c=cos(theta), z=s+c, with 0<theta<pi/2. Then

```
f=(s+c-1)/(sc)=2/(z+1),       1/2<f<=1.
```

The following identities are exact:

```
(1-f)(1+c/s) = c(s+c)/((1+s)(1+c)) <= 1/2;

f-1+s/(2c) = s(s+c/2-1/2)/(c(1+c)) >= 0;

(f-1/2)(1+c/s)-1/2
  = c(1-s)(1-c+s/2)/(s^2(1+s)) >= 0.
```

For the second, s+c/2-1/2 = (s+z-1)/2 >= 0. For the first, c/(1+c)<=1/2 and
(s+c)/(1+s)<=1. All denominators are positive.

## A-block: direct edge-margin proof

Use orthonormal directions n_1=(c,s), n_2=(-s,c). Let the four positive edge margins of
A in Q_A be a_-,a_+,b_-,b_+, where

```
a_-+a_+=b_-+b_+=ell>1.
```

Thus a_- is the distance in the negative n_1 coordinate from A to the corresponding
edge, and analogously for the others.
Exact clipping gives the two lengths consumed from A along the critical segments:

```
u=min(a_-/s,b_-/c,1),
v=min(a_+/c,b_-/s,1/2).
```

The left wall gives

```
c*a_- + s*b_+ <= 1.
```

D is excluded precisely when at least one of

```
a_+ <= s/2,       b_+ <= c/2
```

holds. It cannot leave through a lower edge, since D-A=(0,1/2) has positive n_1 and n_2
coordinates.

If b_+<=c/2, then b_->1-c/2. Hence b_-/c>1/2 and b_-/s>1/2. If u+v<=1/2 were possible,
its clipping minima would imply a_-/s<=1/2 and a_+/c<=1/2. But then ell=a_-+a_+<=z/2<1,
a contradiction.

Otherwise take a_+<=s/2, and set x=a_+, y=b_-. Then a_-/s>1/2. If u+v<=1/2, the actual
minima must be

```
u=y/c,       v=min(x/c,y/s)<1/2.
```

The wall inequality becomes

```
c*x+s*y >= ell*z-1 > z-1,       x<=s/2.
```

When v=y/s, it follows that y/c>f-1/2 and therefore

```
u+v>(f-1/2)(1+c/s)>=1/2,
```

contradicting the assumed upper bound.
When v=x/c,

```
s(x+y)>z-1+(s-c)x.
```

If s<=c, use x<=s/2 to obtain

```
u+v=(x+y)/c > f-1/2+s/(2c)>=1/2.
```

If s>c, the same inequality gives u+v>f>1/2 directly.
This exhausts the cases.

For an axis-aligned square, exclusion of D and inclusion of A imply its top edge is at
height at most 3/2. Side >1 puts its bottom edge below 1/2, so its vertical consumption
alone is >1/2. Thus the angle endpoints are covered without division by zero.
This proves the A-block assertion for every orientation.

## B-block: cap localization and direct length bound

Its horizontal chord at y=1 contains B and excludes A,C, so both endpoints lie in [1,2]
and its length is at most 1. A chord joining opposite edges of a square of side ell>1
has length ell/s or ell/c, greater than 1. Therefore this chord cuts a proper top or
bottom corner cap. Vertex-transition cases are excluded by the same length bound.
Axis-aligned squares are excluded immediately as their chord length is ell>1.

The bottom cap is impossible by a direct four-facet argument.
Use the same upward directions (c,s),(-s,c) and four positive edge margins of B, denoted
a_-,a_+,b_-,b_+, whose opposite pairs sum to ell.
Exclusion of A and C says

```
A: a_- <= c/2 or b_+ <= s/2;
C: a_+ <= c/2 or b_- <= s/2.
```

The two choices that bound opposite margins give ell<=c or ell<=s, impossible.
The bottom-cap choice a_-<=c/2 and b_-<=s/2 puts E strictly inside: its coordinates from
that corner are a_-+s/2 and b_-+c/2, both positive and at most (s+c)/2<1<ell.
The only remaining choice is a_+<=c/2 and b_+<=s/2, the top cap.

It remains to treat the top cap.
Choose theta so that the descending left edge has direction (-s,-c), and the descending
right edge direction (c,-s). Let t>=0 be the bottom vertex’s height.
The top vertex has height t+ell*z, and the cap depth at y=1 is h=t+ell*z-1. The
horizontal chord length is

```
w=h/(sc) >= (ell*z-1)/(sc) > f.
```

Let v be the distance from A to its left endpoint.
Since its right endpoint is at most C.x=2,

```
0<=v<=1-w<1-f.
```

The descending left edge intersects x=1 at y=1-u with u=(c/s)*v. This intersection is on
the actual edge, rather than its extension: the left vertex has height t+ell*s, and

```
s^2 * ((1-t-ell*s) - (c/s)*(1-w))
  = c[ell(1+sc)-c-s] + t*c^2
  > 0,
```

because 1+sc-c-s=(1-s)(1-c)>=0 and ell>1. Thus 1-u is above that vertex and nonnegative.
Q_B genuinely crosses the vertical segment there.

The A-connected free portions therefore have lengths u and v, and

```
u+v < (1-f)(1+c/s) <= 1/2.
```

This proves the B-block assertion.
Strictness comes from ell>1; neither a common epsilon nor a positive uniform angular gap
was assumed.
The two squares have independent orientation parameters; the inequalities do
not assume they are parallel or share a tilt.

## Consequence and reusable checker

Convexity anchors both Q_A traces at A. If Q_A and Q_B were disjoint, the two Q_A
lengths could not exceed the corresponding A-connected free lengths left by Q_B. The
demand exceeds 1/2, whereas the available length is less than 1/2. This contradiction
gives a complete independent local derivation of the source’s adjacent-singleton
exclusion.

A reusable verifier must establish four things:

1. Exact segment clipping, with open membership, endpoint ownership, and identification
   of the component accessible from the distinguished site.
   Summing the entire free complement is insufficient.
2. The square edge-margin identities and wall inequalities; the cap classification must
   cover all orientations, including axis and vertex-transition exclusions.
3. Universal positivity of the three displayed identities and the edge-validity
   inequality. A half-angle substitution gives rational functions with positive
   denominators, allowing polynomial certificates; a sampled angle sweep would not
   certify these quantified statements.
4. A sound bridge from incidence masks to the geometric hypotheses, followed by the
   convexity/disjointness resource contradiction.

The current allowed-mask control does not assume a stronger adjacent-singleton rule than
the source: its conflicts are exactly the D4 images of perimeter pair A,B. It correctly
excludes pairs involving the center from this premise’s ablation control.
The direct derivation above actually requires fewer exclusions than full isolation: Q_A
contains A and avoids D; Q_B contains B and avoids A,C,E. Generalizing the result to
additional masks would require an explicit new consumer contract, not an unrecorded
change to the current source-premised replay.

The source defines one fixed common side 1+epsilon, with epsilon>0 small.
For the singleton rule, its extension in the existing record to arbitrary side >1 is
safe: one may shrink about the contained singleton to a smaller common side while
preserving that singleton, exclusions, containment, and disjointness.
The direct proof above also establishes the unequal-side version without this reduction.

The separate exact-two-point adjacency condition remains a source assertion on p. 18;
this bounded slice did not independently prove that condition, Lemma 6, Lemma 7, or the
later EH-to-EHJK geometric forcing.
The finite incidence program remains properly labelled conditional until all its
required continuous premises have independent certificates.

The independent audit accepted the inequalities and case exhaustion after making the
B-square’s bottom-wall premise explicit in the opening statement.
The coordinator also checked the four-facet alternatives and the actual-edge inequality.
This is an analytic proof; no sampled-angle computation supplies its universal
quantifiers.

## Kearney–Shiu wording check

The existing n-006 prose’s generic n-1 unavoidable-point argument is not the proof in
Kearney–Shiu Section 3. That proof uses two seven-point lattices related by a quarter
turn and sharing the center, separates the center-covered and center-uncovered cases,
and uses geometric compatibility and segment-intersection bounds to exclude both.
Correcting that prose changes neither s(6)=3 nor its published-proof evidence.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
