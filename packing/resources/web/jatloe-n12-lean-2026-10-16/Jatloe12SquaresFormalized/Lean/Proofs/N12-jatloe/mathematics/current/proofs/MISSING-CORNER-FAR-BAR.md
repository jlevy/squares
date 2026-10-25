# A far paired-corner segment replaces the missing wall origin

All decimals are exact rationals. Owned points are strict; excluded points and whole segments may touch square boundaries. The actual squares in a support comparison have common side a>1. The theorem below does not assume a strict origin in the wall square.

## 1. The local statement

**Theorem 1.** Let K,W be open squares of common side a>1 with disjoint interiors. Suppose K has closure in y≥−1, strictly owns

    P=(0,−.086), A=(.82,0), S=(.96,−.24),

and excludes E=(0,0). Suppose W strictly owns

    P_W=(1,−.086), R=(1.8,0),

excludes the three points

    M=(1.35,.65), F0=(1,.5), F1=(2,.5),

and excludes the whole segment

    I={2}×[−.086,0].

Then W has a strictly positive canonical angle. The entire segment I is a premise; replacing it by its two endpoint exclusions is not the assertion proved here.

### 1.1. Frames and forced nonpositive-W faces

The complete orientation argument in Section 1.1 of `MISSING-CORNER-WALL-SIGN.md` uses only the stated K data. It puts every possible K into a frame

    u_K=(l,h), v_K=(−h,l), l>0, h>0, l²+h²=1.

Write U,V for its lower faces and B=V+a. Then

    U<−.086h<0, B≤0,
    hU+lB≥al−1.                                      (1)

The last inequality is precisely the genuine lower wall. Set x=h/(1+l)=(1−l)/h>0.

Suppose W has nonpositive canonical frame

    u_W=(d,−t), v_W=(t,d), d≥t≥0, d²+t²=1.

For W's face coordinates translate by (−1,0). Its strict points are now P_W=(0,−.086), R=(.8,0). Write L,H for its lower faces and J=L+a, T=H+a for its upper faces. The foreign S is (−.04,−.24), and M,F0,F1 become (.35,.65),(0,.5),(1,.5).

Both upper bands of S are strict. For u compare with R; for v compare with P_W, with positive gap .04t+.154d. Thus S is lower u or lower v. If it were lower v, H≥−.04t−.24d. The upper u band and lower v band of M follow from R,P_W. An upper v exit at M would imply

    a≤.39t+.89d≤sqrt(.9442)<1.

So M would be lower u, L≥.35d−.65t. Both lower bands of C=(1,0), the upper endpoint of I in this chart, follow from R. If C were upper u the width would be at most .65(d+t)<1. Thus C would be upper v, T≤t, giving

    a≤1.04t+.24d≤1.28/sqrt(2)<1.

These contradictions force S lower u. Comparing with strict P_W gives

    L≥−.04d+.24t,
    0≤t/d<20/77.                                     (2)

The same separate point argument as in Section 1.2 of `MISSING-CORNER-WALL-SIGN.md` now gives

    T≤t+.5d.                                         (3)

For completeness, F0 has its upper u and lower v bands strict by R,P_W, so is lower u or upper v. F1 has both lower bands strict by R; the u comparison is .2d−.5t>0 by (2). Thus F1 is upper u or upper v. If neither were upper v, their opposite u faces would have distance d≤1<a. Therefore one is upper v, which proves (3). No common owner for F0,F1 is used.

### 1.2. The actual far segment gives two alternatives

Apply the elementary separating-axis principle to the actual square W and the whole vertical segment I. Direct the normal from W toward I. The strict point R and the segment endpoint (2,0) force its first coordinate positive. The possible directions are therefore u_W,v_W and (1,0). In W's translated chart they give, respectively,

    J≤d,   T≤t−.086d,   dJ+tT≤1.                   (4)

The last inequality is the full rightmost support of W. The middle alternative contradicts the strict R: it would require

    .8t<T≤t−.086d,
    t/d>43/100>20/77.

Thus the complete remaining alternatives from the actual foreign segment are

    J≤d,  or  dJ+tT≤1.                              (5)

Tangency to an endpoint or to the interior of I is included in these weak support alternatives.

### 1.3. Three possible K–W directions

Let a separating normal n point from K to W. The strict pair P,P_W has horizontal difference (1,0), so n_x>0. The pairs A,P_W and S,P_W give

    −20/77<n_y/n_x<90/43.                            (6)

