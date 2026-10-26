# C1092 MPPM without a wall omission: a common radial reduction

All terminating decimals are exact rational numbers. Retain the complete original C1092 entrance in C1092-ORIGINAL-ENTRANCE.txt, its actual twelve open square owners, common side 1<a≤1.001, disjoint interiors and genuine container. The present MPPM class has

    Y8≥2, X9≤2, Y10≤2, X11≥2.

This chapter concerns the branch in which Q9 owns F2, Q10 owns G8, Q11 owns F7, and Q8 owns G1. No historical 802-vector or 82-vector reduction is assumed. The original wall-sign chord theorem supplies the complementary auxiliaries, so the actual four pairs are

    Q9: F2,G2; Q10: F8,G8; Q11: F7,G7; Q8: F1,G1.     (1)

Owned points are strict; an absent auxiliary is merely excluded from that owner and need not be assigned elsewhere. All face and separating equalities are allowed.

## 1. Three actual central alternatives

In the southwest sector write A=Q4. The original covering alternatives, after the strict foreign points in (1), require

    at least one of F0,F4 in A;
    at least one of G0,G3 in A.                         (2)

Additional auxiliaries may still be present. If A owned F4,G0 and omitted both F0,G3, reflect MIXED-SPAN-FOUR-POINTS.md through x=2. Its two strict anchors would be F4,G0, and its four exclusions would be G3,F0,G2,F2. The first two are the hypothesized omissions and the last two are strict in the one actual Q9. That theorem excludes this alternative.

Consequently the following three alternatives exhaust (2):

1. A owns its ordinary pair F0,G0.
2. A owns its inward pair F4,G3.
3. A owns F0,G3 and omits G0,F4.

The first two may overlap. They are used as a cover, not as a partition. The third is the remaining elbow alternative. Simultaneous quarter-turns R(x,y)=(4−y,x) give the same complete cover for the other three actual central squares. They preserve the original entrance and the MPPM signs.

A useful further consequence is

    F4,G3 in Q4  ⇒  F6,G5 in Q5 and F3,G4 in Q7.       (3)

Indeed Q5's F covering forces F6, because F4 is in Q4 and F8 is in Q10. If Q5 omitted G5, its G covering would force G6; the mixed-span theorem after a quarter-turn followed by reflection in y=2 would use strict F6,G6 and excluded F4,G5,F8,G8. This is impossible. Hence G5 also belongs to Q5.

Now apply the retained ordinary wall-reach lemma, reproduced in C981-RETAINED-CONTINUOUS-LEMMAS.md, SectionA.2, to actual Q9 in the chart (xi,eta)=(y,4−x). Its strict marker and outer anchor are the original bottom marker,F2; its two excluded points are G5 in Q5 and F4 in Q4. Its real wall is the bottom wall. Therefore (1.44,1) is strict in actual Q9, and so is (1.5,1), by convexity with F2=(1.6,1).

The retained crosspoint theorem reproduced in the appendix of C893-CONTINUOUS-EXCLUSION.md now applies to Q4 under the simultaneous map (x,y)↦(4−y,4−x). Its strict marker and two inward anchors become Q4's marker,G3,F4; its two neighboring marker exclusions are the actual SE and NW markers; and its two outer exclusions become (1.6,1),(1.5,1), both in actual Q9. Its strict conclusion is

    (1.5,2) in Q4.                                   (3a)

G3 in Q4 and G1 in Q8 force G4 in Q7. If Q7 omitted F3, its F covering would force F5. The reflected ELBOW-CROSSPOINT theorem, followed by R³, would then apply to Q7's strict marker,F5,G4, with excluded F3 by hypothesis, the actual NE marker, and the actual top marker. Its strict point is also (1.5,2), contrary to (3a). Hence Q7 owns F3. This proves (3) with the actual wall advance and both genuine point owners retained.

## 2. A radial lemma for an inward square missing its ordinary auxiliary

**Lemma 1.** Let C be an open square of side a>1, with actual center Z. Suppose C strictly owns

    M=(.35,.35), P=(0,.26), Q=(.26,0),

and excludes the two neighboring markers

    N=(−.35,.35), D=(.35,−.35),

as well as the two points A=(.26,1), B=(.4,1). If C excludes at least one of

    R0=(1,.26), R1=(1,.4),

then

    |Z|<a/sqrt(2).                                    (4)

If O=(0,0) is excluded as well, the stronger bound |Z|<1/sqrt(2) holds. No wall, other actual square, side upper bound, or whole foreign segment is needed.

