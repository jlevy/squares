# An actual bottom wall square owns its lower midpoint

Every terminating decimal is an exact rational. Owned points and the entire owned segment below are strict in their actual owners. Exclusions and separating supports may be tangent. The proof uses full square supports and all continuous angle ranges; no numerical angle enclosure is a premise.

## 1. Local statement

**Theorem 1.** Let W and C be disjoint open squares of the same side a>1. Suppose W has a strictly positive canonical frame

    u=(d,t), v=(−t,d), d≥t>0, d²+t²=1,

and strictly owns

    O=(0,0), P=(0,−.086), R=(.8,0).

Suppose W excludes S=(−.04,−.24), F0=(0,.5), and the entire segment

    I=[M=(.35,.65), H=(1,.5)].

Suppose C has its closure in x≤2,y≥−1, strictly owns A=(1,0), and excludes H. Then

    Z=(0,−.5) belongs strictly to W.

The segment premise in the C974 application is supplied by one actual southeast square containing both M and H. No replacement square or reassignment of its points is made. The local theorem does not need a wall or center condition for W, or any angle restriction on C.

## 2. The missing midpoint and the actual foreign segment

Write L,V for W's lower face coordinates and J=L+a,T=V+a for its upper coordinates. Strict O implies L,V<0 and J,T>0.

At F0 the two u-bands follow from P,R, and its lower v-band follows from O. Therefore

    T≤.5d.                                             (1)

Since A belongs to the disjoint actual C, W excludes it. At A, the lower u-band follows from R and the upper v-band follows from O. Thus A is upper u or lower v. At M both lower bands follow from P,R, so M is upper u or upper v. If A were lower v and M upper v, their opposite faces would give

    a≤.65(d+t)≤.65sqrt(2)<1.

Consequently either A or M is upper u. Their u-projections are d and .35d+.65t≤d, respectively, so

    J≤d.                                               (2)

The excluded S has both upper bands from P, with positive projection increments .04d+.154t and .154d−.04t. If it were lower v, (1) would give a≤.74d−.04t<1. Hence

    L≥−.04d−.24t,
    1<a≤1.04d+.24t,
    t/d<2/3.                                          (3)

For the final implication, the function (1.04+.24r)/sqrt(1+r²) decreases on r≥2/3, and at r=2/3 its value is 3.6/sqrt(13)<1. This excludes the complete complementary angle interval.

Set

    theta=atan(t/d), z=t/(1+d).

The bound (3) gives

    0<z<4/13<1/3, d>4/5, t<3/5.                    (4)

Indeed the tangent corresponding to z=4/13 is 104/153>2/3, and d>3/sqrt(13)>4/5, t<2/sqrt(13)<3/5.

At the target Z its upper u,v-bands follow from P. Its lower v-band follows from (1), since

    V=T−a≤.5d−a<.5d−1≤−.5d=v(Z).

Suppose Z were missing. Its only possible exit is therefore lower u:

    L≥−.5t, J≥a−.5t.                               (5)

The square W is disjoint from the entire segment I. The separating-axis theorem for a square and a segment supplies an axis from u,v or a normal to the segment. Both endpoints have u-coordinate above L. The upper-u separation is impossible because

    u(M)=.35d+.65t<(.35+.65·2/3)d<.8d<J.

The lower-v separation is impossible because v(M)=.65d−.35t>0>V. The two remaining alternatives are therefore

    T≤v(H)=.5d−t,                                    (6a)

or

    A0 J+B0 T≤9.5,
    A0=3d+13t>0, B0=13d−3t>0.                      (6b)

For (6b), the segment lies on 3x+13y=9.5. Strict O is on the lower side, so its normal has the displayed orientation. The direction (3,13) has the displayed positive coefficients A0,B0 in the square frame; hence the left side is the full upper support of W in that direction. The whole segment has been retained in this step, including its endpoints and possible tangencies.

## 3. A strict crossing below the actual corner point

