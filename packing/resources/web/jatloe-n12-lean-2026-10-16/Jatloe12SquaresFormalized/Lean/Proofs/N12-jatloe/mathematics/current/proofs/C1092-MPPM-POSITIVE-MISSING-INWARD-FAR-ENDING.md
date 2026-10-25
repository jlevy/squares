# C1092 MPPM: a positive missing-center inward square cannot face an ordinary opposite

Every terminating decimal is an exact rational. Owned points are strict;
excluded points and separating supports may be equalities. All local squares
are actual open squares of common side a>1. This chapter uses no side upper
bound, container relaxation or finite orientation list.

## 1. The local ending and its actual inputs

**Theorem 1.** Retain the complete local hypotheses of
C1092-MPPM-POSITIVE-MISSING-INWARD-SUCCESSOR.md, Theorem 1, for C and E.
Suppose in addition that C excludes the whole segment

    S=[R,H1], R=(-1.086,0), H1=(-1,.26),               (1)

and E excludes the point

    F=(1,-.56).                                       (2)

Then C and E cannot have disjoint interiors.

The preceding theorem has already proved the strict point Y=(0,-.5) in C,
the strictly positive C angle p, the strictly negative E angle q, and
the simultaneous C faces

    u=(c,s), v=(-s,c), c>=s>0, c^2+s^2=1,
    U>=-c-.4s, A=U+a<=0,
    V>=.4s-c, H=V+a<=.35(c+s).                       (3)

The lower and upper u-faces in (3) imply

    1<a<=c+.4s,
    0<x:=s/(1+c)<2/5.                                (4)

Thus p<2 arctan(2/5)<pi/4. E has frame

    u_E=(d,-t), v_E=(t,d), d>=t>0, d^2+t^2=1.

Write L,W for its lower faces and J_E=L+a,K_E=W+a for its upper faces.
Its original strict anchors and foreign points are exactly

    M=(.35,-.35), B0=(.26,-1), B=(.4,-1), Y_E=(.5,-1) strict;
    G=(1,-.4), K0=(1,-1), R0=(0,-1.086), Y=(0,-.5) excluded.

These force the same elementary ordinary faces as
C1092-MPPM-ELBOW-EXCLUSION.md, Lemma 1:

    L>=.5t, J_E<=d+t,
    W>=-1.086d, K_E<=t-.4d,
    1<a<=t+.686d.                                     (5)

For completeness, Y has its other three bands from B,M,B0 and so is lower
u. At G both lower bands follow from M,B, while its upper u-band follows
from d+.4t<=1+.5t<a+L; hence it is upper v. At K0 its lower u and upper
v-bands follow from B,M; a lower-v exit would give a<=.6d. Thus it is
upper u. At R0 both upper bands follow from B,B0; a lower-u exit would
give a<=d-.086t<=1. Thus it is lower v. This proves all of (5) without
any residual-elbow premise.

At F both lower bands follow from M,B0. If F were upper u, (5) would
give a<=d+.06t, hence t<.12; but a<=t+.686d<.806 would then be impossible.
Consequently F is upper v and

    K_E<=t-.56d,
    1<a<=t+.526d.                                     (6)

The function sin q+.526cos q increases strictly on the canonical range.
At q0=2 arctan(3/10), its value is 53933/54500<1. Thus

    q>q0, d<91/109, t>60/109,
    d+t-1>19/50.                                      (7)

Put

    kappa=cd-st=cos(p+q)>0,
    lambda=ct+sd=sin(p+q)>0.                           (8)

The strict positivity of kappa follows from (4) and q<=pi/4. The marker
difference (.7,0) makes every C-to-E separating normal have positive
horizontal component. The full remaining actual face-normal list is

    u, -v, u_E, v_E.                                  (9)

The proofs below cover all four, whether or not an individual endpoint
normal is eligible in the strict cone.

## 2. Three of the four actual sources fail on the whole angle range

For u, use A>=a-c-.4s, L<=d+t-a and W<=t-.56d-a. The support difference
is strictly greater than

    F_u=1-c-.4s+kappa(1-d-t)+lambda(1-t+.56d).         (10)

For fixed q its p derivative is

    F_u'=s-.4c+lambda(d+t-1)+kappa(1-t+.56d).