By (2), the W direction v_W has slope greater than 77/20 when t>0 and has first coordinate zero when t=0. It cannot satisfy (6). Thus the full list of possible actual square normals is

    u_W, u_K, −v_K.

We exclude all three, using each actual support rather than a center approximation.

## 2. The direction u_W is impossible

Put κ=ld−ht and σ=lt+hd>0. Then u_W=κu_K−σv_K.

If κ≥0, (1) gives

    upper_K(u_W)
      =a(κ+σ)+κU−σB
      ≥a(κ+σ+κl/h)−κ/h.                            (7)

First suppose J≤d in (5). The lower W support is d+L≤2d−a. Comparing this with (7) and using a>1 would require

    1−d+(1−h)(dx+t)<0.                             (8)

The exact simplification used here is

    κ(1−x)+σ−d=(1−h)(dx+t).

All terms on the left of (8) are nonnegative, a contradiction.

If instead dJ+tT≤1, the strict R gives T>.8t and hence

    J≤(1−.8t²)/d=d+.2t²/d.

So the lower W support is at most 2d+.2t²/d−a. The same comparison, still using a>1, would require

    1−d−.2t²/d+(1−h)(dx+t)<0.                      (9)

But

    1−d−.2t²/d=t²(.8d−.2)/[d(1+d)]≥0,

since d≥1/sqrt(2)>1/4. This again contradicts (9).

If κ<0, (1) gives instead

    upper_K(u_W)=κU+σ(a−B)>σ.

Moreover

    σ−d=l[t−dl/(1+h)]>0,

because κ<0 implies t>ld/h. In the first alternative of (5), the lower W support is at most 2d−a<d. In the second it is at most 2d+.2t²/d−a<d, by a>1 and the nonnegative expression just displayed. Both contradict upper_K(u_W)>σ>d. Thus every κ sign is covered.

## 3. The direction −v_K is impossible

Put n=−v_K=(h,−l), and define

    κ=hd+lt>0, η=ht−ld.

Here n=κu_W+ηv_W, while its upper K support is a−B≥a>1.

If J≤d, then L≤d−a<0. Strict P_W gives H<−.086d<0, and strict R gives T>.8t≥0. According as η≥0 or η<0, the lower W support is

    h+κL+ηH,  or  h+κL+ηT.

In either case it is less than h<1. This cannot separate W from K.

Suppose instead dJ+tT≤1. Since L≤(1−tT)/d−a and η−κt/d=−l/d, the case η<0 gives

    lower_W(n)
      ≤h+κ/d−aκ−(l/d)T
      <h(2−d)+lt(.2/d−1).                           (10)

The case condition says l>ht/d. The coefficient t(.2/d−1) is nonpositive. Substituting this bound in (10) yields

    lower_W(n)<h[9/5−1/d+1/(5d²)].                  (11)

If η≥0, use H=T−a to obtain instead

    lower_W(n)
      ≤h+κ/d−a(κ+η)−(l/d)T
      <h(2−d−t)+l(d−t+.2t/d).                      (12)

Now l≤ht/d, and the coefficient d−t+.2t/d is nonnegative. Substitution again gives (11). These strict bounds use a>1 and T>.8t; they include η=0 and t=0 wherever those case conditions permit.

Finally, with w=1/d∈[1,sqrt(2)],

    9/5−1/d+1/(5d²)
      =1−(w−1)(4−w)/5≤1.

Thus the lower W support is less than h<1 in every subcase, whereas the upper K support exceeds 1. This rules out −v_K.

## 4. The direction u_K is impossible

If this direction survives the cone (6), then h/l<90/43. Consequently

    0<x<2/3,
    κ=ld−ht>0, σ=lt+hd>0,                         (13)

where positivity of κ uses (h/l)(t/d)<(90/43)(20/77)<1. Its actual supports satisfy

    upper_K(u_K)≥a(1+l/h)−1/h,
    lower_W(u_K)=l+κL+σH.                           (14)

### 4.1. The upper-u alternative from the far segment

If J≤d, combine L≤d−a and H≤t+.5d−a with (14). Separation and a>1 would force

    F=1−l−x+κ(1−d)+σ(1−t−.5d)<0.                  (15)

