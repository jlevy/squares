# The merged marker supplies the missing corner seed

This is the new local lemma used to finish C1091. All decimals are exact
rationals. An exclusion means nonmembership in the **open** square; contact
with a face is allowed. No wall, side upper bound, or hypothesis about another
square's orientation is used.

## Theorem

Let an open square Q have side a>1. Suppose it strictly contains

    H=(-.086,0),  M=(.65,.65),

and excludes

    O=(0,0),  G=(.74,1).

Then Q strictly contains

    Z=(-.24,.87).

Equivalently, after translation by (1,1): a square strictly containing
(.914,1),(1.65,1.65), and excluding (1,1),(1.74,2), must strictly contain
**(.76,1.87)**.

## Proof

A square has a canonical frame of one of the two forms

    u=cx+sy, v=-sx+cy,        or        u=cx-sy, v=sx+cy,
    c>=s>=0, c²+s²=1.

Write its strict bands as U<u<U+a and V<v<V+a. An anchor having the same
projection as a target still supplies a strict band to that target.

In the second frame, the projections of O are between those of H and M:

    u(H)=-.086c < 0 <= .65(c-s)=u(M),
    v(H)=-.086s <= 0 < .65(c+s)=v(M).

All four bands of O would be strict. This contradicts its exclusion, including
at an axial or diagonal frame. Thus the first frame must be used.

In the first frame, O has both strict u-bands from H,M and its strict upper
v-band from H. Its exclusion can only be through the lower v-face:

    V>=0.                                                   (1)

Strict ownership of H, with v(H)=.086s, now implies s>0.

At G the lower u-band follows from H. The lower v-band follows from M, because

    v(G)-v(M)=.35c-.09s >= .26c > 0.

Its upper v-band is strict as well, since

    v(G)=c-.74s <= 1 < V+a.

Hence the exclusion of G forces the upper u-face:

    J:=U+a <= u(G)=.74c+s.                                  (2)

We check the four strict bands of Z explicitly.

**Lower u-band.** By Cauchy–Schwarz,

    u(G)-u(Z)=.98c+.13s
               <= sqrt(.98²+.13²)=sqrt(.9773)<1<a.

Combining with (2) yields U=J-a<u(Z).

**Upper u-band.** The strict point M gives

    u(M)-u(Z)=.89c-.22s >= .67c > 0.

**Lower v-band.** The strict point H gives

    v(Z)-v(H)=.87c+.154s > 0.

**Upper v-band.** Equation (1) and the second exact norm margin give

    v(Z)=.87c+.24s
           <=sqrt(.87²+.24²)=sqrt(.8145)<1<V+a.

Thus all four inequalities are strict, proving Z belongs to Q. ∎

## Actual C1091 application

Let A=Q4 be the actual owner of mask258. It strictly owns both original
markers (.914,1),(1.65,1.65). The earlier residual reduction proves (1,1)
strictly in Q0. In the exceptional top-wall branch of the completion,
(1.74,2)=G3 is strictly in N=Q7. These are actual foreign owners, so the
lemma proves

    (.76,1.87) strictly in A.                               (3)

The actual left wall Q8 strictly owns (.914,2),(1,2.4). It excludes (1,1.74)
and the point (3), both strictly in A, and excludes (1.65,2.35), strictly in
N. Its real container wall is x>=0. The all-angle wall theorem
`../../C1089/reference/recovered-lemmas/C981-WALL-CYCLES.md`, Theorem 4,
therefore gives (1,2.8) strictly in Q8. Convexity with Q8's strict F1 yields

    {1} x [2.26,2.8] strictly in Q8.                         (4)

The argument uses A's extra marker as a strict anchor. It never calls A a
singleton and never treats its central marker as globally absent. This is
what permits the actual C981 local support lemmas to be reused safely.
