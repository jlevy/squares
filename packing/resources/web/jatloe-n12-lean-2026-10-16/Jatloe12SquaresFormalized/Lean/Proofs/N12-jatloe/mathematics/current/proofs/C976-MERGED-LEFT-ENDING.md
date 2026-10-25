# C976: a continuous ending for both nonnegative northeast alternatives

Decimals denote exact rationals. Every owned point is strictly in its indicated open square of side a>1. Every excluded point or segment may touch its boundary. The local theorem below uses no wall and no upper bound on a.

## 1. The strengthened merged-left point theorem

**Theorem 1.** Suppose an open square N of side a>1 strictly owns

    P=(−.086,0), M=(.65,.35), H=(0,.26),

and excludes D=(.5,0), K=(0,1), and the complete segments

    T=[.27,.74]×{1},
    V=[S,L], S=(−.24,−.13), L=(0,−.26).

Then Z=(.27,−.04) is strictly in N.

**Canonical notation.** In either frame u=(c,s), v=(−s,c) or u=(c,−s), v=(s,c), take c≥s≥0 and c²+s²=1. Write U,V0 for the lower band coordinates, and A=U+a, B=V0+a for the upper ones. The symbol V for the foreign segment will never denote a face coordinate.

## 2. The nonpositive sign

Use u=(c,−s), v=(s,c), and put τ=s/c. If τ≤3/7, the excluded D has all four bands strictly from P,M: its only potentially limiting comparison is

    u(M)−u(D)=.15c−.35s≥0.

Thus τ>3/7; this also excludes the axial case. The target's lower u and upper v bands follow from P,M. Its lower v band follows from P because

    v(Z)−v(P)=.356s−.04c>0.

If τ≤38/39, its upper u band follows from M, with difference .38c−.39s≥0. Suppose instead τ>38/39 and that Z is upper u, A≤u(Z). At K its upper u band follows from M and its lower v band from H. Its lower u band is strict because

    u(Z)−u(K)=.27c+1.04s≤1.31/sqrt(2)<1<a.

Consequently K is upper v, B≤c. At L both u bands follow from P,M; the upper-u difference .65c−.61s≥.04c is positive. Its upper v band follows from H, so L is lower v, V0≥−.26c. These faces give

    a≤1.26c<7.56/sqrt(61)<1,

since τ>38/39>5/6 implies c<6/sqrt(61), and 7.56²<61. This contradiction proves the target for the nonpositive sign.

## 3. Positive sign: the actual top segment supplies an angle bound

Use u=(c,s), v=(−s,c), with τ=s/c and t=s/(1+c). The point D has its lower u, upper u and upper v bands from P,M, so

    V0≥−.5s.                                            (1)

The point K has both lower bands from P,H and its upper u band from M, the latter comparison being .65(c−s)≥0. Hence

    B≤c.                                                (2)

Let T0=(.27,1), T1=(.74,1). Both lower bands at these endpoints follow from P. If T1 were upper v, (1) would give a≤c−.24s≤1. Therefore

    A≤.74c+s.                                          (3)

If τ≤38/65, the upper u band of T0 follows from M because .38c−.65s≥0. Thus T0 must be upper v, B≤c−.27s. These two endpoint faces and exclusion of the whole segment T force

    sA+cB≤1.                                           (4)

Indeed, if sA+cB>1, the open interval

    (c−B)/s < x < (A−s)/c

would be nonempty and lie inside [.27,.74] by the two endpoint bounds. Its points (x,1) would have all four bands strictly and meet the excluded segment. The axis s=0 has already been excluded, so the division is legitimate.

On the other hand, strict ownership of M and a>1, together with (1), give

    sA+cB>c+.15cs+.35s².                               (5)

This last expression exceeds one on 0<τ≤38/65. To verify it on a larger interval, t<8/25 there, and the exact identity is

    c+.15cs+.35s²−1
      =t(3−6t−3t²−20t³)/(10(1+t²)²).

The parenthesized polynomial decreases on [0,8/25] and equals 367/3125>0 at its right endpoint. Equations (4)–(5) contradict one another. Therefore

    τ>38/65.                                            (6)

In this interval an upper-v exclusion of T0 would give a≤c+.23s<1. The function (1+.23τ)/sqrt(1+τ²) decreases for τ≥38/65, and its value at that endpoint is 3687/(50sqrt(5669))<1; the exact squared comparison is 3687²<2500·5669. Consequently

    A≤.27c+s.                                          (7)

## 4. The actual left segment completes the lower-face information

Both upper bands at S follow from P,H. Its exclusion cannot be lower v: by (2) that would give a≤1.13c−.24s<1. Indeed (6) implies c<65/sqrt(5669)<7/8, so even 1.13c<791/800<1. Thus S is lower u, and its lower v band is strictly inside the square by the same opposite-width estimate.

Both upper bands at L follow from M,H. Suppose L were not lower u. Then it would be lower v, V0≥−.26c; from (2), a≤1.26c. Therefore c>50/63, and

    t²=(1−c)/(1+c)<13/113<(17/50)².                  (8)

The line through the excluded segment S L is

    .13x+.24y=−.0624.

Its coefficients in u,v coordinates are α=.13c+.24s>0 and β=.24c−.13s>0. The endpoint S lies weakly below its lower u face and strictly above its lower v face; L lies strictly above its lower u face and weakly below its lower v face. Their upper bands are strict. Exclusion of the complete segment therefore implies

    αU+βV0≥−.0624.                                    (9)

