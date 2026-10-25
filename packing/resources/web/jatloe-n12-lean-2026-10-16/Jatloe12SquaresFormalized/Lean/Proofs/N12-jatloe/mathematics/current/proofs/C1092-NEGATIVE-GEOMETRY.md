# C1092: the enlarged negative geometric theorem and its actual application

All finite decimals in this file are exact rationals. Owned points are strictly
inside their actual squares. Excluded points may lie on their boundaries.

## 1. A weaker entrance, valid through half-angle 1/8

**Theorem.** Let eight distinct open squares C₀,…,C₃,B₀,…,B₃ have one common
side a>1, pairwise disjoint interiors, and closures in [0,4]². Put
R(x,y)=(4−y,x), and describe Cᵢ and Bᵢ in the chart R^(−i). Indices are
cyclic. Suppose that in these charts the following assertions hold.

1. Cᵢ has normals n(qᵢ)=(c(qᵢ),−s(qᵢ)) and (s(qᵢ),c(qᵢ)), where

       c(t)=(1−t²)/(1+t²),  s(t)=2t/(1+t²),
       q₀=h,  0≤h≤1/8,  |qᵢ|≤h.

2. Cᵢ strictly owns U=(1,87/50), T=(87/50,2), and excludes A=(1,1).
   Its center C satisfies

       27/20≤Cₓ≤3/2,   Cᵧ≥3/2.

3. With J the center of Cᵢ₊₁ in the same chart,

       0≤Jₓ−Cₓ≤11/10,   −1/2≤Jᵧ−Cᵧ≤0.

4. Bᵢ has normals (b_c,b_s), (−b_s,b_c), where b_c²+b_s²=1,
   b_c≥49/50 and |b_s|≤19/100. Its center B satisfies

       Bₓ≤9/5,   |Cₓ−Bₓ|≤1/4,   0≤Cᵧ−Bᵧ≤3/2.

5. Bᵢ strictly owns P=(2,1), L=(8/5,1).

Then this configuration is impossible. There is no upper bound on a.

The center lower bound is 27/20, rather than the handoff's 283/200. This
specific weakening is what permits application to both terminal ranges 50
and 51. The proof below derives the support inequalities needed by the
proved scalar theorem in C1092-CYCLES.md; it does not assume them.

## 2. Forced central faces

The point D=(1,2) is automatically excluded from every central square:
the preceding actual boundary square Bᵢ₋₁ owns it, because its local
point P=(2,1) becomes R^(−1)P=(1,2) in sector i. Thus the cyclic
boundary-point hypothesis also proves every needed D exclusion.

Throughout |q|≤1/8,

    c(q)≥63/65,   |s(q)|≤16/65<1/4.

If q≥0, write C=c(q), S=s(q)≥0, so the first normal is (C,−S).
Comparison of D with strict U rules out the upper first face and lower
second face. Comparison with strict T rules out the upper second face.
Thus D exits at the lower first face:

    C(1−Cₓ)−S(2−Cᵧ)≤−a/2.                              (1)

Here and below "exits" includes equality at a face. With Cₓ≤3/2≤Cᵧ,
(1) implies a≤C+S.

If q=−r<0, put C=c(r), S=s(r)>0, so the normals are (C,S), (−S,C).
U rules out D's lower first and lower second faces; T rules out its upper
first face. Therefore D exits at the upper second face. A cannot exit at
the lower second face: its projection distance from D in that normal is
C≤1<a. U prevents A from exiting at either upper face. A therefore exits
at the lower first face:

    C(1−Cₓ)+S(1−Cᵧ)≤−a/2.                              (2)

All these conclusions allow every boundary contact of A and D.

## 3. A moving strict boundary point

When b_s>0, the actual boundary square strictly owns

    Q=(2−b_s/10,1+b_s/2).                                (3)

Indeed its first projection lies strictly below that of P because
b_s(−b_c/10+b_s/2)≤−3b_s/1000<0. Its first projection lies above that
of L because b_c(2/5−b_s/10)+b_s²/2>0. Its second projection lies above
that of P because b_s²/10+b_cb_s/2>0. These prove three strict bands.

For the fourth band, the actual wall gives Bᵧ≥a(b_c+b_s)/2. Together
with Bₓ≤9/5 and a>1, this yields

    (−b_s,b_c)·(Q−B)−a/2
      < −(1−b_c)²/2−b_s/5+b_s²/10<0.                    (4)

