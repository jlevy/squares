# A mixed span is impossible with four isolated exclusions

Every decimal below is an exact rational. An owned point is strictly in the open square. An excluded point may lie on its boundary. No wall, side upper bound, center condition, original marker, or whole foreign segment is needed.

**Theorem.** No open square of side a>1 can strictly own

    A=(2,1.74), B=(3,1.6)

while excluding all four points

    D=(2.26,2), H=(3,1.74), F=(2.26,1), T=(2.4,1).

**Proof.** Translate by (−2,−1), obtaining

    A=(0,.74), B=(1,.6), D=(.26,1), H=(1,.74),
    F=(.26,0), T=(.4,0).

Every square admits one of the canonical frames

    u=(c,s), v=(−s,c),   or   u=(c,−s), v=(s,c),
    c≥s≥0, c²+s²=1.

Let U,V be its lower face coordinates. Thus strict membership means U<u(X)<U+a and V<v(X)<V+a. A strict anchor with the same projection as a proposed point still supplies the corresponding strict band.

First take the nonpositive frame u=(c,−s), v=(s,c). At D the lower u band follows from A, the upper u band from B, and the lower v band from A, since the respective nonnegative projection differences are

    u(D)−u(A)=.26(c−s),
    u(B)−u(D)=.74c+.4s,
    v(D)−v(A)=.26(c+s).

Thus D must be upper v. At F the lower u band follows from A, the upper u band from B, and the upper v band from A:

    u(F)−u(A)=.26c+.74s>0,
    u(B)−u(F)=.74c−.6s≥.14c>0,
    v(A)−v(F)=.74c−.26s≥.48c>0.

Therefore F must be lower v. These opposite faces give a≤v(D)−v(F)=c≤1, a contradiction. This includes s=0 and c=s.

Now take the nonnegative frame u=(c,s), v=(−s,c). At H, the lower u and lower v bands follow from B, and the upper v band follows from A:

    u(H)−u(B)=.14s≥0,
    v(H)−v(B)=.14c>0,
    v(A)−v(H)=s≥0.

Hence H must be upper u. At D, the lower u and lower v bands follow from A, and the upper u band follows from B:

    u(D)−u(A)=.26(c+s)>0,
    v(D)−v(A)=.26(c−s)≥0,
    u(B)−u(D)=.74c−.4s≥.34c>0.

Hence D must be upper v. The upper u and upper v bands of F follow from B and A, respectively. It must therefore be lower u or lower v. Lower v together with D upper v would give a≤c≤1, so F is lower u. Consequently

    a≤u(H)−u(F)=.74(c+s).                              (1)

Put τ=s/c. If 0≤τ≤1/2, the increasing function (1+τ)/sqrt(1+τ²) gives

    a≤.74·3/sqrt(5)=2.22/sqrt(5)<1,

because 2.22²=4.9284<5. Thus τ>1/2 is necessary.

At T the upper u and upper v bands follow strictly from B and A. Its lower u band is also strict: otherwise T lower u together with H upper u would imply

    a≤u(H)−u(T)=.6c+.74s≤sqrt(.9076)<1.

Therefore T must be lower v. Together with D upper v this yields

    a≤v(D)−v(T)=c+.14s.

The function (1+.14τ)/sqrt(1+τ²) decreases for τ≥1/2, since its derivative has the sign of .14−τ. Hence

    a≤2.14/sqrt(5)<1,

because 2.14²=4.5796<5. This final contradiction covers the rest of the canonical interval. All exterior face inequalities were weak and every interior comparison was strict; tangency creates no exception. ∎

## Exact transfer to C974 and C976

Apply the simultaneous rotation R(x,y)=(4−y,x). The theorem's two strict points become

    A↦G6=(2.26,2),  B↦F7=(2.4,3),

and its four excluded points become

    D↦F5=(2,2.26),  H↦G7=(2.26,3),
    F↦F9=(3,2.26),  T↦G9=(3,2.4).

In either original family, northeast Q7 with label65664 owns F7,G6 and excludes F5,G7. The last two exclusions are strict in the actual right wall Q10 in every retained alternative. Thus label65664 is impossible. No point from two different owners has been joined into a fictitious segment.

This also supplies a shorter reusable ending for any other retained mixed-span configuration with exactly these six point premises. Where H is owned by the candidate square, the theorem is inapplicable; the stronger earlier whole-segment lemma remains distinct.
