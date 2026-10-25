# C1092 MMMP: the remaining partial-right outer-arm branch is impossible

Every terminating decimal is an exact rational. All squares are the original actual open squares of common side a>1, with disjoint interiors. Owned points are strict. Missing-point faces, actual wall and center conditions, and separating supports may be equality. Every orientation is retained over its full continuous canonical interval.

**Theorem 1.** In the original MMMP family, F8 cannot belong strictly to Q10 while G8 belongs strictly to Q5.

The proof uses the new southeast floor for this exact ownership branch and treats both signs of the actual right square. Its southeast sine bound is derived under strict G8 ownership, without importing the bound from the contrary G8-exclusion branch.

## 1. The simultaneous actual entrance

Translate by (-2,-2), and write E=Q5, N=Q6, R=Q10. By `C1092-MMMP-PARTIAL-RIGHT-SOUTHEAST-FLOOR.md`, E has positive frame

    u_E=(c,s), v_E=(-s,c), c>=s>0, c^2+s^2=1,
    s/c<1/3, s<1/sqrt(10)<.32, c>3/sqrt(10)>.94.

Let A,H be its upper u_E,v_E faces. The same actual-square theorem gives

    H<=0, H>-.26s,
    sA+cH>a(c+s)-1,
    A>a-z, z=s/(1+c).                            (1)

Its strict points include

    D=(.26,0), G=(1,-.4).                        (2)

The foreign point G9 belongs to actual R universally, and the premise puts F8 in that same square. Hence its entire strict bar is

    {1}x[-.26,.4] in R.                          (3)

Its genuine original right wall and closed MMMP center sign are

    closure(R) subset {x<=2}, center_y(R)>=0.     (4)

The northeast cap theorem and the new branch-specific theorem `C1092-MMMP-PARTIAL-RIGHT-NORTHEAST-BOUND.md` give

    u_N=(b,t), v_N=(-t,b), b>=t>0, b^2+t^2=1,
    U_N>=.4t, V_N>=.4b-t,
    A_N=U_N+a<=b+t, H_N=V_N+a<=b,
    2 arctan(1/4)<theta<theta0=2 arctan(1/3).     (5)

Thus 4/5<b<15/17 and 8/15<t/b<3/4. In the scalar estimates we may enlarge this to theta<=theta0. Actual N strictly owns

    M_N=(.35,.35), F=(.4,1), P=(.47,.12).         (6)

These are its marker, its F7, and the point from Theorem1 of `C1092-MMMP-NORTHEAST-LOWER-TIP.md`.

Two convenient consequences of the fresh angle bound are

    0<z<.32/1.94=16/97<1/6,
    eta:=z(1-s)<(.32)(.68)/1.94
               =272/2425<.113.                  (7)

For the second comparison use that s(1-s) increases on 0<=s<=.32, and 1+c>1.94.

There is a particularly short complete E--R normal cone in this ownership branch. The strict pair D in E and (1,0) in R forces n_x>0 for a separating normal from E toward R. The strict pair G=(1,-.4) in E and F8=(1,-.26) in R forces n_y>0. Thus every such normal lies in the strict upper-right quadrant. This observation uses actual ownership of G8 and F8 in their different squares.

## 2. A nonpositive right angle is impossible

Suppose R has canonical frame

    u_R=(B,-T), v_R=(T,B), B>=T>=0,
    B^2+T^2=1.

Let L,K be its lower faces. The actual bar (3) gives

    L<B-.4T, K<T-.26B.                          (8)

By the strict quadrant just proved, the only possible E--R sources are u_E and v_R. At T=0 the latter is already absent from that strict cone; retaining it below does no harm.

### 2.1. The actual southeast square forces T/B<1/2

Put

    k=cB-sT>0, h=sB+cT>0.

For v_R, the full upper E support is hA+kH. Equations (1),(8) show that its excess over the right lower support is strictly greater than

    B[.26+s(1-z-.26c)]
       +T[c(1-z)+.26s^2-1].                     (9)

The coefficient of B exceeds .26. By (7) and c>.94, the coefficient of T exceeds

    (.94)(5/6)-1=-13/60.

Thus (9) is greater than

    .26B-(13/60)T>=(13/300)B>0.

This eliminates v_R.

The remaining u_E source has full lower R support kL+hK. By (8),

    lower_R(u_E)
       <k(B-.4T)+h(T-.26B)
        =c-.66cBT-s(.26B^2-.4T^2).

Since A>a-z>1-z, separation would require

    .66cBT+s(.26B^2-.4T^2)<eta<.113.             (10)

If T/B>=1/2, then

    5BT-2=(2T-B)(2B-T)>=0,
    .26B^2-.4T^2=.26-.66T^2>=-.07.

