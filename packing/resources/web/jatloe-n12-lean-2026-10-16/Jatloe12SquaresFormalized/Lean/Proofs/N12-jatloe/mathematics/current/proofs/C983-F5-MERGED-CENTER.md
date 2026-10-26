# C983 F5-only: the merged center from its actual left neighbor

Every terminating decimal below is an exact rational. Owned points and the stated bar are strict in their named actual open squares. An exclusion allows tangency. The proof uses the original common side 1<a≤1001/1000, full square supports, and a genuine container wall. All canonical orientations, including their endpoints, are covered continuously.

## 1. A two-square local theorem and its actual source map

**Theorem 1.** Let W,L be open squares of the same side 1<a≤1001/1000 with disjoint interiors. In the following local coordinates suppose that W strictly owns

    P=(−.35,−.35), Q=(−.35,.35),
    D=(−.26,0), F=(0,.26),                         (1)

and excludes F0=(−1,−.26). Suppose that the actual square L strictly owns

    M=(−1−e,0), B=(−1,.26), R=(−1,.8),
    e=43/500=.086,                                (2)

and lies in the genuine half-plane x≥−2. Then O=(0,0) lies strictly in W.

For C983 merged label8224, translate the original coordinates by (−2,−2) and take W=Q7,L=Q8. The complete source map is:

| Local datum | Original point and actual source |
|---|---|
| W owns P,Q | The southwest and northwest markers in this one merged Q7 |
| W owns D,F | G3 and F5 from its exact label8224 |
| W excludes F0 | F0=(1,1.74), strictly in actual singleton Q1 |
| L owns M | The original marker (.914,2) in Q8 |
| L owns B | F1=(1,2.26), in every original Q8 component |
| L owns R | (1,2.8), established in Section 1 of `C983-F5-CENTRAL-REDUCTION.md` |
| L lies in x≥−2 | The original genuine left wall x≥0 |

In particular convexity gives the whole strict bar

    {−1}×[.26,.8] ⊂ L.                             (3)

The theorem therefore proves the unconditional F5-only statement

    (2,2) ∈ Q7 strictly.                           (4)

It requires no top or right component, no left-wall origin, no vertical merged crosspoint, and no exclusion of a western marker from Q7.

We prove the local theorem in the remaining sections. Write a square in orthonormal coordinates u,v with strict bands U<u<U+a and V<v<V+a. For any direction n, its maximum and minimum on the closed square are obtained by choosing the upper or lower endpoint independently according to the sign of each frame coefficient of n. Disjoint open squares have a separating axis normal to a face of one of the two actual squares; their closed supports may touch. We use these complete supports throughout.

## 2. Missing center forces a short negative angle

First give W a positive canonical frame

    u=(d,r), v=(−r,d), d≥r≥0, d²+r²=1.

At O its lower u and v bands follow from P, whose projections are −.35(d+r) and .35(r−d). Its upper u band follows from F, whose u projection is .26r≥0. Its upper v band follows from Q, whose v projection is .35(d+r)>0. Strictness of the anchors gives all four strict bands, including r=0 and r=d. Thus O is already in W in this orientation.

For a contradiction we may consequently assume a negative canonical frame

    u_W=(d,−r), v_W=(r,d), d≥r≥0, d²+r²=1,
    lower faces U,V; upper faces A=U+a,H=V+a.      (5)

At O the lower u band follows from D, the lower v band from P, and the upper v band from F. A missing O must therefore satisfy

    A≤0, U≤−a.                                   (6)

The excluded F0=(−1,−.26) satisfies the upper u band by comparison with D, the projection gap being .74d−.26r>0, and the upper v band by comparison with F, the gap being r+.52d>0. If it exited through lower u, then U≥−d+.26r and (6) would give a≤d−.26r≤1. Hence its exit is necessarily

    V≥−r−.26d.                                   (7)

The strict P gives V<−.35(d+r), so

    r/d>9/65, in particular r>0.                 (8)

The foreign point B satisfies both upper bands of W: compare its u projection with D and its v projection with F, with respective gaps .74d+.26r and r. Its two possible exits are lower u and lower v.

Suppose B exited through lower v. Then V≥−r+.26d and the strict P would give

    r/d>61/65.                                   (9)