If p>=arctan(.4), every term here is nonnegative and the last one is
positive. If p<=arctan(.4), then

    kappa>=cos(pi/4+arctan(.4))=3/sqrt(58)>3/8,
    lambda>=t>11/20,
    1-t+.56d>=1-.44/sqrt(2)>17/25.

Together with (7), these give F_u'>-2/5+(11/20)(19/50)+(3/8)(17/25)
=8/125>0. At p=0,

    F_u=d+t-1-.44dt>=.36dt>0,

because d+t-1=2dt/(1+d+t)>=.8dt. Thus (10) is positive for every p in
(4), and u cannot separate.

For -v, use H<=.35(c+s), L<=d+t-a and W>=-1.086d. Its strict lower
support margin is

    F_{-v}=1-.35(c+s)+kappa(1-1.086d)+lambda(1-d-t).

Here 1-1.086d>0 by (7), while 0<lambda<=1. Therefore

    F_{-v}>=2-(d+t)-.35(c+s)>=2-1.35sqrt(2)>0.        (11)

For v_E, use A>=a-c-.4s, H>=a+.4s-c and W<=t-.56d-a. Its strict
lower margin is

    F_{v_E}=1+(kappa+lambda)(1-c)
                   +.4(kappa-lambda)s-t+.56d.

Since |kappa-lambda|<=1 and t<=d<=1, this is at least
1-.4s-.44d>4/25>0. All coefficients of a replaced by 1 are positive.
Only the source u_E remains.

## 3. The marker cap closes every central half-angle x>=1/5

Using (3), the exact upper support on u_E is kappa A-lambda V. With
L<=d+t-a, its deficit from the E lower support has the strict lower bound

    F=1-d-t+kappa(1-c-.4s)+lambda[1-.35(c+s)]
     =1-d B_0-t A_0,                                 (12)
    A_0=1.35-c+s-.75s^2-.65cs,
    B_0=2-c-s-.65s^2+.75cs.

The exact single-variable identity is

    400(1+x^2)^2(1-A_0^2-B_0^2)
      =-[5409x^4-2196x^3-366x^2-204x+49].             (13)

On 1/5<=x<2/5, the bracket in (13) is at most

    x^3(5409x-2196)-366x^2-204x+49
       <=-366/25-204/5+49=-161/25<0.                (14)

Indeed 5409x-2196<5409(2/5)-2196=-162/5<0, and the remaining quadratic
is decreasing for x>=0. Thus A_0^2+B_0^2<1. Cauchy's inequality now
gives d B_0+t A_0<1 for every actual unit (d,t), and (12) is positive.
This proves the whole larger-angle regime.

## 4. The actual segment supplies two sources for x<=1/5

Suppose now 0<x<=1/5. Orient a separating normal from S toward C.
The strict C point J=(-.26,0), compared with R, forces n_x>0.
C's u normal cannot separate: by A<=0,

    lower_C(u)=U<=-a<-1,
    upper_S(u)>=u(H1)=-c+.26s>=-1.

The separating-axis theorem for the actual square C and the one segment
S therefore leaves only

    -v=(s,-c),
    n=(.26,-.086), perpendicular to S.                (15)

This cover does not assume F0 ownership or a negative vertical component
from an unproved C point. All other C signed normals have negative
horizontal component; the opposite segment normal does as well.

Define

    alpha=.26c-.086s>0,
    gamma=.26s+.086c>0,
    D0=.28236.

For the first source in (15), the maximum projection of S is -1.086s,
so it gives

    H<=1.086s.                                        (16)

For the second source, n has the constant value -D0 on S, and the exact
minimum projection of C is alpha U-gamma H. Hence it gives

    alpha U-gamma H>=-D0.                            (17)

Both conclusions retain weak separation and use the same actual C.

## 5. The transverse segment source

Under (16), the u_E support difference is strictly greater than

    F_1=1-d-t+kappa(1-c-.4s)+lambda(1-1.086s)
       =1-A_1 d-B_1 t,                               (18)
    A_1=2-c-s+.086s^2+.4cs,
    B_1=1-c+s+.086cs-.4s^2.

The coefficient A_1 is positive. At q0, its q derivative is positive
because the exact identity

    60A_1-91B_1
      =[15000-67413x+56060x^2-83587x^3-500x^4]
                                            /[250(1+x^2)^2]        (19)

has positive numerator on 0<=x<=1/5. Indeed the last three terms are
at least x^2[56060-83587/5-500/25]>=0, while
15000-67413x>=7587/5>0. Since t/d>=60/91, (19) also gives

    partial F_1/partial q=A_1t-B_1d>0

