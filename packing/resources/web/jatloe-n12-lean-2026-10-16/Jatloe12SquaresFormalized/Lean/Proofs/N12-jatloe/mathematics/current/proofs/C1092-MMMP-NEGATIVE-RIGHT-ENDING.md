# C1092 MMMP: a nonpositive right angle forces the northeast half-angle above one third

All terminating decimals are exact rational numbers. The squares are the original actual open squares of common side a>1, with disjoint interiors. Owned points are strict. Exclusions, closure supports, the genuine right wall and the closed right-center sign retain possible equality throughout.

**Main theorem.** In the original MMMP family, suppose actual Q10 owns F8=(3,1.74) and actual Q5 excludes G8=(3,1.6). If Q10 has a nonpositive canonical angle, then the positive canonical angle theta of actual Q6 satisfies

    tan(theta/2)>1/3.

Only the strict Q10 bar {3}x[1.74,2.4] is needed. In particular G8 need not belong to Q10. Combined with `C1092-MMMP-NORTHEAST-UPPER-THIRD.md`, this excludes the whole nonpositive right-angle part of the stated branch. No positive-right sign theorem is used in the proof.

## 1. Exact actual-square entrance

Translate by (-2,-2), and write

    E=Q5, N=Q6, R=Q10.

The theorem `C1092-MMMP-RIGHT-NEAR-BOTTOM-ORIGIN.md` gives E the positive canonical frame

    u_E=(c,s), v_E=(-s,c), c>=s>0,
    c^2+s^2=1, s<.21, c>.97.

E strictly owns

    M_E=(.35,-.35), I=(0,-.26), D=(.26,0).

The actual Q7 owns O=(0,0), and the actual Q9 owns the whole strict bar [0,.4]x{-1}. Let U_E,V_E be E's lower faces and

    A=U_E+a, H=V_E+a, z=s/(1+c).

The four-band missing-O argument and **Lemma1 only** of `C1092-MMMP-SOUTHEAST-FLOOR-RIGHT-SIGN.md` give

    H<=0, A>a-z,
    0<z<21/197<.11.                              (1)

That lemma is the actual-bottom-bar proof of s A+c H>a(c+s)-1. It uses the entire strict bar, including exclusion of a closure vertex lying on its interior, to establish A>a-z. No assertion about the right square's angle from any later section of that file is used here. Strict D also gives

    H>-.26s.                                     (2)

Universal right-far ownership puts G9=(3,2.4) strictly in the same actual R. Its strict F8, which is the premise of this theorem, and convexity therefore give

    {1}x[-.26,.4] strictly in R.                  (3)

The genuine original wall and MMMP center sign become

    closure(R) subset {x<=2},
    center_y(R)>=0.                              (4)

The full top-cap theorem gives N the positive original canonical frame

    u_N=(b,t), v_N=(-t,b), b>=t>0,
    b^2+t^2=1,

with lower faces U_N,V_N and upper faces A_N=U_N+a,H_N=V_N+a satisfying

    U_N>=.4t, V_N>=.4b-t,
    A_N<=b+t, H_N<=b,
    tan(theta/2)>1/4.                            (5)

This is the literal translation of `C1092-MMMP-NORTHEAST-TOP-CAP.md`; all four faces concern this one actual N. Its strict marker and F7 are

    M_N=(.35,.35), F=(.4,1).                     (6)

Thus every strict point, bar, wall and face in the argument belongs to its stated actual original owner. In particular (3) uses F8 and G9, rather than presumed G8 ownership.

Suppose now that R has a nonpositive canonical frame

    u_R=(B,-T), v_R=(T,B), B>=T>=0,
    B^2+T^2=1.

Write L,K for its lower face coordinates. The endpoints of the actual bar (3) give

    L<B-.4T, K<T-.26B.                           (7)

The strict inequalities in (7) are projections of strict points of R.

## 2. The southeast square forces T/B<1/2

Orient a separating normal from E toward R. The strict points D=(.26,0) in E and (1,0) in the actual bar (3) force its horizontal component to be strictly positive. The complete possible face-normal sources are therefore

    u_E, -v_E, u_R, v_R.                         (8)

