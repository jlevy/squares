# C1092 MPPM: every nonordinary central owner is isolated

Every terminating decimal below is an exact rational number. A point owned by an open square is strictly inside it. An excluded point may be on its boundary. All inequalities concerning excluded faces and separating supports are weak; the common side satisfies a>1.

The local two-square theorem in Sections 1–3 uses no container, upper side bound or numerical orientation catalogue. Section 4 applies it to the complete original no-omission MPPM entrance retained in C1092-ORIGINAL-ENTRANCE.txt, using the already proved covering alternatives in C1092-MPPM-NO-OMISSION-REDUCTION.md. This is a further continuous reduction, not a claimed ending of the entire no-omission family.

## 1. The sharper residual-elbow profile

**Lemma 1.** Suppose an open square C of side a>1 strictly owns

    M=(−.35,−.35), P=(−1,−.26), Q=(−.26,0),

and excludes

    N=(−.35,.35), G=(−1,−.4), R0=(−1.086,0),
    T=(0,−.26), B=(−.4,−1).

Then C has a strictly positive canonical frame

    u=(c,s), v=(−s,c), c≥s>0, c²+s²=1.

Write U,V for the lower faces and J=U+a, K=V+a for the upper faces. Then

    U≥−c−.4s,       J≤−.26s,
    V≥.4s−c,        K≤.35(c+s),                       (1)

and C strictly owns X=(0,−.5). Its half-angle and unit components satisfy

    0<s/(1+c)<7/50,   c>24/25,   0<s<7/25.           (2)

**Proof.** Apply the complete three-anchor theorem in ELBOW-CROSSPOINT.md after translating its coordinates by (−2,−2) and reflecting the horizontal coordinate. Its three strict anchors become M,P,Q and its three excluded points become N,G,R0. That theorem excludes every nonpositive canonical representative of C, including the axial and diagonal alternatives. Its surviving positive frame gives

    U≥−c−.4s, K≤.35(c+s), X strictly in C.             (3)

At T the lower u-band follows strictly from Q, since

    u(T)−u(Q)=.26(c−s)≥0.

The upper v-band also follows strictly from Q, since

    v(Q)−v(T)=.26(c+s)>0.

Thus T must be upper u or lower v. The latter, together with the upper-v cap in (3), would give

    a≤.61c+.35s≤sqrt(.4946)<1.

Consequently J≤u(T)=−.26s.

At B both upper bands follow from strict anchors:

    u(M)−u(B)=.05c+.65s>0,
    v(P)−v(B)=.6s+.74c>0.

Thus B must be lower u or lower v. A lower-u exit, together with J≤−.26s, would give

    a≤.4c+.74s≤sqrt(.7076)<1.

Therefore V≥v(B)=.4s−c. This proves every face in (1).

The two u-faces now imply

    1<a≤c+.14s.                                      (4)

Set z=s/(1+c). Since s>0, the exact half-angle identity

    c+.14s−1=2z(.14−z)/(1+z²)

gives 0<z<7/50. At z=7/50 the corresponding values are

    c=2451/2549>24/25, s=700/2549<7/25.

Cosine decreases and sine increases on the canonical interval, so (2) follows. All strict conclusions use the strict anchors or a>1, and no excluded-face equality has been discarded. ∎

## 2. Two consecutive residual elbows cannot be disjoint

Let R(x,y)=(−y,x) be the quarter-turn about the local origin.

**Theorem 2.** There do not exist two open squares C0,C1 of the same side a>1, with disjoint interiors, such that C0 satisfies all the hypotheses of Lemma 1 and C1 satisfies their simultaneous image under R.

**Proof.** Apply Lemma 1 separately to both actual squares, using local coordinates before rotation for C1. Let their positive canonical angles be p,q, and put

    c=cos p, s=sin p, d=cos q, t=sin q.

Both angles lie strictly between zero and 2 arctan(7/50). In particular

    c,d>24/25, 0<s,t<7/25.                            (5)

For C0 retain faces U,V,J,K as in (1). Let U′,V′,J′,K′ be C1's faces in its coordinates before applying R. In the physical positive frame

    u′=(d,t), v′=(−t,d),

C1 has lower faces

    mathcal U=−K′, mathcal V=U′.

This follows because R sends its local longitudinal axis to v′ and its local transverse axis to −u′. Its profile (1) therefore yields the three bounds

    mathcal U≤d−.4t−a,
    −d−.4t≤mathcal V≤−.26t−a.                       (6)

We retain C0's corresponding bounds

    J≥a−c−.4s,
    K≥a+.4s−c,
    V≤.35(c+s)−a.                                    (7)

### 2.1. The complete separator list

