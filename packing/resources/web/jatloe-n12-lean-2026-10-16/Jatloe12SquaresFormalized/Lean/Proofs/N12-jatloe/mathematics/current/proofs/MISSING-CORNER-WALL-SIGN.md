# A missing-corner singleton forces the adjacent wall angle

All decimals below are exact rationals. Points owned by an open square are strict. An excluded point may lie on its boundary. The two squares have the same side length; this is used in the actual support comparison. No upper bound on that length is needed.

## 1. The local theorem

**Theorem 1.** Let K and W be two open squares of common side a>1 with disjoint interiors. Suppose K has its closure in y≥−1, owns

    P=(0,−.086), A=(.82,0), S=(.96,−.24),

and excludes E=(0,0). Suppose W owns

    O=(1,0), P_W=(1,−.086), R=(1.8,0),

and excludes

    M=(1.35,.65), C=(2,0), F0=(1,.5), F1=(2,.5).

Then W has a strictly positive canonical angle. Equivalently, W cannot have a frame

    u_W=(d,−t), v_W=(t,d),  d≥t≥0, d²+t²=1.

The theorem uses the real lower wall of K. It does not require a wall for W, a prescribed center for either square, or a common owner for F0 and F1. The additional excluded point S of W comes from the actual owner K.

### 1.1. A frame for every orientation of K

For a positive canonical frame u=(c,s), v=(−s,c), c≥s≥0, the lower u band of E follows from P, its upper u band follows from A, and its lower v band follows from P. Hence exclusion of E forces the upper v face to be at most zero. If s=0 this contradicts the strict point A, whose v coordinate is zero. Thus s>0 in this case.

For a negative canonical frame u=(c,−s), v=(s,c), c≥s≥0, the upper u band of E follows from A, and both its v bands follow from P,A. Hence exclusion of E forces the lower u face to be at least zero. Again s=0 is impossible, now because P has u coordinate zero. Relabel the axes as u_K=(s,c), v_K=(−c,s). The new upper v face is the negative of the old lower u face.

Consequently every possible K admits a frame

    u_K=(l,h), v_K=(−h,l),
    l>0, h>0, l²+h²=1.

Write U,V for its lower face coordinates, and B=V+a for its upper v coordinate. The strict point P and the excluded E give

    U<−.086h<0,   B≤0.                              (1)

The genuine lower wall gives hU+lV≥−1, or

    hU+lB≥al−1.                                    (2)

Set x=h/(1+l)=(1−l)/h; this is positive.

### 1.2. A nonpositive W has a small angle and two upper caps

Suppose for contradiction that W has the nonpositive frame in the theorem. For this subsection translate W's coordinates by (−1,0), so its strict points are

    O=(0,0), P_W=(0,−.086), R=(.8,0),

and the excluded points become

    S=(−.04,−.24), M=(.35,.65), C=(1,0),
    F0=(0,.5), F1=(1,.5).

Let L,H be its lower face coordinates and J=L+a, T=H+a its upper coordinates in this translated chart.

At S, both upper bands are strict: the upper u band follows from R because .84d−.24t≥.60d>0, and the upper v band follows from O. Thus S is lower u or lower v.

If S were lower v, then H≥−.04t−.24d. At M its upper u band follows from R, and its lower v band follows from O. Thus M is lower u or upper v. The latter possibility would imply

    a≤.39t+.89d≤sqrt(.9442)<1.

Therefore M would be lower u, L≥.35d−.65t. Both lower bands of C follow strictly from R, so C is upper u or upper v. An upper u face at C would give

    a≤.65(d+t)≤.65sqrt(2)<1.

Hence C would be upper v, T≤t. Together with the assumed lower v face at S this gives

    a≤1.04t+.24d≤1.28/sqrt(2)<1.

The last expression is maximized at t=d on the canonical interval. This is another contradiction. Therefore S is lower u:

    L≥−.04d+.24t.

Comparing with the strict point P_W gives

    −.04d+.24t<.086t,
    0≤t/d<20/77.                                   (3)

At F0 its upper u band follows from R and its lower v band follows from O. Thus F0 is lower u or upper v. At F1 both lower bands follow from R: for u the difference is .2d−.5t>0 by (3), and for v it is .2t+.5d>0. Hence F1 is upper u or upper v. If neither were upper v, the opposite u faces at F0,F1 would give a≤d≤1. Thus at least one is upper v, and in either case

    T≤t+.5d,   H≤t+.5d−a.                          (4)

