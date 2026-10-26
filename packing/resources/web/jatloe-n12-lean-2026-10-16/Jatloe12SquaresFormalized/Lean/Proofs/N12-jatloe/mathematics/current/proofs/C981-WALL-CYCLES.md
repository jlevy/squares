# C981: wall advancement and completed continuous reductions

All decimal numbers below denote exact rational numbers. An owned point is in the open interior of its actual square. An excluded point may lie on a face. Every square has side a>1; all support separations are allowed to be weak.

**Completed original-row simplification: all seventeen targets.** This chapter gives complete continuous exclusions of representatives **24, 26, 39, 59, 71, 105, and 108**. The companion `C981-COMMON-CYCLE.md` gives one common continuous ending for **2, 28, 30, 37, 43, 69, 103, and 107**. Finally, `C981-LAST-TWO-CYCLES.md`, using the proved positive-angle reduction in `C981-OPPOSITE-CENTRAL-ANGLE.md`, completes **29 and 104**. Every ending has been independently audited. The proofs use actual square bands, named foreign points, and strict segments of named wall owners. Theorem 4 below supplies the stronger wall points (1,2.8)∈Q8 and (2.8,1)∈Q9 in all seventeen target rows. Historical scope statements in the intermediate sections describe the indicated stage of this chapter; the combined current scope is the seventeen-row statement here.

## 1. A stronger wall advance from the actual singleton corner

**Theorem 1.** Let an open square W of side a>1 be contained in x≥0. Suppose W strictly owns (.914,2) and (1,2.4), and excludes

    F=(1,1.74), G=(1.74,2), H=(.76,1.87).

Then W strictly owns (1,2.67).

The new premise H is a genuine strict point of the actual singleton corner in C981. It cannot be supplied merely by taking the convex hull of unrelated excluded points.

**Proof.** Relabel W's faces so that its unit normal is (l,h), where l>0, h≥0 and l²+h²=1. This positive quadrant labeling covers every orientation, including those whose canonical angle is negative. Write its lower face coordinates U,V, so membership means

    U<lx+hy<U+a,
    V<−hx+ly<V+a.

The minimum x coordinate of the closed square is lU−h(V+a). Containment therefore gives

    lU≥h(V+a).                                             (1)

Both upper bands of F follow strictly from the owned point (1,2.4). Thus F's exclusion gives

    U≥l+1.74h    or    V≥−h+1.74l.                         (2)

The lower U band of G follows from the owned point (.914,2), and its upper V band follows from (1,2.4). Therefore

    U+a≤1.74l+2h    or    V≥−1.74h+2l.                    (3)

The target P=(1,2.67) already has both lower bands strictly from (1,2.4). We prove both upper bands.

First suppose the first alternative in (2) holds. The first alternative in (3) would imply

    a≤.74l+.26h≤sqrt(.74²+.26²)<1,

which is impossible. Hence V≥−1.74h+2l. Consequently

    U(P)−U≤.93h<1<a,
    V(P)−V≤.74h+.67l≤sqrt(.74²+.67²)<1<a,

because .74²+.67²=.9965. Both target upper bands are strict.

Now suppose V≥−h+1.74l, the second alternative in (2). Its target upper V band is strict since V(P)−V≤.93l<1<a. At H, the upper U band follows strictly from (.914,2). Its upper V band is also strict, since

    V(H)−(−h+1.74l)=.24h+.13l
       ≤sqrt(.24²+.13²)<1<a.

As H is excluded, it therefore satisfies one of the two lower face alternatives

    U≥.76l+1.87h    or    V≥−.76h+1.87l.                  (4)

The first gives

    U(P)−U≤.24l+.80h≤sqrt(.24²+.80²)<1<a,

where .24²+.80²=.6976.

In the second alternative, suppose for contradiction that the upper U band of P fails: U+a≤l+2.67h. Multiply by l, use (1), and then the second lower bound in (4). The result is

    a(l+h)≤1−.24h²+.80lh.                                (5)

Put K=l+h. Then 1≤K≤sqrt(2) and

    K−1=2lh/(K+1)≥2(sqrt(2)−1)lh≥.80lh.

Thus (5) gives aK≤K−.24h²≤K, contradicting a>1 and K>0. This proves the remaining strict upper band and the theorem. The proof includes h=0 and equalities at every excluded point. ∎

### Exact C981 owner mapping

The following seventeen original representatives all have Q1 owning H=(.76,1.87), Q8 owning (.914,2),(1,2.4), and exact auxiliary set Q8={1,11}:

    2,24,26,28,29,30,37,39,43,
    59,71,103,104,105,107,69,108.

The exact Q8 set excludes F=(1,1.74), auxiliary 0, and G=(1.74,2), auxiliary 13. The different actual owner Q1 supplies the exclusion of H. Therefore Theorem 1 yields

    (1,2.67)∈Q8                                            (6)

for every one of these seventeen alternatives. No assumption about ownership of an auxiliary absent from all owners is used.

Reflect the same theorem across x=y. Q9 owns (2,.914),(2.4,1), has exact auxiliary set {6,15}, and excludes (1.74,1),(2,1.74). Q0 strictly owns (1.87,.76), which becomes H. Hence all seventeen alternatives also satisfy

    (2.67,1)∈Q9.                                           (7)

Both statements strengthen the former 2.56 wall advances by .11. They use the existing singleton corner consequences without an angle or center enclosure and require no upper bound on a.

## 2. The center premise in a two-line capacity theorem can often be removed

**Theorem 2.** Let Q be an open square of side a>1 which meets two parallel lines a distance d apart, with 0<d≤1. Let their positive open chord lengths be ℓ0,ℓ1. Then

    ℓ0+ℓ1>min(1,2d,2sqrt(2)−2d).                         (8)

In particular, if 1/2≤d≤1, then

    ℓ0+ℓ1>min(1,2sqrt(2)−2d),                            (9)

without any hypothesis on the center of Q. A strict owned point on each line is enough to ensure both intersections.

**Proof.** By a rigid change of coordinates take vertical lines. Write the absolute normal components as c≥s≥0, c²+s²=1. If s=0, every nonempty vertical chord has length a, and (8) holds.

For s>0 put R=a(c+s)/2. A vertical line at distance t≥0 from the center has chord length

    f(t)=min(a/c,max(0,(R−t)/(cs))).                      (10)

If the center is between the lines, their distances t0,t1 satisfy t0+t1=d. If either chord is on the plateau, their sum is at least a/c>1. Otherwise the sum equals

    [a(c+s)−d]/(cs)>[(c+s)−d]/(cs).

Writing z=c+s, so 1<z≤sqrt(2) and cs=(z²−1)/2, the final expression is 2(z−d)/(z²−1). Its derivative has numerator −2(z²−2dz+1), which is negative for 0<d≤1 and z>1. Its minimum occurs at z=sqrt(2), giving 2sqrt(2)−2d. This proves the usual bound for a center between the lines.

If the center lies outside the strip, their distances differ by d. Both chords are positive by hypothesis. A plateau chord again gives a sum>1. If neither is on the plateau, formula (10) shows that the nearer chord is exactly d/(cs) longer than the farther chord. Since cs≤1/2 and the farther chord is strictly positive,

    ℓ0+ℓ1>d/(cs)≥2d.

These alternatives prove (8). Since 2d≥1 on [1/2,1], (9) follows. Centers on either line may be put in the first alternative; the formulas agree at all plateau and midpoint boundaries. ∎

This replaces a center-between-lines derivation whenever both line intersections have independent geometric provenance. It does not justify omitting the intersection hypotheses: a square can lie entirely on one side of both lines.

## 3. A universal positive-angle longitudinal-axis reduction

**Theorem 3.** Let C and B be disjoint open squares of common side a>1, with canonical nonnegative frames

    C: (d,S), 0≤S≤d, d²+S²=1;
    B: (b,t), 0≤t≤b, b²+t²=1.

Suppose C strictly owns

    (2,2), (1.5,2), (2,1.5), (1.65,1.65),

and excludes (2.26,2). Suppose B strictly owns

    (1.65,2.35), (1,2.4).

Then C strictly owns K=(1.3,1.8), and neither square's longitudinal face-normal axis can separate C and B. Consequently their disjointness requires one of the two forward transverse separations

    upper_C(−t,b)≤V_B^−,
    V_C^+≤lower_B(−S,d).                                  (11)

No small-angle hypothesis on C is needed.

**Proof.** Denote C's lower and upper face values by U_C^−, U_C^+, V_C^−, V_C^+. At the excluded point (2.26,2), its lower U and upper V bands follow from the strict center (2,2). Its lower V band follows from (2,1.5), because .5d−.26S≥.24d>0. Thus

    U_C^+≤2.26d+2S.                                       (12)