If the lower corner were on the other side of the line, a nonempty part of the segment between its two lower-face crossings would be strictly in N. Equality is the allowed corner tangency.

Combining (9), (7), and (2),

    a(.37c+.11s)≤.3375−.0351s²+.0648cs.                (10)

The right side is strictly less than .37c+.11s whenever (8) holds. Here is a complete exact polynomial certificate. Let

    q(t)=(325+904t−5346t²+3496t³−7075t⁴)/10000.

Then

    q(t)=(1+t²)²(.37c+.11s−.3375+.0351s²−.0648cs).

For z=50t/17 on [0,1], its Bernstein expansion is

    q(t)=Σ(j=0,...,4) binom(4,j) b_j z^j(1−z)^(4−j),

with the five positive coefficients

    (b0,b1,b2,b3,b4)=
    (13/400,5023/125000,939201/25000000,
     4388639/156250000,14305853/2500000000).

Expanding verifies the identity; the nonnegative basis sums to one. Hence q>0 on the full interval [0,17/50]. Equation (10) contradicts a>1. Thus L must be lower u:

    U≥−.26s.

Together with (7), this implies a≤.27c+1.26s. The right side increases throughout the canonical interval and at t=7/20 is exactly 44757/44900<1. Consequently

    t>7/20.                                             (11)

## 5. All target bands are strict in the positive sign

The lower u, upper u and upper v bands of Z follow from P,M,P, respectively. Their differences are

    u(Z)−u(P)=.356c−.04s≥.316c>0,
    u(M)−u(Z)=.38c+.39s>0,
    v(P)−v(Z)=.356s+.04c>0.

For the last band, use (2) and a>1. The opposite gap c−v(Z)=1.04c+.27s decreases for τ≥38/65. By (11) it is less than its exact value at t=7/20,

    1.04c+.27s<11016/11225<1<a.

Thus V0=B−a<v(Z). The positive sign is complete. The proof covers both diagonal limits, excludes the axial case by the original strict anchors, and permits every exterior tangency. This proves Theorem 1. ∎

## 6. The actual C976 branch ends at a duplicate point

Assume the retained central labels are Q6=327936 and Q7=131232, and that Q7 has nonnegative canonical angle. Corollary 3 of `C974-C976-FINAL-ANGLE-REDUCTIONS.md` puts (1.27,3) strictly in the actual top square Q11. Its established top origin (2,3), and the original G4=(1.74,3), put the entire interval [1.27,1.74]×{3} strictly in that same actual owner.

Apply Theorem 1 above to the merged left square N=Q8 after translating by (−1,−2).

| Local datum | Original datum | Actual owner |
|---|---|---|
| P=(−.086,0) | (.914,2) | Q8, original left-wall marker |
| M=(.65,.35) | (1.65,2.35) | Q8, original merged northwest marker in C976 |
| H=(0,.26) | F1=(1,2.26) | Q8, retained label2050 |
| Excluded D=(.5,0) | (1.5,2) | Q5, completed strict crosspoint |
| Excluded K=(0,1) | (1,3) | Actual paired northwest corner Q4 |
| Excluded top segment T | [1.27,1.74]×{3} | One actual Q11, as proved above |
| Excluded left segment S L | [(.76,1.87),(1,1.74)] | One actual singleton Q1, its retained seed and F0 |

Every owner supplying an exclusion is distinct from Q8. Thus

    (1.27,1.96)∈Q8 strictly.                            (12)

Theorem 1 of `C974-C976-SW-SUPPORT-POINT.md` gives that same point strictly in actual Q5, using its actual southeast and bottom neighbours and the fixed southwest singleton supports. This contradicts the disjoint interiors of Q5 and Q8.

Therefore the C976 pair (327936,131232) is impossible whenever Q7 has a nonnegative canonical angle. Any remaining occurrence of that exact pair must have strictly negative canonical angle; it then has the established northeast crosspoint (2.5,3) and right-wall origin (3,2).

## 7. The top-only northeast alternative has the same ending

Suppose instead the retained northeast label is Q7=131200 and its canonical angle is nonnegative. Corollary 4 of `TOP-ONLY-LEFT-POINT.md` gives (1.2,3) strictly in the actual top square Q11. Its strict G4=(1.74,3) therefore puts the whole shorter interval [1.27,1.74]×{3} strictly in that same owner.

All the other inputs in the table of Section 6 are unchanged. In this branch Q8 may have retained label2050 or2082; both own F1=(1,2.26), and both have the same original merged northwest marker and left-wall marker. Theorem 1 uses no F5 exclusion from Q8, so the optional F5 ownership in label2082 has no effect. Likewise Q5 may have label8208 or8240; both satisfy the exact all-angle southwest support-point theorem. Apply Theorem 1 to Q8 with the same two genuine foreign segments to obtain (1.27,1.96) strictly in Q8. That point is already strict in Q5, giving the same contradiction.

Thus both remaining C976 central pairs are impossible whenever Q7 has nonnegative canonical angle. Every remaining C976 configuration must have Q6=327936, Q7 in {131200,131232}, and strictly negative canonical angle for Q7. Both alternatives have the established northeast point (2.5,3) and right-wall origin (3,2).

C974 has no northwest marker in Q8. Theorem 1's merged-marker premise is consequently unavailable there, and this chapter asserts no C974 branch closure. The top-wall advance itself remains valid for the positive top-only branch of C974 by its separate actual-owner proof.
