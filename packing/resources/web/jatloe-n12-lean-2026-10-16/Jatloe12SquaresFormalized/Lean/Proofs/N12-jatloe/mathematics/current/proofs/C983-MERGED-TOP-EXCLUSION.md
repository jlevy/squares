# C983: the merged western square cannot own the left top auxiliary

All terminating decimals are exact rationals. Every owned point belongs
strictly to the actual open square. An excluded segment may meet its
boundary. The following theorem states explicitly its modest side cap;
the original model provides it.

## 1. A continuous two-anchor, one-segment obstruction

**Theorem.** No open square Q of side

    1<a≤1001/1000

can strictly own both

    P=(1.65,1.65), T=(1.6,3),

while excluding N=(2.35,2.35) and the entire segment

    S={1}×[2.26,2.4].

Write J=(1,2.26), L=(1,2.4). No container wall or other owner is
assumed in the local theorem. In one orientation sign the segment
becomes a genuine supporting line by convexity.

## 2. Nonnegative canonical angles: opposite widths

Use the frame u=(c,s), v=(−s,c), with c≥s≥0 and c²+s²=1. Let
U,V be the lower face coordinates, so strict membership is

    U<u·X<U+a, V<v·X<V+a.

At N both lower bands follow from P, and its upper v-band follows
from T. The three increments are

    u(N)−u(P)=.7(c+s)>0,
    v(N)−v(P)=.7(c−s)≥0,
    v(T)−v(N)=.75s+.65c>0.

Thus its exclusion forces U+a≤2.35(c+s). At L its upper u-band
follows from T, lower v-band from P, and upper v-band from T:

    u(T)−u(L)=.6(c+s)>0,
    v(L)−v(P)=.65s+.75c>0,
    v(T)−v(L)=.6(c−s)≥0.

Therefore U≥c+2.4s. These two exclusions imply

    a≤1.35c−.05s.

But the two strict anchors have v-projection difference

    v(T)−v(P)=1.35c+.05s<a.

The inequalities are inconsistent, including s=0 and c=s. This
orientation sign needs only the point L and no upper bound on a.

## 3. Nonpositive canonical angles: the excluded segment is a wall

Now use u=(c,−s), v=(s,c), c≥s≥0, c²+s²=1. Strict ownership
of P,T implies

    1.35c−.05s<a≤1001/1000.                         (1)

Put τ=s/c. The function (1.35−.05τ)/sqrt(1+τ²) decreases for
τ≥0, since its derivative has the sign of −.05−1.35τ. At τ=5/6
its value is 157/(20sqrt(61)), and the exact squared comparison is

    [157/(20sqrt(61))]²−(1001/1000)²
      =500439/61000000>0.

Consequently

    τ>5/6, .64<s<5/7, c>7/10.                     (2)

Here s>5/sqrt(61)>.64 follows from 25/61>(16/25)², and the
canonical upper bound s≤1/sqrt(2)<5/7 is strict as displayed.

At L, the upper u-band follows from P and both v-bands follow
from P,T. In detail,

    u(P)−u(L)=.65c+.75s>0,
    v(L)−v(P)=.75c−.65s≥.10c>0,
    v(T)−v(L)=.6(c+s)>0.

Thus

    U≥c−2.4s.                                      (3)

At J its upper u-band follows from P, its upper v-band from T,
and its lower u-band from T. The last, nontrivial increment is

    u(J)−u(T)=−.6c+.74s
       >[−.6+.74(5/6)]c=c/60>0.

Therefore

    V≥s+2.26c.                                     (4)

Every hypothetical strict point of Q on x=1 would have y<2.4
by (3) and y>2.26 by (4). It would lie on the actual excluded
segment S. Thus Q has no interior intersection with x=1. Since
its strict point P lies to the right, convexity puts its entire
closure in x≥1. The exact left support is

    cU+sV≥1.                                       (5)

This line is derived from the excluded whole segment. It is not
an additional container hypothesis.

## 4. The opposite marker is now strict in all four bands

Both lower bands of N follow from P. We prove that both upper
bands are strict too.

Strict ownership of P gives V<1.65(c+s). Combining this with (5)
and a>1,

    c[U+a−u(N)]
       >ac−1.35+.7s(c+s)
       >c−1.35+.7s(c+s).                           (6)

The last expression is positive throughout (2). Indeed
1−c=s²/(1+c)≤.6s², so it is at least

    p(s)=−.35+.7s+.1s²−.42s³.

On [.64,5/7], the derivative .7+.2s−1.26s² is decreasing and
is at least its endpoint value 1/5. Hence p increases there, and

    p(.64)=.02885952>0.

Equation (6) therefore gives u(N)<U+a strictly.

Similarly, strict ownership of T gives U<1.6c−3s. From (5),

    s[V+a−v(N)]
       >as−.6−.75s²+.65cs
       >s−.6−.75s²+.65cs
       ≥1.455s−.75s²−.6.                           (7)

The final quadratic is concave. Its values at .64 and 5/7 are

    3/125 and 111/1960,

respectively, both positive. It is therefore positive on the
whole interval. Since s>0, equation (7) proves v(N)<V+a.

All four bands of N are strict, contradicting its exclusion.
Together with Section 2 this covers every orientation, all
canonical endpoints, and all permitted exterior tangencies. ∎