At K=(1.3,1.8), the lower U band follows from (12) and a>1, since its distance in this normal from (2.26,2) is

    .96d+.20S≤sqrt(.96²+.20²)=sqrt(.9616)<1<a.

The upper U band follows from (2,2). Its lower V band follows from (2,1.5), with increment .7S+.3d>0. Its upper V band follows from (1.5,2), whose V projection exceeds K's by .2(d−S)≥0. As the comparison point is strict, the diagonal tie d=S still gives a strict target band. Hence K∈C.

On the C longitudinal axis (d,S), C cannot precede B because the projection of C's strict center minus that of B's marker is .35(d−S)≥0. B cannot precede C because the projection of B's strict marker minus that of K is .35d+.55S>0.

On the B longitudinal axis (b,t), C cannot precede B because the projection of C's strict center minus that of B(1,2.4) is b−.4t>0. B cannot precede C because the marker's projection minus K's is .35b+.55t>0.

On either transverse axis, the reverse order is ruled out by the strict southwest and northwest markers of C and B, with equal x coordinates and y coordinates differing by .7. The separating-axis theorem for two squares retains all four axes. After the eliminations above only the two directions in (11) remain. Equal projections at zero or maximal canonical angle cause no extra branch because both compared points are strict. ∎

The earlier positive-C analysis first obtained 5S<d and then used K=(1.3,1.9) to remove the longitudinal axes. The slightly lower point (1.3,1.8) removes that entrance dependency and handles the whole canonical sector.

## Scope of the results above

Theorem 1 supplies stronger actual wall points in all seventeen target alternatives. Theorem 2 supplies an improved strip criterion. Theorem 3 removes longitudinal separators on an entire positive/positive sector after the genuine center and crosspoints have been established. These are complete local mathematical statements. By themselves they are not a complete exclusion of all seventeen original alternatives; the remaining support or chord contradiction must still be supplied before any full row is marked simplified.

## 4. Using the actual central marker advances both walls to 2.8

**Theorem 4.** Let W be an open square of side a>1 contained in x≥0. Suppose W strictly owns (.914,2),(1,2.4), and excludes the three points

    F=(1,1.74), H=(.76,1.87), M=(1.65,2.35).

Then W strictly owns P=(1,2.8).

The point M is the genuine C981 marker owned by Q7; H is the singleton corner seed owned by Q1. This theorem does not need the inward auxiliary exclusion (1.74,2).

### A scalar wall inequality

For l>0,h≥0,l²+h²=1,

    l+h−1+.24h²≥.93lh.                                  (13)

Here is an exact proof on the entire quarter circle. Put t=h/(1+l), so 0≤t<1, l=(1−t²)/(1+t²), and h=2t/(1+t²). Multiplication by the positive denominator (1+t²)² gives

    (1+t²)²[l+h−1+.24h²−.93lh]
       =2t[.07−.52t+1.93t²−t³].

For 0≤t≤1/2, the bracket is at least

    .07−.52t+1.43t²
       =(143/100)(t−2/11)²+1/44>0.

For 1/2≤t≤1, it is at least

    .07−.52t+.93t²
       =.93(t−1/2)²+.41(t−1/2)+17/400>0.

Thus (13) holds, including h=0.

### Proof of the wall theorem

Use the same positive frame and face values U,V as in Theorem 1. The wall gives lU≥h(V+a), and exclusion of F gives

    U≥l+1.74h    or    V≥−h+1.74l.                       (14)

The target has both lower bands strictly from (1,2.4).

If the second lower bound

    V≥−.76h+1.87l                                       (15)

is ever obtained, the target upper U band is automatic. Indeed, its failure U+a≤l+2.8h would imply, using the actual wall,

    a(l+h)≤1−.24h²+.93lh≤l+h

by (13), contradicting a>1. We will use this implication below. Also, a lower U bound U≥.76l+1.87h automatically gives the target upper U band, since

    U(P)−(.76l+1.87h)=.24l+.93h
       ≤sqrt(.24²+.93²)=sqrt(.9225)<1<a.               (16)

**First branch of (14).** Suppose U≥l+1.74h. At M, the lower U band follows from (.914,2), and the upper V band follows from (1,2.4). Its upper U band follows because

    U(M)−(l+1.74h)=.65l+.61h
       ≤sqrt(.65²+.61²)=sqrt(.7946)<1<a.

The exclusion of M therefore forces

    V≥−1.65h+2.35l.                                     (17)

This gives the target upper V band, since

    V(P)−(−1.65h+2.35l)=.65h+.45l
       ≤sqrt(.625)<1<a.

At H, the upper U band follows from the owned marker. Its upper V band follows from (17), since

    V(H)−(−1.65h+2.35l)=.89h−.48l≤.89<1<a.

Thus H must escape at a lower face. If it gives U≥.76l+1.87h, use (16); if it gives (15), use the scalar wall implication. This closes the first branch for every angle.

**Second branch of (14).** Suppose V≥−h+1.74l. At H the upper U band follows from the owned marker, and the upper V band follows because

    V(H)−(−h+1.74l)=.24h+.13l<1<a.

Thus H again escapes at a lower face.

If it gives (15), its upper U consequence has already been proved, while the upper V band follows from

    V(P)−(−.76h+1.87l)=−.24h+.93l≤.24h+.93l<1<a.

Suppose instead that U≥.76l+1.87h. The target upper U band follows from (16). If 1.06l≤1, its upper V band follows directly from the second branch of (14). In the only remaining subcase l>50/53, we have

    h²<1−(50/53)²=309/2809<1/9,
    0≤h<1/3.

On this interval the function .89sqrt(1−h²)+.48h is increasing: its derivative is .48−.89h/l>0, since h≤1/3 and l≥2sqrt(2)/3. Its value at h=1/3 is strictly less than one, because

    .89(2sqrt(2)/3)+.16<1
    ⇔ sqrt(2)<126/89,

and 2·89²=15842<15876=126². Consequently

    U(M)−(.76l+1.87h)=.89l+.48h<1<a.

The other strict bands of M are exactly those used above: lower U from (.914,2), and upper V from (1,2.4). Its exclusion therefore forces (17), which gives the target upper V band as before. This closes the last subcase and proves the theorem. ∎

### Application to all seventeen target representatives

Every row in the seventeen-row list in Section 1 satisfies the premises with W=Q8: F is auxiliary 0 excluded from Q8; H is strict in Q1; and M is marker 11 strict in Q7. Therefore

    (1,2.8)∈Q8.                                          (18)

After transposition x↔y, the same theorem applies with W=Q9. The three foreign points are then (1.74,1) from Q0's original auxiliaries, (1.87,.76) strict in Q0, and (2.35,1.65) strict in Q5. Thus

    (2.8,1)∈Q9.                                          (19)

These conclusions use only the common C981 marker and singleton corner data and the common Q8,Q9 auxiliary sets. The original nine variants at Q5 and Q10, the six secondary variants, and the two strip rows all satisfy the same actual hypotheses. No orientation restrictions and no side upper bound have been added.

Compared with the earlier wall reach at 2.56, (18) and (19) advance the actual wall points by .24. This is the strongest shared advancement established here. It is a proved entrance simplification; a terminal contradiction must still be proved before using it to delete the old finite exclusion of an entire representative.

## 5. A two-anchor obstruction closes representatives 24 and 26

**Theorem 5 (two anchors above an excluded segment).** Let Q be an open square of side a>1. No container assumption or upper side bound is needed. Suppose Q strictly contains

\[
A=(2,1.74),\qquad B=(3,1.6),
\]

and excludes

\[
G=(2.26,2),\qquad H=(3,1.74),
\]

as well as the entire segment

\[
[2.26,2.8]\times\{1\}.
\]

Then no such square exists. Both isolated exclusions and the segment exclusion are weak: boundary contact is allowed. The statement is invariant under transporting the square and all its point and segment data by one isometry.

### Proof

Choose canonical absolute components c≥s≥0, c²+s²=1. In either signed frame, write U,V for the lower face values, and U+a,V+a for the upper values.

**Nonpositive canonical sign.** Take

\[
u=(c,-s),\qquad v=(s,c).
\]

At G, the lower u-band is strict by comparison with A, because

\[
u\cdot(G-A)=.26(c-s)\ge0.
\]

Its upper u-band is strict by comparison with B, since

\[
u\cdot(B-G)=.74c+.4s>0.
\]

Its lower v-band is strict by comparison with A, since

