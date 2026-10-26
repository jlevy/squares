# C976: the actual merged left square reaches the upper line

All decimals denote exact rationals. Owned points are strict in the indicated open square of side a>1. Excluded points and whole segments may touch its boundary. The local theorem uses no container wall or upper bound on a.

## 1. Statement and the sign forced by the southwest strict point

**Theorem 1.** Let N strictly own

    P=(−.086,0), M=(.65,.35), H=(0,.26),

and exclude D=(.5,0), K=(0,1), X=(.27,−.04), and the complete segments

    T=[.44,.74]×{1},
    S L=[(−.24,−.13),(0,−.26)].

Then N has a strictly positive canonical angle. In its positive frame

    u=(c,s), v=(−s,c), c≥s>0, c²+s²=1,

it satisfies

    21/65<s/c<3/4,                                      (1)

and strictly owns

    Z=(.25,1), J=(0,.8).                                (2)

Write U,V for lower faces and A=U+a, B=V+a. First exclude the nonpositive canonical frame u=(c,−s), v=(s,c). The negative-sign part of Theorem 1 in `C976-MERGED-LEFT-ENDING.md`, Section 2, uses exactly P,M,H,D,K,L and proves that X is strict; its top-segment hypothesis is unused in that sign. Here is the relevant argument explicitly.

If s/c≤3/7, D is strict from P,M, contrary to its exclusion. Thus s/c>3/7. Three bands of X follow from P,M, and its upper u band also follows from M when s/c≤38/39. In the remaining interval, suppose A≤u(X). At K the lower u band is strict because u(X)−u(K)=.27c+1.04s≤1.31/sqrt(2)<1<a; its upper u and lower v bands follow from M,H. Hence B≤c. At L the two u bands follow from P,M and the upper v band from H, so V≥−.26c. This gives a≤1.26c<7.56/sqrt(61)<1, since s/c>38/39>5/6. All alternatives contradict X being excluded. This includes the axial and diagonal endpoints, so N has a strictly positive canonical frame.

## 2. The short actual top segment supplies a broad angle interval

In the positive frame, comparisons with P,M show that D has both u bands and its upper v band strict. At K both lower bands follow from P,H and its upper u band follows from M. At X both u bands and the upper v band follow from P,M. Thus their exclusions give

    V≥−.5s, B≤c, V≥−.27s−.04c.                         (3)

Both lower bands of each endpoint of T follow from P. An upper-v exit of T1=(.74,1), opposing the first face in (3), would imply a≤c−.24s≤1. Hence

    A≤.74c+s.                                          (4)

Suppose s/c≤21/65. Then T0=(.44,1) has its upper u band strict by M, because .21c−.65s≥0. It must be upper v, so B≤c−.44s. Exclusion of the entire segment T, together with these opposite endpoint faces, implies

    sA+cB≤1.                                           (5)

Indeed, if the left side were larger, the nonempty chord interval

    (c−B)/s < x < (A−s)/c

on y=1 would lie inside [.44,.74]. Its points have both upper bands strict; both lower bands hold there by P. This would meet the excluded whole segment.

But strict ownership of M and (3) give

    sA+cB>c+.15cs+.35s²>1.                             (6)

For the last comparison, put t=s/(1+c). In the assumed interval 0<t<8/25, and

    c+.15cs+.35s²−1
      =t(3−6t−3t²−20t³)/(10(1+t²)²).

The parenthesized polynomial decreases on [0,8/25] and equals 367/3125>0 at its right endpoint. Equations (5)–(6) are contradictory. Thus s/c>21/65.

Now an upper-v exit of T0 would give a≤c+.06s<1. To check strictness, t>.06 in this interval: at t=.06 one has s/c=300/2491<21/65. The identity c+.06s−1=2t(.06−t)/(1+t²) proves the claimed comparison. Consequently

    A≤.44c+s.                                          (7)

The last two faces in (3) give a≤1.04c+.27s. This expression decreases for s/c≥3/4 and equals .994<1 at s/c=3/4. Thus s/c<3/4. This proves (1), with both endpoints strictly excluded by a>1.

## 3. The upper point Z has four strict bands

The lower u band of Z follows from P and its lower v band follows from H; the latter increment is .74c−.25s>0. Its upper v band follows strictly from the last lower face in (3), since

    v(Z)−V≤1.04c+.02s<1<a.                             (8)

The expression on the right decreases for s/c≥21/65. Its exact value at that endpoint is 3401/(50sqrt(4666))<1, because 3401²<2500·4666.

If s/c≤8/13, the upper u band of Z follows from M: u(M)−u(Z)=.4c−.65s≥0. It remains to prove that band when

    8/13<s/c<3/4.                                      (9)

Both upper bands at L follow from M,H. If L exits through lower u, then U≥−.26s and

    u(Z)−U≤.25c+1.26s<.956<1<a.

The expression increases over the canonical interval; .956 is its value at s/c=3/4. Hence this case is complete.

Otherwise L is strictly above its lower u face and exits through lower v. At S both upper bands follow from P,H. A lower-v exit of S would, by B≤c, imply

    a≤1.13c−.24s<1

throughout (9). For example, this expression decreases there and at s/c=8/13 equals 1277/(100sqrt(233))<1. Therefore S exits through lower u, and its lower v band is strict by the same opposite-width estimate.

The line of S L is .13x+.24y=−.0624. Its coefficients in the u,v frame are

    α=.13c+.24s>0, β=.24c−.13s>0.

