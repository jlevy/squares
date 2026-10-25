# The missing-corner singleton owns the lower midpoint

All terminating decimals are exact rationals. A point owned by an open square is strict. Exterior points and separating faces may be tangent. All support comparisons below concern the two actual squares, of common side length a>1.

## 1. Local theorem

**Theorem 1.** Let K,W satisfy the hypotheses of Theorem 1 of `MISSING-CORNER-WALL-SIGN.md`. Explicitly, their open interiors are disjoint, K has its closure in y≥−1, K strictly owns

    P=(0,−.086), A=(.82,0), S=(.96,−.24),

and K excludes E=(0,0). The square W strictly owns

    O=(1,0), P_W=(1,−.086), R=(1.8,0),

and excludes

    M=(1.35,.65), C=(2,0), F0=(1,.5), F1=(2,.5).

Then K strictly owns

    Z=(1,−.5).

No wall for W, center sign, or further segment premise is needed.

### 1.1. The two positive frames and the wall support

Theorems 1 and 2 of `MISSING-CORNER-WALL-SIGN.md` apply with exactly these hypotheses. Both squares therefore have strictly positive canonical angles. Write

    u_K=(l,h), v_K=(−h,l), l≥h>0, l²+h²=1,
    u_W=(d,t), v_W=(−t,d), d≥t>0, d²+t²=1.

For K let U,V be its lower face coordinates and B=V+a its upper v coordinate. As proved directly from P,A,E and the genuine lower wall in that chapter,

    U<−.086h<0, B≤0,
    hU+lB≥al−1.                                      (1)

Set x=h/(1+l)=(1−l)/h. In particular,

    U+a≥a(1+l/h)−1/h>1−x.                           (2)

The strictness in (2) uses a>1 and the positive coefficient 1+l/h. It is preserved if the lower wall or the excluded point E is tangent.

For W's face coordinates, translate its chart by (−1,0). Its strict points are then (0,0),(0,−.086),(.8,0). Write L,H for its lower faces and J=L+a,T=H+a for its upper faces in this translated chart.

The short face arguments in Section 3.1 of the cited chapter give

    T≤.5d, J≤d.                                      (3)

Here are those arguments to make the precise input visible. At F0=(0,.5), both u bands and the lower v band are strict, by P_W,R,O, so F0 is upper v. At C=(1,0), the lower u band and upper v band are strict, so C is upper u or lower v. At M=(.35,.65), both lower bands are strict, so M is upper u or upper v. Lower v at C together with upper v at M would give a≤.65(d+t)<1. Hence either C or M is upper u; since u(M)=.35d+.65t≤d, this yields the second cap in (3).

The point S, strictly owned by the actual K, has W-chart coordinates (−.04,−.24). Both of its upper bands are strict. For the u band compare with P_W, with gap .04d+.154t>0; for the v band the gap from P_W is .154d−.04t>0. If S were lower v, then (3) would give

    a≤.74d−.04t<1.

Therefore S is lower u, and (3) now implies

    L≥−.04d−.24t,
    1<a≤1.04d+.24t,
    t/d<2/3.                                         (4)

For the last implication, the function (1.04+.24r)/sqrt(1+r²) is strictly decreasing for r≥2/3. Its value at r=2/3 is 3.6/sqrt(13)<1, since 3.6²=12.96<13. This proves the bound for the whole continuous angle interval.

### 1.2. A large K angle would leave only two separating directions

Suppose, for contradiction, that

    h/l≥3/4.                                         (5)

Then h≥3/5, l≤4/5 and x≥1/3. By (4), K's angle is strictly greater than W's. Thus

    κ=ld+ht>0, σ=hd−lt>0,
    u_W=κu_K−σv_K, u_K=κu_W+σv_W.                  (6)

For two squares with disjoint open interiors, a weak separating normal can be chosen among their actual face normals. Direct this normal n from K toward W. The strict pair A,O forces n_x>0. The strict pair S,O forces n_y/n_x>−1/6. Each remaining positive-x face normal −v_K or −v_W has slope at most −1, so it cannot separate. Therefore only

    n=u_W or n=u_K                                  (7)

can remain. This argument uses actual-square separation; it does not replace either square by its listed strict hull.

### 1.3. The direction u_W is impossible

By (1),(6),

    upper_K(u_W)
      =a(κ+σ)+κU−σB
      ≥a(κ+σ+κl/h)−κ/h.

By J≤d, the lower W support in the original chart is d+L≤2d−a. If this were a separating direction, comparison and a>1 would require

    F1=1−d+(1−h)(dx−t)<0.                         (8)

The simplification uses the exact identity

    κ(1−x)+σ−d=(1−h)(dx−t).

