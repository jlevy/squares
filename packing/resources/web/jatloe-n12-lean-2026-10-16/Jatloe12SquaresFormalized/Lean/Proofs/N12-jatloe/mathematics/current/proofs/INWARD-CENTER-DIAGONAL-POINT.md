# A known inward center forces the diagonal halfpoint

All terminating decimals are exact rationals. An owned point is strictly inside its actual open square; an excluded point may be tangent. There is no angle, wall or side upper bound in this statement.

**Theorem 1.** Suppose an open square C of side a>1 strictly owns

    O=(0,0), M=(.35,.35),

and excludes

    N=(−.35,.35), D=(.35,−.35).

Then it strictly owns

    Z=(.5,.5).

**Proof.** The complete point data and the target are invariant under transposition x↔y. Transpose the same actual square if necessary, and label its canonical faces so that its normals are

    u=(c,−s), v=(s,c), c≥s≥0, c²+s²=1.

Write U,V for the lower faces. Strict O ownership gives U,V<0 and U+a,V+a>0.

At N, its upper u-band follows from O because u(N)=−.35(c+s)<0. Its lower v-band follows from O because v(N)=.35(c−s)≥0. Its upper v-band follows from M because v(M)−v(N)=.7s≥0. A projection equal to that of a strict anchor still satisfies the corresponding strict band. Thus the only possible exit of N is lower u, and

    U≥−.35(c+s).                                   (1)

At D, its lower u-band and upper v-band follow from O, since u(D)=.35(c+s)>0 and v(D)=−.35(c−s)≤0. If D exited upper u, (1) would give

    a≤.7(c+s)≤.7sqrt(2)<1,

which is impossible. Hence D is lower v:

    V≥−.35(c−s).                                   (2)

For Z, both lower bands follow strictly from M: its two projection increments are .15(c−s)≥0 and .15(c+s)>0. Its two upper bands follow from (1),(2), because

    u(Z)−U≤.85c−.15s≤.85<1<a,
    v(Z)−V≤.85c+.15s≤sqrt(.85²+.15²)
                         =sqrt(.745)<1<a.

Thus all four bands of Z are strict. This also covers the axial and diagonal canonical endpoints. Transposition proves the other sign without changing any owner or exclusion. ∎

## C1092 MMMP consequence

The full inward-center theorem proves (2,2) strictly in actual Q7 for every original MMMP alternative. Apply Theorem 1 in the chart

    (xi,eta)=(2−x,y−2).

The strict M is Q7's original northwest marker. The excluded N,D are respectively the original northeast marker in actual Q6 and southwest marker in actual Q4. Thus the theorem's Z gives

    (1.5,2.5) strictly in Q7.

The three other vertices (2,2),(1.5,2),(2,2.5) are already strict by `C1092-MMMP-FULL-INWARD-CENTER.md` and `C1092-MMMP-CENTER-CROSSPOINTS.md`. Convexity therefore puts the whole closed half-unit square

    [1.5,2]×[2,2.5]

strictly inside this same actual Q7. Its edges are strict foreign segments for every other original owner. This conclusion assigns neither G1 nor any missing auxiliary point to an artificial owner.

## A longer diagonal point from the same hypotheses

**Corollary 2.** Under exactly the hypotheses of Theorem 1, every point (k,k) with

    .35≤k≤sqrt(151)/20

is strict in C. In particular C strictly owns (.61,.61).

**Proof.** Retain the same canonical transposition and the forced lower faces (1),(2). Both lower bands of (k,k) follow from M. For the upper bands,

    u(k,k)−U≤(k+.35)c−(k−.35)s≤k+.35<1,
    v(k,k)−V≤(k+.35)c+(k−.35)s
               ≤sqrt(2k²+49/200)≤1<a.

The final quadratic inequality is exactly k²≤151/400. Also sqrt(151)/20<.65, so the first upper bound is strict. Transposition fixes the target and proves the other sign. This establishes the full interval, including its irrational endpoint and both canonical orientation endpoints. ∎

In the actual MMMP chart above, k=.61 gives the additional strict point

    (1.39,2.61)∈Q7.

Its only hypotheses remain the original two foreign central markers and the already proved strict center; no auxiliary ownership or wall condition has been added.
