# The negative mixed northeast square has a short continuous angle interval

All decimals are exact rationals. The square in the local theorem has side a>1. Its owned points are strict; the excluded segment may touch its boundary.

## 1. A horizontal foreign segment forces its right endpoint onto the lower face

**Theorem 1.** Let N have nonpositive canonical frame

    u=(c,−s), v=(s,c), c≥s≥0, c²+s²=1,

and strictly own

    F=(0,−.74), M=(.35,−.65), G=(.26,0).

Suppose N excludes O=(0,0) and the entire segment

    I=[.26,.5]×{−1}.

Then its angle is strictly negative and

    0<s/c<13/25.                                       (1)

Moreover, if U,V are its lower faces and A=U+a, B=V+a, then

    U≥0, V≥.5s−c.                                     (2)

**Proof.** At O both upper bands follow from G. The upper-v comparison is still strict when s=0 because G is strict. The lower-v band follows from M, since .65c−.35s≥.30c>0. Hence O must exit through lower u and U≥0. Strict ownership of F gives U<.74s, so s>0; this already excludes the axial case.

At D=(.26,−1), the lower u and upper v bands follow from G. Its upper u band is strict because

    u(D)−U≤.26c+s≤1.26/sqrt(2)<1<a.

Thus D exits through lower v:

    V≥.26s−c.                                         (3)

At X=(.5,−1), the lower u and upper v bands follow from M. The corresponding strict differences are .15c+.35s>0 and .35c−.15s>0. Therefore its exclusion has only the alternatives

    A≤.5c+s,  or  V≥.5s−c.                            (4)

Suppose the first alternative holds. Since U≥0 and a>1,

    1<a=A−U≤.5c+s.

The function (.5+τ)/sqrt(1+τ²) increases on 0≤τ≤1 and equals one at τ=3/4. Thus τ=s/c>3/4 and s>3/5. Also X's lower v band is now strict, because

    v(X)−v(F)=.5s−.26c>0.

The complete segment I has its lower u and upper v bands strict, as follows from G at both endpoints and then by affine interpolation. Its left endpoint D exits lower v, whereas its right endpoint X exits upper u and has its lower v band strict. The nonempty chord on y=−1, if present between these two face crossings, is

    (V+c)/s < x < (A−s)/c.

Equation (3) puts its left endpoint at or to the right of .26, and the supposed upper-u alternative in (4) puts its right endpoint at or to the left of .5. Exclusion of the whole segment therefore forces

    −sA+cV≥−1.                                        (5)

Equality represents the allowed tangency of the lower-right vertex to the horizontal line. But A≥a>1 and strict ownership of F gives V<−.74c. Consequently

    −sA+cV<−s−.74c²<−1.

For the last strict inequality use the exact factorization

    s+.74c²−1=(1−s)(.74s−.26)>0,

which holds because 3/5<s≤1/sqrt(2)<1. This contradicts (5), including its equality case. The upper-u alternative in (4) is impossible.

Hence X must exit lower v and gives the second bound in (2). The strict lower-v band of F now yields

    .5s−c≤V<−.74c,

so .5s<.26c and s/c<13/25. This proves (1) and the theorem. No division by s was made before s>0 was proved, and the diagonal endpoint was covered by the same contradiction. ∎

## 2. Exact application to both remaining mixed northeast families

Take the actual northeast square Q7=131232 in C974 or C976, assume its nonpositive canonical sign, and translate by (−2,−3). Its strict F5, northeast marker and G7 are respectively F,M,G of Theorem 1. The excluded origin O is (2,3), strictly owned by actual Q11 through the completed corner-to-wall transfer.

The two endpoints of I are (2.26,2)=G6 and (2.5,2). Both are strict in the same actual southeast square Q6=327936: G6 is part of its exact label, while the crosspoint is proved in `C974-C976-CENTRAL-CROSSPOINTS.md`, Sections 1–2. Convexity of that one open square makes the entire horizontal segment strict in Q6, so it is excluded from Q7 exactly as the theorem requires.

Therefore, in both C974 and C976,

    Q7=131232 with nonpositive sign ⇒0<|tan θ_Q7|<13/25.

This is a further continuous reduction of the remaining negative branch. It does not assert a final contradiction for either entire family and does not apply to Q7=131200, which does not own F5.
