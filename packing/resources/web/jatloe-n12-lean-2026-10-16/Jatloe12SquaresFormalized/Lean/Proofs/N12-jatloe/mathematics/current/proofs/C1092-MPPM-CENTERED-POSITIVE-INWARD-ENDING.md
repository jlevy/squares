# C1092 MPPM: a nonnegative inward owner of the center is impossible

Every terminating decimal in this chapter is an exact rational number. All points described as owned are strictly inside their named actual open squares. Excluded points may lie on a face, and separating supports may be equal. The common side is a>1. The original entrance additionally has a<=1.001, but no argument below uses that upper bound.

Retain the original twelve owners and the no-omission MPPM branch of `C1092-MPPM-NO-OMISSION-REDUCTION.md`. A central owner is called nonordinary here precisely when it does not own its full ordinary pair. Normalize a nonordinary inward owner to Q4, so Q4 owns F4,G3. Suppose that Q4 also owns O=(2,2).

**Theorem 1.** This actual Q4 cannot have a nonnegative canonical orientation, including the axial orientation. Thus every center-owned nonordinary inward Q4, if it exists, has a strictly negative canonical representative. Simultaneous quarter-turns give the corresponding statement for each central sector.

The proof uses Q4 and both of its genuine ordinary neighbors Q5,Q7, together with already owned points in the actual walls and paired corners. It makes no assumption about whether the opposite Q6 is ordinary or inward, and supplies no new owner for an omitted auxiliary.

## 1. The actual inward rectangle and the two ordinary neighbors

Translate the whole configuration by (-2,-2), and write

    C=Q4, E=Q5, W=Q7.

Suppose C has frame

    u=(c,s), v=(-s,c), c>=s>=0, c^2+s^2=1.

Write U,V for its lower faces and A=U+a,H=V+a for its upper faces. The center premise gives

    U,V<0<A,H.                                      (1)

Its strict marker and inward points are

    M_C=(-.35,-.35), I=(0,-.26), J=(-.26,0).

Its two foreign neighboring markers are M_E=(.35,-.35) in E and M_W=(-.35,.35) in W. At M_W, the lower u-band follows from M_C, the upper u-band from O, and the lower v-band from O. Thus M_W is upper v. At M_E, the lower u-band and upper v-band follow from O. Its lower-v alternative would oppose the upper-v face at M_W and give width at most .7(c+s)<=.7sqrt(2)<1. Therefore M_E is upper u. We have proved

    0<A<=.35(c-s),  0<H<=.35(c+s).                  (2)

The inward no-omission reduction, Section1, gives the strict crosspoint

    X=(-.5,0) in C,

and forces the two actual ordinary pairs

    E: G5=(.26,-1), F6=(.4,-1);
    W: G4=(-.26,1), F3=(-.4,1).                    (3)

The point Y=(0,-.5) is also strict in C. Its lower u-band follows from X, because u(Y)-u(X)=.5(c-s)>=0; both upper bands follow from O. Its remaining lower v-band follows from (2):

    v(Y)-V >= a-.85c-.35s
               >=a-sqrt(.845)>0.                  (4)

The local diagonal theorem `INWARD-CENTER-DIAGONAL-POINT.md`, Theorem1, applies after the half-turn about O, using the strict O,M_C and the two actual excluded neighboring markers. It gives (-.5,-.5) strictly in C. Consequently

    the whole [-.5,0] x [-.5,0] is strict in C.      (5)

We also need C's actual inward tip. First G0 is omitted from C. Otherwise, since C is nonordinary, F0 would be omitted. Section2 of `C1092-MPPM-INWARD-OUTER-OWNED-ANGLE.md` excludes every nonnegative orientation from the strict inward pair, strict G0, omitted F0 and actual Q9 segment [F2,G2]. That sign argument does not use its later missing-center premise. Thus it applies here and would already be a contradiction.

With G0 genuinely omitted, Corollary3 of `C1084-DUPLICATE-POINT.md` under the simultaneous clockwise quarter-turn gives

    T_C=(-.01,-.54) strictly in C.                  (6)

