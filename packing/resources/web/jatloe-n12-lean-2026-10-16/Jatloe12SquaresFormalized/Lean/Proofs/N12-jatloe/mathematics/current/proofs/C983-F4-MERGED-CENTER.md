# C983 F4: the actual singleton forces the merged center

All decimals are exact rationals. Every owned point is strict in its one actual square. Foreign points and supports may be tangent. We use the original common side 1<a≤1001/1000 and the actual container walls.

**Theorem.** In every remaining C983 configuration in which merged Q7 owns F4, the point (2,2) is strictly in this same Q7.

For Q7=8240 this already follows from the four-band comparison in Section8 of `C983-F4-CENTRAL-REDUCTION.md`. That chapter also proves the conclusion for every nonpositive canonical angle of either remaining F4 label. The proof below deals with the positive canonical case by comparing the whole actual Q7 and Q1. No southwest point (2,1.5) is assumed.

## 1. The actual entrance and a putative missing center

Use `C983-F4-LEFT-ORIGIN-AND-CORNER-ROOT.md`. Its completed root reduction puts E=(1,1) strictly in actual Q1. Its new left origin (1,2) is strict in actual Q8. Q1 also retains its original strict marker (.914,1), F0=(1,1.74), and singleton seed (.76,1.87). Q1 excludes (1,.914), the original marker in the distinct actual Q0.

Translate by (−2,−2), and write W=Q7, K=Q1. The points needed below are:

| Point | Actual strict owner |
|---|---|
| P=(−.35,−.35), Q=(−.35,.35), F=(0,−.26), D=(−.26,0) | W: its two original markers and F4,G3 |
| E=(−1,−1), A=(−1,−.26), S=(−1.24,−.13), P_K=(−1.086,−1) | K: the proved corner, F0, singleton seed and original marker |
| L=(−1,0) | Actual Q8: the proved left origin |
| P_0=(−1,−1.086) | Actual Q0: its original marker |

The whole segment {−1}×[−1,−.26] is strict in K by convexity of its strict E,A. K has its genuine wall x≥−2.

Suppose W has a nonnegative canonical frame

    u_W=(d,r), v_W=(−r,d), d≥r≥0, d²+r²=1,

and suppose its center point O=(0,0) is missing. Write U,V for W's lower faces and A_W=U+a,H_W=V+a for its upper faces. At O, the lower u band follows from P, the lower v band from F, and the upper v band from Q. Therefore

    A_W≤0, U≤−a<−1.                                  (1)

The excluded L has its upper u band from F and its lower v band from P. A lower u exit of L would combine with (1) to give a≤d≤1. Hence L is upper v:

    H_W≤r.

Strict Q gives H_W>.35(d+r), so

    r/d>7/13.                                         (2)

This already excludes r=0.

## 2. The actual singleton bar leaves a narrow angle interval

At the foreign A=(−1,−.26), the upper u band follows from F, with increment d>0, and the lower v band follows from P, with increment .65r+.09d>0. Thus A is lower u or upper v.

Suppose first that it is upper v, H_W≤r−.26d. Strict Q would give

    r/d>61/65.                                        (3)

Consider the closed leftmost vertex

    Z=(dU−rH_W, rU+dH_W).

Inequality (3) implies d>7/10, r>13/20, and d+r>27/20. Using (1) and H_W>.35(d+r),

    Z_x<−d−.35r(d+r)
       <−[.7+.35(.65)(1.35)]<−1.                    (4)

Put h=r/(1+d)=(1−d)/r. Since r>.65 and 1+d≤2, (3) also gives h>.325>.26. The upper-v cap at A now yields

    Z_y≤−ar+d(r−.26d)
       <−r(1−d)−.26d²
       =−.26−r²(h−.26)<−.26.                       (5)

For its lower ordinate, strict F gives U>−.26r−a, while strict Q gives H_W>.35(d+r). Thus, using a≤1.001, r<5/7, r²≤1/2, and d(d+r)≥d²≥1/2,

    Z_y>−ar−.26r²+.35d(d+r)
       >−1.001(5/7)−.13+.175=−.67>−1.             (6)

The strict W point P has x>−1 and y=−.35. Equations (4)–(6) show that the segment from P to Z crosses the whole actual K bar {−1}×[−1,−.26] at a point before Z. That point is strictly inside W, because it is a proper convex combination of a strict W point and a closure point. Its ordinate is strictly between the bar endpoints. It is also strict in actual K, a contradiction.

Therefore A is lower u. In conjunction with (1),

    U≥−d−.26r,
    1<a≤d+.26r.

The half-angle identity d+.26r−1=2h(.26−h)/(1+h²), together with (2), proves

    1/4<h=r/(1+d)<13/50.                            (7)

Indeed the tangent at h=1/4 is8/15<7/13. In particular, throughout the remaining proof,

    d>.87, .47<r<.49,
    d+r>1.35, d−r>.38.                              (8)

