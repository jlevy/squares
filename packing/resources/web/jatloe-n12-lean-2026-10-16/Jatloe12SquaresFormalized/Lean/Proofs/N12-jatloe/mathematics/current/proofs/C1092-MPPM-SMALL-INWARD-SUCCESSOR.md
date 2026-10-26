# C1092 MPPM: a small negative inward square and its actual ordinary successor

All terminating decimals are exact rational numbers. All named squares are actual open squares of the common side a>1 with disjoint interiors. Owned points are strict; excluded points and separating supports may meet boundaries. The local theorems use no side upper bound and no artificial owner for an omitted auxiliary.

## 1. The local statement and the complete normal cone

Let C have negative canonical frame

    u=(c,-s), v=(s,c), c>=s>0, c^2+s^2=1,
    0<x:=s/(1+c)<=53/500.

Write U,V for its lower faces, A=U+a,H=V+a for its upper faces. Suppose C strictly owns

    M_C=(-.35,-.35), I=(0,-.26), J=(-.26,0),
    X=(-.01,-.54),

and satisfies

    U>=-c+.4s, H<=0.                               (1)

Suppose its ordinary successor E strictly owns

    M=(.35,-.35), B0=(.26,-1), B=(.4,-1),
    Y=(.5,-1),

and excludes the actual points

    I, X, G=(1,-.4), K0=(1,-1),
    R0=(0,-1.086), O_R=(1,0).                       (2)

The exclusions I,X are already supplied by their strict ownership in the different actual C.

**Theorem 1.** Under these hypotheses, E has a strictly negative canonical angle. In that negative frame (d,-t),(t,d), its upper transverse face is at most t-.4d.

**Theorem 2.** If E additionally excludes F=(1,-.56), then C and E cannot have disjoint interiors.

The extra F exclusion will have the actual right-wall owner in the MPPM application. A whole wall segment or boundary-center claim is not a local premise.

The half-angle bound implies the convenient exact estimates

    c>97/100, 0<s<21/100.                           (3)

For example c>=247191/252809 and s<=53000/252809, which give (3) by integer comparison. The strict C points J and I and (1) give the simultaneous inequalities

    A>=a-c+.4s>.4s>0,
    H>-.26s,
    H<=0.                                          (4)

Orient a separating normal from C toward E. The strict marker difference (.7,0) forces n_x>0. The strict pair I,Y gives

    .5n_x-.74n_y>0,
    n_y<(25/37)n_x.                               (5)

The C normal v=(s,c) is therefore impossible, since c/s>97/21>25/37. Its own remaining source is u. We retain the two right-facing E sources for each sign below. This accounts for all actual face normals by the separating-axis theorem, including possible axis directions at endpoints.

## 2. A nonnegative ordinary successor is impossible

Give E the nonnegative frame u_E=(d,t),v_E=(-t,d), d>=t>=0, d^2+t^2=1. Write L,W for its lower faces and J_E=L+a,K_E=W+a for its upper faces.

At G its lower u band follows from M, its lower v band from B, and its upper v band from M. The positive or nonnegative projection increments are

    .65d-.05t>=.60d>0,
    .6(d-t)>=0,
    .65t+.05d>0.

Thus G is upper u, while strict M supplies the other bound

    L<=d-.4t-a,
    K_E>-.35(d+t).                                (6)

Put k=cd-st>0, h=ct+sd>0. From (3) and d>=t,

    k>=d(c-s)>(7/10)(76/100)>1/2.                 (7)

The only possible sources are u,u_E,-v_E.

### 2.1. E's upward normal

If u_E is eligible in (5), then t/d<25/37. Its full upper C support is kA+hH. By (4), it exceeds s(.4k-.26h). The coefficient satisfies

    .4k-.26h
      =d(.4c-.26s)-t(.4s+.26c)
      >d[(83/370)c-(981/1850)s]>0,                (8)

where (3) proves the last sign. For t=0 the first inequality can be weakened to equality without changing positivity. But (6) gives lower_E(u_E)=L<d-.4t-1<=0. Thus this source cannot separate.

### 2.2. E's downward normal