Its original point is (1.99,1.46). The theorem's three strict anchors become Q4's marker,G3,F4; its three exclusions become the actual NW marker, actual SE marker, and exactly the omitted G0. These are the same literal point inputs recorded in Section7 of `C1092-MPPM-SMALL-INWARD-SUCCESSOR.md`; none requires the center to be absent.

The ordinary-marker halfpoint theorem applied to the actual E gives

    Y_E=(.5,-1) strictly in E.                       (7)

For explicit provenance, use the local-to-original map (xi,eta)->(2-eta,2-xi) in `ORDINARY-MARKER-HALFPOINT.md`, with d=.086. Its strict anchors become E's marker and ordinary pair in (3). Its exclusions are F4 in C, the bottom marker in Q9, the inner corner point in Q1, and F8 in Q10. The actual paired-corner transfer, Theorem7 of `C1092-DIRECT-WALL-POINT.md`, with Q1,Q10, b=.914 and ell=1.6, then gives

    O_R=(1,0) strictly in actual Q10.               (8)

In particular E excludes I,T_C by their ownership in C, and excludes the following genuine points:

    G=(1,-.4)       in Q10 (G8),
    K0=(1,-1)      in Q1,
    R0=(0,-1.086)  in Q9,
    O_R=(1,0)      in Q10.                          (9)

These actual point conclusions precede every orientation deduction about E.

## 2. The ordinary southeast neighbor is strictly negative

The complete local calculation in Sections2--4 of `C1092-MMMP-NORTHEAST-ANGLE.md` excludes a nonpositive B when its inward C has a nonpositive frame. That restricted part of the proof uses neither the extra point F of its local statement nor its Section5 positive-C calculation.

Apply exactly that restricted calculation after transposing the current centered coordinates, (x,y)->(y,x). The present nonnegative C becomes the local nonpositive C, and a hypothetically nonnegative E becomes the local nonpositive B. Every input actually used in Sections2--4 has the following source:

| Local point or exclusion | Current original owner or source |
|---|---|
| O,A=(-.5,0),D=(0,-.5),M_C strict in local C | The actual rectangle (5) and Q4 marker |
| Local G=(.35,-.35) excluded from C | Q7 marker after transposition |
| Local M=(-.35,.35) strict in B and excluded from C | Q5 marker after transposition |
| H1=(-1,.26),H2=(-1,.4) strict in B | G5,F6 in the same actual E |
| I_local=(-.39,0),A=(-.5,0) excluded from B | The actual C rectangle (5) |
| J_local=(-.39,1) excluded from B | (1,-.39) on Q10's whole strict G8--F8 segment |
| W_local=(-1.086,0) excluded from B | The actual bottom marker in Q9 |
| K_local=(-1,1) excluded from B | The actual inner corner point in Q1 |

The local proof first obtains all three forced B faces from these exclusions, then exhausts its two remaining actual separating sources for the entire nonpositive C angle range. The unavailable extra F in that chapter is used only in its Section5, which is not invoked here. Hence the literal Sections2--4 contradiction proves that E has a strictly negative canonical orientation. Axial and diagonal representatives are included in that exclusion.

Use its negative frame

    u_E=(d,-t), v_E=(t,d), d>=t>0, d^2+t^2=1,

and denote its lower faces by L,K and upper faces by J_E=L+a,D_E=K+a.

For clarity, the point-only face proof from Section3 of `C1092-MPPM-SMALL-INWARD-SUCCESSOR.md` gives, on the exact actual inputs (3),(6)--(9),

    L>=.26t,  L>=-.01d+.54t,
    J_E<=d+t, K>=-1.086d, D_E<=t.                 (10)

Here is also the complete short face derivation. At I its upper u-band follows from M_E and its lower v-band from F6. If it were upper v, the inner corner K0 would have to be upper u: its lower-v alternative would give width at most .74d-t<1. Then R0 would have to be lower u, since its lower-v alternative gives width at most .826d<1. The resulting two u-faces would give a<=d-.086t<=1. Thus I is lower u. At T_C the other three bands follow from M_E,F6, with projection increments .36d-.19t, .36t+.19d and .46d-.41t, all positive, so T_C is lower u.

