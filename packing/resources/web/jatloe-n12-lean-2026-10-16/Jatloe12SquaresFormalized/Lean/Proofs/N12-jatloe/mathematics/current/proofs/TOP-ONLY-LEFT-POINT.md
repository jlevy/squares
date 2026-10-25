# A top-only central square reaches the left interior line

Every decimal is an exact rational. Owned points are strictly inside the open square of side a>1. Excluded points and whole segments may touch its boundary. No actual container wall or side upper bound is needed in the local theorem.

## 1. Statement and the two strict short chords

**Theorem 1.** Suppose Q strictly owns

    M=(.35,.35), G=(.26,1), Y=(.525,.125),

and excludes P=(0,.26), O=(0,1), C=(1,1), and the whole segment

    B T={1}×[.26,.56].

Then Q strictly owns X=(0,.62).

**Proof.** The strict segment M Y crosses y=.26 at an abscissa strictly between zero and one. The point G is strict on y=1. On each horizontal line, the two endpoints at x=0 and x=1 are excluded. Thus both open chords are positive and lie in (0,1), with lengths at most one. An axis-parallel square would have chord length a>1 and is impossible.

Choose c≥s>0, c²+s²=1 in either canonical frame. The square's horizontal chord function, where positive, is

    ell(y)=min(a/c, (a(c+s)/2−|y−y0|)/(cs)),

where y0 is its center ordinate. Both chords have length at most one, whereas the plateau has length a/c>1, so neither chord is on the plateau.

The center lies strictly between .26 and1. If it were below both lines or above both lines, the two nonplateau chord lengths would differ by

    .74/(cs)≥1.48>1,

impossible for two positive lengths at most one. A center on either chord line would itself give the plateau length greater than one. Therefore the lower chord is in the lower vertex region, and the upper chord is in the upper vertex region. The next two sections write all four endpoint inequalities in each sign. Endpoints may touch the two excluded points, so the resulting inequalities are weak.

## 2. Positive canonical sign

Use u=(c,s), v=(−s,c), with lower faces U,V. On y=.26 the left and right chord endpoints are

    (U−.26s)/c, (.26c−V)/s.

On y=1 they are

    (c−V−a)/s, (U+a−s)/c.

Their containment in [0,1] gives

    U≥.26s, V≥.26c−s,
    V+a≤c, U+a≤c+s.                                  (1)

At the upper bar endpoint T=(1,.56), the lower u band follows from M, and its upper v band follows from G. Its exclusion is consequently upper u or lower v.

Suppose T were not lower v. Then it would be upper u, U+a≤c+.56s. Any hypothetical interior point of Q on x=1 would have, from this upper u face and the lower v face at B in (1),

    y<.56,  y>.26.

It would lie on the excluded whole segment B T. The square therefore has no interior intersection with x=1. Its strict marker M is to the left of that line, so convexity forces its rightmost closed support to be at most one.

But (1) gives the contradictory lower bound

    xmax=c(U+a)−sV≥a(c+s)−.74cs>1.                    (2)

For the final inequality, c+s−1=2cs/(c+s+1)≥(2sqrt(2)−2)cs>.74cs, and a>1. This argument explicitly keeps the weak tangency possibility xmax=1. It follows that T must be lower v:

    V≥.56c−s,  a≤s+.44c.                              (3)

Set t=s/(1+c)∈(0,sqrt(2)−1]. The exact factorization

    s+.44c−1=2(18t−7)(1−t)/(25(1+t²))

and a>1 show that t>7/18. The target X has its upper u band from M, lower v band from M, and upper v band from G. The increments are .35c−.27s≥.08c>0, .35s+.27c>0, and .38c−.26s≥.12c>0, respectively.

Its remaining lower u band follows from U+a≤c+s: the opposite gap is

    (c+s)−u(X)=c+.38s.

This expression decreases once s/c>.38. At t=7/18 the exact components are c=275/373, s=252/373, and its value is 9269/9325<1. Thus in the required interval c+.38s<1<a, proving the final strict target band.

## 3. Negative canonical sign

Use u=(c,−s), v=(s,c). The lower horizontal chord has endpoints

    (V−.26c)/s, (U+a+.26s)/c,

and the upper chord has endpoints

    (U+s)/c, (V+a−c)/s.

Consequently

    V≥.26c, U+a≤c−.26s,
    U≥−s, V+a≤c+s.                                   (4)

