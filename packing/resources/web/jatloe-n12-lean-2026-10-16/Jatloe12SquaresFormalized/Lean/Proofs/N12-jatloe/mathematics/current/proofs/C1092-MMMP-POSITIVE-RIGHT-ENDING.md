# C1092 MMMP: the last positive-right separator is impossible

All terminating decimals are exact rationals. Every square is the actual original open square of common side a>1. All stated owned points are strict. Exterior points, the actual container wall and center condition, and separating supports may be equality. The argument covers whole continuous angle intervals.

**Theorem 1.** In the original MMMP family, the following three conditions cannot hold together:

    Q10 strictly owns F8=(3,1.74),
    Q5 excludes G8=(3,1.6),
    Q10 has a nonnegative canonical angle.

The proof uses the genuine short right bar from F8 to G9. It does not require G8 to belong to Q10.

## 1. The literal simultaneous three-square entrance

Translate by (-2,-2) and write

    E=Q5, N=Q6, R=Q10.

The positive southeast entrance and floor are established in
`C1092-MMMP-RIGHT-NEAR-BOTTOM-ORIGIN.md` and Lemma1 of
`C1092-MMMP-SOUTHEAST-FLOOR-RIGHT-SIGN.md`. With positive frame

    u_E=(c,s), v_E=(-s,c), c>=s>0,
    c^2+s^2=1, s<.21, c>.97,

write A,H for its upper faces and put z=s/(1+c). Their conclusions are

    H<=0,
    sA+cH>a(c+s)-1,
    A>a-z,
    0<z<21/197<.11.                              (1)

These are simultaneous bounds on the actual E. The strict whole bottom bar used to prove (1) is in the actual Q9; no independently placed replacement of that owner is used.

Write the supposed nonnegative right frame as

    u_R=(d,r), v_R=(-r,d), d>=r>=0,
    d^2+r^2=1,

and write L,K for its lower faces. The actual strict right bar, its genuine wall, and its original closed MMMP center sign are

    {1}x[-.26,.4] strictly in R,
    closure(R) subset {x<=2},
    center_y(R)>=0.                              (2)

The actual bar in (2) comes from the stipulated F8 and the universal G9 in Q10. It supplies, in particular,

    L<d-.26r, K+a>-r+.4d.                        (3)

The positive-right reduction in
`C1092-MMMP-POSITIVE-RIGHT-ANGLE-REDUCTION.md` proves

    r/d<1/2,                                    (4)

and the following complete source restrictions for these same owners:

    E to R: only u_E or u_R can separate;
    N to R: only -v_N can separate.              (5)

The southeast restriction uses only the valid downward estimates of the floor chapter. The northeast restriction uses its full actual face table, its strict F7 and the already proved strict point (.47,.12), together with the right bar in (2). Thus (5) does not rely on any upper estimate for an upward normal from the condition center_y(R)>=0.

Finally the original positive northeast frame is

    u_N=(b,t), v_N=(-t,b), b>=t>0,
    b^2+t^2=1.

Its actual top-cap table gives H_N=V_N+a<=b. Combining its strict lower half-angle bound with the theorem
`C1092-MMMP-NORTHEAST-UPPER-THIRD.md` gives, on writing theta for its angle,

    2 arctan(1/4)<theta<theta0=2 arctan(1/3),
    4/5<b<15/17, 8/17<t<3/5,
    8/15<t/b<3/4.                               (6)

For the scalar estimates below we harmlessly allow equality at theta0. This only enlarges the domain and preserves the final strict contradiction.

## 2. The remaining northeast source would force a large right angle

Let rho be the nonnegative right angle. By (4),(6),

    rho<arctan(1/2)<theta.

Set

    k=bd+tr=cos(theta-rho)>0,
    h=td-br=sin(theta-rho)>0.

In the remaining direction n=-v_N=(t,-b), the full upper N support satisfies

    upper_N(n)=-V_N>=a-b.                       (7)

Let (X_R,Y_R) be the actual center of R. The genuine conditions (2) give

    X_R<=2-a(d+r)/2, Y_R>=0.

The components of n in the right frame are h,-k. Therefore its full lower R support is

    lower_R(n)=t X_R-b Y_R-a(h+k)/2
       <=2t-a[(2t+b)d+(2t-b)r]/2.               (8)

The sign of the center-y coefficient in (8) is negative. Thus both uses of the one-sided center bounds are in their valid directions.

If n separated N from R, (7),(8) and a>1 would imply

    F(theta,rho)
       =1-b-2t+[(2t+b)d+(2t-b)r]/2<0.            (9)

The dropped coefficient of a is positive, since it is one plus a positive actual support expression. More explicitly, 2t-b>0 by (6), and every remaining term in the bracket is nonnegative.

For fixed rho, put

    P=1-d/2+r/2, Q=2-d-r.

Then F=1-b P-t Q. Both P and Q are positive. By (4),

    0<=r<1/sqrt(5)<.45,

and consequently

    Q-(3/4)P=(10-5d-11r)/8
                >(10-5-11(.45))/8=1/160>0.     (10)

