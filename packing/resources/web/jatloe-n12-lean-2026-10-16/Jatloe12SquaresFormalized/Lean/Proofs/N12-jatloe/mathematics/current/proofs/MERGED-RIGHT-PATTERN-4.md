# The final merged-right pattern: one strict duplicate point

## 1. A universal strict point in the southwest central square

**Theorem A (southwest-square strict point).** Let A be an open square of side a>1. Suppose A strictly
owns

    C=(1.65,1.65),  P=(2,1.74),  D=(1.74,2),

and excludes the four points

    L=(1,1.65),    B=(1.74,1),
    L'=(1.65,1),   B'=(1,1.74).

Then A strictly owns

    K=(1.95,1.95).

Every terminating decimal is an exact rational. The theorem holds for
every orientation, with no restriction on the center and no upper bound
on a. Its four exclusions are point exclusions; no artificial foreign
segment is required in the theorem.

In the merged-right families C48,C573,C574, the three strict anchors
are part of A's established common strict hull. The genuine singleton
owner V strictly owns {1}×[1.12,1.74], so it owns L and B'. The genuine
singleton owner O strictly owns [1.12,1.74]×{1}, so it owns B and L'.
Their interiors are disjoint from A. Thus all premises follow from the
common physical configuration, independently of the choice of owner of
F5 and independently of the varying bottom owner B of the family.
The letter B in this local theorem denotes the displayed point, not
that varying square.

## 2. Proof of the southwest-square theorem

If two points have Euclidean distance less than a, they cannot be at
or beyond opposite parallel faces of a side-a square. Indeed, their
projections on that unit face normal would then differ by at least a.
The assertion includes points on the face lines.

Translate the coordinates by (-2,-2). Our three strict anchors become

    C=(-.35,-.35),  P=(0,-.26),  D=(-.26,0),

and the points used in the nonnegative-angle proof are

    L=(-1,-.35),  B=(-.26,-1),  K=(-.05,-.05).

The three exact distance squares needed below are

    |L-B|^2 = (.74)^2+(.65)^2 = 9701/10000 < 1,
    |K-L|^2 = (.95)^2+(.30)^2 = 397/400 < 1,
    |K-B|^2 = (.21)^2+(.95)^2 = 4733/5000 < 1.

All three distances are consequently strictly smaller than a.

First suppose A has a nonnegative canonical frame

    u=(c,s),  v=(-s,c),
    c>=s>=0,  c^2+s^2=1.

Write its strict face inequalities as

    U<u·X<U+a,     V<v·X<V+a.

The point K satisfies the strict lower u band and both strict v bands,
because

    u·(K-C) = .30(c+s) > 0,
    v·(K-P) = .05s+.21c > 0,
    v·(D-K) = .21s+.05c > 0.

If K were not in A, its only possible exit would therefore be the
upper u face:

    u·K>=U+a.                                           (1)

At L, the upper u band and lower v band are strict by comparison
with the owned point C:

    u·(C-L) = .65c > 0,
    v·(L-C) = .65s >= 0.

Thus the excluded L can only leave through the lower u face or the
upper v face. The distance |K-L|<a and (1) forbid its lower u exit.
It must be upper-v:

    v·L>=V+a.                                           (2)

At B, both upper bands are strict, because

    u·(D-B) = s >= 0,
    v·(C-B) = .09s+.65c > 0.

Thus the excluded B can only leave through the lower u or lower v
face. The distance |L-B|<a and (2) forbid its lower v exit. It must
be lower-u:

    u·B<=U.                                             (3)

But (1),(3) contradict |K-B|<a. This proves K is strictly interior
for every nonnegative canonical angle. The comparisons with zero
increments remain strict band conclusions because the comparison
points C and D are strict interior points, so the axis and diagonal
endpoints are covered.

For a negative canonical angle, reflect the whole local configuration
by (x,y)↦(y,x). The reflected square has a nonnegative canonical
frame after exchanging its two face normals. The strict anchors P,D
are exchanged and C is fixed. The excluded points L,B are supplied
by the reflections of L',B', respectively. Finally K is fixed. The
nonnegative-angle result therefore applies to the reflected actual
square and proves K belongs strictly to the original A as well.
This completes the theorem for every orientation.


## 3. The exact compulsory point in N