Keep also the exact two-face alternative at C:

    J≤d  or  T≤t.                                  (5)

Nothing here presumes that F0 and F1 have the same actual owner.

### 1.3. Only two actual separating axes can remain

For two squares with disjoint open interiors, there is a weak separating line whose normal is one of their actual face normals. Orient the normal n from K toward W. Strict ownership of A and O implies n_x>0. The pairs A,P_W and S,O also imply

    −1/6<n_y/n_x<90/43.                             (6)

The actual K direction −v_K=(h,−l) cannot separate: its upper support in K is −V=a−B≥a>1, whereas its lower support in W is strictly less than (−v_K)·O=h≤1. The other K direction with positive first coordinate is u_K.

Among W's directions, v_W=(t,d) cannot satisfy (6): if t>0 then d/t>77/20>90/43 by (3), and if t=0 its first coordinate is zero. The remaining possible W direction is u_W. Thus the complete list of surviving directions is u_K,u_W.

Define

    κ=ld−ht,   σ=lt+hd>0.

Then u_W=κu_K−σv_K and u_K=κu_W+σv_W. These are directions of the actual squares, so the following comparisons retain their entire supports.

### 1.4. The direction u_W is impossible

If κ≥0, the upper K support in this direction is

    upper_K(u_W)=κ(U+a)−σV
                 =a(κ+σ)+κU−σB.

Using (2), B≤0 and a>1 gives

    upper_K(u_W)
      ≥a(κ+σ+κl/h)−κ/h
      >κ(1−x)+σ.

The coefficient κ+σ+κl/h is positive, including κ=0. The exact identity

    κ(1−x)+σ−d=(1−h)(dx+t)>0                     (7)

shows that this support is greater than d. The lower W support is strictly less than u_W·O=d, so separation is impossible.

If κ<0, the upper K support instead is

    upper_K(u_W)=κU−σV=κU+σ(a−B)>σ,

by (1). Moreover

    σ−d=l[t−dl/(1+h)]>0,

because κ<0 implies t>ld/h>ld/(1+h). This again contradicts the strict point O in W. Thus u_W is excluded for every possible K orientation and every κ sign.

### 1.5. The direction u_K: the upper-v alternative at C

If u_K is a separator, (6) gives h/l<90/43. Hence

    0<x<2/3,                                      (8)

because h/l=2x/(1−x²) increases for 0<x<1 and is 12/5>90/43 at x=2/3. Combining this cone bound with (3) yields κ>0, since

    (h/l)(t/d)<(90/43)(20/77)<1.

Returning to the global chart of the theorem, W's lower support is therefore

    lower_W(u_K)=κ(d+L)+σ(t+H)
                 =l+κL+σH.                        (9)

Meanwhile (2) and B≤0 give the upper K support bound

    U+a≥a(1+l/h)−1/h>1−x=l−x(1−h).               (10)

First suppose (5) holds through T≤t, so H≤t−a. The strict point O gives L<0. Therefore

    lower_W(u_K)<l+σ(t−1).

By (3), t<1/3 and d>9/10, so

    σ(1−t)≥hd(1−t)>3h/5.

On the other hand,

    x(1−h)=h(1−h)/(1+l)≤h/2,

because l+2h≥l+h≥1. Thus (9) is strictly below (10). This rules out the upper-v alternative at C.

### 1.6. The direction u_K: the upper-u alternative at C

It remains that J≤d in (5), so L≤d−a. Together with (4), equations (9),(10) show that separation would require

    a(1+l/h+κ+σ)
      ≤l+κd+σ(t+.5d)+1/h.

The coefficient of a is positive. Since a>1, a necessary condition is

    F=1−l−x+κ(1−d)+σ(1−t−.5d)<0.                 (11)

Put y=t/(1+d). Bound (3) implies 0≤y<1/7: at y=1/7 one has t/d=7/24>20/77. In these variables

    l=(1−x²)/(1+x²),  h=2x/(1+x²),
    d=(1−y²)/(1+y²),  t=2y/(1+y²).

