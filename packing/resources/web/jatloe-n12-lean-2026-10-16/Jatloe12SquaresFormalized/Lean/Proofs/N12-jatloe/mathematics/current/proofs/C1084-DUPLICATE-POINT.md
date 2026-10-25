# C1084: the strict duplicate point closes the remaining configuration

## 1. Universal strict point in the inward central square

**Theorem 1 (inward central ownership).** Let Q be an open square of side a>1. Suppose that Q strictly owns

    A=(2.35,1.65),  O=(2,1.74),  D=(2.26,2),

and excludes

    L=(1.65,1.65),  N=(2.35,2.35),  E=(2.4,1).

Then Q strictly owns

    K=(2.46,1.99).

Every terminating decimal in this statement and proof denotes its exact
rational value. No bound on the center, no bound above on a, no restriction
on the square's orientation, and no neighboring-square approximation are
assumed.

For the inward C1084 owner Q5, the three strict anchors are its original
marker and its exact auxiliary pair of label 65552. The two excluded
markers L and N have distinct original owners. The excluded auxiliary
point E belongs to the actual bottom square Q9; it is also excluded by
Q5's exact auxiliary label. Thus all six premises are genuine ownership
facts of the remaining configuration.

## 2. Proof of the inward-square theorem

### 2.1. Opposite-face obstruction and coordinates

Call a point lower-u if its projection on a unit face normal u is at or
below the square's lower u face; define upper-u, lower-v, and upper-v
similarly. These definitions include equality, so they describe every
possible failure of strict membership. Every point excluded from Q is of
at least one of these four types.

If two points are at Euclidean distance less than a, they cannot be
beyond opposite parallel faces: their projections on that unit normal
would differ by at least a. We shall use precisely the following exact
distances:

    |L-N|^2 = 49/50,
    |L-E|^2 = 197/200,
    |K-L|^2 = 7717/10000,
    |K-E|^2 = 9837/10000.

All four are strictly less than 1<a^2.

Translate the origin to O. The coordinate vectors, multiplied by 100,
are

| Point | 100(x-2) | 100(y-1.74) |
|---|---:|---:|
| O | 0 | 0 |
| A | 35 | -9 |
| D | 26 | 26 |
| L | -35 | -9 |
| N | 35 | 61 |
| E | 40 | -74 |
| K | 46 | 25 |

Choose canonical orthogonal unit face normals

    u=(c,s),  v=(-s,c),
    c>0,  |s|<=c,  c^2+s^2=1.

Every square admits this choice, by exchanging and reversing its face
normals. We work with the displayed integer coordinate vectors below;
the common positive factor 1/100 does not affect any projection order.

### 2.2. Nonnegative canonical angle

Suppose 0<=s<=c, and put r=s/c. The inequalities

    u(K)-u(O) = 46c+25s > 0,
    v(K)-v(A) = 34c-11s >= 23c > 0,
    v(D)-v(K) = c+20s > 0

and strict ownership of O,A,D rule out lower-u and both v-face exits
for K. Therefore an excluded K would have to be upper-u.

Meanwhile

    u(L)-u(O) = -35c-9s < 0,
    v(L)-v(A) = 70s >= 0.

Thus L cannot be upper-u or lower-v. Since L is excluded, it must be
lower-u or upper-v.

If r<=35/61, then

    v(D)-v(L) = 35c-61s >= 0.

The strict anchor D rules out upper-v for L. Consequently L is lower-u.
An upper-u K would then contradict |K-L|<1<a.

Suppose instead r>35/61. The excluded point E satisfies

    u(E)-u(A) = 5c-65s < 0,
    v(E)-v(O) = -40s-74c < 0.

Consequently E can only be lower-u or lower-v. If L is lower-u, the
preceding |K-L| argument already rules out upper-u for K. Otherwise
L is upper-v. The bound |L-E|<a rules out lower-v for E, so E must
be lower-u. Then |K-E|<a rules out upper-u for K.

This proves strict membership of K for every nonnegative canonical
angle, including axis alignment and the diagonal orientation.

### 2.3. Negative canonical angle

