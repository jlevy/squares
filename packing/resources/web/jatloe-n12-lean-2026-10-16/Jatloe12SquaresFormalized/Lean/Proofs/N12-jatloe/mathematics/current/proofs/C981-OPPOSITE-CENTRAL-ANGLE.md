# C981: an exact angle bound from the two opposite central squares

All terminating decimals below are exact rational numbers. Owned points are strict; exclusions and separations may be weak. The first lemma requires only a>1. The second uses the original permitted cap a≤1001/1000. This chapter supplies the independently audited angle reduction used in the completed exclusions of representatives 29 and 104 in `C981-LAST-TWO-CYCLES.md`. The angle bound is a proved intermediate step; the final chapter supplies the full contradiction for every central-angle sign.

## 1. A small lower-face offset for the inward square

**Theorem 1.** Let A be an open square of side a>1 strictly owning

    P=(0,.26), D=(.26,0), M=(.35,.35).

Suppose A excludes O=(0,0), F=(.26,1), and the whole segment

    S={1}×[.26,.8].

Choose the positive-quadrant face frame

    u=cx+sy, v=−sx+cy, c,s≥0, c²+s²=1.

Writing its lower faces as e,V, one has c,s>0 and

    0≤e<17/500.                                         (1)

Every square orientation has such a positive-quadrant frame; no canonical ordering of c and s is required.

**Proof.** The upper u-band of O follows from M, and its two v-bands follow from D and P. If c=0 or s=0, one owned anchor also gives O's lower u-band, contradicting its exclusion. Thus c,s>0, and the only possible exclusion of O is e≥0.

Suppose e≥.034. Both F and R=(1,.26) have u-projection at most sqrt(1.0676), and

    1.0676<1.034²=1.069156.

Consequently both lie strictly below the upper u-face e+a. At F the lower u-band follows from P, and the lower v-band from D. At R the lower u-band follows from D, and the upper v-band from P. Their exclusions therefore force

    V+a≤c−.26s,    V≥−s+.26c.                           (2)

It follows that a≤.74(c+s). Put H=c+s. Since a>1,

    H>50/37.

In particular c,s>.46: if the smaller component were at most .46, the monotonicity of z+sqrt(1−z²) for 0≤z≤1/sqrt(2) would give

    H≤.46+sqrt(.7884)<.46+.89=1.35<50/37.

The rightmost closed vertex of A has x-coordinate

    X=c(e+a)−sV
      =ce+aH−s(V+a)
      >.034c+H−cs+.26s².                               (3)

We verify that the last expression is greater than one. The identity

    H−cs−1=−(1−c)(1−s)

reduces this to .034c+.26s²>(1−c)(1−s). If s≤.6, then c≥.8 and

    (1−s)/(1+c)<.54/1.8=.3,
    .034c≥.0272>.0144=.36(.3−.26)≥s²(.3−.26).

Using 1−c=s²/(1+c) proves the desired inequality. If s≥.6, the function

    f(s)=(1−s)/(1+sqrt(1−s²))

is decreasing, because its derivative has numerator s−sqrt(1−s²)−1<0. Thus f(s)≤f(.6)=2/9<.26, which proves the same inequality directly. Hence X>1.

Consider now J=(1,.56), which lies in S. Its lower u-band follows from D. Its upper v-band follows from P because .30c−s<0. Its lower v-band follows from the first inequality in (2):

    v(J)−V≥a−.44c−.74s
              >1−sqrt(.44²+.74²)>0.

Therefore J can fail only its upper u-band, giving

    e+a≤c+.56s.                                         (4)

By (2) and (4), every interior intersection of A with x=1 would have .26<y<.56. Such an intersection is forbidden by S. But A strictly owns P at x=0, while its closed rightmost vertex has x-coordinate X>1. The segment from P to that vertex meets x=1 in the open square. This is a contradiction. Thus e<.034=17/500. ∎

## 2. The opposite ordinary central square cannot have a large positive angle

**Theorem 2.** Let A satisfy Theorem 1, and let C be an open square of the same side a, where

    1<a≤1001/1000.

Suppose the interiors of A and C are disjoint. Suppose C strictly owns

    O=(0,0), E=(−.5,0), D_C=(0,−.5), M_C=(−.35,−.35),

and excludes B=(−.35,.35), G=(.35,−.35), and both whole segments

    S_b=[−.8,−.26]×{−1},
    S_l={−1}×[−.56,0].