Direct rational substitution gives the exact identity

    F=P(x,y)/[(1+x²)(1+y²)²],                     (12)

where

    P(x,y)=x²(2−x)
           +y(1−4x−x²)
           +y²(−2x³+6x²−2)
           +y³(−3x²−4x+3)
           +y⁴(−x³+4x²−4x−2).

Here is one continuous positivity estimate on the entire enlarged rectangle 0<x≤2/3, 0≤y≤1/7. The coefficients of y²,y³,y⁴ are at least −2,−1,−5, respectively. For the first, use x²(6−2x)≥0; the second decreases to −1 at x=2/3; and for the third, 2+4x−4x²+x³≤2+8/3+8/27<5. Also

    2y²+y³+5y⁴≤(110/343)y≤y/3.

Consequently

    P≥x²(2−x)+y(1−4x−x²)−y/3
      ≥(25/21)x²−4xy+(2/3)y
      =(25/21)(x−42y/25)²+(2/3)y−(84/25)y²
      ≥(25/21)(x−42y/25)²+(14/75)y.               (13)

The second line uses 2−x−y≥4/3−1/7=25/21. If y>0 the final expression is positive. If y=0, the exact polynomial is x²(2−x)>0. Hence F>0, contradicting (11).

Both remaining actual separating directions are impossible. This completes the proof of Theorem 1. The proof includes t=0, all canonical-angle boundaries, κ=0 and weak exterior face contact. ∎

## 2. Exact C974 application

Retain the local ownership entrance and the two exhaustive missing-corner roots in `C974-ORIGINAL-ENTRANCE.txt`, Sections 1–4, reproduced from the original package. This result does not replace that entrance or the retained missing-corner lemma. Its Section 4 records the following actual consequence: if Q0 excludes E=(1,1), then Q0 strictly owns (1.82,1),(1.96,.76), in addition to its original point (1,.914). Every other exclusion required by that retained lemma is supplied by the original distinct owners.

Apply Theorem 1 with the translation (x,y)↦(x−1,y−1) and the following exact actual owners:

| Theorem role | Original point or square | Actual owner/source |
|---|---|---|
| K | Bottom-left singleton Q0 | Its genuine wall y≥0 becomes y≥−1 |
| P | (1,.914) | Original Q0 marker |
| A,S | (1.82,1),(1.96,.76) | Retained missing-corner consequence for this Q0 |
| E | (1,1) | Excluded in the present root |
| W | Bottom wall Q9 | Distinct actual owner |
| O | (2,1) | Uniform bottom-origin conclusion, `C974-C976-CENTRAL-CROSSPOINTS.md`, Section 8 |
| P_W | (2,.914) | Original Q9 marker |
| R | (2.8,1) | Actual Q9 strong bottom bar |
| M | (2.35,1.65) | Original southeast marker in Q6 |
| C | (3,1) | Actual paired southeast corner Q2 |
| F0 | (2,1.5) | Actual southwest Q5 crosspoint; complete source map in `ELBOW-CROSSPOINT.md` |
| F1 | (3,1.5) | Actual southeast Q6 crosspoint, `C974-C976-CENTRAL-CROSSPOINTS.md`, Sections 5 and 8 |

Every point in the final four rows is excluded from Q9 by its actual distinct strict owner. Theorem 1 therefore proves

    Q0 excludes (1,1)  ⇒  θ_Q9>0                  (14)

for both remaining C974 central pairs, southeast327936 with northeast131200 or131232. No southwest center point has been assumed.

The coordinate-exchanged theorem would apply to the other missing-corner root if actual Q8 were also known to own (1,2). That left-origin premise is not asserted here. Thus (14) is a completed additional reduction for the first missing-corner root; it is not by itself a full C974 exclusion.

## 3. The singleton has a strictly positive angle as well

**Theorem 2.** Under the hypotheses of Theorem 1, K also has a strictly positive canonical angle.

**Proof.** Theorem 1 puts W in a positive canonical frame

    u_W=(d,t), v_W=(−t,d), d≥t≥0, d²+t²=1.

We include t=0 in the argument below, though Theorem 1 already rules it out. Suppose that K has a nonpositive canonical angle. Its reindexed frame from Section 1.1 then satisfies

    0<l≤h<1, l²+h²=1,
    u_K=(l,h), v_K=(−h,l).

