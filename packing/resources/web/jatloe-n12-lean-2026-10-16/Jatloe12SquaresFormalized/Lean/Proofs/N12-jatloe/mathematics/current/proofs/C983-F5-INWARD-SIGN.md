# C983 F5-only: an inward southeast square has negative angle

Every terminating decimal is an exact rational. Owned points and bars are strict in their named actual open squares; exclusions and separating supports allow contact. This local theorem uses full squares of common side a>1. No side upper bound or artificial container wall is used.

## 1. Local theorem and actual application

**Theorem 1.** Let W,E be disjoint open squares of common side a>1. Suppose W strictly owns

    P=(−.35,−.35), O=(0,0), F=(0,.26),             (1)

and E strictly owns

    M=(.35,−.35), I=(0,−.26), D=(.26,0).           (2)

Suppose E excludes A0=(1,−.26) and the whole segment

    B0 B1=[.26,.8]×{−1}.                          (3)

Then E has a strictly negative canonical angle.

For C983 label8224, translate by (−2,−2) and take W=Q7,E=Q5. The W points in (1) are its southwest marker, the universal center from `C983-F5-MERGED-CENTER.md`, and F5. The E points in (2) are its southeast marker,F4,G6. Its omitted F8 supplies the exclusion A0, requiring no new owner for that auxiliary. The whole segment (3) is the universal strict Q9 bar proved in `C983-F5-CENTRAL-REDUCTION.md`. Thus the theorem applies whenever actual Q5 owns F4 and omits F8.

After `C983-F5-LOWER-RIGHT-EXCLUSION.md`, this covers Q5=65552={F4,G6} and Q5=327696={F4,G6,G8}. In particular it covers every southeast possibility in each of the three remaining right-wall components which own both F8 and F9. It also covers these same southeast components when Q10=524800.

## 2. The positive-frame face table

Suppose, for a contradiction, that E has a nonnegative canonical frame

    u=(c,s), v=(−s,c), c≥s≥0, c²+s²=1.

Write its lower faces U,V and upper faces A=U+a,H=V+a. At its excluded O the lower u and v bands follow from I and M, respectively, while the upper u band follows from D. Therefore

    H≤0.                                         (4)

The strict D gives H>−.26s. In particular s=0 is impossible; hence s>0 and c<1.

At the excluded A0=(1,−.26), the lower u band follows from I, the upper v band from D, and the lower v band from V=H−a<−1. For the last comparison,

    v(A0)=−s−.26c>−1,

because s+.26c≤1.26/sqrt(2)<1 over the canonical interval. Thus A0 can exit only through upper u:

    A≤c−.26s,
    U≤c−.26s−a<c−.26s−1.                         (5)

At B0 both upper bands follow from D, so it exits through lower u or lower v. We retain both weak alternatives, even when both hold:

    U≥.26c−s  or  V≥−.26s−c.                     (6)

If the second alternative holds, then

    H≥a−c−.26s>1−c−.26s.                         (7)

If it does not hold, the first does. At B1 the lower u band follows from I, with gap .8c−.74s≥.06c>0, and the upper v band from D. Were B1 upper u, (6) would give

    a≤(.8c−s)−(.26c−s)=.54c<1,

which is impossible. Consequently

    U≥.26c−s, V≥−.8s−c.                          (8)

Any interior intersection of E with y=−1 would, by (8), have .26<x<.8 and would belong to the whole excluded segment (3). There is no such intersection. The strict marker M is above that line, so convexity forces the full closed lower support of E to satisfy

    y_min=sU+cV≥−1.                              (9)

Equation (9) has been proved from the one actual foreign bar; it is not an assumed wall on E. We shall call (7) the first case and (9) the second. They cover every possibility in (6).

## 3. The exhaustive W-to-E normal list

Orient a prospective separating direction n from W toward E. The strict pair P,M gives n_x>0. The strict pair F,I gives n_y<0. E's only face-normal direction in this cone is

    −v_E=(s,−c).                                  (10)

If W has negative canonical frame (d,−r),(r,d), with d≥r≥0, its only additional possible direction is (d,−r). If W has positive canonical frame (d,r),(−r,d), its only additional possible direction is (r,−d). Retaining their axial endpoints only enlarges the list. Every reverse or other face direction fails one of the two strict component inequalities.

On direction (10), E's lower support is −H and the strict P in W has projection

    (−v_E)·P=.35(c−s).                            (11)

We will use that projection, and the strict O in W where indicated, to exclude each of these full actual-square directions.

## 4. First bottom-bar case: the lower v bound

Assume (7), along with (4),(5). Equation (7) and H≤0 imply

    c+.26s>1,
    0<z=s/(1+c)<13/50.

The half-angle identity is c+.26s−1=2z(.26−z)/(1+z²). Consequently

    c>2331/2669>.873,
    s<1300/2669<.49,
    .35(c−s)>2681/20000>.134.                    (12)

Also, throughout the entire unit circle,

    c+.26s−1≤sqrt(1+.26²)−1<.034,                 (13)

where 1.034²>1+.26² is an exact squared comparison. From (7), −H<c+.26s−1. Equations (11)–(13) immediately exclude E's normal (10).

### 4.1. W has negative canonical frame

Put

    k=cd−sr≥0, h=sd+cr>0.

The full lower support of E in direction (d,−r) is kU−hH. By (5),(7), it is strictly less than

    k(c−.26s−1)−h(1−c−.26s)
      =d D1+r R1,                                (14)

