# C1092 MPPM: a positive missing-center inward square and the actual preceding wall origin

All terminating decimals are exact rationals. Every square is an actual open
square of common side a>1. Owned points are strict; excluded points and
separating supports permit equality. No wall-center, side upper bound or
orientation catalogue is used in the local theorem.

## 1. A local two-square theorem

**Theorem 1.** Retain all local hypotheses of
C1092-MPPM-POSITIVE-MISSING-INWARD-SUCCESSOR.md, Theorem1, for C and its
actual ordinary successor E. Suppose additionally that C excludes

    P=(-1,0).

Then the actual C and E cannot have disjoint interiors.

For clarity, the strict C points of that theorem are

    M_C=(-.35,-.35), I=(0,-.26), J=(-.26,0),
    X=(-.5,0), T=(-.01,-.54),

its exclusions are O=(0,0), G0=(-1,-.4), F2=(-.4,-1), N=(-.35,.35),
and it has a nonnegative canonical frame. The strict E points are

    M_E=(.35,-.35), B0=(.26,-1), B1=(.4,-1), Y_E=(.5,-1),

with excluded G_E=(1,-.4), K0=(1,-1), R0=(0,-1.086).
The new point P may be an ordinary exclusion in the local theorem; the
application below supplies the actual preceding wall owner.

The reviewed predecessor theorem proves that C is strictly positive, E
strictly negative, and that Y=(0,-.5) is strict in C. Write

    C: u=(c,s), v=(-s,c), lower faces U,V, upper faces A=U+a,H=V+a;
    E: u_E=(d,-t), v_E=(t,d), lower faces L,W, upper faces J_E,K_E.

Here c>=s>0, d>=t>0 and both frames are orthonormal. The simultaneous
C face profile is

    U>=-c-.4s, A>=a-c-.4s, A<=0,
    V>=.4s-c, H<=.35(c+s).                           (1)

In particular

    0<x:=s/(1+c)<2/5,                               (2)

because 1<a<=c+.4s. This gives p=arctan(s/c)<2 arctan(2/5)<pi/4.

The actual negative E faces are

    L>=.5t, J_E<=d+t,
    W>=-1.086d, K_E<=t-.4d.                        (3)

These are the ordinary face argument reproduced in Section1 of
C1092-MPPM-POSITIVE-MISSING-INWARD-FAR-ENDING.md before its additional
far-point hypothesis is used. They require exactly the above E anchors,
its three exclusions and the strict point Y in the different actual C.
For completeness, Y is lower u in E. Then G_E has both lower bands from
M_E,B1, and its upper u-band is strict because

    d+.4t< a+.5t<=J_E.

Thus G_E is upper v. The point K0 has its lower u and upper v-bands from
B1,M_E; a lower-v exit would give width at most .6d. Hence K0 is upper u.
Finally R0 has both upper bands from B0,B1; a lower-u exit would give
width at most d-.086t<=1. It is lower v. This proves all of (3) using
the actual points, with no ordinary-opposite assumption.

The new exclusion P yields the additional central cap

    H<=s.                                          (4)

Indeed its upper u-band follows from M_C, with increment
.65c-.35s>=.30c>0. Its lower v-band follows from strict X, with increment
s/2>0. The only possible exits are therefore lower u and upper v.
A lower-u exit U>=-c, together with A<=0, would give a<=c<=1. It is
impossible, proving (4). This is an opposed-face argument, not an
inference from the distance to a strict point.

Put

    kappa=cd-st=cos(p+q)>0,
    lambda=ct+sd=sin(p+q)>0,
    q=arctan(t/d).

The strict positivity of kappa follows from (2) and q<=pi/4. The strict
marker difference between C and E forces every C-to-E separating normal
to have positive x component. The complete remaining actual face-normal
list is

    u, -v, u_E, v_E.                                (5)

The proof below defeats all four, even if an individual normal is
ineligible in a sharper strict cone.

## 2. Three sources fail on the full angle range

### 2.1. The C source u

Using (1),(3), the difference upper_C(u)-lower_E(u) is strictly greater
than

    F_u=1-c-.4s+kappa(1-d-t)+lambda(1-t+.4d)
       =1-c A_q+s B_q,
    A_q=2-d-t+.6dt,
    B_q=d-t+.6t^2.                                  (6)

The coefficient of a replaced by1 is 1+kappa+lambda>0. Also

    0<A_q<1, B_q>0.

For the upper bound on A_q, use

    d+t-1=2dt/(1+d+t)>.8dt>.6dt;

the lower bound follows from A_q>=2-sqrt(2)>0. The sign of B_q follows
from d>=t>0. Consequently (6) is strictly positive for every c,s in
(1). This source cannot separate.

### 2.2. The C source -v

Use H<=.35(c+s), L<=d+t-a and K_E=W+a>=a-1.086d. The strict lower
support margin is

    F_{-v}=1-.35(c+s)+kappa(1-1.086d)
                           +lambda(1-d-t).         (7)

Here kappa(1-1.086d)>=-.086, whether the factor in parentheses is
positive or negative. Since lambda<=1 and 1-d-t<0, we also have
lambda(1-d-t)>=1-d-t. Therefore

    F_{-v}>=1.914-1.35sqrt(2)>33/7000>0,             (8)

where sqrt(2)<99/70 gives the displayed rational reserve. This argument
allows every canonical E angle and uses the actual bottom-marker face
W>=-1.086d, rather than a discarded position variable.

### 2.3. The E source v_E

The lower face in (1) gives H=V+a>=a+.4s-c. With A>=a-c-.4s and
W<=t-.4d-a, the strict lower margin is

    F_{v_E}=1+(kappa+lambda)(1-c)
                    +.4(kappa-lambda)s-t+.4d.

