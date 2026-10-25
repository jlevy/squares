# A three-square support contradiction completes C974

All decimals are exact rationals. Strict ownership refers to the open interior of the named actual square. Exterior faces and genuine container walls may be tangent. The three squares compared below retain the same physical side length a>1.

## 1. The local three-square theorem

**Theorem 1.** Let K,W,C be open squares of common side a>1, with pairwise disjoint interiors. Suppose that K has closure in y≥−1, strictly owns

    P=(0,−.086), A=(.82,0), S=(.96,−.24),

and excludes E=(0,0). Suppose W strictly owns

    O=(1,0), P_W=(1,−.086), R=(1.8,0),

and excludes

    M=(1.35,.65), F0=(1,.5), F1=(2,.5).

Finally suppose C has closure in x≤3,y≥−1, strictly owns A_C=(2,0), and excludes F1.

Then this configuration is impossible.

The point M is only an excluded point in the statement. No segment beginning at M, and no strict owner for M, is assumed.

### 1.1. The established positive frames and actual supports

Since C strictly owns A_C, W excludes that point as well. Thus K,W have exactly the hypotheses of Theorem 1 of `MISSING-CORNER-WALL-SIGN.md`. Theorems 1 and 2 there give strictly positive canonical angles for both squares. The complete angle argument in `MISSING-CORNER-MIDPOINT.md`, Section 1.4, further gives

    u_K=(l,h), v_K=(−h,l), l≥h>0, l²+h²=1,
    0<h/l<3/4.                                        (1)

Write U,V for K's lower faces and B=V+a for its upper v face. Its strict marker, excluded E, and genuine lower wall give

    U<−.086h<0, B≤0,
    hU+lB≥al−1.                                      (2)

In particular, if

    x=h/(1+l),

then 0<x<1/3 and

    U+a≥a(1+l/h)−1/h>1−x.                           (3)

For W, use the translated chart (X,Y)=(x_original−1,y_original). In this chart its strict points are (0,0),(0,−.086),(.8,0). Put

    u_W=(d,t), v_W=(−t,d), d≥t>0, d²+t²=1,
    L,H lower faces, J=L+a, T=H+a upper faces.

The point comparisons in `MISSING-CORNER-MIDPOINT.md`, Section 1.1, use precisely the hypotheses above and give

    J≤d, T≤.5d, 0<t/d<2/3.                         (4)

For reference, F0 forces the upper-v cap. The two-face alternatives at A_C and M force the upper-u cap. The actual foreign S then forces L≥−.04d−.24t, so 1<a≤1.04d+.24t, yielding the last bound. These comparisons use M only as an excluded point.

Set

    z=t/(1+d), k=z(1−t), f(x)=x(1−h)
                              =x(1−x)²/(1+x²).

The domain available throughout is

    0<x<1/3, 0<z<4/13<1/3,
    d>3/sqrt(13)>83/100.                            (5)

Strict O gives L,H<0 and J,T>0.

## 2. Actual K–W separation forces a sharper lower face

We prove the uniform inequality

    L>−k=−z(1−t).                                   (6)

The full supports of K and W are essential here.

Orient a separating normal from K toward W. The strict pair A,O forces its first component positive, and the strict pair S,O forces its slope to exceed −1/6. The negative-slope normals −v_K,−v_W have slope at most −1. Hence the only remaining actual square normals are u_K and u_W.

Define

    κ=ld+ht>0, σ=hd−lt.

The sign of σ is the sign of x−z. We treat both actual directions and both signs without restricting either angle to a sampled set.

### 2.1. The direction u_W when x≥z

Here σ≥0 and u_W=κu_K−σv_K. The wall inequalities (2) give

    upper_K(u_W)
      =a(κ+σ)+κU−σB
      ≥a(κ+σ+κl/h)−κ/h
      >κ(1−x)+σ.

The lower W support in the common original chart is d+L. Separation therefore requires

    L>κ(1−x)+σ−d=(1−h)(dx−t).                     (7)

If dx−t≥0, this already implies (6). Otherwise, the function

    1−h=(1−x)²/(1+x²)

decreases on 0≤x<1. Since x≥z and dz−t=−z,

    (1−h)(dx−t)≥(1−t)(dx−t)
                ≥−z(1−t)=−k.