Theorem 9 of `OTHER-GEOMETRY.md`, using the actual top container wall and the strict corner segment {3}×[3,3.6], proves the additional strict top-square point (2,3)∈T. Theorem 6 of `C981-WALL-CYCLES.md`, under transposition of the entire configuration, proves that N has strictly positive canonical angle. Its exact hypotheses are N's strict marker (1.65,2.35), N's auxiliary point (1.6,3), the foreign points (1,3)∈K, (2,3.086)∈T, (2,2.26)∈W, and the actual strict L segment {1}×[2.26,2.8].

Apply Theorem 10 of `OTHER-GEOMETRY.md` in N's rotated and translated coordinates

\[
(\xi,\eta)=(y-2,2-x).
\]

That theorem applies to a positive-angle square owning (.35,.35),(1,.26), and excluding (.26,0),(1,0),(1,1) and the whole [.26,.8]×{1}. Here the two owned points are N's (1.65,2.35),(1.74,3); the three isolated exclusions are respectively W's (2,2.26), T's newly proved (2,3), and K's (1,3); the whole segment belongs to L. No exclusion is an invented owner assignment.

The theorem proves an exact half-angle interval 13/87<t<1/5 and, from four strict square-band comparisons, the open region of points (α,−β) satisfying

\[
\frac7{20}\le\alpha\le\frac12,\qquad
0\le\beta\le\frac15,\qquad
12\alpha-5\beta>4,\qquad
5655\alpha+18500\beta<5369.
\]

Choose α=121/300 and β=1/6. The last two inequalities have exact positive margins 1/150 and 289/60. Returning to the original coordinates gives

\[
E_*:=\left(\frac{13}{6},\frac{721}{300}\right)\in N
\quad\text{strictly}. \tag{1}
\]

The complete proof of the region theorem includes the axis, all face alternatives, endpoint tangencies, and the strict interpolation through the genuine foreign segment. This step does not use any separation assertion about the complete squares A and W.

## 4. A merged square forced to own the same central point

**Theorem B (merged-square strict point).** Let W be an open square of side a>1. In coordinates translated by (−2,−2), suppose W strictly owns

\[
P=(.35,-.35),\qquad Q=(.35,.35),\qquad H=(0,.26),
\]

and excludes

\[
F=(0,-.26),\qquad J=(1,-.26),\qquad
B=(543/500,0),\qquad E=(1/6,121/300).
\]

Then W strictly owns

\[
K_*=(-1/20,-1/20).
\]

No container hypothesis, upper side bound, or equality of the side with any neighboring square is needed.

**Proof.** Set α=121/300 and β=1/6. Every square has a canonical positive or negative frame with c≥s≥0 and c²+s²=1. Write its strict bands as U<u·X<U+a and V<v·X<V+a. All exclusions allow equality with a supporting line.

First suppose the negative frame u=(c,−s), v=(s,c) is available. The point F has strict upper u-band by P, strict upper v-band by H, and strict lower u-band by H. The corresponding projection differences are

\[
u(P)-u(F)=.35c+.09s>0,\qquad
v(H)-v(F)=.52c>0,\qquad
u(F)-u(H)=.52s\ge0.
\]

Thus its exclusion forces V≥−.26c. At E, both u-bands and the lower v-band are strict:

\[
\begin{aligned}
u(E)-u(H)&=\frac16c-\frac{43}{300}s
\ge\frac7{300}c>0,\\
u(Q)-u(E)&=\frac{11}{60}c+\frac4{75}s>0,\\
v(E)-v(H)&=\frac16s+\frac{43}{300}c>0.
\end{aligned}
\]

Hence E can leave only through the upper v-face. Together with the bound from F, this yields

\[
a\le\frac16s+\frac{199}{300}c
\le\sqrt{\left(\frac16\right)^2+\left(\frac{199}{300}\right)^2}
=\frac{\sqrt{42101}}{300}<1,
\]

a contradiction. This excludes the negative frame, including s=0.

We may therefore use the strictly positive frame u=(c,s), v=(−s,c), with s>0. At F its two upper bands are strict by H, and its lower v-band is strict by P, because

\[
v(F)-v(P)=.35s+.09c>0.
\]

Consequently

\[
U\ge-.26s. \tag{2}
\]

At J the lower u-band is strict by P, and the upper v-band is strict by H. An upper u-face exclusion would give a≤c by (2). Thus J must leave through the lower v-face:

\[
V\ge-s-.26c. \tag{3}
\]

