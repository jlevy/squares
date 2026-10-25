# C1092 MPPM: a shallow positive forward owner before a steep positive missing owner receives its halfpoint

Every terminating decimal is an exact rational. Strict points belong to the actual open squares named in the proof. Face exits and separating supports are weak, so tangencies are retained. The local theorem uses two actual squares of common side a>1. Its final application retains the original no-omission OOOO setting and 1<a<=1.001.

## 1. A local two-square statement

Work in coordinates centered at (2,2). Let C have positive canonical frame

    u=(c,s), v=(-s,c), c>=s>0, c^2+s^2=1,

with lower faces U,V and upper faces A=U+a,H=V+a. Suppose C strictly owns

    M=(-.35,-.35), T=(-.26,0),

and

    U>=-c-.5s, H<=s,
    0<x=s/(1+c)<=3/10.                            (1)

Let E have positive canonical frame

    e=(d,t), f=(-t,d), d>=t>0, d^2+t^2=1,

with lower faces L,K and upper faces J=L+a,D=K+a. Suppose E strictly owns

    M_E=(.35,-.35), B0=(.26,-1),

and its simultaneous actual faces satisfy

    L>=-1.086t, J<=d-.56t, K>=-d-t,
    y=t/(1+d)>1/3.                               (2)

**Theorem 1.** C and E cannot have disjoint open interiors.

The steep angle in (2) implies

    d<.8, t>.6, d+t>1.4,

and (1) gives c>=91/109, s<=60/109. If p,q are the positive C,E angles, then q>p. Put

    alpha=cd+st=cos(q-p)>0,
    delta=ct-sd=sin(q-p)>0.

In particular

    u=alpha e-delta f,
    -v=-delta e-alpha f,
    -f=delta u-alpha v.                           (3)

## 2. Every possible actual separating normal

Direct a separating normal from C toward E. The strict markers give n_x>0. The strict pair T,B0 gives

    .52 n_x-n_y>0.                               (4)

The upward E normal e=(d,t) fails (4), since t/d>3/4>.52. Its other positive normal f has negative horizontal component. All remaining signed normals with nonpositive horizontal component fail the marker inequality. Thus the separating-axis theorem leaves only

    u=(c,s), -v=(s,-c), -f=(t,-d).                (5)

These are actual face normals of the two full squares. No extra direction or point-hull support is introduced.

## 3. C's upward normal

By (1),(2),

    A>=a-c-.5s, L<=d-.56t-a, D>=a-d-t.

Using (3),

    lower_E(u)=alpha L-delta D
       <=alpha(d-.56t-a)-delta(a-d-t).

The support gap A-lower_E(u) has positive a-coefficient 1+alpha+delta. Decreasing a to 1 leaves the strict lower bound

    F_u=1-P_u c-Q_u s,
    P_u=2-d-t+.44dt,
    Q_u=-.5-t+d+.44t^2.                           (6)

The complete range (2) gives

    P_u<2-1.4+.44/2=.82,
    Q_u<-.5-.6+.8+.44/2=-.08.

Consequently F_u>1-.82c>=.18>0. This excludes C's normal u throughout the two-angle domain.

## 4. C's downward normal

Here upper_C(-v)=a-H>=a-s. The lower E support is

    lower_E(-v)=-delta J-alpha D
       <=-delta(a-1.086t)-alpha(a-d-t).

Again the positive a-coefficient is 1+alpha+delta. At a=1 the strict lower support gap is

    F_v=1-s+alpha(1-d-t)+delta(1-1.086t).          (7)

The first parenthesis multiplying alpha is negative, and alpha<=1. The last parenthesis is positive because t<=1/sqrt(2) and 1.086<sqrt(2). Therefore

    F_v>=2-s-(d+t)>=2-60/109-sqrt(2)
        >753/21800>0.                            (8)

The last exact comparison uses sqrt(2)<283/200, whose square is immediate. Thus C's second possible normal also fails.

## 5. E's downward normal: the exact continuous endpoint

