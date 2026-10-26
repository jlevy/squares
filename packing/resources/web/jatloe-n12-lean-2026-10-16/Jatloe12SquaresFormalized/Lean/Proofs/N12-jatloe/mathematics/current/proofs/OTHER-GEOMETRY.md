# Continuous geometric replacements for Chapter 04

## 1. An anchor-and-exclusion theorem for a long chord

**Theorem 1.** Let Q be an open square of side a>1. No container assumption is needed. Suppose that, for some parameters

\[
0<d\le\frac1{10},\qquad p\ge d,\qquad r\ge\frac{29}{40},
\]

Q strictly contains P=(0,-p) and R=(r,0), and does not contain E=(-d,0). Then Q has an open chord of length strictly greater than one on the line x=1/2.

The conclusion is unchanged under a simultaneous translation, rotation, or reflection of Q, the three points, and the line. The excluded point need not be strictly exterior; boundary exclusion suffices.

### Proof

Choose canonical orthonormal face normals with c≥s≥0 and c²+s²=1. There are two signs to consider. If the normals are u=(c,s), v=(-s,c), write Q as

\[
U<u\cdot z<U+a,\qquad V<v\cdot z<V+a.
\]

The point E has projections -dc and ds. Since R is strict, E cannot escape through the upper u-face; since P is strict, it cannot escape through the lower v-face. Consequently at least one of

\[
U\ge-dc,\qquad V+a\le ds
\]

holds. No strictness has been assumed in these alternatives.

Write x_+ for the rightmost abscissa of the closed square. Here

\[
x_+=c(U+a)-sV.
\]

In the first alternative, strict membership of R gives V<-rs. Therefore

\[
x_+\ge ac-dc^2+rs^2,
\]

with a strict inequality when s>0. For s=0, a>1 will provide the strict inequality below. In the second alternative, strict membership of R gives U>rc-a, and hence

\[
x_+>as+rc^2-ds^2.
\]

Now consider the other sign, u=(c,-s), v=(s,c). The excluded E has projections -dc and -ds. Its upper-face alternatives are impossible by R; its lower v-face alternative is impossible because P has v-projection -pc≤-dc≤-ds and is strict. Thus U≥-dc. As V>rs-a by strict ownership of R,

\[
x_+=c(U+a)+s(V+a)\ge ac-dc^2+rs^2.
\]

Again the weak inequality is sufficient because a>1 and c>0. These arguments include s=0 and c=s; no division by s occurred.

We next prove the two elementary inequalities

\[
c-dc^2+rs^2\ge\frac12+cs,
\qquad
s+rc^2-ds^2>\frac12+cs. \tag{1}
\]

For the first, c≥1/√2>2/3 gives

\[
c\ge1-\frac35s^2,
\]

because the difference is (1-c)(3c-2)/5≥0. Using d≤1/10 and r≥29/40, we obtain

\[
\begin{aligned}
c-dc^2+rs^2-\frac12-cs
&\ge\left(\frac12-d\right)c^2+\left(r-\frac1{10}\right)s^2-cs\\
&\ge\frac25c^2+\frac58s^2-cs\\
&=\frac25\left(c-\frac54s\right)^2\ge0.
\end{aligned}
\]

For the second, put t=s/c∈[0,1]. Multiplication by 1+t² gives

\[
(1+t^2)\left(s+rc^2-ds^2-\frac12-cs\right)
=r-\frac12-\left(d+\frac12\right)t^2+t(\sqrt{1+t^2}-1).
\]

On [0,1], √(1+t²)≥1+(2/5)t²: both sides are nonnegative, and subtracting their squares gives t²(5-4t²)/25≥0. Thus the last expression is at least

\[
\frac9{40}-\frac35t^2+\frac25t^3
=\frac1{40}+\frac15(1-t)^2(2t+1)>0.
\]

This proves (1). In every face alternative, therefore,

\[
x_+>\frac12+cs. \tag{2}
\]

Let X be Q's center abscissa and H=a(c+s)/2 its horizontal support radius. Equation (2) says X+H>1/2+cs. Strict membership of P, whose abscissa is zero, says X-H<0. Consequently

\[
H-|X-\tfrac12|
=\min(\tfrac12-(X-H),(X+H)-\tfrac12)>cs,
\]

because the first entry is greater than 1/2≥cs and the second is greater than cs. For s>0, the exact chord formula gives

\[
\ell=\min\left(\frac a c,\frac{H-|X-1/2|}{cs}\right)>1.
\]

For s=0, the same strict inequalities place x=1/2 strictly between the vertical sides, and the chord length is a>1. This completes the proof. ∎

### Exact applications to Chapter 04

All the relevant singleton anchors have p=d=43/500 and r=37/50, so they satisfy the theorem with room to spare.

| Case(s) | Actual target square | Owned P after transport | Owned R after transport | Excluded E after transport | Long-chord line |
|---|---|---|---|---|---|
| C702 | owner 0, mask 1 | (1,.914) | (1.74,1) | (.914,1) | x=3/2 |
| C1072 | owner 0, mask 1 | (1,.914) | (1.74,1) | (.914,1) | x=3/2 |
| C888, C889, C893 | owner 3, mask 16 | (3,3.086) | (2.26,3) | (3.086,3) | x=5/2 |

The first two applications translate the theorem by (1,1). The last application maps (x,y) to (3-x,3-y). Each excluded E is an original marker outside the indicated singleton's exact original signature, so no extra auxiliary exclusion has been introduced. In particular, moving marker 5 between other owners in C889 or C893 has no effect on this argument: owner 3 still excludes that marker.

This replaces one of the four angle-dependent reach checks in each of five listed common-line families. It proves the required long chord directly and does not require the stronger sufficient bound using the side-one radius ρ. It does not by itself supply the other three chords or exclude any complete family.

## 2. A wall theorem replacing the boundary-target reach calculations

**Theorem 2.** Let Q be an open square of side a>1 whose closure lies in y≥0. Suppose Q strictly contains

\[
(2,.914),\qquad(2.4,1),
\]

and excludes

\[
(2.35,1.65),\qquad(1.87,.76),\qquad(1.74,1).
\]

Then its chord on x=5/2 has length strictly greater than one. No center bound, upper side bound, or restriction on the angle is required.

### Proof

Translate by (-2,-1), and put

\[
P=(0,-d),\quad R=(r,0),\quad
E=(-e,-k),\quad F=(-f,0),\quad H=(b,h),
\]

where

\[
d=.086,\quad r=.4,\quad e=.13,\quad k=.24,\quad
f=.26,\quad b=.35,\quad h=.65.
\]

The square lies in y≥-1. We prove that its rightmost abscissa x_+ satisfies

\[
x_+>\frac12+cs,\qquad c\ge s\ge0,\quad c^2+s^2=1. \tag{3}
\]

Together with the strict owned point P at x=0, this proves the chord assertion exactly as in Theorem 1.

Use lower band coordinates U,V and distinguish the two canonical signs. Throughout the proof, a weak exterior inequality is allowed for an excluded point. Incompatible opposite-face assignments will be ruled out using

\[
(.61)^2+(.65)^2=.7946<1,
\qquad
(.13)^2+(.24)^2=.0745<1. \tag{4}
\]

**Positive sign:** u=(c,s), v=(-s,c). The strict anchors restrict F to its lower u-face or upper v-face; E to one of its two lower faces; and H to one of its two upper faces. These assertions follow directly by comparing projections with P and R. For example, E has both projections below P's: the second comparison uses .13s-.24c<-.086c because s≤c.

If F exits through the lower u-face, U≥-fc. An upper u-face exclusion of H would imply

\[
a\le (b+f)c+hs=.61c+.65s<1
\]

by (4), so H must exit through its upper v-face. Thus V+a≤-bs+hc and

\[
x_+=c(U+a)-sV\ge a(c+s)-fc^2+bs^2-hcs. \tag{5}
\]

