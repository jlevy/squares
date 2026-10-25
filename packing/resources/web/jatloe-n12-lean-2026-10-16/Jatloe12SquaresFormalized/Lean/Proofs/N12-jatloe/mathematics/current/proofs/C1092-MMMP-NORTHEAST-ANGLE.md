# C1092 MMMP: the northeast square has strictly positive angle

All terminating decimals are exact rationals. Owned points belong to the interiors of their stated actual squares. Exclusions may be on a face, and separation of closure supports may be equality. The common side satisfies a>1; no upper bound on a is used below.

## 1. A local actual-pair theorem

**Theorem 1.** Let C and B be disjoint open squares of the same side a>1. Suppose C strictly owns

    O=(0,0), A=(-.5,0), D=(0,-.5), M_C=(-.35,-.35),

and excludes

    G=(.35,-.35), M=(-.35,.35), F=(-.39,-1).

Suppose B strictly owns

    M=(-.35,.35), H1=(-1,.26), H2=(-1,.4),

and excludes

    I=(-.39,0), J=(-.39,1), W=(-1.086,0), K=(-1,1),
    A=(-.5,0).

Then B has no nonpositive canonical frame. Equivalently, its canonical angle is strictly positive; the square with diagonal face directions is also excluded because it has a nonpositive canonical representative.

No wall, center sign, or origin in a boundary square is a premise. In particular, the point (-1,0), which would correspond to the top origin in the MMMP application, is not assumed to be foreign to B.

Write R_Q(n) and L_Q(n) for the full maximum and minimum closure supports of an actual square Q. Disjoint interiors imply separation on a face-normal axis of one of the two actual squares. We retain the whole side-a square in every support computation.

## 2. Three forced upper faces and the paired-corner alternative

Suppose that B has the nonpositive frame

    u_B=(b,-t), v_B=(t,b), b>=t>=0, b^2+t^2=1,

and lower face coordinates p,q. At J its lower u-band follows from H2, its upper u-band from M, and its lower v-band from M. The three positive projection increments are

    u_B(J)-u_B(H2)=.61b-.6t>=.01b>0,
    u_B(M)-u_B(J)=.04b+.65t>0,
    v_B(J)-v_B(M)=.65b-.04t>=.61b>0.

Thus J is upper v. At I, the lower u-band follows from H2 and the upper v-band from M, since

    u_B(I)-u_B(H2)=.61b+.4t>0,
    v_B(M)-v_B(I)=.35b+.04t>0.

It is upper u or lower v. Its lower-v alternative, opposed to J's upper v-face, would give a<=b<=1. Consequently

    p+a<=-.39b, q+a<=b-.39t.                         (1)

Strict M gives -.35(b+t)<p+a<=-.39b, so t>0.

At W both upper bands are strict by M and H2, respectively:

    u_B(M)-u_B(W)=.736b-.35t>=.386b>0,
    v_B(H2)-v_B(W)=.4b+.086t>0.

Thus W is lower u or lower v. A lower-u W, opposed to I in (1), would give a<=.696b<1. Hence

    q>=-1.086t.                                      (2)

The corner point K has its upper u-band and lower v-band from H2, so it can only be lower u or upper v. Suppose it were upper v. Then (2) would give

    1<a<=b+.086t.

With z=t/(1+b)>0 and 1-b=zt, this implies z<.086 and t=2z/(1+z^2)<.172. Since b>=1/sqrt(2)>.7, the point A would now have all four strict bands in B:

* Its lower u-band follows from p<=-.39b-a, because u_B(A)-p>1-.11b>0.
* Its upper u-band follows from M, because u_B(M)-u_B(A)=.15b-.35t>.105-.0602>0.
* Its upper v-band follows from M, because v_B(M)=.35(b-t)>0>-.5t=v_B(A).
* Its lower v-band follows from q<=b-t-a<-t, while v_B(A)=-.5t>-t.

But A is excluded from B. The upper-v corner alternative is impossible. Therefore the genuine K exclusion forces

    p>=-b-t.                                         (3)

Equations (1),(3), rather than an unproved point at (-1,0), are the complete boundary face information used below.

They give 1<a<=t+.61b. Setting h=t/(1+b), the exact identity

    (1+h^2)(t+.61b-1)=(1-h)(161h-39)/100

implies h>39/161. Thus

    t>6279/13721>.45, b<12200/13721<.9.             (4)

We also retain b>7/10, t<5/7, and 1<b+t<10/7. Each follows from the canonical interval, t>0, and sqrt(2)<10/7.

## 3. The exact support convention and normal cover

For lower face coordinates z1,z2 and orthonormal face normals e1,e2, write n=alpha e1+beta e2. The exact full supports are

    L_Q(n)=alpha z1+beta z2
                 +a min(alpha,0)+a min(beta,0),
    R_Q(n)=L_Q(n)+a(|alpha|+|beta|).                 (5)

Choose either canonical sign for C and use u,v for its upper face coordinates; its lower coordinates are u-a,v-a. Strict O gives u,v>0.

