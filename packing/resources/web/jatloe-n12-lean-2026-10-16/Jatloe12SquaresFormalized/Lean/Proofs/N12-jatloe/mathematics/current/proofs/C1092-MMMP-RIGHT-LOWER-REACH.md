# C1092 MMMP: the actual northeast square forces a downward right-wall reach

Every terminating decimal denotes an exact rational. All squares are open, their side lengths are the same number a>1, and their interiors are disjoint. Owned points are strict. Excluded points, real container walls and separating supports may be equality. No upper bound on a or boundary-center hypothesis is used in the local theorem.

## 1. The complete two-square statement

**Theorem 1.** Let N and R be two actual disjoint open squares of common side a>1. Suppose N has positive canonical frame

    u_N=(b,t), v_N=(-t,b),
    b>=t>0, b^2+t^2=1, t/(1+b)>1/4.

Write U_N,V_N for its lower faces and A_N=U_N+a,H_N=V_N+a for its upper faces. Assume the actual bounds

    U_N>=.4t, V_N>=.4b-t,
    A_N<=b+t, H_N<=b,                              (1)

and strict ownership of

    M=(.35,.35), F=(.4,1), Y=(.5,1), K_*= (.47,.12).

Suppose R has its genuine right wall x<=2 and strictly owns

    S=(1.086,0), O_R=(1,0), T=(1,.4).             (2)

Then R strictly owns (1,-.16). Consequently its whole segment

    {1} x [-.16,.4]                              (3)

is strict in this same actual R.

We prove the stronger pointwise statement that every P=(1,-z), with 0<z<=.16, is strict in R. The proof retains all four possible actual separating axes for each sign of R, and keeps the wall of that same R in every support comparison.

### The literal MMMP application

Translate the original coordinates by (-2,-2). Take N=Q6 and R=Q10. The complete actual input ledger is

| Local premise | Original source |
|---|---|
| N strict M | Q6's original marker (2.35,2.35) |
| N strict F | F7=(2.4,3), in Q6 by the MMMP core |
| N strict Y | (2.5,3), proved in C1092-MMMP-RIGHT-ORIGIN.md |
| N strict K_* | (2.47,2.12), proved in C1092-MMMP-NORTHEAST-LOWER-TIP.md |
| N frame, angle and (1) | C1092-MMMP-NORTHEAST-TOP-CAP.md |
| R strict S | Q10's original marker (3.086,2) |
| R strict O_R | (3,2), proved in C1092-MMMP-RIGHT-ORIGIN.md |
| R strict T | G9=(3,2.4), proved in C1092-MMMP-RIGHT-FAR-AUXILIARY.md |
| R real wall x<=2 | Original container wall x<=4 |

For clarity, the top-cap chapter uses the quarter-turned chart (X,Y)=(2-y,x-2) and lower faces p,q. On returning to the present translated chart, U_N=q and V_N=-(p+a), so its four bounds are exactly (1), with A_N=q+a and H_N=-p. No new angle sign is inferred in making this change of face names.

Thus Theorem 1 proves, throughout the whole original MMMP family,

    (3,1.84) strictly in Q10,
    {3} x [1.84,2.4] strictly in Q10.            (4)

This application does not depend on the later exact component524800, on any southeast auxiliary ownership, or on an assumed owner for an omitted auxiliary.

## 2. Common actual separating directions and northeast supports

Suppose for a contradiction that P=(1,-z), 0<z<=.16, is excluded from R. Choose R's canonical magnitude rho in [0,pi/4], and put

    d=cos(rho), r=sin(rho), d>=r>=0.

Write L,K for its lower faces, and J=K+a. We consider both signs of R below.

The strict segment from O_R to T contains (1,.35). Together with the strict N marker M, it forces every separating normal from N toward R to have positive horizontal component. Indeed the displacement between these two strict points is (.65,0), and strict ownership makes its projection along an oriented separating normal positive. The separating-axis theorem for two rectangles therefore leaves exactly the two right-facing axes of each actual square. A vertical endpoint direction is already excluded by this strict cone; retaining it in the calculations causes no problem.