Thus (6) follows also in this case, including x=z.

### 2.2. The direction u_K when x≥z

Now u_K=κu_W+σv_W. Its actual lower W support is

    lower_W(u_K)=l+κL+σH
                 ≤l+κL+σ(.5d−a).

Compare this with (3) and use a>1. A necessary condition for separation is

    κL>σ(1−.5d)−f(x).                              (8)

We show that the right side of (8) is at least −κk. Exact half-angle substitution gives

    κk+σ(1−.5d)−f(x)
      =−(x−z)P(x,z)/[(1+x²)(1+z²)²],              (9)

where

    P=x²(1+z²)²
       +x(−z³−6z²+z−2)
       −z⁴+2z³−3z²−2z.

On the whole domain 0<x,z<1/3, the first term is at most 4x/9, the coefficient of x is at most −5/3, and the final line is at most −2z. Consequently

    P≤−11x/9−2z<0.

As x−z≥0, (9) is nonnegative. Inequality (8) proves (6).

### 2.3. The direction u_W when x<z

Put γ=−σ>0, so u_W=κu_K+γv_K. Its exact upper K support is

    upper_K(u_W)=κ(U+a)+γB.

Using the wall in (2), its coefficient of B after eliminating U is

    γ−κl/h=−d/h<0.

Since B≤0, it follows that

    upper_K(u_W)≥κ[a(1+l/h)−1/h]>κ(1−x).

Separation requires L>κ(1−x)−d. The exact identity

    κ(1−x)−d+k
      =−(x−z)Q(x,z)/[(1+x²)(1+z²)]                (10)

has

    Q=x²(z²−1)+2x(z+1)+(1−z)²
      ≥−x²+2x+(1−z)²>0.

Because x−z<0, (10) is positive, and (6) follows.

### 2.4. The direction u_K when x<z

Here u_K=κu_W−γv_W. Since T>0, the actual lower W support obeys

    lower_W(u_K)=l+κL−γT<l+κL.

Comparison with (3) yields

    κL>−f(x).                                      (11)

First suppose z≤2/7. The exact identity

    κk−f(x)
      =−(x−z)R(x,z)/[(1+x²)(1+z²)²]               (12)

has

    R=x²(1+z²)²
       +2x(z³−3z²+z−1)
       −z⁴+2z³−2z+1.

On 0≤x,z≤1/3,

    R_x=2[x(1+z²)²+z³−3z²+z−1]
        ≤−106/243<0.

Since x<z,

    R(x,z)≥R(z,z)
      =(1−z)(1+z²)(1−3z−z²−z³)>0.                 (13)

The final cubic decreases for z≥0 and has value 13/343 at z=2/7. Thus (12) is positive, and (11) gives (6).

It remains to exclude the entire range z≥2/7 from this separating-direction alternative. In that range (4) and the half-angle formula give

    83/100<d≤45/53, 1−d≥8/53.

Combining (11) with L=J−a≤d−a<d−1 would require

    κ(1−d)<f(x).                                   (14)

For 0<x≤1/5, the derivative

    f'(x)=(1−x)(1−3x−x²−x³)/(1+x²)²

is positive. Hence f(x)≤f(1/5)=8/65. Also κ≥d because the positive difference between the W and K angles is at most the W angle. Therefore

    κ(1−d)−f(x)
      >(83/100)(8/53)−8/65
       =38/17225>0,                                (15)

contradicting (14).

For 1/5≤x<z, the angle difference is at most

    atan(2/3)−2atan(1/5),

so

    κ≥46/(13sqrt(13))>49/50.

The last comparison follows exactly from

    46²·50²−49²·13³=15003>0.

Moreover f(x)<7/50 throughout 0≤x≤1/3. Indeed the numerator of 7/50−f(x), after multiplication by 50(1+x²), satisfies

    7−50x+107x²−50x³
      ≥7−50x+(271/3)x²
       =(271/3)(x−75/271)²+22/271>0.               (16)

Consequently

    κ(1−d)−f(x)
      >(49/50)(8/53)−7/50
       =21/2650>0.                                 (17)

This again contradicts (14). The large-z range is excluded, and all remaining alternatives give (6). These four cases exhaust the actual K–W separating directions and their relative-angle signs.