where

    D1=(c−1)(c+s)+.26s(s−c)<0,
    R1=(c−1)(c−s)+.26s(c+s).

The exact other endpoint is

    D1+R1=2c(c−1)+.52s²
          =(1−c)(.52−1.48c)<0.                    (15)

The last sign follows from c≥1/sqrt(2)>.7. Since 0≤r/d≤1, the affine expression D1+(r/d)R1 is negative at both endpoints and therefore negative throughout. Thus (14) is negative. The strict O gives a positive upper support of W on this direction, contradicting separation.

### 4.2. W has positive canonical frame

Set

    delta=cr−sd, k=cd+sr>0.

First suppose delta≥0. E's full lower support in direction (r,−d) is delta U−kH. Subtract the strict P projection .35(d−r). Equations (5),(7) bound this difference strictly above by

    delta(c−.26s−1)−k(1−c−.26s)−.35(d−r)
      =d D2+r R2,                                (16)

where

    D2=(c−1)(c−s)+.26s(c+s)−.35<0,
    R2=(c−1)(c+s)+.26s(s−c)+.35.

Indeed s(c+s)≤1 gives D2≤.26−.35=−.09. The sum D2+R2 is exactly the negative expression in (15). The same affine endpoint argument on 0≤r/d≤1 shows that (16) is negative, contradicting separation.

If delta≤0, the W angle is at most the E angle. Thus d−r≥c−s. Now E's full lower support is delta A−kH. Its strict D gives A>.26c>0, while k≤1. Hence, using (7),(13),

    lower_E(r,−d)
       <k(c+.26s−1)≤c+.26s−1<.034.

But the strict P in W has projection .35(d−r)≥.35(c−s)>.134 by (12). This also contradicts separation. The common endpoint delta=0 is included without division. Every direction has failed in the first bottom-bar case.

## 5. Second bottom-bar case: the proved lower support

Assume (9). Recalling V=H−a, it gives

    H≥a−1/c−(s/c)U.                              (17)

With (5) and a>1, this also yields

    H>[c+s−1−cs+.26s²]/c.

Let

    F0=c+s−1−cs+.26s².

The gap needed for E's normal (10) is strictly positive:

    F0+.35c(c−s)
      =c+s−1−1.35cs+.26s²+.35c²
      ≥.35c²−.55cs+.26s²
      ≥.06c²>0.                                  (18)

The first inequality uses c+s−1≥.8cs, which follows from c+s<3/2. For the second, put t=s/c∈[0,1]; the quadratic .35−.55t+.26t² decreases on [0,1] and equals .06 at1. Therefore −H<.35(c−s), opposite to the support ordering required by the strict W point P. E's own normal is excluded.

We will use the common negative quantity

    X=(1−c)(c+s−1)−.26s<0.                       (19)

Indeed 1−c=sz, with z=s/(1+c)≤sqrt(2)−1, and c+s−1≤sqrt(2)−1. Hence

    X=s[z(c+s−1)−.26]
      ≤s[(sqrt(2)−1)²−.26]<0.

The last strict inequality is exact because (sqrt(2)−1)²=3−2sqrt(2)<.26, equivalently sqrt(2)>137/100.

### 5.1. W has negative canonical frame

Use k,h from Section 4.1. By (17),

    lower_E(d,−r)=kU−hH
       ≤(d/c)U−ah+h/c,

where the exact elimination identity is ck+sh=d. Substituting (5), and then a>1, makes the last expression strictly less than

    (d/c)(c−.26s−1)−h+h/c.

After multiplication by c, its numerator is

    (1−c)(h−d)−.26ds
      =d[(1−c)(s−1)−.26s]+rc(1−c)
      ≤d[(1−c)(c+s−1)−.26s]
      =dX<0.                                     (20)

We used r≤d. Thus the full lower support of E is negative, whereas the strict O supplies positive upper support in W. This direction cannot separate.

### 5.2. W has positive canonical frame, with either relative angle order

Use delta,k from Section 4.2. Its full lower E support is

    delta U−kH+a min(delta,0)
       ≤delta U−kH.

By (17) and the exact identity c delta+sk=r, this is at most

    (r/c)U−ak+k/c.

Apply (5) and a>1. After subtracting the strict P projection .35(d−r) and multiplying by c, the resulting strict upper bound is

    (1−c)(k−r)−.26rs−.35c(d−r)
      =d D3+r R3,                                (21)

where

    D3=c(.65−c)<0,
    R3=(1−c)(s−1)−.26s+.35c.

The exact endpoint sum is D3+R3=X<0. Again the expression D3+(r/d)R3 is affine on [0,1] and negative at both endpoints. Equation (21) is negative for every W angle and every relative order of the two angles. The strict P projection already exceeds the full lower E support, excluding this final direction.

Both cases from (6) have now exhausted every actual face-normal direction in the strict separating cone. W and a nonnegative E cannot have disjoint interiors. E's canonical angle is therefore strictly negative, proving the local theorem. ∎

## 6. Scope

The source map in Section 1 gives the claimed negative sign for every remaining F4-containing southeast component which omits F8. The entire sign argument uses only the actual merged square, the actual southeast square, the true F8 exclusion and the complete actual Q9 bar. It neither assigns F4 to merged Q7 nor imports a merged vertical midpoint. The algebraic support identities above were independently reconstructed symbolically; the proof itself is the continuous face, support and endpoint argument displayed here.