At T=0 the last direction has zero horizontal component and is already excluded. Retaining it in the estimates below only enlarges the list to be eliminated.

Set

    k=cB-sT>0, h=sB+cT>0.                       (9)

The positivity of k follows from c>.97, s<.21 and T<=B.

### 2.1. Three normal sources are impossible

For -v_E=(s,-c), compare the strict I in E with the strict upper endpoint (1,.4) in R. The displacement has scalar product

    s-.66c<.21-(.66)(.97)<0.

It cannot point strictly from the first square to the second along a separating support. Thus this source is impossible.

For R's own downward normal u_R, its full upper E support is

    upper_E(u_R)=k A-h(H-a).

Using (1), a>1 and (9),

    upper_E(u_R)>k(1-z)+h
                  =B(c+z)+T(1-s)>B.              (10)

The identity in (10) follows from

    c+s-cz=c+z, c-s+sz=1-s.

Its final strict inequality follows from

    c+z-1=z(1-s)>0.

But lower_R(u_R)=L<B by (7). This source is also impossible.

For R's upward normal v_R, its full upper E support is h A+k H. Equations (1),(2) give

    upper_E(v_R)>h(1-z)-.26s k.

Subtracting the strict upper bound for K in (7), the resulting support gap is greater than

    B[.26+s(1-z-.26c)]
      +T[c(1-z)+.26s^2-1].                       (11)

The coefficient of B exceeds .26 because z<.11 and c<=1. The coefficient of T is greater than

    (.97)(.89)-1=-.1367>-.137.

Consequently (11) is greater than

    .26B-.137T>=.123B>0.

This last source cannot separate either. These estimates cover T=0 as well.

### 2.2. The only remaining source gives a strict small right angle

The sole remaining direction in (8) is u_E. Its full lower R support has both coefficients positive:

    lower_R(u_E)=k L+h K.

Using (7),

    lower_R(u_E)
      <k(B-.4T)+h(T-.26B)
       =c-.66cBT-s(.26B^2-.4T^2).                (12)

Since upper_E(u_E)=A>1-z, separation would require

    .66cBT+s(.26B^2-.4T^2)
       <c-1+z=z(1-s)<.11.                        (13)

Suppose T/B>=1/2. As T<=B, the exact factorization

    5BT-2=(2T-B)(2B-T)>=0

gives BT>=2/5. Also T^2<=1/2, so

    .26B^2-.4T^2=.26-.66T^2>=-.07.

The left side of (13) is therefore strictly greater than

    (.66)(.97)(2/5)-(.07)(.21)
       =.24138>.11.                              (14)

This is a contradiction. Hence

    T/B<1/2.                                     (15)

Both canonical right endpoints were retained until this conclusion. No numerical angle samples or unproved support source have been used.

## 3. Assume the northeast half-angle is at most one third

Put theta0=2 arctan(1/3), so

    cos(theta0)=4/5, sin(theta0)=3/5.

Suppose tan(theta/2)<=1/3. Together with (5), the continuous northeast interval is

    2 arctan(1/4)<theta<=theta0,
    4/5<=b<15/17, 8/17<t<=3/5,
    8/15<t/b<=3/4.                               (16)

Orient a separating normal from N toward R. Their strict points M_N=(.35,.35) and (1,.35), the latter in the actual bar (3), force its horizontal component to be positive. Its possible actual sources are

    u_N, -v_N, u_R, v_R.

Both upward sources are excluded using the strict N point F=(.4,1) and the strict bottom endpoint (1,-.26) of R. For u_N their displacement has projection

    .6b-1.26t
      <[.6-(1.26)(8/15)]b=-.072b<0.

For v_R the projection is

    .6T-1.26B<=-.66B<0.

Therefore the complete surviving sources for these actual N,R are

    u_R or -v_N.                                 (17)

This is the step that permits the short bar (3). The actual F7 abscissa .4 supplies the displayed negative projection even when G8 is absent from R.

## 4. The right square's downward normal cannot separate

