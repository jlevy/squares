# C1092 MPPM: a positive missing-forward owner cannot take the origin of a shallow negative wall square

Every terminating decimal is exact. Owned points are strict interior points of the named actual open squares. Exclusion and separating supports allow equality. The local proof uses only a common side a>1 and one actual left wall; it has no upper side bound or central-angle cutoff.

## 1. The two actual squares

Let C have positive canonical frame

    u=(c,s), v=(-s,c), c>=s>0, c^2+s^2=1,
    U<u dot Z<A=U+a, V<v dot Z<H=V+a.

Suppose C strictly owns

    P=(-1,-.26), D=(-1,0),

and has the actual upper-face cap

    A<=-.26c.                                    (1)

Let L be an actual square of side a, disjoint from C, with negative canonical frame

    e=(d,-t), f=(t,d), d>=t>=0, d^2+t^2=1,
    U_L<e dot Z<A_L=U_L+a,
    V_L<f dot Z<H_L=V_L+a.

Suppose L strictly owns

    W=(-1.086,0), P_L=(-1,.26),

has its closure in x>=-2, and excludes

    Z=(-1.086,1).                                (2)

**Theorem 1.** These actual squares can be disjoint only if

    t/d>5/12.                                    (3)

The excluded Z will be the marker of the actual upper paired corner. It is retained even though that corner's full shape is unnecessary in this local theorem.

## 2. The genuine wall faces and exhaustive normal cone

Since D is strict in C, it is excluded from L. Its lower e-band follows from W, its lower f-band follows from W, and its upper f-band follows from P_L. The increments are .086d>0, .086t>=0 and .26d>0. A zero increment inherits the strict band of its owned anchor. Therefore

    A_L<=-d.                                    (4)

If t=0, the true left wall and (4) give U_L=A_L-a<=-1-a<-2, a contradiction. Thus t>0.

At the excluded Z, the upper e-band and lower f-band follow from W. Its lower e-band follows from (4), because

    e dot Z-U_L>=a-.086d-t>0,
    .086d+t<=1.086/sqrt(2)<1.

The last maximum is on the full canonical interval: the derivative of .086 cos beta+sin beta is positive there. Consequently Z can only exit through upper f, and

    H_L<=d-1.086t,
    V_L<=d-1.086t-a.                            (5)

Direct a separating normal from C toward L. The two strict pairs D,W and P,P_L respectively give n_x<0 and n_y>0. The separating-axis theorem leaves exactly the two possible actual sources

    v=(-s,c), -e=(-d,t).                         (6)

Suppose, for contradiction, t/d<=5/12. Then

    d>=12/13, t>0,
    k=cd-st>0, ell=sd+ct>0.                      (7)

The strict sign of k follows already from t/d<1 and s/c<=1. All weak separating equalities are retained below.

## 3. C's transverse normal is impossible

The true left wall of the same actual L is

    d U_L+t V_L>=-2,

or equivalently

    A_L>=a-2/d-(t/d)V_L.                         (8)

In L's frame, v=-ell e+k f. Therefore its exact lower support is

    lower_L(v)=-ell A_L+k V_L.

Use (8); the resulting coefficient of V_L is k+ell t/d=c/d>0. Then use (5). Since the resulting coefficient of a is -ell-c/d<0, decreasing a to 1 gives a strict bound. With z=t/(1+d)=(1-d)/t, exact simplification yields

    lower_L(v)-s
      < (ct/d)[.914-d-z+(s/c)dz].                (9)

As s/c<=1 and 0<d<1, the bracket satisfies

    .914-d-z+(s/c)dz
      <=.914-d-z(1-d)
      <=.914-12/13=-59/6500<0.                  (10)

The prefactor in (9) is positive. Thus lower_L(v)<s, whereas the strict D in C gives upper_C(v)=H>s. This excludes C's actual normal v.

Equation (9) uses the real wall in its valid direction and the upper f-face of that same square L. It makes no upper estimate by dropping a positive center contribution.

## 4. The wall square's own normal is impossible

The exact frame change is -e=-k u+ell v. From (1), U<=-.26c-a. Together with H>s from the strict D, this gives

    upper_C(-e)=-kU+ell H
      >k(a+.26c)+ell s.                          (11)

The strict W in L gives lower_L(-e)=-A_L<1.086d. The actual support difference in (11) is therefore strictly larger than its value at a=1, namely

    k(1+.26c)+ell s-1.086d
      =d[(1-.74c)(c-(t/d)s)-.086].              (12)

All factors used next have their correct signs. On the full central canonical range, c>7/10 and s<=c. On (7),

    1-.74c>=13/50,
    c-(t/d)s>=(7/12)c>49/120.

Hence the bracket in (12) is strictly greater than

    (13/50)(49/120)-43/500=121/6000>0.           (13)

This excludes the remaining actual normal -e. Both possible sources in (6) have failed, proving Theorem 1. The axial L endpoint was excluded directly, and the equalities t/d=5/12, s=c and every weak wall or face contact were kept in the proof. ∎

## 5. Literal original application and its remaining input

Retain the no-omission OOOO MPPM entrance. Suppose the positive ordinary Q4 omits forward G3=(1.74,2), but strictly owns the preceding origin D=(1,2). Translate by (-2,-2). Its ordinary F0 is P, and Lemma 1 of C1092-MPPM-MISSING-POSITIVE-WALL-ORDER.md gives the cap (1), without any assumed owner for D.

The actual preceding wall L=Q8 has strict W=(.914,2), P_L=F1=(1,2.26), and the true wall x>=0. The point Z=(.914,3) belongs strictly to the actual paired corner Q3, and is therefore excluded from L. Thus if Q8 has negative canonical angle, Theorem 1 gives its absolute slope strictly greater than 5/12.

The complete source map is

| Local datum | Actual original source |
|---|---|
| P,D strict in C | Ordinary F0 and the stipulated strict (1,2) in Q4 |
| A<=-.26c | Positive missing-forward G3 profile of the same Q4 |
| W,P_L strict in L | Q8's original marker and F1 |
| Z excluded from L | The original outer marker (.914,3) in actual Q3 |
| Actual left wall | Original closure of Q8 in x>=0 |

Simultaneous quarter turns give the corresponding statement in every sector. In particular this theorem can be joined to any independently proved upper bound <=5/12 for that same negative wall under its missing-origin premise. No such upper bound is assumed in Theorem 1 itself, and this chapter by itself does not assert universal origin ownership.