Suppose s=-t with 0<t<=c. The normals are now u=(c,-t), v=(t,c),
and put r=t/c. The strict anchors O,A give

    u(K)-u(O) = 46c-25t >= 21c > 0,
    v(K)-v(A) = 11t+34c > 0.

Thus K is strictly above both lower faces. Only upper-u and upper-v
need to be ruled out.

The excluded point L satisfies

    u(L)-u(O) = -35c+9t <= -26c < 0,
    v(L)-v(O) = -35t-9c < 0.

Therefore L can only be lower-u or lower-v. The excluded point E
satisfies

    u(E)-u(O) = 40c+74t > 0,
    v(E)-v(O) = 40t-74c <= -34c < 0.

Therefore E can only be upper-u or lower-v.

First rule out upper-v for K, uniformly for all r. If E is lower-v,
then |K-E|<a does so directly. If E is not lower-v, it is upper-u.
Then |L-E|<a rules out lower-u for L, so L must be lower-v. The
bound |K-L|<a again rules out upper-v for K.

It remains to rule out upper-u. If r>=11/34, then

    u(K)-u(A) = 11c-34t <= 0.

Since A is strictly below the upper u face, K is also strictly below it.

If r<11/34, use the excluded point N. Its u projection is strictly
between those of the strict anchors O and A, because

    u(N)-u(O) = 35c-61t
               > (35-61*11/34)c = (519/34)c > 0,
    u(N)-u(A) = -70t < 0.

Also v(N)-v(O)=35t+61c>0. Thus N can only be upper-v. The distance
|L-N|<a rules out lower-v for L. Hence L must be lower-u, and
|K-L|<a rules out upper-u for K.

Neither upper face can contain or be crossed by K. Along with the
strict lower-face inequalities, this proves K belongs to the interior
of Q for every negative canonical angle, and completes the theorem.


## 3. The outward square owns the same point

**Theorem 2 (outward positive-angle ownership).** Let D be an open square of side a>1 with a positive canonical frame

\[
u=(c,s),\qquad v=(-s,c),\qquad
c\ge s\ge0,\qquad c^2+s^2=1.
\]

In coordinates translated by (−2,−2), suppose D strictly owns

\[
N=(.35,.35),\qquad A=(1,.26),
\]

and excludes

\[
G=(.26,0),\ R=(1.086,0),\
F=(.26,1),\ T=(.8,1),\
P=(1,1),\ H=(1.086,1).
\]

Then D strictly owns K=(.46,−.01). Equivalently, in the original coordinates it owns (2.46,1.99).

No container hypothesis or upper side bound is required. The proof permits weak exterior equalities at all six excluded points.

**Proof.** Write

\[
D=\{X:U<u\cdot X<U+a,\quad V<v\cdot X<V+a\}.
\]

First we force four face assignments.

Both upper bands of G are strict by comparison with N:

\[
u(N)-u(G)=.09c+.35s>0,\qquad
v(N)-v(G)=.35c-.09s>0.
\]

Thus G leaves through a lower face. Suppose it left through the lower v-face, so V≥−.26s. At F the upper u-band is strict by comparison with A, because

\[
u(A)-u(F)=.74(c-s)\ge0,
\]

and the lower v-band is strict by comparison with N. The upper v-face alternative for F would give a≤c≤1, using V≥−.26s. Consequently F would have to leave through its lower u-face:

\[
U\ge.26c+s.
\]

At T both lower bands are strict by N, since its projection increments are .45c+.65s>0 and .65c−.45s>0. An upper v-face exclusion of T would give a≤c−.54s≤1. Thus T would leave through the upper u-face, yielding

\[
a\le(.8c+s)-(.26c+s)=.54c<1.
\]

This contradiction proves

\[
U\ge.26c. \tag{1}
\]

At R the lower u-band is strict by N and the upper v-band is strict by A:

\[
u(R)-u(N)=.736c-.35s>0,\qquad
v(A)-v(R)=.26c+.086s>0.
\]

Its upper u-face alternative, combined with (1), would give a≤.826c<1. Therefore

