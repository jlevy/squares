# C1092 MMMP: the bottom origin beside the double right wall

All terminating decimals are exact rational numbers. Strict points retain their named actual open-square owners; exclusions and separating supports permit tangency. The local theorem uses common side a>1, the full actual squares and one genuine wall. It imposes no boundary-center sign or upper side bound.

## 1. The local two-square obstruction

**Theorem 1.** Let C,W be open squares of common side a>1 with disjoint interiors. Suppose C has a nonnegative canonical frame and strictly owns

    M=(.35,.35), I=(0,.26), J=(.26,0),

while excluding O=(0,0), A=(.4,1) and H0=(.5,1). Suppose W has closure in x≤2, strictly owns

    S=(1.086,0), G=(1,.26), B=(1,.4),

and excludes P=(1,0). Then this configuration is impossible.

The two isolated points A,H0 are exclusions only. No segment between them, or particular owner of them, is a premise of this local theorem.

### 1.1. The inward angle and a strict half-angle point

Write C's frame as u=(c,s), v=(−s,c), with c≥s≥0 and c²+s²=1. Let e,V be its lower faces and T=V+a its upper v face. The three other bands of its missing O follow from M,I,J, so

    0≤e<.26s.                                    (1)

Thus s>0. At A the lower u and v bands follow from M,J, and its upper u band follows from

    u(A)=.4c+s≤1.4/sqrt(2)<1<a+e.

Consequently

    T≤c−.4s.                                     (2)

Set z=s/(1+c), so c+sz=1 and −s+cz=−z. If z≥.26, then G=(1,.26) would be strict in C: its lower u band follows from J; its upper u band follows from c+.26s≤1<a+e; and its upper v band follows from I. Its last lower v band follows from (2), since

    v(G)−V>1−.74c−.6s≥1−sqrt(.9076)>0.

This contradicts the actual strict ownership of G in W. Hence

    0<z<13/50, c>2331/2669>.873,
    0<s<1300/2669<.49.                           (3)

At H0 the lower u band follows from M and the lower v band from J. The upper u band follows from .5c+s<.99<1<a+e. Its exclusion therefore gives

    T≤c−.5s.                                     (4)

Now Z=(1,z) is strictly in C. Its u projection is1, strictly between e and e+a, and its upper v band follows from I. For its lower v band use (4) and

    c−.5s+z−1=z(.5−s−.5c)
                =−sz(1−z/2)<0.

Thus V<c−.5s−1<−z=v(Z), proving the last strict band.

### 1.2. The whole actual boundary square and its angle order

An axis-parallel W would contain P strictly, taking its x coordinate from G and its y coordinate from S. We may therefore choose its actual face normals as

    w=(b,t), w_perp=(−t,b), b,t>0, b²+t²=1.

There is no assumption b≥t. This choice includes every nonaxis orientation. Write L,H for its lower faces. Its actual marker and right wall give

    L<1.086b, H<−1.086t,
    b(L+a)−tH≤2.                                (5)

The missing P has both v bands from S,B and its upper u band from B; hence L≥b. More strongly, the just-proved strict C point Z is excluded from W. Since 0<z<.26, both its v bands and its upper u band follow from the same strict S,B. Therefore

    L≥b+tz.                                      (6)

Let θ,β∈(0,pi/2) denote the angles of u,w, respectively; θ is canonical but β need not be. We have

    β>θ.                                         (7)

Indeed, (5),(6), with a>1, imply

    btz<1−b−.086t²,
    z<[t/(1+b)](.914−.086b)/b.                   (8)

If β≤θ, then t/(1+b)≤z and b≥c>.873>457/543. The final factor in (8) is then less than1. This would give z<t/(1+b)≤z, a contradiction.

The strict pair J,S forces every C-to-W separating normal to have positive x component. The strict pair Z,B forces its y component positive as well. The complete list of actual face-normal directions in this cone is therefore just u and w. Define

    α=bc+ts>0, δ=tc−bs>0.                       (9)

The strict inequality for δ is exactly (7).

## 2. C's own normal cannot separate

