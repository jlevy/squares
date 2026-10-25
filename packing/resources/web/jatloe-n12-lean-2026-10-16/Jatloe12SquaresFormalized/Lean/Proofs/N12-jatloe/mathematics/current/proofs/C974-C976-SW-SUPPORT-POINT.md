# A southwest strict point from the actual lower and southeast neighbours

Every terminating decimal denotes an exact rational. All square memberships are strict; exterior faces and separating supports may be tangent. This theorem uses a>1 but no upper bound on a and no container wall.

## 1. The theorem

**Theorem 1.** Let A be an open square of side a>1 strictly owning

    M=(1.65,1.65), P=(2,1.74), D=(1.74,2),
    E=(1.5,2), F=(2,1.5).

Suppose it excludes N=(1.65,2.35), R=(2.35,1.65), O=(2,1),
the points L=(1,1.6), J=(1,1.74), and the two complete segments

    B Z=[1.5,1.74]×{1},
    R G=[(2.35,1.65),(2.26,2)].

Then A strictly owns

    X=(1.27,1.96).                                      (1)

The two segments need not share an owner. In the applications each is the strict segment of its own specified actual neighbour. No segment joining different owners is used.

## 2. Two lower-face consequences

For a positive canonical frame u=(c,s), v=(−s,c), with c≥s≥0 and c²+s²=1, let U,V be the lower face coordinates of A. Write B0=(1.6,1), a point of the excluded segment B Z.

At B0 both upper bands follow from M. If B0 were lower u, then N would have its upper u band strictly because

    u(N)−u(B0)=.05c+1.35s≤1.4/sqrt(2)<1<a.

Both lower bands of N follow from M, so N would be upper v. At R its lower u band follows from M, its upper v band from D, and its upper u band would be strict because

    u(R)−u(B0)=.75c+.65s≤sqrt(.985)<1<a.

Thus R would be lower v. The opposite v width from R to N is .7(c+s)≤.7sqrt(2)<1, impossible. Therefore

    V≥v(B0)=c−1.6s.                                    (2)

At J its upper u band follows from D, and its lower v band from M. An upper v exclusion would combine with (2) to give

    a≤v(J)−v(B0)=.74c+.6s≤sqrt(.9076)<1.

Hence

    U≥u(J)=c+1.74s.                                    (3)

Apply this same argument after exchanging x and y. The strict anchors M,P,D remain available, and the excluded B0,J,N,R become the given L,Z,R,N. Thus in a negative canonical frame u=(c,−s), v=(s,c) we have

    U≥u(L)=c−1.6s,   V≥v(Z)=1.74s+c.                  (4)

These statements include s=0 and c=s. At each zero coordinate difference, the comparison is with an already strict owned anchor.

## 3. The actual southeast segment leaves two separating supports

Translate all coordinates by (−2,−2) for the remainder of the local proof. Thus

    M=(−.35,−.35), P=(0,−.26), D=(−.26,0),
    E=(−.5,0), F=(0,−.5), X=(−.73,−.04),
    R=(.35,−.35), G=(.26,0), O=(0,−1).

The segment R G lies on w·z=k, where

    w=(35,9),  k=91/10.                                (5)

A square disjoint from a closed segment admits weak separation along one of its own two face normals or the segment normal. This follows, for example, by taking the difference of the closed square and the segment: its edge normals are precisely these three directions. If none weakly separated, the origin would be interior to that difference, and the segment would meet the open square.

Orient the candidate separation so that A lies below the foreign segment. The opposite u direction is impossible because R is strictly above A's lower u face by comparison with M, in either sign. The opposite v direction is impossible because G is strictly above the lower v face by comparison with P in either sign. The direction placing A above the segment in w is impossible because w·M<k.

Separation placing A below the segment in v is also impossible. In a positive frame v(D)−v(R)=.61s+.35c>0. In a negative frame it would give V+a≤v(R), whereas (4), now translated, gives V≥−.26s−c. The resulting width is

    a≤v(R)−v(Z)=.61s+.65c≤sqrt(.7946)<1.

Consequently at least one of these two inequalities holds:

    U+a≤u(G),                                         (6)
    upper_A(w)≤k.                                     (7)

The first actual upper-u bound may be stronger; the endpoint G is enough for (6).

## 4. Positive canonical angles: the lower u band

Use u=(c,s), v=(−s,c). The target's upper u band is strict by E, and its lower v band is strict by M. The coordinate increments are .23c+.04s>0 and .38s+.31c>0.

If (6) holds, its lower u band follows because

    u(G)−u(X)=.99c+.04s≤sqrt(.9817)<1<a.