If dx≥t, every term in F1 is nonnegative. If dx<t, the bounds 1−h≤2/5 and x≥1/3 give

    F1≥1−d+(2/5)(d/3−t)
       =1−(13/15)d−(2/5)t
       ≥1−sqrt(41/45)>0.                           (9)

Both alternatives contradict (8).

### 1.4. The direction u_K is impossible

The exact W lower support in this direction is

    lower_W(u_K)=l+κL+σH
                ≤l+κd+.5σd−a(κ+σ),               (10)

using both caps in (3). Compare (10) with (2), before discarding its positive a−1 term. Separation would require

    F2=κ(1−d)+σ(1−.5d)−x(1−h)<0.                 (11)

We prove a strictly positive bound on the entire enlarged domain (5), 0≤t/d≤2/3. Put

    A0=d(1−.5d)+t(1−d)>0,
    B0=.5d(4−3d−t).

The exact support identity is

    κ(1−d)+σ(1−.5d)=(h−l)A0+lB0.                 (12)

Since h−l≥−l/4, the right-hand side is at least lG(t), where d=sqrt(1−t²) and

    G(t)=B0−A0/4
        =(7/4)d−(11/8)d²−(1/4)dt−(1/4)t.         (13)

The W angle bound puts 0≤t≤2/sqrt(13). On this whole interval,

    G(t)>1/4.                                       (14)

Here is a continuous proof of (14), including both interval endpoints. Differentiate (13) and set

    Q(t)=4d³G''(t)=11d³−7+3t−2t³.

Since t²≤4/13<1/2,

    Q''(t)=−33(d−t²/d)−12t<0.

Thus Q is concave. Its endpoint values are

    Q(0)=4,
    Q(2/sqrt(13))=359/(13sqrt(13))−7>0.

The last strict inequality follows from 359²>7²·13³. Concavity puts Q above its positive endpoint chord, so G''>0 throughout the interval. At its right endpoint,

    G'(2/sqrt(13))=−17/12+61/(12sqrt(13))<0,

because 61²=3721<3757=17²·13. As G' is increasing, it is negative everywhere on the interval; hence G is decreasing. Finally,

    G(2/sqrt(13))−1/4
      =19/(4sqrt(13))−137/104>0,                  (15)

because 494²−13·137²=39>0. This proves (14) without sampling angles.

On the other hand,

    x(1−h)=hl²/[(1+h)(1+l)]≤l/4,                 (16)

since both h/(1+h) and l/(1+l) are at most 1/2. Equations (12)–(16) give

    F2>l/4−x(1−h)≥0,

contradicting (11). Both possible actual separating directions have been excluded. Therefore the assumed large K angle (5) is impossible:

    0<h/l<3/4.                                      (17)

### 1.5. The four strict bands of the midpoint

We now verify Z=(1,−.5) directly. Its lower u band follows from P:

    u_K(Z)−u_K(P)=l−.414h≥.586l>0.

Its upper v band follows from A:

    v_K(A)−v_K(Z)=.18h+.5l>0.

For its upper u band, (2) and the exact identity

    1−x−(l−.5h)=(1−l)(1−x/2)>0

give u_K(Z)<U+a. Both factors are positive since h>0 and x≤sqrt(2)−1<1.

Finally, on 0≤h/l≤3/4 one has h+.5l≤1. This follows, for example, by writing it as (r+.5)/sqrt(1+r²), which is increasing for 0≤r≤3/4 and equals 1 at r=3/4. Hence

    V=B−a≤−a<−1≤−h−.5l=v_K(Z).

The lower v band is strict as well. Thus all four inequalities for strict ownership hold, proving the theorem. The argument includes every exterior tangency, and the earlier cited sign theorem covers the axial and orientation-boundary alternatives. ∎

## 2. Exact C974 consequence

Retain the original local ownership entrance and its first missing-corner root, reproduced in `C974-ORIGINAL-ENTRANCE.txt`, Sections 1–4. The exact owner map in Section 2 of `MISSING-CORNER-WALL-SIGN.md` supplies every hypothesis of Theorem 1, with K=Q0, W=Q9 and the translation (x,y)↦(x−1,y−1). In particular the strict Q9 origin (2,1) is the uniform conclusion of Section 8 of `C974-C976-CENTRAL-CROSSPOINTS.md`; the point (2,1.5) belongs to the actual Q5, and (3,1.5) belongs to the actual Q6. No southwest central origin is substituted for either point.

The target translates back to

    Q0 excludes (1,1)  ⇒  (2,.5) is strictly in Q0.   (18)

This conclusion holds in both remaining C974 central pairs. The independent Q9 half is now proved in `BOTTOM-WALL-LOWER-MIDPOINT.md`, using the paired corner Q2 and the actual Q6 segment. The joining theorem `C974-FIRST-MISSING-CORNER-ENDING.md` therefore closes the complete first root. Theorem 1 above does not assume or use the Q9 midpoint containment.