\[
v\cdot(G-A)=.26(c+s)>0.
\]

Consequently G's exclusion forces

\[
V+a\le2c+2.26s. \tag{20}
\]

The segment supplies the excluded point F=(2.26,1). Its lower u-band is strict by A, and its upper u-band is strict by B:

\[
u\cdot(F-A)=.26c+.74s>0,
\qquad u\cdot(B-F)=.74c-.6s\ge.14c>0.
\]

Its upper v-band is strict by A, since

\[
v\cdot(F-A)=.26s-.74c\le-.48c<0.
\]

Thus F must leave through the lower v-face, giving V≥c+2.26s. Together with (20), this yields a≤c≤1, a contradiction. This argument includes s=0 and c=s.

**Nonnegative canonical sign.** Take

\[
u=(c,s),\qquad v=(-s,c).
\]

At G, its lower u-band and lower v-band follow strictly from A, because the increments are .26(c+s)>0 and .26(c-s)≥0. Its upper u-band follows strictly from B, whose projection exceeds G's by .74c-.4s≥.34c>0. Thus

\[
V+a\le2c-2.26s. \tag{21}
\]

At H, its lower u- and v-bands follow strictly from B, with increments .14s≥0 and .14c>0. Its upper v-band follows strictly from A, since v·(H-A)=−s≤0. Consequently

\[
U+a\le3c+1.74s. \tag{22}
\]

The excluded F=(2.26,1) has strict upper bands: compare its u-projection with B and its v-projection with A. It therefore leaves through a lower face. The alternative V≥c−2.26s, combined with (21), gives a≤c≤1. Hence

\[
U\ge2.26c+s. \tag{23}
\]

The other segment endpoint E=(2.8,1) has strict lower and upper u-bands, by A and B respectively:

\[
u\cdot(E-A)=.8c-.74s\ge.06c>0,
\qquad u\cdot(B-E)=.2c+.6s>0.
\]

Its upper v-band is strict by A, because v·(E-A)=−.8s−.74c<0. Its exclusion thus forces

\[
V\ge c-2.8s. \tag{24}
\]

Consider Q's closed bottom vertex

\[
Z=(cU-sV,\ sU+cV).
\]

For s=0, (21) and (24) already give a≤1. We may therefore suppose s>0. Equations (21) and (23) give

\[
Z_x\ge c(2.26c+s)-s(2c-2.26s-a)
=2.26+s(a-c)>2.26. \tag{25}
\]

Strict ownership of A gives U<2c+1.74s. Together with (24),

\[
Z_x< c(2c+1.74s)-s(c-2.8s)
=2+.8s^2+.74cs
\le2.77<2.8, \tag{26}
\]

where s²≤1/2 and cs≤1/2 were used. Thus the vertex abscissa lies strictly inside the excluded segment's horizontal span.

On the other hand, (21) and (22) imply

\[
\begin{aligned}
Z_y
&\le s(3c+1.74s-a)+c(2c-2.26s-a)\\
&=2-.26s^2+.74cs-a(c+s)\\
&<2-.26s^2+.74cs-(c+s)\\
&\le1-.26s^2-.06cs\le1.
\end{aligned} \tag{27}
\]

For the last line use

\[
c+s-1=\frac{2cs}{c+s+1}\ge\frac45cs,
\]

which follows from c+s≤√2<3/2. The strict inequality in (27) comes from a>1.

The segment AB lies strictly in Q. At x=Zₓ its ordinate is strictly between 1.6 and 1.74, since 2.26<Zₓ<2.8 lies between Aₓ=2 and Bₓ=3. Join that strict point to the closed vertex Z. Because Zᵧ<1, the joining segment crosses y=1 before reaching Z. Every such intermediate point is strictly inside an open convex square. Its abscissa lies in (2.26,2.8), contradicting the excluded segment.

Both canonical signs, every limiting angle, and all possible tangencies have now been covered. ∎

### Exact C981 owner mapping

Theorem 4 applied to the actual Q₉ gives the strict point (2.8,1). Its original auxiliary point (2.26,1) is also strict. Therefore

\[
[2.26,2.8]\times\{1\}\subset Q_9.
\]

Every point of this segment is outside the different actual square Q₅. The remaining hypotheses of Theorem 5 are supplied as follows:

| Representatives | Target | Strict A | Strict B | Excluded G | Excluded H | Whole-segment owner |
|---|---|---|---|---|---|---|
| 24, 26 | Q₅ | auxiliary 4: (2,1.74) | auxiliary 18: (3,1.6) | auxiliary 16: (2.26,2) | auxiliary 8: (3,1.74) | Q₉ |

In both rows Q₅'s exact auxiliary set is {4,18}. Hence both omitted auxiliaries G,H are genuinely excluded. Row 26's ownership of H by Q₁₀ reinforces that exclusion; row 24 needs only the exact absence from Q₅. No owner is fabricated for an auxiliary absent globally.

The Q₉ wall advance uses its original marker (2,.914), original auxiliary (2.4,1), and the genuine foreign points (1.74,1),(1.87,.76) in Q₀ and (2.35,1.65) in Q₅. Those hypotheses hold in both rows. Thus the segment proof uses the actual common side and the actual owner Q₉ throughout.

**Conclusion. Representatives 24 and 26 are completely excluded by Theorems 4–5.** This is a continuous two-square obstruction, with no orientation subdivision, center enclosure, finite propagation schedule, or upper bound on a. The added points in the other first-target rows can remove G's or H's exclusion from Q₅, so this conclusion is not silently extended to those rows.

### Parameter form of the same two-anchor obstruction

The preceding proof is not tied to the numerical pair of anchor heights. In normalized coordinates its following general form holds:

\[
\frac12\le h\le2\sqrt2-2,\qquad
1-h\le k\le h,\qquad h\le r\le1.
\]

A square of side a>1 cannot strictly own (0,h),(1,k), exclude (1−h,1),(1,h), and exclude the whole segment [1−h,r]×{0}. The rational restriction h≤4/5 is sufficient. Theorem 5 is the translate by (2,1) of h=37/50, k=3/5, r=4/5. In fact its excluded segment may end at x=2.74 instead of 2.8.

For completeness put p=1−h and use the same lower face coordinates. In the negative canonical frame the comparisons with the two strict anchors force

\[
V+a\le c+ps,\qquad V\ge ps,
\]

from (p,1) and (p,0), giving a≤c≤1. The required projection comparisons use p≤h, k≤h, and p≤k; equality is allowed because the anchor comparisons remain strict in the bands.

In the positive canonical frame the two isolated exclusions and the two segment endpoints give exactly

\[
V+a\le c-ps,\qquad U+a\le c+hs,
\qquad U\ge pc,\qquad V\ge-rs.
\]

The alternative lower V-face at (p,0) again gives a≤c and is discarded only after that contradiction. At (r,0), its lower U-band follows from rc−hs≥0, using r≥h. All remaining comparisons follow from p≤k≤h exactly as in the numerical proof.

If s=0 the V inequalities already contradict a>1. For s>0 the bottom vertex Z=(cU−sV,sU+cV) obeys

\[
Z_x\ge p+s(a-c)>p,
\qquad
Z_x<hcs+rs^2\le\frac{h+r}{2}\le r,
\]

where strict ownership of (0,h) supplies the strict upper bound. Its height satisfies

\[
Z_y\le1-ps^2+hcs-a(c+s)
<1-ps^2+hcs-(c+s)\le-ps^2\le0,
\]

because c+s−1≥(2√2−2)cs≥hcs. The strict anchor segment has positive height at every abscissa in [0,1], so joining its point at Zₓ to Z produces a strict square point on the excluded segment. This proves the parameter form with all equality cases included.


## 6. A sign lock for the outward central pair

**Theorem 6 (outward central sign lock).** Let C be an open square of side a>1. Suppose C strictly owns

\[
M=(2.35,1.65),\qquad A=(3,1.6),
\]

and excludes the three points

\[
P=(3,1),\qquad R=(3.086,2),\qquad E=(2.26,2)
\]

and the whole segment

\[
S=[2.26,2.8]\times\{1\}.
\]

Then C has strictly negative canonical angle. In particular, it cannot have a frame

\[
u=(c,s),\qquad v=(-s,c),\qquad c\ge s\ge0,\qquad c^2+s^2=1.
\]

This conclusion includes exclusion of the axial angle and the positive 45-degree representative. It is a sign restriction, not a complete exclusion of C.

**Proof.** Suppose the displayed nonnegative frame exists, and write C as

\[
U<u\cdot X<U+a,\qquad V<v\cdot X<V+a.
\]