throughout q>=q0. Its minimum is therefore its q0 value, namely

    F_1(q0)=(10x+3)(750-3380x+2879x^2-3550x^3)
                                           /[13625(1+x^2)^2].     (20)

The cubic factor is positive on the whole interval: 750-3380x>=74>0,
and 2879-3550x>=2169>0. Thus (18) is positive. This excludes u_E under
the first actual segment source.

## 6. The oblique segment source

Under (17), the exact upper C support obeys

    upper_C(u_E)>=a(kappa+lambda)
                 +(kappa-lambda alpha/gamma)U-lambda D0/gamma.

The coefficient of U is negative, because the exact identity

    kappa gamma-lambda alpha=.086d-.26t<0            (21)

uses (7). Substitute U<=-a from the genuinely excluded O. After
subtracting L<=d+t-a, multiplying by gamma>0 and dropping a to 1
strictly, the margin is

    G=gamma(1-d-t)+lambda L0,
    L0=alpha+gamma-D0.                               (22)

Its a coefficient before this drop is gamma+lambda(alpha+gamma)>0.
Notice that no stronger, elbow-specific cap A<=-.26s has been used.

Put A_2=gamma-sL0 and B_2=gamma-cL0, so
G=gamma-dA_2-tB_2. On x<=1/5 one has s<=5/13<.4 and

    L0=.346c+.174s-.28236<=.13324<.14,
    A_2=gamma-sL0>.086c+.12s>0.                      (23)

At q0 its q derivative has the exact expression

    A_2(60/109)-B_2(91/109)
       =P(x)/[2725000(1+x^2)^2],                    (24)
    P(x)=1496169x^4+690380x^3-2618300x^2+197780x+78131.

Discard the first two nonnegative terms and use x^2<=x/5. The result is

    P(x)>=78131-325880x>=12955>0.

Together with A_2>0 and t/d>=60/91, this proves partial G/partial q>0
for every q>=q0. Finally its endpoint is

    G(q0)=[516420x^4-1963519x^3+272700x^2+132781x+2580]
                                            /[1362500(1+x^2)^2].  (25)

Its numerator is at least

    2580+[132781-1963519/25]x
       =2580+(1356006/25)x>0,

using x^3<=x/25 and discarding the nonnegative square and fourth-power
terms. Thus (22) is positive on the entire small-angle regime.

Both actual segment sources, and therefore the last actual C/E source,
are impossible. Sections 2-6 prove Theorem 1 for every allowed central
angle and every ordinary successor angle, including weak support
equalities and the rational regime boundary x=1/5.

## 7. The exact original consequence

Retain the complete original no-omission MPPM entrance and normalize the
genuinely inward owner as Q4. Suppose G0 and the physical center (2,2)
are omitted from Q4 and Q4 has positive canonical angle. The complete
actual C/Q5 ledger for the preceding successor theorem is in that
chapter's Section 8. In particular Q5 is the actual ordinary successor,
and the strict inward tip and both relevant halfpoints have independent
owner-preserving proofs.

The segment S in (1), after translation by (2,2), joins the actual Q8
marker (.914,2) to its actual strict F1=(1,2.26). Every point of that
closed segment is strict in Q8 and therefore excluded from the different
actual Q4. No point is assigned to a surrogate square.

If the opposite Q6 has its ordinary pair F9,G9, the actual right wall
square Q10 strictly owns (3,1.44), by the ordinary wall-reach map recorded
in C1092-MPPM-NONORDINARY-ISOLATION.md. More explicitly, use the retained
wall lemma in coordinates (xi,eta)=(4-x,4-y): its marker and outer anchor
are the actual right marker and G8 in Q10; its two exclusions are F9 in
Q6 and G6 (which is excluded from Q10 by the original no-omission
ordinary-central reduction). The standard target (1,2.56) becomes
(3,1.44). Thus the local point F=(1,-.56) is strict in actual Q10 and
excluded from Q5. Theorem 1 gives a contradiction.

Therefore a positive missing-center inward Q4 omitting G0 cannot have an
ordinary opposite Q6. With the independently proved elbow exclusion,
this leaves only the two-opposite-inward OIOI pattern for this branch.
The statement permits either ownership or omission of F0 by Q4. It
does not itself exclude the remaining OIOI geometry.