\[
V\ge-1.086s. \tag{2}
\]

At H both lower bands are strict: use N for u and A for v. If it exited through the upper v-face, (2) would imply a≤c≤1. Hence

\[
U+a\le1.086c+s. \tag{3}
\]

Combining (1) and (3), and using a>1 and c≤1, gives

\[
1<a\le.826c+s\le.826+s,
\qquad s>.174. \tag{4}
\]

At P both lower bands are strict by N. If it exited through the upper v-face, (2) would give a≤c+.086s. Since c≤1−s²/2, this would imply

\[
1<c+.086s\le1-\frac{s^2}{2}+.086s,
\qquad 0<s<.172,
\]

contradicting (4). Thus

\[
U+a\le c+s. \tag{5}
\]

We now check K's four strict bands. The upper bands are immediate:

\[
u(A)-u(K)=.54c+.27s>0,\qquad
v(N)-v(K)=.36c+.11s>0. \tag{6}
\]

As already noted, T has strict lower bands and therefore exits through an upper face.

If T exits through the upper u-face, then U+a≤.8c+s. The projection gap to K satisfies

\[
u(T)-u(K)=.34c+1.01s
\le\frac{1.35}{\sqrt2}<1<a. \tag{7}
\]

The first inequality follows because .34 cos θ+1.01 sin θ increases on 0≤θ≤π/4; the last is equivalent to 1.35²<2. It follows from (7) that K has strict lower u-band.

If instead T exits through its upper v-face, then V+a≤c−.8s. Combining this with (2) gives

\[
1<a\le c+.286s. \tag{8}
\]

Put t=s/(1+c), the nonnegative half-angle parameter. Here s>0 by (4), and (8) gives t<.286=143/500. The function .54 cos θ+1.01 sin θ is increasing on the entire canonical interval. At t=143/500 its exact value is

\[
.54c+1.01s
=
\frac{13419377}{13522450}<1.
\]

Consequently, throughout (8),

\[
u(P)-u(K)=.54c+1.01s<1<a. \tag{9}
\]

Equation (5) and (9) again give the strict lower u-band of K.

For clarity, the rational evaluation in (9) uses

\[
c=\frac{229551}{270449},\qquad
s=\frac{143000}{270449}
\]

at t=143/500. The difference between the denominator and numerator of the displayed value is the positive integer 103073; no numerical approximation is involved.

It remains to prove the lower v-band. If s/c≥1/2, compare directly with A:

\[
v(K)-v(A)=.54s-.27c\ge0,
\]

so K has that strict band. If s/c<1/2, then s<1/√5<.45. In this case T cannot exit through its upper u-face, because (1) would give

\[
a\le.54c+s<.54+.45=.99<1.
\]

Thus T exits through the upper v-face. Equations (4) and c≤1 give

\[
v(T)-v(K)=1.01c-.34s
<1.01-.34(.174)=.95084<1<a.
\]

Since V+a≤v(T), this implies V<v(K). Together with (6)–(9), all four bands of K are strict, proving K∈D. ∎

## 4. Exact C1084 mapping and complete exclusion

Use the original C1084 owner order retained in `C1084-CENTRAL-REDUCTION.md`. That chapter reduces the family, up to simultaneous reflection in y=2, to

\[
Q_5:\{4,16\},\qquad Q_6:\{9,19\},\qquad Q_{10}:\{8,18\}.
\]

The mixed-span alternative was already completely excluded there. In the displayed remaining alternative, the inward square Q₅ meets Theorem 1, and the outward square Q₆ meets Theorem 2 after its angle is fixed by Theorem 6 of `C981-WALL-CYCLES.md`.

For the outward square the exact points are:

| Theorem point | Original coordinates | Genuine source |
|---|---|---|
| Strict N | (2.35,2.35) | Q₆'s original northeast central marker |
| Strict A | (3,2.26) | Q₆'s auxiliary 9 |
| Excluded G | (2.26,2) | Q₅'s auxiliary 16 |
| Excluded R | (3.086,2) | Q₁₀'s original right wall marker |
| Excluded F | (2.26,3) | Q₁₁'s auxiliary 17 |
| Excluded T | (2.8,3) | Strictly in Q₁₁ by the reflected wall-advance theorem |
| Excluded P | (3,3) | Strictly in the actual paired northeast corner Q₂ |
| Excluded H | (3.086,3) | Q₂'s original right corner marker |