Define

    R_*=(1,z−.5).

The identities d+tz=1 and t−dz=z give

    u(R_*)=1−.5t, v(R_*)=−z−.5d.                    (7)

Its lower u-band follows from O; its upper u-band follows strictly from (5) and a>1; its upper v-band follows from O. We prove its remaining lower v-band in both alternatives (6).

If (6a) holds, then

    T−v(R_*)≤d−t+z<1<a,
    1−d+t−z=z(d+t)>0.                              (8)

If (6b) holds, use (5) to obtain

    B0[T−v(R_*)−a]
      ≤9.5+(t/2)A0+B0(z+d/2)−a(A0+B0)
      =−E−(a−1)(A0+B0)<0,                          (9)

where the exact identity is

    E=A0+B0−9.5−(t/2)A0−B0(z+d/2)
     =z(13z²−26z+7)/(1+z²)>0.                     (10)

The quadratic in (10) decreases on 0≤z≤4/13 and has value 3/13 at 4/13. Thus its sign follows on the complete interval (4). In either case T−v(R_*)<a, so v(R_*)>V. We have proved

    R_* is strictly in the same actual W.            (11)

Because z<1/3, this point lies strictly below A=(1,0) in C.

## 4. The unrestricted actual corner support

Transform the actual corner square C by

    (x,y)↦(2−x,y+1).

Its genuine walls become the first-quadrant walls. Its strict point A becomes (1,1), and its excluded H becomes (1,1.5). Theorem 6 of `C1092-DIRECT-WALL-POINT.md` therefore applies to this same transformed square, for every orientation. In the original local chart its conclusion is

    lower_C(c,s)≤2c−s−aF(c,s),
    F(c,s)=2c−1−cs/(1+c),                           (12)

for every c,s≥0 with c²+s²=1. This is a full support profile of C, not the support of only its listed points. It includes both axial endpoints.

Orient a separating normal n from W toward C. Comparing R=(.8,0) in W with A in C gives n_x>0. Comparing the new R_* in W with that same A gives n_y>0. Thus every possible separator is in the open first quadrant. It is enough to exclude every unit direction

    n=(c,s)=(cos(phi),sin(phi)), 0≤phi≤pi/2.

This enlarged closed range includes all actual edge normals of both squares that can lie in the strict cone. We show directly that upper_W(n)>lower_C(n) throughout it.

## 5. Directions no steeper than the wall square

First let 0≤phi≤theta and put w=s/(1+c). Then 0≤w≤z. From strict R_* and (12),

    upper_W(n)−lower_C(n)
      >n·R_*−[2c−s−aF(c,s)]
      =(a−1)F(c,s)+s[z−w+w²/2]≥0.                 (13)

Here (c+s)/(1+c)=.5+w−w²/2 gives the displayed identity. The last inequality uses w≤z and F>0 throughout this interval. Indeed theta<atan(2/3)<pi/4, and for 0≤phi≤pi/4 one has

    F=2c−1−cw≥c(2−(sqrt(2)−1))−1
      ≥(3−sqrt(2))/sqrt(2)−1>0.

For clarity, the final expression equals 3/sqrt(2)−2>0. Thus the coefficient of a−1 is positive even at phi=0. The strict ownership in the first line of (13) excludes separation also at every endpoint.

## 6. Intermediate directions: one positive cubic

Now suppose theta≤phi≤pi/3. Set

    alpha=cd+st=cos(phi−theta)>0,
    beta=sd−ct=sin(phi−theta)≥0.

Using the full W support, strict O, and (5),

    upper_W(n)=alpha J+beta T≥alpha(a−t/2).

After subtracting (12), the resulting lower bound is

    (a−1)(alpha+F)+f,
    f=(1−t/2)cos(phi−theta)−1+w,
    w=s/(1+c).                                      (14)

The coefficient alpha+F is positive on this whole interval. Indeed alpha≥c, c≥1/2 and w≤1/sqrt(3), so

    alpha+F≥c(3−w)−1≥(1−1/sqrt(3))/2>0.            (15)