The endpoints exit through the two different lower faces, while their upper bands are strict. Exclusion of the whole segment consequently forces

    αU+βV≥−.0624.                                      (10)

If the lower corner lay on the other side, a nonempty portion between the two lower-face crossings would lie strictly in N; equality in (10) is the allowed corner tangency.

Using V≤c−a in (10),

    α(A−u(Z))
      ≥a(α+β)−βc−αu(Z)−.0624
      >f(c,s),

where

    f(c,s)=.37c+.11s−.3024−.0325c²−.06cs.

This f is positive throughout (9). Its derivative with respect to the canonical angle is

    −.37s+.11c+.065cs−.06(c²−s²)<0:

indeed s>1/2, c≤1, cs≤1/2 and c²−s²≥0 give the strict upper bound −.0425. At the endpoint s/c=3/4, f=.01>0. Hence f>.01 throughout (9). Since α>0, A>u(Z), completing Z's last strict band.

For J=(0,.8), its lower u band follows from P, its upper u band from M, and its lower v band from H. Its upper v band follows from (3), because

    v(J)−V≤.84c+.27s≤sqrt(.7785)<1<a.

This proves both points in (2), covering every angle and exterior tangency. ∎

## 4. Exact C976 ownership and the northwest corner consequence

First make the required top reach explicit. Apply Theorem 1 of `C974-C976-CONTINUOUS-REDUCTIONS.md` to actual Q11 under (x,y)↦(4−y,4−x). Its strict top marker and F3 map to (.914,2),(1,2.4); its excluded G7 in actual Q7 maps to (1,1.74); the northwest marker in actual Q8 maps to (1.65,2.35). The genuine top wall maps to x≥0. That theorem gives (1.44,3) strictly in Q11, and its strict G4 gives the entire top segment [1.44,1.74]×{3} in that same owner.

Translate actual Q8 by (−1,−2). Its original merged markers give P,M, and both retained labels2050,2082 give H=F1. The required D=(1.5,2) and X=(1.27,1.96) are strict in actual southwest Q5 by the completed crosspoint and southwest support-point lemmas. K=(1,3) is strict in the actual paired northwest corner Q4. The short top segment is the actual Q11 segment just proved. The segment S L is the retained actual singleton Q1 segment [(.76,1.87),(1,1.74)]. Thus every exclusion has a genuine different owner, and Theorem 1 gives

    (1.25,3)∈Q8, (1,2.8)∈Q8, both strictly.             (11)

It also gives the strictly positive Q8 angle interval (1), independently of the remaining northeast label or its sign.

The actual Q4 already owns (1,3), excludes the point (1,2.8) in Q8 and the point (1.44,3) in Q11, and has its closure in x≥0. Apply Theorem 5 of `OTHER-GEOMETRY.md` in coordinates (ξ,η)=(y−3,1−x), with

    p=.44, q=.2, r=.6.

Its exact conditions are p²+q²=.2336<1, p²+r²=.5536<1 and q+r=.8<2sqrt(2)−2. Hence

    (1,3.6)∈Q4 strictly.                               (12)

The full segment {1}×[3,3.6] is therefore strict in that single actual corner. These are further continuous consequences for C976. They do not assert the complete contradiction for its remaining strictly negative northeast branches. The corresponding C974 marker is absent, so the merged-marker premise used for (11) is not available in C974.

## 5. A slightly farther strict point on the upper line

**Corollary 2.** Under the hypotheses of Theorem 1, the point

    Z*=(.28,1)

is also strict in N. Consequently the actual C976 owner Q8 strictly owns

    (1.28,3).                                          (13)

**Proof.** Retain the positive frame, the interval 21/65<s/c<3/4, and all the weak faces proved in Sections 1–2. The lower u band of Z* follows from P, and its lower v band follows from H, with increment .74c−.28s>0. Its upper v band follows from V≥−.27s−.04c, because

    v(Z*)−V≤1.04c−.01s<1.04c+.02s<1<a,

where the last strict bound is (8).

If s/c≤37/65, its upper u band follows from M, since u(M)−u(Z*)=.37c−.65s≥0. Suppose therefore that 37/65<s/c<3/4. If L exits lower u, then U≥−.26s and

    u(Z*)−U≤.28c+1.26s<.98<1<a;

the expression increases in the canonical angle, and .98 is its value at s/c=3/4.

Otherwise L is strictly above its lower u face and exits lower v. At S both upper bands still follow from P,H. A lower-v exit would imply a≤1.13c−.24s. This expression decreases on the present interval, and its value at the left endpoint is

    6457/(100sqrt(5594))<1,

as follows by squaring positive quantities. Thus S exits lower u and has its lower v band strict. The same whole-segment argument as in (10), including its tangency case, gives αU+βV≥−.0624, with α=.13c+.24s>0 and β=.24c−.13s>0. Combining it with V≤c−a now yields

    α(A−u(Z*))
      >f*(c,s)=.37c+.11s−.3024−.0364c²−.0672cs.

This scalar decreases in the required interval. Indeed s>49/100 there, c≤1, cs≤1/2, and c²−s²≥0, so its angular derivative obeys

    −.37s+.11c+.0728cs−.0672(c²−s²)
      <−.37(.49)+.11+.0364=−.0349<0.

At c=4/5,s=3/5 its exact value is

    f*=253/62500=.004048>0.

Therefore A>u(Z*) strictly. All four target bands hold, including the split endpoint s/c=37/65; the other angle endpoints were already strictly excluded. Translating by (1,2) gives (13) for the same actual Q8 used in Section 4. No extra exclusion or foreign owner was added. ∎
