# C1092: a wall-center sign forces a strict forward auxiliary

All terminating decimals below are exact rational numbers. An owned point is strictly interior; an excluded point may lie on a face. The lemma uses the actual wall and actual center coordinate and has no angle or auxiliary-ownership premise.

## 1. The continuous wall-sign lemma

**Theorem 1.** Let W be an open square of side a>1, with closure in x≥0. Suppose W strictly owns P=(.914,2), excludes N=(1.65,2.35), and its center ordinate satisfies Y_W≥2. Then W strictly owns

    A=(1,2.26).                                      (1)

No upper side bound, other marker, or additional owner is required.

**Proof.** Translate by (−1,−2). The named points and wall become

    P=(−d,0), N=(b,h), A=(0,r),
    d=.086, b=.65, h=.35, r=.26,
    closure(W)⊆{x≥−1}, center(W)=(X,Y), Y≥0.

Choose absolute canonical components c≥s≥0 with c²+s²=1, and put K=c+s. The square's horizontal support radius is aK/2, so the wall gives

    X≥−1+aK/2.                                      (2)

Write U,V for its lower face coordinates. We repeatedly use

    K≥1+(4/5)cs,
    c≥1−(3/5)s²,
    c≥1/sqrt(2)>7/10.                               (3)

The first identity follows from K−1=2cs/(K+1) and K+1<5/2. For the second, the difference between its two sides is (1−c)(3c−2)/5≥0.

### 1.1. Positive canonical sign

Let u=(c,s), v=(−s,c). Both lower bands of A follow strictly from P, because

    u(A)−u(P)=dc+rs>0,
    v(A)−v(P)=rc−ds≥(r−d)c>0.

If A failed its upper u-band, its center form would give cX+sY≤rs−a/2. Together with (2) and Y≥0 this would require

    a(1+cK)≤2c+2rs.

But

    1+cK−2c−2rs=(1−c)²+s(c−.52)≥0,

contradicting a>1. Thus A's upper u-band is strict.

Suppose its upper v-band failed, so V+a≤rc. We determine N's possible exit. Its lower u-band follows from P. A lower v-face exit would give opposed-face width

    a≤v(A)−v(N)=bs+(r−h)c=.65s−.09c<1,

which is impossible. An upper v-face exit at N is impossible as well. Indeed U<u(P)=−dc and V+a≤v(N)=−bs+hc would imply

    Y=s(U+a/2)+c(V+a/2)
      ≤hc²−(b+d)cs−(c−s)/2
       =c(.35c−1/2)+s[1/2−.736c]<0.                (4)

Both bracketed coefficients are negative by (3). This contradicts Y≥0. Therefore N must exit through its upper u-face, U+a≤bc+hs. Together with the assumed upper-v exit of A, this gives

    Y≤rc²+hs²+bcs−aK/2
      <−.24c²−.15s²+.25cs<0.                       (5)

The first strict bound uses (3). For the last sign,

    .24c²+.15s²−.25cs
      =.15(c−s)²+.09c²+.05cs>0.

This contradiction proves all four strict bands of A for the positive sign, including s=0 and c=s.

### 1.2. Negative canonical sign

Let u=(c,−s), v=(s,c). The lower v-band of A follows strictly from P.

If its upper v-band failed, (2) and Y≥0 would require

    a(1+sK)≤2s+2rc.

This is impossible because

    1+sK−2s−2rc=(1−s)²+c(s−.52)>0.                (6)

For s≥.52 both terms on the right are nonnegative and the first is positive. For s≤.52, use c≤1 and the nonpositive coefficient s−.52 to bound it below by

    (1−s)²+s−.52=(s−1/2)²+.23>0.

Next suppose A failed its upper u-band. If rs≥dc, this band is already strict by P. We may therefore assume

    rs<dc.                                         (7)

The strict lower v-band of P gives sX+cY<−ds+a/2. Hence

    c(cX−sY)=X−s(sX+cY)
      ≥X+ds²−as/2
      ≥−1+ac/2+ds²,

while the assumed upper-u failure gives c(cX−sY)≤−rcs−ac/2. Thus

    ac≤1−ds²−rcs.                                  (8)

At s=0 this says a≤1. At s>0, (3) and (7) yield

    c+ds²+rcs−1
      ≥s[rc−(.6−d)s]>0,

since

    r²−d(.6−d)=5849/250000>0.

This contradicts (8), because a>1 and c>0. A's upper u-band is therefore strict.

Only its lower u-band could still fail. Suppose U≥−rs. Both lower bands of N follow strictly from P: their projection increments are

    (b+d)c−hs≥(.736−.35)c>0,
    (b+d)s+hc>0.

An upper u-face exit at N would give

    a≤u(N)−u(A)=bc+(r−h)s=.65c−.09s<1,

so N must exit through its upper v-face, V+a≤bs+hc. It follows that

    Y=−s(U+a/2)+c(V+a/2)
      ≤rs²+bcs+hc²−aK/2
      <−.15c²−.24s²+.25cs<0,                       (9)

where

    .15c²+.24s²−.25cs
      =.15(c−s)²+.09s²+.05cs>0.

Again Y≥0 is contradicted. Thus A has all four strict bands in the second sign too. Every exterior assignment was weak; strict ownership follows from the displayed positive margins and a>1. ∎

## 2. Exact applications to the original C1092 wall signs

Use the supplied original C1092 owner numbering and marker/auxiliary convention. Every application below uses an original marker outside the wall square's original marker group. Thus the required exclusion is independent of all 55,126 auxiliary alternatives. The table states every coordinate used in these applications explicitly.

| Actual owner | Closed center sign | Original owned wall marker | Excluded original central marker | Compulsory strict auxiliary |
|---|---|---|---|---|
| Q8 | Y8≥2 | (.914,2) | (1.65,2.35) | F1=(1,2.26) |
| Q9 | X9≥2 | (2,.914) | (2.35,1.65) | G5=(2.26,1) |
| Q10 | Y10≥2 | (3.086,2) | (2.35,2.35) | F9=(3,2.26) |
| Q11 | X11≥2 | (2,3.086) | (2.35,2.35) | G7=(2.26,3) |
| Q11 | X11≤2 | (2,3.086) | (1.65,2.35) | G4=(1.74,3) |

The transports from Theorem 1 are respectively the identity, (x,y)↦(y,x), (x,y)↦(4−x,y), (x,y)↦(y,4−x), and (x,y)↦(4−y,4−x). Each maps the wall, marker, central exclusion and center sign simultaneously. In particular, equality of a wall-center coordinate with 2 is included.

Consequently the original MMMM class has the first four compulsory auxiliaries. The original MMMP class has the first three and the last compulsory auxiliary. This is a proved continuous ownership reduction from the whole original entrance; it is not by itself an exclusion of either wall class.