The exact lower W support in direction u is

    lower_W(u)=αL−δ(H+a).

Eliminate H with the genuine wall in (5). The exact identity α−δb/t=s/t gives

    lower_W(u)≤(s/t)L−aδ(1+b/t)+2δ/t.            (10)

We show that this support is less than1. This contradicts upper_C(u)=e+a>1.

Put ε=.914. If b≥ε, (5) gives L<(2−1.086t²)/b−a. Substitution into (10), replacing a by1 only in its negative coefficients, yields

    lower_W(u)<cK+sJ1,
    K=2−b−t, J1=b−t+εt/b.                      (11)

For fixed β, the function K cos θ+J1 sin θ increases for 0≤θ≤β. To verify this on the whole interval, K,J1 are positive, so its derivative decreases there; its value at θ=β is

    J1 b−Kt=1−1.086t>0,

because b≥.914 implies t<.406. Thus θ<β and (11) give

    lower_W(u)<bK+tJ1=1.086b+ε/b−1<1.            (12)

The last exact sign follows from

    1.086b+ε/b−2=(b−1)(1.086b−ε)/b<0.

Here b<1 and b≥ε>ε/1.086.

It remains that b≤ε. Using the strict L<1.086b in (10) now gives

    lower_W(u)<cK+sJ2,
    K=2−b−t, J2=b(b+t−ε)/t.                     (13)

The strict marker S also gives lower_W(u)<1.086c. Hence c≤500/543 is already impossible for this separating source. We need only consider

    c>500/543>.92, 0<s<.391.                     (14)

Let β0=arccos ε. On β0≤β≤pi/4, K and J2 both decrease with β. Indeed K'=t−b≤0 and

    J2'=−t−b+(ε−b)/t²<0,

since b+t²(b+t)−1=t²[b+t−1/(1+b)]≥0. Thus the right side of (13) is at most

    cK0+sε, K0=2−ε−sqrt(1−ε²)<.681.

This last expression increases with θ over the interval (14): its derivative is εc−K0s>.914(.92)−.681(.4)>0. At its upper endpoint c0=500/543<.921 and s0=sqrt(44849)/543<.391. Therefore its full-interval bound is

    cK0+sε<.681(.921)+.914(.391)
            =39383/40000<1.                      (15)

On pi/4≤β≤pi/2, the function cK+sJ2 is convex in β. The exact second derivatives are

    K''=b+t>0,
    J2''=t−b+[(b−ε)²+1−ε²]/t³>0.

Its continuous endpoint values are less than1. At pi/4, use c≤1, s<.4 and sqrt(2)>7/5 to obtain

    c(2−sqrt(2))+s(sqrt(2)−ε)
      <2−.4ε−.6sqrt(2)<993/1250<1.

At pi/2 the value is c<1, since s>0. Convexity therefore makes (13) less than1 throughout this last interval. Together (11)–(15) exclude u at every pair of actual angles, including all switching endpoints.

## 3. W's own normal cannot separate

First observe from (5) that

    L<1                                             (16)

for every W angle. If b≤ε, use L<1.086ε=.992604. If b≥ε, use exactly the strict bound and factor in (12), applied directly to L.

The strict marker M in C gives T>.35(c−s). Define q=.35(c−s)>0. Its actual upper support in direction w is

    upper_C(w)=α(e+a)+δT>α+δq.                   (17)

First suppose β≤arctan(3/4). For fixed β, the function

    q−tan((β−θ)/2)

increases with θ on 0≤θ≤β, because its derivative is at least .5−.35sqrt(2)>0. Its value at0 is at least .35−1/3=1/60. Thus, putting d=β−θ>0,

    α+δq−1=sin d[q−tan(d/2)]>0.

Equations (16),(17) contradict upper_C(w)≤L in this regime.

Suppose instead β≥arctan(3/4), so t≥.75b. The positive coefficient s+qc and (17) give

    α+δq−1.086b≥b f(s),

where, with c=sqrt(1−s²),

    f(s)=c+.75s−1.086+.2625+.0875s²−.6125sc.

