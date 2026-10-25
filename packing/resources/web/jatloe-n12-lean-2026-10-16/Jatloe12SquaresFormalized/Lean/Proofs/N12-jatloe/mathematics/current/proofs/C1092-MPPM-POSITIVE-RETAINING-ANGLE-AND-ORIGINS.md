# C1092 MPPM: a positive retaining successor is shallow when its next crosspoint is foreign

All terminating decimals are exact rational numbers. Strict ownership refers to the interior of an actual open square. Exclusion and separating supports permit equality. The local theorem uses only common side a>1; its actual applications retain the original no-omission OOOO entrance and 1<a<=1.001.

## 1. A local steep-recipient obstruction

Let C and E have physical canonical frames

    u=(c,s), v=(-s,c), e=(d,t), f=(-t,d),
    c=cos p, s=sin p, d=cos q, t=sin q,
    0<=p,q<=pi/4.

Write C's upper u,v faces as A,K. Write E's lower e face as -K_E and its upper f face as A_E. Thus E's own-sector upper faces, after the actual quarter turn, are A_E,K_E. Suppose the two squares strictly own the respective markers

    M_C=(-.35,-.35), M_E=(.35,-.35),

and their simultaneous faces satisfy

    a-c-s<=A<=0, a+.4s-c<=K<=s,
    A_E>-.26d, A_E<=0, 0<K_E<=t.                (1)

**Theorem 1.** The additional pair of conditions

    q>=q0=2 atan(1/3), K_E>=a-.5d              (2)

is incompatible with disjoint open interiors.

The endpoint q=q0 is included. Put

    kappa=cos(q-p)>0, sigma=sin(q-p).

The strict marker displacement M_E-M_C=(.7,0) forces the horizontal component of every directed separator from C toward E to be positive. The separating-axis theorem for the two actual squares therefore leaves exactly u,e,-v,-f, apart from harmless duplicate axes at an endpoint. Theorem 1 of C1092-MPPM-POSITIVE-RETAINING-FIRST-NORMALS.md excludes -v and -f under the subset of (1) consisting of A>=a-c-s, A<=0, K<=s, A_E>-.26d and 0<K_E<=t. That theorem includes both relative angle orders and all weak face equalities.

We exclude the two remaining actual sources without replacing either square's faces. Their exact necessary support inequalities are

    u: A+kappa K_E+sigma A_E<=a min(sigma,0),   (3)
    e: K_E+kappa A+sigma K<=a min(sigma,0).     (4)

Indeed u=kappa e-sigma f. For sigma>=0 its lower E support is -kappa K_E-sigma A_E, while for sigma<=0 it is -kappa K_E-sigma(A_E-a). Also e=kappa u+sigma v, so its upper C support is kappa A+sigma K-a min(sigma,0). These give (3),(4) with their actual signed faces.

Throughout (2),

    1/sqrt(2)<=d<=4/5, 3/5<=t<=1/sqrt(2).

The function 1.5 cos q+sin q decreases on [q0,pi/4], because its derivative is -1.5 sin q+cos q<=-.1<0. In particular

    1.5d+t<=9/5.                                (5)

## 2. The current first normal u

### 2.1. q>=p

Here sigma>=0. By (1),(2), the left side of (3) is at least

    a(1+kappa)-(c+s)-.5kappa d-.26sigma d,

with a strict improvement when sigma>0 from A_E>-.26d. Its coefficient 1+kappa of a is positive, so a>1 gives the strict lower bound

    F=1+kappa-(c+s)-.5kappa d-.26sigma d
     =1-kappa P-sigma Q,
    P=1.5d+t-1, Q=t-.74d.                       (6)

The identity uses c=d kappa+t sigma and s=t kappa-d sigma. On [q0,pi/4], (5) gives 0<P<=.8. Moreover Q increases, its value at q0 is .008, and its value at pi/4 is .26/sqrt(2)<.184. Consequently

    P^2+Q^2<(.8)^2+(.184)^2=.673856<1.

Cauchy's inequality and kappa^2+sigma^2=1 show F>0. The right side of (3) is zero in this order, a contradiction.

### 2.2. q<=p

Now sigma<=0, so A_E<=0 gives sigma A_E>=0. The difference between the two sides required in (3) is bounded below by

    a(1+kappa-sigma)-(c+s)-.5kappa d.

Its positive a coefficient gives the strict lower bound

    F=1-(c+s)+kappa(1-.5d)-sigma.                (7)

Here both p and q lie in [q0,pi/4]. Thus

    kappa>=cos(pi/4-q0)=7sqrt(2)/10>.98,
    c+s<=sqrt(2)<1.415, 1-.5d>=.6, -sigma>=0.

It follows that F>1-1.415+.98(.6)=.173>0. This contradicts (3), including p=q.

## 3. The successor first normal e

### 3.1. q>=p

Use the lower bounds for all three faces K_E,A,K in (4). Its left side is at least

    a(1+kappa+sigma)-.5d-kappa(c+s)+sigma(.4s-c).

The coefficient 1+kappa+sigma is positive. After using a>1, the exact remaining expression is

    F=1+kappa+sigma-1.5d-t-.6s sigma
     =1-1.5d-t+kappa+sigma(1-.6s).               (8)

Set z=tan((q-p)/2). The closed relative-angle range gives 0<=z<=sqrt(2)-1<.415, and

    1-kappa=sigma z.

Since s<.71,

    kappa+sigma(1-.6s)
      =1+sigma(1-z-.6s)>=1,

where 1-z-.6s>1-.415-.426=.159. Therefore (5) gives F>=2-1.5d-t>=.2>0, contrary to (4).

