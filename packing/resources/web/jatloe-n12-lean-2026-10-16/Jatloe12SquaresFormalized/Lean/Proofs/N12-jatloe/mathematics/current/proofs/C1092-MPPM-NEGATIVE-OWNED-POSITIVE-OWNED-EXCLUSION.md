# C1092 MPPM: a nonpositive retaining owner cannot precede a positive retaining owner

Every terminating decimal is an exact rational. Strict points belong to the named actual open squares. Exclusion and separating supports permit equality. The local obstruction uses only a common side a>1. Its application retains the original no-omission OOOO entrance and the original range 1<a<=1.001.

The two forward memberships in the title are genuine strict ownership assumptions. No backward-inner exclusion in the positive square is imposed or inferred.

## 1. A local obstruction with one actual wall segment

Use coordinates centered at (2,2). Let the actual square C have nonpositive canonical frame

    u=(c,-s), v=(s,c), c>=s>=0, c^2+s^2=1,

with lower faces U,V and upper faces A=U+a,H=V+a. Suppose C strictly owns

    M=(-.35,-.35), P0=(-1,-.26), G0=(-1,-.4),
    T=(-.26,0),

and excludes the two points

    D0=(-1,0), N=(-.35,.35).

Let its actual successor E have positive canonical frame

    e=(d,t), f=(-t,d), d>=t>0, d^2+t^2=1,

with lower faces L,K and upper faces J=L+a,Q=K+a. Suppose E strictly owns

    M_E=(.35,-.35), B0=(.26,-1), B1=(.4,-1),
    I=(0,-.26),

and excludes

    Q0=(1,-1), F=(1,-.56).

Retain one actual open square B, disjoint from C and E, which strictly owns the whole segment

    [-.56,0] x {-1}.                              (1)

In particular P=(0,-1) is excluded from E. Suppose finally that E's positive half-angle satisfies

    0<y=t/(1+d)<=7/32.                            (2)

**Theorem 1.** These actual squares cannot have disjoint open interiors.

The strict segment (1) is retained as one actual square's segment throughout the proof. It is not replaced by unrelated endpoints or by a container-wall approximation.

## 2. The negative square's genuine faces and clearance

Sections 2--3 of C1092-MPPM-NEGATIVE-FORWARD-POSITIVE-H.md apply to exactly the present C,E,B. Their local hypotheses do not include the potentially reassigned point (0,.26), nor any backward-inner exclusion in E. The actual strict I in E gives C's necessary upper-u cap. For clarity the resulting simultaneous bounds are

    U>=-c, A<=.26s, H<=.35(c-s),
    0<x=s/(1+c)<13/50, c>.87, s<.49.             (3)

Here D0 is lower u, I is upper u, and the actual foreign marker N is upper v. The opposed u faces give a<=c+.26s, whose exact half-angle identity excludes x=0 and gives x<13/50. At x=0, strict P0 also directly contradicts the lower face at D0.

The same whole-bar argument gives

    V>=-c-.56s,
    Z_y>-1,

where Z=A u+V v is the actual lowest closure vertex of C. Its abscissa is strictly greater than -.56. If Z_y<=-1, the cap A<=.26s gives Z_x<=0, and the segment to the strict T meets the actual strict segment (1). Equality Z_y=-1 is also impossible: a closure point of C inside the open B would force the interiors to intersect.

Writing the actual center of C as (X_C,Y_C), the derived lower faces and clearance give

    Y_C>Y_*=-1+(c+s)/2,
    X_C>X_*=-1+[1/2+sY_*]/c.                     (4)

These are simultaneous bounds on the same actual C. The proof does not replace its upper transverse face by a cap from an auxiliary whose owner may have changed.

## 3. The positive successor's two necessary faces

The strict P=(0,-1) in B is outside E. Its upper e-band follows from B0, and its two f-bands follow from B0,I. Consequently it is a lower-e exit, so

    L>=-t.                                       (5)

At the actual excluded corner Q0=(1,-1), the lower e-band and upper f-band are strict from B1. The only possible exits are upper e or lower f. An upper-e exit J<=d-t would combine with (5) to give a<=d<=1. Therefore Q0 is lower f:

    K>=-d-t.                                     (6)

The angle bound (2) gives

    d>=975/1073, t<=448/1073<.42,
    t/d<=448/975<11/15.                           (7)

At F=(1,-.56), the lower e-band follows from B1 with increment .6d+.44t>0. Its lower f-band follows from B1 with increment .44d-.6t>0 by (7). Its upper f-band follows from M_E with increment .21d+.65t>0. The genuine F exclusion therefore forces upper e:

    J<=d-.56t.                                   (8)

This argument uses the actual whole-square bands and the actual strict anchors; it does not infer an unproved face from the distance to a strict point.

## 4. The complete separating-normal cover

Orient any separating normal from C toward E. The strict markers force n_x>0, while the strict pair T,I forces n_x-n_y>0. The separating-axis theorem therefore leaves only the actual sources

    u=(c,-s), e=(d,t), -f=(t,-d).                 (9)

Set

    k=cd-st>0, ell=ct+sd>0.

The positivity of k follows from c>s under (3) and d>=t. The exact frame decompositions are

    u=k e-ell f,
    e=k u+ell v,
    -f=ell u-k v.                                (10)

Every support comparison below keeps the same actual side a until its coefficient is known to be positive.