The exact endpoint values are d>2331/2669, r<1300/2669, and r>8/17. The sum d+r increases throughout this canonical range and is greater than23/17>1.35.

## 3. The exhaustive actual separating directions

Orient a separating normal n from K toward W. Strict A∈K and F∈W have difference (1,0), while strict E∈K and P∈W have difference (.65,.65). Hence

    n_x>0, n_x+n_y>0.                                (9)

The separating-axis theorem supplies an actual edge normal of one of the two squares. The W direction −v_W=(r,−d) fails (9), so only u_W remains from W.

If K has a nonnegative canonical frame (b,t),(−t,b), b≥t≥0, its direction (t,−b) also fails (9). Its only remaining direction is (b,t). Thus this sign of K has only two candidates, u_W and u_K.

If K has a nonpositive canonical frame (b,−t),(t,b), both displayed K directions may be retained. In that sign we must exclude u_W,u_K,v_K. Retaining a candidate with a zero first component only enlarges the list; the support contradictions below include that endpoint.

Write p=atan(r/d) and q=atan(t/b). All comparisons below use actual full square supports and keep both relative-angle orders.

## 4. A nonnegative K: its wall and foreign marker give an exact support minimum

For the next two sections use coordinates centered at E instead of O, so K's strict points become

    E=(0,0), P_K=(−e,0), A=(0,.74), S=(−.24,.87),
    e=43/500=.086,

and its foreign P_0 is (0,−e). Its actual wall is x≥−1. Let L_K,V_K be its lower face values and J=L_K+a,H=V_K+a its upper values in this E chart.

In the nonnegative frame u_K=(b,t),v_K=(−t,b), the lower u band of P_0 follows from P_K, with increment e(b−t)≥0. Its upper u and upper v bands follow from E. Hence P_0 must leave through lower v:

    V_K≥−eb, H≥a−eb.

The genuine left wall gives

    bL_K−tH≥−1,
    J≥a+(tH−1)/b.                                  (10)

For n=u_W=(d,r), put k=db+rt>0. If q≤p, set η=rb−dt≥0. Then the full K support is kJ+ηH. Eliminating J with (10), the coefficient of H is kt/b+η=r/b. Consequently, since a>1,

    upper_K^E(u_W)
       ≥a(k+r/b)−k/b−er
       >B_−(q):=k+(r−k)/b−er.                     (11)

Here the superscript E denotes the current E-centered chart. If q≥p, put γ=dt−rb≥0. The full support is kJ−γV_K=kJ−γH+aγ. The same elimination, again with coefficient r/b, gives

    upper_K^E(u_W)
       >B_+(q):=k+γ+(r−k)/b−er.                   (12)

These two exact scalar bounds attain their common minimum at q=p. Indeed

    B_−=d(b−1)+r[t+(1−t)/b−e],
    B_−'=−dt+r[b−1+t/(1+t)]≤(r−d)t≤0,

where b−1≤0 and t/(1+t)≤t. Also

    B_+=(d−r)b+(d+r)t−d+r(1−t)/b−er,
    B_+'=d(b−t)+r[b+t−1/(1+t)]≥0.

The last two summands are nonnegative because b≥t, b+t≥1, and 1/(1+t)≤1. At the joining angle b=d,t=r, both bounds equal

    B_p=1+(r−1)/d−er.                              (13)

The margin above d+r−1 is strictly positive. With h from (7), the exact identity is

    d[B_p−(d+r−1)]
       =r P(h)/(1+h²),
    P(h)=−2h³+(1043/500)h²−43/500.                 (14)

On 1/4≤h≤13/50, P'(h)=2h(1043/500−3h)>0, and

    P(1/4)=21/1600>0.                              (15)

Thus (11)–(15) prove upper_K^E(u_W)>d+r−1. Changing back to the O chart subtracts d+r, so

    upper_K^O(u_W)>−1.

But lower_W(u_W)=U≤−a<−1 by (1). This contradicts separation and rules out the W normal for every nonnegative K angle.

## 5. A nonnegative K cannot separate by its own normal either

From (10), in the E chart,

    J≥a(1+t/b)−1/b−et>1+(t−1)/b−et.

Changing to the O chart gives the lower bound

    upper_K^O(u_K)>L(q),
    L(q)=1−b−t+(t−1)/b−et.                         (16)

We compare this with the full W lower support.

### 5.1. The order q≤p

Put k=db+rt, η=rb−dt≥0. By (1) and strict Q,

    lower_W(u_K)=kU−ηH_W
                  <−k−.35η(d+r).

Define

    A_−=d+.35r(d+r),
    B_−=r−1−e−.35d(d+r).

The exact difference after multiplication by b is

    b[L(q)+k+.35η(d+r)]
       =G_−(q)
       =b+t−2+A_−+(1−A_−)t²+B_−bt.                (17)

Here A_−>1, because 1−d=hr and h<.26<.35(d+r). Also B_−<−1: by (8),

    r−.35d(d+r)<.49−.35(.87)(1.35)
                        =.078925<e.

