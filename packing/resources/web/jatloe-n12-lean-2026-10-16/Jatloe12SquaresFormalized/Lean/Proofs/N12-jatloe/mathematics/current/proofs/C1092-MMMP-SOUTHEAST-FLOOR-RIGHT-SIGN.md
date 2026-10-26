# C1092 MMMP: the whole bottom bar gives a strict southeast support floor

All terminating decimals are exact rationals. Every square is an actual open square, ownership is strict, and exterior or separating-face inequalities may be equality. We use common side a>1 and retain both the strict whole bottom bar and the actual right wall and center condition.

## 1. The exact original entrance

Assume that actual Q10 owns F8=(3,1.74) and actual Q5 excludes G8=(3,1.6). The approved theorem `C1092-MMMP-RIGHT-NEAR-BOTTOM-ORIGIN.md` then gives

    F4,G6 strictly in Q5,
    Q5 positive, 0<s<.21, c>.97,
    (2,1) strictly in Q9.

Translate by (-2,-2), write C=Q5, and choose its positive canonical frame

    u=(c,s), v=(-s,c), c>=s>0, c^2+s^2=1.

Let U,V be its lower face coordinates, and A=U+a,H=V+a its upper coordinates. Its strict anchors are

    M=(.35,-.35), I=(0,-.26), D=(.26,0).

The foreign center O=(0,0) lies strictly in Q7. Its two u bands follow from I,D, and its lower v band follows from M, so it is upper v:

    H<=0.                                          (1)

The absent G8 is G=(1,-.4). Its lower u band follows from D, and its upper v band follows from M. If it left through lower v, (1) would imply

    a<=s+.4c<.6,

where the strict bound is established in Section4 of RIGHT-NEAR-BOTTOM-ORIGIN. Thus it is upper u:

    A<=c-.4s.                                      (2)

The actual Q9 contains the entire strict segment

    B=[0,.4] x {-1},                               (3)

by its just-proved origin and universal F6 ownership. The actual R=Q10 has closure in x<=2, center ordinate at least zero, and strictly owns P_R=(1,0), its universal right origin. These are the genuine original right wall, closed MMMP sign Y10>=2, and right-origin theorem.

No G8 ownership in Q10 is required. Its exclusion from Q5 is the premise giving (2).

## 2. The whole bar gives an exact support floor for C

**Lemma 1.** Under the entrance above, put z=s/(1+c). The lower closed vertex of C lies strictly above y=-1 and has abscissa in (0,1/4). Consequently

    sA+cH>a(c+s)-1,
    U>(ac-1)/s>-z,
    A>a-z.                                        (4)

**Proof.** The left endpoint P=(0,-1) of the actual bar is excluded from C. Its two upper bands follow from I. If it left through lower v, then V>=-c and (1) would give a=H-V<=c<=1. Therefore P is lower u:

    U>=-s.                                        (5)

Together with (2), this also gives

    a=A-U<=c+.6s.                                 (6)

The lower closed vertex is

    Z=(cU-sV, sU+cV).

From (1),(5) one obtains

    Z_x>=-cs+as=s(a-c)>0.                          (7)

Strict I gives U<-.26s. Strict D gives H>-.26s, or V>-a-.26s. Thus (6) yields

    Z_x<-.26cs+s(a+.26s)
         <s(a+.26s)<=s(c+.86s)
         <.21(1+.86·.21)
          =123963/500000<1/4.                      (8)

We show Z_y>-1 using the actual bar, rather than its two endpoint exclusions. If Z_y<-1, the segment from strict M to Z crosses y=-1 before reaching Z, with abscissa strictly between0 and.4 by (7),(8) and M_x=.35. Every point before Z on this segment belongs to the interior of C: its four strict defining linear bands are interpolated between a strict point and a closure point. This gives a strict intersection with (3).

If Z_y=-1, then Z itself is in the strict bar (3), hence in the open square Q9, and also in the closure of C. This too is impossible: an open neighborhood of Z inside Q9 must meet C because Z is a closure point of C. Thus closures of one square cannot meet the interior of a disjoint open square. This explicitly excludes the potentially tangent endpoint case.

We have proved Z_y>-1. Replacing U,V by A-a,H-a gives the first inequality in (4). Alternatively, V=H-a<=-a and sU+cV>-1 give

    U>(ac-1-cH)/s>=(ac-1)/s.

Since a>1 and (1-c)/s=z, the last quantity is greater than -z. Adding a proves the final assertion of (4). ∎

## 3. The two downward right sources are excluded

**Lemma 2.** Assume in addition that R has a nonnegative canonical frame

    w=(d,r), w_perp=(-r,d), d>=r>=0, d^2+r^2=1.

Of the actual separating sources from C toward R, the two downward directions -v and -w_perp are impossible. Thus only the upward directions u and w remain. This lemma makes no assertion that the nonnegative sign of R is impossible.

**Proof.** The strict pair D=(.26,0) in C and P_R=(1,0) in R forces every separating normal from C toward R to have n_x>0. The complete possible actual face-normal directions are therefore

    u, -v, w, -w_perp.

At an axial endpoint a direction with zero x component is already excluded by this strict cone. Including that direction in a bound below does no harm. The genuine wall and center hypotheses are

    center_x(R)<=2-a(d+r)/2,
    center_y(R)>=0.                               (9)

For a unit direction n, its actual-square support radius is

    (a/2)(|n dot w|+|n dot w_perp|),

and the parenthesized width is at least1.

For n=-v=(s,-c), both signs in (9) give the legitimate upper support estimate

    lower_R(-v)<=2s-a[s(d+r)+width_R(-v)]/2
                  <=2s-a/2<.42-.5<0.

But upper_C(-v)=-V=a-H>=a>1 by (1), so this direction cannot separate.

For n=-w_perp=(r,-d), put

    alpha=cd+sr=cos(rho-q)>0,
    delta=cr-sd=sin(rho-q),

where q=arcsin(s) and rho=arcsin(r). Its components in C's frame are delta,-alpha. If delta>=0, its upper C support is delta A-alpha V>=a alpha, because A>a-z>0. If delta<0, the support is delta U-alpha V>=a alpha, because strict I gives U<0. Also alpha>=1/sqrt(2), since q,rho belong to [0,pi/4].

On R's own downward normal, (9) gives

    lower_R(-w_perp)<=2r-a[1+r(d+r)]/2
                       <=2r-1/2-r^2
                       <=sqrt(2)-1<1/sqrt(2).

The second inequality uses d>=r; the third uses monotonicity of 2r-1/2-r^2 on 0<=r<=1/sqrt(2). This is strictly below upper_C(-w_perp)>=a/sqrt(2), so the other downward source cannot separate either. The only remaining actual sources are u and w. ∎

## 4. Scope of the proved reduction

Whenever Q10 owns F8 and Q5 excludes G8, the actual southeast Q5 has the quantitative positive angle and the exact strict coupled floor (4). If Q10 is nonnegative, its actual pair with Q5 can separate only on one of the two upward normals in Lemma2. These statements hold whether G8 is owned by Q10 or by neither of these two squares.

The hypothesis center_y(R)>=0 upper-bounds supports in downward directions, as used in Lemma2. It does not upper-bound supports in upward directions: their nonnegative center-y contribution must be retained. In particular, this chapter does not conclude a negative right angle. The remaining upward separation requires the actual northeast owner or another additional geometric premise.

The floor proof uses the strict whole bar of the actual Q9, including the possible tangency of a central closure vertex. Independent absences of the two endpoints do not replace that premise.