This is exactly the continuously positive scalar proved in Section 1.6 of `MISSING-CORNER-WALL-SIGN.md`. To identify the reused argument precisely, put y=t/(1+d), so 0≤y<1/7. Its exact rational numerator is

    (1+x²)(1+y²)²F
      =x²(2−x)+y(1−4x−x²)
       +y²(−2x³+6x²−2)
       +y³(−3x²−4x+3)
       +y⁴(−x³+4x²−4x−2).

On the whole rectangle 0<x≤2/3,0≤y≤1/7 that proof gives

    (1+x²)(1+y²)²F
      ≥(25/21)(x−42y/25)²+(14/75)y>0

when y>0. At y=0 the exact numerator is x²(2−x)>0. Hence (15) is impossible.

### 4.2. The horizontal support alternative from the far segment

If dJ+tT≤1, use (3) and the identity σ−κt/d=h/d to get

    lower_W(u_K)
      ≤l+κ/d−a(κ+σ)+(h/d)T
      ≤2l+.5h−a(κ+σ).

Combining with (14) and a>1 would require

    F0=−x(1−h)+l(d+t−1)+h(d−t−.5)<0.              (16)

This expression is nonnegative over the whole required angle domain. Indeed (2) implies 0≤t<20/77<7/25. With d=sqrt(1−t²), F0 is a concave function of t because the coefficient of d is l+h>0. It suffices to bound its two endpoint values on the enlarged interval [0,7/25].

At t=0,d=1,

    F0=.5h−x(1−h)≥0,

since x(1−h)=h(1−h)/(1+l)≤h/2 follows from l+2h≥1.

At t=7/25,d=24/25,

    F0=(6/25)l+(9/50)h−x(1−h)>1/200.             (17)

For the exact final inequality, l+h≥1 gives the first two terms at least 9/50. Also 1+l≥2−h, so

    x(1−h)≤h(1−h)/(2−h)<7/40.

The last strict inequality follows from the complete square identity

    40h²−47h+14=40(h−47/80)²+31/160>0.

Thus (17) has the margin 9/50−7/40=1/200. Concavity now puts F0 above the chord between these two nonnegative endpoint values. This contradicts (16).

Every actual K–W separating direction is impossible under the assumed nonpositive W angle. This proves Theorem 1 continuously, including the axis, the canonical diagonal, all relative-angle sign changes, and all tangencies to the far segment. ∎

## 5. Exact C974 application to the second missing-corner root

The retained entrance in `C974-ORIGINAL-ENTRANCE.txt`, Section 4, has two exhaustive roots. Consider the second: E=(1,1) is strict in Q0 and excluded from Q1. Its coordinate-exchanged missing-corner lemma gives strict (1,1.82),(.76,1.96) in the actual Q1.

Use the isometry

    (x,y)↦(y−1,x−1).

It transposes the orientation sign. Every local premise above has the following exact source:

| Local role | Original point or square | Actual owner/source |
|---|---|---|
| K | Left-bottom singleton Q1 | Its genuine x≥0 wall becomes local y≥−1 |
| P | (.914,1) | Original Q1 marker |
| A,S | (1,1.82),(.76,1.96) | Retained missing-corner lemma for this actual Q1 |
| E | (1,1) | Excluded in the current root |
| W | Left wall Q8 | Distinct actual square |
| P_W | (.914,2) | Original Q8 marker |
| R | (1,2.8) | Actual Q8 strong wall reach |
| M | (1.65,2.35) | Globally absent northwest marker in C974 |
| F0 | (1.5,2) | Strict in actual Q5; transposed retained crosspoint map in `C974-C976-SW-SUPPORT-POINT.md`, Section 8 |
| F1 | (1.5,3) | Strict in actual Q11's single-owner segment [1.44,2]×{3} |
| Whole I | [(.914,3),(1,3)] | Entirely strict in the one actual paired corner Q4 |

The top segment in the F1 row uses Q11's established strict points (1.44,3),(2,3). The short corner segment in the final row uses Q4's two original paired-corner points; no outward corner extension is needed.

Theorem 1 gives a strictly positive angle in this transposed chart. Therefore the original actual left wall satisfies

    Q0 owns (1,1), Q1 excludes (1,1)
      ⇒ θ_Q8<0.                                     (18)

This conclusion holds for both remaining C974 central pairs. It does not assume that Q8 owns (1,2). Combined with the first-root result in `MISSING-CORNER-WALL-SIGN.md`, the two genuine alternatives are now

    first root:  θ_Q0>0 and θ_Q9>0;
    second root: θ_Q8<0.

They are additional completed continuous reductions. A final C974 contradiction is not claimed in this chapter.