The full upper C support on -v_E=(t,-d) is

    hA-kV=hA+k(a-H)>k>1/2

by (4),(7). Its lower E support is -K_E<.35(d+t)<=.35sqrt(2)<1/2. This source fails as well.

### 2.3. C's normal: an exact continuous polynomial certificate

The exact lower E support is kL-hK_E. By (4),(6), its deficit from upper_C(u)=A is strictly greater than

    F_plus=1-c+.4s+k(1-d+.4t)-.35h(d+t).           (9)

Every coefficient of a replaced by1 is positive. Set y=t/(1+d), and use the standard rational half-angle formulas for c,s,d,t. Then

    P_plus=20(1+x^2)(1+y^2)^2 F_plus
      =x^2(80y^4+2y^3+68y^2-2y+40)
        +x(2y^4-132y^3-4y^2-28y+2)
        -40y^4-2y^3+12y^2+2y.                    (10)

The canonical interval lies within0<=y<=5/12, because sqrt(2)-1<5/12. The companion `C1092-MPPM-SMALL-INWARD-SUPPORT-CERTIFICATE.txt` gives an exact Bernstein expansion on the three full rectangles

    0<=x<=53/500,
    y in [0,1/5], [1/5,1/3], [1/3,5/12].

Their least coefficients are respectively

    0, 42572/78125, 1377211/21600000.

In the first rectangle only coefficient(0,0) is zero, and every row of positive x degree is strictly positive. The actual x>0 therefore makes P_plus>0 even on y=0. All other rectangles have strictly positive coefficients. The exact polynomial identity, complete coefficient tables and the formula for their reconstruction are included in that companion. The nonnegative Bernstein weights sum to1 on each whole rectangle, so this is a continuous proof of F_plus>0, including every endpoint, not sampled angle evidence.

Thus u cannot separate either. This excludes the entire nonnegative E sign.

## 3. The negative successor's actual forced faces

Now give E the negative frame

    u_E=(d,-t), v_E=(t,d), d>=t>=0,
    L,W lower faces, J_E=L+a,K_E=W+a.

The upward E normal v_E is ineligible in (5), since d/t>=1>25/37 whenever t>0; at t=0 its horizontal component is zero. Only u and u_E remain.

We first establish

    L>=.26t,
    L>=-.01d+.54t,
    J_E<=d+t,
    W>=-1.086d,
    K_E<=t.                                        (11)

At I its upper u band follows from M and its lower v band from B. Thus I is lower u or upper v. Suppose the latter, K_E<=-.26d. At K0 its lower u and upper v bands follow from B and M; a lower v exit would give width at most .74d-t<1. Hence K0 would be upper u, J_E<=d+t. At R0 both upper bands follow from B0,B. A lower v exit would give width at most .826d<1, so it would be lower u, L>=1.086t. The two resulting u faces give a<=d-.086t<=1, impossible. Therefore I is lower u and L>=.26t.

At X its upper u and upper v bands follow from M, and its lower v band follows from B. The three positive increments are

    .36d-.19t>=.17d,
    .36t+.19d,
    .46d-.41t>=.05d.

Thus X is lower u and L>=-.01d+.54t.

At O_R both lower bands follow from M and B. An upper u exit would oppose L>=.26t and give width at most d-.26t<=1. Thus O_R is upper v and K_E<=t.

At K0 its lower u and upper v bands are strict as before. A lower v exit now gives width at most d<=1, so J_E<=d+t. Finally R0 has both upper bands as before, and its lower u alternative would give a<=d-.086t<=1. Hence W>=-1.086d. This proves (11). It also excludes t=0: the u width would then be at most1. Consequently E has strictly negative angle.

All these point exits permit equality. They use the one actual E and the exclusions in (2), with no boundary-center estimate.

## 4. The outer point G cannot be an upper-u exit

Both lower E bands at G follow strictly from M,B. Thus it is upper u or upper v. Suppose it were upper u, so

    L<=d+.4t-a.                                    (12)

We defeat both possible actual normals for both orders of p and q, the positive magnitudes of the C and E angles. Write

    k=cd+st=cos(q-p)>0,
    delta=ct-sd=sin(q-p).