In particular a≤.74c+s. The factorization

    .74c+s−1=(87t−13)(1−t)/(50(1+t²))

gives t>13/87.

At T both lower bands follow from M. An upper v exclusion would give, using (4),

    a≤v(T)−.26c=s+.30c≤1.30/sqrt(2)<1,

which is impossible. The displayed canonical bound holds because s+.30c increases on 0≤theta≤pi/4. Thus

    U+a≤c−.56s.                                       (5)

The target's upper u band follows from M, with increment .35c+.27s>0. Its upper v band follows from G, with increment .26s+.38c>0. Its lower v band follows strictly from the opposite upper face V+a≤c+s because

    (c+s)−v(X)=.38c+s≤1.38/sqrt(2)<1<a.

Finally (5) gives the opposite gap for its lower u band:

    (c−.56s)−u(X)=c+.06s<1<a.

For this last strict comparison, c+.06s−1=2t(.06−t)/(1+t²)<0 since t>13/87>.06. Hence all four target bands are strict in the negative sign too. Both canonical diagonal endpoints have been included, and the axial case was excluded by the two strict short chords. ∎

## 4. The top-only actual owner in C974 and C976

**Corollary 2.** In either remaining C974 or C976 configuration with northeast Q7=131200, the actual Q7 strictly owns

    (2,2.62).                                          (6)

Translate by (−2,−2). The theorem's M,G are the original northeast marker and G7=(2.26,3). Its Y is the point (2.525,2.125) established for that actual top-only owner by Theorem 3 of `OUTWARD-BAR-AND-UPPER-SPAN.md`. That earlier theorem needs exactly the owned northeast marker and F7, the excluded F5, the actual top origin and northeast corner, and the actual right bar—all already present here.

The present theorem's excluded P is F5, excluded by Q7's exact label; no owner for it is presumed. Its O is (2,3), strict in actual Q11. Its C is (3,3), strict in paired corner Q3. Its entire B T is the established strict bar {3}×[2.26,2.56] in actual Q10. The point (6) follows.

This is a further strict point, not by itself a completed contradiction for either family. Its hypotheses deliberately retain the F5 exclusion; it is not applied to the mixed northeast label131232, which owns that point. The additional positive-sign consequence below does complete the corresponding C976 branch.

## 5. A positive-sign tip and an actual top-wall advance

**Corollary 3.** Under the hypotheses of Theorem 1, suppose Q has the positive canonical frame used in Section 2. Then Q strictly owns

    Z=(.026,1).

**Proof.** Retain the weak faces proved in that section:

    U≥.26s, U+a≤c+s, V≥.56c−s.

The lower u band of Z follows strictly from the opposite upper face because

    (c+s)−u(Z)=.974c<1<a.

Its upper u band follows strictly from the opposite lower face because

    u(Z)−.26s=.026c+.74s≤.766<1<a.

Its lower v band follows from the strict point M: the increment is

    v(Z)−v(M)=.324s+.65c>0.

Finally its upper v band follows from the opposite lower face because

    v(Z)−(.56c−s)=.44c+.974s
      ≤1.414/sqrt(2)<1<a.

The first bound holds throughout the canonical interval because .44c+.974s increases there. The second is exact: 1.414²=1.999396<2. Every target band is therefore strict, including at c=s. The axial case is already impossible by the two strict short chords in Section 1. ∎

**Corollary 4.** In either remaining C974 or C976 configuration with Q7=131200 and nonnegative canonical angle, the actual top square Q11 strictly owns

    (1.2,3).

The preceding results put the two strict points (2.026,3) and (2,2.62) in the same actual northeast square Q7. Q11 excludes them, strictly owns its established origin (2,3), and has its closure in the real upper container half-plane y≤4.

Transport all these data by (x,y)↦(2−x,y−3). Apply Theorem 5 of `OTHER-GEOMETRY.md` to Q11 with

    p=.38, q=.026, r=.8.

The strict origin becomes (0,0), the two foreign points become F=(−q,0) and H=(0,−p), and the real wall becomes y≤1. Every parameter condition holds:

    p²+q²=.145076<1,
    p²+r²=.7844<1,
    q+r=.826<2sqrt(2)−2.

For the last exact inequality, 1.413²=1.996569<2. The corner reach theorem is stated for an arbitrary square with this single actual upper wall; it does not require Q11 to be an original corner owner. It gives the strict local point (.8,0), hence the claimed original point (1.2,3). No additional owner or hypothetical foreign segment has been introduced.