If C has positive canonical frame

    u_C=dx+ry, v_C=−rx+dy,
    0≤r≤d, d²+r²=1,

then

    r<8/25.                                             (5)

**Proof.** Write the upper C-face values as u,v, so its lower values are u−a,v−a. Strict ownership gives u,v>0. At B the lower u-band follows from M_C, the upper u-band from O, and the lower v-band from O. Therefore v≤.35(d+r). At G the lower u- and upper v-bands follow from O. A lower v-face exclusion would give

    a≤.7(d+r)≤.7sqrt(2)<1.

It is impossible, so

    u≤.35(d−r),    v≤.35(d+r).                          (6)

Assume r≥.32. In particular r>0, and the cap on a implies all numerical estimates below.

### 2.1. The bottom segment becomes a supporting line

At K=(−.26,−1), both upper bands follow from O. By (6),

    u−u_C(K)≤.61d+.65r≤sqrt(.7946)<1<a.

Thus K is strictly above the lower u-face, and its exclusion forces

    v−a≥.26r−d.                                        (7)

At J=(−.8,−1), both upper bands again follow from O. If J is excluded by the lower u-face, (7) shows that every interior intersection with y=−1 would have −.8<x<−.26, contrary to the whole excluded segment S_b. Since O lies above the line, convexity then puts the entire closed C in y≥−1.

If instead J is excluded by the lower v-face, then v−a≥.8r−d. Since u−a>−a, the minimum y-coordinate is

    r(u−a)+d(v−a)>−ar+.8dr−d²
                  =−1+r(r+.8d−a)>−1.

For the last inequality, the function r+.8sqrt(1−r²) increases on 0≤r≤1/sqrt(2). At r=.32 its cosine exceeds .947, so r+.8d>1.0776>1.001≥a. This proves in both alternatives that

    the closed square C lies in y≥−1.                  (8)

### 2.2. The left segment also becomes a supporting line

At J_l=(−1,−.56), the upper u-band follows from O and the upper v-band from E. Its lower v-band follows from (6), because

    v−v_C(J_l)≤.91d−.65r≤.91<1<a.

Its exclusion forces

    u−a≥−d−.56r.                                       (9)

At K_l=(−1,0), the upper u-band follows from O and the lower v-band from E. It therefore satisfies either u−a≥−d or v≤r. The second alternative, together with (9), confines every interior intersection with x=−1 to −.56<y<0, contradicting S_l. Since O is strictly to the right, this alternative puts the closed square in x≥−1.

We show that the first alternative u−a≥−d is impossible using the actual disjointness of A and C. It gives

    u≥a−d>1−d≥r²/2≥.0512.                             (10)

Use the positive-quadrant frame (c,s) of A and its lower face e from Theorem 1. On either transverse face normal (−r,d) or (−s,c), A has strict anchors on both sides of projection zero, while C strictly owns O. Neither axis can separate the squares. On either positive face normal (d,r) or (c,s), the reverse order A-before-C is impossible, again using O and the positive anchors of A. Thus only C-before-A on one of these two positive normals could separate them.

Put

    α=cd+sr>0, β=sd−cr.

The minimum A-support on (d,r) is at most e. Indeed its expression is αe−βV when β≤0, and αe−β(V+a) when β≥0. The strict anchors of A give V<−.26s<0<V+a, so in either expression the second term is nonpositive; also α≤1 and e≥0. Equation (10) and e<.034 exclude separation on (d,r).

For separation on (c,s), use v>.5r from E and v−a<−.5d from D_C. If β≥0, the maximum C-support is strictly bounded below by

    α(a−d)+β(.5r)
      =c(ad−1+.5r²)+s(ar−.5dr).                        (11)

The first coefficient is negative: since a−1≤.001,

    1−d−.5r²=r⁴/[2(1+d)²]≥.32⁴/8=.00131072>.001d.

The second coefficient is positive. Therefore (11) increases with the angle of (c,s) above the angle of (d,r). Its value at equality of the angles is a−d.

If β≤0, the corresponding lower bound is

    α(a−d)−β(.5d)
      =c(ad−d²+.5dr)+s(ar−rd−.5d²).                    (12)