At O_R both lower bands follow from M_E,F6. An upper-u exit opposed to I gives a<=d-.26t<=1, so O_R is upper v. At K0 the lower-u and upper-v bands follow from F6,M_E; its lower-v exit would now give a<=d<=1, so it is upper u. Finally R0 has both upper bands from G5,M_E; its lower-u exit would give a<=d-.086t<=1, so it is lower v. These are precisely (10), with every excluded-face equality retained.

## 3. G8 is the southeast square's upper transverse face

Every separating normal from C toward E has n_x>0 by the two strict markers. The strict pair Y=(0,-.5) in C and Y_E=(.5,-1) in E also gives n_y<n_x. Hence E's upward transverse source (t,d) cannot separate.

C's downward transverse source -v=(s,-c) cannot separate either: by (2),

    upper_C(-v)=a-H>.35(c+s)=(-v) dot M_E.

The strict E marker therefore defeats that source. The complete actual face-normal list has reduced to u and u_E.

Put

    k=cd-st>=0, j=ct+sd>0.

At G both lower E bands follow from M_E,F6. Suppose G were upper u. Then L<=d+.4t-a. On C's own u direction, (10) gives

    lower_E(u)<=k(d+.4t-a)+j(t-a).

Since A>0 and a>1, its deficit from upper_C(u)=A is strictly greater than

    -c[1-d-t+.4dt]-s[t-d-.4t^2]>0.                (11)

Indeed d+t-1=2dt/(1+d+t)>=.8dt, and t>0,d>=t. Both bracket signs in (11) are therefore the required ones.

On E's own u_E direction the upper C support is kA+j(a-H). Its deficit from L is strictly greater than

    1-d-.4t+j[1-.35(c+s)]
      >=1-d+.25t>0.                               (12)

For the middle inequality, j>=t(c+s), and, with h=c+s,

    h(1-.35h)-.65=(h-1)(.65-.35h)>=0

throughout 1<=h<=sqrt(2). Thus both possible separators fail. G cannot be upper u and must be upper v. We have proved the full actual E table

    L>=.26t, L>=-.01d+.54t,
    J_E<=d+t, K>=-1.086d, D_E<=t-.4d.             (13)

Its transverse width gives

    1<a<=t+.686d,
    z:=t/(1+d)>157/843>.186.                      (14)

The last implication is the exact half-angle factorization of t+.686d-1, whose positive root in the canonical half-angle interval is (1-.686)/(1+.686)=157/843.

## 4. The inward square is shallow and its upper face is high

The same complete C--E normal cone still leaves only u,u_E. On u, (13) now gives

    lower_E(u)<=k(d+t-a)+j(t-.4d-a)
      <c[1-d-t+.6dt]+s[t-d-.4-.6t^2]<0.           (15)

Again d+t-1>=.8dt makes the first bracket negative, and the second is negative because d>=t. This contradicts A>0. Consequently the only actual separator is E's own downward normal, and its exact necessary inequality is

    kA+j(a-H)<=L<=d+t-a.                           (16)

Let h=c+s and q0=1-.35h>0. From (2),(16), strict A>0 and a>1 imply

    1<d(1-sq0)+t(1-cq0).                          (17)

Both displayed coefficients are positive. Cauchy--Schwarz and the exact identity

    (1-sq0)^2+(1-cq0)^2-1
       =P(h):=2-2.7h+.8225h^2                     (18)

therefore give P(h)>0. On 1<=h<=sqrt(2)<10/7,

    P'(h)=-2.7+1.645h<=-.35,
    P(1.13)=-2999/4000000<0.

It follows that

    c+s<1.13, s<.14, c>.99.                       (19)

For the sine bound, sqrt(1-r^2)+r is increasing on [0,1/sqrt(2)], and at r=.14 it is greater than .99+.14=1.13. The cosine bound follows from 1-.14^2>.99^2.