The sign-lock application uses the same actual Q₆ marker, its auxiliary 19 at (3,2.4), the isolated exclusions (3,3),(3.086,2),(2.26,2), and the whole segment [2.26,2.8]×{3} in Q₁₁. Reflect the full local configuration in y=2 to apply that theorem. It excludes every nonpositive canonical angle of the original Q₆, leaving precisely the positive angle covered by Theorem 2 above.

The point T and the whole top segment come from the actual Q₁₁. Its reflected wall-advance premises are the original top wall marker (2,3.086), auxiliary (2.4,3), and foreign strict points (1.74,3),(1.87,3.24),(2.35,2.35). The first two foreign points are in the actual northwest singleton Q₃; the last is in Q₆. Auxiliary (2.26,3) is also strict in Q₁₁. Convexity therefore gives the entire strict segment. No union of points with different owners has been substituted for a square.

Theorems 1 and 2 now give the same strict point:

\[
(2.46,1.99)\in Q_5\cap Q_6.
\]

The two actual open squares have disjoint interiors, so this is impossible. The simultaneous reflected remaining alternative is impossible for the same reason.

**Conclusion. C1084 is completely excluded by the retained local ownership entrance, the two wall advances, the mixed-span obstruction, the outward sign lock, and the two strict-point theorems in this chapter.** The geometric ending has no orientation subdivision, center enclosure, propagated local domain, finite reach table, or upper bound on a. Every exclusion and every auxiliary owner used in it is identified above or in the inward-square theorem's mapping.

## 5. A stronger inward point for reuse

**Corollary 3.** Under exactly the six point premises of Theorem 1, the
inward square also strictly owns

    K*=(2.54,1.99).

Here is the full check against the proof, retaining its face argument
and including the changed threshold. In the translated coordinates of
Section 2, multiply by 100 as before. The target is now K*=(54,25),
while all other coordinate vectors are unchanged. The two changed
distance squares are

    |K*-L|^2 = (.89)^2+(.34)^2 = 9077/10000 < 1,
    |K*-E|^2 = (.14)^2+(.99)^2 = 9997/10000 < 1.

The distances |L-N| and |L-E| retain their original values below one.

For a nonnegative canonical angle, K* has strict lower u band and both
strict v bands, since

    u(K*)-u(O)=54c+25s>0,
    v(K*)-v(A)=34c-19s>=15c>0,
    v(D)-v(K*)=c+28s>0.

Thus an excluded K* would be upper-u. The unchanged L/E argument of
Section 2.2, split at s/c=35/61, forces either L or E to be lower-u.
Either choice contradicts the corresponding displayed distance to K*.

For a negative canonical angle, write u=(c,-t), v=(t,c) with
0<t<=c. The target has both strict lower bands:

    u(K*)-u(O)=54c-25t>=29c>0,
    v(K*)-v(A)=19t+34c>0.

The unchanged L/E alternatives of Section 2.3 rule out upper-v for K*:
either E is lower-v, or E is upper-u and then L must be lower-v.
Both alternatives contradict the relevant distance to an upper-v K*.

To rule out upper-u, if t/c>=19/34 then

    u(K*)-u(A)=19c-34t<=0,

so strict ownership of A gives that band directly. If t/c<19/34,
then N's u projection is strictly between those of O and A:

    u(N)-u(O)=35c-61t
              >(35-61*19/34)c=(31/34)c>0,
    u(N)-u(A)=-70t<0.

Its lower v band is strict by O, so N must be upper-v. The distance
|L-N|<a forces L to be lower-u. Finally |K*-L|<a rules out upper-u
for K*. All four target bands are strict, proving the corollary for
every canonical angle. The established C1084 application continues to
use its original common point; this stronger conclusion is available
for other actual-owner configurations satisfying the same six premises.
