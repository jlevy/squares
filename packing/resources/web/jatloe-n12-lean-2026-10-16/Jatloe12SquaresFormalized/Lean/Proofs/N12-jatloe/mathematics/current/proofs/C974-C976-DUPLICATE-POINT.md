# Further strict-point contradictions for C974 and C976

Every decimal is an exact rational. Owned points are strictly interior; excluded points may touch faces. All squares have side a>1. The point lemmas have no container premise or upper bound on a. Their applications use the original local ownership entrance, whose precise source is recorded in `C974-C976-CONTINUOUS-REDUCTIONS.md`.

## 1. A stronger point in the outward square

**Theorem 1.** Let Q have a nonnegative canonical frame u=(c,s), v=(−s,c), where c≥s≥0 and c²+s²=1. In coordinates translated by (−2,−2), suppose Q strictly owns

    N=(.35,.35), A=(1,.26),

and excludes

    G=(.26,0), R=(1.086,0), F=(.26,1), T=(.8,1),
    P=(1,1), H=(1.086,1).

Then Q strictly owns K=(.50,−.04), or (2.50,1.96) in the original coordinates.

These are exactly the hypotheses of Theorem 2 in `C1084-DUPLICATE-POINT.md`; only the forced point is different. For completeness the face reduction is repeated below.

**Proof.** Let U,V denote the lower face coordinates. At G both upper bands follow strictly from N, so G is lower u or lower v. Suppose G were lower v, giving V≥−.26s. At F its upper u band follows from A and its lower v band from N. It cannot be upper v, since this would give a≤c≤1. Thus F is lower u, U≥.26c+s. At T both lower bands follow from N; if T were upper v, then a≤c−.54s≤1, so it is upper u. But then a≤.54c<1. This contradiction proves

    U≥.26c.                                             (1)

At R the lower u band follows from N and the upper v band from A. Its upper u exclusion would give a≤.826c<1 by (1), so

    V≥−1.086s.                                          (2)

At H both lower bands follow from N,A. Upper v would give a≤c≤1 by (2), so U+a≤1.086c+s. Combining this with (1) gives

    1<a≤.826c+s≤.826+s,  hence s>.174.                  (3)

At P both lower bands follow from N. If it were upper v, (2) would imply a≤c+.086s. Since c≤1−s²/2, this forces 0<s<.172, contrary to (3). Consequently

    U+a≤c+s.                                            (4)

The target's two upper bands follow from strict anchors:

    u(A)−u(K)=.50c+.30s>0,
    v(N)−v(K)=.15s+.39c>0.                              (5)

As above, T has both lower bands and therefore exits through an upper face. If T is upper u, then

    u(T)−u(K)=.30c+1.04s≤1.34/sqrt(2)<1<a.

Here .30cosθ+1.04sinθ increases for 0≤θ≤π/4. The opposite-face comparison proves K's strict lower u band.

If T is upper v, then (2) gives 1<a≤c+.286s. Put t=s/(1+c). Since s>0, the exact half-angle identity

    c+.286s−1=2t(.286−t)/(1+t²)

implies t<143/500. The function .50cosθ+1.04sinθ increases on the canonical interval. At t=143/500,

    c=229551/270449,  s=143000/270449,
    .50c+1.04s=526991/540898<1.                          (6)

The exact margin in (6) is 13907/540898. Equation (4) and the opposite-face gap u(P)−u(K)=.50c+1.04s<1<a again prove K's lower u band.

For the lower v band, if s/c≥3/5, then

    v(K)−v(A)=.50s−.30c≥0,

and the strict anchor A suffices. If s/c<3/5, T cannot be upper u: (1) would give

    a≤.54c+s≤5.7/sqrt(34)<1,

where the middle expression increases up to s/c=3/5 and 5.7²=32.49<34. Therefore T is upper v. From (3),

    v(T)−v(K)=1.04c−.30s
              <1.04−.30(.174)=.9878<1<a.