If instead F exits through the upper v-face, V+a≤fs. A lower v-face exclusion of E would give

\[
a\le(f-e)s+kc=.13s+.24c<1,
\]

so E exits through its lower u-face, U≥-ec-ks. Consequently

\[
x_+\ge a(c+s)-ec^2-(k+f)cs. \tag{6}
\]

This exhausts the positive sign, including zero sine.

**Negative sign:** u=(c,-s), v=(s,c). F and E can each escape only through lower faces. H can escape only through its lower u-face or upper v-face. For E, its u-projection is at most (.24-.13)c=.11c<rc, and its v-projection is below P's, so its two upper-face alternatives are impossible. For H, its u-projection is less than R's and its v-projection is greater than P's, giving the stated alternatives.

If E exits through the lower u-face, U≥-ec+ks. The actual bottom wall gives

\[
-s(U+a)+cV\ge-1.
\]

Since x_+=c(U+a)+s(V+a), elimination of V yields

\[
x_+\ge-e+\frac{a-(1-k)s}{c}+as. \tag{7}
\]

If E exits through the lower v-face and F through the lower u-face, then V≥-es-kc and U≥-fc. Hence

\[
x_+\ge a(c+s)-fc^2-es^2-kcs. \tag{8}
\]

The only remaining possibility has F exiting through the lower v-face. An upper v-face exclusion of H would force

\[
a\le(b+f)s+hc=.61s+.65c<1,
\]

so H exits through its lower u-face. Thus V≥-fs and U≥bc-hs, and

\[
x_+\ge a(c+s)+bc^2-(h+f)cs. \tag{9}
\]

The three negative-sign alternatives exhaust all exclusions. They include both choices when a point lies at an exterior corner, so tangencies require no additional argument.

It remains to verify (3) in (5)–(9). On c≥s≥0,

\[
c+s\ge1+\frac45cs, \tag{10}
\]

because c+s-1=2cs/(c+s+1) and c+s≤√2<3/2. For the four bounds (5), (6), (8), (9), replace a by 1, subtract 1/2+cs, and apply (10). The resulting lower bounds are respectively

\[
\begin{array}{c|l}
(5)& .24c^2+.85s^2-.85cs\\
(6)& .37c^2+.50s^2-.70cs\\
(8)& .24c^2+.37s^2-.44cs\\
(9)& .85c^2+.50s^2-1.11cs.
\end{array}
\]

All are strictly positive. Explicit decompositions for the first three are

\[
\begin{aligned}
.24c^2+.85s^2-.85cs
&=\frac15(c-2s)^2+\frac1{40}(c-s)^2+\frac3{200}c^2+\frac1{40}s^2,\\
.37c^2+.50s^2-.70cs
&=\frac7{20}(c-s)^2+\frac1{50}c^2+\frac3{20}s^2,\\
.24c^2+.37s^2-.44cs
&=\frac{11}{50}(c-s)^2+\frac1{50}c^2+\frac3{20}s^2.
\end{aligned}
\]

For the fourth, cs≤c² gives

\[
.85c^2+.50s^2-1.11cs
=\frac12(c-s)^2+.35c^2-.11cs
\ge\frac12(c-s)^2+.24c^2>0.
\]

Finally, the expression obtained from (7) after putting a=1 and subtracting 1/2+cs, multiplied by c>0, is

\[
1-.63c-.76s+cs(1-c)
\ge1-\sqrt{(.63)^2+(.76)^2}>0,
\]

because (.63)²+(.76)²=1949/2000<1. Thus (3) holds in every case. The open-chord argument from Theorem 1 finishes the proof, including the axial case s=0. ∎

### Exact case applications

For the bottom targets, the points (1.87,.76) and (1.74,1) belong strictly to the actual southwest singleton, while (2.35,1.65) is an excluded original central marker. The theorem therefore applies directly. For the upper targets, transport the full local statement by the indicated isometry.

| Cases | Target owner(s) | Isometry from Theorem 2 | Source of the two singleton exclusions | Target line |
|---|---|---|---|---|
| C888, C889, C893 | owner 9, mask 8192 | identity | southwest owner 0, mask 1 | x=5/2 |
| C1084 | owner 9, mask 8192 | identity | southwest owner 0, mask 1 | x=5/2 |
| C1084 | owner 11, mask 32768 | (x,y)↦(x,4-y) | northwest owner 3, mask 64 | x=5/2 |
| C702 | owner 11, mask 32768 | (x,y)↦(4-x,4-y) | northeast owner 3, mask 16 | x=3/2 |
| C1072 | owner 11, mask 32768 | (x,y)↦(4-x,4-y) | northeast owner 2, mask 16 | x=3/2 |

For C702, the two northeast singleton seed points are explicitly (2.13,3.24),(2.26,3); they are the half-turn of the southwest seed pair and are listed in the recovered C702 common strict hull H₃. Its upper target owns (1.6,3),(2,3.086). For C1072 these same strict singleton points are already listed in Chapter 04. In each half-turn application the central exclusion becomes (1.65,2.35), which is outside the top wall owner's exact signature. In the reflected C1084 application it becomes (2.35,2.35), likewise outside that top wall owner's exact signature.

Therefore Theorems 1–2 replace both outer target calculations in C702, C888, C889, C893, C1072, and C1084. The two central target chords remain a separate requirement if one uses the complete four-chord contradiction; no complete case exclusion follows from just these two theorems. All six of these families are now excluded by the strict-point endings in their dedicated chapters, indexed in Section 12 below. Those proofs make their remaining central chord calculations unnecessary.

### Center conclusion and direct C974 reduction

The same hypotheses of Theorem 2 give the stronger center bound

\[
X_Q>2+\frac{23}{200}. \tag{11}
\]

Here X_Q is in the original coordinates. To check this without a new geometric argument, subtract a(c+s)/2 from the five lower bounds (5)–(9), obtaining the translated center abscissa. In the four non-wall expressions, a>1 and (10) give the following strict lower bounds:

\[
\begin{array}{c|l|l}
\text{bound}&\text{quadratic lower bound}&\text{uniform lower bound}\\
(5)& .24c^2+.85s^2-.25cs& .115c^2+.725s^2\ge.115\\
(6)& .37c^2+.50s^2-.10cs& .32c^2+.45s^2\ge.32\\
(8)& .24c^2+.37s^2+.16cs& .24\\
(9)& .85c^2+.50s^2-.51cs& .595c^2+.245s^2\ge.245.
\end{array}
\]

The bounds in the last column use 2cs≤c²+s²=1 and nonnegativity of c,s. For (7), multiplication of the center lower bound at a=1 by c gives

\[
\frac12+\frac12s^2+\frac12cs-.13c-.76s
\ge .37+s^2-.76s
=(s-.38)^2+.2256\ge.2256.
\]

Here cs≥s² and c≤1 were used. The coefficient of a before its replacement by 1 is (1+s(c+s))/(2c)>0, so the actual bound is strict. Since c≤1, division by c preserves the stated lower margin. This proves (11).

**C974 application.** Its bottom wall square Q₉ strictly owns (2,.914),(2.4,1). It excludes the southeast central marker (2.35,1.65), since that marker belongs to Q₆; it excludes (1.87,.76),(1.74,1), since both are strict in the actual singleton Q₀. Its closure lies above y=0. Thus

\[
X_9>2+\frac{23}{200}.
\]

Transposing Theorem 2 gives the left wall conclusion. Q₈ strictly owns (.914,2),(1,2.4). It excludes (1.65,2.35), which is the genuinely absent northwest marker in C974, and it excludes (.76,1.87),(1,1.74), both strict in Q₁. Its closure lies in x≥0. Therefore

\[
Y_8>2+\frac{23}{200}.
\]