For both signs of R, the N source u_N is impossible: the strict pair Y in N and O_R in R gives

    u_N(O_R-Y)=.5b-t<0,                          (5)

because the half-angle premise implies t/b>8/15>1/2. We repeatedly use the other N source n=-v_N=(t,-b), whose upper support is

    upper_N(n)=-V_N>=a-b.                        (6)

Two further bounds from (1) will be useful. Put

    C=b+t-.6bt, D=b-t-1+.6t^2.

Throughout the complete N angle interval,

    C>1.1, D>=-.7.                              (7)

To verify (7), differentiate with respect to the positive N angle theta. One has

    C'=(b-t)[1-.6(b+t)]>=0,
    D'=-(b+t)+1.2bt<0.

The first bracket is positive since b+t<=sqrt(2)<5/3. At theta=2 arctan(1/4), C-1=30/289>1/10. At theta=pi/4, D=-.7. The strict lower N-angle bound gives (7), including the diagonal endpoint.

### A positive right square cannot use its upward axis

For a nonnegative R frame w=(d,r),v=(-r,d), put

    k=bd+tr>0, delta=br-td.

If delta>=0, the exact support is k A_N+delta H_N. The bounds (1), together with a>1, give A_N>b and H_N>-t. Hence

    upper_N(w)>kb-delta t=d.

If delta<0, its exact support is k A_N+delta V_N. Since A_N>=a+.4t and V_N<=b-a,

    upper_N(w)>=a(k-delta)+.4tk+b delta
                >d[b+t-.6bt]+r[1+t-b-.6t^2]>d.   (8)

The last coefficient of r is positive because it equals (1-b)+t(1-.6t). The strict R origin gives lower_R(w)=L<d. Thus w cannot separate N from R in either order of the two angles.

### A negative right square cannot use its upward axis

For a negative R frame w=(d,-r),v=(r,d), its upward right-facing source is v. The strict pair F in N and O_R in R gives

    v(O_R-F)=.6r-d<0.                            (9)

Thus this source is impossible as well.

## 3. Nonnegative R: the lower-v exit of P is impossible

Use the frame w=(d,r),v=(-r,d). Since O_R is strict, P is strictly below both upper faces. If P leaves through the lower v face, then

    K>=-r-zd, J>=a-r-zd.                        (10)

The two upward sources are excluded in Section 2. For R's own downward source -v=(r,-d), the strict N point K_* gives

    upper_N(-v)+J
      >.47r-.12d+a-r-zd
      >1-.53r-(.12+z)d
      >=1-sqrt(.53^2+.28^2)>0.                  (11)

This contradicts upper_N(-v)<=lower_R(-v)=-J.

For the remaining N source n=(t,-b), put

    h=td-br, k=bd+tr>0.

Its lower R support is

    lower_R(n)=hL-kJ+a min(h,0).

The strict origin gives L<d<L+a, so hL+a min(h,0)<=hd for either sign of h. Using (10) and hd+kr=t,

    lower_R(n)<=t-ak+zdk.

Together with (6), the support gap is strictly greater than

    1-b-t+k(1-zd)
      >=1-sqrt(2)+.84/sqrt(2)
       =1-(29/25)/sqrt(2)>6/35>0.               (12)

Here k=cos(theta-rho)>=1/sqrt(2), d<=1, and sqrt(2)>7/5. Thus this exit is impossible, including r=0 and h=0.

## 4. Nonnegative R: the lower-u exit and its own downward source

The only other possible exit of P in this frame is

    L>=d-zr.                                    (13)

Since the origin gives L<d, this forces r>0. The real right wall is the exact inequality

    dL-rJ+a(d+r)<=2.                             (14)

Suppose R's own downward normal -v=(r,-d) separated N from R. The strict point K_* would then give

    J<-.47r+.12d.

Combine this with (13),(14), and a>1. A necessary condition would be

    d+r-1-.53r^2-(z+.12)dr<0.                   (15)