## 3. The wall square crosses strictly below the actual corner

By (6), J=L+a>a−k>1−k. Together with J≤d, this implies

    1−d<k=z(1−t).

Since 1−d=tz and z>0,

    t<1/2, z<2−sqrt(3).                             (18)

Define

    beta0=(1+z²)/2−2z>0,
    R_**=(1,−beta0)

in W's translated chart. The upper bound in (18) proves beta0>0, by the smaller root of z²−4z+1. The exact projections are

    u_W(R_**)=1−k,
    v_W(R_**)=−t−beta0 d.                            (19)

The lower u band follows from strict O; the upper u band follows strictly from J>a−k>1−k. The upper v band also follows from O. For the lower v band, T≤.5d and the identity

    1−[t+d(.5+beta0)]
      =z²(3−z)(1−z)/[2(1+z²)]>0                   (20)

give T−v_W(R_**)<1<a. Thus

    R_** is strictly in the same actual W.             (21)

It lies below the actual corner point A_C=(1,0) in this translated chart. It also lies above the comparison height used below:

    −beta0−(z−.5)=z−z²/2>0.                         (22)

Finally, throughout (5),

    k<t/2,

because 2(1−t)<1+d is equivalent to z<2. Therefore

    J>a−k>a−t/2.                                    (23)

## 4. The actual corner profile rules out every direction

In W's translated chart, C has closure in x≤2,y≥−1, strictly owns A_C=(1,0), and excludes F1=(1,.5). Under (x,y)↦(2−x,y+1), it becomes a genuine first-quadrant square strictly owning (1,1) and excluding (1,1.5). The all-angle profile, Theorem 6 of `C1092-DIRECT-WALL-POINT.md`, therefore gives

    lower_C(c,s)≤2c−s−aF(c,s),
    F(c,s)=2c−1−cs/(1+c),                            (24)

for every unit c,s≥0. This is the support of the actual C, for all its orientations.

Orient any separating normal from W toward C. Strict R=(.8,0) and A_C imply its first component is positive. Strict R_** and A_C imply its second component is positive. Thus it remains to exclude the enlarged closed quadrant of unit normals

    (c,s)=(cos(phi),sin(phi)), 0≤phi≤pi/2.

We provide the complete continuous comparison. Put theta=atan(t/d), w=s/(1+c), and retain z=t/(1+d).

### 4.1. Directions 0≤phi≤theta

Here 0≤w≤z. By strict R_**, (22), and (24),

    upper_W(c,s)−lower_C(c,s)
      >(a−1)F(c,s)+s[z−w+w²/2]≥0.                 (25)

The displayed expression is the exact comparison with (1,z−.5), and (22) only increases its value. The identity used to simplify it is

    (c+s)/(1+c)=.5+w−w²/2.

Also F>0 throughout this range: theta<atan(2/3)<pi/4, and on 0≤phi≤pi/4 one has F≥3/sqrt(2)−2>0. Since a−1>0, even the axial endpoint is excluded. Strict ownership supplies the strict first inequality.

### 4.2. Directions theta≤phi≤pi/3

Set alpha=cos(phi−theta)>0 and beta=sin(phi−theta)≥0. The full W support, T>0, and (23) yield

    upper_W(c,s)≥alpha(a−t/2).

Subtracting (24) gives the lower bound

    (a−1)(alpha+F)+g,
    g=(1−t/2)cos(phi−theta)−1+w.                    (26)

Here alpha≥c, c≥1/2 and w≤1/sqrt(3), so

    alpha+F≥(1−1/sqrt(3))/2>0.

For completeness the exact continuous cubic identity establishing g>0 is as follows. Set v0=(w−z)/(1−z), so 0≤v0≤1. Half-angle substitution gives

    (1+z²)²(1+w²)g
      =b0(1−v0)³+3b1 v0(1−v0)²
         +3b2 v0²(1−v0)+b3 v0³,                   (27)

where

    b0=z³(1+z²)²,
    b1=(1+z²)(1+z+z²)(3z²−2z+1)/3,
    b2=2z(2z⁴−z³+5z²−3z+3)/3,
    b3=4z(z²−z+1).