The word “excludes” permits equality with a supporting line throughout the proof. Every comparison with a strictly owned point gives a strict band condition even when the projection increment is zero.

At P, both upper bands follow strictly from A. The lower u-band follows from M, because

\[
u\cdot(P-M)=.65(c-s)\ge0.
\]

Thus P can leave only through the lower v-face, and

\[
V\ge c-3s. \tag{28}
\]

At R both lower bands follow strictly from A:

\[
u\cdot(R-A)=.086c+.4s>0,\qquad
v\cdot(R-A)=.4c-.086s\ge.314c>0.
\]

If R left through the upper v-face, (28) would give

\[
a\le(2c-3.086s)-(c-3s)=c-.086s\le1.
\]

Therefore R leaves through the upper u-face:

\[
U+a\le3.086c+2s. \tag{29}
\]

At E the upper u-band follows from A, since

\[
u\cdot(A-E)=.74c-.4s\ge.34c>0.
\]

The lower v-band follows from M, since

\[
v\cdot(E-M)=.09s+.35c>0.
\]

Thus E leaves through the lower u-face or the upper v-face. The former choice, combined with (29), would give a≤.826c<1. Hence

\[
V+a\le2c-2.26s. \tag{30}
\]

The left endpoint F=(2.26,1) of S has strict upper u-band by comparison with A, and strict upper v-band by comparison with M:

\[
u\cdot(A-F)=.74c+.6s>0,\qquad
v\cdot(F-M)=.09s-.65c<0.
\]

If F left through the lower v-face, (30) would give a≤c≤1. Its exclusion therefore forces

\[
U\ge2.26c+s. \tag{31}
\]

The right endpoint T=(2.8,1) likewise has strict upper bands:

\[
u\cdot(A-T)=.2c+.6s>0,\qquad
v\cdot(T-M)=-.45s-.65c<0.
\]

If it left through the lower u-face, (29) would give

\[
a\le.286c+s\le\frac{1.286}{\sqrt2}<1.
\]

The middle inequality follows because .286 cos θ+sin θ is increasing for 0≤θ≤π/4; the last follows from 1.286²<2. Thus

\[
V\ge c-2.8s. \tag{32}
\]

For s=0, (30) and (32) already imply a≤1. Assume s>0, and consider the closed bottom vertex

\[
Z=(cU-sV,\ sU+cV).
\]

Equations (30) and (31) imply

\[
Z_x\ge2.26+s(a-c)>2.26. \tag{33}
\]

Equations (29) and (32) give

\[
\begin{aligned}
Z_x
&\le3.086-.286s^2+cs-ac\\
&<3.086-.286s^2+cs-c\\
&=2.8-c(1-s-.286c)<2.8, \tag{34}
\end{aligned}
\]

using the strict inequality .286c+s<1 already established above. Finally, (29) and (30) give

\[
\begin{aligned}
Z_y
&\le2+.826cs-a(c+s)\\
&<2+.826cs-(c+s)<1. \tag{35}
\end{aligned}
\]

Indeed

\[
c+s-1=\frac{2cs}{c+s+1}
\ge(2\sqrt2-2)cs,
\]

and .826<2√2−2. Since s>0, the last comparison is strict.

Both M and Z have abscissae strictly between 2.26 and 2.8. The point M is strictly in C and lies above y=1; Z belongs to the closed square and lies below y=1. Their joining segment crosses y=1 at an intermediate point whose abscissa is strictly between 2.26 and 2.8. An intermediate point joining an interior point of a convex square to a point of its closure is interior. This contradicts exclusion of S. ∎

### Exact owner applications

The following applications use a genuine whole segment in one actual boundary square; pointwise exclusion of its endpoints alone would not suffice.

| Family or representatives | Target in theorem coordinates | Strict anchors | Three isolated exclusions | Actual owner of S | Result |
|---|---|---|---|---|---|
| C981 rows 30, 39, 69 | Q₅ | marker M and auxiliary 18: A | P in Q₂; R in Q₁₀; auxiliary 16 absent from the exact Q₅ label | Q₉, from auxiliary 15 and Theorem 4 | Q₅ has strictly negative canonical angle |
| Remaining C1084 configuration, reflected by (x,y)↦(x,4−y) | reflected Q₆ | reflected marker (2.35,2.35) and auxiliary 19: (3,2.4) | reflected P in Q₂; R in Q₁₀; auxiliary 16: E in Q₅ | reflected Q₁₁, from auxiliary 17 and the reflected Theorem 4 | original Q₆ has strictly positive canonical angle |

The reflection in the second row is applied to the entire configuration. It sends the actual Q₁₁ segment [2.26,2.8]×{3} to S and reverses the canonical angle sign of Q₆. Thus no isolated-square reflection is being used to change a separation relation.

The theorem also applies to C981 rows 24 and 26, already completely excluded by Theorem 5. It does not apply to rows whose exact Q₅ label owns E; those rows must retain their extra ownership rather than treating E as an exclusion.


## 7. The extra inward anchor closes representative 39

**Theorem 7 (outward pair with an inward anchor).** Let Q be an open square of side a>1, strictly owning

\[
M=(2.35,1.65),\qquad A=(2,1.74),\qquad B=(3,1.6).
\]

Suppose Q excludes

\[
P=(3,1),\quad R=(3.086,2),\quad G=(2.26,2)
\]

and the whole segment [2.26,2.8]×{1}. Then Q cannot exist.

**Proof.** The strict points M,B, the three isolated exclusions, and the whole segment meet Theorem 6. Consequently every nonnegative canonical angle is impossible.

For a remaining negative canonical frame, write

\[
u=(c,-s),\qquad v=(s,c),\qquad
c\ge s\ge0,\qquad c^2+s^2=1.
\]

The excluded point G has strict lower u-band by comparison with A, strict upper u-band by comparison with B, and strict lower v-band by comparison with A:

\[
u(G)-u(A)=.26(c-s)\ge0,
\]

\[
u(B)-u(G)=.74c+.4s>0,\qquad
v(G)-v(A)=.26(c+s)>0.
\]

Its only possible excluded face is therefore the upper v-face:

\[
V+a\le2c+2.26s. \tag{36}
\]

The segment supplies the excluded F=(2.26,1). At F, its lower u-band is strict by A, its upper u-band is strict by B, and its upper v-band is strict by A:

\[
u(F)-u(A)=.26c+.74s>0,
\]

\[
u(B)-u(F)=.74c-.6s\ge.14c>0,
\]

\[
v(F)-v(A)=.26s-.74c\le-.48c<0.
\]

Thus F leaves only through the lower v-face, giving

\[
V\ge c+2.26s.
\]

Together with (36), this implies a≤c≤1, a contradiction. Every weak-face equality and the diagonal canonical endpoint are covered by the strict anchor comparisons. ∎

### Exact owner application and updated C981 scope

In representative 39, Q₅'s exact auxiliary set is {4,8,18}. It owns A through auxiliary 4 and B through auxiliary 18, as well as its original marker M. Auxiliary 16, the point G, is absent from that exact set and hence excluded. The actual corner Q₂ owns P; the actual right wall Q₁₀ owns R. The actual bottom square Q₉ owns F and, by Theorem 4, the whole segment to (2.8,1). All hypotheses of Theorem 7 are therefore genuine facts of that row.

The theorem does not require exclusion of H=(3,1.74). Indeed H is strictly in Q₅ in representative 39. This is exactly why the earlier all-angle two-anchor theorem did not by itself cover the row.

The same theorem also covers representatives 24 and 26, whose Q₅ squares have the same three strict points M,A,B and the same isolated exclusions. Thus the completed C981 original-row simplifications are now

\[
\boxed{24,\ 26,\ 39}.
\]

Sections 8–9 add complete exclusions of three further targets. The final completed scope and exact source ledger are recorded at the end of the chapter.

### A strict point for the two remaining lower-outward rows

Representatives 30 and 69 still have Q₅ owning both outward auxiliaries (3,1.74),(3,1.6), and Theorem 6 fixes its canonical angle as strictly negative. Reflect the entire relevant local configuration in y=2 and apply Theorem 2 of `C1084-DUPLICATE-POINT.md`. It gives the additional genuine strict point

\[
(2.46,2.01)\in Q_5. \tag{37}
\]

The reflected theorem's six exclusions come from the original points

\[
(2.26,2),\ (3.086,2),\ (2.26,1),\
(2.8,1),\ (3,1),\ (3.086,1).
\]