### 4.1. E's own normal

If q>=p, delta>=0 and the upper C support is kA-delta V. By (4), it is at least k(a-c+.4s)+delta a. Subtracting (12), and replacing a by1 with positive coefficient, gives a strict lower margin

    1+k-2kc+delta(1+s-.4c)>0.                      (13)

Here1+k-2kc=1-k+2k(1-c)>0 and the delta coefficient is positive.

If q<=p, put gamma=-delta>=0. The upper C support is kA+gamma H, strictly greater than k(a-c+.4s)-.26gamma s. The resulting strict lower margin is

    1+k-2kc+gamma(.4c-1.26s)>0.                   (14)

The last coefficient is positive by (3). Thus u_E cannot separate in either angle order.

### 4.2. C's own normal

If q>=p, the lower E support is kL+delta W. Use (12) and W=K_E-a<=t-a from (11). Subtract from (4), and replace a by1. The strict lower margin is

    F=1-2c+.4s+k+delta-.4kt
      >=2(1-c)+delta[.6-delta/(1+k)]>0.           (15)

For the inequality use t=ks+delta c, k^2+delta^2=1, and kc<=1. Also delta/(1+k)=tan((q-p)/2)<=sqrt(2)-1<.6. Since c<1, the final sign is strict even at delta=0.

If q<=p, gamma=-delta>=0 and the lower E support is kL-gamma K_E. The actual marker gives K_E>.35(t-d). With (12), the strict lower margin becomes

    F=1-2c+k+gamma(.05d-.65t).                     (16)

Now k>=c, and

    2gamma t=cos(p-2q)-c<=1-c.

Therefore

    F>=(27/40)(1-c)+.05gamma d>0.                 (17)

This excludes u in the second angle order too. No angle endpoint has been lost. Thus (12) is impossible; G must be upper v:

    K_E<=t-.4d,
    1<a<=t+.686d.                                 (18)

This completes Theorem1.

## 5. The genuine far point makes E's angle steep

For Theorem2 suppose F=(1,-.56) is also excluded. At F both lower E bands follow from M,B0 with positive increments .65d+.21t and .74t+.44d. Thus F is upper u or upper v.

The function sin q+.686 cos q is increasing on [0,pi/4]. At q1=2 arctan(1/6), its value is36.01/37<1. Equation (18) therefore gives q>q1 and d<35/37.

If F were upper u, the second lower-u bound in (11) would give

    a<=1.01d+.02t
      <(101/100)(35/37)+1/50
       =3609/3700<1,

a contradiction. Consequently F is upper v and

    K_E<=t-.56d,
    1<a<=t+.526d.                                 (19)

The latter function is again strictly increasing on the canonical interval. At q0=2 arctan(3/10), its value is53933/54500<1. Hence

    q>q0,
    y=t/(1+d)>3/10>x,
    delta=ct-sd>0.                                (20)

Only the two downward longitudinal normals remain, as proved in Section3.

## 6. The two final supports have positive continuous margins

For C's own normal, (11),(19) give

    lower_E(u)=kL+delta W
      <=k(d+t-a)+delta(t-.56d-a).

Subtracting from A>=a-c+.4s and using a>1 gives the strict lower margin

    F_C=1-c+.4s+k(1-d-t)+delta(1-t+.56d).           (21)

For E's own normal, the exact upper C support is kA-delta V. Equations (1),(4) give

    upper_C(u_E)>=k(a-c+.4s)+delta a.

Its lower E support is L<=d+t-a. The strict lower margin is therefore

    F_E=1-d-t+k(1-c+.4s)+delta.                     (22)

Both coefficients of a that were replaced by1 are1+k+delta>0. The exact numerator polynomials are

    P_C=25(1+x^2)(1+y^2)^2 F_C
      =x^2(100y^4-72y^3+150y^2-28y+50)
        +x(42y^4+100y^3-104y^2+100y-58)
        -50y^4+72y^3-50y^2+28y;

    P_E=5(1+x^2)^2(1+y^2) F_E
      =x^4(20y^2-20y-10)
        +x^3(14y^2+40y-14)
        +x^2(10y^2-4y+10)
        +x(6y^2-6)+10y^2.                         (23)