Consequently the left side of (10) would exceed

    (.66)(.94)(2/5)-(.07)(.32)=.22576>.113.

Therefore every possible actual E--R separator forces

    T/B<1/2.                                    (11)

### 2.2. The two remaining actual northeast sources both fail

Orient a separating normal from N toward R. The strict pair M_N and (1,.35) in (3) forces n_x>0, so its possible sources are u_N,-v_N,u_R,v_R. The displacement from strict F=(.4,1) in N to strict F8=(1,-.26) in R has projections

    .6b-1.26t<-.072b<0 on u_N,
    .6T-1.26B<0 on v_R.

Thus only u_R and -v_N remain.

For u_R, put alpha=bB-tT>0 and beta=tB+bT>0. The actual caps in (5) yield

    upper_N(u_R)=alpha A_N-beta V_N
       >=alpha(a+.4t)-beta(b-a)
        >B C+T D,

    C=b+t-.6bt, D=b-t-1+.6t^2.                   (12)

On the complete interval 2 arctan(1/4)<theta<=theta0,

    C'=(b-t)[1-.6(b+t)]>0,
    D'=-t-b+1.2bt<0.

At its lower endpoint C-1=30/289>1/10; at theta0 one has D+.4=-23/125. Using (8),(11), therefore,

    upper_N(u_R)-L
       >B/10-(23/125)T>B/125>0.                 (13)

This source is impossible.

For n=-v_N=(t,-b), write (X_R,Y_R) for R's actual center. Its wall and center sign (4) give

    X_R<=2-a(B+T)/2, Y_R>=0.

The components of n in R's frame are beta,-alpha. Hence

    lower_R(n)
       =tX_R-bY_R-a(alpha+beta)/2
       <=2t-a[(2t+b)B+bT]/2.                    (14)

Set w=T/(1+B). By (11), 0<=w<1/4. The exact bracket difference is

    (2t+b)B+bT-(2t+b)
       =T[b-(2t+b)w]>=0,                        (15)

since the inner bracket exceeds 3b/4-t/2>=3b/8>0. The product is zero when T=0, but a>1 still makes the next comparison strict. Thus (14) gives

    lower_R(n)<t-b/2<=1-b<a-b<=upper_N(n).       (16)

The middle comparison follows from t+b/2<=1 for theta<=theta0: that function increases with theta and has endpoint value1. This eliminates the last actual source. No nonpositive canonical right angle can occur.

## 3. A nonnegative right angle also forces a small right slope

Now give R the frame

    u_R=(d,r), v_R=(-r,d), d>=r>=0,
    d^2+r^2=1.

Write L,K for its lower faces and J=K+a. The strict endpoint faces from (3) are

    L<d-.26r, J>-r+.4d.                         (17)

The upper-right E--R normal cone from Section1 now leaves precisely u_E and u_R. Let q,rho be the positive E angle and nonnegative R angle.

If rho<=q, then r/d<=s/c<1/3. Otherwise put

    alpha=cd+sr>0, delta=cr-sd>=0.

For the right-supplied direction u_R, retain the strict coupled floor. With A0=[a(c+s)-1]/s, (1) gives A>A0, and

    upper_E(u_R)=alpha A+delta H
       =(d/c)A+(delta/c)(sA+cH)
        >alpha A0>alpha(1-z).                  (18)

Here d+delta s=c alpha and A0=a-z+(a-1)c/s. At delta=0 the strict A>A0 inequality retains the strictness in (18).

Combining (17),(18), separation would require

    -d P+r Q<0,
    P=z(c+s), Q=.26+s(1-z)>0.                   (19)

The exact identity

    (1+c)(5Q-12P)
       =1.3(1+c)+s(5-7c)-17s^2                 (20)

has a strictly positive right side, because

    1.3(1+c)+s(5-7c)-17s^2
       >2.522-.64-1.7408=.1412>0.               (21)

We used c>.94, c<=1 and s<.32. Thus P/Q<5/12, so (19) requires r/d<5/12. Including rho<=q, this source always forces

    r/d<5/12 if u_R separates E from R.          (22)

For the other source u_E in the angle order rho>=q, its full lower R support is alpha L-delta J. By (17),

    lower_R(u_E)
       <alpha(d-.26r)-delta(-r+.4d)
        =c-.66cdr+s(.4d^2-.26r^2).

Separation would therefore require

    .66cdr-s(.4d^2-.26r^2)<eta<.113.             (23)

If r/d>=1/2, the factorization 5dr-2=(2r-d)(2d-r)>=0 gives dr>=2/5, and .4d^2-.26r^2<=.4. The left side of (23) would exceed

    (.66)(.94)(2/5)-(.4)(.32)=.12016>.113.