Every coefficient is positive. In b1, 3z²−2z+1=3(z−1/3)²+2/3. In b2, the last factor is greater than 3−3z−z³≥53/27 on 0<z<1/3. The other two signs are immediate. The nonnegative cubic basis functions in (27) sum to 1. Thus g>0 on the entire interval, including both endpoints. Equations (26),(27) rule out all these directions.

### 4.3. Directions pi/3≤phi≤pi/2

Still alpha>0,beta≥0, so upper_W(c,s)>alpha(1−t/2). If c>0, then s/c≥sqrt(3)>3/2, giving

    alpha(1−t/2)>c(d+3t/2)(1−t/2)>c.               (28)

Indeed d>4/5,t<3/5, and

    (d+3t/2)(1−t/2)−1
      =−t²/(1+d)+t(3/2−d/2)−3t²/4
      ≥t−47t²/36>13t/60>0.

If c=0, the same full W support is strictly positive because alpha=t>0. But the actual strict point A_C=(1,0) gives lower_C(c,s)<c in every direction. This contradicts (28), including its c=0 endpoint.

Every possible separating normal between the actual W and C has been ruled out. This contradicts their disjoint interiors and completes Theorem 1. All genuine-wall and exterior-face inequalities stayed weak; strict contradictions arose from the owned points and a>1. No segment beginning at M occurred anywhere in the proof. ∎

## 5. Exact application to both remaining C974 roots

The prior continuous reductions leave the same two final central pairs:

    Q6=327936, Q7=131200 or131232.

Their actual top label is16392; the actual bottom and left owners have their proved origins. The original C974 entrance and its two exhaustive missing-corner roots are reproduced in `C974-ORIGINAL-ENTRANCE.txt`. That retained entrance, rather than any new enumeration, supplies the two strict singleton hulls used below.

Apply Theorem 1 in the two simultaneous isometries shown in the table.

| Theorem datum | First root: Q0 excludes (1,1), map (x−1,y−1) | Second root: Q0 owns (1,1), Q1 excludes it, map (y−1,x−1) |
|---|---|---|
| Actual singleton K | Q0 | Q1 |
| Its P,A,S | (1,.914),(1.82,1),(1.96,.76) | (.914,1),(1,1.82),(.76,1.96) |
| Its excluded E | (1,1), present root | (1,1), present root |
| Actual adjacent wall W | Q9 | Q8 |
| Its O | (2,1), uniform bottom origin | (1,2), proved in `C974-LEFT-ORIGIN-AND-MIDPOINT.md`, Section 2 |
| Its P_W,R | (2,.914),(2.8,1) | (.914,2),(1,2.8) |
| Its excluded M | (2.35,1.65), actual Q6 marker | (1.65,2.35), globally absent marker |
| Its excluded F0 | (2,1.5), actual Q5 | (1.5,2), actual Q5 |
| Its excluded F1 | (3,1.5), actual Q6 | (1.5,3), actual Q11 |
| Actual paired corner C | Q2 | Q4 |
| Its A_C | (3,1), actual paired-corner point | (1,3), actual paired-corner point |
| C excludes F1 | Same actual Q6 point | Same actual Q11 point |
| K's lower wall | Original y≥0 | Original x≥0 |
| C's two walls | Original x≤4,y≥0 | Original y≤4,x≥0 |

The first-column origins, strict crosspoints and strong bottom reach have their completed exact sources in `MISSING-CORNER-WALL-SIGN.md`, Section 2, and `C974-C976-CENTRAL-CROSSPOINTS.md`, Sections 5 and 8. The second-column top exclusion, left origin, strong left reach and actual Q5 crosspoint are mapped explicitly in `C974-LEFT-ORIGIN-AND-MIDPOINT.md`, Sections 1–3. The strict singleton points are precisely the retained missing-corner consequences in those respective roots.

The point M has no assumed owning square: in the first column it is excluded because Q6 owns it, while in the second it is excluded because it is globally absent. No owner has been changed between columns. The same actual paired corner supplies A_C, its real walls, and the exclusion of F1 in each application.

Thus Theorem 1 contradicts each of the two exhaustive missing-corner roots, for each of the two remaining central pairs. Combined with the preceding audited continuous branch reductions, this completes the entire retained C974 family. No final finite angle or terminal-domain certificate remains for that family.