But d+r-1=2dr/(1+d+r), and sqrt(2)<10/7. Hence the left side of (15) is

    dr[2/(1+d+r)-.53(r/d)-(z+.12)]
      >dr[14/17-.81]
       =(23/1700)dr>0.                         (16)

This is a contradiction. No center bound has been substituted for the real wall in this argument.

## 5. Nonnegative R: the N downward source has two continuous scalar ranges

It remains, under (13), to exclude n=(t,-b). Keep h=td-br and k=bd+tr. Its exact lower R support and (6) imply

    kJ<=hL+a min(h,0)-a+b.

Substitution into the real wall (14), using dk-rh=b, gives

    bL<=2k+rb-a[k(d+r)+r-r min(h,0)].            (17)

The coefficient of a in brackets is strictly positive. Combine (13),(17) and a>1. The resulting necessary scalar condition is

    F=b(d-zr)+k(d+r)+r(1-b)-2k-r min(h,0)<0.    (18)

We prove the opposite over the entire canonical ranges. Set

    w=r/(1+d), 0<w<=sqrt(2)-1,
    A_0=1+z-d(1-w)>0,
    B_0=2-d-r>0.

The identity d+r-1=r(1-w) gives the exact rearrangement

    F=r[1-A_0 b-B_0 t]-r min(h,0)
       >=r[1-A_0 b-B_0 t].                      (19)

There are just two closed scalar ranges.

**First range: 0<w<=1/4.** The half-angle formulas give

    B_0-A_0
      =[1-z-3w+(1-z)w^2+w^3]/(1+w^2)>0,

because 1-z-3w>=.09. Consequently A_0 cos(theta)+B_0 sin(theta) is increasing throughout 0<=theta<=pi/4, since its derivative is B_0 cos(theta)-A_0 sin(theta)>0. Moreover

    A_0+B_0=3+z-2d-w<=1+z,

because

    2d+w-2=w(1-4w+w^2)/(1+w^2)>=0.

Thus

    A_0b+B_0t<=(1+z)/sqrt(2)
                  <=(29/25)/sqrt(2)<29/35<1.    (20)

**Second range: 1/4<=w<=sqrt(2)-1.** The quantity d+r increases with rho through its canonical interval, so

    B_0<=2-(15/17+8/17)=11/17.

The product d(1-w) decreases as w increases and is at least sqrt(2)-1. Hence, using sqrt(2)>141/100,

    A_0<=2+z-sqrt(2)<3/4.

Cauchy--Schwarz therefore gives

    A_0b+B_0t<=sqrt(A_0^2+B_0^2)
       <sqrt(9/16+121/289)
        =sqrt(4537/4624)<1.                     (21)

Equations (19)--(21) prove F>0. This contradicts (18) for both orders of theta and rho, since the extra term -r min(h,0) in (19) is nonnegative. All possible exits of P for nonnegative R have now been excluded.

## 6. Negative R: an upper-u exit contradicts the same actual N

Use the negative frame w=(d,-r),v=(r,d). The strict point T supplies P's lower-u band, since

    w(P)-w(T)=(z+.4)r>=0.

The strict origin supplies its upper-v band, since v(P)=r-zd<r. Hence the only possible exits are upper u or lower v.

In the upper-u alternative,

    L+a<=d+zr.

The strict actual marker S then gives zr>.086d, so r/d>.086/.16=43/80>1/2. In particular

    w_R=r/(1+d)>1/5>z.

Indeed a half-angle at most1/5 has tangent at most5/12<1/2. Since a>1,

    L<d+zr-1=r(z-w_R)<0.                        (22)

The two upward sources fail by (5),(9). For R's downward source w, the strict N marker gives upper_N(w)>.35(d-r)>=0>L.

For the remaining N source n=(t,-b), write

    h=td+br>0, k=bd-tr>=0.

The strict R origin gives J>r>0. Therefore

    lower_R(n)=hL-kJ<0,
    upper_N(n)>=a-b>0,

even if k=0. This eliminates the upper-u exit.