Retain K's U,V,B and its genuine wall inequalities (1),(2). Put x=h/(1+l) as before, so x≥sqrt(2)−1>2/5.

### 3.1. Two uniform upper caps for W

Translate W's point coordinates by (−1,0) as in Section 1.2, and again write L,H,J=L+a,T=H+a for its face positions in this chart. At F0=(0,.5), both u bands are strict by P_W,R, and its lower v band is strict by O. Hence

    T≤.5d.                                           (15)

At C=(1,0), the lower u band follows from R and the upper v band follows from O. Thus C is upper u or lower v. At M=(.35,.65), both lower bands are strict: compare with P_W in u and R in v. Therefore M is upper u or upper v.

If C were lower v and M upper v, their opposite faces would imply

    a≤.65(d+t)≤.65sqrt(2)<1.

Consequently either C is upper u, or M is upper u. In the latter case u(M)=.35d+.65t≤d. Thus in both cases

    J≤d.                                             (16)

These caps use the named excluded points separately; they require no extra foreign segment.

### 3.2. The two actual separating directions

For a normal directed from K to W, strict A,O give n_x>0, and strict S,O give n_y/n_x>−1/6. The K direction −v_K cannot separate by exactly the support comparison in Section 1.3. The W direction −v_W=(t,−d) cannot satisfy this strict cone bound: for t>0 its slope is at most −1, and for t=0 its first coordinate is zero. Thus only u_K and u_W remain.

Set

    κ=ld+ht>0, σ=hd−lt≥0.

The last inequality follows from h≥l and d≥t. Now u_W=κu_K−σv_K and u_K=κu_W+σv_W. Both formulas retain the complete actual square supports, including σ=0.

### 3.3. The direction u_W

Using (2) and B≤0,

    upper_K(u_W)
      =a(κ+σ)+κU−σB
      ≥a(κ+σ+κl/h)−κ/h.

By (16), the lower W support in the global chart is d+L≤2d−a. Hence separation, together with a>1, would force

    F1=1−d+(1−h)(dx−t)<0.                         (17)

Here the exact simplification is

    κ(1−x)+σ−d=(1−h)(dx−t).

If dx≥t, every term in F1 is nonnegative. If dx<t, use h≥1/sqrt(2)>7/10 and x>2/5 to obtain

    F1>1−d+(3/10)((2/5)d−t)
       =1−.88d−.30t
       ≥1−sqrt(.8644)>0.

Both cases contradict (17).

### 3.4. The direction u_K

In the global chart, the lower W support equals

    lower_W(u_K)=κ(d+L)+σ(−t+H)=l+κL+σH.

Bounds (15),(16) therefore imply

    lower_W(u_K)≤l+κd+.5σd−a(κ+σ).

The genuine K wall still gives U+a≥a(1+l/h)−1/h. Comparing these supports and using a>1 would require

    F2=κ(1−d)+σ(1−.5d)−x(1−h)<0.                  (18)

This last expression is positive throughout the entire two-angle domain. Indeed define

    A0=d(1−.5d)+t(1−d)>0,
    B0=.5d(4−3d−t).

The exact identity

    κ(1−d)+σ(1−.5d)=(h−l)A0+lB0                 (19)

has nonnegative first term. By Cauchy–Schwarz,

    3d+t≤sqrt(10)<13/4,  d≥1/sqrt(2)>7/10,

and consequently B0>21/80. On the other hand,

    x(1−h)=hl²/[(1+h)(1+l)]≤l/4,

because h/(1+h)≤1/2 and l/(1+l)≤1/2. Equations (18),(19) now give

    F2>21l/80−l/4=l/80>0,

a contradiction.

Both actual separating directions have been exhausted. The assumed nonpositive K orientation is therefore impossible. Axial K was already excluded in Section 1.1; the diagonal and the case σ=0 are included above. All exterior face inequalities remain weak. ∎

**Exact C974 consequence.** The owner mapping of Section 2 is unchanged. Thus both remaining central pairs satisfy the stronger implication

    Q0 excludes (1,1)  ⇒  θ_Q0>0 and θ_Q9>0.        (20)

This uses the actual Q0–Q9 square separation. It does not infer an angle for Q6 from its point exclusions alone.