In rows 30 and 69, the first is absent from Q₅'s exact auxiliary set; the second is Q₁₀'s original marker; the third and fourth are strict in the actual Q₉; and the last two are strict in the actual southeast corner Q₂. Its reflected strict anchors are the Q₅ marker and auxiliary 8. Thus (37) is a valid local strengthening for both rows, with no unnamed owner for the globally absent southwest marker.

The point (37) is a proved consequence, not a complete row exclusion; a further genuine overlap or capacity contradiction is still required for those two rows.


## 8. A shorter wall segment suffices for the remaining inward–outward pairs

The following two results lower the necessary wall reach from 2.8 to 2.73. They are proved statements about actual square supports. Their application to a C981 representative still requires the stated whole segment in its actual top square.

**Theorem 8 (shorter-segment outward sign lock).** In Theorem 6, replace the excluded segment by

\[
S_{.73}=[2.26,2.73]\times\{1\}.
\]

Keep exactly the same two strict anchors and three isolated exclusions. The conclusion is unchanged: the canonical angle is strictly negative.

**Proof.** Follow the nonnegative-angle argument of Theorem 6. Its first three forced faces do not use the right endpoint of the segment and give

\[
U+a\le3.086c+2s,\qquad V+a\le2c-2.26s,
\qquad U\ge2.26c+s.
\]

At the new endpoint T=(2.73,1), the upper u-band follows strictly by comparison with the strict anchor (3,1.6), and the upper v-band follows strictly by comparison with M=(2.35,1.65), because

\[
u(3,1.6)-u(T)=.27c+.6s>0,
\qquad v(M)-v(T)=.65c+.38s>0.
\]

If T were on or below the lower u-face, combining U≥2.73c+s with the upper u-face bound would give

\[
a\le .356c+s\le\frac{1.356}{\sqrt2}<1.
\]

Here .356 cos θ+sin θ is increasing on 0≤θ≤π/4, and 1.356²=1.838736<2. Thus the only possible excluded face is the lower v-face:

\[
V\ge c-2.73s.
\]

For s=0 this contradicts V+a≤2c−2.26s. For s>0, the same closed bottom vertex Z=(cU−sV,sU+cV) as in Theorem 6 satisfies

\[
Z_x\ge2.26+s(a-c)>2.26,
\]

\[
Z_x\le3.086-.356s^2+cs-ac
<2.73-c(1-s-.356c)<2.73,
\]

and

\[
Z_y\le2+.826cs-a(c+s)<1.
\]

The last inequality is exactly the scalar estimate in (35). The segment from strict M to this closed vertex crosses the interior of S_.73 at a strict point of the square, a contradiction. All face equalities are retained. ∎

**Theorem 9 (stronger outward point with shorter wall reach).** Let D be an open square of side a>1 with a nonnegative canonical frame

\[
u=(c,s),\qquad v=(-s,c),\qquad c\ge s\ge0,
\qquad c^2+s^2=1.
\]

In coordinates translated by (−2,−2), suppose D strictly owns

\[
N=(.35,.35),\qquad A=(1,.26)
\]

and excludes the six points

\[
G=(.26,0),\quad R=(1.086,0),\quad F=(.26,1),
\quad T=(.73,1),\quad P=(1,1),\quad H=(1.086,1).
\]

Then D strictly owns K*=(.54,−.01). In the original coordinates, this is (2.54,1.99).

**Proof.** Write U,V for the lower band coordinates. The following first forced faces repeat the support argument of Theorem 2 in `C1084-DUPLICATE-POINT.md`, with the changed endpoint checked here.

The point G has both upper bands strict by N, so it is lower-u or lower-v. If G were lower-v, then F has its upper u-band strict by A and its lower v-band strict by N; an upper-v exclusion of F would give a≤c. Thus F must be lower-u. At T both lower bands are strict by N. An upper-v exclusion would give a≤c−.47s≤1, using the assumed lower-v face at G. Thus T must be upper-u. Its separation from F then gives a≤.47c<1. This contradiction proves

\[
U\ge .26c. \tag{38}
\]

At R the lower u-band is strict by N and the upper v-band is strict by A. An upper-u exclusion would imply a≤.826c<1 by (38). Therefore

\[
V\ge-1.086s. \tag{39}
\]

At H both lower bands are strict by A. An upper-v exclusion would give a≤c≤1 by (39), so H is upper-u. It follows that

\[
a\le .826c+s,\qquad s>.174. \tag{40}
\]

Both lower bands of P are strict by A. If P were upper-v, (39) would give a≤c+.086s. Since c≤1−s²/2 and a>1, this would imply s<.172, contradicting (40). Hence

\[
U+a\le c+s. \tag{41}
\]

The upper u-band of K* is strict by A, and its upper v-band is strict by N. It remains to check the two lower bands.

For the lower u-band, T again has both lower bands strict by N and hence is upper-u or upper-v. In its upper-u case,

\[
u(T)-u(K*)=.19c+1.01s
\le\frac{1.20}{\sqrt2}<1<a,
\]

so U<u(K*). In its upper-v case, (39) gives a≤c+.356s. Put h=s/(1+c). The strict inequality a>1 implies h<.356=89/250. The function .46 cos θ+1.01 sin θ is increasing throughout the canonical interval. At h=89/250,

\[
c=\frac{54579}{70421},\qquad s=\frac{44500}{70421},
\]

and therefore

\[
.46c+1.01s
\le \frac{3502567}{3521050}<1. \tag{42}
\]

The numerator is smaller than the denominator by 18483. Combining (41) with u(P)−u(K*)=.46c+1.01s proves U<u(K*) in this case too.

For the lower v-band, if s/c≥27/46 then

\[
v(K*)-v(A)=.46s-.27c\ge0,
\]

and strict ownership of A supplies the band. Otherwise

\[
s<\frac{27}{\sqrt{2845}}<.51.
\]

An upper-u exclusion of T would now imply, using (38),

\[
a\le .47c+s<.47+.51=.98,
\]

which is impossible. Thus T is upper-v, and (40) yields

\[
v(T)-v(K*)=1.01c-.19s
<1.01-.19(.174)=.97694<1<a.
\]

It follows that V<v(K*). All four bands are strict, so K* is strictly owned. The zero-angle case is already impossible in (40), and all tangencies at excluded points and the canonical diagonal endpoint are included. ∎

### Exact conditional C981 closure and the remaining obligation

**Corollary 10.** Each of the C981 representatives

\[
59,\ 71,\ 104,\ 105,\ 107,\ 108
\]

is impossible if its actual top square Q₁₁ strictly owns (2.73,3).

**Proof and owner mapping.** The six rows have the following common strict ownership:

| Actual square | Strict points used |
|---|---|
| Q₅ | Its marker (2.35,1.65), auxiliary 4 at (2,1.74), and auxiliary 16 at (2.26,2) |
| Q₆ | Its marker (2.35,2.35), auxiliary 9 at (3,2.26), and auxiliary 19 at (3,2.4) |
| Q₉ | Auxiliary 6 at (2.4,1) |
| Q₁₀ | Its marker (3.086,2) |
| Q₁₁ | Auxiliary 17 at (2.26,3), and the conditional point (2.73,3) |
| Q₃ | The actual northeast corner points (3,3) and (3.086,3) |

The globally absent southwest central marker (1.65,1.65) is excluded from Q₅; it has no artificial owner. The Q₆ marker and the strict Q₉ point supply the other two inward-square exclusions. Corollary 3 of `C1084-DUPLICATE-POINT.md` therefore gives

\[
(2.54,1.99)\in Q_5.
\]

The conditional point and Q₁₁'s auxiliary 17 give the whole strict segment [2.26,2.73]×{3} in that one actual square. Reflect the complete local configuration in y=2 and apply Theorem 8 to Q₆. The strict anchors are the reflected Q₆ marker and its auxiliary 19; the three isolated exclusions come from Q₃, Q₁₀, and Q₅. Consequently Q₆ has strictly positive canonical angle in the original coordinates.

The six exclusions in Theorem 9 now come from Q₅ at G, Q₁₀ at R, Q₁₁ at F and T, and Q₃ at P and H. Applying that theorem to Q₆ gives

\[
(2.54,1.99)\in Q_6,
\]

contradicting disjoint interiors of the actual squares Q₅ and Q₆. ∎

**Status of this particular entrance route.** Section 9 below proves (2.73,3) strict in the actual Q₁₁ of rows 59, 105, 108. Section 11 also proves it for row 71. This reach has not been proved for rows 104, 107, but their complete exclusions now follow by the different actual support routes in `C981-LAST-TWO-CYCLES.md` and Section 8 of `C981-COMMON-CYCLE.md`, respectively. C981 has a paired northwest corner, so the singleton point (1.87,3.24) used to advance the C1084 top square cannot be imported. The corollary remains a completed conditional reduction; it does not assume that extra reach, an orientation interval, a center box, or a stronger auxiliary owner.