This function is positive on the complete interval 0≤s≤.49. A direct second derivative gives

    f''(s)=[−1+(49/80)s(3−2s²)]/c³+7/40
            ≤−2749801/40000000<0.

Here s(3−2s²) increases on that interval, and the numerator in brackets remains negative, so replacing c³ by1 gives an upper bound. The endpoint values satisfy

    f(0)=353/2000>17/100,
    f(.49)>1396799/8000000>17/100.

For the latter rational lower bound use sqrt(1−.49²)>.871; its coefficient 1−.6125(.49) is positive. Concavity proves f(s)>17/100 throughout. Consequently (17) is strictly greater than1.086b, whereas the actual lower W support is L<1.086b by (5). The last source w is impossible as well.

Both actual separating directions have failed. This proves Theorem1 for all its angles, side lengths and weak exterior contacts. ∎

## 4. Literal application to the original double-right MMMP branch

**Corollary 2.** Throughout the original MMMP branch in which Q10 owns G8, the actual bottom owner Q9 strictly owns (2,1).

The theorem `C1092-MMMP-RIGHT-DOUBLE-SPAN.md` gives Q10 exactly787200, with F8,F9,G8,G9 strict, and gives F4,G6 in actual Q5. Corollary3 of `C1092-MMMP-SOUTHEAST-CENTER-REDUCTION.md` proves that this Q5 has a strictly positive original canonical angle. The actual Q7 owns (2,2), so Q5 excludes it. The bottom pair F6,G5 is already universal by `C1092-MMMP-BOTTOM-ORDINARY-PAIR.md`.

Suppose (2,1) were excluded from Q9. Reflect Theorem7 of `C1092-DIRECT-WALL-POINT.md` through x=2 and take its actual K=Q1, B=Q9, b=.914, ell=1.6. The strict corner anchors become (3,.914),(3,1), and the strict boundary anchors become (2,.914),F6=(2.4,1). The corner quadrant and bottom boundary wall are genuine container walls. The contrapositive of that theorem therefore puts (3,1.5) strictly in actual Q1.

Use the simultaneous quarter-turn chart

    (X,Y)=(2−y,x−2), C=Q5, W=Q9.

Every premise of Theorem1 now has a literal actual source:

| Local datum | Original actual source |
|---|---|
| C's strict M,I,J | Q5 marker,G6,F4 |
| C's excluded O | (2,2), strict in actual Q7 |
| C's excluded A=(.4,1) | G8=(3,1.6), strict in actual Q10 |
| C's excluded H0=(.5,1) | (3,1.5), just proved strict in actual Q1 |
| W's strict S,G,B | Q9 marker,G5,F6 |
| W's excluded P | The supposed missing (2,1) |
| W's real wall X≤2 | The genuine original bottom wall y≥0 |
| C's nonnegative canonical sign | The already proved positive sign of actual Q5; a quarter-turn preserves it |

The two actual squares are disjoint and have their physical common side a>1. Theorem1 contradicts the supposed missing origin. This proves the corollary. Convexity now puts the whole [2,2.4]×{1} strictly in this same actual Q9. ∎

## 5. A uniform small-angle consequence for the same actual southeast owner

**Corollary 3.** In the double-right MMMP branch the positive southeast angle obeys

    s+.4c<.6, s<21/100, c>97/100.                 (18)

In the preceding chart the strict inward anchors and missing O still give (1),(2); the actual W point G gives (3) without any use of H0. The new bottom origin makes {1}×[0,.4] strict in W. If s+.4c≥.6, the point Z=(1,z) on this actual bar would be strict in C: its first three bands are as in Section1.1, while its lower v band follows from (2) and

    c−.4s+z−1=z(.6−s−.4c)≤0.

This is impossible. Thus the first inequality of (18) holds. The function s+.4sqrt(1−s²) increases on the canonical interval, and at s=.21 its cosine exceeds .975, making its value greater than .6. Hence s<.21, which implies c>.97. These bounds retain their strictness at the threshold and the origin is already excluded from the axial sign by (1).

The chapter proves the actual bottom origin and the uniform angle bound in the double-right branch. The final whole MMMP contradiction remains a separate obligation.