It remains to treat (7). Put

    α=35c+9s>0,  β=9c−35s,
    t=s/(1+c)∈[0,sqrt(2)−1]⊂[0,5/12].

Suppose X were lower u, U≥u(X). For β≥0, (2) gives V≥.4s−c in translated coordinates, and therefore

    upper_A(w)≥αu(X)+β(.4s−c)+a(α+β).

Since a>1, this is strictly greater than k if

    f1=α+β−α(.73c+.04s)+β(.4s−c)−k>0.                (8)

Here β≥0 implies t<1/7: the ratio s/c at t=1/7 is 7/24>9/35. The exact positivity certificate in Section 7 proves (8) on the larger closed interval 0≤t≤1/7.

For β≤0 use strict ownership of P to get V<−.26c. Now

    upper_A(w)=α(U+a)+βV
       ≥α(u(X)+a)−.26cβ,

with a strict inequality when β<0; the factor a>1 makes the comparison strict also at β=0. It is therefore enough that

    f2=α(1−.73c−.04s)−.26cβ−k>0.                     (9)

The condition β≤0 implies t>1/8, since s/c=16/63<9/35 at t=1/8. Section 7 proves (9) on [1/8,5/12]. Both possibilities contradict (7). Thus X has its lower u band strictly for every positive canonical angle.

## 5. Positive canonical angles: the upper v band

For τ=s/c≥3/4, (2) gives the required upper v band directly: the opposite gap from B0 to X is .96c+.33s, which decreases for τ≥3/4 and at the endpoint equals

    (.96)(4/5)+(.33)(3/5)=483/500<1.

Assume τ≤3/4 and suppose that X were upper v, V+a≤v(X). The point B=(1.5,1) has both upper bands from M. Its lower v band is strict because

    v(X)−v(B)=.96c+.23s≤sqrt(.9745)<1<a.

Hence B is lower u. At N both lower bands follow from M, and its upper u band follows from the opposite lower face at B:

    u(N)−u(B)=.15c+1.35s≤93/100<1

on τ≤3/4. Thus N is upper v. At R its lower u band follows from M and its upper v band from D. If R were lower v, the two opposite v faces at R,N would give width .7(c+s)<1. Therefore R must be upper u.

At Z=(1.74,1), the upper u band follows from D, and the upper v band from M. Its lower u band is strict from the upper face at R, because

    u(R)−u(Z)=.61c+.65s≤sqrt(.7946)<1<a.

Thus Z is lower v. The complete segment B Z joins a point strictly above the lower v face and weakly left of the lower u face to a point strictly right of the lower u face and weakly below the lower v face. Both upper bands are strict along the segment. Since B Z lies on y=1, its exclusion forces the lowest closed vertex of A to satisfy

    sU+cV≥1                                             (10)

in the original coordinates. Indeed if that vertex were below y=1, a nonempty part of the segment between its two lower-face crossings would satisfy all four strict bands. Equality in (10) is exactly the possible vertex tangency.

Use the upper-u face at R and the supposed upper-v face at X in (10). They imply

    a(c+s)≤.96−.31s²+1.08cs.                           (11)

The half-angle satisfies 0≤t≤1/3 because τ≤3/4. The exact positive polynomial certificate for

    f3=c+s−.96+.31s²−1.08cs

on that interval is given in Section 7. Thus (11) contradicts a>1. This proves the fourth target band for the positive sign.

## 6. Negative canonical angles

Use u=(c,−s), v=(s,c). The target's upper u band is strict from E, with difference .23c−.04s≥.19c>0. Its upper v band is strict from D, with difference .47s+.04c>0.

If (6) holds, the lower u band follows from u(G)−u(X)=.99c−.04s≤.99<1. Strict ownership of F also gives .5s<.26c, hence s/c<.52. In that interval its lower v band follows from M because

    v(X)−v(M)=.31c−.38s>.1124c>0.

Now assume (7), and put

    α=35c−9s>0,  β=35s+9c>0.

First suppose the lower v band of X failed. When s/c≤3/4 it is already strict by M, since .31c−.38s≥.025c>0. Thus only s/c≥3/4 remains. Equation (4) gives, in translated coordinates, U≥−c+.4s≥−c+.26s. Hence the lower-v failure and a>1 would yield

    upper_A(w)>α(−c+.26s)+β(−.73s−.04c)+α+β.

The right side minus k is

    44c+26s+7.47s²+10.13cs−44.46>0,

because c>7/10 and s≥3/5 in this interval, so its first two terms already exceed 46.4. This contradicts (7). The lower v band is proved.