Equation (16), again with A>0 and a>1, gives the stronger face lower bound

    H>1-(d+t-1)/j
      >=1-(1-z)/(c+s),                            (20)

because d+t-1=t(1-z) and j>=t(c+s). Also s/(1+c)<14/199<.08, so

    c+s=1+s-s^2/(1+c)>=1+.92s.

With (14), (20) consequently proves

    H>.186+.66s.                                  (21)

For an explicit whole-interval check, the difference between (z+.92s)/(1+.92s) and the right side of (21) has numerator

    z-.186+s(.08888-.6072s)>0,

since 0<=s<.14 and .08888-.6072(.14)=.003872>0. This includes s=0 by z>.186.

## 5. A genuine southeast point gives the inward square's narrow upper cap

The point Z_E=(.14,-.5) is strict in the same E. From (13), its four open-band gaps are at least

    a-.86d-.5t,
    a-.14d-.24t,
    a-.1d-.86t,
    a-.586d-.14t.                                 (22)

Their squared coefficient norms are respectively .9896,.0772,.7496,.362996, all strictly less than 1. Cauchy--Schwarz and a>1 prove all four gaps positive, without an angle restriction beyond the canonical range.

Thus Z_E is genuinely excluded from C. In C its lower u-band follows from O, because

    .14c-.5s>.0686>0.

Its upper v-band follows from O, and its lower v-band follows from the actual T_C in (6), because

    v(Z_E)-v(T_C)=.04c-.15s>.0186>0.

Consequently Z_E is upper u, giving

    0<A<=.14c-.5s<.14.                            (23)

The strictness in (22) and these comparisons makes (23) valid even when Z_E touches C's closure.

## 6. The other ordinary neighbor imposes an incompatible upper bound

We prove the following consequence of the actual C,W pair:

    H<.136+s.                                     (24)

Suppose instead H>=eta+s, where eta=.136=17/125. Retain (1),(19),(23). The complete point inputs in W are its strict marker and ordinary pair

    M_W=(-.35,.35), T0=(-.26,1), T1=(-.4,1).

The following points are genuinely excluded from this W:

    Z=(0,1.086)      actual Q11 marker,
    B=(.26,1)       G7 in actual Q11,
    C0=(-1,1)       actual paired Q3 inner corner,
    C1=(-1,1.086)   actual paired Q3 upper marker.

All these coordinates are translated original coordinates. In particular C1 is the actual original marker (1,3.086), not an invented point on a wall.

Orient every separating normal from C toward W. Their marker difference (0,.7) forces n_y>0. C's upward longitudinal normal u=(c,s) cannot separate, since C owns O while u dot M_W=.35(s-c)<=0. Thus C's only possible source is v=(-s,c).

A nonnegative W has only its upward transverse normal besides its upward longitudinal normal; the latter is excluded by the same comparison of O with M_W. A nonpositive W has its two upward normals available. These are all signed actual face normals supplied by the separating-axis theorem. The next two sections treat both complete canonical sign domains, including their endpoints.

## 7. Every nonnegative orientation of W fails

Use W's frame (b,r),(-r,b), with b>=r>=0, b^2+r^2=1. Write P,Q for its lower faces and J_W=P+a,D_W=Q+a for its upper faces.

At Z both lower bands are strict from T0,M_W. Thus Z is upper u or upper v. At C0 its upper u-band follows from T0 and its lower v-band from M_W. Thus C0 is lower u or upper v. At C1 the same two strict bands follow from T0,M_W: the increments are .74b-.086r>0 and .736b+.65r>0. If Z is upper u and C1 lower u, their two faces would give a<=b<=1. Hence, in that case, C1 is upper v. In every case we have the universal upper cap

    D_W<=1.086b+r.                                (25)

When Z is upper v the stronger D_W<=1.086b holds. When Z is upper u we have J_W<=1.086r. If additionally C0 is upper v, D_W<=b+r. If instead C0 is lower u, then

    1<a<=b+.086r,
    r/(1+b)<43/500,
    b+r<29/25.                                    (26)