The last inequality follows from 0<b_s≤19/100. Thus all four bands in
(3) are strict. No point surrogate for B or independent side variable was
introduced.

## 4. The widened wall strip

For q≥0 the right-lower central vertex is

    Z=(Cₓ+a(C−S)/2, Cᵧ−a(C+S)/2).

Since C−S≥47/65 and a>1,

    Zₓ>27/20+47/130=89/52>17/10.                        (5)

By a≤C+S and Cₓ≤3/2,

    Zₓ≤3/2+(C+S)(C−S)/2≤2.                             (6)

These are the only uses of the numerical lower bound for Cₓ in the
geometric argument. In particular the old bound 283/200 is unnecessary.

Let (x,y)=C−B. A horizontal first normal from either square has projection
of absolute value at most 1/4+(1/4)(3/2)=5/8<1. An upward second normal
has projection at least −1/16>−1, because y≥0. Disjoint side-a squares
require a separating projection of magnitude at least a>1 on one of
their side normals. Hence only an upward second normal, from C or B,
can separate B below C.

Suppose Zᵧ≤1. For the central upward normal (S,C), (6) gives
(S,C)·(Z−P)≤0. The same comparison with P applies to the boundary
upward normal when b_s≤0. Either contradicts the separating order:
a closed point of C must have strictly larger projection than the strict
point P of B, even if the squares touch.

For the remaining case b_s>0 and boundary normal (−b_s,b_c), use (3).
By (5) and Zᵧ≤1,

    (−b_s,b_c)·(Z−Q)
      < b_s(3/10−b_s/10−b_c/2)<0,                       (7)

because b_c/2≥49/100. This is the same contradiction. Consequently

    Cᵧ>1+a(C+S)/2                                      (8)

for every q≥0, including q=0.

## 5. Exact cyclic upper bounds

Write each local center as (2−Xᵢ,2−Yᵢ). Put

    c=c(h), s=s(h), w=c+s, d=c−s,
    Fᵢ=wXᵢ+dYᵢ.

For q=qᵢ≥0, (1) and (8) give

    c(q)Xᵢ−s(q)Yᵢ≤c(q)−a/2,
    Yᵢ≤1−a(c(q)+s(q))/2.

Their elimination multipliers w and w s(q)+d c(q) are positive.
Replacing a by 1 on the resulting upper bound gives

    Fᵢ≤E(h,q)=2c−w(1−s(q))/c(q)+s c(q)−c s(q)
             =1−D(h,q).                                (9)

The exact rational identity for D is the nonnegative formula proved in
C1092-CYCLES.md §1.

For q=−r<0, (2) gives

    c(r)Xᵢ+s(r)Yᵢ≤c(r)+s(r)−a/2,
    Yᵢ≤1/2.

The coefficient needed for elimination satisfies

    c(r)d−w s(r)≥(63²−2·63·16−16²)/65²
                =1697/4225>0.

It follows that

    Fᵢ≤c+w r/(1+r)=1+r−D(h,−r).                        (10)

Again D is exactly the displayed rational formula in C1092-CYCLES.md.
Thus, throughout the full range h≤1/8,

    Fᵢ≤1+max(−qᵢ,0)−D(h,qᵢ).                          (11)

## 6. Actual central separation and closure

Let (x,y)=J−C. A second normal from either central square has projection
of absolute value at most (1/4)(11/10)+1/2=31/40<1.
A forward first normal has projection at least −1/8>−1, since x≥0
and |y|≤1/2. Thus only a forward first normal of an endpoint can separate
each adjacent pair.

For endpoint parameters u,v, the difference between their chosen near-
horizontal angles has positive cosine: its absolute value is at most
4 arctan(1/8)<π/2. The exact sum of the two support radii is

    a[1+G(u,v)],
    G(u,v)=|u−v|(1+uv−|u−v|)/[(1+u²)(1+v²)]≥0.

The identity follows directly from the sine and cosine subtraction
formulas. Transport the selected endpoint normal to n(h). The vertical
term is nonnegative because y≤0 and s increases on this range. The
horizontal loss is at most

    (11/10)[max(c(u),c(v))−c(h)].

