# C1092 MMMP: the positive right angle is small and only the northeast normal remains

All terminating decimals are exact rational numbers. We retain the actual original open squares, their common side a>1 and disjoint interiors. Owned points are strict; exterior points, closure supports and the genuine boundary-center conditions may be equality. Every angle comparison is over its whole stated interval.

**Theorem.** In the original MMMP family, suppose actual Q10 owns F8 and actual Q5 excludes G8. If actual R=Q10 has a nonnegative canonical frame

    u_R=(d,r), v_R=(-r,d), d>=r>=0,
    d^2+r^2=1,

then

    r/d<1/2.                                      (1)

Moreover, of all face normals of the actual northeast N=Q6 and R, only the northeast downward normal -v_N can separate N from R. In particular R's own downward normal is impossible. The remaining northeast-normal case is not excluded in this chapter.

## 1. The actual entrance and the two southeast sources

Translate by (-2,-2), and write E=Q5. As in `C1092-MMMP-RIGHT-NEAR-BOTTOM-ORIGIN.md`, E has positive canonical frame

    u_E=(c,s), v_E=(-s,c), c>=s>0,
    c^2+s^2=1, s<.21, c>.97.

Write A,H for its upper u_E,v_E faces and put z=s/(1+c). Its strict inward pair is (0,-.26),(.26,0). The foreign actual Q7 center gives H<=0. The strict whole bottom bar [0,.4]x{-1} belongs to actual Q9. Lemma1 of `C1092-MMMP-SOUTHEAST-FLOOR-RIGHT-SIGN.md` gives the exact coupled support

    sA+cH>a(c+s)-1,
    A>a-z,
    H<=0,
    0<z<21/197<.11.                               (2)

This is the genuine whole-bar statement; separate endpoint exclusions do not replace it.

Universal G9 ownership and the present actual F8 ownership give the strict bar

    {1}x[-.26,.4] in R.                           (3)

Let L,K be R's lower u_R,v_R face coordinates and let J=K+a be its upper v_R face. The two strict endpoint projections needed below are

    L<d-.26r, J>-r+.4d.                          (4)

The actual right wall is x<=2 and the actual right center ordinate is nonnegative. Lemma2 of `C1092-MMMP-SOUTHEAST-FLOOR-RIGHT-SIGN.md` uses precisely these conditions, (2), and the strict right origin (1,0) in (3). It excludes both downward E--R normal sources. Therefore a separating normal from E toward R must be one of

    u_E or u_R.                                  (5)

These are full-square separating sources. No bound on an upward center contribution has been assumed.

## 2. Both actual sources force r/d<1/2

Let q,rho be the respective positive and nonnegative canonical angles of E,R. If rho<=q, then immediately

    r/d<=s/c<21/97<1/2.

It remains the complete other angle order rho>=q. Put

    alpha=cd+sr>0, delta=cr-sd>=0.                 (6)

### 2.1. The right square's upward normal

Suppose u_R separates E from R. Its full upper E support is

    upper_E(u_R)=alpha A+delta H.

Set

    A0=[a(c+s)-1]/s.

The strict coupled inequality and H<=0 in (2) imply A>A0. Retaining the coupling gives

    alpha A+delta H
       =(d/c)A+(delta/c)(sA+cH)
       >=(d/c)A+(delta/c)[a(c+s)-1]
        >alpha A0>alpha(1-z).                    (7)

Here the identity d+delta s=c alpha supplies the penultimate coefficient, and

    A0=a-z+(a-1)c/s>1-z.

When delta=0, the first comparison in (7) is equality, while A>A0 keeps the next comparison strict. Thus the joining angle has been included.

Equations (4),(7) show that this separating source requires

    d[-z(c+s)]+r[.26+s(1-z)]<0.                  (8)

Suppose r/d>=1/2. The second bracket is positive. The left side of (8) is then at least

    (d/2)[.26+s(1-z)-2z(c+s)]>0.                 (9)

For the last strict sign, the exact identity is

    2z(c+s)-s(1-z)-.26
       =[3s^2-s(1-c)-.26(1+c)]/(1+c).

Its numerator is strictly smaller than

    3(.21)^2-(.26)(1.97)
      =.1323-.5122=-.3799<0.                     (10)

This contradicts (8). Therefore this source forces r/d<1/2.

### 2.2. The southeast square's upward normal

Suppose instead that u_E separates E from R. Its components in R's frame are alpha,-delta. Hence its full lower R support uses J, the actual upper v_R face, and (4) gives

    lower_R(u_E)=alpha L-delta J
       <alpha(d-.26r)-delta(-r+.4d)
        =c-.66cdr+s(.4d^2-.26r^2).                (11)