Thus this source forces r/d<1/2 as well. The alternative rho<=q already has r/d<1/3, so all actual E--R sources and both full angle orders give

    r/d<1/2.                                    (24)

## 4. The northeast square forces the conflicting slope r/d>5/12

The strict N--R pair M_N,(1,.35) again gives a positive horizontal component. Its possible sources are u_N,-v_N,u_R,-v_R. The u_N source is excluded by the same F-to-F8 displacement used in Section2.

By (5),(24), rho<theta. Put k=bd+tr>0 and j=br-td<0. The full actual N caps give

    upper_N(u_R)
       =k A_N+j V_N
       >=k(a+.4t)+j(b-a)
        >d[b+t-.6bt]+r[1+t-b-.6t^2]>d.           (25)

The first bracket exceeds1, since b+t-1=2bt/(1+b+t)>.6bt; the second is (1-b)+t(1-.6t)>0. But strict (1,0) in R gives L<d. This removes u_R.

For -v_R=(r,-d), use the strict N point P=(.47,.12) and actual G9=(1,.4). Their displacement has projection

    .53r-.28d<-.015d<0                         (26)

by (24), so it cannot align with an N--R separating support. Thus the only remaining source is -v_N.

Set h=td-br>0 and k=bd+tr>0. In this remaining direction the actual N and R supports satisfy

    upper_N(-v_N)=-V_N>=a-b,
    lower_R(-v_N)
       =tX_R-bY_R-a(h+k)/2
       <=2t-a[(2t+b)d+(2t-b)r]/2.               (27)

The second line uses the same actual R wall and its nonnegative center ordinate, with the center-y coefficient negative. Separation and a>1 would therefore require

    F(theta,rho)
      =1-b-2t+[(2t+b)d+(2t-b)r]/2<0.            (28)

The coefficient of a is positive; in particular 2t-b>0 by (5).

For fixed rho, put P0=1-d/2+r/2 and Q0=2-d-r. These are positive and F=1-bP0-tQ0. By (24), r<1/sqrt(5)<.45, so

    Q0-(3/4)P0=(10-5d-11r)/8>1/160>0.

It follows that partial_theta F=tP0-bQ0<0 over the whole interval (5). At theta0 one has

    F(theta0,rho)=d+.2r-1.

Thus (28) implies d+.2r-1<0. The case r=0 is impossible immediately. Otherwise, with w=r/(1+d), the identity

    d+.2r-1=r(.2-w)

forces w>1/5 and therefore

    r/d=2w/(1-w^2)>5/12.                         (29)

This contradicts (22), excluding the right-supplied E--R source.

## 5. The last southeast source contradicts the same slope

Only u_E can remain for E--R. By (29), rho>arctan(5/12)>q, since s/c<1/3. Hence its exact necessary inequality (23) applies with the stated upper right face.

For fixed c,s, define the scalar loss

    L0(rho)=.66cdr-s(.4d^2-.26r^2).

Its derivative on arctan(5/12)<=rho<=pi/4 is

    L0'=.66c(d^2-r^2)+1.32sdr>0.                (30)

At the lower endpoint (d,r)=(12/13,5/13),

    L0=(396c-511s)/1690.

Thus (29) and the fresh bounds c>.94,s<.32 give

    L0>(396(.94)-511(.32))/1690
       =2609/21125>.12>.113.                    (31)

This contradicts (23). Both E--R sources have now failed under the necessary consequence of the sole N--R source. Consequently the nonnegative canonical right sign is impossible as well.

Together with Section2, this excludes every canonical orientation of the actual R, including axial and diagonal representatives. Theorem1 follows.

## 6. The resulting exact original right component

**Theorem 2.** Throughout the original MMMP family,

    Q10 excludes F8,
    Q10=524800={F9,G9}.

Indeed, Theorem2 of `C1092-MMMP-POSITIVE-RIGHT-ENDING.md` proves that F8 in actual Q10 forces G8 strictly in actual Q5. Theorem1 above excludes precisely that remaining ownership branch. Hence F8 cannot belong to Q10 at all.

For the exact label, require the universal F9,G9 in the literal original Q10 component row and remove every component meeting the actual foreign F6,F7,G6. As displayed and checked in the preceding positive-right ending, this leaves exactly524800,525056,787200. The latter two contain F8 and are now excluded. Thus only524800 remains.

The theorem has not assigned any southeast angle or inward point to this last F8-absent branch. Every fresh floor and small-angle estimate in the present proof was used only while the actual F8-in-Q10 premise held. All supports, bars, strict points, real wall and center conditions used in the contradiction belong to the same explicitly named original squares.