## 7. Negative R: both downward sources fail for a lower-v exit

The remaining possible exit is

    K>=r-zd, J>=a+r-zd.                         (23)

The real right wall is now

    d(L+a)+rJ<=2.                               (24)

### 7.1. R's own downward normal

Set k=bd-tr>=0 and h=td+br>0. From (1), the exact N support on w=(d,-r) satisfies

    upper_N(w)=kA_N-hV_N
       >=a(k+h)+.4tk-bh>dC+rD,                  (25)

where C,D are the quantities in (7). If w separated, then L>dC+rD. Combining this with (23),(24), and a>1 would force

    d+r-1+d^2(C-1)+dr(D-z)<0.                  (26)

On the other hand, d+r-1=2dr/(1+d+r)>=.8dr because d+r<3/2. By (7) and z<=.16 the left side of (26) is strictly greater than

    .1d^2-.06dr>=.04d^2>0.                     (27)

Thus w cannot separate. The argument also covers r=0 directly.

### 7.2. N's own downward normal

Keep h=td+br>0 and k=bd-tr>=0. Its lower R support is hL-kJ. Eliminating L by the real wall (24), and then using (23), gives

    lower_R(n)
       <=2h/d-ah-(b/d)J
       <=2t+b(r/d)-a(h+b/d)+bz.                 (28)

Here hr+kd=b. Subtracting (28) from (6), with a>1, proves that the support gap is strictly greater than

    G=1-(2-d)t+b[(1-d)(1-r)/d-z].               (29)

For fixed d,r,z, this expression decreases strictly with the N angle theta: writing X=2-d>=1 and Y=z-(1-d)(1-r)/d<=.16, its derivative is -Xb+Yt<0. Thus

    G>=1-[2-d+z-(1-d)(1-r)/d]/sqrt(2).

Since r<=d,

    (1-d)(1-r)/d>=(1-d)^2/d.

The function 4-2d-1/d is decreasing on 1/sqrt(2)<=d<=1, because its derivative is -2+1/d^2<=0. Its maximum is4-2sqrt(2). Consequently

    2-d-(1-d)(1-r)/d<=4-2sqrt(2),

and hence

    G>=3-(4+z)/sqrt(2)
       >=3-(104/25)/sqrt(2)>1/35>0.             (30)

The last strict bound uses sqrt(2)>7/5. This contradicts the remaining separating source.

All exits of P have been excluded for both canonical signs of R. The point P is therefore strict in R. Taking z=.16 and joining it to the strict T proves (3), and the original-source ledger proves (4). This completes Theorem1.

## 8. The two reviewed negative missing-origin profiles are now impossible

**Corollary 2.** In original MMMP, if actual Q5 has a nonpositive canonical angle and owns either the inward pair F4,G6 or the ordinary pair F8,G8, then actual Q9 strictly owns its bottom origin (2,1).

For the inward pair, suppose that origin were missing. Theorems1--2 of `C1092-MMMP-NEGATIVE-INWARD-MISSING-ORIGIN.md` supply a strictly negative frame and an actual strict point

    (3,2-z) in Q5, 0<z<.154.

For the ordinary pair, the complete missing-origin profile in `C1092-MMMP-ORDINARY-SOUTHEAST-MISSING-ORIGIN.md`, followed by Section1 of `C1092-MMMP-NEGATIVE-ORDINARY-HALFANGLE-POINT.md`, gives the same actual point with 0<z<.13. The profile itself excludes all nonnegative-angle alternatives that could arise under missing origin, so axial cases cause no gap.

In both cases this strict point lies in the whole actual Q10 segment (4), since .154<.16. It would be strictly owned by two distinct original squares Q5 and Q10, contradicting their disjoint interiors. Thus the bottom origin is strict in Q9.

The argument requires no southeast/right relative-center assumption and no inferred face bound from a strictly owned high endpoint. Every upper or lower support used above is either a displayed actual face bound, a real wall equation, or the appropriate exact support of one of the same two actual squares.