In this case d>.7, r>.65 and d+r>1.35. Put z=r/(1+d). Equation (9) also gives z>.26: otherwise r/d=2z/(1−z²)≤1300/2331<61/65.

Consider the closed vertex of W at the two lower faces,

    Z=(dU+rV, −rU+dV).

Using (6) and the strict P,

    Z_x<−d−.35r(d+r)
       <−.7−.35(.65)(1.35)<−1.                  (10)

The lower bound V≥−r+.26d gives

    Z_y≥ar−dr+.26d²
       >.26+r²(z−.26)>.26.                      (11)

The strict F gives U>−a−.26r. Using this and the strict P for the opposite bound,

    Z_y<ar+.26r²−.35d(d+r)
       <1.001(5/7)+.13−.175=.67<.8.             (12)

Here r≤1/sqrt(2)<5/7, r²≤1/2 and d(d+r)≥1/2. The strict point Q=(−.35,.35) lies to the right of x=−1. The segment from Q to the closed vertex Z crosses x=−1 at a height strictly between .26 and .8. Except for Z, this segment lies strictly in the open square W. Its crossing therefore belongs both to W and to the actual bar (3), a contradiction.

B must exit through lower u. Combining U≥−d−.26r with (6) gives

    1<a≤d+.26r.

The exact half-angle formula now yields

    0<z=r/(1+d)<13/50.                            (13)

Indeed d+.26r−1=2z(.26−z)/(1+z²). We will repeatedly use the consequences

    d>2331/2669>.873,
    r<1300/2669<.49,
    r/d<1300/2331<.56,
    d−(3/2)r>0.                                  (14)

Let p be the angle with d=cos p,r=sin p. Thus 0<p<2 arctan(13/50)<π/4.

## 3. Every possible separating face

Orient a prospective separating direction n from L toward W. Strict B in L and F in W have difference (1,0), so

    n_x>0.

Strict R in L and P in W have difference (.65,−1.15), so also

    n_y<(13/23)n_x.                               (15)

Of W's face normals only u_W=(d,−r) remains: its other normal with nonnegative first coordinate is (r,d), whose slope is at least 1, and the reverse directions have nonpositive first coordinate.

For L choose either a negative canonical frame (b,−t),(t,b) or a positive canonical frame (b,t),(−t,b), where

    b=cos q, t=sin q, 0≤q≤π/4.

In the negative frame, (t,b) fails (15), leaving only (b,−t). In the positive frame retain (b,t) and (t,−b). These are a covering list; retaining a direction even if its slope happens to fail (15) only enlarges the list to be excluded. Their zero-angle cases are covered as well.

Thus there are exactly the following families to disprove:

    L negative: u_W or (b,−t);
    L positive: u_W, (b,t), or (t,−b).             (16)

For L alone translate once more to a chart centered at (−1,0). Its strict marker is now (−e,0), its strict points B,R are (0,.26),(0,.8), and its real wall is x≥−1. A projection computed in this L chart is shifted by −n_x when expressed back in the W chart.

## 4. Negative L: its full support on W's axis

Give L the negative frame (b,−t),(t,b), with lower faces ℓ,m. Its strict marker and genuine leftmost vertex give

    ℓ<−eb, m<−et,
    bℓ+tm≥−1.                                   (17)

In particular its own upper u face J=ℓ+a satisfies

    J>a−1/b+et²/b.

Set

    k=db+rt=cos(q−p)>0,
    j=dt−rb=sin(q−p).

The full upper support of L in direction u_W, in its local chart, is

    k(ℓ+a)+jm+a max(j,0).

Eliminate ℓ using (17). The coefficient of m is j−kt/b=−r/b. Since m<−et and a>1, after the shift −d its upper support is strictly greater than

    B_−(q)=k−2d−(1−e)rt/b,       0≤q≤p,
    B_+(q)=k+j−2d−(1−e)rt/b,     p≤q≤π/4.        (18)

Each function is strictly concave on its indicated interval:

    B_−''=−k−2(1−e)rt/b³<0,
    B_+''=−(k+j)−2(1−e)rt/b³<0.

Here k+j>0 on the second interval. At the endpoints,

    B_−(0)=−d>−1,

    B_−(p)=B_+(p)
      =−1+[er²−(1−d)²]/d
      =−1+r²(e−z²)/d>−1,                        (19)