Set

    alpha=bB-tT>0, beta=tB+bT>0.

These are the positive cosine and sine of the sum of the northeast angle and the magnitude of the right angle. Their positivity also follows directly from (15),(16).

For n=u_R, the full upper N support is

    upper_N(u_R)=alpha A_N-beta V_N.

The actual lower-U and upper-H faces in (5) give

    A_N>=a+.4t, V_N<=b-a.

Hence a>1 yields

    upper_N(u_R)
      >=alpha(a+.4t)-beta(b-a)
       >B C+T D,

    C=b+t-.6bt,
    D=b-t-1+.6t^2.                               (18)

We bound these scalar coefficients on the entire interval (16). Their derivatives with respect to theta satisfy

    C'=(b-t)[1-.6(b+t)]>0,
    D'=-t-b+1.2bt<0.

For the first sign use b>t and .6sqrt(2)<1. For the second use b+t>=1 and bt<=1/2. At the lower endpoint theta=2 arctan(1/4),

    C-1=30/289>1/10.

At the upper endpoint theta=theta0,

    D+.4=-23/125.

Thus throughout the whole interval,

    C-1>1/10, D+.4>=-23/125.                     (19)

Subtracting L<B-.4T from (18), and applying (15),(19), gives

    upper_N(u_R)-L
       >B/10-(23/125)T
        >B/125>0.                                (20)

The actual squares therefore cannot separate along u_R.

## 5. The northeast square's downward normal cannot separate

For the remaining direction n=-v_N=(t,-b), the full upper N support is

    upper_N(-v_N)=-V_N>=a-b>1-b.                  (21)

Let (x_R,y_R) be the actual center of R. Its right wall and center sign in (4) give

    x_R<=2-a(B+T)/2, y_R>=0.

The components of n in R's frame are beta and -alpha, both with the signs already established. Its full lower support therefore satisfies

    lower_R(-v_N)
       =t x_R-b y_R-a(alpha+beta)/2
       <=2t-a[(2t+b)B+bT]/2.                     (22)

In particular the nonnegative actual center ordinate is used with its negative coefficient; it has not been dropped from an upward support estimate.

Put w=T/(1+B). By (15),

    0<=w<1/4.

Using 1-B=T w, the exact difference of the bracket in (22) from 2t+b is

    (2t+b)B+bT-(2t+b)
       =T[b-(2t+b)w]>=0.                         (23)

Indeed, by (16) the expression in square brackets is greater than

    b-(2t+b)/4=3b/4-t/2>=3b/8>0.

If T=0 the product in (23) is zero; all subsequent support comparisons remain strict because a>1. Equations (22),(23) consequently give

    lower_R(-v_N)<t-b/2.                          (24)

The function sin(theta)+(1/2)cos(theta) is strictly increasing on the interval (16), since its derivative is b-t/2>0. Its value at theta0 is exactly1. Therefore

    t+b/2<=1,
    t-b/2<=1-b.                                  (25)

Equations (21),(24),(25) contradict separation along -v_N. This removes the last source in (17).

## 6. Conclusion and precise scope

Every actual N--R separating source is impossible under tan(theta/2)<=1/3. Therefore a nonpositive canonical right angle forces

    tan(theta/2)>1/3.

The independent theorem `C1092-MMMP-NORTHEAST-UPPER-THIRD.md` gives tan(theta/2)<1/3 under the same two original branch premises, Q10 owning F8 and Q5 excluding G8. Combining the two excludes every nonpositive canonical right angle in that branch.

The proof does not require G8 in the right square, the longer double-right bar, a southeast center, or any assertion about a positive right angle. Its only use of `C1092-MMMP-SOUTHEAST-FLOOR-RIGHT-SIGN.md` is the actual-bar Lemma1 and the elementary missing-center cap from its entrance. Thus a separate positive-right argument remains necessary to exclude the whole original branch.

Every support formula above is for one of the three named actual squares. The two right-face bounds in (7) come from strict points of their single actual bar, and (22) uses that same square's genuine wall and center. Exact positive margins, including (14) and (20), exclude all weak exterior and separating-face equalities.