We give a complete exact proof that f>0. Substitute

    d=(1−z²)/(1+z²), t=2z/(1+z²),
    c=(1−w²)/(1+w²), s=2w/(1+w²).

Here z≤w≤1/sqrt(3)<1. Put v0=(w−z)/(1−z), so 0≤v0≤1. Direct polynomial expansion gives the identity

    (1+z²)²(1+w²)f
      =b0(1−v0)³+3b1 v0(1−v0)²
         +3b2 v0²(1−v0)+b3 v0³,                   (16)

where

    b0=z³(1+z²)²,
    b1=(1+z²)(1+z+z²)(3z²−2z+1)/3,
    b2=2z(2z⁴−z³+5z²−3z+3)/3,
    b3=4z(z²−z+1).

Every coefficient is strictly positive. For b1 use 3z²−2z+1=3(z−1/3)²+2/3. For b2, since 0<z<1/3, its last factor is greater than 3−3z−z³≥53/27>0. The two other signs are immediate. The four nonnegative basis functions in (16) sum to 1, so (16) proves f>0 over the entire closed interval. This identity supplies a continuous inequality, with no angle samples or subdivisions. Equations (14)–(16) exclude every direction in this range.

## 7. Steeper directions

Finally let pi/3≤phi≤pi/2. Still alpha>0,beta≥0, so

    upper_W(n)≥alpha(a−t/2)>alpha(1−t/2).

If c>0, then s/c≥sqrt(3)>3/2. Hence

    alpha(1−t/2)>c(d+3t/2)(1−t/2)>c.              (17)

For the last inequality, (4) gives

    (d+3t/2)(1−t/2)−1
      =−t²/(1+d)+t(3/2−d/2)−3t²/4
      ≥t−47t²/36
      >13t/60>0.                                  (18)

We used d>4/5 to bound 1/(1+d)<5/9, and t<3/5 for the last line. If c=0, the same support is strictly positive, since alpha=t>0 and J≥a−t/2>0.

The actual strict point A=(1,0) in C gives lower_C(n)<n·A=c. Thus (17), and its c=0 endpoint, again contradict separation. All possible separating directions have now been excluded. The supposition (5) is impossible, proving strict ownership of Z by W. ∎

## 8. Exact first-root C974 application

In the first missing-corner root, actual Q0 excludes (1,1). Theorems 1 and 2 of `MISSING-CORNER-WALL-SIGN.md` prove that actual Q9 has a strictly positive canonical angle. Apply Theorem 1 above with W=Q9,C=Q2 and the simultaneous translation

    (X,Y)=(x−2,y−1).

Every datum has the following genuine actual source:

| Local datum | Original point or segment | Actual source |
|---|---|---|
| O,P,R strict in W | (2,1),(2,.914),(2.8,1) | Q9's proved origin, original marker and strong bottom reach |
| Excluded S | (1.96,.76) | Q0's retained missing-corner strict point |
| Excluded F0 | (2,1.5) | Actual southwest Q5 crosspoint |
| Excluded whole I | [(2.35,1.65),(3,1.5)] | Original marker and proved crosspoint in the same southeast Q6 |
| A strict in C | (3,1) | Actual paired southeast corner Q2 |
| H excluded from C | (3,1.5) | The same actual southeast Q6 |
| C's two walls | x≤4,y≥0 | Actual original container walls |

The common origin and southeast crosspoint hold for both remaining central pairs by Sections 5 and 8 of `C974-C976-CENTRAL-CROSSPOINTS.md`. The actual bottom reach and the southwest crosspoint have the sources recorded in `MISSING-CORNER-WALL-SIGN.md`, Section 2. All squares retain their original common side and disjoint interiors. The local target returns to

    Q0 excludes (1,1) ⇒ (2,.5) is strictly in Q9.    (19)

No additional angle, center, label or upper-side hypothesis has been used.