In both signs, neither order on C's longitudinal u-axis is possible. The marker M in B is opposite the foreign G: its u projection is the negative of G's. The appropriate upper-face bound for C derived below gives

    u-a<u_Bmarker_on_C_axis<0<u.

Thus the strict point M rules out B-before-C and O rules out C-before-B on that axis. Likewise C-before-B on B's longitudinal axis is excluded by O and H2, whose B longitudinal projection is -b-.4t<0.

For either upward transverse axis, B-before-C is excluded by M_C and M: their x-coordinates are equal and their y-coordinates differ by .7. Finally C-before-B on B's transverse axis is impossible because R_C(v_B)>0 by O, while (1) gives

    q<=b-.39t-a<0.

After these strict point comparisons, the only possible separators are

    p+a<=L_C(u_B),                                    (L)
    v<=L_B(v_C).                                     (V)

The computations below check both for each entire canonical sign of C. No direction is inferred from a hull substituted for an actual square.

## 4. A nonpositive C is impossible

Take C's frame to be

    u_C=(d,-r), v_C=(r,d), d>=r>=0, d^2+r^2=1.

At G its lower u-band follows from O, its upper v-band from O, and its lower v-band from D. Hence G is upper u, and

    0<u<=.35(d+r), v>0, v-a<-.5d.                    (6)

In particular .7(d+r)<=.7sqrt(2)<1<a, verifying the longitudinal-axis comparison stated in Section 3.

Put

    alpha=bd+tr>0, h=br-td.

### 4.1. The transverse source (V)

If h>=0, (5) and the upper faces (1), followed by a>1, give

    L_B(v_C)=h p+alpha q<d f+r g,
    f=1-b+t-t^2,
    g=-.39-b-t+bt<0.

The exact identity b f+t g=b-1-.39t<=0 yields

    b(d f+r g)=d(b f+t g)+h g<=0.

Thus L_B(v_C)<0<v, excluding (V).

If h<=0, use the actual strict marker M, which gives p+a>-.35(b+t). The exact full lower support instead satisfies

    L_B(v_C)=h(p+a)+alpha q<d f2+r g2,
    f2=1-b-.65t^2-.04bt,
    g2=-.35-.04t^2+.65bt-t.

Since 1-b=t^2/(1+b)<=.6t^2, one has

    f2<=-.05t^2-.04bt<0,
    g2<=-.35-.04t^2-.35t<0.

Again L_B(v_C)<0<v. Equality h=0 is covered by either argument.

### 4.2. The longitudinal source (L)

If h>=0, then

    L_C(u_B)=alpha(u-a)+h(v-a).

Use (6), a>1, and the strict projection bound from D. Subtracting the projection -.35(b+t) of B's strict marker M gives the strict upper bound bF+tG0, where

    F=.7-d-.35r^2-.15dr,
    G0=.85-r-.15r^2+.35dr>0.

The last positivity follows from d>=r and r<5/7. Direct expansion gives

    dF+rG0=.7(d+r)-1<0,
    d(bF+tG0)=b(dF+rG0)-hG0<0.

Therefore L_C(u_B)<u_B(M)<p+a, contradicting (L).

If h<0, put k=-h=td-br>0. By (3),(5), (L) would require

    a(1+alpha)<=b+t+alpha u-kv.

Set H=d+r and q0=1-.35H>0. Using (6) and a>1 gives

    1<b+t-alpha q0.                                  (7)

But

    2alpha-(b+t)H=(b-t)(d-r)>=0,
    Hq0-.65=(H-1)(.65-.35H)>=0,

where 1<=H<10/7. Consequently

    b+t-alpha q0<=(b+t)(1-Hq0/2)
                  <=(10/7)(1-.65/2)=27/28<1,

contrary to (7). This completes both sources for every nonpositive C angle, including the axial and diagonal cases.

## 5. A nonnegative C has a stronger transverse lower bound

Now take

    u_C=(d,r), v_C=(-r,d), d>=r>=0, d^2+r^2=1.

At M its lower u-band follows from A, its upper u-band from O, and its lower v-band from M_C. Therefore it is upper v:

    0<v<=.35(d+r).

At G its lower u-band follows from O and its upper v-band from M_C. It can only be upper u or lower v. A lower-v G opposed to M's upper v-face would give a<=.7(d+r)<=.7sqrt(2)<1. Thus

    0<u<=.35(d-r), v>0.                               (8)

This also excludes d=r immediately, though retaining that endpoint in the estimates causes no problem. The inequality .7(d-r)<1 gives the remaining longitudinal comparison used in Section 3.

The actual foreign bar endpoint F has both upper bands from M_C:

    u_C(M_C)-u_C(F)=.04d+.65r>0,
    v_C(M_C)-v_C(F)=.65d-.04r>0.

It is lower u or lower v. Its lower-u alternative, opposed to G's upper u-face in (8), would give

    a<=.74d+.65r<=sqrt(.9701)<1.