Differentiating with respect to the continuous northeast angle gives

    partial_theta F=t P-b Q
       <=b[(3/4)P-Q]<0.                         (11)

Thus F decreases throughout the whole interval (6). At theta0, where (b,t)=(4/5,3/5), its value is

    F(theta0,rho)=d+.2r-1.                       (12)

The strict necessary inequality (9) therefore forces d+.2r-1<0. If r=0, (12) is zero, already a contradiction. Otherwise put w=r/(1+d). The identity 1-d=r w gives

    d+.2r-1=r(.2-w).

Hence w>1/5. As 2w/(1-w^2) is strictly increasing for 0<=w<1, we obtain the necessary right-slope bound

    r/d>5/12.                                   (13)

This bound follows from the last actual N--R source, the same actual R wall and center, and the upper northeast angle. It does not assume an independently chosen position of R.

## 3. The right-supplied southeast separator contradicts (13)

The southeast angle q satisfies tan(q)=s/c<21/97<5/12. Thus (13) implies rho>q. Put

    alpha=cd+sr>0, delta=cr-sd>0.

For the first source u_R in (5), the exact upper E support is alpha A+delta H. Define

    A0=[a(c+s)-1]/s.

The coupled floor and H<=0 in (1) give A>A0. Retaining both pieces of that coupling,

    alpha A+delta H
       =(d/c)A+(delta/c)(sA+cH)
        >alpha A0>alpha(1-z),                   (14)

where d+delta s=c alpha and

    A0=a-z+(a-1)c/s>1-z.

By the strict face bound (3), separation along u_R would therefore require

    -d z(c+s)+r[.26+s(1-z)]<0.                  (15)

In fact (15) forces r/d<1/3. To verify this, the coefficient of r is positive, and the exact identity

    .26+s(1-z)-3z(c+s)
      =[.26(1+c)-s(2c-1)-4s^2]/(1+c)            (16)

has a strictly positive numerator. Indeed, c>.97, 0<s<.21 and 2c-1<=1 give

    .26(1+c)-s(2c-1)-4s^2
       >(.26)(1.97)-.21-4(.21)^2
        =.1258>0.                              (17)

If r/d>=1/3, the left side of (15) would thus be positive. Consequently this actual source requires r/d<1/3, contradicting (13).

## 4. The southeast-supplied separator also contradicts (13)

For the only other source u_E in (5), the coefficients in the right frame are alpha,-delta. Since rho>q, the latter is negative; the lower R support uses its actual upper v_R face. Using both strict bounds in (3),

    lower_R(u_E)=alpha L-delta(K+a)
       <alpha(d-.26r)-delta(-r+.4d)
        =c-.66cdr+s(.4d^2-.26r^2).              (18)

But upper_E(u_E)=A>1-z. Separation along u_E would require

    .66cdr-s(.4d^2-.26r^2)
       <c-1+z=z(1-s)<.11.                       (19)

For 0<=r/d<=1, the function kappa/(1+kappa^2) is increasing. Hence (13) gives

    dr>60/169.

As .4d^2-.26r^2<=.4, the left side of (19) is strictly greater than

    (.66)(.97)(60/169)-(.4)(.21)
       =3027/21125>.14>.11.                     (20)

This is a contradiction as well. Every actual southeast source remaining in (5) has now failed under the necessary consequence of the actual northeast source. This proves Theorem1.

## 5. The complete original near-right omission is excluded

**Theorem 2.** In the whole original MMMP family,

    Q10 owns F8  implies  Q5 strictly owns G8.    (21)

**Proof.** If Q5 excluded G8, its actual Q10 would have either a nonnegative or a nonpositive canonical representative. Theorem1 excludes the former. The theorem
`C1092-MMMP-NEGATIVE-RIGHT-ENDING.md`, combined with the same northeast upper-third theorem, excludes the latter. These two closed sign domains cover every square orientation, including the axial and diagonal representatives. Thus an absent G8 is impossible, proving its strict ownership in Q5. All uses of absence permit equality, so a boundary-only membership causes no exception. ∎

In the original V10 row, requiring its universal F9,G9 and excluding the actual foreign F6 in Q9, F7 in Q6, and G6 in Q5 leaves precisely the following literal right-component list:

    524800={F9,G9},
    525056={F8,F9,G9},
    787200={F8,F9,G8,G9}.

The last component is impossible by (21), since its actual G8 is then foreign to Q5. If F8 belongs to Q10, its remaining component is exactly525056, and the right-near theorem together with (21) gives actual Q5 the strict F4,G6,G8, a positive angle, and the actual Q9 bottom origin (2,1). This last conclusion does not retain the small-sine bound s<.21: that bound used the contrary G8 exclusion.

The untouched alternative Q10=524800 is still a separate original branch. The present theorem closes the entire F8-in-Q10/G8-excluded-from-Q5 branch, including both ownership and global absence possibilities for G8 outside Q5. Every support and point used in its proof belongs to the same explicitly named actual owner throughout.