Every separating normal from C0 toward C1 has strictly positive horizontal component: compare their strict markers (−.35,−.35) and (.35,−.35). It also has strictly positive vertical component: Lemma 1 puts X=(0,−.5) strictly in C0, while R(Q)=(0,−.26) is a prescribed strict point of C1.

For two disjoint open squares a supporting line may therefore be chosen with normal equal to one of the two positive longitudinal axes u=(c,s) and u′=(d,t). Indeed, the separating-axis theorem supplies a face normal of one of the actual squares; all other signed face normals have a nonpositive component and fail one of the preceding strict point comparisons. This includes touching closures. No direction arising merely from an auxiliary point configuration is substituted for an actual square normal.

Write

    kappa=cos(q−p)=cd+st,
    sigma=sin(q−p)=ct−sd.

On the full closed range used below,

    kappa>24/25, |sigma|<7/25,
    kappa−|sigma|>0.                                 (8)

We shall contradict separation on each of the two axes, for both relative angle orders. In each calculation replacing a by 1 strictly decreases the relevant support difference, because its coefficient is 1+kappa+|sigma|>0. Thus a nonnegative margin with a replaced by 1 proves strictly overlapping projection interiors on that axis.

### 2.2. The order q≥p

Here sigma≥0. In the u direction, the minimum projection of C1 is

    L1(u)=kappa mathcal U−sigma(mathcal V+a).

By (6),

    L1(u)≤kappa(d−.4t−a)+sigma(d+.4t−a).

Subtract this from C0's maximum J, using (7). The resulting support difference is strictly greater than

    F0=1−c−.4s+(kappa+sigma)(1−d)
                       +.4(kappa−sigma)t.             (9)

For fixed p, at q=p this is 2(1−c)≥0. Its exact derivative with respect to the ordinary angle q is

    dF0/dq=(kappa−sigma)(1−.6d)
                         +.6(kappa+sigma)t>0.         (10)

Every factor whose sign is used is positive by (5),(8). Therefore F0≥0 throughout q≥p, ruling out u.

In the u′ direction C0's maximum is

    U0(u′)=kappa J+sigma K.

Use (7) and subtract C1's minimum mathcal U, bounded by (6). The support difference is strictly greater than

    F1=1+kappa+sigma−d+.4t
                     −(kappa+sigma)c
                     −.4(kappa−sigma)s.              (11)

Again F1=2(1−c) at q=p, and its exact q derivative is

    dF1/dq=t+.4d+(kappa−sigma)(1−c)
                         +.4(kappa+sigma)s>0.         (12)

Thus F1≥0, ruling out u′ as well.

### 2.3. The order q≤p

Now sigma≤0. In the u direction C1's minimum is

    L1(u)=kappa mathcal U−sigma mathcal V
         ≤kappa(d−.4t−a)−sigma(−.26t−a).

Subtracting from J gives a support difference strictly greater than

    F2=1−c−.4s+kappa(1−d+.4t)
                           −sigma(1+.26t).            (13)

For fixed q, at p=q this equals 2(1−d). Its exact p derivative is

    dF2/dp=s−.4c+sigma(1−d+.4t)
                           +kappa(1+.26t).

Using (5),(8), we obtain the uniform rational lower bound

    dF2/dp≥24/25−2/5−(7/25)[1/25+(2/5)(7/25)]
           =1617/3125>0.                              (14)

Consequently F2≥0, and u cannot separate.

Finally, in the u′ direction C0's maximum is

    U0(u′)=kappa J+sigma V
         ≥kappa(a−c−.4s)+sigma[.35(c+s)−a],

where the last inequality uses sigma≤0 and the upper bound on V in (7). Subtracting mathcal U gives a support difference strictly greater than

    F3=1+kappa−sigma−d+.4t
                  −kappa c−.4kappa s+.35sigma(c+s).   (15)

At p=q this is 2(1−d). Its exact p derivative is

    dF3/dp=kappa[1−.75c+.65s]
                   +sigma[1−.65c−.75s].              (16)

The first bracket is at least 1/4. The second bracket is at most

    1−.65(24/25)=47/125.

If the second bracket is negative, its product with sigma is nonnegative; otherwise (8) applies directly. In either case

    dF3/dp≥(24/25)(1/4)−(7/25)(47/125)
           =421/3125>0.                              (17)

Thus F3≥0 and the last possible axis is impossible. The two orders include equality p=q, and the strict factor from a>1 handles the zero diagonal margin without any limiting argument. We have excluded every actual square normal in the genuine separator cone. Theorem 2 follows. ∎

## 3. Literal owner maps in the no-omission entrance

The physical quarter-turn is now R(x,y)=(4−y,x), about (2,2). It cycles Q4,Q5,Q6,Q7 and Q8,Q9,Q10,Q11 and preserves the complete no-omission MPPM entrance. The exact cover from Section 1 of C1092-MPPM-NO-OMISSION-REDUCTION.md is