because e−z²>.086−.26²=23/1250>0. At the remaining endpoint,

    B_+(π/4)=(sqrt(2)−2)d−(1−e)r>−1.             (20)

For completeness, (2−sqrt(2))d+(1−e)r increases with p on (13): its derivative is −(2−sqrt(2))r+(1−e)d>−.586(.49)+.914(.873)>0. Since sqrt(2)>707/500, its value at the upper endpoint in (14) is strictly less than

    [293·2331+457·1300]/[500·2669]
      =1277083/1334500<1,

with exact margin 57417/1334500. This proves (20). Concavity and all three endpoint bounds show that the upper support of L on u_W is greater than −1 everywhere. The lower support of W on that axis is U≤−a<−1. This direction cannot separate.

## 5. Negative L: its own axis when q≤p

The upper support of L on its own direction (b,−t), now in the W chart, is strictly greater than

    Λ(q)=1−b−1/b+et²/b.                           (21)

Put h=rb−dt. For q≤p we have h≥0, so the full lower support of W on this axis is

    kU+hV<−k−.35h(d+r).                           (22)

Define the constants, with p fixed,

    A_−=d+.35r(d+r),
    C_−=r−.35d(d+r).

The exact difference identity is

    b[Λ+k+.35h(d+r)]
      =G_−(q)
      =b−2+A_−+(1+e−A_−)t²+C_−bt.               (23)

We have

    A_−−1=r[.35(d+r)−z]>0,
    C_−+.35=r[1−.35d+.35r]>0.

On 0≤q≤p, b≥d>.873 and cos(2q)≥0. Consequently

    G_−''=−b+2(1+e−A_−)(b²−t²)−4C_−bt
           <−.873+.172+.7=−.001<0.              (24)

If 1+e−A_− is negative its contribution is nonpositive; otherwise it is less than e. We also used bt≤1/2 and C_−>−.35. The two endpoint values are

    G_−(0)=A_−−1>0,
    G_−(p)=er²−(1−d)²=r²(e−z²)>0.               (25)

Concavity makes the whole gap positive. Equations (21)–(25) contradict the support ordering required for separation.

## 6. Negative L: its own axis when q≥p

Now h≤0. The strict F gives H>.26d, so the full lower support of W is

    kU+hH<−k+.26dh.                               (26)

Put

    A_+=d−.26dr,
    C_+=r+.26d²>0.

The corresponding wall gap is

    b[Λ+k−.26dh]
      =G_+(q)
      =b−2+A_++(1+e−A_+)t²+C_+bt.               (27)

Here A_+<1 and, using dr≤1/2 and (14),

    0<1+e−A_+<1.086−.873+.13=.343.

Thus on the whole canonical interval

    G_+''=−b+2(1+e−A_+)(b²−t²)−4C_+bt
           <−.7+.686=−.014<0.                   (28)

For the far end of the interval we will use the actual strict marker as a second support bound. Set

    b_*=1−e=.914,
    t_*=sqrt(1−b_*²), q_*=arccos(b_*).

The exact inequalities .4<t_*<.406 follow by squaring. At q=q_* the wall bound (21) equals the marker projection:

    Λ(q_*)=−(1+e)b_*.

The marker itself gives, for every q,

    upper_L(b,−t)>−(1+e)b.

Its difference from the bound (26) is

    D(q)=−(1+e)b+k−.26dh
        =b(A_+−1−e)+tC_+.                        (29)

The first coefficient is negative and the second positive, so D strictly increases with q.

If p≥q_*, then at q=p,

    D(p)=1−(1+e)d≥1−(1+e)(1−e)=e²>0.

The increasing marker gap excludes the entire interval q≥p in this case.

It remains to treat p≤q_*. On [p,q_*], use (27),(28). Its first endpoint is again

    G_+(p)=r²(e−z²)>0.

At its second endpoint the gap equals b_*f(p), where

    f(p)=b_*d+t_*r+.26t_*d²−.26b_*dr−1+e².       (30)

This is strictly positive on 0≤p≤q_*. Indeed its exact second derivative is

    f''=−b_*d−t_*r−.52t_*(d²−r²)+1.04b_*dr
        ≤b_*²(−1+1.04t_*)<0.                     (31)