Indeed r=0 would already make the first inequality impossible. The usual half-angle identity gives the second. At the endpoint 43/500 the sum b+r is 291151/251849<29/25, and that sum increases throughout the canonical interval.

Put

    k=cb+sr=cos(phi-p)>0,
    delta=cr-sb=sin(phi-p),

where p,phi are C's and W's ordinary nonnegative angles.

### 7.1. W's own transverse normal cannot separate

First suppose phi<=p. Its exact upper C support is -delta A+kH, at least kH. Here k>=c>.99. But (25), a>1 and r<=s give

    lower_W(-r,b)=Q<.086+s,
    kH>.99(.136+s)>.086+s.

The latter difference is at least .04864-.01(.14)>0, so the source fails.

Now suppose phi>=p. Its exact upper C support is delta(a-A)+kH. Subtract Q, use (23),(25), and retain the strictly positive a coefficient. The difference is strictly greater than

    F=1-1.086b-r
           +delta(1-.14c+.5s)+k(.136+s)
      =1-b Q_b-r Q_r,                             (27)

where

    Q_b=1.086-.136c+s-1.14cs+.5s^2,
    Q_r=1-c+.14-1.14s^2-.5cs-.136s.

The full range (19) gives Q_b<=.95 and Q_r<=.14. Explicitly,

    Q_b-.95=.136(1-c)+s(1-1.14c)+.5s^2
               <=s[-.1286+.57s]<=0,

using 1-c=s^2/(1+c), c>.99 and .136/(1+c)<.07. Also 1/(1+c)<.51 gives

    Q_r-.14<=-.63s^2-.5cs-.136s<=0.

Therefore

    F>=1-.95b-.14r>=1-sqrt(.9221)>0.              (28)

This source fails in the second angle order as well.

### 7.2. C's normal when phi<=p

Here delta<=0. Strict T0 in W gives J_W>-.26b+r. Using this and (25), the exact lower W support on v obeys

    lower_W(v)=delta J_W+kQ
      <c f0(phi)+s f1(phi),                        (29)

where

    f0=1+.086b^2+.74br-b,
    f1=.26+.74r^2+.086br-r.

This is obtained by replacing a by 1 in its negative coefficient. On 0<=phi<=p, r<=s<.14 and b>=c>.99. Direct differentiation gives

    f0'=-.172br+.74(b^2-r^2)+r>.68,
    f1'=1.48br+.086(b^2-r^2)-b>=-1.

For the first bound, .74(1-2(.14)^2)-.172(.14)=.686912>.68 suffices. Hence

    (c f0+s f1)'>.99(.68)-.14=.5332>0.

Its maximum on this whole interval is at phi=p. There delta=0,k=1, so (29)'s right side is s+1.086c-1<=s+.086. Thus lower_W(v)<s+.086<H, excluding C's source in this angle order.

### 7.3. C's normal when phi>=p

Now delta>=0 and lower_W(v)=delta P+kQ. If Z is upper v, P is strictly below u_W(M_W)=.35(r-b)<=0 and Q<.086. Thus lower_W(v)<.086<H.

Suppose Z is upper u. If C0 is upper v, the caps above give

    lower_W(v)
      <=delta(1.086r-a)+k(b+r-a)
      <c F0+s F1,

    F0=.5(b+r-1)^2+.086r^2,
    F1=r^2+b-r-.086br.                             (30)

We have F1<=1 and

    F0<=1.543-sqrt(2)<.13.

The latter strict bound follows, for example, from (1.413)^2<2. Therefore lower_W(v)<.13+s<H.

If C0 is instead lower u, retain (26) and the cap at C1. Then

    lower_W(v)
      <=delta(1.086r-a)+k(1.086b+r-a)
      <c G0+s G1,

    G0=.086+.5(b+r-1)^2<.0988,
    G1=r^2+b-r<=1.                                (31)

Again lower_W(v)<.136+s<=H. Every forced-face alternative for nonnegative W and both actual normal sources have failed.