These deductions use only the common C974 seed hulls and its fixed common auxiliary points. They apply to both missing-corner alternatives and to every member of the 85-element cover; no auxiliary cardinality or coverage assumption is used. They remove the entire center-sign analysis for the two comparisons Y₈≥2 and X₉≥2 in Chapter 04 §3.4. The right and top center comparisons, and the contradiction in the remaining center region, are not consequences asserted here.

**Merged-right application.** In each of the four residual common patterns, L and R have chords longer than one on y=5/2. For L use the same transposition, with its central exclusion (1.65,2.35) supplied by N and its two singleton exclusions supplied by V. For R reflect this entire transposed configuration in x=2: its anchors are (3.086,2),(3,2.4), its central exclusion (2.35,2.35) comes from W, and its singleton exclusions (3.24,1.87),(3,1.74) come from I. Both also have center ordinates strictly greater than 2+23/200.

Thus a horizontal line-capacity contradiction for these common patterns needs only a sufficient combined chord bound for N and W on y=5/2. The assertion that both remaining chords are long is not added as a hypothesis or claimed as proved.

## 3. A stronger two-chord obstruction

**Theorem 3.** Let Q be an open square of side a>1. Suppose

\[
\frac12\le r\le 2\sqrt2-2,
\qquad 0<h_0<1,\quad0<h_1<1.
\]

It is impossible that Q strictly owns (0,h₀),(r,h₁), excludes (0,0),(r,0), and excludes the entire segment [0,r]×{1}.

The simpler rational upper bound r≤4/5 is sufficient. In particular, the heights h₀,h₁ need not be at most r. The lower two excluded points may have different physical owners; only the upper segment must have a valid whole-segment exclusion.

### Proof

Write X for the center abscissa, and choose absolute canonical components c≥s≥0, c²+s²=1. Set

\[
H=\frac a2(c+s).
\]

Each of the two vertical chords, at x=0 and x=r, is nonempty. Its owned anchor has ordinate strictly between zero and one, while both endpoints (x,0),(x,1) are outside Q. Therefore each entire open chord lies in 0<y<1 and has length at most one.

If s=0, any nonempty vertical chord has length a>1, an immediate contradiction. Hence s>0. By the exact chord formula and a/c>1, a chord of length at most one must satisfy

\[
H-|x-X|\le cs. \tag{12}
\]

The center lies strictly between the two lines. Indeed, if X≤0, (12) at x=0 gives X+H≤cs≤1/2≤r. This contradicts the strict owned point at x=r, whose abscissa is less than the rightmost support X+H. If X≥r, (12) at x=r gives X-H≥r-cs≥0, contradicting the strict owned point at x=0.

Moreover, a chord of length at most one lies strictly outside the plateau |x-X|≤a(c-s)/2, because every chord on that plateau has length a/c>1. Consequently

\[
X>\frac a2(c-s),\qquad r-X>\frac a2(c-s). \tag{13}
\]

The top and bottom vertices of Q have abscissas X±a(c-s)/2, in one order or the other according to the signed angle. Thus (13) places both abscissas strictly in (0,r).

Let y₊ be the ordinate of the top vertex. The line segment joining the two strict owned anchors is strict in Q and has ordinate between zero and one at every abscissa in [0,r]. At the top vertex's abscissa there is therefore a strict owned point below y=1. If y₊>1, the segment from that strict point to the closed top vertex crosses y=1 at a strict point of Q with abscissa in (0,r). This contradicts the excluded upper segment. Hence

\[
y_+\le1. \tag{14}
\]

A reflection in x=r/2 interchanges the two hypotheses and their anchors, preserves all exclusions, and changes the signed angle. We may therefore use the positive frame u=(c,s), v=(-s,c), with lower faces U,V. This is a symmetry of the entire local configuration, not a reflection of one square while leaving its point data fixed.

The line x=0 is to the left of the plateau. Its lower endpoint is y=U/s. Because its chord lies above y=0, U≥0. The line x=r is to the right of the plateau. Its lower endpoint is y=(V+sr)/c, so V≥-sr. Therefore

\[
y_+=s(U+a)+c(V+a)\ge a(c+s)-r cs.
\]

But

\[
c+s-1=\frac{2cs}{c+s+1}
\ge(2\sqrt2-2)cs\ge r cs.
\]

It follows that

\[
y_+\ge a(c+s)-r cs>c+s-r cs\ge1,
\]

contradicting (14). Strictness comes from a>1 and c+s>0. Every limiting angle, the critical value r=2√2-2, and all boundary contacts of the excluded points and segment have been included. ∎

### Relation to the retained lower-points/upper-segment lemma

The earlier theorem assumes strict points (x,h),(r,k), with x≤p<r, 1/2≤r-p≤4/5, 0<h,k<1, together with the two lower exclusions and the upper segment over [p,r]. Interpolate the strict owned segment at x=p. Its height lies strictly between zero and one. Translate p to zero and apply Theorem 3.

Thus all its height-versus-horizontal-span conditions can be removed: neither h≤r-x nor k≤r-p is needed, and neither height needs a lower bound of 1/2. This is an actual strengthening, with a complete continuous proof, and preserves all earlier C715 and shared-pattern applications.

## 4. Complete exclusion of merged-right pattern 3

**Corollary 4.** None of the three original marker families C48, C573, C574 can realize shared pattern 3, in which A owns F₅=(2,2.26).

### Proof from the actual owners

Use only the following strict points from Chapter 04:

- W owns (2.35,1.65),(2.35,2.35).
- A owns (2,1.5) and, in pattern 3, (2,2.26).
- I owns (3,1.6),(3,1.74).
- R owns (3,2.26).

The strict W segment supplies (2.35,2.26). The strict I segment supplies (3,1.65). The strict A segment contains every point (2,y) with 1.65≤y≤2.26. Since A,I,R are actual squares distinct from W, those A/I/R points are outside W. This is a valid same-owner source for the entire segment; no segment has been inferred from two unrelated excluded points.

Apply the isometry and translation

\[
(x,y)\longmapsto(y-1.65,\ 3-x).
\]

Then W has the two strict anchors

\[
(0,.65),\qquad(.61,.65).
\]

Its two lower excluded points are (0,0),(.61,0), supplied by I and R respectively. Its whole upper excluded segment is [0,.61]×{1}, supplied by A. Theorem 3 applies with r=61/100 and h₀=h₁=13/20, because 1/2≤61/100≤4/5.

This contradiction uses no point or exclusion of the varying bottom owner B. It therefore excludes pattern 3 uniformly in all three original families. It also uses no angle bound, wall-center bound, subdivision, or numerical enclosure. ∎

### What this removes

The recovered finite treatment of merged-right pattern 3 listed 59 directed pair/chord domain updates and 32 continuous orientation cells per owner. Corollary 4 replaces that complete ending with the displayed four actual-owner point rows and Theorem 3. Its two requirements that are not original markers—the A crosspoint (2,1.5) and I's strict segment at x=3—are already explicit established strict points in the supplied Chapter 04 entrance.

The four residual patterns of that chapter have therefore been reduced to patterns 1, 4, and 5. Their complete exclusions are not asserted by Corollary 4.

## 5. A corner reach theorem with two foreign points

**Theorem 5.** Let Q be an open square of side a>1 whose closure lies in y≤1. Suppose Q strictly owns O=(0,0), and excludes F=(−q,0) and H=(0,−p), where p,q>0. If r≥0 satisfies

\[
p^2+q^2\le1,\qquad p^2+r^2\le1,\qquad q+r\le2\sqrt2-2,
\]

then Q strictly owns P=(r,0). The wall is the actual coordinate wall y≤1; no bound on the other three supports is required.

### Proof

The case r=0 is immediate. Suppose r>0. Choose c≥s≥0, c²+s²=1 and set K=c+s. We repeatedly use

\[
K-(q+r)cs\ge1, \tag{15}
\]

because K−1=2cs/(K+1) and K≤√2. We also have q+r<1. All point exclusions below permit equality.