We used d≥b_*, d²−r²≥0 and dr≤b_*t_* on this interval. Its endpoint values satisfy

    f(0)=−e+e²+.26t_*
          >−.086+.007396+.104
          =6349/250000>0,
    f(q_*)=e²=1849/250000>0.                     (32)

Concavity proves f(p)>0. Therefore both endpoints of G_+ on [p,q_*] are positive, so that entire wall gap is positive as well. For q≥q_*, the increasing marker gap D starts at this same positive value and remains positive. This excludes every remaining negative-L direction, with q=p and q=q_* included.

## 7. Positive L: its full support on W's axis

Give L the positive frame (b,t),(−t,b), again with lower faces ℓ,m. Its marker and its genuine leftmost vertex give

    m<et,
    bℓ−t(m+a)≥−1.                               (33)

Set

    k=db−rt>0, h=dt+rb>0.

The first positivity follows from b≥t and d>r. The full upper support of L on u_W, in the L chart, is k(ℓ+a)−hm. Eliminating ℓ with (33) gives coefficient kt/b−h=−r/b on m. After using m<et, a>1 and the shift −d, this upper support is strictly greater than

    B(q)=d(b+t−2)+r g(q),
    g(q)=t[(1−e−t)/b−1].                         (34)

The following scalar bound holds over the whole canonical interval:

    g(q)≥−(3/2)(b+t−1).                           (35)

To see it without sampling, multiply its left-minus-right expression by b. The exact expansion is

    b[g+(3/2)(b+t−1)]
      =(3/2)(1−b)+(1−e)t+(1/2)bt−(5/2)t²
      ≥t[(1−e)+(1/2)b−(7/4)t]
      ≥t[(1−e)−(5/4)t]≥0.

The first inequality uses 1−b=t²/(1+b)≥t²/2, the second uses b≥t, and the last uses t<5/7 and 1−e=.914>25/28. With (14), (34),(35) imply

    B(q)≥−d+[d−(3/2)r](b+t−1)≥−d>−1.

Again W's lower support is U≤−a<−1, so its own normal cannot separate.

## 8. Positive L: both of its own remaining normals

On L's normal (b,t), its strict point R=(−1,.8) has projection −b+.8t. The full lower support of W is, with the k,h of Section 7,

    kU+hV<−k−.35h(d+r).

The strict support gap is therefore bounded below by

    −b+.8t+k+.35h(d+r)
      =b[d−1+.35r(d+r)]
         +t[.8−r+.35d(d+r)]>0.                   (36)

The first coefficient is r[.35(d+r)−z]>0 and the second is greater than .8−r>0. This axis cannot separate.

For the remaining normal (t,−b), its W-frame coefficients are h>0 and −k<0. Thus W's full lower support is

    hU−kH<−h−.26dk.

The strict marker of L has projection −(1+e)t in the W chart. The gap is

    h+.26dk−(1+e)t
      =b[r+.26d²]+t[d−.26dr−1−e].                (37)

The second coefficient is negative. Since b≥t, (37) is at least

    b[d+r−1+.26d²−.26dr−e].

For d²+r²=1 and d,r≥0,

    d+r−1=2dr/(d+r+1)≥.8dr,

because sqrt(2)<3/2. Consequently the expression in brackets is at least

    .26d²+.54dr−e≥.13−.086=11/250>0.             (38)

This final direction also fails. Together Sections 4–8 exhaust the full face-normal list (16), contradicting disjointness of the two actual squares under the missing-center assumption. O must be strictly in W, completing Theorem 1 and the actual conclusion (4). ∎

## 9. Scope and exact algebra audit

This chapter proves the merged center throughout all of label8224, before selecting any of its five right-wall components. It uses one actual merged square and its one actual left-wall neighbor; the singleton Q1 supplies only the true exclusion F0. It does not import the invalid southwest crosspoint from a configuration whose northwest marker had another owner.

An independent symbolic reconstruction checked the eleven full-support and gap identities, both second derivative formulas, the half-angle identities and every stated nontrivial rational endpoint. Each identity and all of its mathematical uses are displayed above. The algebra checks supplement the complete all-domain signs, concavity arguments, exhaustive directions and actual-owner proof in this chapter.