Its first coefficient is positive. Its second is at most d(a−1.5d)<0, because d≥1/sqrt(2)>.7 and a≤1.001. Thus (12) decreases with the angle of (c,s) up to the angle of (d,r), and again has minimum a−d. These bounds remain weakly valid when β=0. Equation (10) therefore makes the maximum C-support greater than .0512, whereas A's minimum support on this same axis is e<.034. This excludes the final possible separator.

The alternative u−a≥−d is impossible. We have proved

    the closed square C lies in x≥−1.                  (13)

### 2.3. The two supporting lines contradict the small offset

Put H=d+r. From (8) and (13), both coordinates of the center of C are at least aH/2−1. Consequently the maximum C-support on any positive unit normal (c,s) is bounded below by

    c(ad−1)+s(aH−1),   if sd−cr≥0,
    c(aH−1)+s(ar−1),   if sd−cr≤0.                      (14)

Here ad−1<0, ar−1<0, and aH−1>0; for example r≥.32 gives d<.948 and hence ad<.949<1. The first expression increases with the angle above that of (d,r), and the second decreases up to that angle. The common minimum is

    a(1+dr)−H>1+dr−H=(H−1)²/2.                        (15)

Since H increases on the canonical interval and at r=.32 one has d>.947,

    (H−1)²/2>.267²/2=.0356445>.034.

Thus (14) is greater than .034 for every positive unit normal, including (d,r). By the same exhaustive separation argument used in §2.2, only the positive normals (d,r) and (c,s) can separate C from A. On the first, the minimum A-support is at most e<.034; on the second it equals e<.034. Equation (15) rules out both. This contradicts disjointness, so r<.32=8/25 as claimed. ∎

## 3. Exact entrance of C981 representatives 29 and 104

For representative 29, first rotate the entire actual configuration by (x,y)↦(4−y,x), and then translate by (−2,−2). Set A=Q5 and C=Q7. The common continuous entrance proved in `C981-COMMON-CYCLE.md` supplies the strict Q7 center and crosspoints, the strict Q8 segment {1}×[2.26,2.8], the strict Q9 segment [2.26,2.8]×{1}, and the strict Q11 segment [1.44,2]×{3}. Its center and wall-origin derivations do not use the unavailable Q10 point (3,2.56).

| Datum in Theorems 1–2 | Actual strict source before the rotation |
|---|---|
| A owns P,D,M | Q5: (2.26,2),(2,1.74),(2.35,1.65) |
| A excludes O | Q7: (2,2) |
| A excludes F=(.26,1) | Q10: (3,1.74), auxiliary 8 |
| A excludes the whole segment S | Q9: [2.26,2.8]×{1} |
| C owns O,E,D_C,M_C | Q7: (2,2),(2,2.5),(1.5,2),(1.65,2.35) |
| C excludes B | Q6: (2.35,2.35) |
| C excludes G | Globally absent marker (1.65,1.65) |
| C excludes the whole segment S_b | Q8: {1}×[2.26,2.8] |
| C excludes the whole segment S_l | Q11: [1.44,2]×{3} |

For representative 104, first transpose the entire configuration by (x,y)↦(y,x), and relabel actual squares by

    (Q̃0,Q̃1,Q̃2,Q̃3,Q̃4,Q̃5,Q̃6,Q̃7,Q̃8,Q̃9,Q̃10,Q̃11)
      =(Q1,Q0,Q4,Q3,Q2,Q7,Q6,Q5,Q9,Q8,Q11,Q10).

Its exact auxiliary sets then agree with the entrance used above:

    Q̃5={4,16}, Q̃6={7,17}, Q̃7={5,13},
    Q̃8={1,11}, Q̃9={6,15}, Q̃10={8,9,19}, Q̃11={3,14}.

The extra auxiliary 18 belongs to Q̃2; neither theorem uses it. In particular the ordinary-wall center theorem proves the actual center in Q̃7=Q5, not in Q̃5=Q7. Now apply the same rotation and translation, and put A=Q̃5, C=Q̃7. Every entry of the table applies literally to the relabeled actual owner.

The original shared model permits 1<a≤1001/1000 when needed; that is the explicit cap used in Theorem 2. No additional center, wall, or auxiliary owner is assumed. The rigorous common conclusion here is conditional on the sign: if the ordinary central square has a positive canonical angle, its sine is less than 8/25. `C981-LAST-TWO-CYCLES.md` joins this bound to the actual right-wall square and both central-angle endings, completing representatives 29 and 104 without any further entrance premise.