The exact coefficient certificate in `C1092-MPPM-SMALL-INWARD-SUPPORT-CERTIFICATE.txt` expands these on the entire closed rectangle

    0<=x<=53/500, 3/10<=y<=5/12.

All Bernstein coefficients are strictly positive. Their respective minimum coefficients are

    300932897/125000000,
    133610978399/312500000000.

The certificate states all coefficients and the exact reconstruction identities. It proves F_C,F_E>0 on the entire enlarged domain containing (20). Thus neither actual square normal can separate. This proves Theorem2 for every E orientation, including all canonical endpoints and all weak separating contacts. ∎

## 7. Literal original MPPM application and its scope

In the original no-omission MPPM family, suppose Q4 owns its inward pair F4,G3 and omits G0. Suppose also that its center point (2,2) is absent and that Q4 has negative canonical half-angle at most53/500. Translate the whole configuration by(-2,-2) and take C=Q4,E=Q5.

The actual point and face sources are:

| Local datum | Actual original source |
|---|---|
| C marker,I,J | Q4 marker,F4=(2,1.74),G3=(1.74,2) |
| C tip X=(-.01,-.54) | (1.99,1.46) in Q4 by C1084 Corollary3 under the simultaneous clockwise quarter-turn; its outer exclusion is exactly the omitted G0 |
| H<=0 | Missing(2,2): its two u bands follow from the inward pair and its lower v band from the marker, so it is upper v |
| U>=-c+.4s | G0=(1,1.6) is excluded; it is lower u since its lower v exit would give width at most s+.4c<1 |
| E marker,B0,B | Q5 marker,G5,F6, forced by the original inward-neighbor theorem |
| E halfpoint Y | (2.5,1) in Q5 by ORDINARY-MARKER-HALFPOINT, since F4 is foreign in Q4 |
| E exclusion G | G8=(3,1.6), strict in the actual no-omission Q10 |
| E exclusion K0 | (3,1), strict in the actual paired Q1 |
| E exclusion R0 | The original bottom marker(2,.914), strict in Q9 |
| E exclusion O_R | (3,2), strict in Q10 by the actual Q1 paired-corner transfer from Y |

The full inward source is `C1092-MPPM-NO-OMISSION-REDUCTION.md`, Section1; the tip source is `C1084-DUPLICATE-POINT.md`, Corollary3. For the halfpoint theorem the local-to-original map is (xi,eta)->(2-eta,2-xi), d=.086. In this map the theorem's foreign wall marker is the actual bottom marker in Q9, and its fourth excluded point F=(.26,-1) is original F8=(3,1.74), strictly owned by the actual Q10. The paired-corner transfer, Theorem7 of `C1092-DIRECT-WALL-POINT.md`, then uses actual Q1 and Q10 with b=.914 and ell=1.6.

For the forced G0 exit in the table, its upper u and upper v bands follow from the strict marker and J. Its two remaining possibilities are lower u and lower v. A lower v exit, together with H<=0, would give a<=s+.4c<=7sqrt(2)/10<1, because sin p+.4cos p increases throughout the canonical interval0<=p<=pi/4. Thus it is lower u. Every point and support in this entrance belongs to the named actual owner.

If opposite Q6 has its ordinary pair, it owns F9=(3,2.26). Section5 of `C1092-MPPM-NONORDINARY-ISOLATION.md` advances the actual Q10 to (3,1.44). This is precisely the extra F=(1,-.56) in Theorem2, with its actual owner Q10. Theorem2 is then a contradiction.

Therefore in this small-negative, missing-center, G0-omitted inward branch, Q5 must have negative angle and its stated full transverse cap; moreover opposite Q6 cannot be ordinary. Combined with the completed elbow exclusion, the opposite square must have its inward alternative. This chapter does not assume the bottom-wall small-angle theorem or assert that all other inward regimes are already closed. Its local support results can be joined to those further original-entrance deductions separately.