First take u=(c,s), v=(−s,c). Write U,V for the lower band values. The strict point O gives U,V<0<U+a,V+a. The target P therefore already satisfies its lower u-band and upper v-band. The excluded F can leave only through the lower u-face or upper v-face.

If U≥−qc, then

\[
U+a\ge a-qc>rc.
\]

The upper wall gives s(U+a)+c(V+a)≤1, so

\[
cV\le1-aK-sU\le1-aK+qcs<-rcs
\]

by (15) and a>1. Thus V<−rs, proving P's two remaining strict bands.

If V+a≤qs instead, then

\[
V\le qs-a<-rs.
\]

Both coordinates of H in this frame are nonpositive, so H can leave only through a lower face. A lower v-face exclusion would give

\[
a\le qs+pc\le\sqrt{q^2+p^2}\le1,
\]

which is impossible. Hence U≥−ps, and

\[
U+a\ge a-ps>rc,
\]

since ps+rc≤√(p²+r²)≤1. This completes the positive sign.

For the other sign take u=(c,−s), v=(s,c). The point P already satisfies both lower bands. The excluded F can leave only through a lower face, while H can leave only through the upper u-face or lower v-face.

If U≥−qc, then U+a>rc. An upper u-face exclusion of H would imply

\[
a\le qc+ps\le\sqrt{q^2+p^2}\le1.
\]

Thus H leaves through the lower v-face, V≥−pc, and

\[
V+a\ge a-pc>rs.
\]

If V≥−qs instead, then V+a>rs. For s=0 this alternative is incompatible with the strict O, because it would say V≥0. Thus s>0 in this branch. The actual upper wall now reads −sU+c(V+a)≤1. Consequently

\[
s(U+a)\ge aK+cV-1\ge aK-qcs-1>rcs
\]

by (15), and U+a>rc follows. These are both remaining strict bands of P.

The four alternatives include c=s and every possible tangency. The zero-sine branch was treated explicitly. All strict target inequalities come from a>1, so equality in any parameter bound is allowed. ∎

### Exact corner enlargements in the merged-right families

The wall advance theorem in `C981-WALL-CYCLES.md`, Theorem 4, gives the strict points (1,2.8) in L and (3,2.8) in R from the actual singleton hulls V,I and central markers N,W. This application is uniform in the residual patterns 1,3,4,5. The established top-wall point (2.56,3) is strict in T in all four residual patterns.

The following three applications of Theorem 5 use actual foreign owners throughout:

| Target owner | Transport to Theorem 5 | Foreign F; owner | Foreign H; owner | (p,q,r) | New strict point |
|---|---|---|---|---|---|
| E | (x,y)↦(x−3,y−3) | (2.56,3); T | (3,2.8); R | (1/5,11/25,19/50) | (3.38,3) |
| E | (x,y)↦(y−3,x−3) | (3,2.8); R | (2.56,3); T | (11/25,1/5,3/5) | (3,3.6) |
| K | (x,y)↦(y−3,1−x) | (1,2.8); L | (1.74,3); N | (37/50,1/5,3/5) | (1,3.6) |

The strict origins (3,3) in E and (1,3) in K are the established paired-corner points. The corresponding upper walls are respectively y≤4, x≤4, and x≥0, all genuine container walls transported together with the squares and points.

The first row has q+r=41/50, and the last two have q+r=4/5. Both are at most 2√2−2; for 41/50 this follows from (141/100)²<2. The largest value of p²+r² among the three rows is 2269/2500<1, and p²+q²≤1469/2500<1. Thus every parameter condition has been checked exactly.

Each new point can be joined to every other strict point of its same corner square. In particular, the full segment [3,3.38]×{3} is a genuine excluded segment for R and W. This conclusion requires no auxiliary ownership convention for the omitted paired corners E,K.

## 6. Two short chords force a large strict hull

**Theorem 6.** Let Q be an open square of side a>1. Suppose Q strictly owns

\[
(.35,-.35),\qquad(.35,.35),
\]

and excludes the four points

\[
(0,-.26),\ (0,.26),\ (1,-.26),\ (1,.26). \tag{16}
\]

The square cannot be axis parallel. In a canonical positive frame u=(c,s), v=(−s,c), c≥s>0, it strictly owns

\[
D_0=(1.02,0),\qquad D_1=(1.02,.02),\qquad D_2=(.96,.11). \tag{17}
\]

Furthermore, if the entire segment joining (1.086,0) to (1,.26) is excluded from Q, then a canonical negative frame is impossible. Consequently, under this additional segment hypothesis, all three points in (17) are strictly owned without any orientation assumption.

### Two chords and their four endpoint inequalities

Write k=13/50=.26 and h=7/20=.35. Both horizontal lines y=±k pass through strict points of Q's owned vertical segment. Their open chords contain x=.35 and exclude x=0,1. Thus both chords lie in (0,1) and have length at most one. Axis alignment would give chord length a>1, so it is impossible.

Let Y be the center ordinate, H=a(c+s)/2 the vertical support radius, with c≥s>0. We first show

\[
-k<Y<k. \tag{18}
\]

If Y≤−k, the short chord on y=−k is at or above the center. The exact square-chord formula gives Y+H+k≤cs. Therefore the upper support is at most cs−k≤1/2−k=.24, contradicting the strict owned point at height h=.35. The case Y≥k follows by vertical reflection, using the lower owned point. This proves (18), including either possible center equality.

The plateau of the horizontal chord function has length a/c>1. Hence each of these two short chords is strictly outside that plateau. In the positive frame, the lower chord is the one adjacent to the closed bottom vertex, and the upper chord is adjacent to the closed top vertex. Writing U,V for lower band values, their endpoints are respectively

\[
\left(\frac{U+ks}{c},\frac{-kc-V}{s}\right),
\qquad
\left(\frac{kc-V-a}{s},\frac{U+a-ks}{c}\right),
\]

where each pair lists left and right abscissas. Their containment in (0,1), with endpoint tangency permitted, gives

\[
U\ge-ks,\qquad V\ge-kc-s,\qquad
V+a\le kc,\qquad U+a\le c+ks. \tag{19}
\]

In particular,

\[
1<a\le s+2kc=s+\frac{13}{25}c. \tag{20}
\]

The same scalar bound holds in the negative frame, by reflecting y together with all four exclusions and both owned points.

### Three positive-sign completions

Put t=tan(θ/2), where c=cosθ, s=sinθ and 0<θ≤π/4. Inequality (20) is equivalent to

\[
19t^2-25t+6<0.
\]

Its roots are 6/19 and 1, so t>6/19. Thus θ is larger than the angle θ₀ with

\[
\cos\theta_0=\frac{325}{397},\qquad
\sin\theta_0=\frac{228}{397}. \tag{21}
\]

For A,B≥0 with B/A≤228/325, the quantity Ac+Bs decreases for θ≥θ₀ up to π/4. One may see this directly by writing θ=θ₀+φ: its sine coefficient becomes B cosθ₀−A sinθ₀≤0, and its cosine coefficient is nonnegative. Hence

\[
Ac+Bs\le\frac{325A+228B}{397}. \tag{22}
\]

For a target D=(x,y) in (17), inequality (19) gives U+a≥a−ks. Its strict upper u-band follows from

\[
xc+(y+k)s<1<a.
\]

Here (22) gives the following exact upper bounds:

| Target | (A,B)=(x,y+k) | Bound from (22) |
|---|---|---|
| D₀ | (51/50,13/50) | 19539/19850<1 |
| D₁ | (51/50,7/25) | 19767/19850<1 |
| D₂ | (24/25,37/100) | 39636/39700<1 |

All three coefficient ratios satisfy the stated condition in (22).

The strict lower v-band follows from V≤kc−a and

\[
xs+(k-y)c<1<a.
\]

Indeed x≥k−y≥0, so the left side is at most (x+k−y)/√2. The three numerators x+k−y are 32/25,63/50,111/100, each strictly less than √2.