### 2.1. A symmetric pair of excluded outer points

First suppose R1 is excluded. The strict points M,P,Q, the two excluded markers, and the two excluded points R1,B are invariant under transposition, with N,D and R1,B interchanged. If O belongs to C, its strict membership already gives |Z|<a/sqrt(2), by its two strict center projections. We may therefore suppose O excluded and transpose all data, if necessary, to give C the nonpositive canonical frame

    u=(c,−s), v=(s,c), c≥s≥0, c²+s²=1.

Write U,V for its lower faces. The two u-bands of O follow strictly from P,Q, and its upper v-band follows from M. Thus

    V≥0, V<.26s,                                     (5)

so s>0. The complete face argument of Proposition3 in C1092-MMMP-INWARD-CENTER.md uses exactly the strict M,P,Q and excluded R1,B,N in these coordinates, without its later ownership inspection. It gives

    U≥−.35(c+s), U+a≤c−.4s, V+a≤c+.4s.              (6)

For precision, its forced faces are R1 upper u, B upper v, and N lower u. R1's upper v-band follows from s+.4c≤.7(c+s)<1<a+V. A lower-u B would give width .6(c+s)<1. An upper-u B would require s/c<1/13, whereas N lower v would require s/c>35/61; N lower u paired with B upper u would give width .75c−.65s<1. Thus B is upper v. Finally N lower v would give width .65c+.75s≤sqrt(.985)<1, so N is lower u. This proves every face in (6), including weak exits.

The center projections z_u=U+a/2, z_v=V+a/2 are both strictly positive: use (5),(6), a>1 and .35(c+s)≤.35sqrt(2)<1/2. Their upper bounds are

    0<z_u≤c−.4s−a/2<c−.4s−1/2,
    0<z_v≤c+.4s−a/2<c+.4s−1/2.

The bounds on the right are positive because they exceed the actual positive projections. Hence

    |Z|²<2(c−1/2)²+.32s²<1/2.                       (7)

The complete exact identity proving the last sign is

    1/2−[2(c−1/2)²+.32s²]
      =s²[42/25−2/(1+c)]>0.

Indeed c>7/10 gives the bracket at least 42/25−20/17=214/425>0, and s>0. This proves (4) in the symmetric case.

### 2.2. R0 is excluded but R1 is owned

It remains that R0 is excluded and R1 is strict in C. A nonnegative canonical frame is impossible. In such a frame (c,s),(−s,c), R0's lower u-band follows from Q and its two upper bands follow from R1,M. Thus R0 is lower v. At B, both lower bands follow from Q,M, while its upper u-band follows from R1, since

    u(R1)−u(B)=.6(c−s)≥0.

Thus B is upper v. These two opposite faces would give

    a≤v(B)−v(R0)=.74c+.6s≤sqrt(.9076)<1.

This includes the axial and diagonal representatives. We may therefore use the negative frame u=(c,−s),v=(s,c), with c≥s>0. If O is strict, (4) again follows immediately, so suppose it absent. Equation (5) follows as before.

The excluded R0 has both lower bands from Q and its upper v-band from

    v(R0)=s+.26c≤1.26/sqrt(2)<1<a+V.

Consequently U+a≤c−.26s. For B, its lower v-band follows from M. A lower-u exit would combine with R0's upper-u exit to give width .6c+.74s≤sqrt(.9076)<1. An upper-u exit would require s/c<1/13; the same two N alternatives just used in Section2.1 exclude it. Therefore B is upper v. N cannot then be lower v, because .65c+.75s≤sqrt(.985)<1. We have proved

    U≥−.35(c+s), U+a≤c−.26s,
    V≥0, V+a≤c+.4s.                                  (8)

At A=(.26,1), its upper u-band follows from M, with increment .09c+.65s>0, and its lower v-band follows from M, with increment .65c−.09s>0. Thus A is lower u or upper v.

If A is upper v, replace the last cap in (8) by V+a≤c+.26s. The center projections are positive by the same argument as before, so

    |Z|²<2(c−1/2)²+2(.26)²s²<1/2.

The exact difference from 1/2 is

    s²[2(1−.26²)−2/(1+c)]>0,

since c>7/10 and 2(1−.26²)=1.8648>20/17.

If A is lower u, its opposite cap at R0 gives a≤.74(c+s). If s/c≤1/2, the right side is at most2.22/sqrt(5)<1. Therefore

    s/c>1/2, s>2/5.                                  (9)