## 8. Every nonpositive orientation of W fails

Use frame (b,-r),(r,b), with b>=r>=0. Keep P,Q,J_W,D_W for its faces. At C0, the upper u-band follows from T0 and both v-bands follow from M_W,T0. Equal projection increments at r=0 or b=r are strict bands because their anchors are strict. Thus C0 is lower u. At Z both lower bands follow from T0,M_W. Its upper-u alternative would oppose C0 and give a<=b-.086r<=1. Consequently

    P>=-b-r, J_W>=a-b-r,
    D_W<=1.086b, Q<=1.086b-a.                    (32)

Put

    k=cb-sr>=b(c-s)>0, j=cr+sb>=0.

### 8.1. The upward right-facing normal of W

On n=(r,b), the exact upper C support is jA+kH>=kH. Since H>=.136+s,

    kH>=b(c-s)(.136+s)>.7(.13464)>.086.            (33)

For the strict middle bound, c>.99 gives

    (c-s)(.136+s)>.13464+.854s-s^2>=.13464.

Equation (32) gives lower_W(n)=Q<.086, so this source cannot separate.

### 8.2. The upward left-facing normal of W

For n=(-b,r), its full upper C support is k(a-A)+jH. By (23) and the supposed lower bound on H, this exceeds

    .86k+j(.136+s).

The strict W marker gives lower_W(n)=-J_W<.35(b+r). The support difference is therefore greater than bF+rG, where

    F=.86c+.136s+s^2-.35>.5014,
    G=.136c+s(c-.86)-.35>-.21536.                 (34)

Since b>=r>=0, F>0 and F+G>.28604, this difference is positive regardless of the sign of G. Thus this source fails too.

### 8.3. C's normal and a continuous quartic bound

The only remaining actual source is v=(-s,c). From (32),

    lower_W(v)=-j J_W+kQ
      <=j(b+r-a)+k(1.086b-a)
      <c f(phi)+s g(phi),                          (35)

where

    f=.086b^2+.5(b+r-1)^2,
    g=b^2-.086br-b+r<=1.

We prove f<.136 on the entire canonical interval. Set w=r/(1+b), so 0<=w<=sqrt(2)-1<5/12. The exact positive-denominator identity is

    500(1+w^2)^2(.136-f)
       =-975w^4+2000w^3-778w^2+25.                (36)

Put h=w-1/3, so -1/3<=h<=1/12. The numerator in (36) becomes exactly

    16/27+(32/9)h+h^2(572+700h-975h^2).

Throughout this whole interval,

    572+700h-975h^2>=691/3.

Consequently the numerator is at least

    16/27+(32/9)h+(691/3)h^2>0.                  (37)

This quadratic has positive leading coefficient and discriminant -1600/3<0. Thus (37) proves (36) strictly positive for all angles, not only for selected orientations. Combining (35)--(37),

    lower_W(v)<.136c+s<=.136+s<=H.

This last actual separator is impossible as well. Sections7--8 exhaust both closed canonical signs of W, proving (24).

## 9. The final contradiction and exact scope

The two ordinary neighbors have imposed (21) and (24) on the upper face H of the same actual inward square C. Their difference satisfies

    (.186+.66s)-(.136+s)
       =.05-.34s>.05-.34(.14)=3/1250>0.

These inequalities are incompatible. This proves Theorem1 for the full nonnegative canonical C domain, including the axial endpoint and all weak face or separation contacts.

The proof used the no-omission inward-neighbor theorem only to obtain the actual crosspoint and ordinary pairs in (3); the center O was the stated premise. G0's omission was derived from nonordinary status and the independent nonnegative-sign obstruction. Each later strict point belonged to its named actual C,E,Q10 or paired corner, and the final W argument used its own full square together with the genuine Q11 and Q3 points. No ordinary status or center conclusion was imposed on the opposite Q6.

This chapter closes every center-owned, nonnegative, nonordinary inward regime. Its strictly negative center-owned counterpart is a separate remaining regime unless excluded by another proved chapter.