The other two strict bands follow directly from the owned upper anchor (.35,.35): for every target,

\[
xc+ys>.35(c+s),
\qquad
-xs+yc<.35(c-s).
\]

For the first comparison, (x−.35)c+(y−.35)s is positive because c≥s and x+y>.70; for the second, (.35−y)c+(x−.35)s is positive. Therefore all three targets are strict, as asserted.

### The right-hand segment excludes the negative sign

Suppose the square has a negative canonical frame, and reflect y. The reflected square has the positive frame just used, the same owned bar and four exclusions, and excludes the entire segment with endpoints

\[
B_0=(1+e,0),\qquad B_1=(1,-k),
\quad e=43/500=.086.
\]

We retain (19)–(20). At B₀ the lower u- and upper v-bands are strict by comparison with the owned bar. A lower v-face exclusion would yield

\[
a\le kc+(1+e)s\le\frac{k+1+e}{\sqrt2}<1,
\]

where the middle inequality follows because (1+e)>k and 0≤θ≤π/4, and k+1+e=673/500<√2. Consequently B₀ exits through the upper u-face, and its v-band is strict.

At B₁ the u-band is strict. Its lower u-band follows from

\[
c-ks>.35(c+s),
\]

because .65c−.61s>0. Its upper u-band follows from U+a≥a−ks>c−ks. Its exclusion is therefore through the lower v-face, as is also explicit in (19).

Both u- and v-projections decrease along B₀B₁. Since B₀ has a strict v-band and B₁ has a strict u-band, avoiding the entire segment forces the upper-u entry parameter to be at least the lower-v exit parameter. Cross multiplication gives precisely

\[
(kc-es)(U+a)-(ks+ec)V\le k(1+e). \tag{23}
\]

For completeness, the projection decrements from B₀ to B₁ are ec+ks>0 and kc−es>0. The entry and exit parameters are

\[
\frac{u(B_0)-(U+a)}{ec+ks},\qquad
\frac{v(B_0)-V}{kc-es}.
\]

If the first were smaller, every parameter strictly between them would satisfy both strict bands. Their equality is allowed in (23), so a segment touching only a corner has not been omitted.

The bounds U+a≥a−ks and V≤kc−a imply that the left side of (23) is at least

\[
a\big((k+e)c+(k-e)s\big)-2k^2cs-ke(c^2-s^2).
\]

As a>1 and both coefficients are positive, this is strictly greater than

\[
k\big(c+s-2kcs\big)+e(c-s)\big(1-k(c+s)\big)
\ge k\big(c+s-2kcs\big),
\]

because c≥s and k(c+s)<1. The elementary bound c+s≥1+(4/5)cs then makes this at least

\[
k\left(1+\frac7{25}cs\right).
\]

Finally, (20) gives s>12/25, while c≥1/√2>7/10. Hence

\[
\frac7{25}cs>\frac{294}{3125}>\frac{43}{500}=e.
\]

The left side of (23) is therefore strictly greater than k(1+e), a contradiction. This excludes the negative sign. The argument includes 45°, which can in fact be represented in either canonical sign, and the axis case was already excluded by the chord lengths. ∎

## 7. A right-wall square cannot avoid the forced hull and corner point

**Theorem 7.** No open square R of side a>1 with closure in x≤1 can strictly own

\[
P=(.086,0),\qquad B=(0,.26),\qquad C=(0,.8)
\]

while excluding all four points

\[
D_0=(.02,0),\quad D_1=(.02,.02),\quad
D_2=(-.04,.11),\quad E=(.38,1). \tag{24}
\]

No other wall, common-side premise, or upper bound on a is needed.

### Positive canonical sign

Write u=(c,s), v=(−s,c), c≥s≥0. Put d=.02 and b=.38. The excluded D₀ has three strict bands by comparison with P and C: its upper u-band follows from P, its lower v-band from P, and its upper v-band from C. Hence

\[
U\ge dc. \tag{25}
\]

The two lower bands of E are strict by comparison with P, so E leaves through an upper face. If U+a≤bc+s, then (25) gives

\[
a\le(b-d)c+s\le\frac{1+b-d}{\sqrt2}<1,
\]

because b−d=9/25<1 and (34/25)²<2. Thus E must leave through its upper v-face:

\[
V+a\le c-bs. \tag{26}
\]

The actual right wall now gives

\[
1\ge c(U+a)-sV\ge a(c+s)+dc^2-cs+bs^2.
\]

We show that the final expression is greater than one for every angle. Since a>1, it suffices to prove

\[
\Phi=c+s-1-cs+\frac1{50}c^2+\frac{19}{50}s^2>0.
\]

Set t=tan(θ/2)∈[0,√2−1]. An exact substitution yields

\[
50(1+t^2)^2\Phi=1-26t^2+200t^3-99t^4.
\]

The polynomial has the following positive decomposition:

\[
\begin{aligned}
1-26t^2+200t^3-99t^4
={}&(1-4t)^2\\
&+2t\left(75\left(t-\frac7{50}\right)^2+\frac{253}{100}\right)\\
&+t^3(50-99t).
\end{aligned}
\]

For 0≤t≤√2−1<1/2, all terms are nonnegative. At t=0 the first is one; at t>0 the middle term is positive and 50−99t>0. Thus Φ>0, contradicting the wall. This includes the zero-angle endpoint.

### Negative canonical sign

Now write u=(c,−s), v=(s,c), c≥s≥0, and put τ=s/c∈[0,1]. Comparisons of D₀ with P and C show that both its u-bands and its upper v-band are strict. Its exclusion therefore forces

\[
V\ge ds. \tag{27}
\]

We first prove τ<5/6. If τ≥5/6, then E's u-projection lies strictly between those of C and B:

\[
u(E)-u(C)=.38c-.2s>0,
\]

\[
u(E)-u(B)=.38c-.74s<0.
\]

Its lower v-band is strict by P. Thus E must leave through the upper v-face, and (27) implies

\[
a\le c+(b-d)s=c+\frac9{25}s.
\]

The function (1+(9/25)τ)/√(1+τ²) is decreasing for τ≥5/6, so

\[
a\le\frac{39}{5\sqrt{61}}<1,
\]

where the last comparison is exactly 1521<1525. This contradiction proves τ<5/6.

If 0≤τ≤1/4, the point D₁ satisfies both strict u-bands by comparison with P and C. Its v-projection also lies strictly between theirs, because

\[
v(D_1)-v(P)=c(.02-.066\tau)>0,
\qquad
v(D_1)\le.04c<.8c=v(C).
\]

It is therefore strictly inside R, contradicting its exclusion.

If 1/4≤τ<5/6, use D₂ instead. Its u-projection lies strictly between those of C and P, since

\[
u(D_2)-u(C)=c(-.04+.69\tau)>0,
\qquad u(D_2)<0<u(P).
\]

Its v-projection is likewise strictly between theirs:

\[
v(D_2)-v(P)=c(.11-.126\tau)>0,
\qquad v(D_2)<.11c<.8c=v(C).
\]

Thus D₂ is strictly inside R, again a contradiction. These two intervals cover all τ<5/6 and overlap at the harmless equality τ=1/4. Both signs and every boundary angle have been covered. ∎

## 8. Complete exclusions of merged-right patterns 1 and 5

**Corollary 8.** Patterns 1 and 5 of Chapter 04, Section 1.2, are impossible in each of C48,C573,C574.

### Exact ownership deduction

In either pattern, W owns the two vertical markers (2.35,1.65),(2.35,2.35). It excludes

\[
(2,1.74),\ (2,2.26),\ (3,1.74),\ (3,2.26).
\]

The first is strict in A, the third in I, and the fourth in R. The second is F₅: in pattern 1 it is absent from W's exact auxiliary subset, and in pattern 5 it is strict in N. In particular, pattern 1 does not require inventing a foreign owner for a globally unowned auxiliary.