The exact upper support of C in the remaining direction is

    upper_C(-f)=delta A-alpha V
               =delta A+alpha(a-H).

Since lower_E(-f)=-D<=d+t-a, the positive a-coefficient 1+alpha+delta gives the strict lower gap

    F=1-d-t+delta(1-c-.5s)+alpha(1-s)
     =1-Qd-Pt,                                    (9)

where

    P=2-c-s+.5cs,
    Q=1-c+s-.5s^2.                               (10)

Both coefficients are positive: P>=2-sqrt(2)>0, and Q=s(1+x-s/2)>0. Moreover

    P-Q=1-2s+.5cs+.5s^2
        >1-2(5/9)+.5(5/9)^2=7/162>0,             (11)

because s<=60/109<5/9 and 1-2s+.5s^2 decreases on this interval.

For fixed p, the derivative of Q cos q+P sin q is

    -Q sin q+P cos q>=t(P-Q)>0,

using d>=t>0. Thus F has its minimum over the whole E interval at q=pi/4. At this endpoint,

    F>=1-(P+Q)/sqrt(2).

The coefficient sum and its exact p-derivative are

    P+Q=3-2c+.5s(c-s),
    d(P+Q)/dp=(2-c)s+.5(c^2-s^2)>0.               (12)

Hence its maximum over (1) is attained at x=3/10, where (c,s)=(91,60)/109. Its exact value is

    P+Q<=16735/11881<sqrt(2),

the strict radical inequality being equivalent to

    2(11881)^2-(16735)^2=2256097>0.               (13)

Combining (9)--(13) gives the positive uniform margin

    F>=1-16735/(11881 sqrt(2))>0.

Thus E's last actual normal is impossible. All sources in (5), both closed canonical upper endpoints and every weak support equality have been retained. This proves Theorem 1.

## 6. The actual ordinary-owner application

**Corollary 2.** Suppose actual ordinary C=Q4 is positive, owns its forward G3, and has half-angle at most 3/10. Suppose its actual ordinary successor E=Q5 is positive, omits its own forward F4, and has half-angle greater than 1/3. Then C strictly owns its outer halfpoint (1,1.5), and actual Q9 strictly owns its origin (2,1).

The C cap H<=s is the genuine positive-forward D theorem. If C's local outer halfpoint (-1,-.5) were missing, the full lower-face argument in Section 8 of C1092-MPPM-FLANKED-POSITIVE-HALFPOINT.md would give U>=-c-.5s. That argument uses only C's original marker,F0,G0,G3 and the actual foreign northwest marker; it neither requires a sign for Q7 nor assigns the missing halfpoint another owner.

For E, Theorem 1 of C1092-MPPM-POSITIVE-CROSSPOINT-SEEDS.md gives, in E's own southwest chart with positive frame,

    U_E>=-d-t, V_E>=.56t-d,
    A_E<=-.26d, H_E<=1.086t.

The stronger lower V_E comes from E's stated forward omission, with the genuine whole advanced Q10 bar. The simultaneous quarter-turn into the present chart sends its own first normal to f and its second normal to -e. Therefore its actual present faces satisfy

    K>=-d-t, J<=d-.56t, L>=-1.086t,

exactly (2). The additional cap D<=-.26d is also available but is not needed in this proof. The strict points M_E,B0 are Q5's marker and G5=(2.26,1). No right or bottom origin is used to obtain these faces.

Theorem 1 now contradicts the supposed missing C halfpoint. Its strict ownership in C supplies the excluded halfpoint for the actual paired-corner transfer, Theorem 7 of C1092-DIRECT-WALL-POINT.md, with Q0,Q9,b=.914,ell=1.6. The exact strict anchors are Q0(1,.914),(1,1) and Q9(2,.914),F2=(1.6,1), with their original real walls. The conclusion is Q9(2,1) strictly.

All statements rotate with the complete actual-owner table. The proof distinguishes both forward omissions explicitly and has no premise on the sign or membership of either remaining central square.