The strictness is retained at delta=0 because alpha>0 and the L bound is strict. Since upper_E(u_E)=A>1-z, separation would require

    .66cdr-s(.4d^2-.26r^2)
       <c-1+z=z(1-s)<.11.                        (12)

If r/d>=1/2, then r<=d and the exact factorization

    5dr-2=(2r-d)(2d-r)>=0

gives dr>=2/5. Also .4d^2-.26r^2<=.4. The left side of (12) would consequently be strictly greater than

    (.66)(.97)(2/5)-(.4)(.21)
      =.17208>.11,                               (13)

again a contradiction. Thus this second source also forces r/d<1/2. All possible E--R sources and both relative angle orders have now been covered, proving (1).

## 3. The complete actual northeast normal list

The original positive canonical frame and complete cap table of N are

    u_N=(b,t), v_N=(-t,b), b>=t>0,
    b^2+t^2=1,
    U_N>=.4t, V_N>=.4b-t,
    A_N=U_N+a<=b+t, H_N=V_N+a<=b,
    t/(1+b)>1/4.                                 (14)

These are the conclusions of `C1092-MMMP-NORTHEAST-TOP-CAP.md` transported back to this chart. Its actual strict points needed here are

    M_N=(.35,.35), F=(.4,1), P=(.47,.12).          (15)

The first is its marker, the second its F7, and the third is the universal strict point proved in Theorem1 of `C1092-MMMP-NORTHEAST-LOWER-TIP.md`.

Orient a separating normal from N toward R. The strict pair M_N and (1,.35) in the actual bar (3) forces a positive horizontal component. The complete possible sources are therefore

    u_N, -v_N, u_R, -v_R.                        (16)

The argument below eliminates three members of this list.

### 3.1. The northeast upward normal

The half-angle bound in (14) gives t/b>8/15. The displacement from the strict F=(.4,1) in N to the strict lower endpoint (1,-.26) in R has u_N projection

    .6b-1.26t
       <[.6-(1.26)(8/15)]b=-.072b<0.

It cannot align with a separating support from N to R, so u_N is impossible.

### 3.2. The right upward normal

For completeness this exclusion follows from the full cap table without a restriction on the relative N,R angle. Put

    k=bd+tr>0, j=br-td.

If j<=0, the full upper N support is k A_N+j V_N. The lower-U and upper-H bounds in (14) give

    upper_N(u_R)
       >=k(a+.4t)+j(b-a)
        >d[b+t-.6bt]+r[1+t-b-.6t^2]>d.            (17)

The a coefficient k-j is positive; it is the sum of a positive cosine and the nonnegative magnitude of the other coefficient. The first square bracket in (17) is strictly greater than1, since

    b+t-1=2bt/(1+b+t)>.6bt.

The exact last comparison follows from 1+b+t<=1+sqrt(2)<10/3. The second square bracket is positive because

    1+t-b-.6t^2=(1-b)+t(1-.6t)>0.

If j>=0, the upper support is k A_N+j H_N. The actual caps give

    A_N>=a+.4t>b,
    H_N>=a+.4b-t>-t.

Thus

    upper_N(u_R)>kb-jt=d.                        (18)

The strictness in (18) also holds at j=0 because k>0. But the strict origin (1,0) in R gives lower_R(u_R)=L<d. Both complete angle orders therefore exclude u_R.

### 3.3. The right downward normal

Use the strict N point P=(.47,.12) and the strict R upper endpoint G9=(1,.4). Their displacement has projection on -v_R=(r,-d)

    .53r-.28d
       <[(.53)/2-.28]d=-.015d<0,                 (19)

by (1). This strict point comparison excludes the actual right downward source directly.

At r=0 that source already has zero horizontal component and is absent from the strict cone; (19) remains valid. Thus all canonical endpoints and all potential zero coefficients have been included.

## 4. The precise remaining actual source

The only possible N--R direction left in (16) is

    -v_N=(t,-b).

At the same time, E--R has only its two upward sources (5), and the same actual R satisfies r/d<1/2. These are simultaneous statements about the same three original squares. They do not replace R by separate realizations for its two neighbors.

The proof uses only the actual short bar (3), not G8 in R. It retains the southeast floor and the whole northeast face table from their explicitly cited actual owners. It excludes the right-supplied northeast separator but leaves the last northeast-supplied separator for the coupled three-square ending.