The actual R owns both (3.086,2) and (3,2.26). It therefore owns the entire segment joining them, which W excludes. Apply Theorem 6 after translating by (−2,−2). It follows that W strictly owns

\[
(3.02,2),\qquad(3.02,2.02),\qquad(2.96,2.11). \tag{28}
\]

The wall advance in `C981-WALL-CYCLES.md`, Theorem 4, supplies the strict R point (3,2.8). Theorem 5 above, using the actual T point (2.56,3), then supplies the strict E point (3.38,3). The deductions use I's singleton hull and W's original upper marker exactly as in Section 5; they do not depend on the varying owner B.

Now translate the actual square R by (−3,−2). Its strict points (3.086,2),(3,2.26),(3,2.8) become P,B,C in Theorem 7, and the genuine container wall x≤4 becomes x≤1. The three points in (28), owned by the different actual W, become D₀,D₁,D₂. The strict corner point (3.38,3), owned by the different actual E, becomes the excluded E in (24). Every hypothesis of Theorem 7 is therefore satisfied, giving a contradiction.

This proof applies unchanged to C48,C573,C574 and uses only their genuine common points and exclusions. It has no finite orientation subdivision, local-domain propagation, side upper bound, or unproved center condition. ∎

### Updated merged-right scope

Corollary 4 completely excludes pattern 3. Corollary 8 completely excludes patterns 1 and 5. Together with the three pre-existing short exclusions of patterns 2,6,7, six of the original seven common patterns now have continuous geometric exclusions. At this stage only pattern 4, where W owns F₅, remains outside these particular arguments (the later Sections 9–11 and companion proof complete it): its ownership removes one of the four exclusions in (16), so Theorem 6 must not be applied there.

## 9. A wall point completion supplied by a perpendicular foreign segment

**Theorem 9.** Let Q be an open square of side a>1 whose closure lies in y≤1. Suppose it strictly owns

\[
P=(0,e),\qquad S=(r,0),\qquad 0<e<1,\quad0<r<1,
\]

and excludes the whole segment

\[
\{1\}\times[0,q],\qquad\frac12\le q<1.
\]

Then Q strictly owns O=(0,0). There is no upper bound on a.

### Proof

Assume O is excluded. In an axis-parallel square, strict ownership of P and S immediately makes O strict, a contradiction. We may therefore choose one of the two canonical signs with c≥s>0 and c²+s²=1. Put K=c+s. We shall force the closed rightmost vertex Z to satisfy

\[
Z_x>1,\qquad0<Z_y<q. \tag{29}
\]

The segment joining the strict point S=(r,0) to Z then meets x=1 at a height strictly between 0 and q. Since r<1<Zₓ, the intersection occurs before Z, and is strictly inside Q. This contradicts the excluded segment.

**Positive sign:** u=(c,s), v=(−s,c). Comparing O with P and S makes its two upper bands and lower v-band strict. Hence U≥0. At B₀=(1,0), its lower u-band and upper v-band are strict by S and P. Its upper u-band is strict because U+a≥a>1≥c. Its exclusion consequently gives V≥−s.

The actual upper wall is

\[
s(U+a)+c(V+a)\le1.
\]

For the rightmost vertex Z=(c(U+a)−sV, s(U+a)+cV), elimination of V gives

\[
Z_x\ge\frac{U+a-s}{c}+as
>\frac{1-s}{c}+s\ge1.
\]

The final inequality is (1−s)(1/c−1)≥0. Also

\[
Z_y\ge s(U+a-c)\ge s(a-c)>0,
\]

and the actual wall gives

\[
Z_y\le1-ac<1-c\le1-\frac1{\sqrt2}<\frac12\le q.
\]

Thus (29) holds in this sign.

**Negative sign:** u=(c,−s), v=(s,c). Comparing O with P and S makes both its u-bands and its upper v-band strict. Hence V≥0. The point B₀=(1,0) has a strict lower u-band by S, a strict lower v-band by S because r<1, and a strict upper v-band because V+a≥a>1≥s. Its exclusion gives U+a≤c.

The actual upper wall is now

\[
-sU+c(V+a)\le1. \tag{30}
\]

For the rightmost vertex Z=(c(U+a)+s(V+a), −s(U+a)+c(V+a)), this yields

\[
Z_x\ge\frac{V+a-c}{s}+ac
>\frac{1-c}{s}+c\ge1,
\]

where the last inequality is (1−c)(1/s−1)≥0. Moreover,

\[
Z_y\ge c(a-s)>0.
\]

To bound Zᵧ from above, consider B₁=(1,q). Its lower u-band is strict by P, since c−(q−e)s=c−qs+es≥(1−q)c+es>0. Its lower v-band is strict by S. Its upper u-band is also strict: (30) and V≥0 imply

\[
\begin{aligned}
s\big((U+a)-(c-qs)\big)
&\ge aK-1-cs+qs^2\\
&>K-1-cs+qs^2\ge0.
\end{aligned}
\]

The last inequality follows from

\[
K-1-cs=-\frac{2c^2s^2}{(K+1)^2}\ge-\frac12s^2,
\]

using K+1≥2c and q≥1/2. Therefore B₁'s exclusion forces V+a≤s+qc. Because V≥0 and a>1, this gives s+qc>1. Finally, Z lies a s below the upper vertex, so (30) gives

\[
Z_y\le1-as<1-s<qc\le q.
\]

Thus (29) holds in this sign as well. All possible tangencies were retained as weak face inequalities; the contradiction is strict because a>1 and the interpolation ends before the closed vertex. ∎

### Exact merged-right top-wall application

The paired corner E strictly owns both (3,3) and (3,3.6), the latter by Theorem 5. Hence it strictly owns the whole vertical segment {3}×[3,3.6]. The different actual T excludes that segment.

Translate the actual T by (−2,−3). Its strict marker (2,3.086) and auxiliary point (2.26,3) become P=(0,.086) and S=(.26,0). Its real top container wall becomes y≤1. The corner segment becomes {1}×[0,.6]. Theorem 9 with e=43/500,r=13/50,q=3/5 therefore proves

\[
(2,3)\in T\quad\text{strictly}. \tag{31}
\]

This conclusion holds in all four residual merged-right patterns, including the remaining pattern 4. Consequently every other actual owner excludes the full strict T segment [2,2.56]×{3}, not merely its originally listed subsegment [2.26,2.56]×{3}.

## 10. A foreign whole segment gives an exact angle interval and a strict region

**Theorem 10 (outward angle interval and strict point region).** Let D be an open square of side a>1 with a nonnegative canonical frame

\[
u=(c,s),\qquad v=(-s,c),\qquad c\ge s\ge0,\qquad c^2+s^2=1.
\]

Suppose D strictly owns

\[
N=(.35,.35),\qquad A=(1,.26),
\]

and excludes the three points

\[
G=(.26,0),\qquad R_0=(1,0),\qquad P=(1,1),
\]

and the whole segment

\[
S=[.26,.8]\times\{1\}.
\]

Write D as U<u·X<U+a, V<v·X<V+a. Then s>0, and

\[
\begin{gathered}
U\ge.26c,\qquad V\ge-s,\qquad
U+a\le c+s,\qquad V+a\le c-.8s, \\
\frac{13}{87}<t:=\frac{s}{1+c}<\frac15. \tag{32}
\end{gathered}
\]

Moreover, D strictly owns every point (α,−β) satisfying

\[
\frac7{20}\le\alpha\le\frac12,\qquad
0\le\beta\le\frac15,\qquad
12\alpha-5\beta>4,\qquad
5655\alpha+18500\beta<5369. \tag{33}
\]

No container hypothesis or upper bound on a is required. In particular, all statements remain valid when any of the excluded points or segment endpoints is tangent to a square face.