Finally suppose the lower u band of X failed. At O=(0,−1), its lower u band and upper v band follow from P. It must be lower v or upper u.

If O is lower v, V≥−c. The supposed lower-u face at X then gives

    upper_A(w)>α+β+α(−.73c+.04s)−βc.

Section 7 proves that the last expression exceeds k throughout the canonical interval. This is the polynomial f4 there.

If O is upper u, then U+a≤s, so the target's lower-u failure implies

    a≤.73c+.96s.

The right side increases throughout the canonical interval; at t=4/25 its exact value is 63657/64100<1. Thus t>4/25. Equation (4) gives V≥−.26s−c, and we obtain

    upper_A(w)>α+β+α(−.73c+.04s)+β(−.26s−c).

The expression exceeds k by the polynomial f5 of Section 7 on [4/25,5/12]. This again contradicts (7). The two weak exterior alternatives for O are exhaustive even when both hold. All target bands are now strict in both canonical signs. ∎

## 7. Exact polynomial certificates

The following certificates are finite algebraic identities on entire closed intervals, not angle enumerations. For t∈[l,r] put z=(t−l)/(r−l). A degree-four polynomial p has the displayed Bernstein form

    p(t)=Σ(j=0,...,4) binom(4,j) b_j z^j(1−z)^(4−j).

All displayed coefficients b_j are positive. The five basis terms are nonnegative and sum to one, including at the interval endpoints, so p(t)>0 on its whole interval.

Here p_i=(1+t²)² f_i after substituting c=(1−t²)/(1+t²), s=2t/(1+t²). For f4 and f5, subtract k from their displayed support expressions in Section 6. The exact polynomials are

    p1=(35+926t−654t²−11326t³−8765t⁴)/100,
    p2=(−199+2026t+3614t²+1574t³−7199t⁴)/100,
    p3=(1−4t−17t²+104t³−49t⁴)/25,
    p4=(35−206t+4946t²+10606t³−8765t⁴)/100,
    p5=(35−674t+1306t²+11074t³−8765t⁴)/100.

Their complete coefficient data are:

| Polynomial | Interval [l,r] | (b0,b1,b2,b3,b4) |
|---|---|---|
| p1 | [0,1/7] | (7/20,953/1400,4847/4900,167/140,14078/12005) |
| p2 | [1/8,5/12] | (458897/409600,2008619/614400,16363519/2764800,12362191/1382400,24250201/2073600) |
| p3 | [0,1/3] | (1/25,2/75,1/1350,1/1350,83/2025) |
| p4 | [0,5/12] | (7/20,13/96,11681/8640,409031/69120,5436479/414720) |
| p5 | [4/25,5/12] | (16287/7812500,10925491/37500000,31314797/27000000,24524261/8640000,429475/82944) |

Every identity follows by expanding the displayed five terms. Since (1+t²)²>0, these certificates establish precisely the strict scalar comparisons used above.

## 8. Exact C974/C976 application

In either remaining pair the southwest owner A=Q5 owns the five theorem anchors: its original marker, F4,G3, and both proved central crosspoints. For explicit traceability, F=(2,1.5) is the half-turn application of the retained central crosspoint lemma from the appendix of `C893-CONTINUOUS-EXCLUSION.md`, with the complete owner mapping written under “Exact C974 and C976 consequence” in `ELBOW-CROSSPOINT.md`. Its foreign points (1,1.5),(1,1.6) lie in actual Q1, and its foreign southeast and northwest markers are the original Q6 marker and the absent or Q8-owned northwest marker. Transpose that whole application to obtain E=(1.5,2): the two singleton roles Q0,Q1 exchange, the required points (1.5,1),(1.6,1) lie in Q0's strict horizontal segment, and the same two foreign central markers exchange. Both point premises therefore hold in the actual configuration, independently of the theorem being proved here.

The excluded N is the northwest marker, absent in C974 and in distinct actual Q8 in C976. R is the original marker in actual Q6. O=(2,1) is strict in actual Q9 by the completed bottom-origin transfer.

The excluded points L=(1,1.6) and J=(1,1.74) belong to actual Q1. The whole segment [1.5,1.74]×{1} is strict in actual Q0, whose retained strict segment runs from (1.12,1) to (1.74,1). Finally the whole segment R G is strict in actual Q6=327936, which owns its southeast marker R and G6=(2.26,2).

Theorem 1 therefore gives (1.27,1.96) strictly in actual Q5 in both remaining central pairs and both original families. It does not by itself exclude either family; the companion `C976-MERGED-LEFT-ENDING.md` uses the point to close the positive mixed-northeast branch of C976.