The positive center projections and (8) now give

    |Z|²<(c−.26s−1/2)²+(c+.4s−1/2)²=:E.

The exact identity is

    1/2−E
      =s²[4431/2500−2/(1+c)]+(7/50)s(1−2c).

Using c>7/10, c≤1, and (9), its right side is at least

    s[(25327/42500)s−7/50]
      >s[(25327/42500)(2/5)−7/50]
      =(5226/53125)s>0.

Thus |Z|<1/sqrt(2) in this last alternative as well. All canonical signs, both A exits, O ownership and every excluded-face equality have been treated. This proves Lemma1. ∎

## 3. The elbow square has the stronger radial bound

**Lemma 2.** Let C strictly own, in coordinates centered at the physical point (2,2),

    M=(−.35,−.35), P=(−1,−.26), Q=(−.26,0),

and exclude

    G=(−1,−.4), N=(−.35,.35),
    R=(−1.086,0), D=(.35,−.35), B=(−.4,−1).

Then its actual center Z satisfies |Z|<1/sqrt(2), for every side a>1.

**Proof.** Reflect the three-anchor theorem in ELBOW-CROSSPOINT.md. Its strict points are M,P,Q, and its excluded points are N,G,R. Its complete all-angle proof forces the positive frame (c,s),(−s,c), with c≥s>0, and the lower/upper face bounds

    U≥−c−.4s, V+a≤.35(c+s).                         (10)

At D, its lower u-band and upper v-band follow strictly from M. Thus D is upper u or lower v. A lower-v exit paired with (10) would give a≤.7(c+s)≤.7sqrt(2)<1. Therefore

    U+a≤.35(c−s).                                    (11)

At B both upper bands follow from M,P: the positive projection differences are .05c+.65s and .6s+.74c. A lower-u exit paired with (11) would give a≤.75c+.65s≤sqrt(.985)<1. Hence

    V≥.4s−c.                                          (12)

The two center projections are strictly negative by (10),(11), since a/2>1/2>.35(c+s). Their positive opposites x=−z_u,y=−z_v obey

    0<x≤c+.4s−a/2<c+.4s−1/2,
    0<y≤c−.4s−a/2<c−.4s−1/2.

The same exact identity (7) now gives x²+y²<1/2. This proves the lemma. Every assumed exit was weak, and every final center comparison is strict. ∎

## 4. Actual no-omission maps and a global consequence

**Theorem 3.** In the entire original no-omission MPPM branch, at least one of the four actual central squares owns its ordinary pair

    Q4: F0,G0; Q5: F6,G5; Q6: F9,G9; Q7: F3,G4.       (13)

More precisely, every central square that does not own its pair in (13) has its actual center at distance strictly less than a/sqrt(2) from the common physical point (2,2).

**Proof.** It suffices to give the southwest map; simultaneous quarter-turns preserve every hypothesis and fix (2,2). By Section1, a southwest square missing its full ordinary pair either has the inward pair F4,G3 or is the elbow alternative.

For the inward pair use the half-turn chart (xi,eta)=(2−x,2−y). The strict M,P,Q of Lemma1 are respectively the original SW marker,F4,G3. Its two excluded neighboring markers are the actual SE and NW markers. Its A,B are G2,F2, both strictly in actual Q9. The two possible excluded R0,R1 are exactly F0,G0. Since the full ordinary pair is not owned, at least one is genuinely excluded. Thus Lemma1 applies, preserving any ownership of the other outer auxiliary.

For the elbow alternative simply translate by (−2,−2). In Lemma2, M,P,Q are the actual SW marker,F0,G3. Its excluded G is the omitted G0; N,D are the actual NW and SE markers; R is the actual Q8 marker; and B is F2, strictly in Q9. Lemma2 applies. No segment or missing-point owner is required.

If all four central owners missed their respective ordinary pair, their four actual centers would all lie in the open disk of radius a/sqrt(2) about (2,2). Four points in that disk have a pair at distance less than a: order their polar arguments and choose a consecutive gap at most pi/2; the cosine rule bounds that squared distance strictly below a². If one center is the disk center, the same conclusion is immediate. But each actual open side-a square contains its open concentric disk of radius a/2, so disjoint interiors require all their centers to be at distance at least a. This is a contradiction, proving (13). ∎

This chapter supplies a continuous reduction of the complete original branch, not its final exclusion. The remaining obligation is the actual cyclic geometry when one or more of the ordinary pairs (13) is owned. No inner auxiliary is inferred merely from an ordinary pair: that would require additional actual-neighbor support.