**Proof.** The upper bands of G are strict by the owned point N, because the projection differences are .09c+.35s>0 and .35c−.09s>0. Thus G leaves through a lower face. Suppose first that V≥−.26s. Let F=(.26,1) and T=(.8,1), the endpoints of S.

At F the upper u-band is strict by A, since u(A)−u(F)=.74(c−s)≥0, and the lower v-band is strict by N. If F left through its upper v-face, then a≤c≤1. Therefore its exclusion would force U≥.26c+s. At T both lower bands are strict by N: the increments are .45c+.65s>0 and .65c−.45s>0. Its upper v-face alternative would give a≤c−.54s≤1. Thus it would leave through the upper u-face, and a≤.54c<1. This contradiction proves

\[
U\ge.26c. \tag{34}
\]

At R₀ the lower u-band is strict by N, since .65c−.35s>0, and the upper v-band is strict by A, since v(A)−v(R₀)=.26c>0. Its upper u-face alternative, together with (34), would give a≤.74c<1. Consequently

\[
V\ge-s. \tag{35}
\]

At P both lower bands are strict by N: the increments are .65(c+s)>0 and .65(c−s)≥0. Its upper v-face alternative, together with (35), gives a≤c≤1. Therefore

\[
U+a\le c+s. \tag{36}
\]

The bounds (34) and (36) exclude s=0. They also give

\[
1<a\le .74c+s. \tag{37}
\]

At F the upper u-band and lower v-band are strict, as already shown. Its lower u-face alternative, combined with (36), gives a≤.74c<1. Hence

\[
V+a\le c-.26s. \tag{38}
\]

We next use the whole segment S, not only its endpoints. Suppose c+.2s≤1. At T both lower bands are strict. An upper v-face exclusion would give a≤c+.2s≤1 by (35), so it must instead satisfy

\[
U+a\le .8c+s. \tag{39}
\]

Consider the closed upper vertex

\[
Z=\big(c(U+a)-s(V+a),\ s(U+a)+c(V+a)\big).
\]

By (34) and (38),

\[
Z_x\ge .26+c(a-s)>.26.
\]

By (35) and (39),

\[
Z_x\le .8+s(c+.2s-a)<.8.
\]

On the other hand, (34) and (35) imply

\[
Z_y\ge a(c+s)-.74cs>c+s-.74cs>1.
\]

Here s>0, and c+s−1≥(4/5)cs, the elementary inequality used earlier in this file. The strict point N has .26<Nₓ<.8 and Nᵧ<1. Its segment to Z therefore crosses S before reaching Z. Every such intermediate point joining a strict point of a convex square to a point of its closure is strict. This contradicts exclusion of S. We have proved

\[
c+.2s>1. \tag{40}
\]

The half-angle identity

\[
c+.2s-1=\frac{2t(.2-t)}{1+t^2}
\]

and s>0 give t<1/5. In particular s<5/13<2/5. Thus T cannot satisfy (39), since (34) would give a≤.54c+s<.54+.4<1. It follows that T leaves through the upper v-face, giving the fourth bound in (32).

Finally, (37) and

\[
.74c+s-1=\frac{(1-t)(87t-13)}{50(1+t^2)}
\]

give t>13/87, because t<1/5<1. This completes (32).

For (33), let X=(α,−β). Its upper u-band is strict by A, and its upper v-band is strict by N:

\[
\begin{aligned}
u(A)-u(X)&=(1-\alpha)c+(.26+\beta)s>0,\\
v(N)-v(X)&=(.35+\beta)c+(\alpha-.35)s>0.
\end{aligned}
\]

The lower u-band follows from (36). Indeed, the expression (1−α)c+(1+β)s increases with the angle throughout 0≤θ≤π/4: its derivative is at least (α+β)c>0. At t=1/5, the exact cosine and sine are 12/13 and 5/13. Hence

\[
\begin{aligned}
u(P)-u(X)
&=(1-\alpha)c+(1+\beta)s\\
&<\frac{17-12\alpha+5\beta}{13}<1<a.
\end{aligned}
\]

Since U+a≤u(P), this gives U<u(X).

Similarly, (1+β)c−(.8−α)s decreases strictly with the angle, because .8−α≥.3>0. At t=13/87 the exact cosine and sine are 3700/3869 and 1131/3869. Thus

\[
\begin{aligned}
v(T)-v(X)
&=(1+\beta)c-(.8-\alpha)s\\
&<\frac{13976+5655\alpha+18500\beta}{19345}<1<a,
\end{aligned}
\]

where the last inequality is exactly the last condition in (33). Since V+a≤v(T), this proves the strict lower v-band. All four bands are strict, so X∈D. ∎

### Exact application to the remaining merged-right pattern 4

The actual N has strictly positive canonical angle. This follows from Theorem 6 of `C981-WALL-CYCLES.md`, under the transpose (x,y)↦(y,x): its strict anchors are N's marker (1.65,2.35) and auxiliary point (1.6,3); the three exclusions are the actual K point (1,3), the actual T marker (2,3.086), and the actual W point (2,2.26). The whole foreign segment is L's strict {1}×[2.26,2.8]. The transpose reverses the sign, so the theorem's strictly negative conclusion becomes the strictly positive canonical angle of N. This excludes both the axial and ambiguous 45-degree representatives.

Apply Theorem 10 to N in the rotated and translated coordinates

\[
(\xi,\eta)=(y-2,2-x).
\]

The square's canonical angle is unchanged by this rotation through a right angle. Every hypothesis has an actual strict owner:

| Theorem datum | Original point or segment | Actual owner |
|---|---|---|
| N=(.35,.35) | (1.65,2.35) | N |
| A=(1,.26) | (1.74,3) | N |
| G=(.26,0) | (2,2.26) | W, in pattern 4 |
| R₀=(1,0) | (2,3) | T, by Theorem 9 |
| P=(1,1) | (1,3) | K |
| S=[.26,.8]×{1} | {1}×[2.26,2.8] | L |

Consequently, N strictly owns every original point (2+β,2+α) with parameters (33). Useful exact examples are

\[
(2.1,2.4),\qquad(2.16,2.41),\qquad(2.16,2.42),\qquad
\left(\frac{13}{6},\frac{721}{300}\right).
\]

For the last point, α=121/300 and β=1/6, and the two strict margins in (33) are respectively 1/150 and 289/60. These are additional compulsory strict points in N; this theorem by itself does not claim the complete exclusion of pattern 4.

### Complete conclusion for merged-right pattern 4

The sharp N point above closes the remaining pattern. The complete two-square argument is in `MERGED-RIGHT-PATTERN-4.md`: its Theorem A forces A to own (1.95,1.95) from its three southwest anchors and the genuine O/V segment points; its Theorem B forces W to own the same point from the sharp N point, W's two markers and F₅, and the actual A/I/R exclusions. Both proofs cover all orientations and every allowed tangency. Thus pattern 4 is excluded as well. Combined with Corollaries 4 and 8 here and the retained original short exclusions, every one of the seven merged-right alternatives is now completely excluded.

## 11. A short bar obstruction gives the primary merged-right dichotomy

**Theorem 11 (two-short-chord near-center completion).** Let Q be an open square of side a>1, strictly owning (.35,−.35) and (.35,.35). Suppose it excludes

\[
(0,-.26),\quad(0,.26),\quad(1,-.26),\quad(1,.26),\quad(1.086,0).
\]

Then Q strictly owns both points

\[
K_-:=(-.05,-.05),\qquad K_+:=(-.05,.05). \tag{41}
\]

This theorem uses point exclusions only. It requires no container, foreign segment, neighbor orientation, or upper bound on a.

**Proof.** We include the short-chord part to make this completion independently usable. Both lines y=±k, where k=.26, meet Q's strict owned vertical segment and exclude x=0,1. Their nonempty open chords therefore lie in (0,1) and have lengths at most one. Axis alignment would give length a>1, so it is impossible.

