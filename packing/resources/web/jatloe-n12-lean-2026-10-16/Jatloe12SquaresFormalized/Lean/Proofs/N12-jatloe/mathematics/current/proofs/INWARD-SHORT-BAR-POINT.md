# An inward central square and a short actual bottom segment

All terminating decimals denote exact rationals. A strictly owned point
belongs to the open square. An excluded point or segment may touch a
supporting line. No container, upper side bound, or orientation condition
is imposed in the following theorem.

## 1. The local strict-point theorem

**Theorem.** Let A be an open square of side a>1. Suppose A strictly owns

    M=(.35,−.35), D=(.26,0), P=(0,−.26),

excludes F=(1,−.26), and excludes the entire segment

    S=[.26,.35]×{−1}.

Then A strictly owns K=(.05,−.05).

Write R=(.26,−1) and T=(.35,−1) for the endpoints of S.
The segment premise is essential to the positive-angle proof: separate
unowned endpoints are not substituted for one actual foreign segment.

## 2. Positive canonical angles

Use u=(c,s), v=(−s,c), where c≥s≥0 and c²+s²=1. Write the open
bands as U<u·X<U+a and V<v·X<V+a. Suppose K is excluded.
Its lower-u, upper-u, and lower-v bands are strict by P,M,M:

    u(K)−u(P)=.05c+.21s>0,
    u(M)−u(K)=.30(c−s)≥0,
    v(K)−v(M)=.30(c+s)>0.

Even when a displayed increment is zero, the anchor is strict. Thus

    V+a≤v(K)=−.05(c+s).                              (1)

At F its lower-u band follows from M, its upper-v band from P, and
its lower-v band follows from the opposite cap (1). The three gaps are

    u(F)−u(M)=.65c+.09s>0,
    v(P)−v(F)=s≥0,
    v(K)−v(F)=.21c+.95s≤sqrt(.9466)<1<a.

Consequently F is upper-u:

    U+a≤c−.26s.                                      (2)

At R its upper-u band follows from D and its upper-v band from M.
Its lower-v band again follows from (1), since

    u(D)−u(R)=s≥0,
    v(M)−v(R)=.65c−.09s>0,
    v(K)−v(R)=.95c+.21s≤sqrt(.9466)<1<a.

Hence R is lower-u:

    U≥.26c−s.                                       (3)

In particular (2),(3) imply a≤.74(c+s), so s>0. At T its
upper-v band is strict by M, with gap .65c. A lower-u exclusion
would contradict (2), since the resulting width would be
.65c+.74s≤sqrt(.9701)<1. An upper-u exclusion would contradict
(3), giving width .09c<1. Thus T is lower-v. Both its u bands
are strict and

    V≥−.35s−c.                                      (4)

On y=−1 put

    x_u=(U+s)/c,        x_v=(−c−V)/s.

The conclusions at R,T give

    .26≤x_u<.35,        .26<x_v≤.35.

Throughout S the upper-u band is strict by T and the upper-v band
is strict by M. If x_u<x_v, every abscissa strictly between them
would also satisfy both lower bands and would be a strict point of
A on S. Since the entire segment is excluded, x_u≥x_v. Multiplication
by cs>0 yields

    sU+cV≥−1.                                       (5)

The left side is the ordinate of A's lowest closed vertex. The two
upper caps (1),(2) instead give

    sU+cV≤.95cs−.21s²−.05−a(c+s).

Together with (5), this would imply

    a(c+s)≤.95+.95cs−.21s².                         (6)

Let w=c+s. The identity w−1=2cs/(w+1) gives w−1≥(4/5)cs,
because w≤sqrt(2)<3/2. Therefore

    w−(.95+.95cs−.21s²)
       ≥.05−.15cs+.21s²
       ≥.05−.15s+.21s²
       =(21/100)(s−5/14)²+13/560>0.

This contradicts (6), since a>1. The target is strict in the entire
nonnegative canonical sector, including its axial and diagonal limits.

## 3. Negative canonical angles

Now use u=(c,−s), v=(s,c), with the same c≥s≥0. The target's
upper-u, lower-v, and upper-v bands are strict by M,P,D:

    u(M)−u(K)=.30(c+s)>0,
    v(K)−v(P)=.05s+.21c>0,
    v(D)−v(K)=.21s+.05c>0.

If K were excluded, it would therefore be lower-u:

    U≥.05(c+s).                                      (7)

At F both lower bands are strict by M and P respectively. If F
were upper-u, (7) would imply

    a≤.95c+.21s≤sqrt(.9466)<1.

Thus F must be upper-v:

    V+a≤s−.26c.                                      (8)

At T its lower-u and upper-v bands follow from M, with gaps .65s≥0
and .65c>0. Its lower-v band follows from (8), because

    v(F)−v(T)=.65s+.74c≤sqrt(.9701)<1<a.

The excluded T is consequently upper-u, U+a≤.35c+s. Together
with (7) this gives

    a≤.30c+.95s≤sqrt(.9925)<1,

which is impossible. This sign uses only F,T as exclusions. Both
signs preserve weak exterior inequalities and prove all four target
bands strictly, completing the theorem. ∎

## 4. An exact merged-left consequence in C983

Use C983's original owner numbering: Q5 is the southeast central
square, Q7 owns both western central markers, Q8 is the left wall,
Q9 the bottom wall, and Q0,Q1 are the southwest singletons. The
retained local label families are those of
`C983-01-entrance-and-catalogue.txt` in the supplied earlier source.

**Corollary.** In C983, suppose Q5 owns F4=(2,1.74) and G6=(2.26,2)
and excludes F8=(3,1.74). Then Q7 must own F5=(2,2.26).

Every original Q9 label owns F6=(2.4,1) and G5=(2.26,1), so the
whole segment [2.26,2.35]×{1} is strict in that one actual owner.
Apply the local theorem to Q5 after translation by (−2,−2). It gives

    (2.05,1.95) strictly in Q5.                       (9)

Suppose Q7 excluded F5. It excludes F4 because Q5 owns F4. It also
excludes F0=(1,1.74), F1=(1,2.26), and the left-wall marker (.914,2):
these are strict in Q1,Q8,Q8 respectively, by their exact original
labels and marker ownership. Its two strict western markers are
(1.65,1.65),(1.65,2.35). Reflect x↦4−x and translate by (−2,−2).
Theorem 11 of [OTHER-GEOMETRY.md](OTHER-GEOMETRY.md) applies to this
actual merged square: its two anchors become (.35,±.35), its four
chord-endpoint exclusions become (0,±.26),(1,±.26), and its fifth
exclusion becomes (1.086,0). The theorem gives, in original coordinates,

    (2.05,1.95) strictly in Q7.

This contradicts (9). Thus F5 is strict in Q7, as asserted. The
corollary is a proved common ownership implication, not a complete
exclusion of C983 or an assumption that every auxiliary is owned.