## 5. Exact C983 ownership consequence

In C983, the actual square Q7 owns both western central markers,
including P=(1.65,1.65). The northeast marker N=(2.35,2.35) is
strict in the distinct actual square Q6. Every original left-wall
label for Q8, namely 2050 or 2058, owns both F1=(1,2.26) and
G1=(1,2.4). Therefore the whole segment S is strict in the one
actual Q8 and excluded from Q7.

The theorem proves

    F3=(1.6,3) is outside Q7.                       (8)

It eliminates every retained Q7 label containing F3 at once:

    8200, 8216, 8232, 24584, 24600, 24616, 73768.

These are all such labels in the retained C983 local family.
The argument does not subdivide square angles or enumerate
twelve-owner configurations. It uses one common pair of strict
anchors, one actual foreign marker, and one actual foreign segment.
It is a completed ownership reduction, not a whole-family exclusion.

## 6. The nearer top auxiliary fixes the angle and forces F5

**Lemma 2.** Under the same side condition, if a square strictly owns
P=(1.65,1.65) and T'=(1.74,3), and excludes J=(1,2.26), then it
has a strictly positive canonical angle and strictly owns F5=(2,2.26).

For a nonpositive canonical frame, the two anchors have v-projection
difference

    1.35c+.09s<a.

The left side, as a function of the angle on [0,π/4], is positive
and concave, so its minimum is attained at an endpoint. Both endpoint
values 1.35 and 1.44/sqrt(2) exceed 1001/1000; the latter squared
comparison is 1.0368>1.002001. This contradicts the permitted side
cap, including both angle endpoints. Thus the angle is strictly
positive.

In the positive frame, J's upper u-band and upper v-band follow
from T', and its lower v-band follows from P:

    u(T')−u(J)=.74(c+s)>0,
    v(T')−v(J)=.74(c−s)≥0,
    v(J)−v(P)=.65s+.61c>0.

Therefore U≥c+2.26s. At F5 both lower bands follow from P and
its upper v-band follows from T', with increments

    .35c+.61s>0, .61c−.35s≥.26c>0,
    .26s+.74c>0.

An upper u-face exclusion of F5 would now give a≤c≤1.
Its fourth band is therefore strict too, proving the lemma.

In C983 the point J belongs strictly to actual Q8, so the lemma
applies whenever merged Q7 owns G4=(1.74,3). Thus

    Q7 owns G4 ⇒ Q7 is positive and owns F5.         (9)

## 7. Two immediate restrictions from the merged anchors

Merged Q7 cannot own G7=(2.26,3). Its distance squared from the
strict southwest marker P is

    .61²+1.35²=2.1946>2(1001/1000)²=2.004002.

The diameter of the closure of a side-a square is a sqrt(2).
Two strict points cannot have the displayed larger distance. This
eliminates both original merged labels 139296 and 139312.

Finally, if Q7 owns G6=(2.26,2), then it owns at least one of
F4=(2,1.74) and F5=(2,2.26). This conclusion requires neither a
side cap nor a foreign exclusion. Translate by (−2,−2); its anchors
are the two points (−.35,±.35) and (.26,0). In a nonnegative frame,
the target F5=(0,.26) has its lower u- and lower v-bands from
(−.35,−.35), its upper u-band from (.26,0), and its upper v-band
from (−.35,.35). The nonnegative increments are

    .35c+.61s, .61c−.35s, .26(c−s), .35s+.09c.

The first, second and fourth are positive, and equality in the
third still compares against a strict anchor. Thus F5 is strict.
Reflection in y=2 proves strict F4 for a nonpositive frame.
Consequently

    Q7 owns G6 ⇒ Q7 owns F4 or F5,                  (10)

with the specified stronger conclusion in each orientation sign.

## 8. Combined exact merged-owner reduction

For reference, the retained original local family for Q7 is

    8192,24576,73728,8200,24584,8208,24592,73744,
    8216,24600,8224,24608,73760,139296,8232,24616,
    73768,8240,24624,73776,139312.

Remove the F3 labels by (8), the G7 labels by the diameter argument,
and 73728 by (10). Among the remaining G4 labels, (9) excludes
24576 and 24592. The necessary local family is reduced to

    8192,8208,8224,8240,24608,24624,73744,73760,73776.

The label24624 owns F4,F5,G3,G4 and is also impossible by a short
ownership chain. Because G4 would belong to Q7, the retained top
labels of Q11 reduce to131200,655488,131232; all three own F7,G7.
Hence northeast Q6 excludes F5 and F7. Every retained northeast
label avoiding those two points owns F9. The retained right-wall
labels avoiding F9 are262400 and327936, both owning F8. Southeast
Q5 would then exclude both F4 and F8, whereas every one of its
retained original labels owns at least one of those two points.
This is a contradiction. In each step disjointness is used between
the indicated actual owners; no assertion that every auxiliary is
owned somewhere is required.

Thus the necessary original merged-owner family is

    8192,8208,8224,8240,24608,73744,73760,73776.

This short deletion argument concerns exact point ownership sets;
it does not subdivide orientations. Each substantive geometric
implication above is proved for the full continuous orientation
domain. The inward southeast implication in
[INWARD-SHORT-BAR-POINT.md](INWARD-SHORT-BAR-POINT.md) is an
additional independent restriction on the surviving configurations.