Reflection in y=0 preserves every hypothesis and exchanges the two targets. We may consequently prove both targets for a positive canonical frame u=(c,s), v=(−s,c), c≥s>0. Write the lower band values U,V, the center ordinate Y, and the vertical support radius H=a(c+s)/2. If Y≤−k, the short upper-side chord at y=−k gives Y+H+k≤cs by the exact square-chord formula. The upper support would be at most cs−k≤.24, contrary to ownership at height .35. The reflected argument excludes Y≥k. Thus −k<Y<k.

The plateau chord has length a/c>1. Both short chords are therefore strictly outside the plateau and adjacent to the bottom and top vertices respectively. Their four endpoints, with supporting-line tangency permitted, give exactly

\[
U\ge-ks,\quad V\ge-kc-s,\quad
V+a\le kc,\quad U+a\le c+ks. \tag{42}
\]

For completeness, their left/right abscissas are

\[
\left(\frac{U+ks}{c},\frac{-kc-V}{s}\right)
\quad\text{at }y=-k,\qquad
\left(\frac{kc-V-a}{s},\frac{U+a-ks}{c}\right)
\quad\text{at }y=k.
\]

In particular 1<a≤s+(13/25)c. With t=s/(1+c), this is 19t²−25t+6<0. The roots are 6/19 and 1, so

\[
t>6/19,\qquad
\theta>\theta_0,\qquad
(\cos\theta_0,\sin\theta_0)=(325/397,228/397). \tag{43}
\]

Put B=(1.086,0). Its lower u-band is strict by the owned point (.35,−.35), and its upper v-band is strict by (.35,.35). If B left through the lower v-face, then V≥−1.086s; (42) would imply

\[
a\le .26c+1.086s\le\frac{673}{500\sqrt2}<1.
\]

The middle bound is the value at θ=π/4, since the expression increases on the canonical interval; the last inequality is 673²<2·500². Hence B leaves through the upper u-face:

\[
U+a\le1.086c. \tag{44}
\]

For either Kσ=(−.05,σ.05), σ∈{−1,1}, the upper u-band and lower v-band are strict by the owned point (.35,−.35). Indeed its u-projection is .35(c−s)≥0≥u(Kσ), and

\[
v(K_\sigma)-v(.35,-.35)=.4s+(.35+\sigma .05)c>0.
\]

For the upper v-band, use V≥−.26c−s from (42). Then

\[
v(K_\sigma)-V
\le(.26+\sigma .05)c+1.05s
\le .31c+1.05s
\le\frac{1.36}{\sqrt2}<1<a.
\]

Finally,

\[
u(B)-u(K_\sigma)
=1.136c-\sigma .05s
\le1.136c+.05s
\le\frac{1.136(325)+.05(228)}{397}
=\frac{1903}{1985}<1<a.
\]

The penultimate inequality follows from (43), since 1.136 cos θ+.05 sin θ decreases for θ≥θ₀. Together with (44), it proves the lower u-band. All four bands are strict. Reflection supplies the negative sign, with the pair of targets exchanged. All axis and diagonal endpoints and every exterior tangency have been covered. ∎

### Primary exclusion of all three merged-right families in two alternatives

Theorem A of `MERGED-RIGHT-PATTERN-4.md` applies to the actual southwest square A in every original pattern. It strictly owns (1.95,1.95); the only additional exclusions in that theorem are supplied by the actual O/V singleton segments already established in the common entrance.

If W excludes F₅=(2,2.26), translate W by (−2,−2) and apply Theorem 11. Its owned points are its two genuine central markers. Its four chord-endpoint exclusions are F₄ in A, F₅ by this alternative, F₈ in I, and F₉ in R. Its fifth exclusion is the original marker (3.086,2) in R. Thus W also strictly owns (1.95,1.95), contradicting the disjointness of A and W. This one argument covers original patterns 1,2,3,5,6,7, including the pattern with F₅ owned by T. It uses no top-wall extension or extra ownership of F₃.

The remaining alternative is W strictly owning F₅. The original exhaustive alternatives identify it as pattern 4. Its N ownership of F₃ and the legitimate top extension are retained. The complete N-region and duplicate-point proof in `MERGED-RIGHT-PATTERN-4.md` excludes this alternative as well.

This is the primary short proof for C48,C573,C574. The earlier Theorems 3,6,7 and their corollaries remain valid independent geometric results, but their longer case-specific endings are unnecessary in this two-alternative proof.

### Immediate C702 consequence

The same first alternative applies to C702. Its actual southwest owner Q₆ owns the same three anchors and has the same O=Q₀ and V=Q₁ singleton segments, so Theorem A gives (1.95,1.95)∈Q₆. Its merged-right Q₇ owns the same two vertical markers. Its foreign endpoints F₄,F₈,F₉ belong respectively to Q₆,Q₁₀,Q₄, and the original marker (3.086,2) belongs to Q₁₀. Therefore Q₇ cannot exclude F₅.

Consequently every C702 packing would have

\[
F_5=(2,2.26)\in Q_7\quad\text{strictly}.
\]

This eliminates at once the four alternatives in which F₅ belongs to no selected square, or belongs to Q₆,Q₈,Q₁₁. Only the exact Q₇ auxiliary label 65568 remains; the other variable labels lose their optional F₅ bit. C702-CONTINUOUS-REDUCTION.md supplies the genuine wall segment for that last alternative, and the two C702 point theorems complete its exclusion by forcing (1.30,1.93) into Q₆ and Q₈.

## 12. Completed continuous central endings for the common-line families

The original capacity targets led to strict-point contradictions, so the two central chord bounds need not be established separately. The following are complete family exclusions after their retained local ownership entrances.

| Original family | Actual central owners | Continuous ending | Complete chapter |
|---|---|---|---|
| C702 | Q₆,Q₈ | Both own (1.30,1.93) after the one surviving merged-square auxiliary choice | `C702-CONTINUOUS-REDUCTION.md`, `C702-DUPLICATE-POINT.md`, `C702-N-STRICT-POINT.md` |
| C1072 | Q₄,Q₇ | Four exhaustive left-side choices; two mixed spans are impossible, and the other two force a shared (1.54,1.99) or (1.54,2.01) | `C1072-CONTINUOUS-REDUCTION.md` |
| C888 | Q₅,Q₆ | Split by the right-wall lower or upper pair; mixed spans are impossible, and the other choices force a shared (2.46,1.99) or (2.46,2.01) | `C888-C889-CONTINUOUS-EXCLUSION.md` |
| C889 | Q₅,Q₆ | The upper right-wall pair gives the same complete split and a shared (2.46,2.01) | `C888-C889-CONTINUOUS-EXCLUSION.md` |
| C893 | Q₅,Q₆ | The northeast square owns at least one of (2.5,2),(2.54,1.99), while the southeast square owns both | `C893-CONTINUOUS-EXCLUSION.md` |
| C1084 | Q₅,Q₆ | The remaining inward–outward pair shares (2.46,1.99), up to the stated whole-configuration reflection | `C1084-CENTRAL-REDUCTION.md`, `C1084-DUPLICATE-POINT.md` |

Two additional reusable point theorems drive these endings. `OUTWARD-STRONG-BAR.md` proves an all-angle outward point with the longer actual segment [2.26,2.86]×{3}, without assuming exclusion of (3,3). The new theorem in `C893-CONTINUOUS-EXCLUSION.md` instead takes the corner marker (3.086,3) as owned and proves a two-point alternative using only three owned and three excluded points. The marker's different statuses are therefore preserved rather than identified across cases.

Every new continuous proof includes both angle signs, the axial and diagonal limits, and tangency at excluded points or complete segments. Each actual-owner mapping and each retained entrance is recorded in the indicated chapter. These endings replace the relevant later finite propagation/capacity calculations; they do not claim to replace the original finite local ownership rule itself. No complete C982 conclusion is added by this section, and the C974 center estimates earlier in this file retain their stated, separate scope.