As |kappa-lambda|<=1 and t<=d, this is at least

    1-.4s-.6d>=.4-.2sqrt(2)>0.                    (9)

Thus this source fails as well. All three displayed margins came from
strictly dropping a>1 with positive coefficient.

## 3. The final E source u_E: two continuous central ranges

The exact upper C support is kappa A-lambda V. Subtracting
L<=d+t-a and using (1), any chosen upper cap H<=H_* gives the strict
lower margin

    F=1-d-t+kappa(1-c-.4s)+lambda(1-H_*).           (10)

Only this source needs the new origin cap (4).

### 3.1. The range 0<x<=1/5

Choose H_*=s in (10). Direct expansion gives

    F=1-d A_1-t B_1,
    A_1=2-c-s+.4cs,
    B_1=1-c+s-.4s^2.

The exact single-variable identity is

    25(1+x^2)^2(1-A_1^2-B_1^2)
      =-4x(75x^3-55x^2+59x-15).                   (11)

For 0<x<=1/5, the cubic factor is at most

    75/125+59/5-15=-13/5<0,

where the negative square term was discarded. Therefore
A_1^2+B_1^2<1. Since (d,t) is a unit vector, Cauchy's inequality gives
dA_1+tB_1<1, so (10) is strictly positive.

### 3.2. The range 1/5<=x<2/5

Use the marker cap H_*=.35(c+s). The margin (10) expands as

    F=1-d B_2-t A_2,
    A_2=1.35-c+s-.75s^2-.65cs,
    B_2=2-c-s-.65s^2+.75cs.

The exact identity already used in the reviewed far-point ending is

    400(1+x^2)^2(1-A_2^2-B_2^2)
      =-[5409x^4-2196x^3-366x^2-204x+49].          (12)

For x<2/5, the coefficient 5409x-2196 is less than -162/5. Thus the
bracket in (12) is at most

    -366x^2-204x+49<=-161/25<0

on x>=1/5. Again the coefficient vector has norm less than1, and (10)
is strictly positive for every actual unit (d,t).

The intervals in Sections3.1--3.2 cover the entire domain (2), including
their common endpoint. All four actual normals in (5) are now
impossible. This proves Theorem1, with every weak face or separating
equality retained. ∎

## 4. Literal OIOI entrance: the left origin has an actual owner

**Corollary 2.** In the original no-omission MPPM family, suppose Q4
owns its inward pair F4,G3 and omits G0. Suppose Q4 has positive
canonical angle, and the opposite Q6 owns its inward pair F5,G6.
Then Q4 strictly owns O=(2,2).

**Proof.** Suppose O excluded. The full actual C=Q4,E=Q5 entrance for
the predecessor theorem is recorded in Section8 of
C1092-MPPM-POSITIVE-MISSING-INWARD-SUCCESSOR.md. It supplies the strict
tip (1.99,1.46), the strict crosspoint (1.5,2), the ordinary successor
F6,G5 in Q5, its strict halfpoint (2.5,1), and every marker/auxiliary
exclusion used in Theorem1. The tip's outer exclusion is exactly the
hypothesized omission G0. No opposite-central hypothesis was used for
any of those facts.

It remains only to supply P=(-1,0), or original (1,2), as an actual
foreign point. The inward-neighbor theorem also gives F3,G4 in actual
Q7. Since F5 is strict in the actual opposite Q6, it is excluded from
Q7. Apply ORDINARY-MARKER-HALFPOINT.md under the simultaneous transpose
(x,y)->(y,x). Its exact source ledger is

| Standard ordinary-point datum | Transposed original point and actual source |
|---|---|
| Marker (2.35,1.65) | NW marker (1.65,2.35) in Q7 |
| Strict (3,1.74) | G4=(1.74,3) in Q7 |
| Strict (3,1.6) | F3=(1.6,3) in Q7 |
| Excluded (2.26,2) | F5=(2,2.26) in the opposite actual Q6 |
| Excluded (3.086,2) | Top marker (2,3.086) in Q11 |
| Excluded (3,1) | Paired NW inner point (1,3) in Q3 |
| Excluded (2.26,1) | F1=(1,2.26) in actual Q8 |
| Strict conclusion (3,1.5) | (1.5,3) in actual Q7 |

Now use the actual paired-corner transfer, Theorem7 of
C1092-DIRECT-WALL-POINT.md, under R^3(x,y)=(y,4-x). The original
bottom-chart roles become

| Transfer datum | Actual NW/left datum |
|---|---|
| K owns (1,.914),(1,1) | Q3 owns (.914,3),(1,3) |
| K excludes (1,1.5) | (1.5,3) is strict in the different actual Q7 |
| B owns (2,.914),(1.6,1) | Q8 owns (.914,2),(1,2.4) |
| Real corner and bottom walls | Actual NW corner walls and actual left wall |
| Strict conclusion (2,1) | (1,2) is strict in the actual Q8 |

The constants are b=.914 and ell=1.6. All four actual owners in these
two transfers are distinct, and no lower hull from another square is
assigned to Q3 or Q8. We have therefore proved the additional exclusion
P from C=Q4 literally. Theorem1 is a contradiction. ∎

This corollary does not require a sign or center-point premise on the
opposite inward Q6. Together with the previously reviewed ordinary-
opposite far-point ending, it removes every positive, missing-center,
G0-omitted genuinely inward alternative after the ordinary/inward/elbow
ownership reduction. It also applies when the opposite owner has both
an inward and an ordinary pair, since its proof uses actual F5 ownership
rather than a disjoint label classification.