It follows on the whole canonical interval that

    G_−'=b−t+2(1−A_−)bt+B_−(b²−t²)
          ≤(b−t)(1−b−t)≤0.

Thus G_−(q)≥G_−(p). At q=p, k=1 and η=0, so

    G_−(p)=d[L(p)+1]=d[B_p−(d+r−1)]>0

by (14),(15). Equations (16),(17) therefore give upper_K^O(u_K)>lower_W(u_K), contradicting separation.

### 5.2. The order q≥p

Put γ=dt−rb≥0. Strict P gives V<−.35(d−r), so the full W lower support obeys

    lower_W(u_K)=kU+γV
                 <−k−.35γ(d−r).

Set

    A_+=d−.35r(d−r)<1,
    B_+=r−1−e+.35d(d−r)>−.6.

The last inequality follows explicitly from (8):

    B_+>.47−1.086+.35(.87)(.38)
         =−.50029>−.6.

The exact analogue of (17) is

    b[L(q)+k+.35γ(d−r)]
       =G_+(q)
       =b+t−2+A_++(1−A_+)t²+B_+bt.                (18)

Its derivative satisfies

    G_+'≥(b−t)[1−.6(b+t)]+2(1−A_+)bt≥0,

since b+t≤sqrt(2)<5/3. Thus G_+(q)≥G_+(p), and its value at p is again the positive margin (14),(15). The same strict support contradiction follows. Both relative-angle orders, including their common endpoint, have been exhausted.

## 6. A nonpositive K: both of its normals fail directly

Give K its nonpositive canonical frame u_K=(b,−t),v_K=(t,b). The following comparisons use the O chart for W and the displayed original K points from Section1.

For n=u_K, put k=db−rt>0 and η=rb+dt>0. These signs hold because p<2atan(13/50) and q≤pi/4, so p+q<pi/2. By (1) and strict Q,

    lower_W(u_K)=kU−ηH_W<−k−.35η(d+r).

Strict E=(−1,−1) in K gives upper_K(u_K)>−b+t. The difference between this K point value and the last W bound is

    b[d−1+.35r(d+r)]
       +t[1−r+.35d(d+r)]>0.                       (19)

The first bracket equals r[.35(d+r)−h]>0 by (7), and the second is positive because r<1. Hence this normal cannot separate.

For n=v_K=(t,b), its components in W's frame are

    α=dt+rb>0, β=db−rt>0.

By (1) and strict P,

    lower_W(v_K)=αU+βV<−α−.35β(d−r).

Strict S=(−1.24,−.13) in K gives upper_K(v_K)>−1.24t−.13b. The difference from the last W bound is

    bB_0+tT_0,
    B_0=r+.35d(d−r)−.13>0,
    T_0=d−.35r(d−r)−1.24<0.

Since b≥t, it is at least b(B_0+T_0), and

    B_0+T_0=d+r−1.37+.35(d−r)²
       >1.35−1.37+.35(.38)²=.03054>0.             (20)

Thus the second K normal also fails, including the retained t=0 endpoint.

## 7. A nonpositive K cannot separate by the W normal

Use the E-centered chart for K once more. Its upper faces J,H satisfy J>0 by strict E, and H>.87b−.24t by strict S=(−.24,.87). The latter quantity is positive, since b≥t. For n=u_W, the two frame components are k=db−rt>0 and η=dt+rb>0. Its full support consequently obeys

    upper_K^E(u_W)=kJ+ηH
                    >(dt+rb)(.87b−.24t).          (21)

For fixed p, the right side is a concave function of q on [0,pi/4]. Its exact expansion is

    .435r−.12d
       +(.435r+.12d)cos(2q)
       +(.435d−.12r)sin(2q).

Both nonconstant coefficients are positive, so its second derivative is nonpositive on this interval. Subtract d+r−1. At q=0 the result is

    1−d−.13r=r(h−.13)>0.

At q=pi/4 it is

    1−.685(d+r)≥1−.685sqrt(2)>0,

where the final exact squared comparison is2·137²<200². Concavity puts the entire function above the chord joining these two positive endpoints. Hence (21) gives upper_K^E(u_W)>d+r−1. In the O chart this is upper_K(u_W)>−1, again opposite to lower_W(u_W)≤−a<−1.

Every actual normal for both signs of K has now failed. This contradicts the disjoint open interiors of the actual Q1 and Q7. The putative missing O was therefore impossible. Together with the already proved nonpositive W comparison, this proves the theorem for every orientation. All exterior alternatives and bar contacts were weak until the strict point or a>1 supplied the contradiction. ∎

## 8. Scope

The theorem supplies (2,2) in the one actual merged Q7 throughout the remaining F4 configurations. Its new positive-angle proof depends on the proved left origin and the proved Q1 ownership of (1,1); it does not assume a favorable singleton angle. The surviving Q0-missing root and the full C983 ending still require their final contradiction. Neither the bottom origin nor the different merged point (2,1.5) is claimed here.