## 9. Actual top-wall reach and complete exclusion of rows 59, 105, 108

The following three small support lemmas resolve the missing reach obligation in three of the six representatives of Corollary 10.

**Theorem 11 (wall origin alternative).** Let W be an open square of side a>1 contained in y≤1. Suppose it strictly owns P=(0,e) and B=(r,0), where 0<e<1 and 0<r≤z≤2√2−2. If W excludes O=(0,0), then it strictly owns T=(z,0).

**Proof.** Use canonical coordinates c≥s≥0, c²+s²=1, and lower bands U,V. Put H=c+s. We use

    H−1 = 2cs/(H+1) ≥ (2√2−2)cs ≥ zcs.                 (43)

For u=(c,s), v=(−s,c), the point O has its upper u-band strict by B and both v-bands strict by B and P. Its exclusion therefore forces U≥0. At T the lower u-band is strict by B, its upper v-band is strict by P, and

    u(T)−U ≤ zc < 1 < a.

Only the lower v-band remains. The actual top wall gives

    s(U+a)+c(V+a) ≤ 1.

If V≥−zs, this would imply aH≤1+zcs−sU≤1+zcs≤H, contradicting a>1. Hence the remaining band is strict.

For u=(c,−s), v=(s,c), both u-bands of O are strict by P and B, and its upper v-band is strict by P. Thus V≥0. Both lower bands of T are strict by B, and

    v(T)−V ≤ zs < 1 < a.

The top wall now reads −sU+c(V+a)≤1. If U+a≤zc, it would imply aH≤1+zcs−cV≤H, again impossible. This proves the remaining upper u-band. The axial case is either covered by the displayed contradictions or is already impossible because a strict anchor has the same projection as the excluded O. ∎

**Theorem 12 (the upper-left central tip).** Let N be an open square of side a>1. In coordinates translated by (−2,−3), suppose it strictly owns

    F=(−.26,0), A=(0,−.74), M=(−.35,−.65)

and excludes

    O=(0,0), Z=(−.4,0), B=(−.26,−1),
    R=(.35,−.65), L=(−1,−.2).

Then N strictly owns X=(−.03,0), which is (1.97,3) in the original coordinates.

**Proof.** First consider u=(c,−s), v=(s,c), c≥s≥0. The point Z has its upper u-band strict by A, upper v-band strict by F, and lower v-band strict by M, since

    v(Z)−v(M)=.65c−.05s>0.

Thus Z can be excluded only through the lower u-face. At R the lower u-band is strict by F, lower v-band strict by A, and upper v-band strict by F, because

    v(R)−v(A)=.35s+.09c>0,
    v(F)−v(R)=.65c−.61s≥.04c>0.

Therefore R is on or above the upper u-face. These two exclusions give

    a ≤ .75c+.65s ≤ sqrt(.75²+.65²)=sqrt(.985)<1,

a contradiction. This also excludes the axial case.

Now take u=(c,s), v=(−s,c), with s>0. The point O has its lower u-band strict by F, lower v-band strict by A, and upper v-band strict by F. Hence

    U+a ≤ 0.                                             (44)

The point Z has its upper u-band strict by F and lower v-band strict by A. A lower u-face exclusion would combine with (44) to give a≤.4c<1. Therefore Z must be upper-v:

    V+a ≤ .4s.                                           (45)

The point B has both upper bands strict by F. If B were lower-u, (44) would imply

    a ≤ .26c+s ≤ 1.26/sqrt(2)<1,

where the middle expression is increasing throughout the canonical interval. Thus

    V ≥ .26s−c,       a ≤ c+.14s.                         (46)

The point L has its upper u-band strict by F and its lower v-band strict by A:

    u(F)−u(L)=.74c+.2s>0,
    v(L)−v(A)=s+.54c>0.

If L were upper-v, (46) would give a≤.8c+.74s. Taking three quarters of the bound a≤c+.14s and one quarter of this new bound yields

    a ≤ .95c+.29s ≤ sqrt(.95²+.29²)=sqrt(.9866)<1.

Thus L is lower-u, so U≥−c−.2s.

At X the lower u-band is strict by F, lower v-band strict by A, and upper v-band strict by F. Its upper u-band is strict because

    u(X)−U ≤ .97c+.2s
              ≤ sqrt(.97²+.2²)=sqrt(.9809)<1<a.

All four bands are therefore strict. All inequalities at the five excluded points were weak, so the result includes every tangency. ∎

**Theorem 13 (top wall reach from a nearby foreign tip).** Let W be an open square of side a>1 contained in y≤1. Suppose it strictly owns

    P=(0,.086), B=(.4,0)

and excludes

    L=(−.03,0), A=(0,−.74).

Then W strictly owns T=(.73,0).

**Proof.** For u=(c,s), v=(−s,c), c≥s≥0, the point L has its upper u-band and lower v-band strict by B. Its upper v-band is strict by P, since

    v(P)−v(L)=.086c−.03s≥.056c>0.

Thus U≥−.03c. The target has its lower u-band strict by B and upper v-band strict by P. Also

    u(T)−U≤.76c<1<a.

If its remaining lower v-band failed, V≥−.73s. The top wall would then give

    a(c+s) ≤ 1+.76cs ≤ c+s,

using (43) and .76<2√2−2. This is impossible.

For u=(c,−s), v=(s,c), both upper bands of L are strict by B and P. If L is lower-v, V≥−.03s. The target has both lower bands strict by B and has its upper v-band strict since v(T)−V≤.76s<1<a. A failure of its upper u-band, combined with the top wall −sU+c(V+a)≤1, again gives a(c+s)≤1+.76cs≤c+s, which is impossible.

It remains to consider a lower-u exclusion of L, namely U≥−.03c. Strict ownership of P then forces

    .086s < .03c,       s/c < 15/43.                     (47)

The point A has its lower u-band and upper v-band strict by P. Its upper u-band is strict by B, since

    .74s < .74(15/43)c < .4c.

Thus A must be lower-v, giving V≥−.74c. Both lower bands of T are strict by B, and its two upper bands follow from

    u(T)−U≤.76c<1<a,
    v(T)−V≤.73s+.74c
               < .73(15/43)+.74 = 4277/4300 <1<a.

This proves T strictly in W for every canonical orientation. ∎

### Exact row applications

Consider one of representatives 59, 105, 108. Translate coordinates by (−2,−3), so the actual top wall becomes y≤1. The actual Q₁₁ strictly owns P=(0,.086), auxiliary (.26,0), and B=(.4,0).

If Q₁₁ excludes O=(0,0), Theorem 11 with z=.8 gives (2.8,3) strictly in Q₁₁. Convexity with the owned point (2.4,3) supplies (2.73,3).

Otherwise O is strictly in Q₁₁. Consequently O is excluded from the different actual square Q₇. The remaining inputs to Theorem 12 have the following exact sources:

| Theorem input in original coordinates | Row 59 | Row 105 | Row 108 |
|---|---|---|---|
| Strict F=(1.74,3) in Q₇ | Auxiliary 14 | Auxiliary 14 | Auxiliary 14 |
| Strict A=(2,2.26) in Q₇ | Auxiliary 5 | Auxiliary 5 | Auxiliary 5 |
| Strict M=(1.65,2.35) in Q₇ | Q₇ marker | Q₇ marker | Q₇ marker |
| Excluded Z=(1.6,3) from Q₇ | Auxiliary 3 absent from exact Q₇ label | Auxiliary 3 in Q₄ | Auxiliary 3 in Q₄ |
| Excluded B=(1.74,2) from Q₇ | Auxiliary 13 in Q₅ | Auxiliary 13 absent from exact Q₇ label | Auxiliary 13 in Q₅ |
| Excluded R=(2.35,2.35) from Q₇ | Q₆ marker | Q₆ marker | Q₆ marker |
| Excluded L=(1,2.8) from Q₇ | Actual Q₈, Theorem 4 | Actual Q₈, Theorem 4 | Actual Q₈, Theorem 4 |

Thus Theorem 12 gives the strict point (1.97,3) in the actual Q₇. Both this point and the already owned A=(2,2.26) are excluded from Q₁₁. Theorem 13 therefore applies to Q₁₁ and gives its strict point (2.73,3).

Both exhaustive cases have established the actual reach required by Corollary 10. That corollary now forces the same strict point (2.54,1.99) in the different actual squares Q₅ and Q₆. Each representative is impossible.