The point E has strict lower u-band by H, strict lower v-band by P, and strict upper u-band by Q:

\[
\begin{aligned}
u(E)-u(H)&=\frac16c+\frac{43}{300}s>0,\\
v(E)-v(P)&=\frac{11}{60}s+\frac{113}{150}c>0,\\
u(Q)-u(E)&=\frac{11}{60}c-\frac4{75}s
\ge\frac{13}{100}c>0.
\end{aligned}
\]

It therefore leaves through its upper v-face:

\[
V+a\le\frac{121}{300}c-\frac16s. \tag{4}
\]

Combining (3) and (4),

\[
1<a\le\frac{199}{300}c+\frac56s. \tag{5}
\]

The expression on the right increases strictly throughout the canonical angle interval, since 5/6>199/300. At half-angle t=s/(1+c)=7/25, its exact value is

\[
\frac{199}{300}\frac{288}{337}
+\frac56\frac{175}{337}
=\frac{50531}{50550}<1.
\]

Therefore

\[
t>\frac7{25}. \tag{6}
\]

At B the lower u-band is strict by P and the upper v-band is strict by H. If B left through its lower v-face, then V≥−(543/500)s, and (4) would give

\[
a\le\frac{121}{300}c+\frac{1379}{1500}s
\le\frac{496}{375\sqrt2}<1.
\]

The middle inequality holds because the expression increases on 0≤θ≤π/4, and the last is the exact integer inequality 496²<2·375². Thus B must leave through its upper u-face:

\[
U+a\le\frac{543}{500}c. \tag{7}
\]

We now check K*=(-1/20,-1/20) in all four strict bands. The two upper bands are strict by H:

\[
u(H)-u(K_*)=.05c+.31s>0,\qquad
v(H)-v(K_*)=.31c-.05s>0.
\]

For the lower v-band, (4) is sufficient, since

\[
v(E)-v(K_*)=\frac{34}{75}c-\frac{13}{60}s
\le\frac{34}{75}<1<a.
\]

For the lower u-band, consider

\[
u(B)-u(K_*)=\frac{142}{125}c+\frac1{20}s.
\]

This decreases strictly for every angle with t≥7/25: its derivative is c/20−(142/125)s<0, using s/c≥175/288. At t=7/25 it equals

\[
\frac{142}{125}\frac{288}{337}
+\frac1{20}\frac{175}{337}
=\frac{167959}{168500}<1.
\]

Thus (6)–(7) give u(B)−u(K*)<1<a and U<u(K*). All four bands are strict, proving K*∈W. The proof has retained every exterior tangency as a weak face inequality, and all membership conclusions follow from strict interior comparisons or a>1. ∎

## 5. Exact pattern mapping and complete exclusion

In merged-right pattern 4, W is the actual owner of both right central markers and the additional auxiliary point F₅=(2,2.26). Under translation by (−2,−2), its three strict points and four exclusions in Theorem B are exactly:

| Theorem B datum | Original point | Actual owner |
|---|---|---|
| P=(.35,−.35) | (2.35,1.65) | W |
| Q=(.35,.35) | (2.35,2.35) | W |
| H=(0,.26) | (2,2.26) | W, by pattern 4 |
| F=(0,−.26) | (2,1.74) | A |
| J=(1,−.26) | (3,1.74) | I |
| B=(543/500,0) | (3.086,2) | R |
| E=(1/6,121/300) | (13/6,721/300) | N, by (1) |

The actual squares are distinct and have disjoint open interiors. Every foreign strict point in the table is consequently excluded from W. Theorem B proves

\[
(39/20,39/20)=(1.95,1.95)\in W
\quad\text{strictly}. \tag{8}
\]

Theorem A proves that the same point is strictly in the different actual square A. Its foreign segment points are supplied by the actual singleton owners O and V, as mapped in Section 2. Thus (8) contradicts the disjointness of A and W.

This is a complete continuous exclusion of merged-right pattern 4. It applies uniformly to its occurrences in C48, C573, and C574. The argument uses actual owners at every stage, permits all allowed tangencies, and does not rely on sampled angles, numerical feasibility, an artificial finite hull serving as a complete square, or a split of the merged owner W into two squares.

Together with Corollary 4 of `OTHER-GEOMETRY.md` (pattern 3), Corollary 8 there (patterns 1 and 5), and the retained short arguments for patterns 2, 6, and 7, all seven merged-right alternatives now have complete mathematical exclusions.