### 3.2. q<=p

Here sigma<=0, so the upper cap K<=s gives sigma K>=sigma s. Subtracting the right side of (4), the support difference is at least

    a(1+kappa-sigma)-.5d-kappa(c+s)+sigma s.

Its a coefficient is positive. At a=1 the exact expression simplifies to

    F=1-1.5d+kappa(1-s)-sigma,                   (9)

using d=kappa c-sigma s. Both angles again lie in [q0,pi/4], so d<=.8, kappa>.98, 1-s>.29 and -sigma>=0. Hence

    F>-.2+.98(.29)=421/5000>0.

This excludes the final directed actual normal. Every possible separator has now failed, proving Theorem 1. No angle interval was sampled, and equality of any excluded point with a face is retained in the argument. ∎

## 4. The literal positive-recipient consequence

**Corollary 2.** In the retained OOOO entrance, suppose a positive central E retains its own forward point, its actual predecessor C is positive, and the next actual central strictly owns its crosspoint. Then E has

    tan(q)<13/25, q-half-angle<1/4,
    A_E<=-.5t,                                   (10)

strictly owns its own outer halfpoint, and supplies the next actual wall origin through its actual paired corner.

For the representative C=Q4, E=Q5, translation by (-2,-2) gives the physical frames and strict markers in Section 1. The universal positive theorem C1092-MPPM-UNIVERSAL-POSITIVE-CROSSPOINTS.md gives the simultaneous C faces in (1), and the corresponding own-sector faces of E give A_E<=0 and K_E<=t. E's genuine strict forward F4=(2,1.74), whose own-sector coordinates are (-.26,0), gives A_E>-.26d and K_E>.26t>0. The change of own-sector basis to the physical chart is (e_E,f_E)=(f,-e), so K_E is exactly minus the physical lower e face, as used above.

The next crosspoint is now a genuine excluded point in E. The local face proof of Theorem 1 in C1092-MPPM-POSITIVE-CROSSPOINT-ANGLE-DICHOTOMY.md therefore applies without its introductory all-positive restriction: that proof uses only E's strict ordinary points and forward point, its four actual faces, and this excluded crosspoint. It gives either its shallow alternative (10), or

    q-half-angle>1/3, K_E>=a-.5d.

The latter satisfies (2) and is excluded by Theorem 1. The shallow alternative thus holds. Since the slope at half-angle 1/4 is 8/15>13/25, strict monotonicity of 2x/(1-x^2) gives the sharper half-angle bound in (10). The same reviewed four-band argument supplies E's strict outer halfpoint; the genuine paired-corner theorem then supplies its next actual wall origin.

Every original owner in this application is displayed here:

| Positive predecessor C | Positive retaining recipient E | Required crosspoint in the next actual owner | E's strict outer halfpoint | Actual wall origin obtained |
|---|---|---|---|---|
| Q4 | Q5 | Q6(2.5,2) | Q5(2.5,1) | Q10(3,2) |
| Q5 | Q6 | Q7(2,2.5) | Q6(3,2.5) | Q11(2,3) |
| Q6 | Q7 | Q4(1.5,2) | Q7(1.5,3) | Q8(1,2) |
| Q7 | Q4 | Q5(2,1.5) | Q4(1,1.5) | Q9(2,1) |

Each row is the simultaneous actual quarter turn R(x,y)=(4-y,x), including the relevant paired corner and real container walls. In particular the required next crosspoint is supplied if that next central is positive, by the universal positive-crosspoint theorem. It is also supplied if that next central is nonpositive and retains its forward point, by the universal retaining-crosspoint lemma. No crosspoint is presumed for a nonpositive missing-forward next owner.

## 5. All actual origins in the all-positive cycle

**Corollary 3.** Every still-possible all-positive OOOO configuration has all four actual wall origins. Every retaining central satisfies (10); every central has the simultaneous strengthened lower-v bound

    V>=.56s-c.                                   (11)

Indeed all four crosspoints are genuine by the universal positive theorem. Every retaining recipient therefore satisfies Corollary 2, and strictly owns its own outer halfpoint. Every missing-forward central has its outer halfpoint by the ordinary-marker halfpoint theorem. The four literal paired-corner transfers put (2,1),(3,2),(2,3),(1,2) in Q9,Q10,Q11,Q8 respectively.

For (11), a missing-forward central already has that bound in its reviewed whole-bar profile. For a retaining central normalize to Q4 and retain A<=-.5s from (10). The point F=(-.56,-1), or original (1.44,1), lies strictly in the same actual bottom owner Q9 by its established ordinary advance from G5=(2.26,1). It is excluded from C. Its lower-u band is strict because

    u(F)-U>=a-.56c-.5s>0,

using .56c+.5s<=sqrt(.56^2+.5^2)=sqrt(.5636)<1. Its upper-u band is strict by C's marker, since u(M)-u(F)=.21c+.65s>0. Its upper-v band is strict by P=(-1,-.26), since v(P)-v(F)=.44s+.74c>0. Thus its only exit is lower v, giving exactly V>=v(F)=.56s-c. The same actual advance rotates with Q9 through every row.

The all-positive remainder consequently has strict X and outer halfpoint at every central, all four genuine boundary origins, and the actual simultaneous profiles

    U>=-c-s, V>=.56s-c, K<=s,
    A<=-.26c for a missing forward,
    A<=-.5s and tan(p)<13/25 for a retained forward.

These are consequences of the same actual twelve-square configuration. This chapter does not yet assert a contradiction for the resulting all-origin cycle, nor does it assign an omitted auxiliary to a neighboring owner.