Hence F is lower v. We obtain the additional actual-face bound

    v>=a+.39r-d>1+.39r-d.                             (9)

This is the ingredient that extends the positive-C argument to its entire canonical interval.

## 6. Both remaining sources fail for every nonnegative C angle

Put

    alpha=bd-tr>=0, k=br+td>0.

### 6.1. The longitudinal source (L)

The exact lower C support is alpha(u-a)-kv. By (3), a necessary condition for (L) is

    a(1+alpha)<=b+t+alpha u-kv.

Insert (8),(9) and a>1. The resulting strict necessary inequality is

    1<bF+tG,                                         (10)

where the exact coefficients are

    F=1.35-d-r+.65dr-.74r^2,
    G=2+r-d-.74dr-.65r^2.                             (11)

They satisfy G>=.305>0 and

    G-F=.65+2r-1.39dr+.09r^2>0.

For fixed d,r, the function sqrt(1-t^2)F+tG increases throughout 0<=t<=1/sqrt(2): if F<=0 its derivative is positive directly; if F>0 it is at least G-F>0. Its maximum is therefore (F+G)/sqrt(2). Moreover

    F+G=1.35+2(1-d)-.09dr-1.39r^2<=1.35,             (12)

because 1-d=r^2/(1+d) and d>=1/sqrt(2)>.7 give 2(1-d)<1.2r^2 for r>0; the r=0 endpoint gives equality in (12). Thus

    bF+tG<=1.35/sqrt(2)<1,

contradicting (10).

### 6.2. The transverse source (V)

Its exact support is

    L_B(v_C)=-k(p+a)+alpha q.

Use the lower p-face (3) and upper q-face (1). Dropping a to 1 in the resulting positive coefficient gives

    L_B(v_C)<-dK+rJ,
    K=b+t-1-.61bt,
    J=1-b+t-.61t^2.                                  (13)

Here K>0, since

    K=(b+t-1)[1-.305(b+t+1)]>0.

The function sqrt(1-t^2)+t is increasing on the canonical interval. Thus (4) gives b+t>sqrt(1-.45^2)+.45>.89+.45=1.34. As a function of H=b+t, K=H-1-.305(H^2-1) is increasing for 1<=H<10/7. Therefore

    K>K(1.34)=.097342>.095,
    0<1-K<.905.                                      (14)

Also J>.245 using b<.9, t>.45 and t^2<=.5. Holding b=sqrt(1-t^2), its derivative is 1+t/b-1.22t>0. Hence

    J<=J(1/sqrt(2))=.695,
    |J-.39|<=.305.                                   (15)

Equations (14),(15), d^2+r^2=1, and Cauchy--Schwarz give

    d(1-K)+r(J-.39)
       <=sqrt((1-K)^2+(J-.39)^2)
       <sqrt(.905^2+.305^2)=sqrt(.91205)<1.

Combining this with (9),(13),

    L_B(v_C)<-dK+rJ<1+.39r-d<v.

This excludes (V). Both remaining directions, all angle orders, and all axis endpoints have now been checked for each canonical sign of C. A separating axis does not exist, contradicting the disjointness of the actual squares. Theorem 1 follows. ∎

## 7. The full original MMMP application

**Corollary 2.** In every original C1092 MMMP alternative, the actual northeast square Q6 has a strictly positive canonical angle.

Use the same quarter-turn chart on every actual owner:

    (X,Y)=(2-y,x-2), C=Q7, B=Q6.

The complete input ledger is

| Local datum | Original point | Genuine source |
|---|---|---|
| O,A,D strict in C | (2,2),(2,2.5),(1.5,2) | Full MMMP center and crosspoint theorems for Q7 |
| M_C strict in C | (1.65,2.35) | Q7's original marker |
| G excluded from C | (1.65,1.65) | Actual Q4 original marker |
| M excluded from C, strict in B | (2.35,2.35) | Actual Q6 original marker |
| F excluded from C | (1,2.39) | Actual Q8 wall-sign chord |
| H1,H2 strict in B | G7=(2.26,3), F7=(2.4,3) | Full MMMP core-owner theorem |
| I excluded from B | (2,2.39) | Strict segment from (2,2) to (2,2.5) in actual Q7 |
| J excluded from B | (3,2.39) | Actual Q10 wall-sign chord |
| W excluded from B | (2,3.086) | Actual Q11 original marker |
| K excluded from B | (3,3) | Actual paired corner Q2 |
| A excluded from B | (2,2.5) | Actual Q7 strict crosspoint |

Every point is available before this corollary. Neither the top origin (2,3), the right origin (3,2), the second inward tip, nor any southeast owner alternative is required. The chart is a rotation, so it preserves the canonical angle sign after the usual face relabeling. Theorem 1 therefore gives the stated original northeast sign.

This is a complete all-angle sign theorem for one actual central owner. It does not by itself exclude the whole MMMP sector; the remaining positive-angle northeast configuration still has to be coupled to the other actual owners.