This gives the remaining strict lower band. Every band of K is strict, including all limiting face contacts and the diagonal orientation. The axial orientation was already excluded by (3). ∎

## 2. An inward square with a top anchor owns the same reflected point

**Theorem 2.** Let Q strictly own

    M=(2.35,2.35), A=(2,2.26), D=(2.26,2), T=(2.4,3),

and exclude

    F=(2.26,3), L=(1.65,2.35), B=(2.35,1.65).

Then Q strictly owns K=(2.50,2.04), for every orientation.

**Proof.** Translate by (−2,−2). The points become

    M=(.35,.35), A=(0,.26), D=(.26,0), T=(.4,1),
    F=(.26,1), L=(−.35,.35), B=(.35,−.35),
    K=(.50,.04).

Let U,V be the lower face coordinates. First use a nonnegative canonical frame u=(c,s), v=(−s,c), with c≥s≥0 and c²+s²=1. The lower u band of K follows from D, and its upper v band follows from M, since

    u(K)−u(D)=.24c+.04s>0,
    v(M)−v(K)=.15s+.31c>0.                              (7)

Write τ=s/c. If τ≥1/6, then at F the lower u band follows from M, the upper u band from T, and the lower v band from M:

    u(F)−u(M)=−.09c+.65s≥(.65/6−.09)c>0,
    u(T)−u(F)=.14c>0,
    v(F)−v(M)=.09s+.65c>0.

Thus F is upper v. The gap to the target satisfies

    v(F)−v(K)=.96c+.24s≤sqrt(.9792)<1<a,

which gives K's strict lower v band. Its upper u band follows from T because

    u(T)−u(K)=−.10c+.96s≥(.96/6−.10)c=.06c>0.

This proves all four bands for τ≥1/6.

If 0≤τ<1/6, the lower v band of K follows directly from D:

    v(K)−v(D)=.04c−.24s>0.

Only its upper u band remains. At B the lower u band follows from D, and the upper u and upper v bands follow from M,D:

    u(B)−u(D)=.09c−.35s>(.09−.35/6)c>0,
    u(M)−u(B)=.70s≥0,
    v(D)−v(B)=.09s+.35c>0.

Thus B is lower v. At L the upper u and lower v bands follow from A, because

    u(A)−u(L)=.35c−.09s>0,
    v(L)−v(A)=.35s+.09c>0.

An upper v exclusion of L would combine with B lower v to give

    a≤v(L)−v(B)=.70(c+s)<.70(7/6)c<1.

Therefore L is lower u. If K were upper u, then

    a≤u(K)−u(L)=.85c−.31s≤.85<1.

This contradiction gives its final strict band and completes the nonnegative sign, including s=0.

For the nonpositive canonical frame u=(c,−s), v=(s,c), the target's lower u, lower v and upper v bands follow from D,D,M:

    u(K)−u(D)=.24c−.04s≥.20c>0,
    v(K)−v(D)=.24s+.04c>0,
    v(M)−v(K)=−.15s+.31c≥.16c>0.

At F, both upper bands follow from T, with increments .14c>0 and .14s≥0, while its lower v band follows from A, with increment .26s+.74c>0. Hence F is lower u. If K were upper u, the opposite faces would give

    a≤u(K)−u(F)=.24c+.96s≤sqrt(.9792)<1.

Thus the last target band is strict. Both signs and their endpoints have now been covered. ∎

## 3. Exact duplicate-point application

In C974 or C976, suppose northeast Q7 has label65696: it owns F5,F7,G6 and excludes G7. Its own marker is M=(2.35,2.35); its other two excluded markers in Theorem 2 belong to actual southeast Q6 and, respectively, are globally absent in C974 or owned by actual left Q8 in C976. Therefore

    (2.50,2.04)∈Q7 strictly.                            (8)