At this point the complete continuous original-row exclusions are

    24, 26, 39, 59, 105, 108.

Section 11 additionally closes row 71, giving the final seven-row scope recorded below. The tip lemma above must not be transferred unchanged to row 71, whose Q₇ owns Z; to row 107, whose Q₇ owns B; or to row 104, whose Q₇ does not own F. Their actual auxiliary differences are substantive. The separate whole-segment argument in Section 11 handles row 71 without excluding its owned Z.

## 10. Source ledger for the seven completed original representatives

The sole original ownership entrance is `../original-handoff/03-C981-SHARED-WALL-CYCLES.md`: its Sections 1–2 give the exact marker/auxiliary conventions and retained strict corner points; Section 3 gives rows 24, 26, 39; Section 4 gives rows 59, 71, 105; and Section 5 gives row 108. The marker ownership is common to all seven and is reproduced in the owner mapping above. The exact auxiliary rows relevant to every new inference are:

| Row | Q₀ | Q₁ | Q₂ | Q₃ | Q₄ | Q₅ | Q₆ | Q₇ | Q₈ | Q₉ | Q₁₀ | Q₁₁ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 24 | {2,12} | {0,10} | ∅ | ∅ | ∅ | {4,18} | {7,17} | {5,13} | {1,11} | {6,15} | {9,19} | {3,14} |
| 26 | {2,12} | {0,10} | ∅ | ∅ | ∅ | {4,18} | {7,17} | {5,13} | {1,11} | {6,15} | {8,9,19} | {3,14} |
| 39 | {2,12} | {0,10} | ∅ | ∅ | ∅ | {4,8,18} | {7,17} | {5,13} | {1,11} | {6,15} | {9,19} | {3,14} |
| 59 | {2,12} | {0,10} | ∅ | ∅ | ∅ | {4,13,16} | {9,19} | {5,14} | {1,11} | {6,15} | {8,18} | {7,17} |
| 71 | {2,12} | {0,10} | ∅ | ∅ | ∅ | {4,13,16} | {9,19} | {3,5,14} | {1,11} | {6,15} | {8,18} | {7,17} |
| 105 | {2,12} | {0,10} | ∅ | ∅ | {3} | {4,16} | {9,19} | {5,14} | {1,11} | {6,15} | {8,18} | {7,17} |
| 108 | {2,12} | {0,10} | ∅ | ∅ | {3} | {4,13,16} | {9,19} | {5,14} | {1,11} | {6,15} | {8,18} | {7,17} |

The retained strict singleton point (.76,1.87) in Q₁, the Q₈ marker, auxiliary 11 in Q₈, auxiliary 0 excluded from Q₈, and marker 11 excluded from Q₈ give Theorem 4's left-wall advance. Transpose the coordinates and use the retained strict point (1.87,.76) in Q₀ to get its bottom-wall counterpart in Q₉. These are original stated consequences, not newly inferred singleton positions.

For rows 24, 26, 39, Theorem 7 uses only Q₅'s marker and auxiliaries 4,18; its exact omission of 16; the actual Q₂ corner point (3,1); the actual Q₁₀ marker; and the actual Q₉ segment from auxiliary 15 to its advanced point. Thus no missing auxiliary is assigned an owner.

For rows 59, 105, 108, the table in Section 9 identifies each input to Theorem 12. Section 11 supplies the different exact input table and complete cap argument for row 71; it also gives a unified alternative for all four. The top-wall arguments use the actual Q₁₁ marker and auxiliary 7. The two final duplicate-point lemmas use only the exact central labels, the actual Q₉ marker/auxiliary data already specified, and the actual Q₃ corner. These four proofs need neither an ordinary-center consequence for Q₇, nor a propagated auxiliary domain, nor an assumed upper bound on a. All square separations used are consequences of the original pairwise disjoint interiors; all whole segments used lie strictly inside one explicitly named owner. This chapter's own completed scope is seven original rows. The companion `C981-COMMON-CYCLE.md` closes eight more with a single common ending, and `C981-LAST-TWO-CYCLES.md` completes 29 and 104. Together the three chapters continuously exclude all seventeen targets.

## 11. The whole left-wall segment closes row 71 as well

The distinction between a whole foreign segment and its two endpoints is decisive here. Row 71 owns auxiliary 3 in Q₇, so Theorem 12 cannot be used unchanged. The following two lemmas replace that excluded-point premise by the actual Q₈ segment and cover both signs of Q₇'s angle.

**Theorem 14 (a tip or a shallow circular cap).** In coordinates translated by (−2,−3), let N be an open square of side a>1 strictly owning

    F=(−.26,0), A=(0,−.74).

Suppose it excludes O=(0,0), B=(−.26,−1), and the whole segment

    J L = {−1}×[−.74,−.2].

Then the axial orientation is impossible. For a positive canonical angle, N strictly owns X=(−.03,0). For a negative canonical angle, every point of the compact region

    C = { (x,y): −.26≤x≤0, −.0345≤y≤0,
                    (x+.26)²+(y+1)²≤1 }                 (48)

is strictly in N.

**Proof for a positive canonical frame.** Write u=(c,s), v=(−s,c), c≥s>0, with lower faces U,V. The owned F,A give strict lower u, lower v, and upper v bands at O. Hence U+a≤0. The excluded B has both upper bands strict by F. If B were lower-u, the upper-u bound at O would give

    a≤.26c+s≤1.26/sqrt(2)<1.

Consequently

    V≥.26s−c.                                            (49)

The point L=(−1,−.2) has its upper u-band strict by F and its lower v-band strict by A. If L is lower-u, the three direct strict bands at X and the estimate

    u(X)−u(L)=.97c+.2s≤sqrt(.9809)<1<a

give X strictly, as before.

Suppose instead that L is upper-v, so V+a≤s−.2c. At J=(−1,−.74), its upper u-band and lower v-band are strict by A. An upper-v exclusion would combine with (49) to give

    a≤v(J)−v(B)=.26c+.74s≤sqrt(.6152)<1.

Thus J is lower-u, U≥−c−.74s.

These two endpoint faces, together with exclusion of the whole segment, force the entire closed square N to lie in x≥−1. Indeed any interior point of N on x=−1 would have, from its strict u and v bands,

    y>−.74,       y<−.2.

It would lie on the excluded segment. If the minimum x coordinate of the closed square were less than −1, an interior point with x<−1 joined to the strict anchor A with x=0 would give just such an interior point on the line. Therefore

    cU−s(V+a)≥−1.                                        (50)

At X the lower u-band is strict by F, lower v-band strict by A, and upper v-band strict by F. Suppose its last band failed, so U+a≤−.03c. Combining this with (49) and (50) gives

    a(c+s)≤1−.03c²−.26s²+cs.                            (51)

But c+s−1≥(2sqrt(2)−2)cs>.828cs, and

    .03c²+.26s²−.172cs
      = (3/100)(c−(43/15)s)²+(101/7500)s² >0.

Thus the right side of (51) is strictly less than c+s, a contradiction. This proves the positive-angle conclusion.

**Proof for a negative canonical frame.** Put u=(c,−s), v=(s,c), c≥s≥0. At B, its lower u-band is strict by F, upper u-band strict by A, and upper v-band strict by F. Therefore

    V≥−.26s−c=v(B).                                      (52)

Let Y=(x,y) belong to C. The lower u-band follows from F because

    u(Y)−u(F)=(x+.26)c−ys≥0.

The upper u-band follows from A because

    u(A)−u(Y)=−xc+(y+.74)s≥0.

Its lower v-band follows strictly from A, since

    v(Y)−v(A)=xs+(y+.74)c
                ≥(.48−.0345)c>0.

Finally, the defining disk inequality in (48) gives

    v(Y)−V≤v(Y)−v(B)
       =(x+.26)s+(y+1)c≤sqrt((x+.26)²+(y+1)²)≤1<a.

Thus the upper v-band is strict too. Every point of C is genuinely interior, including its circular boundary. For an axial square F and A already supply both bands at O, so the assumed exclusion of O is impossible. ∎

**Theorem 15 (top-wall reach past a foreign shallow cap).** Let W be an open square of side a>1 contained in y≤1, strictly owning

    P=(0,.086), D=(.4,0),

and excluding every point of C in (48). Then W strictly owns T=(.73,0).

**Proof.** The cap contains the following three exact points:

    F=(−.26,0), Y₀=(0,−p), Y₄=(−.2,−.002), p=.0345.

Indeed

    .26²+.9655²=.99979025<1,
    .06²+.998²=.999604<1.

It also contains the circular arc points used below.

