# A unit vertical span cannot fit between these two strict foreign bars

All terminating decimals are exact rationals. Strict ownership is retained, and excluded points may lie on a face. The theorem has no angle, wall, center or upper-side assumption.

**Theorem 1.** An open square B of side a>1 cannot strictly own both

    O=(0,0), P=(0,1)

while excluding the five points

    L_0=(−.26,.26), R_0=(.74,.26),
    L_1=(−.26,.39), R_1=(.74,.39),
    L_2=(−.26,.5).

**Proof.** Write U,V for the lower face values. Choose a canonical sign with absolute components c≥s≥0, c²+s²=1. We consider both whole signs.

First take the negative frame u=(c,−s), v=(s,c). The point L_0 has its upper u-band from strict O, since its u-projection is −.26(c+s)<0. Its lower v-band follows from O because .26(c−s)≥0, and its upper v-band follows from P. Hence its only possible exit is lower u:

    U≥−.26c−.26s.                                  (1)

The point R_0 has both lower bands from O, since .74c−.26s>0 and .74s+.26c>0. If it exited upper u, its opposite face with (1) would give a≤c≤1. It must therefore exit upper v:

    V+a≤.74s+.26c.

But P is strict, so c<V+a. Consequently .74c<.74s, contrary to c≥s. This excludes the entire negative canonical sign, including the axial and diagonal endpoints.

Now take the positive frame u=(c,s), v=(−s,c). The point L_1 has its upper u-band from P, lower v-band from O, and upper v-band from P. The corresponding positive projection gaps are

    u(P)−u(L_1)=.26c+.61s>0,
    v(L_1)=.26s+.39c>0,
    v(P)−v(L_1)=.61c−.26s>0.

Thus L_1 is lower u, so U≥−.26c+.39s. At R_1 the lower u-band follows from O and the upper v-band follows from P. An upper u exit would oppose L_1 with width a≤c≤1. Hence R_1 is lower v:

    V≥.39c−.74s.

Since O is strict, V<0. Thus

    s/c>39/74>13/25=.52,                            (2)

where the strict rational comparison is 39·25=975>962=13·74.

But the genuinely excluded L_2 now lies in all four strict bands. Both lower bands follow from O, since

    u(L_2)=−.26c+.5s>0,
    v(L_2)=.26s+.5c>0.

Both upper bands follow from P, since

    u(P)−u(L_2)=.26c+.5s>0,
    v(P)−v(L_2)=.5c−.26s≥.24c>0.

This is impossible. The two signs exhaust every square orientation. ∎

## C1092 MMMP: the northeast inner auxiliary is excluded

**Corollary 2.** In every original MMMP configuration, the actual northeast square Q6 excludes G6=(2.26,2). Its exact original label is therefore one of

    131200, 655488.

The core-owner theorem already proves G7=(2.26,3) strictly in Q6. Suppose G6 also belonged to this square, and translate the original coordinates by (−2.26,−2). They become the theorem's strict O,P. The complete source map for its exclusions is

| Local point | Original point | Actual strict owner |
|---|---|---|
| L_0 | (2,2.26)=F5 | Q7 by the core-owner theorem |
| R_0 | (3,2.26)=F9 | Q10 by the wall-sign chord |
| L_1 | (2,2.39) | Q7's strict segment from (2,2) to (2,2.5) |
| R_1 | (3,2.39) | Q10's strict wall-sign chord |
| L_2 | (2,2.5) | Q7 by the full-center crosspoint theorem |

Every source is an actual different original owner. In particular the Q7 center and crosspoint have already been proved for every MMMP auxiliary alternative; no northeast auxiliary choice was used in proving them. Theorem 1 contradicts the hypothetical G6 ownership.

The core-owner theorem leaves only 131200,196736,655488 for Q6. The middle label adds G6 to its compulsory F7,G7 pair, and has now been excluded. Hence the two displayed labels are the exact remaining alternatives. No angle or historical mask refinement is used.