Since Q7 owns G6, the retained southeast family forces Q6 to have label262400, owning F8,G8 and excluding G6. The actual bottom Q9 owns the whole segment [2.26,2.8]×{1}, by the strong wall theorem with the actual southwest singleton Q0; this exact mapping is established in Section 4 of `C974-C976-CONTINUOUS-REDUCTIONS.md`. The outward sign theorem therefore forces Q6 to have a strictly negative canonical angle.

Reflect every point in Theorem 1 through y=2. Its own N,A become Q6's southeast marker and F8=(3,1.74). The six required excluded points have these genuine sources:

| Reflected point | Coordinates | Actual source |
|---|---|---|
| G | (2.26,2) | G6 strictly in Q7 |
| R | (3.086,2) | Right wall Q10 marker |
| F | (2.26,1) | G5 strictly in bottom Q9 |
| T | (2.8,1) | Strong reach of that same Q9 |
| P | (3,1) | Paired southeast corner Q2 |
| H | (3.086,1) | Q2's original marker |

Its reflected angle premise is exactly the sign just proved. Theorem 1 gives

    (2.50,2.04)∈Q6 strictly,                            (9)

contradicting (8) and disjoint interiors. Thus label65696 is impossible in both original families.

## 4. The top owner is forced to its two-point leftward label

Corollary 4 of `C974-C976-CONTINUOUS-REDUCTIONS.md` already excluded every top label containing F7. Thus the top owner has one of

    16392,147464,16424,147496,

all owning F3,G4 and optionally F5 and/or G7.

First suppose top Q11 owns G7. Because Q11 also owns G4, northeast Q7 excludes both G4,G7. Its complete retained local family consequently reduces to the following three possibilities:

    65568: F5,G6;
    65664: F7,G6;
    65696: F5,F7,G6.

The first is impossible by the inward–outward contradiction, Theorem 3 of `C974-C976-CONTINUOUS-REDUCTIONS.md`. The second is impossible by the rotated theorem in `MIXED-SPAN-FOUR-POINTS.md`. The third is impossible by Section 3 above. Therefore Q11 cannot own G7, leaving only labels16392 and16424.

Suppose next that top Q11 owns F5, so that its label is16424. Since Q11 already owns the marker (2,3.086), convexity puts the whole segment

    {2}×[2.26,3.086]

strictly in that one square. Northeast Q7 excludes F5,G4. Its retained family has only labels65664,131200,196736. The first has already been excluded; each of the other two owns both F7=(2.4,3) and G7=(2.26,3).

Apply Theorem 1 of `C981-COMMON-CYCLE.md` to actual Q7. It owns its northeast marker and these two top auxiliaries. Its five excluded points are all supplied by actual owners:

| Required exclusion | Genuine source |
|---|---|
| (2,2.4) | The displayed strict segment in Q11 |
| (2,3) | The same segment in Q11 |
| (3,2.4) | G9 strictly in right wall Q10 |
| (3,3) | Paired northeast corner Q3 |
| (3,2.56) | Theorem 1 of `C974-C976-CONTINUOUS-REDUCTIONS.md`, in that same Q10 |

It follows that (2,2.65) is strict in Q7. This point also lies in Q11's displayed strict segment, a contradiction.

We have therefore proved, in both C974 and C976, the uniform conclusion

    top Q11 has exactly label16392={F3,G4}.             (10)

This reduction uses the complete retained local label families only for the stated structural disjunctions. It does not enumerate the original twelve-owner vectors and does not replace the earlier finite local ownership entrance.

## 5. Present scope

The theorems above and `MIXED-SPAN-FOUR-POINTS.md` remove northeast labels65664 and65696 and every top alternative except16392. The direct actual-corner transfer in Section 3.1 of `C974-C976-CONTINUOUS-REDUCTIONS.md` then gives (2,3) strictly in the top owner throughout both surviving families, using only the legitimate weaker left-wall advance in C976. The larger left-wall/corner segment completion remains an additional C974-only consequence. Neither family is marked fully excluded by this chapter alone; their remaining central configurations require an additional continuous ending.