The next center in the current chart is (2+Yᵢ₊₁,2−Xᵢ₊₁), so

    Σ n(h)·(Jᵢ−Cᵢ)=Σ Fᵢ.

Combining the lower support bounds with (11) now gives exactly

    0≥4(a−1)+Φ,

where Φ is the scalar expression proved nonnegative in C1092-CYCLES.md.
Since a>1, this is impossible. The proof covers h=0, equal angles, ties
for the maximum, either endpoint normal source, and touching boundaries.

## 7. Application to the formerly hard negative ranges 50 and 51

Use the original last MPPM auxiliary assignment

    (0,0,0,0,9217,32848,590336,16424,2050,4100,262400,131200).

Take Cᵢ to be owner 4+i and Bᵢ to be owners 9,10,11,8 respectively,
in the same cyclic charts as the theorem. The preserved incoming
maximal-angle deductions terminate at the states

    maxangle-mppm23-k50-1-segments-seed,
    maxangle-mppm23-k51-1-segments-seed.

Their exact rational center enclosures give the following common bounds,
each already combined over all four sectors. These deliberately coarse
fractions follow by outward rounding of the endpoint coordinates:

| Quantity | Both ranges satisfy | Required by the theorem |
|---|---:|---:|
| Cₓ | 7/5<Cₓ<29/20 | 27/20≤Cₓ≤3/2 |
| Cᵧ | Cᵧ>31/20 | Cᵧ≥3/2 |
| Jₓ−Cₓ | 19/20<Jₓ−Cₓ<51/50 | 0≤Jₓ−Cₓ≤11/10 |
| Jᵧ−Cᵧ | −21/100<Jᵧ−Cᵧ<−13/100 | −1/2≤Jᵧ−Cᵧ≤0 |
| Bₓ | Bₓ<8/5 | Bₓ≤9/5 |
| abs(Cₓ−Bₓ) | <9/50 | ≤1/4 |
| Cᵧ−Bᵧ | 1<Cᵧ−Bᵧ<28/25 | 0≤Cᵧ−Bᵧ≤3/2 |
| b_c | ≥7296/7345>99/100 | ≥49/50 |
| abs(b_s) | ≤847/7345<3/25 | ≤19/100 |

The smallest Cₓ in range 50 is 28179691/20000000, and in range 51 it
is 141303367/100000000. Both exceed 27/20; neither exceeds the old
unnecessary common threshold 283/200. This is why a literal application
of the earlier entrance would have been invalid.

For every sector in each range the preserved strict compulsory hulls
contain the following points after rotation to that sector:

| Actual owner | Strict points used |
|---|---|
| Central owner 4+i | U=(1,87/50), T=(87/50,2) |
| Boundary owner 8+(i+1 mod 4) | P=(2,1), L=(8/5,1) |
| Corner owner i | A=(1,1) |
| Preceding boundary owner 8+i | D=(1,2) |

Thus A,D are excluded from the central square by actual disjointness.
The strict hull statements allow a point on the boundary of the hull:
the convex hull of finitely many strict points remains strictly in the
open convex square. All 48 indicated memberships were checked with
exact rational oriented edge inequalities; the rational endpoint record
is included in NEGATIVE-50-51-ENTRANCE-DATA.txt.

For raw half-angle t in [k/64,(k+1)/64], the near-horizontal negative
normal has parameter q=(1−t)/(1+t). Hence range 50 has

    13/115≤h≤7/57<1/8,

and range 51 has

    3/29≤h≤13/115<1/8.

The actual maximal-angle choice gives |qᵢ|≤h, with ties retained. Every
physical hypothesis of the enlarged theorem therefore holds at these
two endpoints. The continuous contradiction replaces both old terminal
adaptive covers in full.

### Precise retained dependency

This application retains the incoming geometric deductions that produced
the two endpoint states. It does not assert that the final MPPM ownership
pattern alone implies all the displayed center and point facts. In
particular the original common-parent deductions, the 431 parametric
cuts, and the two incoming maximal-angle histories are not deleted by
this result. The terminal negative calculations are replaced; a direct
entrance from the original MPPM markers remains a separate task.

The earlier negative ranges 52–63 already satisfy the stronger old
entrance and have h≤3/29. They are also covered by this single enlarged
theorem. Thus every negative terminal range 50–63 now shares the same
continuous ending, once its preserved incoming hypotheses are supplied.