| Actual central owner | Ordinary pair | Inward pair | Residual elbow pair | Points omitted in that elbow alternative |
|---|---|---|---|---|
| Q4 | F0,G0 | F4,G3 | F0,G3 | G0,F4 |
| Q5 | F6,G5 | F4,G6 | F4,G5 | F6,G6 |
| Q6 | F9,G9 | F5,G6 | F9,G6 | G9,F5 |
| Q7 | F3,G4 | F5,G3 | F5,G4 | F3,G3 |

The first two columns may overlap; they are a cover, not a disjoint assignment rule.

For the southwest elbow, translate by (−2,−2). Lemma 1's M,P,Q are the actual SW marker,F0,G3 in Q4. Its exclusions have the following literal sources:

| Local excluded point | Original point | Actual reason for exclusion from Q4 |
|---|---|---|
| N=(−.35,.35) | NW marker (1.65,2.35) | Strict in Q7 |
| G=(−1,−.4) | G0=(1,1.6) | Omitted in this exact elbow alternative |
| R0=(−1.086,0) | Left marker (.914,2) | Strict in Q8 |
| T=(0,−.26) | F4=(2,1.74) | Omitted in this exact elbow alternative |
| B=(−.4,−1) | F2=(1.6,1) | Strict in Q9 by the no-omission entrance |

Rotating this entire source table gives all other rows. Thus when consecutive actual central owners both have the residual elbow alternative, their genuine strict anchors and exclusions meet Theorem 2 exactly. In particular, an omitted auxiliary is used only as an exclusion from its own square; no foreign owner is invented for it. Each occurrence of B is instead a prescribed auxiliary of the corresponding actual boundary owner.

## 4. The strengthened structural conclusion

**Corollary 3.** In the entire original no-omission MPPM family, every actual central square that fails to own its ordinary pair has both cyclic neighbors owning their ordinary pairs. Hence at least two of the four central owners are ordinary. There are at most two nonordinary central owners; if there are two, they are opposite.

**Proof.** The retained covering theorem says a nonordinary central square has either the inward pair or the residual elbow alternative. The actual-neighbor implication (3) of C1092-MPPM-NO-OMISSION-REDUCTION.md and its rotations already prove that an inward owner has both neighbors ordinary.

Suppose instead that a residual elbow has a nonordinary neighbor. If that neighbor is inward, the same established implication would force the elbow to be ordinary, contrary to its explicit omission in the table above. Otherwise the neighbor is another residual elbow, which Theorem 2 excludes. Thus every nonordinary owner is isolated. On a four-cycle this gives the claimed count and placement. ∎

Up to simultaneous quarter-turn, the remaining type arrangements are therefore

    OOOO, OOOX, OXOY,

where O means the actual ordinary pair is owned and X,Y mean genuinely nonordinary owners, each with an inward or residual elbow alternative. An inward owner that also owns its ordinary pair is counted as O. These are structural alternatives, not a replacement enumeration of auxiliary labels.

## 5. A genuine ordinary wall advance available in the remaining types

Theorem 1 of C1092-MPPM-ORDINARY-CENTRAL-REDUCTION.md proves that F0 in Q4 excludes G3 from actual Q8. In the present no-omission entrance Q8 already owns its marker (.914,2) and G1=(1,2.4), while F0=(1,1.74) is strict in Q4. Apply the retained all-orientation ordinary wall-reach lemma in Section A.2 of C981-RETAINED-CONTINUOUS-LEMMAS.md to this actual Q8, with

    w=1.74, d0=1.74, z=2.56.

The two excluded points are F0 and G3. The latter is known to be absent from Q8, irrespective of whether another central owner has it. The numerical hypotheses are exactly

    .82<14/17, .74²+.26²=.6152<1,
    .56²+.74²=.8612<1.

The real left wall supplies the geometric wall hypothesis. Therefore (1,2.56) is strict in actual Q8. Simultaneous rotation gives the complete implication table:

| Strict central premise | Strict point forced in its actual adjacent boundary |
|---|---|
| F0 in Q4 | (1,2.56) in Q8 |
| G5 in Q5 | (1.44,1) in Q9 |
| F9 in Q6 | (3,1.44) in Q10 |
| G4 in Q7 | (2.56,3) in Q11 |

Each conclusion supplies the whole strict segment joining it to that boundary's already owned ordinary pair. In particular all four advances hold in the OOOO subbranch. They also hold individually in every mixed type where the stated central premise is present. No wall origin is inferred from these advances alone.

The remaining obligation is a continuous contradiction for the surviving actual cyclic types, with their actual boundaries and corners retained. The present chapter completes the adjacent-elbow exclusion and the nonordinary isolation theorem; it does not assume that the mixed types have the all-four-ordinary assignment.