First take u=(c,s), v=(−s,c), c≥s≥0. The target already has its lower u-band strict by D and upper v-band strict by P, so it can fail only through the upper u-face or lower v-face.

Suppose T is upper-u. The point F has its upper u-band and lower v-band strict by D. A lower-u exclusion of F would give a≤.99c<1. Thus F is upper-v. Strict ownership of P then forces

    .086c<.26s,       s/c>43/130.                        (53)

At Y₀, the upper u-band is strict by D and upper v-band by P. Its lower v-band is strict by D because .4s>pc in (53). Its lower u-band is strict from the upper-u bound at T, since

    u(T)−u(Y₀)=.73c+ps≤sqrt(.73²+p²)<1<a.

This would put the excluded Y₀ strictly in W, a contradiction.

It remains in this frame to suppose T is lower-v, V≥−.73s. The point F again has its upper u-band and lower v-band strict by D. An upper-v exclusion of F would give a≤.99s<1. Therefore U≥−.26c. The top wall gives

    a(c+s)≤1+.99cs.                                      (54)

The case s=0 contradicts a>1. For s>0, (54) implies

    2/(c+s+1)<.99,       c+s>101/99,       s>2/99.        (55)

Both upper bands of Y₀ are strict by P, so it is lower-u or lower-v. A lower-u exclusion U≥−ps would, with the top wall and the lower-v bound at T, imply

    a(c+s)≤1+.73cs+ps²
              ≤1+(.73+p)cs<c+s,

because .73+p=.7645<2sqrt(2)−2. Thus Y₀ is lower-v, V≥−pc. Strict ownership of D then yields

    s/c<p/.4=69/800,       c+s<869/800.                 (56)

At Y₄ both upper bands are strict by D and P; the upper v comparison uses .088c−.2s>0 from (56). If Y₄ were lower-u, the wall inequality would give

    a(c+s)≤1+.93cs+.002s²≤1+.932cs<c+s,

where the last comparison follows from

    2/(c+s+1)>1600/1669>.932.

Hence Y₄ is lower-v, V≥.2s−.002c. Combining this with the strict inequality V<−.4s from D gives s/c<1/300 and therefore s<1/300. This contradicts (55). The target is strict for every nonnegative canonical angle.

Now take u=(c,−s), v=(s,c), c≥s≥0. Both lower bands of T are strict by D, so an exclusion is upper-u or upper-v. If T is upper-v, then Y₀ has both u-bands strict by P,D and its upper v-band strict by P. Its lower v-band follows from

    v(T)−v(Y₀)=.73s+pc≤sqrt(.73²+p²)<1<a.

Again Y₀ would be strict in W. Thus only an upper-u exclusion of T remains:

    U+a≤.73c.                                            (57)

For every Y=(x,y) in C its lower u-band is now strict, because

    u(T)−u(Y)=(.73−x)c+ys≤.99c<1<a.

Its upper u-band is strict by D, since u(Y)≤ps<.4c, and its upper v-band is strict by P, since v(Y)≤0<.086c. The exclusion of each such Y therefore forces V≥v(Y).

If 0≤s≤.26, take the point

    Y=(s−.26,c−1).

It belongs to C: its squared distance to (−.26,−1) is one, and c≥sqrt(1−.26²)>.9655. Hence

    V≥v(Y)=1−c−.26s.

The wall inequality and (57) then give

    a(c+s)≤1−c+c²+.99cs≤c+s.

For the last comparison, subtract c+s and use 1−c≤s:

    (1−c)²−s+.99cs
      ≤s(1−c)−s+.99cs=−.01cs≤0.

This contradicts a>1.

If s>.26, use Y₀ to get V≥−pc. Equations (57) and the top wall give

    a(c+s)≤1+.73cs+pc².                                 (58)

The right side is less than c+s, as the following two rational bounds verify. For .26<s<1/3, one has (c+s)²=1+2cs<5/3<1.3², so

    c+s−1>(20/23)cs,

and consequently

    c+s−1−.73cs−pc²
       > c²[(20/23−.73)(s/c)−p]
       > c²[(20/23−.73)(.26)−.0345] >0.

For s≥1/3, one has s/c≥1/sqrt(8)>.353, and c+s−1>.828cs. Hence

    c+s−1−.73cs−pc²
       >c²[.098(s/c)−.0345]
       >c²[.098(.353)−.0345]=.000094c²>0.

Thus (58) also contradicts a>1. Every excluded face was weak throughout, and the arc points used have strict membership in N even when their disk distance equals one. ∎

### Complete row 71 application and the unified four-row reach

**Corollary 16.** The actual Q₁₁ strictly owns (2.73,3), and the representative is impossible, in each of rows

    59, 71, 105, 108.

For the three previously closed rows, Section 9 already proves this. For row 71, translate by (−2,−3) and write W=Q₁₁, N=Q₇. The actual W owns P=(0,.086), D=(.4,0), and (.26,0). If it excludes O, Theorem 11 gives the farther point (.8,0), hence (.73,0).

Otherwise O is strictly in W and excluded from N. Theorem 14 has exactly the following actual inputs:

| Input | Genuine source in row 71 |
|---|---|
| N owns F=(1.74,3) | Q₇ auxiliary 14 |
| N owns A=(2,2.26) | Q₇ auxiliary 5 |
| N excludes O=(2,3) | Strict point of the different actual Q₁₁ in this case |
| N excludes B=(1.74,2) | Q₅ auxiliary 13 |
| N excludes {1}×[2.26,2.8] | One strict segment in actual Q₈, from auxiliary 1 and Theorem 4 |

A positive canonical angle of N yields its strict point (1.97,3), and Theorem 13 applied to W gives (2.73,3). A negative canonical angle yields the whole strict region C in N, so Theorem 15 gives the same point in W. The axial case is impossible. Corollary 10 then gives the shared strict point (2.54,1.99) in Q₅ and Q₆, a contradiction.

The extra point (1.6,3) owned by Q₇ in row 71 is never used as an exclusion. This is the required difference from the earlier tip lemma. The identical inputs also hold in rows 59, 105, 108, so this provides a unified reach argument for all four.

**Representatives completed within this chapter:**

    24, 26, 39, 59, 71, 105, 108.

The companion `C981-COMMON-CYCLE.md` additionally completes 2,28,30,37,43,69,103,107, and `C981-LAST-TWO-CYCLES.md` completes 29,104. Thus all seventeen targets have new continuous endings. The particular top-reach entrance of Corollary 10 has not been proved in rows 104 and 107; their completed endings use other actual support consequences.

## 12. Historical top-reach route for rows 104 and 107

Rows 104 and 107 retain the conditional complete exclusion of Corollary 10: it suffices to prove the actual point (2.73,3) strictly in Q₁₁. The following additional strict points are available without any ordinary-center premise:

    (2.54,1.99) ∈ Q₅,       (1.46,2.01) ∈ Q₇.            (59)

The first is Corollary 3 of `C1084-DUPLICATE-POINT.md`, with its original orientation. The second is the same theorem after the half-turn (x,y)↦(4−x,4−y). The complete sources for the second application are:

| Half-turned theorem input | Actual strict owner or exclusion source in both rows |
|---|---|
| Owned marker (1.65,2.35) | Q₇'s original northwest marker |
| Owned anchor (2,2.26) | Q₇ auxiliary 5 |
| Owned anchor (1.74,2) | Q₇ auxiliary 13 |
| Excluded marker (2.35,2.35) | The different actual Q₆ |
| Excluded marker (1.65,1.65) | The genuinely missing original marker |
| Excluded point (1.6,3) | The different actual Q₄, auxiliary 3 |

The points in (59) belong to different positions and are not a duplicate-point contradiction. They can be joined only to points of their respective same owners. No ownership of (2,2) has been inferred from them.

The remaining top auxiliary difference is exact: row 104 has (1.74,3) strictly in Q₁₁ and not in Q₇, whereas row 107 has it strictly in Q₇ and not in Q₁₁. Both rows have (1.74,2) strictly in Q₇. Thus Theorem 14's lower excluded point is unavailable in both rows, and its upper owned point is unavailable in row 104. Neither the tip theorem nor the cap theorem is applied beyond its stated hypotheses.

The unproved step in this particular route is the actual Q₁₁ reach (2.73,3). It is not used in either completed exclusion: Section 8 of `C981-COMMON-CYCLE.md` completes row 107 by transposition, and `C981-LAST-TWO-CYCLES.md` completes row 104 by the actual right-wall and two-central angle contradiction. The historical route above is retained to distinguish its precise conditional premise from the support consequences actually proved. No unproved reach, support bound, center, or favorable orientation enters the seventeen completed replacements.