## 5. E's upward source fails by the actual clearance

By (4) and a>1,

    upper_C(e)>dX_*+tY_*+(k+ell)/2
               =(1-c)(d kappa-t),
    kappa=(1-x)/(1+x)>0.                          (11)

The displayed equality is the exact center/support identity from the negative predecessor proof. The strict I in E gives lower_E(e)<-.26t. Thus the actual support excess is strictly greater than

    (1-c)d kappa+t(c-.74)>0,                      (12)

using 0<c<1 and c>.87. This excludes e. In fact this source needs no upper bound on E's angle.

## 6. C's own source: a single exact norm certificate

From (6),(8),

    lower_E(u)=kL-ell Q
       <=k(d-.56t-a)-ell(a-d-t).

Since upper_C(u)=A>=a-c, their excess has positive a-coefficient 1+k+ell. At a=1 its exact value is

    F_u=1-P_u c-Q_u s,
    P_u=2-d-t+.44dt,
    Q_u=1-d+t-.44t^2.                             (13)

Writing y=t/(1+d), direct substitution gives

    1-P_u^2-Q_u^2
      =-4y[1875y^3-1450y^2+1446y-350]
         /[625(1+y^2)^2].                         (14)

The bracket is strictly negative throughout 0<y<=7/32. Indeed

    1875y^3-1450y^2+1446y-350
       <=1875(7/32)^3+1446(7/32)-350
       =-460747/32768<0.

Hence P_u^2+Q_u^2<1. Cauchy's inequality gives P_u c+Q_u s<1, so F_u>0. The actual side a>1 further increases the support excess. Thus u cannot separate.

## 7. E's downward source: retain the actual marker cap

The genuine bounds in (3) and (6) give

    upper_C(-f)=ell A-kV
       >=ell(a-c)+k[a-.35(c-s)],
    lower_E(-f)=-Q<=d+t-a.

Their excess has positive a-coefficient 1+k+ell. Replacing a by 1 leaves

    F_f=1-P_f d-Q_f t,
    P_f=1-c-s+.65cs+.35c^2,
    Q_f=2-c+s-.35cs-.65s^2.                       (15)

On the entire predecessor domain (3), P_f<.4. To verify this, use s(.65c-1)<=0 and observe that 1-c+.35c^2 decreases for .87<c<=1. Its value at c=.87 is .394915<.4.

For the other coefficient,

    Q_f<1.13+.6955s-.65s^2
        <=1052837/800000<1.32.                   (16)

The middle bound is the exact maximum of the displayed concave quadratic. Combining (7),(15),(16),

    P_f d+Q_f t<.4+1.32(.42)=1193/1250<1.

Thus the support excess in (15) is strictly greater than 57/1250. This excludes -f. It uses only the actual N-marker cap, with no cap at a potentially reassigned inner point.

All sources in (9) have failed. The proof retains every weak support equality and all canonical endpoints allowed by (2),(3). Theorem 1 follows.

## 8. Literal application to a retaining negative-to-positive edge

**Corollary 2.** In the original no-omission OOOO family, a nonpositive ordinary central which owns its forward point cannot be followed by a positive ordinary central which also owns its forward point.

Normalize these actual owners to C=Q4 and E=Q5. Their stipulated forward points are G3=(1.74,2) and F4=(2,1.74). No condition is imposed on E's backward G6=(2.26,2), or on the forward memberships and signs of Q6,Q7.

The following is the complete additional source ledger for Theorem 1.

| Local datum | Literal original source |
|---|---|
| C's M,P0,G0,T | Q4 marker, F0, G0, and its stipulated strict G3 |
| C excludes D0=(-1,0) | Theorem 1 of C1092-MPPM-NEGATIVE-FORWARD-POSITIVE-H.md, valid even if actual Q8 omits (1,2) |
| C excludes N=(-.35,.35) | The strict northwest marker in actual Q7 |
| E's M_E,B0,B1,I | Q5 marker, G5, F6, and its stipulated strict F4 |
| E excludes Q0=(1,-1) | The actual paired southeast corner Q1 strictly owns (3,1) |
| E excludes F=(1,-.56) | The actual Q10 strictly owns its ordinary advance (3,1.44) |
| The whole segment (1) in B | Actual Q9 owns (1.44,1) and (2,1), hence their entire strict segment |

The Q9 origin comes from the unconditional nonpositive ordinary halfpoint theorem for C. Its far point (1.44,1) is the ordinary Q9 advance whose genuine source is E's strict G5. The Q10 far point (3,1.44) is its ordinary advance whose genuine source is actual Q6's ordinary F9. These are the no-omission OOOO sources and require no origin or forward membership in Q6 or Q7.

Finally, Corollary 2 of C1092-MPPM-NEGATIVE-OWNED-POSITIVE-CEILING.md, rotated to this actual C,E pair, gives

    0<y<11/100<7/32.

Its genuine preceding-origin exclusion is exactly the one in the table, and its actual clearance segment is the same Q9 segment used here. Thus it supplies (2) without any new assumed angle cutoff. Theorem 1 now contradicts actual disjointness and proves Corollary 2.

Simultaneous quarter-turns R(x,y)=(4-y,x) give the other three edges with every actual owner retained. This corollary excludes the stated retaining-to-retaining sign transition. It does not assign an owner to a missing forward point and does not yet exclude a positive missing-forward recipient.
